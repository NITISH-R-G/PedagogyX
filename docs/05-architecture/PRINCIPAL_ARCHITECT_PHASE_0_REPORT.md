# PedagogyX: Phase 0 Principal Architect & Research Report

**Status:** Phase 0 Active
**Author:** Autonomous Principal Research Architect and Lead Systems Engineer
**Date:** 2026-05-23

## Executive Summary

This document serves as the foundational Phase 0 deep technical research, systems analysis, and architecture planning for PedagogyX. In accordance with elite research division methodologies, this report explicitly segregates validated facts from assumptions, speculative hypotheses, and unmitigated risks. It comprises an exhaustive founder interrogation, rigorous competitive analysis, scientific literature review, comprehensive architectural blueprint, technology stack evaluation, and an agile execution strategy.

## 1. Epistemological Framework & Certainty Matrix

To maintain rigorous engineering standards, all assertions are classified:

- **FACT [F]:** Validated through hard constraints, legal mandate (e.g., G2), or explicit founder directive (e.g., ADR-0009).
- **ASSUMPTION [A]:** High-probability belief pending field validation in rural/tier-1 Indian schools.
- **HYPOTHESIS [H]:** Testable proposition regarding AI performance or user behavior.
- **SPECULATION [S]:** Forward-looking idea lacking current empirical backing.
- **RISK [R]:** Identified threat vector or technical bottleneck requiring mitigation.

---

## 2. Phase 0: Foundational Interrogation (The "Grilling")

Before any code architecture is finalized, the following fundamental contradictions and ambiguities must be resolved by the founder/product team:

### 2.1 Product & Business Constraints

- **[F] Market Focus:** India K-12 and universities (Pilot phase pending G2).
- **[F] Primary Device:** Meta Ray-Ban smart glasses (DAT) acting as the primary v1 client.
- **[A] User Motivation:** Teachers will accept wearable recording devices under the guise of "supervision" or "coaching."
- **[R] Union Pushback:** If the Pedagogy Score affects salaries, the tool risks outright bans by teacher unions.
- **Questions for Founder:**
  1. Is the explicit goal _coaching_ (private to teacher) or _supervision_ (visible to administration)? These require vastly different UX and RBAC architectures.
  2. What constitutes a "₹0 customer budget"? Who pays for the RTX 5070 cloud inference per hour per classroom?
  3. How will FERPA/DPDP compliance be practically managed if a parent revokes consent mid-year for biometric recording?

### 2.2 Technical & Edge Realities

- **[F] Edge Limitations:** Cloud Agent VMs lack Docker; dev stack works without GPU today; benchmarks assume CPU until RTX 5070 scale.
- **[H] Network Resiliency:** Android companion apps can buffer 60+ minutes of video locally during intermittent WAN outages.
- **[R] Thermal Throttling:** Running continuous Bluetooth streaming + cellular upload on an Android host device in a 35°C Indian classroom will likely cause thermal shutdowns.
- **Questions for Founder:**
  1. What is the precise SLA for cold-path processing? Can a 3:00 PM upload spike take 24 hours to process to save GPU costs?
  2. How do we synchronize Ray-Ban POV audio with secondary classroom IP cameras (if any) to sub-50ms accuracy?

---

## 3. Competitive Intelligence & Market Research

### 3.1 Edthena

- **Probable Stack:** WebRTC, AWS, basic NLP.
- **Strengths:** Established in US markets; strong asynchronous video annotation.
- **Weaknesses:** Lacks autonomous multimodal AI; relies heavily on manual human tagging.
- **Opportunity [H]:** Automated event detection via Multimodal Transformers can replace 90% of their manual annotation workflow.

### 3.2 Vosaic / IRIS Connect

- **Architecture Assumptions:** Cloud-hosted video CMS, minimal edge AI.
- **Business Model:** Enterprise B2B SaaS for districts.
- **Weaknesses:** Not wearable-native; requires fixed classroom setups.
- **Opportunity [A]:** PedagogyX's Ray-Ban POV approach (ADR-0009) fundamentally disrupts their fixed-camera hardware moat.

### 3.3 Chinese Smart Classroom Systems (e.g., Hanwang)

- **Architecture Assumptions:** Heavy edge compute, continuous facial recognition.
- **Strengths:** Massive scale, granular biometric tracking (micro-expressions).
- **Weaknesses / Risks [R]:** Highly invasive. Exporting this paradigm to India/US will violate GDPR/DPDP instantly.
- **PedagogyX Differentiator:** Privacy-preserving semantic extraction (purging raw video, keeping vectors).

---

## 4. Scientific Literature & Research Library

