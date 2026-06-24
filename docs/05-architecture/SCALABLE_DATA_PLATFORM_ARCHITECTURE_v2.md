# Scalable Data Platform Architecture v2

## Data Problem Analysis

- **Business Requirements:** The platform must support large-scale ingestion of wearable capture data (audio, visual, metrics) from Meta Ray-Ban devices (DAT) and provide scalable access to transformed analytical and machine learning data for the PedagogyX Phase 0 to G2 rollout.
- **Data Sources:** Primary ingestion from Android-capture-DAT clients (audio chunks, visual telemetry, metadata), external APIs, and internal microservices (worker-cv, worker-asr, worker-metrics).
- **Scale Assumptions:** Capable of scaling from initial beta (gigabytes/day) to petabyte-scale real-world capture as deployment extends to hundreds of schools globally.
- **Freshness Requirements:** Low latency (near real-time) for real-time pedagogical feedback telemetry, with batch processing for daily aggregate reports and ML training extraction.
- **Failure Scenarios:** Must gracefully handle missing event data, delayed event deliveries, schema drift from client updates, and infrastructure out-of-memory or network partitioning scenarios.

## Data Architecture

- **Ingestion Systems:** Distributed REST APIs for initial intake combined with Kafka-based event streaming to decouple the fast client uploads from slower worker nodes.
- **Transformation Pipelines:** Modular, containerized processing using distributed execution (e.g., Apache Spark or Flink) for complex telemetry correlations and audio-visual parsing.
- **Storage Systems:** Delta Lake or Apache Iceberg for the core Data Lakehouse architecture to enable ACID compliance over cheap object storage (S3/MinIO), tiered based on access patterns.
- **Orchestration Workflows:** Centralized orchestration using Apache Airflow or Dagster to manage complex dependency chains and trigger retries automatically on failure.
- **Serving Layers:** High-concurrency OLAP engine (e.g., Trino, ClickHouse) caching recent data in Redis for instantaneous dashboard queries and API responses.

## Pipeline Design

- **ETL/ELT Workflows:** ELT approach preferred: raw data lands immediately in the lake; transformations applied downstream using dbt for metric aggregation to keep raw data perfectly immutable.
- **Streaming Architecture:** Kafka topics partitioned by school or session ID. Flink used for real-time stateful stream processing and windowing.
- **Retries:** Configured exponential backoff for external API integrations (e.g., LLM inference points).
- **Replayability:** Event sourcing model enabling full rewind and replayability from Kafka cold storage or Delta Lake history in case of faulty transformations.
- **Idempotency:** All pipeline jobs uniquely keyed (e.g., hash of session_id and timestamp) ensuring safe reruns without duplication.

## Storage & Warehouse Design

- **Schema Strategy:** Medallion architecture (Bronze, Silver, Gold). Bronze for raw JSON/binary telemetry, Silver for flattened/validated tables, Gold for optimized dimensional models.
- **Partitioning:** Primarily partitioned by `date` and `tenant_id` (school/region) to heavily optimize the typical query access patterns.
- **Indexing:** Z-ordering on high-cardinality keys like `session_id` and `user_id` to dramatically reduce file scanning.
- **Optimization Strategy:** Automatic background compaction, vacuuming of old data versions, and materialized views for top-level pedagogical metrics.

## Data Quality & Governance

- **Validation:** Strict schema enforcement on ingestion via Protocol Buffers/Avro. Great Expectations runs continuously to detect nulls, range violations, and referential integrity loss.
- **Lineage:** Automated lineage tracking from raw client telemetry through transformation scripts to the final BI dashboards, integrated into a metadata catalog.
- **Anomaly Detection:** Statistical checks on event volume and distribution to flag broken client updates or silent sensor failures before reports generate.
- **Governance Controls:** Data cataloging, dictionary curation, and formalized data contracts between the application engineering team and the data platform team.

## Observability

- **Monitoring:** Comprehensive Prometheus/Grafana dashboards tracking Kafka lag, Spark executor utilization, Airflow task durations, and data lake growth rates.
- **Logging:** Structured JSON logs shipped to a centralized logging cluster (e.g., ELK or Datadog) tagged with execution IDs and pipeline names.
- **SLA Tracking:** Daily SLA reports comparing actual data freshness and completeness against target business expectations.
- **Diagnostics:** Distributed tracing (OpenTelemetry) spanning API ingress all the way to database writes, ensuring immediate root-cause isolation.

## Security & Compliance

- **Access Control:** Role-Based Access Control (RBAC) enforced at the column and row levels. Read access granted strictly through authorized views.
- **Encryption:** AES-256 encryption at rest. All data in transit strictly TLS 1.3 encrypted.
- **Retention:** Hard deletion policies for compliance (e.g., GDPR/G2 requirements), removing raw unanonymized data after 30 days while retaining aggregated metrics indefinitely.
- **Governance:** Regular automated audits of access logs to detect unauthorized or anomalous access patterns across the platform.

## Performance Optimization

- **Query Optimization:** Analyzing Trino/Spark execution plans to identify skewed joins and broadcast join opportunities.
- **Compute Optimization:** Auto-scaling Kubernetes clusters based on pipeline queue depth, right-sizing executors for memory-intensive CV/ASR tasks.
- **Caching:** Redis implementation for hot dashboard metrics, and caching intermediate RDDs/DataFrames in complex iterative ML feature extraction.
- **Scaling Strategy:** Fully decoupled compute and storage. Horizontal scaling of Kafka brokers and stateless processing nodes to handle sudden spikes in school session concurrency.

## Risks & Tradeoffs

- **Operational Risks:** Managing distributed Kafka/Flink infrastructure requires significant operational maturity and can be brittle if under-resourced.
- **Scaling Concerns:** High-frequency visual telemetry may overwhelm initial ingestion bounds if not properly compressed or batch-uploaded by the DAT client.
- **Consistency Tradeoffs:** Eventual consistency accepted in the real-time serving layer to achieve necessary write throughput and lower latency.
- **Cost Implications:** Maintaining dual-stack processing (streaming + batch) and extended Delta Lake histories increases storage/compute costs; aggressive lifecycle policies must mitigate this.

## Agile Sprint Plan

- **Milestones:**
  - Sprint 1: Local Docker infrastructure parity (Kafka, MinIO, Spark).
  - Sprint 2: Bronze layer ingestion pipelines for Meta DAT telemetry.
  - Sprint 3: Silver/Gold transformations with dbt and Trino querying.
  - Sprint 4: CI/CD automation, Great Expectations integration, and performance benchmarking.
- **Implementation Phases:** Phase 0 focuses on synthetic data. Phase 1 targets single-school scale. Phase 2 moves to multi-tenant global architecture.
- **Priorities:** Immutability, reproducibility, schema enforcement, and rapid ingestion.
- **Expected Platform Improvements:** Elimination of manual data wrangling, deterministic replay of pedagogical events, and high-confidence metrics generation.
