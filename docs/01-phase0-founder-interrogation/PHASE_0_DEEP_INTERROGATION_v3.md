# Phase 0: Ultimate Deep Interrogation (v3)

## Objective

To rigorously interrogate assumptions, constraints, and long-term implications of the PedagogyX platform before proceeding to Phase 1 engineering implementation. This covers exhaustive aspects of product, technical, scaling, privacy, compliance, and user experience for the smart-glasses-primary multimodal AI classroom intelligence system.

---

## 1. Product & Business Strategy Questions

### 1.1 Market Positioning and Go-to-Market

1. Is the primary sales motion top-down (district/state level) or bottom-up (individual schools/departments)?
2. If we are targeting India first, what is the exact pricing expectation post-pilot? Will schools pay per classroom, per teacher, or per student?
3. How will we mitigate the risk of pilot churn if the hardware cost (glasses + host phone) must eventually be borne by the school?
4. Are we treating universities and K-12 schools as fundamentally different tenants with separate RBAC, or a unified hierarchy?
5. How does the product position itself against Chinese surveillance-style smart classrooms versus Western coaching platforms like Edthena?
6. Are we explicitly marketing this as a "surveillance" tool for administration, or a "coaching" tool for teachers?
7. In "supervision mode," what guarantees do teachers have against automated punitive action based on AI hallucinations?
8. Are teachers unionized in the target initial market, and if so, what are the specific collective bargaining constraints around classroom recording?
9. Is there an intent to eventually sell anonymized aggregate data to educational researchers or textbook publishers?
10. If the product is highly successful, does it become a mandatory continuous evaluation tool or remain an opt-in coaching tool?

### 1.2 User Experience and Engagement

11. What is the expected time-to-insight from the end of a lesson to the admin/teacher receiving the Pedagogy Index?
12. How does the teacher initiate a recording session seamlessly on the Ray-Ban glasses without disrupting the start of class?
13. If the teacher's phone (host) goes to sleep or loses Wi-Fi, what feedback is provided to the teacher during the lesson?
14. How are teachers expected to consume the generated feedback? Through a mobile app, an email report, or a web dashboard?
15. If a teacher disagrees with the AI's assessment of their pedagogy, what is the dispute resolution UX?
16. How do we visualize "student engagement" without violating the constraint against individual student profiling?
17. Does the UI need to display real-time metrics to coaches/admins while the class is happening, or is post-class processing sufficient?
18. How will the dashboard accommodate teachers who teach multiple subjects with vastly different pedagogical requirements (e.g., math vs. physical education)?
19. Will the system offer gamification elements for teachers improving their pedagogy score, or is it strictly analytical?
20. What is the minimum acceptable accuracy of the transcription (ASR) before teachers lose trust in the system?

### 1.3 Legal, Compliance & Ethics

21. What is the exact legal definition of "consent" required under the India Digital Personal Data Protection (DPDP) Act for classroom video recording?
22. Are we obtaining consent directly from parents, or relying on institutional consent policies?
23. If a student explicitly opts out, does the system dynamically obscure them in the video feed, or is the teacher prohibited from recording?
24. How do we handle incidental capture of sensitive PII (e.g., medical information written on a board or spoken aloud)?
25. Is FERPA/GDPR compliance an architectural requirement now to prevent re-architecting for US/EU expansion later?
26. How long is the raw video and audio data retained before being permanently deleted?
27. Who holds the encryption keys to the raw video data—PedagogyX, or the school administration?
28. Is there a "break-glass" procedure for law enforcement requests regarding classroom footage?
29. If the AI detects a dangerous or illegal situation (e.g., violence in the classroom), is it programmed to generate an immediate alert?
30. How do we prevent bias in the pedagogical assessment algorithms against non-native speakers or regional accents?

---

## 2. Technical Architecture & Infrastructure Questions

### 2.1 Edge & Client Constraints (Meta Ray-Ban & Android)

31. Given the Meta Ray-Ban glasses battery life, can they reliably sustain a 45-60 minute continuous video stream?
32. What happens if the glasses overheat during a session? What is the failover or recovery state?
33. How resilient is the WebRTC/chunking protocol to intermittent classroom Wi-Fi dropouts?
34. Does the Android host app need to operate completely in the background, and how do we prevent the OS from killing the process?
35. How is audio synchronized with video if the streams drift during a long capture session?
36. Are we doing any local processing (e.g., wake word detection, VAD) on the Android device before sending to the cloud?
37. What is the minimum upload bandwidth required per classroom to stream the DAT video feed in real-time?
38. Can the system gracefully degrade to audio-only if video bandwidth is insufficient?
39. How do we handle time-zone synchronization across devices if the phone clock is out of sync with the server?
40. What is the exact Bluetooth latency between the glasses and the Android host, and does it impact real-time coaching feedback?

### 2.2 Cloud Architecture & Scalability

41. Can the architecture handle a "thundering herd" problem when all classes in a school end at exactly 10:00 AM and upload their data?
42. Are we utilizing a serverless architecture for the ingestion API, or dedicated containers with connection pooling?
43. How are video chunks reassembled on the server without consuming massive amounts of ephemeral disk space?
44. If we deploy in the `ap-south-1` region, what is the cross-AZ replication strategy for disaster recovery?
45. How does the Postgres database schema scale when we have millions of session records and fine-grained temporal events?
46. Are we using a message broker (Kafka/RabbitMQ) or a Redis-based queue (Celery/RQ) for asynchronous processing?
47. What is the exact auto-scaling trigger for the GPU workers? Queue depth, CPU utilization, or predicted schedule?
48. How do we isolate tenant data physically or logically to prevent accidental cross-school data leaks?
49. If a cloud region goes down, what is the recovery time objective (RTO) and recovery point objective (RPO)?
50. How are we managing secrets and environment variables securely across the fleet?

