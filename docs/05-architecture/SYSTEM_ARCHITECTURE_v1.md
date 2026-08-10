# SYSTEM ARCHITECTURE: PEDAGOGYX PLATFORM

**Document Status:** DRAFT
**Date:** 2024-03-XX
**Author:** Autonomous Principal Research Architect & Lead Systems Engineer
**Classification:** INTERNAL ONLY

## 1. High-Level Architecture Overview

PedagogyX is a distributed, edge-to-cloud multimodal AI platform designed to ingest, synchronize, and analyze classroom data (audio, video, context). The architecture prioritizes **Privacy-by-Design**, **Offline Resilience**, and **Cost-Optimized Inference**.

### 1.1 The Three-Tier Architecture

1.  **The Edge Tier (Classroom Capture):**
    - **Primary Client:** Meta Ray-Ban Smart Glasses (via DAT - Android).
    - **Fallback Client:** Standard mobile device or classroom IP camera.
    - **Responsibilities:** Media capture, local VAD (Voice Activity Detection), edge-blurring of PII (if legally required), data chunking, and secure transmission.
2.  **The Ingestion & Stream Tier (The Bridge):**
    - **Components:** API Gateway, Event Streaming Platform (Kafka/Redpanda).
    - **Responsibilities:** Terminate TLS, authenticate devices, buffer incoming media chunks, and route events to processing workers. Handles network instability via resumable uploads.
3.  **The Cloud Intelligence Tier (The Brain):**
    - **Components:** Worker pods (ASR, CV, NLP), Vector Databases, Knowledge Graphs, and Core API.
    - **Responsibilities:** Multimodal fusion, transcription, pedagogical analysis, long-term memory storage, and serving the frontend dashboard.

---

## 2. Detailed Data Flow & Pipelines

### 2.1 The Ingestion Pipeline (Device to Cloud)

- **Capture:** The DAT app on Android connects to the Ray-Bans. It captures video and audio, chunking them into 1-minute segments.
- **Upload:** Chunks are uploaded via secure, resumable HTTPS POST to an S3-compatible object store (e.g., MinIO for on-prem/local dev, AWS S3 for prod).
- **Event Generation:** Upon successful upload of a chunk, the storage layer triggers an event to Redpanda/Kafka: `ChunkUploadedEvent(session_id, chunk_id, object_url)`.

### 2.2 The ML Inference Pipeline

- **Worker-ASR:** Listens for `ChunkUploadedEvent`. Downloads audio, runs Voice Activity Detection (Silero VAD), performs diarization (Pyannote), and transcribes (WhisperX). Outputs timestamped transcript JSON.
- **Worker-CV (Future Phase):** Listens for `ChunkUploadedEvent`. Samples frames, runs pose estimation/object detection, and generates visual semantic embeddings.
- **Worker-Fusion:** Aggregates ASR and CV outputs. Cross-references timestamps. Uses an LLM (via API or local vLLM instance) to analyze the 1-minute context against pedagogical rubrics.
- **Vectorization:** Embeddings of the transcript and analysis are stored in a Vector DB (Qdrant) for longitudinal RAG.

---

## 3. Storage & Database Architecture

- **Relational Database (PostgreSQL):** Stores users, schools, permissions (RBAC), session metadata, and final aggregated scoring metrics.
- **Object Storage (S3/MinIO):** Stores raw video/audio chunks and generated assets (highlight reels, reports). Strict lifecycle policies (e.g., delete raw video after 30 days) apply here.
- **Vector Database (Qdrant):** Stores embedding vectors of classroom dialogue and insights. Crucial for the AI coaching agent to "remember" past sessions.
- **Cache/State (Redis):** Manages session states, rate limiting, and temporary processing locks.

---

## 4. Scalability & Resilience Strategy

- **Asynchronous Processing:** By decoupling ingestion from inference via Kafka, a massive spike in classroom uploads at 9:00 AM will merely increase the queue length, not crash the API.
- **Autoscaling Workers:** Kubernetes Horizontal Pod Autoscaler (HPA) will scale ML worker pods based on Kafka lag.
- **GPU Cost Optimization:** We will separate CPU-bound tasks (routing, basic NLP) from GPU-bound tasks (Whisper inference). We will utilize spot instances or specialized GPU cloud providers (e.g., RunPod) for the heavy lifting.

---

## 5. Security & Compliance Architecture

- **Data Residency:** For the India G2 pilot, all infrastructure (API, DBs, Storage) will be deployed in the `ap-south-1` region to comply with DPDP.
- **Encryption:** Data is encrypted at rest (AES-256) and in transit (TLS 1.3).
- **PII Destruction:** If strict privacy is mandated, the ML pipeline can be configured to transcribe the audio and immediately permanently delete the raw media file, storing only the anonymized text and metadata.
- **Tenant Isolation:** Row-level security (RLS) in PostgreSQL ensures a user in School District A cannot query data from School District B.
