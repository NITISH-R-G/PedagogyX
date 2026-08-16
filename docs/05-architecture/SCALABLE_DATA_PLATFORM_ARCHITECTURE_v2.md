# Scalable Data Platform Architecture

**Status:** Proposed Architecture
**Role:** Autonomous Senior Data Engineer & Scalable Data Platform Architect

This document details the data engineering strategy, pipeline architecture, and warehouse design for the PedagogyX multimodal classroom intelligence platform. The system processes high-volume audio, video, and screen capture streams across a hybrid edge-cloud infrastructure to power AI-driven pedagogy analytics.

---

## Data Problem Analysis

PedagogyX ingests high-throughput multimodal data (audio, screen, and multiple camera feeds) from thin clients (Meta Ray-Ban Android devices and Windows smartboards).

### Business Requirements

- Capture and process teacher interactions, student engagement, and classroom activity to generate actionable pedagogy scores.
- Support both live supervision (hot path) and authoritative batch analytics (cold path).
- Strictly adhere to data residency laws (India cloud).

### Data Sources & Scale Assumptions

- Multi-stream A/V chunks (mic, screen, cam1, cam2) uploaded via WAN from Edge LAN buffers.
- Scale: Hundreds of simultaneous classrooms resulting in terabytes of daily raw video/audio.
- Eventual scale up to petabytes as historical sessions are retained for ML training.

### Freshness & SLA Requirements

- **Hot path**: ~5s rolling latency for live dashboards and supervision.
- **Cold path**: Batch processing SLA to deliver final authoritative scores within hours of session completion.

### Failure Scenarios

- Network partitions between Edge LAN and India Cloud.
- Out-of-order or dropped media chunks due to poor school connectivity.
- ASR/CV worker failures and GPU exhaustion.
- Schema drift from evolving thin client telemetry.

---

## Data Architecture

The architecture leverages a hybrid edge-cloud model optimized for resiliency and throughput, utilizing an entirely OSS-first stack.

- **Ingestion Systems**:
  - Edge nodes (school LAN) run an ingest buffer to mitigate WAN instability.
  - Data is synchronized and forwarded to a cloud-hosted MediaMTX gateway or WebRTC SFU.
- **Transformation Pipelines**:
  - Event-driven worker queues (Redis) decouple ingestion from heavy ML processing.
  - Python-based background workers pull A/V streams, align multi-modal events (A/V sync), and execute YOLO CV or Transformer-based ASR/diarization models.
- **Storage Systems**:
  - **Postgres**: Relational metadata, session states, and telemetry.
  - **MinIO**: Scalable object storage for raw streaming chunks, transcoded media, and extracted artifacts.
- **Orchestration Workflows**:
  - Event-driven orchestration with Redis streams for hot-path triggering.
  - Airflow or Dagster for cold-path batch scheduling, re-processing failed jobs, and managing complex ML pipelines.
- **Serving Layers**:
  - Live Analytics Bus (Kafka/Redis) for real-time dashboard subscriptions.
  - Fast API Gateway routing queries to Postgres or cached aggregations for historical score delivery.

---

## Pipeline Design

Pipelines are divided into dual paths to balance latency and reliability.

### ETL/ELT Workflows & Streaming Architecture

- **Real-Time (Hot) Pipeline**: Streaming WebRTC ingest → Edge Feature Workers → Live Analytics Bus. Workloads involve activity detection via lightweight models, talk-ratio estimation, stream health telemetry. Designed for "at-most-once" or "at-least-once" delivery where momentary data loss is acceptable in favor of low latency.
- **Batch (Cold) Pipeline**: Chunked upload → Object Archive (MinIO) → Transcode/Align → Heavy ML Fusion → Score Materialization.
- **Retries & Replayability**: Background workers must implement a Dead Letter Queue (DLQ) pattern. Failed processing (e.g., ASR exceptions) pushes raw payloads to a DLQ (`{JOB_QUEUE}:dlq`) and logs full tracebacks. All pipelines are designed to be entirely replayable from the raw MinIO storage.
- **Idempotency**: All job processing steps (transcode, save, metric update) must be idempotent to support safe replayability. Unique session and chunk identifiers are strictly enforced at the database level to prevent duplicate processing.
- **Synchronization**: Master clock relies on the audio sample clock, using cross-correlation to align video and screen OCR events.

---

## Storage & Warehouse Design

### Schema Strategy

- **OLTP**: Postgres handles session management, client registry, RBAC mapping, and queue state.
- **Data Lakehouse / OLAP**: Future analytics layers (e.g., ClickHouse or StarRocks) will model dimensional data (Star/Snowflake Schema) for cross-tenant school/district analytics.
- Data structures enforce strong validation for client-side schemas to prevent upstream silent corruption.

### Partitioning & Indexing

