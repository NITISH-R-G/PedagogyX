# Comprehensive Tech Stack Evaluation

## Backend Stack Analysis

### Python (FastAPI) vs. Go vs. Rust vs. Node.js

- **Python (FastAPI)**: Selected for its seamless integration with the AI/ML ecosystem. FastAPI provides high-performance async capabilities (via Starlette) and automatic OpenAPI documentation, which is crucial for rapid prototyping and connecting deeply with PyTorch/HuggingFace ecosystems.
- **Go**: Offers superior concurrency and lower memory footprint, excellent for high-throughput API gateways and infrastructure tools. However, bridging Go to complex Python ML pipelines introduces serialization overhead and complexity.
- **Rust**: Unmatched performance and memory safety. Ideal for core, highly-optimized components (e.g., custom video processing extensions). Too slow to iterate for the entire backend during Phase 0/1.
- **Node.js**: Strong ecosystem, particularly good if sharing code with the frontend (Next.js). However, lacks the native scientific computing libraries needed for a deep-tech AI platform.
- **Decision**: Python (FastAPI) for core API and ML orchestration. Node.js reserved specifically for the Next.js frontend server.

## AI/ML Frameworks

### PyTorch vs. TensorFlow vs. ONNX

- **PyTorch**: The absolute standard for AI research. Massive model hub (HuggingFace), intuitive eager execution, and strong community support. Best for model development and fine-tuning.
- **TensorFlow**: Historically strong in production deployment (TFX), but PyTorch has caught up. Less favored by current researchers.
- **ONNX/TensorRT**: Crucial for inference optimization. Models trained in PyTorch will be exported to ONNX and compiled with TensorRT to maximize throughput on NVIDIA hardware (e.g., RTX 5070 target).
- **Decision**: PyTorch for R&D and training. ONNX/TensorRT for production inference pipelines.

## Video Pipelines

### FFmpeg vs. GStreamer vs. WebRTC

- **FFmpeg**: The industry standard workhorse for video transcoding and frame extraction. Universally supported, extensive CLI, but can be complex to integrate deeply into application memory without wrappers.
- **GStreamer**: Pipeline-based multimedia framework. Excellent for building complex, low-latency streaming applications. Steeper learning curve than FFmpeg.
- **WebRTC**: Required for any ultra-low-latency _live_ streaming directly to browsers.
- **Decision**: FFmpeg for backend asynchronous processing (frame extraction, audio separation). WebRTC will be evaluated later if real-time tele-coaching becomes a feature.

## Databases

### Relational (Postgres) vs. NoSQL vs. Vector (Qdrant)

- **PostgreSQL**: Unquestionable choice for relational metadata (users, organizations, session metadata, RBAC). ACID compliant, battle-tested, extensible (PostGIS, pgvector).
- **Qdrant**: High-performance vector database written in Rust. Crucial for storing multimodal embeddings and enabling semantic search across pedagogical events. Preferred over Pinecone for self-hosting capabilities (data residency requirements).
- **Decision**: PostgreSQL as the primary transactional datastore. Qdrant for vector storage. Redis for caching and event brokering (if Kafka is deemed too heavy initially).

## Frontend

### React / Next.js vs. Alternatives

- **Next.js (React)**: Industry standard for scalable web applications. Provides SSR for performance, excellent developer experience, and a vast ecosystem of UI components (shadcn/ui, Tailwind).
- **Decision**: Next.js is selected. It provides the necessary structure for building complex, data-heavy dashboards for educational analytics.

## Infrastructure & Orchestration

### Kubernetes vs. Serverless vs. Docker Swarm

- **Kubernetes (K8s)**: The de facto standard for container orchestration at scale. Handles complex deployments, GPU scheduling, and scaling policies. Essential for managing the distributed microservices of PedagogyX.
- **Serverless**: Good for bursty workloads, but difficult to manage long-running inference jobs (e.g., 45-minute video processing) due to timeouts and cold starts. High cost at sustained scale.
- **Decision**: Kubernetes for cloud orchestration. Docker Compose for local MVP/development.

## Cloud Strategy

### AWS vs. GCP vs. Azure vs. Hybrid

- **AWS**: Deepest feature set, strong presence in India (ap-south-1) for DPDP compliance. Excellent managed services (EKS, RDS, MSK).
- **GCP**: Strong AI tooling, often preferred for K8s (GKE).
- **Hybrid (Self-Hosted GPU)**: Given the high cost of cloud GPUs, a hybrid model where baseline APIs are cloud-hosted (AWS) and heavy inference is routed to self-hosted, collocated GPU clusters (e.g., racks of RTX 5070s) is economically necessary for long-term SaaS viability in education.
- **Decision**: AWS for core cloud infrastructure (ap-south-1). Develop inference services to be highly portable (K8s) to allow routing to on-premise GPU clusters as scale demands.
