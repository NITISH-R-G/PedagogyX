# Backend Architecture Report v3.0

**Date:** 2026-05-24
**Role:** Autonomous Senior Backend Developer & Distributed Systems Architect
**Context:** PedagogyX Phase 0 + MVP boilerplate, updated with Meta Ray-Ban (DAT) primary client path ([ADR-0009](../08-rfc-adr/ADR-0009-meta-rayban-primary-client.md)), and threaded connection pooling for robust database operations.

## System & Requirement Analysis

- **Requirements:** Support high-throughput multimodal ingest from Meta Ray-Ban glasses and edge Android devices, process live preview metrics, orchestrate cold path GPU ML inference (ASR, CV, LLM on RTX 5070), provide low-latency administrative dashboards, enforce India data residency, and ensure strict tenant (school/university) isolation. Must ensure zero silent failures or connection starvation during Postgres DB interactions.
- **Constraints:** ₹0 per-classroom edge hardware budget (pilot), central OSS-only ML stack, constrained central GPU compute (single RTX 5070 limit per ADR-0006), unreliable school internet connections.
- **Edge Cases:** Network disconnections during upload requiring chunk resumability, delayed ML processing due to queue bottlenecks, out-of-order stream synchronization, and connection dropping or transactional conflicts during context manager yielding.
- **Scale Assumptions:** Phased India rollout starting with pilot deployments, requiring architectural runway for horizontal scaling of the control plane and queue-based backpressure for the centralized ML pool. Production traffic requiring reliable connection pooling and transaction rollbacks without swallowing the underlying SQL errors.

## Backend Architecture

- **Services:**
  - `api`: FastAPI control plane for CRUD, session lifecycle, and chunked upload endpoints. It handles synchronous database interactions via threadpool to avoid blocking the async event loop.
  - `worker-metrics`: Python background worker generating live "preview" metrics.
  - `worker-asr`: Python background worker orchestrating audio transcription (stubbed/Whisper).
  - `worker-cv`: Python background worker stub for Phase 2 video processing.
- **APIs:** RESTful endpoints (`/v1/sessions/*`) for session lifecycle, synchronous preview retrieval, and chunked binary uploads. DAT session routes and primary session upload endpoints using simple `HTTPBearer` authentication for MVP.
- **Data Flow:** Capture Client (Android DAT Host) -> Chunked HTTPS Uploads -> API Gateway -> Pydantic validation -> Database connection yield from `get_conn()` -> Direct SQL execution -> Commit or explicit Rollback on `psycopg2.Error` -> MinIO (Storage) -> Redis (Job Queue) -> Python Worker Pool (ASR/Metrics/CV) -> PostgreSQL (Scores) -> Web Dashboards.
- **Event Systems:** Redis-backed queues acting as the asynchronous event bus between API session completion and background workers. Minimal event tracking in `dat_session_events` to mirror Meta Wearables DAT lifecycle.
- **Abstractions:** Strict separation between ingest (hot/cold buffers) and downstream ML processing to absorb demand spikes. Thin abstraction over standard `psycopg2` context managers; explicit control over transaction boundaries within the route handlers, now utilizing eager `ThreadedConnectionPool` initialization.

## Database Design

- **Schema:** PostgreSQL relational schema managing `tenant_id`, `school_id`, `session_id`, `chunk_metadata`, `dat_sessions`, `dat_session_events`, and `metrics` structured strictly with Foreign Keys, optimized for rapid insertion of chunk metadata and temporal state transitions.
- **Indexing:** B-Tree indices on `session_id` in `session_chunks`, `dat_session_id` in `dat_session_events`, `school_id`, and `status` to optimize common dashboard lookups.
- **Caching:** Redis reserved for asynchronous job enqueueing; not currently caching DB lookups as state is highly dynamic. Moving toward Redis-based session caching for tenant metadata.
- **Consistency Strategy:** Strong consistency enforced by PostgreSQL `commit()` in the `get_conn()` success path. Eventual consistency for ML outputs and aggregated scores.
- **Scaling Strategy:** Native `psycopg2` `ThreadedConnectionPool` configured within the FastAPI application's lifespan to prevent worker-side connection starvation and overhead, replacing naive one-off connections. Future read-replicas for dashboard queries, and augmentation with PgBouncer if connections exceed safe limits.

## API Strategy

- **Endpoints:** Clean REST `/v1/` routing mapping directly to resources (e.g., `/v1/sessions`, `/v1/sessions/{id}/chunks/{idx}`, `/v1/dat-sessions`).
- **Validation:** Pydantic models with `Field` constraints enforcing rigid data typing, bounds checking (e.g., `chunk_index` limits), and payload size limits.
- **Authentication:** `HTTPBearer` (Environment-configured static API key verified via dependency injection) ensures baseline access control for MVP. OAuth2/OIDC integration planned for G2 compliance phase.
- **Rate Limiting:** IP-based and Tenant-based rate limiting on the API Gateway to prevent DoS via bulk uploads.
- **Versioning:** URL-level versioning (`/v1/`) to guarantee backward compatibility with deployed Android apps.

## Scalability Strategy

