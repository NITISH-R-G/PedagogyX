# System Architecture Report

## Overview

This document outlines the distributed system architecture for PedagogyX, moving from a conceptual hybrid edge/cloud model to concrete component mapping based on the current repository structure.

## Document History

- **Version:** v1.0
- **Author:** Autonomous Principal Research Architect
- **Date:** 2026-05-24

## 1. High-Level Architecture Topology

PedagogyX utilizes a Hybrid Edge/Cloud topology (ADR-0008).

### 1.1 Edge Tier (School LAN)

- **Capture Client:** Meta Ray-Ban smart glasses streaming to the Android DAT host app (`clients/android-capture-dat`).
- **Edge Buffer/Gateway:** A local device or lightweight server receiving the DAT stream over local WiFi, buffering it to handle intermittent internet connectivity.
- **Local Inference (Optional/Future):** RTX 5070 (12GB VRAM) for real-time, low-latency audio processing or lightweight video clipping before pushing to the cloud.

### 1.2 Cloud Tier (`ap-south-1`)

- **API Gateway & Core Logic:** FastAPI (`services/api`) handling routing, authentication, and session management (`/v1/dat-sessions`).
- **Frontend Dashboard:** Next.js and React (`services/web`) serving the analytics and pedagogical insights to school administrators.
- **Asynchronous Processing Workers:**
  - `services/worker-asr`: Handles heavy Automatic Speech Recognition tasks (e.g., Hindi/English transcription) offloaded from the edge.
  - `services/worker-cv`: Handles Computer Vision tasks (e.g., whiteboard OCR, activity recognition) on buffered video frames.
  - `services/worker-metrics`: Aggregates outputs from ASR and CV to generate pedagogical scores (M-A, M-B, M-C).

## 2. Data Flow (Happy Path)

1. **Capture:** Teacher wears Meta Ray-Bans. Video/Audio is streamed to the Android DAT app.
2. **Ingest:** Android app sends the `StreamSession` data to the Edge Buffer via local network.
3. **Transmission:** Edge Buffer securely uploads the data payload to the cloud API (`services/api`).
4. **Queueing:** API persists raw data (or pointers to object storage) and publishes events to a message broker (e.g., Redis).
5. **Processing:**
   - `worker-asr` consumes audio events, generates transcripts, and stores them.
   - `worker-cv` consumes video events, generates frame embeddings/classifications, and stores them.
6. **Aggregation:** `worker-metrics` consumes completion events from ASR/CV, calculates pedagogical scores, and updates the database.
7. **Delivery:** Administrator logs into the `services/web` Next.js dashboard to view the synthesized reports.

## 3. Known Constraints and Risks

- **Network Reliability:** The edge buffer is critical. If the school LAN fails, the Android DAT app must gracefully buffer locally without losing data or killing the glasses' battery.
- **Hardware Limits:** Any processing pushed to the edge must strictly adhere to the 12GB VRAM limit of the RTX 5070.
- **Compliance:** All cloud components must be deployed in India (`ap-south-1`) to comply with DPDP requirements for the Year 1 pilot.

## 4. Next Steps

- Finalize the event schema for communication between `api` and the `worker-*` microservices.
- Determine the exact queuing technology (e.g., Redis Streams, RabbitMQ) to be implemented in the boilerplate.

EOF
