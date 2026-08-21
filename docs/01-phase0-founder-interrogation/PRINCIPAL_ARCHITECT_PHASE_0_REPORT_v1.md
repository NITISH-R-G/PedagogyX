# Principal Architect Phase 0 Report

## Overview

This report serves as the foundational Phase 0 deep technical interrogation for PedagogyX, outlining the core product requirements, technical constraints, risks, and critical path assumptions before substantial implementation begins.

## Document History

- **Version:** v1.0
- **Author:** Autonomous Principal Research Architect
- **Date:** 2026-05-24

## 1. Validated Facts (G0 & G2 Gates)

Based on recent product alignment (2026-05-19 & 2026-05-23), the following facts are solidified:

### 1.1 Product Facts

- **Primary Market:** India (K-12 district + university).
- **Compliance Required:** DPDP (Digital Personal Data Protection Act of India), demanding strict data residency (`ap-south-1`).
- **Product Focus:** Monitoring and assessing **teacher pedagogy** and instructional quality. Not meant for punitive student ranking.
- **Client Base:** Dual-segment (Schools and Universities). Decision makers are Principals/Deans/Campus IT.
- **Commercial:** Year 1 is a free pilot; schools have no expectation of cloud infrastructure OPEX.
- **Target Metrics:** Primary metric is M-A (Coverage), Secondary metrics are M-B (Time-to-insight), M-C (Admin action on flags).
- **Admin Visibility:** Administrators have visibility into individual teacher AI pedagogy scores.

### 1.2 Technical Facts

- **Capture Strategy (Primary):** Meta Ray-Ban smart glasses (POV video + mic) integrated via Android DAT host application (`clients/android-capture-dat`).
- **Capture Strategy (Secondary/Phase 1b):** Multi-cam/smartboards are deferred.
- **Infrastructure Mode:** Hybrid architecture (ADR-0008). LAN edge buffer for ingest -> India cloud GPU for analytics.
- **AI Stack (OSS First):** Ollama/vLLM for on-prem processing; specific focus on models that can fit on consumer-grade GPUs (e.g. Qwen2.5-7B-Q4).
- **Edge Constraints:** Maximum edge GPU available is RTX 5070 (12 GB VRAM).
- **Language Support:** English + Hindi ASR required for the primary India market.

## 2. Assumptions & Hypotheses

### 2.1 Assumptions

- **Assumption 1:** The Meta Ray-Ban DAT stream over local WiFi will have sufficient bandwidth and reliability to stream to the edge buffer without significant packet loss in Indian classroom environments.
- **Assumption 2:** A single RTX 5070 per school/LAN is sufficient to process the buffered queued video/audio from all active DAT clients throughout a standard school day, assuming asynchronous processing to the cloud.
- **Assumption 3:** Cloud infrastructure costs for the free Year 1 pilot can be strictly controlled via batching inference requests and using low-cost generic compute rather than high-tier GPU instances, relying on edge nodes for heavy lifting.
- **Assumption 4:** Teachers will accept wearing Meta Ray-Bans during instruction, and the school administration will mandate it despite potential comfort or privacy concerns.

### 2.2 Hypotheses

- **Hypothesis 1:** Utilizing quantized OSS models (Q4) on 12GB VRAM can yield accurate enough pedagogical scoring (e.g., detecting teacher speaking ratio, pacing, question types) without requiring massive cloud-side foundational models for every inference pass.
- **Hypothesis 2:** Splitting the pipeline into real-time audio/ASR (for fast feedback) and asynchronous video processing (for deep pedagogical analysis) will optimize the user experience while minimizing peak infrastructure load.

## 3. Speculative Ideas & Open Questions

### 3.1 Speculative Ideas

- **Idea A:** Implementing a "Supervision Mode" vs "Coaching Mode" toggle. In India, Supervision Mode is default, enabling full student ID video and real-time admin scoring. Coaching mode (for future US expansion) would enforce de-identification and restrict admin access.
- **Idea B:** Utilizing edge-device metadata (IMU from glasses) to supplement pedagogical data (e.g., is the teacher looking at the students or the board?).

### 3.2 Deep Founder Interrogation Questions (Pending Answers)

#### Product / Operational

1. **Network Reliability:** What happens if the school's LAN goes down? Does the DAT client buffer on the phone, or is data lost?
2. **Device Lifecycle:** Who charges the Meta Ray-Bans and Android devices? Are they school property or teacher property?
3. **FERPA/GDPR:** While India DPDP is Year 1, when are we targeting FERPA/GDPR compliance, and should the architecture enforce these constraints globally from Day 1 to avoid massive refactoring?
4. **Data Retention:** What is the legal requirement for retaining student-visible video in the Indian market post-analysis?

#### Technical / Architecture

1. **ASR Ambiguity:** While Hindi/English is assumed, are there specific Indian regional dialects (e.g., Hinglish mixtures, Marathi, Tamil) that require specialized ASR models beyond generic Whisper/OSS?
2. **Sync Pipelines:** With the shift to Ray-Bans, is there still a requirement to synchronize multiple distinct audio/video streams (RFC-0002), or is it strictly one AV stream per session now?
3. **Vector Storage:** For longitudinal analytics and teaching style clustering, which vector database is preferred given the OSS requirement (e.g., Qdrant, Milvus)?
4. **Security/RBAC:** How granular must the RBAC be? Do department heads see different data than principals?

## 4. Next Steps & Engineering Focus

1. Finalize the DAT `StreamSession` in `CaptureActivity` (Android client).
2. Wire the lifecycle to `/v1/dat-sessions` on the API.
3. Conduct pilot with the Mock Device Kit prior to real glasses deployment.
4. Establish the exact DPDP legal constraints (G2 legal memo) to unblock production data handling.

EOF
