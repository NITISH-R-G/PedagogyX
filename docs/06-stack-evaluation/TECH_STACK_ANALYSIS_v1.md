# TECH STACK ANALYSIS v1

**CONFIDENTIAL INTERNAL RESEARCH DOCUMENT**
**AUTHOR:** Autonomous Principal Research Architect
**PROJECT:** PedagogyX
**STATUS:** PRE-IMPLEMENTATION (Phase 0)

## 1. Backend Language Selection

- **Python (FastAPI):**
- _Pros:_ First-class support for ML/AI libraries (PyTorch, HuggingFace, Ray). Extremely fast development speed. FastAPI provides excellent async support and automatic OpenAPI docs.
- _Cons:_ GIL limitations for heavy CPU concurrency (though mostly mitigated by async I/O and offloading to C-extensions/GPUs).
- _Verdict:_ **Selected** for all core ML orchestration, data processing, and API routing.
- **Node.js / TypeScript:**
- _Pros:_ Ubiquitous, excellent ecosystem for real-time (WebSockets) and frontend integration (Next.js backend-for-frontend).
- _Cons:_ Poor fit for heavy mathematical or ML workloads.
- _Verdict:_ **Selected** strictly for the BFF (Backend-For-Frontend) layer and specific real-time signaling tasks, delegating heavy lifting to Python services.
- **Go / Rust:**
- _Pros:_ Exceptional performance, memory safety (Rust), high concurrency.
- _Cons:_ Slower development velocity compared to Python; smaller AI/ML ecosystems.
- _Verdict:_ **Rejected** for Phase 1 to prioritize development speed and ML integration, but reserved for rewriting specific, high-throughput bottlenecks in later phases.

## 2. AI/ML Frameworks

- **PyTorch:**
- _Pros:_ Industry standard for research and multimodal model development. Massive ecosystem (HuggingFace Transformers).
- _Cons:_ Can be heavy for edge deployment.
- _Verdict:_ **Selected** as the primary training and cloud-inference framework.
- **ONNX / TensorRT:**
- _Pros:_ Highly optimized for inference, crucial for maximizing the 12GB VRAM edge constraint.
- _Verdict:_ **Selected** for edge deployment. PyTorch models will be exported to ONNX/TensorRT for local execution.

## 3. Video Pipelines

- **FFmpeg:**
- _Pros:_ Industry standard, ubiquitous, handles almost every format.
- _Cons:_ Command-line driven, can be clunky to integrate into complex Python async pipelines robustly.
- _Verdict:_ **Selected** for base transcoding and frame extraction.
- **GStreamer:**
- _Pros:_ Highly modular, excellent for complex, real-time pipelines and hardware acceleration.
- _Cons:_ Extremely steep learning curve; complex C API.
- _Verdict:_ **Considered** for Phase 2 if FFmpeg proves insufficient for real-time edge streaming requirements.

## 4. Databases

- **PostgreSQL:**
- _Verdict:_ **Selected** for all relational data (users, tenants, RBAC, application state). Unrivaled stability and JSONB support for semi-structured metadata.
- **Qdrant:**
- _Verdict:_ **Selected** for vector storage. Excellent performance, Rust-based, scales well, and handles complex multimodal embeddings efficiently.
- **Neo4j / ArangoDB:**
- _Verdict:_ **Selected (Neo4j)** for the Knowledge Graph. Essential for modeling complex temporal relationships between educational events (e.g., matching a teacher's specific question type to a subsequent change in student engagement).

## 5. Frontend & Infrastructure

- **Next.js (React):**
- _Verdict:_ **Selected** for the teacher dashboard. Industry standard, excellent server-side rendering (SSR) for performance, and strong TypeScript support.
- **Kubernetes (K8s):**
- _Verdict:_ **Selected** for cloud orchestration. Necessary for managing the complex interplay of API services, GPU workloads (via Ray), and databases at scale.

EOF
