# PedagogyX: Architecture Scaffolding & System Design

**Author:** Principal Research Architect
**Document Version:** v1.0
**Status:** DRAFT

## 1. High-Level System Architecture

The PedagogyX system is designed as a distributed, event-driven architecture capable of processing multimodal streams (video, audio, text) from classrooms.

### Core Components

1.  **Client Capture Devices (Edge):**
    - Meta Ray-Ban DAT (Primary v1 client).
    - Secondary: Android/Windows smartboards.
    - Function: Captures raw video/audio, performs local buffering, and handles secure transmission to the cloud.
2.  **Ingress API & Storage (Cloud):**
    - Node.js/Express API Gateway.
    - Handles authentication, device registration, and initial payload validation.
    - Raw media is streamed directly to Object Storage (MinIO/S3).
3.  **Event Bus (Message Queue):**
    - Redis (MVP) / Kafka (Production).
    - Decouples media ingestion from processing. Triggers jobs upon successful file upload.
4.  **AI Inference Workers (Python):**
    - **ASR Worker (Audio):** Extracts audio, runs VAD (Voice Activity Detection), and transcription (Whisper).
    - **Vision Worker (Video):** Samples frames, runs pose estimation, engagement tracking, and board OCR.
    - **NLP/Metrics Worker:** Aggregates transcripts and visual context, computes pedagogical metrics, and interfaces with LLMs for coaching generation.
5.  **Data Persistence Layer:**
    - **PostgreSQL:** Relational data (Users, Schools, Sessions, Aggregated Metrics).
    - **Qdrant:** Vector embeddings of transcripts and generated insights for semantic search/RAG.
    - **MinIO/S3:** Blob storage for raw video, processed chunks, and artifacts.
6.  **Web Dashboard (Next.js):**
    - Provides interfaces for teachers to view coaching insights and admins to view aggregate analytics.

## 2. Multimodal Data Pipeline (The "Cold Path")

Given the constraint of post-processing (not strict real-time), the system utilizes a "Cold Path" batch processing architecture:

1.  **Upload & Ingest:** Session ends. Client uploads MP4/WebM to MinIO.
2.  **Job Enqueue:** Ingress API creates a `Session` record in Postgres and publishes a `process_session` event to Redis.
3.  **Audio Extraction & ASR:**
    - Worker pulls event.
    - Uses FFmpeg to extract `.wav`.
    - Runs Whisper model -> Generates timestamped VTT/JSON transcript.
    - Publishes `asr_complete` event.
4.  **Pedagogical Metric Computation:**
    - Metrics worker consumes `asr_complete`.
    - Analyzes transcript for metrics (e.g., Teacher Talk Time, Question Ratios).
    - Generates prompt containing transcript + context -> Sends to LLM (e.g., Llama 3 on local GPU or API).
    - Saves metrics and coaching feedback to Postgres.
5.  **Notification:** System updates Next.js UI or sends email to the teacher that their session analysis is ready.

## 3. Deployment Architecture (Phase 1 MVP)

To meet the ₹0 customer pilot budget and utilize the specified RTX 5070 hardware, the MVP will be deployed using a monolithic Docker Compose stack on a single bare-metal server.

- **Host OS:** Ubuntu Linux 22.04 LTS
- **Hardware:** Single Node, 1x NVIDIA RTX 5070, 32GB+ RAM, NVMe Storage.
- **Orchestration:** `docker compose`
- **Containers:**
- `web` (Next.js App + Node API)
- `worker-asr` (Python, PyTorch, Whisper, GPU accelerated)
- `worker-metrics` (Python, NLP/LLM tasks, GPU accelerated)
- `db` (PostgreSQL 15)
- `redis` (Redis 7)
- `minio` (S3 compatible storage)
- `qdrant` (Vector DB)

## 4. Security & Privacy Architecture (India DPDP Compliance)

- **Data Localization:** All infrastructure (including MinIO and Postgres) must be hosted in the `ap-south-1` region (Mumbai).
- **Data Minimization:** Models focus on _teacher_ audio/video. Student faces/voices are not the primary target and should be blurred/anonymized at the edge if hardware permits, or dropped from the pipeline immediately after aggregate metrics (like noise level) are computed.
- **Encryption:** TLS 1.3 in transit. AES-256 for data at rest.
- **Data Retention:** Automatic deletion policies on MinIO for raw video after metrics are generated (e.g., 7 days), retaining only anonymized transcripts and metrics for longitudinal analysis.

## 5. Scalability Path (Phase 2+)

1.  Migrate from Docker Compose to managed Kubernetes (EKS/GKE) in the target region.
2.  Replace Redis Pub/Sub with Kafka for persistent event streaming.
3.  Introduce dedicated GPU node pools for workers, utilizing auto-scaling based on queue depth (KEDA).
4.  Transition edge clients to run lightweight ONNX models for preliminary anonymization (face blurring) before upload.
