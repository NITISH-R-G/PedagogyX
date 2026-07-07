# Product Engineering Architecture Report v4

## Product & Problem Analysis

PedagogyX is an AI-driven multimodal classroom intelligence platform. The primary client base involves Meta Ray-Ban smart glasses (DAT) users and low-end Windows smartboards acting as edge capture nodes.
The system operates under significant constraints: deployment in environments with low bandwidth (Indian schools), zero customer budget for infrastructure (D-10 constraint), and reliance on a centralized OSS-based inference cloud powered by consumer-grade GPUs (e.g., RTX 5070).
Additionally, strict compliance with India's DPDP framework necessitates a zero-trust, privacy-focused architecture, currently blocking production student data until G2 clearance. The core engineering problem is ensuring resilient multi-stream ingestion, scalable low-latency background processing, robust data storage, and highly usable analytics dashboards, all while optimizing for Maintainability, Scalability, Reliability, User Experience, Developer Experience, Performance, Security, Product Quality, Extensibility, and Production Readiness.

## Full Stack Architecture

The PedagogyX platform is a distributed microservices system designed for end-to-end efficiency:

- **Edge Clients:** Meta Ray-Ban glasses via Android DAT companion apps, and Windows smartboards.
- **Ingestion & API Gateway:** A FastAPI service handles session management, HTTP chunk ingestion, and RBAC tenant isolation.
- **Async Workers:** Background workers (Python/Celery or Redis Streams) process jobs including ASR (`worker-asr` using faster-whisper) and CV processing.
- **Storage Tier:** PostgreSQL for relational pedagogical data; MinIO (S3-compatible) for durable object storage (video/audio chunks).
- **Frontend Presentation:** Next.js (App Router) and React-based web application providing the Admin Shell and real-time visualization of analytics.
- **Caching & Message Queue:** Redis is used for high-throughput queuing and temporary caching between the API and workers.

## Frontend Strategy

The frontend is built with React and Next.js utilizing the App Router to maximize User Experience, Performance, and SEO:

- **UI Architecture:** Component-driven development optimized for React Server Components (RSC) to reduce client-side bundle size.
- **Styling & Design System:** Tailwind CSS v4 provides utility-first styling ensuring visual consistency and rapid iteration.
- **State Management:** Leverage React Context and server-side state where possible. Client state is minimized for responsiveness.
- **Accessibility:** Ensure ARIA compliance and keyboard navigation for all interactive elements in the teacher pedagogy dashboards.
- **Optimization Strategy:** Implement aggressive image/asset optimization, code splitting, and lazy loading. Ensure initial render speed is high even on poor network conditions.

## Backend Strategy

The backend focuses on robust API contracts, fault tolerance, and Operational Simplicity:

- **API Architecture:** RESTful FastAPI gateway handles stateless request routing and synchronous tenant validation.
- **Async Systems:** Event-driven worker architecture offloads heavy AI inference (ASR, CV) to background processes to maintain API latency.
- **Caching:** Redis acts as both a job queue and a fast cache for frequently accessed hot-path metrics.
- **Scalability Strategy:** Stateless API nodes scale horizontally. Workers scale based on queue depth and GPU availability.
- **Fault Tolerance:** Robust Dead Letter Queue (DLQ) implementations for async workers to ensure failed inference jobs do not poison the queue and can be retried or inspected.

## Database Design

The database strategy ensures query efficiency, consistency, and scalability:

- **Schema:** Relational schema in PostgreSQL with strong normalization for tenants, sessions, and analytical metrics.
- **Indexing:** Targeted B-tree indexing on foreign keys and frequently queried temporal fields (e.g., session timestamps) to prevent slow joins.
- **Optimization:** Share database cursors in backend helper functions to prevent N+1 queries. Evaluate read replicas if read-heavy analytics overwhelm the primary node.
- **Consistency Strategy:** Use structured migrations (via SQL scripts in `sql/`) ensuring schema consistency across dev and prod environments.

## Security Strategy

A zero-trust approach compliant with G2 and DPDP frameworks:

