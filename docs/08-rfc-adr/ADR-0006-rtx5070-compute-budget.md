# ADR-0006: RTX 5070 (12 GB) — Development & Benchmark GPU Only

| Field | Value |
|-------|-------|
| **Status** | **Amended** (2026-05-19) |
| **Date** | 2026-05-19 (original), amended same day |
| **Hardware** | NVIDIA GeForce RTX 5070, **12 GB GDDR7** |

## Context (correction)

Founder clarified: **RTX 5070 is for development**, not where the production app runs.

**Production clients:** **Android** devices and **Windows smartboards** with **low-end specs** (classroom floor).

## Decision

### RTX 5070 role — **DEV ONLY**

| Use | Allowed |
|-----|---------|
| Local integration testing | Yes |
| Model export (ONNX / TensorRT) | Yes |
| Benchmark faster-whisper, YOLO, Ollama before deploy | Yes |
| Training / LoRA fine-tune (small) | Yes |
| Production inference in schools | **No** |

### Production inference location

**[ASSUMPTION until D-PROC answered]** Central **OSS processing service** (India-hosted VPS or district server with GPU)—**not** on smartboards.

See [ADR-0007](ADR-0007-production-clients-low-end.md).

### Dev machine pipeline validation (5070)

Use 12 GB VRAM rules from [GPU_BUDGET_RTX5070.md](../05-architecture/GPU_BUDGET_RTX5070.md) to:

- Prove models fit and meet latency targets **before** deploying weights to central servers
- Size central server GPU requirements (e.g. “production needs same VRAM profile per N concurrent lessons”)

## Supersedes

Previous text implying one RTX 5070 **per school edge node** in production — **withdrawn**.

## Related

- [ADR-0007](ADR-0007-production-clients-low-end.md)
- [PRODUCTION_CLIENT_SPEC.md](../05-architecture/PRODUCTION_CLIENT_SPEC.md)
