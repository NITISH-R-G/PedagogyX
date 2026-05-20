# Benchmark Results Summary

**Run date:** 2026-05-20 (UTC)  
**Host:** Cursor Cloud VM — **CPU only** (no `nvidia-smi`)  
**Purpose:** Baseline automation; **replace with RTX 5070 CUDA run** for production sizing (S02-03).

---

## Measured (CPU, silent audio — lower bound RTF)

| Script  | Model / config        | Wall (s) | Metric                             | JSON                                |
| ------- | --------------------- | -------- | ---------------------------------- | ----------------------------------- |
| Whisper | medium, 120 s audio   | 2.27     | RTF **0.019**                      | `results/whisper_medium_cpu.json`   |
| Whisper | large-v3, 120 s audio | 3.84     | RTF **0.032**                      | `results/whisper_large-v3_cpu.json` |
| YOLO11n | 480p, 200 frames      | 5.93     | **33.8 FPS**                       | `results/yolo_480p_cpu.json`        |
| YOLO11n | 720p, 100 frames      | 3.12     | **32.1 FPS**                       | `results/yolo_720p_cpu.json`        |
| Ollama  | qwen2.5 7B Q4         | —        | **Skipped** (Ollama not installed) | —                                   |

**Caveat:** Silent audio RTF is **not representative** of real classroom speech; use GPU run with sample lesson audio on RTX 5070.

---

## Extrapolated RTX 5070 planning numbers (from [GPU_BUDGET_RTX5070.md](../docs/05-architecture/GPU_BUDGET_RTX5070.md))

Until GPU JSON exists, size pilots using these **estimates**:

| Job                      | Est. wall (50 min lesson) | VRAM    |
| ------------------------ | ------------------------- | ------- |
| ASR medium INT8          | 8–15 min                  | ~3 GB   |
| ASR large-v3 INT8        | 15–25 min                 | ~5 GB   |
| CV 480p batch            | 5–10 min                  | ~2 GB   |
| LLM Qwen2.5-7B Q4 report | 2–5 min                   | ~5–6 GB |

**Pilot capacity (1× 12 GB GPU):** ~2 live preview lessons + overnight batch for ~16 rooms (see [GPU_PILOT_COST_MODEL.md](../docs/05-architecture/GPU_PILOT_COST_MODEL.md)).

---

## Re-run on RTX 5070 (founder machine)

```bash
cd benchmarks && ./bench_full_pipeline.sh
# Requires: NVIDIA driver, Ollama + qwen2.5:7b-instruct-q4_K_M
```

Commit new JSON under `benchmarks/results/` with `_cuda` suffix and update this file.
