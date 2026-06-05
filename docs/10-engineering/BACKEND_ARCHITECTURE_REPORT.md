# Backend Architecture Report

## System & Requirement Analysis

**Requirements:**

- Process high-volume audio/video data from edge clients (Meta Ray-Ban smart glasses via Android host app).
- Support scalable, asynchronous processing for transcription and metrics.
- Ensure strict privacy, data residency, and tenant isolation per Indian compliance (DPDP).

**Constraints:**

- Classrooms have intermittent connectivity, requiring robust edge buffering.
- Inference workers run on an OSS-first cold path utilizing RTX 5070 worker nodes.
- Maintainability is enforced via strict coding standards and zero-tolerance for silent exceptions.

**Edge Cases:**

- Interruptions during uploads require retry and chunk resumption management.
- Unpredictable loads require resilient queue behavior and DLQ utilization.

**Scale Assumptions:**

- Global scale with millions of requests.
- High likelihood of traffic spikes and need for horizontal scale for worker processes.

## Backend Architecture

**Services:**

- A stateless REST API gateway (FastAPI).
- Background worker nodes (`worker-asr`, `worker-metrics`).
- A Next.js front-end for dashboards.

**APIs:**

- RESTful HTTP API to ingest media chunks and metadata.

**Data Flow:**

- Edge clients -> REST API (buffered/ingested) -> MinIO (blob storage) -> Redis Queue -> Worker nodes (ASR, CV, Metrics) -> PostgreSQL (aggregated metrics).

**Event Systems:**

- Redis manages asynchronous tasks to decouple ingestion from compute-heavy inference.

**Abstractions:**

- Clear boundaries between the gateway and background workers.
- Shared dead letter queue (DLQ) implementations for resilience.

## Database Design

**Schema:**

- PostgreSQL for relational metadata (sessions, metrics, user states).
- Object Storage (MinIO) for heavy binary data (video chunks, transcripts).

**Indexing:**

- Designed for rapid metric aggregation and session lookups.

**Caching:**

- N/A for database results initially; Redis is strictly used for the queue layer.

**Consistency Strategy:**

- Strong consistency via PostgreSQL ACID transactions for metadata.

**Scaling Strategy:**

- Lean relational tables, offloading blob storage.
- Horizontal scaling on read-heavy paths if needed, while primary scaling bottleneck lies in compute (inference tier).

## API Strategy

**Endpoints:**

- Media upload and processing triggers.
- Insight latency and preview generation checks.

**Validation:**

- Strict Pydantic models and FastAPI dependencies.

**Authentication:**

- Currently `HTTPBearer` with API keys; migrating to JWT-based RBAC.

**Rate Limiting:**

- Necessary for edge API boundaries (future implementation).

**Versioning:**

- Consistent semantic API routes (e.g., `v1`).

## Scalability Strategy

**Horizontal Scaling:**

- The background workers scale horizontally to handle variable loads (limited by GPU availability).
- Stateless API containers scale out trivially behind load balancers.

**Caching:**

- Potential read-through caching for dashboard metrics in the future.

**Partitioning:**

- Future multi-tenant isolation and partitioning strategy by school/district.

**Async Processing:**

- Offloaded fully to Redis queues and distinct worker pools.

**Load Balancing:**

- Even distribution of requests across the FastAPI tier.

## Reliability Strategy

**Retries:**

- Built into the edge client sync engine.

**Failover & Redundancy:**

- Stateless services can be killed/restarted.

**Recovery Mechanisms:**

- Strict DLQ pattern implementation in worker nodes (uncaught exceptions are logged and payloads persisted).

## Security Strategy

**Authentication & Authorization:**

- Strict API token verification, progressing to JWT.

**Validation:**

- All payloads strictly typed and size constrained to prevent memory exhaustion.

**Vulnerability Prevention:**

- Avoidance of string interpolation for SQL queries; using psycopg2 parameterized queries.
- Least privilege access for DB and MinIO credentials.

## Observability

**Logging:**

- Centralized structured logging to `sys.stderr` for rapid diagnostics.

**Tracing:**

- SLA monitoring through latency metrics (`insight_latency_sec`).

**Monitoring & Alerting:**

- Tracking Redis queue depth, SLA violations, and DLQ accumulation.

## Performance Optimization

**Bottlenecks:**

- Inference node GPU swapping and DB connection overheads.

**Query Optimization:**

- Continuous assessment to eliminate N+1 database connection issues by passing shared cursors down to helper routines (as an ongoing backlog item).

**Caching & Concurrency:**

- Connection pooling is paramount for reducing overhead. DB connections strictly scoped inside context managers.

## Risks & Tradeoffs

**Operational Risks:**

- Edge network failures leading to data loss prior to server ingestion.
- Mocking external services complicates the testing setup.

**Scaling Concerns:**

- Queue bottlenecks due to heavy concurrent uploads waiting for finite RTX 5070 worker capacity.

**Complexity Tradeoffs:**

- Distributing tasks requires complex error handling (DLQ) rather than simple monolithic transaction rollbacks.

## Agile Sprint Plan

**Implementation Phases:**

- **Sprint 1 (Current):** Consolidate backend architecture report and assess current tech debt.
- **Sprint 2:** Robust ingestion & state management, ensuring gateway retry & resume logic and refining DLQ abstractions.
- **Sprint 3:** Resolve identified backend performance bottlenecks (like N+1 queries) and improve observability metrics.

**Milestones:**

- Publish autonomous architecture documentation (Completed).

**Priorities:**

- Reliability and maintainability.
- Operational transparency via DLQs.
