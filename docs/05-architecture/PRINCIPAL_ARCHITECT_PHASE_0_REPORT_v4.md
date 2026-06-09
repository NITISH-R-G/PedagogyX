# Principal Architect Phase 0 Report v4

**Owner:** Autonomous Principal Research Architect & Lead Systems Engineer
**Project:** PedagogyX
**Status:** In Progress
**Date:** 2026-06-05

## Phase 0 — Foundational Interrogation

Before embarking on significant architectural refactoring, coding, or pipeline deployment, it is imperative to align around core principles, risk domains, and long-term viability. The most common point of failure for deep-tech educational AI systems is a rush to build the MVP before adequately addressing the scale constraints and systemic realities of classroom data ingestion.

### Product Questions

- **Deployment Scope:** Is the system initially targeting K-12 public schools, high-end private institutions, universities, or corporate training environments? The risk profile for K-12 public is drastically higher, demanding significantly stricter compliance barriers.
- **Goal Dynamics:** What is the foundational objective? Is it teacher support/coaching (actionable self-reflection) or administrative oversight/punitive (surveillance-based evaluation)? Support models dramatically increase adoption.
- **Geographic Markets:** Do we focus exclusively on US/UK, or aggressively target India/Southeast Asia? Market dictates compliance (FERPA/GDPR vs. DPDP) and bandwidth availability.
- **Real-Time vs. Asynchronous Analytics:** Does the teacher need live dashboard feedback (requiring sub-second inference) or end-of-day asynchronous reports (permitting massive batch compute efficiencies)?
- **Hardware Integration Strategy:** Relying on fixed room cameras creates dead zones and installation bottlenecks. We are pivoting to mobile client-first architectures, specifically Meta Ray-Ban POV ingestion (as indicated by ADR-0009). Will this be subsidized, or BYOD?
- **Explainability Constraints:** If a teacher receives a pedagogical effectiveness score of 72/100, do they require line-by-line justification linked back to specific video timestamps?

### Technical Questions

- **Video Ingestion:** How will the edge clients handle spotty network connectivity? We need resilient chunked upload architectures utilizing multi-part REST or robust WebRTC buffering, rather than naive streaming.
- **Multimodal Alignment:** How do we sync audio, video, slide text (via OCR), and whiteboard ink in time space? Time-series synchronization pipelines are non-trivial when clocks skew on edge devices.
- **Latency & Streaming Inference:** If we must provide real-time engagement alerts, can we afford to round-trip to the cloud? Must we deploy lightweight YOLO/MobileNet models directly on the teacher's phone?
- **Audio Quality:** Classrooms are incredibly noisy. How are we structuring the microphone arrays or beamforming pipelines to isolate the teacher's voice from 30 overlapping students?
- **Storage Constraints:** High-res video across 10,000 classrooms equates to petabytes rapidly. What is the archival strategy? Will we aggressive downsample video after extracting semantic embeddings?
- **Identity & Compliance:** How do we handle incidental capture of students? Must we implement real-time edge face-blurring before video ever hits our cloud endpoints?
- **Vector Retrieval:** To enable an "AI Coach" over historical data, what vector database strategy (Milvus, Qdrant, Pinecone) offers the best latency for long-context educational history retrieval?

### Competitor Analysis

A rigorous assessment of the existing landscape reveals significant gaps that PedagogyX can exploit.

- **Edthena & IRIS Connect:**
  - _Strengths:_ Strong pedagogical frameworks, deep integration into teacher coaching models.
  - _Weaknesses:_ Primarily manual video annotation systems. Very limited autonomous AI insight generation. They rely on human coaches watching the video.
  - _Differentiator:_ PedagogyX will fully automate the insight pipeline, removing the human bottleneck.
- **Vosaic:**
  - _Strengths:_ Excellent timeline-based annotation UX.
  - _Weaknesses:_ Similar to Edthena, relies heavily on human effort. AI capabilities are bolted on, not fundamental.
- **AI Sokrates / Chinese Smart Classroom systems:**
  - _Strengths:_ Highly advanced computer vision, real-time engagement tracking, massive scale deployments.
  - _Weaknesses:_ Surveillance-heavy UX, often lacks explainability, extremely high infrastructure requirements (often requiring dedicated on-prem GPU servers per school).
  - _Differentiator:_ PedagogyX will provide comparable analytical depth using cloud-native, privacy-preserving architectures that focus on support rather than surveillance.
- **Zoom/Teams/Meet Educational Analytics:**
  - _Strengths:_ Built-in audience, massive distribution.
  - _Weaknesses:_ Useless for physical/hybrid classrooms. Limited pedagogical understanding; mostly generic meeting metrics.

