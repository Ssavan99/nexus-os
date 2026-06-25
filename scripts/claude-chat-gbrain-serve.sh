#!/usr/bin/env bash
#
# Phase 2D.2 — always-on GBrain read-only HTTP MCP for claude.ai over an ngrok
# STATIC domain. Designed to be run by launchd (KeepAlive), but also runnable by
# hand for testing. Starts `gbrain serve --http` (DCR off, bound to localhost)
# and an ngrok tunnel pinned to your reserved static domain, then waits; if
# either child dies it tears both down and exits so launchd restarts cleanly.
#
# Config: create scripts/tunnel.env (gitignored) with:
#     STABLE_DOMAIN=your-name.ngrok-free.app
# The ngrok authtoken must already be configured (`ngrok config add-authtoken …`).

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
[[ -f "$HERE/tunnel.env" ]] && source "$HERE/tunnel.env"

GBRAIN="${GBRAIN_BIN:-/Users/ssavan99/.bun/bin/gbrain}"
NGROK="${NGROK_BIN:-/opt/homebrew/bin/ngrok}"
PORT="${PORT:-3131}"
: "${STABLE_DOMAIN:?Set STABLE_DOMAIN in scripts/tunnel.env (e.g. your-name.ngrok-free.app)}"
PUBLIC_URL="https://${STABLE_DOMAIN}"
GB_LOG="${GB_LOG:-/tmp/nexus-gbrain-http.log}"
NG_LOG="${NG_LOG:-/tmp/nexus-ngrok.log}"

cleanup() {
  [[ -n "${GB_PID:-}" ]] && kill "$GB_PID" 2>/dev/null || true
  [[ -n "${NG_PID:-}" ]] && kill "$NG_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "[$(date)] starting gbrain serve --http (issuer $PUBLIC_URL)"
"$GBRAIN" serve --http --port "$PORT" --bind 127.0.0.1 --public-url "$PUBLIC_URL" >"$GB_LOG" 2>&1 &
GB_PID=$!

echo "[$(date)] starting ngrok on static domain $STABLE_DOMAIN -> localhost:$PORT"
"$NGROK" http "--domain=${STABLE_DOMAIN}" "$PORT" --log stdout >"$NG_LOG" 2>&1 &
NG_PID=$!

# If either process exits, stop the other so launchd recycles the whole unit.
# (macOS /bin/bash is 3.2 with no `wait -n`, so poll both PIDs instead.)
while kill -0 "$GB_PID" 2>/dev/null && kill -0 "$NG_PID" 2>/dev/null; do
  sleep 5
done
echo "[$(date)] a child exited; shutting down the other and letting launchd restart"
