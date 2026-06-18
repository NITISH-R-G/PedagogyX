# Senior Systems Engineer Report

## System Overview

PedagogyX is an educational analytics platform utilizing Meta Ray-Ban smart glasses (via the Wearables Device Access Toolkit and an Android companion app) as the primary v1 capture client.

The current system provides core boilerplate to ingest session data and extract metrics (such as talk ratios). The goal of this architecture is to process large volumes of multimedia inputs (audio/video), execute heavy processing asynchronously, and provide an analytics dashboard, all while remaining highly scalable, available, and fault-tolerant in a production environment.

**Requirements:**

- High throughput for multimedia uploads from edge clients (Android).
- Asynchronous orchestration for heavy AI processing jobs (ASR, CV).
- Durable, scalable storage for multi-media files.
- Resilient messaging for task distribution.
- Real-time/near real-time analytics aggregation.

**Scale Assumptions:**

- Millions of daily active students/teachers.
- Hundreds of terabytes (TB) of audio and video generated per day.
- Spiky traffic patterns (e.g., matching the start/end times of school days or classes).
- Stringent compliance, security, and privacy requirements.

**Constraints:**

- The processing of heavy multimedia payloads introduces latency limits.
- Edge client network connectivity can be unreliable, requiring resilient sync and upload mechanisms.
- Production school data requires high security/legal sign-off.

## High Level Architecture

The system is structured as an asynchronous microservices architecture to decouple lightweight API operations from heavy ML processing operations.

**Major Components:**

1.  **Web (Frontend):** Next.js 15 application utilizing App Router and Tailwind CSS v4 to serve the administrator dashboard and metric visualization components.
2.  **API Gateway / Core Backend (`services/api`):** FastAPI-based web service managing session ingestion, health checks, direct DB CRUD operations, and presigned URL generation for edge media uploads. It orchestrates the submission of asynchronous jobs.
3.  **Workers (`services/worker-asr`, `services/worker-cv`, `services/worker-metrics`):** Python-based asynchronous workers.
    - `worker-asr`: Processes Automatic Speech Recognition.
    - `worker-cv`: Processes Computer Vision tasks.
    - `worker-metrics`: Aggregates the results into business metrics (e.g., talk ratios).
4.  **Message Broker:** Redis handles job queueing and distribution for the worker pool.
5.  **Object Storage:** MinIO (S3-compatible) serves as the persistent storage layer for uploaded multimedia chunks and raw assets.
6.  **Relational Database:** PostgreSQL manages structured state, session metadata, user accounts, and aggregated metrics.

**Data Flow:**

1.  Client device (Android companion app) requests an upload session from the API.
2.  API responds with metadata and a direct-upload presigned S3 URL.
3.  Client uploads raw media directly to Object Storage (MinIO/S3).
4.  Client signals the API that the upload is complete.
5.  API enqueues a job message onto Redis.
6.  Workers (ASR/CV) pick up the job, pull the data from Object Storage, run processing, and save intermediate results back to the DB or Object Storage.
7.  `worker-metrics` aggregates the processed data into final metrics in PostgreSQL.
8.  The Web frontend queries the API for dashboard metrics.

## Infrastructure Design

The current local boilerplate utilizes Docker Compose (`infra/compose.dev.yaml`), but production will target a highly available, multi-region Cloud Native footprint.

**Deployment Topology (Production):**

- **Kubernetes (EKS/GKE):** Container orchestration for the API, Web, and Worker components. This enables granular autoscaling based on specific workload demands (e.g., CPU/GPU metrics).
- **Multi-Region/Multi-AZ:** Core API and Storage deployed across multiple Availability Zones to ensure high availability. Edge ingestion optimized via CDN or regional edge proxies.

**Cloud Architecture & Networking:**

- **Ingress / Edge:** Global Anycast IP mapping to a WAF and L7 Load Balancer. CDN caches static assets for the Next.js frontend.
- **Service Mesh:** Istio or Linkerd to handle internal microservice mutual TLS (mTLS), circuit breaking, and traffic shaping.
- **Managed Services:** Replace local Redis, MinIO, and PostgreSQL with managed Cloud equivalents (e.g., AWS ElastiCache, Amazon S3, Amazon Aurora Serverless) to reduce operational overhead.
- **Compute:** CPU nodes for API/Web and `worker-metrics`. GPU-enabled node pools for `worker-asr` and `worker-cv` to accelerate inference workloads.

## Database Design

**Schema Strategy:**
The PostgreSQL database handles stateful entities: `sessions`, `chunks`, `metrics`. We optimize for rapid inserts from workers and fast analytical reads for the web dashboard.

**Replication & Scaling:**

- **Primary-Replica Setup:** A single primary node handles write operations (ingestion state, worker results). Multiple read replicas handle the dashboard read query volume.
- **Connection Pooling:** PgBouncer or an equivalent proxy to handle the high connection churn from scaled-out worker pools and APIs.

**Consistency Model:**

- **Strong Consistency** for critical state (session creation, client synchronization).
- **Eventual Consistency** for metric aggregation and analytics, provided via the asynchronous worker pipeline.

**Future Considerations:**

- If analytical queries become a bottleneck, implement a CDC (Change Data Capture) pipeline (e.g., Debezium) to stream data from Postgres into an OLAP datastore (e.g., ClickHouse or Snowflake) for heavy dashboard metrics.

## Scalability Strategy

**Horizontal Scaling:**

