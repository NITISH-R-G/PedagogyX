# PRINCIPAL ARCHITECT PHASE 0 FOUNDER INTERROGATION REPORT

**Document Type:** Foundational Architecture & Product Requirements Interrogation
**Author:** Principal Research Architect & Lead Systems Engineer, PedagogyX
**Status:** DRAFT / BLOCKING IMPLEMENTATION
**Context:** Phase 0 - Pre-Implementation Risk & Requirements Discovery

## 1. EXECUTIVE SUMMARY

Before any production code is written or system architecture is finalized, the following exhaustive interrogation must be resolved. We are building a world-class multimodal AI classroom intelligence platform. Hallucinating requirements will lead to catastrophic technical debt. This document serves as the absolute foundational block for product alignment, risk mitigation, and technical feasibility scoping. Implementation remains firmly blocked until these structural constraints are explicitly documented.

---

## 2. PRODUCT & BUSINESS STRATEGY QUESTIONS

### 2.1 Target Audience, Market Positioning, & Core Use Cases

1. Is PedagogyX primarily an enterprise SaaS platform (B2B), a direct-to-educator tool (B2C), or a government-level infrastructure (B2G)?
2. If B2B, are the primary buyers school districts, individual schools, universities, or corporate training departments?
3. What is the fundamental value proposition: is this designed for teacher self-improvement (coaching), administrator oversight (surveillance), or automated grading/evaluation?
4. Will the system be deployed in physical classrooms, online classes, or hybrid learning environments?
5. What are the specific target countries for the initial rollout and subsequent phases?
6. Given the India DPDP compliance requirements, are we exclusively targeting the Indian market first? What is the timeline for global expansion?
7. Is mobile-first design required for teacher dashboards and insights? Or is desktop access sufficient?
8. Are teachers unionized in our target markets, and if so, what are the union regulations regarding AI evaluation of instructional quality?
9. Is real-time inference and feedback required (e.g., in-ear coaching), or is post-processing (batch processing after class) acceptable?
10. Is an offline mode or low-bandwidth mode required for classrooms with poor internet connectivity?
11. Should the platform support multilingual classrooms? Which languages are mandatory for v1?
12. How will we handle code-switching (e.g., mixing English and Hindi) during live sessions?
13. Can administrators see individual teacher analytics, or is the data strictly siloed for the teacher's private coaching?
14. Is human-in-the-loop (expert reviewer) mandatory before feedback is delivered to the teacher?
15. Will the AI actively score pedagogical effectiveness (e.g., giving a score out of 100), or will it only provide descriptive analytics?
16. Are we building public leaderboards for instructional quality, or is all scoring strictly private?
17. What is the exact success metric for the pilot program?
18. How do we quantify an improvement in teaching methodology objectively?
19. What is the allowable false positive rate for negative pedagogical feedback?
20. Will students have access to the system, or is it strictly teacher/admin facing?
21. Are we integrating with existing Learning Management Systems (LMS)? If so, which ones (Canvas, Blackboard, Moodle)?
22. Do we expect to charge per teacher, per school, per student, or per classroom?
23. Will there be a freemium model, or is it purely enterprise licensing?
24. How do we handle substitution teachers or guest lecturers?
25. Can teachers opt out of specific types of analysis (e.g., voice tone)?
26. How are we preventing the system from being weaponized for punitive measures by school administrators?
27. Do we need to support special education environments, which may have highly variable behavioral patterns?
28. Is there a physical hardware distribution model we must support, or bring-your-own-device (BYOD)?
29. How do we onboard a school with 100 teachers vs a district with 10,000 teachers?
30. What is the expected churn rate and how does the AI provide immediate sticky value in week 1?

### 2.2 Legal, Ethical, Privacy & Surveillance Boundaries

