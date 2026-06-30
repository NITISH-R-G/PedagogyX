# Full Stack Product Architecture Report

## Product & Problem Analysis

PedagogyX is an AI-driven classroom intelligence platform built to monitor, analyze, and improve teacher performance and student engagement. The core problem is accurately capturing high-fidelity, real-time multimodal data (audio, video, speech patterns) in dynamic classroom environments without disrupting the teaching process. Furthermore, the platform faces the challenge of strictly protecting student privacy (PII) to comply with regional regulations (such as India's G2 legal requirements), which restricts raw data handling and pilot rollouts. The platform must be robust enough to handle the primary client capture device, Meta Ray-Ban (DAT) smart glasses, ensuring a seamless flow of data to processing backend services.

## Full Stack Architecture

PedagogyX utilizes a robust, hybrid Edge-Cloud architecture designed for high availability and low latency.

- **Client Tier**: Meta Ray-Ban smart glasses interface with an Android host app (clients/android-capture-dat) for real-time capturing of audio and video.
- **Edge Ingest Tier**: An edge ingest buffer acts as a high-throughput lane ensuring reliable, chunked data forwarding even over spotty network connections.
- **Cloud Backend Tier**: Built around an OSS-first centralized inference backend, the system separates workloads into a real-time Hot Path (e.g., YOLO) and an asynchronous Cold Path (e.g., faster-whisper via Ollama).
- **Microservices**: Orchestrated via Docker Compose (and eventually Kubernetes), core services include `api`, `web`, `worker-asr`, `worker-cv`, and `worker-metrics`.
- **Frontend Dashboard**: A comprehensive administrative dashboard built with Next.js and React provides actionable insights and metric visualization for educators and school administrators.

## Frontend Strategy

The frontend strategy prioritizes a highly responsive, accessible, and insightful user experience, tailored for school administrators.

- **Architecture**: A Next.js (App Router) based dashboard heavily leveraging React Server Components to reduce client-side JS bundles, accelerating initial page loads.
- **UI & UX**: Built with Tailwind CSS for utility-first responsive styling and Radix UI primitives to ensure high accessibility and consistency.
- **State Management**: Utilizing lightweight React Context or Zustand for client-side interactions, while leaning on server-side rendering for data-heavy metric displays.
- **Performance**: Edge-cached static assets and debounced Server-Sent Events (SSE) or optimized polling for the Hot Path metrics to ensure a seamless real-time viewing experience without overwhelming the browser.

## Backend Strategy

The backend is meticulously designed for extreme scalability, fault tolerance, and developer productivity.

- **Framework**: FastAPI powers the RESTful and WebSocket API endpoints, offering strong type safety via Pydantic and massive async throughput capabilities.
- **Asynchronous Processing**: Background workers (Python-based) handle heavy AI inferences (like ASR via faster-whisper) decoupled from the main API by pulling jobs from Redis queues.
- **Architecture Flow**: A clear separation between the API layer for client interaction and the Worker layer for deep AI analytics. The architecture employs Dead Letter Queues (DLQ) for gracefully handling processing failures.
- **Reliability**: Services are stateless where possible, allowing horizontal scaling based on queue depth and processing latency.

## Database Design

The database architecture emphasizes data integrity, fast querying for metrics, and secure handling of multimedia assets.

- **Relational Storage**: PostgreSQL is the primary store for structured data (e.g., user metadata, session details, and processed pedagogical metrics).
- **Object Storage**: MinIO or a comparable S3-compatible blob storage securely handles raw unstructured media chunks.
- **Query Optimization**: Advanced indexing strategies on session identifiers and timestamps to prevent N+1 queries during complex timeline reconstructions.
- **Connection Management**: Shared connection pooling via SQLAlchemy/asyncpg ensures optimal database connection usage and reduces overhead during high concurrency.

## Security Strategy

Security and privacy are foundational given the educational context of the product.

- **Authentication & Authorization**: Implementation of robust OAuth 2.0 and JWT-based bearer token mechanisms (`HTTPBearer` in FastAPI) with granular role-based access control (RBAC).
- **Data Privacy**: Absolute adherence to G2 legal constraints meaning no PII is permanently stored or processed without anonymization. AI inference happens locally or on strictly managed instances.
- **Network Security**: Enforced TLS/HTTPS everywhere, strict CORS policies, and rate-limiting at the API gateway layer.
- **Secrets Management**: Configuration via `.env` files (excluded from version control) and Pydantic settings configured securely to prevent leaks.

## DevOps & Deployment

The deployment pipeline guarantees operational simplicity, safety, and rapid iteration.

- **Infrastructure Automation**: Infrastructure as Code (IaC) principles guide deployment. Local and pilot testing relies heavily on Docker Compose (`infra/compose.dev.yaml`).
- **CI/CD Workflows**: GitHub Actions orchestrates linting (`ruff`, `markdownlint`, `prettier`), unit testing (`pytest`, `vitest`), and build artifact generation for zero-downtime deployments.
- **Observability Stack**: Comprehensive logging, metric extraction, and tracing. Worker errors propagate tracebacks to standard output and are captured in centralized aggregation tools for rapid incident response.
- **Deployment Safety**: Immutable container images ensure that what is tested in staging is exactly what is deployed to production.

## Testing Strategy

An extensive testing regime guarantees system stability and high-quality software releases.

- **Backend**: Thorough API and background worker testing using `pytest` and `pytest-mock`. Complete end-to-end simulations using synthetic data generators (`tools/mock-capture`) allow full pipeline validation without requiring physical Meta Ray-Ban hardware.
- **Frontend**: Unit testing via Vitest and React Testing Library for components. Visual regression and end-to-end flow testing via Playwright.
- **CI Enforcement**: All tests, linting, and formatting checks must pass prior to merging. Pre-commit hooks and the `./scripts/dev-verify.sh` pipeline enforce standard adherence locally.

## Refactoring Opportunities

Continuous improvement to simplify and modularize the codebase for long-term sustainability.

- **Backend Modularization**: Decoupling massive monolithic route handlers in FastAPI into dedicated, reusable service layer functions.
- **Frontend Componentization**: Standardizing React components further to remove any inline styling, enforcing a strict Tailwind CSS utility class methodology.
- **Database Access**: Streamlining database context managers to ensure consistent, efficient sharing of active cursors across multiple complex queries.

## Risks & Tradeoffs

Pragmatic evaluation of architectural choices and their inherent risks.

- **Hardware Dependency**: The heavy reliance on Meta Ray-Ban (DAT) limits the initial rollout scope. Generalizing the ingest buffer for IP cameras adds complexity but is a necessary future tradeoff.
- **Processing Latency vs. Accuracy**: Heavy multimodal AI models on the Cold Path yield high accuracy but introduce latency, delaying final authoritative metrics. Visual differentiation in the UI between Hot Path estimates and Cold Path final data mitigates this UX risk.
- **Regulatory Blocking**: The hard stop on production school data pending India G2 sign-off means system scalability must largely be validated via synthetic benchmarks rather than real-world organic traffic.

## Agile Sprint Plan

A structured execution plan targeting high-impact incremental improvements.

- **Sprint 1: Solidify MVP End-to-End Flow**
  - Integrate `tools/mock-capture` with the `api` and `worker-asr` services to ensure stable, automated chunk ingestion and processing.
- **Sprint 2: Real-time UI Improvements**
  - Enhance the Next.js admin dashboard to visualize simulated Hot Path data using SSE, focusing on rendering performance and bento-box responsiveness.
- **Sprint 3: CI/CD & Testing Hardening**
  - Expand the `pytest` test suites and Playwright front-end evaluations. Finalize the CI verification pipelines ensuring production readiness for phase 1 pilot.
- **Sprint 4: Security & Privacy Auditing**
  - Implement strict data anonymization routines and comprehensive access controls, preparing the platform for eventual G2 legal compliance clearance.
