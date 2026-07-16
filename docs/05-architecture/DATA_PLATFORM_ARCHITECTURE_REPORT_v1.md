# Data Platform Architecture Report (v1)

## Data Problem Analysis

PedagogyX is a multimodal AI classroom intelligence platform designed to ingest and analyze vast volumes of unstructured data (voice, video, slides, and student engagement metrics) to measure pedagogical efficiency. The platform must handle continuous high-throughput real-time data from client devices (such as Meta Ray-Ban glasses) and support subsequent heavy batch-processing pipelines for complex multimodal AI inferences.

**Key Challenges & Requirements:**

- **Multimodal Data Scale:** Ingestion of continuous A/V streams (Hot Path) and periodic batch payloads (Cold Path). Expected volumes start in the hundreds of gigabytes per session, scaling rapidly.
- **Latency & Freshness:** Real-time metrics must be updated sub-second for dashboard visibility, while deep analytical processing (e.g., semantic analysis, detailed engagement scoring) is acceptable on an hourly or end-of-day SLA.
- **Regulatory & Privacy Blockers:** Production school data is currently blocked pending G2 (India legal sign-off). The platform must currently operate exclusively on synthetic test sessions while laying the groundwork for robust PII anonymization.
- **Failure Scenarios:** Unstable network connectivity from classrooms, interrupted uploads, malformed multi-part payloads, and delayed events.

## Data Architecture

The data architecture follows a robust, decoupled Lambda-like pattern tailored for AI-centric workloads, separating fast operational intelligence from deep analytical processing.

- **Ingestion Layer:** API Gateway backed by scalable object storage (MinIO for on-prem/dev, S3 for production) to receive raw binary multimodal data, and a fast messaging queue (Redis/Kafka) for real-time engagement telemetry.
- **Processing Paths:**
  - **Hot Path:** Real-time stream processing for immediate metrics (e.g., YOLO object detection events, simple audio thresholds) feeding directly into the real-time operational database.
  - **Cold Path:** Orchestrated batch processing (e.g., faster-whisper for accurate transcription, Ollama for semantic summarization) reading from the data lake, performing transformations, and loading results into the analytical warehouse.
- **Serving Layer:** PostgreSQL acts as the primary operational store, with plans to introduce a scalable OLAP engine (e.g., ClickHouse or Snowflake) as data volume and query complexity increase.

## Pipeline Design

Pipelines are designed for idempotency, replayability, and resilience against transient failures.

- **Streaming Pipelines (Hot Path):** High-throughput microservices (`worker-cv`, `worker-metrics`) consume events directly from the ingestion queue, process telemetry, and upsert records into PostgreSQL.
- **Batch Pipelines (Cold Path):** Heavy AI inference workers (`worker-asr` and offline batch jobs) are orchestrated via an asynchronous task queue.
  - **Idempotency:** All jobs are keyed by a unique `session_id` and `chunk_id`. Overlapping retries simply overwrite or ignore duplicate data.
  - **Replayability:** Raw immutable events are stored indefinitely in the object store. In the event of a model upgrade or pipeline bug, historical data can be entirely re-processed from the source.
  - **Backpressure & Retries:** Strict exponential backoff mechanisms prevent the central OSS offline inference backend from being overwhelmed during peak hours (e.g., end of school day).

## Storage & Warehouse Design

The storage architecture balances the need for cheap, vast storage for raw assets and fast, structured storage for analytical queries.

- **Data Lake (Raw & Bronze):** MinIO/S3 object storage for raw MP4s, WAVs, and JSON event logs.
- **Operational Database (Silver):** PostgreSQL for structured metadata, session tracking, and normalized metric dimensions.
  - **Schema Design:** Heavily normalized for transactional integrity, utilizing UUIDs, appropriate foreign keys, and JSONB columns for flexible semi-structured inference outputs.
- **Analytical Warehouse (Gold):** (Future Phase) Dimensional models utilizing a Star Schema approach to aggregate metrics by school, classroom, teacher, and time dimensions. For MVP, materialized views in PostgreSQL are utilized to serve pre-aggregated analytical queries efficiently.
- **Partitioning Strategy:** PostgreSQL tables for high-volume time-series metrics are partitioned natively by date (`created_at`) to optimize read and retention operations.

## Data Quality & Governance

Robust data quality mechanisms are enforced to prevent "garbage in, garbage out" scenarios, critical for downstream AI model reliability.

