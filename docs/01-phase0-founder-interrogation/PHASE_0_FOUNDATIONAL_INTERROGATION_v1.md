# Phase 0: Foundational Interrogation

## Introduction

Before implementation begins for PedagogyX, this document serves as a foundational interrogation to clarify ambiguities, challenge assumptions, and force precise product decisions. As the principal research architect, my mandate is to eliminate vague architecture and ensure technical viability for a multimodal AI classroom intelligence platform.

## State of Knowledge

### Validated Facts

- **Target Market**: India (K-12 and universities) primarily, requiring strict DPDP compliance and data residency in the `ap-south-1` region.
- **Primary Client**: Meta Ray-Ban smart glasses via an Android companion app (DAT) replaces smartboards as the primary capture surface (ADR-0009).
- **Architecture**: Hybrid Edge/Cloud topology (ADR-0008). Hardware constraint: max 12GB VRAM per node at the edge.
- **Tech Stack**: Python (FastAPI), Node.js, PyTorch, ONNX, FFmpeg, PostgreSQL, Qdrant, Redis.
- **Objective**: Analyze teacher voice, classroom video, slides/whiteboard; measure pedagogical efficiency, student engagement, and generate continuous teaching feedback.

### Assumptions

- Schools have adequate bandwidth to upload compressed multimodal data if edge processing is insufficient.
- Meta Ray-Ban devices can capture high enough fidelity audio/video from the back of the classroom or teacher's perspective without overheating.
- Teachers will adopt wearable capture devices without significant pushback.
- School administrators are willing to pay for insights derived from this data.

### Hypotheses

- Analyzing teacher/student speaking ratios and temporal event modeling directly correlates with pedagogical efficiency.
- Multimodal embeddings combining speech emotion and classroom activity can predict student burnout and engagement.
- Edge AI (max 12GB VRAM) is capable of running optimized ONNX/TensorRT models for real-time speech and face blurring before uploading to the cloud.

### Speculative Ideas

- Real-time AI coaching agents whispering feedback into the teacher's ear via the Ray-Ban audio output.
- Longitudinal educational knowledge graphs that map a teacher's style evolution across their career.
- Hallucination-resistant lesson summaries automatically generated and sent to parents.

## 1. Product & Business Interrogation

### Target Audience & Licensing

- Is this strictly B2B (schools/universities), or is there a B2G (government) or B2C (individual teacher self-improvement) play?
- Will this be licensed as an enterprise SaaS platform, per-seat, or per-classroom?
- Are we targeting physical classrooms, hybrid setups, or fully online classes?
- Is offline mode required for rural Indian schools with intermittent connectivity?

### Privacy, Ethics & Compliance

- Is India DPDP compliance the _only_ strict requirement, or do we need GDPR/FERPA compliance for future markets?
- Is student facial analysis allowed under current DPDP interpretations?
- Is biometric analysis (e.g., student emotion, gaze tracking) legally and ethically permissible?
- Will the architecture require a privacy-first, edge-only processing model for PII, or is cloud processing acceptable if encrypted?
- Is China-style surveillance (constant monitoring) acceptable to the market, or must the system feel strictly like instructional coaching?
- Is human-in-the-loop review mandatory for generated feedback before teachers see it?

### Stakeholders & Governance

- Are teachers' unions involved or expected to block deployment?
- Can school administrators see raw teacher analytics, or is the scoring strictly private to the teacher for self-improvement?
- Should the AI score pedagogy on a standardized scale, or adapt to the school's specific rubric?

### Core Product Capabilities

- Should the AI detect emotional tone in the teacher's voice?
- Is it required to evaluate individual student engagement, or aggregate classroom engagement?
- Is multilingual support (e.g., Hindi, English, regional Indian languages) required for the NLP models?
- Is a low-bandwidth mobile-first dashboard required for teachers in low-connectivity areas?
- Is the feedback delivered in real-time, or via post-processing (e.g., end-of-day reports)?

## 2. Technical & Systems Interrogation

### Infrastructure & Scalability

- What is the expected concurrent latency budget for processing a 1-hour classroom session?
- Will inference pipelines run entirely on the cloud, or is edge-processing mandatory to reduce bandwidth?
- What are the specific GPU requirements for the cloud clusters? Are we bounded by H100 availability, or designing for ubiquitous L4/T4 GPUs?
- How will we manage GPU scheduling for bursty workloads (e.g., all classes ending at 3:00 PM)?

### Hardware & Data Capture

- Given the Meta Ray-Ban primary client, what are the battery and thermal constraints for 45-minute continuous recording?
- How do we handle classroom hardware topology if the Ray-Ban glasses run out of battery? Are there secondary capture devices?
- What is the expected audio quality? Do we need to deploy secondary microphone arrays to capture student responses clearly?
- How do we build synchronization pipelines if multiple devices (smart glasses + fixed cameras) are used?

### AI & Multimodal Inference

- How will we fuse multimodal data (teacher perspective video from glasses + audio + slide deck OCR)?
- What is the temporal event modeling strategy? Are we using sliding windows or long-context transformers?
- How will we handle live transcription in noisy Indian classroom environments (reverberation, overlapping speech, code-mixing)?
- What vector database architecture will scale for billions of multimodal embeddings generated per semester?

### Data Ops & ML Lifecycle

- How will we manage data labeling and annotation workflows for pedagogical efficiency? Who are the domain experts grading the ground truth?
- Is there a pipeline for synthetic data generation to bootstrap the models before G2 (real data) is unblocked?
- What is the strategy for model retraining? Will we employ federated learning to preserve privacy across different school districts?
- How do we prevent knowledge graph pollution when generating long-term teacher profiles?

### Security & Observability

- What is the distributed systems architecture for observability across edge devices (Android DAT) and cloud microservices?
- How strict is the role-based access control (RBAC)? Can an admin access a teacher's raw video?
- How are we securing the streaming pipelines from the Ray-Ban glasses to the Android companion app to the cloud?
