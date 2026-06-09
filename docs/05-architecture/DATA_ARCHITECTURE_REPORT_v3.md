# Scalable Data Platform Architecture

## Data Problem Analysis

- **Business Requirements:** Capture, process, and analyze massive volumes of multimodal classroom data (audio, screen, multi-camera feeds from Meta Ray-Ban smart glasses and Android companion apps) to generate reliable, high-quality real-time and historical pedagogy scores.
- **Data Sources:** High-throughput streaming and chunked media data from edge devices (Meta Ray-Ban smart glasses via Wearables Device Access Toolkit), Android companion apps, and Windows smartboards.
- **Scale Assumptions:** The system is engineered to handle hundreds of concurrent classrooms, producing terabytes of raw audio/video daily, seamlessly scaling up to petabytes of historical data for large-scale ML training and complex analytics.
- **Freshness Requirements:** The real-time metrics pipeline (hot path) demands an SLA of ~5 seconds rolling latency. The comprehensive batch analytics and authoritative scoring delivery (cold path) must be finalized within hours of session completion.
- **Failure Scenarios:** Must gracefully handle unreliable school LANs, intermittent edge-to-cloud WAN partitions, delayed or out-of-order media chunks, GPU-accelerated worker node failures, malformed data, and schema drift from evolving edge clients.

## Data Architecture

- **Ingestion Systems:** Edge ingestion buffering handles transient network issues. Streams sync via WebRTC or HTTP chunking to a highly available, load-balanced Cloud Gateway.
- **Transformation Pipelines:** Decoupled, asynchronous worker architecture (`worker-cv`, `worker-asr`, `worker-metrics`). Event-driven queues (Redis/Kafka) route tasks for multi-modal alignment, computer vision extraction, and speech recognition.
- **Storage Systems:** MinIO/S3 for highly durable object storage of raw streaming chunks and transcoded media. PostgreSQL as the central OLTP database for relational metadata, RBAC mapping, and materialized session states.
- **Orchestration Workflows:** Distributed queue architecture for decoupled processing, using Celery/Redis for robust orchestration of ML inference pipelines.
- **Serving Layers:** High-performance FastAPI Gateway routing queries. Caching and aggregation layers serve real-time dashboard data directly to the Next.js/React frontend.

## Pipeline Design

- **ETL/ELT Workflows:** Dual-path architecture separating Hot (low-latency event processing -> Redis/Kafka Bus -> UI) and Cold (Chunk upload -> MinIO -> Transcode/Align -> Heavy ML inference -> Warehouse Materialization).
- **Streaming Architecture:** Event-driven stream processors manage stateful extractions, ensuring low-latency delivery and handling delayed events via time-windowing.
- **Retries:** Exponential backoff with jitter and fully traceable dead-letter queues (DLQs) for failed background tasks and transient network interruptions.
- **Replayability:** Job processing steps (e.g., transcoding, feature extraction) write outputs to deterministic paths, enabling complete replayability of sessions without side effects.
- **Idempotency:** Core processing functions, score aggregations, and ML fusions are strictly idempotent, guaranteeing correct results even under "at-least-once" delivery semantics.

## Storage & Warehouse Design

- **Schema Strategy:** Strongly typed Pydantic schemas enforce data contracts at boundaries, preventing silent data corruption. Core relational data modeled in PostgreSQL.
- **Partitioning:** Large metric tables in PostgreSQL partition by tenant ID and time intervals (e.g., weekly) to ensure scalable scan performance and manage index growth.
- **Indexing:** MinIO object paths designed to prevent hot-spotting (e.g., hashed prefixes). PostgreSQL utilizes composite indices tailored to the most frequent access patterns and dashboard queries.
- **Optimization Strategy:** Connection pooling optimization (sharing cursors to prevent N+1 connection overheads) and aggressive materialization of common queries.

## Data Quality & Governance

