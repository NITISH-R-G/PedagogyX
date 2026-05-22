# Exhaustive Tech Stack Analysis & Architecture Decisions

**Version:** 1.0
**Author:** Architecture Team
**Constraints:** FOSS-first, ₹0 customer budget, RTX 5070 sizing.

## 1. Backend Languages

We evaluated core backend languages against latency, concurrency, ML integration, infra cost, maintainability, and hiring difficulty.

| Language    | Latency & Perf                       | Concurrency                                                               | ML Integration                                     | Infra Cost                             | Maintainability & Hiring                                   | Verdict                              |
| ----------- | ------------------------------------ | ------------------------------------------------------------------------- | -------------------------------------------------- | -------------------------------------- | ---------------------------------------------------------- | ------------------------------------ |
| **Go**      | Extremely low latency. Fast startup. | Excellent. Goroutines are perfect for handling thousands of media chunks. | Poor. Limited ML libraries compared to Python.     | Lowest. Tiny memory footprint.         | High maintainability. Easy to hire system engineers.       | **WINNER (API Gateway & Signaling)** |
| **Rust**    | Best-in-class, C-level speeds.       | Excellent, safe concurrency.                                              | Moderate (tch-rs exists but ecosystem is nascent). | Lowest.                                | Steep learning curve slows dev velocity. Hiring is harder. | Rejected for v1.                     |
| **Python**  | High latency.                        | Poor (GIL limits true threading).                                         | Unmatched (PyTorch, Pandas).                       | High (requires more RAM/CPU to scale). | Excellent hiring pool for data scientists.                 | **WINNER (ML Worker Daemons)**       |
| **Node.js** | Moderate (V8 is fast for I/O).       | Good for I/O, terrible for CPU-bound tasks.                               | Poor (TensorFlow.js is mostly for browsers).       | Moderate.                              | Easy to hire full-stack devs.                              | Rejected for core backend.           |
| **Java**    | High throughput, slow startup.       | Excellent (JVM threads, Virtual threads).                                 | Moderate (Deeplearning4j).                         | High memory footprint.                 | Huge enterprise hiring pool.                               | Rejected (Too heavy for edge nodes). |

## 2. AI / ML Frameworks

Evaluated for inference optimization, GPU efficiency, portability, and edge deployment.

| Framework      | Inference Optimization        | GPU Efficiency                             | Portability                    | Edge Deployment                     | Verdict                                   |
| -------------- | ----------------------------- | ------------------------------------------ | ------------------------------ | ----------------------------------- | ----------------------------------------- |
| **TensorRT**   | Best-in-class for NVIDIA.     | Maximizes RTX 5070 throughput.             | Poor (tied to NVIDIA).         | Impossible on low-end Android edge. | **WINNER (Cloud CV Pipeline)**            |
| **PyTorch**    | Moderate (TorchScript helps). | High, but higher VRAM overhead.            | Excellent across hardware.     | Moderate (PyTorch Mobile).          | Base for training/dev.                    |
| **ONNX**       | High (ONNX Runtime).          | Good, but rarely beats TensorRT on NVIDIA. | Excellent (Hardware agnostic). | Excellent (WebAssembly, Android).   | **WINNER (CPU Fallbacks)**                |
| **TensorFlow** | High (XLA compiler).          | High.                                      | Good.                          | Excellent (TFLite).                 | Rejected (Team expertise favors PyTorch). |
| **JAX**        | Excellent for TPUs.           | Good for GPUs.                             | Moderate.                      | Poor.                               | Rejected.                                 |

## 3. Video Pipelines

Evaluated for latency, complexity, and specific feature sets.

| Tool              | Focus                      | Latency       | Complexity                       | Verdict                         |
| ----------------- | -------------------------- | ------------- | -------------------------------- | ------------------------------- |
| **MediaMTX**      | WebRTC/RTSP routing.       | Sub-second.   | Low (Zero dependency Go binary). | **WINNER (Ingest Hub)**         |
| **FFmpeg**        | Transcoding & Chunking.    | High (Batch). | Moderate (CLI).                  | **WINNER (Cold Path Chunking)** |
| **WebRTC (Pion)** | P2P streaming.             | Ultra-low.    | High (ICE/STUN/TURN management). | Used internally by MediaMTX.    |
| **GStreamer**     | Complex pipeline building. | Low.          | Extremely High.                  | Rejected (Overkill for MVP).    |
| **DeepStream**    | High-throughput CV.        | Ultra-low.    | High (C++ NVIDIA specific).      | Deferred to Phase 2.            |

## 4. Databases

Evaluated for analytical capability, JSON support, and vector search.

| Database       | Primary Use Case | Relational/ACID            | Vector Support                    | Verdict                         |
| -------------- | ---------------- | -------------------------- | --------------------------------- | ------------------------------- |
| **PostgreSQL** | Truth, Metadata. | Excellent.                 | Yes (pgvector).                   | **WINNER (Primary Store)**      |
| **MinIO**      | Blob / S3.       | N/A                        | N/A                               | **WINNER (Video/JSON Storage)** |
| **ClickHouse** | OLAP Analytics.  | No (Eventual consistency). | No.                               | Deferred to Phase 2.            |
| **MongoDB**    | Document store.  | Weak ACID across shards.   | Atlas Vector Search (cloud only). | Rejected.                       |
| **Cassandra**  | High-write TSDB. | Tunable consistency.       | Vector search in newer versions.  | Overkill for Phase 1.           |
| **Neo4j**      | Graph DB.        | Yes.                       | N/A                               | Rejected.                       |

## 5. Frontend

Evaluated for platform support and team velocity.

| Framework          | Platform               | SSR Support | Bundle Size         | Verdict                                      |
| ------------------ | ---------------------- | ----------- | ------------------- | -------------------------------------------- |
| **Next.js**        | Web Admin.             | Excellent.  | Moderate.           | **WINNER (Admin Dashboard)**                 |
| **React**          | Web SPA.               | No.         | Large.              | Used within Next.js.                         |
| **Tauri**          | Windows Desktop.       | N/A         | Tiny.               | **WINNER (Windows Capture Agent)**           |
| **Electron**       | Windows Desktop.       | N/A         | Massive (Chromium). | Rejected.                                    |
| **Flutter**        | Cross-platform mobile. | N/A         | Moderate.           | Rejected (Android specific features needed). |
| **Kotlin/Compose** | Native Android.        | N/A         | Small.              | **WINNER (Android Capture Agent)**           |

## 6. Infrastructure & Cloud Architecture

Evaluated for control, cost, and reliability.

| Option                           | Control                 | Cost at Scale (GPU)                     | Operational Complexity         | Verdict                              |
| -------------------------------- | ----------------------- | --------------------------------------- | ------------------------------ | ------------------------------------ |
| **Self-Hosted VPS (Bare Metal)** | Complete.               | Lowest (Flat monthly fee for RTX 5070). | High (Must manage OS/Drivers). | **WINNER (GPU Pool)**                |
| **Docker Compose**               | High.                   | Free.                                   | Low.                           | **WINNER (Phase 1 Deploy)**          |
| **AWS (ap-south-1)**             | Low (Managed services). | Astronomical (Egress + GPU hourly).     | Low.                           | Rejected.                            |
| **GCP / Azure**                  | Low.                    | Astronomical.                           | Low.                           | Rejected.                            |
| **Kubernetes (K3s)**             | Complete.               | Free.                                   | Extremely High.                | Deferred to Phase 2.                 |
| **Nomad / Swarm**                | Complete.               | Free.                                   | Moderate.                      | Rejected (Go straight to K8s later). |
