# Exhaustive Tech Stack Evaluation & Comparison

**Status:** Draft v1.0
**Owner:** PedagogyX Lead Systems Engineer

This document provides a rigorous evaluation of potential technology stacks for the PedagogyX platform, adhering to the project mandates: OSS-first, self-hosted, central inference servers (India-based cloud), and a primary focus on Meta Ray-Ban glasses via Android companion app (DAT).

---

## 1. Backend Language & Framework

**Requirements:** High concurrency for ingestion (Hot Path), smooth integration with ML pipelines (Cold Path), low latency, and maintainability.

| Language / Framework   | Concurrency / Latency                                              | ML Integration (PyTorch/ONNX)                                        | Maintainability & Hiring                                 | Verdict                                         |
| :--------------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------- | :------------------------------------------------------- | :---------------------------------------------- |
| **Go** (Fiber/Gin)     | Excellent. Goroutines handle massive concurrent WebSockets easily. | Poor. Requires CGO bindings to C++ ML libs; clunky.                  | Very Good. Easy to read, strong standard library.        | **Candidate (Ingestion Gateway Only)**          |
| **Rust** (Axum)        | Best-in-class latency and memory safety.                           | Fair. `tch-rs` exists but ecosystem is immature compared to Python.  | Difficult. High learning curve, slower feature velocity. | **Rejected** (Too slow for early stage MVP)     |
| **Python** (FastAPI)   | Moderate. Asyncio is good, but GIL limits true parallelism.        | **Best-in-class.** Native integration with PyTorch, HF, Ultralytics. | Excellent. Massive ecosystem, easy hiring.               | **Selected (Core API & Workers)**               |
| **Node.js** (NestJS)   | Good for I/O bound tasks.                                          | Poor. Python must run as separate microservices.                     | Good. Ubiquitous.                                        | **Rejected** (Disconnects API from ML logic)    |
| **Java** (Spring Boot) | Excellent (Virtual Threads in JDK 21+).                            | Poor. DJL exists but cumbersome.                                     | Good. Enterprise standard.                               | **Rejected** (Overkill, poor ML dev experience) |

**Decision:** **Python (FastAPI)** is selected for the core API and Worker nodes to eliminate friction between web logic and ML inference. We will optimize FastAPI using `gunicorn` with `uvicorn` workers and threadpools for blocking I/O (e.g., `psycopg2`). If WebSocket ingestion becomes a bottleneck later, a Go-based ingestion gateway can be placed in front of Redis.

---

## 2. AI / ML Frameworks

**Requirements:** Maximize GPU efficiency on RTX 5070s (per ADR-0006), portability, and stream processing.

