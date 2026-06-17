# Scalable Data Platform Architecture Report v3

## Data Problem Analysis

- business requirements: Capture, process, and analyze multimodal classroom data (audio, screen, multi-camera feeds) to generate real-time and historical pedagogy scores via Edge and India Cloud infrastructure. Handle expanding scope as the platform adds deeper ML capabilities.
- data sources: High-volume streaming data from thin clients such as Meta Ray-Ban Android devices and Windows smartboards. Potential for future integrations with other IoT devices.
- scale assumptions: Designed to handle hundreds of concurrent classrooms producing terabytes of raw A/V daily, eventually scaling to petabytes for ML training purposes. Requires robust backpressure mechanisms.
- freshness requirements: Real-time dashboard SLA is ~5 seconds rolling latency (hot path). Batch analytics and authoritative scoring delivery within hours of session completion (cold path).
- failure scenarios: Network partitions between school LANs and the cloud, out-of-order media chunks, intermittent WAN connectivity, GPU worker failures, schema drift from client telemetry. Must support graceful degradation.

## Data Architecture

- ingestion systems: Edge nodes run a LAN ingest buffer to mitigate WAN instability, syncing chunks up to a Cloud-hosted MediaMTX or WebRTC gateway. Introducing localized caching to reduce WAN load.
- transformation pipelines: Decoupled via Redis event queues. Python-based background workers process A/V streams, perform multi-modal alignment, and execute models like YOLO CV and Transformer-based ASR. Migration towards Apache Kafka or similar distributed event streaming for higher throughput.
- storage systems: PostgreSQL for relational metadata, session states, and RBAC mapping. MinIO for object storage holding raw streaming chunks, transcoded media, and extracted artifacts. Evaluating Iceberg or Delta Lake formats for long-term analytical storage.
- orchestration workflows: Event-driven via Redis queues and Celery-style worker architecture for background tasks. Airflow/Prefect for complex batch and ML pipelines.
- serving layers: Fast API Gateway routing queries to Postgres or cached aggregation layers. Live Analytics Bus (Kafka/Redis) serves real-time subscriptions to frontend dashboards.

## Pipeline Design

- ETL/ELT workflows: Dual-path architecture separating Hot (WebRTC ingest -> Feature Workers -> Live Bus) and Cold (Chunk upload -> MinIO -> Transcode/Align -> ML Fusion -> Materialization) processing.
- streaming architecture: Event-driven workers utilizing WebRTC for low-latency live extraction. Implementing Flink or Spark Structured Streaming for complex real-time aggregations.
- retries: Background workers utilize custom retry mechanisms with full traceback logging for network-related failures. Exponential backoff and dead-letter queues (DLQs) are standard.
- replayability: Job processing steps (transcoding, metric materialization) are idempotent to ensure safe replay. Event-sourcing patterns implemented to reconstruct state.
- idempotency: Implemented heavily in the ML fusion and score materialization steps to recover from processing interruptions.

## Storage & Warehouse Design

- schema strategy: OLTP via Postgres for core session management. Pydantic enforced schemas prevent upstream silent corruption. Star schema in a dedicated data warehouse (e.g., Snowflake, BigQuery) for complex analytics.
- partitioning: Postgres tables for large metrics partitioned by session date and tenant ID to improve scan performance and limit index sizes. Time-based partitioning in data lake.
- indexing: MinIO prefixes designed as `tenant_id/session_id/stream_type/timestamp.mp4` to avoid hot spotting. Postgres uses specific indexes on metadata queries. Materialized views for frequent complex queries.
- optimization strategy: Connection pooling optimizations in backend services by passing existing cursors instead of opening new ones, avoiding N+1 connection overhead. Vector embeddings stored in a dedicated vector database (e.g., pgvector, Milvus).

## Data Quality & Governance

