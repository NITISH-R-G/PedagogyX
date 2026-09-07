# Product Engineering Architecture Report v4

## Product & Problem Analysis

PedagogyX is an AI classroom intelligence platform designed to optimize teacher performance by analyzing multimodal inputs. The primary challenge is capturing high-quality audio and video without disrupting the classroom environment, while ensuring strict data privacy and compliance (especially Phase 0 G2 constraints regarding PII). The initial product targets the Meta Ray-Ban (DAT) smart glasses as the primary capture device, ensuring a seamless, wearable recording solution for teachers. The system must also operate efficiently in constrained environments (Indian schools with low bandwidth), using a centralized OSS-based inference cloud powered by consumer-grade GPUs (e.g., RTX 5070).

## Full Stack Architecture

The system employs a Hybrid Edge-Cloud architecture to handle constrained bandwidth environments and intensive background processing.

- **Frontend Structure**: Next.js (React Server Components) admin shell using Tailwind CSS for utility-first styling.
- **Backend Structure**: A stateless API gateway built with FastAPI handling chunk ingestion and session management. Background Python workers (using Celery/Redis) process heavy multimodal jobs.
- **APIs**: RESTful endpoints with multipart chunk ingestion, protected via RBAC and API keys.
- **Database Architecture**: PostgreSQL for structured relational data (sessions, metrics) and MinIO (S3-compatible) for object storage (video/audio chunks, ML artifacts).
- **Infrastructure Layout**: Centralized FOSS backend deployed via Docker Compose (FastAPI, Redis, PostgreSQL, MinIO, and Worker nodes), ensuring compatibility with on-premise or localized data centers to meet data residency laws.

## Frontend Strategy

The frontend focuses on delivering a seamless administrative and visualization experience.

- **UI Architecture**: Modular component design in Next.js using Server Components to minimize client bundle size.
- **State Management**: React Context and hooks for local state, with data fetching optimized for real-time visualization of Hot Path metrics.
- **Responsiveness**: Tailwind CSS v4 provides utility-first responsive breakpoints ensuring functionality across mobile, tablet, and desktop viewports.
- **Accessibility**: Adherence to WCAG guidelines, ensuring color contrast, semantic HTML, and screen-reader compatibility.
- **Optimization Strategy**: Lazy loading of large visual components and using Server Components to reduce time-to-interactive for teachers reviewing insights.

## Backend Strategy

The backend emphasizes high-throughput ingestion and asynchronous processing.

- **API Architecture**: FastAPI provides typed, asynchronous REST endpoints, ensuring robust validation via Pydantic.
- **Database Workflows**: Connection sharing implemented to avoid N+1 connection overhead during high-frequency telemetry ingestion.
- **Caching**: Redis is utilized for rate-limiting, session state caching, and queue management for worker nodes.
- **Async Systems**: Heavy tasks (YOLO computer vision, Whisper ASR) are offloaded to dedicated background workers, preventing API thread starvation.
- **Scalability Strategy**: Stateless API and separated worker nodes allow horizontal scaling based on queue depth and incoming traffic volume.

## Database Design

The data persistence layer ensures consistency and fast retrieval for pedagogical analytics.

- **Schema**: Normalized tables for sessions, teachers, schools, and metrics, ensuring data integrity.
- **Indexing**: B-tree indexes on session identifiers and timestamp columns to optimize time-series queries for dashboard visualizations.
- **Optimization**: Paging and cursor-based pagination for fetching historical session data to minimize memory consumption.
- **Consistency Strategy**: ACID compliance via PostgreSQL, with transactional boundaries defined around session completion and metric aggregation workflows.

## Security Strategy

Security is paramount due to the presence of minor student data.

- **Authentication**: Strict API key validation via `HTTPBearer` for service-to-service and client-to-server communication.
- **Authorization**: Role-Based Access Control (RBAC) ensuring teachers only view their own insights and admins have supervised access.
- **Validation**: Rigorous Pydantic schema validation on all inputs to prevent injection attacks and data corruption.
- **Vulnerability Prevention**: Environment variables explicitly enforced (no default fallbacks for secrets). No PII or production data processed without legal G2 clearance.

## DevOps & Deployment

The deployment pipeline is built for reliability and rapid iteration.

- **CI/CD**: GitHub Actions automate testing, linting (Ruff, ESLint, markdownlint), and Docker builds.
- **Hosting**: Docker Compose is used for local development and edge deployments, ensuring consistent environments.
- **Observability**: Dead Letter Queues (DLQ) for failed worker jobs, with tracebacks directed to standard error for centralized log aggregation. System-wide `/health` probes.
- **Rollback Systems**: Versioned Docker images and database migration scripts allow for quick rollbacks of faulty deployments.

## Testing Strategy

Testing ensures stability across the entire stack.

- **Unit Testing**: `pytest` and `pytest-mock` for backend logic, ensuring workers handle varied inputs correctly.
- **Integration Testing**: API tests with mocked database and MinIO interactions to validate the end-to-end ingestion flow.
- **End to End Testing**: Synthetic session simulators (`tools/mock-capture`) validate the complete ingest-to-metrics pipeline.
- **Validation Workflows**: Pre-commit hooks and `./scripts/dev-verify.sh` ensure code and documentation quality before merges.

## Refactoring Opportunities

Continuous improvement areas identified for the next development cycle.

- **Simplifications**: Centralize and unify the Dead Letter Queue (DLQ) logic across all background workers (`worker-asr`, `worker-cv`, `worker-metrics`).
- **Modularization**: Break down monolithic API route files into domain-driven service modules (e.g., session management, chunk processing).
- **Scalability Improvements**: Implement connection pooling using an async-compatible ORM driver (like asyncpg) to further reduce database connection latency under load.

## Risks & Tradeoffs

Architectural decisions involve inherent tradeoffs.

- **Technical Limitations**: Using consumer-grade GPUs (RTX 5070) limits the size of LLMs and CV models, requiring quantization and model distillation techniques.
- **Complexity Tradeoffs**: The Hybrid Edge-Cloud architecture with asynchronous processing adds operational complexity compared to a monolithic synchronous API, but is necessary for low-latency ingest.
- **Scalability Concerns**: Network intermittent connectivity from edge capture devices (Ray-Ban glasses) necessitates robust chunk buffering and resumable upload logic, increasing client-side complexity.

## Agile Sprint Plan

Structured plan to implement the architecture.

- **Sprint 1: Ingestion Pipeline Validation**: Solidify FastAPI chunk ingestion and MinIO storage, ensuring resilient uploads from edge devices.
- **Sprint 2: Async Processing Polish**: Standardize DLQ across all Python workers and optimize Redis queue handling for real-time (Hot Path) metrics.
- **Sprint 3: Next.js Dashboard Build**: Implement the teacher analytics dashboard using Next.js Server Components and Tailwind CSS v4.
- **Sprint 4: End-to-End Testing & Security Audit**: Expand test coverage, validate RBAC, and execute a mock-capture simulated load test.
