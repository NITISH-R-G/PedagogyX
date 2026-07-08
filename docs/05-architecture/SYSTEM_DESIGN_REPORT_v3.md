# PedagogyX System Design Report v3

## System Overview

PedagogyX is a world-class, multimodal AI classroom intelligence and teacher optimization platform built on a Hybrid Edge-Cloud distributed architecture. Operating under strict constraints regarding data privacy, limited network bandwidth, and edge compute limits, the system processes massive concurrent audio and video streams.

The primary v1 client targets Meta Ray-Ban smart glasses (DAT) via Android hosts, streaming real-time telemetry (Hot Path) and batch authoritative analytics (Cold Path). The system is engineered to be highly fault-tolerant, globally scalable yet locally resilient, optimizing for operational excellence in high-friction environments with variable connectivity.

## High Level Architecture

The architecture is structured into a resilient four-tier model to ensure decoupled scaling and fault isolation:

- **Capture & Edge Tier:** Thin clients (Meta Ray-Ban POV via Android) stream over LAN to a robust Edge Buffer. This tier utilizes high-throughput Go services to ingest, normalize (FFmpeg), and buffer A/V chunks.
- **Ingestion & Gateway Tier:** A high-performance stateless API gateway manages tenant routing, authentication, and volumetric rate limiting, channeling data efficiently into asynchronous message queues.
- **Cloud ML Processing Tier:** An OSS-first backend executing the real-time (Hot Path - WebRTC/SFU for instant metrics) and batch (Cold Path - ASR, CV fusion via PyTorch/ONNX on RTX 5070 clusters) pipelines.
- **Storage & State Tier:** PostgreSQL (with pgvector) for structured state, tenant mapping, and RAG embeddings. MinIO handles immutable, scalable object storage for high-volume video/audio blobs.

## Infrastructure Design

Designed for multi-region scalability with immediate focus on India data residency (DPDP compliance):

- **Deployment Topology:** Kubernetes (K8s) serves as the core orchestration plane in the cloud, dynamically auto-scaling stateless worker nodes based on queue depth metrics. Edge nodes leverage k3s/Docker Compose for simplified, automated deployments.
- **Cloud Architecture:** Infrastructure-as-Code (IaC) manages all resources. Multi-AZ deployment ensures high availability.
- **Networking:** Asynchronous, event-driven design. UDP/WebRTC optimizes the Hot Path, while gRPC and resumable chunked HTTP ensure reliable Cold Path transfers over unreliable WAN.
- **Orchestration:** Advanced scheduling with node affinity ensures GPU workloads (RTX 5070) are fully saturated, maximizing cost efficiency for the AI inference pipeline.

## Database Design

Optimized for high-throughput writes and complex analytical reads:

- **Schema Strategy:** Event-sourced, append-only logs for classroom streams, combined with relational entity modeling for RBAC.
- **Scaling & Replication:** Master-Replica PostgreSQL topology with PgBouncer connection pooling to handle connection spikes from horizontally scaling workers. Read replicas isolate admin dashboard queries from the critical ingestion path.
- **Consistency Model:** Eventual consistency across Edge-Cloud sync; strong ACID consistency within authoritative grading and transaction boundaries.
- **Storage Tiering:** Ephemeral storage for raw A/V (purged post-inference for compliance), durable block storage for final embedding vectors and pedagogy metrics.

## Scalability Strategy

Built to accommodate millions of concurrent streams and unpredictable classroom schedules:

- **Horizontal Scaling:** API, Go ingest, and ML workers scale independently. Queue-driven autoscaling ensures elasticity against morning/afternoon traffic spikes.
- **Partitioning & Sharding:** Logical multi-tenant data partitioning by school/district, setting the foundation for future physical sharding.
- **Caching:** Multi-layered caching strategy using Redis for hot session state, API responses, and user RBAC, drastically reducing database load.
- **Load Balancing:** L7 routing with intelligent traffic shaping and backpressure mechanisms protects backend workers from being overwhelmed.

## Reliability Strategy

Designed for zero-downtime and graceful degradation:

