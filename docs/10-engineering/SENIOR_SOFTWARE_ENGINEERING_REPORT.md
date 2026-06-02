# Senior Software Engineering & Product Engineering Architecture Report

**Status:** Active
**Owner:** Autonomous Senior Software Engineer & Product Engineering Architect

## Problem Analysis

PedagogyX is developing an innovative multimodal AI classroom intelligence platform tailored for Indian educational contexts. The primary objective is to build a highly scalable, reliable, and privacy-preserving platform capable of ingesting high-volume audio/video data from edge clients (primarily Meta Ray-Ban smart glasses via an Android host application).

**Key Requirements & Constraints:**

- **Edge Inference & Connectivity:** Classrooms often experience intermittent connectivity, necessitating robust local chunking, buffering, and uploading over potentially unstable WAN links.
- **Compute Scalability:** Centralized inference relies on an OSS-first cold path utilizing RTX 5070 worker nodes. Processing loads are highly variable, requiring decoupling through asynchronous job queues.
- **Privacy & Compliance (India DPDP):** Strict data residency, encryption, and tenant isolation (school-level) are mandatory.
- **Developer Experience & Maintainability:** The architecture must be resilient to changing requirements, enforcing strict coding standards, preventing silent failures, and maintaining clean service boundaries.

## Architecture Design

The current system architecture is a loosely coupled **Hybrid Edge-Cloud (Tiered)** system.

- **Edge Tier:** Meta Ray-Ban smart glasses interface via Bluetooth to Android devices (DAT Host), which handle chunked HTTPS uploads to the centralized cloud API.
- **API/Gateway Tier (FastAPI):** A stateless REST API handles TLS termination, authentication via `HTTPBearer`, and routes media chunks directly into MinIO object storage. It orchestrates downstream processing by enqueuing task metadata into Redis.
- **State & Queue Tier:**
  - **Redis** manages asynchronous tasks, serving distinct queues for separate worker pools to prevent GPU memory fragmentation.
  - **PostgreSQL** serves as the primary relational database for metadata, session states, and ML analytics, interacted with via synchronous `psycopg2` within FastAPI threadpools.
- **Inference Tier (Python Workers):** Distributed task runners (ASR, CV, Metrics) dequeue jobs. They enforce a strict Dead Letter Queue (DLQ) pattern and ban silent exceptions to maximize operational observability.
- **Frontend Tier (Next.js):** A modern React application leveraging App Router and Tailwind CSS v4, delivering Server-Side Rendered dashboards for administrators and teachers to review pedagogical insights.

## Implementation Strategy

1. **Ingestion & Buffering:** Ensure the FastAPI ingestion path can gracefully handle out-of-order or interrupted chunk uploads, managing session states robustly in PostgreSQL.
2. **Worker Decoupling:** Maintain strict boundaries between `worker-asr` and `worker-metrics`. As `worker-asr` completes transcripts, it should transition session states and trigger downstream metric aggregations.
3. **Database Interaction Refactoring:** Centralize database connections. Refactor worker scripts to pass active database cursors (e.g., `RealDictCursor`) to helper methods to eliminate N+1 connection overhead and improve latency.
4. **Frontend Integration:** Connect the Next.js frontend with the FastAPI backend using secure, typed API interactions, enabling real-time preview readiness states.

## Code Quality Strategy

- **Linting & Formatting:** Enforce consistent formatting using Prettier for markdown (`docs/**/*.md`) and Ruff for Python (`services/`, `tools/`).
- **Testing:**
  - Comprehensive Pytest suites for FastAPI and workers, extensively mocking external services (e.g., MinIO, Redis, PostgreSQL context managers) to ensure logic isolation.
  - Vitest for Next.js frontend component testing.
- **Error Handling:** Absolute prohibition of `except Exception: pass`. All caught exceptions must be logged to `sys.stderr` with tracebacks.
- **Configuration:** Strict typing via Pydantic `BaseSettings`. Secrets must default to `None` to prevent hardcoded credentials from reaching source control.

## Performance Optimization

- **Database Connections:** Refactor DB helper methods to accept pre-existing cursors, eliminating the latency of establishing new connections for granular queries.
- **Inference Throughput:** Maximize GPU utilization by isolating ASR and CV workloads to dedicated worker pools, avoiding costly weight-swapping delays.
- **Frontend Delivery:** Utilize Next.js React Server Components (RSC) to minimize client-side JavaScript execution, paired with optimized asset delivery for dashboard metrics.
- **Storage Strategy:** Offload all heavy blob data (video chunks, transcripts) to MinIO, keeping the PostgreSQL database lean for rapid metric aggregation and session queries.

## Security Considerations

- **Authentication:** Currently utilizing API keys via `HTTPBearer`. Future migrations will target robust JWT-based RBAC to isolate school and district tenants.
- **Data Privacy:** Enforce regional data residency within India. Secure MinIO buckets with appropriate SSE-C / KMS integrations.
- **Least Privilege:** API and worker containers run as non-root users. Application roles in PostgreSQL are strictly scoped.
- **Input Validation:** All incoming payloads and file uploads are strictly validated and constrained by size via Pydantic and FastAPI `File(...)` dependencies to prevent memory exhaustion attacks.

## Observability

- **Structured Logging:** Centralized logging across all Python services outputting to standard streams for aggregation.
- **Queue Monitoring:** Implementing Prometheus exporters (future state) to track Redis queue depths and trigger autoscaling of worker nodes.
- **Dead Letter Queues (DLQ):** Every worker strictly implements DLQs. Failed payloads are appended to `<queue>:dlq` and full tracebacks are emitted to `sys.stderr`.
- **System Metrics:** `insight_latency_sec` is actively tracked within the platform to monitor the end-to-end SLA from media upload to insight generation.

## Refactoring Opportunities

- **N+1 Connection Overhead:** The `worker-metrics` currently opens independent connections within its `_compute_talk_ratio` and `_insight_latency_sec` helpers. These will be refactored to accept a shared cursor instantiated in the primary `process_job` loop.
- **Centralized Database Utilities:** Consolidate context managers and cursor factories across all legacy scripts to match the optimized pattern in `services/api/app/db.py`.
- **Error Handling Standardization:** Abstract the DLQ and traceback logging logic into a shared package to ensure uniformity across all future workers.

## Risks & Tradeoffs

- **Intermittent Connectivity:** The edge-to-cloud architecture heavily relies on the DAT Host app's ability to cache and resume uploads. If local storage is constrained, data loss may occur before it reaches the API gateway.
- **Asynchronous Latency:** While queueing decouples the system, massive concurrent uploads could bottleneck the inference workers, increasing the `insight_latency_sec` beyond acceptable thresholds for teachers expecting immediate feedback.
- **Testing Complexity:** Mocking stateful systems like MinIO and PostgreSQL context managers requires verbose setup, potentially slowing down developer velocity when extending core processing pipelines.

## Agile Sprint Plan

- **Sprint 1 (Current): Architecture Consolidation & Refactoring**
  - Publish this engineering architecture report.
  - Refactor `worker-metrics` to eliminate N+1 database connections by implementing cursor passing.
  - Verify changes via existing Pytest suites.
- **Sprint 2: Robust Ingestion & State Management**
  - Implement and test chunk resumption and out-of-order handling in the FastAPI gateway.
  - Finalize DLQ abstractions for worker nodes.
- **Sprint 3: Insight Delivery Integration**
  - Wire up Next.js dashboards to live API metric endpoints.
  - Implement visual regression and E2E verification workflows using Playwright.
