# AI System Architecture Report v3

**Owner:** Autonomous Principal Research Architect & Lead Systems Engineer
**Project:** PedagogyX
**Status:** In Progress

## 1. Executive Summary

The core objective of PedagogyX is to construct a world-class multimodal AI classroom intelligence and teacher optimization platform. The system operates within highly constrained boundaries: it must utilize a FOSS-first software stack, run inference offline due to India data residency regulations, and process incoming audio/visual streams captured from low-end clients, primarily Meta Ray-Ban (DAT) smart glasses (per ADR-0009).

This architecture departs from traditional surveillance by strictly focusing on instructional coaching, multimodal pedagogical analysis, and continuous teacher improvement loops.

## 2. Epistemic Status (Facts, Assumptions, Hypotheses, Speculative Ideas)

Before detailing the architecture, it is critical to separate known constraints from unvalidated hypotheses.

### 2.1 Validated Facts

- **Hardware Profile:** Primary v1 capture client is Meta Ray-Ban smart glasses via an Android companion app (DAT host), replacing smartboards as the primary capture surface (ADR-0009).
- **Compute Constraints:** Cloud inference operates on self-hosted RTX 5070 (12GB VRAM) clusters (ADR-0006). Hard memory bounds dictate orchestration of heavy multimodal pipelines.
- **Data Residency & Privacy:** Strict DPDP compliance requires data residency in the `ap-south-1` region. Raw biometric capture (faces/voices) must be tightly controlled and potentially ephemeral.
- **Topology:** Hybrid Edge/Cloud architecture. The edge (Android host) handles buffering, upload lifecycle, and potential minimal preprocessing; the central cloud handles batch inference and heavy ML fusion (ADR-0008).

### 2.2 Assumptions

- **Edge Connectivity:** We assume highly unstable, intermittent WAN connectivity in target Indian classrooms, necessitating robust chunk buffering at the Android edge.
- **Battery & Thermal:** We assume the Meta Ray-Ban and Android host can sustain a 45-60 minute continuous recording session without critical thermal failure or battery exhaustion, though this is actively under evaluation via the Mock Device Kit (MDK).
- **Audio Clarity:** We assume the Ray-Ban microphone array, situated closely to the teacher's mouth, provides sufficient SNR (Signal-to-Noise Ratio) to effectively use quantized Whisper variants without severe Word Error Rate (WER) degradation from classroom background noise.

### 2.3 Hypotheses

- **Pedagogical Fusion:** We hypothesize that late fusion of transcribed text (semantic), voice prosody (affective), and teacher POV head-pose/gaze (kinesic) will yield a significantly more accurate "Pedagogy Index" than text-only analysis (e.g., AI Sokrates).
- **POV Computer Vision:** We hypothesize that engagement detection algorithms, traditionally trained on fixed IP cameras, can be successfully adapted or fine-tuned to process erratic POV footage from the Ray-Bans.

### 2.4 Speculative Ideas

- **Real-Time Ear-Piece Coaching:** An autonomous agent providing real-time, whispered haptic or audio feedback to the teacher via the Ray-Bans (e.g., "Pacing is too fast, pause for questions").
- **Whiteboard POV OCR:** Extracting high-quality semantic meaning from a moving POV stream capturing chalk/whiteboards.

## 3. Multimodal System Architecture

The AI stack separates into edge processing and centralized FOSS inference components, adhering strictly to a D-PROC Hybrid topology.

### 3.1 Dual-Path Processing Pipeline

- **Hot Path (Real-time / Near Real-time):**
  - **Function:** Fast, low-latency heuristics for basic telemetry, connection state, talk ratios (via VAD), and lightweight activity detection.
  - **Models:** Lightweight YOLO variants or purely heuristic audio energy models.
  - **Storage:** Ephemeral Redis state caching.
- **Cold Path (Batch Authoritative):**
  - **Function:** High-precision, authoritative pedagogy scoring, deep transcription via ASR, multi-modal fusion, and full diarization powered by advanced GPU inference workers.
  - **Execution:** Directed Acyclic Graph (DAG) orchestration via background worker queues (Python-based Celery/Temporal) ensuring systematic handling of out-of-sync audio/video chunks.

### 3.2 Model Stack

- **Speech-to-Text (ASR):** Open-source Whisper variants (e.g., Distil-Whisper or Whisper v3) optimized for English/Hindi code-switching and quantized for RTX 5070 constraints.
- **Computer Vision (CV):** Lightweight YOLO models for engagement bounding boxes and smaller transformer models (e.g., MobileVLM/LLaVA with 4-bit quantization) for batch pedagogical scene understanding.
- **LLM/Reasoning:** Locally deployed quantized LLMs (e.g., Qwen2.5-7B-Q4 via vLLM) focusing on summarization, parsing pedagogical rubrics, and generating structured JSON reports.

### 3.3 RAG & Vector Retrieval Design

To ensure feedback is grounded in institutional reality (not generic AI advice), a Retrieval-Augmented Generation approach is employed.

- **Vector Database:** PostgreSQL with the `pgvector` extension for unified ACID-compliant storage alongside structured data.
- **Ingestion Pipeline:** School guidelines, pedagogical rubrics (e.g., modified Danielson Framework), and historical lesson templates are embedded using lightweight sentence-transformers.
- **Retrieval Workflow:** When the LLM evaluates a transcript chunk, a hybrid search (keyword + semantic) retrieves the exact rubric dimension to anchor the prompt, mitigating hallucination. Cross-encoder reranking is applied for high-stakes policy matches.

