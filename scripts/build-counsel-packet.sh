#!/usr/bin/env bash
# Build a counsel attachment bundle (Markdown docs only). S02-01 helper.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist"
STAMP="$(date -u +%Y%m%d)"
ARCHIVE="$OUT/pedagogyx-counsel-packet-${STAMP}.tar.gz"

mkdir -p "$OUT"

FILES=(
  docs/07-compliance-ethics/INDIA_DPDP_COUNSEL_ENGAGEMENT_BRIEF.md
  docs/07-compliance-ethics/INDIA_DPDP_ARCHITECTURE.md
  docs/07-compliance-ethics/ETHICAL_FRAMEWORK.md
  docs/07-compliance-ethics/COMPLIANCE_ANALYSIS.md
  docs/10-risks/THREAT_MODEL_STRIDE_v0.1.md
  docs/01-phase0-founder-interrogation/FOUNDER_ANSWERS.md
  docs/08-rfc-adr/RFC-0002-capture-agent-sync-protocol.md
  docs/02-product/ADMIN_LIVE_DASHBOARD_WIREFRAMES.md
  docs/02-product/PRD-v0.1-draft.md
  docs/08-rfc-adr/ADR-0008-d-proc-hybrid-central-ml.md
)

cd "$ROOT"
tar -czf "$ARCHIVE" "${FILES[@]}"
echo "Created: $ARCHIVE"
echo "Attach to counsel email with COUNSEL_OUTREACH_PACKAGE.md cover note."
