# Product Engineering Architecture Report v4

## Problem Analysis

PedagogyX is developing an advanced AI-driven multimodal classroom intelligence platform. The primary client base includes Meta Ray-Ban smart glasses (DAT) users and low-end Windows smartboards acting as edge capture agents. The operational environment is highly constrained, targeting Indian schools with low bandwidth and intermittent connectivity. The system requires a centralized OSS-based inference cloud powered by consumer-grade GPUs (e.g., RTX 5070) to meet the zero customer budget constraint for infrastructure (D-10 constraint). We must maintain a robust multi-stream ingestion system, provide low-latency processing, and ensure high reliability. Due to India's DPDP framework, the platform must enforce a strict zero-trust, privacy-focused architecture, blocking production student data until G2 clearance is achieved. The engineering challenge is delivering a scalable, responsive product experience under severe hardware, network, and regulatory constraints.

## Architecture Design

- **Client & Edge Tier**
  - Android-based DAT host app for Meta Ray-Ban glasses and low-end Windows smartboards as primary capture agents.
  - Edge nodes on the district or school LAN acting as resilient ingestion buffers to handle intermittent uplink connectivity.
- **Ingestion & API Gateway**
  - A FastAPI-based stateless API gateway handles session management, HTTP chunk ingestion, authentication, and structured RBAC for strict tenant isolation.
- **Asynchronous Processing Plane**
  - Background Python workers extract insights from the data using specialized models (ASR via faster-whisper, CV via YOLO). These workers consume jobs from Redis queues.
- **Data & Storage Layer**
  - PostgreSQL serves as the primary relational store for structured data, pedagogical indices, and system state.
  - MinIO (S3-compatible) provides durable object storage for video/audio chunks and ML artifacts.
- **Frontend Presentation Layer**
  - A Next.js (App Router) based Admin Shell visualizes insights, operating via two primary data paths: a Hot Path for real-time heuristics and a Cold Path for authoritative batch evaluations.

## Implementation Strategy

- **Phase 1: Resilient Edge Ingestion**
  - Enhance the FastAPI backend and Edge LAN buffers to support highly resilient, resumable multipart chunk uploads with cryptographic signature validation to combat intermittent connectivity.
- **Phase 2: Scalable Async Processing**
  - Harden the Redis queue architecture with Celery/Python workers (`worker-asr`, `worker-metrics`, `worker-cv`).
  - Solidify Dead Letter Queue (DLQ) implementations to catch and handle processing exceptions gracefully.
- **Phase 3: Secure Data Storage MVP**
  - Deploy PostgreSQL schemas for relational models and pedagogical indices. Configure MinIO buckets with strict lifecycle policies for temporary ML artifact storage.
- **Phase 4: Frontend Next.js Admin Shell**
  - Deliver the Next.js React Server Components (RSC) dashboard for teacher pedagogy insights and live analytics.
- **Phase 5: Constrained GPU Optimization**
  - Transition from CPU-bound mock processing to GPU-bound inference on consumer-grade hardware (RTX 5070) using TensorRT and vLLM.

## Code Quality Strategy

- **Static Analysis & Linting**
  - Enforce Ruff for Python formatting, linting, and bug detection to ensure consistent code quality.
  - Utilize ESLint and Prettier for the Next.js frontend to maintain strict TypeScript standards.
  - Apply markdownlint for comprehensive documentation validation via `./scripts/dev-verify.sh --docs-only`.
- **Testing & Coverage Requirements**
  - Mandate rigorous unit tests for all backend services, utilizing comprehensive mocks for database and MinIO interactions.
  - Validate UI components and React hooks using Vitest and React Testing Library.
- **Type Safety & Contracts**
  - Enforce strict type checking across boundaries: Pydantic models in the Python backend and TypeScript interfaces in the React frontend.

## Performance Optimization

- **Database Efficiency**
  - Utilize shared database cursors in backend data access layers and implement dataloaders to mitigate N+1 query inefficiencies.
- **Worker Concurrency & Isolation**
  - Isolate background inference (ASR, CV) on dedicated worker nodes separate from the API process pool to prevent resource starvation.
- **Frontend Render Optimization**
  - Maximize the use of Next.js React Server Components (RSC) to minimize client-side JavaScript bundle sizes and accelerate initial page loads.
