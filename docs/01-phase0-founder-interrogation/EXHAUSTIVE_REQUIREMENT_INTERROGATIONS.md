# Exhaustive Requirement Interrogations

**Status:** Phase 0 Investigation
**Date:** 2026-05-30
**Owner:** Architecture Team

As the Autonomous Principal Research Architect, I have compiled this exhaustive list of interrogations to strictly define boundaries, uncover contradictions, and force concrete product decisions from the founder before any production code is written for PedagogyX.

## 1. Product & Market Boundaries

1. **Market Focus:** Is the ultimate target market US K-12, US Higher Ed, Indian K-12, or corporate training? The MVP is in India, but what is the 3-year plan?
2. **End User vs. Buyer:** The teacher uses the system, but the administrator buys it. If the AI detects poor teaching, does the administrator get alerted? If yes, how do we handle teacher union backlash?
3. **Opt-Out Policies:** Can a teacher refuse to be recorded on a given day without penalty? Can a student opt-out?
4. **Surveillance vs. Coaching:** Is this system marketed as an "evaluator" (punitive/scoring) or a "copilot" (growth/coaching)? The architecture changes drastically based on this answer.
5. **Hardware Constraints:** We are pivoting to Meta Ray-Bans as the primary client. What happens if a teacher refuses to wear glasses? Is there a stationary room camera fallback?
6. **Cost per Seat:** What is the target monthly cost per teacher? If inference costs exceed this, how do we degrade service gracefully?

## 2. Compliance, Privacy & Legal Constraints

1. **India DPDP Compliance:** Does the system require full localization of data in India?
2. **FERPA/GDPR Future-Proofing:** Do we need to build automated PII redaction (blurring faces, muting names) into the Phase 1 edge pipeline, or can we rely on legal waivers for the MVP?
3. **Biometric Analysis:** Are we legally permitted to analyze student facial expressions for "engagement," or is this a massive liability?
4. **Data Retention:** How long are raw video/audio assets kept? 30 days? 1 year? Forever?
5. **Right to be Forgotten:** If a teacher leaves the district, do we purge their models and data?

## 3. Deep Technical & Architectural Interrogations

### 3.1 Edge vs. Cloud

1. **Network Reliability:** Indian pilot schools will have terrible internet. If the glasses record 4 hours of video, it cannot stream live. Are we confirming the architecture is asynchronous batch upload only?
2. **Local Storage:** The Android DAT host will run out of storage quickly. What is the eviction policy for uploaded chunks?
3. **Edge Processing:** Should we run VAD (Voice Activity Detection) on the Android phone to avoid uploading 30 minutes of silent reading time?

### 3.2 AI Pipeline & Inference

1. **Speaker Diarization:** In a noisy classroom of 40 students, how do we distinguish the teacher's voice from a loud student?
2. **Multimodal Fusion:** Are we correlating audio transcripts with visual slide changes in real-time or post-processing?
3. **Hallucinations:** If the AI generates a coaching insight based on hallucinated ASR output (e.g., misinterpreting a Hindi accent), how do we provide a human-in-the-loop correction mechanism?

### 3.3 Scalability & Infrastructure

1. **GPU Allocation:** We are using consumer-grade RTX 5070s for cost savings. Have we modeled the VRAM limits for running faster-whisper + a vision transformer simultaneously?
2. **Queueing Strategy:** If 500 teachers finish class at 3:00 PM and upload simultaneously, the system will buckle. What is the queuing and rate-limiting strategy?
3. **Disaster Recovery:** If the ap-south-1 region goes down, do we fail over, or do we accept downtime for cost savings?
