#!/usr/bin/env bash
#
# Phase 2D — bring up GBrain's read-only HTTP MCP behind a Cloudflare quick tunnel
# for the claude.ai custom connector. Run this in YOUR OWN terminal and leave it
# running while you use the connector (Ctrl-C to stop everything).
#
# It starts the tunnel first (to learn the public URL), then starts
# `gbrain serve --http` with --public-url set to that URL, and prints the
# connector URL to paste into claude.ai.
#
# Auth model: DCR stays OFF. A pre-registered read-scoped public (PKCE) client
# is used. Paste its Client ID into claude.ai's connector "OAuth Client ID"
# field (leave Client Secret empty).
#
# NOTE: trycloudflare URLs are random and change every run. For an always-on
# stable URL, switch to a named Cloudflare tunnel (needs a domain) — see
# docs/claude-chat-gbrain-plan.md (stage 2D.2).

set -euo pipefail

GBRAIN="${GBRAIN_BIN:-/Users/ssavan99/.bun/bin/gbrain}"
PORT="${PORT:-3131}"
# Fixed log paths so the assistant can read them for debugging.
CF_LOG="/tmp/nexus-cf.log"
GB_LOG="/tmp/nexus-gbrain-http.log"

cleanup() {
  echo
  echo "Shutting down tunnel + server..."
  [[ -n "${CF_PID:-}" ]] && kill "$CF_PID" 2>/dev/null || true
  [[ -n "${GB_PID:-}" ]] && kill "$GB_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Starting Cloudflare quick tunnel -> http://localhost:${PORT} ..."
cloudflared tunnel --url "http://localhost:${PORT}" >"$CF_LOG" 2>&1 &
CF_PID=$!

# Wait for the public URL to appear in the tunnel log.
URL=""
for _ in $(seq 1 30); do
  URL="$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' "$CF_LOG" | head -1 || true)"
  [[ -n "$URL" ]] && break
  sleep 1
done
if [[ -z "$URL" ]]; then
  echo "ERROR: tunnel URL not found. Tunnel log:"; cat "$CF_LOG"; exit 1
fi
echo "Tunnel URL: $URL"

echo "Starting gbrain serve --http (DCR off) with issuer $URL ..."
"$GBRAIN" serve --http --port "$PORT" --bind 127.0.0.1 --public-url "$URL" >"$GB_LOG" 2>&1 &
GB_PID=$!
echo "Server log: $GB_LOG  |  Tunnel log: $CF_LOG"

# Wait for health via the tunnel.
for _ in $(seq 1 20); do
  if curl -fsS -o /dev/null "$URL/health" 2>/dev/null; then break; fi
  sleep 1
done

cat <<EOF

============================================================
  GBrain read-only connector is LIVE (leave this running)
============================================================
  Paste this into claude.ai -> Add custom connector -> URL:

      $URL/mcp

  Then in the connector's Advanced / OAuth section:
    - OAuth Client ID: <your read-only client id>
    - Client Secret:   (leave empty — public PKCE client)

  Ctrl-C here stops the tunnel and server.
============================================================
EOF

wait
