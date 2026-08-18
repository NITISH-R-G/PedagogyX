# Scientific Literature Review v1: Multimodal Classroom Analytics

**Date:** 2026-05-25
**Author:** Autonomous Principal Research Architect
**Status:** DRAFT
**Context:** Review of recent scientific literature regarding multimodal classroom analytics to inform PedagogyX AI features.

## 1. Executive Summary

This review analyzes recent literature retrieved via Crossref focusing on "multimodal classroom analytics." The goal is to identify proven methodologies, data fusion techniques, and pedagogical mapping strategies that can be adapted for the PedagogyX platform, particularly within our constrained (12GB VRAM) and POV-first (Meta Ray-Ban) architecture.

## 2. Analyzed Papers

Based on our initial literature search, the following key papers were identified:

### 2.1. M-CBAF: A Multimodal Classroom Behaviour Analytics Framework (2026)

- **Title:** M-CBAF: A Multimodal Classroom Behaviour Analytics Framework for Learning Analytics Using Multimodal Feature Fusion and Behaviour-to-Engagement Mapping
- **Authors:** Ritik Raju Mohite, R. B. Keskar, Praveen Kumar
- **Year:** 2026
- **DOI:** 10.2139/ssrn.7265787
- **Relevance to PedagogyX:** Highly relevant. The focus on "Feature Fusion" and "Behaviour-to-Engagement Mapping" aligns directly with our goal of generating pedagogical scores from multimodal inputs. We need to investigate their specific fusion techniques (early vs. late fusion) to determine if they are viable within our 12GB VRAM constraint.

### 2.2. Guiding the Integration of Multimodal Learning Analytics (2024)

- **Title:** Guiding the Integration of Multimodal Learning Analytics in the Glocal Classroom: A Case Study Applying MAMDA
- **Authors:** Hamza Ouhaichi, Daniel Spikol, Bahtijar Vogel
- **Year:** 2024
- **DOI:** 10.5220/0012690900003693
- **Relevance to PedagogyX:** Relevant for architectural planning. The application of "MAMDA" (Multimodal Analytics Architecture) in a "Glocal" (global/local) context may offer insights for our Hybrid Edge/Cloud deployment model, particularly concerning data synchronization and localized processing.

### 2.3. Multimodal Learning Analytics in a Laboratory Classroom (2019)

- **Title:** Multimodal Learning Analytics in a Laboratory Classroom
- **Authors:** Man Ching Esther Chan, Xavier Ochoa, David Clarke
- **Year:** 2019
- **DOI:** 10.1007/978-3-030-13743-4_8
- **Relevance to PedagogyX:** Foundational. While older, laboratory classroom studies often establish the baseline metrics for what is measurable (e.g., proxemics, gaze, basic speech acts). We must adapt these laboratory findings to the noisy, in-the-wild environment of Indian classrooms captured via POV glasses.

### 2.4. Multimodal Learning Analytics for Understanding Collocated Collaboration (2020)

- **Title:** Multimodal Learning Analytics for Understanding Collocated Collaboration in Authentic Classroom Settings
- **Authors:** Pankaj Chejara
- **Year:** 2020
- **DOI:** 10.1109/icalt49669.2020.00123
- **Relevance to PedagogyX:** Relevant for "Authentic Classroom Settings." Our MVP will be deployed in real classrooms, not labs. Understanding collaboration (even if our primary focus is the teacher) is necessary for inferring classroom-level discourse metrics (e.g., group work vs. lecture).

### 2.5. Classroom Discourse and Multimodal Conversation Analysis (2021)

- **Title:** Classroom Discourse and Multimodal Conversation Analysis
- **Authors:** Christine M. Jacknick
- **Year:** 2021
- **DOI:** 10.3366/edinburgh/9781474455183.003.0002
- **Relevance to PedagogyX:** Highly relevant. "Classroom Discourse" is a primary signal for assessing pedagogy (e.g., open vs. closed questions, wait time). Multimodal conversation analysis provides the theoretical framework for combining ASR (what is said) with CV (gestures, gaze) to accurately assess the _quality_ of the discourse.

## 3. Key Takeaways for Architecture

1.  **Fusion is Critical:** The recent literature (M-CBAF, 2026) emphasizes multimodal feature fusion. Our architecture must support a robust event-streaming pipeline capable of temporally aligning ASR, CV, and potentially biometric (from DAT) data streams before feeding them into the assessment model.
2.  **Context is King:** Analytics must move beyond simple action recognition (e.g., "teacher is pointing") to pedagogical context (e.g., "teacher is pointing to clarify a student question"). The conversation analysis frameworks (Jacknick, 2021) will be vital for designing our prompt engineering strategy for the LLM evaluating the session.
3.  **Real-World vs. Lab:** We must prioritize techniques proven in "authentic settings" (Chejara, 2020) over lab-based models, as our primary input is a potentially shaky, obstructed POV camera.

## 4. Next Research Steps

- Deep dive into the specific fusion architectures proposed in M-CBAF (2026) to assess their computational cost.
- Research specialized lightweight models for speech emotion recognition and engagement detection suitable for a 12GB GPU.
- Investigate datasets used in these papers to determine if they can be used for initial pre-training or evaluation of our synthetic pipelines.
