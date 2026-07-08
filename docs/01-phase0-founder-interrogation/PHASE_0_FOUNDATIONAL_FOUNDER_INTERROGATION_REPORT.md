# PHASE 0: FOUNDATIONAL FOUNDER INTERROGATION REPORT

## Executive Summary

This document serves as the foundational interrogation framework for the PedagogyX platform. As the Principal Research Architect and Lead Systems Engineer, this report acts as the critical barrier before any production implementation begins. We must rigorously extract precise product requirements, technical constraints, legal boundaries, and pedagogical philosophies from the founding team.

This interrogation matrix is designed to force explicit decisions, eliminate ambiguous requirements, and expose architectural risks early.

---

## 1. Epistemological State (Knowledge Matrix)

Before diving into the questions, we must clearly define the current epistemological state of the project.

### 1.1 Validated Facts

- The system is a multimodal AI classroom intelligence platform.
- The system analyzes teacher voice, classroom video, slides, and whiteboard content.
- The system measures pedagogical efficiency and student engagement.
- The MVP (Phase 0) targets Meta Ray-Ban glasses via `clients/android-capture-dat`.
- Production school data is currently blocked pending G2 (India legal sign-off).
- Synthetic test sessions are currently allowed.

### 1.2 Assumptions

- Assume we will need to deploy robust Hindi-English code-switching models due to India-focused deployment constraints.
- Assume the platform operates in a hybrid edge-cloud paradigm (Ray-Ban glasses for edge capture, cloud for heavy inference).
- Assume latency is critical for certain real-time coaching features, but post-processing is acceptable for longitudinal analytics.
- Assume a microservices architecture leveraging Docker/Kubernetes is the intended deployment model.

### 1.3 Hypotheses

- _Hypothesis 1:_ Real-time teacher feedback via audio (e.g., bone conduction on smart glasses) will improve instructional quality faster than post-class dashboard reviews.
- _Hypothesis 2:_ Multimodal fusion of speech (transcript), audio (prosody), and vision (teacher/student posture) will yield significantly more accurate engagement metrics than unimodal analysis.
- _Hypothesis 3:_ An event-driven architecture using Redis Streams or Celery for the Cold Path AI inference pipeline can efficiently handle the variable load of 45-60 minute classroom recordings.

### 1.4 Speculative Ideas

- Integration of federated learning to allow schools to train specialized models locally without exporting PII.
- Generative AI simulation of classrooms for teacher pre-training (VR integration).
- Autonomous drone or multi-camera smart classroom pods to replace Ray-Ban glasses in permanent installations.

---

## 2. Product Interrogation

### 2.1 Core Business & Market Strategy

1. Is this enterprise SaaS, or is there a direct-to-consumer/direct-to-teacher play?
2. Are the primary buyers individual schools, large school districts, university systems, or government education ministries?
3. What are the specific target countries for the initial rollout beyond India?
4. What is the expected pricing model (per teacher, per student, per classroom, per school)?
5. Is the primary value proposition instructional coaching (formative), teacher evaluation (summative), or both?
6. Are teachers the primary end-users, or are administrators/principals the primary consumers of the analytics?
7. Will teacher unions be consulted or involved in the deployment process? How do we handle union objections to continuous monitoring?
8. Is there a "freemium" tier planned to drive grassroots adoption among individual teachers?
9. Who owns the intellectual property of the recorded sessions (the teacher, the school, or PedagogyX)?
10. If a teacher leaves a school, does their longitudinal data travel with them or stay with the institution?

### 2.2 Operational Modalities

11. Is this system exclusively for physical classrooms, or must it support online/hybrid environments (e.g., Zoom/Teams integration)?
12. Is the primary feedback mechanism real-time (during class) or post-processing (after class)?
13. If real-time, what is the maximum acceptable latency from event occurrence to feedback delivery?
14. Is offline mode strictly required for schools with poor internet connectivity? For how long must the edge device buffer data?
15. Will the system operate in low-bandwidth environments? What is the minimum required uplink speed?
16. Is a mobile-first dashboard required for teachers, or is a desktop-first approach acceptable?
17. Are we building a hardware-agnostic platform, or will we strictly bundle with specific hardware (e.g., Meta Ray-Ban)?
18. Do we require permanent in-classroom camera installations for non-wearable deployments?

### 2.3 Privacy, Legal & Compliance

19. Is China-style surveillance (constant biometric tracking, emotional scoring tied to disciplinary action) acceptable to the business model, or strictly prohibited?
20. Is student facial analysis and recognition allowed?
21. Is biometric tracking (e.g., gaze estimation, posture tracking, micro-expression analysis) allowed?
22. Which legal jurisdictions take absolute priority (e.g., India DPDP, US FERPA, EU GDPR)?
23. What is the exact data retention policy? Do we delete raw video immediately after inference, or retain it for model training?
24. If we retain video for model training, how is explicit consent gathered from minors' guardians?
25. Is human-in-the-loop (HITL) review mandatory for the AI coaching insights?
26. Is explainable AI mandatory? Must the system provide the exact timestamp/clip that triggered a specific piece of feedback?
27. Are teacher scores public within the school, or strictly private to the teacher and their designated coach?
28. Will the system include an explicit "off" switch or privacy shutter that the teacher can easily verify?
29. How do we handle incidental capture of sensitive information (e.g., a student discussing a personal issue with the teacher)?
30. Is there a process for automated PII redaction (face blurring, name bleeping) before data hits cloud storage?

