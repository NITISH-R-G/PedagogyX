# PedagogyX Data Architecture Report
**Author:** Autonomous Senior Data Engineer & Scalable Data Platform Architect
**Date:** Current
**Version:** v3

## Data Problem Analysis

### Business Requirements
PedagogyX is an educational analytics platform utilizing Meta Ray-Ban smart glasses (via the Wearables Device Access Toolkit and an Android companion app) as the primary v1 capture client. The system must process multimodal data (audio, video, telemetry) continuously, extract pedagogical insights, and serve these insights to educators with low latency to inform instructional strategies. The primary goal is to provide reliable, scalable, and actionable analytics without intruding on the teaching workflow.

### Data Sources
1. **Meta Ray-Ban Smart Glasses:** Video (FPV), audio, and device telemetry via Bluetooth/Wi-Fi.
2. **Android Companion App (Wearables DAT):** Session metadata, user interactions, synchronization state, and buffered edge data.
3. **Internal Operational Data:** Application state, API usage logs, system health metrics.

### Scale Assumptions
- **Ingestion:** Anticipating thousands of simultaneous teaching sessions (1-2 hours each), streaming ~2-5 Mbps of compressed AV data per client. Resulting in multi-TB daily ingestion.
- **Processing:** Hundreds of concurrent stream processing jobs extracting transcriptions, speaker diarization, and visual cues (e.g., student engagement levels).
- **Storage:** Petabyte-scale data lake for historical sessions to train future AI models; high-performance data warehouse for aggregated analytics.

### Freshness Requirements
- Real-time event streams: sub-second latency for critical operational metrics and session state.
- Analytics pipeline: < 5 minutes for post-session summarized insights (transcriptions, engagement scores).
- Batch analytics: daily/weekly aggregates for school administration.

### Failure Scenarios
- Unstable network connections in schools causing delayed, out-of-order, or malformed data packets.
- Edge device battery depletion or app crashes causing abrupt session termination.
- Spike in concurrent sessions overwhelming stream processing clusters.

## Data Architecture

### Ingestion Systems
- **Edge-to-Cloud:** Android Companion App utilizes a resilient publish-subscribe mechanism (e.g., gRPC/WebSocket for control, multipart uploads for media) to land data securely into cloud object storage (raw zone) and stream events into a distributed message broker (Kafka).

### Transformation Pipelines
- **Stream Processing (Apache Flink / Spark Structured Streaming):** Consumes Kafka topics to perform real-time deduplication, sessionization, and stateful event enrichment.
- **Batch Processing (Apache Spark / Databricks):** Nightly processing jobs that run heavy ML inferences, re-process failed sessions, and aggregate metrics for the data warehouse.

### Storage Systems
- **Data Lake (Amazon S3 / GCS):** Tiered storage architecture.
  - *Raw Zone:* Immutable, appended-only raw captures.
  - *Refined Zone:* Parquet/Delta Lake formatted tables (transcriptions, metadata).
  - *Curated Zone:* Feature stores and ML-ready datasets.
- **Data Warehouse (Snowflake / BigQuery):** Highly optimized OLAP storage for serving dashboard metrics to educators and administrators.

### Orchestration Workflows
- **Apache Airflow / Dagster:** Centralized orchestration of all batch ETL/ELT jobs, ML pipeline triggers, and data quality checks. Ensures dependency management, retries, and SLA tracking.

### Serving Layers
- **Real-time API (FastAPI/Redis):** Serves real-time session status and quick queries.
- **Analytics API:** Exposes warehouse views securely to the PedagogyX Next.js frontend.

## Pipeline Design

### ETL/ELT Workflows
- **ELT First Approach:** Raw data is immediately loaded into the Data Lake (Delta format). Transformation logic (dbt) runs over the refined zone to build dimensional models in the warehouse.

### Streaming Architecture
- **Event Mesh:** Kafka topics structured by domain (e.g., `telemetry.raw`, `audio.transcribed`, `session.events`).
- **Processing:** Flink jobs handle watermarking to manage late-arriving events from disconnected Android clients, ensuring accurate session boundaries.

### Retries & Replayability
- **Idempotency:** All downstream sinks (Delta tables, OLAP DBs) enforce upserts based on a composite key (`session_id` + `event_id`).
- **Dead Letter Queues (DLQs):** Malformed events are routed to DLQs for inspection, alerting, and manual/automated replay via Airflow.

## Storage & Warehouse Design

### Schema Strategy

- **Star Schema Design:**
  - *Fact Tables:* `fact_session_events`, `fact_transcriptions`, `fact_engagement_metrics`.
  - *Dimension Tables:* `dim_educator`, `dim_device`, `dim_school`, `dim_class`.

### Partitioning & Indexing

