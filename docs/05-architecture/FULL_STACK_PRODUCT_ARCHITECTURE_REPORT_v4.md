# Full Stack Product Architecture Report

## Product & Problem Analysis

PedagogyX is an elite, scalable AI classroom intelligence platform engineered to augment teaching performance through multimodal input analysis. Our core product challenge involves ingesting high-throughput audio and video data non-intrusively during live classroom sessions, while concurrently solving for stringent data privacy and enterprise compliance (specifically navigating Phase 0 G2 constraints regarding PII). The product experience centers on the Meta Ray-Ban (DAT) smart glasses as the primary capture device, requiring a seamless bridge between wearable hardware and our cloud infrastructure, guaranteeing zero friction for educators. Our end-to-end mission is to deliver actionable, near real-time pedagogical metrics without disrupting natural classroom dynamics.

## Full Stack Architecture

We employ a highly resilient Hybrid Edge-Cloud architecture designed for maximum fault tolerance and ingest scalability, operating under strict production-readiness paradigms.

### Client

Meta Ray-Ban smart glasses (DAT) interfacing seamlessly with an Android host application, acting as the primary edge ingestion node.

### Edge Ingest

A highly concurrent, high-throughput ingest buffer service written in Go, deployed locally or on edge devices, responsible for robust chunk buffering and resilient forwarding over constrained networks.

### Central API Gateway

A horizontally scalable OSS-first FastAPI backend gateway. It coordinates session state, handles chunk validation, enforces API contracts, and orchestrates distributed queueing.

### Asynchronous Worker Fleet

Python-based scalable workers consuming from Redis. Core services include `worker-asr` (faster-whisper inference) and `worker-metrics`, decoupled for independent scaling and optimized for high-throughput stream processing.

### Admin & Insights Console

A high-performance Next.js web application delivering real-time actionable insights to administrators and pedagogical coaches.

## Frontend Strategy

Our Next.js frontend is engineered for absolute UX clarity, responsiveness, and developer experience.

### UI Architecture

Component-driven design leveraging React Server Components for optimal initial load times and Client Components for rich interactivity. We utilize Tailwind CSS v4 for utility-first, highly maintainable styling, optimizing bundle size and rendering performance.

### State Management

Intelligent caching and data fetching via React Query and Next.js built-in caching layers, ensuring real-time UI updates (e.g., talk ratios, live session metrics) with minimal network overhead.

### Accessibility & Performance

Strict adherence to WCAG 2.1 AA standards. We continuously monitor Core Web Vitals (LCP, FID, CLS), ensuring the dashboard feels instantaneous and accessible across all devices, particularly low-powered administrative tablets.

## Backend Strategy

The backend is architected for extreme reliability, low latency, and asynchronous scalability.

### API Architecture

FastAPI provides type-safe, asynchronous REST and WebSocket interfaces. The API layer focuses solely on validation, routing, and immediate acknowledgment, pushing all heavy computation to background queues.

### Asynchronous Systems

Heavy inference and metric extraction are completely decoupled via Redis-backed task queues. Workers implement idempotency, Dead Letter Queues (DLQ), and exponential backoff retry mechanisms to ensure zero data loss during ingest spikes.

### Scalability Strategy

Stateless API nodes scale horizontally behind a load balancer. Worker fleets scale dynamically based on queue depth metrics, allowing us to absorb massive surges in end-of-class upload bursts efficiently.

## Database Design

Our data layer prioritizes schema consistency, efficient querying, and horizontal scaling capabilities.

### Schema & Storage

- **Relational Data:** PostgreSQL acts as the source of truth for session metadata, user configurations, and structural relationships.
- **Blob Storage:** MinIO (S3-compatible) securely stores unstructured media chunks, isolated by tenant and session.

### Query Optimization

Rigorous indexing strategies on high-cardinality columns (e.g., session IDs, timestamps). We enforce strict connection pooling (via PgBouncer or equivalent) and avoid N+1 query patterns through eager loading and optimized joins in our data access layer.

### Migrations & Consistency