- **Model Inference Efficiency**
  - Implement model quantization (e.g., INT4/AWQ) for Large Language Models to operate within the 12GB VRAM constraints of the targeted RTX 5070 hardware.

## Security Considerations

- **Strict Environment & Secret Management**
  - Enforce explicit validation of critical environment variables (e.g., `DATABASE_URL`, `REDIS_URL`, `API_KEY`) to prevent default-bypass vulnerabilities and secure infrastructure access.
- **Authentication & RBAC Controls**
  - Implement robust API key validation and structured RBAC to ensure supervision limits are strictly maintained per the G2 clearance protocol requirements.
- **Input Validation & Sanitization**
  - Apply rigorous Pydantic schema validation on all incoming API requests to mitigate injection attacks and malformed data issues.
- **Data Privacy & Anonymization**
  - Strictly exclude student faces and PII identifiers from LLM context windows; process only anonymized metadata and transcripts to maintain DPDP compliance.

## Observability

- **Structured Logging & Telemetry**
  - Aggregate standardized JSON-formatted logs from FastAPI endpoints and worker services into a centralized observability stack.
- **Robust Exception Tracking**
  - Explicitly log worker failures, full tracebacks, and pipeline exceptions to `sys.stderr` and monitoring platforms via the standardized DLQ flow.
- **Proactive Health Checks**
  - Implement system-wide `/health` probes across all services, checked natively during CI via the `dev-verify.sh` script.
- **Inference & Infrastructure Monitoring**
  - Monitor critical infrastructure metrics including GPU VRAM utilization, Celery queue wait times, latency distributions, and model drift in the pedagogical indices.

## Refactoring Opportunities

- **Dead Letter Queue (DLQ) Standardization**
  - Standardize error handling and DLQ retry mechanisms across all async Python workers (`worker-asr`, `worker-metrics`, `worker-cv`) to reduce boilerplate and improve reliability.
- **Next.js CSS Architecture Modernization**
  - Migrate legacy inline styles and disjointed CSS within the Next.js admin shell to cohesive Tailwind CSS v4 utility classes for maintainability.
- **API Domain Modularization**
  - Break down large FastAPI routing controllers into smaller, domain-driven service modules to reduce tight coupling and improve testability.

## Risks & Tradeoffs

- **Edge Connectivity vs. Architecture Complexity**
  - Relying on intermittent school networks increases data loss risks. **Tradeoff**: Implementing complex edge buffering nodes improves reliability but adds significant architectural overhead and maintenance cost compared to a direct-to-cloud model.
- **Hardware Constraints vs. Model Capability**
  - Consumer-grade GPUs (RTX 5070 with 12GB VRAM) heavily restrict AI model sizes. **Tradeoff**: Utilizing specialized, unimodal extraction models (Whisper + YOLO) with late text fusion enables operation within budget but sacrifices the nuanced understanding of heavy multimodal LLMs.
- **Data Privacy Blockers vs. Product Iteration**
  - Strict G2 compliance delays real-world testing with student data. **Tradeoff**: Relying on synthetic mock data (MDK) enables continued development and mitigates catastrophic legal risks but limits early empirical ML accuracy benchmarking.

## Agile Sprint Plan

- **Sprint 1: Edge Ingestion & API MVP**
  - Establish PostgreSQL schemas, MinIO buckets, and FastAPI endpoints to support robust, resumable multipart chunk ingestion.
- **Sprint 2: Async Processing Pipelines**
  - Implement primary consumers for `worker-asr` and `worker-cv`, establish robust DLQ patterns, and finalize Redis queue configurations.
- **Sprint 3: Wearables Client Integration**
  - Connect the Android DAT companion app and Meta Ray-Ban simulator to the backend API, ensuring seamless end-to-end data flow and error handling.
- **Sprint 4: Next.js Admin Dashboard**
  - Finalize React Server Components, apply standardized Tailwind styling, and deploy the live analytics dashboard for real-time Hot Path metrics.
- **Sprint 5: System Scale & Optimization Validation**
  - Profile the backend to resolve N+1 query issues, optimize GPU throughput using TensorRT and vLLM, and execute full `./scripts/dev-verify.sh` pipeline validations.
