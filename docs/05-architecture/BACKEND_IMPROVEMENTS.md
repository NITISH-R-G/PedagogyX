# Backend System Improvements

## System & Requirement Analysis

- **Requirements:** Improve the resilience and fault tolerance of the database interactions by refining the database connection management utility. Adhere to strict backend and distributed system architect standards, prioritizing scalability, security, observability, and code health conventions.
- **Constraints:** FOSS-first environment, self-hosted deployment targeting central inference servers. Direct database operations using `psycopg2`. No proprietary cloud APIs.
- **Edge Cases:** Connections dropping or transactional conflicts during context manager yielding.
- **Scale Assumptions:** Production traffic requiring reliable connection pooling and transaction rollbacks without swallowing the underlying SQL errors.

## Backend Architecture

- **Services:** FastAPI based API server handling synchronous database interactions via threadpool to avoid blocking the async event loop.
- **APIs:** Dat session routes and primary session upload endpoints using simple `HTTPBearer` authentication for MVP.
- **Data Flow:** Incoming REST calls -> Pydantic validation -> Database connection yield from `get_conn()` -> Direct SQL execution -> Commit or explicit Rollback on `psycopg2.Error`.
- **Event Systems:** Minimal event tracking in `dat_session_events` to mirror Meta Wearables DAT lifecycle.
- **Abstractions:** Thin abstraction over standard `psycopg2` context managers; explicit control over transaction boundaries within the route handlers.

## Database Design

- **Schema:** Existing PostgreSQL relations (`sessions`, `session_chunks`, `dat_sessions`, etc.) optimized for rapid insertion of chunk metadata and temporal state transitions.
- **Indexing:** Required on primary and foreign keys (e.g. `session_id` in `session_chunks`, `dat_session_id` in `dat_session_events`).
- **Caching:** Redis reserved for asynchronous job enqueueing; not currently caching DB lookups as state is highly dynamic.
- **Consistency Strategy:** Strong consistency enforced by PostgreSQL `commit()` in the `get_conn()` success path.
- **Scaling Strategy:** Relying on Postgres' innate connection pooling initially, to be augmented with PgBouncer if connections exceed safe limits.

## API Strategy

- **Endpoints:** RESTful patterns mapping directly to resources (`/v1/sessions`, `/v1/dat-sessions`).
- **Validation:** Pydantic models with `Field` constraints ensuring payload integrity.
- **Authentication:** Environment-configured static API key verified via dependency injection.
- **Rate Limiting:** To be implemented at the API Gateway or using Redis token bucket per tenant.
- **Versioning:** URL path versioning (`/v1/`) established.

## Scalability Strategy

- **Horizontal Scaling:** API layer is stateless (save for chunk uploads which hit MinIO directly); easily scaled across multiple Kubernetes pods.
- **Caching:** Not primary bottleneck yet; future use of Redis for read-heavy API responses (like dashboard data).
- **Partitioning:** Database table partitioning by tenant (`school_id`) or time for `dat_session_events` if volume requires.
- **Async Processing:** Blocking I/O localized to `def` endpoints, offloading ASR processing to Redis queue for background workers.
- **Load Balancing:** Standard round-robin via K8s service or Nginx ingress.

## Reliability Strategy

- **Retries:** Client-side retries expected for chunk uploads.
- **Failover:** Database operations correctly rollback on specific `psycopg2.Error` to prevent partial data writes and connection corruption.
- **Redundancy:** MinIO and Postgres deployment redundancy required via infrastructure layer (e.g., highly available StatefulSets).
- **Recovery Mechanisms:** Explicit connection closure and exception logging to stderr ensures transient errors are visible and don't permanently exhaust the connection pool.

## Security Strategy

- **Authentication:** `HTTPBearer` ensures baseline access control.
- **Authorization:** `school_id` required in payloads to allow future tenant-level isolation and RBAC.
- **Validation:** Explicit bounds checking (e.g., `chunk_index` max sizes) and content length validation.
- **Vulnerability Prevention:** Parameterized SQL queries via `psycopg2` prevent SQL injection attacks. Secrets managed via `Pydantic Settings` defaults to prevent hardcoded credential leakage.

## Observability

- **Logging:** All database errors explicitly captured and sent to `sys.stderr` inside `db_utils.py` to populate container logs.
- **Tracing:** Currently implicit via logs; OTel tracing to be added to track connection duration and query execution times.
- **Monitoring:** Metrics gathered from standard endpoint hit counts and status code returns.
- **Alerting:** Infrastructure monitoring on container restarts and >500 status code rates from the API.

## Performance Optimization

- **Bottlenecks:** Avoiding N+1 database queries; connection open/close overhead mitigated by reusing connections in helper methods where possible (passing `cursor`).
- **Query Optimization:** Targeted inserts with `RETURNING` clauses to avoid follow-up `SELECT` statements.
- **Caching:** Not strictly needed in MVP.
- **Concurrency Optimization:** Synchronous operations run in the FastAPI threadpool; memory footprint strictly controlled by reading `UploadFile` chunks efficiently via blocking read.

## Risks & Tradeoffs

- **Operational Risks:** `psycopg2` direct connections without pooling (like PgBouncer) may lead to connection exhaustion under high load spikes.
- **Scaling Concerns:** Synchronous DB execution ties up threadpool threads. If DB is slow, API latency degrades quickly.
- **Complexity Tradeoffs:** Chosen direct SQL approach via `psycopg2` is simple and predictable, but sacrifices the convenience and migration tooling of a full ORM like SQLAlchemy.

## Agile Sprint Plan

- **Implementation Phases:** Phase 1: Database Error Handling (Completed). Phase 2: Add connection pooling. Phase 3: Optimize large session chunk retrieval.
- **Milestones:** MVP API robust against transient database errors.
- **Priorities:** High priority on ensuring no silent failures during database operations.
- **Expected Outcomes:** Reduced debugging time, clearer log outputs for operations, and safer transaction rollbacks.