## 4. Prompt, Reasoning & Context Strategy

Prompts are designed as immutable contracts between the orchestrator and the LLM, maintaining strict instructional boundaries.

- **Few-Shot Grounding:** Prompts utilize few-shot examples bounded by system guidelines. The LLM is instructed _never_ to guess student sentiment if visual/audio evidence is lacking.
- **Timestamp Anchoring:** All LLM conclusions (e.g., "The teacher asked a high-order cognitive question") must strictly trace back to an explicit transcript timestamp or a specific CV event frame.
- **Hallucination Mitigation:** A secondary validation chain (LLM-as-a-judge or strict regex parsing) checks the proposed coaching tip against the retrieved facts and ASR confidence scores.
- **Context Management:** Long 45-minute sessions are hierarchically chunked and aggressively summarized before final evaluation, keeping the context window within the strict boundaries of the quantized 7B model.

## 5. Security, Safety & Compliance

Ensuring the security of minor student data and the integrity of the models is paramount.

- **DPDP & Tiered Analytics:** Adhering to ADR-0002, analytics are tiered. Raw video is processed ephemerally on the cold path and subsequently purged, retaining only semantic embeddings or anonymized state logs.
- **Prompt Injection Prevention:** Input sanitization separates untrusted audio transcripts from internal system prompts. Transcripts are treated strictly as data payloads, not executable instructions.
- **Permission Controls:** Strict RBAC limits viewing access. Teachers see actionable feedback; admins view aggregate anonymized reports. Internal engineering ML debugging access is strictly audited.
- **Output Validation:** Rigid JSON schema validation (e.g., Pydantic/Guidance) forces LLMs to return strict structured outputs. Failures trigger safe "Review Needed" states rather than hallucinations.

## 6. Observability & Evaluation Pipelines

Operating FOSS models offline demands rigorous telemetry.

- **Telemetry & Tracing:** OpenTelemetry traces the entire lifecycle from the Ray-Ban DAT Bluetooth capture, through the Android edge buffer, API Gateway, and down to the RTX 5070 worker queue execution time.
- **Dead Letter Queues (DLQ):** Comprehensive DLQ implementation for worker failures, capturing full tracebacks to rapidly debug A/V drift or chunk corruption.
- **Automated Evaluations:** Unit testing (`pytest`) simulates end-to-end synthetic sessions. Nightly builds run LLM-as-a-judge pipelines validating schema adherence, citation accuracy, and hallucination rates.
- **Benchmarks:** Tracking ASR Word Error Rate (WER) on noisy Indian classroom audio and CV precision on engagement metrics.

## 7. Performance & Resource Optimization

- **VRAM Budgeting:** RTX 5070 memory boundaries are strictly enforced. ASR, CV, and LLM workloads must run on separate dedicated worker nodes or utilize aggressive context offloading.
- **Quantization:** Utilizing integer quantization (INT4/INT8/AWQ) on LLMs and Vision models to maximize batch throughput over latency for the cold path.
- **Network Resiliency:** Streaming transcription on the edge is avoided in favor of robust chunk-based uploads, separating logic into distinct micro-batches to survive WAN dropouts.

## 8. Risks, Tradeoffs & Unknowns

- **POV CV Degradation:** Applying models trained on static cameras to erratic Ray-Ban POV footage may yield unusable engagement heatmaps. **Mitigation:** Heavy reliance on ASR/prosody as the primary signal, with CV acting as an optional enhancer.
- **Hallucination under Constraints:** Smaller local quantized models (7B) have higher hallucination rates than massive proprietary APIs (GPT-4). **Mitigation:** Extreme structured generation constraints and RAG anchoring.
- **Clock Drift:** Audio sync drift between the glasses and the phone during long sessions. **Mitigation:** Implementing the Master Clock protocol defined in RFC-0002.
- **Scaling Ceiling:** Offline GPU provisioning means rigid scaling limits; unpredictable end-of-day upload spikes will inevitably delay cold-path authoritative scoring.

## 9. Agile Sprint Plan (Phase 0 -> Phase 1)

- **Sprint 1 (Infrastructure & MVP ASR):** Setup RTX 5070 worker nodes in Docker Compose. Deploy vLLM and Whisper. Implement the chunked ASR pipeline and basic Python worker queues.
- **Sprint 2 (DAT Edge Integration):** Develop the Android DAT host integration using the Mock Device Kit (MDK). Build the edge LAN buffer and chunk upload lifecycle.
- **Sprint 3 (Cold Path Fusion & RAG):** Implement the full batch ML fusion pipeline. Integrate pgvector for pedagogical template retrieval. Develop the Qwen2.5-7B prompts.
- **Sprint 4 (Observability & Hardening):** Implement OpenTelemetry and DLQ monitoring. Establish the automated evaluation pipeline for hallucination tracking. Conduct end-to-end latency testing.
- **Sprint 5 (Pilot & Refinement):** Deploy to Indian pilot schools. Monitor model drift. Iterate on prompt grounding based on real-world code-switched classroom acoustics.
