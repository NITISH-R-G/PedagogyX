# Backend Architecture Report v3.0

**Date:** 2026-06-16
**Role:** Autonomous Senior Backend Developer & Distributed Systems Architect
**Context:** PedagogyX Phase 0 + MVP boilerplate, adapting to a growing deployment in India. Incorporating refined ASR and Metrics workers handling asynchronous chunk processing offloaded from Meta Ray-Ban glasses and edge Android devices.

## System & Requirement Analysis

- **Requirements:** Sustain high-throughput, chunked multimodal data ingest from edge Android devices and Meta Ray-Ban glasses. Decouple long-running ML workloads (ASR, Metrics, future CV) to run asynchronously using consumer-grade GPU compute (RTX 5070 limit per ADR-0006). Deliver low-latency API responses for dashboard read paths and enforce strict tenant-level (school/university) data isolation, adhering to local India data residency policies.
- **Constraints:** Extremely constrained central GPU compute ($0 per-classroom edge hardware budget), variable and unreliable edge network connections necessitating reliable chunk upload resumption, strictly OSS central AI stack.
- **Edge Cases:** Network disconnects during active session chunk uploads requiring clean resumption. Out-of-order chunk arrivals. Long queued processing times during peak school hours leading to extended polling/preview wait times. Queue poisoning from corrupted media chunks.
- **Scale Assumptions:** Phased rollout targeting increasing classrooms. The stateless API control plane must scale horizontally independently from the backpressure-absorbing worker pool.

## Backend Architecture

- **Services:**
  - `api`: FastAPI-based synchronous control plane. Handles session creation, metadata tracking, chunk ingestion directly to object storage, and serves dashboard query endpoints.
  - `worker-metrics`: Python background service continuously pulling from `jobs:talk_ratio`. Computes `teacher_talk_ratio` and `student_talk_ratio` based on generated transcripts.
  - `worker-asr`: Python background service orchestrating core speech-to-text transcription models (Whisper/stubbed mode) via `jobs:asr`.
  - `worker-cv`: Placeholder service intended for future Phase 2 video/computer vision inference.
- **APIs:** RESTful endpoints built with FastAPI under the `/v1/` namespace. Includes strict validation through Pydantic models.
- **Data Flow:** Capture Client -> Chunked HTTPS Uploads -> FastAPI -> MinIO (Storage via S3 protocol) -> PostgreSQL (Metadata). Upon session completion, FastAPI enqueues jobs in Redis -> `worker-asr` generates transcripts -> `worker-metrics` processes transcripts to calculate engagement ratios -> PostgreSQL (Results).
- **Event Systems:** Redis-backed queues acting as a scalable, high-throughput asynchronous event bus linking the fast ingest layer with the slow ML inference layer.
- **Abstractions:** Clear boundaries between the synchronous HTTP ingest/query layer and the asynchronous worker processing layer, utilizing Redis queues and Object Storage as the integration points.

## Database Design

- **Schema:** PostgreSQL relational schema managing `sessions`, `chunks`, `session_metrics`, and `session_transcripts`. Enforces data integrity through foreign keys mapping back to `tenant_id` and `school_id`.
- **Indexing:** Essential B-Tree indices applied to `session_id`, `school_id`, and `status` to ensure fast lookups for common dashboard queries. Uniqueness constraints on `session_id` within metric and transcript tables for idempotent inserts/updates.
- **Caching:** Future implementation of an in-memory caching layer (Redis) for frequently accessed tenant metadata and dashboard aggregates to minimize redundant database load.
- **Consistency Strategy:** Strong consistency enforced for session states and chunk metadata directly within PostgreSQL. Eventual consistency accepted for computationally heavy ML outputs.
- **Scaling Strategy:** Connection pooling (utilizing `psycopg2.pool.ThreadedConnectionPool` or external PgBouncer) to manage connection exhaustion from horizontally scaling workers and API instances.

## API Strategy

- **Endpoints:** Predictable RESTful paths (`/v1/sessions`, `/v1/schools/{id}/overview`, `/v1/sessions/{id}/preview`).
- **Validation:** Rigorous Pydantic schema validation enforcing types, checking boundaries (e.g., chunk index constraints), and setting maximum payload byte sizes at the ingestion boundary to prevent memory exhaustion.
- **Authentication:** Preparing for integration with standard OAuth2/OIDC protocols (to be activated during the G2 compliance phase).
- **Rate Limiting:** Network-layer rate limiting (IP and Tenant-based via Ingress/API Gateway) is critical to protect against bulk upload DoS attacks or misconfigured client retry loops.
- **Versioning:** URL-path versioning (`/v1/`) combined with semantic backward compatibility guarantees to avoid breaking distributed, disconnected edge Android clients.

