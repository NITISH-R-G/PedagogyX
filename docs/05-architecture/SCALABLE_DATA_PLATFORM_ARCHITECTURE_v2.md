# Scalable Data Platform Architecture Report

**Version:** 2.0
**Author:** Autonomous Senior Data Engineer & Scalable Data Platform Architect
**Date:** 2026-06-16

## 1. Data Problem Analysis

### Business Requirements

- Provide an open-source, offline-first multimodal AI data platform.
- Serve edge compute devices (consumer-grade RTX 5070 constraints, ~12GB VRAM).
- Capture audio, video, and screen data from classrooms to generate advanced analytical insights (teacher talk ratios, student engagement metrics, etc.).
- Maintain strict compliance with Free and Open Source Software (FOSS) mandates.

### Data Sources

- Classroom multimodal data inputs: Audio, Video, and Screen Capture (Screen, Camera feeds).
- Model Inference Metadata (YOLO object detection bounding boxes, Whisper transcripts, Diarization data).

### Scale Assumptions

- Millions of classroom hours translated to petabytes of long-term storage data over time.
- Widespread edge nodes processing data locally under poor connectivity scenarios, creating intermittent bulk data sync loads.

### Freshness Requirements

- Inference outputs processed at the edge must be synced to central storage asynchronously.
- Central aggregations and rollups can tolerate daily or hourly latency based on network availability at the edge.

### Failure Scenarios

- Unreliable edge network connections dropping payloads.
- Schema drift caused by new models or updated client collection telemetry.
- Processing backlogs due to bursts of bulk syncs when edge nodes reconnect.

## 2. Data Architecture

### Ingestion Systems

- **Edge Data Sync:** Resilient data synchronization protocols supporting retry logic, backpressure, and chunked uploads to object storage.
- **Message Bus:** Kafka or Redis Streams as the primary ingestion buffer for metadata and telemetry to decouple ingestion from processing.

### Transformation Pipelines

- **ETL/ELT Layer:** Containerized worker services (like `worker-asr`, `worker-metrics`, `worker-cv`) process raw data into structured entities and AI metrics.
- Distributed task queues implemented via Redis for horizontal scaling of inference tasks.

### Storage Systems

- **Data Lake (Object Storage):** MinIO used for durable storage of raw multimedia files (audio/video chunks), enabling scalability and FOSS compliance.
- **Relational Database:** PostgreSQL utilized for structured metadata, schema-enforced AI metrics, transactional operations, and aggregation tracking.

### Orchestration Workflows

- **Task Orchestration:** Python-based distributed task workers using Redis for queues, managing dependencies like audio chunk processing before talk ratio calculation.

### Serving Layers

- **FastAPI Backend:** Serves the Next.js frontend with processed metrics.
- High-concurrency read replicas (future) for fast dashboard metric retrieval.

## 3. Pipeline Design

### ETL/ELT Workflows

- **Extraction:** Raw media is pulled from object storage (MinIO) by worker nodes.
- **Transformation:** Worker containers perform AI inference (e.g., ASR, Diarization, CV) and aggregations.
- **Load:** Structured output and raw inference schemas are saved into PostgreSQL.

### Streaming Architecture

- **Queue System:** Currently using Redis queues for tasks (`jobs:asr`, `jobs:talk_ratio`).
- Future state may introduce Apache Kafka to handle stream processing for event-driven architectures with strict ordering and event replay.

### Retries & Backpressure

- Exponential backoff and retry logic implemented at the worker level for processing failures (e.g., MinIO timeout or DB connection failure).
- Rate-limiting to ensure backend DBs or MinIO instances are not overwhelmed by bulk ingestion.

### Replayability & Idempotency

- All data ingestion and transformation jobs must be fully idempotent, relying on composite primary keys or deterministic chunk hashing.
- Workers can be instructed to reprocess specific time ranges or chunk sets without corrupting downstream metrics.

## 4. Storage & Warehouse Design

### Schema Strategy

- **Normalized Relational Model:** Core entities (Sessions, Chunks, Transcripts, Entities) mapped via strictly typed SQL schemas (PostgreSQL).
- JSONB columns in PostgreSQL used strategically to absorb evolving schemas from raw AI inference output, paired with strong validation before promoting to structured tables.

