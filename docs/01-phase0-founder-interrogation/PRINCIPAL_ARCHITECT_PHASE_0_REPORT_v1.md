# PRINCIPAL ARCHITECT PHASE 0 FOUNDER INTERROGATION REPORT

**Document Type:** Foundational Architecture & Product Requirements Interrogation
**Author:** Principal Research Architect & Lead Systems Engineer, PedagogyX
**Status:** DRAFT / BLOCKING IMPLEMENTATION
**Context:** Phase 0 - Pre-Implementation Risk & Requirements Discovery

## 1. EXECUTIVE SUMMARY

Before any production code is written or system architecture is finalized, the following questions must be explicitly answered to resolve critical ambiguities, determine structural constraints, and align the technical implementation with the strategic business objectives. Hallucinating requirements will lead to catastrophic technical debt.

---

## 2. PRODUCT & BUSINESS STRATEGY QUESTIONS

### 2.1 Target Audience & Market Positioning

1. Is PedagogyX primarily an enterprise SaaS platform (B2B), a direct-to-educator tool (B2C), or a government-level infrastructure (B2G)?
2. If B2B, are the primary buyers school districts, individual schools, universities, or corporate training departments?
3. What is the fundamental value proposition: is this designed for teacher self-improvement (coaching), administrator oversight (surveillance), or automated grading/evaluation?
4. Will the system be deployed in physical classrooms, online classes, or hybrid learning environments?
5. What are the specific target countries for the initial rollout and subsequent phases?
6. Given the India DPDP compliance requirements, are we exclusively targeting the Indian market first? What is the timeline for global expansion?
7. Is mobile-first design required for teacher dashboards and insights? Or is desktop access sufficient?
8. Are teachers unionized in our target markets, and if so, what are the union regulations regarding AI evaluation of instructional quality?

### 2.2 Operational Constraints & UX

9. Is real-time inference and feedback required (e.g., in-ear coaching), or is post-processing (batch processing after class) acceptable?
10. Is an offline mode or low-bandwidth mode required for classrooms with poor internet connectivity?
11. Should the platform support multilingual classrooms? Which languages are mandatory for v1?
12. How will we handle code-switching (e.g., mixing English and Hindi) during live sessions?
13. Can administrators see individual teacher analytics, or is the data strictly siloed for the teacher's private coaching?
14. Is human-in-the-loop (expert reviewer) mandatory before feedback is delivered to the teacher?
15. Will the AI actively score pedagogical effectiveness (e.g., giving a score out of 100), or will it only provide descriptive analytics?
16. Are we building public leaderboards for instructional quality, or is all scoring strictly private?

### 2.3 Legal, Ethical & Privacy Boundaries

17. Is China-style behavioral surveillance (tracking every student's gaze and posture) acceptable or explicitly forbidden by company policy?
18. Is student facial analysis and biometric tracking allowed, or must all student faces be blurred/anonymized at the edge?
19. Which specific legal jurisdictions are we optimizing compliance for in v1 (e.g., GDPR, FERPA, India DPDP)?
20. Under India DPDP, how do we handle consent mechanisms for minors in the classroom?
21. Is explainable AI (XAI) mandatory for all AI-generated coaching insights? How deep must the traceability be?
22. If a teacher disputes an AI-generated pedagogical score, what is the arbitration and auditing process?
23. What are the data retention policies for raw classroom video/audio versus processed analytics?

---

## 3. TECHNICAL & ARCHITECTURAL QUESTIONS

### 3.1 Hardware & Edge Integration

24. The v1 hardware client is Meta Ray-Ban. How are we bypassing or managing the battery and thermal limitations of these glasses during a 45-60 minute class?
25. Are we streaming live from the Meta Ray-Bans to a mobile companion app, and then to the cloud, or directly to the cloud?
26. What happens when the Bluetooth connection between the glasses and the companion device drops?
27. Are we supplementing the Ray-Bans with fixed classroom camera topologies? If so, what is the spatial configuration?
28. What microphone arrays are we relying on? Are we exclusively using the Ray-Ban microphones, or adding ambient mics?
29. How do we achieve sub-millisecond synchronization between multiple camera/audio streams if we expand beyond a single device?
30. Is edge AI processing required on the companion mobile device to redact PII before cloud upload?

### 3.2 Cloud Infrastructure & Scalability

31. Given the ap-south-1 data residency requirement, how do we design multi-region failover if we expand beyond India?
32. What is the expected concurrency of live video streams during peak school hours (e.g., 9:00 AM to 11:00 AM IST)?
33. Are we utilizing a serverless architecture for variable workloads, or a persistent Kubernetes cluster for GPU processing?
34. What is the acceptable latency budget for real-time processing pipelines (e.g., ASR, diarization, emotion detection)?
35. How are we orchestrating GPU scheduling for heavy multimodal models to minimize idle costs?
36. Are we planning on self-hosting GPU clusters or relying on managed cloud providers (AWS/GCP/Azure)?
37. What is the projected storage architecture for raw video data? Are we tiering storage (e.g., S3 Standard to Glacier) based on the academic calendar?

### 3.3 AI, ML & Multimodal Pipelines

38. What is the exact multimodal fusion strategy? Are we using early fusion, late fusion, or hybrid fusion for audio and visual streams?
39. Which ASR models are we evaluating for high-noise classroom environments (e.g., Whisper v3, custom conformers)?
40. How will we perform accurate speaker diarization when there are 30+ students in a highly reverberant room?
41. What vector databases (e.g., Qdrant, Milvus) are we evaluating for long-context memory and semantic search of classroom transcripts?
42. How are we modeling temporal events (e.g., a teacher asks a question, waits 5 seconds, a student answers)?
43. What is the strategy for long-context video understanding? Are we extracting keyframes or using spatio-temporal transformers?
44. How will the system perform slide semantic analysis and whiteboard OCR simultaneously with action recognition?
45. Are we utilizing LLM agents for orchestration of these sub-tasks, and if so, which foundational models?

### 3.4 ML Ops & Data Pipelines

46. Currently, data flow is restricted to synthetic/test sessions. How are we generating high-fidelity synthetic classroom data to train the models?
47. What is the annotation workflow for when we receive real data? Will we use in-house experts or outsourced labeling?
48. How do we handle concept drift when teaching methodologies evolve or vary significantly between regions?
49. Are we exploring privacy-preserving ML techniques (e.g., federated learning) to improve models without centralizing PII?
50. What is the continuous retraining pipeline architecture? How frequently will models be updated?

### 3.5 Security & Observability

51. What is the Role-Based Access Control (RBAC) model for school districts (District Admin, Principal, Teacher, Student)?
52. How are we implementing end-to-end encryption for video streams originating from the Meta Ray-Bans?
53. What observability stack (e.g., Prometheus, Grafana, Datadog) will we use to monitor inference latency, GPU utilization, and ASR error rates?
54. How do we detect and alert on anomalous data patterns (e.g., a teacher covering the camera lens)?
55. What is our strategy for securing API endpoints and preventing unauthorized data scraping?

---

## 4. NEXT STEPS

A formal review meeting is required to process these questions. Responses will be codified into Architectural Decision Records (ADRs) and the foundational Product Requirements Document (PRD). Implementation remains blocked until critical ambiguities (specifically regarding privacy bounds and real-time latency budgets) are resolved.
