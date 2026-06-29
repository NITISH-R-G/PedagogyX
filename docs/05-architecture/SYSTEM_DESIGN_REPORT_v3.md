# PedagogyX System Design Report v3

## System Overview

PedagogyX is an elite, multimodal AI-driven classroom intelligence and teacher optimization platform operating on a globally distributed, Hybrid Edge-Cloud architecture. Designed to process massive concurrent streams of audiovisual data in real-time, the system leverages Meta Ray-Ban smart glasses (via Android host clients) to capture high-fidelity classroom interactions. Operating primarily within the strict regulatory constraints of India's data residency laws (G2 compliance), PedagogyX ensures world-class privacy, scalability, and resilience.

The architecture supports a dual-path processing model:

- **Hot Path (Real-Time)**: Low-latency, lightweight telemetry providing immediate feedback loops (e.g., talk ratio estimates, activity detection) utilizing WebRTC SFU and edge feature workers.
- **Cold Path (Batch)**: Comprehensive, deeply-analyzed pedagogy scoring, multi-camera stream alignment, and transformer-based ML fusion stored durably in MinIO and PostgreSQL for authoritative reporting.

## High Level Architecture

The platform is organized into three distinct operational tiers, orchestrated via a centralized control plane:

- **Capture Layer**: Meta Ray-Ban glasses function as thin clients streaming securely to an Android host, supplemented by low-spec Windows Smartboards. These devices securely transmit screen, mic, and camera feeds over local networks.
- **LAN Edge Buffer**: Hybrid edge nodes deployed at the district or school level. These nodes ingest streams via high-throughput Go services, buffering data and executing lightweight hot-path analytics to provide resilience against intermittent WAN connectivity.
- **PedagogyX India Cloud (OSS Stack)**: A centralized, highly available backend infrastructure. High-performance Go ingest gateways route incoming data to robust, asynchronous Python job queues for batch processing (transcoding, indexing, ML fusion) on auto-scaled GPU workers (optimized for RTX 5070 budgets).
- **Control Plane**: A secure API Gateway featuring strict multi-tenant RBAC to isolate K-12 and University environments.

## Infrastructure Design

PedagogyX employs a globally-aware but locally-constrained infrastructure model engineered for massive scale and operational simplicity.

- **Deployment Topology**: School edge nodes interface with a centralized cloud infrastructure deployed across multiple availability zones in India. Edge instances are optimized for latency-sensitive operations using constrained compute.
- **Cloud Architecture**: A Kubernetes-native microservices ecosystem. High-performance Go ingest APIs at the edge and cloud gateway seamlessly manage mass concurrent connections. Python workers handle intensive AI/ML operations.
- **Networking**: Audio serves as the master synchronization clock for dispersed devices. UDP/WebRTC powers the hot path, while resumable, chunked HTTP/gRPC handles the authoritative cold path over unstable WAN links.
- **Orchestration**: Kubernetes auto-scales cloud GPU worker nodes based on Redis queue depth. Edge deployments utilize simplified orchestration (e.g., K3s or Docker Compose) to minimize operational overhead in low-tech environments.

## Database Design

The storage architecture is optimized for high throughput, data integrity, and complex analytical queries.

- **Schema Strategy**: PostgreSQL manages relational data, entity relationships, tenant RBAC matrices, and final structured pedagogy scores. Time-series data and event logs use append-only optimization patterns.
- **Object Storage**: MinIO provides an S3-compatible, horizontally scalable object store for immutable video/audio chunk archives and final synchronized artifacts.
- **Replication & Scaling**: PostgreSQL utilizes asynchronous read-replicas for admin dashboard queries, segregating heavy analytical workloads from high-throughput write streams. PgBouncer manages connection pooling to prevent exhaustion.
- **Consistency Model**: The system embraces eventual consistency for the hot path and enforces strong consistency within database transaction boundaries for cold path pedagogy scores, ensuring authoritative SLA metrics.

## Scalability Strategy

The system is designed to scale horizontally without bottlenecks, gracefully handling unpredictable spikes during typical classroom hours.

- **Horizontal Scaling**: Stateless Go ingest gateways and Python API services scale linearly based on CPU utilization and incoming traffic.
- **Queueing & Async**: Background AI workers (ASR, CV, Metrics) leverage Redis-backed asynchronous queues. A robust Dead Letter Queue (DLQ) pattern captures failed payloads for retry and analysis.
- **Caching**: Redis caches aggregated admin metrics and tenant RBAC structures to significantly reduce PostgreSQL load during dashboard rendering.
- **Partitioning**: Multi-tenant database schema logically partitions data by school/district, enabling seamless physical sharding when data volumes demand it.