### Partitioning

- Time-series metric tables (e.g., raw inferences, telemetry) should be partitioned by `session_id` or temporal boundaries (e.g., daily/monthly) to ensure scan efficiency.

### Indexing

- B-Tree indexes on heavily queried foreign keys (`session_id`).
- GIN indexes for JSONB columns containing flexible but frequently queried metadata.

### Optimization Strategy

- Offload large blob storage to MinIO immediately; avoid database bloat.
- Materialized views or aggregated rollup tables (e.g., `daily_session_metrics`) used to accelerate frequent UI analytical queries.

## 5. Data Quality & Governance

### Validation

- **Schema Enforcement:** Pydantic models validate all incoming payloads at the FastAPI layer before database insertion.
- Constraint checks (foreign keys, uniqueness) enforced at the PostgreSQL layer.

### Lineage

- Explicit tracking of parent-child relationships (e.g., Chunk -> Transcript -> Talk Ratio Metric) ensures transparency in how downstream metrics were computed.

### Anomaly Detection

- Future implementation of automated statistical bounds checking on processed metrics to detect drift in model outputs.

### Governance Controls

- Clear ownership models for each data pipeline.
- FOSS compliance mandates zero proprietary dependencies in the stack.

## 6. Observability

### Monitoring

- Health checks for database, Redis, MinIO, and all services continuously monitored.
- Real-time queue length tracking and worker processing latency metrics.

### Logging

- Centralized structured JSON logging across FastAPI and worker containers.

### SLA Tracking

- P95 and P99 metrics tracked for chunk processing latency and API response times.

### Diagnostics

- Distributed tracing (e.g., OpenTelemetry) for complex end-to-end task flows.

## 7. Security & Compliance

### Access Control

- API Key authentication and Role-Based Access Control (RBAC) across data services.
- Least-privilege IAM models applied to worker access to MinIO buckets and database tables.

### Encryption

- Data at rest encrypted. Data in transit encrypted via TLS across all components.

### Retention & Deletion

- Strict data residency compliance (India offline-first design).
- Right-to-be-forgotten deletion workflows cascading from PostgreSQL out to object storage (MinIO).

### Governance

- PII handling constraints dictate offline or localized inference processing.

## 8. Performance Optimization

### Query Optimization

- Avoid `SELECT *`. Leverage projection and index-only scans.
- Tune PostgreSQL settings for expected workload (`work_mem`, `shared_buffers`).

### Compute Optimization

- Scale AI workers horizontally. Use model quantization (e.g., INT8/FP16) or optimize batching logic for RTX 5070 constraints.

### Caching

- Cache frequently accessed aggregated metrics in Redis to serve dashboard queries quickly.

### Scaling Strategy

- Stateless worker nodes dynamically scaled based on queue depths.
- Read replicas for the PostgreSQL database when read/write contention increases.

## 9. Risks & Tradeoffs

### Operational Risks

- Hardware constraints (RTX 5070, 12GB VRAM) limit model sizes or concurrency at edge nodes, causing processing bottlenecks.
- Asynchronous task failures causing silent data dropping if observability is poor.

### Scaling Concerns

- Heavy reliance on Redis for both caching and queuing could become a bottleneck at massive scale; Kafka transition might be required.

### Consistency Tradeoffs

- Eventual consistency accepted for downstream aggregations, prioritizing system availability and partition tolerance.

### Cost Implications

- Using open-source components avoids licensing costs, but increases operational overhead (self-managing MinIO, PostgreSQL, etc.).

## 10. Agile Sprint Plan

### Sprint 1: Stability & Metrics Pipeline

- Implement basic talk ratio aggregation pipeline.
- Fortify worker-asr and worker-metrics idempotency.
- Establish robust monitoring for Redis queue lengths.

### Sprint 2: Storage & Partitioning

- Implement PostgreSQL table partitioning for raw telemetry.
- Optimize indexing strategy for analytics queries.
- Roll out structured logging.

### Sprint 3: Resilience & Scale

- Implement comprehensive retry and dead-letter queue patterns.
- Benchmark and tune container scaling based on Redis queue depths.
- Document full system lineage and schemas.
