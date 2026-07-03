# AI System Architecture Report

## System Overview

PedagogyX is a mission-critical, multimodal AI classroom intelligence platform designed to analyze classroom sessions (voice, video, slides, student engagement) and measure pedagogical efficiency. Operating at scale, it processes immense streams of real-time and batch multimedia data from high-throughput edge clients (primarily Meta Ray-Ban via the DAT client app on Android). The platform is built to operate securely in privacy-sensitive environments, ensuring data compliance and zero-trust policies, especially critical as production school data is blocked until G2 (India legal sign-off). The system architecture embraces world-class infrastructure patterns for massively scalable, fault-tolerant execution.

## High Level Architecture

The PedagogyX architecture leverages an event-driven microservices pattern with a split between real-time inference (Hot Path) and batch intelligence (Cold Path) to optimize inference efficiency and cost.

- **Client Tier**: Meta Ray-Ban glasses capturing rich streams of audiovisual data via Android DAT clients.
- **API Gateway (FastAPI)**: A high-performance, strictly-typed ingress layer managing traffic routing, authentication, rate limiting, and request validation.
- **Real-Time Hot Path**: Low-latency edge and centralized inference services (e.g., YOLO) for immediate classroom engagement feedback.
- **Batch Cold Path**: Centralized OSS offline inference backend (e.g., faster-whisper, Ollama) running heavily parallelized compute tasks on durable message queues.
- **Core Services**: Domain-isolated microservices (`web`, `api`, `worker-cv`, `worker-metrics`, `worker-asr`).
- **Frontend Tier**: React and Next.js for high-fidelity educator dashboards and intelligence visualization.

## Infrastructure Design

Designed for multi-region resilience and extreme scalability.

- **Kubernetes Orchestration**: Core workloads deployed on a managed Kubernetes service across isolated availability zones.
- **GPU Node Pools**: Dedicated autoscaling node pools handling deep learning inference. Traffic routing isolates CPU and GPU tasks efficiently.
- **Container Registry & CI/CD**: Immutable artifact deployments managed through advanced GitOps (ArgoCD or Flux) ensuring zero-downtime canary rollouts.
- **Service Mesh**: Istio or Linkerd to manage mTLS, detailed traffic telemetry, and fine-grained access control across the cluster.
- **Edge Infrastructure**: A global CDN routing frontend assets to minimize latency, with edge-optimized TLS termination.

## Database Design

A polyglot persistence strategy ensuring optimal read/write access paths.

- **Relational Datastore (PostgreSQL)**: Handles core domain models, tenant management, and user configurations ensuring strong consistency (ACID).
- **Time-Series / Analytics DB (ClickHouse / TimescaleDB)**: Stores high-frequency multimodal metrics (e.g., classroom engagement scores over time) optimized for OLAP aggregations.
- **Blob Storage (S3-compatible)**: Secure, immutable storage for raw media assets (audio, video) with strict lifecycle policies and encryption at rest.
- **In-Memory Cache (Redis)**: Acts as a high-throughput session cache and coordinates distributed locking for ephemeral state.

## Scalability Strategy

Built to accommodate millions of edge devices and unpredictable traffic spikes.

- **Horizontal Pod Autoscaling (HPA)**: Metric-driven scaling of `api` and worker nodes based on CPU/Memory and custom queue length metrics (KEDA).
- **Asynchronous Queues (Kafka / RabbitMQ)**: Decouples ingestion from inference. Heavy workloads (ASR, CV) are processed via durable backpressure-handling message queues.
- **Read Replicas**: Database query offloading for analytics dashboards via asynchronous replication topologies.
- **Stateless Services**: All `api` and web layer components are completely stateless, allowing frictionless vertical and horizontal scaling.

## Reliability Strategy

Assuming constant infrastructure failures to maintain high availability.

- **Circuit Breakers & Retries**: Implemented aggressively around external API calls and heavy GPU inference boundaries.
- **Graceful Degradation**: If the `worker-cv` system is overwhelmed or fails, the core system continues basic ASR logging without dropping the session.
- **Redundancy**: Multi-AZ deployments with active-active service architectures. Data is continuously replicated and snapshot-backed.
- **Dead Letter Queues (DLQ)**: Failed AI inference tasks are securely isolated for manual review and retry, ensuring zero data loss.

## Security Architecture

A zero-trust model safeguarding highly sensitive student data.

- **Data Privacy**: Strict anonymization pipelines at the edge. No PII is logged; full compliance with legal constraints (G2 sign-off boundaries).
- **Authentication & IAM**: OAuth2 / OIDC via strict RBAC. API gateways enforce least-privilege access tokens.
- **Encryption**: TLS 1.3 for all data in transit. AES-256 for all data at rest. Secrets managed dynamically via HashiCorp Vault or AWS Secrets Manager.
- **DDoS Resilience**: Edge-level web application firewalls (WAF) and strict API rate limiting to mitigate abuse.

## Observability Stack

Comprehensive, low-noise monitoring for rapid incident diagnostics.

- **Distributed Tracing (OpenTelemetry)**: Full request lifecycles traced from the client, through the API, to the asynchronous workers.
- **Metrics (Prometheus / Grafana)**: Real-time dashboards monitoring p50/p95/p99 latency, inference throughput, error rates, and GPU utilization.
- **Centralized Logging (ELK / Loki)**: Structured JSON logging across all microservices.
- **Alerting**: Actionable alerts mapped to SLIs/SLOs to prevent pager fatigue, with automated incident creation.

## Performance Optimization

Relentless tuning across the entire stack.

- **Inference Optimization**: Utilizing TensorRT and ONNX runtimes on the Cold Path for maximum throughput per GPU hour.
- **Payload Compression**: Aggressive gRPC / Protobuf adoption for internal service communication to reduce network I/O.
- **Caching**: Multi-level caching (CDN for static, Redis for dynamic) to guarantee sub-100ms dashboard rendering.
- **Query Tuning**: Strict indexing policies, query analysis, and continuous vacuuming on PostgreSQL to prevent database lock contention.

## Tradeoffs

- **Complexity vs. Maintainability**: Event-driven microservices introduce operational complexity but are strictly required to scale CPU-bound API tasks independently of GPU-bound workers.
- **Latency vs. Cost**: Shifting heavy models (faster-whisper) to the Cold Path increases time-to-insight for educators but drastically reduces expensive idle GPU costs.
- **Consistency vs. Availability**: Using eventual consistency for analytics dashboards allows higher availability and ingestion throughput during traffic spikes.

## Agile Sprint Plan

- **Sprint 1: Foundational Infrastructure**: Provision multi-AZ Kubernetes clusters, core database instances, and CI/CD deployment pipelines.
- **Sprint 2: Ingestion & API Layer**: Deploy the FastAPI ingress with strict security controls, rate limiting, and Redis caching.
- **Sprint 3: AI Inference Workers**: Stand up the asynchronous message queues and deploy the `worker-asr` and `worker-cv` services on GPU nodes.
- **Sprint 4: Observability & Resilience**: Implement full OpenTelemetry tracing, configure circuit breakers, and conduct chaos engineering (fault-injection) tests.
- **Sprint 5: Scale & Load Testing**: Execute high-concurrency simulated traffic runs to tune autoscaling policies and database connection pools.
