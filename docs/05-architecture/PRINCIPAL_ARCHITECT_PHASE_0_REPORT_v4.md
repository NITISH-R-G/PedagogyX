# Principal Architect Phase 0 Report v4

**Owner:** Autonomous Principal Research Architect & Lead Systems Engineer
**Project:** PedagogyX
**Status:** In Progress
**Date:** 2026-05-27

## Phase 0 — Foundational Interrogation

Before proceeding with any structural code generation, we must interrogate the core product tenets. Too many AI startups fail because they build highly complex multimodal pipelines without fully understanding their legal, pedagogical, and scale constraints.

### Product Questions

- **Customer Profiling:** Is this enterprise SaaS targeting wealthy private schools, or a state-mandated evaluation platform targeting public districts? (Current founder answers indicate a hybrid model for India, focusing on K-12 and university, potentially scaling globally).
- **Surveillance vs. Coaching:** Is the platform built for surveillance (punitive) or instructional coaching (supportive)? The implementation of "China-style supervision" in specific markets requires strict architectural boundaries to prevent privacy leaks.
- **Hardware & Latency Constraints:** Can we assume low-latency, high-bandwidth school networks? No. Our architecture must buffer at the edge and withstand prolonged WAN dropouts.
- **Compliance & Geography:** What are the exact requirements for DPDP compliance in India regarding the capture of minor biometrics (faces, voices)? We must implement privacy-first models that purge raw video and maintain only embedding vectors or non-reversible states where legal mandates dictate.
- **Deployment Modality:** The shift from fixed smartboards to Meta Ray-Ban POV client architectures (ADR-0009) vastly changes our network ingestion layer. How do we ensure teacher comfort, safety, and battery life during a full day?

### Technical Questions

- **Scalability & Inference:** Can our cloud inference handle concurrent cold-path ASR and Vision fusion from hundreds of simultaneous DAT-host Android devices? Can we safely scale using RTX 5070 constraints?
- **Synchronization:** What is the precise mechanism for aligning POV video from Ray-Bans with audio tracks that might be captured at different sampling rates?
- **Storage Strategy:** Are we persisting the raw multimedia payloads, or strictly processing them ephemerally?
- **Federated vs. Centralized ML:** Is it feasible to push lightweight inference (e.g., VAD) down to the Android companion app to save bandwidth, or must everything be processed centrally?

## Research Phase

### Competitor Analysis

- **Edthena & Vosaic:** These rely heavily on manual tagging, IP camera installations, and high CapEx setups.
  - _Opportunity:_ Meta Ray-Ban POV architecture bypasses expensive installations, reducing onboarding friction to zero.
- **AI Sokrates:** NLP-heavy text analysis based on transcripts.
  - _Opportunity:_ We integrate spatial and kinesic tracking, creating a true multimodal index superior to purely lexical analysis.
- **Chinese Smart Classrooms (Hanwang, Tencent):** Massive surveillance-grade infrastructure.
  - _Weakness/Opportunity:_ They are legally non-compliant in GDPR/DPDP regions. We must build a privacy-first, verifiable system that offers similar analytical depth without panoptic capture.
- **Zoom AI / Microsoft Teams:** General-purpose meeting intelligence.
  - _Weakness:_ They are not aligned with pedagogical rubrics (e.g., Danielson Framework).

### Research Papers

- **Multimodal Learning Analytics (MMLA):** Fusing prosody, kinesics, and semantics provides significantly stronger correlations to pedagogical effectiveness.
- **Speech Emotion Recognition (SER) in Noisy Environments:** Generic off-the-shelf Whisper models degrade under heavy Indian code-switching. We must evaluate specialized or fine-tuned variants.
- **Long-Context Video Understanding:** Architectures such as Qwen-VL or Gemini 1.5 Pro equivalents are essential for holistic classroom segment analysis rather than chunked, disjointed evaluations.
- **Pedagogical Alignment:** Converting qualitative rubrics into embedded vectors for Retrieval-Augmented Generation (RAG).

## Architecture Phase

### Mandatory Tech Stack Analysis

**Backend:**

- **Go:** Selected for the ingestion gateway due to unparalleled concurrency handling and low latency during heavy edge-client uploads.
- **Python (FastAPI):** Selected for the core ML orchestration and API tier due to native ML library integration.

**AI/ML:**

- **PyTorch:** Standard for model research.
- **ONNX/TensorRT:** Essential for maximizing RTX 5070 utilization during cold-path batch processing.

**Video Pipelines:**

- **FFmpeg:** Selected for robust chunking and format normalization on the edge and server side.

**Databases:**

- **PostgreSQL (pgvector):** Selected for unified state management and vector retrieval, reducing operational complexity.
- **Redis:** Selected for managing asynchronous Dead Letter Queues (DLQ) and hot-path caching.

**Frontend:**

- **Next.js:** Server-side rendering guarantees performance on lower-end devices typically used by K-12 administration.

**Infrastructure:**

- **Self-Hosted GPUs:** Required to manage OPEX and satisfy data residency laws. RTX 5070 clusters offer the best ROI.
- **Docker Compose / Kubernetes:** Compose for edge nodes and development (`compose.dev.yaml`), K3s/K8s for central cloud orchestration.

### AI Features To Research

- **Teacher Talk Time & Wait Time:** Real-time VAD processing to calculate pacing and instructional ratios.
- **Pedagogical Pattern Detection:** Analyzing the sequence of question-asking, student response, and teacher feedback.
- **Multimodal Event Timelines:** Correlating visual cues (e.g., student gaze direction) with audio (teacher volume/tone).
- **Hallucination-Resistant RAG Coaching:** Ensuring all AI-generated feedback strictly cites transcript timestamps and references institutional guidelines.

## Scrum & Agile Requirements

- **Sprint Rituals:** Maintain strict Sprint Planning, Retrospectives, and Backlog Grooming.
- **Technical Debt:** Dedicate 20% of every sprint to observability improvements, DLQ analysis, and refactoring N+1 query loops.
- **RFC/ADR Documentation:** No architecture changes proceed without a formal Architecture Decision Record (ADR). The recent shift to Ray-Ban capture is documented in ADR-0009.
- **Story Structuring:** All epics must be broken down into testable stories with precise acceptance criteria. Code must not be merged without corresponding test coverage and DLQ fail-safes.

## Documentation Requirements

The system must maintain exhaustive, continuously updated documentation.

- **Product Requirements Document (PRD)**
- **System Architecture & Data Governance Specs**
- **Multimodal Inference Pipeline Diagram**
- **Observability and Telemetry Standards**
- **Synthetic Data Generation and Prompt Engineering Guides**

## Implementation Rules

1. **Architecture First:** The core ingestion pipeline, DLQ handling, and data schemas must stabilize before any specific ML heuristics are coded.
2. **Observability First:** Implementing structured logging, traceback captures, and Prometheus endpoints precedes business logic.
3. **Contracts First:** APIs between the Next.js frontend, Go Gateway, and Python workers must be rigidly defined via OpenAPI/Swagger.
4. **No Premature Optimization:** Optimize Hot-Path vs Cold-Path separation early, but do not prematurely optimize batch sizes until benchmarked on production RTX 5070 nodes.
5. **Security & Privacy:** Default to the highest privacy settings (purging video after extracting necessary embeddings) until explicitly authorized by DPDP compliance reviews (G2 block).
