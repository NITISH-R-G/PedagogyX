# Stack Evaluation — OSS-First + RTX 5070 Constraint

**Status:** v0.2 | **ADRs:** [ADR-0005](../08-rfc-adr/ADR-0005-foss-first-stack.md), [ADR-0006](../08-rfc-adr/ADR-0006-rtx5070-compute-budget.md)

**Canonical OSS list:** [OSS_STACK_REFERENCE.md](OSS_STACK_REFERENCE.md)

---

## Executive recommendation

| Layer         | Choice                                            | Why                        |
| ------------- | ------------------------------------------------- | -------------------------- |
| Policy        | **100% OSS core path**                            | Founder mandate            |
| Compute       | **On-prem edge** with **RTX 5070 12GB**           | No cloud GPU budget        |
| API           | **Go** (ingest/control) + **Python** (ML workers) | Performance + ML ecosystem |
| ML train      | **PyTorch** → export **ONNX** → **TensorRT**      | 5070 inference             |
| LLM           | **Ollama** + **Qwen2.5-7B-Q4**                    | Fits 12 GB alone           |
| ASR           | **faster-whisper**                                | OSS, no API fees           |
| Media         | **FFmpeg** + **MediaMTX**                         | OSS                        |
| Data          | **PostgreSQL** + **MinIO** + **ClickHouse**       | OSS                        |
| Orchestration | **Docker Compose** (pilot) → **k3s**              | OSS                        |
| Cloud         | **Optional** — only for non-GPU static hosting    | Avoid GPU SaaS             |

**Removed from default plan:** AWS Transcribe, OpenAI, commercial ASR, managed vector SaaS.

---

## Backend languages (unchanged preference, OSS-aligned)

| Role                            | Language                  |
| ------------------------------- | ------------------------- |
| API gateway, auth proxy, upload | **Go**                    |
| ML workers, eval scripts        | **Python 3.11+**          |
| Capture agent                   | **Tauri (Rust)** + FFmpeg |

---

## ML frameworks

| Use                 | Tool                    |
| ------------------- | ----------------------- |
| Training / export   | PyTorch                 |
| Serving             | ONNX Runtime + TensorRT |
| LLM                 | Ollama or vLLM (OSS)    |
| Experiment tracking | **MLflow** (OSS)        |

---

## Video

| Use               | Tool                 |
| ----------------- | -------------------- |
| Transcode         | FFmpeg               |
| Live ingest       | MediaMTX             |
| Future live coach | Janus (GPL — review) |

---

## Frontend

**Next.js** — OSS, self-hosted static export or Node server on same edge box.

---

## Infrastructure

### Development (RTX 5070 workstation)

Docker Compose full stack; benchmarks per [GPU_BUDGET_RTX5070.md](../05-architecture/GPU_BUDGET_RTX5070.md).

### Production

| Layer    | Host                                     |
| -------- | ---------------------------------------- |
| Clients  | Android + Windows smartboard (low spec)  |
| API + ML | Central OSS servers (India — D-PROC TBD) |
| Dev GPU  | RTX 5070 **not in classroom**            |

### Obsolete note — school-edge 5070

```text
Single server (64 GB RAM recommended, 2 TB NVMe)
├── Docker Compose
├── 1× RTX 5070 for all GPU jobs (scheduled)
└── Serve 1–2 live classrooms + overnight batch for 8–16 recordings
```

**Not viable on one 5070:** 20 simultaneous live multi-cam ML sessions.

---

## Cost model shift

| Before (cloud) | After (OSS + 5070)                 |
| -------------- | ---------------------------------- |
| $/GPU-hour AWS | Cap-ex: GPU + server ~$1.5–2k/node |
| $/ASR minute   | Electricity + ops time             |
| Scaling        | Buy more 5070 nodes                |

See [GPU_BUDGET_RTX5070.md](../05-architecture/GPU_BUDGET_RTX5070.md).
