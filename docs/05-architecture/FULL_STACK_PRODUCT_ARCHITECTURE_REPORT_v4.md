# FULL STACK PRODUCT ARCHITECTURE REPORT V4

## Product & Problem Analysis

PedagogyX is pioneering a Hybrid Edge-Cloud product using Meta Ray-Ban smart glasses via Android for data capture, Go-based LAN edge buffers for initial ingestion, and an OSS-first AI backend physically located in India for processing in hot and cold paths.

**Problem Spaces Addressed:**

- **Capture Latency:** Real-time ingestion using edge buffers ensures audio and telemetry from the Meta glasses are staged efficiently without dropping chunks.
- **Privacy & Security:** As production school data requires stringent G2 legal sign-off, the MVP handles mock/synthetic testing cleanly in the cloud path, enforcing structural compliance controls early in the application architecture.

**Target Outcomes:** Robust Edge-Cloud scaling, uncompromising reliability, sub-second latency targets for critical hot paths, and simple but powerful developer experience.

## Full Stack Architecture

The PedagogyX architecture integrates multiple specialized tiers designed to interact smoothly with high predictability:

- **Client Tier:** Meta Ray-Ban Android client applications connecting via DAT interfaces to local networks.
- **Edge Buffer Tier:** High-throughput Go services designed for zero data loss running locally to handle immediate ingest before batch syncing.
- **Cloud Gateway Tier:** FastAPI endpoints (`services/api`) serving as resilient ingress with thorough validation and authentication schemas.
- **Worker Tiers:** Distributed processing queues (e.g., `worker-metrics`, `worker-asr`) handling decoupled AI transformations with OSS models (hot/cold separation).
- **Frontend App Tier:** React/Next.js UI interfaces (`services/web`) providing analytics and operational insights to users with high performance bounds.

## Frontend Strategy

The frontend platform acts as the core administrative and analytics surface, strictly separated from raw streaming inputs.

- **Tech Stack:** Next.js utilizing React 19 server/client components for optimal loading patterns, backed by TailwindCSS for consistent design language.
- **Optimizations:** Data is fetched intelligently using caching libraries combined with optimistic UI updates. Render-blocking operations are offloaded from the main thread, emphasizing accessibility (WCAG) and smooth interaction dynamics.
- **Deployment:** Vercel or equivalent static edge serving, separating presentation scaling constraints from API limitations.

## Backend Strategy

A microservices oriented, OSS-first Python implementation scales core business logic dynamically.

- **Framework:** FastAPI chosen for async readiness, built-in validation mechanisms, and structured documentation rendering.
- **Distribution:** Workloads are split conceptually into synchronous low-latency requests (API) and asynchronous high-throughput processing (Workers).
- **Architectural Principles:** SOLID code architecture across modules, strict boundary definitions between the REST layer, domain logic, and infrastructure adapters.

## Database Design

State resilience and transactional stability govern data structure decisions.

- **Primary Relational Store:** PostgreSQL managing persistent entity states (users, sessions, configurations) requiring ACID properties.
- **In-Memory Store:** Redis for ephemeral state coordination, background task queuing (Celery/RQ), and high-velocity request caching.
- **Object Storage:** S3/MinIO handling blob structures (audio chunks, large metrics files) keeping DB sizing clean and performant.

## Security Strategy

Comprehensive Defense in Depth tailored for sensitive environment operations:

- **Identity:** OIDC/JWT based token lifecycles with strict audience controls and minimal privilege scopes.
- **Encryption:** TLS 1.3 mandated on all transit paths. At-rest encryption utilized for object stores and primary databases.
- **Validation:** Input sanitized using Pydantic across all edge and API boundaries to prevent injection and tampering prior to domain processing.
- **Audit Logging:** System trails emitted for every user interaction, enabling reliable security oversight without degrading critical paths.

## DevOps & Deployment

Automated, predictable, and isolated cloud footprints prioritize stability and developer velocity.

- **Containerization:** All services packaged identically via Docker, with reproducible builds preventing "works on my machine" syndromes.
- **CI/CD Pipelines:** GitHub Actions enforcing type checks, linting, formatting, and tests before merge, supplemented by automated deployment into staging boundaries.
- **Local Development:** Unified via Docker Compose enabling a single command MVP stack instantiation combined with hot-reloading configurations.

## Testing Strategy

Achieving engineering confidence through multi-layered validation:

- **Unit Testing:** `pytest` suite testing core domain logic and data transformations in isolation with mocked dependencies.
- **Integration Testing:** Live local containers (Testcontainers/Compose) verifying API contracts against actual Redis/Postgres/MinIO instances.
- **Frontend Testing:** Vitest and React Testing Library deployed for component rendering scenarios and interactions.
- **Smoke/E2E:** End to end synthetic workflow validation scripts enforcing holistic confidence.

## Refactoring Opportunities

Areas evaluated for proactive modernization:

- **API Boundary Simplification:** Coalescing fragmented FastAPI routes into clearer RESTful resource domains.
- **Type Rigidity:** Enforcing tighter Type Hint definitions and `mypy` strictness across Python boundaries.
- **Error Granularity:** Centralizing `HTTPException` constants via `fastapi.status` standards universally instead of generic error captures.

## Risks & Tradeoffs

- **Edge to Cloud Reliability:** Dropped connection states require complex client side retries handling temporal inconsistency at the Go edge layer.
- **Asynchronous Debugging:** Queue-based worker architecture demands heavier investment in tracing solutions to diagnose latent failure loops effectively.
- **AI Processing Costs:** Self-hosting OSS models versus relying on proprietary SaaS involves continuous benchmarking to balance unit economics and inference latency parameters.

## Agile Sprint Plan

- **Sprint 1 - Foundations:** Establish core API container deployments, Redis task queues, and Postgres connection pools. Implement base mock-capture data pipelines.
- **Sprint 2 - Processing Path:** Bring up worker containers (`worker-asr`, `worker-metrics`). Configure MinIO integration for blob storage paths and test ingestion loops.
- **Sprint 3 - UI/UX Delivery:** Deploy baseline Next.js application, integrating basic authentication. Wire up API calls for session visibility.
- **Sprint 4 - Optimization & Scale:** Implement end-to-end integration testing, refine error handling, enforce caching strategies, and document system operations for the MVP lifecycle.
