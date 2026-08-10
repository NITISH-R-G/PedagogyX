# AGILE SPRINT PLAN: PHASE 0 TO MVP

**Document Status:** DRAFT
**Date:** 2024-03-XX
**Author:** Autonomous Principal Research Architect & Lead Systems Engineer
**Classification:** INTERNAL ONLY

## Overview

This document outlines the strategic Agile roadmap from Phase 0 (Research & Architecture) to the deployment of the Minimum Viable Product (MVP) for the India G2 Pilot.

---

## Sprint 0: Foundational Interrogation & Research (Current)

**Goal:** Achieve total architectural clarity and mitigate existential project risks before writing code.

- **Epic 1: Founder Interrogation**
- _Task:_ Complete the 100+ question interrogation regarding product scope, privacy, and technical boundaries.
- _Task:_ Document founder responses and resulting architectural implications.
- **Epic 2: Deep Research**
- _Task:_ Synthesize research papers on multimodal pedagogy analysis.
- _Task:_ Complete exhaustive competitor analysis (Edthena, Vosaic, etc.).
- **Epic 3: Architecture Definition**
- _Task:_ Finalize System Architecture and Tech Stack Comparison.
- _Task:_ Draft India DPDP Compliance Architecture.

---

## Sprint 1: Infrastructure as Code & Core Services

**Goal:** Stand up the non-AI foundational infrastructure required to ingest and store data securely.

- **Epic 1: The Backbone**
- _Task:_ Deploy local Docker Compose stack (Postgres, Qdrant, Redis).
- _Task:_ Set up local MinIO for S3-compatible object storage.
- **Epic 2: Core API**
- _Task:_ Scaffold FastAPI service.
- _Task:_ Implement JWT Authentication and RBAC schemas.
- _Task:_ Build secure, resumable file upload endpoints.
- **Epic 3: Observability**
- _Task:_ Integrate structured JSON logging.
- _Task:_ Set up local Prometheus/Grafana or equivalent tracing.

---

## Sprint 2: The Capture Client (DAT)

**Goal:** Build the mechanism to actually record classroom data via the primary client.

- **Epic 1: Android DAT App**
- _Task:_ Initialize Kotlin Android project.
- _Task:_ Integrate with Meta Wearables DAT SDK.
- _Task:_ Implement reliable chunking of 1-minute video/audio segments.
- _Task:_ Implement upload queue with exponential backoff for network drops.

---

## Sprint 3: AI Pipeline - Audio & NLP

**Goal:** Ingest raw audio and turn it into actionable pedagogical insights.

- **Epic 1: The ASR Worker**
- _Task:_ Scaffold Python worker listening to event queue.
- _Task:_ Integrate Silero VAD for voice detection.
- _Task:_ Integrate WhisperX for diarized, timestamped transcription.
- **Epic 2: The NLP Coaching Agent**
- _Task:_ Design the LangChain/LlamaIndex pipeline for RAG.
- _Task:_ Prompt engineer the "Pedagogical Evaluator" agent to measure Wait-Time and Talk-Ratio.
- _Task:_ Store resulting embeddings in Qdrant.

---

## Sprint 4: Dashboard & G2 Pilot Prep

**Goal:** Visualize the AI insights for the teacher and ensure system stability.

- **Epic 1: Teacher Dashboard (Next.js)**
- _Task:_ Scaffold Next.js frontend.
- _Task:_ Build Session History view.
- _Task:_ Build detailed pedagogical metrics visualization (charts for talk-time, wait-time).
- **Epic 2: G2 Pilot Hardening**
- _Task:_ Load test the API with synthetic concurrent classroom uploads.
- _Task:_ Verify India DPDP data residency boundaries.
- _Task:_ Finalize deployment manifests for `ap-south-1`.

---

## Risk Matrix

| Risk                              | Impact   | Likelihood | Mitigation Strategy                                                                                                                  |
| :-------------------------------- | :------- | :--------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| **Meta DAT SDK Instability**      | High     | Medium     | Rely heavily on the provided mock capture scripts; build abstract interfaces so we can swap to standard IP cameras if Ray-Bans fail. |
| **India DPDP Violation**          | Critical | Low        | Strict enforcement of `ap-south-1` region deployment; no PII logging in standard application logs.                                   |
| **ASR Hallucinations (Hinglish)** | High     | High       | A/B test various open-source models; prioritize Whisper models fine-tuned on Indic languages.                                        |
| **GPU Cloud Cost Spikes**         | Medium   | High       | Implement aggressive auto-scaling; scale down to zero during non-school hours.                                                       |
