# Product Engineering Architecture Report v4

## Product & Problem Analysis

PedagogyX is developing an AI-driven multimodal classroom intelligence platform targeting a primary client base of Meta Ray-Ban smart glasses (DAT) users and low-end Windows smartboards. The platform addresses the need for actionable pedagogical insights in constrained environments, specifically Indian schools characterized by low bandwidth and intermittent connectivity.

The core challenge involves maintaining robust multi-stream ingestion (audio/video), low-latency processing, and high reliability with zero customer budget for infrastructure (D-10 constraint). We operate under strict data sovereignty and privacy constraints per India's DPDP framework, specifically blocking production student data until G2 clearance is achieved. The product relies exclusively on synthetic mock data for Phase 0 testing and MVP validation.

The system must deliver high Product Quality and User Experience while optimizing for Maintainability, Scalability, Reliability, Developer Experience, Performance, Security, Extensibility, and Production Readiness.

## Full Stack Architecture

The architecture represents an end-to-end, production-grade decoupled system optimized for high-throughput ingestion and resource-constrained inference:

- **Client Tier**: Android-based DAT host app for Meta Ray-Ban glasses and low-end Windows smartboards acting as capture agents. Edge nodes (District/School LAN) buffer media seamlessly.
- **API/Ingestion Gateway**: Stateless FastAPI layer handling session management, robust chunk ingestion, and immediate synchronous validation.
- **Event-Driven Backend**: Asynchronous inference pipelines managed via Redis queues (Cold Path) executing parallel tasks across Python worker processes (`worker-asr`, `worker-cv`, `worker-metrics`).
- **Data & Storage Layer**: PostgreSQL for scalable relational data and pedagogical indices. MinIO (S3-compatible) serves as the durable object store for media payloads and processed artifacts.
- **Frontend Presentation Layer**: Next.js (React) Admin Shell visualizing actionable insights with a focus on real-time heuristic feedback (Hot Path) and batch-analyzed evaluation (Cold Path).

## Frontend Strategy

The Next.js presentation layer is engineered to be lightweight, responsive, and resilient for low-bandwidth networks:

- **UI Architecture**: React Server Components (RSC) to minimize client-side JavaScript payloads, improving Initial Load Time and Core Web Vitals.
- **State Management**: Leverage server-driven state where possible, utilizing optimized client hooks only for interactive heuristic overlays.
- **Responsiveness**: Fluid layout strategies implemented via Tailwind CSS v4, supporting dynamic viewport adaptation from desktop administrative dashboards down to mobile supervisor views.
- **Accessibility**: Comprehensive adherence to WCAG 2.1 AA standards, ensuring UI inclusivity for visually impaired administrative staff.
- **Optimization Strategy**: Image optimization, dynamic component hydration, and strict caching headers to decrease rendering latency under bandwidth constraints.

## Backend Strategy

The backend design champions fault tolerance, high concurrency, and stateless scalability to seamlessly bridge edge clients and backend GPU models:

- **API Architecture**: FastAPI provides asynchronous handlers optimized for IO-bound multipart media uploads and validation.
- **Database Workflows**: Highly optimized connection pooling utilizing shared cursors to aggressively eliminate N+1 queries.
- **Async Systems**: A robust event-driven Cold Path architecture (via Celery/Redis) executing isolated AI inferences to prevent thread starvation on the API Gateway.
- **Scalability Strategy**: Independent vertical scaling of API and worker deployments. Specific tuning for Python worker parallelism mapped to RTX 5070 constraints.
- **Performance**: Strict latency monitoring for the Hot Path and throughput optimization for batch Cold Path jobs, adhering to multi-tenant service isolation.

## Database Design

PostgreSQL acts as the authoritative source of truth for the system's structured metadata and multi-tenant isolation:

- **Schema**: Fully normalized schemas strictly isolating tenant data, pedagogical indices, and session telemetry.
- **Indexing**: Optimized B-Tree and Hash indexing strategies applied to time-series query patterns, session lookups, and RBAC evaluations.
- **Optimization**: Strategic denormalization applied to high-read analytics tables to reduce cross-table joins during Next.js dashboard hydration.
- **Consistency Strategy**: Strict ACID compliance using bounded transactions. A Dead Letter Queue (DLQ) state table explicitly tracks asynchronous task failures, avoiding orphaned processing states.

## Security Strategy

A zero-trust model is enforced continuously to uphold G2 compliance mandates and protect against PII leakage:

