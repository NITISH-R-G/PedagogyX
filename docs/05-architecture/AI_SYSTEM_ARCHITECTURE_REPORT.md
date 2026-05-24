# AI System Architecture & Applied Intelligence Report

**Version:** 2.0
**Author:** Autonomous Senior AI Engineer & Applied Intelligence Systems Architect
**Focus:** Multimodal Classroom Intelligence Pipeline for PedagogyX

## AI Problem Analysis

The core mission of PedagogyX is to democratize elite teacher coaching by extracting highly nuanced, multimodal pedagogical signals from wild classroom environments. The operational constraints dictate a ₹0 customer hardware budget, mandating the use of ultra-lightweight edge capture (Meta Ray-Ban smart glasses via an Android host app) streaming to a centralized, OSS-first inference stack. The fundamental AI engineering challenge lies in reconciling the extreme variability of Indian classroom environments (heavy code-switching between Hindi and English, severe acoustic noise, poor lighting, occlusion) with the severe compute limitations of our target infrastructure (12GB VRAM RTX 5070 central GPU pools).

We must synthesize raw, temporally asynchronous streams—point-of-view video from the teacher, lapel or glasses microphone audio, and background activity—into a unified, deterministic "Pedagogy Index" without hallucination. Furthermore, strict adherence to India's DPDP privacy regulations prohibits the transmission of PII to third-party cloud APIs, necessitating a fully self-hosted, air-gapped capable AI pipeline. The failure scenarios are catastrophic: hallucinating a negative interaction could destroy a teacher's career, while drifting into latency bottlenecks would render the live supervision dashboards useless.

## AI System Architecture

To achieve massive scale on consumer-grade hardware, the AI architecture is explicitly bifurcated into a lightweight Hot Path for real-time telemetry and a deterministic Cold Path for authoritative evaluation.

**1. Hot Path (Real-Time Ingestion & Heuristics)**
The Android DAT client streams chunked A/V payloads via a local edge buffer to the central MediaMTX ingest node. For live supervision, we bypass deep learning where possible. A highly quantized `faster-whisper` (tiny or small model) transcribes audio, feeding basic Python-based heuristics to estimate talk ratios (Teacher vs. Student) within a 5-second rolling window. YOLO11n (TensorRT optimized, 480p) processes video frames at a maximum of 5 FPS to establish gross spatial tracking. These metrics power the live admin dashboard via WebSockets.

**2. Cold Path (Authoritative Multimodal Fusion)**
The authoritative batch pipeline operates overnight or asynchronously.

- **Audio Processing:** A medium/large-v3 `faster-whisper` model, accelerated by CTranslate2, processes the high-fidelity audio chunk to produce highly accurate bilingual transcripts. Pyannote handles speaker diarization, classifying distinct teacher and student segments.
- **Visual & Contextual Processing:** YOLO11n extracts detailed student attention proxies and teacher movement vectors.
- **Alignment Engine:** A deterministic temporal alignment service unifies the transcript timestamps with the visual bounding box event stream into a dense JSON payload.
- **Reasoning Engine:** The aligned JSON is injected into an Ollama-served `Qwen2.5-7B-Instruct` model (quantized to Q4_K_M). This model functions exclusively as a pedagogical reasoning engine, outputting structured scoring rubrics and interaction summaries.

## Prompt & Reasoning Strategy

The LLM is highly constrained. We employ a "Chain of Verification" and structured output enforcement to completely eliminate narrative hallucinations. The system prompt forces `Qwen2.5-7B-Instruct` into a strict data-transformation role rather than a creative one.

**Prompt Structure:**

1. **System Directive:** "You are an expert pedagogical evaluator. You must strictly base all evaluations on the provided JSON event log. Do not infer events that are not explicitly documented."
2. **Context Window:** The temporally aligned transcript and visual metadata JSON.
3. **Task Definition:** Specific classification requests (e.g., "Identify instances of 'Wait Time' exceeding 3 seconds following a teacher question.").
4. **Output Format:** Forced JSON schema generation, requiring the LLM to cite specific `{timestamp}` and `{event_id}` attributes for every pedagogical claim.

**Grounding & Hallucination Mitigation:**
By divorcing the reasoning layer from the raw pixel/audio domain, we constrain the LLM to logic over deterministic metadata. The UI is architected to parse the generated JSON and render hyperlinks directly to the corresponding video timestamps. If the LLM hallucinates an event, the missing or invalid timestamp acts as an immediate failure flag, allowing the system to suppress the output.

## RAG & Retrieval Design

The pedagogical evaluation cannot exist in a vacuum; it must be grounded in the school district's specific curriculum and approved teaching frameworks.

**Ingestion Pipeline:**
District standards, lesson plans, and historical teacher performance rubrics are ingested, chunked hierarchically by topic and grade level, and embedded using a lightweight, multilingual model (`BGE-m3`) capable of handling Hindi/English contexts. The vectors are stored in a centralized `pgvector` instance, co-located with the session data to simplify tenant isolation.

**Retrieval Workflow:**
During the Cold Path reasoning phase, the system executes a semantic search using the extracted keywords from the session transcript. The top-k relevant curriculum standards are injected into the LLM's context window. This RAG strategy allows the model to evaluate not just _how_ the teacher taught, but _if_ they taught the required material, ensuring the feedback is contextually tethered to the specific lesson objectives.

## AI Infrastructure

The infrastructure topology is ruthlessly optimized for the ₹0 edge hardware budget, shifting all compute to a centralized, high-density GPU pool.

