# Autonomous Senior Systems Engineer & System Design Architect Report v2

## System Overview

### Purpose

PedagogyX is an advanced educational analysis platform designed to ingest multimodal data (video, audio, metrics) captured primarily via the Meta Ray-Ban v1 client (`clients/android-capture-dat`). The platform provides deep, privacy-preserving insights into classroom dynamics and educational interactions.

### Requirements

- 100% Free and Open Source Software (FOSS) mandate.
- Support for complete offline execution to guarantee data residency compliance.
- Support for multimodal ingestion from mobile devices, specifically Meta Ray-Ban glasses.
- Highly modular microservices architecture supporting diverse workloads (web, api, worker-cv, worker-metrics, worker-asr).
- Strict adherence to the sequence of architecture, foundations, then UI development.

### Scale Assumptions

- Designed to handle high-bandwidth video and audio streams from numerous concurrent classroom recording sessions.
- Data processing includes compute-intensive computer vision (CV) and automatic speech recognition (ASR) workloads.
- The system must function effectively both in edge offline environments and potentially scaled centralized environments, though offline capability is paramount.

### Constraints

- **Hardware Limitations:** Processing must comfortably operate on consumer-grade hardware, specifically bounded by a maximum of an RTX 5070 with 12GB VRAM.
- **Data Privacy:** Complete offline support required.
- **Legal Compliance:** G2 (India legal sign-off) blocks production data; development relies solely on docs, benchmarks, boilerplate dev stack, and synthetic test sessions.

---

## High Level Architecture

### Major Components

1. **clients/android-capture-dat:** Android-based capture application integrating with Meta Ray-Ban v1 for video/audio streaming.
2. **api (FastAPI):** Central orchestrator, handling ingestion, authentication, and routing workloads.
3. **web (Next.js & React):** The presentation layer for configuring sessions and viewing educational insights.
4. **worker-cv:** Specialized asynchronous worker dedicated to computer vision tasks (e.g., student engagement tracking).
5. **worker-asr:** Specialized asynchronous worker for transcription and audio analysis.
6. **worker-metrics:** Worker aggregating inferences into structured educational metrics and dashboards.

### Interactions & Data Flow

1. Capture client streams multimodal data to the `api` service.
2. The `api` service authenticates and securely stores raw assets (simulated edge storage/MinIO), generating analysis tasks.
3. Tasks are enqueued via a lightweight message broker (e.g., Redis).
4. `worker-cv` and `worker-asr` consume tasks, process data within the 12GB VRAM constraints (utilizing quantization and model multiplexing), and emit inferences back to the broker/database.
5. `worker-metrics` aggregates inferences and updates the analytical data store.
6. `web` queries the `api` for processed results.

### Service Boundaries

- **API:** Stateless, high-throughput, orchestration and edge gateway.
- **Workers:** Stateful (with model weights loaded), asynchronous processing, hardware-bound.
- **Web:** UI exclusively, strictly decoupled from core business logic.

---

## Infrastructure Design

### Deployment Topology

- **Offline Edge Mode:** Fully containerized via Docker Compose (`infra/compose.dev.yaml`), deploying all microservices, databases, and message queues on a single node equipped with an RTX 5070.
- **Cloud/Scaled Mode:** Easily translatable to a Kubernetes environment using Helm charts, scaling API pods horizontally and worker pods horizontally based on GPU node availability.

### Cloud Architecture

- Platform agnostic, but optimized for bare-metal edge deployments given the data residency constraints. If deployed in the cloud, relies on managed PostgreSQL, Redis, and S3-compatible storage.

### Networking

- Internal service-to-service communication occurs over a secure virtual network.
- `api` serves as the sole ingress point for the client applications, protected by authentication.

### Orchestration

- Current baseline relies on Docker Compose for reproducibility and offline execution.
- Path to production orchestration (if scaled beyond a single edge node) involves K3s or full Kubernetes, heavily leaning on custom resource definitions (CRDs) for GPU workload scheduling.

---

## Database Design

### Schema Strategy

- Relational schema (PostgreSQL) optimized for complex educational metadata, session tracking, and user management.
- Utilizes `psycopg2.pool.ThreadedConnectionPool` for robust multi-threaded API access.

### Replication & Scaling

- For single-node offline deployments, relies on local volume persistence.
- In distributed environments, primary-replica replication for PostgreSQL to scale read queries from the `web` and `worker-metrics` services.

### Consistency Model

- **Strong Consistency:** Required for session management, metadata, and configuration (PostgreSQL).
- **Eventual Consistency:** Acceptable for aggregated metrics and asynchronous processing results.

---

## Scalability Strategy

### Horizontal Scaling

