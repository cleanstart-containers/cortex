# Cortex – CleanStart Image

A production-grade, multi-tenant, horizontally scalable, long-term Prometheus metrics storage system — packaged in a simplified, ready-to-run container image by CleanStart. The CleanStart Cortex image provides a production-ready, security-hardened container optimized for enterprise environments. Built on a minimal base OS with comprehensive security hardening, this image delivers reliable application execution with advanced security features.

**📌 CleanStart Foundation:** Security-hardened, minimal base OS designed for enterprise containerized environments.

**Image Path:** `ghcr.io/cleanstart-containers/cortex`

**Image:** `ghcr.io/cleanstart-containers/cortex:latest-dev`

**Registry:** CleanStart Registry

---

## Overview

The CleanStart Cortex image provides a fully integrated, single-binary deployment of the Cortex project. It is designed for local clusters, development setups, automated testing, CI pipelines, and learning environments that need a complete Cortex stack without the operational overhead of multi-component deployments.

This image bundles all core Cortex services into one optimized container runtime and includes sensible defaults, pre-created storage directories, and runtime readiness optimizations. This Cortex container is part of the CleanStart application suite, featuring enterprise-grade security hardening, automated vulnerability management, and compliance with industry standards.

---

## About CleanStart

CleanStart is a comprehensive container registry providing security-hardened, enterprise-ready container images. Our images are designed with security-first principles, featuring minimal attack surfaces, regular security updates, and compliance with industry standards.

### About CleanStart Images

CleanStart images are built on secure, minimal base operating systems and optimized for production environments. Each image undergoes rigorous security testing, vulnerability scanning, and compliance validation to ensure enterprise-grade security and reliability.

---

## Key Features

- **Security-First Design**: Built with minimal attack surfaces and security hardening
- **Enterprise Compliance**: Meets industry standards including FIPS, STIG, and CIS benchmarks
- **Regular Updates**: Automated security patches and vulnerability management
- **Multi-Architecture Support**: Available for AMD64 and ARM64 architectures
- **Production Ready**: Optimized for enterprise deployment and scaling (`ghcr.io/cleanstart-containers/cortex:latest`)
- **Comprehensive Documentation**: Detailed guides and best practices for each image

---

## All-in-One Cortex Deployment

The image includes the full Cortex stack:

- **Distributor** - Receives metrics via remote write
- **Ingester** - Buffers, processes, and writes TSDB blocks
- **Querier** - Executes PromQL queries
- **Query-Frontend** - Adds caching, batching, and parallelization
- **Alertmanager** - Multi-tenant alerting management
- **Ruler** - Evaluates rules and alerts
- **Compactor** - Performs TSDB block compaction
- **Store-Gateway** - Loads and serves long-term storage blocks

All components run in a single binary while still exposing individual functionality through the standard Cortex APIs.

---

## Included Components

### Cortex Core Subsystems

| Subsystem | Description |
|-----------|-------------|
| **Distributor** | Receives metrics via remote write |
| **Ingester** | Buffers, processes, and writes TSDB blocks |
| **Querier** | Executes PromQL queries |
| **Query Frontend** | Adds caching, batching, and parallelization |
| **Alertmanager** | Multi-tenant alerting management |
| **Ruler** | Evaluates rules and alerts |
| **Compactor** | Performs TSDB block compaction |
| **Store Gateway** | Loads and serves long-term storage blocks |

---

## Health and Debug Endpoints

Exports built-in Cortex diagnostics:

- `/ready` – Readiness status
- `/services` – Running internal services overview
- `/config` – Live configuration dump
- `/metrics` – Prometheus metrics for the Cortex process
- `/ingester/ring` – Ring visualizer for ingesters

Useful for validation, monitoring, debugging, and load experimentation.

---

## Typical Use Cases

