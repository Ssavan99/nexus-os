#!/usr/bin/env bash
#
# Nexus v1 — keep the GBrain brain in sync with the Obsidian vault (no git).
# Idempotent: `gbrain import` upserts by slug and skips unchanged pages
# (content-hash short-circuit), so re-running is cheap. Then embed + extract
# only what changed. Runs under launchd on an interval (see
# scripts/com.nexus.brain-sync.plist), or by hand.
#
# Config: set VAULT_PATH in the environment to override the default.

set -euo pipefail

GBRAIN="${GBRAIN_BIN:-/Users/ssavan99/.bun/bin/gbrain}"
VAULT="${VAULT_PATH:-/Users/ssavan99/Desktop/Personal-Obsidian}"

if [[ ! -d "$VAULT" ]]; then
  echo "[$(date)] vault not found: $VAULT" >&2
  exit 1
fi

echo "[$(date)] import $VAULT -> brain"
"$GBRAIN" import "$VAULT"

echo "[$(date)] embed stale chunks (local Ollama)"
"$GBRAIN" embed --stale || echo "[$(date)] embed step non-fatal error (Ollama down?)"

echo "[$(date)] extract stale links/timeline"
"$GBRAIN" extract --stale || echo "[$(date)] extract step non-fatal error"

echo "[$(date)] brain sync done"
