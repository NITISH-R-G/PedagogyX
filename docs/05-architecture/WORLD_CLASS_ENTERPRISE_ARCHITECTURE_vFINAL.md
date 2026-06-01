# World-Class Enterprise Architecture (PedagogyX vFINAL Phase 0)

**Status:** Phase 0 Active
**Date:** 2026-05-25
**Owner:** Lead Systems Engineer & Principal Research Architect
**Domain:** Multimodal Classroom Analytics & AI Pedagogy

## 1. System Overview

PedagogyX is designed as a hybrid Edge-Cloud, multimodal AI platform for classroom intelligence. The system ingests POV video and audio from Meta Ray-Ban smart glasses via an Android DAT companion app, processes it using a self-hosted OSS AI stack (ASR, CV, LLMs) on GPU clusters, and generates actionable pedagogical feedback.

**Core Mandates:**

- **OSS-First:** No proprietary APIs (OpenAI, AWS Transcribe). All ML models are self-hosted.
- **Thin Client Edge:** The Ray-Bans + Android phone act strictly as capture/buffer devices. Heavy ML inference occurs in the cloud.
- **India Data Residency:** Cloud infrastructure must be local to India.
- **Dual Pipeline:** Real-time ingestion (Hot Path) vs. Batch Processing (Cold Path).

## 2. High-Level Architecture

The architecture is divided into three distinct zones: Edge Capture, Control Plane, and Data/ML Plane.

### A. Edge Capture Zone (Classroom)

- **Hardware:** Meta Ray-Ban Smart Glasses.
- **Client:** Android companion app running the Wearables DAT (Device Access Toolkit) SDK.
- **Function:** Captures Bluetooth video/audio streams from glasses. Implements a local ring buffer to handle intermittent classroom network connectivity. Uploads chunked data (e.g., 5-second segments) to the cloud API via HTTPS/WebSockets.

### B. Control Plane (India Cloud)

- **API Gateway:** NGINX/Traefik handling SSL termination, rate limiting, and request routing.
- **Core API:** Python/FastAPI application. Manages authentication (RBAC), tenant isolation, session registration, and metadata CRUD operations.
- **Job Broker:** Redis. Manages the queue for asynchronous video processing tasks.

### C. Data & ML Plane (India Cloud GPU Cluster)

- **Hot Path (Ingest):** MediaMTX for handling WebRTC/RTSP streams (if live viewing is enabled).
- **Cold Path (Storage):** MinIO (S3-compatible) for immutable storage of raw video chunks, transcoded files, and output JSON reports.
- **Database:** PostgreSQL (psycopg2) for relational state (users, sessions, organization hierarchy, pedagogy scores).
- **Vector Database:** Qdrant. Stores embeddings of pedagogical rubrics and historical session transcripts for RAG-based LLM generation.
- **Worker Nodes (RTX 5070 Cluster):**
  - **Worker-ASR:** Runs `faster-whisper` for transcription and Pyannote for diarization.
  - **Worker-CV:** Runs YOLOv10 (TensorRT optimized) for spatial tracking, bounding boxes, and action recognition from the video stream.
  - **Worker-LLM:** Runs Qwen 2.5 (vLLM) to fuse ASR text and CV events into a final pedagogical report using RAG.

## 3. Multimodal Inference Pipeline (The Cold Path)

1.  **Chunk Assembly:** API receives 5s video chunks and stores them in MinIO. Once the session ends, a "Merge" job is dispatched to Redis.
2.  **Transcoding:** An FFmpeg worker merges chunks, normalizes audio to 16kHz mono (optimal for ASR), and extracts a lower-framerate video proxy for CV.
3.  **Parallel Inference:**
    - _ASR Job:_ Processes audio -> outputs JSON transcript with timestamps.
    - _CV Job:_ Processes video proxy -> outputs JSON of bounding box events (e.g., `{"timestamp": 12.5, "event": "teacher_at_whiteboard"}`).
4.  **Temporal Fusion:** A lightweight Python script aligns the ASR transcript and CV events chronologically.
5.  **LLM Evaluation:** The fused JSON is passed to the vLLM worker running Qwen 2.5. The LLM is prompted via RAG (pulling from Qdrant) to evaluate the session against defined pedagogical rubrics.
6.  **Report Generation:** The LLM outputs a structured JSON report (scores, coaching tips, timelines) which is saved to Postgres and MinIO.

## 4. Scalability & Reliability Strategy

- **Asynchronous Processing:** The API _never_ blocks on ML tasks. All heavy lifting is offloaded to Redis queues and background workers.
- **GPU Batching:** We utilize TensorRT and vLLM to maximize continuous batching on the RTX 5070s, crucial for staying within the D-10 cost budget.
- **Idempotent Workers:** All worker tasks are idempotent. If a worker dies mid-transcription, the Redis job is re-queued and processed by another node safely.
- **Dead Letter Queue (DLQ):** Failed jobs are routed to a DLQ for developer inspection to prevent silent failures and queue blocking.

## 5. Security & Privacy Architecture

- **Data Residency:** All Postgres, MinIO, and Redis instances are hosted on India-based servers.
- **RBAC (Role-Based Access Control):** Strict isolation at the API level. Teachers can view their own data; Principals can view aggregated school data; cross-tenant access is physically impossible via Postgres row-level security (RLS).
- **In-Transit Encryption:** TLS 1.3 enforced on all API and WebSocket endpoints.
- **At-Rest Encryption:** Disk-level encryption on the MinIO volumes.
- **Privacy by Design:** To comply with potential biometric regulations, CV models (YOLO) are trained for _generalized object detection_ (person, hand raised) rather than facial recognition. We do not store biometric templates.

## 6. Observability Stack

- **Logging:** Centralized structured JSON logging (ELK stack or Grafana Loki). No silent exceptions. All errors print tracebacks.
- **Metrics:** Prometheus scraping FastAPI endpoints (request latency, 4xx/5xx rates) and Redis queues (queue depth, worker processing time).
- **Dashboards:** Grafana visualizing system health, GPU utilization (via `dcgm-exporter`), and cost-per-session metrics.
- **Tracing:** OpenTelemetry integration to track a video chunk's journey from the Edge API through the Redis ML pipeline.
