# Deep Research Literature Review & Papers Database

**Status:** Draft v1.0
**Owner:** PedagogyX Research Architecture Team

This document serves as an exhaustive catalog and summary of critical scientific literature underpinning the PedagogyX multimodal architecture. It expands upon the initial seed corpus to cover advanced topics in affective computing, classroom discourse analysis, teacher effectiveness modeling, and long-context video understanding.

## I. Multimodal Machine Learning & Long-Context Video

### 1. Long-Context Video Understanding with Multimodal Transformers

**Tags:** `LKV`, `MM`, `CV`
**Publication Year:** 2023 (Various NeurIPS / CVPR)
**Summary:** Recent advancements in models like Video-LLaMA and long-context variants of Qwen/GPT-4V demonstrate the ability to process extended video sequences by using memory banks and hierarchical tokenization.
**Relevance to PedagogyX:** Crucial for the "Cold Path" analysis of 45-60 minute classroom sessions, allowing the AI to connect a concept introduced at minute 5 with a student's question at minute 40.
**Metrics:** mAP on ActivityNet, Long Video QA benchmarks.
**Limitations:** Extreme GPU memory consumption; highly susceptible to hallucination when temporal gaps are wide.

### 2. Instructional Activity Recognition Transformer (NSF PAR)

**Tags:** `CV`, `MM`, `TE`
**Publication Year:** 2022
**Summary:** Proposes a transformer-based architecture specifically fine-tuned for recognizing complex instructional activities (e.g., "teacher lecturing," "group work," "student presentation") using multimodal fusion of audio and video streams.
**Relevance to PedagogyX:** Directly informs our pedagogical index scoring pipeline.
**Datasets:** Proprietary NSF funded classroom dataset.
**Limitations:** Relies heavily on fixed, high-angle classroom cameras. Transferability to POV (Ray-Ban glasses) is unknown and requires validation.

## II. Affective Computing & Engagement Detection

### 3. DAiSEE: Towards User Engagement Recognition in the Wild (Kaur et al.)

**Tags:** `AFF`, `CV`
**Publication Year:** 2016
**Summary:** A foundational paper introducing the DAiSEE dataset for recognizing boredom, engagement, confusion, and frustration using deep convolutional networks.
**Relevance to PedagogyX:** Provides the theoretical basis for our "Student Attention Proxy."
**Datasets:** DAiSEE (E-learning context, frontal face).
**Limitations:** Primarily e-learning; transferring these models to physical classrooms with varying head poses, occlusion, and low resolution is notoriously difficult.

### 4. Classroom Group Engagement Analysis (Nature Sci Data)

**Tags:** `AFF`, `CV`
**Publication Year:** 2025
**Summary:** A recent dataset and baseline model focusing on measuring engagement at the _group_ level rather than isolated individuals, utilizing spatial-temporal graphs.
**Relevance to PedagogyX:** highly relevant for measuring overall classroom climate and pacing effectiveness.
**Metrics:** Group Cohesion Index, average engagement score.
**Limitations:** Compute-heavy; graph neural networks (GNNs) may struggle on low-end cloud tier allocations without extreme optimization.

## III. Classroom Discourse & Teacher Effectiveness

### 5. Automated Analysis of Teacher Questions (Donnelly et al.)

**Tags:** `CDA`, `SYS`
**Publication Year:** 2016 (ACL)
**Summary:** Uses NLP (and early ASR) to classify teacher questions into distinct pedagogical categories (e.g., procedural, factual, high-order cognitive).
**Relevance to PedagogyX:** Essential for generating automated coaching feedback ("You asked 80% factual questions today, try incorporating more high-order queries").
**Datasets:** Proprietary audio transcripts.
**Limitations:** Heavily reliant on perfect ASR. In a noisy Indian classroom context, WER (Word Error Rate) spikes will degrade classification accuracy severely.

### 6. STAS: System for Teacher Analysis and Support (Ku et al.)

**Tags:** `TE`, `SYS`
**Publication Year:** 2018 (ICCE)
**Summary:** Explores the architecture and UX of a system designed to provide automated feedback to teachers based on audio and video inputs, focusing on teacher acceptance.
**Relevance to PedagogyX:** Informs our dashboard UX and the need to frame AI as a "coach" rather than a "supervisor" to avoid rejection by unions and staff.

### 7. Student Diarization in Noisy Environments (Karumbaiah et al.)

**Tags:** `CDA`, `SYS`
**Publication Year:** 2024 (EDM)
**Summary:** State-of-the-art approaches to speaker diarization (who spoke when) specifically tuned for the acoustic chaos of K-12 classrooms.
**Relevance to PedagogyX:** Crucial for calculating the Teacher-to-Student talk ratio.
**Metrics:** Diarization Error Rate (DER).
**Limitations:** Extreme difficulty distinguishing between different children's voices.

## IV. Reproducibility & Implementation Plan

- **Action Item 1:** We must prioritize models with available weights (e.g., HuggingFace) to build the initial proof-of-concept for the cold path pipeline.
- **Action Item 2:** We must immediately begin synthesizing a custom dataset mimicking POV classroom footage to fine-tune activity recognition models, as existing datasets heavily bias toward fixed cameras.
- **Action Item 3:** ASR evaluation requires immediate benchmarking on "Hinglish" datasets to establish a baseline WER before trusting downstream NLP pedagogical analysis.
