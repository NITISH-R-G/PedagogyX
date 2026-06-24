# Principal Architect Phase 0 Report v4

**Owner:** Autonomous Principal Research Architect & Lead Systems Engineer
**Project:** PedagogyX
**Status:** In Progress
**Date:** 2026-05-27

## Phase 0 — Foundational Interrogation

Before proceeding with any structural code generation, we must interrogate the core product tenets. Too many AI startups fail because they build highly complex multimodal pipelines without fully understanding their legal, pedagogical, and scale constraints.

### Product Questions

- **Customer Profiling:** Is this enterprise SaaS targeting wealthy private schools, or a state-mandated evaluation platform targeting public districts? (Current founder answers indicate a hybrid model for India, focusing on K-12 and university, potentially scaling globally).
- **Surveillance vs. Coaching:** Is the platform built for surveillance (punitive) or instructional coaching (supportive)? The implementation of "China-style supervision" in specific markets requires strict architectural boundaries to prevent privacy leaks. Is human review mandatory? Should the AI score pedagogy? Should the AI evaluate student engagement?
- **Hardware & Latency Constraints:** Can we assume low-latency, high-bandwidth school networks? No. Our architecture must buffer at the edge and withstand prolonged WAN dropouts. Is this for offline mode? Is this cloud-native?
- **Compliance & Geography:** What are the exact requirements for DPDP compliance in India regarding the capture of minor biometrics (faces, voices)? We must implement privacy-first models that purge raw video and maintain only embedding vectors or non-reversible states where legal mandates dictate. Is FERPA or GDPR compliance required? Is student facial analysis allowed?
- **Deployment Modality:** The shift from fixed smartboards to Meta Ray-Ban POV client architectures (ADR-0009) vastly changes our network ingestion layer. How do we ensure teacher comfort, safety, and battery life during a full day?

### Technical Questions

- **Scalability & Inference:** Can our cloud inference handle concurrent cold-path ASR and Vision fusion from hundreds of simultaneous DAT-host Android devices? Can we safely scale using RTX 5070 constraints?
- **Synchronization:** What is the precise mechanism for aligning POV video from Ray-Bans with audio tracks that might be captured at different sampling rates?
- **Storage Strategy:** Are we persisting the raw multimedia payloads, or strictly processing them ephemerally?
- **Federated vs. Centralized ML:** Is it feasible to push lightweight inference (e.g., VAD) down to the Android companion app to save bandwidth, or must everything be processed centrally?
- **ML Ops:** How will we handle data labeling, annotation workflows, synthetic data generation, and model retraining while maintaining privacy?
- **Observability & Security:** What is the required observability stack? How do we implement role-based access control? Is privacy-preserving ML required?

## Research Phase

### Competitor Analysis

Our research analyzed major systems globally, including: Edthena, Vosaic, IRIS Connect, AI Sokrates, Chinese Smart Classroom systems, multimodal classroom research systems, lecture capture systems, corporate training intelligence systems, Zoom AI analytics, Microsoft Teams teaching analytics, Google Meet educational analytics, and AI meeting intelligence tools.

#### Edthena

- **Architecture Assumptions:** Video upload portal with asynchronous feedback workflows.
- **Strengths:** Strong pedagogical frameworks, deep market penetration in US K-12.
- **Weaknesses:** Highly manual, lacks real-time multimodal intelligence.
- **Opportunities for Disruption:** Automate the feedback loop with multimodal transformers instead of relying entirely on peer or mentor review.

#### Vosaic

- **Architecture Assumptions:** Cloud-based video annotation and timeline mapping.
- **Strengths:** Excellent timeline-based UX for coding behaviors.
- **Weaknesses:** Requires manual coding of events.
- **Opportunities for Disruption:** Zero-shot classroom activity recognition to auto-code timelines.

#### Chinese Smart Classroom Systems (e.g., Tencent Cloud Education)

- **Architecture Assumptions:** Edge compute boxes fused with multiple 4K PTZ cameras, continuous streaming, massive centralized analytics.
- **Strengths:** Deep integration, real-time engagement and facial analysis.
- **Weaknesses:** Unacceptable privacy implications for Western or Indian markets, highly surveillance-oriented.
- **Opportunities for Disruption:** Provide edge-based, privacy-first anonymization that extracts instructional patterns without persisting student PII.

### Research Papers

We continuously search for and summarize papers covering: multimodal AI, classroom analytics, educational data mining, affective computing, speech emotion recognition, engagement detection, pedagogical analysis, teacher effectiveness modeling, instructional design, classroom discourse analysis, computer vision for education, multimodal transformers, long-context video understanding, classroom activity recognition, educational reinforcement learning, AI coaching systems, and learning analytics.

_Selected key literature mapped for PedagogyX:_