31. Is China-style behavioral surveillance (tracking every student's gaze, posture, micro-expressions) acceptable or explicitly forbidden by company policy?
32. Is student facial analysis and biometric tracking allowed, or must all student faces be blurred/anonymized at the edge?
33. Which specific legal jurisdictions are we optimizing compliance for in v1 (e.g., GDPR, FERPA, COPPA, India DPDP)?
34. Under India DPDP, how do we handle consent mechanisms for minors in the classroom? Is it opt-in or opt-out?
35. How do we handle a student whose parent explicitly denied consent, but they are physically in the classroom being recorded?
36. Is explainable AI (XAI) mandatory for all AI-generated coaching insights? How deep must the traceability be?
37. If a teacher disputes an AI-generated pedagogical score, what is the arbitration and auditing process?
38. What are the data retention policies for raw classroom video/audio versus processed analytics?
39. Are we legally mandated to delete raw video data immediately after processing?
40. How do we handle requests for data deletion (Right to be Forgotten) from students who have graduated?
41. Who owns the extracted intellectual property (the insights, the models trained on the school's data)?
42. Is it legally permissible to use one school's anonymized data to improve the model for a competing school district?
43. How are we auditing the system for racial, gender, and linguistic bias in pedagogical evaluation?
44. Will we undergo third-party ethical algorithmic auditing before launch?
45. How do we handle mandated reporting situations (e.g., AI detects signs of abuse or bullying in the classroom)?
46. What is the legal liability if our system misinterprets a classroom event?
47. Are we indemnifying schools against privacy lawsuits?
48. How do we handle Law Enforcement Agency (LEA) requests for classroom footage?
49. Do we have a legal strategy for preventing reverse engineering of anonymized data?
50. What is the fallback if biometric privacy laws become stricter mid-development?

---

## 3. TECHNICAL & ARCHITECTURAL QUESTIONS

### 3.1 Hardware, Edge Integration, & Signal Acquisition

51. The v1 hardware client is Meta Ray-Ban. How are we bypassing or managing the battery and thermal limitations of these glasses during a 45-60 minute class?
52. Are we streaming live from the Meta Ray-Bans to a mobile companion app, and then to the cloud, or directly to the cloud?
53. What happens when the Bluetooth connection between the glasses and the companion device drops?
54. Are we supplementing the Ray-Bans with fixed classroom camera topologies? If so, what is the spatial configuration?
55. What microphone arrays are we relying on? Are we exclusively using the Ray-Ban microphones, or adding ambient mics?
56. How do we achieve sub-millisecond synchronization between multiple camera/audio streams if we expand beyond a single device?
57. Is edge AI processing required on the companion mobile device to redact PII (blurring faces) before cloud upload?
58. What is the expected frame rate and resolution required for accurate multimodal inference? Is 720p at 15fps sufficient, or do we need 1080p at 30fps?
59. How does the system handle rapid head movements (motion blur) common with head-mounted wearables?
60. What is the strategy for audio occlusion (teacher turns away from the class while speaking)?
61. Can we guarantee audio intelligibility for students sitting in the back row?
62. Are we implementing active noise cancellation pipelines at the edge to remove HVAC or external street noise?
63. How do we handle classroom lighting variability (glare, dark rooms during projector use)?
64. Is the companion app running on iOS, Android, or both? What are the minimum OS requirements?
65. What is the fail-safe if the mobile device runs out of storage during an offline session?
66. Are we building custom embedded hardware long-term, or sticking with consumer wearables?
67. How do we manage firmware updates for edge devices securely?
68. What is the expected bandwidth requirement per classroom? (e.g., 5 Mbps continuous upload)?
69. Can the system gracefully degrade features under extreme network congestion?
70. How do we handle clock drift between the mobile device and the server during long sessions?

### 3.2 Cloud Infrastructure, Scalability, & Deployment

71. Given the ap-south-1 data residency requirement, how do we design multi-region failover if we expand beyond India?
72. What is the expected concurrency of live video streams during peak school hours (e.g., 9:00 AM to 11:00 AM IST)?
73. Are we utilizing a serverless architecture for variable workloads, or a persistent Kubernetes cluster for GPU processing?
74. What is the acceptable latency budget for real-time processing pipelines (e.g., ASR, diarization, emotion detection)?
75. How are we orchestrating GPU scheduling for heavy multimodal models to minimize idle costs?
76. Are we planning on self-hosting GPU clusters or relying on managed cloud providers (AWS/GCP/Azure)?
77. What is the projected storage architecture for raw video data? Are we tiering storage (e.g., S3 Standard to Glacier) based on the academic calendar?
78. How do we handle the massive "thundering herd" problem when 10,000 teachers end their classes at exactly 10:00 AM and upload videos simultaneously?
79. What is the maximum acceptable processing time before a teacher receives their post-class report? (e.g., 5 minutes, 1 hour, 24 hours?)
80. What is the disaster recovery RTO (Recovery Time Objective) and RPO (Recovery Point Objective)?
81. How are we scaling WebSocket connections for live transcription dashboards?
82. What is our strategy for stateless vs stateful microservices?
83. Are we using Apache Kafka or RabbitMQ for the central event bus?
84. How do we handle schema evolution in our event streams without breaking downstream ML models?
85. What is the CDN strategy for delivering processed highlight reels back to the teachers?
86. How are we handling multi-tenancy at the database layer (Row-level security vs isolated databases per district)?
87. What is our strategy for zero-downtime deployments during the school year?
88. How are we managing secrets and configuration across environments (Vault, AWS Secrets Manager)?
89. What is the SLA we are legally bound to provide to enterprise clients?
90. How do we implement backpressure in our video ingestion pipeline if inference nodes are overwhelmed?

### 3.3 AI, ML, & Multimodal Inference Pipelines

91. What is the exact multimodal fusion strategy? Are we using early fusion, late fusion, or hybrid fusion for audio and visual streams?
92. Which ASR (Automatic Speech Recognition) models are we evaluating for high-noise classroom environments (e.g., Whisper v3, custom conformers)?
93. How will we perform accurate speaker diarization when there are 30+ students in a highly reverberant room?
94. What vector databases (e.g., Qdrant, Milvus, Pinecone) are we evaluating for long-context memory and semantic search of classroom transcripts?
95. How are we modeling temporal events (e.g., a teacher asks a question, waits 5 seconds, a student answers)?
96. What is the strategy for long-context video understanding? Are we extracting keyframes or using spatio-temporal transformers?
97. How will the system perform slide semantic analysis and whiteboard OCR simultaneously with action recognition?
98. Are we utilizing LLM agents for orchestration of these sub-tasks, and if so, which foundational models (GPT-4, Claude 3.5 Sonnet, Llama 3)?
99. How are we detecting instructional pacing (speaking rate, pause duration, wait time)?
100.  Are we implementing a custom knowledge graph to map the curriculum being taught to standard state/national curricula?
101.  How do we handle domain-specific vocabulary (e.g., advanced physics terminology) that standard ASR models misinterpret?
102.  What is the strategy for speech emotion recognition (SER) without crossing ethical boundaries?
103.  How are we quantifying "student engagement" without relying on pseudoscientific facial emotion tracking?
104.  Are we using foundational vision models (e.g., Florence-2, CLIP) for zero-shot classroom activity recognition?
105.  How do we prevent hallucinations when the LLM generates the final coaching feedback?
106.  What is the latency overhead of chaining multiple foundation models together (ASR -> LLM -> Vector DB -> Coaching LLM)?
107.  Are we compiling models to ONNX or TensorRT for faster inference?
108.  How are we handling the context window limits of LLMs for a 60-minute highly dense class transcript?
109.  What is the strategy for grounding the AI feedback in established pedagogical frameworks (e.g., Danielson Framework, Marzano)?
110.  How do we build an evaluation pipeline (EvalOps) to measure if our AI coaching is actually accurate against human experts?

### 3.4 ML Ops, Data Pipelines, & Model Lifecycle

111. Currently, data flow is restricted to synthetic/test sessions. How are we generating high-fidelity synthetic classroom data to train the models?
112. What is the annotation workflow for when we receive real data? Will we use in-house experts or outsourced labeling?
113. How do we handle concept drift when teaching methodologies evolve or vary significantly between regions?
114. Are we exploring privacy-preserving ML techniques (e.g., federated learning) to improve models without centralizing PII?
115. What is the continuous retraining pipeline architecture? How frequently will models be updated?
116. How do we version control our datasets (DVC)?
117. What is the strategy for shadow testing new model versions in production without affecting user UX?
118. How do we handle active learning? (Identifying edge case classrooms and requesting human labeling).
119. What is the expected cost per hour of inference per classroom, and how does that align with unit economics?
120. Are we implementing strict reproducibility standards for all ML experiments?

### 3.5 Security, IAM, & Observability

121. What is the Role-Based Access Control (RBAC) model for school districts (District Admin, Principal, Teacher, Student, Parent)?
122. How are we implementing end-to-end encryption for video streams originating from the Meta Ray-Bans?
123. What observability stack (e.g., Prometheus, Grafana, Datadog) will we use to monitor inference latency, GPU utilization, and ASR error rates?
124. How do we detect and alert on anomalous data patterns (e.g., a teacher covering the camera lens, or a stream dropping frames)?
125. What is our strategy for securing API endpoints and preventing unauthorized data scraping?
126. How are we auditing administrative access to the platform?
127. What is the SIEM (Security Information and Event Management) strategy?
128. Are we running automated penetration testing and vulnerability scanning in CI/CD?
129. How do we handle key rotation for encryption keys used to store sensitive PII?
130. What is the incident response playbook for a suspected data breach involving student audio/video?

---

## 4. COMPETITOR ANALYSIS

To build a world-class system, we must understand the landscape. Below is a deep analysis of existing systems globally.

### 4.1 Edthena

- **Architecture Assumptions:** Cloud-centric asynchronous video upload, likely standard microservices, basic NLP on transcripts.
- **Likely Stack:** AWS, React, Python/Django, basic ASR APIs.
- **Strengths:** Strong entrenchment in US K-12, highly familiar to instructional coaches, solid workflow for peer feedback.
- **Weaknesses:** Highly manual, lacks deep autonomous AI analysis, low real-time capability, primarily an asynchronous workflow tool.
- **Disruption Opportunity:** Automate the entire feedback loop using multimodal AI so coaches spend time reviewing high-level insights rather than manually timestamping videos.

### 4.2 Vosaic

- **Architecture Assumptions:** Video streaming focused platform, likely heavy WebRTC/HLS pipelines.
- **Likely Stack:** AWS Media Services, Node.js, specialized video players.
- **Strengths:** Excellent manual coding and tagging interfaces for video, strong in higher ed and simulation environments.
- **Weaknesses:** Missing advanced foundational AI models. It relies on the human to do the "intelligence" part.
- **Disruption Opportunity:** Introduce zero-shot action recognition and automated event tagging to replace their manual timeline creation.

### 4.3 IRIS Connect

- **Architecture Assumptions:** Proprietary hardware kits linked to cloud services, heavy emphasis on secure video transport.
- **Likely Stack:** Custom edge OS on their hardware, Azure/AWS backend, mature RBAC systems.
- **Strengths:** High trust in European markets, strong GDPR compliance, excellent physical hardware kits.
- **Weaknesses:** Expensive hardware deployments, slower to adopt bleeding-edge LLM and multimodal models.
- **Disruption Opportunity:** Utilize cheap, ubiquitous wearables (Ray-Bans) instead of heavy, expensive proprietary hardware kits.

### 4.4 AI Sokrates

- **Architecture Assumptions:** Heavy NLP and conversational analysis.
- **Strengths:** Focus on pedagogical conversational dynamics, questioning strategies.
- **Weaknesses:** Potentially lacks deep visual context analysis (whiteboard/slide integration).
- **Disruption Opportunity:** Full multimodal fusion. Don't just analyze what the teacher said, analyze what was on the slide when they said it, and how the students reacted visually.

### 4.5 Chinese Smart Classroom Systems (e.g., SenseTime, Megvii education branches)

- **Architecture Assumptions:** Heavy edge-compute, intensive computer vision, multi-camera topologies per room.
- **Likely Stack:** C++, TensorRT, custom silicon, deep learning vision models.
- **Strengths:** Incredibly advanced real-time biometric tracking, high precision facial recognition, massive datasets.
- **Weaknesses:** Completely incompatible with Western and Indian privacy standards. High surveillance, low trust. Focuses on compliance rather than pedagogical improvement.
- **Disruption Opportunity:** Build the "anti-surveillance" privacy-first alternative. Deliver equal analytical power but focused purely on teacher coaching with strict edge-anonymization.

---

## 5. RESEARCH PAPERS & SCIENTIFIC FOUNDATION

We must base our architecture on peer-reviewed literature. Continuous research is mandatory.

### 5.1 Multimodal Classroom Analytics

- **Focus:** How to fuse audio, video, and textual data to understand complex classroom dynamics.
- **Key Literature Area:** "Multimodal Learning Analytics (MMLA) in physical classrooms." We need to review papers on synchronized capture of teacher proxemics and speech.

### 5.2 Speech Emotion Recognition (SER) & Pedagogical Tone

- **Focus:** Identifying instructional enthusiasm, clarity, and pacing.
- **Limitations to Track:** Many SER models generalize poorly to noisy environments or novel accents. We must look at papers addressing domain adaptation for SER in education.

### 5.3 Teacher Effectiveness Modeling

- **Focus:** Quantifying "good teaching" based on established rubrics (CLASS, Danielson).
- **Literature Need:** Research bridging the gap between automated NLP metrics (e.g., Question/Answer ratios, wait times) and human-rated pedagogical scores.

### 5.4 Long-Context Video Understanding

- **Focus:** Summarizing a 60-minute video into a coherent coaching narrative.
- **Key Architecture:** Spatio-temporal transformers, hierarchical memory networks for long videos.

---

## 6. MANDATORY TECH STACK ANALYSIS

### 6.1 Backend

- **Go:** High concurrency, excellent for video streaming and event routing. Low latency.
- **Rust:** Highest performance, memory safety, steep learning curve. Good for core low-level pipelines.
- **Python (FastAPI):** Mandatory for ML integration. Excellent ecosystem. Risk of GIL blocking high-concurrency streams, requiring careful async/multiprocessing design.
- **Node.js:** Excellent for WebSocket handling and frontend integration. Weak for heavy computational tasks.
- **Decision Matrix:** We will likely need a polyglot architecture: Go/Node for edge ingestion/websockets, and Python for the heavy ML inference and orchestration layers.

### 6.2 AI/ML Frameworks

- **PyTorch:** Industry standard for research and deployment. Mandatory for foundational models.
- **ONNX / TensorRT:** Mandatory for deployment optimization. All models must be compiled for maximum GPU efficiency to maintain unit economics.

### 6.3 Video Pipelines

- **FFmpeg:** The foundational tool. Complex but necessary.
- **GStreamer:** Better for complex, real-time edge pipelines. Steeper learning curve.
- **WebRTC:** Essential for real-time streaming from the companion app to the cloud.

### 6.4 Databases

- **PostgreSQL:** Primary relational store (Users, Organizations, Metadata).
- **Qdrant / Milvus:** Vector databases mandatory for semantic search over transcripts and RAG for the AI coach.
- **Redis:** Caching, rate limiting, and fast ephemeral state.

### 6.5 Infrastructure & Cloud

- **Kubernetes:** Mandatory for orchestrating complex ML workloads and ensuring high availability.
- **AWS (ap-south-1):** AWS provides the deepest ML infrastructure (Inferentia, Trainium, A100/H100 instances) required for heavy workloads, while meeting data residency requirements.

---

## 7. AI FEATURES TO RESEARCH (R&D BACKLOG)

1. **Teacher Emotion Analysis:** Is it reliable across cultures?
2. **Speech Clarity Scoring:** Can we detect mumbling or acoustic issues?
3. **Classroom Engagement Heatmaps:** Can we infer engagement purely from aggregate movement/noise without facial recognition?
4. **Teacher/Student Speaking Ratios:** Essential metric (Teacher Talk Time vs Student Talk Time).
5. **Wait Time Detection:** Detecting the pause after a question.
6. **Whiteboard OCR / Slide Semantic Analysis:** Extracting context from visual aids.
7. **Hallucination-resistant Feedback:** Constraining the LLM to only output feedback backed by concrete video timestamps.

---

## 8. SCRUM, AGILE, & DOCUMENTATION REQUIREMENTS

We will operate as an elite engineering organization.

### 8.1 Agile Workflows

- Maintain strict Epics, Stories, and Tasks.
- All architectural decisions will be codified in ADRs (Architecture Decision Records).
- Weekly Sprint Planning and Retrospectives.

### 8.2 Mandatory Documentation Drafts Required Before Code

1. Product Requirements Document (PRD) v1
2. End-to-End System Architecture Diagram
3. Privacy & Data Governance Model
4. API Contracts (OpenAPI/Swagger)
5. ML Model Evaluation Protocol
6. Infrastructure-as-Code (Terraform) Specs

---

## 9. IMPLEMENTATION RULES (THE COMMITMENT)

- **No random UI coding.** We build the foundation first.
- **Contracts First:** APIs and schemas must be defined before implementation.
- **Observability First:** Logging and tracing exist before business logic.
- **Testing First:** Test-driven development for critical paths.
- **Benchmark-driven:** We optimize based on data, not guesses.

END OF REPORT
