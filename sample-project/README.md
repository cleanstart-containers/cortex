# CleanStart Cortex Sample Project

## Overview

This project demonstrates the **cleanstart/cortex:latest-dev** image - a horizontally scalable, highly available, multi-tenant, long-term Prometheus storage system.

## What is Cortex?

Cortex provides:
- **Long-term metric storage** - Store Prometheus metrics for extended periods
- **Multi-tenancy** - Support multiple isolated tenants
- **Horizontal scalability** - Scale components independently
- **High availability** - Built-in replication and fault tolerance
- **Prometheus compatibility** - Compatible with Prometheus remote write/read APIs

## Project Structure
```
cortex-sample-project/
├── Dockerfile              # Custom Cortex image with configuration
├── cortex-config.yaml      # Cortex configuration file
└── README.md              # This file
```

## Testing Steps

### Step 1: Build Docker Image
```bash
docker build -t cortex-simple:v1 .
```

**Expected Output:**
```
[+] Building 1.4s (8/8) FINISHED
 => [3/3] COPY cortex-config.yaml /etc/cortex/config.yaml
 => exporting to image
 => => naming to docker.io/library/cortex-simple:v1
```

### Step 2: Run Cortex Container
```bash
docker run -d \
  --name cortex-simple \
  -p 9009:9009 \
  -p 9095:9095 \
  cortex-simple:v1
```

**Expected Output:**
```
<container_id>
```

### Step 3: Verify Container is Running
```bash
docker ps | grep cortex-simple
```

**Expected Output:**
```
CONTAINER ID   IMAGE              PORTS                                              STATUS
<id>           cortex-simple:v1   0.0.0.0:9009->9009/tcp, 0.0.0.0:9095->9095/tcp    Up X seconds
```

### Step 4: Check Container Logs
```bash
docker logs cortex-simple
```

**Expected Output (Success Indicators):**
```
ts=... msg="Starting Cortex" version="(version=1.20.0...)"
ts=... msg="server listening on addresses" http=[::]:9009 grpc=[::]:9095
ts=... msg="Cortex started"
ts=... msg="gossip settled; proceeding"
```

### Step 5: Health Check
```bash
curl http://localhost:9009/ready
```

**Expected Output:**
```
ready
```

### Step 6: Check Running Services
```bash
curl http://localhost:9009/services
```

**Expected Output (HTML page showing):**
```
Service                      | Status
-----------------------------|--------
alertmanager                 | Running
compactor                    | Running
distributor-service          | Running
ingester-service             | Running
querier                      | Running
query-frontend               | Running
ruler                        | Running
store-gateway                | Running
```

### Step 7: Check Build Information
```bash
curl http://localhost:9009/metrics | grep cortex_build_info
```

**Expected Output:**
```
cortex_build_info{branch="master",goarch="amd64",goos="linux",
goversion="go1.25.4",revision="b72a536fe...",version="1.20.0"} 1
```

### Step 8: Check Ingester Ring
```bash
curl http://localhost:9009/ingester/ring
```

**Expected Output (HTML page showing):**
```
Instance ID    | State  | Address        | Tokens
---------------|--------|----------------|-------
<container_id> | ACTIVE | 172.17.0.2:9095| 128
```

### Step 9: Check Configuration
```bash
curl http://localhost:9009/config | head -30
```

**Expected Output:**
```
target: all
auth_enabled: true
server:
  http_listen_port: 9009
  grpc_listen_port: 9095
...
```

### Step 10: Verify Storage Directories
```bash
docker exec cortex-simple ls -la /tmp/ | grep cortex
```

**Expected Output:**
```
drwxr-xr-x    2 root     root          4096 ... cortex-alertmanager
drwxr-xr-x    2 root     root          4096 ... cortex-compactor
drwxr-xr-x    2 root     root          4096 ... cortex-data
drwxr-xr-x    2 root     root          4096 ... cortex-rules
drwxr-xr-x    2 root     root          4096 ... cortex-sync
drwxr-xr-x    2 root     root          4096 ... cortex-tsdb
```

### Step 11: Test Prometheus Remote Write API

Create a test metric file:
```bash
cat > test-metric.txt << 'METRIC'
# TYPE test_metric counter
test_metric{job="test",instance="local"} 42
METRIC
```

Push the metric to Cortex:
```bash
curl -X POST \
  -H "Content-Type: text/plain" \
  -H "X-Scope-OrgID: demo" \
  --data-binary @test-metric.txt \
  http://localhost:9009/api/v1/push
```

**Expected Output:**
```
(Empty response with HTTP 200 or 204)
```

### Step 12: Query the Pushed Metric

Wait a few seconds, then query:
```bash
curl -G 'http://localhost:9009/prometheus/api/v1/query' \
  -H "X-Scope-OrgID: demo" \
  --data-urlencode 'query=test_metric'
```

**Expected Output:**
```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "instance": "local",
          "job": "test"
        },
        "value": [<timestamp>, "42"]
      }
    ]
  }
}
```

### Step 13: List Available Metrics
```bash
curl -H "X-Scope-OrgID: demo" \
  http://localhost:9009/prometheus/api/v1/label/__name__/values
```

**Expected Output:**
```json
{
  "status": "success",
  "data": ["test_metric"]
}
```

### Step 14: Access Interactive Shell
```bash
docker exec -it cortex-simple sh
```

Inside the container:
```bash
# Check running process
ps aux | grep cortex

# Check storage directories
ls -la /tmp/cortex-*

# Check configuration
cat /etc/cortex/config.yaml

# Exit
exit
```

### Step 15: Monitor Container Resources
```bash
docker stats cortex-simple --no-stream
```

**Expected Output:**
```
CONTAINER ID   NAME           CPU %   MEM USAGE / LIMIT   NET I/O
<id>           cortex-simple  X%      XXXMiB / XXXGiB     XXkB / XXkB
```

### Step 16: View Real-time Logs
```bash
docker logs -f cortex-simple
```

## Cleanup
```bash
# Stop the container
docker stop cortex-simple

# Remove the container
docker rm cortex-simple

# Remove the image (optional)
docker rmi cortex-simple:v1

# Remove test files
rm test-metric.txt
```