- **Validation:** Pre-ingest Pydantic validation of all telemetry and media metadata. Rejection and routing of invalid payloads to DLQs.
- **Lineage:** End-to-end distributed tracing. Every finalized pedagogy score can be traced back to its raw chunk identifiers and processing job IDs.
- **Anomaly Detection:** Automated checks for missing audio chunks, excessive null predictions from ML workers, and structural anomalies in session data.
- **Governance Controls:** Strict adherence to data privacy constraints. Production data remains blocked pending legal sign-off; the system actively restricts processing to synthetic test sessions and MVP environments, ensuring full DPDP compliance.

## Observability

- **Monitoring:** Real-time tracking of queue depths, ingestion lag, worker saturation (e.g., GPU memory limits), and API error rates via Prometheus/Grafana.
- **Logging:** Structured JSON logging across all microservices (`api`, `worker-cv`, etc.). Centralized log aggregation with correlation IDs to trace individual classroom sessions end-to-end.
- **SLA Tracking:** Continuous monitoring of the hot path latency (event creation to dashboard render) and cold path completion times against established SLAs.
- **Diagnostics:** Comprehensive system diagnostics with rapid failure detection for ML workers and storage access bottlenecks.

## Security & Compliance

- **Access Control:** Strict Role-Based Access Control (RBAC) and Row-Level Security (RLS) in PostgreSQL ensure logical tenant isolation. Teachers access only their own metrics.
- **Encryption:** TLS 1.3 for all WAN transport and edge-to-cloud communications. AES-256 encryption for data at rest in MinIO and PostgreSQL.
- **Retention:** Automated data lifecycle policies. High-volume raw media chunks are aggressively purged post-processing, while anonymized, structured analytics are retained long-term for AI training.
- **Governance:** Full compliance with strict educational data regulations, enforcing data isolation and minimizing PII footprint.

## Performance Optimization

- **Query Optimization:** Eliminating N+1 database connection problems through shared cursors and optimizing complex joins via materialized views in PostgreSQL.
- **Compute Optimization:** Batching inference requests for `worker-cv` and `worker-asr` to maximize GPU utilization and throughput.
- **Caching:** Aggressive Redis caching for high-read, low-write endpoints, heavily reducing load on the primary PostgreSQL database.
- **Scaling Strategy:** Horizontal pod autoscaling (HPA) for stateless worker pods based on queue length and processing latency metrics.

## Risks & Tradeoffs

- **Operational Risks:** Vulnerability to unpredictable school network stability. Tradeoff: We invest in heavy edge-buffering, which improves reliability but can delay cold path processing.
- **Scaling Concerns:** Complex multimodal ML inference is compute-intensive and can bottleneck rapidly. Mitigated by dynamic scaling and strict priority queuing for premium tenants.
- **Consistency Tradeoffs:** The real-time hot path trades strong consistency for extremely low latency. Authoritative, fully consistent data is guaranteed by the asynchronous cold path.
- **Cost Implications:** Maintaining large volumes of raw streaming video is highly expensive. Tradeoff requires strict archival or deletion policies balanced against future ML dataset needs.

## Agile Sprint Plan

- **Milestones:**
  1. Solidify edge ingestion robustness and complete integration with Meta Ray-Ban companion app telemetry.
  2. Implement robust DLQ handling and schema validation for all ML worker queues.
  3. Deploy centralized observability dashboards tracking pipeline freshness SLAs.
- **Implementation Phases:**
  - Sprint 1: Enforce Pydantic schema contracts and fix N+1 connection issues in database utilities.
  - Sprint 2: Deploy partitioned PostgreSQL schema for scalable metrics storage and finalize MinIO prefix structures.
  - Sprint 3: Implement comprehensive end-to-end tracing and real-time SLA alerting.
- **Priorities:** Eliminate any possibility of silent data loss, guarantee pipeline idempotency, and ensure strict governance over synthetic vs. production data.
- **Expected Platform Improvements:** Drastically increased pipeline reliability, measurable improvements in hot-path latency, and a robust foundation for petabyte-scale ML training data.
