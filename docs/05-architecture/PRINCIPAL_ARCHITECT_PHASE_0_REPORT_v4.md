# Principal Architect Phase 0 Report v4

**Owner:** Autonomous Principal Research Architect & Lead Systems Engineer
**Project:** PedagogyX
**Status:** In Progress
**Date:** 2026-06-11

## Phase 0 — Foundational Interrogation

Before proceeding with any implementation code generation, we must deeply interrogate the core product tenets. A failure to identify architectural blind spots now will lead to catastrophic debt during scaling. The focus is on a scalable, privacy-first, edge-cloud multimodal system.

## Product Questions

- **Customer Profiling:** Is this enterprise SaaS targeting wealthy private schools, or a state-mandated evaluation platform targeting public districts? (Current founder answers indicate a hybrid model for India, focusing on K-12 and university, potentially scaling globally).
- **Surveillance vs. Coaching:** Is the platform built for surveillance (punitive) or instructional coaching (supportive)? The implementation of "China-style supervision" in specific markets requires strict architectural boundaries to prevent privacy leaks.
- **Hardware & Latency Constraints:** Can we assume low-latency, high-bandwidth school networks? No. Our architecture must buffer at the edge and withstand prolonged WAN dropouts.
- **Compliance & Geography:** What are the exact requirements for DPDP compliance in India regarding the capture of minor biometrics (faces, voices)? We must implement privacy-first models that purge raw video and maintain only embedding vectors or non-reversible states where legal mandates dictate.
- **Deployment Modality:** The shift from fixed smartboards to Meta Ray-Ban POV client architectures vastly changes our network ingestion layer. How do we ensure teacher comfort, safety, and battery life during a full day?
- **Data Residency:** Will government-funded schools demand strict onshore data residency within their exact district limits, requiring edge deployments, or is regional cloud sufficient?

## Technical Questions

- **Scalability & Inference:** Can our cloud inference handle concurrent cold-path ASR and Vision fusion from hundreds of simultaneous DAT-host Android devices? Can we safely scale using RTX 5070 constraints?
- **Synchronization:** What is the precise mechanism for aligning POV video from Ray-Bans with audio tracks that might be captured at different sampling rates?
- **Storage Strategy:** Are we persisting the raw multimedia payloads, or strictly processing them ephemerally?
- **Federated vs. Centralized ML:** Is it feasible to push lightweight inference (e.g., VAD) down to the Android companion app to save bandwidth, or must everything be processed centrally?
- **Network Resiliency:** What occurs during a complete loss of internet connectivity during an instruction segment? Do we implement local persistent storage buffering on the Android DAT client?
- **Microphone Array Processing:** How does the Ray-Ban directional audio handle significant ambient classroom noise and code-switching?

## Competitor Analysis

- **Edthena & Vosaic:** These rely heavily on manual tagging, IP camera installations, and high CapEx setups.
  - _Opportunity:_ Meta Ray-Ban POV architecture bypasses expensive installations, reducing onboarding friction to zero.
- **AI Sokrates:** NLP-heavy text analysis based on transcripts.
  - _Opportunity:_ We integrate spatial and kinesic tracking, creating a true multimodal index superior to purely lexical analysis.
- **Chinese Smart Classrooms (Hanwang, Tencent):** Massive surveillance-grade infrastructure.
  - _Weakness/Opportunity:_ They are legally non-compliant in GDPR/DPDP regions. We must build a privacy-first, verifiable system that offers similar analytical depth without panoptic capture.
- **Zoom AI / Microsoft Teams:** General-purpose meeting intelligence.
  - _Weakness:_ They are not aligned with pedagogical rubrics (e.g., Danielson Framework).
- **IRIS Connect:** Strong pedagogical focus but lacks advanced automated multimodal ingestion.
  - _Opportunity:_ Incorporate automated multimodal processing mapped to instructional frameworks without the manual effort.

## Research Papers

- **Multimodal Learning Analytics (MMLA):** Fusing prosody, kinesics, and semantics provides significantly stronger correlations to pedagogical effectiveness.
- **Speech Emotion Recognition (SER) in Noisy Environments:** Generic off-the-shelf Whisper models degrade under heavy Indian code-switching. We must evaluate specialized or fine-tuned variants.
- **Long-Context Video Understanding:** Architectures such as Qwen-VL or Gemini 1.5 Pro equivalents are essential for holistic classroom segment analysis rather than chunked, disjointed evaluations.
- **Pedagogical Alignment:** Converting qualitative rubrics into embedded vectors for Retrieval-Augmented Generation (RAG).
- **Federated Learning for Education:** Preserving student privacy while improving global model weights across highly distributed district edges.

