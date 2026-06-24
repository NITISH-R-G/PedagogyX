# Backend Architecture Report v3.0

**Date:** 2026-06-15
**Role:** Autonomous Senior Backend Developer & Distributed Systems Architect
**Context:** PedagogyX Phase 0 + MVP boilerplate. Upgraded architecture for Meta Ray-Ban (DAT) primary client ingest, robust chunked video/audio processing, asynchronous ML worker orchestration (ASR, CV, LLM on RTX 5070), and stringent reliability and scalability improvements.

## System & Requirement Analysis

- **Requirements:**
  - Handle massive concurrency of high-throughput multimodal ingest (audio/video chunks) from Meta Ray-Ban glasses via Edge Android devices.
  - Process live preview metrics and orchestrate cold path GPU ML inference (ASR, CV, LLM) effectively on constrained central GPU compute (single RTX 5070 per ADR-0006).
  - Guarantee fault tolerance, low-latency administrative dashboards, strict tenant isolation, and India data residency.
- **Constraints:**
  - ₹0 per-classroom edge hardware budget.
  - OSS-only ML stack with constrained central GPU compute limit.
  - Intermittent and unreliable edge network connections in schools.
- **Edge Cases:**
  - Network drops during chunked uploads requiring robust resumability.
  - Spiky ML processing leading to deep queues; requires intelligent backpressure.
  - Out-of-order data stream synchronization.
- **Scale Assumptions:**
  - Phased India rollout starting with pilot scale.
  - Requires horizontal architectural runway for API gateway and control plane.
  - Worker pools must flexibly scale, though bound by hardware limitations.

## Backend Architecture

- **Services:**
  - `api`: FastAPI-based stateless control plane managing CRUD, session lifecycle, and chunked high-throughput ingestion.
  - `worker-metrics`: Python background worker generating live "preview" metrics. Entry point: `worker.metrics_main`.
  - `worker-asr`: Python background worker orchestrating audio transcription. Entry point: `worker.asr_main`.
  - `worker-cv`: Python background worker handling Phase 2 video processing.
- **APIs:**
  - RESTful HTTP APIs `/v1/sessions/*` for session orchestration.
  - Reliable chunked binary upload endpoints over HTTPS.
- **Data Flow:**
  Capture Client (Android DAT) → Load Balancer → FastAPI Gateway → MinIO (Object Storage) → Redis (Job Queues) → Python Worker Pool (ASR/CV/Metrics) → PostgreSQL (Scores/Metadata) → Web Client (React/Next.js Dashboards).
- **Event Systems:**
  - Redis-backed decoupled message queues serving as the asynchronous event bus between the API tier and ML background workers.
- **Abstractions:**
  - Strict separation of the high-throughput ingest layer (hot buffer) and the heavy ML processing layer (cold buffer). This prevents slow workers from dragging down API ingestion performance.

## Database Design

- **Schema:**
  - PostgreSQL relational schema strongly enforcing strict referential integrity.
  - Core entities: `tenant_id`, `school_id`, `session_id`, `chunk_metadata`, `metrics`.
- **Indexing:**
  - Targeted B-Tree indexing on highly queried fields: `session_id`, `school_id`, `tenant_id`, and `status`.
- **Caching:**
  - Redis for in-memory caching of tenant configurations and session metadata to alleviate PostgreSQL load.
- **Consistency Strategy:**
  - Strong consistency for ingest metadata and session states in PostgreSQL.
  - Eventual consistency for delayed ML output metrics and analytical aggregations.
- **Scaling Strategy:**
  - PgBouncer for robust connection pooling across multiple horizontal API instances and workers.
  - Read-replicas slated for heavy read-path dashboard workloads.

## API Strategy

- **Endpoints:** Clean, predictable REST abstractions scoped under `/v1/`.
- **Validation:**
  - Pydantic models utilized comprehensively for rigid schema enforcement, payload bounds checking, and type safety.
- **Authentication:**
  - Cryptographically secure OAuth2/OIDC integration planned for G2 compliance.
- **Rate Limiting:**
  - Multi-tiered rate limiting (IP-based and Tenant-based) implemented at the API Gateway to gracefully handle DoS and prevent bulk upload flooding.
- **Versioning:**
  - Explicit URL-level versioning (e.g., `/v1/`) ensuring backward compatibility as Android DAT clients evolve.