- validation: Pre-ingest validation of A/V chunks ensuring correct format and metadata presence. Great Expectations or similar framework for batch data quality checks.
- lineage: End-to-end trace IDs link raw chunk IDs directly to final pedagogy score generation steps. DataHub or Amundsen for automated lineage tracking and metadata management.
- anomaly detection: Proactive monitoring for sudden drops in audio volume, missing frames, and incomplete session uploads. Automated alerts for data quality breaches.
- governance controls: Pydantic schemas enforce API payload contracts. Real student data remains restricted until G2 (India legal sign-off) is complete; currently strictly utilizing synthetic test data. Strict adherence to DPDP and GDPR.

## Observability

- monitoring: Tracking queue depths, DLQ sizes, and job failure rates. Monitoring Edge LAN buffers and GPU memory saturation. Prometheus and Grafana for infrastructure and platform metrics.
- logging: Detailed traceback logging to sys.stderr for all failed background tasks. Immutable logging of score exports and stream views. Centralized logging with ELK/EFK stack or Datadog.
- SLA tracking: Hot path latency (chunk arrival to output) and cold path latency (session completion to final score) continuously measured. Data freshness and completeness dashboards.
- diagnostics: Cross-service correlation IDs utilized in log aggregation to rapidly debug pipeline failures. Distributed tracing with Jaeger or OpenTelemetry.

## Security & Compliance

- access control: Role-Based Access Control (RBAC) ensures tenant isolation, allowing teachers access to their own data and admins aggregate views. Integration with corporate SSO/IdP.
- encryption: TLS 1.3 enforced for all Edge to Cloud WAN transport. Data at rest in MinIO and PostgreSQL is fully encrypted using KMS.
- retention: Strict data retention policies applied. Raw video subject to aggressive lifecycle rules (e.g., deletion after 30 days) while anonymized metadata and transcripts are retained for ML training. Automated data purging mechanisms.
- governance: Logical tenant isolation in Postgres using Row-Level Security (RLS) to strictly enforce DPDP compliance. Regular security audits and penetration testing.

## Performance Optimization

- query optimization: Passing existing cursors to database helper methods avoids N+1 problems in backend and background worker codebases. EXPLAIN ANALYZE used for tuning complex analytical queries.
- compute optimization: Compute-heavy tasks like A/V sync and model inference are heavily batched to maximize GPU utilization. Autoscaling node pools for varying ML workloads.
- caching: Fast API layers and Live Analytics Bus use Redis for caching aggregate telemetry. CDN for serving static or frequently accessed historical assets.
- scaling strategy: Stateless worker pods scale horizontally based on Redis queue depth and SLA thresholds. Edge buffer compression mitigates transient WAN drops. Separation of compute and storage in analytics workloads.

## Risks & Tradeoffs

- operational risks: Dependence on school WAN stability. Mitigated by robust edge buffering, acknowledging it delays cold path materialization. Increased operational complexity with distributed architectures.
- scaling concerns: Complex ML fusion processing bottlenecking on available compute resources (e.g., RTX 5070 budget). Managing large-scale distributed databases and streaming platforms requires specialized expertise.
- consistency tradeoffs: Real-time hot path trades consistency for low latency (at-most-once delivery), whereas the batch cold path guarantees eventual consistency and exactly-once processing via idempotency. Eventual consistency in distributed caches.
- cost implications: Storing high volume multi-stream raw video continuously is expensive. The tradeoff requires aggressive archival or deletion of raw assets shortly after successful processing. Cloud egress costs and compute costs for ML models must be carefully monitored.

## Agile Sprint Plan

- milestones: Establish resilient core storage and DLQ patterns, migrate high-throughput queues to Kafka, implement comprehensive data quality checks, and deploy advanced observability dashboards.
- implementation phases:
  1. Enforce Pydantic schemas and standard DLQ patterns for background workers. Initialize Kafka deployment.
  2. Implement idempotent chunk aggregation for MinIO and integrate Great Expectations.
  3. Deploy queue monitoring, latency SLAs, and automated lineage tracking.
- priorities: Guarantee pipeline reliability, ensure no silent data loss during ingest, optimize ML compute utilization, and minimize operational friction.
- expected platform improvements: Drastically lower error rates, predictable scalability of ML workers, improved visibility into end-to-end data lineage, and reduced infrastructure costs per processed session.
