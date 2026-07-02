# Data Platform Architecture Report

## Data Problem Analysis

PedagogyX requires a highly scalable, robust data platform to support its multimodal AI classroom intelligence workflows. The system must process real-time and batch data derived from classroom sessions, including voice, video, slide captures, and student engagement metrics. The core business requirement is to accurately measure pedagogical efficiency by analyzing high-throughput multimodal inputs. Data sources include the primary v1 client (Meta Ray-Ban via Android capture), producing massive streams of unstructured media and metadata. The system must accommodate strict data isolation rules since production school data is blocked until G2 (India legal sign-off). Key requirements include supporting a Hot Path for real-time inferencing (e.g., YOLO) and a Cold Path for batch analysis (e.g., faster-whisper, Ollama), meaning our data infrastructure must handle unpredictable, bursty ingestion and ensure data consistency, high availability, and zero data loss under failure scenarios.

## Data Architecture

The data architecture follows a unified, distributed lakehouse model designed to serve both the Hot Path and Cold Path workloads running on our central OSS offline inference backend.

- **Ingestion Systems**: Kafka for high-throughput, low-latency streaming events from the `api` service (which receives data from Meta Ray-Ban clients), combined with scalable object storage (e.g., S3-compatible) for raw unstructured media.
- **Transformation Pipelines**: Spark Structured Streaming and batch processors orchestrated by Dagster/Airflow, consuming raw media and transforming it into structured features for inference.
- **Storage Systems**: Delta Lake or Apache Iceberg on distributed object storage to enable ACID transactions, schema evolution, and unified batch/streaming access.
- **Orchestration Workflows**: Centralized orchestration using Airflow to manage the lifecycle of the Cold Path batch inference jobs across `worker-asr`, `worker-cv`, and `worker-metrics`.
- **Serving Layers**: Low-latency OLAP datastores (e.g., ClickHouse or Apache Pinot) for serving pedagogical efficiency metrics to the FastAPI backend and Next.js/React frontend.

## Pipeline Design

- **ETL/ELT Workflows**: ELT is prioritized. Raw media and metadata are ingested into object storage (Bronze layer). Subsequent transformations decode, align, and enrich the multimodal data (Silver layer), before aggregating metrics for pedagogical analysis (Gold layer).
- **Streaming Architecture**: The Hot Path utilizes Kafka topics and Flink/Spark Streaming to process engagement metrics and YOLO-based computer vision outputs with sub-second latency.
- **Retries & Replayability**: All streaming and batch pipelines implement dead-letter queues (DLQs) and explicit checkpointing to guarantee at-least-once delivery. The architecture is designed to allow full replayability from the Bronze layer in case of downstream logic updates or failure.
- **Idempotency**: All data transformation jobs are fundamentally idempotent, utilizing deterministic partition overwriting to prevent duplicate records during retries or replays.

## Storage & Warehouse Design

- **Schema Strategy**: We leverage a dimensional model in our serving layer, mapping classroom sessions as facts and students, teachers, and pedagogical frameworks as dimensions. The lakehouse schemas are tightly managed and versioned using Schema Registry.
- **Partitioning**: Data is partitioned by `school_id`, `session_id`, and `date`. This heavily optimizes scan times for the Cold Path workers retrieving session media for offline inference.
- **Indexing**: Z-Ordering and clustering strategies are employed on high-cardinality columns like `session_id` to dramatically improve performance during analytical queries on pedagogical efficiency.
- **Optimization Strategy**: Automated background processes perform regular compaction, vacuuming, and file-sizing optimization on the Delta/Iceberg tables to ensure optimal read latency for the `api` and `worker-metrics` services.

## Data Quality & Governance

