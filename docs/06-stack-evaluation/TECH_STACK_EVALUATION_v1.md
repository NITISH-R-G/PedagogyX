# Tech Stack Evaluation v1

## Introduction

As the principal research architect for PedagogyX, this document provides an exhaustive evaluation of the technology stack required to build our autonomous multimodal AI classroom intelligence platform. The selected stack must balance execution velocity with extreme scalability, privacy compliance (India DPDP), and the unique constraints of hybrid edge/cloud multimodal ML pipelines.

---

## 1. Backend Framework Evaluation

### Candidates: Python (FastAPI), Go, Rust, Node.js, Java (Spring Boot)

- **Python (FastAPI)**
- _Strengths_: Unmatched ecosystem for ML/AI. Asynchronous by default. High execution velocity.
- _Weaknesses_: Global Interpreter Lock (GIL) limits true concurrency. Higher latency and memory usage than compiled languages.
- **Go**
- _Strengths_: Excellent concurrency model (goroutines). Very low latency. Great for microservices and API gateways. Fast compilation.
- _Weaknesses_: Poor ML ecosystem. Verbose error handling.
- **Rust**
- _Strengths_: Maximum performance and memory safety. No garbage collection pauses.
- _Weaknesses_: Steepest learning curve. Slower execution velocity for early-stage startups.
- **Node.js**
- _Strengths_: Ubiquitous. Great for I/O-bound tasks and real-time websockets (e.g., chat/coaching interfaces).
- _Weaknesses_: Single-threaded (though worker threads exist). Poor for heavy computational tasks.
- **Java (Spring Boot)**
- _Strengths_: Enterprise proven. Massive ecosystem.
- _Weaknesses_: Heavyweight, slow startup times (bad for serverless scaling). Verbose.

**Decision**: **Python (FastAPI)** is selected for the core data ingestion and AI orchestration services due to its seamless integration with the PyTorch/ML ecosystem. We accept the latency tradeoff for development velocity and ML compatibility. Node.js will be used selectively for BFF (Backend-for-Frontend) and real-time websocket services.

---

## 2. AI/ML Framework Evaluation

### Candidates: PyTorch, TensorFlow, JAX, ONNX, TensorRT

- **PyTorch**
- _Strengths_: De facto standard for research and modern transformer architectures (Hugging Face). Excellent dynamic computation graph.
- **TensorFlow**
- _Strengths_: Historically better for production serving (TF Serving) and edge (TF Lite).
- _Weaknesses_: Losing mindshare to PyTorch in research; ecosystem feels fragmented (TF1 vs TF2).
- **JAX**
- _Strengths_: Incredible performance on TPUs/GPUs. Great for massive scale.
- _Weaknesses_: Functional programming paradigm is a learning curve. Smaller ecosystem than PyTorch.
- **ONNX (Open Neural Network Exchange)**
- _Strengths_: Framework agnostic. Critical for exporting PyTorch models to optimized deployment formats.
- **TensorRT (NVIDIA)**
- _Strengths_: Maximum inference optimization on NVIDIA hardware (crucial for our 12GB edge VRAM constraint).

**Decision**: **PyTorch** for all model training, experimentation, and cloud inference. **ONNX** and **TensorRT** are absolutely mandatory for optimizing models to run on the constrained edge hardware (ADR-0008).

---

## 3. Video Pipeline Evaluation

### Candidates: FFmpeg, GStreamer, WebRTC, RTSP, NVIDIA DeepStream

- **FFmpeg**: The undisputed king of media processing. Best for batch transcoding and extracting audio tracks for ASR.
- **GStreamer**: Pipeline-based architecture. Excellent for complex, real-time routing, but steep learning curve.
- **WebRTC**: Required for ultra-low latency live streaming (e.g., if we build a real-time coaching whisper feature).
- **NVIDIA DeepStream**: Highly optimized for real-time video analytics on NVIDIA GPUs.

**Decision**: **FFmpeg** for all cloud-side batch processing (transcoding, audio extraction). **WebRTC** will be investigated for the Meta Ray-Ban (DAT) to cloud pipeline if real-time feedback becomes a firm requirement; otherwise, standard chunked HTTP/gRPC uploads are preferred for stability.

---

## 4. Database Architecture Evaluation

### Relational (Candidates: PostgreSQL, MySQL)

- **Decision**: **PostgreSQL**. Superior JSON support (JSONB), advanced indexing, and rock-solid reliability for enterprise SaaS metadata, RBAC, and telemetry.

### Vector Databases (Candidates: Qdrant, Milvus, Weaviate, Pinecone)

- **Decision**: **Qdrant**. Chosen for its performance, Rust-based architecture, and ability to run locally (for edge deployments) or in the cloud. It is crucial for storing multimodal embeddings and enabling semantic search across classroom events.

### Knowledge Graph (Candidates: Neo4j, Amazon Neptune)

- **Decision**: **Neo4j**. Best-in-class graph database for modeling the complex relationships between teachers, pedagogies, student outcomes, and long-term analytics.

### Caching & Queues (Candidates: Redis, RabbitMQ, Kafka)

- **Decision**: **Redis** for caching. We will use a distributed event bus (likely **Redpanda** or managed Kafka) for handling the high-throughput, decoupled asynchronous ML worker pipelines.

---

## 5. Frontend Framework Evaluation

### Candidates: React, Next.js, Flutter (Mobile), Electron (Desktop)

- **Next.js (React)**: Best choice for the web dashboard. Provides SSR/SSG for fast load times, excellent developer experience, and a massive ecosystem for charting/analytics components.
- **Flutter**: If a mobile app is required beyond the Meta DAT companion app (e.g., a dedicated app for teachers to review feedback), Flutter offers the best cross-platform velocity.

**Decision**: **Next.js (React)** for the primary web application and admin portals.

---

## 6. Infrastructure & Cloud Evaluation

### Orchestration (Candidates: Kubernetes, Nomad, Docker Swarm)

- **Decision**: **Kubernetes (K8s)**. Mandatory for managing the complex, distributed, microservice-based architecture, scaling GPU node pools, and handling stateful sets.

### Cloud Providers (Candidates: AWS, GCP, Azure, Hybrid)

- **Decision**: **AWS (ap-south-1)** is the primary target due to mature ML infrastructure (SageMaker, Inferentia/Trainium options) and strict DPDP compliance data residency in India. However, the architecture must remain heavily containerized to allow hybrid deployments if large school districts mandate on-premise hardware for privacy reasons.
