#!/usr/bin/env bash
# Verify dev environment without RTX 5070. Exit 0 = OK for CPU dev today.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== PedagogyX dev-verify (CPU OK) ==="

echo "--- markdownlint ---"
npx --yes markdownlint-cli 'docs/**/*.md'

echo "--- prettier check ---"
npx --yes prettier --check 'docs/**/*.md'

echo "--- benchmarks (cpu profile) ---"
if ! command -v ollama >/dev/null 2>&1; then
  echo "WARN: ollama not installed; LLM step may skip (see benchmarks/DEV_WITHOUT_GPU.md)"
elif ! curl -sf http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  echo "Starting ollama serve in background..."
  ollama serve >/tmp/ollama-dev-verify.log 2>&1 &
  sleep 2
fi

cd benchmarks
./bench_full_pipeline.sh cpu

echo "=== dev-verify PASSED ==="
echo "Tomorrow on RTX 5070: cd benchmarks && ./bench_full_pipeline.sh gpu"