1. **Long-context video understanding for instructional events:** Investigates how temporal window sizes affect the recognition of teaching phases (e.g., direct instruction vs. guided practice).
2. **Privacy-preserving classroom audio analysis:** Methods for performing speaker diarization and VAD at the edge.
3. **Multimodal fusion for student engagement:** Using body pose and audio cues to estimate cognitive load without facial recognition.

## Architecture Phase

### Mandatory Tech Stack Analysis

#### Backend

- **Go vs. Rust vs. Python vs. Node.js vs. Java:** Python is chosen for deep ML integration (FastAPI). Go is considered for high-throughput ingestion microservices if Node.js/Python become bottlenecks. Node.js is excellent for real-time signaling.
- **Decision:** Python (FastAPI) as the primary ML serving and API layer.

#### AI/ML

- **PyTorch vs. TensorFlow vs. JAX vs. ONNX vs. TensorRT:**
- **Decision:** PyTorch for research and training. Export to ONNX and run via TensorRT for maximum inference optimization on our consumer-grade RTX 5070 constraints.

#### Video Pipelines

- **FFmpeg vs. GStreamer vs. WebRTC vs. NVIDIA DeepStream:**
- **Decision:** WebRTC for live ingestion (from Meta Ray-Bans -> Android -> Cloud). FFmpeg for cold-path chunk processing. NVIDIA DeepStream to be evaluated for GPU-accelerated video analytics pipelines.

#### Databases

- **Postgres vs. ClickHouse vs. Cassandra vs. MongoDB vs. Vector DBs (Weaviate/Qdrant/Milvus/Neo4j):**
- **Decision:** PostgreSQL for relational state. Qdrant or Milvus for embedding retrieval (RAG). ClickHouse for high-volume telemetry and analytics.

#### Frontend

- **React vs. Next.js vs. Flutter vs. Electron:**
- **Decision:** React/Next.js for the core platform. Flutter for the mobile companion app.

#### Infrastructure & Cloud

- **Kubernetes vs. Docker Swarm vs. Serverless vs. Self-hosted GPU clusters vs. AWS/GCP:**
- **Decision:** Self-hosted GPU clusters or bare-metal providers to control costs with RTX 5070 hardware limitations. Kubernetes for orchestration. Strict offline capabilities or edge architectures for data residency compliance (India legal constraints).

### AI Features to Research

We are actively researching the feasibility and architecture for:

- Teacher emotion analysis and speech clarity scoring.
- Classroom engagement heatmaps and interaction graphs.
- Teacher/student speaking ratios and pedagogical pattern detection.
- Instructional pacing analysis.
- Whiteboard OCR and slide semantic analysis.
- Multimodal event timelines and automatic lesson summaries.
- Hallucination-resistant feedback and AI coaching agents.
- Longitudinal teacher analytics and educational knowledge graphs.
- Teaching style clustering and classroom anomaly detection.
- Burnout prediction and adaptive coaching recommendations.

## Scrum + Agile Requirements

We maintain rigorous agile workflows:

- Product, technical, and research backlogs.
- Sprint planning, retrospectives, and milestone tracking.
- RFC and ADR documents for every major architectural decision.
- Dependency graphs and technical debt tracking.

Tasks are broken down into Epics, Stories, Tasks, and Sub-tasks with strict Acceptance Criteria and Risk Scoring.

## Documentation Requirements

Extensive documentation is mandatory before coding. This includes:

- Product requirements document (PRD)
- System architecture and AI architecture
- Multimodal pipelines and data governance
- Privacy architecture and ML ops strategy
- Observability and infra deployment
- Scaling strategy and edge deployment
- Security architecture (Authentication, RBAC)
- Event streaming and benchmarking
- Testing strategy and synthetic data generation
- Annotation tooling and prompt engineering strategy
- Agent orchestration and GPU optimization
- Compliance, ethical, and cost analysis
- Classroom hardware requirements

## Important Engineering Philosophy

We prioritize:

- Scalability, privacy, and explainability.
- Educational usefulness and ethical safeguards.
- Research rigor and production readiness.
- Long-term maintainability.
- Modular architecture and event-driven systems.
- Observability-first engineering and AI eval pipelines.
- Infrastructure-as-code and benchmark-driven development.
- Typed APIs, fault tolerance, and enterprise security.

## Implementation Rules

Before any coding begins:

- Architecture must stabilize.
- Risks must be identified and technical tradeoffs analyzed.
- Scalability assumptions must be modeled.
- Research must be fully documented.

When coding begins, we follow strict sequence rules:

- Begin with foundations.
- Observability first.
- Infrastructure first.
- Contracts and schemas first.
- Testing and evaluation pipelines first.
- NEVER start by building UI screens randomly.