- **Authentication**: Secure, scoped API key validation protecting Edge-to-Gateway requests. Environment variables rigorously managed (e.g., `API_KEY`) without fallback bypass.
- **Authorization**: Granular RBAC ensuring complete tenant isolation.
- **Validation**: Strict Pydantic models validate all incoming payloads against expected structures, aggressively filtering malformed edge data.
- **Vulnerability Prevention**: Exclusion of all student PII from LLM prompts to enforce anonymized metadata transcription. Robust defense against XSS/CSRF via strict Next.js header controls.

## DevOps & Deployment

The infrastructure pipeline optimizes for reproducible builds and rapid recovery from operational anomalies:

- **CI/CD**: Fully automated GitHub Actions pipeline validating linting (Ruff, ESLint, Markdownlint), formatting (Black, Prettier), and executing rigorous unit test suites with mandatory 85% coverage via Pytest.
- **Hosting**: Containerized deployment orchestratable via Docker Compose (MVP) with scaling pathways designed for future Kubernetes orchestration.
- **Observability**: Centralized, standardized JSON-structured logging from all API and worker boundaries. Comprehensive `/health` probe instrumentation via `dev-verify.sh`.
- **Rollback Systems**: Deterministic container tagging and explicit database migration versioning to guarantee safe rollback capabilities under failure conditions.

## Testing Strategy

Quality assurance enforces high-confidence releases while supporting rapid iterative development:

- **Unit Testing**: Pytest coverage enforced at >=85% across all FastAPI controllers and worker logic. Complex IO dependencies (PostgreSQL, MinIO) strictly mocked to accelerate test velocity.
- **Integration Testing**: Containerized smoke tests (`compose-smoke.sh`) orchestrating realistic end-to-end interactions between the mock capture client and backend storage.
- **End-to-End Testing**: Vitest integration for React components and Playwright testing for critical user workflows in the Next.js shell.
- **Validation Workflows**: Continuous API payload integrity verification and worker execution simulation ensuring stable event ingestion boundaries.

## Refactoring Opportunities

Continuous architectural refinement is necessary to minimize technical debt:

- **Simplifications**: Consolidate redundant error handling and Dead Letter Queue (DLQ) publishing logic across `worker-asr`, `worker-cv`, and `worker-metrics` into a centralized base worker class.
- **Modularization**: Decouple large FastAPI route files into specific, domain-focused modules (e.g., sessions, media, telemetry) to improve code maintainability and test isolation.
- **Scalability Improvements**: Migrate the legacy Next.js inline CSS styles completely to utility-driven Tailwind CSS v4, yielding smaller bundle sizes and unified visual language.

## Risks & Tradeoffs

System architectural decisions involve key compromises optimizing for the current constraints:

- **Hardware Limitations**: Running on consumer-grade GPUs (RTX 5070 with 12GB VRAM) heavily restricts the ability to run concurrent monolithic multimodal LLMs. **Tradeoff**: Implementing unimodal models (faster-whisper large-v3 for Hindi-English ASR, YOLO for CV) with late-stage textual fusion, decreasing total VRAM footprint at the cost of integration complexity.
- **Data Privacy Blockers**: G2 clearance blocks production data access. **Tradeoff**: Relying solely on synthetic data (MDK) delays real-world ML accuracy tuning but entirely removes catastrophic compliance breaches during MVP.
- **Network Resilience**: Expectation of severe packet loss from remote Indian classrooms. **Tradeoff**: Offloading complex chunk buffering and resumability to the Meta Ray-Ban edge clients, significantly increasing edge application complexity to ensure backend purity.

## Agile Sprint Plan

- **Sprint 1: Architecture Core & Storage**
  - Implement base Next.js application shell, deploy PostgreSQL, and stabilize MinIO multipart upload pathways in FastAPI.
- **Sprint 2: Robust Inference Pipeline**
  - Launch `worker-asr` running faster-whisper large-v3, stabilize Celery/Redis message passing, and formalize DLQ recovery logic.
- **Sprint 3: Client Ingestion Reliability**
  - Integrate Meta Ray-Ban `android-capture-dat` client streams, validate edge resumable uploads under simulated packet loss.
- **Sprint 4: Product Dashboard Delivery**
  - Deploy server-rendered pedagogy metrics dashboard in Next.js, displaying both heuristic Hot Path data and batch Cold Path analytics.
- **Sprint 5: System Hardening & Validation**
  - Optimize Python API database access to eliminate N+1 cursors. Attain >= 85% Pytest coverage and execute end-to-end pipeline validation via `./scripts/dev-verify.sh`.
