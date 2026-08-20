# PRINCIPAL ARCHITECT PHASE 0 REPORT v1

**CONFIDENTIAL INTERNAL RESEARCH DOCUMENT**
**AUTHOR:** Autonomous Principal Research Architect & Lead Systems Engineer
**PROJECT:** PedagogyX - Multimodal AI Classroom Intelligence Platform
**STATUS:** PRE-IMPLEMENTATION (Phase 0)

## EXECUTIVE SUMMARY

This document represents the Phase 0 foundational interrogation for PedagogyX. As the Autonomous Principal Research Architect, my mission is to stabilize the architecture, identify risks, and explicitly define the product and technical scope before a single line of production code is written. This platform is not a rushed MVP; it is designed to rival or exceed global leaders in educational intelligence such as Edthena, Vosaic, IRIS Connect, AI Sokrates, and advanced multimodal classroom research systems.

This interrogation forces precise product decisions, identifies contradictions, and challenges all assumptions.

---

## 1. EPISTEMOLOGICAL STATE: FACTS, ASSUMPTIONS, HYPOTHESES, IDEAS

To maintain architectural rigor, we must clearly separate what we know from what we believe.

### Validated Facts

- The primary v1 client is Meta Ray-Ban via the DAT (clients/android-capture-dat) application (ADR-0009).
- Production school data for PedagogyX remains blocked until G2 (India legal sign-off). Allowed development scope is restricted to docs, `benchmarks/`, boilerplate dev stack, and synthetic test sessions only.
- The system architecture utilizes a Hybrid Edge/Cloud topology (ADR-0008) to process multimodal data streams under strict hardware constraints (max 12GB VRAM per node).
- The technical stack includes Python (FastAPI) and Node.js for backend services, PyTorch and ONNX for AI/ML, FFmpeg for video processing, and PostgreSQL, Qdrant, and Redis for data/vector storage.

### Assumptions

- _Assumption 1:_ The 12GB VRAM edge node constraint implies we will rely heavily on optimized, quantized models (e.g., ONNX, TensorRT, or INT8/INT4 weights) for local inference (e.g., local transcription, basic object detection) before sending embeddings or metadata to the cloud.
- _Assumption 2:_ Meta Ray-Ban glasses will provide sufficient battery life and thermal headroom to record a standard 45-60 minute classroom session without catastrophic failure.
- _Assumption 3:_ A multimodal knowledge graph architecture will be necessary to fuse asynchronous streams (voice, video, slide text) into cohesive temporal events.
- _Assumption 4:_ AI coaching insights will be generated asynchronously post-class, not in real-time on the edge device, due to compute constraints.

### Hypotheses

- _Hypothesis 1 (Pedagogical Efficacy):_ Providing teachers with objective metrics (e.g., teacher-to-student speaking ratios, interaction heatmaps) will lead to measurable improvements in instructional pacing over a 3-month longitudinal period.
- _Hypothesis 2 (Multimodal Fusion):_ Fusing audio transcription (ASR) with visual gesture recognition (CV) will yield a 20% increase in the accuracy of detecting student engagement compared to unimodal analysis.
- _Hypothesis 3 (Edge Offloading):_ Performing initial FFmpeg frame extraction and lightweight audio separation at the edge will reduce required cloud bandwidth by 60%, making the system viable in low-bandwidth Indian school environments.

### Speculative Ideas

- _Idea 1 (Federated Learning):_ In subsequent phases, utilize federated learning to refine speech emotion recognition models locally on edge devices to maintain strict privacy compliance without centralized audio storage.
- _Idea 2 (Generative AI Avatars):_ Create interactive, personalized AI coaching avatars that role-play difficult classroom management scenarios based on a teacher's historical weaknesses.
- _Idea 3 (Ambient Hallucination Detection):_ Implement a secondary LLM pipeline specifically designed to audit the primary AI feedback engine, ensuring that instructional coaching insights do not hallucinate pedagogical theories.

---

## 2. EXHAUSTIVE PRODUCT INTERROGATION (100 Questions)

To finalize the product architecture, the founder must provide explicit answers to the following questions. Vagueness is unacceptable.

### 2.1 Market & Business Model

