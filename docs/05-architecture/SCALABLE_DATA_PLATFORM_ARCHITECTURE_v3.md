# SCALABLE DATA PLATFORM ARCHITECTURE v3

**Status:** Strategic Data Architecture Evolution
**Role:** Autonomous Senior Data Engineer & Scalable Data Platform Architect

This document details the advanced data engineering strategy, scalable pipeline architecture, and robust warehouse design for the PedagogyX multimodal classroom intelligence platform. As a mission-critical system designed for high throughput, strict governance, and long-term sustainability, this architecture operates at the level of elite tech organizations (Netflix, Uber, Databricks).

## Data Problem Analysis

PedagogyX ingests high-throughput, multimodal data streams (audio, screen, and multiple camera feeds) from highly distributed edge locations (schools) running thin clients (Meta Ray-Ban Android devices, Windows smartboards).

### Business Requirements

- Extract actionable, objective pedagogy insights from massive volumes of classroom interactions.
- Provide a resilient, hybrid hot/cold path for both real-time operational supervision and authoritative historical analytics.
- Strictly adhere to localized data residency compliance (India Cloud) before processing.

### Scale Assumptions & Failure Scenarios

- **Throughput & Scale:** Designed to handle terabytes of daily raw data from hundreds of simultaneous classrooms, scaling elegantly to petabytes for historical machine learning datasets.
- **Failures:** Network partitions at the edge, dropped/delayed media chunks, out-of-order event delivery, and ASR/CV GPU resource exhaustion are all assumed norms, not exceptions.
- **Freshness SLA:** ~5s rolling latency for live dashboards (hot path) and daily batch SLA for authoritative pedagogical scoring (cold path).

## Data Architecture

The overarching system is a hybrid edge-to-cloud topology built entirely on open-source software (OSS) foundations, optimized for reliability and cost-efficiency.

- **Ingestion Layer:** Edge nodes operate local ingest buffers to absorb WAN instability. These synchronize with a robust WebRTC/MediaMTX gateway in the cloud.
- **Processing Layer:** Background, event-driven worker pods consume from durable queues. Python workers handle A/V sync, execute ML transformations (ASR, Diarization, CV), and materialize state.
- **Storage Layer:** MinIO provides scalable object storage for large media blobs. PostgreSQL manages relational session state, telemetry, and queue orchestration.
- **Serving Layer:** FastAPI routing, backed by Redis for high-concurrency read queries and live subscriptions (Kafka/Redis Live Analytics Bus).

## Pipeline Design

Pipelines are decoupled to isolate fast-path operational data from slow-path heavy ML transformations.

### Streaming (Hot) Pipeline

- **Architecture:** WebRTC event ingest to lightweight feature workers emitting to a Live Analytics Bus.
- **Design Principles:** At-least-once delivery for near real-time telemetry (talk ratios, volume drops), where slight data loss is acceptable for low-latency supervision.

### Batch (Cold) Pipeline

- **Architecture:** Chunked uploads to MinIO → Transcode & Align → Heavy ML Inference Fusion → Analytics Materialization.
- **Reliability:** Built strictly with retries, robust Dead Letter Queues (DLQ), and exactly-once processing guarantees where necessary.
- **Idempotency:** Every transformation step (e.g., audio alignment, metric generation) is strictly idempotent to allow safe replay of failed jobs without duplicating analytical outcomes.

## Storage & Warehouse Design

### Operational & Analytical Storage Strategy

- **OLTP / Metadata:** PostgreSQL houses the core operational registry (tenants, sessions, devices, RBAC).
- **Data Lake:** MinIO acts as the raw and curated data lake. Objects are carefully prefixed (`tenant_id/session_id/stream_type/timestamp`) to prevent hot spotting and optimize rapid prefix scans during batch processing.
- **Warehouse Modeling:** Future analytical workloads will utilize a dimensional star schema (e.g., ClickHouse integration) separating facts (pedagogy events) from dimensions (classes, teachers, time).

### Optimization Strategy

