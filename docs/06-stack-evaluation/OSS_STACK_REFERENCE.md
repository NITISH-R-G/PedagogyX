# Open-Source Stack Reference (PedagogyX Default)

**Policy:** [ADR-0005](../08-rfc-adr/ADR-0005-foss-first-stack.md)  
**GPU:** [GPU_BUDGET_RTX5070.md](../05-architecture/GPU_BUDGET_RTX5070.md)

---

## Layer map

| Layer | OSS choice | License | Avoid (paid API) |
|-------|------------|---------|------------------|
| **Capture agent** | **Tauri** (Rust) + GStreamer / FFmpeg | MIT / LGPL | Commercial SDKs |
| **Media server** | **MediaMTX** or **Janus** WebRTC | MIT / GPL | Twilio, Agora |
| **Transcode** | **FFmpeg** | LGPL | AWS Elemental |
| **Object storage** | **MinIO** | AGPL | S3-only lock-in (S3 API OK) |
| **DB** | **PostgreSQL** | PostgreSQL | — |
| **Analytics OLAP** | **ClickHouse** | Apache-2.0 | — |
| **Queue** | **Redpanda** or **NATS JetStream** | BSL / Apache | SQS-only design |
| **Orchestration** | **k3s** (light K8s) or **Docker Compose** (pilot) | Apache | — |
| **Auth** | **Keycloak** | Apache-2.0 | Auth0 |
| **Observability** | **Prometheus + Grafana + Loki** | Apache / AGPL | Datadog default |
| **ASR** | **faster-whisper** (CTranslate2) | MIT | Deepgram, Google STT |
| **Diarization** | **WhisperX** / **sortformer** (verify license) | varies | — |
| **VAD** | **silero-vad** | MIT | — |
| **CV detect** | **Ultralytics YOLO11** → ONNX → **TensorRT** | AGPL* | Commercial CV APIs |
| **OCR (slides)** | **PaddleOCR** or **Tesseract** | Apache | Google Vision |
| **Embeddings** | **sentence-transformers** (e.g. `paraphrase-multilingual-MiniLM`) | Apache | OpenAI embeddings |
| **Vector DB** | **Qdrant** (self-hosted) | Apache-2.0 | Pinecone |
| **LLM serving** | **Ollama** or **vLLM** | MIT / Apache | OpenAI, Anthropic |
| **LLM weights** | **Qwen2.5-7B-Instruct**, **Llama-3.2-3B** (Q4 quant) | Apache / Llama license | — |
| **Inference runtime** | **ONNX Runtime** + **TensorRT** | MIT / NVIDIA EULA | — |
| **API** | **Go** (Fiber/Chi) or **Python FastAPI** | BSD / MIT | — |
| **Web UI** | **Next.js** | MIT | — |

\* YOLO AGPL: ensure compliance (source offer) or use Apache-licensed detectors if needed.

---

## India-specific OSS notes

| Need | OSS approach |
|------|----------------|
| Hindi + English ASR | `whisper-large-v3` with language detect; fine-tune LoRA on consented data later |
| Low bandwidth | Agent-side H.265 encode; upload after class if live fails |
| On-prem only | MinIO + Postgres on school LAN; optional sync to district server |

---

## D-12 default (founder silent + OSS mandate)

**No cloud LLM** on student-adjacent content.  
**Ollama/vLLM** on same machine as RTX 5070; prompts = transcript + JSON metrics only.

---

## What we do NOT run on RTX 5070 12 GB (v1)

| Capability | Reason |
|------------|--------|
| Video-LLM (Qwen2-VL 7B) + multi-cam + Whisper large concurrently | VRAM overflow |
| 4× 1080p live CV streams | Bandwidth + VRAM |
| 70B LLM | Impossible on 12 GB |
| Cloud auto-scale GPU | Hardware constraint |

---

## Pilot install (single RTX 5070 box)

```text
Docker Compose on Ubuntu 24.04 + NVIDIA driver 550+
├── mediamtx          # ingest
├── minio
├── postgres
├── redis
├── nats              # job queue
├── worker-asr        # faster-whisper
├── worker-cv         # TensorRT YOLO (batch)
├── worker-llm        # Ollama
├── api               # Go/FastAPI
└── web               # Next.js static + API proxy
```

**Target pilot:** 1 GPU → **2 classrooms** hot audio + **all rooms** cold batch overnight.