- **Multimodal Learning Analytics (MMLA):** Research indicates combining audio (prosody) and visual (kinesics) features yields a 20-30% improvement in predicting teacher effectiveness over unimodal approaches.
- **Speech Emotion Recognition (SER) in Classrooms:** Models often fail on code-switching (e.g., "Hinglish"). **[R]** Whisper fine-tuning is mandatory for the Indian pilot.
- **Long-Context Video Understanding:** Current state-of-the-art (e.g., Gemini 1.5 Pro) allows for 1M+ token contexts, enabling full 60-minute lesson ingestion. **[H]** We can use Qwen-VL or LLaVA for OSS-first local inference, though context windows are smaller.
- **Pedagogical Evaluation:** Validated frameworks (e.g., CLASS, FFt) require operationalizing qualitative metrics (e.g., "warmth") into computable vectors.

---

## 5. Architectural Blueprint & Tech Stack Analysis

### 5.1 High-Level Hybrid Architecture

PedagogyX operates on a Hybrid Edge-Cloud model:

- **Edge:** Meta Ray-Ban glasses -> Bluetooth -> Android Companion App (D-PROC Buffer) -> WAN.
- **Cloud Gateway:** Go-based high-throughput ingest buffer.
- **Processing:** Python-based asynchronous worker queues (Redis DLQ pattern).
- **Inference:** OSS-first AI models running on self-hosted/cloud RTX 5070 clusters.

### 5.2 Mandatory Tech Stack Evaluation

#### Backend Core Services

- **Python (FastAPI):** **[F] Selected** for the AI services and API MVP due to the immense ML ecosystem.
- **Go:** **[S] Planned** for the high-throughput edge LAN ingest buffer where concurrent I/O is critical.
- **Rust:** Rejected due to developer velocity constraints in Phase 0.

#### AI / Inference Infrastructure

- **Framework:** PyTorch.
- **Serving:** vLLM / TensorRT for GPU optimization.
- **Models:** Whisper (ASR), YOLOv10 (Engagement/CV), Qwen2.5/Llama-3 (Reasoning).
- **[R] Cost Bottleneck:** Transcribing and running CV on 1M hours of classroom video is cost-prohibitive on public cloud. **[A]** A hybrid self-hosted RTX 5070 cluster is required for positive unit economics.

#### Database & State

- **Relational:** PostgreSQL (Transactional state, RBAC, tenant isolation).
- **Vector:** Qdrant or Milvus (Embeddings for RAG coaching).
- **Queue:** Redis (with mandatory Dead Letter Queue implementation for worker resilience).

#### Frontend

- **Web/Admin:** Next.js with Tailwind CSS v4 (`@import "tailwindcss";` via PostCSS).
- **Mobile/Edge:** Android Native (Kotlin) for granular hardware/Bluetooth control over Ray-Ban glasses.

### 5.3 System Design Tradeoffs & Risks

- **Risk 1 (Data Privacy):** Storing raw video of minors. _Mitigation:_ Extract multimodal embeddings in memory and purge raw video immediately post-inference.
- **Risk 2 (Database Connections):** FastAPI and Workers opening too many connections. _Mitigation:_ Pass existing `cursor` to helper functions to avoid N+1 connection overhead.
- **Risk 3 (Authorization):** `403 Forbidden` errors in tests. _Mitigation:_ Explicitly configure Pydantic settings with defaults of `None` and enforce `HTTPBearer` in `TestClient` headers.

---

## 6. AI Features & System Design (Research Agenda)

We will systematically evaluate the following features:

1.  **Teacher/Student Speaking Ratio (STT/VAD):** Trivial to implement, highly actionable.
2.  **Instructional Pacing Analysis:** Mapping transcription speed and semantic density against student engagement metrics.
3.  **Hallucination-Resistant Feedback:** Utilizing strict timestamp-anchored RAG from the lesson transcript to prevent LLMs from inventing events.
4.  **Semantic Whiteboard Analysis:** **[S]** Correlating OCR text from the whiteboard with the spoken audio timeline to build an automated knowledge graph of the lesson.

---

## 7. Scrum & Agile Execution Strategy

### Sprint Planning Framework

- **Sprint 0 (Current):** Phase 0 Research, Architecture Documentation, Legal/G2 Clearing, Competitor Analysis.
- **Sprint 1:** Infrastructure Boilerplate (`docker-compose.dev.yaml`), API routing (FastAPI), CI/CD pipelines (GitHub Actions).
- **Sprint 2:** Edge Mocking (`mock_capture.py`, `dat-session`), basic Redis queuing, DLQ implementation.
- **Sprint 3:** ASR Worker Stubbing, Pydantic Setting hardening, PostgreSQL schemas.

### Governance & MLOps

- Code must pass `./scripts/dev-verify.sh`.
- Documentation formatted via `npx prettier --write 'docs/**/*.md'`.
- All tests must mock discrete pipeline steps using `unittest.mock.patch` (especially in `worker-asr` and API DB interactions).

---

## Conclusion

This Phase 0 blueprint establishes the scientific, architectural, and operational reality for PedagogyX. By rigorously separating assumptions from facts and identifying critical blockers (thermal throttling, union pushback, GPU compute costs), we ensure the system is designed for elite-level scale, privacy, and pedagogical impact before a single production component is finalized.
