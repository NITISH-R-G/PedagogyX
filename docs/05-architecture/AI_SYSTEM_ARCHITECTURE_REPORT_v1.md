# PedagogyX: AI System Architecture Report v1

**Date:** 2026-05-24
**Author:** Autonomous Senior AI Engineer & Applied Intelligence Systems Architect

## 1. Reliability

The AI pipeline must gracefully handle corrupted audio chunks and varying network speeds. We will implement robust error handling around model inference (e.g., fallback to lighter models if VRAM is exhausted) and use a message queue (Redis) to ensure no dropped tasks during peak hours.

## 2. Accuracy

Given the DPDP constraints and India focus, ASR must excel at Hindi-English code-switching. We will leverage state-of-the-art multilingual OSS models (e.g., faster-whisper large-v3) and build a synthetic data pipeline for continuous fine-tuning on regional educational accents.

## 3. Scalability

The system is bifurcated into a "Hot Path" (lightweight, real-time edge processing/VAD) and a "Cold Path" (deep batch processing). The Cold Path relies on an asynchronous task queue allowing us to linearly scale GPU nodes (RTX 5070s) as processing demand grows.

## 4. Maintainability

All models will be containerized via Docker and served via standard APIs (e.g., OpenAI compatible API via vLLM). This decouples the core backend from specific model implementations, allowing us to swap models as OSS capabilities evolve without refactoring the API service.

## 5. Inference Efficiency

Constrained by 12GB VRAM on the RTX 5070:

- We will use aggressive quantization (INT4/AWQ) for LLMs (e.g., Qwen2.5-7B-Instruct).
- Models will not be kept in memory simultaneously. A robust orchestrator will unload ASR models before loading LLMs for batch analysis.
- Flash Attention 2 will be utilized where applicable.

## 6. User Value

The AI focuses on extracting actionable pedagogical insights (e.g., Socratic questioning ratios, pacing) rather than surveillance. The output must be highly interpretable, providing specific timestamps and transcripts as evidence for any AI-generated score to build trust with teachers.

## 7. Observability

Every stage of the ML pipeline will log metrics:

- Inference latency (per chunk and total).
- VRAM usage peaks.
- ASR confidence scores.
  We will use Prometheus/Grafana to monitor these metrics to detect model drift or hardware degradation.

## 8. Security

AI runs entirely on-premise/controlled cloud infrastructure (OSS models only). No PII is sent to external APIs (OpenAI/Anthropic). This guarantees DPDP compliance and prevents data leakage.

## 9. Extensibility

The pipeline is designed as a DAG (Directed Acyclic Graph) of events. New modalities (e.g., smartboard OCR) can be added as new event listeners on the message bus without disrupting the core audio pipeline.

## 10. Long Term Sustainability

By relying purely on OSS models and consumer-grade GPUs, the OPEX per classroom approaches zero, aligning with the founder's "₹0 budget" constraint. Continuous fine-tuning pipelines ensure the models adapt to new pedagogical frameworks over time.
