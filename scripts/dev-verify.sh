#!/usr/bin/env bash
# Verify dev environment. CPU benchmarks optional (no RTX 5070 required for --docs-only).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

DOCS_ONLY=false
for arg in "$@"; do
  case "$arg" in
    --docs-only) DOCS_ONLY=true ;;
    -h | --help)
      echo "Usage: $0 [--docs-only]"
      echo "  --docs-only   markdownlint + prettier (CI-friendly)"
      echo "  (default)     docs + benchmarks cpu profile"
      exit 0
      ;;
  esac
done

echo "=== PedagogyX dev-verify ==="

echo "--- markdownlint ---"
npx --yes markdownlint-cli '**/*.md' --ignore node_modules

echo "--- prettier check ---"
npx --yes prettier --check '**/*.md' --ignore-path .gitignore

echo "--- python linting (black, isort, flake8) ---"
VENV_BIN="benchmarks/.venv/bin"
if [[ -x "$VENV_BIN/black" && -x "$VENV_BIN/isort" && -x "$VENV_BIN/flake8" ]]; then
  "$VENV_BIN/black" --check --line-length=100 benchmarks/*.py
  "$VENV_BIN/isort" --check-only --profile black --line-length=100 benchmarks/*.py
  "$VENV_BIN/flake8" --max-line-length=100 benchmarks/*.py
elif command -v black >/dev/null 2>&1; then
  black --check --line-length=100 benchmarks/*.py
  isort --check-only --profile black --line-length=100 benchmarks/*.py
  flake8 --max-line-length=100 benchmarks/*.py
else
  echo "WARN: Python linters (black, isort, flake8) not found. Skipping Python linting."
  echo "To run python linting locally, run: pip install -r benchmarks/requirements-bench.txt"
fi

if [[ "$DOCS_ONLY" == true ]]; then
  echo "=== dev-verify PASSED (docs only) ==="
  exit 0
fi

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
