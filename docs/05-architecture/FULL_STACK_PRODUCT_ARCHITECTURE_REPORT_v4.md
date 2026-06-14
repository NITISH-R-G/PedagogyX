# PedagogyX Full Stack Product Architecture Report

## 1. Product & Problem Analysis

**Requirements:**
PedagogyX requires an end-to-end multimodal AI classroom intelligence platform capable of capturing, processing, and analyzing classroom interactions. The platform must process audio via ASR (Automatic Speech Recognition) to generate transcripts and calculate talk ratios, with future support for computer vision (CV). The solution needs to be robust, secure, and intuitive for school administrators and teachers.

**User Workflows:**

- A teacher or device records a session.
- Audio chunks are uploaded to the API sequentially or in bulk.
- Upon completion, the session is processed asynchronously to extract metrics (e.g., teacher-to-student talk ratio) and generate transcripts.
- School administrators and teachers can review sessions, metrics, and insights via a Next.js web application.

**Edge Cases:**

- Network interruptions during chunk uploads.
- Missing or malformed chunk processing.
- Delays in asynchronous worker execution.
- High concurrent uploads from multiple classrooms.

**Constraints:**

- Must handle potentially large audio data seamlessly.
- Need for low latency insights where possible.
- Local development without GPU requirements, but production will require GPU acceleration for models.

## 2. Full Stack Architecture

**Frontend Structure:**
Next.js 15 App Router providing an administrative and teacher-facing school overview interface. It communicates directly with the central REST API.

**Backend Structure:**
A Python-based FastAPI microservice architecture orchestrating the core business logic.

- **api:** Manages session lifecycles, health checks, chunk uploads, and queues jobs.
- **worker-asr:** Consumes jobs from Redis to perform speech-to-text processing (using faster-whisper in production).
- **worker-metrics:** Calculates insights such as preview talk ratios from ASR segments.
- **worker-cv:** Placeholder for Phase 2 computer vision capabilities.

**APIs:**
RESTful API for session management, providing endpoints to create sessions, upload chunks, complete sessions, and fetch preview metrics/transcripts.

**Database Architecture:**

- **PostgreSQL:** Primary relational datastore for sessions, chunks metadata, transcripts, metrics, and DAT (Device Access Toolkit) session states.
- **Redis:** In-memory queue (RQ/Celery or custom pub/sub) for asynchronous task dispatch to workers.
- **MinIO:** Object storage for storing raw audio/video chunks and artifacts.

**Infrastructure Layout:**
Docker Compose-based local development stack simulating production cloud environments with distinct services for APIs, workers, databases, and frontend.

## 3. Frontend Strategy

**UI Architecture:**
React 19 Server Components with Next.js App Router for optimal rendering performance. Tailwind CSS is used for styling.

**State Management:**
Server-side data fetching combined with lightweight client state for interactions, minimizing heavy client-side Redux/Context overhead where possible.

**Responsiveness:**
Mobile-first Tailwind CSS implementation ensuring the web interface is functional on tablets (in-classroom) and desktops (administration).

**Accessibility:**
Semantic HTML, ARIA labels, and keyboard navigability following WCAG guidelines to ensure inclusive usage by all school staff.

**Optimization Strategy:**

- React Server Components to reduce client bundle size.
- Lazy loading for heavy charts/visualizations.
- API response caching via Next.js cache mechanisms.

## 4. Backend Strategy

**API Architecture:**
FastAPI providing asynchronous endpoints. Usage of Python concurrency to handle IO-bound tasks like fetching from databases and object storage efficiently.

**Database Workflows:**
Connection pooling via `psycopg2` within FastAPI lifecycle. Heavy processing is offloaded from the API to prevent blocking.

**Caching:**
Redis can be utilized to cache heavily accessed session summaries and school overview data, reducing PostgreSQL load.

**Async Systems:**
Worker-based architecture where the API merely enqueues tasks upon session completion, ensuring horizontal scalability.

**Scalability Strategy:**
Stateless API servers and horizontally scalable workers. As processing needs increase, `worker-asr` and `worker-cv` can be scaled out independently, possibly running on GPU-backed instances.

