# PedagogyX: Architecture Report v1

**Date:** 2026-05-24
**Author:** Autonomous Senior Full Stack Developer & Product Systems Architect

## 1. Product & Problem Analysis

PedagogyX requires a system capable of multimodal data capture in constrained environments (rural/urban India), real-time edge processing to meet strict privacy rules (DPDP), and long-context pedagogical assessment using OSS AI on consumer-grade GPUs (RTX 5070 12GB).
The primary client is Meta Ray-Ban smart glasses tethered to an Android device (DAT host) acting as an edge buffer. The objective is assessing teacher pedagogical performance, not student surveillance.

## 2. Full Stack Architecture

- **Edge:** Android App (DAT host) interfacing with Meta Ray-Bans via Bluetooth. Handles local buffering, chunking, VAD (Voice Activity Detection), and secure transmission.
- **API Gateway/Backend:** Modular architecture, built to handle erratic network conditions and large multi-part file uploads (video/audio chunks).
- **Event Bus:** Kafka or Redis Streams for decoupling the "hot path" (real-time processing, websocket updates) and the "cold path" (deep batch AI analytics).
- **AI Engine (OSS on-prem):** Local GPU server (RTX 5070) orchestrating optimized OSS models (e.g., faster-whisper, Qwen2.5-7B quantized) via vLLM or Ollama for inference.

## 3. Frontend Strategy

- **Web Dashboard (Admins):** React/Next.js for a robust, performant dashboard. Focus on accessible data visualization for pedagogical scores.
- **Mobile App (Edge Capture):** Android Native or Flutter (if cross-platform becomes a future requirement) to manage Bluetooth connections to Ray-Bans and background file processing securely.

## 4. Backend Strategy

- **Framework:** FastAPI (Python). Highly suited for both AI integrations and async workloads (websockets, chunked uploads).
- **Task Queues:** Celery (with Redis) for scheduling cold-path ML inference tasks.
- **Storage:** MinIO (S3-compatible) for raw video/audio chunks and processed artifacts.

## 5. Database Design

- **Relational Database:** PostgreSQL for primary operational data (users, schools, permissions, pedagogical scores, metadata).
- **Vector Database:** Qdrant or Weaviate for storing long-context lesson embeddings to enable semantic search and AI coaching RAG.

## 6. Security Strategy

- **Data Residency:** India region (e.g., AWS ap-south-1) for DPDP compliance.
- **Encryption:** AES-256 for data at rest. TLS 1.3 for data in transit.
- **Edge Privacy:** Minimal PII retention on the edge device. Local encryption before transmission.

## 7. DevOps & Deployment

- **Containerization:** Docker for all services.
- **Orchestration:** Docker Compose for local/on-prem, Kubernetes for cloud scaling.
- **CI/CD:** GitHub Actions for automated testing, linting (Ruff, Black, Mypy), and deployment.

## 8. Testing Strategy

- **Backend:** Pytest for API endpoints, integration tests, and task queues.
- **Frontend:** Playwright for E2E dashboard testing.
- **Edge:** Emulators for Android testing and network degradation simulations.

## 9. Refactoring Opportunities

- Ensure the existing `services/api` modularity supports the transition to event-driven processing (Kafka/Redis) for decoupled ML pipelines.

## 10. Risks & Tradeoffs

- **Hardware Constraints:** 12GB VRAM is tight for running high-quality ASR and an LLM simultaneously. Tradeoff: We must heavily rely on sequential processing (batch) and quantization, increasing latency for deep insights.
- **Edge Reliability:** Meta Ray-Bans battery life and Bluetooth stability during 60-minute classes. Tradeoff: Robust local buffering on the Android host is critical, delaying cloud sync if necessary.

## 11. Agile Sprint Plan

- **Sprint 1:** Core infrastructure (Docker Compose, Postgres, MinIO, Redis). FastAPI skeleton.
- **Sprint 2:** Edge upload API and basic chunking/reassembly logic.
- **Sprint 3:** VAD and ASR integration (faster-whisper) on the backend.
- **Sprint 4:** LLM integration (vLLM/Ollama) for basic pedagogical scoring.
