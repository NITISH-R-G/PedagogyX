# Full Stack Product Architecture Report v4

## Product & Problem Analysis

- **Requirements**: PedagogyX requires a robust, scalable architecture to process, analyze, and present educational or behavioral data captured via edge devices like Meta Ray-Ban smart glasses (DAT client). The system needs real-time capability, seamless edge-to-cloud synchronization, high reliability, and an intuitive frontend interface for reviewing multi-modal data.
- **User Workflows**: Users will capture multimodal data (video, audio) using smart glasses, which is synced to the cloud. They will then use the web interface to review transcripts, view computer vision (CV) analyses, and aggregate metrics.
- **Edge Cases**: Offline device usage with large sync payloads upon reconnection, intermittent connectivity during large video uploads, malformed multi-modal data processing, and handling partial CV or ASR failures.
- **Constraints**: G2 legal sign-off is required for production school data, meaning development operates on synthetic data. System must maintain strict data isolation and privacy boundaries.

## Full Stack Architecture

- **Frontend Structure**: `services/web` utilizing Next.js 15, React 19, Tailwind CSS, and Vite/Vitest for a high-performance SSR and CSR hybrid application.
- **Backend Structure**: `services/api` leveraging FastAPI for asynchronous API endpoints, integrating with `worker-cv`, `worker-metrics`, and `worker-asr` microservices for heavy asynchronous processing tasks.
- **APIs**: RESTful interfaces exposed via FastAPI, strictly typed using Pydantic, enabling robust client-server contracts.
- **Database Architecture**: PostgreSQL for relational state, Redis for fast caching and message brokering to Celery/background workers, and MinIO/S3 for scalable blob storage (video/audio).
- **Infrastructure Layout**: Docker Compose driven local MVP stack (`infra/compose.dev.yml`), intended to scale out via Kubernetes or managed cloud services in production, segregating web traffic from intensive worker pools.

## Frontend Strategy

- **UI Architecture**: Component-driven architecture using React Server Components where applicable for SEO and initial load speed, combined with client components for rich interactive multimodal data viewers.
- **State Management**: Server state management using React Query (or Next.js App Router data fetching) alongside context-based or lightweight local state (e.g., Zustand) for UI interactions.
- **Responsiveness**: Mobile-first design heavily utilizing Tailwind CSS to guarantee seamless experiences across desktop and mobile browsers.
- **Accessibility**: Adherence to WCAG standards using semantic HTML and highly accessible Radix UI or similar headless components to ensure inclusivity.
- **Optimization Strategy**: Aggressive image and asset optimization, route-level code splitting, and memoization of expensive rendering trees for timeline/video data visualization.

## Backend Strategy

- **API Architecture**: FastAPI-driven modular routers separating domain concerns. Use of dependency injection for scalable and testable database/service access.
- **Database Workflows**: Async SQLAlchemy or similar ORM integrated with FastAPI to prevent blocking I/O during heavy concurrency.
- **Caching**: Redis used for caching frequent metadata reads, pre-computation of aggregate metrics, and managing rate limiting or session states.
- **Async Systems**: Offloading CV and ASR tasks to dedicated Python worker containers (`worker-cv`, `worker-asr`) communicating via message queues (Redis/RabbitMQ).
- **Scalability Strategy**: Stateless API tier designed for horizontal autoscaling. Worker queues strictly partitioned to prevent long-running CV tasks from starving fast ASR tasks.

## Database Design

- **Schema**: Normalized schema for core domains (Users, Sessions, Devices). JSONB fields for flexible metadata or variable schema metrics output from CV/ASR models.
- **Indexing**: B-Tree indexes on primary lookups (user_id, session_id), composite indexes for time-series range queries (session_id + timestamp).
- **Optimization**: Read replicas for analytical queries and dashboards to offload pressure from the primary write database processing incoming telemetry.
- **Consistency Strategy**: Strict ACID compliance for user and billing data; eventual consistency acceptable for derived ML insights and processed metrics streams.

## Security Strategy

- **Authentication**: JWT-based stateless authentication or secure HttpOnly cookies for web clients, and mutual TLS or secure API keys for the edge devices (Ray-Ban DAT).
- **Authorization**: Role-Based Access Control (RBAC) enforced via FastAPI dependency layers, ensuring users only access their authorized session data.
- **Validation**: Strict input validation boundary enforced by Pydantic models on every incoming request, stripping unverified payloads immediately.
- **Vulnerability Prevention**: Automated dependency scanning, CSP headers, rate limiting on auth endpoints, SQL injection prevention via parameterized ORM queries, and safe handling of user-uploaded media files (malware scanning before CV processing).

## DevOps & Deployment

- **CI/CD**: GitHub Actions pipelines for automated linting, type-checking, unit testing (Vitest and Pytest), and container builds. Enforced zero-downtime rolling deployments.
- **Hosting**: Scalable cloud deployment strategy utilizing managed container services (e.g., AWS ECS or EKS), managed PostgreSQL (RDS), and managed Redis (ElastiCache).
- **Observability**: Centralized logging via ELK/Datadog, APM tracing for request flows traversing API and workers, and Prometheus/Grafana for infrastructure metrics.
- **Rollback Systems**: Immutable container tagging combined with blue/green deployment strategies and automated database migration rollback scripts.

## Testing Strategy

- **Unit Testing**: Pytest for backend endpoints and isolated business logic. Vitest for React components and utility functions in the frontend.
- **Integration Testing**: Testing API contracts against the database in a spun-up test container environment. Cross-service validation between API and workers.
- **End to End Testing**: Playwright or Cypress tests validating critical user journeys (login, viewing a session, generating a report).
- **Validation Workflows**: `scripts/dev-verify.sh` enforcing formatting (Prettier, Markdownlint) and successful test suites before any pull request can be merged.

## Refactoring Opportunities

- **Simplifications**: Consolidate repetitive Tailwind classes into reusable component libraries or configuration presets.
- **Modularization**: Decouple shared Pydantic schemas into a common library repository or package accessible by API, `worker-cv`, and `worker-asr` to maintain strict parity.
- **Scalability Improvements**: Introduce a dedicated real-time layer (e.g., WebSockets or Server-Sent Events) to stream status updates from ASR/CV workers directly to the web client instead of aggressive polling.

## Risks & Tradeoffs

- **Technical Limitations**: Processing high-resolution video streams for CV is extremely compute-intensive. Relying on synchronous processing or under-provisioned worker pools will cause unacceptable delays.
- **Complexity Tradeoffs**: Managing distributed microservices (web, api, cv, asr, metrics) introduces operational overhead and networking complexity compared to a monolith, but is strictly necessary for independent scaling of ML tasks.
- **Scalability Concerns**: The ingestion endpoint must be highly robust to handle sudden bursts of data from offline devices syncing simultaneously without exhausting database connection pools.

## Agile Sprint Plan

- **Milestones**:
  - Sprint 1: Establish foundational observability, infrastructure, schemas, and CI pipelines (PedagogyX implementation rules).
  - Sprint 2: Core API CRUD operations and database migrations, synthetic data pipelines.
  - Sprint 3: Implement ASR and CV worker queues with dummy/synthetic processing.
  - Sprint 4: Frontend dashboard integration with Next.js app router and real-time status updates.
- **Implementation Phases**: Infrastructure -> Core APIs -> Async Workers -> Frontend Integration -> E2E Polish.
- **Priorities**: System stability, clear API contracts, and deterministic test suites take precedence over feature breadth.
- **Expected Outcomes**: A resilient, testable MVP stack capable of ingesting device data, queueing it for mock multi-modal processing, and rendering the results in a performant React 19 interface.