- **Failover & Recovery:** Automated multi-AZ failover for Postgres and MinIO. Ephemeral stateless pods self-heal upon failure.
- **Resilience Patterns:** Circuit breakers, retry mechanisms with exponential backoff, and strict Dead Letter Queues (DLQs) prevent data loss during pipeline failures.
- **Edge Buffering:** The LAN Edge acts as a massive bulkhead, spooling data locally during WAN outages and reconciling asynchronously once connectivity is restored.
- **Graceful Degradation:** When GPU clusters are saturated, the system degrades to providing real-time Hot Path metrics only, queuing heavy Cold Path analysis without breaking the user experience.

## Security Architecture

Zero-trust security model enforcing defense-in-depth:

- **Authentication & Authorization:** Strict OIDC/OAuth2 protocols with fine-grained, tiered RBAC (Teacher vs. Admin).
- **Data Protection:** TLS 1.3 for data in transit; AES-256 for data at rest. Full compliance with Indian DPDP laws (G2).
- **Privacy By Design:** Automated purging of raw biometric data (faces, raw audio) immediately following vector embedding extraction.
- **Abuse Prevention:** Distributed rate limiting, payload signature verification, and automated DDoS mitigation at the Gateway.

## Observability Stack

Comprehensive, actionable insights driving operational excellence:

- **Tracing:** OpenTelemetry instruments end-to-end request lifecycle, tracking chunks from Ray-Bans through Edge to Cloud GPU inference.
- **Metrics:** Prometheus aggregates system metrics (p50/p95/p99 latency, GPU utilization, queue lag, DLQ depth).
- **Logging:** Structured JSON logs centralized for rapid querying, with integrated error tracking and traceback capture.
- **Alerting:** Automated, threshold-based alerting via Grafana targeting anomalous error rates and SLA breaches, minimizing noise and alert fatigue.

## Performance Optimization

Relentless focus on efficiency and latency reduction:

- **Throughput Optimization:** Go-based ingest services maximize concurrent I/O operations with minimal memory footprint. Asynchronous batching of database writes.
- **Latency Optimization:** Pushing lightweight VAD/telemetry to the Edge reduces perceived latency. Audio serves as the master clock for rapid A/V sync without heavy compute overhead.
- **Inference Optimization:** Utilizing ONNX/TensorRT quantization on RTX 5070 clusters maximizes batch processing speed and minimizes GPU memory bottlenecks.

## Tradeoffs

- **Edge Complexity vs. Cloud Cost:** Pushing logic to the Edge increases deployment complexity but significantly reduces cloud WAN bandwidth and inference costs.
- **Consistency vs. Availability:** Opting for eventual consistency in the Hot Path allows massive scale and availability, delaying authoritative metrics to the Cold Path.
- **FOSS vs. Managed AI APIs:** Building and maintaining a self-hosted OSS stack requires higher initial engineering investment but yields long-term cost efficiency, DPDP compliance, and vendor independence.
- **Future Improvements:** Transitioning to lightweight federated learning at the edge, optimizing video chunk sizes dynamically based on network bandwidth, and further quantization of ML models.

## Agile Sprint Plan

- **Sprint 1: Resilient Edge Foundation:** Harden the Go-based LAN Edge buffer, ensuring robust resumable uploads and local failover spooling for Meta Ray-Ban streams.
- **Sprint 2: Gateway & Control Plane:** Deploy the API Gateway with strict RBAC, rate limiting, and core OIDC integration. Establish baseline K8s cluster.
- **Sprint 3: Stateful Data Tier:** Provision highly available Postgres (with pgvector) and MinIO object storage. Implement Redis caching layer.
- **Sprint 4: Asynchronous Processing Pipeline:** Implement event-driven queues, background workers (ASR, CV), and strict DLQ monitoring.
- **Sprint 5: ML Inference Integration:** Deploy OSS PyTorch/ONNX models onto RTX 5070 clusters, optimizing batch sizes and concurrency limits.
- **Sprint 6: Synchronization & Analytics:** Implement audio-master clock synchronization and develop the final Cold Path pedagogy scoring algorithm.
- **Sprint 7: Observability & Hardening:** Deploy OpenTelemetry tracing, Prometheus metrics, and comprehensive alerting. Execute load testing and chaos engineering.
