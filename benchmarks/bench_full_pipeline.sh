#!/usr/bin/env bash
# End-to-end dev benchmark runner. S01-09
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "=== PedagogyX RTX 5070 benchmark suite ==="
date -u

if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
else
  echo "WARN: nvidia-smi not found — GPU benchmarks may fall back to CPU or skip"
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

run python bench_whisper.py --model medium --duration-sec 120
run python bench_whisper.py --model large-v3 --duration-sec 120
run python bench_yolo_trt.py --height 480 --width 854 --frames 200
run python bench_yolo_trt.py --height 720 --width 1280 --frames 100
run python bench_ollama.py

if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader >> results/nvidia-smi-snapshot.txt
fi

echo "=== Done. Results in $ROOT/results/ ==="
