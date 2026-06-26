# PedagogyX System Design Report v3

## System Overview

- **Purpose**: PedagogyX serves as a highly scalable, real-time multimodal AI classroom intelligence and teacher optimization platform. Its core mission is to securely capture, ingest, analyze, and store audio-visual telemetry from classrooms to deliver actionable pedagogical insights.
- **Requirements**: Provide both real-time (hot path) telemetry and deeply analyzed batch (cold path) metrics. Must run within a self-hosted FOSS ecosystem, strictly within India to meet data residency (G2) rules, support low-end edge endpoints (Windows Smartboards, Meta Ray-Ban on Android), and operate under a constrained RTX 5070 GPU compute budget.
- **Scale Assumptions**: Millions of users, significant burst traffic during typical classroom start/end times, high concurrent A/V stream ingest rates, resilient to intermittent or poor WAN connectivity at the edge.
- **Constraints**: No proprietary AI API usage. Complete tenant isolation. Deep cost efficiency given hardware budgets. Strict hardware constraints per worker node.

## High Level Architecture

- **Major Components**:
  1. Capture Layer: Meta Ray-Ban glasses, Android host DAT, Windows Smartboards.
  2. Edge Layer (LAN Edge Buffer): Go-based high-throughput ingestion gateways at the school level for stream buffering and localized hot-path feature generation.
  3. Cloud Layer (PedagogyX India OSS Stack): API Gateway, async queues, scalable Python GPU workers (CV, ASR, Metrics), Relational and Object storage.
  4. Control Plane: L7 load balancing, tenant configuration, and unified multi-tenant RBAC interfaces.
- **Interactions**: Capture clients stream continuously to local Edge Buffers via UDP/WebRTC. The Edge Buffer handles immediate analysis and coordinates resumable, chunked data uploads to the centralized Cloud Layer via HTTP/gRPC.
- **Data Flow**: Edge ingest -> local spooling -> centralized queue (Redis) -> GPU Worker processing -> results storage (Postgres/MinIO) -> Client consumption via GraphQL/REST API.
- **Service Boundaries**: Edge services (Ingest/Hot-path metrics) strictly separated from Cloud asynchronous heavy-lifting (ASR/CV Fusion). Control plane manages authorization completely separate from data-plane telemetry streams.

## Infrastructure Design

- **Deployment Topology**: A hybrid Edge-Cloud topology. Hundreds of K3s/Docker-Compose edge nodes in school districts feeding into a central highly-available Kubernetes (EKS/AKS equivalent) cluster in the India region.
- **Cloud Architecture**: Microservices oriented. Ingest and gateways utilize compiled languages (Go) for extreme I/O efficiency, while ML workers leverage Python ecosystems.
- **Networking**: Audio acts as the master sync clock. WebRTC for local lightweight viewing; resilient TCP/chunked upload (gRPC/HTTP) to overcome WAN flakiness between edge and cloud. Service mesh (e.g., Istio or Linkerd) internally handles mTLS and observability within the cloud.
- **Orchestration**: Kubernetes HPA dynamically scales GPU workers based on queue depth. Edge deployments are managed immutably using standard container configurations to simplify remote administration.

## Database Design

- **Schema Strategy**: Relational persistence via PostgreSQL. Strict referential integrity for RBAC, tenant models, and final analytical scoring. Usage of JSONB columns where schema flexibility is needed without sacrificing indexing.
- **Replication**: Multi-AZ PostgreSQL primary-replica architecture. Heavy dashboard reads are routed to read-replicas. Connection pooling via PgBouncer prevents connection exhaustion from horizontally scaled services.
- **Scaling**: Logical partitioning by tenant/district to limit blast radius and ease future physical sharding.
- **Consistency Model**: Eventual consistency for telemetry and queue processing; Strong ACID consistency for tenant configurations, RBAC, and final pedagogy scores.

## Scalability Strategy

- **Horizontal Scaling**: Stateless edge ingestion and cloud API gateways scale out automatically based on CPU/Memory thresholds. GPU ML workers scale based on Redis queue depth.
- **Caching**: Multi-tier caching. Redis handles session states, aggregated leaderboards, and query result caching to shield PostgreSQL from repeated complex aggregations.
- **Partitioning**: Multi-tenant data segregation at the database level. Queues logically partitioned to prevent single heavy tenants from starving others (Fair Queuing).
- **Load Balancing**: Global L7 Ingress for API routing and L4 load balancers for raw media ingest, handling sticky sessions where necessary for stream reassembly.

