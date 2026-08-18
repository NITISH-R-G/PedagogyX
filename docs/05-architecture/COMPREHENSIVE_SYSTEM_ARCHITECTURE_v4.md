# Comprehensive System Architecture v4

**Date:** 2026-05-25
**Author:** Autonomous Principal Research Architect
**Status:** DRAFT
**Context:** System architecture detailing the hybrid edge/cloud model (ADR-0008) and the Meta Ray-Ban primary capture pivot (ADR-0009).

## 1. Executive Summary

This document outlines the v4 architecture for PedagogyX. Driven by founder constraints (free pilot, ₹0 customer budget) and technical mandates (max RTX 5070 12GB, strict OSS), the system utilizes a **Hybrid Edge/Cloud topology**. The primary capture mechanism is the Meta Ray-Ban smart glasses streaming to a Data Acquisition Terminal (DAT) running on an Android host device, which acts as the local edge buffer before transmitting to the cloud (ap-south-1).

## 2. High-Level Architecture Diagram

```mermaid
graph TD
    subgraph Edge: Classroom
        Glasses[Meta Ray-Ban Glasses] -->|Bluetooth/Wi-Fi Direct| DAT[Android DAT App]
        DAT -->|Local Buffer / Initial Pre-processing| LAN[School LAN]
    end

    subgraph Cloud: ap-south-1
        LAN -->|Secure Sync Protocol| API Gateway[API Gateway (FastAPI)]

        API Gateway --> Kafka[Event Stream (Kafka/Redis PubSub)]

        Kafka --> ASR_Worker[ASR Worker (Whisper/Faster-Whisper)]
        Kafka --> CV_Worker[CV Worker (YOLO/Object Detection)]
        Kafka --> Metrics_Worker[Metrics Aggregation Worker]

        ASR_Worker --> Fusion_Engine[Multimodal Fusion Engine]
        CV_Worker --> Fusion_Engine

        Fusion_Engine --> LLM_Inference[LLM Inference (Qwen2.5-7B-Q4)]

        LLM_Inference --> DB_Postgres[(PostgreSQL)]
        LLM_Inference --> DB_Vector[(Qdrant Vector Store)]

        DB_Postgres --> WebApp[Web Frontend (Next.js)]
        DB_Vector --> WebApp
    end

    style Glasses fill:#f9f,stroke:#333,stroke-width:2px
    style DAT fill:#bbf,stroke:#333,stroke-width:2px
    style LLM_Inference fill:#fbb,stroke:#333,stroke-width:2px
```

## 3. Component Deep Dive

### 3.1 Edge Tier (Data Acquisition Terminal - DAT)

- **Responsibility:** Reliable capture from Meta Ray-Ban, local buffering to mitigate network flakiness, and secure transmission to the cloud.
- **Hardware:** Android smartphone.
- **Software:** Custom DAT application.
- **Key Challenge:** Maintaining A/V sync from the Bluetooth/Wi-Fi Direct stream before sending it to the cloud. Must support a low-bandwidth degradation mode.

### 3.2 Ingestion & Streaming (Cloud)

- **API Gateway:** FastAPI-based entry point. Handles authentication (device tokens) and routes incoming data streams.
- **Event Bus:** Given the requirement for real-time coaching (<3s latency) and asynchronous processing, a robust message broker (Redis PubSub for MVP, migrating to Kafka for scale) is required to decouple ingestion from inference.

### 3.3 Worker Nodes (The 12GB VRAM Constraint)

- **ASR Worker:** Must support English and Hindi. Highly optimized models (e.g., Faster-Whisper) are required to fit within the memory budget alongside other models.
- **CV Worker:** Focuses on extracting pedagogical features from the POV stream (e.g., gaze estimation, detecting instructional materials like whiteboard text or slides).
- **Multimodal Fusion:** A crucial component (identified in our Literature Review) that temporally aligns the ASR transcripts with the CV events before sending them to the LLM.

### 3.4 Intelligence Layer

- **LLM Inference:** The core pedagogical reasoning engine. Constrained to RTX 5070 12GB. We must utilize heavily quantized, OSS models. **Qwen2.5-7B-Q4 (or similar)** is the current primary candidate for its balance of reasoning capability and memory footprint. It will generate the pedagogical assessments and real-time coaching prompts.

### 3.5 Storage Layer

- **Relational Database:** PostgreSQL for structured data (user accounts, rubrics, final assessment scores).
- **Vector Database:** Qdrant for storing embeddings of transcripts and assessment reports to enable semantic search and longitudinal analysis of teacher progress.

## 4. Operational Modes (Supervision vs. Coaching)

The architecture must support dynamic RBAC and data masking based on the operational mode:

- **Supervision Mode (Default India):** Unmasked video streams stored (where legally permitted) and full assessment dashboards available to school administration.
- **Coaching Mode:** Video streams may be processed ephemerally and discarded, or aggressively de-identified (blurring student faces). Assessment data is restricted primarily to the teacher and their designated coach.

## 5. Risks and Mitigation

- **Latency vs. Inference Cost:** Achieving <3s latency for real-time coaching on a single RTX 5070 while simultaneously running ASR, CV, and LLM inference is the highest technical risk.
- _Mitigation:_ Extreme quantization, model pruning, and potentially moving lightweight wake-word/basic ASR directly to the Android DAT device in Phase 2.
- **Data Residency & DPDP Compliance:**
- _Mitigation:_ Strict deployment to ap-south-1 only. End-to-end encryption from DAT to Cloud. Implementation blocked pending G2 legal sign-off.
