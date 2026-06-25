# Product Engineering Architecture Report v4

## Problem Analysis

The core objective of PedagogyX is to build a highly scalable, real-time multimodal classroom intelligence platform capable of operating in bandwidth-constrained environments (specifically Indian schools). The primary client interface is the Meta Ray-Ban smart glasses (DAT), along with low-end Windows smartboards acting as edge capture nodes.

**Constraints & Edge Cases:**

- **Zero-trust & Privacy Requirements:** A strict data-blocking protocol must be maintained to prevent unauthorized production data access prior to G2 legal clearance.
- **Intermittent Connectivity:** Schools often experience low-bandwidth or disconnected environments, demanding robust, resumable ingestion pipelines.
- **Hardware Limitations:** Centralized OSS-first ML processing is bottlenecked by consumer-grade GPUs (e.g., RTX 5070 with 12GB VRAM), heavily restricting parameter sizes for multimodal processing.
- **Scale:** The system must seamlessly support concurrent streams from numerous classrooms without dropping chunks or causing severe latency.

## Architecture Design

PedagogyX is structured as a Hybrid Edge-Cloud platform to optimally handle the constraints.

**Components & Boundaries:**

- **Capture Layer (Edge):** Android-based Meta Ray-Ban (DAT) app, coupled with Go-based edge ingest buffers running locally on school LANs to prevent data loss.
- **API & Routing Gateway:** A high-performance FastAPI service processing stateless multipart uploads, enforcing immediate authorization checks.
- **Async Workers (Cloud):** A distributed processing tier relying on Redis as a message broker. Dedicated Python workers (`worker-asr` for faster-whisper, `worker-cv` for YOLO, `worker-metrics` for NLP analytics) process background workloads.
- **Storage Subsystem:** PostgreSQL manages tenant configuration and pedagogical metadata. MinIO serves as the S3-compatible backend for durable blob storage of media chunks.
- **Presentation Layer:** Next.js (React) front-end deployed for the Admin Dashboard and pedagogical UI, using React Server Components (RSC) to minimize client overhead.

## Implementation Strategy

A phased rollout strategy is strictly adhered to, allowing for iterative quality control.

- **Phase 1 (Ingest Core):** Finalize FastAPI chunk ingestion endpoints with built-in retry mechanisms and checksum validations for edge nodes. Stand up the fundamental storage tiers (PostgreSQL and MinIO).
- **Phase 2 (Worker Orchestration):** Establish scalable Celery/Redis background task queues. Deploy the ASR, CV, and Metrics workers with Dead Letter Queues (DLQs) to prevent queue poisoning by malformed classroom audio/video chunks.
- **Phase 3 (Analytics Delivery):** Connect the frontend to the real-time hot path data bus (via Websockets or SSE), and present authoritative cold path evaluation data when long-running processing completes.
- **Phase 4 (GPU Optimization):** Standardize the inference tier using vLLM and TensorRT to maximize throughput on RTX 5070 units, focusing on INT4 quantized models.

## Code Quality Strategy

Maintaining high engineering standards is critical for multiple contributors and long-term sustainability.

- **Backend Enforcement:** Strict usage of Ruff for Python linting and formatting. Type safety is enforced via exhaustive Pydantic models for every API request/response.
- **Frontend Governance:** Prettier and ESLint (Strict Mode) are mandatory. All Next.js UI components must utilize TypeScript interfaces and Vitest for coverage.
- **Documentation & Consistency:** Markdownlint ensures all technical documentation is readable and consistent, actively enforced via `./scripts/dev-verify.sh`.
- **Validation:** Automated test suites must cover edge cases, especially network partition simulations and malformed media chunks.

## Performance Optimization

