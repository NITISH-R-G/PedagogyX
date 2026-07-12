# PedagogyX System Design Report v3

## System Overview

PedagogyX is an elite, massive-scale multimodal AI classroom intelligence and teacher optimization platform designed under a Hybrid Edge-Cloud architecture. The system is engineered to capture audio and visual telemetry via low-power endpoints (primarily Meta Ray-Ban DAT smart glasses and rudimentary Windows Smartboards) in potentially hostile network environments (K-12 and university classrooms). The primary goal is to provide deeply analyzed pedagogy scoring, real-time feedback, and full transformer fusion analytics.

Operating under severe constraints—a strict open-source, non-proprietary AI stack, hard India data residency laws (G2 legal restrictions), and heavily bottlenecked compute budgets (RTX 5070 GPU limits)—this architecture assumes millions of concurrent users with massive ingestion spikes occurring universally at class dismissal times. It is optimized for absolute reliability under chaotic failure states, minimizing blast radius while aggressively pushing boundaries on cost efficiency and developer productivity.

## High Level Architecture

The architecture is structured around four decoupled, fault-tolerant tiers:

- **Capture Tier**: Stateless, low-compute edge devices (Meta Ray-Ban Android host DAT clients) operating as dumb terminals streaming raw, chunked A/V payloads.
- **LAN Edge Buffer (Survival Tier)**: Highly-concurrent Go-based ingest gateways deployed locally at the district/school level. These nodes perform real-time hot-path lightweight feature extraction (e.g., active speaker detection, WebRTC SFU telemetry) and provide a crucial massive local buffer to survive complete WAN degradation.
- **PedagogyX Central Cloud (Heavy Compute)**: A Kubernetes-orchestrated, globally aware but physically constrained (India-only) OSS stack. It features Python-based ML asynchronous worker fleets operating off decoupled queue systems to perform cold-path complex transformer fusions, speech-to-text, and visual analytics.
- **Control Plane & API Gateway**: A centralized ingress tier managing multi-tenant RBAC, traffic shaping, zero-trust authentication, and administrative query federation.

## Infrastructure Design

Infrastructure is designed as completely reproducible, infrastructure-as-code deployments optimizing for multi-region failovers (within Indian borders) and edge volatility.

- **Cloud Topology**: Multi-AZ Kubernetes clusters managing stateless application components. Autoscaling is aggressively tied to queue depth SLA metrics rather than simple CPU load.
- **Edge Deployment**: Docker Compose/K3s single-node deployments optimized for ultra-low operational overhead. Updates are pushed via immutable container images.
- **Networking**: Dual-path networking strategy. The Hot Path leverages WebRTC/UDP for sub-second telemetry delivery. The Cold Path leverages resumable, chunked gRPC/HTTP uploads built for immense backpressure and WAN instability. Audio signals act as a universal master clock to bypass complex distributed time-sync overhead.

## Database Design

The storage tier enforces strict separation between OLTP, object storage, and ephemeral state:

- **Relational Storage (Postgres)**: Serves as the ultimate source of truth for entity relationships, tenant isolation matrices, and finalized pedagogy scores. Structured with rigorous schema design, connection pooling (PgBouncer) to prevent N+1 connection thrashing from scaled workers, and read-replicas handling heavy admin dashboard queries.
- **Object Storage (MinIO)**: Highly scalable S3-compatible blob storage housing immutable A/V chunk archives. Buckets are strictly partitioned by tenant and lifecycle policies automate tiering.
- **Queue/State (Redis)**: Manages ephemeral hot-path state, distributed locking, and robust asynchronous job queues.
- **Consistency**: The system embraces Eventual Consistency for intermediate telemetry and Strong Consistency strictly enforced within Postgres transaction boundaries for the authoritative cold-path pedagogy SLA metrics.

## Scalability Strategy

The system scales completely horizontally across all axes, designed to absorb 100x traffic spikes seamlessly:

- **Horizontal Pod Autoscaling**: Stateless Go gateways and Python worker nodes scale automatically based on custom Redis queue metrics.
- **Decoupled Job Processing**: Heavy ML inference is fully asynchronous. A robust Dead Letter Queue (DLQ) topology prevents systemic failure from poison pills and enables non-destructive retry loops.
- **Traffic Shaping**: Edge nodes dynamically throttle upload bandwidth and queue depth based on cloud backpressure signaling, effectively flattening the curve of end-of-class mass upload events.
- **Caching**: Multi-level caching strategies via Redis for expensive aggregate admin dashboard queries, significantly reducing database I/O bottlenecks.

