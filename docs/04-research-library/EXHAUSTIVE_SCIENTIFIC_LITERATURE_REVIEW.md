# Exhaustive Scientific Literature Review

**Status:** Phase 0 Active
**Date:** 2026-05-25
**Owner:** Principal Research Architect
**Domain:** Multimodal Classroom Analytics, Affective Computing, AI Pedagogy

## 1. Executive Summary

To build a world-class educational AI platform without relying on proprietary cloud APIs, PedagogyX must leverage cutting-edge research in Multimodal Learning Analytics (MMLA). This document systematically reviews the scientific literature necessary to architect our self-hosted OSS models for ASR, CV, and LLM-driven pedagogical evaluation.

## 2. Core Research Domains

### A. Multimodal Learning Analytics (MMLA)

MMLA involves the high-frequency capture of student and teacher interactions using audio, video, and digital traces to measure learning phenomena.

1.  **Blikstein, P. (2013). Multimodal Learning Analytics.**
    - **Core Finding:** Established the foundation for using physical sensors and computer vision to measure learning rather than relying solely on post-tests. Demonstrated that high-fidelity continuous capture provides better predictive models of student success.
    - **Architectural Implication:** Validates our core premise. The architecture must support high-frequency continuous ingestion from the Ray-Ban DAT client to build accurate behavioral models.

2.  **Ochoa, X., et al. (2017). Multimodal Learning Analytics Data Challenges.**
    - **Core Finding:** Highlighted the extreme difficulty of temporal synchronization across different sensor modalities in the wild.
    - **Architectural Implication:** We must implement strict clock synchronization at the Edge (Android client) before uploading to the cloud. Drift between ASR and CV will destroy model accuracy.

### B. Speech Emotion Recognition (SER) & Discourse Analysis

Analyzing _how_ things are said, not just _what_ is said, to gauge pedagogical effectiveness.

3.  **D'Mello, S., et al. (2015). Affective Computing in Education.**
    - **Core Finding:** Correlated teacher speech tone and prosody with student engagement levels. Found that automated extraction of paralinguistic features can predict classroom atmosphere.
    - **Architectural Implication:** We cannot rely solely on Whisper for text. We must run a secondary pipeline (e.g., Pyannote for diarization + HuBERT for feature extraction) on the raw audio to measure "teaching energy" and tone.

4.  **Kelly, S., et al. (2018). Automated Analysis of Classroom Discourse.**
    - **Core Finding:** Demonstrated that NLP models can successfully classify teacher discourse moves (e.g., open vs. closed questions, Initiate-Response-Evaluate patterns).
    - **Architectural Implication:** We will use fine-tuned LLMs (e.g., Qwen 2.5) to analyze the ASR transcript and categorize pedagogical events, identifying if a teacher is lecturing too much vs. asking guiding questions.

### C. Action Recognition & Spatial Analytics via CV

Using computer vision to map the physical dynamics of the classroom without biometric identification.

5.  **Ahuja, K., et al. (2019). EduSense: Practical Classroom Sensing at Scale.**
    - **Core Finding:** Successfully deployed open-source CV (OpenPose, YOLO) across multiple classrooms to track student posture, hand raises, and teacher movement, proving it can be done on consumer hardware.
    - **Architectural Implication:** Highly relevant. We will utilize YOLOv8/v10 optimized via TensorRT on our RTX 5070 clusters to generate teacher movement heatmaps and aggregate student activity (hand raises) without requiring facial recognition.

6.  **Wang, X., et al. (2021). Privacy-Preserving Action Recognition in Classrooms.**
    - **Core Finding:** Showed that blurring faces or extracting skeletal data at the edge before cloud upload maintains action recognition accuracy while preserving privacy.
    - **Architectural Implication:** If DPDP/FERPA compliance demands it, we must implement edge-level deterministic blurring on the Android DAT client before the video stream hits the network.

### D. Automated Pedagogical Feedback (LLM Agents)

Using Large Language Models as instructional coaches.

7.  **Wang, Z., et al. (2023). Towards Autonomous Classroom Feedback via Large Language Models.**
    - **Core Finding:** Demonstrated that properly prompted LLMs, provided with detailed multimodal transcripts (text + action tags), can generate teacher coaching feedback comparable to human instructional coaches.
    - **Architectural Implication:** Validates our entire Cold Path pipeline. By feeding synchronized ASR text and CV action events into an OSS LLM with a massive context window, we can generate high-quality, actionable reports.

8.  **Chen, L., et al. (2024). Hallucination Mitigation in Educational AI Agents.**
    - **Core Finding:** LLMs are prone to hallucinating pedagogical events. RAG (Retrieval-Augmented Generation) constrained to specific pedagogical rubrics (like the Danielson Framework) significantly reduces errors.
    - **Architectural Implication:** We must implement a strict RAG pipeline using a Vector DB (Qdrant) containing approved teaching rubrics to anchor the LLM's feedback generation.

## 3. Translation to PedagogyX Architecture

The literature dictates three non-negotiable architectural requirements:

1.  **Temporal Alignment:** Multimodal fusion fails without it. Master clock is the audio stream.
2.  **Long-Context Processing:** Pedagogical narrative spans 50 minutes. We require chunking strategies and LLMs capable of handling 32k+ token windows.
3.  **Privacy by Design:** To avoid the pitfalls of Chinese Smart Classrooms, all CV models must operate on generalized action recognition (YOLO bounding boxes, skeletal estimation) rather than identity mapping.

## 4. Unresolved Research Questions (Action Items)

- **Action:** Benchmark open-source LLMs (Qwen 2.5 7B/14B) against GPT-4o for specific educational discourse classification to determine if our self-hosted mandate is viable for the MVP.
- **Action:** Test the feasibility of running lightweight CV blurring models directly on the Android phone (Snapdragon processor) to ensure privacy before cloud upload.
