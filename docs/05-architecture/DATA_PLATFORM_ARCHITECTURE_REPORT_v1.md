# Data Platform Architecture Report

## PedagogyX: Autonomous Senior Data Engineer & Scalable Data Platform Architect

### 1. Data Problem Analysis

**Business Requirements:** PedagogyX requires a robust, scalable data platform to ingest, process, and analyze multimodal classroom session data (voice, video, slides, student engagement) to measure pedagogical efficiency. The system must support real-time inference via a Hot Path and asynchronous batch processing via a Cold Path.
**Data Sources:** Meta Ray-Ban glasses (via `clients/android-capture-dat`), classroom cameras, microphone arrays, presentation software integrations, and manual metadata uploads.
**Scale Assumptions:** High volume streaming data (audio/video frames) leading to terabytes of raw ingestion per day across hundreds of classrooms. Model inferences and metadata generate billions of rows of structured metrics daily.
**Freshness Requirements:** Real-time metrics (e.g., YOLO object detection for engagement) require sub-second latency (Hot Path). Deep pedagogical analysis (e.g., faster-whisper transcriptions, Ollama LLM insights) has a relaxed SLA of minutes to hours (Cold Path).
**Failure Scenarios:** Unstable network connections from edge devices, malformed video streams, delayed event delivery, ML inference timeouts, and sudden bursts in data volume during school hours.

### 2. Data Architecture

The data architecture follows a distributed, decoupled lakehouse pattern utilizing event-driven microservices.
**Ingestion Systems:** An edge-to-cloud ingestion gateway accepts streaming events from Meta Ray-Ban clients and routes them into Kafka/Redpanda for decoupled buffering.
**Transformation Pipelines:** Stream processing engines (e.g., Flink) normalize raw multimodal telemetry and route it to the respective AI inference workers (`worker-cv` for vision, `worker-asr` for speech). The `worker-metrics` aggregates the AI outputs.
**Storage Systems:** A central OSS offline inference backend is backed by an object storage data lake (S3-compatible) for raw multimodal assets (audio, video) and a distributed data warehouse (e.g., Snowflake or Databricks) for analytical metrics.
**Orchestration Workflows:** Airflow or Dagster coordinates batch Cold Path jobs, ML feature engineering, and downstream ETL/ELT transformations.
**Serving Layers:** A high-concurrency OLAP engine serves aggregated pedagogical metrics to the `api` (FastAPI) and `web` (React/Next.js) dashboards with millisecond latency.

### 3. Pipeline Design

**ETL/ELT Workflows:** Raw telemetry is ingested as JSON/Protobuf, dumped to the data lake (Bronze layer), transformed into structured schema using dbt (Silver layer), and aggregated for analytical dashboards (Gold layer).
**Streaming Architecture:** Hot Path pipelines leverage Kafka streams for real-time engagement detection (YOLO via `worker-cv`). Cold Path uses Kafka topics to queue asynchronous processing (faster-whisper via `worker-asr`).
**Retries & Fault Tolerance:** Dead Letter Queues (DLQs) handle malformed payloads. Microservices implement exponential backoff and circuit breakers for downstream failures.
**Replayability & Idempotency:** All events carry unique transaction IDs and timestamps, allowing exactly-once processing semantics where possible, and idempotent upserts in the warehouse. Event sourcing allows full replay from the data lake in case of logic changes.

### 4. Storage & Warehouse Design

**Schema Strategy:** The data warehouse employs a dimensional model (Star Schema). Fact tables store granular AI inferences (e.g., engagement events, spoken phrases), while dimension tables store classroom, teacher, and session metadata.
**Partitioning:** Fact tables are heavily partitioned by `date` and `school_id` to optimize query performance and data lifecycle management.
**Indexing & Clustering:** Clustering keys are applied to heavily filtered columns such as `session_id` and `timestamp`.
**Optimization Strategy:** Incremental materialized views aggregate real-time metrics. Infrequently accessed raw multimodal data is tiered to cold storage to minimize cost, while analytical metadata remains in hot compute clusters.

