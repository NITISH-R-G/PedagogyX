# Benchmark Results Summary

**Last run:** 2026-05-20 (UTC)  
**Active profile:** **`cpu`** — works **without RTX 5070** (use until founder machine available)  
**Tomorrow:** run `./bench_full_pipeline.sh gpu` on RTX 5070 for production sizing.

---

## CPU profile — **PASS** (dev-ready today)

| Step               | Result | Metric              |
| ------------------ | ------ | ------------------- |
| Whisper small      | OK     | 30 s audio, CPU     |
| Whisper medium     | OK     | 60 s audio, CPU     |
| YOLO11n 480p       | OK     | ~33 FPS CPU         |
| Ollama llama3.2:1b | OK     | **~10.6 tok/s** CPU |

Run again:

```bash
cd benchmarks && ./bench_full_pipeline.sh cpu
```

Full dev check from repo root:

```bash
./scripts/dev-verify.sh
```

See [DEV_WITHOUT_GPU.md](DEV_WITHOUT_GPU.md).

---

## GPU profile — **pending** (RTX 5070 from tomorrow)

```bash
cd benchmarks
ollama pull qwen2.5:7b-instruct-q4_K_M
./bench_full_pipeline.sh gpu
```

Commit JSON under `results/*_cuda.json` and update this file.

---

## Planning estimates (until GPU run)

Use [GPU_PILOT_COST_MODEL.md](../docs/05-architecture/GPU_PILOT_COST_MODEL.md) and [GPU_BUDGET_RTX5070.md](../docs/05-architecture/GPU_BUDGET_RTX5070.md) for pilot capacity until CUDA numbers land.

| Job (50 min lesson, est.) | Wall      | VRAM    |
| ------------------------- | --------- | ------- |
| ASR medium INT8           | 8–15 min  | ~3 GB   |
| ASR large-v3 INT8         | 15–25 min | ~5 GB   |
| CV 480p batch             | 5–10 min  | ~2 GB   |
| LLM Qwen2.5-7B Q4         | 2–5 min   | ~5–6 GB |

**Pilot capacity (1× 12 GB GPU):** ~2 live previews + overnight batch ~16 rooms.

---

## Historical CPU baseline (silent audio — not speech-realistic)

| Script           | Config       | RTF / FPS |
| ---------------- | ------------ | --------- |
| Whisper medium   | 120 s silent | RTF 0.019 |
| Whisper large-v3 | 120 s silent | RTF 0.032 |
| YOLO 480p        | 200 frames   | 33.8 FPS  |

Use GPU profile with real lesson audio for authoritative sizing.