Database schema changes are strictly version-controlled via Alembic, ensuring zero-downtime migrations and schema consistency across environments.

## Security Strategy

Security is baked into the foundation, reflecting our strict adherence to data privacy regulations.

### Authentication & Authorization

Zero-trust API architecture. Endpoints require robust Bearer token validation with granular scope enforcement. We are transitioning towards OAuth2 with JWT for stateless, secure session management.

### Data Protection

Strict segregation of PII. Phase 0 G2 compliance dictates that no real school data is processed without legal sign-off. All media chunks are encrypted at rest and in transit (TLS 1.3).

### Vulnerability Prevention

Automated dependency scanning, strict input validation using Pydantic models at the API boundary, and defensive programming to neutralize injection attacks and CSRF vulnerabilities.

## DevOps & Deployment

We maintain a deployment-aware engineering culture focused on operational visibility and automated safety.

### CI/CD Pipelines

Robust GitHub Actions workflows enforce testing, linting, and security audits on every PR. We prioritize reproducible builds and immutable container artifacts for both API and frontend services.

### Infrastructure & Hosting

Containerized microservices orchestrated via Docker Compose for local/pilot setups, with a clear migration path to Kubernetes for production scaling.

### Observability

Centralized logging, distributed tracing, and comprehensive metrics collection. Worker failures and API errors trigger immediate alerts via Dead Letter Queue monitoring, guaranteeing rapid incident response.

## Testing Strategy

Our testing philosophy guarantees predictable behavior and deployment confidence.

### Validation Workflows

- **Unit Testing:** `pytest` for robust validation of backend business logic and worker isolation; `vitest` for frontend component logic.
- **Integration Testing:** Automated API endpoint testing using mock databases and `pytest-mock` to verify complex state transitions.
- **End-to-End Testing:** Synthetic session simulators (`tools/mock-capture`) that validate the complete data pipeline from edge ingest to UI visualization. Playwright is utilized for frontend regression testing.

## Refactoring Opportunities

Continuous improvement is essential for long-term maintainability.

### Simplification & Modularization

- Decouple monolithic API route handlers by abstracting business logic into isolated, independently testable service classes.
- Standardize the database session injection pattern across the entire backend to eliminate redundant connection lifecycle management.

### Scalability Improvements

- Transition from basic Redis queueing to a more robust event-streaming platform (e.g., Kafka or RabbitMQ) as throughput demands increase, enabling advanced pub/sub patterns and replayability.

## Risks & Tradeoffs

Engineering decisions involve balancing constraints and product goals.

### Complexity Tradeoffs

Maintaining a distributed async architecture introduces operational overhead (monitoring queues, handling partial failures) but is an unavoidable tradeoff to achieve our required ingest scalability and latency guarantees.

### Technical Limitations

Heavy reliance on Meta Ray-Ban devices for high-quality capture poses a hardware lock-in risk. We mitigate this by designing generalized API contracts that can seamlessly integrate alternative wearable or IP camera inputs in the future.

### Scalability Concerns

Handling simultaneous uploads from hundreds of classrooms at the end of a period could overwhelm our network ingress and storage IOPS. We must rigorously test our edge buffering strategy and rate-limiting policies.

## Agile Sprint Plan

Our execution roadmap prioritizes foundational stability and scalable product features.

### Sprint 06: Vertical Pipeline Stability

- Stabilize the edge-to-cloud data ingestion pipeline.
- Implement comprehensive unit and integration tests for the `worker-asr` service.
- Refactor API handlers for better modularity and error handling.

### Sprint 07: Observability & Resilience

- Deploy advanced DLQ mechanisms and alerting for asynchronous worker failures.
- Implement connection pooling and optimize heavy read queries on the dashboard.
- Upgrade frontend telemetry to track Core Web Vitals in production.

### Sprint 08: Security & Scalability Hardening

- Complete transition to JWT-based OAuth2 authentication.
- Conduct load testing on the async worker queue simulating peak classroom traffic.
- Finalize UI/UX refinements for the Next.js admin dashboard based on simulated user workflows.
