# Dev without RTX 5070 (today)

**You can develop and validate tooling on CPU today.** Run the full GPU sizing profile tomorrow on the RTX 5070.

---

## Quick start (works now — no GPU)

```bash
# 1. Docs lint (same as CI)
npx markdownlint-cli 'docs/**/*.md'

# 2. Benchmarks — CPU profile (~2–5 min)
cd benchmarks
./bench_full_pipeline.sh cpu

# 3. Or everything at once from repo root
./scripts/dev-verify.sh
```

### Ollama (optional, for LLM step)

```bash
# One-time (Linux)
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &   # background
ollama pull llama3.2:1b   # small model for CPU smoke test
```

CPU profile uses `llama3.2:1b` by default. GPU profile tomorrow uses `qwen2.5:7b-instruct-q4_K_M`.

---

## Tomorrow — RTX 5070

```bash
cd benchmarks
./bench_full_pipeline.sh gpu
# Requires: NVIDIA driver, ollama pull qwen2.5:7b-instruct-q4_K_M
```

Update [BENCHMARK_RESULTS_SUMMARY.md](BENCHMARK_RESULTS_SUMMARY.md) with `_cuda` JSON files.

---

## What CPU results are good for

| Use CPU today            | Wait for 5070                  |
| ------------------------ | ------------------------------ |
| Scripts run end-to-end   | Production GPU sizing          |
| CI smoke tests           | VRAM peak / RTF on real speech |
| Dev environment sanity   | Ollama 7B Q4 latency           |
| Docs + architecture work | Pilot capacity hard numbers    |

Planning numbers until GPU run: [GPU_PILOT_COST_MODEL.md](../docs/05-architecture/GPU_PILOT_COST_MODEL.md) (estimates).