1. Is this enterprise SaaS or consumer?
2. Is this B2B (selling to districts/schools) or B2C (selling to individual teachers)?
3. Is this for primary/secondary schools, universities, or corporate training?
4. Are governments a target client (B2G)?
5. Is the primary purpose teacher self-improvement, instructional coaching, or administrative surveillance?
6. What countries are the immediate target markets outside of the India pilot?
7. Is China-style continuous administrative surveillance acceptable, or is this strictly a private coaching tool for the teacher?
8. Will administrators have access to raw teacher analytics or only aggregated, anonymized scores?
9. Are teachers' unions involved in the deployment, and have their requirements been gathered?
10. What is the expected pricing model (per teacher, per school, per student)?
11. Are there specific funding grants (e.g., Title I) we are aiming to qualify for?
12. How does the business model scale with computational costs of video analysis?
13. Is white-labeling a requirement for large school districts?
14. Will there be an API available for third-party LMS integration?
15. Do we expect to monetize aggregated, anonymized pedagogical data?

### 2.2 Environment & Modality

16. Is this exclusively for physical classrooms, online classes, or hybrid environments?
17. Is offline mode strictly required, or can the edge device buffer and upload when network is restored?
18. How long must the edge device buffer if offline? (e.g., 24 hours of recording?)
19. Is low-bandwidth mode required for rural deployments?
20. What is the absolute minimum upload bandwidth supported?
21. Is mobile-first required for the teacher dashboard?
22. Will the system need to integrate with physical classroom hardware (e.g., smartboards, projectors)?
23. How do we handle acoustic challenges like extreme echo or outdoor background noise?
24. How many distinct speakers must the system differentiate in a single room?
25. Is there a strict limit on the duration of a single recording session?
26. Do teachers wear lapel mics in addition to the Meta Ray-Bans?
27. Are there secondary fixed cameras in the room?
28. How do we handle network partitions during live streaming?
29. Does the system need to operate on constrained institutional Wi-Fi (e.g., captive portals)?
30. Are there specific physical accessibility requirements for the hardware?

### 2.3 Ethics, Privacy, & Compliance

31. Is privacy-first architecture required at the hardware level (e.g., physical mute/blind switches)?
32. What legal jurisdictions matter for Phase 1 and Phase 2?
33. Is FERPA compliance required?
34. Is GDPR compliance required?
35. Is India DPDP (Digital Personal Data Protection) compliance strictly required before any non-synthetic data ingestion?
36. Is student facial analysis explicitly allowed, or must faces be blurred/anonymized at the edge?
37. Is biometric analysis (e.g., gait, micro-expressions) allowed?
38. Is explainable AI (XAI) mandatory for any generated coaching insights?
39. Is human-in-the-loop (HITL) review mandatory before feedback is delivered to a teacher?
40. How is explicit consent gathered from parents/minors?
41. Can a student opt-out, and if so, how does the system dynamically mask them?
42. Is data retention policy fixed (e.g., 30 days) or customizable per tenant?
43. Are there requirements for immutable audit logs of who viewed which recording?
44. How do we handle "right to be forgotten" requests for ML models?
45. Is encrypted local storage on the edge node required?
46. Do we need third-party security audits before launch?
47. How are AI hallucinations handled in the context of professional evaluation?
48. What is the liability model if the AI gives incorrect pedagogical advice?
49. Are there specific DEI (Diversity, Equity, Inclusion) fairness metrics the models must pass?
50. How do we prevent bias against specific accents or dialects?

### 2.4 Product Features & AI Capabilities

51. Should the AI score pedagogy on a standardized rubric (e.g., Danielson Framework)?
52. If yes to a rubric, can districts customize the rubric?
53. Should the AI detect emotional tone (speech emotion recognition) of the teacher?
54. Should the AI detect emotional tone of the students?
55. Should the AI evaluate individual student engagement, or only aggregate classroom engagement?
56. Is multilingual support required from day one, and if so, which languages/dialects (e.g., Hindi, Hinglish)?
57. Is the system real-time or post-processing only?
58. Are teacher scoring metrics public within the school, or strictly private?
59. Does the system automatically detect transitions between instructional phases (e.g., lecture to group work)?
60. Is whiteboard OCR required to index what was written during class?
61. Should the system cross-reference teacher speech with slide deck content?
62. How granular is the feedback? (e.g., timestamped annotations vs. overall summary?)
63. Are there gamification elements for teacher improvement?
64. Does the system suggest specific external resources (e.g., articles, videos) based on identified weaknesses?
65. Can teachers edit or reject AI-generated feedback?
66. Is there a peer-review feature for teachers to share clips with colleagues?
67. Does the system track longitudinal progress (e.g., week over week)?
68. How does the system handle co-teaching or guest speakers?
69. Should the AI generate automatic lesson summaries for students?
70. Is there an interactive chatbot for the teacher to query their own data ("How much time did I spend talking today?")?

