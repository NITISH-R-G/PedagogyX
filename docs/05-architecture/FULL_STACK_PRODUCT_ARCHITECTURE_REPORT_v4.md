# Full Stack Product Architecture Report v4

## Product & Problem Analysis

PedagogyX is an AI classroom intelligence platform that empowers teachers with insights by analyzing multimodal inputs. The core challenge is capturing high-quality audio and video seamlessly within a classroom setting without causing distraction, while adhering to strict data privacy and compliance guidelines (e.g., G2 constraints regarding PII). The current product strategy utilizes Meta Ray-Ban smart glasses (DAT) as the primary edge capture device, facilitating an unobtrusive recording experience.

## Full Stack Architecture

The architecture follows a Hybrid Edge-Cloud pattern.

### Client

Meta Ray-Ban smart glasses (DAT) connected to an Android companion application.

### Edge Ingestion

A robust, high-throughput ingest buffer built in Go, designed for reliable chunk transmission over local networks.

### Cloud Backend

A central, OSS-first FastAPI service orchestrating session management, media ingestion, and message queue publishing.

### Background Processing

Asynchronous Python workers (such as `worker-asr` powered by faster-whisper) handle heavy computational tasks by consuming from Redis.

### Web Interface

A Next.js-based admin dashboard delivering near real-time insights and classroom metrics.

## Frontend Strategy

The web interface focuses on speed, accessibility, and high developer velocity.

### UI Architecture

Built with Next.js 15 and styled using Tailwind CSS v4. Component composition prioritizes modularity and reusability.

### State Management

Utilizes React's native state management (hooks and context) combined with efficient data fetching strategies for metric updates.

### Responsiveness & Accessibility

Interfaces are fully responsive across devices and strictly adhere to WCAG standards, ensuring inclusive administrative workflows.

## Backend Strategy

The API layer is built for maintainability, reliability, and asynchronous scale.

### API Architecture

FastAPI provides strongly typed, asynchronous REST endpoints, well-suited for streaming media uploads and chunk management.

### Async Workflows

Intensive processing like Automatic Speech Recognition (ASR) is decoupled from the main thread via Redis queues, with workers implementing robust Dead Letter Queue (DLQ) patterns for failure recovery.

### Scalability Strategy

Services are containerized via Docker. API nodes and background worker nodes can scale horizontally independently based on payload load and processing demands.

## Database Design

The data layer prioritizes integrity, efficient querying, and scalable blob storage.

### Schema and Storage

PostgreSQL serves as the primary relational store for sessions, user data, and metadata. MinIO manages unstructured media blobs (audio/video chunks) securely.

### Optimization

Database schema employs strategic indexing for rapid session lookup. Query execution shares single database cursors to prevent N+1 connection overhead and optimize connection pooling.

## Security Strategy

Given the educational context, strict security protocols are enforced.

### Authentication & Authorization

Endpoints are secured with Bearer tokens (`HTTPBearer`) requiring valid API keys for access control.

### Data Privacy

Adheres to zero PII processing until formal G2 legal sign-off. Test environments use exclusively synthetic data.

### Secrets Management

Pydantic settings manage configuration with safe defaults (e.g., `None` for secrets), and `.gitignore` prevents accidental exposure of `.env` files.

## DevOps & Deployment

Deployment pipelines prioritize operational simplicity, reproducibility, and safety.

### CI/CD

GitHub Actions drive automated linting, testing, and formatting for all components (web, API, workers, and docs).

### Local Infrastructure

Docker Compose orchestrates local development and pilot deployments seamlessly.

### Observability

Workers push stack traces to `sys.stderr` for log aggregation, and DLQ mechanisms provide visibility into processing failures.

## Testing Strategy

A multi-layered testing approach guarantees application stability.

### Backend Validation

Uses `pytest` combined with `pytest-mock` to evaluate endpoints and worker logic. Tests mock Pydantic environments properly to validate configurations.

### Frontend Validation

Vitest handles unit testing for Next.js components and utility functions, while Playwright performs visual regression and frontend e2e testing.

### End to End Integration

Synthetic data simulators (e.g., `tools/mock-capture`) allow full pipeline validation from ingestion to metric output without physical hardware requirements.

## Refactoring Opportunities

Continuous improvement is embedded into the engineering cycle.

### Modularity

Ongoing efforts to extract business logic and validation routines from FastAPI route handlers into dedicated service layers.

### Connection Management

Standardization of database context managers to ensure consistent, efficient sharing of cursors across transactions.

### Resilience

Enhancing background workers with automatic, exponential backoff retries and better unified telemetry tracing.

## Risks & Tradeoffs

Key architectural considerations requiring ongoing monitoring.

### Hardware Dependencies

Strong reliance on Meta Ray-Ban devices may necessitate a generalized ingest protocol later to support diverse IP cameras if supply constraints emerge.

### Asynchronous Latency

Decoupled media processing inherently introduces a delay between capture and dashboard availability; optimizing worker throughput is essential to mitigate this.

### Regulatory Barriers

Strict PII regulations block the usage of real-world testing data, which may obscure edge cases until final G2 authorization.

## Agile Sprint Plan

Structured, iterative development goals.

### Sprint 03

Deliver the foundational vertical slice: operational mock capture, robust chunk upload endpoints, basic ASR worker integration, and MVP Next.js admin interface. Ensure Docker Compose stability.

### Sprint 04

Enhance metric extraction algorithms, improve data visualization in the Next.js frontend, and expand CI/CD coverage with mocked PostgreSQL interactions.

### Sprint 05

Transition authentication from static API keys to scoped OAuth flows, optimize worker concurrency capabilities, and finalize frontend accessibility audits.
