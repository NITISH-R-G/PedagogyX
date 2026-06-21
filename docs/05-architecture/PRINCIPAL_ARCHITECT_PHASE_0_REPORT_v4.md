# Principal Architect Phase 0 Report v4

**Owner:** Autonomous Principal Research Architect & Lead Systems Engineer
**Project:** PedagogyX
**Status:** Under Review
**Date:** 2026-06-15
**Optimizing for:** Modular architecture, event-driven systems, scalable distributed systems, observability-first engineering, AI eval pipelines, reproducibility, infrastructure-as-code, research-grade experimentation, benchmark-driven development, typed APIs, fault tolerance, and enterprise security.

## Product Questions

Before beginning implementation, we must resolve fundamental product contradictions:

- **Deployment & Scaling:** Is the final product aiming for enterprise SaaS, or B2B integration into existing LMS platforms?
- **Privacy & Legality:** How do we handle GDPR, FERPA, and India DPDP compliance when using Meta Ray-Ban POV client architectures? Does capturing minor biometrics (faces, voices) require strict edge-only processing or federated learning?
- **Audience & Use Cases:** Are we optimizing for teacher self-improvement via autonomous coaching, or state-mandated evaluation? The tone and UI must adjust dramatically.
- **Hardware Profile:** What is the minimal viable internet bandwidth required per classroom to upload continuous streams, and do we require an offline sync mode for low-resource environments?

## Technical Questions

- **Video Ingestion:** With Meta Ray-Ban POV, how do we handle continuous DAT upload streams across varying connection qualities? Should we buffer entirely at the edge?
- **Audio Synchronization:** How do we accurately align independent classroom microphone arrays with POV audio, potentially at different sampling rates?
- **Scalability constraints:** Can our self-hosted inference clusters handle bursty workloads when schools synchronize simultaneously at 3 PM?
- **Storage Strategy:** Are we strictly processing media and keeping only embedding vectors (to satisfy privacy policies) or persisting original media?

## Competitor Analysis

- **Edthena & Vosaic:** Both rely heavily on manual tagging and expensive fixed-camera installations. Our Meta Ray-Ban DAT integration removes the hardware CapEx friction, allowing instantaneous adoption.
- **AI Sokrates:** Relies mostly on transcription (NLP-heavy text analysis). Their weakness is missing the spatial, kinesic, and emotional context of the classroom.
- **Chinese Smart Classrooms (Hanwang, Tencent):** Massive surveillance-grade infrastructure that lacks privacy safeguards. We will disrupt this via privacy-preserving embedded analytics.
- **Zoom / MS Teams Analytics:** Great for meeting intelligence, but completely unaligned with pedagogical frameworks like the Danielson Framework.

## Research Papers

- **Multimodal Learning Analytics (MMLA):** Combining kinesics, semantics, and prosody provides the most accurate correlation to student outcomes. (Key focus for our fusion model).
- **Speech Emotion Recognition (SER) in Noisy Environments:** Off-the-shelf ASR degrades rapidly. We will need robust Voice Activity Detection (VAD) and diarization specific to K-12 classroom acoustics.
- **Long-Context Video Understanding:** Architectures such as Qwen-VL or Gemini 1.5 Pro equivalents are essential for holistic, multi-minute classroom segment analysis.
- **Pedagogical Alignment:** Converting qualitative rubrics into embedded vectors for Retrieval-Augmented Generation (RAG) coaching.

## Architecture Design

Our architecture must prioritize an observability-first, event-driven scalable approach:

- **Edge Capture (Android DAT):** Buffering and local formatting using FFmpeg before sync.
- **Ingestion Layer:** Go-based high-concurrency gateway to process incoming streams and route them to cloud storage.
- **Event Streaming:** Redis-backed queues managing video and audio chunk processing via decoupled Python workers (`worker-cv`, `worker-asr`).
- **Data Persistence:** PostgreSQL with pgvector for relational data and semantic retrieval. MinIO/S3 for ephemeral media storage prior to embedding extraction.
- **Frontend Layer:** Next.js Server-Side Rendered dashboard to guarantee performance on lower-end devices.

## Tech Stack Analysis

- **Backend / API:** Python (FastAPI) for ML integration; Go for high-concurrency edge ingestion.
- **AI/ML:** PyTorch and ONNX/TensorRT for maximizing GPU (RTX 5070) utilization during cold-path batch inference.
- **Video Pipelines:** FFmpeg on the edge and server for reliable chunking and format normalization.
- **Databases:** PostgreSQL (pgvector) for state management and RAG retrieval. Redis for DLQ and hot-path caching.
- **Frontend:** Next.js and React for responsive, accessible dashboards.
- **Infrastructure:** Self-Hosted GPUs via K3s/K8s for data residency, docker-compose for MVP local dev.

## AI Features

- **Teacher Talk Time & Wait Time:** Real-time VAD processing to calculate pacing and instructional ratios.
- **Pedagogical Pattern Detection:** Analyzing the sequence of question-asking, student response, and teacher feedback.
- **Multimodal Event Timelines:** Correlating visual cues (e.g., student gaze direction) with audio (teacher volume/tone).
- **Hallucination-Resistant RAG Coaching:** Ensuring all AI-generated feedback strictly cites transcript timestamps and references institutional guidelines.

## Scrum/Agile Requirements

- **Sprint Cadence:** Two-week sprints with strict Sprint Planning, Retrospectives, and Backlog Grooming.
- **Technical Debt:** 20% of engineering bandwidth per sprint dedicated to observability improvements, refactoring, and benchmark testing.
- **Documentation:** ADRs (Architecture Decision Records) required before any major stack change (e.g., ADR-0009).
- **Epic Structuring:** Stories must contain explicit acceptance criteria and cannot merge without comprehensive unit/integration test coverage and DLQ fail-safes.

## Documentation Requirements

The system must maintain exhaustive, continuously updated documentation:

- **Product Requirements Document (PRD)**
- **System Architecture & Data Governance Specs**
- **Multimodal Inference Pipeline Diagram**
- **Observability and Telemetry Standards**
- **Synthetic Data Generation and Prompt Engineering Guides**
- **Privacy Architecture and Risk Tradeoffs**
