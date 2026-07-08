# Exhaustive Tech Stack Analysis

**Date:** 2026-05-24

## 1. Backend Frameworks

| Language    | Framework      | Strengths                                                          | Weaknesses                                                          | Conclusion                                                                                       |
| :---------- | :------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------- |
| **Go**      | Gin / Fiber    | Extremely low latency, high concurrency, tiny binaries.            | Weak ecosystem for ML integration; difficult to hire ML-Go hybrids. | Rejected for v1 due to ML friction.                                                              |
| **Rust**    | Axum           | Safest concurrency, C-like speed.                                  | Steepest learning curve, slower iteration speed.                    | Overkill for a web gateway interacting with external GPUs.                                       |
| **Python**  | **FastAPI**    | Perfect for ML integration, native async/await, massive ecosystem. | Slower execution speed (GIL), higher memory footprint.              | **Selected.** Speed of integrating ML pipelines trumps raw request throughput for this use case. |
| **Node.js** | Express / Nest | V8 is fast for I/O; huge talent pool.                              | Poor for CPU-bound tasks (ML orchestration).                        | Rejected.                                                                                        |
| **Java**    | Spring Boot    | Enterprise grade, highly observable.                               | Heavyweight, slow startup, friction with Python ML ecosystem.       | Rejected.                                                                                        |

## 2. AI/ML Frameworks

| Framework           | Strengths                                            | Weaknesses                                               | Conclusion                                                                                            |
| :------------------ | :--------------------------------------------------- | :------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| **PyTorch**         | Dominant in research, dynamic graphs, easy to debug. | Slower out-of-the-box inference than optimized runtimes. | **Selected (Core ML).** Essential for custom models and initial fine-tuning.                          |
| **TensorFlow**      | Great for production edge (TFLite).                  | Declining research share; complex API.                   | Rejected.                                                                                             |
| **JAX**             | Incredible for TPU scaling.                          | Steeper learning curve; niche outside Google.            | Rejected (we are GPU focused).                                                                        |
| **ONNX / TensorRT** | Maximum inference speed on NVIDIA GPUs.              | Harder to debug; model conversion can be brittle.        | **Selected (Inference).** We will compile PyTorch models to TensorRT/ONNX for the Cold Path pipeline. |

## 3. Video Pipelines

| Tool          | Strengths                                         | Weaknesses                                                              | Conclusion                                                         |
| :------------ | :------------------------------------------------ | :---------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **FFmpeg**    | Universal, handles everything, CLI based.         | Difficult to integrate natively into apps; process management overhead. | **Selected (Batch).** Used in Celery workers for chunk reassembly. |
| **GStreamer** | High-performance, pipeline-based, great for edge. | Steep learning curve; complex C API.                                    | Rejected for initial cloud MVP.                                    |
| **WebRTC**    | Built for low-latency live streaming.             | Overhead for purely asynchronous processing.                            | Rejected (until live coaching is required).                        |

## 4. Databases

| Database            | Type       | Strengths                                   | Weaknesses                                        | Conclusion                                                 |
| :------------------ | :--------- | :------------------------------------------ | :------------------------------------------------ | :--------------------------------------------------------- |
| **PostgreSQL**      | Relational | ACID compliant, robust, handles JSONb.      | Can struggle with massive scale without sharding. | **Selected.** Primary data store.                          |
| **ClickHouse**      | OLAP       | Blazing fast for analytics and time-series. | Overkill for Phase 1 data volume.                 | Deferred.                                                  |
| **Qdrant / Milvus** | Vector     | Optimized for embedding search (RAG).       | Operational overhead.                             | **Selected (Qdrant).** Needed for pedagogical AI coaching. |

## 5. Cloud & Infrastructure

| Provider/Tool        | Strengths                                    | Weaknesses                               | Conclusion                                                                                       |
| :------------------- | :------------------------------------------- | :--------------------------------------- | :----------------------------------------------------------------------------------------------- |
| **AWS (ap-south-1)** | Unmatched reliability, vast ecosystem.       | Expensive bandwidth and GPU instances.   | **Selected (Control Plane).** We will use AWS for DB, Storage, and API.                          |
| **Self-Hosted GPU**  | Drastically lower inference cost (RTX 5070). | CapEx heavy, maintenance overhead.       | **Selected (Data Plane).** We will host OSS AI on our own hardware to meet the ₹0 school budget. |
| **Docker Compose**   | Simple, reproducible.                        | Lacks self-healing and advanced scaling. | **Selected (Phase 1).** Sufficient for MVP and edge deployment.                                  |
| **Kubernetes**       | Infinite scaling, self-healing.              | Massive complexity tax for a small team. | Deferred (Phase 2).                                                                              |
