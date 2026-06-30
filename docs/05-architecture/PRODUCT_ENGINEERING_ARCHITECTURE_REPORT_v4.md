# Product Engineering Architecture Report v4

## Problem Analysis

PedagogyX is building an AI-driven multimodal classroom intelligence platform. The primary client base includes Meta Ray-Ban smart glasses (DAT) users and low-end Windows smartboards, operating as edge capture agents.

- **Requirements**: Robust multi-stream ingestion from edge capture agents; low-latency processing for real-time pedagogical insights (Hot Path) and authoritative batch evaluations (Cold Path).
- **Constraints**: Deployment targets constrained environments (e.g., Indian schools with low bandwidth). Centralized OSS-based inference must run on consumer-grade GPUs (e.g., RTX 5070 with 12GB VRAM). Zero customer budget for infrastructure (D-10 constraint).
- **Edge Cases**: Intermittent connectivity during video/audio uploads; failed asynchronous jobs; data malformations; partial multimodal stream ingestion.
- **Scalability Considerations**: The architecture must scale efficiently through horizontal worker instances processing background queues while ensuring PostgreSQL connection pools do not get exhausted during burst ingestions.

## Architecture Design

- **Components**:
  - Edge clients (Meta Ray-Ban DAT, Windows smartboards).
  - API Gateway (`services/api` via FastAPI).
  - Worker Pipelines (`services/worker-asr`, `services/worker-cv`, `services/worker-metrics`).
  - Next.js Admin UI (`services/web`).
- **Data Flow**: Edge nodes capture and buffer data, sending resumable HTTP chunks to the FastAPI gateway. The gateway stores chunks in MinIO and metadata in PostgreSQL, enqueuing processing tasks to Redis. Workers pull tasks, perform ML inference, and store results. The Next.js frontend retrieves insights from the API.
- **APIs**: FastAPI exposes stateless, resumable chunk ingestion and session management APIs with RBAC.
- **Abstractions**: Abstracted storage layer (S3-compatible) using MinIO; abstracted message bus (Redis).
- **Service Boundaries**: Hard boundaries between synchronous ingest gateway (FastAPI) and asynchronous ML processing (Python Celery Workers). UI layer isolated in React/Next.js.

## Implementation Strategy

- **Step by Step Plan**:
  1. Solidify FastAPI ingestion logic and PostgreSQL database schema.
  2. Implement reliable Redis queuing for Celery workers with a strong Dead Letter Queue (DLQ).
  3. Deploy Next.js frontend integrating with backend APIs for real-time telemetry.
  4. Optimize GPU inference with TensorRT and quantization.
- **Modules**: `api` (ingest), `worker-asr` (speech-to-text), `worker-cv` (computer vision), `worker-metrics` (analytics), `web` (admin shell).
- **Dependencies**: FastAPI, PostgreSQL, MinIO, Redis, Celery, faster-whisper, YOLO, Next.js, React.
- **Workflows**: Device provisioning -> Session creation -> Chunk ingestion -> Async processing -> Analytics visualization.

## Code Quality Strategy

- **Testing**: End-to-end synthetic testing of pipelines (`make dat-session`). Mandatory API unit testing mocking DB/MinIO. Vitest for UI components.
- **Validation**: Strict Pydantic models for all API requests/responses in FastAPI. TypeScript interfaces mirroring Pydantic definitions in the Next.js frontend.
- **Linting**: Ruff for Python (`ruff check services tools`). ESLint/Prettier for Next.js. Markdown linting for docs (`npx markdownlint-cli`).
- **Type Safety**: Enforced strict mode in TypeScript; MyPy or Ruff type checking enabled for Python microservices.

## Performance Optimization

- **Bottlenecks**: N+1 queries in the FastAPI layer; queue starvation on single GPU instances; memory exhaustion during large chunk processing.
- **Caching**: Aggressive caching of frequent API GET requests using Redis. Edge caching for static Next.js assets.
- **Concurrency**: Background inference runs out-of-process via Celery workers, freeing up FastAPI event loop for high-throughput ingestion.
- **Optimization Strategy**: Share DB cursors in backend helper functions to avoid N+1 queries. Utilize INT4/AWQ quantization for models to fit in the 12GB VRAM constraints of the RTX 5070.

## Security Considerations

- **Authentication**: Zero-trust API architecture using secure API key validation. Strict tenant isolation for school sessions.
- **Authorization**: Role-Based Access Control (RBAC) ensuring supervision limits align with G2 clearance protocols.
- **Validation**: Comprehensive schema validation to mitigate injection, XSS, and payload tampering attacks.
- **Vulnerability Mitigation**: Production student data is strictly blocked from the system until G2 DPDP clearance. LLM context strips identifiable faces and PII. Strict environment variable enforcement (e.g., `DATABASE_URL`, `API_KEY`).

## Observability

- **Logging**: Structured JSON logging across all FastAPI and Python worker containers. Explicit error tracebacks mapped to stderr via DLQ.
- **Monitoring**: `/health` checks across all services. Monitoring GPU VRAM usage and Redis queue depths.
- **Diagnostics**: End-to-end tracing headers propagated from edge clients through the API gateway to async workers for granular request tracing.

## Refactoring Opportunities

- **Simplifications**: Centralize DLQ handling and error reporting across `worker-asr`, `worker-cv`, and `worker-metrics` into a single shared `core-worker` library.
- **Modularization**: Break down large API controllers in FastAPI into modular, domain-driven route handlers.
- **Maintainability Improvements**: Migrate the Next.js admin shell from legacy inline CSS or standard stylesheets to fully adopted Tailwind CSS v4 utility classes.

## Risks & Tradeoffs

- **Technical Risks**: Frequent network drops from edge devices in bandwidth-constrained Indian schools leading to incomplete streams.
- **Scaling Limitations**: Standardizing on consumer GPUs limits large monolithic ML models.
- **Complexity Tradeoffs**: We trade simplified deployment (monolith) for a distributed architecture (FastAPI + Workers) to ensure ML inference latency does not block core API ingestion threads. We trade multimodal LLMs for unimodal processing (Whisper + YOLO) due to 12GB VRAM restrictions.

## Agile Sprint Plan

- **Milestones**:
  - M1: Robust API Ingestion & Storage.
  - M2: Asynchronous Worker Pipeline and DLQ robustness.
  - M3: End-to-End Client Integration (Meta Ray-Ban Simulator).
  - M4: Next.js Frontend Dashboards.
  - M5: GPU Profiling and Optimization.
- **Priorities**: System reliability and ingestion stability (M1 & M2) are P0, followed by client integration (M3).
- **Implementation Phases**:
  - Sprint 1: Setup schemas, MinIO, and chunk endpoints.
  - Sprint 2: Deploy Celery workers with Redis, test DLQ patterns.
  - Sprint 3: Connect Android DAT simulator.
  - Sprint 4: Build hot-path analytics UI in Next.js.
  - Sprint 5: Quantization, TensorRT integrations, and final E2E benchmarking.
- **Expected Outcomes**: A highly reliable, privacy-compliant, low-latency API architecture capable of processing multimodal capture data in zero-infrastructure edge environments.
