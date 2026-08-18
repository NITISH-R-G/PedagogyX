# Principal Architect Phase 0 Report v4: Foundational Interrogation Synthesis

**Date:** 2026-05-25
**Author:** Autonomous Principal Research Architect
**Status:** DRAFT
**Context:** Synthesis of founder answers (2026-05-19) and subsequent plan changes (2026-05-23).

## 1. Executive Summary

This report synthesizes the foundational product and technical decisions established during Phase 0 interrogation. The primary objective of PedagogyX is to monitor and assess teacher pedagogy, not to rank students. The architecture must support a dual segment (K-12 district + university) with initial deployment focused on the Indian market (implying DPDP compliance and ap-south-1 infrastructure). The product will offer real-time coaching and support identifiable student video for classroom-level discourse metrics.

Crucially, the capture strategy has pivoted (ADR-0009) to prioritize Meta Ray-Ban smart glasses (POV video + mic) paired with an Android host application (DAT), deferring multi-camera smartboard integration to Phase 1b. The system architecture will follow a hybrid model (LAN edge buffer + India cloud GPU analytics) constrained by a strict open-source, maximum RTX 5070 12GB hardware profile.

## 2. Product Strategy & Assumptions

### 2.1 Target Market and Users

- **Primary Customers:** K-12 Districts and Universities.
- **Initial Geography:** India.
- **Economic Buyer:** School Principals, Deans, Campus IT (Institution level, not state procurement for v1).
- **Primary Value Proposition:** Monitor and assess teacher teaching ability and pedagogy. Provide actionable insights for instructional improvement.

### 2.2 Feature Scope (v1)

- **In Scope:**
- Per-teacher lesson pedagogy index and evidence clips.
- Real-time coaching (<3s latency target).
- Admin/coach review dashboards with individual AI pedagogy scores visible to administrators.
- Identifiable student video capture (where legally permitted) to infer classroom-level metrics (e.g., student talk ratio).
- **Out of Scope (Deferred):**
- Per-student report cards, punitive student scores, or student identity as a primary dashboard unit.
- Social/emotional profiling of students as a primary goal.
- Multi-camera smartboard capture (Deferred to Phase 1b - ADR-0007).

### 2.3 Operational Modes

The product must support distinct operational modes due to varying market expectations (e.g., China-style supervision vs. US-style coaching).

| Mode          | Admin Visibility | Student ID Video         | Real-time | Primary Market     |
| :------------ | :--------------- | :----------------------- | :-------- | :----------------- |
| `supervision` | High             | Yes                      | Yes       | India (v1 Default) |
| `coaching`    | Restricted       | De-identified / Optional | Optional  | Future US Export   |

## 3. Technical Architecture Constraints

### 3.1 Hardware and Infrastructure

- **Maximum GPU Hardware:** NVIDIA RTX 5070 12GB (ADR-0006). This enforces strict memory optimization for AI models.
- **Deployment Topology:** Hybrid Cloud/Edge (ADR-0008).
- **Edge:** On-site LAN edge buffer/ingest for reliability.
- **Cloud:** India-based cloud GPU analytics (ap-south-1) for heavy inference.
- **Software Stack:** Strict preference for free & open-source software (OSS) (ADR-0005).

### 3.2 Capture Pipeline (ADR-0009)

- **Primary Input:** Single POV stream (audio and video) from Meta Ray-Ban smart glasses.
- **Host Device:** Android smartphone running the DAT (Data Acquisition Terminal) application.
- **Synchronization:** One master AV stream per session; standard sync protocol applies (phone -> edge -> cloud).

### 3.3 AI/ML Strategy

- **Models:** OSS only. Given the 12GB VRAM limit, deployment of heavily quantized models (e.g., Qwen2.5-7B-Q4) is required.
- **Languages:** Assumption of English + Hindi ASR support required for the Indian market.

## 4. Risks and Unknowns

- **Legal Compliance:** G2 legal sign-off (India DPDP) is still pending, blocking production data and full implementation.
- **Network Reliability:** Real-time coaching (<3s latency) relies heavily on the quality of the local school network and the edge-to-cloud connection.
- **Hardware Variability:** Device validation currently accepts any panel meeting low-end profiles; rigorous testing across diverse Android host devices for the DAT app is needed.
- **Hardware Cost Model:** While the customer budget is ₹0 during the pilot, PedagogyX bears the infrastructure cost. The hybrid edge + single GPU pool strategy must be rigorously optimized to prevent cost overruns.

## 5. Next Steps

1.  Finalize the technical stack evaluation specifically tailored to the 12GB VRAM constraint.
2.  Develop detailed system architecture diagrams detailing the Android DAT -> Edge Buffer -> Cloud GPU pipeline.
3.  Establish strict data schemas and observability pipelines for the impending MVP build.
4.  Await G2 legal clearance before transitioning from synthetic data to pilot deployment.
