# Enterprise Stack Evaluation & Architecture Analysis

**Status:** Draft v1.0
**Date:** 2026-05-24
**Owner:** Principal Systems Engineer

This document provides a rigorous evaluation of the technology stack choices for PedagogyX, optimizing for the unique constraints of the project: D-PROC=C (Hybrid Edge-Cloud), RTX 5070 GPU budget, ₹0 customer hardware cost, and real-time/near-real-time latency targets.

## 1. Backend Stack

### Go (Golang) vs. Python vs. Rust vs. Node.js

- **Python (Winner for ML Integration):** Python is mandatory for the AI workers (`worker-asr`, multimodal fusion) due to the PyTorch ecosystem. Using Python (FastAPI/Litestar) for the core API reduces cognitive load and allows seamless code sharing between the API and ML workers.
- **Go (Strong Contender for API):** Unmatched for high-concurrency, low-latency streaming endpoints (handling thousands of inbound video chunks). However, maintaining two separate ecosystems (Go for API, Python for ML) increases complexity for a small early team.
- **Rust:** Unbeatable for safety and performance, but the compilation times and steep learning curve will kill execution velocity in Phase 1.
- **Node.js:** Excellent for I/O bound tasks, but weaker in CPU-heavy or native ML integration compared to Python/Go.

_Architecture Decision:_ **Python (FastAPI)** for the primary API to maintain ecosystem velocity with the ML stack, utilizing `asyncio` for concurrent chunk ingestion. We will evaluate migrating specific high-throughput ingestion endpoints to Go if Python becomes a bottleneck in Sprint 06+.

## 2. AI/ML Inference Pipeline

### PyTorch vs. TensorRT vs. ONNX Runtime

- **PyTorch (Native):** Great for research and training, but highly inefficient for production inference on a 12GB RTX 5070.
- **ONNX Runtime:** Good cross-platform compatibility, but often misses hardware-specific optimizations.
- **TensorRT (Winner for Vision):** Essential for maximizing throughput on NVIDIA GPUs. We must export YOLO/CNN models to TensorRT engines to meet the latency requirements on the RTX 5070.
- **faster-whisper (CTranslate2):** For ASR, `faster-whisper` (which uses CTranslate2) is significantly faster and uses less VRAM than native HuggingFace transformers, making it the definitive choice for the audio pipeline.
- **vLLM / Ollama:** For LLM serving, vLLM offers the highest throughput via PagedAttention, but Ollama provides a simpler developer experience for local testing. We will use vLLM in production and Ollama for local dev.

## 3. Video Pipeline & Ingestion

### HLS/DASH vs. WebRTC vs. Chunked HTTPS

- **WebRTC:** Required for true sub-second real-time coaching. However, it is notoriously complex to scale, traverse NATs (TURN servers), and record reliably.
- **Chunked HTTPS (Winner for Phase 1):** The Android DAT app buffers video from the Ray-Ban glasses and uploads discrete chunks (e.g., 5-second MP4s) via HTTPS POST. This is highly resilient to dropouts in poor Indian classroom networks and drastically simplifies the backend (stateless API).
- **Processing:** `FFmpeg` will be used to extract audio tracks from the chunks before sending them to the ASR worker.

## 4. Databases & Storage

### PostgreSQL vs. Vector DBs vs. Graph DBs

- **PostgreSQL (Winner for Relational Data):** Essential for RBAC, user management, session metadata, and rubric scores.
- **MinIO / S3 (Winner for Object Storage):** Required for storing the raw video chunks, extracted audio, and generated timeline JSONs.
- **Vector DB (Qdrant/Milvus):** Required later for RAG (Retrieval-Augmented Generation) when querying past lessons for long-term pedagogical coaching. We will defer this until Phase 2 and rely on structured JSON/SQL queries for Phase 1.

## 5. Frontend & Admin Shell

### Next.js vs. React (SPA)

- **Next.js (Winner):** Provides Server-Side Rendering (SSR) for the Admin Dashboard, improving perceived performance on low-end school admin computers. Excellent API route integration for backend-for-frontend (BFF) patterns.

## 6. Infrastructure & Deployment

### Kubernetes vs. Docker Compose vs. Nomad

- **Docker Compose (Winner for Phase 1):** As specified in the constraints, the pilot stack runs on a founder machine/local environment using `compose.dev.yaml`.
- **Kubernetes (Deferred):** K8s is the enterprise standard, but it is massive overkill for a Phase 1 pilot running on a single RTX 5070 machine. We will design the architecture as containerized microservices to allow easy migration to K8s later.

## 7. Cloud vs. Edge

- **Hybrid (D-PROC=C):** The Meta Ray-Ban glasses + Android app act purely as a capture and buffering edge layer. All heavy ML processing occurs centrally on the founder-funded RTX 5070 cluster. This drastically reduces the requirements on the customer's hardware, aligning with the ₹0 budget constraint.

---

_End of Stack Evaluation._
