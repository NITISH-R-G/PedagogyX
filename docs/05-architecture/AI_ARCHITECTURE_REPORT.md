# AI Architecture Report

**Status:** Draft v1.0
**Date:** 2026-05-20
**Role:** Autonomous Senior AI Engineer & Applied Intelligence Systems Architect

## 1. AI Problem Analysis

The core problem is robust multimodal intelligence in highly constrained, noisy environments. We must process audio (heavy accents, code-switching, noise), video (low resolution, poor lighting, occlusions), and slide text to synthesize an authoritative "Pedagogy Index." Accuracy and reliability are paramount; a hallucinated or biased evaluation will destroy trust instantly.

## 2. AI System Architecture

The pipeline is split into a Hot Path (real-time, heuristics, lightweight) and a Cold Path (batch, authoritative, deep models).

- **Audio Pipeline (Cold):** `faster-whisper` (ASR) -> PyAnnote (Diarization) -> Audio feature extraction (librosa).
- **Vision Pipeline (Cold):** YOLOv8-pose (Student attention/posture proxy) -> Florence-2/Tesseract (Slide OCR).
- **Fusion & Intelligence (Cold):** Raw events are aligned temporally. `Qwen2.5-7B` via vLLM ingests the chunked multimodal context to generate coaching narratives and classify pedagogical patterns (e.g., wait time).

## 3. Prompt & Reasoning Strategy

- **Strict Constraints:** Prompts for the LLM must enforce a "Chain of Verification." The model must cite the specific timestamp and speaker ID for every claim it makes in the coaching summary.
- **Few-Shot Prompting:** Prompts will include examples of excellent pedagogical practices (based on Indian curriculum standards) to anchor the model's evaluations.

## 4. RAG & Retrieval Design

- **Vector Store:** Qdrant.
- **Embeddings:** BGE-m3 for robust multilingual and long-context embeddings.
- **Mechanism:** District curriculum documents, teaching rubrics, and historical teacher transcripts are embedded. During the generation of the coaching summary, relevant standard benchmarks are retrieved to contextualize the feedback.

## 5. AI Infrastructure

- **Hardware:** Bare-metal RTX 5070 (12GB VRAM) clusters to meet the ₹0 budget constraint.
- **Serving:** `vLLM` provides high-throughput LLM serving with PagedAttention. `TensorRT` is used to compile CV and Audio models for maximum inference speed on NVIDIA hardware.
- **Queuing:** Celery workers manage the massive async batch loads.

## 6. Evaluation Strategy

- **ASR:** Measure Word Error Rate (WER) against a custom golden dataset of noisy Indian classroom audio. Target: <15% WER.
- **Diarization:** Measure Diarization Error Rate (DER). Target: <20%.
- **LLM:** Automated evaluations using a larger model (e.g., GPT-4 class, during dev only) to score the Qwen2.5 outputs for hallucination rate, tone, and pedagogical alignment. Human-in-the-loop review by expert educators is mandatory before G2 pilot launch.

## 7. Security & Safety

- **Data Minimization:** Student faces and names are explicitly NOT fed into the LLM. Only anonymized transcripts and bounding box statistics are used for reasoning.
- **Prompt Injection:** The LLM does not interact directly with raw user input during the processing pipeline, mitigating traditional injection attacks.

## 8. Observability

- **Model Telemetry:** Log inference latency, VRAM usage, and queue wait times in Prometheus.
- **Drift Detection:** Monitor the distribution of the generated "Pedagogy Index" scores. A sudden shift indicates model drift or an unhandled environmental change (e.g., a new microphone type).

## 9. Performance Optimization

- **Quantization:** `Qwen2.5-7B` must run in INT4/AWQ format to fit comfortably within the 12GB VRAM limit while leaving room for the CV/ASR models on the same or adjacent nodes.
- **Micro-batching:** For the Hot Path, CV models will skip frames (e.g., analyzing 1 frame per second instead of 30) to dramatically reduce load without losing meaningful pedagogical state.

## 10. Risks & Tradeoffs

- **Risk:** The 12GB VRAM constraint of the RTX 5070 severely limits the use of powerful multimodel LLMs (like LLaVA-NeXT) in concurrent pipelines. **Tradeoff:** We must rely on highly optimized, unimodal extraction (Whisper + YOLO) followed by late text fusion in a smaller LLM, sacrificing some deep cross-modal reasoning capabilities.

## 11. Agile Sprint Plan

- **Sprint 1:** Benchmark `faster-whisper` and `Qwen2.5-7B` on the RTX 5070 dev machine. Establish baseline throughput metrics.
- **Sprint 2:** Build the audio pipeline: Pipeline `faster-whisper` output into PyAnnote diarization. Generate the first synchronized `[Time][Speaker] Text` artifact.
- **Sprint 3:** Build the LLM fusion layer. Feed the artifact into vLLM and iteratively refine prompts until the output consistently aligns with a known human-generated rubric.
