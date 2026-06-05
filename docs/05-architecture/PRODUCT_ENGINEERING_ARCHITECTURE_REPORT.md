# Product Engineering & Architecture Report

**Status:** Phase 0 Architecture Planning
**Role:** Autonomous Senior Software Engineer & Product Engineering Architect

## Problem Analysis

PedagogyX is developing an AI-driven classroom intelligence platform designed to ingest multimodal data (audio, video, text) via thin clients (specifically Meta Ray-Ban glasses via Android DAT and low-end Windows smartboards) and process this data through a central OSS-based inference cloud. The system operates under severe constraints:

- **Hardware/Cost:** Edge devices have extremely limited compute capacity. The cloud processing cluster relies on affordable consumer-grade GPUs (e.g., RTX 5070), requiring aggressive batching and queuing strategies.
- **Connectivity:** Deployments typically encounter unreliable, low-bandwidth LAN/WAN environments in Indian schools.
- **Privacy/Compliance:** Stringent requirements around data residency (India DPDP), teacher consent, and supervision limits necessitate a zero-trust architecture. Data extraction must prioritize pedagogical feedback rather than punitive surveillance.

## Architecture Design

The current MVP focuses on an end-to-end vertical slice (Session Creation -> Audio Upload -> Faster-Whisper ASR -> Talk Ratio Metrics Display).

- **Client Layer:** Meta Ray-Ban glasses tethered to an Android device (via DAT stream sessions), acting as a capture and chunking buffer.
- **Edge/Buffer Layer:** Intermittent local caching that reliably resumes multi-part uploads over HTTPS.
- **API/Control Plane:** A stateless FastAPI application managing sessions, upload URLs, and RBAC auth. It enqueues processing jobs.
- **Worker Pool:** Dedicated microservices for asynchronous ML workloads (`worker-asr` for audio transcription, `worker-cv` stubbed for future computer vision, `worker-metrics` for talk ratio logic).
- **Data Storage:** Postgres handles structured relational metadata, while MinIO securely archives chunks and ML outputs. Redis manages job queues.
- **Frontend:** A responsive Next.js Admin shell to display Hot Path (preliminary) and Cold Path (authoritative) pedagogical insights.

## Implementation Strategy

1.  **MVP Scaffolding:** Develop Docker Compose-based environment for API, MinIO, Postgres, Redis, workers, and frontend.
2.  **Ingestion API:** Implement robust, resumable endpoints for multi-part chunk uploading that gracefully handle intermittent connectivity.
3.  **Job Pipeline:** Connect the API to Redis queues, triggering the `worker-asr` to transcribe audio with Faster-Whisper, followed by `worker-metrics` calculating preliminary talk ratios.
4.  **UI Dashboards:** Build out a performant React application using Next.js 15 Server Components, ensuring fast initial loads and providing SSE/polling mechanisms for Hot Path metric updates.

## Code Quality Strategy

- **Static Analysis:** Strict enforcement of Ruff for Python code formatting and linting, and ESLint/Prettier for the frontend TypeScript codebase.
- **Testing Constraints:** Required unit test coverage across all critical paths. All modules must include isolated test directories. Backend API tests will mock database/MinIO transactions; frontend UI components will utilize Vitest.
- **Type Safety:** Heavy reliance on Pydantic models for API request/response validation and strict TypeScript interfaces for React Server Components.

## Performance Optimization

- **Decoupled Workloads:** Offloading blocking inference operations (ASR, CV) to background Python workers prevents API starvation.
- **Database Connections:** Sharing cursors in backend helper methods ensures connection pooling is utilized without N+1 instantiation bottlenecks.
- **Frontend Rendering:** Next.js RSC avoids shipping large JS bundles to K-12 admin browsers, rendering static tables server-side.

## Security Considerations

- **Authentication/Authorization:** Immediate implementation of API Keys for MVP, with a firm design roadmap toward OAuth2/OIDC. Tenant isolation (Row-Level Security) is critical.
- **Data Sanitization:** Never trusting client telemetry. Chunk signatures and sizes are strictly validated.
- **Secret Management:** Pydantic settings fall back securely; explicit definition of required environment variables (`DATABASE_URL`, `MINIO_KEYS`, `API_KEY`) is enforced to prevent implicit bypasses or 403 scenarios.

## Observability

- **Structured Logging:** JSON-based operational logging across FastAPI and worker containers. Exception tracebacks (including those in DLQs) strictly pushed to `sys.stderr`.
- **System Health:** Robust `/health` probes across all services integrated into the `dev-verify.sh` and CI flows.

## Refactoring Opportunities

- **Inline Styles in UI:** The Next.js frontend currently contains inline styles which must be systematically migrated to Tailwind CSS utility classes.
- **Worker Pipeline Resilience:** Refactoring the current Redis consumer loops to implement a robust Dead Letter Queue (DLQ) pattern, capturing failed jobs and raw payloads to avoid poisoning the main ingestion stream.

## Risks & Tradeoffs

- **Latency vs. Batching:** Relying on async queues significantly improves cost-efficiency on consumer GPUs but inherently delays the Time-to-Insight (M-B metric).
- **Edge Complexity:** Moving logic to the cloud simplifies the Android DAT client but increases reliance on volatile school internet connections.
- **GIL Limitations:** Utilizing Python for high-concurrency API nodes might introduce CPU bottlenecks; horizontal scaling via Uvicorn workers is a required tradeoff to leverage the broader ML ecosystem.

## Agile Sprint Plan

- **Sprint 3 (Current):** Stand up the core API, PostgreSQL schemas, and MinIO upload endpoints. Run mock captures and finalize the Next.js static scaffold.
- **Sprint 4:** Solidify the `worker-asr` integration (Faster-Whisper on CPU/GPU depending on environment) and the `worker-metrics` pipeline.
- **Sprint 5:** Transition the Android DAT client from synthetic uploads to live Meta Ray-Ban captures. Refine frontend dashboards to consume live metrics.
