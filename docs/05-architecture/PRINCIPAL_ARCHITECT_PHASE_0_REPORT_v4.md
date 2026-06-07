# Principal Architect Phase 0 Report v4

**Owner:** Autonomous Principal Research Architect & Lead Systems Engineer
**Project:** PedagogyX
**Status:** In Progress
**Date:** 2026-05-27

## Core Objective and Execution Philosophy

Our mission is not to rush an MVP. PedagogyX aims to be one of the most advanced AI-powered classroom intelligence and teacher optimization platforms globally. We mandate an exhaustive research, architecture, and planning phase equivalent to 30 days of effort before significant code is written. We operate as a hybrid of a DeepMind research division, MIT Media Lab, and elite enterprise architecture team.

## Phase 0 — Foundational Interrogation

### Product Questions

We must demand clarity from the founders on the core purpose of this system:

- **Core Modality:** Is this for instructional coaching (supportive) or surveillance (punitive)? If deployed in Indian districts, will the evaluation be state-mandated?
- **Privacy & Compliance:** What are the exact implications of India's DPDP, GDPR, and FERPA? Is capturing minor biometrics (faces, voices) permitted? Can we implement a privacy-first architecture that strictly purges raw video post-inference and maintains only abstract embedding vectors?
- **Hardware Topology:** Given the pivot to Meta Ray-Ban POV client architectures (ADR-0009), how do we handle battery life, teacher comfort, and variable classroom lighting compared to fixed IP cameras?
- **SaaS Dynamics:** Is this enterprise B2B for wealthy private schools, or large-scale, low-cost deployment for public districts?
- **Network Realities:** Can we guarantee low-latency, high-bandwidth school networks? No. Our edge architecture must assume prolonged WAN dropouts and operate in an offline or heavily buffered mode.
- **AI Specifics:** Should the AI explicitly score pedagogy according to rubrics like the Danielson Framework? Should we detect emotional tone and student engagement? Is explainable AI mandatory?

### Technical Questions

- **Scalability & Inference:** Can our cloud inference handle concurrent cold-path ASR and Vision fusion from hundreds of simultaneous DAT-host Android devices? Can we safely scale using RTX 5070 constraints?
- **Synchronization Pipeline:** What is the precise mechanism for aligning POV video from Ray-Bans with audio tracks captured at varying sampling rates?
- **Storage Architecture:** Are we persisting the raw multimedia payloads, or strictly processing them ephemerally? If we require historical data for longitudinal analytics, what is the cold storage strategy?
- **Distributed ML:** Is it feasible to push lightweight inference (e.g., Voice Activity Detection) down to the Android companion app to save bandwidth, or must everything be processed centrally?
- **Observability:** How do we trace a single classroom session's data flow from the Meta Ray-Bans, through the Android client, to the ingestion API, and across multiple asynchronous AI workers?

## Research Phase

### Competitor Analysis

- **Edthena & Vosaic:**
  - _Architecture/Stack:_ Likely monolithic or traditional microservices relying on manual tagging and uploaded fixed-camera video.
  - _Weaknesses:_ High friction in capture, requiring significant CapEx for classroom setups.
  - _Opportunities:_ Our Meta Ray-Ban POV architecture bypasses expensive installations, reducing onboarding friction to zero.
- **IRIS Connect:**
  - _Strengths:_ Strong integration with established coaching frameworks.
  - _Weaknesses:_ Limited automated AI analysis.
- **AI Sokrates:**
  - _Architecture:_ NLP-heavy text analysis based on transcripts.
  - _Weaknesses:_ Ignores non-verbal cues.
  - _Opportunities:_ We integrate spatial and kinesic tracking, creating a true multimodal index superior to purely lexical analysis.
- **Chinese Smart Classrooms (Hanwang, Tencent):**
  - _Architecture:_ Massive surveillance-grade infrastructure, heavy centralized GPU processing.
  - _Weaknesses:_ Legally non-compliant in GDPR/DPDP regions.
  - _Opportunities:_ We must build a privacy-first, verifiable system that offers similar analytical depth without panoptic capture.
- **Zoom AI / Microsoft Teams / Google Meet:**
  - _Architecture:_ Cloud-native, optimized for real-time webRTC streams.
  - _Weaknesses:_ General-purpose meeting intelligence, not aligned with pedagogical rubrics.

### Research Papers

We will continuously index literature across the following domains:

- **Multimodal Learning Analytics (MMLA):** Fusing prosody, kinesics, and semantics provides significantly stronger correlations to pedagogical effectiveness than unimodal analysis.
- **Speech Emotion Recognition (SER):** Generic off-the-shelf Whisper models degrade under heavy Indian code-switching and classroom noise. We must evaluate specialized or fine-tuned variants.
- **Long-Context Video Understanding:** Architectures such as Qwen-VL or Gemini 1.5 Pro equivalents are essential for holistic classroom segment analysis, allowing for reasoning across temporal events.
- **Pedagogical Alignment:** Converting qualitative rubrics into embedded vectors for Retrieval-Augmented Generation (RAG) to ensure AI coaching is grounded in recognized educational theory.

