# Backend Architecture Report v3.0

**Date:** 2026-05-27
**Role:** Autonomous Senior Backend Developer & Distributed Systems Architect
**Context:** PedagogyX MVP boilerplate API, transitioning to resilient distributed systems and scale, keeping in mind the integration of Meta Ray-Ban glasses and WebRTC chunking strategies.

## System & Requirement Analysis

- **Requirements:** Build an incredibly resilient and high-performance backend system for PedagogyX capable of handling massive spikes in multimodal video/audio ingestion, asynchronous machine learning tasks (ASR, CV, NLP) on limited GPU hardware, and delivering real-time actionable metrics for supervision interfaces. Must maintain 100% compliance with India DPDP data residency standards.
- **Constraints:** Centralized GPU bottleneck (single RTX 5070 per ADR-0006), unstable school edge internet connections with frequent drops, and a ₹0 edge hardware budget.
- **Edge Cases:** Network partitions severing edge upload connections mid-chunk, Redis queue overflow, and database transient connection drops.
- **Scale Assumptions:** Phased India rollout beginning with K-12 pilot classrooms, demanding rapid horizontal scaling of the ingest gateways and rigorous queue management to protect the ML inference pipeline.

## Backend Architecture

- **Services:**
  - `api`: FastAPI-based ingress control plane that manages the ingestion of chunked binary assets, session lifecycle, and Meta Ray-Ban client states.
  - `worker-metrics`: Python asynchronous worker that aggregates intermediate scores and generates real-time pedagogical previews.
  - `worker-asr`: Python asynchronous worker handling the cold-path audio transcription queue via Whisper integration.
  - `worker-cv`: Python asynchronous worker handling computer vision inferences (Phase 2).
- **APIs:** Fast, fully async RESTful endpoints for managing school/room/teacher hierarchies, device linking, and heavy chunked media uploads.
- **Data Flow:** Capture Client (Android/WebRTC) -> Nginx/Traefik Ingress -> FastAPI (`services/api`) -> S3/MinIO for blob storage -> Redis queues -> Python ML Workers -> PostgreSQL aggregation -> Admin Dashboards.
- **Event Systems:** Deeply decoupled event-driven queues utilizing Redis lists/streams to transition state between HTTP ingest completion and ML task execution.
- **Abstractions:** Clear abstraction between high-velocity stateless request handling in FastAPI and robust background processing in the worker daemon pool.

## Database Design

- **Schema:** Relational PostgreSQL schema prioritizing strict integrity (`sessions`, `chunks`, `metrics`, `dat_sessions`, `dat_session_events`). Heavy use of foreign key constraints to enforce tenant isolation.
- **Indexing:** B-Tree indexing on primary identifiers (`session_id`, `school_id`, `chunk_index`) and temporal indices on `created_at` for high-performance dashboard queries.
- **Caching:** Aggressive Redis caching strategy to be adopted for static tenant configuration to offload database reads.
- **Consistency Strategy:** Strong consistency is enforced via explicit transaction management (`psycopg2` direct control) during the ingestion and lifecycle phases. Eventual consistency applies strictly to analytical outputs.
- **Scaling Strategy:** Connection pooling implementations (e.g., PgBouncer) sit in front of Postgres to handle the large number of concurrent worker and API node connections without exhausting database memory.

## API Strategy

- **Endpoints:** Clean, well-documented REST APIs under `/v1/sessions` and `/v1/dat-sessions`. Operations follow standard HTTP verb semantics.
- **Validation:** Pydantic is utilized heavily for strict request validation, schema generation (OpenAPI), bounds checking, and preventing malformed inputs from reaching the database.
- **Authentication:** Currently utilizing simplified `HTTPBearer` with API key validation, transitioning to OpenID Connect (OIDC) / OAuth2 for robust JWT-based edge node authentication.
- **Rate Limiting:** IP and tenant-based rate limiting via Redis token bucket algorithm to prevent noisy neighbor problems and mitigate DoS vectors on the ingest paths.
- **Versioning:** URI-based API versioning (`/v1/`) to ensure long-term backward compatibility with deployed edge android clients.

## Scalability Strategy

