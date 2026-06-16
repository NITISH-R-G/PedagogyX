# Product Engineering Architecture Report v4

## Problem Analysis

PedagogyX is developing an AI-driven multimodal classroom intelligence platform targeting a primary client base of Meta Ray-Ban smart glasses (DAT) users and low-end Windows smartboards. The system needs to operate efficiently in constrained environments (Indian schools with low bandwidth), using a centralized OSS-based inference cloud powered by consumer-grade GPUs (e.g., RTX 5070). We must enforce a strict zero-trust, privacy-focused architecture compliant with India's DPDP framework, specifically blocking production student data until G2 clearance is achieved. The core challenge is maintaining robust multi-stream ingestion, low-latency processing, high reliability, maintainability, and exceptional product quality with zero customer budget for infrastructure.

## Architecture Design

- **Client Tier**
  - Android-based DAT host app for Meta Ray-Ban glasses and low-end Windows smartboards acting as capture agents.
  - Edge nodes (District/School LAN) providing resilient ingest buffering.
- **Ingestion & API Plane**
  - FastAPI serving as the stateless gateway for session management and HTTP chunk ingestion, coupled with RBAC for tenant isolation.
- **Asynchronous Processing Workers**
  - Background Python workers (ASR via faster-whisper, CV via YOLO, and metrics processors) pulling jobs from Redis queues.
- **Data & Storage**
  - PostgreSQL for structured relational data and pedagogical indices.
  - MinIO (S3-compatible) for durable object storage of video/audio chunks and ML artifacts.
- **Frontend Presentation**
  - Next.js based Admin Shell to visualize insights across a two-path system: Hot Path (real-time heuristics) and Cold Path (authoritative batch evaluations).

## Implementation Strategy

- **Phase 1: Ingestion & Storage**
  - Deploy Docker Compose stack encompassing FastAPI, MinIO, PostgreSQL, and Redis.
  - Develop resilient, resumable chunk upload APIs with signature validation to handle intermittent connectivity.
- **Phase 2: Worker Pipelines**
  - Integrate Redis queues with Celery/Python worker stubs (`worker-asr` and `worker-metrics`).
  - Implement a Dead Letter Queue (DLQ) pattern to catch processing exceptions and avoid main queue poisoning.
- **Phase 3: Frontend & Analytics**
  - Implement the Next.js React Server Components (RSC) to serve the teacher pedagogy dashboards and live analytics bus securely.
- **Phase 4: Optimization**
  - Move from CPU-bound mock processing to GPU-bound (RTX 5070) inference models using TensorRT and vLLM.

## Code Quality Strategy

- **Static Analysis & Formatting**
  - Enforce Ruff for Python formatting, linting, and bug detection.
  - Use ESLint and Prettier for the Next.js frontend TypeScript codebase.
  - Apply markdownlint for all documentation checks via `./scripts/dev-verify.sh --docs-only`.
- **Testing & Coverage**
  - Mandatory unit tests for all services. API tests must mock database/MinIO.
  - UI components verified using Vitest.
- **Type Safety**
  - Strict type checking utilizing Pydantic models in Python and TypeScript interfaces in the React frontend.

## Performance Optimization

- **Database Access**
  - Share database cursors in backend helper functions to mitigate N+1 query inefficiencies.
- **Worker Concurrency**
  - Run background inference (ASR, CV) on dedicated workers outside the API process pool to avoid starvation.
- **Frontend Optimization**
  - Next.js RSC is used extensively to minimize JavaScript bundle sizes delivered to clients, enhancing initial render speeds.
- **Model Efficiency**
  - Quantization (e.g., INT4/AWQ) for Large Language Models to fit comfortably within the 12GB VRAM constraints of the RTX 5070.

## Security Considerations

- **Environment Management**
  - Explicit enforcement of critical environment variables (e.g., `DATABASE_URL`, `REDIS_URL`, `API_KEY`) to prevent default-bypass vulnerabilities.
- **Authentication & RBAC**
  - Implement robust API key validation and structured RBAC to ensure supervision limits are strictly maintained per the G2 clearance protocol.
- **Input Validation**
  - Rigorous Pydantic schema validation on all API inputs to prevent injection attacks.
- **Data Privacy**
  - Student faces and identifiers are strictly excluded from LLM context; only anonymized metadata and transcripts are processed.

## Observability

- **Structured Telemetry**
  - Aggregate standardized JSON logs from FastAPI and worker services.
  - Explicitly log worker failures, full tracebacks, and exceptions to `sys.stderr` via the DLQ flow.
- **Health Checks**
  - System-wide `/health` probes across all services, checked natively via `dev-verify.sh`.
- **Inference Monitoring**
  - Monitor GPU VRAM utilization, Celery queue wait times, and model drift in the pedagogical indices.

## Refactoring Opportunities

- **Dead Letter Queue Robustness**
  - Standardize error handling and DLQ mechanisms across all async Python workers (`worker-asr`, `worker-metrics`, `worker-cv`).
- **CSS Architecture**
  - Migrate legacy inline styles in the Next.js admin shell to Tailwind CSS v4 utility classes.
- **API Modularization**
  - Break down large API controllers into smaller, domain-driven service modules to reduce coupling.

## Risks & Tradeoffs

- **Edge Connectivity Vulnerability**
  - Relying on intermittent school networks increases upload failure risk. **Tradeoff**: Implementing robust edge buffering complexity vs. simplified client apps.
- **Hardware Constraints**
  - Consumer-grade GPUs (RTX 5070 with 12GB VRAM) heavily restrict model sizes. **Tradeoff**: We use specialized, unimodal extraction (Whisper + YOLO) followed by late text fusion instead of memory-heavy multimodal models.
- **Data Privacy Blockers**
  - The strict G2 compliance block delays testing with real student data. **Tradeoff**: Reliance on synthetic mock data (MDK) limits early ML accuracy benchmarking but mitigates catastrophic legal risks.

## Agile Sprint Plan

- **Sprint 1: Core API & Storage MVP**
  - Set up PostgreSQL schemas, MinIO buckets, and FastAPI endpoints for multipart chunk ingestion.
- **Sprint 2: Async Pipeline Stability**
  - Implement `worker-asr` and `worker-metrics` consumers, establish DLQ patterns, and deploy Redis queue configurations.
- **Sprint 3: Wearables Client Integration**
  - Connect the Android DAT companion app and Meta Ray-Ban simulator to the backend API. Ensure end-to-end data flow.
- **Sprint 4: UI Dashboards & Frontend Verification**
  - Finalize Next.js Server Components, apply Tailwind styling, and deploy the live analytics dashboard for the Hot Path metrics.
- **Sprint 5: Scale & Optimization**
  - Profile the backend for cursor N+1 issues and optimize GPU throughput using TensorRT and vLLM. Execute full `./scripts/dev-verify.sh` pipeline validations.
