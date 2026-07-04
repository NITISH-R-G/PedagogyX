# PedagogyX Data Platform Architecture Report

**Version:** 1.0
**Role:** Autonomous Senior Data Engineer & Scalable Data Platform Architect

## Data Problem Analysis

- **Business Requirements:** The platform needs to process multimodal classroom session data (voice, video, slides, student engagement) to measure pedagogical efficiency and provide actionable insights. The system currently focuses on MVP (Phase 0) processing synthetic test sessions via Meta Ray-Ban client.
- **Data Sources:** Real-time capture data from Meta Ray-Ban glasses (audio, video, images), synthetic test sessions, and classroom metadata.
- **Scale Assumptions:** Initially terabytes, scaling to petabytes as the system expands across schools. The ASR pipeline must handle robust Hindi-English code-switching.
- **Freshness Requirements:** Low-latency for real-time engagement metrics (Hot Path) and asynchronous batch processing for deep analysis (Cold Path).
- **Failure Scenarios:** Unreliable internet connectivity in schools leading to delayed events, malformed capture data, and intermittent infrastructure failures during batch AI inference.

## Data Architecture

- **Ingestion Systems:** API endpoints (FastAPI) receiving multimodal data streams from clients (Android/Meta Ray-Ban).
- **Transformation Pipelines:** Two-tier architecture:
  - **Hot Path (Real-time):** Fast, low-latency processing (e.g., YOLO for engagement tracking).
  - **Cold Path (Batch):** Asynchronous processing using Redis Streams/Celery for heavy workloads like ASR (faster-whisper large-v3) and LLM analysis (Ollama).
- **Storage Systems:**
  - Raw and processed media: MinIO (S3-compatible object storage).
  - Relational and metadata: PostgreSQL.
  - Caching and queuing: Redis.
- **Orchestration Workflows:** Event-driven orchestration using Celery and Redis Streams to manage long-running AI inference tasks asynchronously.
- **Serving Layers:** RESTful APIs served via FastAPI querying PostgreSQL for dashboard metrics and analytics.

## Pipeline Design

- **ETL/ELT Workflows:** Raw data is ingested into MinIO. Metadata is persisted to PostgreSQL. Event triggers enqueue jobs into Redis Streams/Celery for Cold Path processing. Results are written back to PostgreSQL.
- **Streaming Architecture:** Event-driven architecture handling asynchronous AI inference and continuous ingestion from wearable clients.
- **Retries:** Exponential backoff for transient failures in AI workers (ASR, CV, Metrics).
- **Replayability:** Raw payloads stored immutably in MinIO to allow replay of any failed or updated AI pipeline.
- **Idempotency:** Unique session and event IDs ensure that reprocessing data yields identical results without duplication.

## Storage & Warehouse Design

- **Schema Strategy:** Normalized operational schema in PostgreSQL for Phase 0. Future evolution to a star schema for the data warehouse as analytical queries grow.
- **Partitioning:** PostgreSQL partition by date/school ID for session data to maintain fast query times. MinIO partitioned by date and session.
- **Indexing:** B-Tree and GIN indexes on frequently queried JSON/metadata fields in PostgreSQL.
- **Optimization Strategy:** Leverage materialized views for pedagogical efficiency metrics to prevent inefficient scans during dashboard loads.

## Data Quality & Governance

- **Validation:** Pydantic schemas in FastAPI strictly validate incoming payload structures.
- **Lineage:** Metadata tracking from raw MinIO object to final analytical metrics stored in PostgreSQL.
- **Anomaly Detection:** Pipeline monitoring to detect incomplete sessions or unusually low confidence scores from ASR/CV models.
- **Governance Controls:** Strict access controls on test/synthetic data. Preparing for G2 (India legal sign-off) requirements before ingesting real production school data.

## Observability

- **Monitoring:** Health dashboards and Prometheus/Grafana integration for tracking pipeline latency, worker queue lengths, and system health.
- **Logging:** Centralized structured JSON logging across FastAPI and Celery workers to track failed jobs and schema drift.
- **SLA Tracking:** Tracking freshness of Cold Path inference and real-time Hot Path latency.
- **Diagnostics:** Detailed tracing for event-driven pipelines to identify bottlenecks in the ASR or LLM processing stages.

## Security & Compliance

- **Access Control:** Role-Based Access Control (RBAC) via FastAPI endpoints.
- **Encryption:** TLS for data in transit; encrypted storage at rest for both MinIO and PostgreSQL.
- **Retention:** Defined retention policies for raw video/audio to comply with future school privacy agreements.
- **Governance:** Strict adherence to Phase 0 constraints: no production school data until G2 legal sign-off. PII handling mechanisms being built for future real data.

## Performance Optimization

- **Query Optimization:** Extensive use of PostgreSQL indexes and optimized queries to minimize compute utilization.
- **Compute Optimization:** Horizontal scaling of Celery workers for heavy Cold Path workloads (worker-asr, worker-cv).
- **Caching:** Redis used heavily for caching frequent metrics and API responses to reduce database load.
- **Scaling Strategy:** Central OSS offline inference backend to scale independently from web APIs.

## Risks & Tradeoffs

- **Operational Risks:** Managing distributed Celery workers and state consistency during pipeline failures.
- **Scaling Concerns:** High GPU cost and scaling limitations for batch ASR and LLM processing; handled by asynchronous Cold Path design.
- **Consistency Tradeoffs:** Eventual consistency in the Cold Path vs. immediate consistency in standard CRUD operations.
- **Cost Implications:** AI inference (GPU) costs vs. processing latency. Utilizing OSS models (faster-whisper, Ollama) significantly reduces API costs but increases infrastructure complexity.

## Agile Sprint Plan

- **Milestones:**
  1. Solidify Phase 0 data ingestion and storage (PostgreSQL + MinIO).
  2. Stabilize Celery/Redis event-driven Cold Path.
  3. Implement observability and schema validation.
- **Implementation Phases:** Current phase focuses on resilient ingestion from Meta Ray-Ban and reliable ASR/CV inference.
- **Priorities:** Broken pipelines in worker-asr, scalability blockers in Cold Path queue management.
- **Expected Platform Improvements:** High reliability in synthetic data processing, paving the way for G2 approval and real-world data scaling.
