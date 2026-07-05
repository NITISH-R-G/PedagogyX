# Phase 0: Foundational Founder Interrogation Report v1

**Date:** Current
**Author:** Autonomous Principal Research Architect & Lead Systems Engineer
**Project:** PedagogyX

## Executive Summary

This document serves as the exhaustive foundational interrogation of the PedagogyX founder. Before any significant system architecture or implementation begins, these critical business, legal, product, and technical questions must be answered to form a complete operational picture.

We currently have a few known architectural facts based on prior context:

- **Primary v1 Client:** Meta Ray-Ban POV video + mic via DAT on a teacher’s Android phone host app.
- **Data Pipeline:** Hybrid edge + cloud (ap-south-1).
- **Asynchronous Processing:** Redis/Celery event-driven architecture for the cold path AI inference pipeline.
- **ASR:** Multilingual OSS models (faster-whisper large-v3) for Hindi-English code-switching.
- **Regulatory Blockers:** Awaiting India DPDP (Data Digital Personal Data Protection Act) legal sign-off (G2 memo) to handle production school data. Currently, only synthetic test sessions are permitted.
- **Hardware/AI limits:** Max GPU is RTX 5070 12 GB, preferring OSS LLMs on-prem (Ollama/vLLM).

However, many deep systemic variables remain undefined. This document requests explicit answers on the following.

---

## Part 1: Product & Business Strategy Questions

### 1.1 Market & Economics

- Is the PedagogyX system primarily positioned as a B2B Enterprise SaaS tool, or a Top-Down Government Surveillance tool?
- While the current budget per classroom is ₹0 / $0 during the test year, what is the expected ACV (Annual Contract Value) for a school post-pilot?
- Who is the primary persona consuming the longitudinal analytics: the individual teacher (for coaching), the principal (for evaluation), or a district admin (for macro trends)?
- How does the system handle teacher union backlash? What is our response to "AI supervision"?

### 1.2 User Experience & Pedagogy Modeling

- What specific pedagogical frameworks (e.g., Flanders Interaction Analysis, Marzano, Danielson) should the AI use to evaluate teaching effectiveness?
- Are we scoring emotional tone? If so, what rubrics define "good" versus "bad" tone in the Indian context?
- For the Meta Ray-Ban capture: How does the teacher start/stop sessions? Is it a continuous 45-minute recording, or segment-based?
- How is student engagement defined when captured primarily via a teacher's POV glasses? Are we looking for eye-contact, posture, or verbal participation?

---

## Part 2: Legal, Privacy & Compliance Questions

### 2.1 India DPDP Compliance & Global Standards

- What is the explicit legal mechanism for obtaining student/parent consent for capturing identifiable video and audio in Indian classrooms under DPDP?
- Can we default to aggressive real-time face blurring at the edge (on the Android host device) before transmitting to the cloud to reduce DPDP risk?
- Is FERPA/GDPR compliance necessary to architecture _now_ for future US/EU expansion, or do we hardcode to Indian DPDP requirements for v1?

### 2.2 Explainable AI & Auditing

- When the system issues a "pedagogical score" that an administrator sees, how much interpretability (Explainable AI) is legally or ethically required?
- Do teachers have the right to appeal or request deletion of a session if they feel the AI hallucinated a bad score?
- What are the data retention policies for raw video vs. vector embeddings vs. metadata?

---

## Part 3: Technical & Architectural Questions

### 3.1 Edge Capture & Streaming Pipeline

- The Meta Ray-Ban glasses pair to an Android device. What is the guaranteed upload bandwidth from the Android device to the local LAN edge buffer or directly to the ap-south-1 cloud?
- Will the Android app perform any local ML inference (e.g., VAD, face blurring, silence stripping) before uploading, or is it a dumb pipe?
- If the classroom loses internet for 3 hours, how much local storage must the Android DAT host app allocate to spool video?

### 3.2 AI & Inference Stack

- Our cold path uses Redis/Celery. For real-time coaching (under 3s latency), how are we bypassing the cold path? Do we need a dedicated WebRTC signaling server + fast-path inference worker?
- We have a memory constraint of RTX 5070 (12GB VRAM). Are we required to run faster-whisper, video encoding/decoding, and a 7B LLM (like Qwen2.5) concurrently on the same 12GB GPU, or are these scaled across multiple nodes?
- How will the system perform Hindi-English code-switching robustly? Does it require custom fine-tuning of faster-whisper, or is the base model sufficient for Indian accents and classroom noise?

### 3.3 Storage & Retrieval

- Are we building an educational knowledge graph (Neo4j) to map curriculum concepts mentioned in the audio, or just using vector databases (Milvus/Qdrant) for semantic search over transcripts?
- How are multimodal embeddings (audio, video, text) fused and stored?

### 3.4 Security & RBAC

- Are we required to implement Row-Level Security (RLS) in PostgreSQL to ensure strict tenant isolation down to the school or classroom level?
- How are video assets encrypted at rest in MinIO? Who holds the keys?

---

## Part 4: Research & Development Strategy

### 4.1 Evaluation & Benchmarking

- What is the ground truth dataset we are evaluating our AI against? Do we have expert human annotators (master teachers) grading the synthetic data?
- How do we measure "hallucinations" in pedagogical coaching feedback?
- Is the platform permitted to use federated learning to improve models without centralizing PII video data?

## Required Action

Please provide detailed responses to the above questions. Your answers will establish the foundational architectural constraints required to move into Phase 1 (Competitive Analysis & Research) and define the technical schemas.