- **API/Web:** Stateless, scaling based on CPU/Memory utilization and incoming request rate.
- **Workers:** Scaled via KEDA (Kubernetes Event-driven Autoscaling) based on the depth of the Redis queues (`jobs:asr`, `jobs:talk_ratio`). This ensures GPU instances are provisioned only when a backlog of ML jobs exists, optimizing cost.

**Caching:**

- **Redis:** Serves dual purpose: as the job queue broker and as an ephemeral cache layer for frequent API read requests (e.g., configuration, recent session states) to reduce Postgres load.
- **CDN:** Aggressive caching of the Web frontend static assets and dashboard shell.

**Partitioning & Load Balancing:**

- Use L7 load balancers to distribute traffic across API pods.
- Implement storage tiering: move processed or aged session media from hot S3 buckets to cold storage (e.g., S3 Glacier) to manage storage costs at scale.

## Reliability Strategy

**Resilience Patterns:**

- **Asynchronous Decoupling:** By pushing heavy processing to workers, the API gateway remains highly responsive even under massive upload spikes.
- **Retries & Dead Letter Queues (DLQ):** Failed worker jobs are automatically retried with exponential backoff. Persistent failures are moved to a DLQ for manual inspection, preventing poison-pill messages from blocking the pipeline.
- **Circuit Breakers:** Implemented on internal service calls (e.g., API to Postgres/Redis) to fail fast during underlying outages and prevent cascading failures.

**Failover & Redundancy:**

- Managed Database features (e.g., Multi-AZ deployments) provide automatic failover capabilities.
- Stateless Kubernetes pods guarantee automatic replacement of unhealthy application instances.

## Security Architecture

**Authentication & Authorization:**

- Edge clients authenticate via API keys (`API_KEY`) and secure tokens.
- Internal microservices utilize Kubernetes Service Accounts and mTLS (via Service Mesh) for zero-trust network communication.
- Web dashboard access must integrate robust Identity Provider (IdP) authentication with strict RBAC (Role-Based Access Control) given the sensitivity of educational data.

**Encryption:**

- **In Transit:** All external traffic is enforced over TLS 1.3. Internal cluster traffic is encrypted via mTLS.
- **At Rest:** Storage layers (PostgreSQL, S3, Redis) leverage KMS-backed encryption for all stored data.

**Abuse Prevention:**

- WAF (Web Application Firewall) to block malicious external traffic.
- Rate limiting at the API Gateway level to prevent noisy neighbor problems and mitigate DDoS vectors against session ingestion endpoints.

## Observability Stack

**Logging, Tracing, & Monitoring:**

- **Structured Logging:** All services output JSON-formatted logs, aggregated centrally (e.g., via Fluent Bit to OpenSearch/Elasticsearch or Datadog).
- **Distributed Tracing:** OpenTelemetry instrumentation across Next.js, FastAPI, and Python Workers to trace the lifecycle of a request from client upload through worker processing.
- **Metrics:** Prometheus scrapes system metrics (CPU, Memory, Redis queue depth) and business metrics (Job processing time, ASR accuracy).
- **Alerting:** Grafana/Alertmanager triggers PagerDuty alerts on critical SLO breaches (e.g., high API error rates, unbounded queue growth, low DB connection availability).

## Performance Optimization

**Bottlenecks & Latency:**

- **Network I/O:** The direct-to-S3 upload pattern via presigned URLs removes the API service from the heavy media streaming path, significantly optimizing ingress latency and bandwidth costs.
- **Worker Throughput:** Batch processing of media chunks and maintaining warm GPU memory states in `worker-asr`/`worker-cv` will maximize inference throughput.

**Throughput Optimization:**

- Utilizing Redis for high-speed queueing ensures that task dispatching operates at microsecond latencies.
- Implementing asynchronous PostgreSQL drivers (e.g., `asyncpg`) in the FastAPI backend enables highly concurrent database operations without thread blocking.

## Tradeoffs

**Pros:**

- Highly modular and scalable asynchronous architecture.
- Clear separation of concerns between ingestion, processing, and visualization.
- Cost-efficient via specific component autoscaling (scaling GPU workers independently of API nodes).

**Cons & Limitations:**

- **Operational Complexity:** Managing a distributed queue system with asynchronous state updates is harder to debug and monitor than a synchronous monolith.
- **Eventual Consistency:** The Web dashboard will not reflect real-time processing immediately, which may impact user experience if processing queues back up.

**Future Improvements:**

- Replace Redis queues with a more robust streaming platform (e.g., Apache Kafka) to allow for event replay, stream processing, and multi-consumer pub/sub scenarios as the complexity of analytics grows.
- Implement robust Data lifecycle management policies for the Object Storage layer.

## Agile Sprint Plan

### Phase 1: Foundation & Observability (Sprint 1)

- Implement OpenTelemetry distributed tracing across `api`, `web`, and `workers`.
- Establish structured JSON logging and Prometheus metric endpoints.
- Finalize production IaC (Terraform) for managed dependencies (RDS, S3, ElastiCache).

### Phase 2: Reliability & Scaling (Sprint 2)

- Implement robust dead letter queues and worker retry logic.
- Configure Kubernetes HPA (Horizontal Pod Autoscaler) and KEDA for queue-depth based scaling of workers.
- Integrate PgBouncer for database connection pooling.

### Phase 3: Security & Production Readiness (Sprint 3)

- Configure WAF, API rate limiting, and internal service mesh mTLS.
- Perform load testing to validate ingestion throughput and asynchronous pipeline stability.
- Finalize disaster recovery runbooks.