- **Schema Validation:** Strict Pydantic models at the API layer enforce schema constraints on incoming metadata.
- **Data Contracts:** Clear API specifications between the ingestion layer and processing workers ensure backward compatibility during schema evolution.
- **Anomaly Detection:** Automated checks monitor the ratio of incoming raw data size to produced text/metric outputs, alerting on sudden drops in expected inference yield (e.g., a silent failure in `worker-asr`).
- **Lineage:** Metadata tables record the exact pipeline version and AI model version used to generate specific insights, ensuring full traceability from raw video frame to pedagogical efficiency score.

## Observability

Comprehensive monitoring is deployed across the entire data lifecycle.

- **Infrastructure & Pipeline Monitoring:** System metrics, queue depths, and processing latencies are actively tracked.
- **SLA & Freshness Tracking:** Dashboards monitor the time elapsed from session end to the completion of the Cold Path processing.
- **Logging & Diagnostics:** Centralized structured logging across all microservices provides deep context on failures. Trace IDs are injected at ingestion and propagated through all asynchronous tasks.
- **Failure Alerts:** Actionable alerts are routed to the data engineering team for prolonged queue stagnation, excessive dead-letter events, or degraded infrastructure health.

## Security & Compliance

Given the highly sensitive nature of classroom audio and video, security is paramount and built-in at the infrastructure level.

- **Access Control:** Strict Least Privilege Access policies on all internal systems and API endpoints. Service-to-service communication is authenticated.
- **Data Encryption:** All data is encrypted at rest in object storage and PostgreSQL (AES-256) and in transit via TLS 1.3.
- **Data Isolation & Compliance:** Pending G2 compliance, the system currently isolates and restricts processing to synthetic data. Future phases will introduce automated PII scrubbing (blurring faces, muting sensitive audio segments) in the Cold Path before data is made available for generalized analytics or model training.
- **Retention Policies:** Automated TTL rules purge raw multimodal data after the required analytical extraction, minimizing risk exposure.

## Performance Optimization

Efficiency is engineered into the system to manage the high computational and storage costs associated with AI inferences.

- **Compute Optimization:** Decoupling Hot/Cold paths ensures expensive GPU instances are heavily utilized only for batched Cold Path jobs, while lightweight CPU instances handle real-time streaming.
- **Query Optimization:** Strategic indexing (B-Tree on foreign keys, GIN on JSONB fields) and aggressive use of materialized views in PostgreSQL to optimize read paths for the frontend dashboard.
- **Caching:** Redis is utilized to cache frequently accessed metadata, session states, and pre-computed dashboard aggregates to reduce database load.

## Risks & Tradeoffs

- **PostgreSQL vs. Dedicated OLAP:** For MVP speed, PostgreSQL handles both operational and analytical loads. _Tradeoff:_ As data scales, complex analytical queries will degrade operational performance, necessitating an eventual migration of analytical workloads to a specialized OLAP engine.
- **Cost vs. Latency (Cold Path):** Deep semantic analysis is computationally expensive. _Tradeoff:_ We accept higher latency (delayed availability of deep insights) to run these workloads efficiently in batches during off-peak hours to manage infrastructure costs.
- **Data Completeness vs. Connectivity:** Classrooms often have poor Wi-Fi. _Tradeoff:_ The system architecture must rely heavily on the client device (Meta Ray-Ban/Android app) to buffer and robustly retry uploads, potentially delaying the "complete" status of a session by hours.

## Agile Sprint Plan

- **Sprint 1: Foundational Infrastructure**
  - Provision MinIO/S3 and configure PostgreSQL partitions.
  - Implement raw data ingestion API with Pydantic validation.
  - Setup basic structured logging and trace propagation.
- **Sprint 2: Hot Path Implementation**
  - Deploy Redis queues and construct `worker-cv` / `worker-metrics` streaming consumers.
  - Build baseline materialized views for real-time operational dashboarding.
- **Sprint 3: Cold Path & AI Orchestration**
  - Implement asynchronous task queue for orchestration.
  - Deploy `worker-asr` pipeline reading from data lake and writing to PostgreSQL.
  - Establish data lineage tracking in the metadata schema.
- **Sprint 4: Observability & Resilience**
  - Implement dead-letter queues and automated replay scripts.
  - Create SLA monitoring dashboards (queue depth, processing latency).
  - Finalize security configurations and prepare synthetic test environment for Phase 0 sign-off.
