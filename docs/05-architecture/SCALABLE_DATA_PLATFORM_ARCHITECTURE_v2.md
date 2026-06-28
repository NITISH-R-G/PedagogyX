# Scalable Data Platform Architecture v2

**Status:** Proposed Architecture
**Role:** Autonomous Senior Data Engineer & Scalable Data Platform Architect

This document details the data engineering strategy, pipeline architecture, and warehouse design for the PedagogyX multimodal classroom intelligence platform. The system processes high-volume audio, video, and screen capture streams across a hybrid edge-cloud infrastructure to power AI-driven pedagogy analytics.

## Data Problem Analysis

PedagogyX ingests high-throughput multimodal data (audio, screen, and multiple camera feeds) from thin clients (Meta Ray-Ban Android devices and Windows smartboards).

### Business Requirements

- Capture and process teacher interactions, student engagement, and classroom activity to generate actionable pedagogy scores.
- Support both live supervision (hot path) and authoritative batch analytics (cold path).
- Strictly adhere to data residency laws (India cloud) requiring localized storage and processing.

### Data Sources & Scale Assumptions

- Multi-stream A/V chunks (mic, screen, cam1, cam2) uploaded via WAN from Edge LAN buffers.
- Target Scale: Hundreds of simultaneous classrooms resulting in terabytes of daily raw video/audio.
- Long-term Scale: Eventual scale up to petabytes as historical sessions are retained for ML model training and evaluation.

### Freshness & SLA Requirements

- **Hot path**: ~5s rolling latency for live dashboards and supervision.
- **Cold path**: Batch processing SLA to deliver final authoritative scores within hours of session completion.
- **Failure Scenarios**: Network partitions between Edge LAN and India Cloud; out-of-order or dropped media chunks due to poor school connectivity; ASR/CV worker failures and GPU exhaustion; schema drift from evolving thin client telemetry.

## Data Architecture

The architecture leverages a hybrid edge-cloud model optimized for resiliency and throughput, utilizing an entirely OSS-first stack.

### Ingestion Systems

- Edge nodes (school LAN) run an ingest buffer to mitigate WAN instability, ensuring local writes before asynchronous cloud sync.
- Data is synchronized and forwarded to a cloud-hosted MediaMTX gateway or WebRTC SFU for stream multiplexing.

### Transformation Pipelines

- Event-driven worker queues (Redis) decouple ingestion from heavy ML processing.
- Python-based background workers pull A/V streams, align multi-modal events (A/V sync), and execute YOLO CV or Transformer-based ASR/diarization models.

### Storage Systems

- **Postgres**: Relational metadata, session states, and telemetry.
- **MinIO**: Scalable object storage for raw streaming chunks, transcoded media, and extracted artifacts.

### Serving Layers

- Live Analytics Bus (Kafka/Redis) for real-time dashboard subscriptions.
- FastAPI Gateway routing queries to Postgres or cached aggregations for historical score delivery.

## Pipeline Design

Pipelines are divided into dual paths to balance latency and reliability.

### Real-Time (Hot) Pipeline

- **Architecture**: Streaming WebRTC ingest → Edge Feature Workers → Live Analytics Bus.
- **Workloads**: Activity detection via lightweight models, talk-ratio estimation, stream health telemetry.
- **Fault Tolerance**: Designed for "at-most-once" or "at-least-once" delivery where momentary data loss is acceptable in favor of low latency.

### Batch (Cold) Pipeline

- **Architecture**: Chunked upload → Object Archive (MinIO) → Transcode/Align → Heavy ML Fusion → Score Materialization.
- **Retries & Replayability**: Background workers must implement a Dead Letter Queue (DLQ) pattern. Failed processing (e.g., ASR exceptions) pushes raw payloads to a DLQ (`{JOB_QUEUE}:dlq`) and logs full tracebacks.
- **Idempotency**: All job processing steps (transcode, save, metric update) must be idempotent to support safe replayability.

## Storage & Warehouse Design

### Schema Strategy

- **OLTP**: Postgres handles session management, client registry, RBAC mapping, and queue state.
- **Data Lakehouse / OLAP**: Future analytics layers (e.g., ClickHouse or Apache Pinot) will model dimensional data (Star Schema) for cross-tenant school/district analytics.

