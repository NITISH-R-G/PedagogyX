# World-Class System Design & Architecture Report

**Status:** Draft v1.0
**Owner:** PedagogyX System Design Architect

This document outlines the elite, highly scalable, and privacy-preserving hybrid edge-cloud architecture designed for PedagogyX. It dictates the topological layout from raw capture on Meta Ray-Ban glasses to the final generation of the AI Pedagogy Index on central GPU clusters.

---

## 1. High-Level Architectural Topology (D-PROC Hybrid)

The system utilizes a **Hybrid Edge-Cloud (Tiered)** architecture to balance network constraints in rural/tier-2 Indian schools with the massive compute required for multimodal AI inference.

### Tier 1: The Edge (Capture & Ingest)

- **Primary Hardware:** Meta Ray-Ban Smart Glasses (POV capture) connected via Bluetooth to a low-end Android device (DAT Host).
- **Secondary Hardware (Phase 1b):** Fixed Windows/Android smartboards acting as room-scale cameras.
- **Edge Responsibilities:**
  - Secure device authentication (mTLS / API Keys via `HTTPBearer`).
  - Local buffering (handling intermittent school Wi-Fi drops).
  - Chunking video/audio into manageable payloads (e.g., 5-minute segments).
  - _Future:_ Lightweight on-device Voice Activity Detection (VAD) to prevent uploading empty silence.

### Tier 2: The Ingestion Gateway (Cloud Entrypoint)

- **Infrastructure:** Load-balanced FastAPI endpoints hosted in an India-based cloud region (DPDP compliance).
- **Responsibilities:**
  - Terminate TLS.
  - Validate auth tokens.
  - Stream chunks directly into Object Storage (MinIO) to prevent memory exhaustion on API nodes.
  - Publish "Chunk Received" events to the Message Broker (Redis).

### Tier 3: The Cold Path (Asynchronous ML Inference)

- **Infrastructure:** Scalable fleet of Python worker nodes equipped with NVIDIA RTX 5070s.
- **Responsibilities:**
  - **Worker-ASR:** Dequeue audio tasks, run Whisper (or fine-tuned regional model), diarize speakers, and generate timestamped VTT transcripts.
  - **Worker-CV:** Dequeue video tasks, run YOLO/SCB-DETR via ONNX/TensorRT for engagement tracking, object detection (whiteboards), and head-pose estimation.
  - **Worker-Pedagogy:** A distinct orchestration node that waits for ASR and CV tasks for a specific session to complete, fuses the data, and prompts the LLM (e.g., Qwen2.5) for the pedagogical score and coaching narrative.

### Tier 4: Storage & State

- **Object Storage (MinIO):** Holds raw video chunks, assembled master videos, and generated audio files.
- **Relational Database (PostgreSQL):** Stores users, schools, RBAC policies, session metadata, generated transcripts (structured), and final scores. Interacted via synchronous `psycopg2` within FastAPI threadpools.
- **Vector Database (Qdrant - Future):** Stores embeddings of transcripts and coaching advice for semantic RAG search across a teacher's longitudinal history.

---

## 2. Event Pipeline & Dataflow Diagram

```text
[Meta Ray-Ban] --(BT)--> [Android DAT App]
                               |
                               | (HTTPS / Chunked Upload)
                               v
                     [FastAPI Ingest Gateway]
                               |
          +--------------------+--------------------+
          | (Save to Disk)                          | (Publish Event)
          v                                         v
   [MinIO Object Store]                       [Redis Queue]
          |                                         |
          | (Read Chunk)                            | (Dequeue Task)
          +--------------------+--------------------+
                               |
                               v
                     [GPU Worker Nodes]
                    /                  \
            [Worker-ASR]             [Worker-CV]
                 |                        |
                 +----------+-------------+
                            |
                            v
                   [Worker-Pedagogy / LLM]
                            |
                            v
                      [PostgreSQL DB]
                            |
                            v
                   [Next.js Admin Dashboard]
```

---

## 3. Distributed Systems & Scalability Strategy

1.  **Stateless API Tier:** The FastAPI ingestion nodes hold zero state. They can be horizontally auto-scaled based on CPU utilization or incoming request rate using Kubernetes HPA (Horizontal Pod Autoscaler).
2.  **Decoupled Compute (Queue-Driven):** By pushing inference to a Redis queue, a 3:00 PM spike in uploads from 1,000 classrooms will not crash the system. It simply increases queue depth. The SLA dictates how fast the GPU cluster must drain this queue (e.g., within 4 hours).
3.  **GPU Scheduling Efficiency:**
    - CV models (YOLO) will utilize `stream=True` and strict batching to maximize memory bandwidth on the RTX 5070s.
    - ASR and CV pipelines run on separate worker pools to prevent GPU memory fragmentation caused by constantly swapping model weights.

---

## 4. Security & Privacy Architecture (India DPDP)

1.  **Data Residency:** Entire infrastructure deployed in an India region (e.g., AWS `ap-south-1` or equivalent local provider).
2.  **Encryption:** TLS 1.3 in transit. MinIO configured with SSE-C (Server-Side Encryption with Customer-provided keys) or KMS.
3.  **Authentication:** MVP relies on `HTTPBearer` API keys. Production will migrate to short-lived JWTs managed by a central identity provider, mapping strictly to School/District RBAC roles.
4.  **Least Privilege Execution:** Worker nodes run as non-root containers. Database credentials are injected at runtime and default to `None` in Pydantic settings to prevent accidental commits.

---

## 5. Observability Stack

- **Metrics:** Prometheus scraping FastAPI endpoints, Redis queue depths, and GPU utilization metrics (via `dcgm-exporter`).
- **Logs:** Structured JSON logging across all Python services (API and Workers), aggregated centrally.
- **Exception Handling (Code Health):** Strict ban on `except Exception: pass`. All worker failures must log tracebacks to `sys.stderr` and fail the queue job, moving it to a Dead Letter Queue (DLQ) for human debugging.
