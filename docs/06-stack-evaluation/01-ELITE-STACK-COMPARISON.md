# Elite Tech Stack Evaluation

**Author:** Autonomous Principal Research Architect
**Phase:** 0
**Status:** In Progress

## Introduction

Before implementation, we must rigorously evaluate the foundational technologies that will power PedagogyX. The choices must balance extreme scale, GPU efficiency, maintainability, and our specific hybrid edge-cloud constraints.

## 1. Backend

### Comparison

- **Go:** Exceptional for high-throughput, concurrent networking. Ideal for the edge LAN ingest buffer and cloud gateway.
- **Python:** The undisputed leader in the ML/AI ecosystem. Mandatory for the multimodal inference pipelines and orchestration.
- **Rust:** Excellent memory safety and performance, but slower development cycle and less ML ecosystem integration than Python.
- **Node.js:** Good for I/O bound frontend-adjacent services, but poor for heavy computational tasks.
- **Java:** Enterprise proven, but heavy footprint and less natural fit for modern GPU workflows compared to Python.

### Decision

- **Ingest/Gateway:** Go
- **AI Services & Core API:** Python (FastAPI)

## 2. AI/ML Frameworks

### Comparison

- **PyTorch:** The standard for AI research and multimodal transformer architectures. Massive community and flexibility.
- **TensorFlow:** Excellent production serving (TF Serving), but losing mindshare in research.
- **JAX:** Incredible performance on TPUs/GPUs, but steeper learning curve.
- **ONNX / TensorRT:** Crucial for optimizing PyTorch models for inference, especially on the target RTX 5070 GPUs.

### Decision

- **Core Framework:** PyTorch
- **Inference Optimization:** TensorRT for deployment on the 5070 clusters.

## 3. Video Pipelines

### Comparison

- **FFmpeg:** The universal standard for media processing. Required for slicing and transcoding.
- **GStreamer:** Powerful for building complex, low-latency streaming pipelines.
- **WebRTC:** Essential for real-time, low-latency communication (e.g., if we build a live coaching interface).
- **NVIDIA DeepStream:** Highly optimized for running computer vision on NVIDIA hardware, but ties us deeply to the NVIDIA ecosystem.

### Decision

- Use **FFmpeg** for reliable chunking and batch processing. Investigate **WebRTC** only if real-time sub-second latency is mandated by the product.

## 4. Databases

### Comparison

- **Postgres:** The gold standard for relational data, tenant metadata, and structured logs.
- **ClickHouse:** Unbeatable for massive analytical workloads and time-series telemetry.
- **MongoDB:** Flexible schema, but unnecessary if our data models are well-understood.
- **Vector DBs (Qdrant vs. Milvus vs. pgvector):** pgvector is easiest to start with since we are using Postgres, but Milvus or Qdrant will be necessary for massive-scale semantic retrieval over thousands of classroom sessions.

### Decision

- **Relational:** PostgreSQL
- **Vector (Initial):** pgvector (migrate to Qdrant at scale)

## 5. Frontend

### Comparison

- **Next.js (React):** Industry standard for modern web applications, excellent ecosystem (Tailwind, Radix).
- **Flutter:** Great for cross-platform mobile, but less ideal for complex, data-heavy web dashboards.
- **Tauri/Electron:** Only needed if a thick desktop client is required, which contradicts our web-first approach.

### Decision

- **Web App / Admin:** Next.js with React.

## 6. Infrastructure

### Comparison

- **Kubernetes:** The standard for container orchestration, but complex to manage.
- **Docker Compose:** Sufficient for local dev and the initial MVP pilot, but will not scale.
- **Cloud vs. Bare Metal:** Given the massive cost of cloud GPUs, deploying to self-hosted bare-metal GPU clusters (e.g., in an Indian data center) may be economically mandatory for the business model.

### Decision

- **Pilot:** Docker Compose for simplicity and rapid iteration.
- **Production:** Kubernetes on specialized GPU cloud providers or bare metal.

## Summary of Stack

- **Primary Languages:** Python (Backend/AI), Go (Ingest), TypeScript (Frontend)
- **AI:** PyTorch + TensorRT + faster-whisper + Ollama
- **Data:** Postgres + pgvector + MinIO (S3)
- **UI:** Next.js
- **Infra:** Docker -> Kubernetes
