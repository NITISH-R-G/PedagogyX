# Hardware & OSS Constraints (Founder)

**Last updated:** 2026-05-19 (amended)

---

## Development vs production

| Environment | Hardware | Role |
|-------------|----------|------|
| **Development** | NVIDIA **RTX 5070 12 GB** | Benchmarks, train/export models, local Compose stack — **not production** |
| **Production clients** | **Android** + **low-end Windows smartboards** | Capture, encode, upload only — **no GPU ML on device** |
| **Production ML** | **Hybrid** — school/district **LAN edge** (buffer/ingest) + **India cloud GPU** (analytics) | OSS: faster-whisper, TensorRT/YOLO, Ollama on cloud; edge per ADR-0008 |

---

## OSS policy

**Free & open source** for core platform — see [ADR-0005](../08-rfc-adr/ADR-0005-foss-first-stack.md).

No paid ASR/LLM APIs in core path. Cloud **hosting** may cost money; software remains OSS.

---

## Production client limits (smartboards)

- **No** on-device Whisper, YOLO, or 7B LLM
- **Yes** hardware H.264 encode when available
- **Yes** offline buffer + resumable upload
- Multi-cam: **screen + mic + 0–1 cam** on device; extra cameras via **RTSP to server**

---

## Real-time analytics path (revised)

| Layer | Where |
|-------|--------|
| Live talk ratio / previews | **Central server** (streaming chunks or WebRTC) |
| Final pedagogy index | **Central server** batch queue |
| Dev validation of models | **RTX 5070** workstation |

---

## Docs

- [PRODUCTION_CLIENT_SPEC.md](../05-architecture/PRODUCTION_CLIENT_SPEC.md)
- [ADR-0006](../08-rfc-adr/ADR-0006-rtx5070-compute-budget.md) (dev GPU)
- [ADR-0007](../08-rfc-adr/ADR-0007-production-clients-low-end.md)
- [GPU_BUDGET_RTX5070.md](../05-architecture/GPU_BUDGET_RTX5070.md) (dev benchmarking)
- [OSS_STACK_REFERENCE.md](../06-stack-evaluation/OSS_STACK_REFERENCE.md)

---

## Still open

| ID | Question |
|----|----------|
| **D-DEV** | Confirm pilot site **make/model** (research list in [INDIA_PILOT_DEVICE_REFERENCE.md](INDIA_PILOT_DEVICE_REFERENCE.md)) |
| **D-20** | Closed: **M-A** primary, **M-B** + **M-C** secondary |
