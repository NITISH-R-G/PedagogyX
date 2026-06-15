# Scalable Data Platform Architecture Report (v3)

## Data Problem Analysis

- **Business requirements**: To capture, orchestrate, and analyze multimodal classroom data (audio, vision, device state) from Meta Ray-Ban smart glasses (primary DAT client) in order to generate pedagogy metrics (e.g., talk-ratios, behavioral insights).
- **Data sources**: High-volume streaming AV inputs from Edge/Android clients, alongside structured lifecycle telemetry, captured across unreliable LAN/WAN infrastructure in schools.
- **Scale assumptions**: System must horizontally scale to ingest from hundreds to thousands of concurrent classrooms generating hundreds of gigabytes per session, scaling efficiently while remaining within strict consumer hardware constraints (RTX 5070 / 12GB VRAM limits per processing node).
- **Freshness requirements**: Dual-track freshness SLA; a hot-path for streaming real-time operational telemetry (sub-second to 5 seconds), and a batch-path for heavy-duty metric materialization and ML model generation (minutes to hours).
- **Failure scenarios**: The architecture expects delayed events, out-of-order chunks due to edge device disconnects, missing frames, chunk upload failures, worker crashes on OOM, and schema drift.

## Data Architecture

- **Ingestion systems**: Edge-node client buffers write to scalable FastAPI endpoints which proxy chunks into MinIO object storage. Redis serves as an event ingestion bus for high-velocity telemetry and session state tracking.
- **Transformation pipelines**: Decoupled, asynchronous Python background workers (e.g., `worker-asr`, `worker-metrics`, `worker-cv`) triggered via Redis queues (e.g., `jobs:asr`, `jobs:talk_ratio`).
- **Storage systems**: MinIO for raw, immutable multimodal object storage (AV chunks). PostgreSQL serves as the canonical relational store for normalized data (e.g., `sessions`, `dat_sessions`, `session_metrics`). Redis for queuing and ephemeral state.
- **Orchestration workflows**: Lightweight queue-based choreography (Celery-style custom Redis processors) where jobs publish events down the pipeline (e.g., `asr` triggers `talk_ratio` metrics).
- **Serving layers**: Next.js 15 and React 19 frontends served through FastAPI aggregators. High-throughput operational queries read directly from tuned Postgres views and Redis caches.

## Pipeline Design

- **ETL/ELT workflows**: ELT pattern where raw chunks are first secured in MinIO. Workers pull object references, execute compute-heavy models (e.g., Whisper, YOLO), and load structured telemetry back into Postgres (`session_transcripts`, `session_metrics`).
- **Streaming architecture**: Event-driven architecture using Redis `blpop` consumers for robust task distribution and decoupled microservices.
- **Retries**: Configurable poll timeouts and error catching mechanisms in workers that aggressively shunt failures to explicit Dead Letter Queues (`JOB_QUEUE:dlq`).
- **Replayability**: Raw AV chunks and telemetry are persistently stored before processing, enabling full historical replay through the model pipelines if logic is updated or workers fail.
- **Idempotency**: Workers use `ON CONFLICT DO UPDATE` (upsert patterns in PostgreSQL) to safely handle duplicate job dispatches and ensure idempotent metric materialization.

## Storage & Warehouse Design

- **Schema strategy**: Highly normalized OLTP schemas mapped strictly via `Pydantic` and `psycopg2` direct queries for high throughput. Specialized tables separate DAT lifecycle telemetry from pure pedagogy metadata.
- **Partitioning**: Logical partitioning by `school_id` and `session_id` using composite indices (e.g., `idx_sessions_school_created`) designed for multitenant isolation and rapid tenant-scoped queries.
- **Indexing**: Extensive use of index clustering on critical join paths (`session_id`), covering indices on status checks, and UUID primary keys for global uniqueness.
- **Optimization strategy**: Pushdown computation using JSONB fields for sparse segments (`segments_json`), avoiding heavy JOINs for time-series extraction while minimizing N+1 connection overhead using connection pooling.

## Data Quality & Governance