## 5. Database Design

**Schema:**

- `sessions`: Core entity tracking the lifecycle of a recorded event.
- `session_chunks`: Tracks uploaded file chunks and their object storage keys.
- `session_transcripts` & `session_metrics`: Stores processed AI outputs.
- `dat_sessions` & `dat_session_events`: Tracks physical device capture states and events.

**Indexing:**
Indexes on `school_id` and `created_at` in the `sessions` table, and `session_id` in chunks and metrics tables to optimize read operations.

**Optimization:**
Using UUIDs for distributed ID generation and partitioning potential. JSONB used for flexible segment/event data.

**Consistency Strategy:**
Foreign keys with cascading deletes to maintain referential integrity. Transactions for multi-step operations like chunk metadata insertion.

## 6. Security Strategy

**Authentication & Authorization:**
API Key validation (currently placeholder) for service-to-service and client-to-API communication. Future implementation of JWT or OAuth2 for user-level access control.

**Validation:**
Pydantic models in FastAPI ensure strict input validation on all endpoints, rejecting malformed requests immediately.

**Vulnerability Prevention:**

- Parameterized SQL queries to prevent injection (handled via DB driver/ORM).
- File upload size limits to prevent DoS attacks.
- Secure environment variable management.

## 7. DevOps & Deployment

**CI/CD:**
GitHub Actions for continuous integration, testing, and building Docker images.

**Hosting:**
Containerized deployments suitable for Kubernetes or AWS ECS. Distinct node groups for CPU workloads (API, web) and GPU workloads (workers).

**Observability:**
Logs streamed from workers and API. Next steps include adding Prometheus metrics for endpoint latency and OpenTelemetry for distributed tracing.

**Rollback Systems:**
Immutable Docker image tags and database migrations managed systematically to allow point-in-time rollbacks.

## 8. Testing Strategy

**Unit Testing:**
Pytest for backend logic, including mocked database and MinIO interactions. Vitest for frontend React components.

**Integration Testing:**
Tests verifying the complete flow from session creation, chunk upload, to queue enqueueing using isolated test databases.

**End-to-End Testing:**
Playwright tests simulating teacher interactions on the web UI and verifying backend processing outcomes.

**Validation Workflows:**
Pre-commit hooks and CI pipelines enforcing code formatting (Prettier, Flake8), type checking (mypy, tsc), and test coverage.

## 9. Refactoring Opportunities

**Simplifications:**
Consolidate repeated database access patterns in FastAPI into a more structured repository pattern.

**Modularization:**
Separate the DAT session logic from standard sessions if they evolve differently, establishing clear bounded contexts.

**Scalability Improvements:**
Implement streaming chunk uploads directly to MinIO via pre-signed URLs to bypass the API server entirely, reducing API memory and network bottleneck.

## 10. Risks & Tradeoffs

**Technical Limitations:**
Local dev lacks GPU, meaning `worker-asr` uses a stub. This creates a disparity between dev and production behaviors.

**Complexity Tradeoffs:**
Microservices introduce operational complexity (managing queues, distributed tracing) but are necessary for the heavy, async nature of AI processing.

**Scalability Concerns:**
Database connection limits as the number of workers scales. Pgbouncer or similar connection pooling at the infrastructure level will be required.

## 11. Agile Sprint Plan

### Milestone 1: Hardening the Foundation (Sprint 4)

- **Priorities:** Implement pre-signed URLs for MinIO chunk uploads, removing API bottleneck. Add robust error handling in workers.
- **Expected Outcomes:** More stable uploads and reduced API load.

### Milestone 2: Production Readiness (Sprint 5)

- **Priorities:** Integrate real `faster-whisper` in a GPU container for `worker-asr`. Set up full CI/CD deployment to staging.
- **Expected Outcomes:** End-to-end ASR processing working in a production-like environment.

### Milestone 3: Observability & Security (Sprint 6)

- **Priorities:** Add OpenTelemetry tracing, Prometheus metrics, and implement proper JWT authentication.
- **Expected Outcomes:** Secure platform with deep visibility into processing latency and system health.
