# Full Stack Product Architecture Report

## Product & Problem Analysis

PedagogyX is an AI classroom intelligence platform designed to optimize teacher performance by analyzing multimodal inputs. The primary challenge is capturing high-quality audio and video without disrupting the classroom environment, while ensuring strict data privacy and compliance (especially Phase 0 G2 constraints regarding PII). The product targets the Meta Ray-Ban (DAT) smart glasses via Android as the primary capture device, ensuring a seamless, wearable recording solution for teachers. Development is currently limited to docs, benchmarks, the MVP boilerplate stack, and synthetic test sessions because production school data is blocked until G2 legal sign-off.

## Full Stack Architecture

The system employs a Hybrid Edge-Cloud architecture:

- **Client**: Meta Ray-Ban smart glasses (DAT) interfacing with an Android host app.
- **Edge**: A high-throughput ingest buffer (LAN) written in Go to forward data chunks reliably.
- **Cloud API**: A central, OSS-first FastAPI backend managing sessions, chunk ingestion, and queue orchestration running in India for hot/cold path processing.
- **Background Workers**: Asynchronous Python workers (`worker-asr` using faster-whisper, `worker-metrics`, and `worker-cv`) pulling from Redis queues.
- **Web Frontend**: A Next.js 15 / React 19 based web application for visualization and administrative tasks.

## Frontend Strategy

The frontend is built using Next.js 15, React 19, and TailwindCSS 4, focusing on performance, scalability, and an excellent developer experience.

- **UI Architecture**: Component-based using React, taking advantage of modern React 19 features and Next.js App Router.
- **State Management**: Built-in React state features and potentially lightweight context providers.
- **Responsiveness**: Fully responsive UI driven by TailwindCSS.
- **Accessibility**: Standard HTML5 semantic tags and ARIA attributes integrated into reusable components.
- **Optimization Strategy**: Leveraging Next.js Server Components, image optimization, and caching strategies.

## Backend Strategy

The backend relies on an OSS-first FastAPI application tailored for rapid development and high performance.

- **API Architecture**: RESTful API utilizing FastAPI for type-safe, auto-documented endpoints. Includes comprehensive `dat` session routes (`/v1/sessions/...`).
- **Database Workloads**: Relational schema managed by SQLAlchemy or direct async drivers (e.g., asyncpg).
- **Caching**: Redis is utilized heavily as an asynchronous task queue broker and caching layer.
- **Async Systems**: Heavy offloading to background workers (`worker-asr`, `worker-metrics`, `worker-cv`) over Redis to prevent blocking the main API thread.
- **Scalability Strategy**: Stateless API deployment, horizontal scaling of worker nodes, MinIO/S3 for scalable blob storage.

## Database Design

- **Schema**: Tables for `sessions`, `chunks`, `metrics`, and `transcripts`.
- **Indexing**: Optimized indexes on session IDs and timestamps to quickly aggregate classroom analytics.
- **Optimization**: Read-heavy operations are cached or pre-computed via the background workers.
- **Consistency Strategy**: Standard ACID properties on the primary relational store; eventual consistency for async computed metrics.

## Security Strategy

- **Authentication**: Strict validation of API keys and session tokens.
- **Authorization**: Role-based or token-based authorization limiting endpoint access.
- **Validation**: Strict schema validation on every request via Pydantic in FastAPI.
- **Vulnerability Prevention**: Use of updated libraries, parameterized queries to prevent SQL injection, and ensuring no PII leaks into the OSS components. Data compliance limits current development to synthetic test sessions until G2 sign-off.

## DevOps & Deployment

- **CI/CD**: Automated validation scripts (`./scripts/dev-verify.sh`), GitHub Actions for testing and deployment.
- **Hosting**: Docker compose is used for local development (`infra/compose.dev.yaml`), cloud deployment strategy focuses on Kubernetes or managed container services.
- **Observability**: FastAPI health checks, logging in workers, and integration with standard observability stacks (Prometheus/Grafana expected).
- **Rollback Systems**: Container tagging and infrastructure-as-code deployments for rapid rollbacks.

## Testing Strategy

- **Unit Testing**: Vitest for the frontend, pytest with pytest-asyncio for backend APIs and workers.
- **Integration Testing**: Local Docker Compose smoke tests, `dat-session-smoke` using CLI scripts.
- **End to End Testing**: E2E testing to simulate DAT device flows through the entire system.
- **Validation Workflows**: Pre-commit hooks, CI checks for markdown, formatting, and tests.

## Refactoring Opportunities

- **Simplifications**: Centralizing shared models between FastAPI and background workers.
- **Modularization**: Decoupling the frontend into distinct micro-frontends or strict domain-driven directories if complexity grows.
- **Scalability Improvements**: Moving from local Redis/MinIO to managed cloud equivalents for production; adding distributed tracing for the async queues.

## Risks & Tradeoffs

- **Technical Limitations**: Meta Ray-Ban Android proxy introduces latency; Go LAN buffer adds an intermediate failure point.
- **Complexity Tradeoffs**: Managing multiple Python background workers increases operational complexity over a monolith, but is necessary for long-running ML tasks.
- **Scalability Concerns**: Fast transcription (`worker-asr`) requires significant GPU resources which might become a bottleneck under heavy concurrent classroom sessions.

## Agile Sprint Plan

- **Milestone 1**: Complete boilerplate and local docker-compose environment for the API, workers, and Next.js frontend.
- **Milestone 2**: Finalize synthetic data pipelines for local E2E testing to bypass G2 PII constraints.
- **Milestone 3**: Implement resilient task orchestration between API and `worker-asr`/`worker-metrics`.
- **Milestone 4**: Finalize UI dashboards for metric visualization.
- **Expected Outcomes**: A robust MVP stack deployed locally and ready for immediate cloud migration once Phase 0 G2 constraints are lifted.
