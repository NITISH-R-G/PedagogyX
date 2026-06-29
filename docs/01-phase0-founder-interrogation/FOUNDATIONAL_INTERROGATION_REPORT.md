# Phase 0: Foundational Interrogation Report

**Status:** Phase 0 Active
**Author:** Autonomous Principal Research Architect & Lead Systems Engineer
**Domain:** Deep-tech Educational AI Platform (PedagogyX)

## Product Questions

The following questions probe the core product vision, market strategy, and ethical boundaries:

- **Primary Customer:** Is the platform built primarily as an empowerment tool for teachers, or a supervision and compliance tool for administrators? How do we balance both if they conflict?
- **Global Compliance & Privacy:** Given the Day 1 launch in India (DPDP compliance required) and potential future expansion to regions with FERPA and GDPR, what is the strategy for strict data localization and biometric consent?
- **Consent & Anonymization:** How do we handle parent requests to "forget" their child's data in recorded sessions? Are we implementing deterministic blurring of student faces at the edge?
- **Pedagogical Evaluation:** What specific pedagogical frameworks (e.g., Danielson Framework, CLASS, or custom rubrics) will the AI evaluate against?
- **AI Scoring Visibility:** Is the AI's "Pedagogy Score" public to administrators or kept private to the individual teacher for self-improvement?
- **Market & Pricing Assumptions:** If the budget per classroom for the pilot is ₹0/$0, how do we subsidize the high cost of GPU inference without bleeding capital?

## Technical Questions

Critical technical interrogations to resolve before implementation:

- **Hardware Limitations (Meta Ray-Ban):** The primary v1 client relies on Meta Ray-Ban glasses. How do we address their limited battery life (~4 hours max) and potential heat dissipation issues during a continuous 50-minute recording?
- **Offline & Low-Bandwidth Scenarios:** For schools with poor internet connectivity, what local storage capacity is required on the Android companion app? Do we employ a low-bandwidth mode uploading audio first and video later?
- **Multimodal Sync & Drift:** What is the acceptable drift tolerance when synchronizing Ray-Ban POV video and audio from the teacher's mic?
- **Acoustic Challenges:** Classroom environments are highly reverberant. Can the teacher's lapel/glasses mic accurately capture questions from students in the back row? If not, how do we prevent skewed interaction analytics?
- **Edge vs. Cloud ML:** The D-PROC model is Hybrid (LAN edge + India cloud GPU). How are we scaling concurrent ingest from 1,000+ classrooms finishing at the same time?
- **Hallucination Prevention:** How do we mitigate the risk of the LLM hallucinating negative feedback, which could severely impact a teacher's career?

## Competitor Analysis

An analysis of global competitors and adjacent systems:

- **Edthena / Vosaic / IRIS Connect:**
  - **Strengths:** Established presence in US schools; strong UX for coaching and human-in-the-loop annotations.
  - **Weaknesses:** Often rely on manual capture or single wide-angle cameras; limited automated multimodal AI inference.
  - **Opportunities:** Disruption via frictionless capture (Meta Ray-Bans) and automated, objective pedagogical insights.
- **Chinese Smart Classroom Systems:**
  - **Strengths:** High automation; extensive use of computer vision for continuous student engagement tracking.
  - **Weaknesses:** Heavy reliance on continuous, unconsented facial emotion recognition, creating massive ethical and cultural friction outside of China.
  - **Opportunities:** Offering a privacy-preserving alternative that focuses on teacher pedagogy rather than student surveillance.
- **AI Meeting Intelligence (Zoom AI, Read.ai):**
  - **Strengths:** Exceptional at general meeting summarization, talk-time ratios, and simple speech metrics.
  - **Weaknesses:** Lack of specialized educational context; incapable of measuring true pedagogical effectiveness or classroom dynamics.

## Research Papers

Extensive scientific literature review must inform our AI systems:

