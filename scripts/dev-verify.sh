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
npx --yes markdownlint-cli \
  'docs/**/*.md' 'README.md' 'DEVELOPING.md' 'AGENTS.md' \
  'infra/README.md' 'services/README.md' \
  'services/api/README.md' 'services/web/README.md' 'services/worker-asr/README.md' 'services/worker-cv/README.md' \
  'packages/capture-core/README.md' 'tools/mock-capture/README.md' \
  --ignore '**/node_modules/**'

echo "--- prettier check ---"
npx --yes prettier --check \
  'docs/**/*.md' 'README.md' 'DEVELOPING.md' 'AGENTS.md' \
  'infra/README.md' 'services/README.md' \
  'services/api/README.md' 'services/web/README.md' 'services/worker-asr/README.md' 'services/worker-cv/README.md' \
  'packages/capture-core/README.md' 'tools/mock-capture/README.md'

echo "--- python linting (black, isort, flake8) ---"

get_linter_cmd() {
  local cmd=$1
  if [ -x "benchmarks/.venv/bin/$cmd" ]; then
    echo "benchmarks/.venv/bin/$cmd"
  elif command -v "$cmd" >/dev/null 2>&1; then
    echo "$cmd"
  else
    echo ""
  fi
}

BLACK_CMD=$(get_linter_cmd "black")
ISORT_CMD=$(get_linter_cmd "isort")
FLAKE8_CMD=$(get_linter_cmd "flake8")

if [ -n "$BLACK_CMD" ] && [ -n "$ISORT_CMD" ] && [ -n "$FLAKE8_CMD" ]; then
  $BLACK_CMD --check --line-length=100 benchmarks/*.py
  $ISORT_CMD --check-only --profile black --line-length=100 benchmarks/*.py
  $FLAKE8_CMD --max-line-length=100 benchmarks/*.py
else
  echo "WARN: Python linters (black, isort, flake8) not fully found. Skipping benchmark Python linting."
  echo "To run python linting: cd benchmarks && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-bench.txt"
fi

echo "--- ruff (services/tools) ---"
if command -v ruff >/dev/null 2>&1; then
  ruff check services tools packages/capture-core/py
elif python3 -m ruff --version >/dev/null 2>&1; then
  python3 -m ruff check services tools packages/capture-core/py
else
  pip install -q ruff
  python3 -m ruff check services tools packages/capture-core/py
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
