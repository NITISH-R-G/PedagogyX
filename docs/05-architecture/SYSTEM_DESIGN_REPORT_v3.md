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
- **PedagogyX India Cloud (OSS Stack)**: Centralized backend handling heavy processing. Ingest gateways route data to asynchronous job queues for batch processing (transcoding, indexing, ML fusion) on GPU workers (`worker-cv`, `worker-metrics`, `worker-asr`), and store results in durable object storage and relational databases.
- **Control Plane**: An API Gateway with strict RBAC manages tenant isolation (K-12 vs University) and provides supervised access to raw video and analytical pedagogy scores.

### Architectural Decision: Edge-Cloud Hybrid Topology

- **Problem Statement**: Cloud-only ingest suffers from severe latency and complete service degradation during frequent school WAN outages.
- **Constraints**: Budget restricts deploying heavy GPU hardware directly into schools.
- **Tradeoffs**: Increased deployment complexity at the school level (running edge nodes) vs. extreme resilience and lower cloud ingestion spikes.
- **Alternatives Considered**: Direct-to-Cloud streaming (rejected due to WAN reliability), Thick Edge (rejected due to hardware cost).
- **Scalability Implications**: Edge nodes act as a distributed shock absorber, smoothing traffic before it hits the centralized cloud ingest gateways.
- **Operational Implications**: Requires robust remote-management and self-healing for the edge nodes, as on-site IT support is limited.
- **Cost Implications**: Significantly reduces peak bandwidth requirements on the cloud side, saving on transit costs. Requires small, cheap hardware (e.g., Raspberry Pi or low-end NUCs) per school.
- **Reliability Implications**: The system survives intermittent internet outages seamlessly.
- **Security Implications**: Requires secure tunnel provisioning (e.g., WireGuard/Tailscale) from edge to cloud, and local data encryption on the edge buffer.
- **Future Extensibility**: Edge nodes can be upgraded to run quantized, lightweight LLMs or local Whisper models as hardware costs drop, further reducing cloud compute reliance.

## Infrastructure Design

PedagogyX employs a globally-aware but locally-constrained infrastructure model.

- **Deployment Topology**: School edge nodes interface with a centralized Indian cloud infrastructure. Edge instances ensure latency-sensitive buffering and basic inference using limited local compute.
- **Cloud Architecture**: Kubernetes-based microservices architecture. High-performance ingest APIs written in Go reside at the edge and cloud gateway to handle mass concurrent connections. Python workers perform AI/ML tasks using the OSS stack.
- **Networking**: Audio acts as the master clock for stream synchronization across dispersed devices. UDP/WebRTC is utilized for the hot path, while resumable chunked HTTP/gRPC uploads handle the authoritative cold path over potentially unstable WAN links to the cloud.
- **Orchestration**: Kubernetes handles cloud auto-scaling of GPU worker nodes based on queue depth. Edge deployments are managed via simplified container orchestration (e.g., Docker Compose/K3s) for operational simplicity in low-tech environments.

### Architectural Decision: WebRTC vs Chunked HTTP for Ingest

- **Problem Statement**: Need to balance real-time feedback requirements with the necessity of guaranteed, lossless delivery for the authoritative batch AI analysis.
- **Constraints**: Unreliable school WAN connections; strict zero-data-loss requirement for the cold path.
- **Tradeoffs**: Dual-path complexity vs. meeting both latency and reliability SLAs.
- **Alternatives Considered**: Pure WebRTC with cloud-side recording (rejected due to packet loss corrupting final data), Pure HTTP chunking (rejected due to lack of real-time telemetry).
- **Scalability Implications**: WebRTC requires Stateful SFUs (scaling linearly with active streams), while HTTP chunking can use simple, highly scalable stateless load balancers.
- **Operational Implications**: Managing ICE negotiations and TURN servers adds network operational overhead.
- **Cost Implications**: Dual ingest increases local network utilization.
- **Reliability Implications**: The dual-path architecture isolates the critical cold-path data from the vagaries of real-time network jitter.
- **Security Implications**: Both streams require robust TLS/DTLS encryption.
- **Future Extensibility**: The WebRTC stream can later be used for bi-directional real-time teacher coaching (e.g., an earpiece prompt).

## Database Design

