# Full Stack Architecture Report

**Status:** Draft v1.0
**Owner:** PedagogyX System Design Architect

## Product & Problem Analysis

**Problem Statement:**
PedagogyX requires an elite, highly scalable, and privacy-preserving platform for multimodal AI classroom intelligence. The system must seamlessly ingest video/audio data from thin edge clients (primarily Meta Ray-Ban smart glasses) and process it centrally in an OSS-first inference backend to generate pedagogical scores and insights for teachers.

**Requirements & Constraints:**

- End-to-end operation from edge capture to admin dashboards.
- Hybrid Edge-Cloud (D-PROC Hybrid) architecture bridging disconnected/intermittent school environments with India-based cloud inference.
- Production scale processing of heavy multimodal data (video, audio).
- Strict adherence to India DPDP compliance (data residency and privacy).
- First-class developer experience, testing rigor, and operational observability.

**User Workflows:**

1. Teacher starts session via Android host app connected to Ray-Ban glasses.
2. Intermittent chunks of encrypted A/V data are transmitted over school LAN to an edge buffer, then forwarded over WAN to the PedagogyX Cloud API.
3. Cold-path inference workers securely transcribe and analyze the media asynchronously.
4. Administrators and teachers view aggregated metrics and coaching insights via a high-performance Next.js web application.

## Full Stack Architecture

The PedagogyX platform is a distributed, multi-tiered architecture that strictly separates edge ingestion, API brokering, ML inference, and user presentation.

**1. Edge/Client Tier:**

- Meta Ray-Ban Smart Glasses capturing POV and microphone.
- Android DAT Host App acting as the immediate relay and edge buffer.
- District Edge Node functioning as a LAN ingest buffer and forwarder.

**2. API & Gateway Tier:**

- Horizontally scalable FastAPI application acting as the primary ingestion endpoint and REST API for the Next.js frontend.
- Secure, stateless HTTP endpoints that handle chunked uploads, directing them efficiently to MinIO.

**3. State & Queue Tier:**

- Redis for asynchronous job queuing and Dead Letter Queue (DLQ) implementations.
- PostgreSQL as the primary relational store for metadata, RBAC, and ML inference results.
- MinIO for high-throughput S3-compatible object storage of raw streams and transcripts.

**4. Inference Tier:**

- Distributed Python worker fleet utilizing Celery/Redis for task dequeueing.
- Distinct specialized pools (Worker-ASR, Worker-CV, Worker-Metrics) to prevent GPU fragmentation and maximize throughput on RTX 5070 clusters.

## Frontend Strategy

**UI Architecture:**
The primary admin and teacher interface is built with Next.js App Router for optimal Server-Side Rendering (SSR) and SEO/performance characteristics.

**State Management & Data Fetching:**

- Server Actions for secure mutations.
- React Server Components (RSC) to reduce client-side bundle size.

**Styling & Design System:**

- Tailwind CSS v4 configured via PostCSS and `@import "tailwindcss";` in global styles.
- Reusable, accessible component library based on Radix UI or equivalent primitives.
- High focus on responsiveness and interaction smoothness, targeting 60fps animations.

**Optimization:**

- Extensive use of Next.js Image optimization and dynamic imports to ensure fast startup times.
- Strict accessibility audits ensuring compliance with WCAG 2.1 AA standards.

## Backend Strategy

**API Architecture:**

- Modern, type-safe REST APIs built with FastAPI and Pydantic.
- Threadpool-backed synchronous database interactions (`psycopg2`) properly decoupled from the async event loop to prevent blocking.

**Asynchronous Workflows:**

- Decoupled ML execution using a Redis-backed queue system.
- Dead Letter Queue (DLQ) pattern strictly enforced for all worker nodes. Tracebacks and raw payloads are logged and saved for human debugging.

**Scalability Strategy:**

- Stateless FastAPI nodes scalable via Kubernetes HPA.
- Dedicated worker node scaling based on Redis queue depths and target SLAs (e.g., draining peak traffic within 4 hours).

## Database Design

**Schema Architecture:**

- Fully normalized PostgreSQL schema modeling Schools, Users, Sessions, Chunks, and Analytics.
- Strategic denormalization for heavy read queries (e.g., rolling up metrics into aggregate tables).

**Optimization & Consistency:**

