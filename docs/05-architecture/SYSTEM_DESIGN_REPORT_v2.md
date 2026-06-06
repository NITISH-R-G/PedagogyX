# PedagogyX System Design Report

## System Overview

PedagogyX is a multimodal AI classroom intelligence and teacher optimization platform operating on a Hybrid Edge-Cloud model. The primary v1 client utilizes Meta Ray-Ban smart glasses (DAT) running via an Android host to capture classroom audio and visual data. This data is ingested through a LAN edge buffer using high-throughput Go services and forwarded to a centralized, OSS-first AI backend in India.

The system supports two processing paths:

1. **Real-Time (Hot Path)**: Provides lightweight immediate telemetry (e.g., talk ratio estimates, activity detection) via webRTC SFU and edge feature workers.
2. **Batch (Cold Path)**: Provides authoritative, deeply-analyzed pedagogy scoring, multi-cam stream alignment, full transformer fusion, and comprehensive analytics stored in MinIO and Postgres.

Constraints include operating within a self-hosted FOSS ecosystem without proprietary AI APIs, maintaining strict India data residency boundaries (G2 legal restrictions), accommodating low-end endpoint hardware, and strict compute budgeting on GPU usage. Scale assumptions include massive concurrent AV stream ingestions and processing spikes during typical classroom hours.

## High Level Architecture

The platform is organized into three major layers plus a control plane:

- **Capture Layer**: Meta Ray-Ban glasses acting as thin clients streaming to an Android host, complemented by low-spec Windows Smartboards. These devices stream screen, mic, and camera feeds.
- **Edge Buffer (LAN Edge)**: Hybrid edge nodes deployed at the district/school level. These nodes handle stream ingest, buffering, and lightweight hot-path analytics, providing resilience against WAN failures.
- **PedagogyX India Cloud (OSS Stack)**: Centralized backend handling heavy processing. Ingest gateways route data to asynchronous job queues for batch processing (transcoding, indexing, ML fusion) on GPU workers, and store results in durable object storage and relational databases.
- **Control Plane**: An API Gateway with strict RBAC manages tenant isolation (K-12 vs University) and provides supervised access to raw video and analytical pedagogy scores.

## Infrastructure Design

PedagogyX employs a globally-aware but locally-constrained infrastructure model.

- **Deployment Topology**: School edge nodes interface with a centralized Indian cloud infrastructure. Edge instances ensure latency-sensitive buffering and basic inference using limited local compute.
- **Cloud Architecture**: Kubernetes-based microservices architecture. High-performance ingest APIs written in Go reside at the edge and cloud gateway to handle mass concurrent connections. Python workers perform AI/ML tasks using the OSS stack.
- **Networking**: Audio acts as the master clock for stream synchronization across dispersed devices. UDP/WebRTC is utilized for the hot path, while resumable chunked HTTP/gRPC uploads handle the authoritative cold path over potentially unstable WAN links to the cloud.
- **Orchestration**: Kubernetes handles cloud auto-scaling of GPU worker nodes based on queue depth. Edge deployments are managed via simplified container orchestration (e.g., Docker Compose/K3s) for operational simplicity in low-tech environments.

## Database Design

- **Schema Strategy**: Relational storage (Postgres) houses entity relationships, tenant RBAC matrices, and final structured pedagogy scores. Time-series data and event logs are optimized for append-only patterns.
- **Object Storage**: MinIO serves as the scalable object store for immutable video/audio chunk archives and final synced A/V artifacts.
- **Replication & Scaling**: Postgres utilizes read-replicas for admin dashboard queries, segregating heavy analytical reads from high-throughput write streams. Connection pooling (e.g., PgBouncer) prevents connection exhaustion from horizontally scaling edge/worker nodes. Avoid N+1 connection overhead by passing cursors to helper methods.
- **Consistency Model**: Eventual consistency across the hot path. Strong consistency is enforced within the database transaction boundaries for the cold path final pedagogy scores, which act as the authoritative SLA metric.

## Scalability Strategy

- **Horizontal Scaling**: Stateless Go ingest gateways and Python API services scale linearly based on CPU/traffic.
- **Queueing & Async**: Background workers (ASR, CV, Metrics) use Redis-backed queues. A robust Dead Letter Queue (DLQ) pattern is implemented, capturing failed payloads and full tracebacks for resilience.
- **Caching**: Aggregated admin metrics and tenant structures are cached via Redis to reduce Postgres load during dashboard rendering.
- **Load Balancing**: L7 ingress controllers route traffic intelligently, while edge buffering smooths out bursty upload traffic generated at the end of class sessions.
- **Partitioning**: Multi-tenant database design logically partitions data by school/district, allowing future physical sharding if required by data volume.