| Framework      | GPU Efficiency (Batching)                    | Edge Portability                  | Ecosystem & Pre-trained Models                | Verdict                                    |
| :------------- | :------------------------------------------- | :-------------------------------- | :-------------------------------------------- | :----------------------------------------- |
| **PyTorch**    | High. Eager execution makes debugging easy.  | Good (PyTorch Mobile/ExecuTorch). | **Massive.** Industry standard for research.  | **Selected (Training & Prototyping)**      |
| **TensorFlow** | High.                                        | Excellent (TF Lite).              | Declining in research; strong in legacy prod. | **Rejected**                               |
| **JAX**        | Highest for TPUs/multi-GPU.                  | Poor.                             | Growing, but niche.                           | **Rejected**                               |
| **ONNX**       | High. Highly optimized for diverse hardware. | Excellent.                        | N/A (It's an export format, not training).    | **Selected (Production Inference Format)** |
| **TensorRT**   | **Maximum.** NVIDIA specific optimization.   | Poor (NVIDIA only).               | N/A (Compiler).                               | **Selected (Cloud GPU Inference)**         |

**Decision:** Train/Fine-tune in **PyTorch**. Export to **ONNX** or compile with **TensorRT** for production inference on the cloud RTX 5070 clusters to maximize throughput and minimize latency. We will heavily utilize `stream=True` in Ultralytics YOLO to maximize batching parallelism and avoid memory bloat.

---

## 3. Video & Streaming Pipelines

**Requirements:** Handle incoming streams from Meta Ray-Ban (via Android DAT app), synchronize audio/video, and process for inference.

| Technology             | Latency             | Complexity                       | Flexibility                                  | Verdict                                      |
| :--------------------- | :------------------ | :------------------------------- | :------------------------------------------- | :------------------------------------------- |
| **FFmpeg** (CLI/libav) | High (Batch).       | Moderate.                        | **Unmatched.** Can transcode/mux anything.   | **Selected (Cold Path Processing)**          |
| **GStreamer**          | Low.                | Very High. Steep learning curve. | Extremely flexible pipeline graphs.          | **Candidate (If real-time hot path needed)** |
| **WebRTC**             | Ultra-Low (<500ms). | High (Signaling, STUN/TURN).     | Good for live viewing, hard for ML ingest.   | **Rejected for ML ingest; Keep for UI**      |
| **NVIDIA DeepStream**  | Low.                | High. NVIDIA lock-in.            | **Maximum throughput** for video CV on GPUs. | **Selected (Future Scaled CV Pipeline)**     |

**Decision:** MVP will use HTTP/WebSocket chunked uploads from the Android DAT client. The backend will use **FFmpeg** to assemble chunks and extract audio for ASR.

---

## 4. Databases & Storage

**Requirements:** Transactional integrity, high write throughput for telemetry, and vector storage for RAG coaching.

| Category                    | Option          | Pros                                         | Cons                                          | Verdict                                         |
| :-------------------------- | :-------------- | :------------------------------------------- | :-------------------------------------------- | :---------------------------------------------- |
| **Relational / State**      | **PostgreSQL**  | ACID, JSONB support, ubiquitous.             | Write-scaling at massive scale is hard.       | **Selected (psycopg2 sync driver)**             |
| **Time-Series / Telemetry** | ClickHouse      | Blistering fast analytics.                   | Operational overhead.                         | **Future (Phase 2)**                            |
| **Message Broker**          | **Redis**       | In-memory, ultra-fast, simple lists/streams. | Data loss possible if not persisted properly. | **Selected (Job Queues & Caching)**             |
| **Object Storage**          | **MinIO**       | S3-compatible, self-hosted, OSS.             | Requires disk management.                     | **Selected (Raw Video/Audio Storage)**          |
| **Vector DB**               | Qdrant / Milvus | Fast similarity search for pedagogical RAG.  | Additional infrastructure complexity.         | **Selected (Qdrant for MVP due to Rust speed)** |

**Decision:** **Postgres** (via `psycopg2`) for core state. **Redis** for the worker queues. **MinIO** for self-hosted OSS object storage.

---

## 5. Frontend & UI Architecture

**Requirements:** Highly responsive Admin Web Shell, complex data visualization (timelines, heatmaps).

| Framework           | Rendering                                        | Developer Experience               | Ecosystem                                         | Verdict                        |
| :------------------ | :----------------------------------------------- | :--------------------------------- | :------------------------------------------------ | :----------------------------- |
| **Next.js (React)** | SSR/RSC for SEO (if needed) & fast initial load. | Excellent. App Router is standard. | Massive. Easy access to charting libs (Recharts). | **Selected (Admin Web Shell)** |
| Vue / Nuxt          | Very good.                                       | Excellent.                         | Smaller ecosystem than React.                     | **Rejected**                   |
| Flutter (Web)       | Canvas based.                                    | Good for cross-platform.           | Poor SEO, non-standard DOM, heavy bundle.         | **Rejected**                   |

**Decision:** **Next.js 15 App Router** for the `services/web` frontend, optimizing for maintainability and scalable component architecture.

---

## 6. Infrastructure & Deployment

**Requirements:** Self-hosted India cloud, manageable for a small team, reproducible.

| Technology       | Pros                                               | Cons                                             | Verdict                              |
| :--------------- | :------------------------------------------------- | :----------------------------------------------- | :----------------------------------- |
| Docker Compose   | Simple, great for MVP/single-node.                 | Lacks self-healing and multi-node orchestration. | **Selected (Local Dev & Pilot MVP)** |
| Kubernetes (K3s) | Industry standard orchestration, self-healing.     | Steep learning curve, operational overhead.      | **Selected (Production Scale)**      |
| Nomad            | Simpler than K8s, handles non-container workloads. | Smaller ecosystem.                               | **Rejected**                         |

**Decision:** Start with **Docker Compose** (already in `infra/compose.dev.yaml`) for the internal pilot. Transition to a lightweight Kubernetes distribution (**K3s**) on bare-metal or self-managed VMs for production to manage the distributed GPU worker nodes.