- Strict Foreign Key constraints for referential integrity.
- Indexing strategies heavily focused on session retrieval, tenant isolation (school_id), and timestamp ranges.
- Helper methods for DB interactions explicitly pass existing cursors (e.g., `RealDictCursor`) to prevent N+1 connection overhead.

**Storage Layer:**

- MinIO strictly separates binary blobs from metadata, ensuring the PostgreSQL database remains lightweight and highly performant.

## Security Strategy

**Authentication & Authorization:**

- Current MVP leverages `HTTPBearer` with strict API key validation mapped via Pydantic settings.
- Future state migrates to short-lived JWTs and comprehensive Role-Based Access Control (RBAC) ensuring tenant isolation (e.g., School Admin vs. Teacher views).

**Validation & Defaults:**

- All inputs are strictly validated at the boundary via Pydantic.
- Environmental secrets are never defaulted to strings. All `BaseSettings` secrets default to `None` to ensure safe failure if misconfigured.

**Data Protection:**

- TLS 1.3 enforced for all transit.
- DPDP-compliant data residency confined to India cloud regions.

## DevOps & Deployment

**CI/CD Pipeline:**

- Comprehensive GitHub Actions workflows (`.github/workflows/test.yml`) automating backend (`pytest`), workers, and frontend (`vitest`) testing on push/PRs.
- Strict linting enforcement (`dev-verify.sh`) for markdown and Python.

**Infrastructure as Code:**

- Docker Compose for a pristine, reproducible local development environment (`infra/compose.dev.yaml`), explicitly defining variables like `API_KEY`.
- Production targets Kubernetes, orchestrating FastAPI, Redis, MinIO, and GPU-enabled worker nodes.

**Observability:**

- Prometheus for metrics gathering across API endpoints and queue depths.
- Centralized structured logging for all Python services with absolute bans on silent exceptions (`except Exception: pass`). All errors must print to `sys.stderr`.

## Testing Strategy

**Backend Validation:**

- Exhaustive Pytest suites isolating database connections using `unittest.mock.patch`.
- Explicit testing of rollback and exception paths for context managers.
- Execution contexts strictly managed by setting required environment dummy variables (e.g., `API_KEY="dev_api_key_placeholder"`) during tests.

**Frontend & End-to-End:**

- Vitest for unit testing Next.js components.
- Playwright integration for automated visual verification and End-to-End user flow validation.

**Worker Testing:**

- Mocking of discrete synchronous pipeline steps (fetching, downloading, transcribing, saving) to test orchestration logic in isolation.

## Refactoring Opportunities

**Current Debt & Simplifications:**

- Unify database connection logic and context manager utilization across legacy scripts to match the optimized `get_conn()` and cursor-passing pattern.
- Consolidate error handling and logging formatting across worker nodes to a centralized standard library module.
- Modularize the Next.js frontend to abstract common data-fetching patterns into distinct service hooks.

## Risks & Tradeoffs

**Architecture Limitations:**

- **Network Dependency:** The edge-to-cloud upload path relies on school connectivity, necessitating complex local chunk buffering on Android hosts.
- **Queue Backpressure:** High peak ingestion could outpace RTX 5070 worker throughput, leading to increased latency in insight delivery to administrators.

**Complexity Tradeoffs:**

- Maintaining separate environments for local GPUless testing (stub workers) vs. actual faster-whisper inference introduces configuration complexity.
- Building custom edge buffering in Android increases the client surface area compared to a simple WebRTC stream, but is essential for intermittent connections.

## Agile Sprint Plan

### Sprint 1: Architecture Formalization & Core Stubs

- Finalize this architecture report and integrate with broader Phase 0 documentation.
- Standardize Pydantic settings and security defaults across the repository.

### Sprint 2: Robust Ingestion & DLQ

- Enhance the FastAPI ingest pipeline to handle unstable chunk streams.
- Implement strictly conforming Dead Letter Queues across `worker-asr` and `worker-metrics`.

### Sprint 3: Database & Auth Scaling

- Refactor database helpers to eliminate N+1 connection overhead.
- Transition from static API keys to a flexible RBAC model for the Next.js frontend.

### Sprint 4: Frontend V1 & Playwright E2E

- Build the initial Tailwind v4 admin dashboards.
- Automate screenshot verification and visual regression testing using Playwright.