## Reliability Strategy

- **Failover**: Automated failover of database primaries. Stateless worker pods are instantly rescheduled upon node failure.
- **Redundancy**: High-availability configurations for all stateful services (Redis Sentinel/Cluster, Multi-AZ MinIO, Postgres Replicas).
- **Recovery Mechanisms**: Resumable edge buffering guarantees no data loss during WAN outages (Bulkhead pattern). Dead Letter Queues (DLQ) capture failed ML payloads for manual or automated retry after bug fixes.
- **Resilience Patterns**: Circuit breakers on third-party (OSS model) calls, timeout strategies on all external network boundaries, and graceful degradation (serving cached data or hot-path estimates when cold-path processing is delayed).

## Security Architecture

- **Authentication**: OIDC-compliant identity providers integrated into the API Gateway. JWTs used for stateless session verification.
- **Authorization**: Comprehensive RBAC enforcing strict data visibility constraints (Teacher vs Admin vs District Supervisor).
- **Encryption**: TLS 1.3 for all data in transit. AES-256 for data at rest across MinIO and PostgreSQL.
- **Abuse Prevention**: Strict rate limiting by IP and tenant at the Edge and Ingress levels. Input validation and payload scanning to reject malformed A/V chunks before reaching internal storage.

## Observability Stack

- **Logging**: Structured JSON logging aggregated centrally (e.g., FluentBit -> ELK/Loki). All DLQ errors include stack traces and execution contexts.
- **Tracing**: OpenTelemetry distributed tracing across the entire request lifecycle (Edge -> Gateway -> Queue -> Worker -> DB).
- **Monitoring**: Prometheus scraping metrics from all components. Node Exporters for hardware (especially GPU utilization).
- **Alerting**: Grafana dashboards with alerting on critical SLAs (e.g., end-to-end processing latency, queue buildup, edge node disconnection rates, 5xx error spikes).

## Performance Optimization

- **Bottlenecks**: Mitigating WAN upload limits via aggressive local edge compression and buffering. Circumventing GPU compute bottlenecks through strict batching and prioritization queues.
- **Latency Optimization**: Pushing hot-path analytics (talk ratios, voice activity) to the edge. Minimizing payload sizes through efficient codecs.
- **Throughput Optimization**: Go-based ingest layers handle tens of thousands of concurrent connections. Asynchronous processing removes waiting from the user request lifecycle.

## Tradeoffs

- **Pros**: Exceptionally resilient to network failures due to edge buffering. Highly cost-effective using OSS models and off-the-shelf GPU hardware. Highly scalable.
- **Cons**: High operational complexity in managing edge nodes. The reliance on asynchronous batch processing means authoritative data is delayed.
- **Limitations**: Bounded by the RTX 5070 GPU compute budget, preventing the use of heavier, monolithic multi-modal models in real-time.
- **Future Improvements**: Transitioning to lighter, quantized models at the edge for deeper local analysis. Implementing WebAssembly (Wasm) at the edge for safely deploying dynamic analytic logic without container rebuilds.

## Agile Sprint Plan

- **Milestones & Implementation Phases**:
  - **Sprint 1-2**: Infrastructure As Code (Terraform/Helm) setup for the Cloud Layer (Postgres, MinIO, Redis, K8s).
  - **Sprint 3-4**: Deployment of the Go-based LAN Edge Buffer and cloud Ingest API; end-to-end A/V chunk upload testing.
  - **Sprint 5-6**: Development and deployment of Python Async Workers (ASR, CV) and DLQ mechanisms.
  - **Sprint 7-8**: Implementation of the Cold Path batch fusion ML pipeline and authoritative Pedagogy scoring.
  - **Sprint 9**: Observability deployment, load testing, chaos engineering, and final security audit.
- **Technical Priorities**: Robust stream ingestion, queue reliability, and GPU utilization efficiency.
- **Risk Assessment**: The primary risk remains edge-node hardware failures and network unpredictability, heavily mitigated by the resumable buffer architecture.
