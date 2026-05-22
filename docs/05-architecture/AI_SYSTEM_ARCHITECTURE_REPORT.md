# AI System Architecture & Applied Intelligence Report

**Version:** 1.0
**Author:** Autonomous Senior AI Engineer & Applied Intelligence Systems Architect
**Focus:** Multimodal Classroom Intelligence Pipeline

## 1. AI Problem Analysis

The core AI challenge in PedagogyX is transforming raw, asynchronous, multi-modal sensor data (video from multiple cameras, audio from a lapel mic, screen captures) into a cohesive, pedagogical narrative. This must be done efficiently on consumer-grade GPUs (RTX 5070) without relying on proprietary cloud models.

- **Challenges:** Accent-heavy speech in noisy environments, varying classroom lighting, occlusion of students, and context-dependent pedagogical assessment (a "good" strategy in Math might be "bad" in Art).

## 2. AI System Architecture

The AI pipeline is a multi-stage fusion process:

1. **Extraction (Edge/Ingest):** Basic heuristics to filter out empty rooms or absolute silence.
2. **Perception Layer (GPU Workers):**
   - **Audio:** `faster-whisper` for ASR. Pyannote for speaker diarization (Teacher vs. Student).
   - **Video:** YOLOv8 (exported to TensorRT) for spatial tracking (teacher location, gross student posture).
   - **Screen:** OCR (Tesseract or a lightweight layout LM) to extract text from slides/board.
3. **Alignment Layer:** Temporal alignment of transcript, bounding boxes, and OCR text into a unified chronological JSON structure.
4. **Reasoning Layer:** Ollama running Qwen2.5 (7B) ingests the aligned JSON to classify pedagogical moves (e.g., "Check for Understanding", "Direct Instruction") and generate feedback.

## 3. Prompt & Reasoning Strategy

- **System Prompts:** Must be highly restrictive, forcing the LLM to act as a strict instructional coach using a specific rubric.
- **Few-Shot Examples:** Embed examples of "good" and "bad" teaching moments mapped to JSON data directly in the prompt.
- **Chain of Thought:** The prompt will force the LLM to explain _why_ it assigned a score before outputting the final JSON score.

## 4. RAG & Retrieval Design

- **Goal:** Contextualize the evaluation based on district curriculum or specific lesson plans.
- **Implementation:** Vectorize uploaded lesson plans using `all-MiniLM-L6-v2` and store in pgvector.
- **Retrieval:** During the Reasoning Layer, retrieve relevant sections of the lesson plan to allow the LLM to evaluate if the teacher met the stated objectives.

## 5. AI Infrastructure

- **Hardware:** Centralized pool of RTX 5070 (12GB VRAM) machines.
- **Deployment:** Containerized worker daemons. TensorRT for CV, CTranslate2 for ASR, llama.cpp backend for Ollama.
- **VRAM Management:** The pipeline must multiplex tasks to fit within the 12GB limit. E.g., unload YOLO from VRAM before loading the Qwen2.5 model, or run them on dedicated worker nodes.

## 6. Evaluation Strategy

- **Ground Truth:** We need a small, human-annotated dataset of 50 classroom videos (annotated for talk ratio, pedagogical moves, and engagement).
- **Automated Evals:** Compare system outputs against ground truth using metrics like Word Error Rate (WER) for ASR, mean Average Precision (mAP) for CV, and exact match/LLM-as-a-judge for pedagogical scoring.

## 7. Security & Safety

- **Hallucination Prevention:** The UI must visually distinguish between "Facts" (ASR transcripts) and "AI Inferences" (Engagement scores). The LLM prompt must strictly forbid generating feedback without citing a specific timestamped event.
- **Data Privacy:** Faces in video must be blurred before long-term storage using a lightweight anonymization pass during the CV stage if DPDP regulations demand it.

## 8. Observability

- **Metrics:** Track VRAM usage, inference latency per chunk, and LLM token generation speed (tokens/sec).
- **Failure Logging:** Log edge cases where the pipeline fails (e.g., ASR confidence < 40%) for active learning and future model fine-tuning.

## 9. Performance Optimization

- **Quantization:** Run Qwen2.5 in 4-bit or 8-bit quantization to fit into VRAM while preserving reasoning capabilities.
- **Batching:** `faster-whisper` and TensorRT models must process video chunks in batches rather than frame-by-frame to maximize GPU utilization.

## 10. Risks & Tradeoffs

- **Risk:** The 7B LLM fails to grasp nuanced pedagogical strategies compared to a 70B model or GPT-4.
  - **Mitigation:** Rely heavily on the structured data (talk ratio, movement) for objective metrics, and frame LLM outputs strictly as "suggestions" rather than definitive judgments.
- **Tradeoff:** Running sequential inference (CV -> ASR -> LLM) on a single 12GB GPU increases total latency. We accept this tradeoff to meet the ₹0 customer hardware cost constraint.

## 11. Agile Sprint Plan (AI Track)

- **Sprint 03:** Deploy `faster-whisper` container and validate English/Hindi WER against a sample video.
- **Sprint 04:** Build and test the YOLO + TensorRT pipeline for basic teacher tracking.
- **Sprint 05:** Construct the prompt engineering harness for Qwen2.5 and run the first end-to-end multimodal fusion test.