## Scalability Strategy

- **Horizontal Scaling:**
  - Fully stateless FastAPI nodes designed for effortless horizontal scaling behind L7 Load Balancers.
- **Caching:**
  - Aggressive caching of static and semi-static API responses and configurations to reduce database round-trips.
- **Partitioning:**
  - Tenant-based logical data partitioning built into the schema foundation, setting up future physical sharding.
- **Async Processing:**
  - Asynchronous message-driven architecture. API offloads intensive ML tasks immediately to Redis, returning HTTP 202 Accepted.
- **Load Balancing:**
  - L7 routing distributing high-throughput HTTP chunk streams uniformly across API instances.

## Reliability Strategy

- **Retries:**
  - Exponential backoff with jitter natively supported for inter-service communications and edge client uploads.
- **Failover:**
  - Completely stateless control plane ensures immediate request routing to healthy nodes upon instance failure.
- **Redundancy:**
  - High availability targets via Multi-AZ deployed MinIO storage and replicated PostgreSQL clusters.
- **Recovery Mechanisms:**
  - Robust Dead Letter Queues (DLQ) for failed worker jobs to prevent continuous crashing (poison pill messages) and facilitate manual/automated reprocessing.

## Security Strategy

- **Authentication:**
  - Strong cryptographic identities established for IoT/Edge ingest devices.
- **Authorization:**
  - Rigid Role-Based Access Control (RBAC) ensuring uncompromisable tenant boundaries and strict Supervision Mode adherence.
- **Validation:**
  - Zero-trust input boundaries. All payloads are extensively sanitized and validated via FastAPI/Pydantic before internal processing.
- **Vulnerability Prevention:**
  - Dependency scanning and pre-commit linters (Ruff). HTTPS enforcement across all external and internal transit boundaries.

## Observability

- **Logging:**
  - Centralized, structured JSON logging outputting trace IDs (e.g., `session_id`, `worker_mode`) across API and workers for unified SIEM consumption.
- **Tracing:**
  - Distributed tracing (OpenTelemetry) mapping request lifecycles from Edge client upload to background worker completion.
- **Monitoring:**
  - Detailed metrics emitted for system health: Redis queue depth, worker processing latency, HTTP p50/p95/p99 response times, and error rates.
- **Alerting:**
  - Intelligent alerting triggers on DLQ spike anomalies, API health degradation, and storage latency, wired to PagerDuty.

## Performance Optimization

- **Bottlenecks:**
  - ML GPU throughput (RTX 5070 constraints) is decoupled from ingest. Queue depth is carefully monitored to trigger dynamic backpressure.
- **Query Optimization:**
  - Pre-emptive elimination of N+1 query patterns using well-structured JOINs and batched inserts via SQLAlchemy/PostgreSQL cursors.
- **Caching:**
  - In-memory tenant caching significantly reduces initial HTTP request overhead.
- **Concurrency Optimization:**
  - Uvicorn asynchronous thread pools tuned for optimal handling of thousands of simultaneous chunked I/O bounds without GIL blocking issues.

## Risks & Tradeoffs

- **Operational Risks:**
  - The Hybrid Edge-Cloud deployment amplifies operational complexity. Debugging distributed asynchronous workers requires a mature observability stack.
- **Scaling Concerns:**
  - Single central GPU bottleneck could result in significant metric delivery delays during peak school hours. Mitigated by prioritizing hot-path metrics over cold-path heavy inference.
- **Complexity Tradeoffs:**
  - Leveraging HTTP chunked uploads to the API adds computational load to the gateway compared to direct-to-S3 signed URLs, but provides critically required immediate payload validation, boundary security, and ingest control.

## Agile Sprint Plan

- **Sprint 1 (Current):** Optimize robust API ingestion layer for massive concurrency. Harden MinIO storage integration and Redis queues for core worker dispatch.
- **Sprint 2:** Expand Meta Ray-Ban end-to-end telemetry. Implement comprehensive Dead Letter Queues (DLQs) and automated retry capabilities.
- **Sprint 3:** Deploy OpenTelemetry distributed tracing. Benchmark end-to-end latency with the RTX 5070 worker pool and optimize database query patterns.
- **Sprint 4:** Execute comprehensive load testing for edge cases (network drops). Finalize G2 compliance sign-offs and lock production infrastructure definitions.
