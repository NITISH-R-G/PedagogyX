# Phase 0 Architecture Report: PedagogyX

## Product Questions

- **Target Market & Jurisdiction**: Are we primarily targeting US K-12, US Higher Education, or an international market? Is FERPA compliance the only requirement, or do we also need to satisfy GDPR or India's DPDP?
- **Platform Scope**: Is this a B2B Enterprise SaaS tool for schools, or a B2C tool directly for teachers to self-improve? Will administrators have access to a teacher's pedagogy scores? If yes, how do we handle teacher unions?
- **AI Scope**: Is the AI designed to replace instructional coaches or to augment them? Should the AI score the teacher directly, or merely provide neutral observations? Will the AI analyze student faces for engagement, and is biometric tracking legally permitted?
- **Operational Reality**: Will this system run locally on school edge servers to satisfy privacy, or is it a cloud-native platform? Does it need an offline mode for schools with poor connectivity? Is the analysis real-time (live dashboard) or post-processed?

## Technical Questions

- **Infrastructure**: What are our expected ingestion rates per hour? Do we need to transcode 4K video locally via edge computing or upload raw to the cloud? Can we handle synchronous multimodal pipelines (audio + video + slides)?
- **Data Privacy**: How do we handle PII redaction (blurring faces, silencing names) before the data hits our cloud processing pipeline? Do we need a federated learning model to train on school data locally?
- **Hardware Topology**: Will classrooms use Meta Ray-Bans exclusively, or will there be ceiling-mounted 360 cameras, boundary microphones, and screen-capture agents on the teacher's laptop?
- **AI Models & Latency**: For real-time processing, can we run lightweight Whisper and a distilled Vision Transformer on an edge device (e.g., NVIDIA Jetson)? Or must we offload to an A100 GPU cluster? What is the acceptable latency budget for transcription?
- **Storage Strategy**: Should we utilize an S3-compatible object store combined with a vector database (e.g., Weaviate/Milvus) for semantic search of classroom moments, alongside a graph database to model knowledge gaps over time?

## Competitor Analysis

| Competitor      | Probable Stack / Approach                   | Strengths                                 | Weaknesses                                          | Business Model  | Opportunities for Disruption                                           |
| :-------------- | :------------------------------------------ | :---------------------------------------- | :-------------------------------------------------- | :-------------- | :--------------------------------------------------------------------- |
| **Edthena**     | Cloud-based video upload, basic ML tagging. | Strong market presence, teacher-friendly. | Lacks deep multimodal AI, slow manual processing.   | B2B SaaS        | We can automate the tagging and feedback loop instantly using LLMs.    |
| **Vosaic**      | Video platform with timeline-based coding.  | Good UX for researchers and coaches.      | Highly manual. Very little autonomous intelligence. | B2B / Higher Ed | Introduce automated event timelines and pedagogical pattern detection. |
| **AI Sokrates** | NLP-heavy transcript analysis.              | Good conversational analysis.             | Lacks visual and multimodal integration.            | B2B SaaS        | Add vision transformers to fuse slide context with the spoken audio.   |

## Research Papers

- **Title**: _Multimodal Transformers for Educational Activity Recognition_
  - **Summary**: Explores using Vision Transformers fused with audio embeddings to categorize classroom activities (e.g., lecture, group work, silence).
  - **Limitations**: High compute requirements, tested mostly on synthetic data.
- **Title**: _Speech Emotion Recognition in Educational Contexts_
  - **Summary**: Uses CNNs and RNNs on mel-spectrograms to detect teacher enthusiasm and frustration, correlating with student engagement.
  - **Limitations**: Sensitive to classroom noise and poor microphone quality.
- **Title**: _Long-Context Video Understanding with Large Language Models_
  - **Summary**: Discusses using sparse attention mechanisms in LLMs to process 45-minute video transcripts and visual keyframes simultaneously.
  - **Limitations**: Prompt length limitations and hallucination risks when inferring pedagogy.

## Architecture Phase

The PedagogyX architecture will utilize an event-driven, hybrid edge-cloud model to maximize privacy and reduce bandwidth costs.

- **Edge Layer (Classroom)**: Devices (Meta Ray-Bans, local microphones) stream to an edge node (e.g., a local server or teacher's laptop). The edge node performs basic PII redaction and compresses the streams.
- **Ingestion Pipeline**: Data flows into cloud via standard protocols (WebRTC for live, chunked HTTPS uploads for post-processing). An API Gateway directs traffic.
- **Multimodal Processing (Cloud)**:
  - **Audio Pipeline**: Custom Whisper models for diarization and transcription.
  - **Vision Pipeline**: Frame extraction followed by Vision Transformers (ViT) to analyze whiteboard content and student body language (non-facial).
  - **Fusion Engine**: A multimodal transformer aligns audio transcripts with visual frames chronologically.
- **Data Storage**: PostgreSQL for relational data, S3 for raw/processed video, and Qdrant/Milvus for vector embeddings of pedagogical moments.
- **Agent Orchestration**: A large language model (e.g., GPT-4 or fine-tuned Llama-3) acts as the pedagogical coach, querying the vector database to generate personalized teacher feedback.

## Tech Stack Analysis

### Backend

- **Go**: High concurrency, excellent for event-streaming and high-throughput video pipelines. **(Chosen for Ingestion/Streaming)**
- **Python**: Deepest ecosystem for ML/AI integration. **(Chosen for Processing Pipelines/Agents)**

### Databases

- **PostgreSQL**: Robust, standard relational data.
- **ClickHouse**: Exceptional for time-series analytics (e.g., engagement metrics over a 45-minute class).
- **Weaviate**: Vector database chosen for its hybrid search capabilities.

### AI / ML

- **PyTorch**: Industry standard for research and deployment.
- **TensorRT**: Used to optimize inference on cloud GPUs.

### Infrastructure & Cloud

- **Kubernetes**: Standard for orchestrating the microservices.
- **AWS**: Preferred for scaling GPU instances (EC2 p4d instances) dynamically.

## AI Features

- **Automated Lesson Summaries**: Generating a structured breakdown of the lesson using LLMs.
- **Teacher/Student Speaking Ratio**: Precise diarization to show how much the teacher spoke vs. students.
- **Pedagogical Pattern Detection**: Identifying when a teacher uses open-ended vs. closed-ended questions.
- **Slide Semantic Analysis**: OCR on slides to correlate what the teacher is saying with the visual content.
- **Engagement Heatmaps**: Using pose estimation (privacy-preserving) to gauge aggregate classroom attention.

## Agile Requirements

- **Sprint 1-2**: Finalize privacy and legal compliance matrices. Confirm target jurisdictions.
- **Sprint 3-4**: Build the foundational ingestion pipeline (dummy data) and establish Kubernetes infrastructure.
- **Sprint 5-6**: Develop the isolated audio pipeline (diarization and transcription on edge/cloud).
- **Sprint 7-8**: Develop the isolated vision pipeline (frame extraction, basic OCR).
- **Sprint 9-10**: Build the multimodal fusion engine and vector database integration.

## Documentation Requirements

- **Product Requirements Document (PRD)**: Detailed scope, out-of-scope, and user personas.
- **System Architecture Document**: High-level and component-level diagrams.
- **Data Governance & Privacy Framework**: Strict guidelines on PII redaction, data retention, and compliance (FERPA/GDPR).
- **ML Ops Strategy**: Protocols for model deployment, monitoring, and continuous training with synthetic data.
- **Security Architecture**: Detailing encryption at rest/transit, RBAC, and zero-trust principles.
