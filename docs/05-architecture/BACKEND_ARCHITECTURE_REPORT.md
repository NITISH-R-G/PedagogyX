# Backend Architecture Report

**Status:** Draft v1.0
**Date:** 2026-05-20
**Role:** Autonomous Senior Backend Developer & Distributed Systems Architect

## 1. System & Requirement Analysis

PedagogyX requires a robust, scalable backend capable of handling high-throughput, long-running multimodal processing tasks (video, audio, inference) while supporting low-latency real-time dashboards for supervision. The system must operate under strict constraints: ₹0 hardware budget at the edge, OSS-only stack, India DPDP compliance, and an architecture that bridges unreliable school LANs with a centralized cloud processing pool.

## 2. Backend Architecture

We utilize an asynchronous, event-driven microservices architecture built primarily in Python (FastAPI).

- **API Gateway/Control Plane:** Handles auth, tenant routing, and metadata CRUD.
- **Ingest Service:** Manages WebRTC/MediaMTX streams from Edge nodes.
- **Worker Pool:** Celery-based distributed task queue consuming from Redis/RabbitMQ. Workers pull raw assets from MinIO, process them via ML models, and push results.
- **Aggregator Service:** Processes ML outputs into the composite Pedagogy Index and pushes to ClickHouse.

## 3. Database Design

- **Relational (OLTP):** PostgreSQL handles user accounts, RBAC, tenant configuration, and metadata about sessions/schools. Strict schema enforcement ensures data integrity.
- **Time-Series/Analytics (OLAP):** ClickHouse handles high-velocity ML inference events (e.g., frame-by-frame engagement scores, acoustic metrics) for fast dashboard aggregations.
- **Vector DB:** Qdrant stores document/transcript embeddings for semantic search and AI coaching context.
- **Object Storage:** MinIO (S3 API) stores raw video, audio, and extracted ML assets.

## 4. API Strategy

- **RESTful APIs (FastAPI):** Used for standard CRUD operations and control plane interactions. Strongly typed using Pydantic.
- **WebSockets:** Used for the Hot Path to push real-time (preview) metrics to the Admin Live Dashboard.
- **Internal GRPC/HTTP:** Fast internal communication between API and Worker nodes.

## 5. Scalability Strategy

- **Stateless Services:** All API nodes are strictly stateless, allowing horizontal scaling behind load balancers.
- **Queue-Based Decoupling:** Heavy processing is entirely decoupled. If the inference cluster is overwhelmed (due to the RTX 5070 bottleneck), tasks queue safely rather than crashing the control plane.
- **Data Partitioning:** Postgres tables and ClickHouse distributed tables will be partitioned by tenant ID to isolate data and speed up queries.

## 6. Reliability Strategy

- **Design for Failure:** Network partitions between schools and the cloud are expected. Edge nodes must handle local buffering.
- **Retry Mechanics:** Celery workers implement exponential backoff for transient failures (e.g., S3 upload timeouts).
- **Dead Letter Queues:** Failed processing jobs are routed to a DLQ for manual inspection to prevent queue poisoning.

## 7. Security Strategy

- **Authentication:** OAuth2/OIDC integrated with standard identity providers.
- **Authorization:** Fine-grained Role-Based Access Control (RBAC) enforced at the API layer (Tenant isolation is mandatory).
- **Encryption:** TLS 1.3 enforced in transit. Customer Managed Keys (CMK) for data at rest in MinIO/Postgres to comply with strict DPDP requirements.

## 8. Observability

- **Tracing:** OpenTelemetry instruments all requests across API and Worker nodes.
- **Metrics:** Prometheus scrapes system metrics (queue depth, worker utilization, API latency).
- **Logging:** Structured JSON logs shipped to a central aggregator (e.g., ELK or Grafana Loki).

## 9. Performance Optimization

- **Caching:** Redis heavily caches compiled dashboards and frequent API responses.
- **Batching:** Database inserts to ClickHouse are batched by the Aggregator service to maximize throughput.

## 10. Risks & Tradeoffs

- **Risk:** Python's GIL limiting API concurrency. **Tradeoff:** Acceptable for now by scaling Uvicorn workers horizontally, optimizing for the rich PyTorch/ML ecosystem over raw Go/Rust speeds.
- **Risk:** Queue backlog due to limited cloud GPU budget. **Tradeoff:** Strict SLA definition; we guarantee cold-path completion overnight, not instantaneously.

## 11. Agile Sprint Plan

- **Sprint 1:** Provision core infrastructure (Postgres, MinIO, Redis). Deploy API skeleton (FastAPI) with basic auth and tenant schemas.
- **Sprint 2:** Implement Ingest Service and Celery worker scaffolding. Establish robust upload/download mechanisms with MinIO.
- **Sprint 3:** Implement ClickHouse integration and Aggregator service. End-to-end test of a dummy ML pipeline passing data through the system.
