# PedagogyX System Design Architecture Report

## System Overview

- **Purpose**: PedagogyX provides a multimodal AI classroom intelligence and teacher optimization platform. It utilizes a Hybrid Edge-Cloud architecture to ingest audio/visual telemetry, run real-time lightweight analytics (Hot Path), and execute deep, authoritative pedagogy scoring (Cold Path) to improve educational outcomes.
- **Requirements**: Provide real-time classroom telemetry via WebRTC, robust asynchronous batch processing for multi-camera stream alignment and transformer fusion, and secure storage with G2 India legal data residency compliance. Avoid proprietary AI APIs.
- **Scale Assumptions**: The system is designed to support massive concurrent AV stream ingestions from low-end edge endpoints (Meta Ray-Ban smart glasses via Android hosts and Windows Smartboards). It anticipates severe traffic spikes and bursty workloads during typical school hours (e.g., millions of concurrent streams globally).
- **Constraints**: Deep resource constraints at the edge, constrained cloud compute budgets (RTX 5070 GPU limitations), potentially unstable and low-bandwidth school WAN connections, and strict open-source, non-proprietary dependencies to maintain compliance and cost efficiency.

## High Level Architecture

- **Major Components**:
  - **Capture Layer**: Meta Ray-Ban (DAT) clients, Android edge hosts, and smartboards producing real-time multi-modal streams.
  - **Edge Buffer (LAN Edge)**: High-throughput local edge nodes designed for resilient stream ingest, short-term buffering, and local Hot Path inference to shield the cloud from WAN unreliability.
  - **PedagogyX Cloud (OSS Central)**: An ingest gateway, Kafka/Redis-backed asynchronous job queues, Python-based ML worker nodes (CV, ASR, Metrics), and data storage layers.
  - **Control Plane**: A unified API Gateway with robust multi-tenant RBAC managing school-level isolation and administrative access to pedagogy scores and raw media.
- **Interactions**: Capture nodes push real-time streams to the Edge Buffer. The Edge Buffer relays lightweight telemetry directly for Hot Path metrics and spools heavy media chunks to the Cloud over resilient gRPC/HTTP pipelines for Cold Path batch processing.
- **Data Flow**: `Capture -> LAN Buffer -> Edge Inference (Hot) -> Cloud Ingest Gateway -> Async Message Bus -> GPU Workers (Cold) -> Postgres/MinIO -> API/Dashboard`.
- **Service Boundaries**: Hard decoupling between the synchronous, latency-sensitive ingest path (Go) and the asynchronous, computationally heavy inference path (Python).

## Infrastructure Design

- **Deployment Topology**: A globally distributed edge network interfacing with a centralized, multi-AZ cloud presence in India. Edge nodes operate autonomously during network partitions.
- **Cloud Architecture**: Microservices deployed on Kubernetes. Auto-scaling worker nodes dynamically scale horizontally based on queue depth metrics, constrained by hard GPU quotas.
- **Networking**: WebRTC and UDP dominate the Hot Path for ultra-low latency. Resumable, chunked gRPC with heavy retry logic underpins the Cold Path over WAN. Audio streams serve as the system-wide master clock for precise multi-modal cross-correlation.
- **Orchestration**: Kubernetes handles cloud workloads using Helm charts and GitOps. Edge workloads run via simplified docker-compose or K3s setups optimized for low-touch, remote administration.

## Database Design

- **Schema Strategy**: Relational schema (Postgres) tailored for tenant RBAC matrices, pedagogical entity relationships, and structured scoring outputs. Time-series data from Hot Path telemetry is handled via append-only logs.
- **Replication**: Multi-AZ Postgres deployments utilizing streaming replication for high availability. Heavy read workloads (dashboards) are offloaded to dedicated read replicas to preserve primary write throughput.
- **Scaling**: Connection pooling (e.g., PgBouncer) protects the database from connection exhaustion during horizontal worker scaling. Logical partitioning of tenant data by district is implemented to ease future physical sharding.
- **Consistency Model**: Eventual consistency is accepted for Hot Path telemetry. Strong consistency (ACID) is strictly enforced for final Cold Path pedagogy scores and tenant RBAC policies.

## Scalability Strategy

