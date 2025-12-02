# Cortex Deployment on Kind Cluster

## Overview

This guide provides step-by-step instructions to deploy Cortex on a local Kind (Kubernetes in Docker) cluster using the `cleanstart/cortex:latest-dev` image.

## What is Cortex?

Cortex provides:
- **Long-term metric storage** - Store Prometheus metrics for extended periods
- **Multi-tenancy** - Support multiple isolated tenants
- **Horizontal scalability** - Scale components independently
- **High availability** - Built-in replication and fault tolerance
- **Prometheus compatibility** - Compatible with Prometheus remote write/read APIs

## Prerequisites

- Docker installed and running
- Kind installed
- kubectl installed
- Basic understanding of Kubernetes

### Step 1: Deploy Cortex to Kubernetes
```bash
# Apply the deployment manifest
kubectl apply -f deployment.yaml
```

**Expected Output:**
```
namespace/cortex created
configmap/cortex-config created
persistentvolumeclaim/cortex-storage created
deployment.apps/cortex created
service/cortex-service created
service/cortex-nodeport created
```

### Step 2: Watch Pod Startup
```bash
# Watch pod status (this may take 30-60 seconds)
kubectl get pods -n cortex -w
```

**Expected Output:**
```
NAME                      READY   STATUS     RESTARTS   AGE
cortex-xxxxxxxxxxxxxxx    1/1     Running    0          45s
```

### Step 3: Verify All Resources are Created
```bash
# Check all resources in cortex namespace
kubectl get all -n cortex
```

**Expected Output:**
```
NAME                         READY   STATUS    RESTARTS   AGE
pod/cortex-bc9577c7f-27dv6   1/1     Running   0          1m

NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                         AGE
service/cortex-service    ClusterIP   10.96.92.246    <none>        9009/TCP,9095/TCP               1m
service/cortex-nodeport   NodePort    10.96.151.235   <none>        9009:30009/TCP,9095:30095/TCP   1m

NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/cortex   1/1     1            1           1m

NAME                                DESIRED   CURRENT   READY   AGE
replicaset.apps/cortex-bc9577c7f    1         1         1       1m
```

### Step 4: Check Pod Logs
```bash
# View pod logs to verify Cortex started successfully
kubectl logs -n cortex -l app=cortex --tail=50
```

**Expected Output (Success Indicators):**
```
ts=2025-11-28T... msg="Starting Cortex" version="(version=1.20.0...)"
ts=2025-11-28T... msg="server listening on addresses" http=[::]:9009 grpc=[::]:9095
ts=2025-11-28T... msg="Cortex started"
ts=2025-11-28T... msg="gossip settled; proceeding"
```

### Step 5: Verify Init Container Created Directories
```bash
# Check that init container created storage directories
kubectl logs -n cortex -l app=cortex -c init-dirs
```

**Expected Output:**
```
drwxrwxrwx    2 root     root          4096 ... cortex-alertmanager
drwxrwxrwx    2 root     root          4096 ... cortex-compactor
drwxrwxrwx    2 root     root          4096 ... cortex-data
drwxrwxrwx    2 root     root          4096 ... cortex-rules
drwxrwxrwx    2 root     root          4096 ... cortex-sync
drwxrwxrwx    2 root     root          4096 ... cortex-tsdb
```

### Step 6: Wait for Pod to be Ready
```bash
# Wait for pod to pass health checks (may take 30-45 seconds)
kubectl wait --for=condition=ready pod -l app=cortex -n cortex
```

**Expected Output:**
```
pod/cortex-bc9577c7f-27dv6 condition met
```

## Accessing Cortex

### Method 1: Port Forward (Recommended)

This is the most reliable method that works on any cluster:
```bash
# Start port forward (use available port - 9010, 8009, etc.)
kubectl port-forward -n cortex svc/cortex-service 9010:9009 &

# Wait a moment for port forward to establish
sleep 2

# Test health endpoint
curl http://localhost:9010/ready
```

**Expected Output:**
```
ready
```

**Note**: If you get "address already in use" error, another process is using port 9010. Try a different port:
```bash
# Find what's using the port
sudo lsof -i :9010

# Use a different port
kubectl port-forward -n cortex svc/cortex-service 8009:9009 &
curl http://localhost:8009/ready
```

### Method 2: From Inside Cluster
```bash
# Create test pod
kubectl run test-curl --rm -it --image=curlimages/curl -- sh

# Inside the pod, test endpoints:
curl http://cortex-service.cortex.svc.cluster.local:9009/ready
curl http://cortex-service.cortex.svc.cluster.local:9009/services
curl -H "X-Scope-OrgID: demo"  http://cortex-service.cortex.svc.cluster.local:9009/prometheus/api/v1/label/__name__/values

# Exit when done
exit
```

### Method 3: Via Kind Node (NodePort)

If you created cluster with port mappings:
```bash
# Access directly from Kind node
docker exec -it kind-control-plane curl http://localhost:30009/ready
```

