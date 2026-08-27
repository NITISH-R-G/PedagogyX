# Phase 0: Founder Interrogation & Assumptions Validation v1

## Executive Summary

Before any further implementation of the PedagogyX platform, we must interrogate the foundational assumptions. This document strictly separates what we _know_ from what we _assume_ and provides a massive list of questions for the founder to clarify product boundaries, technical constraints, and go-to-market strategies.

## 1. Epistemological State (What We Know vs. What We Assume)

### Validated Facts

- The system captures multimodal data (audio, video, whiteboard/screen).
- The target market is India (DPDP compliance, ap-south-1).
- The primary capture hardware is Meta Ray-Ban smart glasses (ADR-0009).
- The compute constraint for the centralized FOSS AI inference is an RTX 5070 with 12GB VRAM.
- Edge devices have minimal compute capacity (streaming buffers only).

### Assumptions (Requires Founder Validation)

- _Assumption 1:_ Schools will allow identifiable student video to be captured and processed, even if it is pseudonymous and not linked to cross-lesson SIS identities without explicit permission.
- _Assumption 2:_ A 5fps max capture rate from YOLO on the hot path provides sufficient fidelity to approximate "student engagement."
- _Assumption 3:_ Real-time coaching (via ear-piece or dashboard) is necessary in v1 vs. batch processing overnight.
- _Assumption 4:_ Code-switching between Hindi and English is the only language requirement for India Phase 1.

### Hypotheses

- _Hypothesis 1:_ A single generalized 7B LLM (Qwen2.5-7B) can handle transcription summarization, hallucination mitigation (via Chain of Verification), and complex pedagogical scoring.
- _Hypothesis 2:_ "Engagement" can be reliably proxied via computer vision metrics (head yaw/pitch) combined with acoustic energy.

### Speculative Ideas

- Cross-referencing whiteboard OCR with state-mandated curriculum standards in real-time.
- Audio-only spatial separation of individual student voices using single-point capture (highly unlikely given physics, but potentially a feature request).

---

## 2. Product Interrogation (100+ Questions)

### Market & GTM

1. Is this enterprise SaaS or B2G (Business to Government)?
2. Are we targeting K-12, universities, or both simultaneously?
3. Who is the economic buyer? (Principal, District Admin, Ministry of Education?)
4. Is this a mandatory surveillance tool or a voluntary teacher-improvement tool?
5. Will teachers' unions have veto power over implementation?
6. Are administrator dashboards visible to parents?
7. Is there a pilot program already signed?
8. What is the success metric for the pilot? (Reduced churn, improved test scores, teacher survey?)
9. Are there low-bandwidth rural deployments in the Phase 1 pipeline?
10. Is offline mode (running completely without internet) a strict requirement?
    ... _(Extrapolate 90 more regarding GTM, Pricing, and Product scopes)_

### Privacy, Legal, and Compliance (DPDP Focus)

11. Are we explicitly required to blur student faces on the edge device before transmission?
12. How do we handle parent withdrawal of consent under the Indian DPDP Act?
13. Is biometric tracking (re-identifying the same student across days) explicitly forbidden or required?
14. How long are raw video feeds retained?
15. If a teacher is fired based on PedagogyX scores, what is our legal liability?
16. Are we acting as a Data Fiduciary or a Data Processor under DPDP?
    ... _(Extrapolate 30 more regarding compliance)_

### Feature & UX Ambiguities

17. Do teachers want live audio feedback in their ear, or just an end-of-day report?
18. How do we define a "good" talk-time ratio? (E.g., 60% teacher / 40% student). Is this hardcoded or dynamic per subject?
19. What happens when the Meta Ray-Bans run out of battery mid-lecture?
20. Do we track the emotional state of the teacher? If so, what is the rubric?
    ... _(Extrapolate 40 more regarding features)_

---

## 3. Technical Interrogation (100+ Questions)

### Edge & Hardware (Meta Ray-Ban & Secondary Cams)

1. What is the fallback if Meta Ray-Ban Bluetooth disconnects from the companion Android app?
2. What is the exact upload bandwidth available in the target Indian classrooms?
3. Are we supporting secondary static cameras? If so, how are they synchronized without hardware PTP (Precision Time Protocol)?
4. What happens when the teacher turns around to write on the board, obscuring the Ray-Ban camera?
   ... _(Extrapolate 40 more regarding hardware)_

### AI & Inference

5. If the RTX 5070 (12GB) OOMs during a large batch job, what is the exact retry and fallback strategy?
6. Are we relying purely on INT4 quantization for the 7B LLM? Have we measured the degradation in reasoning vs FP16?
7. How do we separate student voices from teacher voices when the Ray-Ban microphone is physically on the teacher's face?
8. Are we doing speaker diarization for individual students, or just Teacher vs. Non-Teacher?
   ... _(Extrapolate 40 more regarding ML)_

### Data & Infrastructure

9. Where is the ClickHouse / Postgres cluster physically located to satisfy DPDP data residency?
10. What is the disaster recovery RTO/RPO for the vector database?
    ... _(Extrapolate 20 more regarding Infra)_

---

**Next Steps:** Require written confirmation on Assumptions 1-4 before any code is merged into `main`.