### 2.5 Scalability, Infra, & MLOps

71. What is the expected latency SLA for post-class analysis delivery?
72. How are we handling GPU scheduling in the cloud? Are we using Ray or standard K8s autoscaling?
73. What is the exact data labeling and annotation workflow for fine-tuning our pedagogy models?
74. Since production data is blocked, what is our synthetic data generation pipeline?
75. What LLM and generation strategy are we using to create realistic "noisy classroom" synthetic data?
76. How are we implementing privacy-preserving ML techniques? Are we anonymizing PII before data hits the training buffer?
77. What is our observability stack for tracking inference bottlenecks and VRAM usage on the edge node?
78. How do we handle model retraining and deployment (CI/CD for ML)?
79. What is the security architecture and role-based access control (RBAC) model for preventing unauthorized access to classroom video streams?
80. How many concurrent classroom streams must a single edge node process?
81. What is the expected peak throughput to the cloud during end-of-day synchronization?
82. Are we using serverless GPU inference for unpredictable burst loads?
83. What is the disaster recovery and backup strategy for the vector database (Qdrant)?
84. How do we version multimodal datasets?
85. What is the A/B testing framework for new model iterations?
86. How are we monitoring model drift in production?
87. What is the maximum acceptable cost per hour of processed video?
88. Are we multi-cloud, or locked into AWS/GCP/Azure?
89. How do we handle schema migrations in the knowledge graph?
90. What is the strategy for caching expensive LLM calls?

### 2.6 Edge vs. Cloud Pipeline

91. What is the exact synchronization pipeline between the Meta Ray-Ban client (DAT) and the 12GB VRAM edge node?
92. Are we streaming RTSP locally, or uploading chunked files?
93. What are the fallback mechanisms if the edge node fails mid-recording?
94. Are we running the ASR (Automatic Speech Recognition) model on the edge or in the cloud?
95. If edge, which quantized model fits in the remaining VRAM alongside CV tasks?
96. How do we handle clock drift between the Meta Ray-Ban audio stream and potential secondary classroom camera feeds?
97. Does the edge node perform local face blurring before upload?
98. What is the hardware lifecycle of the edge node (e.g., replace every 3 years)?
99. How are OTA (Over-The-Air) updates pushed to the edge nodes securely?
100.  If the Meta Ray-Ban loses Bluetooth connection to the edge node, how is data buffered on the glasses?

---

## 3. RISKS & UNKNOWNS

- **Risk 1 (Hardware Constraint):** Relying on Meta Ray-Ban glasses as the primary client introduces massive risks regarding battery life, thermal throttling, and field-of-view limitations for capturing entire classrooms.
- **Risk 2 (Edge Compute):** The strict 12GB VRAM limit on the edge node heavily restricts the size and accuracy of local models. Over-offloading to the cloud will break low-bandwidth requirements.
- **Risk 3 (Data Compliance Block):** The India legal sign-off block means we cannot train on real classroom data. Over-reliance on synthetic data may result in models that fail catastrophically when exposed to real-world acoustic environments (e.g., fan noise, cross-talk).
- **Risk 4 (Temporal Synchronization):** Aligning multiple multimodal streams without a centralized hardware clock is notoriously difficult and can lead to degraded model performance.
- **Unknown 1:** The exact pedagogical framework the AI is expected to use for evaluation.
- **Unknown 2:** The legal viability of capturing student faces/voices without explicit per-student parental consent in target jurisdictions.

---

## 4. NEXT STEPS & IMMEDIATE ACTION ITEMS

1.  **Founder Review:** The founder must review this interrogation document and provide written answers to all questions in Section 2.
2.  **Architecture Stabilization:** Based on the answers, formulate the final Phase 1 system architecture (ADR-0010: Finalized Infrastructure Pipeline).
3.  **Synthetic Data Generation:** Immediately prioritize the creation of the synthetic test session pipeline to unblock the ML engineering team while waiting for G2 sign-off.
4.  **Edge Node Benchmarking:** Conduct stress tests on the 12GB VRAM edge node using candidate quantized ASR and CV models to establish baseline performance metrics.

EOF
