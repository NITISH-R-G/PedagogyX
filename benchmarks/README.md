# RTX 5070 benchmark suite (S01-09)

Dev-only scripts to measure RTF, VRAM, and latency before sizing India cloud GPUs.

**No RTX 5070 today?** Use **`cpu` profile** — full pipeline works. See [DEV_WITHOUT_GPU.md](DEV_WITHOUT_GPU.md).

## Setup

```bash
cd benchmarks
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-bench.txt
```

Optional: [Ollama](https://ollama.com/) for LLM step — `ollama pull llama3.2:1b` (cpu) or `qwen2.5:7b-instruct-q4_K_M` (gpu).

## Run

```bash
# Today (no GPU)
./bench_full_pipeline.sh cpu

# Tomorrow (RTX 5070)
./bench_full_pipeline.sh gpu
```

From repo root: `./scripts/dev-verify.sh` (lint + cpu benchmarks).

## Output

Results in `benchmarks/results/` — see [BENCHMARK_RESULTS_SUMMARY.md](BENCHMARK_RESULTS_SUMMARY.md).

## Policy

Per ADR-0006: **dev workstation only** — not deployed to classroom smartboards.