- **Schema Strategy**: Relational storage (Postgres) houses entity relationships, tenant RBAC matrices, and final structured pedagogy scores. Time-series data and event logs are optimized for append-only patterns.
- **Object Storage**: MinIO serves as the scalable object store for immutable video/audio chunk archives and final synced A/V artifacts.
- **Replication & Scaling**: Postgres utilizes read-replicas for admin dashboard queries, segregating heavy analytical reads from high-throughput write streams. Connection pooling (PgBouncer) prevents connection exhaustion from horizontally scaling edge/worker nodes.
- **Consistency Model**: Eventual consistency across the hot path. Strong consistency is enforced within the database transaction boundaries for the cold path final pedagogy scores, which act as the authoritative SLA metric.

### Architectural Decision: Postgres + MinIO vs Distributed NoSQL

- **Problem Statement**: Need to store large blobs (video/audio) alongside complex relational data (tenant hierarchies, RBAC, pedagogy scores) while maintaining transactional integrity.
- **Constraints**: OSS-first, self-hosted requirement. Avoid expensive managed database services.
- **Tradeoffs**: Operational overhead of managing Postgres and MinIO vs. the vendor lock-in and potential cost of managed NoSQL/Blob services.
- **Alternatives Considered**: MongoDB + GridFS (rejected due to poor relational data handling), Cassandra (rejected due to operational complexity for our current scale and need for ACID transactions on RBAC).
- **Scalability Implications**: MinIO scales horizontally with extreme ease. Postgres requires careful read-replica management and eventual logical sharding by tenant.
- **Operational Implications**: Requires robust Postgres backup/restore procedures (e.g., pgBackRest) and MinIO lifecycle management.
- **Cost Implications**: Self-hosting Postgres and MinIO drastically reduces OPEX compared to AWS RDS/S3 equivalents, especially given heavy video egress/ingress.
- **Reliability Implications**: MinIO provides erasure coding for high durability. Postgres requires synchronous replication for HA, which adds slight write latency.
- **Security Implications**: Both support AES-256 encryption at rest and integrate well with our IAM strategy.
- **Future Extensibility**: MinIO's S3 compatibility allows easy migration to the cloud if the self-hosted strategy changes. Postgres schema is easily extensible via migrations.

## Scalability Strategy

- **Horizontal Scaling**: Stateless Go ingest gateways and Python API services scale linearly based on CPU/traffic.
- **Queueing & Async**: Background workers (`worker-cv`, `worker-metrics`, `worker-asr`) use Redis-backed queues. A robust Dead Letter Queue (DLQ) pattern is implemented, capturing failed payloads and full tracebacks for resilience.
- **Caching**: Aggregated admin metrics and tenant structures are cached via Redis to reduce Postgres load during dashboard rendering.
- **Load Balancing**: L7 ingress controllers route traffic intelligently, while edge buffering smooths out bursty upload traffic generated at the end of class sessions.
- **Partitioning**: Multi-tenant database design logically partitions data by school/district, allowing future physical sharding if required by data volume.

### Architectural Decision: Redis-backed Async Worker Queues

- **Problem Statement**: AI processing (CV, ASR) is highly compute-intensive and bursty, often exceeding the capacity of available GPU resources during peak hours.
- **Constraints**: Strict compute budgeting (RTX 5070 GPU limits).
- **Tradeoffs**: Increased time-to-insight (eventual consistency) vs. the ability to handle massive spikes without dropping requests or over-provisioning hardware.
- **Alternatives Considered**: Synchronous processing (rejected due to immediate timeout and failure under load), Kafka (rejected due to operational complexity compared to Redis for simple task queueing).
- **Scalability Implications**: Workers can auto-scale based on queue depth up to the GPU limit. Unprocessed tasks simply queue up.
- **Operational Implications**: Requires monitoring Redis memory and queue depth SLAs. Dead Letter Queues (DLQs) must be actively managed to reprocess failed tasks.
- **Cost Implications**: Maximizes GPU utilization (cost efficiency) by keeping the pipeline saturated 24/7, smoothing out peak loads.
- **Reliability Implications**: If workers fail, tasks remain in the queue. DLQ pattern prevents poison pill messages from halting the pipeline.
- **Security Implications**: Redis must be secured and isolated within the backend network.
- **Future Extensibility**: Easy to add new specialized worker types (e.g., `worker-nlp`) by simply adding new queues and worker pools.

## Reliability Strategy

