# Phase 0: Exhaustive Requirement Interrogation

**Document Objective**: To rigorously interrogate the fundamental assumptions, product requirements, and technical constraints of PedagogyX before any production implementation.

## 1. System Context & Epistemology

### 1.1 Facts

- **Primary V1 Client**: Meta Ray-Ban smart glasses (DAT) acting as the primary multimodal capture device.
- **Data Locality Strategy**: Hybrid edge-cloud architecture with local buffer/capture and cloud-based AI processing.
- **Pilot Constraints**: No production school data access until G2 (India legal sign-off).
- **Core Value Proposition**: Analyzing classroom sessions for pedagogical efficiency, student engagement, and teacher improvement.

### 1.2 Assumptions

- **Hardware Viability**: Meta Ray-Ban microphones and cameras have sufficient fidelity to accurately capture teacher voice and slide content from the back of the classroom.
- **Network Reliability**: Classrooms will have sufficient uplink bandwidth to upload session data or local edge nodes can reliably buffer it for delayed upload.
- **Teacher Compliance**: Teachers will consent to wearing recording devices or having their classrooms monitored.
- **Legal Compliance**: The platform can navigate FERPA, GDPR, and India DPDP compliance simultaneously.

### 1.3 Hypotheses

- **Pedagogical Impact**: AI-driven multimodal feedback loop will significantly improve teacher instructional quality within 3 months of usage.
- **Cost Effectiveness**: A central OSS-first backend in an India-based cloud will maintain competitive inference costs per classroom session compared to fully proprietary LLM APIs.
- **Multimodal Superiority**: Combining audio + video + slides provides a 3x higher correlation to teaching effectiveness than audio analysis alone.

### 1.4 Speculative Ideas

- **Real-Time Coaching**: Earpiece-based real-time AI whisper coaching during the lesson.
- **Student Affective Analysis**: Tracking micro-expressions of individual students to map engagement heatmaps in real-time.
- **Synthetic Classrooms**: Generating fully synthetic multimodal classroom sessions for model pre-training.

---

## 2. Product Interrogation

### 2.1 Core Identity & Market

1. Is this system fundamentally a surveillance tool or an empowerment tool?
2. Are we selling B2B to schools, B2C directly to teachers, or B2G to ministries of education?
3. What is the business model? Per teacher per month? Per school?
4. If teachers object to the system, who wins the argument: the teacher union or the administration?
5. Do administrators have access to teacher performance metrics?
6. Is the system intended for real-time live coaching or post-class reflective analysis?
7. How do we handle hybrid environments where some students are remote?
8. What is the exact success metric for the founder? ARR? Active daily usage? Measured improvement in student test scores?
9. Is China-style behavioral surveillance acceptable for our brand?
10. If a teacher receives a low AI score, what is the mitigation strategy for burnout?

### 2.2 Legal & Privacy

11. Is student facial analysis explicitly allowed in our target jurisdictions (India first, US later)?
12. How do we obtain consent from minors in a classroom setting?
13. Is biometric analysis of teachers allowed?
14. What are the specific DPDP (India) constraints for educational data?
15. If a parent requests data deletion, how do we scrub their child's face/voice from a 45-minute multimodal session?
16. Can the data be subpoenaed?
17. Is FERPA compliance an immediate blocker for US expansion?

### 2.3 User Experience

18. How does a teacher initiate a session? Is it frictionless?
19. Does the teacher need to manually pair the Meta Ray-Bans to the edge node?
20. How is low-bandwidth handled from a UX perspective?
21. What happens if the glasses battery dies mid-lecture?
22. Is the feedback presented as a dashboard, an email, or a chatbot?
23. Should the AI detect emotional tone and adjust its feedback delivery style?
24. Is explainable AI mandatory? If the AI says "Pacing was too fast", does it need to show a timestamped video clip?

---

## 3. Technical Interrogation

### 3.1 Multimodal Pipeline & Edge

25. What is the exact latency budget for processing a 1-hour lecture?
26. If the Meta Ray-Bans disconnect, is the data lost?
27. What is the fallback if the edge LAN buffer goes down?
28. How are audio and video streams synchronized if they drift?
29. What is the resolution required for whiteboard OCR from a teacher's perspective?
30. Are we running any inference on the edge device itself (e.g., wake word, VAD)?

### 3.2 AI & ML

31. Are we fine-tuning OSS models (Llama 3, Whisper) or relying on commercial APIs?
32. What is the hallucination rate threshold for pedagogical feedback?
33. How are we handling speaker diarization with 30+ students in a noisy room?
34. Can we accurately classify student engagement vs. confusion from low-res background faces?
35. How do we create embeddings that fuse temporal audio, video frames, and slide semantic text?
36. Are we using Long-Context LLMs (e.g., Gemini 1.5 Pro) or a RAG-based chunking strategy for 1-hour sessions?
37. How do we generate ground truth labels for "good teaching"?
38. Are we employing Reinforcement Learning from Human Feedback (RLHF) with expert educators?

### 3.3 Scalability & Infrastructure

39. What is the peak concurrent ingestion rate if 1,000 schools finish 1st period at 9:00 AM?
40. How are we scheduling GPU workloads? Are we using Kubernetes/Ray or simple Celery queues?
41. What is the storage cost of retaining 4K/1080p video for longitudinal analysis over a 5-year teaching career?
42. Do we need multi-region replication for the India DPDP pilot?
43. How do we handle database migrations on massive vector databases containing millions of multimodal embeddings?

---

## 4. Risks & Unknowns

### 4.1 Identified Risks

- **Hardware Lock-in**: Relying primarily on Meta Ray-Ban glasses creates platform risk.
- **Privacy Backlash**: High probability of union/teacher pushback if the system is perceived as punitive.
- **Cost Runaway**: Processing 1-hour multimodal videos at scale can rapidly exhaust GPU budgets.
- **Data Quality**: Classroom acoustics are notoriously poor, severely degrading ASR and diarization quality.

### 4.2 Critical Unknowns

- Exact legal requirements for India's DPDP regarding biometric student data.
- The actual battery life of Meta Ray-Bans when continuously streaming over local network.
- The true pedagogical validity of AI-generated feedback vs. human expert coaching.
