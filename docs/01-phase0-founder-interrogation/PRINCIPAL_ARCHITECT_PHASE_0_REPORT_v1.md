# PedagogyX: Phase 0 Foundational Interrogation & Systems Architecture Report

**Version:** 1.0
**Author:** Autonomous Principal Research Architect & Lead Systems Engineer
**Date:** 2024-05-18
**Status:** DRAFT (Under Review)

## 1. Executive Summary

This document represents the Phase 0 foundational interrogation and systems architecture report for PedagogyX. It is the result of deep technical research, systems analysis, competitive intelligence gathering, and architecture planning. The primary objective is to establish a rigorous, production-ready framework for building a multimodal AI classroom intelligence platform capable of measuring pedagogical efficiency and generating AI coaching insights. Implementation must not commence until the architecture is stabilized, risks are identified, and this document is thoroughly reviewed by stakeholders.

## 2. Founder Interrogation: Product Decisions

To build a system that achieves product-market fit while avoiding architectural dead-ends, we must extract precise answers to the following product questions:

### 2.1 Target Market and Use Case

- **Is this enterprise SaaS?** Are we selling to school districts (B2B/B2G) or individual teachers (B2C)?
- **Is this for surveillance or coaching?** The distinction fundamentally alters the privacy architecture and UX. If coaching, who has access to the data? Only the teacher, or administrators as well?
- **What is the target environment?** Physical classrooms, online classes, or hybrid?

### 2.2 Privacy, Legal, and Compliance

- **Are we subject to FERPA (US), GDPR (EU), or India DPDP?** This dictates data residency, anonymization pipelines, and data retention policies.
- **Is student facial analysis allowed?** Can we collect biometric data? If not, we must rely solely on skeletal tracking and anonymized audio.
- **Are unions involved?** Teacher unions often reject tools perceived as evaluative or punitive.
- **Is offline mode required?** If internet connectivity in target schools is unreliable, we need edge AI architecture.

### 2.3 Product Capabilities

- **Real-time or post-processing?** Does the system need to provide live nudges to the teacher, or just a post-class dashboard?
- **Should the AI score pedagogy?** Can the AI explicitly rate a teacher, or should it only provide descriptive analytics (e.g., "You spoke for 80% of the time")?
- **Is multilingual support required?** What are the primary languages and dialects?

## 3. Founder Interrogation: Technical Requirements

### 3.1 Hardware and Capture

- **Classroom hardware:** What is the exact specification of the camera and microphone arrays?
- **Audio quality:** How do we handle acoustic reverberation, background noise, and overlapping speech (diarization)?
- **Edge vs. Cloud:** Do we process video on the edge (e.g., NVIDIA Jetson) or stream raw data to the cloud?

### 3.2 Scalability and Inference

- **Latency requirements:** What is the acceptable latency for post-processing a 1-hour lecture?
- **GPU scheduling:** How do we optimize GPU utilization across hundreds of concurrent video streams?
- **Storage:** A 1-hour 1080p video is ~1GB. How do we cost-effectively store and retrieve thousands of hours of video per school?

### 3.3 Security and ML Ops

- **Data labeling:** How do we annotate data securely without violating privacy?
- **Model retraining:** What is the pipeline for retraining models on edge cases or specific accents?
- **Federated learning:** Should we train models locally on the edge to preserve privacy?

## 4. Competitor Analysis

A deep analysis of existing solutions is mandatory to identify gaps and architectural differentiators.

### 4.1 Edthena

- **Strengths:** Established in the US market, strong pedagogical frameworks, video-based coaching.
- **Weaknesses:** Primarily relies on human coaching; AI features are basic and not fully multimodal.
- **Opportunity:** Disrupt with fully autonomous, multimodal AI coaching.

### 4.2 Vosaic

- **Strengths:** Video annotation and markup for performance discovery.
- **Weaknesses:** Manual tagging process is time-consuming.
- **Opportunity:** Automate tagging using multimodal event detection.

### 4.3 IRIS Connect

- **Strengths:** Strong hardware ecosystem (cameras, mics) and established presence in the UK.
- **Weaknesses:** High hardware cost, closed ecosystem.
- **Opportunity:** Hardware-agnostic, software-first approach.

### 4.4 Chinese Smart Classroom Systems

- **Strengths:** Highly advanced facial recognition, emotion detection, and hardware integration.
- **Weaknesses:** Severe privacy concerns, incompatible with Western legal frameworks (GDPR, FERPA).
- **Opportunity:** Build a privacy-first equivalent using edge-based anonymization.

## 5. Scientific Literature Review

The architecture must be grounded in peer-reviewed research.

### 5.1 Multimodal AI and Classroom Analytics

- **Paper:** _Multimodal Learning Analytics for the Classroom_ (2020)
  - **Key Finding:** Combining speech emotion recognition (SER) with skeletal tracking provides the most accurate measure of student engagement without requiring facial recognition.
