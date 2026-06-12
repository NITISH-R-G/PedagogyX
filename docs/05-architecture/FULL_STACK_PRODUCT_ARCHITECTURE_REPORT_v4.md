# Full Stack Product Architecture Report

## Product & Problem Analysis

PedagogyX is an AI classroom intelligence platform designed to optimize teacher performance by analyzing multimodal inputs. The primary challenge is capturing high-quality audio and video without disrupting the classroom environment, while ensuring strict data privacy and compliance (especially Phase 0 G2 constraints regarding PII). The initial product targets the Meta Ray-Ban (DAT) smart glasses as the primary capture device, ensuring a seamless, wearable recording solution for teachers.

## Full Stack Architecture

The system employs a Hybrid Edge-Cloud architecture.

### Client

Meta Ray-Ban smart glasses (DAT) interfacing with an Android host app.

### Edge

A high-throughput ingest buffer (LAN) written in Go to forward data chunks reliably.

### Cloud API

A central, OSS-first Fast API backend managing sessions, chunk ingestion, and queue orchestration.

### Background Workers

Asynchronous Python workers (e.g., `worker-asr` using faster-whisper, and `worker-metrics`) pulling from Redis queues.

### Web Shell

A Next.js-based admin dashboard to visualize metrics like talk ratios.

## Frontend Strategy

The frontend is built as a Next.js admin shell optimized for performance, accessibility, and visual consistency.

### UI Architecture

Modular component design using Tailwind CSS v4 for utility-first styling. Configured with `@tailwindcss/postcss` and `@import "tailwindcss";` in `app/globals.css`.

### State Management

Leveraging React's built-in hooks and context, paired with robust data fetching for real-time metric updates.

### Accessibility & UX

Adhering to WCAG guidelines, ensuring responsive layouts for various administrative devices.

## Backend Strategy

The backend is optimized for maintainability, reliability, and asynchronous processing.

### API Architecture

FastAPI provides robust, typed REST endpoints with asynchronous support, ideal for handling chunked media uploads.

### Async Workflows

Heavy lifting (ASR, metric extraction) is decoupled from the API via Redis queues, ensuring low-latency ingest. Workers implement Dead Letter Queue (DLQ) patterns.

### Scalability Strategy

The system is containerized, enabling independent scaling of the API web servers and the background worker nodes based on payload volume.

## Database Design

The persistence layer ensures data integrity and scalability.

### Schema and Storage

PostgreSQL stores structured data (sessions, user metadata, processing status). MinIO handles unstructured media chunks securely.

### Query Optimization

Indexed session identifiers ensure rapid lookup for chunk association. Database connection management passes existing cursors to helper methods to avoid N+1 connection overhead.

## Security Strategy

Security is paramount given the sensitive nature of classroom recordings.

### Authentication and Authorization

API endpoints require a Bearer token (`HTTPBearer`), strictly validating access via API keys.

### Data Protection

No PII or production data is processed until legal (G2) sign-off.

### Environment Configuration

Secret variables in Pydantic settings are defaulted to `None` to prevent hardcoded leaks, and `.gitignore` enforces exclusion of local test `.env` files.

## DevOps & Deployment

The deployment strategy focuses on operational simplicity and reliability.

### CI/CD Pipeline

GitHub Actions automate linting and tests across web, API, and worker services. Docker Compose drives local and pilot deployments.

### Observability

Worker nodes implement Dead Letter Queues (DLQ) for failed jobs and push error tracebacks to `sys.stderr` for log aggregation.

## Testing Strategy

A comprehensive testing strategy guarantees reliable updates.

### Backend Validation

Uses `pytest` with `pytest-mock` to test APIs and workers. Required environment variables are injected into tests to satisfy Pydantic validations.

### Frontend Validation

Next.js UI elements and logic are evaluated via Vitest. Frontend changes are visually verified using Playwright.

### End to End Validation

Synthetic session simulators (`tools/mock-capture`) validate the complete ingest-to-metrics pipeline without needing physical hardware.

## Refactoring Opportunities

Current areas for improvement focus on maintainability and performance.

### Modularity

Migrating shared validation and processing logic from monolithic routes to dedicated service functions in FastAPI.

### Connection Management

Standardizing database connection contexts to share single cursors across related queries consistently.

### Error Handling

Enhancing DLQ patterns to include automatic retry mechanisms and unified telemetry context propagation.

## Risks & Tradeoffs

Key architectural and product considerations.

### Hardware Constraints

The primary capture relies heavily on Meta Ray-Ban devices. Future scalability may require generalizing the ingest buffer to support standard IP cameras.

### Latency vs Accuracy

Processing high-fidelity multimodal data asynchronously introduces a slight delay in metric availability on the frontend.

### Regulatory Friction

PII regulations require strict gating mechanisms, delaying real-world testing until complete legal authorization.

## Agile Sprint Plan

Structured iteration planning.

### Sprint 03

Establish the full vertical slice (mock capture, upload, ASR worker, basic admin web view). Ensure Docker compose functionality and robust chunk ingestion.

### Sprint 04

Focus on robust metrics calculation, improving Next.js frontend visualization, and implementing comprehensive CI testing on mocked database interactions.

### Sprint 05

Hardening security configurations (moving from API keys to granular OAuth scopes) and optimizing worker concurrency models.