- **Authentication & Authorization:** API keys for system services and JWT-based session management for web users. Strict RBAC enforcement.
- **Validation:** Comprehensive input validation utilizing Pydantic in FastAPI to prevent injection attacks and ensure data integrity.
- **Vulnerability Prevention:** Ensure no production student PII is ingested until G2 clearance. Anonymize metadata and transcripts before LLM processing.
- **Secrets Management:** Strict enforcement of environment variables (e.g., `DATABASE_URL`, `REDIS_URL`, `API_KEY`). Avoid hardcoded secrets in source control.

## DevOps & Deployment

Optimizing Developer Experience and deployment reliability:

- **CI/CD:** Automated pipelines via GitHub Actions for testing, linting (Ruff for Python, ESLint/Prettier for JS/TS), and documentation verification (`dev-verify.sh --docs-only`).
- **Hosting & Infrastructure:** Local development relies on a Docker Compose stack (`infra/compose.dev.yaml`). Production targets orchestrated container environments with GPU passthrough for worker nodes.
- **Observability:** Centralized JSON logging across all microservices. Monitor API error rates, worker DLQ metrics, and VRAM utilization for consumer-grade GPUs.
- **Rollback Systems:** Immutable container image tagging and database migration down-scripts to enable rapid rollbacks during deployment failures.

## Testing Strategy

Ensuring high confidence releases and predictable behavior:

- **Unit Testing:** Minimum 85% line coverage for the Python backend using Pytest. Use `TestClient` and `dependency_overrides` centrally in `conftest.py`.
- **Integration Testing:** API tests that mock database and MinIO interactions to ensure reliable validation workflows.
- **End to End Testing:** Utilize scripts like `compose-smoke.sh` and `mock_capture.py` to validate the full pipeline end-to-end locally.
- **Frontend Testing:** Component tests using Vitest and comprehensive linting rules.

## Refactoring Opportunities

Continuously reducing technical debt to improve maintainability:

- **Worker Standardization:** Consolidate error handling and DLQ logic across `worker-asr`, `worker-metrics`, and `worker-cv` into a shared, modular utility package.
- **API Modularization:** Break down large API route files in FastAPI into domain-driven service modules to reduce coupling.
- **CSS Architecture:** Migrate any legacy or inline styling in the Next.js shell to standard Tailwind CSS classes to enhance UI predictability.
- **Test Boilerplate Reduction:** Move localized test overrides and fixture setups into shared `conftest.py` environments to clean up test files.

## Risks & Tradeoffs

Evaluating limitations and making informed technical tradeoffs:

- **Network Resiliency vs. Client Complexity:** Relying on intermittent school network bandwidth requires edge buffering, increasing the complexity of the DAT client but keeping the server architecture simpler.
- **Hardware Constraints vs. Model Accuracy:** Using consumer-grade RTX 5070 GPUs (12GB VRAM) restricts the size of usable models. We trade off massive multi-modal accuracy for chained smaller models (Whisper + YOLO) and LLM quantization (INT4/AWQ).
- **Data Privacy vs. Model Training:** The current G2 blockade prevents gathering real-world student data. We trade off early ML accuracy benchmarking for absolute legal safety by using synthetic data.

## Agile Sprint Plan

- **Sprint 1: Ingestion Pipeline Polish & Metrics Verification**
  - Implement and verify reliable multipart chunk ingestion in FastAPI. Focus on connection drops and resumability.
- **Sprint 2: Async Architecture Resilience**
  - Standardize DLQ across all workers. Deploy shared error handling logic. Validate `worker-asr` memory utilization.
- **Sprint 3: Database & ORM Optimization**
  - Audit PostgreSQL queries for N+1 issues. Apply necessary indexes and refactor data access patterns in the API.
- **Sprint 4: Next.js Dashboard Development**
  - Build out the teacher pedagogy dashboards using React Server Components. Ensure UI responsiveness and Tailwind integration.
- **Sprint 5: End-to-End Testing & CI Enhancement**
  - Achieve the 85% Pytest coverage target. Consolidate `conftest.py` configurations. Finalize the CI verification pipelines.