### Research Papers

We are continuously indexing the scientific literature to inform our models. Critical domains include:

- **Affective Computing & Speech Emotion Recognition:** Analyzing how the teacher's vocal prosody correlates with student engagement.
- **Multimodal Transformers in Education:** Using long-context models to ingest 45-minute lesson transcripts alongside action-recognition visual features.
- **Teacher Effectiveness Modeling:** Mapping specific conversational turn-taking patterns (Teacher-Initiation, Student-Response, Teacher-Evaluation) to learning outcomes.
- **Privacy-Preserving Edge AI:** Techniques for edge-based semantic extraction to minimize raw PII transmission.

### Architecture Phase

The target architecture must be designed for eventual consistency, high throughput, and robust privacy barriers.

- **Client Layer:** Android/iOS companion apps interfacing with Meta Ray-Bans (DAT toolkit). Handles local caching, edge face-blurring (future roadmap), and secure chunked uploads to cloud storage.
- **Ingestion & Orchestration:** API gateway routes media files to raw S3 buckets. An event-driven architecture (e.g., Kafka or SQS) triggers the processing pipeline.
- **Multimodal Pipeline:**
  1. _Speech-to-Text:_ Whisper-v3 or similar for highly accurate transcription with speaker diarization.
  2. _Computer Vision:_ Frame extraction -> OCR (slides/whiteboard) + Action Recognition (teacher movement, student general engagement).
  3. _Semantic Fusion:_ Aligning transcript timestamps with visual context.
- **Intelligence Layer:** LLM-based pedagogical analysis. Prompting large context models (e.g., Claude 3.5 Sonnet / GPT-4o) with the fused timeline to generate coaching insights.
- **Storage Strategy:** Relational data (Postgres) for users/schools, Vector DB (Qdrant/Milvus) for semantic embeddings, Object Storage (S3) for media.

### Tech Stack Analysis

#### Backend

- **Choice:** Python (FastAPI) + Node.js (Next.js backend functions).
- **Rationale:** Python is non-negotiable for seamless ML integration and pipeline orchestration. Node.js handles the high-concurrency, low-latency API gateway and frontend serving needs efficiently.

#### AI/ML

- **Choice:** PyTorch + ONNX Runtime.
- **Rationale:** PyTorch is the undisputed research standard, allowing rapid adoption of new papers. ONNX provides the inference optimization necessary for cost-effective cloud deployments and potential edge push.

#### Databases

- **Choice:** Postgres (Primary), Redis (Caching/Queues), Qdrant (Vector).
- **Rationale:** Postgres is battle-tested. Qdrant offers excellent performance and rust-based reliability for complex filtering (e.g., "find all times this specific teacher used open-ended questions").

#### Infrastructure

- **Choice:** Dockerized services orchestrated by Kubernetes (EKS/GKE), transitioning to serverless components for highly burstable ML tasks where appropriate.
- **Rationale:** Kubernetes provides the control plane needed to schedule massive GPU workloads dynamically based on daily processing peaks (post-school hours).

### AI Features

Priority pipeline sequence:

1. **High-Fidelity Transcription & Diarization:** The absolute baseline. If we don't know exactly what the teacher said, all higher-level analysis fails.
2. **Pedagogical Event Timelines:** Automatically chunking the lesson into segments (Direct Instruction, Group Work, Q&A, Independent Practice).
3. **Teacher Talk vs. Student Talk Ratio:** A classic, proven metric of classroom dynamics.
4. **Question Quality Analysis:** Differentiating between low-level recall questions and high-level analytical questions.
5. **Slide & Whiteboard Semantic Extraction:** Understanding the _content_ being taught to provide context-aware coaching.

### Agile Requirements

- **Sprint Cadence:** 2-week sprints.
- **Epic Structure:** Organized by architectural domains (e.g., Ingestion Pipeline, Transcription Engine, Coaching Dashboard).
- **Issue Tracking:** Strict adherence to Definition of Done (DoD) requiring unit tests, architectural review (ADRs), and performance benchmarking for any ML pipeline component.
- **Backlogs:** Maintained separately for Engineering, Research (model evaluation), and Product.

### Documentation Requirements

- All architectural decisions must be documented via ADRs (Architectural Decision Records) in `docs/08-rfc-adr/`.
- All APIs must be documented using OpenAPI specs (auto-generated via FastAPI).
- Complex dataflows must be visualized using Mermaid.js within the documentation markdown.
- System Architecture, Data Governance, and Privacy Architecture must be maintained as living documents.
