# Full Stack Product Architecture Report

## Product & Problem Analysis

PedagogyX is an AI classroom intelligence platform designed to optimize teacher performance by analyzing multimodal inputs. The primary challenge is capturing high-quality audio and video without disrupting the classroom environment, while ensuring strict data privacy and compliance (especially Phase 0 G2 constraints regarding PII). The initial product targets the Meta Ray-Ban (DAT) smart glasses as the primary capture device, ensuring a seamless, wearable recording solution for teachers. We need a system capable of managing these sessions, securely storing media chunks, processing them with advanced ASR and CV models, and rendering insights on an intuitive dashboard.

## Full Stack Architecture

The system employs a Hybrid Edge-Cloud architecture to balance local capture constraints with scalable cloud processing.

- **Client**: Meta Ray-Ban smart glasses (DAT) interfacing with an Android host app.
- **Edge**: A high-throughput ingest buffer (LAN) written in Go to forward data chunks reliably.
- **Cloud API**: A central, OSS-first Fast API backend managing sessions, chunk ingestion, and queue orchestration.
- **Background Workers**: Asynchronous Python workers (`worker-asr` using faster-whisper, `worker-cv`, `worker-metrics`) pulling from Redis queues.
- **Web Shell**: A Next.js-based admin dashboard to visualize metrics like talk ratios.

## Frontend Strategy

The frontend is built as a Next.js admin shell optimized for performance, accessibility, and visual consistency, treating the user experience as paramount.

- **UI Architecture**: Modular component design using Tailwind CSS v4 for utility-first styling. Configured with `@tailwindcss/postcss` and `@import "tailwindcss";`.
- **State Management**: Leverages React's built-in hooks and Context API, paired with robust data fetching (React Query or similar) for real-time metric updates.
- **Responsiveness**: Ensures layouts automatically adapt from desktop administration panels to mobile-friendly summary views.
- **Accessibility & UX**: Adheres strictly to WCAG guidelines, maintaining high contrast ratios, keyboard navigability, and ARIA labels.
- **Optimization Strategy**: Aggressive code splitting, optimized image loading, and server-side rendering (SSR) for initial data population to improve Core Web Vitals.

## Backend Strategy

The backend is a robust API foundation designed for maintainability, reliability, and asynchronous heavy processing.

- **API Architecture**: FastAPI provides typed REST endpoints with asynchronous capabilities, perfect for handling large chunked media uploads.
- **Async Workflows**: Heavy lifting (ASR, CV processing, metric extraction) is completely decoupled from the main API thread via Redis queues.
- **Database Workflows**: Uses SQLAlchemy as an ORM with optimized connection pooling.
- **Caching**: Employs Redis for caching frequent configurations and session metadata to reduce database load.
- **Scalability Strategy**: The system is fully containerized. We scale the stateless API web servers horizontally based on request throughput and worker nodes based on queue depth.

## Database Design

The database layer uses PostgreSQL for relational data and MinIO for object storage, structured to prevent bottlenecks.

- **Schema**: Highly normalized schema storing structured data (sessions, user metadata, chunks processing status, and final metrics).
- **Indexing**: Extensive use of composite indices on session identifiers and timestamp fields to ensure rapid lookup for chunk association.
- **Optimization**: Active prevention of N+1 queries through eager loading strategies and database connection management passing existing cursors to helper methods.
- **Consistency Strategy**: Enforced via ACID-compliant PostgreSQL transactions for critical operations, while adopting eventual consistency for metric updates processed by workers.

## Security Strategy

Security is embedded at every layer due to the sensitive nature of classroom recordings.

- **Authentication**: API endpoints require a Bearer token (`HTTPBearer`), strictly validating access via API keys.
- **Authorization**: Role-based access control (RBAC) restricts endpoints based on user scopes (e.g., admin vs. teacher).
- **Validation**: Strict Pydantic models validate all incoming client payloads, preventing injection attacks.
- **Vulnerability Prevention**: No PII or production data is processed until legal (G2) sign-off. Secret variables in Pydantic settings are defaulted to `None` to prevent hardcoded leaks, and `.gitignore` enforces exclusion of local test `.env` files.

## DevOps & Deployment

The deployment strategy focuses on operational simplicity, reliability, and continuous delivery.

- **CI/CD**: GitHub Actions automate linting, formatting, unit tests, and frontend integration tests across web, API, and worker services.
- **Hosting**: Docker Compose drives local and pilot deployments, with plans for Kubernetes orchestration in production for advanced scaling.
- **Observability**: Worker nodes implement Dead Letter Queues (DLQ) for failed jobs, push error tracebacks to `sys.stderr` for log aggregation, and integrate telemetry context propagation.
- **Rollback Systems**: Blue-green deployments and automated database migration rollbacks ensure zero downtime and safety during releases.

## Testing Strategy

A comprehensive testing strategy guarantees reliable updates across the full stack.

- **Unit Testing**: Pytest for backend functions and Vitest for frontend components.
- **Integration Testing**: Pytest with `pytest-mock` and overridden dependencies to test APIs and workers.
- **End to End Testing**: Synthetic session simulators (`tools/mock-capture`) validate the complete ingest-to-metrics pipeline without needing physical hardware. Next.js UI elements and logic are verified using Playwright.
- **Validation Workflows**: Pre-commit hooks enforce formatting and linting, ensuring only high-quality code enters the CI pipeline.

## Refactoring Opportunities

Continuous improvement to simplify and modularize the architecture.

- **Simplifications**: Migrating shared validation and processing logic from monolithic routes to dedicated, testable service functions in FastAPI.
- **Modularization**: Creating shared internal packages for domain models and common queue clients to prevent duplication between API and workers.
- **Scalability Improvements**: Enhancing DLQ patterns to include automatic retry mechanisms with exponential backoff and unified telemetry.

## Risks & Tradeoffs

Key architectural decisions and their inherent tradeoffs.

- **Technical Limitations**: The primary capture relies heavily on Meta Ray-Ban devices. Future scalability may require generalizing the ingest buffer to support standard IP cameras, complicating the edge deployment.
- **Complexity Tradeoffs**: Decoupling processing via Redis queues adds operational complexity compared to a monolithic approach but is mandatory for handling slow AI inference.
- **Scalability Concerns**: Managing massive unstructured media volumes in MinIO requires careful lifecycle policies to control storage costs.
- **Regulatory Friction**: PII regulations require strict gating mechanisms, delaying real-world testing until complete legal authorization.

## Agile Sprint Plan

Structured iteration planning for continuous value delivery.

- **Sprint 03**: Establish the full vertical slice (mock capture, upload, ASR worker, basic admin web view). Ensure Docker compose functionality and robust chunk ingestion.
- **Sprint 04**: Focus on robust metrics calculation, improving Next.js frontend visualization, and implementing comprehensive CI testing on mocked database interactions.
- **Sprint 05**: Harden security configurations (moving from API keys to granular OAuth scopes), implement the Dead Letter Queue automatic retries, and optimize worker concurrency models.
- **Sprint 06**: End-to-end integration with actual Meta Ray-Ban hardware (DAT) and real-world latency optimization.