## Architecture Phase

**System & High-Level Architecture:**

- **Edge Capture Layer:** Meta Ray-Ban glasses transmitting POV video and directional audio to Android companion apps via Bluetooth/Wi-Fi Direct.
- **Ingestion Layer:** Resilient API gateways handling chunked uploads with robust retry mechanisms, queuing raw assets into an event stream.
- **Processing Layer:** Multimodal AI workers reading from queues. Separate pipelines for ASR, Video Analytics (Computer Vision), and Metric Extraction.
- **Storage Layer:** Ephemeral block storage for raw assets, vectorized persistent storage for extracted intelligence, and relational stores for user and session metadata.

**Deployment & Infrastructure Maps:**

- K3s/K8s clusters orchestrating the microservices. Self-hosted RTX 5070 clusters for cost-effective heavy inference.

## Tech Stack Analysis

**Backend:**

- **Go:** Selected for the ingestion gateway due to unparalleled concurrency handling and low latency during heavy edge-client uploads.
- **Python (FastAPI):** Selected for the core ML orchestration and API tier due to native ML library integration.

**AI/ML:**

- **PyTorch:** Standard for model research.
- **ONNX/TensorRT:** Essential for maximizing RTX 5070 utilization during cold-path batch processing.

**Video Pipelines:**

- **FFmpeg:** Selected for robust chunking and format normalization on the edge and server side.
- **GStreamer:** Considered for future ultra-low-latency real-time streaming, but FFmpeg is superior for current batch-ingestion workflows.

**Databases:**

- **PostgreSQL (pgvector):** Selected for unified state management and vector retrieval, reducing operational complexity.
- **Redis:** Selected for managing asynchronous Dead Letter Queues (DLQ) and hot-path caching.

**Frontend:**

- **Next.js:** Server-side rendering guarantees performance on lower-end devices typically used by K-12 administration.

**Infrastructure & Cloud:**

- **Self-Hosted GPUs:** Required to manage OPEX and satisfy data residency laws. RTX 5070 clusters offer the best ROI compared to AWS/GCP instances for this specific workload.
- **Docker Compose / Kubernetes:** Compose for edge nodes and development (`compose.dev.yaml`), K3s/K8s for central cloud orchestration.

## AI Features

- **Teacher Talk Time & Wait Time:** Real-time VAD processing to calculate pacing and instructional ratios.
- **Pedagogical Pattern Detection:** Analyzing the sequence of question-asking, student response, and teacher feedback.
- **Multimodal Event Timelines:** Correlating visual cues (e.g., student gaze direction) with audio (teacher volume/tone).
- **Hallucination-Resistant RAG Coaching:** Ensuring all AI-generated feedback strictly cites transcript timestamps and references institutional guidelines.
- **Classroom Engagement Heatmaps:** Aggregated analytics on general classroom attention levels.
- **Longitudinal Teacher Analytics:** Tracking improvement across semesters using dynamic knowledge graphs.

## Agile Requirements

- **Sprint Rituals:** Maintain strict Sprint Planning, Retrospectives, and Backlog Grooming.
- **Technical Debt:** Dedicate 20% of every sprint to observability improvements, DLQ analysis, and refactoring N+1 query loops.
- **RFC/ADR Documentation:** No architecture changes proceed without a formal Architecture Decision Record (ADR). The recent shift to Ray-Ban capture is documented in ADR-0009.
- **Story Structuring:** All epics must be broken down into testable stories with precise acceptance criteria. Code must not be merged without corresponding test coverage and DLQ fail-safes.
- **Dependency Tracking:** Maintain robust graphs of inter-service dependencies.

## Documentation Requirements

The system must maintain exhaustive, continuously updated documentation.

- **Product Requirements Document (PRD):** Defining the specific scope for the next quarter.
- **System Architecture & Data Governance Specs:** Detailing how PII is handled, scrubbed, and secured.
- **Multimodal Inference Pipeline Diagram:** A visual representation of the journey from edge capture to generated insights.
- **Observability and Telemetry Standards:** Instrumentation guidelines for tracing and metrics collection.
- **Synthetic Data Generation and Prompt Engineering Guides:** Ensuring repeatable evaluation conditions.
- **Classroom Hardware Requirements:** Specifications for Android devices serving as gateways.
