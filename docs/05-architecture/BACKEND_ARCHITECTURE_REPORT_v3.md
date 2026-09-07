# Backend Architecture Report v3.0

**Date:** 2026-05-24
**Role:** Autonomous Senior Backend Developer & Distributed Systems Architect
**Context:** PedagogyX Phase 0 + MVP boilerplate, updated with Meta Ray-Ban (DAT) primary client path ([ADR-0009](../08-rfc-adr/ADR-0009-meta-rayban-primary-client.md)). Focus on scaling, reliability, and production readiness.

## System & Requirement Analysis

- **Requirements:** Support high-throughput multimodal ingest from Meta Ray-Ban glasses and edge Android devices, process live preview metrics, orchestrate cold path GPU ML inference (ASR, CV, LLM on RTX 5070), provide low-latency administrative dashboards, enforce India data residency, and ensure strict tenant (school/university) isolation.
- **Constraints:** ₹0 per-classroom edge hardware budget (pilot), central OSS-only ML stack, constrained central GPU compute (single RTX 5070 limit per ADR-0006), unreliable school internet connections.
- **Edge Cases:** Network disconnections during upload requiring chunk resumability, delayed ML processing due to queue bottlenecks, out-of-order stream synchronization, partial session uploads, duplicate chunk submissions.
- **Scale Assumptions:** Phased India rollout starting with pilot deployments, requiring architectural runway for horizontal scaling of the control plane and queue-based backpressure for the centralized ML pool. Assume 10k concurrent ingest streams in initial phases.

## Backend Architecture

- **Services:**
  - `api`: FastAPI control plane for CRUD, session lifecycle, and chunked upload endpoints.
  - `worker-metrics`: Python background worker generating live "preview" metrics asynchronously.
  - `worker-asr`: Python background worker orchestrating audio transcription (stubbed/Whisper) managing inference queues.
  - `worker-cv`: Python background worker stub for Phase 2 video processing.
- **APIs:** RESTful endpoints (`/v1/sessions/*`) for session lifecycle, synchronous preview retrieval, and chunked binary uploads.
- **Data Flow:** Capture Client (Android DAT Host) -> Chunked HTTPS Uploads -> API Gateway -> MinIO (Storage) -> Redis (Job Queue) -> Python Worker Pool (ASR/Metrics/CV) -> PostgreSQL (Scores) -> Web Dashboards.
- **Event Systems:** Redis-backed robust queues acting as the asynchronous event bus between API session completion and background workers, implementing pub/sub for real-time progress updates.
- **Abstractions:** Strict separation between ingest (hot/cold buffers) and downstream ML processing to absorb demand spikes. Hexagonal architecture for clear domain boundaries.

## Database Design

- **Schema:** PostgreSQL relational schema managing `tenant_id`, `school_id`, `session_id`, `chunk_metadata`, and `metrics` structured strictly with Foreign Keys and Constraints for data integrity.
- **Indexing:** B-Tree indices on `session_id`, `school_id`, and `status`. Partial indices on active sessions for fast dashboard lookups.
- **Caching:** Redis-based session caching and metadata caching to alleviate database read load during dashboard access.
- **Consistency Strategy:** Strong consistency for session states and chunk metadata (PostgreSQL); eventual consistency for ML outputs and aggregated scores to allow for decoupled processing.
- **Scaling Strategy:** Connection pooling (PgBouncer) implemented to prevent worker-side connection starvation. Implemented read-replicas for dashboard queries and heavy analytical read workloads.

## API Strategy

- **Endpoints:** Clean REST `/v1/` routing (e.g., `/v1/sessions`, `/v1/sessions/{id}/chunks/{idx}`). Use of proper HTTP verbs and response codes.
- **Validation:** Pydantic models enforcing rigid data typing, bounds checking (e.g., `chunk_index` limits), payload size limits, and sanitization of input variables.
- **Authentication:** Token-based API access for capture clients. OAuth2/OIDC integration planned for G2 compliance phase.
- **Rate Limiting:** Sliding-window rate limiting on the API Gateway (IP-based and Tenant-based) to prevent DoS via bulk uploads and unfair tenant resource consumption.
- **Versioning:** URL-level versioning (`/v1/`) to guarantee backward compatibility with deployed Android apps, with clear deprecation cycles.

## Scalability Strategy

