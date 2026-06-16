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

echo "=== compose-smoke: wait for API to be fully ready ==="
for i in $(seq 1 30); do
  if curl --retry 5 --retry-connrefused --retry-delay 2 -sf http://localhost:8080/health >/dev/null; then
    echo "API is ready!"
    break
  fi
  echo "Waiting for API... $i/30"
  sleep 2
done

echo "=== compose-smoke: API health ==="
curl --retry 5 --retry-connrefused --retry-delay 2 -sf http://localhost:8080/health | tee /tmp/pedagogyx-health.json
echo

echo "=== compose-smoke: create session ==="
SESSION_JSON=$(curl --retry 5 --retry-connrefused --retry-delay 2 -sf -X POST http://localhost:8080/v1/sessions \
  -H 'Authorization: Bearer dev_api_key_placeholder' \
  -H 'Content-Type: application/json' \
  -d '{"school_id":"smoke-test","room_id":"1","teacher_id":"t1"}')
echo "$SESSION_JSON"
SESSION_ID=$(echo "$SESSION_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")

echo "=== compose-smoke: upload chunk ==="
CHUNK_FILE=$(mktemp)
dd if=/dev/zero of="$CHUNK_FILE" bs=1024 count=1 2>/dev/null
curl --retry 5 --retry-connrefused --retry-delay 2 -sf -X POST "http://localhost:8080/v1/sessions/${SESSION_ID}/chunks/0" \
  -H 'Authorization: Bearer dev_api_key_placeholder' \
  -F "file=@${CHUNK_FILE};filename=chunk0.bin"
rm -f "$CHUNK_FILE"

curl --retry 5 --retry-connrefused --retry-delay 2 -sf -H 'Authorization: Bearer dev_api_key_placeholder' -X POST "http://localhost:8080/v1/sessions/${SESSION_ID}/complete" >/dev/null
echo "Session completed: $SESSION_ID"

echo "=== compose-smoke: wait for preview ==="
for i in $(seq 1 45); do
  PREVIEW=$(curl --retry 5 --retry-connrefused --retry-delay 2 -sf -H 'Authorization: Bearer dev_api_key_placeholder' "http://localhost:8080/v1/sessions/${SESSION_ID}/preview" || true)
  if echo "$PREVIEW" | grep -q '"preview_ready": true'; then
    echo "$PREVIEW"
    break
  fi
  sleep 1
done

curl --retry 5 --retry-connrefused --retry-delay 2 -sf -H 'Authorization: Bearer dev_api_key_placeholder' "http://localhost:8080/v1/schools/smoke-test/overview" | head -c 500
echo

echo "=== compose-smoke: web (optional) ==="
if curl --retry 5 --retry-connrefused --retry-delay 2 -sf http://localhost:3000/ >/dev/null; then
  echo "Web OK"
else
  echo "WARN: web not ready (may still be building)"
fi

echo "=== compose-smoke: down ==="
docker compose -f "$COMPOSE_FILE" down

echo "=== compose-smoke PASSED ==="
