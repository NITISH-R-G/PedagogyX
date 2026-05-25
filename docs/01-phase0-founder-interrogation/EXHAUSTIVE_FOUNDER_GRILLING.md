# Exhaustive Founder Interrogation Questionnaire

**Status:** Phase 0 Active
**Date:** 2026-05-25
**Owner:** Principal Research Architect

This document serves as the foundational interrogation of the PedagogyX vision. Before any code is written, we must challenge every assumption and clarify every technical constraint.

## I. Product & Market Strategy

1. **Market Positioning:** You’ve indicated a desire to rival Edthena and Chinese Smart Classroom systems. Are we primarily a B2B Enterprise SaaS for large districts, a B2B solution for individual schools, or a B2C tool for individual teacher self-improvement?
2. **Economic Buyer vs. User:** Who writes the check? Is it the superintendent using discretionary funds, the principal, or the state government? If the system is designed to assess teachers, how do we mitigate the risk of teacher unions blocking adoption?
3. **Primary Use Case:** Is the primary intent **instructional coaching** (private feedback to help teachers improve) or **administrative supervision** (dashboards for principals to evaluate/score teachers)? These two use cases require fundamentally different architectures regarding data privacy, RBAC, and AI output tone.
4. **Target Markets & Compliance:** Which specific countries are we launching in first? If the US, FERPA is mandatory. If the EU, GDPR strictly regulates biometric processing. If India, DPDP mandates data localization. Which legal framework is our Day-1 constraint?
5. **Surveillance Tolerance:** "Chinese Smart Classroom systems" often include facial recognition and emotion tracking of minors. Is this level of surveillance acceptable in our target market? If not, what is the boundary? Is biometric analysis of students permitted?
6. **Hardware Constraints:** What is the assumed classroom hardware budget? Are we requiring schools to purchase expensive multi-camera arrays, or must we run on existing low-end Android/Windows devices? Is this a cloud-native solution, or does it require Edge AI processing on-premise?
7. **Connectivity Constraints:** Are we assuming high-bandwidth, stable internet in every classroom, or must the system support a "low-bandwidth mode" or entirely offline processing?
8. **Explainability & Accountability:** If the AI generates a low "Pedagogy Score," is human review by a master teacher mandatory before that score is finalized? How do we explain the AI's reasoning if a teacher disputes an evaluation?
9. **Multilingual Support:** Is the platform expected to handle multilingual classrooms or code-switching (e.g., mixing English and Spanish) in real-time?

## II. Deep Technical Interrogation

10. **Real-time vs. Post-Processing:** Does the system need to provide real-time coaching nudges to the teacher (e.g., via an earpiece or screen), or is it strictly post-class analytics? Real-time requires WebRTC and edge GPU processing; post-class allows for batch processing and central cloud architecture.
11. **Scalability & Inference Cost:** If 1,000 classrooms upload 50 minutes of video simultaneously at 3:00 PM, what is our target latency (Time-to-Insight)? Can we afford the GPU compute required to process this concurrently, or must we queue it for overnight processing?
12. **Multimodal Synchronization:** How do we intend to synchronize the audio from the teacher's microphone, the video from the classroom camera, and the screen capture from the digital whiteboard? What is the acceptable drift tolerance before multimodal fusion fails?
13. **Audio Quality in the Wild:** Classroom environments are highly reverberant with a low signal-to-noise ratio. Are we mandating a specific microphone array (e.g., lavalier for the teacher), or are we attempting to diarize 30 student voices from a single ceiling mic?
14. **Temporal Event Modeling:** Pedagogical events are long-context. A question asked at minute 5 might be answered at minute 45. How are we structuring our vector database and embedding strategy to capture this long-term temporal context?
15. **Storage Architecture:** High-definition video from thousands of classrooms will generate petabytes of data rapidly. What is the data retention policy? Are we utilizing tiered storage (hot NVMe to cold S3 Glacier)?
16. **MLOps & Continuous Learning:** How do we plan to handle data labeling and annotation for the initial supervised models? Are we generating synthetic data to bootstrap the CV/ASR pipelines, or do we have access to a proprietary dataset of classroom interactions?
17. **Privacy-Preserving ML:** If we cannot stream identifiable student video to the cloud, are we planning to implement federated learning, or must we run deterministic blurring algorithms at the edge before upload?
18. **Hallucination Mitigation:** When using LLM agents to generate teaching feedback, what specific deterministic guardrails (e.g., RAG against approved pedagogical rubrics, structural JSON enforcement) will we implement to prevent the AI from fabricating classroom events?
