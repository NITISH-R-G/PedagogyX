# System Architecture and Design

## System Diagrams

### Core Architecture Overview

```mermaid
graph TD
    Client[Client Devices (Meta Ray-Ban DAT)] -->|Secure WebSockets/HTTPS| API_Gateway[API Gateway (FastAPI)]
    API_Gateway --> Auth[Auth Service]
    API_Gateway --> Ingestion[Data Ingestion Service]

    Ingestion -->|Raw Streams| MinIO[Object Storage (MinIO/S3)]
    Ingestion -->|Events| Kafka[Event Bus (Kafka/Redis Streams)]

    Kafka --> Worker_ASR[Worker: ASR Pipeline]
    Kafka --> Worker_CV[Worker: CV Pipeline]
    Kafka --> Worker_Metrics[Worker: Metrics Aggregation]

    Worker_ASR --> VectorDB[(Vector DB - Qdrant)]
    Worker_CV --> VectorDB
    Worker_Metrics --> Postgres[(Relational DB - Postgres)]

    VectorDB --> Analytics_Engine[Pedagogical Analytics Engine]
    Postgres --> Analytics_Engine

    Analytics_Engine --> Web_UI[Web Dashboard (Next.js)]
```

## Infrastructure Maps

### Deployment Architecture (Hybrid Edge/Cloud)

- Edge (Classroom): Meta Ray-Ban DAT clients capture audio/video. Initial lightweight VAD (Voice Activity Detection) and compression happen on the companion mobile device.
- Ingress: Nginx/Traefik acting as reverse proxy and load balancer.
- Compute (Cloud): Kubernetes cluster (EKS/GKE) managing stateless microservices. GPU nodes provisioned for heavy inference tasks (ASR, complex CV).
- Storage: S3-compatible object storage for video blobs; PostgreSQL for relational metadata (users, sessions); Qdrant for dense vector embeddings of multimodal events.

## Event Pipelines

### Multimodal Dataflow

1. Capture: Client records session.
2. Ingestion: Stream or batch upload to API Gateway.
3. Decoupling: API Gateway writes metadata to Postgres, uploads media to Object Storage, and publishes a `session_created` event to the Event Bus.
4. Parallel Inference:
   - ASR Worker picks up the event, pulls audio, runs Whisper inference, diarizes, and publishes `transcript_generated`.
   - CV Worker picks up the event, pulls video, extracts keyframes, runs engagement/pose detection, and publishes `cv_features_extracted`.
5. Fusion: Analytics Engine subscribes to inference events, temporally aligns ASR and CV data, and generates a unified pedagogical timeline.

## Multimodal Inference Pipelines

### AI Orchestration

- Audio Pipeline: VAD -> Speaker Diarization -> ASR (Whisper) -> NLP (Intent Classification, Sentiment).
- Visual Pipeline: Frame Extraction (FFmpeg) -> Object Detection (YOLO/Custom) -> Pose Estimation -> Activity Recognition.
- Knowledge Graph: Extracted concepts and pedagogical events are mapped into an educational knowledge graph for longitudinal querying.
- Agentic Feedback: An LLM Agent (LangChain/LlamaIndex) queries the vector DB and Knowledge Graph to construct personalized, context-aware coaching feedback for the teacher.

## Security & Data Compliance (India DPDP)

- Data Residency: All infrastructure deployed in AWS `ap-south-1` or equivalent local data centers.
- Encryption: TLS 1.3 in transit; AES-256 for all data at rest in Postgres and S3.
- Anonymization: Automated face blurring for students before long-term storage if required by local policy.
- RBAC: Strict separation of privileges. Teachers own their data; administrators see aggregate anonymized metrics unless explicitly shared.
