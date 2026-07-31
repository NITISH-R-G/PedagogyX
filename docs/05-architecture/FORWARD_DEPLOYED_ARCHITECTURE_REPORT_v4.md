# Forward Deployed Architecture Report v4

## Operational Problem Analysis

PedagogyX requires a robust system to process multimodal classroom data (voice, video, slides, student engagement) to measure pedagogical efficiency. The operational reality involves capturing this data primarily through Meta Ray-Ban smart glasses via an Android companion application (DAT client). Currently, real pilot PII data is blocked pending G2 (India legal sign-off), so the system must operate on synthetic data during Phase 0 and MVP preparation. The main operational constraints involve ensuring seamless data capture, real-time feedback where possible, and reliable batch processing of heavy AI workloads without disrupting the classroom environment.

## System Architecture

The core architecture follows a microservices pattern designed for rapid deployment and iteration.

- **Client Tier**: Meta Ray-Ban glasses capturing multimodal data, routed through the Android DAT client.
- **API Gateway & Services**: A FastAPI-based `api` service handles incoming data streams and client requests.
- **Frontend**: A Next.js/React `web` service provides the dashboard for educators and administrators to view pedagogical insights.
- **Worker Tier**: Specialized workers handle specific workloads: `worker-asr` for speech recognition, `worker-cv` for computer vision, and `worker-metrics` for engagement analysis.
- **Data Layer**: PostgreSQL for relational data and metadata, MinIO for object storage (audio/video/image payloads), and Redis for caching and message brokering between the API and workers.

## Deployment Strategy

The deployment strategy is optimized for speed, reproducibility, and local validation prior to cloud rollout.

- **Local Validation**: Utilize `infra/compose.dev.yaml` for a complete local stack containing PostgreSQL, MinIO, Redis, and all microservices. This ensures operators can test end-to-end flows with synthetic data locally.
- **Cloud Deployment**: The containerized microservices will be deployed to a Kubernetes cluster for scalability. CI/CD pipelines will automate building, testing, and deploying Docker images.
- **Client Rollout**: The Android DAT client will be sideloaded or distributed via private channels to pilot testers equipped with Meta Ray-Ban glasses.
- **Rollback**: Container versioning will allow instant rollbacks of worker nodes or the API service if operational anomalies occur.

## Infrastructure Design

The infrastructure is designed to bridge local development simplicity with cloud-native scalability.

- **Compute**: Stateless FastAPI and React containers scaled horizontally based on traffic. GPU-accelerated instances reserved for the AI Cold Path workers.
- **Storage**: MinIO provides an S3-compatible API, allowing a seamless transition from local object storage to AWS S3 or GCP Cloud Storage in production. PostgreSQL handles transactional data with read replicas planned for scaling.
- **Messaging**: Redis acts as the message broker, decoupling the API ingestion from the asynchronous AI processing workers.
- **Observability**: Prometheus and Grafana will be integrated to monitor API latency, worker queue lengths, and hardware utilization, ensuring operational transparency.

## AI System Design

The AI architecture strictly separates workloads to optimize latency and resource utilization.

- **Hot Path**: Real-time or near real-time processing optimized for low latency. Uses lightweight models like YOLO for immediate visual context or engagement detection.
- **Cold Path**: Batch processing running on a central OSS offline inference backend. This handles heavy lifting like transcription (faster-whisper) and complex analysis (Ollama), consuming data from MinIO and updating PostgreSQL upon completion.
- **Orchestration**: The `api` service routes tasks to the appropriate Redis queues. Workers pick up tasks, process them using the respective models, and push results back to the database.

## Integration Plan

The system integrates various hardware and software components into a unified pipeline.

- **Hardware Integration**: The Android DAT client (`clients/android-capture-dat`) acts as the bridge between the Meta Ray-Ban hardware and the PedagogyX API, managing connection, data buffering, and upload.
- **Service Integration**: Internal services communicate via RESTful HTTP (Frontend to API) and Redis task queues (API to Workers).
- **Data Pipeline**: Raw media from the client is stored in MinIO. The API records metadata in PostgreSQL and enqueues jobs in Redis. Workers pull media from MinIO, process it, and update PostgreSQL with the generated insights.

## Operational Reliability

Reliability is built into the asynchronous processing model to handle unreliable network conditions typical in classroom environments.

- **Offline Support**: The Android DAT client buffers captured data locally if network connectivity drops, syncing with the API once reconnected.
- **Task Retry**: Redis-backed worker queues ensure that if a worker crashes during a heavy AI inference task, the job is not lost and can be retried by another worker.
- **Graceful Degradation**: If the Cold Path workers fall behind, the core API and Hot Path services remain functional, ensuring users can still upload data and view existing insights.

## Risks & Tradeoffs

- **Client Dependency**: High reliance on Meta Ray-Ban and the Android DAT client introduces hardware lock-in and potential platform policy risks.
- **Data Privacy**: The G2 legal block is a significant constraint. Relying on synthetic data for MVP validation may hide real-world edge cases in multimodal capture (e.g., background noise, poor lighting).
- **Inference Cost vs. Speed**: Separating Hot and Cold paths manages costs, but delayed Cold Path insights might impact the perceived immediate value for educators.
- **Complexity**: Operating a full local stack (PostgreSQL, MinIO, Redis, multiple workers) via Docker Compose increases the onboarding friction for new developers or operators.

## Agile Sprint Plan

- **Sprint 1: Core Infrastructure & Synthetic Capture**
  - Stabilize `infra/compose.dev.yaml`.
  - Finalize Android DAT client synthetic data upload to the local API.
- **Sprint 2: Hot Path Pipeline**
  - Implement basic API ingestion routing to MinIO.
  - Deploy `worker-cv` for initial Hot Path processing (YOLO).
- **Sprint 3: Cold Path & Data Persistence**
  - Deploy `worker-asr` (faster-whisper) and integrate central OSS offline inference backend.
  - Implement full metadata persistence in PostgreSQL and result surfacing in the React `web` dashboard.
- **Sprint 4: Operational Readiness**
  - Implement telemetry, logging, and operational dashboards.
  - Conduct end-to-end synthetic load testing to validate the architecture under pressure.
