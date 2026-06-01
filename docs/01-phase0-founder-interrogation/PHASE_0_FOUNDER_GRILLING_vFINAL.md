# Phase 0: Exhaustive Founder Interrogation & Risk Interrogation vFINAL

**Status:** Phase 0 Active
**Date:** 2026-05-25
**Owner:** Principal Research Architect & Lead Systems Engineer
**Domain:** Deep-tech Educational AI Platform (PedagogyX)

## I. Executive Summary

As the Principal Research Architect, my role is to explicitly define, challenge, and stress-test the product vision, architecture, and assumptions of PedagogyX _before_ any production code is written. This document serves as the exhaustive interrogation of the founder's assumptions, identifying contradictions, exposing risks, and forcing precise technical decisions.

## II. Product & Market Strategy Questions

### A. Core Value Proposition & Positioning

1. Are we building a surveillance tool or an empowerment tool? The architecture fundamentally diverges based on this answer.
2. Is the primary economic buyer the district superintendent, the school principal, or the individual teacher?
3. How do we prevent teacher unions from blocking adoption if the system generates a "Pedagogy Score"?
4. If this is an Enterprise SaaS, what are our SLA guarantees regarding video processing turnaround times?
5. Are we competing with low-cost simple video capture (Vosaic) or high-end multimodal analytics (Chinese Smart Classrooms)?
6. Does the system target K-12, Higher Education, or Corporate Training? The pedagogical models are entirely different.
7. What is the acceptable false positive rate for "negative pedagogical feedback"?
8. How does PedagogyX differentiate from generalized AI meeting tools (e.g., Zoom AI, Read.ai)?

### B. Global Compliance & Privacy

9. What countries are our Day 1 launch markets?
10. Is FERPA (US) compliance required at launch?
11. Is GDPR (EU) compliance required? If so, how do we handle the strict prohibition on biometric processing without explicit, revocable consent from minors?
12. Is India DPDP compliance required? (Based on ADR-0003, yes). How do we handle data localization?
13. Is the extraction of student facial data/emotions permitted under local law?
14. How do we handle a parent's request to "forget" their child's data in a recorded classroom session?
15. If a teacher deletes their account, what happens to the aggregate ML models trained on their data?
16. Can administrators see raw video, or only aggregate metrics?
17. Is the AI scoring public (to admins) or private (to the teacher)?

### C. The "Chinese Smart Classroom" Paradigm

18. You mentioned rivaling Chinese Smart Classroom systems. These often rely on continuous, unconsented facial emotion recognition of students. Are we comfortable with this ethical boundary?
19. If not, how do we measure "engagement" without explicit facial analysis?
20. Will we use skeletal tracking (pose estimation) as a proxy for attention? Is this culturally biased?

## III. Deep Technical Interrogation

### A. Hardware & Edge Constraints

21. What is the assumed classroom hardware budget? (<$100, $500, $5000?)
22. Are we requiring schools to install new ceiling multi-camera arrays, or using existing low-end webcams?
23. Based on ADR-0009, Meta Ray-Ban glasses are the primary v1 client. How do we handle battery life (currently ~4 hours max)?
24. How do we handle the POV shaking and rapid head movements of a teacher wearing Ray-Bans?
25. How do we handle the heat dissipation of Ray-Bans during continuous 50-minute recording?
26. If the classroom has poor/no internet, how much local storage does the Android companion app need to buffer 50 minutes of 1080p video?
27. Are we assuming a "low-bandwidth mode" that uploads audio-only first, and video overnight?

### B. Scalability & Cloud Architecture

28. If 1,000 teachers in a district finish their 50-minute class at 3:00 PM and all devices upload simultaneously, what is our expected peak ingest bandwidth?
29. Are we doing real-time processing (requires WebRTC, massive edge compute) or post-processing (batch processing overnight)?
30. How many concurrent RTX 5070s are required to process 1,000 hours of video overnight?
31. What is our strategy for scaling self-hosted GPU clusters vs. bursting to AWS/GCP?
32. What is the expected cost per hour of processed video? If the school pays $10/month per teacher, but GPU inference costs $15/month, we are economically unviable.

### C. Multimodal Inference & Synchronization

33. How do we synchronize the Ray-Ban POV video with the classroom smartboard screen capture?
34. What is the acceptable drift tolerance before multimodal fusion (e.g., matching a slide change to spoken words) fails?
35. Classroom audio is highly reverberant. How do we diarize 30 student voices from a single microphone on the teacher's face?
36. If a student in the back row asks a question, will the Ray-Ban mic capture it? If not, the pedagogical analysis of "teacher-student interaction" is fundamentally flawed.
37. How do we represent temporal events (a question asked at minute 5, answered at minute 45) in our vector database?

### D. AI Model Pipelines

38. Are we using proprietary APIs (OpenAI, Anthropic) or self-hosted OSS models? (ADR-0005 states OSS-first).
39. Can a 7B or 14B parameter OSS model (e.g., Qwen 2.5) accurately evaluate complex pedagogical rubrics, or does it require a 70B model?
40. How do we mitigate LLM hallucinations when generating "teaching feedback"? A hallucinated critique could ruin a teacher's career.
41. Do we have a proprietary dataset of labeled classroom interactions to fine-tune our models? If not, how do we bootstrap performance?
42. How are we handling the bias in ASR (speech-to-text) against regional Indian accents?
43. How do we measure "pedagogical efficiency"? What is the mathematical definition we are optimizing for?

## IV. Required Decisions & Blockers

Before implementation proceeds past the MVP boilerplate, the founder MUST provide concrete answers or accept the architectural constraints imposed by these questions:

- **Blocker 1:** Finalize the strict privacy boundaries regarding student biometric analysis.
- **Blocker 2:** Define the maximum acceptable GPU cost per user per month.
- **Blocker 3:** Confirm the fallback strategy if Meta Ray-Ban battery/heat limitations prevent 50-minute continuous capture.
- **Blocker 4:** Define the specific pedagogical framework (e.g., Danielson Framework, CLASS) the AI is evaluating against.

## V. Risk & Tradeoff Matrix

| Risk Category      | Identified Risk                                          | Impact | Proposed Mitigation                                                                                                 |
| :----------------- | :------------------------------------------------------- | :----- | :------------------------------------------------------------------------------------------------------------------ |
| **Hardware**       | Meta Ray-Ban battery dies mid-class.                     | High   | Fallback to Android phone mic; asynchronous recovery.                                                               |
| **Data Privacy**   | Parent sues over unconsented student recording.          | Fatal  | Strict RBAC; deterministic blurring of student faces at the edge.                                                   |
| **AI Quality**     | AI hallucinates negative feedback, causing union strike. | Fatal  | Human-in-the-loop review for all negative scoring; explicit "AI Confidence Score" visible.                          |
| **Infrastructure** | GPU costs exceed SaaS subscription revenue.              | High   | Aggressive use of TensorRT; batch processing overnight on spot instances; audio-only primary models.                |
| **Acoustics**      | Unable to hear student questions from teacher's mic.     | High   | Focus MVP exclusively on _teacher_ speech metrics (talk time, clarity, pacing) rather than full classroom dialogue. |

Note: This document represents Phase 0 Interrogation. Architecture will adapt based on the resolution of these blockers.
