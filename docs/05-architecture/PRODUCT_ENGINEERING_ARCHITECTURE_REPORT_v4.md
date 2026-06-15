# Product Engineering Architecture Report v4

## Problem Analysis

PedagogyX requires a scalable, resilient, and privacy-first multimodal classroom intelligence platform. The system operates under severe constraints, relying on consumer-grade RTX 5070 GPUs for centralized OSS-based inference, and thin edge devices (Meta Ray-Ban smart glasses via Android DAT and Windows smartboards) for data capture. These edge deployments face unreliable LAN/WAN environments in Indian schools. Furthermore, strict privacy compliance (India DPDP) mandates a zero-trust architecture, barring production student data until G2 clearance.

## Architecture Design

- **Client Layer:** Android DAT host app and Windows smartboards handling raw media capture.
- **Edge Layer:** Local buffering nodes ensuring reliable, resumable multi-part HTTPS uploads.
- **API Plane:** Stateless FastAPI microservice managing session creation, chunk ingestion, and job queuing.
- **Worker Plane:** Dedicated, asynchronous Python worker services (`worker-asr` using Faster-Whisper, `worker-metrics`, `worker-cv`) pulling from Redis queues to isolate CPU/GPU inference from the API.
- **Data Persistence:** PostgreSQL for relational metadata and indices; MinIO for secure, S3-compatible chunk and artifact storage.
- **Frontend Layer:** Next.js Admin shell leveraging React Server Components for Hot Path (real-time) and Cold Path (batch) pedagogical insights.

## Implementation Strategy

1. **MVP Scaffolding:** Establish Docker Compose environments (API, MinIO, PostgreSQL, Redis, and frontend).
2. **Resilient Ingestion:** Implement resumable multi-part endpoints for chunked media uploads.
3. **Async Job Pipeline:** Connect API to Redis queues, activating `worker-asr` for audio transcription and `worker-metrics` for ratio calculations. Implement DLQs to isolate failed jobs.
4. **Interactive Dashboard:** Construct the Next.js admin UI utilizing Tailwind CSS v4 to display actionable insights.

## Code Quality Strategy

- **Static Analysis & Linting:** Strict enforcement of Ruff for Python and ESLint/Prettier for Next.js. Markdown validation via `./scripts/dev-verify.sh --docs-only`.
- **Testing:** Mandatory isolated unit tests. Backend API tests mock database and MinIO interactions; UI verified with Vitest.
- **Type Safety:** Comprehensive use of Pydantic models in Python and strict TypeScript interfaces in React.

## Performance Optimization

- **Decoupled Workloads:** Asynchronous background Python workers handle heavy inference to prevent API thread starvation.
- **Database Efficiency:** Shared cursors within backend helper methods eliminate N+1 query bottlenecks.
- **Frontend Delivery:** Next.js Server Components heavily reduce client-side JS bundles, improving rendering speed.
- **Model Tuning:** Implement model quantization (INT4/AWQ) to fit Large Language Models within the 12GB VRAM limit of the RTX 5070.

## Security Considerations

- **Environment Management:** Explicit variable definitions (`DATABASE_URL`, `MINIO_KEYS`, `API_KEY`) to prevent unsafe defaults.
- **Auth & Authorization:** API Key validation and RBAC for strict tenant isolation.
- **Data Sanitization:** Rigorous validation of client payloads; chunk signatures are verified before storage.
- **Privacy:** Exclusion of student faces and identifiers from LLM processing contexts; adherence to the G2 compliance block.

## Observability

- **Structured Logging:** Centralized JSON logging across all containers. Exception tracebacks and DLQ events output directly to `sys.stderr`.
- **Health Probes:** Comprehensive `/health` endpoints integrated into CI/CD (`dev-verify.sh`).
- **Inference Monitoring:** Tracking of GPU VRAM usage and Celery/Redis queue latencies.

## Refactoring Opportunities

- **UI Styling:** Systematically transition any inline CSS within the Next.js shell to Tailwind v4 utilities.
- **Pipeline Resilience:** Standardize the Dead Letter Queue (DLQ) implementations across all async Python workers (`worker-asr`, `worker-cv`, `worker-metrics`).
- **API Domain Splitting:** Break down monolithic API controllers into focused, domain-driven modules.

## Risks & Tradeoffs

- **Edge Connectivity Vulnerability:** High reliance on intermittent school networks increases risk of upload failure. Tradeoff: Complex edge buffering versus simplified client logic.
- **Hardware Limitations:** RTX 5070 constraints dictate the use of specialized, unimodal extraction (Whisper/YOLO) over memory-intensive multimodal models.
- **Data Privacy Blockers:** The G2 compliance block necessitates reliance on synthetic data (MDK), limiting early real-world ML accuracy benchmarking.

## Agile Sprint Plan

- **Sprint 1: Core API & Storage MVP** Set up PostgreSQL schemas, MinIO, and chunk ingestion endpoints.
- **Sprint 2: Async Pipeline Stability** Implement ASR and metrics consumers, configure Redis, and finalize DLQs.
- **Sprint 3: Wearables Client Integration** Connect Android DAT companion app and Ray-Ban simulator to the backend.
- **Sprint 4: UI Dashboards & Frontend Verification** Finalize Next.js UI, apply Tailwind styling, and launch live analytics.
- **Sprint 5: Scale & Optimization** Resolve N+1 cursor issues, optimize GPU throughput with TensorRT/vLLM, and run full pipeline validations.
