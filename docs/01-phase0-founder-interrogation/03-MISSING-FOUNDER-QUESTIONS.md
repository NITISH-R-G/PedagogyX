# Unresolved Foundational Interrogation Questions

**Date:** 2026-05-24

While preliminary architectural decisions have been made based on assumed constraints (India DPDP, RTX 5070, Meta Ray-Ban), the founder MUST explicitly answer the following questions before any production code is written:

## Product & Market Intent

1.  **Monetization Strategy:** If the initial pilot is free (₹0 budget), what is the explicit monetization trigger? Will districts eventually pay per classroom, or is the plan to monetize the aggregated analytics dataset?
2.  **Teacher Pushback:** How will we handle scenarios where a teacher's union flatly refuses to allow audio recording devices in the classroom? What is our fallback non-recording product offering?
3.  **Score Immutability:** Can a principal manually override an AI-generated pedagogical score if they believe the AI misjudged the lesson context?

## Legal & Compliance (Beyond DPDP)

4.  **FERPA/GDPR Parity:** Even if we launch in India first, how much technical debt are we willing to accept by not building FERPA (US) and GDPR (EU) compliance directly into the v1 data models?
5.  **Data Deletion SLA:** If a teacher requests their data be deleted, what is the SLA for scrubbing their voice embeddings from the vector database and all historical analytics?
6.  **Biometric Consent:** Does capturing a teacher's Voiceprint (necessary for speaker diarization) require explicit biometric consent under local laws, and how is that stored cryptographically?

## Deep Technical Architecture

7.  **Edge Fallback:** If the DAT host (Android device) is destroyed or stolen mid-class, what happens to the buffered data? Is it encrypted at rest using a hardware-backed keystore?
8.  **Model Hallucination:** How do we detect and prevent the LLM from hallucinating pedagogical feedback? Do we require human-in-the-loop review for the first 10,000 generated insights?
9.  **Battery Drain:** What is the maximum acceptable battery drain on the teacher's mobile device running the DAT companion app for a 6-hour school day?
10. **Acoustic Environment:** Indian classrooms are notoriously loud with high reverberation and ceiling fans. What happens if the VAD (Voice Activity Detection) fails to filter background noise and floods the backend with useless audio chunks?
