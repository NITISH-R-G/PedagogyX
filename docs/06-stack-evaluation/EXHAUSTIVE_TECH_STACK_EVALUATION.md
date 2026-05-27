# Exhaustive Tech Stack Evaluation

## Overview

This document evaluates the technological landscape to select the optimal stack for PedagogyX, balancing the need for high-performance multimodal ML pipelines with the constraints of an open-source first (ADR-0005), cost-conscious (ADR-0006) startup environment.

---

## 1. Backend API & Ingestion

### Candidates

- **Python (FastAPI):** Exceptional ML ecosystem integration. High developer velocity. Asynchronous capabilities.
- **Go:** Unmatched concurrency and network performance. Ideal for handling thousands of concurrent WebRTC/video chunk uploads.
- **Rust:** Highest performance and memory safety. Steep learning curve, slower velocity.
- **Node.js:** Ubiquitous, fast I/O. Poor fit for heavy compute or ML integration.
- **Java (Spring):** Enterprise standard, robust. High memory overhead, verbose, slower velocity.

### Decision: Python (FastAPI)

**Rationale:** While Go is superior for pure video ingestion scaling, PedagogyX's core differentiator is AI. Having a unified language (Python) across the API, data pipelines, and ML workers drastically reduces cognitive load and allows ML engineers to contribute to the API. We will mitigate Python's GIL limitations by offloading video processing to C-bindings (FFmpeg) and heavy compute to separate worker processes.

---

## 2. AI / ML Frameworks

### Candidates

- **PyTorch:** The de-facto standard in research. Massive ecosystem (HuggingFace, Ultralytics).
- **TensorFlow:** Strong production tooling (TFX), but losing mindshare in research.
- **JAX:** Incredible performance on TPUs, growing in LLM space, but overkill and complex for standard vision/audio tasks.
- **ONNX/TensorRT:** Inference optimization layers rather than training frameworks.

### Decision: PyTorch + TensorRT (for deployment)

**Rationale:** PyTorch provides the fastest path from research paper to implementation. For production deployment on our specified RTX 5070 hardware (ADR-0006), models will be exported to ONNX and optimized with TensorRT to maximize batch throughput and minimize latency.

---

## 3. Video Pipelines & Streaming

### Candidates

- **FFmpeg:** The undisputed king of media processing. Versatile, but complex CLI.
- **GStreamer:** Pipeline-based, highly optimized C library. Excellent for complex, real-time routing. Steep learning curve.
- **WebRTC:** Essential for real-time, low-latency browser/mobile streaming.
- **MediaMTX:** Lightweight RTSP/WebRTC server.

### Decision: MediaMTX + FFmpeg

**Rationale:** The Android DAT client will stream chunks or WebRTC. MediaMTX acts as an excellent, lightweight bridge to receive WebRTC from the phone and expose it as RTSP/HLS to the backend. FFmpeg (via Python `ffmpeg-python`) will handle offline chunk processing, transcoding, and frame extraction for the ML workers.

---

## 4. Databases & Storage

### Relational / Metadata

- **Candidates:** PostgreSQL, MySQL.
- **Decision:** **PostgreSQL**. Unmatched feature set (JSONB, PostGIS if needed), rock-solid reliability, and excellent Python ORM support (SQLAlchemy/SQLModel).

### Object Storage (Video/Audio)

- **Candidates:** AWS S3, MinIO.
- **Decision:** **MinIO** (Self-hosted/OSS-first) transitioning to S3 for managed scale. MinIO provides absolute S3 compatibility allowing seamless local development.

### Vector Storage (Embeddings)

- **Candidates:** PgVector (Postgres extension), Milvus, Qdrant, Weaviate.
- **Decision:** **PgVector** (Initially). To reduce infrastructure complexity during Phase 1, we will utilize PgVector. If embedding retrieval becomes a bottleneck at scale, we will migrate to Qdrant or Milvus.

---

## 5. Frontend & Admin Shell

### Candidates

- **Next.js (React):** Industry standard for SSR/SSG. Massive ecosystem, excellent performance metrics (Core Web Vitals).
- **Vue / Nuxt:** Excellent developer experience, slightly smaller ecosystem.
- **SvelteKit:** High performance, no virtual DOM. Smaller talent pool.

### Decision: Next.js (React)

**Rationale:** Given the requirement to build an "Admin Web Shell" with complex data visualizations (charts, timelines) and potential SSR needs for SEO/performance, Next.js is the safest and most robust choice. It aligns with the existing boilerplate (`services/web`).

---

## 6. Infrastructure & Orchestration

### Candidates

- **Kubernetes:** The enterprise standard. Complex to manage, requires dedicated DevOps.
- **Docker Swarm:** Much simpler than K8s, built into Docker. Good for early scaling.
- **Nomad:** Elegant, fast scheduler by HashiCorp.
- **Serverless (AWS Lambda, Fargate):** Low operational overhead, high cost at sustained scale. Difficult to integrate with custom GPU workloads.

### Decision: Docker Compose (Phase 1) -> Kubernetes (Phase 2)

**Rationale:** Per ADR-0005 (FOSS-first) and the pilot infrastructure plan, we will utilize `docker compose` for developer environments and initial single-node pilot deployments. As we scale to multi-node GPU clusters, we will migrate to lightweight Kubernetes (K3s) for robust orchestration.

---

## 7. Cloud vs. Edge

### Candidates

- **Public Cloud (AWS/GCP):** Infinite scalability, high cost (especially for GPUs).
- **Self-Hosted GPU Clusters:** High upfront CapEx, vastly lower OpEx over time.
- **Edge AI (On-Device):** Maximum privacy, zero cloud cost. Constrained by battery/compute of Meta Ray-Ban and Android host.

### Decision: Hybrid Cloud (AWS/Local) with Dedicated GPUs

**Rationale:** The architecture mandates D-PROC=C (Hybrid Edge-Cloud). The Android device (Edge) handles capture and network buffering. The heavy ML inference must run centrally. Given the strict ₹0 customer hardware budget and RTX 5070 constraint, we will utilize cost-effective cloud GPU providers (e.g., RunPod, Lambda Labs, or dedicated Hetzner boxes) rather than expensive AWS EC2 P4 instances to maintain sustainable unit economics during the pilot phase.
