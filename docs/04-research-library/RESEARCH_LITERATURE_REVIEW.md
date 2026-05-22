# Research Literature Review & Summaries

**Status:** Draft v0.1
**Date:** 2026-05-20
**Owner:** Architecture Team

## Overview

This document compiles extensive research across Multimodal AI, Educational Data Mining (EDM), Affective Computing, and Classroom Analytics. It serves as the scientific foundation for PedagogyX's composite pedagogy index.

---

## 1. Multimodal AI & Classroom Analytics

### Multimodal Transformers for Long-Context Video Understanding

- **Focus:** Leveraging transformer architectures to process hours of multi-cam video.
- **Key Findings:** Modality fusion (early vs. late) dictates VRAM requirements. Late fusion (aggregating independent Audio and CV embeddings) scales better for resource-constrained environments (like our RTX 5070 limit).
- **Application to PedagogyX:** We will use independent pipelines (YOLO for CV, faster-whisper for Audio) and perform late fusion in a lightweight Python orchestrator to determine state (e.g., "Student discussing while pointing at board").

### AI Sokrates & TPACK Framework Automation

- **Focus:** Automating Technological Pedagogical Content Knowledge (TPACK) evaluation.
- **Key Findings:** High correlation between certain teacher discourse moves (open questions vs. closed) and student outcomes.
- **Application to PedagogyX:** Incorporate discourse move classification into the cold path via `Qwen2.5-7B` prompt engineering.

---

## 2. Educational Data Mining (EDM) & Learning Analytics

### Classroom Discourse Analysis

- **Focus:** Modeling the structure of classroom conversations (Initiation-Response-Evaluation or IRE).
- **Key Findings:** Traditional teacher-dominated IRE limits engagement. S-T (Student-Teacher) speaking curves are standard metrics.
- **Application to PedagogyX:** Our hot path must calculate a rolling Teacher/Student Talk Ratio. The cold path will calculate absolute silence gaps (Wait Time) to measure pedagogical pacing.

### Teacher Effectiveness Modeling

- **Focus:** Determining proxies for "good teaching" via observable metrics.
- **Key Findings:** There is no single "golden metric", but composite indices incorporating time-on-task, equitable student participation, and clear instructional pacing correlate highly with standard rubrics (e.g., Danielson Framework).
- **Application to PedagogyX:** The _Pedagogy Index_ will be a weighted composite of talk ratios, interaction density, and board utilization, explicitly documented as indicative rather than definitively summative.

---

## 3. Affective Computing & Behavioral Intelligence

### Speech Emotion Recognition in Noisy Classrooms

- **Focus:** Detecting teacher clarity and emotional tone (burnout vs. enthusiasm).
- **Key Findings:** Pure audio emotion recognition is highly susceptible to noise (chairs scraping, fan noise).
- **Application to PedagogyX:** Affective computing is deferred to Phase 2 due to reliability issues in low-quality Indian classroom audio captures. We will rely on structural metrics (talk time, pacing) first.

### Engagement Detection via Student Gaze and Pose

- **Focus:** Using CV to measure student attention.
- **Key Findings:** Pose estimation (e.g., leaning forward, head orientation) is a more reliable proxy for engagement than raw facial emotion recognition, which is noisy and ethically fraught.
- **Application to PedagogyX:** YOLO11n will track bounding boxes and basic pose vectors to calculate an "Interaction Density" heatmap, avoiding invasive emotion logging.

---

## Conclusion

The scientific consensus supports a composite, multi-metric approach. PedagogyX must avoid the trap of predicting "learning outcomes" directly from video, instead focusing on measuring _observable pedagogical structures_ (talk time, transitions, board usage) that correlate with quality instruction.
