#!/usr/bin/env bash
# Smoke-test dev Compose stack (requires Docker).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "SKIP: docker not installed"
  exit 0
fi

COMPOSE_FILE="infra/compose.dev.yaml"

echo "=== compose-smoke: up ==="
docker compose -f "$COMPOSE_FILE" up -d --build --wait

echo "=== compose-smoke: API health ==="
curl -sf http://localhost:8080/health | tee /tmp/pedagogyx-health.json
echo

echo "=== compose-smoke: create session ==="
SESSION_JSON=$(curl -sf -X POST http://localhost:8080/v1/sessions \
  -H 'Content-Type: application/json' \
  -d '{"school_id":"smoke-test","room_id":"1","teacher_id":"t1"}')
echo "$SESSION_JSON"
SESSION_ID=$(echo "$SESSION_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")

echo "=== compose-smoke: upload chunk ==="
CHUNK_FILE=$(mktemp)
dd if=/dev/zero of="$CHUNK_FILE" bs=1024 count=1 2>/dev/null
curl -sf -X POST "http://localhost:8080/v1/sessions/${SESSION_ID}/chunks/0" \
  -F "file=@${CHUNK_FILE};filename=chunk0.bin"
rm -f "$CHUNK_FILE"

curl -sf -X POST "http://localhost:8080/v1/sessions/${SESSION_ID}/complete" >/dev/null
echo "Session completed: $SESSION_ID"

echo "=== compose-smoke: wait for preview ==="
for i in $(seq 1 45); do
  PREVIEW=$(curl -sf "http://localhost:8080/v1/sessions/${SESSION_ID}/preview" || true)
  if echo "$PREVIEW" | grep -q '"preview_ready": true'; then
    echo "$PREVIEW"
    break
  fi
  sleep 1
done

curl -sf "http://localhost:8080/v1/schools/smoke-test/overview" | head -c 500
echo

echo "=== compose-smoke: web (optional) ==="
if curl -sf http://localhost:3000/ >/dev/null; then
  echo "Web OK"
else
  echo "WARN: web not ready (may still be building)"
fi

echo "=== compose-smoke: down ==="
docker compose -f "$COMPOSE_FILE" down

echo "=== compose-smoke PASSED ==="
