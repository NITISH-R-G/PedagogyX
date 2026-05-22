# Deep Research Literature Review & Multimodal Analytics

**Version:** 1.0
**Author:** Principal Research Architect
**Domain:** Multimodal Classroom Analytics, Affective Computing, Pedagogical Efficacy

## 1. Overview & Objective

This document synthesizes current academic and industry research relevant to PedagogyX. To build a world-class educational AI platform without relying on proprietary cloud APIs, we must leverage cutting-edge OSS models to replicate or exceed the capabilities detailed in modern multimodal learning analytics (MMLA) literature.

## 2. Core Themes & Research Vectors

### A. Multimodal Learning Analytics (MMLA)

MMLA involves the high-frequency capture of student and teacher interactions using audio, video, and digital traces.

- **Key Paper:** _Blikstein, P. (2013). Multimodal Learning Analytics._
  - **Summary:** Established the foundation for using physical sensors and computer vision to measure learning rather than relying solely on post-tests.
  - **Relevance:** PedagogyX's hybrid capture (Android + Windows) directly implements an MMLA framework.

### B. Speech Emotion Recognition (SER) & Classroom Discourse Analysis

Analyzing _how_ things are said, rather than just _what_ is said.

- **Key Paper:** _D'Mello, S., et al. (2015). Affective Computing in Education._
  - **Summary:** Discusses the correlation between teacher speech tone, student engagement, and learning outcomes.
  - **Relevance:** We will use `faster-whisper` for ASR, but need a secondary pipeline (e.g., Pyannote + Hubert) to extract paralinguistic features to estimate "teaching energy" or "tone."

### C. Action Recognition & Engagement Modeling via Computer Vision

- **Key Paper:** _Ahuja, K., et al. (2019). EduSense: Practical Classroom Sensing at Scale._
  - **Summary:** EduSense used open-source computer vision (OpenPose, YOLO) to track student posture, hand raises, and teacher movement across a classroom.
  - **Relevance:** Highly relevant. PedagogyX will utilize YOLO optimized via TensorRT to achieve similar spatial analytics (teacher movement heatmaps, gross student physical engagement) within our ₹0 client budget constraint.

### D. Automated Pedagogical Analysis & LLM Coaches

- **Key Paper:** _Wang, Z., et al. (2023). Towards Autonomous Classroom Feedback via Large Language Models._
  - **Summary:** Demonstrated that properly prompted LLMs, provided with detailed multimodal transcripts, can generate teacher coaching feedback comparable to human instructional coaches.
  - **Relevance:** Validates our use of Ollama (Qwen2.5) to synthesize ASR and CV data into a "pedagogical index" and generate actionable dashboard feedback.

## 3. Translation to PedagogyX Architecture

The research dictates the following architectural requirements:

1. **Temporal Alignment:** Multimodal models fail without strict temporal alignment. The edge buffer must enforce a unified clock across video and audio streams before they hit the cold-path ML pipeline.
2. **Context Window Limitations:** Analyzing a 50-minute class generates massive text. We must chunk the transcript or use models with 32k+ context windows to allow the LLM to identify narrative pedagogical arcs.
3. **Bias & Fairness:** Research consistently highlights CV bias against darker skin tones and ASR bias against regional accents. Since our MVP targets India, our YOLO weights and faster-whisper models must be explicitly benchmarked against Indian demographic datasets.

## 4. Unresolved Research Questions (Action Items)

- **Q1:** What is the most compute-efficient way to map 2D YOLO bounding boxes from a low-end Android camera to a 3D semantic map of a classroom?
- **Q2:** How accurately can a 7B parameter OSS LLM (like Qwen2.5) classify specific discourse moves (e.g., "IRE: Initiate-Response-Evaluate") compared to GPT-4? _Requires immediate benchmarking._
- **Q3:** How do we algorithmically differentiate "engaged listening" from "boredom" in cultures where students are taught to sit rigidly still?

---

_This document will be continuously updated as new relevant papers are published in LAK and EDM conferences._
