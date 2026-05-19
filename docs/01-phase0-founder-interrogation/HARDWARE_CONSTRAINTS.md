# Hardware & OSS Constraints (Founder)

**Recorded:** 2026-05-19

| Constraint | Value |
|------------|-------|
| **GPU max** | NVIDIA **RTX 5070**, **12 GB** VRAM |
| **Stack** | **Free & open source** for core platform |
| **Cloud AI APIs** | **Not used** in core path (ASR, LLM, CV) |
| **Deployment** | On-prem / school edge server |

## What this means for v1

| Feature | Delivery |
|---------|----------|
| Live talk ratio | Yes — faster-whisper **small** on GPU/CPU |
| Live multi-cam HD CV | **No** on one 5070 — one 480p cam max |
| Multi-cam + screen analytics | Yes — **after class** batch queue |
| Admin final pedagogy score | After cold pipeline (same night or next morning) |
| LLM coaching report | **Ollama** Qwen2.5-7B-Q4 on same GPU |

## To scale beyond ~2 live rooms per GPU

- Add more **RTX 5070** edge nodes (still OSS), or
- Accept **audio-only live** for all rooms + batch video overnight

## Docs

- [GPU_BUDGET_RTX5070.md](../05-architecture/GPU_BUDGET_RTX5070.md)
- [OSS_STACK_REFERENCE.md](../06-stack-evaluation/OSS_STACK_REFERENCE.md)
- [ADR-0005](../08-rfc-adr/ADR-0005-foss-first-stack.md), [ADR-0006](../08-rfc-adr/ADR-0006-rtx5070-compute-budget.md)
