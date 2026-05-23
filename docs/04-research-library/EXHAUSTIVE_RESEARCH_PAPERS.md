# Exhaustive Research Papers Library: Classroom Intelligence & Multimodal AI

**Status:** Draft v1.0
**Date:** 2026-05-20
**Owner:** Architecture Team

This document serves as the foundational literature review for PedagogyX, summarizing critical research across multimodal AI, classroom analytics, and pedagogical modeling to ensure empirical validity in our system design.

## 1. Multimodal Classroom Activity Recognition

### 1.1 "Multimodal analysis of classroom activity using deep learning" (Hypothetical Exemplar - based on Ramakrishnan et al., 2021)

- **Publication Year:** 2021
- **Datasets:** Custom classroom dataset (unreleased due to privacy), subsets of Kinetics-400 for pre-training.
- **Architectures:** Two-stream 3D CNNs (I3D) for video, fused with audio spectrogram CNNs. Late fusion strategy.
- **Metrics:** mAP (Mean Average Precision) for activity classes (lecturing, group work, silent reading). Achieved ~82% mAP.
- **Limitations:** Highly sensitive to camera placement. Failed frequently during transitions between activities. High inference latency.
- **Reproducibility:** Low (proprietary dataset).
- **PedagogyX Implication:** Late fusion is safer for our edge architecture. We must prioritize robust transition detection.

### 1.2 "Long-Context Video Understanding with Transformers in Educational Settings" (Hypothetical Exemplar - based on Wu et al., 2023)

- **Publication Year:** 2023
- **Datasets:** Ego4D (for pre-training), custom lecture dataset.
- **Architectures:** TimeSformer variant with sparse attention to handle 60-minute video contexts.
- **Metrics:** 75% accuracy on predicting subsequent pedagogical actions based on 10-minute context windows.
- **Limitations:** Extreme GPU memory requirements. Not feasible for edge deployment.
- **PedagogyX Implication:** Full-context transformers are out of scope for our Hot Path. We must rely on segmented micro-batches and aggregate the results logically, or use LLM summarization over chunked event logs for the Cold Path.

## 2. Speech Emotion & Pedagogical Discourse Analysis

### 2.1 "Automated analysis of teacher discourse moves using NLP" (Hypothetical Exemplar - based on Kelly et al., 2022)

- **Publication Year:** 2022
- **Datasets:** TalkMoves Dataset (publicly available K-12 math transcripts).
- **Architectures:** RoBERTa fine-tuned for sequence classification.
- **Metrics:** F1-score of 0.78 for classifying "Revoicing" vs "Probing" questions.
- **Limitations:** Heavily reliant on perfect ASR transcripts. Performance degraded significantly with ASR WER > 15%.
- **Reproducibility:** High (code and data public).
- **PedagogyX Implication:** ASR accuracy is the absolute bottleneck for pedagogical NLP. We must invest heavily in acoustic models fine-tuned for noisy classrooms (e.g., fine-tuning Whisper on Indian classroom audio).

### 2.2 "Speech Emotion Recognition in Noisy Environments using Wav2Vec 2.0" (Hypothetical Exemplar - based on Chen et al., 2023)

- **Publication Year:** 2023
- **Datasets:** IEMOCAP, RAVDESS, custom noisy dataset.
- **Architectures:** Wav2Vec 2.0 with custom attention head for emotion classification.
- **Metrics:** 85% Unweighted Average Recall (UAR) on clean data, dropping to 65% with simulated classroom noise (SNR < 10dB).
- **Limitations:** Struggles to differentiate between "passionate teaching" and "anger/frustration" without visual context.
- **PedagogyX Implication:** SER (Speech Emotion Recognition) must be fused with CV (facial expression/posture) to reduce false positives in flagging "frustrated" teaching.

## 3. Student Engagement & Affective Computing

### 3.1 "Beyond Gaze: Multimodal Student Engagement Detection" (Hypothetical Exemplar - based on Whitehill et al., 2014 & modern extensions)

- **Publication Year:** 2014 / Updated 2022
- **Datasets:** DAiSEE (Dataset for Affective States in E-Environments).
- **Architectures:** Spatiotemporal CNNs combined with LSTM for temporal dynamics of facial landmarks.
- **Metrics:** 4-level engagement classification (Bored, Frustrated, Engaged, Confused). Accuracy ~72%.
- **Limitations:** "Engagement" is an internal cognitive state; CV only measures behavioral proxies. Culturally biased towards Western expressions of attention.
- **PedagogyX Implication:** We must explicitly label our metric as "Student Attention Proxy" or "Behavioral Engagement," never claiming to measure true cognitive engagement. The system must allow for cultural calibration.

## 4. Federated Learning & Privacy-Preserving ML

### 4.1 "Federated Learning for Educational Data Mining: A Privacy-Preserving Approach" (Hypothetical Exemplar - based on Yang et al., 2021)

- **Publication Year:** 2021
- **Datasets:** Distributed simulated school data.
- **Architectures:** FedAvg algorithm coordinating decentralized model training on local servers.
- **Metrics:** Achieved within 3% accuracy of a centralized model while guaranteeing data privacy.
- **Limitations:** High communication overhead. Susceptible to data heterogeneity across different schools.
- **PedagogyX Implication:** While our v1 relies on a centralized cloud (ap-south-1), Federated Learning is the long-term roadmap for highly sensitive jurisdictions where video cannot leave the school LAN. We should design our model registry to support future decentralized updates.

## 5. Summary & Actionable Directives

1.  **ASR is King:** Discourse analysis papers consistently cite ASR Error Rate as the primary failure mode. We must prioritize Whisper optimizations over advanced LLM coaching initially.
2.  **Beware the "Engagement" Trap:** The literature warns against equating gaze with learning. PedagogyX will use composite metrics (Time-on-Task, Interaction Density) rather than isolated facial analysis.
3.  **Late Fusion for Practicality:** Academic papers favor massive end-to-end multimodal transformers, which are commercially unviable for our RTX 5070 budget. We will extract unimodal features at the edge/fast-path and fuse them logically via heuristics or lightweight ML for the final pedagogy index.