## Reliability Strategy

Reliability is engineered at every layer to ensure zero data loss and high availability.

- **Failover & Redundancy**: Multi-AZ deployment within the Indian cloud region for PostgreSQL, Redis, and MinIO. Stateless application pods are ephemeral and instantly rescheduled upon failure.
- **Resilience Patterns**: The LAN edge buffer acts as a massive bulkhead. During WAN degradation, edge nodes spool data locally and seamlessly resume chunked uploads upon reconnection.
- **Recovery Mechanisms**: Strict DLQ implementation ensures no dropped frames or lost processing jobs. Comprehensive database backups and point-in-time recovery (PITR) guarantee rapid disaster recovery.
- **Graceful Degradation**: If GPU workers reach maximum saturation, the system degrades to providing only hot path preview metrics while dynamically extending the SLA for batch authoritative metrics.

## Security Architecture

Security is foundational, adhering to zero-trust principles and strict regulatory compliance.

- **Authentication**: Secure OAuth2/OIDC flows integrated directly with the API Gateway.
- **Authorization**: Multi-tiered RBAC enforces strict supervision modes. Teachers access only their own data, while Admins view aggregated metrics with governed drill-down capabilities.
- **Data Protection & Encryption**: All data is encrypted in transit (TLS 1.3) and at rest (AES-256 for MinIO and PostgreSQL). Adherence to India data residency laws is absolute, with PII fenced behind G2 legal gates.
- **Abuse Prevention**: Rate limiting at the Edge and Cloud gateways prevents volumetric exhaustion attacks. Strict payload validation ensures malformed A/V chunks are immediately rejected.

## Observability Stack

Comprehensive observability ensures rapid incident diagnostics and performance tuning.

- **Logging**: Structured JSON logging aggregated centrally. Worker tracebacks are explicitly pushed to stderr and captured by the log aggregator alongside critical DLQ events.
- **Tracing**: OpenTelemetry provides distributed tracing, tracking the entire lifecycle of an A/V chunk from the Meta Ray-Ban client, through the edge buffer, into the cloud queue, and finally into the database.
- **Monitoring & Alerting**: Prometheus and Grafana deliver real-time metrics. Automated alerts trigger on queue depth SLA violations, high error rates, GPU saturation, and edge node disconnections.

## Performance Optimization

Performance is meticulously tuned to minimize latency and maximize throughput.

- **Bottlenecks**: The primary architectural constraints are WAN bandwidth from schools to the cloud and GPU inference compute budgets.
- **Throughput Optimization**: High-throughput LAN edge buffers written in Go maximize network I/O concurrency with minimal memory footprint, efficiently handling massive ingress.
- **Latency Optimization**: Edge processing handles immediate feedback loops, masking cloud latency. Audio is utilized as the master clock to efficiently cross-correlate multi-stream events without heavy central compute overhead.

## Tradeoffs

Architectural decisions balance complexity, cost, and reliability.

- **Pros**: Massive scalability via Edge-Cloud separation; highly cost-efficient due to an OSS-first stack; extremely resilient to poor school internet connections.
- **Cons**: High engineering complexity in maintaining multi-stream synchronization and managing a globally distributed edge architecture. Heavy reliance on async queues increases time-to-value for final scores.
- **Limitations**: The strict RTX 5070 GPU compute budget restricts the complexity of parallel models, necessitating the dual-path design.
- **Future Improvements**: Transitioning edge nodes to handle more complex intermediate feature extraction (e.g., lightweight Whisper models) to further minimize WAN payload sizes and cloud GPU dependency.

## Agile Sprint Plan

An iterative approach to infrastructure engineering and deployment.

- **Phase 1: Edge Ingress & Resilience (Sprints 1-2)**: Deploy Go-based LAN edge buffer, establish Ray-Ban DAT client connectivity, and implement resumable WAN uploads.
- **Phase 2: Cloud Data Pipeline & Partitioning (Sprints 3-4)**: Deploy PostgreSQL, MinIO, and Redis. Implement RBAC API Gateway and logical tenant partitioning.
- **Phase 3: AI Worker Queues & DLQ (Sprints 5-6)**: Implement Python AI workers (ASR, CV, Metrics) with robust DLQ patterns. Optimize OSS models within the RTX 5070 constraints.
- **Phase 4: Stream Sync & Fusion (Sprints 7-8)**: Implement multi-stream audio-master clock synchronization. Develop batch ML fusion and final pedagogy scoring pipelines.
- **Phase 5: Observability & Chaos Engineering (Sprint 9)**: Deploy full OpenTelemetry tracing, establish Prometheus alerting thresholds, and execute chaos engineering to validate edge-disconnect resilience.