- **Horizontal Scaling:** The API is designed entirely stateless. State resides in MinIO and Postgres, allowing instant horizontal autoscaling of FastAPI pods behind the load balancer based on CPU/Memory metrics.
- **Caching:** Dashboards and complex analytical queries will be pre-calculated via materialized views and cached in Redis.
- **Partitioning:** Database tables will be partitioned natively in PostgreSQL by `tenant_id` and temporal boundaries to maintain query speed as the dataset grows massively.
- **Async Processing:** Heavy synchronous I/O operations are offloaded from the event loop using `run_in_threadpool`, while ML workloads are strictly asynchronous.
- **Load Balancing:** L7 HTTP routing is employed to effectively balance load across the API service fleet.

## Reliability Strategy

- **Retries:** Implemented at multiple levels. Client-side SDK exponential backoff for network drops. Worker-side exponential backoff for transient DB/Storage connection failures.
- **Failover:** Multi-AZ deployment strategy for stateless API instances.
- **Redundancy:** MinIO deployed with erasure coding for blob storage resilience. PostgreSQL set up with primary-replica replication for data durability.
- **Recovery Mechanisms:** Dead Letter Queues (DLQs) in Redis isolate poisoned payloads, preventing continuous worker crashes. Explicit database rollback handling for transient SQL errors ensures no partial data corruption.

## Security Strategy

- **Authentication:** Rigid cryptographic identities planned for hardware (Meta Ray-Ban/Android host).
- **Authorization:** Tenant isolation strictly enforced on every API route via context inspection (`school_id` checks).
- **Validation:** Trust no input. Pydantic enforces payload size maximums, content-type checks, and parameter sanitization to defend against injection attacks.
- **Vulnerability Prevention:** Parameterized SQL is non-negotiable. Defense in depth applied via strict network ACLs (workers do not have inbound open ports).

## Observability

- **Logging:** Structured JSON logs are emitted centrally, enriched with context identifiers (`session_id`, `dat_session_id`, `worker_mode`) to trace an event's lifecycle across boundaries.
- **Tracing:** Integration with OpenTelemetry (OTel) is planned for deep distributed tracing across API -> Queue -> Worker boundaries.
- **Monitoring:** Critical metrics are exposed to Prometheus (e.g., `/health`, queue depth, HTTP response latency, status code error rates).
- **Alerting:** Infrastructure alerts trigger automatically on continuous HTTP 500s or sustained DLQ growth.

## Performance Optimization

- **Bottlenecks:** Managing the FastAPI threadpool carefully during massive chunked file reads to ensure the async event loop isn't blocked.
- **Query Optimization:** Eliminating N+1 query patterns by utilizing efficient joins and bulk inserts where appropriate.
- **Caching:** Future implementation of an HTTP conditional GET strategy (ETag) for metadata that updates infrequently.
- **Concurrency Optimization:** Optimizing the database transaction boundaries to lock resources for the absolute minimum duration required.

## Risks & Tradeoffs

- **Operational Risks:** A FOSS-first and centralized AI processing architecture demands intricate queue monitoring and capacity planning to prevent cascading failures during peak school hours.
- **Scaling Concerns:** Python's Global Interpreter Lock (GIL) is a known limitation. We mitigate this by utilizing async where possible, `run_in_threadpool` for blocking I/O, and separate processes/containers for pure CPU/GPU work.
- **Complexity Tradeoffs:** Direct `psycopg2` SQL queries are chosen over massive ORMs like SQLAlchemy to eliminate ORM bloat, increase transparency, and directly control transaction boundaries, though this sacrifices some development speed.

## Agile Sprint Plan

- **Sprint 1 (Immediate):** Hardening API ingestion pathways and improving PostgreSQL transaction error handling. Validating DAT session lifecycle integration.
- **Sprint 2:** Scaling the asynchronous Python workers to handle higher load concurrency, robust DLQ handling in Redis, and deploying pgBouncer.
- **Sprint 3:** Instrument API and Worker nodes with OpenTelemetry. Implement complete observability dashboard (Prometheus + Grafana) for API latency and queue depth.
- **Sprint 4:** Execute full load and chaos testing, specifically severing network connections during chunked uploads and verifying client/server recovery behaviors.
