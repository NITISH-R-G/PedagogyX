# Exhaustive Enterprise Tech Stack Evaluation

**Status:** Phase 0 Active
**Date:** 2026-05-25
**Owner:** Lead Systems Engineer
**Domain:** Deep-tech Educational AI Platform (PedagogyX)

## 1. Executive Summary

This document provides a rigorous, exhaustive evaluation of potential technology stacks for the PedagogyX platform. The evaluation adheres strictly to the project mandates: OSS-first, self-hosted, central inference servers (India-based cloud), and integration with Meta Ray-Ban glasses via Android DAT companion app.

## 2. Backend Language & Framework

**Requirements:** High concurrency for ingestion (Hot Path), low latency, and seamless integration with ML pipelines (Cold Path).

| Language / Framework | Concurrency / Latency                                              | ML Integration                                                       | Maintainability                                          | Verdict                                      |
| :------------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------- | :------------------------------------------------------- | :------------------------------------------- |
| **Go** (Fiber/Gin)   | Excellent. Goroutines handle massive concurrent WebSockets easily. | Poor. Requires CGO bindings to C++ ML libs; clunky.                  | Very Good. Easy to read, strong standard library.        | **Candidate (Ingestion Gateway Only)**       |
| **Rust** (Axum)      | Best-in-class latency and memory safety.                           | Fair. Ecosystem is immature compared to Python.                      | Difficult. High learning curve, slower feature velocity. | **Rejected** (Too slow for early stage MVP)  |
| **Python** (FastAPI) | Moderate. Asyncio is good, but GIL limits true parallelism.        | **Best-in-class.** Native integration with PyTorch, HF, Ultralytics. | Excellent. Massive ecosystem, easy hiring.               | **Selected (Core API & Workers)**            |
| **Node.js** (NestJS) | Good for I/O bound tasks.                                          | Poor. Python must run as separate microservices.                     | Good. Ubiquitous.                                        | **Rejected** (Disconnects API from ML logic) |

**Decision:** **Python (FastAPI)** is selected for the core API and Worker nodes. To mitigate GIL limitations, we will run multiple `uvicorn` workers managed by `gunicorn`, and explicitly define blocking I/O endpoints (like database calls) as standard `def` to utilize threadpools.

## 3. AI / ML Frameworks

**Requirements:** Maximize GPU efficiency on RTX 5070 clusters, high throughput, and ecosystem support.

| Framework           | GPU Efficiency (Batching)                   | Ecosystem & Models              | Edge Portability       | Verdict                             |
| :------------------ | :------------------------------------------ | :------------------------------ | :--------------------- | :---------------------------------- |
| **PyTorch**         | High. Eager execution makes debugging easy. | **Massive.** Industry standard. | Good (PyTorch Mobile). | **Selected (Training & R&D)**       |
| **TensorFlow**      | High.                                       | Declining in research.          | Excellent (TF Lite).   | **Rejected**                        |
| **JAX**             | Highest for TPUs.                           | Niche, though growing.          | Poor.                  | **Rejected**                        |
| **ONNX / TensorRT** | **Maximum.** NVIDIA specific optimization.  | N/A (Compilation targets).      | Poor (NVIDIA only).    | **Selected (Production Inference)** |

**Decision:** R&D and training will be conducted in **PyTorch**. Production inference on the cloud RTX 5070s will utilize **TensorRT** and **vLLM** to maximize throughput and minimize latency, meeting the stringent D-10 compute budget.

## 4. Video & Streaming Pipelines

**Requirements:** Handle incoming streams from the Android DAT client, synchronize A/V, and extract features.

| Technology             | Latency             | Complexity                       | Flexibility                            | Verdict                                 |
| :--------------------- | :------------------ | :------------------------------- | :------------------------------------- | :-------------------------------------- |
| **FFmpeg** (CLI/libav) | High (Batch).       | Moderate.                        | **Unmatched.** Transcode/mux anything. | **Selected (Cold Path Processing)**     |
| **GStreamer**          | Low.                | Very High. Steep learning curve. | Extremely flexible pipeline graphs.    | **Candidate (Future real-time)**        |
| **WebRTC**             | Ultra-Low (<500ms). | High (Signaling, TURN).          | Good for live viewing, hard for ML.    | **Rejected for ML ingest; Keep for UI** |

**Decision:** The MVP relies on chunked HTTP uploads from the DAT client. The backend will use **FFmpeg** to merge chunks, extract audio for ASR, and generate proxy video for CV processing.

## 5. Databases & Storage Architecture

**Requirements:** Transactional integrity, high write throughput for state/jobs, and vector storage for RAG.

| Category           | Option         | Pros                                         | Cons                                  | Verdict                                   |
| :----------------- | :------------- | :------------------------------------------- | :------------------------------------ | :---------------------------------------- |
| **Relational DB**  | **PostgreSQL** | ACID, JSONB, ubiquitous, robust RLS.         | Scaling writes globally is hard.      | **Selected (psycopg2 sync driver)**       |
| **Message Broker** | **Redis**      | In-memory, ultra-fast, robust lists/streams. | Data loss possible if unconfigured.   | **Selected (Job Queues & Cache)**         |
| **Object Storage** | **MinIO**      | S3-compatible, self-hosted, OSS.             | Operational disk management overhead. | **Selected (Raw Video/Audio Storage)**    |
| **Vector DB**      | **Qdrant**     | Extremely fast (Rust), simple deployment.    | Newer ecosystem than Pinecone.        | **Selected (Pedagogical RAG Embeddings)** |

**Decision:** The stack will consist of Postgres (relational state), Redis (async task queues), MinIO (blob storage), and Qdrant (vector embeddings).

## 6. Frontend & Admin UI

**Requirements:** Responsive, component-driven, excellent data visualization capabilities.

| Framework           | Rendering                      | Developer Experience               | Ecosystem                           | Verdict                        |
| :------------------ | :----------------------------- | :--------------------------------- | :---------------------------------- | :----------------------------- |
| **Next.js (React)** | SSR/RSC for fast initial load. | Excellent. App Router is standard. | Massive. Great charting (Recharts). | **Selected (Admin Web Shell)** |
| **Vue / Nuxt**      | Very good.                     | Excellent.                         | Smaller ecosystem than React.       | **Rejected**                   |

**Decision:** **Next.js** using the App Router, styled with **Tailwind CSS v4** (using the `@import "tailwindcss";` directive in `app/globals.css`).

## 7. Cloud Infrastructure & Orchestration

**Requirements:** Self-hosted India cloud, reproducible, manageable.

| Technology           | Pros                                             | Cons                                             | Verdict                                  |
| :------------------- | :----------------------------------------------- | :----------------------------------------------- | :--------------------------------------- |
| **Docker Compose**   | Simple, perfect for MVP and single-node pilots.  | Lacks self-healing and multi-node orchestration. | **Selected (Local Dev & Phase 1 Pilot)** |
| **Kubernetes (K3s)** | Industry standard, self-healing, robust scaling. | Steep learning curve, operational overhead.      | **Selected (Production Scale)**          |

**Decision:** Phase 1 uses Docker Compose (`infra/compose.dev.yaml`). Production will migrate to K3s to manage distributed GPU worker nodes efficiently across bare-metal Indian servers.
