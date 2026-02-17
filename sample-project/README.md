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
├── docker-compose.yml      # Cortex + Prometheus + metrics server
├── prometheus-docker.yml   # Prometheus config (scrape metrics, remote_write to Cortex)
├── serve_metrics.py        # Serves test-metric.txt for Prometheus scrape
├── test-metric.txt         # Sample metric (exposition format)
└── README.md               # This file
```

## Run with Docker Compose

From the project directory:

### 1. Start all services
```bash
docker compose up -d --build
```

Cortex, the metrics server, and Prometheus start. Prometheus scrapes the metrics server. (Remote write to Cortex is disabled due to a compatibility issue between the Cortex base image and Prometheus’s remote-write format.)

### 2. Verify Cortex is ready
```bash
curl http://localhost:9009/ready
```
**Expected:** `ready`

### 3. Check container status and logs
```bash
docker compose ps
docker compose logs cortex
```

### 4. Check running services
```bash
curl http://localhost:9009/services
```
**Expected:** HTML listing alertmanager, compactor, distributor, ingester, querier, query-frontend, ruler, store-gateway.

### 5. Check build information
```bash
curl http://localhost:9009/metrics | grep cortex_build_info
```

### 6. Check ingester ring
```bash
curl http://localhost:9009/ingester/ring
```
**Expected:** HTML with instance state (e.g. ACTIVE).

### 7. Check configuration
```bash
curl http://localhost:9009/config | head -30
```

### 8. Verify storage directories
```bash
docker compose exec cortex ls -la /tmp/ | grep cortex
```
**Expected:** cortex-alertmanager, cortex-compactor, cortex-data, cortex-rules, cortex-sync, cortex-tsdb.

### 9. Query Cortex (Prometheus API)
```bash
curl -G 'http://localhost:9009/prometheus/api/v1/query' \
  -H "X-Scope-OrgID: demo" \
  --data-urlencode 'query=up'
```
**Expected:** Valid JSON. With remote write disabled, Cortex stays up; Prometheus UI is at http://localhost:9093.

### 10. List available metric names
```bash
curl -H "X-Scope-OrgID: demo" \
  http://localhost:9009/prometheus/api/v1/label/__name__/values
```

### 11. Access interactive shell
```bash
docker compose exec cortex sh
```
Inside the container:
```bash
ps aux | grep cortex
ls -la /tmp/cortex-*
cat /etc/cortex/config.yaml
exit
```

### 12. Monitor container resources
```bash
docker compose stats --no-stream
```

### 13. View real-time logs
```bash
docker compose logs -f cortex
```

### 14. Cleanup
```bash
docker compose down
```