- **Horizontal Scaling:** Stateless FastAPI nodes scaled horizontally behind an L7 Load Balancer, dynamically autoscaling based on CPU/Memory pressure.
- **Caching:** Pre-computing complex dashboard aggregations in background jobs and caching to reduce OLTP load during peak hours.
- **Partitioning:** Tenant-based logical data partitioning in the schema design, paving the way for future physical sharding if required.
- **Async Processing:** Complete decoupling of ML inference. Clients poll or use WebSockets for results instead of blocking HTTP requests.
- **Load Balancing:** L7 routing spreading ingest traffic across multiple API instances and ensuring stickiness if required for specific upload workflows.

## Reliability Strategy

- **Retries:** Exponential backoff with jitter implemented in capture clients (Android) and inter-service ML workers to handle transient network and service failures gracefully.
- **Failover:** Stateless API design ensures traffic smoothly shifts during node failures. Active-passive database failover readiness.
- **Redundancy:** Multi-AZ API deployment, Replicated PostgreSQL (planned), and Multi-AZ object storage for MinIO.
- **Recovery Mechanisms:** Robust Dead Letter Queue (DLQ) implementations for failed worker jobs (e.g., `client.rpush(f"{JOB_QUEUE}:dlq", raw)`), preventing queue poisoning and allowing for manual/automated replay.

## Security Strategy

- **Authentication:** Strong cryptographic identities for IoT/Edge devices using JWTs with short expirations and rotation.
- **Authorization:** Rigid RBAC enforcing tenant boundaries (Supervision Mode constraints) ensuring no cross-tenant data leakage.
- **Validation:** No external input trusted; rigid schema validation via FastAPI/Pydantic.
- **Vulnerability Prevention:** Pre-commit linters (Ruff), HTTPS strictly enforced, dependency scanning via GitHub Actions, and container image scanning before deployment.

## Observability

- **Logging:** Structured JSON logs (Loguru) to standard output/error, aggregating to a centralized SIEM (ELK/Datadog). Traces mandate correlation IDs (`session_id`).
- **Tracing:** OpenTelemetry integration for distributed request lifecycle tracing across API, Redis, MinIO, and Python Workers to pinpoint latency bottlenecks.
- **Monitoring:** Exporting rich Prometheus metrics for queue depth, worker processing latency, API response times (p50, p95, p99), and upload success rates.
- **Alerting:** PagerDuty integration for DLQ spikes, API health endpoint failures, and high error rates, with configured anomaly detection.

## Performance Optimization

- **Bottlenecks:** Centralized GPU inference (RTX 5070) identified as the primary throughput bottleneck. Addressed via asynchronous queueing, batching inference requests where possible.
- **Query Optimization:** Avoiding N+1 queries by passing active DB cursors and using bulk fetching techniques within background workers.
- **Caching:** Aggressive Redis caching of static tenant configurations and common dashboard metrics.
- **Concurrency Optimization:** Optimizing Uvicorn thread pools, fine-tuning asyncio event loops, and streaming chunk uploads directly to MinIO to minimize API memory pressure.

## Risks & Tradeoffs

- **Operational Risks:** Hybrid Edge/Cloud architecture increases operational complexity and debugging difficulty, especially with intermittent edge connectivity.
- **Scaling Concerns:** Python's GIL overhead in FastAPI during massive concurrent chunk uploads requires careful tuning of worker counts and possibly migrating heavy I/O to Rust/Go in the future if limits are hit.
- **Complexity Tradeoffs:** Choosing HTTP chunked uploads over direct-to-S3 signed URLs simplifies Edge client logic but increases API gateway load and network hops. Tradeoff accepted to maintain strict validation and control over the ingest buffer.

## Agile Sprint Plan

- **Sprint 1 (Completed):** Refined MVP API ingest, stabilized MinIO storage, and established asynchronous Redis worker queues for metrics.
- **Sprint 2 (Current):** Complete Meta Ray-Ban (DAT) end-to-end integration, implement robust DLQs, finalize RBAC schema for school supervision modes, and introduce comprehensive OpenTelemetry tracing.
- **Sprint 3 (Upcoming):** Deploy initial cloud staging environment, benchmark RTX 5070 queue latency, harden API rate limiting, and conduct chaos testing on worker failover.
- **Sprint 4 (Planned):** G2 compliance audit, DPDP data handling review, database read-replica setup, and production infrastructure freeze.
