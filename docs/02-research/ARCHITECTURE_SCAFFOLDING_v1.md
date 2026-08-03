# PedagogyX: Architecture Scaffolding & System Design

**Author:** Autonomous Principal Research Architect & Lead Systems Engineer
**Date:** 2024
**Status:** DRAFT (Under Evaluation)
**Classification:** HIGHLY CONFIDENTIAL / PROPRIETARY

## Executive Summary

This document outlines the preliminary architecture scaffolding for PedagogyX. Based on the findings in our tech stack and competitive analysis, this architecture emphasizes a hybrid edge/cloud model. This ensures low latency, reduces cloud egress and GPU costs, and rigorously adheres to privacy regulations by processing sensitive multimodal data locally whenever possible.

---

## 1. High-Level System Architecture

### 1.1 The Edge (Classroom Level)

- **Ingestion Hardware:** Dedicated 360-degree cameras and microphone arrays (or wearables like Meta Ray-Bans).
- **Edge Processing Node:** A localized compute unit (e.g., NVIDIA Jetson or a high-end local PC running K3s/Docker).
  - _Responsibilities:_
    - Video/Audio Demuxing (FFmpeg).
    - Local ML Inference (ONNX/TensorRT): Speech-to-text (Whisper), basic pose estimation (YOLO), voice activity detection.
    - Data Anonymization: Stripping raw video feeds before transmitting metadata.
- **Outbound Pipeline:** Secure, encrypted transmission of text transcripts, semantic embeddings, and behavioral telemetry to the cloud via WebSockets/gRPC.

### 1.2 The Cloud (Central Platform)

- **API Gateway:** Node.js/Go based gateway for routing traffic, handling authentication, and managing rate limits.
- **Core Microservices (Python/FastAPI):**
  - _Ingestion Service:_ Receives telemetry and transcripts from edge nodes.
  - _Multimodal Fusion Service:_ Aligns transcripts with OCR data and engagement metrics on a unified timeline.
  - _Pedagogical Engine:_ LLM-driven service (backed by LangChain/LlamaIndex) that queries the educational knowledge graph to score pedagogical efficiency.
- **Asynchronous Workers (Celery/Redis):** Handle long-running post-processing tasks, batch reporting, and email notifications.

---

## 2. Data & Storage Architecture

### 2.1 The Data Tier

- **Primary Relational DB (PostgreSQL):** Stores users, schools, roles, authentication states, and high-level lesson metadata.
- **Vector DB (Qdrant):** Stores embeddings of transcripts, pedagogical concepts, and historical teacher feedback for RAG (Retrieval-Augmented Generation) pipelines.
- **Telemetry Store (ClickHouse):** Stores high-frequency, time-series data such as engagement scores measured at 5-second intervals.
- **Object Storage (S3 API):** For storing processed assets (e.g., anonymized highlight clips, slide PDFs).

---

## 3. Multimodal Inference Pipeline

The intelligence of PedagogyX relies on synthesizing multiple data streams into a cohesive understanding of a lesson.

1. **Audio Stream:**
   - -> VAD (Voice Activity Detection) -> Whisper (Transcription) -> Speaker Diarization -> Sentiment/Pacing Analysis.
2. **Video Stream:**
   - -> Frame Extraction -> YOLO (Pose/Engagement Detection) -> Anonymization/Blurring.
3. **Screen/Board Stream:**
   - -> OCR Engine -> Semantic Extraction -> Alignment with Audio Transcript.
4. **Fusion & Reasoning:**
   - Temporal alignment of all streams -> Pedagogical Knowledge Graph Query -> Generation of Teacher Insights.

---

## 4. Security & Observability

### 4.1 Security

- **Zero Trust:** All intra-service communication authenticated via mTLS.
- **RBAC:** Strict PostgreSQL-enforced role-based access control ensuring teachers only see their data, and admins see aggregated, non-identifying metrics unless explicitly authorized.

### 4.2 Observability

- **Metrics:** Prometheus gathering hardware and application-level metrics.
- **Logs:** Fluent Bit shipping structured JSON logs to OpenSearch.
- **Traces:** OpenTelemetry (OTel) for distributed tracing across edge and cloud microservices.

---

**Next Steps:**
This architecture is contingent upon the Founder's responses regarding acceptable cloud costs, offline requirements, and specific hardware partnerships (e.g., Meta Ray-Bans). Detailed sequence diagrams and infrastructure-as-code (Terraform) modules will be drafted once the Phase 0 requirements are finalized.