### Partitioning & Indexing

- **Postgres**: Partitioning large metric tables by `session_date` or `tenant_id` to bound index sizes and scan times.
- **MinIO**: Prefixing objects efficiently (`tenant_id/session_id/stream_type/timestamp.mp4`) to avoid hot spotting and enable rapid prefix scanning for batch processing.

### Optimization Strategy

- Offload JSONB querying to application side where appropriate or utilize GIN indexes for deeply nested telemetry.

## Data Quality & Governance

### Validation & Lineage

- Pre-ingest validation of A/V chunks (format, length, metadata checks).
- End-to-end lineage tracking from raw chunk ID to the final pedagogy score generation batch run, ensuring auditable derivations.

### Anomaly Detection & Governance

- **Data Contracts**: Strict Pydantic-enforced schemas for API payloads to prevent silent corruption.
- **Anomaly Detection**: Monitoring for sudden drops in audio volume, frame freezing, or incomplete session uploads.
- **Governance Controls**: Until G2 (India legal sign-off) is complete, all real student data ingest is restricted. The platform currently supports only synthetic test sessions and boilerplate benchmarks.

## Observability

The platform requires deep visibility into both streaming health and batch ML reliability.

### Monitoring & Logging

- **Pipeline Monitoring**: Tracking queue depths, DLQ sizes, and job failure rates in real-time.
- **Latency & SLA Tracking**: Measuring chunk arrival to ASR output latency (hot path) and session completion to final score latency (cold path).
- **Diagnostics**: Detailed traceback logging to `sys.stderr` for all DLQ events. Tracing cross-service correlation IDs.
- **Infrastructure Health**: Monitoring GPU memory saturation, Redis memory consumption, and edge buffer disk usage.

## Security & Compliance

### Access Control & Encryption

- **Access Control**: RBAC enforces tenant isolation. Teachers access their own class previews; admins have aggregate and drill-down access.
- **Encryption**: TLS 1.3 for all WAN transport (Edge to Cloud). MinIO encryption at rest.

### Retention & Compliance

- **Data Isolation**: Multi-tenant logical isolation in Postgres using Row-Level Security (RLS) or tenant ID filtering.
- **Audit Logging**: Immutable logging of every stream view and score export to comply with data privacy audits.

## Performance Optimization

### Query & Compute Optimization

- Pass existing database context managers/cursors into helper functions in FastAPI and background workers to eliminate N+1 connection overhead.
- Offload compute-heavy alignments to GPU workers efficiently by batching concurrent video/audio chunks.

### Caching & Scaling Strategy

- Utilize Redis for caching frequently accessed aggregate statistics.
- Horizontally scale stateless worker pods processing Redis queues.
- Optimize Edge LAN buffers to batch compress chunks during periods of intermittent WAN connectivity.

## Risks & Tradeoffs

### Operational Risks & Scaling Concerns

- **Network Reliability**: High dependence on school WAN stability. Mitigated by robust edge buffering, but risks delayed cold path processing.
- **Storage Costs**: Retaining raw multi-stream video is expensive. Tradeoff: Implement aggressive lifecycle policies to downsample or delete raw video after 30 days while retaining metadata and audio transcripts.

### Consistency Tradeoffs

- **Processing Bottlenecks**: Heavy ML fusion could bottleneck on available GPU compute (RTX 5070 budget limitations). Mitigation involves priority queuing where admin-level SLA sessions are processed before teacher previews.

## Agile Sprint Plan

### Milestones & Implementation Phases

- **Sprint 1: Core Storage & DLQ Foundation**
  - Implement Pydantic schema validation for stream metadata.
  - Setup MinIO prefix strategies and Postgres connection pooling optimizations.
  - Enforce standard DLQ patterns for all Redis background workers.
- **Sprint 2: Hot/Cold Pipeline Divergence**
  - Establish the WebRTC ingest framework for the hot path.
  - Build idempotent chunk aggregation logic for the batch cold archive.
- **Sprint 3: Observability & Governance**
  - Deploy queue monitoring and latency SLA dashboards.
  - Automate synthetic data generation tools to test A/V sync without violating G2 restrictions.
  - Document query patterns and partition strategies for the analytics warehouse.
