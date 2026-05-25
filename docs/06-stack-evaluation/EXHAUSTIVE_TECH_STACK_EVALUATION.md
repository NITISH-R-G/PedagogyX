# Exhaustive Tech Stack Evaluation & Comparison

**Status:** Phase 0 Active
**Date:** 2026-05-25
**Owner:** Principal Research Architect

This document details the exhaustive comparison of technologies for the PedagogyX platform, adhering to the founder's ₹0 customer budget and Open Source constraints.

## 1. Backend Architecture

### Candidates: Go vs. Rust vs. Python vs. Node.js

- **Go:** Excellent concurrency (goroutines) for handling thousands of incoming WebRTC/chunk streams. Fast compilation, low memory footprint.
  - _Decision:_ Recommended for the Edge Ingest layer and API Gateway where network I/O and concurrent connections are the primary bottlenecks.
- **Python:** Unmatched ecosystem for ML integration (PyTorch, HuggingFace). Poor concurrency compared to Go; high latency in API serving if not heavily optimized (e.g., using FastAPI + Uvicorn).
  - _Decision:_ Recommended for the ML Worker layer (Cold Path) where heavy inference orchestration is required.
- **Rust:** Supreme memory safety and performance. High hiring difficulty and slow compilation times.
  - _Decision:_ Recommended only for the desktop capture agent where minimizing CPU footprint on constrained school hardware is critical.
- **Node.js:** Ubiquitous, but struggles with heavy CPU-bound tasks (like media transcoding) without complex worker threads.
  - _Decision:_ Rejected for backend core; used only for the Next.js Frontend server.

## 2. AI/ML Inference Stack

### Candidates: PyTorch vs. TensorFlow vs. JAX vs. TensorRT

- **PyTorch:** The industry standard for research and deployment. Excellent dynamic graphs.
  - _Decision:_ The baseline framework for all model weights.
- **TensorFlow/JAX:** Less momentum in the open-source NLP/Audio community currently dominated by HuggingFace/PyTorch.
  - _Decision:_ Rejected.
- **TensorRT (NVIDIA):** Crucial for maximizing inference optimization on our constrained RTX 5070 hardware.
  - _Decision:_ Mandated for compiling YOLO (CV) models to achieve the highest possible frames-per-second on edge/cloud GPUs.
- **vLLM / Ollama:**
  - _Decision:_ Mandated for serving the `Qwen2.5-7B` model due to superior memory management (PagedAttention) and continuous batching capabilities.

## 3. Video Pipelines

### Candidates: FFmpeg vs. GStreamer vs. WebRTC vs. DeepStream

- **WebRTC:** Essential for the sub-second latency required for the "Hot Path" live supervision dashboard.
  - _Decision:_ Selected for live stream ingestion.
- **FFmpeg:** The universal standard for media transcoding and chunking.
  - _Decision:_ Selected for the "Cold Path" asynchronous processing and offline storage formatting.
- **GStreamer / DeepStream:** Highly optimized for complex, multi-stage hardware-accelerated pipelines, but steep learning curve.
  - _Decision:_ Kept in reserve; FFmpeg is sufficient for Phase 1 MVP.

## 4. Databases

### Candidates: Postgres vs. ClickHouse vs. MongoDB vs. Qdrant

- **PostgreSQL (with pgvector):** The absolute bedrock for relational metadata, RBAC, and tenant isolation. `pgvector` allows for RAG capabilities without introducing a secondary database in MVP.
  - _Decision:_ Selected as the primary operational datastore.
- **ClickHouse:** Unparalleled for time-series analytics and aggregating billions of "attention proxy" events.
  - _Decision:_ Deferred to Phase 2. Postgres is sufficient for early pilot scale.
- **Qdrant / Milvus:** Dedicated vector databases.
  - _Decision:_ Deferred to Phase 2. `pgvector` will handle the initial curriculum RAG workload to minimize infrastructure complexity.
- **MongoDB:** NoSQL flexibility.
  - _Decision:_ Rejected. We require strict schemas for pedagogical data governance.

## 5. Cloud & Infrastructure

### Candidates: AWS vs. GCP vs. Self-Hosted Bare Metal vs. Kubernetes

- **Self-Hosted Bare Metal GPU Clusters:** The _only_ way to meet the founder's ₹0 customer hardware budget while providing heavy AI inference is to build/lease bare-metal servers (e.g., via Hetzner or local Indian providers) rather than paying AWS/GCP's massive 400%+ premium on GPU instances.
  - _Decision:_ Primary inference compute will be bare metal.
- **AWS (ap-south-1):** Required for DPDP compliant control-plane hosting (API Gateway, Postgres DB, MinIO storage) due to superior reliability and managed services compared to bare metal.
  - _Decision:_ Hybrid approach. AWS for Control Plane, Bare Metal for Data/Inference Plane.
- **Kubernetes vs. Docker Swarm:**
  - _Decision:_ Kubernetes (K3s/EKS) for the AWS Control Plane for resilience. Docker Swarm for the bare-metal GPU pool to drastically reduce operational complexity during the MVP phase.