- **Database Scalability:** Aggressive index management and shared connection pools (e.g., PgBouncer) to prevent connection starvation and N+1 query patterns within FastAPI routes.
- **Asset Processing:** Moving audio and video processing entirely out of the synchronous request cycle, assigning them to horizontally scalable worker pools.
- **Frontend Optimization:** Leverage Next.js static site generation (SSG) for static admin pages and incremental static regeneration (ISR) for dashboards to ensure sub-100ms render speeds.
- **ML Throughput:** Employ request batching at the inference API layer to maximize GPU core utilization on the RTX 5070 cards without hitting VRAM OOM limits.

## Security Considerations

Security is enforced comprehensively across all layers via a zero-trust model.

- **Authentication & RBAC:** Enforce explicit, granular API key validation and JWT-based session tokens. Tenant boundaries are structurally isolated to meet G2 privacy protocols.
- **Input Sanitization:** All incoming requests, specifically media metadata and chunk identifiers, must pass Pydantic validation to prevent command injection or path traversal on MinIO storage.
- **Data Anonymization:** Implement real-time scrubbing of PII (faces, specific names) before any payload reaches the LLM context, maintaining compliance with India's DPDP act.
- **Secrets Management:** Environment variables (e.g., `DATABASE_URL`, `REDIS_URL`) are strictly required. Default or hardcoded fallback values are blocked in production configurations.

## Observability

High-granularity metrics are required for immediate issue resolution.

- **Logging:** Structured JSON logs are standardized across FastAPI, React, and Python workers to enable automated parsing and alerting.
- **Tracing:** Inject unique Trace IDs at the FastAPI gateway, propagating them through Redis queues to the background workers, allowing full end-to-end trace reconstruction of a session chunk.
- **Diagnostics:** Explicit logging of worker exceptions, including full tracebacks, are routed to `sys.stderr` and DLQ streams to quickly surface malformed payloads.
- **Metrics Monitoring:** Continuous tracking of Celery queue depths, GPU VRAM saturation, database query latencies (p95, p99), and API response times.

## Refactoring Opportunities

Continuous technical debt reduction to simplify operations.

- **DLQ Standardization:** The current error handling across `worker-asr`, `worker-cv`, and `worker-metrics` is slightly fragmented. Refactor into a unified DLQ base class to ensure consistent retry logic.
- **Frontend Architecture:** Migrate older React class components or inline styled elements within the MVP shell to consistent Tailwind CSS utility classes and functional RSCs.
- **Controller Decoupling:** Break down monolithic FastAPI endpoint files by shifting complex business logic into isolated service layers, enhancing testability and domain separation.

## Risks & Tradeoffs

- **Network Resiliency vs. Complexity:** Implementing edge buffers locally in schools guarantees data capture but significantly increases deployment and monitoring complexity (Tradeoff).
- **Hardware vs. Model Capability:** Limiting infrastructure to RTX 5070s saves substantial operational budget but restricts the platform to smaller, heavily quantized models, potentially impacting real-time accuracy (Tradeoff).
- **Compliance Delays:** The strict G2 PII blocker means relying heavily on synthetic data (MDK). This prevents catastrophic privacy breaches but risks ML models overfitting to mock scenarios prior to public launch (Risk).

## Agile Sprint Plan

- **Sprint 1: Core Foundation & Ingest (Current):** Stand up the Next.js shell, FastAPI gateway, Postgres, and MinIO. Implement basic multipart chunk upload APIs.
- **Sprint 2: Async Processing Pipeline:** Develop and deploy the `worker-asr` and `worker-cv` services. Configure Redis and implement robust DLQ mechanisms.
- **Sprint 3: Client Integration & Wearables:** Connect the Android DAT client to the Edge buffer and subsequently to the API. Establish end-to-end data flow validation using synthetic test suites.
- **Sprint 4: Analytics & Hot Path Delivery:** Build out the Next.js dashboards. Wire the WebSocket/SSE connections to display real-time heuristic feedback from the `worker-metrics` service.
- **Sprint 5: Scale, Audit & Optimize:** Conduct deep performance profiling (identifying N+1 issues, memory leaks). Optimize GPU utilization with vLLM. Perform full end-to-end security audits ahead of the G2 data clearance.