## Reliability Strategy

Failure is assumed as a constant. The system incorporates deep defense-in-depth reliability mechanisms:

- **Bulkhead Pattern**: The LAN edge buffer isolates WAN failures. If cloud connectivity severs, schools continue to capture and spool locally, resuming seamlessly upon reconnection without data loss.
- **Graceful Degradation**: If GPU worker queues exceed capacity (the RTX 5070 compute budget ceiling), the system intelligently downgrades to provide only hot-path preview metrics while temporarily relaxing SLAs on heavy batch analytics.
- **Circuit Breakers & Retries**: Exponential backoff and jitter on all inter-service communication to prevent cascading network failures or thundering herd scenarios.
- **Automated Failover**: Postgres high-availability and multi-AZ deployments ensure rapid RTO/RPO during infrastructure outages.

## Security Architecture

A zero-trust model enforcing strict data isolation and supervision:

- **Authentication & Authorization**: OIDC-based identity with deep multi-tiered RBAC. Teachers maintain sovereign access to their raw data, while admins access generalized telemetry unless explicit supervision scopes are requested.
- **Encryption**: TLS 1.3 enforced on all external endpoints. AES-256 encryption at rest for MinIO and Postgres.
- **Data Perimeter**: Strict logical partitioning per school/district tenant. Compliance with India G2 legal bounds is enforced programmatically; synthetic test sessions are clearly demarcated from production PII.
- **Abuse Prevention**: Distributed rate limiting at the ingress layer and robust payload validation to drop malformed streams instantly.

## Observability Stack

Operational visibility is prioritized to enable rapid incident resolution:

- **Distributed Tracing**: OpenTelemetry heavily instrumented across the entire lifecycle, tracing chunks from the Ray-Ban client through the edge buffer and into the worker queues.
- **Logging**: Structured JSON logging aggregated centrally. Stack traces are never swallowed; failed AI payloads are explicitly dumped to stderr and DLQs.
- **Monitoring & Alerting**: Prometheus and Grafana provide real-time dashboards on custom SLIs (queue lag, p99 latency, edge disconnect rates). Alerts are tuned to be highly actionable, minimizing alert fatigue.

## Performance Optimization

Relentless optimization targets edge network latency and central compute bottlenecks:

- **Edge Efficiency**: Go-based services maximize asynchronous I/O and network concurrency, dropping memory overhead significantly compared to interpreted languages.
- **Inference Optimization**: Multi-stream synchronization leverages the audio track as the master clock to bypass computationally expensive video cross-correlation.
- **Payload Compression**: Aggressive chunk compression and early filtering of silence/inactivity frames at the edge buffer drastically reduce WAN payload sizes.

## Tradeoffs

Architectural decisions balance massive scale with harsh constraints:

- **Cost vs. Latency**: Relying on heavily decoupled asynchronous queues maximizes the efficiency of the RTX 5070 budget but introduces high latency for authoritative cold-path metrics.
- **Complexity vs. Resilience**: Implementing a hybrid edge-cloud architecture introduces significant operational complexity in distributed deployments, but is an absolute necessity to guarantee reliability over poor K-12 WAN networks.
- **FOSS vs. Velocity**: The strict OSS-first AI stack limits the use of turnkey cloud APIs, demanding higher internal engineering investment for model tuning but ensuring long-term cost sustainability and absolute data sovereignty.
- **Future Improvements**: We aim to push heavier feature extraction (e.g., quantized Whisper deployments) directly to the edge nodes to further collapse WAN overhead and accelerate initial insights.

## Agile Sprint Plan

A prioritized, high-impact roadmap to production readiness:

- **Sprint 1-2 (Edge Resiliency)**: Harden the Go-based LAN edge buffer, optimizing resumable gRPC uploads and stress-testing the local spooling under simulated network drops.
- **Sprint 3-4 (Cloud Data & RBAC)**: Finalize Postgres schema optimizations for tenant isolation. Deploy API Gateway with strict OIDC/RBAC enforcement.
- **Sprint 5-6 (Async Compute Pipelines)**: Operationalize Python ML workers. Implement and load-test the Redis-backed DLQ patterns and autoscaling rules under RTX 5070 constraints.
- **Sprint 7-8 (Audio Sync & Fusion)**: Develop and profile the master-clock audio synchronization logic. Deploy the cold-path batch ML pedagogy scoring mechanisms.
- **Sprint 9 (Observability & Chaos)**: Complete OpenTelemetry instrumentation. Execute automated chaos engineering (killing edge nodes, saturating queues) to validate graceful degradation SLAs.