- **Failover & Redundancy**: Multi-AZ deployment within the Indian cloud region for Postgres and MinIO. Stateless application pods are ephemeral and easily rescheduled.
- **Resilience Patterns**: The LAN edge buffer acts as a massive bulkhead. If the WAN connection to the India cloud drops, the edge node spools data locally and resumes upload upon reconnection.
- **Recovery Mechanisms**: Strict DLQ implementation ensures no dropped frames or lost processing jobs. Comprehensive database backups and point-in-time recovery capabilities exist for the Postgres instances.
- **Graceful Degradation**: If GPU workers are saturated, the system degrades to showing only the hot path preview metrics while extending the SLA time for the batch authoritative metrics.

### Architectural Decision: Edge Buffering as a Bulkhead

- **Problem Statement**: School internet connectivity is notoriously unreliable, and lost capture data corrupts the AI models' accuracy.
- **Constraints**: Cannot rely on cloud-side ingest for guaranteed delivery during intermittent outages.
- **Tradeoffs**: Increased edge node complexity vs. guaranteed data integrity.
- **Alternatives Considered**: In-memory client buffering (rejected due to limited memory on Ray-Ban glasses and Smartboards).
- **Scalability Implications**: Decouples client ingest rates from cloud ingest rates.
- **Operational Implications**: Edge nodes require sufficient local storage (SSD) to buffer at least 48 hours of classroom data.
- **Cost Implications**: Increases the BOM (Bill of Materials) for the edge node hardware.
- **Reliability Implications**: Dramatically improves overall system reliability from the user's perspective. The system "just works" even when the internet is down.
- **Security Implications**: Buffered data on the edge must be encrypted at rest, as physical security in schools is low.
- **Future Extensibility**: The edge buffer logic can be adapted for mobile deployments (e.g., cellular edge nodes) with minimal changes.

## Security Architecture

- **Authentication**: Modern OAuth2/OIDC flows integrated with the API Gateway.
- **Authorization**: Strict, multi-tiered RBAC enforcing supervision modes. Teachers see their own data; Admins see aggregated district data with drill-down capabilities.
- **Data Protection & Encryption**: All data is encrypted in transit (TLS 1.3) and at rest (AES-256 for MinIO and Postgres). Strict adherence to India data residency laws. Real PII is fenced behind G2 legal gates.
- **Abuse Prevention**: Rate limiting at the Edge and Cloud gateways to prevent volumetric exhaustion. Strict payload validation ensures malformed A/V chunks are rejected early.

### Architectural Decision: Strict Multi-Tiered RBAC & Data Fencing

- **Problem Statement**: Handling sensitive classroom data (audio/video of minors) requires extreme care, and India's data residency and G2 legal restrictions are absolute.
- **Constraints**: G2 legal sign-off blocks production school data. Development is restricted to synthetic/MVP data.
- **Tradeoffs**: Complex implementation of access control logic vs. legal compliance and user trust.
- **Alternatives Considered**: Flat permission model (rejected due to massive privacy violations).
- **Scalability Implications**: RBAC checks must be highly performant (cached in Redis) to avoid becoming a bottleneck on every API request.
- **Operational Implications**: Requires comprehensive audit logging of all data access.
- **Cost Implications**: Negligible direct cost, high implementation cost.
- **Reliability Implications**: A failure in the RBAC service must "fail closed", denying access, rather than "failing open".
- **Security Implications**: Core to the platform's security posture. Mitigates insider threats and cross-tenant data leaks.
- **Future Extensibility**: The RBAC model can be extended to support parental access portals or specialized auditor roles.

## Observability Stack

- **Logging**: Structured JSON logging aggregated centrally. Worker tracebacks explicitly pushed to stderr and captured by the log aggregator alongside DLQ events.
- **Tracing**: Distributed tracing (OpenTelemetry) tracks the lifecycle of an A/V chunk from the Meta Ray-Ban client, through the edge buffer, into the cloud queue, and finally into the pedagogy score generation.
- **Monitoring & Alerting**: Prometheus and Grafana for metrics. Alerts are triggered on queue depth SLA violations, high error rates in processing, and edge node disconnection events.

### Architectural Decision: Audio-Master Clock Tracing