- **Horizontal Scaling:** Stateless FastAPI nodes (save for chunk uploads which hit MinIO directly) easily scaled horizontally across multiple Kubernetes pods behind a Load Balancer.
- **Caching:** Pre-computing complex dashboard aggregations to reduce OLTP load. Not primary bottleneck yet; future use of Redis for read-heavy API responses.
- **Partitioning:** Database table partitioning by tenant (`school_id`) or time for `dat_session_events` if volume requires.
- **Async Processing:** Blocking I/O localized to `def` endpoints and offloading ML processing to Redis queue for background workers. Clients poll or use WebSockets for results instead of blocking HTTP requests.
- **Load Balancing:** L7 routing spreading ingest traffic across multiple API instances. Standard round-robin via K8s service or Nginx ingress.

## Reliability Strategy

- **Retries:** Exponential backoff implemented in capture clients (Android) for chunk uploads and inter-service ML workers.
- **Failover:** Database operations correctly rollback on specific `psycopg2.Error` to prevent partial data writes and connection corruption. Stateless API design ensures traffic smoothly shifts during node failures.
- **Redundancy:** Replicated PostgreSQL (planned) and Multi-AZ object storage. Deployment redundancy required via infrastructure layer (e.g., highly available StatefulSets).
- **Recovery Mechanisms:** Dead Letter Queue (DLQ) implementations for failed worker jobs preventing queue poisoning. Explicit connection closure and exception logging to stderr ensures transient errors are visible and don't permanently exhaust the connection pool.

## Security Strategy

- **Authentication:** `HTTPBearer` ensures baseline access control. Strong cryptographic identities for IoT/Edge devices.
- **Authorization:** `school_id` required in payloads to allow future tenant-level isolation and RBAC enforcing tenant boundaries (Supervision Mode constraints).
- **Validation:** No external input trusted; rigid schema validation via FastAPI/Pydantic. Explicit bounds checking (e.g., `chunk_index` max sizes) and content length validation.
- **Vulnerability Prevention:** Parameterized SQL queries via `psycopg2` prevent SQL injection attacks. Secrets managed via `Pydantic Settings` defaults to prevent hardcoded credential leakage. Pre-commit linters (Ruff) and planned dependency scanning. HTTPS strictly enforced.

## Observability

- **Logging:** All database errors explicitly captured and sent to `sys.stderr` inside `db_utils.py` to populate container logs. Structured JSON logs to standard output/error, aggregating to a centralized SIEM. Traces include `session_id` and `worker_mode`.
- **Tracing:** OpenTelemetry integration (planned) for request lifecycle tracing across API and Workers to track connection duration and query execution times.
- **Monitoring:** Exporting metrics for queue depth, worker latency, standard endpoint hit counts, status code returns, and upload success rates.
- **Alerting:** PagerDuty integration for DLQ spikes, API health endpoint failures, container restarts, and >500 status code rates from the API.

## Performance Optimization

- **Bottlenecks:** Avoiding N+1 database queries; connection open/close overhead mitigated by reusing connections in helper methods where possible and eagerly initialized `ThreadedConnectionPool`. Centralized GPU inference (RTX 5070) identified as the primary throughput bottleneck. Addressed via asynchronous queueing.
- **Query Optimization:** Targeted inserts with `RETURNING` clauses to avoid follow-up `SELECT` statements. Avoiding N+1 queries by passing active DB cursors to helper functions within background workers.
- **Caching:** Aggressive caching of static tenant configurations. Not strictly needed for DB lookups in MVP.
- **Concurrency Optimization:** Synchronous DB operations run in the FastAPI threadpool; memory footprint strictly controlled by reading `UploadFile` chunks efficiently via blocking read. Optimizing Uvicorn thread pools and chunk upload streams to minimize memory pressure.

## Risks & Tradeoffs

- **Operational Risks:** `psycopg2` direct connections without external pooling (like PgBouncer) may lead to connection exhaustion under high load spikes, partially mitigated by `ThreadedConnectionPool`. Hybrid Edge/Cloud architecture increases operational complexity and debugging difficulty.
- **Scaling Concerns:** Synchronous DB execution ties up threadpool threads. If DB is slow, API latency degrades quickly. Python's GIL overhead in FastAPI during massive concurrent chunk uploads.
- **Complexity Tradeoffs:** Chosen direct SQL approach via `psycopg2` is simple and predictable, but sacrifices the convenience and migration tooling of a full ORM like SQLAlchemy. Choosing HTTP chunked uploads over direct-to-S3 signed URLs simplifies Edge client logic but increases API gateway load. Tradeoff accepted to maintain strict validation and control over the ingest buffer.

## Agile Sprint Plan

- **Sprint 1 (Completed):** Refine MVP API ingest, stabilize MinIO storage, establish asynchronous Redis worker queues for metrics, and handle Database Error Handling.
- **Sprint 2 (Current):** Add connection pooling. Implement eager connection pool initialization in FastAPI app lifespan. Optimize large session chunk retrieval. Complete Meta Ray-Ban (DAT) end-to-end integration, implement robust DLQs, and finalize RBAC schema for school supervision modes.
- **Sprint 3:** Deploy initial cloud staging environment, benchmark RTX 5070 queue latency, and harden API rate limiting.
- **Sprint 4:** G2 compliance audit, DPDP data handling review, and production infrastructure freeze.
