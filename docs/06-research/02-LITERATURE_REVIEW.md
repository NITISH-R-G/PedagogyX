# Academic Literature Review: Multimodal Classroom AI

**Date:** 2026-05-24

## Focus Areas

1. Multimodal learning analytics
2. Speech emotion recognition in chaotic environments
3. Edge-optimized vision transformers
4. Pedagogical assessment frameworks

## Key Papers Synthesized

### 1. "Multimodal Engagement Analysis in K-12 Classrooms" (2024)

- **Core Finding:** Fusing audio (pitch, prosody) with visual cues (head pose, body language) improves student engagement detection accuracy by 22% over unimodal approaches.
- **Limitation:** High computational cost; models ran on A100 clusters.
- **Application to PedagogyX:** We must utilize early-fusion lightweight architectures (e.g., MobileViT) to run on the DAT edge device before transmission.

### 2. "Code-Switching ASR in Indian Educational Contexts" (2025)

- **Core Finding:** Whisper models struggle significantly with rapid Hindi-English code-switching without domain-specific fine-tuning.
- **Limitation:** Lack of large open-source datasets for K-12 Indian classrooms.
- **Application to PedagogyX:** We need a pipeline for synthetic data generation to fine-tune our ASR models for the India launch.

### 3. "Evaluating Pedagogical Effectiveness via Discourse Analysis" (2023)

- **Core Finding:** Analyzing the ratio of teacher 'open questions' vs 'closed questions' strongly correlates with student learning outcomes.
- **Limitation:** Requires highly accurate speaker diarization to separate teacher from student voices.
- **Application to PedagogyX:** Our pipeline must prioritize diarization accuracy. The teacher POV audio from the Meta Ray-Bans will serve as the ground truth anchor for the teacher's voice.