- **Postgres Partitioning**: Partitioning large metric tables by `session_date` or `tenant_id` to bound index sizes and scan times.
- **MinIO Partitioning**: Prefixing objects efficiently (`tenant_id/session_id/stream_type/timestamp.mp4`) to avoid hot spotting and enable rapid prefix scanning for batch processing.
- **Indexing**: Optimized B-Tree and Hash indexes on query patterns for dashboards.

### Optimization Strategy

- Offloading historical aggregations into materialized views or external OLAP systems.
- Data lifecycle policies to move cold video data to lower-tier storage within MinIO.

---

## Data Quality & Governance

### Validation & Lineage

- **Validation**: Pre-ingest validation of A/V chunks (format, length, metadata checks). Strict Pydantic-enforced schemas for API payloads.
- **Lineage**: End-to-end lineage tracking from raw chunk ID to the final pedagogy score generation batch run, allowing full tracing of AI score sources.

### Anomaly Detection & Governance Controls

- **Anomaly Detection**: Monitoring for sudden drops in audio volume, frame freezing, or incomplete session uploads.
- **Governance Controls**: Until G2 (India legal sign-off) is complete, all real student data ingest is restricted. The platform currently supports only synthetic test sessions and boilerplate benchmarks. Ownership is strictly assigned to tenant organizations.

---

## Observability

The platform requires deep visibility into both streaming health and batch ML reliability.

- **Monitoring & Logging**: Tracking queue depths, DLQ sizes, and job failure rates in real-time. Detailed traceback logging to `sys.stderr` for all DLQ events. Tracing cross-service correlation IDs. Hardware utilization (monitoring GPU memory saturation and edge buffer disk usage) is also closely tracked.
- **SLA Tracking**: Measuring chunk arrival to ASR output latency (hot path) and session completion to final score latency (cold path).
- **Diagnostics**: Specialized operational dashboards to pinpoint failures down to specific school Edge LAN buffers.

---

## Security & Compliance

- **Access Control**: RBAC enforces tenant isolation. Teachers access their own class previews; admins have aggregate and drill-down access. Least privilege access is enforced across all worker services.
- **Encryption**: TLS 1.3 for all WAN transport (Edge to Cloud). MinIO encryption at rest. Encrypted connections to Postgres.
- **Retention**: Lifecycle rules automatically prune or anonymize PII-heavy raw classroom recordings after 30 days unless explicitly saved for ML training dataset usage.
- **Governance**: Multi-tenant logical isolation in Postgres using Row-Level Security (RLS) or tenant ID filtering. Immutable audit logging of every stream view and score export.

---

## Performance Optimization

### Query & Compute Optimization

- Pass existing database context managers/cursors into helper functions in FastAPI and background workers to eliminate N+1 connection overhead.
- Offload compute-heavy alignments to GPU workers efficiently by batching concurrent video/audio chunks to maximize GPU utilization.
- Optimize query execution plans on Postgres utilizing partition pruning and efficient join algorithms.

### Caching & Scaling Strategy

- **Caching**: Implement Redis-based caching for frequent API aggregations and dashboard lookups to shield Postgres from high concurrent load.
- **Scaling Strategy**: Horizontally scale stateless worker pods processing Redis queues. Optimize Edge LAN buffers to batch compress chunks during periods of intermittent WAN connectivity.

---

## Risks & Tradeoffs

- **Operational Risks**: Network partitions between Edge and Cloud could result in delayed cold path processing or incomplete stream captures. Mitigated by robust edge buffering.
- **Scaling Concerns**: Heavy ML fusion could bottleneck on available GPU compute (RTX 5070 budget limitations).
- **Consistency Tradeoffs**: The hot path sacrifices strict exact-once processing in favor of at-most-once low latency processing, relying on the cold path to eventually reconcile state.
- **Cost Implications**: Retaining raw multi-stream video is incredibly expensive. We tradeoff storage cost vs ML dataset quality by aggressive downsampling or dropping video post-30-days, relying on metadata to train future models.

---

## Agile Sprint Plan

- **Sprint 1: Core Storage & Pipeline Foundation**
  - Implement Pydantic schema validation for stream metadata and ingestion API.
  - Setup MinIO prefix strategies and Postgres connection pooling optimizations.
  - Enforce standard DLQ patterns for all Redis background workers.
- **Sprint 2: Dual Hot/Cold Pipeline Implementation**
  - Establish the WebRTC ingest framework for the hot path.
  - Build idempotent chunk aggregation logic for the batch cold archive.
- **Sprint 3: Observability, Governance & Performance**
  - Deploy queue monitoring, latency SLA dashboards, and hardware monitoring.
  - Automate synthetic data generation tools to test A/V sync without violating G2 restrictions.
  - Document query patterns and partition strategies for the analytics warehouse.
  - Conduct load testing on the GPU background workers to fine-tune batching sizes.