- The `api` and `web` services are entirely stateless and can scale horizontally without limits.
- `worker-cv` and `worker-asr` scale horizontally relative to the number of available GPUs or node resources.

### Caching

- Redis is utilized for caching frequent API responses, user session data, and transient task states to reduce database load.

### Partitioning

- In high-volume scenarios, large multimedia assets are sharded across scalable blob storage (MinIO/S3).

### Load Balancing

- Nginx or Traefik handles ingress load balancing to the `api` and `web` instances.

---

## Reliability Strategy

### Failover & Redundancy

- The system is designed to gracefully degrade. If a `worker-cv` fails, tasks remain in the queue until the worker restarts or another picks it up.
- Automatic restarts via Docker Compose or Kubernetes control loops.

### Recovery Mechanisms

- Robust dead-letter queues (DLQ) for failed CV or ASR tasks to prevent poison pill scenarios and allow manual intervention/reprocessing.

### Resilience Patterns

- **Circuit Breakers:** Implemented in the `api` when communicating with synchronous external services or heavy worker queues to prevent cascading failures.
- **Retries:** Exponential backoff implemented for database connectivity and inter-service HTTP calls.

---

## Security Architecture

### Authentication & Authorization

- Robust HTTPBearer API key authentication for client capture devices (`verify_api_key`).
- Role-Based Access Control (RBAC) enforced at the API layer for the Next.js web application.

### Encryption

- All data in transit is encrypted via TLS.
- Data at rest encryption implemented for database volumes and blob storage to ensure privacy.
- Avoidance of hardcoded credentials in codebase (e.g., SonarCloud compliance via ENV vars).

### Abuse Prevention

- Rate limiting implemented on the `api` ingress to prevent resource exhaustion from rogue client devices or malicious traffic.

---

## Observability Stack

### Logging

- Centralized, structured JSON logging across all microservices (`web`, `api`, `worker-*`).
- Contextual correlation IDs injected at the API gateway and passed to workers.

### Tracing

- Distributed tracing (e.g., OpenTelemetry) to track request lifecycles from the Android client through the API and into the asynchronous worker queues.

### Monitoring & Alerting

- Metrics exported for Prometheus.
- Dashboards for monitoring GPU VRAM utilization (critical for the 12GB constraint), queue lengths, task processing latency, and API error rates.

---

## Performance Optimization

### Bottlenecks

- The primary bottleneck is the RTX 5070 12GB VRAM constraint during concurrent CV and ASR processing.

### Latency Optimization

- Implement model quantization (INT8/FP16) for neural networks in `worker-cv` and `worker-asr` to fit within VRAM and improve inference speed.
- Batch processing of frames/audio segments where applicable to maximize GPU utilization.

### Throughput Optimization

- Decoupling API ingestion from processing. The API immediately acks receipt of data and delegates heavy lifting, maintaining high ingestion throughput.

---

## Tradeoffs

### Pros

- Fully offline capable, guaranteeing absolute data privacy and legal compliance.
- Highly modular, allowing independent scaling and development of specialized workers.
- FOSS mandate ensures long-term sustainability and eliminates vendor lock-in.

### Cons

- Managing complex ML workloads within a strict 12GB VRAM budget requires significant engineering effort in model optimization and memory management.
- Offline-first architecture limits the ability to leverage massive cloud-scale data processing for instantaneous results on large datasets.

### Limitations & Future Improvements

- Current focus on single-node edge limits total concurrency. Future improvements involve distributed edge clustering.
- Expanding client support beyond Meta Ray-Ban v1.

---

## Agile Sprint Plan

### Implementation Phases & Milestones

- **Phase 1: Foundation & Observability (Current)**
  - Establish `infra/compose.dev.yaml` baseline.
  - Implement structured logging, metrics endpoints, and OpenTelemetry tracing across `api` and existing workers.
- **Phase 2: Core Ingestion & Contracts**
  - Finalize API schemas for `clients/android-capture-dat`.
  - Ensure robust authentication and robust database interaction using `psycopg2` pools.
- **Phase 3: Worker Optimization (The 12GB VRAM Challenge)**
  - Implement and benchmark quantized models in `worker-cv` and `worker-asr` to ensure they can run concurrently or sequentially under 12GB VRAM.
  - Establish synthetic testing pipelines (given the G2 data block).
- **Phase 4: Web Application Integration**
  - Connect the Next.js/React frontend to the stabilized API and aggregated metrics.

### Technical Priorities & Risk Assessment

- **Priority:** Model memory management. **Risk:** OOM errors crashing workers due to the strict hardware constraints. Mitigation: rigorous profiling and implementation of model multiplexing or swapping.
- **Priority:** Local development stability. **Risk:** Developer friction due to complex ML dependencies. Mitigation: comprehensive containerization and documentation.
