#!/usr/bin/env bash
# End-to-end benchmark runner. S01-09
# Usage: ./bench_full_pipeline.sh [cpu|gpu]
#   cpu  — works without NVIDIA GPU (default; use until RTX 5070 available)
#   gpu  — full RTX 5070 / CUDA sizing run (tomorrow on founder machine)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

PROFILE="${1:-cpu}"
if [[ "$PROFILE" != "cpu" && "$PROFILE" != "gpu" ]]; then
  echo "Usage: $0 [cpu|gpu]"
  exit 1
fi

echo "=== PedagogyX benchmark suite (profile: $PROFILE) ==="
date -u

if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
  DEVICE="${BENCH_DEVICE:-cuda}"
else
  echo "INFO: No NVIDIA GPU — using CPU profile (valid for dev until RTX 5070)"
  DEVICE="cpu"
  if [[ "$PROFILE" == "gpu" ]]; then
    echo "WARN: gpu profile requested but no GPU found; falling back to cpu"
    PROFILE="cpu"
  fi
fi

mkdir -p results

VENV="$ROOT/.venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "Creating venv at $VENV ..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -r requirements-bench.txt
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

run() {
  echo "--- $*"
  if "$@"; then
    echo "OK: $*"
  else
    echo "SKIP/FAIL: $* (non-fatal)"
  fi
}

if [[ "$PROFILE" == "cpu" ]]; then
  # Fast enough on laptop/cloud VM without GPU
  run python bench_whisper.py --model small --device "$DEVICE" --duration-sec 30
  run python bench_whisper.py --model medium --device "$DEVICE" --duration-sec 60
  run python bench_yolo_trt.py --device "$DEVICE" --height 480 --width 854 --frames 50
  export BENCH_OLLAMA_MODEL="${BENCH_OLLAMA_MODEL:-llama3.2:1b}"
  run python bench_ollama.py --model "$BENCH_OLLAMA_MODEL"
else
  # Full sizing run for RTX 5070 (12 GB)
  run python bench_whisper.py --model medium --device "$DEVICE" --duration-sec 120
  run python bench_whisper.py --model large-v3 --device "$DEVICE" --duration-sec 120
  run python bench_yolo_trt.py --device "$DEVICE" --height 480 --width 854 --frames 200
  run python bench_yolo_trt.py --device "$DEVICE" --height 720 --width 1280 --frames 100
  export BENCH_OLLAMA_MODEL="${BENCH_OLLAMA_MODEL:-qwen2.5:7b-instruct-q4_K_M}"
  run python bench_ollama.py --model "$BENCH_OLLAMA_MODEL"
fi

echo "profile=$PROFILE" > results/last_profile.txt
echo "device=$DEVICE" >> results/last_profile.txt

if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader >> results/nvidia-smi-snapshot.txt
fi

echo "=== Done ($PROFILE). Results in $ROOT/results/ ==="
echo "Tomorrow on RTX 5070: ./bench_full_pipeline.sh gpu"
