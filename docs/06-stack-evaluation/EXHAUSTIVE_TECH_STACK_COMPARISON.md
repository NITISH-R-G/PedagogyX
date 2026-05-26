# Exhaustive Tech Stack Evaluation

**Status:** Research Phase 0 Active
**Date:** 2026-05-26
**Owner:** Principal Research Architect (Jules)

Before committing to a specific technology for the PedagogyX MVP and subsequent enterprise scale-out, we must evaluate the core stack across multiple dimensions: latency, ML ecosystem integration, hiring difficulty, and operational cost.

---

## 1. Backend API & Control Plane

The core API handles routing, RBAC, chunked video uploads from the Android DAT companion, and webhook delivery. It does not perform ML inference directly.

| Language / Framework   | Concurrency Model      | Ecosystem for ML      | Ops Cost / Memory | Recommendation                                                                                                                                                                |
| :--------------------- | :--------------------- | :-------------------- | :---------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Go (Gin/Fiber)**     | Goroutines (Excellent) | Poor (Native ML)      | Very Low          | **Strongly Considered for Scale.** Exceptional for routing and high-throughput chunked uploads. Low memory footprint.                                                         |
| **Python (FastAPI)**   | Asyncio (Good)         | Excellent (Native ML) | Medium            | **Selected for v1 MVP.** Provides the fastest bridge between the API layer and the Python-heavy ML worker queues, minimizing serialization overhead during rapid prototyping. |
| **Rust (Actix/Axum)**  | Async (Excellent)      | Poor (Native ML)      | Very Low          | Rejected. Too steep a learning curve for rapid Phase 0/1 iteration. Overkill for simple API routing.                                                                          |
| **Node.js (Express)**  | Event Loop (Good)      | Poor (Native ML)      | Low               | Rejected. Lack of true multi-threading makes it suboptimal for handling heavy video stream ingest compared to Go/Python.                                                      |
| **Java (Spring Boot)** | Threads (Good)         | Poor (Native ML)      | High              | Rejected. Too heavy for our initial deployment constraints; enterprise boilerplate slows down velocity.                                                                       |

**Decision:** Use **Python (FastAPI)** for the MVP to maintain a unified language across API and ML workers. Migrate API Gateway/Ingestion to **Go** when concurrent DAT uploads exceed Python's async limits.

## 2. AI/ML Inference Frameworks

We are targeting 12GB VRAM class GPUs (RTX 5070) for centralized processing. Efficiency is paramount.

| Framework        | Flexibility                            | Inference Speed (VRAM Efficiency) | Portability        | Recommendation                                                                                                       |
| :--------------- | :------------------------------------- | :-------------------------------- | :----------------- | :------------------------------------------------------------------------------------------------------------------- |
| **PyTorch**      | Excellent (Research standard)          | Medium                            | Good               | **Selected for Training/Prototyping.** Best ecosystem for loading modern Hugging Face models (Whisper).              |
| **TensorFlow**   | Good                                   | Medium                            | Excellent (TFLite) | Rejected. Losing mindshare in the research community; PyTorch is the de-facto standard for our required models.      |
| **ONNX Runtime** | Poor (Training), Excellent (Inference) | High                              | Excellent          | **Selected for Production Inference.** Converting PyTorch models to ONNX allows us to standardize inference engines. |
| **TensorRT**     | Poor (Hardware locked)                 | Very High (Nvidia only)           | Poor               | **Mandated for CV Pipeline.** To hit our throughput goals on RTX 5070s, YOLO models must be optimized via TensorRT.  |

**Decision:** Prototype in PyTorch, deploy optimized models using ONNX and **TensorRT**.

## 3. Video Pipelines & Streaming

Handling the video chunks from the Ray-Ban DAT client to the GPU workers.

| Technology            | Latency      | Complexity | Use Case Fit         | Recommendation                                                                                                                     |
| :-------------------- | :----------- | :--------- | :------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| **FFmpeg**            | High (Batch) | High       | Universal processing | **Selected for Cold Path.** Best for batch processing, chunk concatenation, and extracting audio tracks before passing to Whisper. |
| **GStreamer**         | Low          | Very High  | Real-time pipelines  | Rejected for MVP. Too complex to configure across mixed hardware for Phase 1.                                                      |
| **WebRTC / MediaMTX** | Ultra-Low    | Medium     | Real-time view       | **Selected for Hot Path.** Essential if we implement the "Live Admin Dashboard" (Supervision Mode) later.                          |
| **Nvidia DeepStream** | Low          | High       | High-density CV      | Considered for Phase 2 scaling, but overkill while we establish the underlying data models.                                        |

**Decision:** Use standard HTTP chunked uploads + **FFmpeg** for reliable cold-path processing.

## 4. Database Architecture

We need to store hierarchical user data (Schools -> Teachers -> Sessions), time-series event data (CV/ASR outputs), and high-dimensional embeddings for RAG.

| Database                  | Primary Strength          | Weakness                  | Recommendation                                                                                                                                              |
| :------------------------ | :------------------------ | :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PostgreSQL (pgvector)** | ACID, Relational, Vectors | Scaling vector search     | **Selected.** Provides relational integrity for RBAC and sufficient vector search capabilities for early RAG pipelines without adding a separate DB system. |
| **ClickHouse**            | Time-series, Analytics    | Poor relational modeling  | Rejected. We don't have the scale of telemetry data yet to justify a dedicated OLAP database.                                                               |
| **Milvus / Qdrant**       | High-scale vector search  | Operational overhead      | Deferred. We will outgrow pgvector eventually, but managing a dedicated vector DB in Phase 1 violates our simplicity mandate.                               |
| **MongoDB**               | Schema flexibility        | Weak relational integrity | Rejected. Educational data (Schools, Districts, Users, Roles) is inherently relational.                                                                     |

**Decision:** **PostgreSQL** with the `pgvector` extension to handle both application state and RAG embeddings.

## 5. Storage (Blob / Video)

| Technology | Type                  | Compliance | Cost             | Recommendation                                                                                                                |
| :--------- | :-------------------- | :--------- | :--------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **AWS S3** | Cloud                 | Good       | High (Bandwidth) | Rejected. Violates ADR-0005 (FOSS/Self-hosted preference).                                                                    |
| **MinIO**  | Object, S3-Compatible | Excellent  | Capital Cost     | **Selected.** Allows us to run S3-compatible storage on our own hardware, critical for India data residency and cost control. |

**Decision:** **MinIO** for chunked video and extracted asset storage.

## 6. Frontend / Admin Interface

| Technology           | UX Capability  | Ecosystem | Recommendation                                                                                                                 |
| :------------------- | :------------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **React (Vite/SPA)** | High           | Massive   | **Selected.** Industry standard, massive hiring pool, integrates perfectly with our REST APIs.                                 |
| **Next.js (SSR)**    | High (SEO)     | Large     | Rejected. We are building a secure admin dashboard behind auth; SSR/SEO is irrelevant and adds unnecessary backend complexity. |
| **Flutter / Tauri**  | Cross-platform | Niche     | Rejected. Unnecessary for web-based dashboards.                                                                                |

**Decision:** Pure **React** SPA (built with Vite) to minimize deployment complexity on self-hosted infrastructure.

## Summary Tech Stack

- **API:** Python / FastAPI
- **Database:** PostgreSQL (with pgvector)
- **Storage:** MinIO
- **Workers:** Python / Celery or RQ (backed by Redis)
- **ML Engines:** PyTorch (Dev) -> TensorRT (Prod)
- **Frontend:** React (Vite)
- **Client (Android):** Kotlin / Meta DAT SDK