- Postgres tables containing high-velocity telemetry are partitioned by `session_date` or `tenant_id` to maintain efficient index sizes and rapid pruning.

## Data Quality & Governance

Data reliability is treated as a first-class citizen to prevent silent pipeline corruption.

- **Validation:** Strict, schema-on-write validation using Pydantic at the API boundary ensures only well-formed telemetry enters the platform.
- **Lineage:** Comprehensive end-to-end lineage tracking maps every final pedagogy score back to the specific raw media chunk and ML model version that produced it.
- **Anomaly Detection:** Automated checks monitor for sudden drops in audio volume, frame freezing, or incomplete upload sessions to alert operators before bad data pollutes the analytics.
- **Governance:** Strict adherence to the PedagogyX Phase 0 limitations: all real student data ingest is blocked pending G2 (India legal sign-off). Currently operating only on synthetic test data and benchmarks.

## Observability

Operational transparency is essential for distributed data systems.

- **Pipeline Monitoring:** Centralized metrics track Redis queue depths, DLQ accumulation rates, and worker failure rates in real-time.
- **Latency Tracking:** SLAs are continuously measured across both pipelines (chunk arrival to ASR output for hot path; session completion to final score for cold path).
- **Diagnostics:** Full tracebacks are logged to `sys.stderr` for all DLQ events, and distributed tracing correlation IDs track requests across the ingestion boundary to the worker layer.

## Security & Compliance

The platform enforces strict security boundaries to protect sensitive classroom intelligence.

- **Access Control:** Tenant-level isolation is enforced via RBAC. Row-Level Security (RLS) or logical application-tier filtering is applied in Postgres.
- **Encryption:** TLS 1.3 is mandated for all WAN transit. MinIO is configured for strict encryption at rest.
- **Data Handling:** The platform defaults to least privilege access, heavily scrutinizing the handling of any PII, with strong retention policies in place.

## Performance Optimization

Efficiency dictates the long-term sustainability of the platform.

- **Compute Optimization:** A/V chunks are aggressively batched for ML workers to maximize GPU utilization on constrained hardware (RTX 5070 consumer grade).
- **Query Optimization:** FastAPI and background workers utilize shared database connection pools via injected context managers, entirely eliminating N+1 connection overheads.
- **Scaling Strategy:** Workers horizontally auto-scale based on Redis queue depths, while edge buffers are optimized to batch-compress files locally during poor WAN connectivity.

## Risks & Tradeoffs

- **Network Volatility:** High reliance on under-resourced school network infrastructure. Mitigated by large edge-node disk buffers, but trades off real-time SLA guarantees for eventual consistency.
- **Storage Costs vs. ML Value:** Retaining terabytes of raw multimodal video is cost-prohibitive. Tradeoff: Aggressive lifecycle policies will downsample or purge raw video after 30 days, retaining only the extracted analytical metadata and audio transcripts.
- **Hardware Limitations:** Constrained by consumer-grade GPUs (RTX 5070 12GB). Tradeoff: We implement strict priority queuing (admin SLA over teacher preview) and aggressive batching over lower-latency processing.

## Agile Sprint Plan

- **Sprint 1: Core Reliability Foundations**
  - Implement and enforce strict Pydantic data contracts across all ingestion endpoints.
  - Standardize Dead Letter Queue (DLQ) patterns across all Redis-based background workers.
  - Establish PostgreSQL partitioning strategy for telemetry tables.
- **Sprint 2: Storage & Ingestion Optimization**
  - Finalize MinIO prefix routing to prevent object hot-spotting.
  - Deploy idempotent chunk aggregation logic for the batch processing pipeline.
  - Harden the edge-node offline buffering capabilities.
- **Sprint 3: Observability & Governance Activation**
  - Deploy operational dashboards for tracking pipeline latency, queue depths, and hardware utilization.
  - Automate synthetic data generation to rigorously test A/V synchronization and fault-recovery without violating G2 data residency holds.
  - Finalize the dimensional modeling strategy for future Data Warehouse (OLAP) integration.
