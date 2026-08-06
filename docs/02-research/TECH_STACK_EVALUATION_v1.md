# PedagogyX: Tech Stack & Infrastructure Evaluation

**Author:** Principal Research Architect
**Document Version:** v1.0
**Status:** DRAFT

## Executive Summary

This document provides an exhaustive evaluation of the technology stack options for PedagogyX. The architecture must support real-time multimodal AI inference, high-throughput video pipelines, distributed edge-to-cloud synchronization, and strict data privacy compliance (e.g., India DPDP).

---

## 1. Backend Languages & Frameworks

### Candidates Evaluated

1.  **Python (FastAPI)**
    - **Pros:** De facto standard for AI/ML integration. Vast ecosystem (PyTorch, HuggingFace). Fast iteration speed.
    - **Cons:** GIL limits true concurrency. High memory footprint. Slower execution speed compared to compiled languages.
    - **Verdict:** **Selected for AI microservices and data pipelines.** Necessary for seamless ML integration.
2.  **Go (Golang)**
    - **Pros:** Incredible concurrency model (goroutines). Fast execution. Low memory footprint. Excellent for networking and distributed systems.
    - **Cons:** Less mature ML ecosystem. Verbose error handling.
    - **Verdict:** **Recommended for high-throughput API gateways and video streaming infrastructure.**
3.  **Rust**
    - **Pros:** Memory safety without garbage collection. Blazing fast. Excellent for systems programming and WebAssembly.
    - **Cons:** Steep learning curve. Slower development velocity initially.
    - **Verdict:** Evaluate for specific edge device components where memory/CPU are strictly constrained.
4.  **Node.js (TypeScript)**
    - **Pros:** Ubiquitous. Shared language with frontend. Good ecosystem for generic web APIs.
    - **Cons:** Single-threaded (event loop). Poor for CPU-bound tasks (like video processing or ML).
    - **Verdict:** **Selected for the primary web backend (BFF - Backend for Frontend) integrating with Next.js.**

### Architecture Decision: Polyglot Microservices

- **API Gateway/Web Backend:** Node.js (TypeScript) / Next.js
- **AI Inference Workers:** Python (FastAPI, Celery/RQ)
- **High-Throughput Streaming (Future):** Go

---

## 2. AI & Machine Learning Ecosystem

### Candidates Evaluated

1.  **PyTorch**
    - **Pros:** Industry standard for research and dynamic graphs. Unparalleled model availability on HuggingFace.
    - **Cons:** Slightly heavier deployment footprint compared to optimized ONNX models.
    - **Verdict:** **Selected as the primary framework for training and server-side inference.**
2.  **ONNX (Open Neural Network Exchange) / TensorRT**
    - **Pros:** Highly optimized for inference. Cross-platform. TensorRT maximizes NVIDIA GPU efficiency.
    - **Cons:** Requires conversion steps. Sometimes unsupported custom layers.
    - **Verdict:** **Selected for production inference optimization**, specifically for edge deployment and RTX 5070 GPU optimization.

---

## 3. Video Processing Pipelines

### Candidates Evaluated

1.  **FFmpeg**
    - **Pros:** The industry standard. Supports nearly every codec. Highly optimized.
    - **Cons:** Complex CLI syntax. Difficult to integrate as a library (often requires subprocess calls).
    - **Verdict:** **Selected for core transcoding and chunking tasks.**
2.  **GStreamer**
    - **Pros:** Pipeline-based architecture. Excellent for complex, real-time routing of media.
    - **Cons:** Very steep learning curve. Complex C API.
    - **Verdict:** Evaluate for edge-device capture if FFmpeg proves too rigid.
3.  **WebRTC**
    - **Pros:** Ultra-low latency real-time communication.
    - **Cons:** Complex signaling infrastructure required.
    - **Verdict:** Evaluate if real-time remote coaching (live streaming) becomes a requirement.

---

## 4. Database Architecture

### Candidates Evaluated

1.  **PostgreSQL**
    - **Pros:** Rock-solid relational database. JSONB support. Excellent ecosystem.
    - **Cons:** Can struggle with massive time-series data without extensions (TimescaleDB).
    - **Verdict:** **Selected as the primary transactional database** (users, schools, metadata).
2.  **Qdrant / Milvus (Vector Databases)**
    - **Pros:** Optimized for high-dimensional vector similarity search (crucial for RAG and semantic search of classroom transcripts).
    - **Cons:** Additional infrastructure to manage.
    - **Verdict:** **Qdrant selected** for its Rust-based performance and simplicity in handling multimodal embeddings.
3.  **Redis**
    - **Pros:** In-memory, blazing fast. Excellent for caching and task queues.
    - **Verdict:** **Selected** for caching, rate limiting, and managing Celery/worker queues.

---

## 5. Frontend Technologies

### Candidates Evaluated

1.  **Next.js (React)**
    - **Pros:** Industry standard. Server-Side Rendering (SSR) for performance. Massive ecosystem.
    - **Verdict:** **Selected as the primary frontend framework** for the web dashboard.
2.  **Tailwind CSS**
    - **Pros:** Utility-first, highly maintainable, rapid UI development.
    - **Verdict:** **Selected for styling.**

---

## 6. Infrastructure & Cloud

### Constraints

- India DPDP requires localized processing.
- Founder has a ₹0 customer budget for the pilot (bootstrapped infra).
- Targeting RTX 5070 for initial compute.

### Candidates Evaluated

1.  **Kubernetes (K8s)**
    - **Pros:** Ultimate orchestration, auto-scaling, industry standard.
    - **Cons:** Massive overhead for a pilot. Complex to manage without dedicated DevOps.
    - **Verdict:** Too heavy for Phase 1 MVP. Planned for Phase 2 scaling.
2.  **Docker Compose (Single/Multi-Node VM)**
    - **Pros:** Simple, fast iteration, easy to deploy on a single powerful bare-metal server.
    - **Verdict:** **Selected for Phase 1 Pilot.** A single bare-metal Linux box with an RTX 5070 running Docker Compose is sufficient to validate the MVP cost-effectively.
3.  **Cloud Provider (AWS/GCP vs. Bare Metal/Hetzner)**
    - **Analysis:** Cloud GPUs (AWS p4) are prohibitively expensive for a free pilot. Bare metal providers (Hetzner, runpod) offer significantly cheaper GPU compute.
    - **Verdict:** Utilize low-cost bare-metal GPU hosting for the pilot phase to meet the ₹0 customer budget constraint.

---

## Conclusion

The Phase 1 architecture will rely on a pragmatic, cost-effective stack: **Next.js (Web) + Node.js (API) + Python/FastAPI (Workers) + Postgres/Qdrant + Bare Metal Docker/RTX5070.** This balances rapid development velocity with the specific hardware and cost constraints of the initial pilot.
