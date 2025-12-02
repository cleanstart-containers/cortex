Cortex – CleanStart Image (cleanstart/cortex:latest-dev)

A production-grade, multi-tenant, horizontally scalable, long-term Prometheus metrics storage system — packaged in a simplified, ready-to-run container image by CleanStart.

Overview

The CleanStart Cortex image provides a fully integrated, single-binary deployment of the Cortex project. It is designed for local clusters, development setups, automated testing, CI pipelines, and learning environments that need a complete Cortex stack without the operational overhead of multi-component deployments.

This image bundles all core Cortex services into one optimized container runtime and includes sensible defaults, pre-created storage directories, and runtime readiness optimizations.

Key Features
 All-in-One Cortex Deployment

The image includes the full Cortex stack:
```bash
Distributor

Ingester

Querier

Query-Frontend

Alertmanager

Ruler

Compactor

Store-Gateway
```
All components run in a single binary while still exposing individual functionality through the standard Cortex APIs.

**Health and Debug Endpoints:**

Exports built-in Cortex diagnostics:

/ready – readiness status

/services – running internal services overview

/config – live configuration dump

/metrics – Prometheus metrics for the Cortex process

/ingester/ring – ring visualizer for ingesters

Useful for validation, monitoring, debugging, and load experimentation.

**The image is lightweight and pre-configured for:**

Local test clusters (prod image(cleanstart/cortex:latest) can be used for prod use case)

Ephemeral deployments

Educational or POC environments

Developer workflows that need a full metrics backend quickly

**CI/CD Friendly:**

Because it is:

Single container

Fast to pull

**Minimal configuration required**
It fits perfectly into automated pipelines that need:

Metrics ingestion tests

API compliance checks

Observability validation

Development of Prometheus exporters

**CleanStart Enhancements:**

Compared to a raw upstream Cortex binary, this image includes:

Cleaner directory creation logic

Pre-baked configuration path layout

Improved readiness gating

Simplified startup behavior

Dev-friendly startup messages

More consistent port exposure

**Typical Use Cases:**

Explore Cortex in a local cluster

Build dashboards using long-term metrics storage

Test Prometheus remote write integrations

Run observability backends inside CI

Validate multi-tenant behavior

Develop exporter metrics and observe ingestion in real time

Research distributed Prometheus storage models

**Included Components:**
Cortex Core Subsystems
Subsystem	Description
Distributor	Receives metrics via remote write
Ingester	Buffers, processes, and writes TSDB blocks
Querier	Executes PromQL queries
Query Frontend	Adds caching, batching, and parallelization
Alertmanager	Multi-tenant alerting management
Ruler	Evaluates rules and alerts
Compactor	Performs TSDB block compaction
Store Gateway	Loads and serves long-term storage blocks

**Observability and Debugging:**

The image exposes Cortex’s internal status endpoints for:

Component health

Build information

Runtime metrics

Configuration

Storage and ingester ring conditions

This allows deep visibility into Cortex internals during development or testing.

**Summary:**

The CleanStart Cortex dev Image offers a powerful, developer-friendly way to run the entire Cortex ecosystem in a single lightweight container — ideal for testing, learning, demos, local observability labs, and CI pipelines.
Once tested, prod image can be used for production environments.

You get:

Full Cortex functionality

Multi-tenancy and long-term storage

Prometheus compatibility

Built-in service diagnostics

Zero-configuration bootstrap

All bundled into one simple image.