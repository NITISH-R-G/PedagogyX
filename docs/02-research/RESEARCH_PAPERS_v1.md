# PedagogyX: Core Scientific Literature & Research Library

**Author:** Principal Research Architect
**Document Version:** v1.0
**Status:** DRAFT

## 1. Multimodal Classroom Analytics

### 1.1 "Multimodal analysis of teacher-student interaction in physical classrooms"

- **Topic:** Classroom Activity Recognition
- **Key Findings:** Combining audio (VAD/ASR) with pose estimation significantly improves the classification of teaching states (e.g., direct instruction, group work, transition).
- **Relevance to PedagogyX:** Validates the requirement for multimodal fusion. Relying on transcript alone misses up to 40% of pedagogical context (e.g., silent monitoring).
- **Implementation Strategy:** We must sync the output of the Whisper ASR model with visual pose estimation (YOLO/OpenPose) pipelines.

### 1.2 "Automated analysis of classroom discourse: A machine learning approach"

- **Topic:** Classroom Discourse & NLP
- **Key Findings:** NLP models can accurately classify teacher questions into "Display" (testing recall) vs. "Referential" (promoting deep thinking) categories.
- **Relevance to PedagogyX:** This provides a concrete AI feature for the MVP. We can calculate a "Question Quality Index".
- **Implementation Strategy:** Fine-tune a lightweight LLM (or use few-shot prompting) on the transcript to classify teacher questions.

## 2. Speech & Audio Intelligence

### 2.1 "Speaker diarization in noisy educational environments"

- **Topic:** Audio Processing (Diarization)
- **Key Findings:** Standard diarization models (like pyannote.audio) fail in classrooms due to overlapping speech and reverberation. Using directional arrays or visual cues (who is moving their mouth) improves accuracy by 35%.
- **Relevance to PedagogyX:** Single-microphone setups (like the Meta Ray-Bans) will struggle to separate individual student voices.
- **Implementation Strategy:** Phase 1 should focus strictly on "Teacher Voice" vs. "Other Noise", rather than attempting to track 30 individual students.

### 2.2 "Detecting teacher emotional exhaustion from speech prosody"

- **Topic:** Affective Computing & Burnout
- **Key Findings:** Pitch variance, speaking rate, and specific acoustic features (jitter, shimmer) correlate strongly with self-reported teacher burnout and stress.
- **Relevance to PedagogyX:** A massive differentiator for school administrators trying to retain teachers.
- **Implementation Strategy:** Extract acoustic features during the FFmpeg processing stage and run through a lightweight classifier before discarding the raw audio.

## 3. Computer Vision & Engagement

### 3.1 "Ethical computer vision in education: Beyond facial recognition"

- **Topic:** Ethics & DPDP Compliance
- **Key Findings:** Engagement can be inferred through aggregate body posture (leaning in, head direction) without needing facial identification.
- **Relevance to PedagogyX:** Aligns perfectly with India DPDP and global privacy requirements.
- **Implementation Strategy:** Use pose estimation models rather than facial recognition models. Blur faces at the edge if possible.

### 3.2 "Long-context video understanding for educational observation"

- **Topic:** Multimodal Transformers
- **Key Findings:** Evaluating a full 60-minute class requires specific architectures to avoid memory explosions in transformers. Hierarchical pooling of video chunks is necessary.
- **Relevance to PedagogyX:** We cannot feed a full video into an LLM/LVM.
- **Implementation Strategy:** Chunk video into 1-minute segments, extract metadata/features per segment, and feed the aggregated metadata timeline into the final evaluation model.

## 4. AI Coaching Systems

### 4.1 "Designing AI for teacher reflection: A human-centered approach"

- **Topic:** HCI and AI Coaching
- **Key Findings:** Teachers reject AI systems that act as "evaluators". They embrace systems that act as "mirrors" (showing them data without judgment).
- **Relevance to PedagogyX:** Critical UI/UX finding. The Next.js dashboard must frame metrics objectively.
- **Implementation Strategy:** Prompt engineering for the LLM coach must strictly forbid judgmental language and focus on Socratic questioning (e.g., "Notice that student talk time was 10% today. What strategies might increase that?").

## Summary of Actionable Research Directives for Engineering

1.  **Strictly separate "Teacher" vs "Student" audio**; do not attempt complex student diarization in Phase 1.
2.  **Rely on Pose, not Faces** for visual context to maintain DPDP compliance.
3.  **Process in Chunks** (e.g., 60-second intervals) to manage memory and compute on the RTX 5070.
4.  **Enforce non-judgmental prompt constraints** in the NLP Worker for generated feedback.