### 2.4 Pedagogical & Feature Requirements

31. Should the AI score pedagogy based on a specific, established framework (e.g., Danielson Framework, Marzano, CLASS), or a proprietary PedagogyX model?
32. Should the AI detect the emotional tone of the teacher? If so, what taxonomy of emotions is used?
33. Should the AI evaluate student engagement? How is "engagement" defined (behavioral, cognitive, emotional)?
34. Is multilingual support required on day one? (Confirmed: Hindi-English code-switching is required). What other languages are next?
35. Does the system need to OCR handwritten notes on physical whiteboards, or only digital slides?
36. Will the system generate automated lesson plans or adapt existing ones based on classroom performance?
37. Must the system detect specific instructional activities (e.g., lecture, small group work, silent reading, Q&A)?
38. Should the platform identify specific students by name to track individual engagement, or only aggregate classroom engagement?
39. Does the system need to measure the Teacher Talk Time (TTT) vs. Student Talk Time (STT) ratio?
40. Will there be a feature for teachers to challenge or correct AI-generated feedback?

---

## 3. Technical Interrogation

### 3.1 Architecture & Scalability

41. What is the expected scale on day 1 vs. day 365 (concurrent classrooms, total hours of video per day)?
42. Is a cloud-native architecture acceptable, or must we support on-premise deployments for highly secure/government environments?
43. What is the exact target for end-to-end latency in the real-time inference pipeline?
44. How do we handle network partitions between the edge device (glasses) and the cloud during a live session?
45. Should we optimize for lowest infrastructure cost, or lowest latency, given that both cannot be perfectly maximized?
46. What is the strategy for horizontal scaling of the inference workers?
47. Are we utilizing a distributed event-streaming platform (e.g., Kafka, Redpanda) or relying on Redis/Celery?
48. What is the database strategy for handling high-frequency time-series data (engagement metrics per second)?

### 3.2 Hardware & Edge Capture

49. What are the thermal and battery constraints of the Meta Ray-Ban glasses during continuous 60-minute recording?
50. If the Meta Ray-Ban is the primary client, how do we handle the fact that it only records in short bursts natively? Are we using a custom firmware/app hack?
51. What is the audio quality and microphone array configuration on the edge device? Is it sufficient for far-field student voice capture?
52. Do we need auxiliary microphones deployed in the classroom to capture student responses accurately?
53. How do we synchronize multiple AV streams if auxiliary cameras/microphones are used?
54. What happens if the edge device storage is filled during a network outage?

### 3.3 AI & ML Pipelines

55. What is the strategy for continuous model retraining?
56. How do we build a robust, scalable data annotation and labeling pipeline for classroom data?
57. Are we synthesizing data for edge cases (e.g., rare classroom disruptions) using generative models?
58. What is the exact ML Ops pipeline for deploying updated ASR (faster-whisper) models to production without downtime?
59. How are we handling the long-context memory problem for a 60-minute class? Are we chunking, or using long-context LLMs (e.g., Gemini 1.5 Pro)?
60. What vector database (e.g., Milvus, Qdrant, Pinecone) is planned for multimodal embeddings and semantic search of classroom moments?
61. For multimodal fusion (audio + video), are we doing early fusion, late fusion, or hybrid fusion?
62. How are we implementing the ASR pipeline to support robust Hindi-English code-switching?
63. Are we utilizing LLM agents for orchestration? If so, what framework (LangChain, AutoGen, custom)?

### 3.4 Security & Observability

64. What is the exact Role-Based Access Control (RBAC) model?
65. How are we encrypting data in transit and at rest? Is KMS/BYOK supported for enterprise clients?
66. What observability stack (e.g., Prometheus, Grafana, Datadog, OpenTelemetry) is mandated for the distributed tracing of inference pipelines?
67. How do we monitor model drift and performance degradation over time?
68. What are the automated security testing requirements in the CI/CD pipeline (e.g., SAST, DAST)?
69. How do we detect and alert on edge device failures or tampering during a session?
70. What is the disaster recovery and business continuity plan for the primary cloud region?

---

## 4. Execution Directives & Next Steps

This document is step one of the Phase 0 foundational research. The founders must review these questions and provide definitive answers. Ambiguity in these answers will translate directly to technical debt, architecture revisions, and product failure.

Once answers are provided, the engineering team will proceed to stack evaluation, competitor analysis, and architectural design. No production code for the core application (beyond the current MVP boilerplate) will be written until this foundational phase is complete and signed off.