## Architecture Phase

We demand a WORLD-CLASS architecture encompassing system diagrams, sequence flows, ML pipelines, and deployment strategies.

### Mandatory Tech Stack Analysis

#### Backend

- **Go:** Superior for the ingestion gateway due to unparalleled concurrency handling and low latency during heavy edge-client uploads.
- **Rust:** Excellent memory safety, but slower iteration speed compared to Go for the API layer.
- **Python (FastAPI):** Mandatory for the core ML orchestration and worker tier due to native ecosystem integration (PyTorch, HuggingFace).
- **Node.js/Java:** Not recommended for the core high-throughput multimedia pipeline.

#### AI/ML

- **PyTorch:** Standard for model research and training.
- **ONNX/TensorRT:** Essential for maximizing inference optimization and GPU efficiency on our RTX 5070 clusters during cold-path batch processing.
- **JAX/TensorFlow:** PyTorch is preferred for its dynamic computation graph and research prevalence.

#### Video Pipelines

- **FFmpeg:** Selected for robust chunking and format normalization on the edge and server side.
- **GStreamer/WebRTC:** To be evaluated for any real-time streaming requirements, though asynchronous processing is preferred.

#### Databases

- **PostgreSQL (pgvector):** Selected for unified state management and vector retrieval, reducing operational complexity.
- **ClickHouse:** Potential future addition for high-volume telemetry and analytics.
- **Redis:** Selected for managing asynchronous Dead Letter Queues (DLQ) and hot-path caching.
- **Weaviate/Qdrant:** May be evaluated if pgvector hits scaling limits for our knowledge graphs.

#### Frontend

- **Next.js/React:** Server-side rendering guarantees performance on lower-end devices typically used by K-12 administration.
- **Flutter/Electron:** Flutter/Kotlin for the Android companion app (DAT client).

#### Infrastructure & Cloud

- **Docker/Kubernetes:** Compose for edge nodes and development (`compose.dev.yaml`), K3s/K8s for central cloud orchestration.
- **Self-Hosted GPUs (RTX 5070):** Required to manage OPEX, handle heavy video processing, and satisfy data residency laws.
- **AWS/GCP:** Used for control plane, object storage, and non-GPU workloads.

### AI Features to Research

- **Teacher Emotion Analysis & Speech Clarity:** Real-time VAD processing and tone analysis.
- **Classroom Engagement Heatmaps:** Correlating student gaze and posture with teacher activity.
- **Pedagogical Pattern Detection:** Analyzing the sequence of question-asking, student response, and teacher feedback (e.g., measuring 'wait time').
- **Multimodal Event Timelines:** Correlating visual cues with audio events across a timeline.
- **Hallucination-Resistant RAG Coaching:** Ensuring all AI-generated feedback strictly cites transcript timestamps and references institutional guidelines.
- **Semantic Slide Analysis:** OCR and multimodal understanding of whiteboard/slide content synchronized with speech.

## Scrum & Agile Requirements

We will maintain strict Agile workflows:

- **Backlogs:** Product, technical, and research backlogs with detailed epics, stories, and tasks.
- **Rituals:** Sprint planning, retrospectives, and rigorous grooming.
- **Documentation:** All major architectural decisions must be recorded via RFCs and ADRs (e.g., ADR-0009).
- **Technical Debt:** Dedicate sprint capacity to observability improvements and refactoring.

## Documentation Requirements

The system must maintain exhaustive, continuously updated documentation before coding begins:

- Product Requirements Document (PRD)
- System Architecture & Data Governance Specs
- Multimodal Inference Pipeline Diagram
- Privacy Architecture and ML Ops Strategy
- Observability and Telemetry Standards
- Synthetic Data Generation and Prompt Engineering Guides
- Benchmark-driven Development Guidelines

## Engineering Philosophy and Rules

1. **Architecture First:** The core ingestion pipeline, DLQ handling, and data schemas must stabilize before any specific ML heuristics are coded.
2. **Observability First:** Implementing structured logging, traceback captures, and Prometheus endpoints precedes business logic.
3. **Contracts First:** APIs between the Next.js frontend, Go Gateway, and Python workers must be rigidly defined via OpenAPI/Swagger.
4. **No Premature Optimization:** Optimize Hot-Path vs Cold-Path separation early, but do not prematurely optimize batch sizes until benchmarked on production nodes.
5. **Security & Privacy:** Default to the highest privacy settings (purging video after extracting necessary embeddings) until explicitly authorized by DPDP compliance reviews.
