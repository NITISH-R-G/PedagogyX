# Backend Architecture Report v2.0

**Date:** 2026-05-23
**Role:** Autonomous Senior Backend Developer & Distributed Systems Architect
**Context:** PedagogyX Phase 0 + MVP boilerplate, updated with Meta Ray-Ban (DAT) primary client path ([ADR-0009](../08-rfc-adr/ADR-0009-meta-rayban-primary-client.md)).

## System & Requirement Analysis

- **Requirements:** Support high-throughput multimodal ingest from Meta Ray-Ban glasses and edge Android devices, process live preview metrics, orchestrate cold path GPU ML inference (ASR, CV, LLM on RTX 5070), provide low-latency administrative dashboards, enforce India data residency, and ensure strict tenant (school/university) isolation.
- **Constraints:** ₹0 per-classroom edge hardware budget (pilot), central OSS-only ML stack, constrained central GPU compute (single RTX 5070 limit per ADR-0006), unreliable school internet connections.
- **Edge Cases:** Network disconnections during upload requiring chunk resumability, delayed ML processing due to queue bottlenecks, out-of-order stream synchronization.
- **Scale Assumptions:** Phased India rollout starting with pilot deployments, requiring architectural runway for horizontal scaling of the control plane and queue-based backpressure for the centralized ML pool.

## Backend Architecture

- **Services:**
  - `api`: FastAPI control plane for CRUD, session lifecycle, and chunked upload endpoints.
  - `worker-metrics`: Python background worker generating live "preview" metrics.
  - `worker-asr`: Python background worker orchestrating audio transcription (stubbed/Whisper).
  - `worker-cv`: Python background worker stub for Phase 2 video processing.
- **APIs:** RESTful endpoints (`/v1/sessions/*`) for session lifecycle, synchronous preview retrieval, and chunked binary uploads.
- **Data Flow:** Capture Client (Android DAT Host) -> Chunked HTTPS Uploads -> API Gateway -> MinIO (Storage) -> Redis (Job Queue) -> Python Worker Pool (ASR/Metrics/CV) -> PostgreSQL (Scores) -> Web Dashboards.
- **Event Systems:** Redis-backed queues acting as the asynchronous event bus between API session completion and background workers.
- **Abstractions:** Strict separation between ingest (hot/cold buffers) and downstream ML processing to absorb demand spikes.

## Database Design

- **Schema:** PostgreSQL relational schema managing `tenant_id`, `school_id`, `session_id`, `chunk_metadata`, and `metrics` structured strictly with Foreign Keys.
- **Indexing:** B-Tree indices on `session_id`, `school_id`, and `status` to optimize common dashboard lookups.
- **Caching:** In-memory caching for tenant metadata, moving toward Redis-based session caching.
- **Consistency Strategy:** Strong consistency for session states and chunk metadata (PostgreSQL); eventual consistency for ML outputs and aggregated scores.
- **Scaling Strategy:** Connection pooling (e.g., PgBouncer) to prevent worker-side connection starvation. Future read-replicas for dashboard queries.

## API Strategy

- **Endpoints:** Clean REST `/v1/` routing (e.g., `/v1/sessions`, `/v1/sessions/{id}/chunks/{idx}`).
- **Validation:** Pydantic models enforcing rigid data typing, bounds checking (e.g., `chunk_index` limits), and payload size limits.
- **Authentication:** OAuth2/OIDC integration (planned for G2 compliance phase).
- **Rate Limiting:** IP-based and Tenant-based rate limiting on the API Gateway to prevent DoS via bulk uploads.
- **Versioning:** URL-level versioning (`/v1/`) to guarantee backward compatibility with deployed Android apps.

## Scalability Strategy

- **Horizontal Scaling:** Stateless FastAPI nodes scaled horizontally behind a Load Balancer.
- **Caching:** Pre-computing complex dashboard aggregations to reduce OLTP load.
- **Partitioning:** Tenant-based logical data partitioning in the schema design.
- **Async Processing:** Complete decoupling of ML inference. Clients poll or use WebSockets for results instead of blocking HTTP requests.
- **Load Balancing:** L7 routing spreading ingest traffic across multiple API instances.

## Reliability Strategy

- **Retries:** Exponential backoff implemented in capture clients (Android) and inter-service ML workers.
- **Failover:** Stateless API design ensures traffic smoothly shifts during node failures.
- **Redundancy:** Replicated PostgreSQL (planned) and Multi-AZ object storage.
- **Recovery Mechanisms:** Dead Letter Queue (DLQ) implementations for failed worker jobs (e.g., `client.rpush(f"{JOB_QUEUE}:dlq", raw)`) preventing queue poisoning.

## Security Strategy

- **Authentication:** Strong cryptographic identities for IoT/Edge devices.
- **Authorization:** Rigid RBAC enforcing tenant boundaries (Supervision Mode constraints).
- **Validation:** No external input trusted; rigid schema validation via FastAPI/Pydantic.
- **Vulnerability Prevention:** Pre-commit linters (Ruff) and planned dependency scanning. HTTPS strictly enforced.

## Observability

- **Logging:** Structured JSON logs to standard output/error, aggregating to a centralized SIEM. Traces include `session_id` and `worker_mode`.
- **Tracing:** OpenTelemetry integration (planned) for request lifecycle tracing across API and Workers.
- **Monitoring:** Exporting metrics for queue depth, worker latency, and upload success rates.
- **Alerting:** PagerDuty integration for DLQ spikes or API health endpoint failures.

## Performance Optimization

- **Bottlenecks:** Centralized GPU inference (RTX 5070) identified as the primary throughput bottleneck. Addressed via asynchronous queueing.
- **Query Optimization:** Avoiding N+1 queries by passing active DB cursors to helper functions within background workers.
- **Caching:** Aggressive caching of static tenant configurations.
- **Concurrency Optimization:** Optimizing Uvicorn thread pools and chunk upload streams to minimize memory pressure.

## Risks & Tradeoffs

- **Operational Risks:** Hybrid Edge/Cloud architecture increases operational complexity and debugging difficulty.
- **Scaling Concerns:** Python's GIL overhead in FastAPI during massive concurrent chunk uploads.
- **Complexity Tradeoffs:** Choosing HTTP chunked uploads over direct-to-S3 signed URLs simplifies Edge client logic but increases API gateway load. Tradeoff accepted to maintain strict validation and control over the ingest buffer.

## Agile Sprint Plan

- **Sprint 1 (Current):** Refine MVP API ingest, stabilize MinIO storage, and establish asynchronous Redis worker queues for metrics.
- **Sprint 2:** Complete Meta Ray-Ban (DAT) end-to-end integration, implement robust DLQs, and finalize RBAC schema for school supervision modes.
- **Sprint 3:** Deploy initial cloud staging environment, benchmark RTX 5070 queue latency, and harden API rate limiting.
- **Sprint 4:** G2 compliance audit, DPDP data handling review, and production infrastructure freeze.
