# Usage & Tips

Direct, practical notes for running Nexus day-to-day. Not exhaustive — see `master-plan.md` for the plan, `decision-log.md` for the why.

## Reference the plan from any chat

- Local agents (Claude Code, Codex): point them at `docs/master-plan.md`.
- Cloud agents (claude.ai, ChatGPT): say **"search nexus master plan"** — they retrieve the brain mirror.

## Capture a source (reel / post / article)

Say **"capture this"** (or "capture these") to any agent and give the content in any form: paste a caption, paste a transcript, drop a screenshot (for text-in-video or photo posts), and/or a URL. The agent extracts, writes a `Summary:`, files it in the right `raw/sources/...` folder, and it syncs into the brain within ~5 min. Batch several at once. (Not automatic from Instagram — you provide the content; it handles every type. Spec: `docs/workflows/capture-pipeline.md`.)

## Weekly checklist

- **"refresh my \<area\> backlog"** → builds/updates `wiki/areas/<area>/backlog.md` from your resources.
- **"generate my weekly checklist"** → `wiki/weekly/<year>-W<week>.md` (the one page to open weekly).
- **"mark \<item\> done"** → moves it to Done.

Spec: `docs/workflows/weekly-checklist-engine.md`.

## Force a brain sync now

The vault syncs into the brain every 5 min automatically. To sync immediately after editing notes:

```sh
launchctl kickstart -k gui/$(id -u)/com.nexus.brain-sync
tail -f /tmp/nexus-brain-sync.out    # watch it
```

## Manage the services

```sh
# status (PID | last exit)
launchctl list | grep -E 'com.nexus|ollama|postgres'

# restart the cloud connector (serve --http + ngrok)
launchctl kickstart -k gui/$(id -u)/com.nexus.claude-chat-gbrain

# logs
tail -f /tmp/nexus-gbrain-http.log /tmp/nexus-ngrok.log /tmp/nexus-brain-sync.out

# stop / start a service
launchctl unload -w ~/Library/LaunchAgents/<label>.plist
launchctl load   -w ~/Library/LaunchAgents/<label>.plist
```

Services: `postgresql@17`, `ollama`, `com.nexus.claude-chat-gbrain`, `com.nexus.brain-sync`.

## Quick brain checks

```sh
gbrain stats                 # page/chunk counts, engine
gbrain search "<query>"      # keyword
gbrain query "<question>"    # hybrid (semantic + keyword)
gbrain doctor                # health
```

## If the brain won't start (PGLite legacy recovery)

The brain runs on Postgres now (crash-safe), but if you ever hit a crashed **PGLite** dir (`... WASM ... Aborted()`):

```sh
# stop everything touching it, then:
pg_resetwal -f -D ~/.gbrain/brain.pglite     # needs postgresql@17; clears crashed WAL, no data loss
```

Prefer stopping servers gracefully (`launchctl unload`), never `kill -9` a PGLite server.

## Gotchas

- Claude Code MCP config lives in `~/.claude.json` (`mcpServers`), **not** `~/.claude/settings.json`. Restart Claude Code after changes.
- Cloud agents are **read-only** — they'll show write tools but the server refuses them. Writes happen via local agents or by editing the vault.
- `scripts/tunnel.env` (your ngrok domain) and the vault are never committed.
- ngrok free shows a one-time "Visit Site" interstitial during the OAuth browser step only.
