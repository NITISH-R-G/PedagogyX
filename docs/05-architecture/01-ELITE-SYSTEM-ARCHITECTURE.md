# Elite System Architecture

**Author:** Autonomous Principal Research Architect
**Phase:** 0
**Status:** In Progress

## Introduction

This document outlines the elite, world-class system architecture for PedagogyX, moving from edge capture to multimodal AI inference, designed to eventually rival DeepMind's applied systems.

## 1. High-Level Architecture Overview

The system employs a **Hybrid Edge-Cloud** architecture, specifically optimized for the constraints of the Meta Ray-Ban primary client and the target market (India).

### Core Components

1. **Edge Capture Node (Meta Ray-Ban + Android Host):**
   - Captures POV video and high-fidelity audio.
   - Android Host acts as a LAN buffer and performs initial pre-processing (e.g., audio normalization, privacy masking if edge compute allows).
2. **Ingest Gateway (Go-based):**
   - High-throughput, low-latency gateway designed to handle unreliable network connections.
   - Implements chunking and secure streaming protocols over WAN.
3. **Event Streaming Backbone:**
   - Handles asynchronous message passing (e.g., Kafka or Redis Streams) to decouple ingest from heavy AI processing.
4. **Multimodal Inference Pipeline (Python-based):**
   - Orchestrates the various ML models across available GPU resources.
5. **Data & Knowledge Layer:**
   - Relational DB (Postgres) for metadata and tenant isolation.
   - Vector DB (e.g., Qdrant/Milvus) for storing session embeddings for RAG-based coaching.

## 2. Multimodal AI Pipeline Design

### Phase 1 Processing (Audio-Centric)

- **ASR & Diarization:** Leveraging `faster-whisper` for transcription and speaker diarization to separate teacher voice from student noise.
- **NLP Analysis:** Passing transcripts through a specialized LLM (via Ollama) to evaluate pedagogical techniques (e.g., questioning strategies, clarity).

### Phase 2 Processing (Visual & Fusion)

- **Visual Parsing:** Analyzing video frames for slide content (OCR), whiteboard usage, and general classroom activity.
- **Multimodal Fusion:** Aligning the temporal timestamps of the transcript with the visual events to create a unified session timeline.
- **Affective Computing:** Analyzing speech emotion and visual cues to gauge teacher pacing and engagement.

## 3. Infrastructure & Scalability Strategy

- **GPU Scheduling Strategy:** Given the constraint of target RTX 5070 GPUs for the dev/pilot phase, we must implement a highly efficient batching and queuing system. The pipeline must scale horizontally across multiple consumer-grade GPUs rather than relying on massive enterprise clusters initially.
- **Storage:** Massive video files must be moved to object storage (e.g., MinIO/S3) immediately after ingestion, with only necessary metadata and chunks processed by the GPU workers.
- **Tenant Isolation:** Ensure strict logical isolation of data within the database to comply with privacy requirements and build trust with institutional clients.

## 4. Risks & Unknowns

- **Edge Compute Limits:** The ability of the Android host to perform any meaningful pre-processing before battery/thermal limits are reached is an unknown that requires empirical testing.
- **Multimodal Alignment Latency:** Synchronizing audio transcripts with visual data reliably without introducing massive processing latency.
- **Network Reliability:** Continuous streaming of HD video from rural/semi-urban Indian classrooms is highly risky; robust offline buffering and resume capabilities are critical.

## 5. Security & Privacy Architecture

- **Data Residency:** All cloud infrastructure deployed within India to comply with DPDP.
- **Encryption:** End-to-end encryption in transit (TLS 1.3) and AES-256 at rest for all media files.
- **Anonymization Strategy:** Immediate deletion of raw video streams after feature extraction (pose, text) if longitudinal video playback is not explicitly required by the school contract.

---

_End of Architecture Document._