**Expected Output:**
```
ready
```

## Testing Cortex Endpoints

### Using Port Forward (Replace 9010 with your port)
```bash
# Set your port
PORT=9010

# Health check
curl http://localhost:$PORT/ready

# Services status
curl http://localhost:$PORT/services

# Build information
curl -s http://localhost:$PORT/metrics | grep cortex_build_info

# Query API (with tenant header)
curl -H "X-Scope-OrgID: demo" \
  http://localhost:$PORT/prometheus/api/v1/label/__name__/values

# Ingester ring status
curl http://localhost:$PORT/ingester/ring

# Alertmanager status
curl -H "X-Scope-OrgID: demo" \
  http://localhost:$PORT/alertmanager/api/v2/status
```

### Expected Responses

**Health Check:**
```
ready
```

**Build Info:**
```
cortex_build_info{branch="master",goarch="amd64",goos="linux",
goversion="go1.25.4",revision="b72a536fe...",version="1.20.0"} 1
```

**Services Status (HTML page showing):**
- alertmanager - Running
- compactor - Running
- distributor-service - Running
- grpcclient-service - Running
- ingester-service - Running
- memberlist-kv - Running
- querier - Running
- query-frontend - Running
- query-frontend-tripperware - Running
- ring - Running
- ruler - Running
- server - Running
- store-gateway - Running
- store-queryable - Running

**Query API (initially empty):**
```json
{"status":"success","data":[]}
```

### Step 7: Check Storage and Volumes
```bash
# Check PVC status
kubectl get pvc -n cortex

# Describe PVC
kubectl describe pvc cortex-storage -n cortex

# Check directories inside pod
kubectl exec -n cortex -l app=cortex -- ls -la /data
```

**Expected Output:**
```
NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES
cortex-storage   Bound    pvc-abc123...                             10Gi       RWO

drwxrwxrwx    2 root     root          4096 ... cortex-alertmanager
drwxrwxrwx    2 root     root          4096 ... cortex-compactor
drwxrwxrwx    2 root     root          4096 ... cortex-data
drwxrwxrwx    2 root     root          4096 ... cortex-rules
drwxrwxrwx    2 root     root          4096 ... cortex-sync
drwxrwxrwx    2 root     root          4096 ... cortex-tsdb
```

### Step 8: Execute Commands Inside Pod
```bash
# Get shell access to pod
kubectl exec -n cortex -it $(kubectl get pod -n cortex -l app=cortex -o jsonpath='{.items[0].metadata.name}') -- sh

# Inside pod, run:
ps aux | grep cortex
ls -la /data
cat /etc/cortex/config.yaml
whoami
exit
```

### Step 9: Check Resource Usage
```bash
# Get pod resource usage
kubectl top pod -n cortex

# Describe pod to see resource limits
kubectl describe pod -n cortex -l app=cortex | grep -A 5 "Limits:\|Requests:"
```

**Expected Output:**
```bash
NAME                      CPU(cores)   MEMORY(bytes)
cortex-bc9577c7f-27dv6   50m          250Mi

Limits:
  cpu:     1
  memory:  1Gi
Requests:
  cpu:        250m
  memory:     256Mi
```

## Testing with Prometheus

Deploy Prometheus to send metrics to Cortex:
```bash
# Deploy Prometheus
kubectl apply -f prometheus-deployment.yaml

# Wait for Prometheus to be ready
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring
```

### Verify Prometheus is Sending to Cortex
```bash
# Check Prometheus logs
kubectl logs -n monitoring -l app=prometheus | tail -20

# After 1-2 minutes, query metrics in Cortex
curl -G -H "X-Scope-OrgID: demo" \
  'http://localhost:9010/prometheus/api/v1/query' \
  --data-urlencode 'query=up'
```

**Expected Output (after metrics are ingested):**
```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "job": "prometheus",
          "instance": "localhost:9090"
        },
        "value": [1732794000, "1"]
      }
    ]
  }
}
```

### Query Metrics from Cortex
```bash
# List all available metrics
curl -H "X-Scope-OrgID: demo" \
  http://localhost:9010/prometheus/api/v1/label/__name__/values

# Query specific metric
curl -G -H "X-Scope-OrgID: demo" \
  'http://localhost:9010/prometheus/api/v1/query' \
  --data-urlencode 'query=prometheus_build_info'

# Range query
curl -G -H "X-Scope-OrgID: demo" \
  'http://localhost:9010/prometheus/api/v1/query_range' \
  --data-urlencode 'query=up' \
  --data-urlencode 'start=2025-11-28T00:00:00Z' \
  --data-urlencode 'end=2025-11-28T23:59:59Z' \
  --data-urlencode 'step=15s'
```

## Cleanup

### Delete Cortex Deployment Only
```bash
# Delete all Cortex resources
kubectl delete -f deployment.yaml

# Verify deletion
kubectl get all -n cortex
```

### Delete Prometheus (if deployed)
```bash
kubectl delete -f prometheus-deployment.yaml
```
