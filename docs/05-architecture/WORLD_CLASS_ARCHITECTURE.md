# World-Class Architecture for PedagogyX

**Status:** Research Phase 0 Active
**Date:** 2026-05-26
**Owner:** Principal Research Architect (Jules)
**Target:** D-PROC Hybrid Edge-Cloud (Central OSS Inference) via Ray-Ban DAT

This document outlines the elite, highly scalable, and privacy-preserving distributed systems architecture for PedagogyX. It synthesizes constraints from our founder interrogation, global competitor weaknesses, and limitations identified in current scientific literature.

---

## 1. High-Level Architectural Topology

We are deploying a **D-PROC (Distributed Processing, Central Inference)** architecture. The edge (Android Phone + Ray-Bans) handles raw capture, initial chunking, and upload. The core intelligence resides in a self-hosted central API and GPU worker farm.

```mermaid
flowchart TD
    subgraph Edge [Teacher Edge (Classroom)]
        RB[Ray-Ban Meta Glasses] -- DAT Bluetooth/Wi-Fi --> AND[Android DAT Companion App]
        AND -- "Chunked Encrypted Upload (HTTPS)" --> API_GW[API Gateway / Load Balancer]
        AND -- "Real-Time Telemetry" --> API_GW
    end

    subgraph ControlPlane [Central Cloud (ap-south-1)]
        API_GW --> API[PedagogyX Core API (Go/FastAPI)]
        API --> DB[(PostgreSQL + pgvector)]
        API --> MINIO[(MinIO Object Store)]
        API -- "Queue (RabbitMQ/Kafka)" --> WORKER_Q[Job Queue]
    end

    subgraph InferencePlane [GPU Compute Farm (RTX 5070 Cluster)]
        WORKER_Q --> ASR[Worker: Whisper ASR]
        WORKER_Q --> CV[Worker: YOLO/Pose CV]
        WORKER_Q --> LLM[Worker: Ollama Agent]

        MINIO -- "Pull Chunks" --> ASR
        MINIO -- "Pull Chunks" --> CV

        ASR -- "Transcripts/JSON" --> DB
        CV -- "Event Timelines/JSON" --> DB

        DB -- "RAG Context" --> LLM
        LLM -- "Pedagogical Scoring" --> DB
    end
```

## 2. The Multimodal Event Pipeline (Cold Path)

Given the hardware constraints (RTX 5070s) and research findings against massive raw multimodal transformers, we utilize a **Late-Fusion Event Pipeline**:

1.  **Ingestion & Chunking**: The Android app splits the continuous DAT stream into 2-minute encrypted chunks. If network fails, chunks spool to local storage.
2.  **Parallel Extraction (Layer 1)**:
    - **Audio Queue**: WhisperX processes audio chunks, producing highly accurate, timestamped, diarized transcripts (Speaker 0: Teacher, Speaker 1: Student).
    - **Vision Queue**: YOLOv8-Pose samples video chunks at 1 FPS, extracting bounding boxes, orientation vectors, and slide/whiteboard transitions, discarding raw PII imagery immediately.
3.  **Semantic Structuring (Layer 2)**: Both outputs are written to the database as discrete JSON events (e.g., `{"timestamp": 120, "type": "teacher_question", "text": "What is the capital?"}`).
4.  **LLM Reasoning (Layer 3)**: Ollama loads the structured JSON timeline into context. We prompt the LLM against specific pedagogical rubrics (e.g., "Analyze the wait-time after teacher questions in this timeline").

## 3. Distributed Systems & Scalability Strategy

To rival enterprise SaaS architectures (Edthena, Vosaic) at a fraction of the cost:

- **Asynchronous Processing**: The API is entirely decoupled from inference. Teachers upload sessions, which enter a "Processing" state. Webhooks/SSE notify the client upon completion.
- **Idempotent Workers**: GPU workers pull jobs, process chunks, and write results. If an RTX node crashes mid-chunk, the job times out and is requeued.
- **Storage Tiering**: Raw video chunks are held in fast SSD-backed MinIO for 7 days (for human review if flagged). After 7 days, raw video is purged to comply with DPDP data minimization rules, retaining only the structured JSON metadata and LLM-generated coaching feedback.

## 4. Security, Privacy, and India DPDP Compliance

To deploy in Indian K-12 systems (our primary GTM):

- **Zero PII Persistence**: The CV pipeline extracts skeletal poses and broad classifications (e.g., "Student raising hand"). Facial recognition vectors are strictly disabled.
- **Role-Based Access Control (RBAC)**:
  - _Teacher Role_: Full access to personal session videos, raw transcripts, and AI coaching.
  - _Admin/Supervision Role_: Access limited to aggregate statistics (e.g., average wait time across department) unless the teacher explicitly initiates a "Share for Review" workflow.
- **Encryption**: TLS 1.3 in transit. AES-256 for MinIO objects at rest.

## 5. Deployment Infrastructure (Infrastructure-as-Code)

- **Local/Founder Dev**: Docker Compose orchestrating mocked DAT APIs, a single mock GPU worker, and Postgres.
- **Production Deployment**:
  - Control Plane: Managed Kubernetes (EKS/AKS) or Nomad for lightweight API/Queue orchestration.
  - GPU Plane: Auto-scaling group of bare-metal or cost-optimized cloud instances equipped with RTX 5070 equivalents, heavily leveraging TensorRT for inference optimization.

## 6. Risks & Unknowns (Requires Prototyping)

1.  **DAT Upload Reliability**: Sustaining chunked uploads from a background Android service during active movement in a school network with deep packet inspection.
2.  **GPU Scheduler Thrashing**: Context switching between Whisper, YOLO, and Ollama on a single 12GB VRAM card is inefficient. We must architect dedicated node groups (e.g., Node A only runs Whisper, Node B only runs Ollama) to maximize VRAM utilization.
