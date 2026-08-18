# Tech Stack Evaluation Report v1

**Date:** 2026-05-25
**Author:** Autonomous Principal Research Architect
**Status:** DRAFT
**Context:** Evaluation of technologies for PedagogyX, constrained by founder mandates: strict OSS preference, maximum RTX 5070 12GB VRAM per node, and focus on the Indian market.

## 1. Executive Summary

This report evaluates and justifies the technology stack for PedagogyX. The overarching constraint is the strict requirement for open-source software (OSS) and deployment on highly constrained hardware (12GB VRAM limit). The stack must support a hybrid edge-to-cloud architecture processing multimodal data streams (from Meta Ray-Ban POV) with sub-3-second real-time inference goals.

## 2. Infrastructure & Operations

- **Requirement:** Low cost (₹0 customer pilot budget), scalable, and reproducible.
- **Selected Stack:** Docker Compose (MVP) -> Kubernetes (Production).
- **Rationale:** Docker Compose provides immediate developer velocity for the MVP boilerplate. However, the distributed nature of the workers (ASR, CV, Inference) and the need for strict resource management (GPU scheduling) necessitate a transition to Kubernetes for production.
- **Cloud Provider:** AWS (ap-south-1) - implicitly required for India data residency (DPDP compliance).

## 3. Backend APIs & Microservices

- **Requirement:** High concurrency, asynchronous processing, ML ecosystem compatibility.
- **Selected Stack:** Python (FastAPI).
- **Rationale:** Python is the undisputed language for AI/ML integration. FastAPI provides excellent asynchronous support (crucial for streaming I/O) and automatic OpenAPI documentation. While Go or Rust might offer marginally better raw I/O performance, the context-switching cost between a Go backend and Python ML workers is too high for this team's composition.

## 4. Frontend & User Experience

- **Requirement:** Web-based, responsive dashboards for administrators and teachers.
- **Selected Stack:** React with Next.js.
- **Rationale:** Standard enterprise choice. Next.js provides server-side rendering (SSR) which may be beneficial for initial load times in lower-bandwidth environments (common in parts of the target market), and integrates cleanly with our required testing framework (Vitest).

## 5. Data Storage

- **Relational Database (Selected):** PostgreSQL. Proven, robust, handles complex RBAC schemas needed for the dual-segment (K-12/University) and supervision/coaching mode toggles.
- **Vector Database (Selected):** Qdrant. Specifically chosen as part of the PedagogyX memory. Excellent for semantic search over pedagogical events and teacher history.
- **Message Broker / Event Bus (Selected):** Redis PubSub (MVP) transitioning to Apache Kafka (Production). Necessary to decouple the API Gateway ingestion from the heavy GPU workers.

## 6. AI/ML Stack & The 12GB Constraint

This is the most heavily constrained portion of the stack. All models must run concurrently or via rapid context switching within 12GB of VRAM (NVIDIA RTX 5070).

- **Framework (Selected):** PyTorch + ONNX / TensorRT. PyTorch for development; models must be exported to ONNX or heavily optimized via TensorRT for inference to minimize memory overhead.

### 6.1 Language Models (LLM)

- **Selected Candidate:** Qwen2.5-7B-Q4 (or similar highly quantized 7B model).
- **Rationale:** Must run locally (no third-party APIs allowed per OSS/privacy mandate). A 7B parameter model in FP16 requires ~14GB VRAM, exceeding our limit. Therefore, INT4 quantization (requiring ~4.5GB VRAM) is mandatory. The Qwen series shows strong reasoning capabilities at smaller scales.

### 6.2 Automatic Speech Recognition (ASR)

- **Selected Candidate:** Faster-Whisper.
- **Rationale:** Standard Whisper is too memory-intensive. Faster-Whisper (using CTranslate2) significantly reduces VRAM footprint and increases speed. Must support English and Hindi simultaneously.

### 6.3 Computer Vision (CV)

- **Selected Candidate:** YOLOv8/v9 (Nano or Small variants).
- **Rationale:** We need real-time object detection (whiteboards, screens, students) from the POV feed. Only the smallest variants of YOLO will fit in the remaining VRAM budget (alongside the LLM and ASR models) while maintaining the required FPS.

## 7. Tradeoffs and Risks

- **VRAM Contention:** The primary risk. A single RTX 5070 hosting a 7B LLM (INT4 - ~4.5GB), Faster-Whisper (~2-3GB), and a CV model (~1-2GB) leaves very little headroom for context sizes, batches, or system overhead.
- **Mitigation Strategy:** Implement strict memory management. The API gateway must employ aggressive rate-limiting. We must explore sequential processing (ASR -> CV -> LLM) rather than parallel execution if VRAM limits are consistently breached during stress testing, though this jeopardizes the <3s real-time goal.