### 5. Data Quality & Governance

**Validation:** Schema registries (e.g., Confluent Schema Registry) enforce strict Protobuf/JSON schema validation on ingestion. Data contracts exist between the ingestion API and downstream consumers.
**Lineage:** Tools like Datahub or OpenLineage track data provenance from the edge device through AI workers to the final aggregated metric, ensuring auditability of AI insights.
**Anomaly Detection:** Automated data quality checks run on Silver/Gold tables to detect silent corruption, volume anomalies, or unexpected metric distributions.
**Governance Controls:** Production school data is blocked until G2 (India legal sign-off) via robust environment isolation and data masking. Ownership of datasets is tied to specific microservices and domains.

### 6. Observability

**Monitoring:** Core metrics (pipeline latency, throughput, error rates, consumer lag) are exported to Prometheus and visualized in Grafana.
**Logging:** Centralized structured logging for all microservices (`worker-*`, `api`, `web`) is aggregated into an ELK stack or Datadog for failure diagnostics.
**SLA Tracking:** Freshness tracking is implemented for the Cold Path data to ensure reports are generated within the agreed SLA (e.g., 2 hours post-session).
**Diagnostics:** Distributed tracing (OpenTelemetry) traces requests from the Meta Ray-Ban client through the `api`, into Kafka, and across the AI inference workers to detect bottlenecks.

### 7. Security & Compliance

**Access Control:** Role-Based Access Control (RBAC) is enforced at the warehouse and API levels, utilizing least privilege principles.
**Encryption:** Data is encrypted in transit (TLS 1.3) and at rest (AES-256) across the data lake and warehouse.
**Retention:** Automated lifecycle policies purge raw PII (video/audio) in accordance with local regulations, retaining only anonymized pedagogical metrics.
**Governance:** Compliance with G2 India legal requirements dictates physical data residency and strict geographical partitioning of student data.

### 8. Performance Optimization

**Query Optimization:** Warehouse queries are optimized through partition pruning, avoiding full table scans. Expensive joins are pre-computed in ELT pipelines.
**Compute Optimization:** Autoscaling Kubernetes clusters scale `worker-cv` and `worker-asr` based on queue depth. The warehouse auto-suspends inactive compute clusters.
**Caching:** Redis caches frequent API queries and session metadata to reduce load on the primary transactional database and OLAP warehouse.
**Scaling Strategy:** Separation of storage and compute allows horizontal scaling of the event processing cluster and inference workers without impacting historical data storage.

### 9. Risks & Tradeoffs

**Operational Risks:** Managing complex, distributed Kafka clusters and stateful streaming applications adds operational overhead.
**Scaling Concerns:** Video processing in the Hot Path is highly computationally expensive. Spikes in concurrent classroom sessions may exhaust GPU availability.
**Consistency Tradeoffs:** Real-time Hot Path dashboards prioritize availability and low latency (eventual consistency), while Cold Path analytical reports prioritize strict accuracy and completeness.
**Cost Implications:** High-volume video ingestion and GPU-based inference (YOLO, faster-whisper, Ollama) will be expensive. Cost optimization requires aggressive tiering and efficient batching in the Cold Path.

### 10. Agile Sprint Plan

- **Sprint 1:** Design and provision core infrastructure. Deploy Kafka cluster, object storage data lake, and baseline Kubernetes namespace for the data platform.
- **Sprint 2:** Implement the edge-to-cloud ingestion API. Define data contracts and schema registries for Meta Ray-Ban telemetry.
- **Sprint 3:** Build Hot Path streaming pipelines. Connect `worker-cv` and `worker-metrics` to process real-time engagement data.
- **Sprint 4:** Develop Cold Path batch pipelines. Implement Airflow DAGs to orchestrate `worker-asr` and Ollama inference over stored assets.
- **Sprint 5:** Deploy Data Warehouse and ELT pipelines. Build dbt models for the Star Schema and implement data quality tests.
- **Sprint 6:** Finalize Observability and Security. Implement OpenTelemetry tracing, configure Grafana dashboards, and enforce G2 data residency and access controls.
