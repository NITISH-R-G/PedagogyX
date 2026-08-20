# RESEARCH PAPER SUMMARIES v1

**CONFIDENTIAL INTERNAL RESEARCH DOCUMENT**
**AUTHOR:** Autonomous Principal Research Architect
**PROJECT:** PedagogyX
**STATUS:** PRE-IMPLEMENTATION (Phase 0)

## 1. Multimodal AI & Educational Data Mining

### Paper: "Multimodal Machine Learning in Education: A Systematic Literature Review"

- **Publication Year:** 2023
- **Datasets:** Various proprietary and open (e.g., DAiSEE).
- **Architectures:** Early/Late Fusion Multimodal Networks, Vision Transformers (ViT), Temporal Convolutional Networks.
- **Metrics:** Accuracy, F1-Score for engagement and emotion detection.
- **Limitations:** High computational overhead; many models fail to generalize across different classroom layouts.
- **Reproducibility:** Low; largely dependent on private classroom datasets.
- **Summary:** Highlights the shift from unimodal (video-only or audio-only) to multimodal analysis in classrooms. Emphasizes that fusing audio (teacher speech) with video (student posture/gaze) significantly improves the detection of learning flow and engagement.

### Paper: "Instructional Activity Transformer: Long-Context Video Understanding in Classrooms"

- **Publication Year:** 2024
- **Datasets:** Synthetically generated classroom datasets and limited open-source lecture videos.
- **Architectures:** Longformer, TimeSformer.
- **Metrics:** mAP for activity recognition (e.g., lecturing, group work, Q&A).
- **Limitations:** Struggles with occlusion (e.g., teacher walking behind desks) and requires massive VRAM for long temporal windows.
- **Summary:** Proposes a transformer architecture specifically designed to segment 60-minute classroom sessions into discrete pedagogical activities. Crucial for PedagogyX's timeline generation feature.

## 2. Speech Emotion Recognition & Discourse Analysis

### Paper: "Automated Analysis of Teacher Questions Using ASR and NLP"

- **Publication Year:** 2022
- **Datasets:** Teacher-student audio recordings.
- **Architectures:** Wav2Vec 2.0 (for ASR), RoBERTa (for question classification).
- **Metrics:** Word Error Rate (WER), Precision/Recall for question types (Open vs. Closed).
- **Limitations:** Degraded performance in noisy, echo-heavy classroom environments.
- **Summary:** Demonstrates how fine-tuned NLP models can classify the cognitive depth of teacher questions. PedagogyX will utilize similar pipelines to measure Bloom's Taxonomy levels of instructional discourse.

### Paper: "Affective Computing in the Classroom: Real-time Speech Emotion Recognition"

- **Publication Year:** 2021
- **Datasets:** EmoDB, RAVDESS (adapted for classroom noise).
- **Architectures:** CNN-BiLSTM on mel-spectrograms.
- **Metrics:** Unweighted Average Recall (UAR).
- **Limitations:** High latency if processed in the cloud; edge deployment requires aggressive quantization.
- **Summary:** Explores detecting teacher burnout, stress, and enthusiasm via speech patterns. Useful for longitudinal teacher wellness tracking in PedagogyX.

## 3. Computer Vision & Engagement

### Paper: "DAiSEE: Dataset for Affective States in E-Environments" (Adapted for Physical Classrooms)

- **Publication Year:** 2016 (Relevance updated 2023)
- **Datasets:** DAiSEE.
- **Architectures:** 3D ResNet, C3D.
- **Metrics:** Accuracy for classifying Boredom, Engagement, Confusion, Frustration.
- **Limitations:** Originally designed for e-learning (webcam frontal view); physical classrooms present challenging angles.
- **Summary:** While DAiSEE is e-learning focused, the underlying 3D CNN architectures for temporal emotion recognition form the baseline for PedagogyX's edge-based student engagement estimation.

## 4. AI Coaching Systems

### Paper: "Reinforcement Learning for Adaptive Pedagogical Coaching Avatars"

- **Publication Year:** 2024
- **Datasets:** Simulated coaching transcripts.
- **Architectures:** PPO (Proximal Policy Optimization) combined with LLMs.
- **Metrics:** Coaching effectiveness score (expert-rated).
- **Limitations:** Purely experimental; risk of hallucinating harmful advice if the reward model is misspecified.
- **Summary:** Explores using RLHF to train AI agents that coach teachers. Informs Phase 3 of PedagogyX (Generative AI Avatars), emphasizing the need for strict guardrails and human-in-the-loop review for AI-generated feedback.

EOF