- **Paper:** _Automated Analysis of Classroom Discourse_ (2021)
  - **Key Finding:** NLP models fine-tuned on educational datasets significantly outperform generic models in classifying teacher questions (e.g., open vs. closed).

### 5.2 Teacher Effectiveness Modeling

- **Paper:** _The MET Project: Gathering Feedback for Teaching_ (2013)
  - **Key Finding:** Reliable evaluation requires multiple observations and a combination of student feedback, observation protocols, and value-added measures.

## 6. Architecture Design

The proposed architecture follows a modular, event-driven, distributed systems approach.

### 6.1 Data Capture Pipeline (Edge)

- **Input:** Audio, Video (Teacher + Students), Screen/Slides.
- **Edge Processing:** Local anonymization (blurring faces), initial voice activity detection (VAD), and compression.
- **Transport:** WebRTC for live streams, secure chunked uploads (S3/GCS) for post-processing.

### 6.2 Multimodal Inference Pipeline (Cloud/GPU Cluster)

- **Audio:** Whisper (ASR) + Pyannote (Diarization) + HuBERT (Speech Emotion).
- **Video:** YOLO/MediaPipe (Pose/Action) + CLIP (Multimodal Embeddings).
- **Text:** Llama-3/Mistral (Pedagogical Analysis, Summarization).
- **Fusion:** A multimodal transformer layer aligning audio, video, and text embeddings chronologically.

### 6.3 Storage and Retrieval

- **Relational Data:** PostgreSQL (User profiles, metadata, permissions).
- **Vector Search:** Qdrant (Embeddings for semantic search across lectures).
- **Time-Series/Events:** ClickHouse (Analytics, heatmaps, speaking ratios).
- **Cache/Queue:** Redis + Kafka/RabbitMQ.

## 7. Tech Stack Analysis

An exhaustive evaluation of the technology stack is required before implementation.

### 7.1 Backend Services

- **Go:** High performance, excellent concurrency, great for network IO.
- **Rust:** Highest performance, memory safety, steep learning curve.
- **Python (FastAPI):** Selected. Excellent ecosystem for AI/ML integration, rapid development, sufficient performance for asynchronous orchestrations.
- **Node.js:** Good for I/O, but poor for heavy compute.

### 7.2 AI/ML Frameworks

- **PyTorch:** Selected. Industry standard for research and deployment.
- **TensorFlow:** Waning popularity in research.
- **ONNX/TensorRT:** Selected for inference optimization on production GPUs.

### 7.3 Databases

- **PostgreSQL:** Selected for ACID compliance and robust relational modeling.
- **Qdrant:** Selected for high-performance vector search (Rust-based).
- **ClickHouse:** Selected for lightning-fast time-series analytics (e.g., engagement over time).

### 7.4 Frontend and Client

- **Next.js (React):** Selected for the web dashboard (SEO, server-side rendering, mature ecosystem).
- **Meta Ray-Ban DAT:** Primary v1 client for capture.

### 7.5 Infrastructure

- **Kubernetes:** Selected for scalable container orchestration.
- **AWS/GCP:** Cloud provider (TBD based on GPU availability and cost).

## 8. AI Features to Research

We must continuously evaluate the feasibility of advanced AI features:

- **Speech Clarity Scoring:** Can we accurately score pronunciation and pacing?
- **Classroom Engagement Heatmaps:** Generating visual representations of student focus using skeletal tracking.
- **Teacher/Student Speaking Ratios:** Calculating the exact percentage of "Teacher Talk Time" (TTT) vs. "Student Talk Time" (STT).
- **Hallucination-Resistant Feedback:** Ensuring the AI coach does not invent feedback not grounded in the recording.

## 9. Scrum + Agile Requirements

The project will be managed using rigorous Agile methodologies:

- **Epics:** High-level features (e.g., "Multimodal Inference Pipeline").
- **Stories:** User-centric requirements.
- **Tasks/Sub-tasks:** Granular engineering work.
- **RFCs/ADRs:** Mandatory documentation for significant architectural decisions.

## 10. Engineering Philosophy & Implementation Rules

Before writing production code, the following rules apply:

1. **Stabilize Architecture:** The system design must be reviewed and approved.
2. **Identify Risks:** Explicitly document known unknowns (e.g., GPU costs, latency).
3. **Observability First:** Implement logging, metrics, and tracing before business logic.
4. **Contracts & Schemas First:** Define APIs (OpenAPI) and database schemas before implementation.
5. **Testing & Evals First:** Establish CI/CD pipelines and AI evaluation frameworks.
6. **No UI First:** We will not build shiny UI screens until the underlying infrastructure and data pipelines are proven.

---

_End of Document. Awaiting stakeholder review._