## Reliability Strategy

- **Failover & Redundancy**: Multi-AZ deployment within the Indian cloud region for Postgres and MinIO. Stateless application pods are ephemeral and easily rescheduled.
- **Resilience Patterns**: The LAN edge buffer acts as a massive bulkhead. If the WAN connection to the India cloud drops, the edge node spools data locally and resumes upload upon reconnection.
- **Recovery Mechanisms**: Strict DLQ implementation ensures no dropped frames or lost processing jobs. Comprehensive database backups and point-in-time recovery capabilities exist for the Postgres instances.
- **Graceful Degradation**: If GPU workers are saturated, the system degrades to showing only the hot path preview metrics while extending the SLA time for the batch authoritative metrics.

## Security Architecture

- **Authentication**: Modern OAuth2/OIDC flows integrated with the API Gateway.
- **Authorization**: Strict, multi-tiered RBAC enforcing supervision modes. Teachers see their own data; Admins see aggregated district data with drill-down capabilities.
- **Data Protection & Encryption**: All data is encrypted in transit (TLS 1.3) and at rest (AES-256 for MinIO and Postgres). Strict adherence to India data residency laws. Real PII is fenced behind G2 legal gates.
- **Abuse Prevention**: Rate limiting at the Edge and Cloud gateways to prevent volumetric exhaustion. Strict payload validation ensures malformed A/V chunks are rejected early.

## Observability Stack

- **Logging**: Structured JSON logging aggregated centrally. Worker tracebacks explicitly pushed to stderr and captured by the log aggregator alongside DLQ events.
- **Tracing**: Distributed tracing (e.g., OpenTelemetry) tracks the lifecycle of an A/V chunk from the Meta Ray-Ban client, through the edge buffer, into the cloud queue, and finally into the pedagogy score generation.
- **Monitoring & Alerting**: Prometheus and Grafana for metrics. Alerts are triggered on queue depth SLA violations, high error rates in processing, and edge node disconnection events.

## Performance Optimization

- **Bottlenecks**: The primary bottleneck is WAN bandwidth from schools to the cloud and GPU inference compute limits.
- **Throughput Optimization**: Utilizing Go for the high-throughput LAN edge buffer and cloud gateway maximizes network I/O concurrency with minimal memory overhead.
- **Latency Optimization**: Edge processing handles immediate feedback loops, masking cloud latency. Audio is used as the master clock to efficiently cross-correlate and synchronize multi-stream events without heavy central compute overhead.

## Tradeoffs

- **Pros**: Massive scalability via Edge-Cloud separation; highly cost-efficient due to FOSS stack and lack of proprietary API usage; resilient to poor school internet connections.
- **Cons**: High engineering complexity in maintaining multi-stream sync and a reliable distributed edge architecture. Heavy reliance on asynchronous job queues increases the time-to-value for the final, authoritative scores.
- **Limitations**: The RTX 5070 GPU compute budget restricts the complexity of models run in parallel, necessitating the batch processing design.
- **Future Improvements**: Transitioning edge nodes to handle more complex intermediate feature extraction (e.g., running lightweight local Whisper models) to further reduce WAN payload size.

## Agile Sprint Plan

- **Phase 1: Foundation & Edge Ingest (Sprints 1-2)**: Deploy Go-based LAN edge buffer, establish basic Ray-Ban DAT client connectivity, and implement resumable WAN uploads.
- **Phase 2: Cloud Data Pipeline & Storage (Sprints 3-4)**: Deploy Postgres, MinIO, and Redis. Implement strict RBAC API Gateway and tenant partitioning.
- **Phase 3: Asynchronous AI Workers (Sprints 5-6)**: Implement Python workers (ASR, CV) with the DLQ pattern. Integrate the OSS models within the RTX 5070 constraints.
- **Phase 4: Sync & Analytics (Sprints 7-8)**: Implement multi-stream audio-master clock synchronization. Develop the cold path batch ML fusion and final pedagogy scoring mechanisms.
- **Phase 5: Observability & Hardening (Sprint 9)**: Deploy full OpenTelemetry tracing, establish alerting thresholds, and perform chaos engineering to test edge-disconnect resilience.
