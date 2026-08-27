# Exhaustive Tech Stack Evaluation v1

## 1. Backend Architecture

| Language    | Strengths                                                                   | Weaknesses                                                          | Decision                                                               |
| :---------- | :-------------------------------------------------------------------------- | :------------------------------------------------------------------ | :--------------------------------------------------------------------- |
| **Python**  | Unmatched ML/AI ecosystem (PyTorch, HuggingFace), fast prototyping.         | GIL limits concurrency, higher base latency.                        | **Primary** (for ML orchestration and API).                            |
| **Go**      | Excellent concurrency (goroutines), low latency, compiles to single binary. | Weak ML ecosystem.                                                  | **Secondary** (for high-throughput media ingestion/routing if needed). |
| **Rust**    | Memory safety, zero-cost abstractions, predictable latency.                 | Steep learning curve, slower velocity for MVP.                      | Reject for v1.                                                         |
| **Node.js** | Ubiquitous full-stack language, huge ecosystem.                             | Single-threaded event loop not ideal for heavy compute/ML bridging. | Reject for backend (use for frontend).                                 |
| **Java**    | Enterprise proven, strong JVM ecosystem.                                    | High memory footprint, verbose, slow ML integration.                | Reject.                                                                |

## 2. AI / ML Frameworks

| Framework      | Strengths                                                                    | Weaknesses                                                | Decision                                          |
| :------------- | :--------------------------------------------------------------------------- | :-------------------------------------------------------- | :------------------------------------------------ |
| **PyTorch**    | Industry standard for research, dynamic computation graph.                   | Deployment can be heavy.                                  | **Primary** (for model training/experimentation). |
| **TensorRT**   | Maximizes NVIDIA GPU inference efficiency (crucial for RTX 5070 constraint). | Complex optimization process, hardware locked.            | **Primary** (for optimized YOLO deployment).      |
| **ONNX**       | Hardware agnostic model format.                                              | Sometimes lacks support for cutting-edge transformer ops. | **Secondary** (fallback for edge models).         |
| **TensorFlow** | Production tooling (TFX).                                                    | Declining research share, rigid.                          | Reject.                                           |
| **JAX**        | Excellent for TPUs and massive parallelism.                                  | Niche, overkill for single-GPU inference.                 | Reject.                                           |

## 3. Databases

| Database            | Primary Use Case                                         | Decision & Rationale                                                         |
| :------------------ | :------------------------------------------------------- | :--------------------------------------------------------------------------- |
| **PostgreSQL**      | Relational data, RBAC, transactional state.              | **Adopt.** Industry standard. Can also handle vectors via `pgvector` for v1. |
| **ClickHouse**      | OLAP, time-series metrics (engagement scores over time). | **Adopt.** Perfect for fast aggregation of thousands of CV inference points. |
| **pgvector**        | Vector search for RAG.                                   | **Adopt (v1).** Reduces infra complexity by piggybacking on Postgres.        |
| **Qdrant / Milvus** | High-scale standalone vector databases.                  | **Defer.** Overkill for pilot phase. Migrate if `pgvector` bottlenecks.      |
| **Redis**           | In-memory caching, message brokering (Celery).           | **Adopt.** Essential for hot-path metrics and queue management.              |

## 4. Video Pipelines

| Tool          | Strengths                                 | Weaknesses                            | Decision                                      |
| :------------ | :---------------------------------------- | :------------------------------------ | :-------------------------------------------- |
| **FFmpeg**    | The gold standard for media manipulation. | Complex CLI, heavy for simple tasks.  | **Adopt.** (For batch Cold Path transcoding). |
| **WebRTC**    | Real-time, ultra-low latency streaming.   | Complex state management (ICE, TURN). | **Adopt.** (For Hot Path live preview).       |
| **GStreamer** | Highly modular pipeline architecture.     | Steep learning curve.                 | Reject for v1.                                |
| **MediaMTX**  | Ready-to-use RTSP/WebRTC server.          |                                       | **Adopt.** Fast to deploy for ingest.         |

## 5. Frontend

| Framework                  | Strengths                                                    | Decision & Rationale                                                                                                                                       |
| :------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **React / Next.js**        | Massive ecosystem, SSR/SSG support, fast developer velocity. | **Adopt.** Best choice for the Admin/Teacher dashboard web app.                                                                                            |
| **Flutter / React Native** | Cross-platform mobile.                                       | **Defer.** Mobile companion app is needed for Meta Ray-Bans (Android), but native Android (Kotlin) might be required for raw Bluetooth/Media integrations. |

## 6. Cloud & Infrastructure (India DPDP Context)

| Provider                                        | Strengths                                                     | Decision & Rationale                                                                                                                                                 |
| :---------------------------------------------- | :------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AWS (ap-south-1)**                            | Unmatched reliability, vast services.                         | **Adopt (Control Plane).**                                                                                                                                           |
| **Self-Hosted GPU (Hetzner / local Indian DC)** | Massive cost savings for continuous GPU inference (RTX 5070). | **Adopt (Data Plane).** AWS GPU costs are prohibitive for K-12 budgets. We will use a hybrid approach: AWS for DB/Web, dedicated local GPU servers for ML inference. |
| **Kubernetes (K3s)**                            | Lightweight container orchestration.                          | **Adopt.** Essential for managing the distributed ML worker queues across bare-metal GPU nodes.                                                                      |