- **Validation**: Strict schema validation and data contracts are enforced at the ingestion boundary (FastAPI `api` service). Incoming JSON metadata and media payloads must pass validation checks before being committed to Kafka or object storage.
- **Lineage**: Automated data lineage tracking is implemented across all transformations to trace pedagogical metrics back to the specific classroom session, media artifact, and inference model version.
- **Anomaly Detection**: Statistical anomaly detection runs concurrently with the `worker-metrics` pipeline to flag irregular engagement scores, anomalous video frame rates, or corrupt audio segments.
- **Governance Controls**: Role-based access control (RBAC) and strict environment isolation are implemented to ensure compliance with the G2 (India legal sign-off) block on production school data. Test/Dev environments operate strictly on synthetic or anonymized datasets.

## Observability

- **Monitoring & Logging**: Comprehensive logging using structured JSON formats across all microservices (`api`, `web`, `worker-asr`, `worker-cv`, `worker-metrics`). Centralized logging (e.g., ELK or Promtail/Loki) handles all service outputs.
- **SLA Tracking**: Real-time dashboards track data freshness SLAs for both the Hot Path (< 1 second) and Cold Path (< 4 hours for full session processing).
- **Diagnostics**: Distributed tracing (e.g., OpenTelemetry) correlates requests from the Meta Ray-Ban client through the `api` down to the specific `worker` inference jobs, allowing rapid diagnosis of pipeline stalls or high latency.

## Security & Compliance

- **Access Control**: Least privilege access principles apply to all system accounts, IAM roles, and service identities interacting with the data platform.
- **Encryption**: Data is encrypted both at rest (AES-256 for object storage and lakehouse tables) and in transit (TLS 1.3 for all microservice and client communications).
- **Retention**: Automated retention policies purge raw video and audio streams after 30 days, while aggregated pedagogical efficiency metrics are retained long-term based on compliance rules.
- **Governance**: Pre-G2 sign-off protocols mandate strict geofencing and tenant isolation. PII masking and redaction pipelines are enforced on all processed text and audio transcripts before downstream analytical usage.

## Performance Optimization

- **Query Optimization**: Pushdown filtering and partition pruning are strictly enforced in all analytical queries. Serving layer schemas are denormalized where appropriate to eliminate complex joins for the React/Next.js frontend.
- **Compute Optimization**: `worker-cv` and `worker-asr` compute pools autoscale based on Kafka topic lag, maximizing resource utilization during peak classroom hours while scaling down during off-hours.
- **Caching**: The `api` service leverages Redis for caching frequently accessed pedagogical metrics and session metadata to reduce load on the OLAP datastore.
- **Scaling Strategy**: The system relies on horizontal scaling. Kafka partitions and stateless worker nodes can be scaled linearly to handle increasing parallel classroom sessions globally.

## Risks & Tradeoffs

- **Operational Risks**: Managing distributed streaming and batch processing frameworks (Kafka, Spark) introduces operational complexity. Comprehensive runbooks and CI/CD automation are essential.
- **Scaling Concerns**: The bursty nature of classroom recordings could overwhelm ingestion APIs. Rate limiting and sufficient Kafka buffering are necessary tradeoffs.
- **Consistency Tradeoffs**: The Hot Path sacrifices strong consistency for low latency (eventual consistency), whereas the Cold Path guarantees strong consistency and completeness at the cost of delayed reporting.
- **Cost Implications**: Storing massive volumes of multimodal video and audio data is expensive. Tiered storage strategies and aggressive retention policies are required to optimize S3/object storage costs.

## Agile Sprint Plan

- **Sprint 1**: Establish foundational infrastructure. Deploy Kafka, Object Storage, and configure basic network isolation. Implement ingestion endpoints in the `api` service for the Meta Ray-Ban client.
- **Sprint 2**: Implement the Hot Path. Deploy `worker-cv` for real-time YOLO processing, integrating with Kafka and the Next.js `web` dashboard for live metrics.
- **Sprint 3**: Build the Cold Path data lakehouse (Bronze/Silver). Configure Airflow orchestration for `worker-asr` and `worker-metrics` batch processing of historical session data.
- **Sprint 4**: Finalize serving layer (Gold). Optimize analytical schemas, implement caching, and set up comprehensive Data Observability, Tracing, and Data Quality monitoring. Ensure strict compliance with G2 data blockers before load testing.
