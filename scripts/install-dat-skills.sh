#!/usr/bin/env bash
# Install Meta Wearables DAT agent skills (Cursor, Claude, Codex, etc.)
# Upstream: https://github.com/facebook/meta-wearables-dat-android
set -euo pipefail

TARGET="${1:-cursor}"
URL="https://raw.githubusercontent.com/facebook/meta-wearables-dat-android/main/install-skills.sh"

echo "Fetching Meta install-skills.sh and running: $TARGET"
curl -fsSL "$URL" | bash -s -- "$TARGET"