- **Validation**: Strict schema validation using Pydantic models at the API ingestion layer prevents silent data corruption or malformed payloads from polluting downstream workers.
- **Lineage**: Clear traceability from raw `session_chunks` through `session_transcripts` and ultimately `session_metrics`, bound consistently by a single `session_id` UUID trace key.
- **Anomaly detection**: Metrics latency and confidence intervals (`metric_confidence`) are tracked at the database layer (e.g., `preview_heuristic` vs `preview_stub`).
- **Governance controls**: Production PII is strictly gated. Full compliance with DPDP limits real user data processing until G2 sign-off. RBAC mapping isolates data strictly by tenant (School/Teacher).

## Observability

- **Monitoring**: Real-time queue depth and DLQ monitoring via Redis. Database-level timing tracking for latency (e.g., `insight_latency_sec` on `session_metrics`).
- **Logging**: Standardized `stdout`/`stderr` logging with explicit tracking of session IDs, worker metrics (teacher-talk ratios, confidence scores), and complete tracebacks for job failures.
- **SLA tracking**: SLA metrics are explicitly recorded in Postgres per-session (`completed_at`, `preview_ready_at`, `insight_latency_sec`), allowing for robust operational dashboarding.
- **Diagnostics**: Healthcheck endpoints across the API layer, and transparent queue tracking allow operators to quickly diagnose stalled sessions or OOM-killed workers.

## Security & Compliance

- **Access control**: Tenant isolation at the API level (School/Teacher ID) prevents lateral data exposure. Strict enforcement of least-privilege principles.
- **Encryption**: TLS in transit. At-rest encryption via MinIO internal mechanisms and PostgreSQL volume encryption. Secrets passed via secure environment injection.
- **Retention**: Transient storage architecture allows for aggressive TTL on `session_chunks` while preserving lightweight `session_metrics` long-term for dashboard historical analysis.
- **Governance**: Synthetic data only until G2 regulatory approval. System architecture guarantees complete offline, self-hosted deployment capability to maintain absolute data residency.

## Performance Optimization

- **Query optimization**: Denormalized analytics roll-ups where necessary (e.g., pre-aggregated `school_overview`). Avoiding implicit transactions where possible.
- **Compute optimization**: Right-sizing model execution for consumer hardware. Avoiding bloated ORMs in worker layers; utilizing raw SQL `psycopg2` cursors for maximum throughput and minimal memory overhead.
- **Caching**: Future implementation points toward using Redis not just for queues, but for caching high-read operational views (e.g., school dashboards).
- **Scaling strategy**: Horizontally scalable stateless worker containers (`worker-asr`, `worker-metrics`). Postgres connection pooling efficiently supports a scale-out of API servers and background job runners.

## Risks & Tradeoffs

- **Operational risks**: Relying on unreliable school LANs means chunk upload times may heavily skew `insight_latency_sec`. This is mitigated by robust buffering and idempotent chunk handling.
- **Scaling concerns**: Heavy reliance on Postgres for both state management and analytics queries could become a bottleneck at high scale.
- **Consistency tradeoffs**: Using `ON CONFLICT` implies last-writer-wins, which is acceptable for idempotency but requires strict timestamping to avoid race conditions overriding newer metrics with older delayed jobs.
- **Cost implications**: Utilizing GPU resources for ASR/CV per-session is expensive. Optimizing around RTX 5070 cards necessitates batching constraints which trades off sub-second latency for throughput efficiency.

## Agile Sprint Plan

- **Milestones**:
  - Deploy base hot-path infrastructure (FastAPI + MinIO + Redis + Postgres).
  - Implement robust DLQ monitoring and alert tracking for the background workers.
  - Optimize the connection pooling for Postgres to handle 500+ concurrent worker pods.
- **Implementation phases**:
  1. Roll out robust schema validation and indexing improvements.
  2. Implement advanced data lifecycle management (TTL on MinIO chunks).
  3. Refactor current analytics endpoints into materialized views for improved dashboard latency.
- **Priorities**: System reliability and data quality (zero lost chunks). Hardware-constrained optimization.
- **Expected platform improvements**: Vastly improved metric latency predictability, reduced infrastructure spend (by optimizing for consumer GPUs), and robust resilience against intermittent network disconnects.