- **Inference Systems:** The central OSS backend utilizes containerized worker daemons. We deploy `vLLM` or `Ollama` for high-throughput, PagedAttention-backed LLM serving. Computer vision workloads utilize `TensorRT` to extract maximum performance from the NVIDIA architecture.
- **Hardware Topology:** A scalable pool of RTX 5070 (12GB VRAM) machines.
- **Scaling Strategy:** The system employs asymmetric autoscaling. Hot Path ingest nodes (CPU-bound) scale linearly with concurrent classroom sessions. The Cold Path GPU workers operate off a distributed message queue (Redis/Celery), buffering the overnight batch processing load to maximize GPU utilization (targeting >90% sustained utilization) and smooth out diurnal traffic spikes.
- **VRAM Management:** Given the 12GB limitation, dynamic VRAM swapping is employed. Batch jobs are orchestrated so that a single GPU sequentially loads the CV model, then the ASR model, and finally the LLM, preventing Out-Of-Memory (OOM) crashes while maximizing throughput per node.

## Evaluation Strategy

AI quality cannot be managed purely via intuition; rigorous, automated evaluation pipelines are mandatory.

- **Automated Benchmarks:** We maintain a golden dataset of heavily accented, multi-speaker Indian classroom recordings with manually annotated ground-truth transcripts and bounding boxes. Every commit to the ML pipeline triggers a regression suite measuring Word Error Rate (WER) and Diarization Error Rate (DER).
- **Hallucination Tracking:** The LLM's JSON outputs are continuously parsed to ensure every cited timestamp exists within the source JSON. A failure rate > 0.1% triggers an immediate alert.
- **LLM-as-a-Judge:** During development, we utilize larger models to evaluate the qualitative feedback generated by the 7B model, scoring it for tone, pedagogical accuracy, and alignment with the provided rubric.

## Security & Safety

Security is paramount given the presence of minors in the dataset and the strict requirements of DPDP.

- **Sandboxing & Isolation:** AI workers operate in ephemeral, network-isolated Docker containers with no outbound internet access. They can only communicate with the Redis queue and the MinIO object store.
- **Data Privacy & Anonymization:** Student faces captured via the Ray-Ban glasses are subjected to a lightweight, deterministic blurring pass before long-term storage in the Cold Archive. No raw video is ever passed to the LLM.
- **Prompt Injection Prevention:** The system sanitizes the ingested transcript, stripping control characters and known exploit strings before injecting it into the LLM context, preventing malicious audio segments from hijacking the evaluation logic.

## Observability

Comprehensive telemetry is required to manage the operational complexity of a distributed inference pipeline.

- **Tracing & Monitoring:** We utilize OpenTelemetry to trace requests across the ingest, ASR, CV, and LLM boundaries. Prometheus scrapes node-level metrics (GPU utilization, VRAM allocation, temperature) and application-level metrics (inference latency, token generation speed, queue depth).
- **Analytics Dashboards:** Grafana visualizes the p50 and p95 latencies for both the Hot and Cold paths, enabling rapid identification of bottlenecks.
- **Diagnostics:** Every failure (e.g., ASR confidence dropping below a critical threshold, Ollama timeout) is logged with the full context payload to facilitate offline debugging and targeted fine-tuning.

## Performance Optimization

Operating advanced models on 12GB GPUs requires aggressive, continuous optimization.

- **Quantization:** `Qwen2.5-7B` is quantized to `Q4_K_M` (4-bit), drastically reducing the memory footprint while maintaining reasoning fidelity. ASR models utilize INT8 precision.
- **Batching & Throughput:** `faster-whisper` and the YOLO models process audio and video in large batches, amortizing the cost of memory transfers over multiple frames/seconds of audio.
- **Caching:** RAG embeddings and intermediate feature extraction results are cached in Redis. If a teacher re-processes a lesson or requests a different rubric evaluation, the pipeline skips the expensive perception layer and immediately re-runs the reasoning layer.

## Risks & Tradeoffs

- **Risk:** Relying on a 7B model for complex pedagogical reasoning introduces a risk of shallow or generic feedback compared to frontier models.
  - **Mitigation:** We restrict the LLM to analyzing highly structured, quantitative metadata (talk ratio, pacing) rather than asking it to derive deep emotional or psychological insights from raw text.
- **Tradeoff:** To meet the budget constraints, we process the authoritative "Pedagogy Index" asynchronously. Real-time dashboards rely on highly degraded proxy metrics.
  - **Mitigation:** The UI clearly demarcates "Live Estimates" from "Authoritative Analytics," managing administrator expectations and ensuring contractual SLAs are bound only to the Cold Path processing.

## Agile Sprint Plan

- **Sprint 1 (Current Phase):** Finalize the central OSS backend integration with `faster-whisper` and Ollama. Establish baseline throughput metrics on the RTX 5070 dev machine. Validate the end-to-end flow from the Android DAT client mock capture to the batch processor.
- **Sprint 2:** Implement the temporal alignment engine. Fuse transcript outputs with simulated YOLO metadata. Construct the prompt engineering harness for Qwen2.5-7B and run the first deterministic JSON generation test.
- **Sprint 3:** Build out the RAG vector ingestion pipeline for district curriculums. Integrate semantic retrieval into the reasoning phase.
- **Sprint 4:** Deploy the automated evaluation suite. Run the golden dataset through the pipeline and optimize hyper-parameters to drive down the error rates and ensure 0% hallucination on timestamp citations.
