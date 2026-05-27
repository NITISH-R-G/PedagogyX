# World-Class Enterprise Architecture: PedagogyX

## Overview

This document defines the elite, scalable, and privacy-preserving architecture for PedagogyX. It is designed to support the Phase 1 deployment utilizing Meta Ray-Ban smart glasses (via Android DAT companion app) as the primary edge capture device, streaming to a hybrid cloud-edge ML pipeline.

---

## 1. High-Level System Topology

PedagogyX employs a **Hybrid Edge-Cloud Architecture (D-PROC=C)**.

1.  **Tier 1: Intelligent Edge (Capture)**
    - **Hardware:** Meta Ray-Ban Smart Glasses + Android Host Device.
    - **Responsibilities:** Media capture, Bluetooth (DAT) routing, chunking, local encryption, network resilience buffer.
2.  **Tier 2: Ingestion & Routing (Cloud API)**
    - **Hardware:** Kubernetes/Docker Swarm clusters (AWS `ap-south-1` or equivalent).
    - **Responsibilities:** Authentication (JWT/API Keys), WebRTC termination, payload ingestion, event streaming (Kafka/Redis).
3.  **Tier 3: Multimodal ML Inference (GPU Pool)**
    - **Hardware:** Distributed GPU cluster (e.g., RTX 5070 pool per ADR-0006).
    - **Responsibilities:** ASR, Computer Vision (pose, gaze), NLP/LLM pedagogical classification.
4.  **Tier 4: Persistence & Analytics (Data Layer)**
    - **Hardware:** Managed Postgres, Object Storage (MinIO/S3), Vector Database.
    - **Responsibilities:** Relational metadata, raw/processed video storage, embedding storage for longitudinal search.
5.  **Tier 5: Presentation (Admin/Teacher Web Shell)**
    - **Hardware:** Next.js Server-Side Rendered application.
    - **Responsibilities:** Real-time dashboards, historical analytics, video playback with synchronized transcripts.

---

## 2. System Diagrams

### 2.1 Core Dataflow & Event Pipeline

```mermaid
flowchart TD
    subgraph Edge [Edge: Classroom]
        G[Ray-Ban Glasses] -->|Bluetooth DAT| A[Android Host App]
        A -->|HTTPS Chunks / WebRTC| API_GW
    end

    subgraph Ingestion [Ingestion & API]
        API_GW[FastAPI Gateway] -->|Video Chunks| OS[(MinIO/S3)]
        API_GW -->|Session Metadata| DB[(PostgreSQL)]
        API_GW -->|Enqueue Job| Q[Redis Queue]
    end

    subgraph ML_Pipeline [GPU Workers]
        Q --> W_ASR[worker-asr: Whisper]
        Q --> W_CV[worker-cv: Pose/Gaze]
        Q --> W_NLP[worker-nlp: LLM Pedagogy]

        OS --> W_ASR
        OS --> W_CV

        W_ASR -->|Transcript| DB
        W_CV -->|Visual Events| DB
        W_ASR -->|Transcript| W_NLP
        W_CV -->|Context| W_NLP

        W_NLP -->|Pedagogy Index| DB
    end

    subgraph Presentation [Web Dashboard]
        UI[Next.js Admin Shell] -->|GraphQL/REST| API_GW
        API_GW --> DB
    end
```

### 2.2 Multimodal Inference Pipeline

The ML pipeline uses a late-fusion architecture to generate the final Pedagogy Index.

```mermaid
sequenceDiagram
    participant S3 as Storage
    participant ASR as Audio Pipeline (Whisper)
    participant CV as Vision Pipeline (YOLO/Pose)
    participant NLP as Text Pipeline (LLM)
    participant DB as Event Store

    S3->>ASR: Pull Audio Track
    ASR-->>DB: Save Transcript & Diarization
    S3->>CV: Pull Video Track
    CV-->>DB: Save Pose & Engagement Vectors

    ASR->>NLP: Trigger (Transcript Ready)
    CV->>NLP: Trigger (Vision Vectors Ready)

    Note over NLP: Multimodal Fusion Context
    NLP->>NLP: Apply Pedagogy Prompt Template
    NLP-->>DB: Save Computed Pedagogy Index & Evidence
```

---

## 3. Distributed Systems & Scalability Strategy

- **Stateless Ingestion:** The FastAPI edge nodes are entirely stateless. They receive chunks, write to object storage, and publish an event. They can scale horizontally infinitely based on CPU/Network IO.
- **Asynchronous ML Workers:** ML inference is decoupled from ingestion. If the GPU cluster is overwhelmed, jobs queue in Redis. The Android client is unaffected by backend processing delays.
- **Database Sharding:** PostgreSQL is designed for multi-tenant isolation. Initially, logical separation via `tenant_id` columns is used. Future scaling will employ physical sharding per school district.

## 4. Security & Privacy Architecture (India DPDP Compliant)

- **Zero-Trust Edge:** The Android host app requires short-lived JWTs. The API assumes the network is hostile.
- **Encryption at Rest & Transit:** TLS 1.3 for all transit. MinIO/S3 uses AES-256 server-side encryption. Database volumes are encrypted.
- **PII Segregation:** Audio transcripts and video files are treated as high-risk PII. Aggregate metrics (e.g., "30% teacher talk time") are treated as low-risk analytics.
- **Data Residency:** All infrastructure must be localized to the target region (e.g., `ap-south-1` for India) to comply with data sovereignty laws.

## 5. Deployment & Observability

- **Infrastructure as Code (IaC):** Terraform/Pulumi defines all cloud resources.
- **Containerization:** Docker for all services. Kubernetes/Nomad for orchestration.
- **Observability:**
  - **Metrics:** Prometheus scraping FastAPI and GPU workers.
  - **Logs:** Fluentd/Vector shipping to localized Elasticsearch/Loki.
  - **Tracing:** OpenTelemetry (OTel) spans across the Android client, API, and workers to identify latency bottlenecks in the ML pipeline.