## Scalability Strategy

- **Horizontal Scaling:** API layer is purely stateless and horizontally scales seamlessly via Kubernetes (or similar orchestrators) behind a standard load balancer.
- **Caching:** Aggressive pre-computation and caching of heavy dashboard overview aggregations.
- **Partitioning:** Logical data partitioning across tenants inside PostgreSQL, planning for eventual physical sharding or read-replica setups if dataset size grows.
- **Async Processing:** Heavy lifting is entirely offloaded. API endpoints respond rapidly with `job_enqueued` statuses. Clients utilize periodic polling or future WebSockets for real-time status updates.
- **Load Balancing:** Layer 7 load balancing to evenly distribute inbound API traffic and chunk ingest connections across available `api` pods.

## Reliability Strategy

- **Retries:** Exponential backoff and retry logic implemented on the client capture side for network volatility, and internally between workers connecting to database/storage layers.
- **Failover:** Health checks on the API (`/health`) route ensure automated failover by load balancers. Managed DB and Storage replication ensure data availability.
- **Redundancy:** Distributed state management. API nodes are fully redundant. Object storage utilizes multi-AZ replication in production.
- **Recovery Mechanisms:** Robust Dead Letter Queues (DLQs) such as `jobs:asr:dlq` and `jobs:talk_ratio:dlq` implemented in workers. This prevents malformed data from causing endless crash loops and queue poisoning, allowing manual inspection of failed jobs.

## Security Strategy

- **Authentication:** Edge IoT devices will require robust cryptographic identity verification to accept incoming payloads.
- **Authorization:** Granular RBAC validating tenant boundaries ensuring zero cross-tenant data spillage.
- **Validation:** "Never trust external input." All payloads are checked for byte size, MIME type, and schema correctness before processing.
- **Vulnerability Prevention:** Mandatory TLS 1.3 for data in transit. Enforced dependency scanning and automated static analysis tools (e.g., Ruff) integrated into the CI pipeline.

## Observability

- **Logging:** Structured JSON logs containing tracing context (`session_id`, `school_id`, `worker_mode`) emitted to stdout/stderr and collected by a centralized logging infrastructure (e.g., FluentBit to Loki/OpenSearch).
- **Tracing:** Architecture designed to support OpenTelemetry tracing across the HTTP request lifecycle, propagating through Redis into worker context.
- **Monitoring:** Critical metrics exported: Queue Depth (`blpop` wait times), API HTTP latency (p50/p95/p99), and Worker inference duration.
- **Alerting:** Automated alerts triggered on significant queue buildup, high DLQ ingestion rates, or sustained API 5xx errors.

## Performance Optimization

- **Bottlenecks:** Centralized GPU inference (RTX 5070 limit) is the known primary bottleneck. Mitigated by decoupled async architecture and extensive buffering via MinIO/Redis.
- **Query Optimization:** Eliminating N+1 query patterns. Worker services utilize open, shared database cursor state logically passed to helper functions.
- **Caching:** Avoiding repeated DB calls for slowly changing tenant configurations.
- **Concurrency Optimization:** Optimizing Python's GIL constraints in FastAPI by offloading blocking I/O (like MinIO writes) to thread pools (`asyncio.to_thread` / `run_in_threadpool`).

## Risks & Tradeoffs

- **Operational Risks:** Managing distributed background workers introduces complexity in deployment and tracing compared to a monolith. End-to-end debugging of a chunk's lifecycle requires advanced distributed tracing tools.
- **Scaling Concerns:** Depending on the speed of the ASR model on the RTX 5070, rapid school adoption could lead to extended insight delivery delays. Worker node scaling is limited by GPU availability.
- **Complexity Tradeoffs:** Adopting chunked uploads routed through the FastAPI layer rather than direct pre-signed S3 URLs places significant load on the API layer but provides absolute, immediate control and validation over incoming data formats, a critical requirement for early-stage rollout safety.

## Agile Sprint Plan

- **Sprint 1 (Current):** Solidify the async Redis worker architecture, robustly handle DLQ scenarios, and finalize the `worker-metrics` heuristics calculation.
- **Sprint 2:** Expand integration testing across the `api` and background workers to ensure correct boundary handling. Refine chunk upload limits.
- **Sprint 3:** Deploy and benchmark the ASR worker under simulated load against the RTX 5070 constraints. Optimize connection pooling configurations.
- **Sprint 4:** Prepare infrastructure for G2 data residency compliance audits. Implement rigorous RBAC and finalize security boundary hardening.