- **Horizontal Scaling**: Stateless edge buffers and Go-based cloud ingest gateways scale linearly. Queue-driven GPU workers scale automatically based on backlog, absorbing bursty end-of-class traffic without dropping payloads.
- **Caching**: Multi-tiered caching strategy. Redis is used for tenant metadata, RBAC evaluations, and aggregated dashboard metrics to massively reduce OLTP database strain.
- **Partitioning**: Tenant data is logically partitioned, enabling safe and scalable multi-tenant isolation and localized query optimization.
- **Load Balancing**: Advanced L7 ingress controllers perform intelligent routing and rate limiting, while edge buffers naturally smooth out sudden WAN upload bursts.

## Reliability Strategy

- **Failover**: Multi-AZ cloud infrastructure ensures zero single points of failure for persistent stores. Stateless pods are natively self-healing.
- **Redundancy**: Persistent data is durably stored in distributed object storage (MinIO) and replicated relational databases.
- **Recovery Mechanisms**: Strict Dead Letter Queue (DLQ) implementations capture malformed chunks and failed inferences. Database is backed by continuous WAL archiving for Point-in-Time Recovery (PITR).
- **Resilience Patterns**: The Edge Buffer acts as a critical bulkhead, spooling data locally during WAN failures and performing resumable sync upon recovery. If GPU capacity maxes out, the system gracefully degrades by prioritizing Hot Path metrics while extending Cold Path SLAs.

## Security Architecture

- **Authentication**: OIDC and OAuth2 flows integrated at the API Gateway level for unified identity management.
- **Authorization**: Granular, multi-tier RBAC restricting access at the tenant (district/school) level, enforcing least privilege for both teachers and administrators.
- **Encryption**: TLS 1.3 mandated for all transit. AES-256 encryption at rest for MinIO objects and Postgres volumes.
- **Abuse Prevention**: Rate limiting, strict API payload validation, and volumetric DDoS protection at both the network edge and application ingress to prevent resource exhaustion and malicious injection.

## Observability Stack

- **Logging**: Centralized, structured JSON logging. All worker exceptions and DLQ events contain full context and stack traces to accelerate root cause analysis.
- **Tracing**: Distributed tracing via OpenTelemetry seamlessly tracks request lifecycles from the Ray-Ban client, through the Edge Buffer, into the async workers, ending at the database.
- **Monitoring**: Prometheus scrapes metrics across the cluster, visualized in Grafana.
- **Alerting**: Automated alerts triggered on p99 latency spikes, SLA violations for queue depth, elevated 5xx error rates, and prolonged edge node disconnection events.

## Performance Optimization

- **Bottlenecks**: Intensive cross-correlation of multi-stream video and constrained cloud GPU availability for transformer inference.
- **Latency Optimization**: Edge inference provides near-instant Hot Path telemetry, effectively hiding cold-path cloud latency from end users.
- **Throughput Optimization**: Go-based ingest gateways process massive concurrent I/O with negligible memory overhead. Batching inference requests dynamically maximizes GPU memory utilization and TFLOPS throughput.

## Tradeoffs

- **Pros**: Exceptional resilience to WAN instability via edge buffering; massive scalability due to strict statelessness and async queues; high cost-efficiency and data sovereignty compliance via the FOSS AI stack.
- **Cons**: High architectural complexity regarding distributed state, robust resumable uploads, and asynchronous data synchronization; Cold Path results are inherently delayed.
- **Limitations**: Bounded by the RTX 5070 GPU compute budget, which limits the parameter size of the deployed OSS transformer models.
- **Future Improvements**: Pushing deeper NLP and Whisper models to the Edge Buffer to execute local chunk transcription, further slashing WAN bandwidth utilization and cloud compute requirements.

## Agile Sprint Plan

- **Milestones**:
  - **Sprint 1-2**: Deploy Edge Buffer ingest APIs (Go), establish client connectivity, and implement resumable WAN syncing.
  - **Sprint 3-4**: Provision core cloud infrastructure (Postgres, MinIO, Redis) and establish the API Gateway with strict multi-tenant RBAC.
  - **Sprint 5-6**: Implement async ML worker pipelines (Python) with DLQs, operating within GPU quotas.
  - **Sprint 7-8**: Develop master audio-clock stream alignment and complex Cold Path pedagogy scoring fusion.
  - **Sprint 9**: Roll out comprehensive OpenTelemetry observability, configure automated alerting, and perform rigorous chaos testing on edge disconnects.
- **Technical Priorities**: Reliability of edge-to-cloud handoff; maintaining high throughput on ingest.
- **Risk Assessment**: Medium risk regarding achieving perfect multi-camera stream synchronization under severe packet loss conditions.
