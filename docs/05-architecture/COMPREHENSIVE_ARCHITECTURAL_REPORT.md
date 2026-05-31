# Comprehensive Architectural Report

**Status:** Phase 0 Architecture Planning
**Date:** 2026-05-30
**Owner:** Architecture Team

This document details the exhaustive, world-class system architecture for PedagogyX. It is designed to scale from an India-based pilot (MVP) to a global enterprise rollout, balancing severe edge network constraints with massive centralized GPU compute requirements.

## 1. System Overview

PedagogyX employs a **Hybrid Edge-Cloud (Tiered)** architecture. The system ingests multimodal classroom data (audio, video, POV from Meta Ray-Bans), buffers it locally, and transmits it to a central cloud for asynchronous, heavy AI inference. The resulting insights are surfaced via a Next.js web dashboard.

## 2. High Level Architecture

### Tier 1: The Edge (Capture & Ingest)

- **Primary Client (v1):** Meta Ray-Ban Smart Glasses (POV capture).
- **DAT Host:** An Android device acting as the bridge via the Wearables DAT SDK.
- **Responsibilities:**
  - Local buffering to handle intermittent school Wi-Fi.
  - Chunking video/audio into manageable payloads (e.g., 5-minute segments).
  - Secure TLS transmission to the cloud gateway.
  - _Future:_ On-device Voice Activity Detection (VAD) to minimize bandwidth usage.

### Tier 2: The Ingestion Gateway

- **API Layer:** FastAPI running on Kubernetes (or Docker Compose for MVP).
- **Authentication:** `HTTPBearer` API keys (MVP), transitioning to OAuth2/OIDC.
- **Storage:** Streaming chunks directly to MinIO (S3-compatible) to prevent API node memory exhaustion.
- **Queueing:** Pushing job metadata to Redis (MVP) or Kafka (Production) for asynchronous processing.

### Tier 3: Multimodal Inference Workers (Central Cloud)

- **Audio Processing (ASR):** GPU-accelerated workers running `faster-whisper` for multilingual transcription (e.g., Hindi/English).
- **Computer Vision (CV):** Future workers analyzing video chunks for pedagogical events (e.g., whiteboard usage, slide transitions).
- **NLP & LLM Evaluation:** Evaluating the transcripts and visual events against pedagogical frameworks to generate coaching insights.

### Tier 4: Analytics & Web Dashboard

- **Backend:** Central FastAPI serving aggregated data.
- **Database:** PostgreSQL for relational data, RBAC, and metrics.
- **Frontend:** Next.js (React) providing dashboards for administrators and teachers.

## 3. Technology Stack Evaluation

### Backend API

- **Selection:** Python (FastAPI).
- **Rationale:** Unmatched ecosystem for ML/AI integration. Excellent concurrency with `asyncio`.

### AI/ML Pipeline

- **ASR:** `faster-whisper` (CTranslate2).
- **Audio/Video Manipulation:** `FFmpeg`.
- **Worker Framework:** Custom Python background workers pulling from Redis queues. (Celery deemed too heavy for MVP).

### Databases

- **Relational:** PostgreSQL (via `psycopg2`).
- **Object Storage:** MinIO.
- **In-Memory/Queue:** Redis.

### Frontend

- **Selection:** Next.js + Tailwind CSS.
- **Rationale:** SSR capabilities, vast enterprise ecosystem, rapid development.

### Infrastructure

- **MVP:** Docker Compose on a single GPU-enabled host (e.g., RTX 5070).
- **Production:** Kubernetes on AWS (ap-south-1) or GCP, utilizing horizontal pod autoscaling based on GPU queue depth.

## 4. Scalability Strategy

1. **Decoupled Ingest:** By separating the API ingest from the ML inference via a message broker (Redis), a flood of 3:00 PM uploads will not crash the heavy GPU workers.
2. **Chunked Processing:** Processing 5-minute chunks in parallel across multiple worker nodes rather than waiting for an entire 1-hour video to process sequentially.
3. **Stateless Workers:** ML worker nodes hold no state, allowing them to be spun up or destroyed dynamically based on load.

## 5. Security & Privacy Architecture

1. **Zero Trust API:** All endpoints secured. Raw media access is restricted via presigned URLs.
2. **Data Minimization:** Designing pipelines to extract metadata (transcripts, event tags) and eventually purge the raw video files to comply with DPDP/GDPR.
3. **No Biometric Surveillance:** Explicit architectural decision to avoid student facial recognition, focusing instead on teacher audio and aggregate room dynamics.

## 6. Observability Stack

- **Metrics:** Prometheus + Grafana.
- **Logging:** Structured JSON logging (Fluentd/Loki).
- **Tracing:** OpenTelemetry across the API and worker boundaries to diagnose latency in the ML pipeline.

## 7. Risks & Tradeoffs

- **Bandwidth Dependency:** Relying on cloud inference means schools with zero internet cannot use the full system immediately. Edge AI (running small models on the DAT host) is deferred to Phase 2.
- **Cost Scaling:** GPU inference is expensive. We must rigorously batch requests and explore model quantization (INT8) to keep the per-teacher cost viable for the Indian market.
