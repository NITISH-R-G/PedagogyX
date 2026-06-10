# Product Engineering Architecture Report v4

## Problem Analysis

PedagogyX is an AI-driven multimodal classroom intelligence platform. The primary goal is to use Meta Ray-Ban smart glasses (via the Wearables Device Access Toolkit and an Android companion app) and low-end Windows smartboards as v1 capture clients to ingest classroom data.
The system needs to operate efficiently in constrained environments such as Indian schools with low bandwidth, using a centralized OSS-based inference cloud powered by consumer-grade GPUs (e.g., RTX 5070).
A significant constraint is the D-10 operational requirement, meaning zero customer budget for infrastructure. Furthermore, a strict zero-trust, privacy-focused architecture compliant with India's DPDP framework is mandatory, specifically blocking production student data until G2 clearance is achieved. This forces reliance on synthetic data (MDK) for MVP iterations. The challenge is balancing multi-stream ingestion, low-latency processing, and robust resilience within tight financial and hardware limits.

## Architecture Design

- **Client Tier**
  - Android-based DAT host app for Meta Ray-Ban glasses, alongside low-end Windows smartboards, acting as primary capture agents.
  - Edge buffering mechanisms to handle intermittent school network connectivity.
- **Ingestion & API Plane**
  - FastAPI stateless gateways for session management, RBAC, and reliable HTTP chunk ingestion.
- **Asynchronous Processing Plane**
  - Decoupled Python background workers processing audio via faster-whisper (`worker-asr`), computer vision via YOLO (`worker-cv`), and generating pedagogy insights (`worker-metrics`), all coordinated via Redis message queues.
- **Storage Tier**
  - PostgreSQL for relational pedagogical indices, RBAC policies, and application metadata.
  - MinIO for highly durable, S3-compatible object storage of chunked video/audio and extracted ML artifacts.
- **Frontend Presentation**
  - Next.js (v15) Admin Shell utilizing React Server Components (RSC) and Tailwind CSS (v4) to visualize insights via a Hot Path (real-time heuristics) and a Cold Path (authoritative batch evaluations).

## Implementation Strategy

- **Phase 1: Robust Ingestion MVP**
  - Solidify Docker Compose environment with FastAPI, MinIO, PostgreSQL, and Redis. Ensure resumable chunk upload APIs correctly validate signatures and handle connectivity loss gracefully.
- **Phase 2: Asynchronous Pipeline Hardening**
  - Flesh out the Celery/Python worker structure for `worker-asr` and `worker-cv`. Integrate Dead Letter Queues (DLQs) to prevent queue blocking from malformed edge payloads.
- **Phase 3: Real-Time Frontend Dashboards**
  - Develop Next.js Admin Shell interfaces utilizing Tailwind CSS v4. Connect live analytics busses to visualize the Hot Path metrics.
- **Phase 4: Hardware-Optimized Inference**
  - Transition from CPU-bound mock workers to GPU-accelerated (RTX 5070) inference using optimizations like TensorRT and vLLM to maximize throughput per node.

## Code Quality Strategy

- **Static Analysis**
  - Python: Enforce Ruff for all linting, formatting, and standard bug detection across `services`, `tools`, and `packages`.
  - Frontend: Use ESLint and Prettier for the Next.js TypeScript codebase.
  - Docs: Markdownlint validation across all documentation.
- **Testing**
  - Unit tests covering FastAPI route initialization and config (checking `app.title`, `app.routes`) avoiding execution logic tests on pure routing. Database and MinIO dependencies must be heavily mocked.
  - Vitest and Playwright for Next.js UI verification.
- **Type Safety**
  - Strict type checking utilizing Pydantic (Python) for API validation and TypeScript interfaces for the React frontend state.

## Performance Optimization

- **Database Optimization**
  - Resolve N+1 query bottlenecks by optimizing background helper functions and utilizing connection pooling effectively.
- **Worker Concurrency**
  - Ensure background inference processes (ASR, CV) do not compete with the API process pool for resources. Run them on dedicated isolated workers.