- Explore Cortex in a local cluster
- Build dashboards using long-term metrics storage
- Test Prometheus remote write integrations
- Run observability backends inside CI
- Validate multi-tenant behavior
- Develop exporter metrics and observe ingestion in real time
- Research distributed Prometheus storage models
- Local test clusters (dev image)
- Production deployments (`ghcr.io/cleanstart-containers/cortex:latest`)
- Ephemeral deployments
- Educational or POC environments
- Developer workflows that need a full metrics backend quickly

---

## CI/CD Friendly

Because it is:
- Single container
- Fast to pull
- Minimal configuration required

It fits perfectly into automated pipelines that need:
- Metrics ingestion tests
- API compliance checks
- Observability validation
- Development of Prometheus exporters

---

## CleanStart Enhancements

Compared to a raw upstream Cortex binary, this image includes:

- Cleaner directory creation logic
- Pre-baked configuration path layout
- Improved readiness gating
- Simplified startup behavior
- Dev-friendly startup messages
- More consistent port exposure

---

## Quick Start

### Pull Commands
```bash
docker pull ghcr.io/cleanstart-containers/cortex:latest
docker pull ghcr.io/cleanstart-containers/cortex:latest-dev
```

### Run Commands

Basic test:
```bash
docker run -it --name cortex-test ghcr.io/cleanstart-containers/cortex:latest-dev
```

Production deployment:
```bash
docker run -d --name cortex-prod \
  --read-only \
  --security-opt=no-new-privileges \
  --user 1000:1000 \
  ghcr.io/cleanstart-containers/cortex:latest
```

---

## Observability and Debugging

The image exposes Cortex's internal status endpoints for:

- Component health
- Build information
- Runtime metrics
- Configuration
- Storage and ingester ring conditions

This allows deep visibility into Cortex internals during development or testing.

---

## Architecture Support

CleanStart images support multiple architectures to ensure compatibility across different deployment environments:

- **AMD64**: Intel and AMD x86-64 processors
- **ARM64**: ARM-based processors including Apple Silicon and ARM servers

### Architecture-based Pull Commands
```bash
docker pull --platform linux/amd64 ghcr.io/cleanstart-containers/cortex:latest
docker pull --platform linux/arm64 ghcr.io/cleanstart-containers/cortex:latest
```

---

## Summary

The CleanStart Cortex dev Image offers a powerful, developer-friendly way to run the entire Cortex ecosystem in a single lightweight container — ideal for testing, learning, demos, local observability labs, and CI pipelines.

Once tested, prod image (`ghcr.io/cleanstart-containers/cortex:latest`) can be used for production environments.

You get:
- Full Cortex functionality
- Multi-tenancy and long-term storage
- Prometheus compatibility
- Built-in service diagnostics
- Zero-configuration bootstrap
- All bundled into one simple image

---

## Documentation Resources
Essential links and resources for further information
 
**CleanStart Images**: https://images.cleanstart.com/
 
**Community Images**:
**Docker Hub**: https://hub.docker.com/u/cleanstart<br>
**GitHub**: https://github.com/cleanstart-containers<br>
**AWS ECR Public Gallery**: https://gallery.ecr.aws/cleanstart/
 
**Presence on Social Media**:
**Community**: https://www.linkedin.com/groups/18324021/<br>
**YouTube**: https://www.youtube.com/@CleanStartOfficial<br>
 
**Contribute to Container Use Cases**: https://github.com/cleanstart-dev/cleanstart-use-cases/

## Vulnerability Disclaimer

CleanStart offers Docker images that include third-party open-source libraries and packages maintained by independent contributors. While CleanStart maintains these images and applies industry-standard security practices, it cannot guarantee the security or integrity of upstream components beyond its control.

Users acknowledge and agree that open-source software may contain undiscovered vulnerabilities or introduce new risks through updates. CleanStart shall not be liable for security issues originating from third-party libraries, including but not limited to zero-day exploits, supply chain attacks, or contributor-introduced risks.

**Security remains a shared responsibility:** CleanStart provides updated images and guidance where possible, while users are responsible for evaluating deployments and implementing appropriate controls.