- **Problem Statement**: Correlating events from multiple discrete devices (Smartboard screen, Ray-Ban camera, teacher mic) across unpredictable networks is difficult.
- **Constraints**: Devices lack precise hardware clock synchronization.
- **Tradeoffs**: Increased processing complexity during the batch fusion phase vs. avoiding complex, brittle NTP-based synchronization protocols on unmanaged devices.
- **Alternatives Considered**: Forcing strict NTP sync on all clients (rejected due to impossibility on BYOD/unmanaged hardware).
- **Scalability Implications**: Shifts the burden of synchronization from the ingest phase to the asynchronous worker phase, which is already horizontally scalable.
- **Operational Implications**: Requires robust audio-fingerprinting and cross-correlation algorithms in the `worker-cv` / `worker-asr` pipelines.
- **Cost Implications**: Increases the compute time required for the initial fusion step.
- **Reliability Implications**: highly robust. Even if a device clock drifts significantly, the audio fingerprint acts as an absolute source of truth.
- **Security Implications**: None directly.
- **Future Extensibility**: Allows for the easy integration of new sensor types (e.g., student tablets) as long as they can capture a small snippet of ambient audio.

## Performance Optimization

- **Bottlenecks**: The primary bottleneck is WAN bandwidth from schools to the cloud and GPU inference compute limits.
- **Throughput Optimization**: Utilizing Go for the high-throughput LAN edge buffer and cloud gateway maximizes network I/O concurrency with minimal memory overhead.
- **Latency Optimization**: Edge processing handles immediate feedback loops, masking cloud latency. Audio is used as the master clock to efficiently cross-correlate and synchronize multi-stream events without heavy central compute overhead.

### Architectural Decision: Go for Ingest Gateways

- **Problem Statement**: Cloud and Edge ingest gateways must handle massive numbers of concurrent, long-lived connections (chunked uploads, WebRTC) with low memory footprint.
- **Constraints**: Limited compute resources, especially at the edge.
- **Tradeoffs**: Maintaining a polyglot codebase (Go for ingest, Python for AI) vs. the massive performance gains over Python for high-concurrency network I/O.
- **Alternatives Considered**: Node.js (rejected due to higher memory overhead than Go), Python/Asyncio (rejected due to GIL limitations and lower raw throughput).
- **Scalability Implications**: Go's goroutine model allows a single small instance to handle tens of thousands of concurrent connections.
- **Operational Implications**: Requires building Go deployment pipelines alongside Python pipelines.
- **Cost Implications**: Drastically reduces the number of compute instances required for the API Gateway layer.
- **Reliability Implications**: Go's strong typing and robust standard library lead to highly stable network services.
- **Security Implications**: Go's memory safety prevents a large class of vulnerabilities.
- **Future Extensibility**: Go is excellent for building further edge-networking infrastructure (e.g., custom VPN tunnels or local service discovery).

## Tradeoffs

- **Pros**: Massive scalability via Edge-Cloud separation; highly cost-efficient due to FOSS stack and lack of proprietary API usage; resilient to poor school internet connections.
- **Cons**: High engineering complexity in maintaining multi-stream sync and a reliable distributed edge architecture. Heavy reliance on asynchronous job queues increases the time-to-value for the final, authoritative scores.
- **Limitations**: The RTX 5070 GPU compute budget restricts the complexity of models run in parallel, necessitating the batch processing design. For PedagogyX, production school data is blocked until G2 legal sign-off. Development is strictly limited to docs, benchmarks, the MVP boilerplate stack, and synthetic test sessions.
- **Future Improvements**: Transitioning edge nodes to handle more complex intermediate feature extraction (e.g., running lightweight local Whisper models) to further reduce WAN payload size.

## Agile Sprint Plan

- **Phase 1: Foundation & Edge Ingest (Sprints 1-2)**: Deploy Go-based LAN edge buffer, establish basic Ray-Ban DAT client connectivity, and implement resumable WAN uploads. Verify MVP stack locally using `docker compose -f infra/compose.dev.yml up`.
- **Phase 2: Cloud Data Pipeline & Storage (Sprints 3-4)**: Deploy Postgres, MinIO, and Redis. Implement strict RBAC API Gateway and tenant partitioning.
- **Phase 3: Asynchronous AI Workers (Sprints 5-6)**: Implement Python workers (`worker-cv`, `worker-metrics`, `worker-asr`) with the DLQ pattern. Integrate the OSS models within the RTX 5070 constraints. Test `services/api` ensuring `API_KEY` is set.
- **Phase 4: Sync & Analytics (Sprints 7-8)**: Implement multi-stream audio-master clock synchronization. Develop the cold path batch ML fusion and final pedagogy scoring mechanisms. Ensure `dat-session-smoke` CI test passes using `tools/dat-session-sim/dat_session_cli.py`.
- **Phase 5: Observability & Hardening (Sprint 9)**: Deploy full OpenTelemetry tracing, establish alerting thresholds, and perform chaos engineering to test edge-disconnect resilience.