### 2.3 Machine Learning & AI Pipelines

51. Which specific ASR model (e.g., Whisper, Conformer) is being used, and how does it handle English-Hindi code-switching?
52. How are we performing diarization to distinguish the teacher's voice from students when using a single microphone on the glasses?
53. What is the latency budget for the CV pipeline to extract skeletal/pose data from the POV video stream?
54. Are we utilizing a frozen foundational LLM, or are we fine-tuning it on proprietary pedagogical datasets?
55. How do we prevent the LLM from hallucinating feedback based on incorrectly transcribed audio?
56. Can the pipeline handle multimodal fusion (aligning text, audio sentiment, and video gestures) at a 1-second temporal resolution?
57. What is the fallback strategy if the primary GPU cluster hits quota limits during peak hours?
58. How do we measure and mitigate concept drift in the pedagogical scoring model over time?
59. Are we using vector databases (e.g., Milvus, Qdrant) to store lesson embeddings for longitudinal analysis?
60. What is the annotation workflow to generate ground-truth data for the initial models before pilot deployment?

### 2.4 Security & Observability

61. What is the exact authentication mechanism for the Android app? Long-lived API keys, or OAuth with short-lived JWTs?
62. How do we prevent a malicious actor from spoofing the Android app and uploading forged classroom video?
63. Are all data stores (Postgres, MinIO) encrypted at rest using KMS-managed keys?
64. What observability stack (e.g., Prometheus, Grafana, Datadog) is being used to track end-to-end latency per session?
65. How are we tracing a single video chunk from ingestion through the ML pipeline to the final UI dashboard?
66. Is there a mechanism to automatically redact PII from application logs before they are indexed?
67. How do we monitor the "health" of the AI models in production (e.g., tracking confidence scores over time)?
68. What alerting rules are configured for sudden spikes in API error rates or GPU starvation?
69. Are we running regular penetration tests on the ingestion API?
70. How do we handle database migrations with zero downtime while long-running ML jobs are executing?

## 3. Advanced Pedagogical Research Questions

71. What specific pedagogical framework (e.g., Danielson Framework, Marzano) is the AI benchmarking against?
72. How does the AI differentiate between "wait time" (good pedagogy) and "dead air" (lost instructional time)?
73. Can the system detect high-order cognitive questions versus basic recall questions based on the transcript?
74. How is student engagement quantified purely from a teacher's POV camera without full facial recognition?
75. Does the system analyze the teacher's movement around the classroom (proximity to students) as a metric?
76. How does the AI evaluate the clarity and pacing of instructional delivery?
77. Can the system recognize when a teacher successfully checks for understanding and adjusts instruction dynamically?
78. How does the system handle collaborative learning environments where the teacher is acting as a facilitator rather than a lecturer?
79. What metrics are used to calculate the "Pedagogy Index" composite score?
80. How will we validate that an improved AI Pedagogy Index actually correlates with improved student learning outcomes?

## 4. Hardware & Edge Integration Specifics

81. Does the DAT SDK provide raw camera frames, or compressed video streams, and what codec is used?
82. Can we control the frame rate and resolution of the glasses dynamically based on network conditions?
83. What is the specific error-handling flow when Bluetooth disconnects mid-session?
84. Does the system support external Bluetooth microphones if the glasses microphone is insufficient in a noisy room?
85. How do we handle OS battery optimization killing the PedagogyX background service on the Android host?
86. Is there a mechanism to cache video chunks on the Android device's local storage if upload fails, and how much storage can we safely use?
87. What is the thermal throttling behavior of the phone when performing continuous encryption and upload for an hour?
88. Can we trigger haptic feedback on the glasses to alert the teacher of a critical issue (e.g., session disconnected)?
89. How are firmware updates for the glasses managed or monitored by our system to prevent breaking SDK changes?
90. What telemetry are we collecting from the DAT SDK regarding device health (battery, temperature) during the session?

## 5. Long-term Vision & Roadmap

91. If Phase 1b introduces smartboards, how will we temporally align the glasses POV video with the smartboard screen recording?
92. Are there plans to introduce autonomous AI coaching agents that interact with the teacher via ear-piece during the lesson?
93. How will the platform scale to support multi-language real-time translation for diverse classrooms?
94. Will we eventually build a knowledge graph of all concepts taught across a school district?
95. Can the system be adapted for corporate training or higher education lecture halls with minimal re-architecture?
96. What is the strategy for moving inference to the edge (on the phone) as mobile NPUs become more powerful?
97. How will we build a synthetic dataset for rare classroom edge cases (e.g., emergencies, major disruptions)?
98. What is the timeline for open-sourcing any of the foundational educational AI models we develop?
99. How do we ensure the platform remains a tool for teacher empowerment rather than a dystopian surveillance apparatus?
100.  What is the ultimate exit strategy or long-term structural goal of PedagogyX in the global education ecosystem?