- **Frontend Delivery**
  - Maximize the use of Next.js Server Components to offload rendering to the server, dramatically reducing client-side bundle sizes for faster initial paints on constrained school admin networks.
- **Model Efficiency**
  - Employ model quantization techniques (e.g., INT4/AWQ) for Large Language Models to fit execution pipelines securely within the 12GB VRAM constraints of consumer GPUs.

## Security Considerations

- **Strict Environment Governance**
  - Validate presence of critical environment variables (e.g., `DATABASE_URL`, `REDIS_URL`, `API_KEY`) at startup to prevent fallback to insecure defaults.
- **RBAC & Authentication**
  - Rigorous API key authentication. Ensure RBAC constraints firmly separate tenant data, vital for eventual G2 compliance and privacy.
- **Input Validation**
  - All ingestion endpoints must utilize strict Pydantic schemas to validate structural integrity and prevent injection vectors.
- **Data Privacy & Anonymization**
  - Student identifiers and PII are strictly scrubbed before LLM context generation. Only anonymized metadata and text transcripts are passed downstream.

## Observability

- **Unified Telemetry**
  - Aggregate standardized structured JSON logs from both the FastAPI gateway and asynchronous Celery workers.
- **Error Tracking**
  - Explicitly log all worker failures, full tracebacks, and pipeline exceptions via the Dead Letter Queue workflow, streaming critical errors to `sys.stderr`.
- **System Diagnostics**
  - Implement and maintain `/health` endpoints on all microservices, verifiable via the native `./scripts/dev-verify.sh` pipeline.
- **Inference Telemetry**
  - Deep monitoring of RTX 5070 GPU VRAM utilization, processing queue latency, and prediction drift to ensure the 12GB ceiling is respected.

## Refactoring Opportunities

- **DLQ Standardization**
  - Refactor error handling logic across `worker-asr`, `worker-metrics`, and `worker-cv` to utilize a shared, generalized DLQ pattern.
- **Frontend Styling Modernization**
  - Aggressively migrate any remaining legacy inline styles or CSS modules in the Next.js application to standard Tailwind CSS v4 utility classes.
- **API Monolith Decomposition**
  - Split overloaded FastAPI controllers into smaller, domain-isolated service components (e.g., `ingestion`, `session_management`, `rbac`) to reduce module coupling.

## Risks & Tradeoffs

- **Intermittent Edge Connectivity**
  - **Risk:** Unreliable internet in Indian schools leads to data loss. **Tradeoff:** Adding complex edge buffering logic to the DAT companion app increases client weight but ensures data integrity.
- **VRAM Constraints**
  - **Risk:** Consumer GPUs (12GB RTX 5070) limit complex multimodal model usage. **Tradeoff:** We sacrifice memory-heavy end-to-end multimodal architectures in favor of specialized, unimodal extraction (Whisper + YOLO) followed by late text fusion.
- **G2 Privacy Blockers**
  - **Risk:** The inability to test with real student data delays accurate ML baselining. **Tradeoff:** Relying strictly on synthetic mock data (MDK) prevents catastrophic legal exposure but requires aggressive post-G2 model fine-tuning.

## Agile Sprint Plan

- **Sprint 1: Core API & Storage Resiliency**
  - Deploy PostgreSQL, MinIO, and FastAPI. Focus heavily on resumable, secure multipart chunk ingestion endpoints.
- **Sprint 2: Async Processing & DLQs**
  - Stand up Redis queues. Implement base consumers for `worker-asr` and `worker-metrics` with robust Dead Letter Queue error handling.
- **Sprint 3: Wearables Ingestion End-to-End**
  - Connect the Android DAT companion app simulator to the FastAPI backend. Validate the complete synthetic data flow from client to MinIO.
- **Sprint 4: Real-Time Frontend Implementation**
  - Develop the Next.js Admin Shell using Tailwind v4. Connect it to the backend to visualize the Hot Path real-time analytics.
- **Sprint 5: Scale, Optimize, & Validate**
  - Refactor for N+1 queries. Profile and tune GPU inference logic. Ensure all systems pass the comprehensive `./scripts/dev-verify.sh` pipeline cleanly.
