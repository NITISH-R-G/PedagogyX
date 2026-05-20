# RTX 5070 benchmark suite (S01-09)

Dev-only scripts to measure RTF, VRAM, and latency before sizing India cloud GPUs.

**Requires:** NVIDIA GPU + CUDA for full runs. Scripts exit gracefully on CPU-only VMs.

## Setup

```bash
cd benchmarks
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-bench.txt
```

Optional system deps: [Ollama](https://ollama.com/) for `bench_ollama.py`, TensorRT for YOLO TRT path.

## Run

```bash
./bench_full_pipeline.sh
```

Or individually:

```bash
python bench_whisper.py --model medium --device cuda
python bench_yolo_trt.py --device cuda
python bench_ollama.py --model qwen2.5:7b-instruct-q4_K_M
```

## Output

Results append to `benchmarks/results/` as JSON. Copy summary into [GPU_PILOT_COST_MODEL.md](../docs/05-architecture/GPU_PILOT_COST_MODEL.md).

## Policy

Per ADR-0006: **dev workstation only** — not deployed to classroom smartboards.
