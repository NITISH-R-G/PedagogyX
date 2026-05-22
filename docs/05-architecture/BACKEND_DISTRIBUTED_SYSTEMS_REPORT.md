# Backend Architecture & Distributed Systems Report

**Version:** 1.0
**Author:** Autonomous Senior Backend Developer & Distributed Systems Architect
**Focus:** High-Throughput, Resilient Core API & Event Routing

## 1. System & Requirement Analysis

PedagogyX requires a backend that can handle simultaneous high-bandwidth media ingestion, coordinate complex asynchronous machine learning pipelines, and serve real-time dashboard analytics, all while strictly adhering to the ₹0 customer hardware budget (requiring hyper-efficient central cloud resource usage).

- **High Availability:** Must tolerate school edge node disconnections and central worker node failures.
- **Protocol Diversity:** REST for UI, WebSockets for live telemetry, WebRTC/RTP/Chunked HTTP for media ingest.
- **Cost Constraint:** Maximum utilization of a self-hosted RTX 5070 pool implies aggressive queue management and batching.

## 2. Backend Architecture

The architecture utilizes an **Event-Driven Microservices** pattern, optimized for deployment on bare-metal via Docker Compose (Phase 1) migrating to Kubernetes (Phase 2).

- **Edge Gateway:** MediaMTX handles raw RTMP/WebRTC streams from classrooms.
- **Core API (Go):** Handles authentication, session management, and media chunk metadata ingestion. Chosen for its superior concurrency and low memory footprint.
- **Event Bus (Redis):** Acts as the central nervous system. decoupling ingest from ML processing.
- **ML Worker Daemons (Python):** Horizontally scalable workers pulling jobs from Redis, executing PyTorch/TensorRT inference, and returning results.

## 3. Database Design

- **Primary Datastore:** PostgreSQL 16.
- **Schema Design (Phase 1):**
  - `organizations` (Tenants)
  - `users` (Teachers, Admins, Coaches)
  - `sessions` (Individual recorded classes)
  - `media_assets` (Pointers to MinIO objects)
  - `pedagogy_metrics` (Aggregated TSDB-lite table for dashboard rendering)
- **Blob Storage:** MinIO for raw media and massive JSON inference artifacts.

## 4. API Strategy

- **External Facing APIs (REST/JSON):**
  - Standard CRUD operations for organizations, users, and session metadata.
  - OpenAPI 3.0 specified and strictly validated.
- **Ingest APIs (gRPC / Binary):**
  - Used by edge nodes to upload chunked video to minimize overhead.
- **Real-Time Feeds (WebSockets):**
  - Pushing live status updates to Admin dashboards (e.g., "Session 104 is currently processing").

## 5. Scalability Strategy

- **Stateless API:** The Go API nodes hold no state, allowing instant horizontal scaling behind a reverse proxy (Nginx/Traefik).
- **Queue-Based Backpressure:** If ML workers are saturated, video chunks queue safely in MinIO, and Redis tracks pending jobs. The system degrades gracefully by increasing processing latency rather than crashing.
- **Worker Auto-Scaling:** Python workers can be spun up on spot instances to drain queues during peak hours.

## 6. Reliability Strategy

- **Idempotency:** All worker jobs must be idempotent. If a worker crashes mid-inference, the job is requeued and overwrites previous partial results safely.
- **Graceful Degradation:** If the CV worker pool is offline, the fusion pipeline can proceed with ASR-only analytics, marking CV data as "temporarily unavailable."
- **Circuit Breakers:** Implemented in the Go API when calling external services (if any are introduced later).

## 7. Security Strategy

- **Authentication:** JWT-based stateless auth for UI clients. Short-lived HMAC tokens for edge device upload authorization.
- **Authorization:** Strict Role-Based Access Control (RBAC) enforced at the API layer. Ensure a teacher cannot fetch another teacher's session data.
- **Input Validation:** Go API strictly sanitizes all incoming payloads. Pydantic validates ML worker outputs.

## 8. Observability

- **Tracing:** OpenTelemetry instrumentation across Go API and Python workers to trace a video chunk's journey from ingest to DB write.
- **Logging:** Structured JSON logs aggregated to ELK or a lightweight alternative (e.g., Vector + ClickHouse).
- **Health Checks:** Comprehensive `/health` endpoints for all services verifying DB connectivity and GPU driver state.

## 9. Performance Optimization

- **Connection Pooling:** Aggressive pgBouncer configuration for Postgres.
- **Go Routines:** Utilizing Go's lightweight concurrency for parallelized media chunk handling without thread exhaustion.
- **Cache Layer:** Redis caching for frequently accessed dashboard aggregates.

## 10. Risks & Tradeoffs

- **Risk:** Python's Global Interpreter Lock (GIL) limits concurrency in workers.
  - **Mitigation:** Deploy one worker process per GPU/CPU core, rather than relying on threading within a single process.
- **Risk:** Redis becomes a single point of failure.
  - **Mitigation:** Run Redis in High Availability (Sentinel/Cluster) mode; implement persistent backing (AOF).

## 11. Agile Sprint Plan (Backend Track)

- **Sprint 03:** Scaffold Go API repo. Implement User auth and Session creation endpoints. Establish Postgres schema.
- **Sprint 04:** Integrate Redis queue. Build the Python worker base class for fetching jobs.
- **Sprint 05:** Implement the API endpoint for secure chunk upload to MinIO and subsequent job enqueuing.
