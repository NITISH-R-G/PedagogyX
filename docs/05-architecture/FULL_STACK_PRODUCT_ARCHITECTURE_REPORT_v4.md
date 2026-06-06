# Full Stack Product Architecture Report v4

## Product & Problem Analysis

- **Requirements**: PedagogyX aims to optimize teacher performance via multimodal AI insights. The platform requires high-throughput data ingest from wearable devices without disrupting classrooms. Strict compliance with DPDP data privacy regulations blocks full production until G2 authorization.
- **User Workflows**: Teachers record audio/video via Meta Ray-Ban (DAT) glasses. Sessions are uploaded in chunks from the Android host app to the edge buffer and then to the cloud. Administrators consume the processed session metrics (like Talk Ratio) via a Next.js admin dashboard to monitor pedagogical effectiveness.
- **Edge Cases**: Disconnected environments, intermittent network on smartboards or mobile hotspots, partial uploads, unexpected session interruptions, and extremely low-end hardware on the Android host side.
- **Constraints**: G2 legal blockage limits testing to synthetic data; RTX 5070 GPU constraint for local benchmarking; heavy reliance on FOSS infrastructure per ADR-0005.

## Full Stack Architecture

- **Frontend Structure**: A modular, responsive Next.js web application utilizing Tailwind CSS v4 and React 19, serving as the admin shell.
- **Backend Structure**: A scalable microservices architecture relying on FastAPI (`services/api`) for core endpoints and Python workers (`services/worker-asr`, `services/worker-cv`, `services/worker-metrics`) for asynchronous ML tasks.
- **APIs**: RESTful architecture utilizing chunk-resumable upload endpoints to handle large, discontinuous media payloads efficiently.
- **Database Architecture**: PostgreSQL for structured metadata (sessions, metrics) paired with MinIO for S3-compatible unstructured chunk storage. Redis is used for worker queue orchestration.
- **Infrastructure Layout**: Docker Compose drives local orchestration, scaling cleanly into Kubernetes or container instances in the cloud. Edge buffers intercept device traffic for reliability over unstable LAN/WAN.

## Frontend Strategy

- **UI Architecture**: Component-centric design extracting reusable UI primitives. Layout leverages Tailwind CSS v4 to maintain a strict design token system.
- **State Management**: Uses React 19 primitives (Context, Hooks) prioritizing server components where possible to reduce client payload.
- **Responsiveness**: Fluid layouts using CSS Flexbox and Grid to guarantee usability on limited-resolution administrative devices.
- **Accessibility**: Strict adherence to WCAG AA. Semantic HTML, dual-coded status indicators, and screen-reader compliant ARIA landmarks to ensure inclusive operation.
- **Optimization Strategy**: Aggressive code-splitting, lazy-loading of heavy data visualizations, and minimal client-side JavaScript to optimize Core Web Vitals.

## Backend Strategy

- **API Architecture**: FastAPI handles high-concurrency ingestion and orchestrates background jobs, structured around dependency injection for optimal testing.
- **Database Workflows**: Clean repository patterns to abstract SQL logic. Connection pooling utilizes a shared cursor approach to mitigate N+1 inefficiencies and leakages.
- **Caching**: Global Redis client instantiation with lazy loading prevents connection churn and speeds up frequently accessed data (e.g., active session statuses).
- **Async Systems**: Blocking ML operations (like `faster-whisper` in `worker-asr`) are decoupled onto background Redis queues to maintain non-blocking API event loops.
- **Scalability Strategy**: Stateless API nodes and horizontally scalable worker pods allow independent scaling based on queue depth and payload size.

## Database Design

- **Schema**: Strongly typed relational tables (Sessions, Uploads, Metrics) with normalized foreign key relationships enforcing data integrity.
- **Indexing**: Strategic composite indices on session timestamps, device IDs, and processing statuses to ensure low-latency dashboards for admins.
- **Optimization**: Efficient connection lifecycle management utilizing `@contextlib.contextmanager` and `psycopg2.pool.SimpleConnectionPool` to prevent overhead.
- **Consistency Strategy**: Transactional boundaries bound exactly to logical operations. Chunk assembly leverages atomic commits to prevent orphaned media files.

## Security Strategy

- **Authentication**: Stateless JWT or strict Bearer API Key validation (`HTTPBearer`) protecting all ingest and read operations.
- **Authorization**: Role-Based Access Control (RBAC) ensuring teachers view their own data, while district admins have aggregated scopes.
- **Validation**: Comprehensive Pydantic models validate all incoming payloads. Malformed or unexpectedly large chunks are rejected instantly.
- **Vulnerability Prevention**: No PII processing prior to G2 sign-off. SQL injection prevention via parameterized queries; environment secrets are strictly segregated and validated.

## DevOps & Deployment

- **CI/CD**: GitHub Actions workflow (`dev-verify.yml`) handles Python linting (ruff, black, flake8), frontend formatting (prettier), and security auditing.
- **Hosting**: Current target is local dev and pilot testing via `infra/compose.dev.yaml` simulating production topologies.
- **Observability**: Centralized error tracking via Dead Letter Queues (DLQ) in Redis. Background workers surface traceback errors to standard out for log aggregation.
- **Rollback Systems**: Database migrations are strictly versioned, and stateless container deployments allow instant version reversion.

## Testing Strategy

- **Unit Testing**: Pytest handles backend logic, extensively mocking PostgreSQL connections (`@patch("app.db_utils.psycopg2.connect")`) to isolate test conditions.
- **Integration Testing**: API endpoints tested against mock databases and Redis instances to ensure complete request lifecycles.
- **End to End Testing**: The `tools/mock-capture/` suite simulates Meta Ray-Ban data streams to validate the complete ingest-to-dashboard pipeline locally.
- **Validation Workflows**: Automated linters (`ruff`, `markdownlint`, `prettier`) run prior to code merges to ensure high code quality and uniformity.

## Refactoring Opportunities

- **Simplifications**: Consolidation of disparate endpoint validation logic into unified Pydantic middleware.
- **Modularization**: Refactoring large FastAPI route files into specific domain controllers (e.g., chunk ingest, metrics read).
- **Scalability Improvements**: Shifting long-running metrics computation from synchronous API lifecycle events into explicit worker jobs to free up event loop capacity.

## Risks & Tradeoffs

- **Technical Limitations**: Edge networks in pilot schools might block high-bandwidth chunk uploads, increasing reliance on the local Go ingest buffer.
- **Complexity Tradeoffs**: Managing microservices locally via Docker Compose increases developer friction initially but ensures production parity.
- **Scalability Concerns**: The `worker-asr` relying on faster-whisper demands significant VRAM (RTX 5070 constraints); dynamic scaling on cloud instances could incur substantial cost overheads if not throttled.

## Agile Sprint Plan

- **Milestones**: Deliver Sprint 03 complete with an authorized vertical slice containing chunk ingest, ASR processing, and the admin dashboard MVP.
- **Implementation Phases**:
  1. Finalize the Go ingest buffer and FastAPI upload receivers.
  2. Stand up the `worker-asr` with mocked metrics.
  3. Deploy the Next.js frontend with live polling against the staging API.
- **Priorities**: High-impact administrative analytics (M-A and M-B metrics) and uninterrupted teacher recording UX.
- **Expected Outcomes**: A seamless demonstration of an end-to-end capture session successfully rendered on the admin dashboard, proving architectural viability under production-like conditions.
