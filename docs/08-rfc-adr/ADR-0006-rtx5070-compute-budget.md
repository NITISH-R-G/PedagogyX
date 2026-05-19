# ADR-0006: RTX 5070 (12 GB) Maximum GPU — Compute Budget

| Field | Value |
|-------|-------|
| **Status** | Accepted (founder-directed) |
| **Date** | 2026-05-19 |
| **Hardware** | NVIDIA GeForce RTX 5070, **12 GB GDDR7** **[FACT]**

## Context

Founder stated **RTX 5070 is the max GPU** available. This is a **single consumer GPU** constraint—not a cloud GPU farm. Earlier v1 scope (multi-cam **real-time** + batch + LLM) **cannot run at full fidelity concurrently** on one 12 GB card per deployment unit without strict scheduling and degraded hot path.

## Decision

### Deployment unit

**[ASSUMPTION]** One RTX 5070 per **edge node** (school server or classroom PC), not per cloud tenant.

| Model | Description |
|-------|-------------|
| **A — School edge server** (recommended) | 1× RTX 5070 serves **4–8 classrooms** sequentially / round-robin |
| **B — Per-classroom PC** | 1 GPU per room — best latency, highest hardware cost |
| **C — Cloud GPU** | **Out of scope** until budget allows — violates current hardware constraint |

### Hot path (real-time) — **reduced to fit 12 GB**

| Component | Model | VRAM (approx) | Notes |
|-----------|-------|---------------|-------|
| ASR streaming | `faster-whisper` **small** or **medium** INT8 | 1–3 GB | CPU fallback if GPU saturated |
| Activity CV | YOLO11n / YOLOv8n INT8 TensorRT | 1–2 GB | **One** cam stream @ 480p for live |
| Screen | Frame diff + OCR (PaddleOCR / Tesseract) on CPU | 0 GPU | Avoid GPU OCR in hot path |
| LLM live nudges | **Disabled** on GPU | — | No room with video + ASR |

**Hot path rule:** At most **one** of {medium ASR, small YOLO} on GPU simultaneously unless quantized nano models only.

### Cold path (authoritative) — **serialized jobs**

Run as **queue** on same GPU after lesson ends (or night batch):

1. Full ASR (`medium` or `large-v3` INT8) — ~4–6 GB peak
2. Diarization (WhisperX / pyannote — license-check) — run when ASR unloaded
3. Multi-cam CV batch at 720p — one model load at a time
4. LLM summary via **Ollama** `Qwen2.5-7B-Instruct` Q4_K_M (~5–6 GB) — **exclusive** GPU job

**Never** load large-v3 + 7B LLM + YOLO simultaneously on 12 GB.

### Founder scope adjustment (required honesty)

| Original v1 ask | RTX 5070 reality |
|-----------------|------------------|
| Live multi-cam CV | **Defer** — 1 cam preview @ 480p OR audio-only live |
| Live admin dashboard | **Audio + preview metrics** live; **full pedagogy index** after batch |
| Many concurrent live classes on one box | **Queue** or **audio-only** for excess rooms |

Founder can override by adding GPUs or accepting **non-real-time** video analytics.

## Consequences

- Update [SYSTEM_ARCHITECTURE.md](../05-architecture/SYSTEM_ARCHITECTURE.md) — edge queue scheduler required
- Update SLAs: live = preliminary; final scores after batch on same node
- Pilot sizing: start **1–2 classrooms per GPU**, measure, then tune

## Validation

Benchmark script on RTX 5070: concurrent streams vs VRAM (Sprint 01 TB-009).
