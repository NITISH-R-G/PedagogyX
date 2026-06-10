# Scalable Data Platform Architecture Report v3

## Data Problem Analysis

- business requirements: Support large-scale ingestion, processing, and analytics of multimodal classroom data (audio, screen, multi-camera feeds) to generate pedagogy scores. Improve reliability and scalability of the data platform from previous iterations.
- data sources: High-throughput streaming data from Meta Ray-Ban Android devices and Windows smartboards.
- scale assumptions: Designed to process terabytes to petabytes of raw A/V data efficiently, supporting real-time workloads and evolving schemas.
- freshness requirements: Real-time dashboard SLA ~5 seconds. Batch analytics and scoring delivery within hours.
- failure scenarios: Network partitions, out-of-order chunks, worker node failures, infrastructure outages, schema drift.

## Data Architecture

- ingestion systems: Edge nodes with LAN ingest buffers, syncing to Cloud-hosted MediaMTX/WebRTC gateways.
- transformation pipelines: Decoupled via Redis event queues. Python-based workers handle A/V streams, multimodal alignment, and ML inferences.
- storage systems: PostgreSQL for relational metadata, MinIO for object storage (raw chunks, transcoded media).
- orchestration workflows: Event-driven worker architecture. Kubernetes deployments for scalable containerized pipelines.
- serving layers: Fast API Gateway routing queries. Live Analytics Bus serving real-time subscriptions.

## Pipeline Design

- ETL/ELT workflows: Dual-path architecture. Hot path for WebRTC ingest and live bus. Cold path for batch chunk upload and ML fusion.
- streaming architecture: Event-driven workers with WebRTC for low-latency live extraction.
- retries: Robust retry mechanisms with full traceback logging for network failures.
- replayability: Idempotent job processing steps to ensure safe replay of historical data.
- idempotency: Strongly enforced in ML fusion and materialization steps.

## Storage & Warehouse Design

- schema strategy: OLTP via Postgres. Pydantic schemas enforce data contracts to prevent silent corruption.
- partitioning: Postgres tables partitioned by session date and tenant ID for query optimization.
- indexing: MinIO prefixes designed to avoid hot spotting. Postgres metadata indexes optimized for analytics workflows.
- optimization strategy: Connection pooling optimizations, partition pruning, and compute efficiency improvements.

## Data Quality & Governance

- validation: Pre-ingest validation of A/V chunks and metadata schema enforcement.
- lineage: End-to-end trace IDs linking raw chunks to pedagogy scores.
- anomaly detection: Monitoring for missing frames, incomplete uploads, and silent data corruption.
- governance controls: Pydantic schemas enforce API contracts. Data isolation and retention policies strictly managed.

## Observability

- monitoring: Centralized logging, lineage visualization, freshness tracking, and SLA monitoring.
- logging: Immutable logging of exports and stream views. Detailed tracebacks for task failures.
- SLA tracking: Hot path latency and cold path latency are continuously measured.
- diagnostics: Cross-service correlation IDs for rapid debugging and failure diagnostics.

## Security & Compliance

- access control: Role-Based Access Control (RBAC) ensuring tenant isolation.
- encryption: TLS 1.3 enforced for transport. Data at rest encrypted in MinIO and PostgreSQL.
- retention: Strict retention policies for raw video vs. anonymized metadata.
- governance: Logical tenant isolation using Row-Level Security (RLS).

## Performance Optimization

- query optimization: Passing existing cursors to avoid N+1 connection overhead.
- compute optimization: Compute-heavy tasks (ML inference) batched for GPU utilization.
- caching: Fast API layers use Redis for caching aggregate telemetry.
- scaling strategy: Stateless worker pods scale horizontally based on queue depth and SLAs.

## Risks & Tradeoffs

- operational risks: Dependence on external network stability (school WANs).
- scaling concerns: Compute resource bottlenecks for complex ML fusion tasks.
- consistency tradeoffs: Real-time hot path trades strong consistency for low latency, while batch path guarantees eventual consistency.
- cost implications: High storage costs for multi-stream raw video necessitate aggressive archival strategies.

## Agile Sprint Plan

- milestones: Enhance data reliability, scalability, and observability of the core platform.
- implementation phases:
  1. Optimize data pipeline throughput and fault tolerance.
  2. Implement advanced lineage and anomaly detection systems.
  3. Refactor and modernize outdated architectures to reduce operational friction.
- priorities: Reduce failure rates, optimize warehouse efficiency, and improve platform usability.
- expected platform improvements: Higher data freshness, reduced query times, improved infrastructure automation.