- **Multimodal AI & Transformers:** Research on late vs. early fusion techniques for audio-visual alignment in reverberant environments.
- **Educational Data Mining & Learning Analytics:** Studies detailing the correlation between specific teacher discourse patterns (e.g., wait time, question types) and student outcomes.
- **Affective Computing:** Evaluating the validity and cultural biases inherent in speech emotion recognition and skeletal tracking as proxies for student engagement.
- **LLMs in Pedagogy:** Recent papers exploring the capabilities of smaller, quantized LLMs (like Qwen 2.5) to act as instructional coaches compared to larger frontier models.
- **Privacy-Preserving Machine Learning:** Techniques for running inference at the edge to avoid centralizing PII and biometric data.

## Architecture Phase (Tech Stack Analysis)

Exhaustive comparison of technologies to form our production stack:

- **Backend:**
  - _Candidates:_ Go, Rust, Python (FastAPI), Node.js, Java.
  - _Decision Matrix:_ Python (FastAPI) provides native integration with ML ecosystems, though Rust/Go may be evaluated later for high-concurrency event ingestion pipelines.
- **AI/ML:**
  - _Candidates:_ PyTorch, TensorFlow, JAX, ONNX, TensorRT.
  - _Decision Matrix:_ PyTorch combined with TensorRT for optimized cloud inference on our targeted RTX 5070 hardware budget.
- **Video Pipelines:**
  - _Candidates:_ FFmpeg, GStreamer, WebRTC.
  - _Decision Matrix:_ A mix of WebRTC for live telemetry and FFmpeg for robust edge buffering and chunked upload to our backend.
- **Databases:**
  - _Candidates:_ Postgres, ClickHouse, Qdrant/Milvus/Weaviate.
  - _Decision Matrix:_ Postgres for relational state and RBAC; a vector database (e.g., Weaviate/Qdrant) for multimodal embeddings and temporal classroom events.
- **Infrastructure & Cloud:**
  - _Candidates:_ AWS, GCP, self-hosted GPU clusters.
  - _Decision Matrix:_ Self-hosted GPU clusters initially to contain costs during the unmonetized pilot phase, with Kubernetes managing container orchestration.

## AI Features

Key AI features requiring deep feasibility research:

- **Teacher Speech & Pedagogy Analysis:** Measuring talk-to-listen ratios, speech clarity, instructional pacing, and question distribution (open vs. closed questions).
- **Multimodal Event Timelines:** Correlating slide semantic analysis with spoken words and gaze estimation to build a complete lesson timeline.
- **Hallucination-Resistant Coaching:** Generating automated, rubric-aligned feedback that explicitly states its confidence score and relies strictly on cited video evidence.
- **Privacy-Safe Engagement Metrics:** Calculating classroom-level engagement proxies (e.g., aggregate noise levels, generic pose estimation) without performing facial recognition on minors.
- **Longitudinal Analytics:** Tracking teacher improvement across multiple sessions, visualizing the adoption of recommended pedagogical strategies over time.

## Scrum & Agile Requirements

To maintain rigorous development standards:

- **Backlog Management:** Strict maintenance of Product, Technical, and Research backlogs. All work must be linked to epics and detailed user stories.
- **Milestone Tracking:** Clear dependency graphs, especially between edge client development (Meta Ray-Ban DAT) and cloud API availability.
- **RFCs and ADRs:** Mandatory documentation of all architectural decisions and tradeoff analyses before implementation.
- **Ceremonies:** Regular sprint planning and retrospectives to address technical debt and rapidly iterate on founder feedback.

## Documentation Requirements

Extensive technical documentation must precede implementation:

- **System Architecture & Data Governance:** Diagrams and documents detailing data flow, privacy boundaries, and edge-to-cloud sync protocols (RFC-0002).
- **Compliance Analysis:** Thorough review against India DPDP and subsequent regulations, focusing on anonymization pipelines.
- **ML Ops Strategy:** Defined pipelines for model evaluation, synthetic data generation, and prompt engineering strategies.
- **Testing Strategy:** Rigorous benchmark-driven development and unit/integration testing frameworks.
- **Infrastructure as Code:** Complete documentation for the deployment architecture, GPU optimization, and observability stack.