- **Data Lake Partitioning:** `date=YYYY-MM-DD/school_id=XXX/session_id=YYY` to optimize read patterns for ML training and re-processing.
- **Warehouse Clustering:** Cluster keys on `school_id` and `timestamp` to ensure efficient predicate pushdown for multi-tenant queries.

### Optimization Strategy

- Materialized views for commonly requested dashboard widgets (e.g., daily engagement trends).
- Dynamic scaling of warehouse compute based on predictable school hours.

## Data Quality & Governance

### Validation

- **Schema Enforcement:** Confluent Schema Registry (Protobuf/Avro) strictly enforces payload structure at the Kafka producer level (Android App).
- **Data Contracts:** Explicit API and data shape agreements between the mobile team and the data platform team.

### Lineage

- **Metadata Management:** Tools like DataHub or OpenLineage capture end-to-end trace logs from the edge device ingestion point down to the specific BI dashboard query.

### Anomaly Detection & Governance Controls

- Automated Great Expectations checks on the warehouse (e.g., ensuring `session_duration > 0`).
- Role-Based Access Control (RBAC) ensuring educators only see their classes, while admins see anonymized aggregates.

## Observability

### Monitoring

- Prometheus/Grafana stack monitoring Kafka lag, Flink job throughput, Airflow task durations, and API latency.

### Logging

- Centralized ELK/Datadog stack correlating edge application logs with cloud backend processing logs via unified `trace_id`.

### SLA Tracking & Diagnostics

- Dashboards tracking data freshness (e.g., P99 latency of video availability).
- Alerts configured for broken pipelines, SLA breaches, and abnormal drop-offs in ingestion rates.

## Security & Compliance

### Access Control

- Strict IAM roles enforcing least privilege. Storage buckets are private by default.
- PII handling workflows: Auto-redaction of student faces and names from raw media before it enters the Refined Zone.

### Encryption

- **In Transit:** TLS 1.3 mandated for all API endpoints and broker connections.
- **At Rest:** AES-256 encryption using KMS for S3, Kafka volumes, and Snowflake databases.

### Retention & Governance

- Automated lifecycle policies: Raw video is aged out to Glacier after 30 days unless flagged for ML training (with legal sign-off).
- Full audit logging of all data warehouse queries and internal administrative actions.

## Performance Optimization

### Query Optimization

- Implementing dbt to pre-aggregate complex ML output metrics into flat, easily queryable tables.
- Preventing inefficient scans by strictly enforcing partition filters in BI tools.

### Compute Optimization & Caching

- Utilizing Redis for caching high-frequency frontend requests (e.g., active session statuses).
- Right-sizing Spark clusters and utilizing spot instances for fault-tolerant nightly batch jobs to optimize infrastructure costs.

## Risks & Tradeoffs

### Operational Risks

- Managing massive video data uploads over variable school Wi-Fi networks may lead to incomplete sessions.
  *Mitigation:* Robust edge-side buffering on the Android device with resumable uploads.

### Scaling Concerns

- Sudden bursts of traffic at the start of a school day.
  *Mitigation:* Over-provisioning Kafka ingest clusters and autoscaling Flink/Spark workers.

### Consistency Tradeoffs

- Choosing eventual consistency for ML insights to prioritize system availability and reduce synchronous processing blocking.

### Cost Implications

- Petabyte-scale video storage is expensive.
  *Tradeoff:* Aggressive lifecycle management and utilizing intelligent tiering to reduce long-term storage costs.

## Agile Sprint Plan

### Sprint 1: Infrastructure & Ingestion Baseline

- **Milestone:** Reliable ingestion pipeline.
- **Tasks:** Provision Kafka clusters, S3 buckets, and configure Schema Registry. Establish resilient upload APIs for the Android DAT.
- **Expected Improvement:** 99.9% ingestion uptime with schema validation.

### Sprint 2: Core Processing & Data Lake

- **Milestone:** Delta Lake architecture established.
- **Tasks:** Deploy Airflow and Flink. Build the ELT pipelines to move data from Raw to Refined zones.
- **Expected Improvement:** Fully automated, idempotent data processing with DLQ handling.

### Sprint 3: Warehouse & Serving

- **Milestone:** Analytics ready for the Next.js frontend.
- **Tasks:** Implement Snowflake/BigQuery schema, dbt transformations, and expose secure Analytics APIs.
- **Expected Improvement:** < 1-second query latency for core pedagogical dashboards.

### Sprint 4: Observability, Quality & Governance

- **Milestone:** Production-grade reliability.
- **Tasks:** Deploy OpenLineage, Great Expectations, and comprehensive Grafana dashboards. Implement PII redaction jobs.
- **Expected Improvement:** Total platform visibility, proactive alerting, and compliance readiness.
