# claude-kb — a self-growing knowledge base from your Claude usage

Turn every Claude session — CLI and app — into a rolling record of *what you
built and learned*: tools used, files touched, decisions made, errors hit,
recurring themes. New sessions append automatically; you never start from a
blank page.

## The honest constraints (read this first)

This design is shaped by what's actually reachable, not what we'd wish for:

| Source | Can it be automated? | How it gets in |
| --- | --- | --- |
| **Claude Code CLI** (local) | ✅ Yes | A `SessionEnd` hook distills each session automatically. |
| **Claude Code on the web** | ⚠️ Per-repo | Containers are ephemeral, so the hook must **push to a repo** before the container recycles. Add the hook to each repo you care about. |
| **claude.ai app** | ❌ No live access | No API exists. You periodically run **Settings → Privacy → Export data**, then feed the `conversations.json` to the ingester. |

There is no way to "scrape all history" in one shot — the app has no API, and
CLI transcripts only exist on the machine that ran them. What this system does
instead is **capture forward, from now on**, and let you backfill the app
manually whenever you export.

> **Privacy:** entries contain your prompts and Claude's replies. Point the KB
> at a **private** repo. Do not use a public repo (like a profile repo) as the
> live target.

## What's here

```
claude-kb/
├── scripts/
│   ├── distill_session.py   # one CLI transcript  → structured entry (.json + .md)
│   ├── ingest_app_export.py # claude.ai export     → entries
│   └── synthesize.py        # all entries          → KNOWLEDGE.md digest
├── hooks/
│   └── on_session_end.sh    # the automation: distill + synthesize + commit/push
├── settings/
│   ├── user-settings-hook.json    # global hook (local, every session)
│   └── project-settings.json      # per-repo hook (web / specific projects)
├── entries/                 # append-only, one file per session (the raw record)
└── KNOWLEDGE.md             # the compiled, human-readable digest
```

## How it works

1. **Distill** — `distill_session.py` parses a session's JSONL transcript and
   pulls out the signal: prompts (topics), tool-use counts, files touched, bash
   commands, errors surfaced back to the model, and the assistant's own summary
   text (where "what we learned" lives). Deterministic, no LLM, zero cost.
2. **Ingest** (app) — `ingest_app_export.py` does the same for conversations in
   a claude.ai data export. The export schema drifts over time, so the parser is
   defensive about field names.
3. **Synthesize** — `synthesize.py` aggregates every entry into `KNOWLEDGE.md`:
   an at-a-glance summary, a tool leaderboard, recurring themes, and a
   newest-first timeline. Pass `--llm` to additionally have headless
   `claude -p` write a narrative "what we learned" section.
4. **Automate** — `on_session_end.sh` chains distill → synthesize → git
   commit/push. Wire it to the `SessionEnd` hook and it runs itself. It is
   best-effort and always exits 0, so it can never block a session.

## Setup

### 1. Put this in a private repo
Move `claude-kb/` into (or clone it as) a **private** repo, then note its
absolute path — call it `$KB`.

### 2. Local CLI — capture every session automatically
Merge `settings/user-settings-hook.json` into `~/.claude/settings.json`, setting
`CLAUDE_KB_DIR` to `$KB`. Every local session now distills itself on exit and
pushes to the repo.

### 3. Claude Code on the web — capture per repo
In each repo you work in on the web, commit `settings/project-settings.json` as
that repo's `.claude/settings.json`, with `CLAUDE_KB_DIR` pointing at a checkout
of your KB repo and `CLAUDE_KB_PUSH=1` (mandatory on the web — the container is
wiped, so an un-pushed entry is lost).

### 4. App — periodic backfill
When you want app history in, export from **claude.ai → Settings → Privacy →
Export data**, then:

```sh
python3 $KB/scripts/ingest_app_export.py path/to/conversations.json --out-dir $KB/entries
python3 $KB/scripts/synthesize.py --entries-dir $KB/entries --out $KB/KNOWLEDGE.md
```

`--since YYYY-MM-DD` limits ingestion to recent conversations so re-exports stay cheap.

## Manual / on-demand use

Capture the current session yourself without waiting for the hook:

```sh
# newest transcript for the current project
T=$(ls -t ~/.claude/projects/*/*.jsonl | head -n1)
python3 scripts/distill_session.py "$T" --out-dir entries
python3 scripts/synthesize.py --entries-dir entries --out KNOWLEDGE.md --llm
```

## Configuration (env vars read by the hook)

| Variable | Default | Meaning |
| --- | --- | --- |
| `CLAUDE_KB_DIR` | this repo | Local knowledge-base checkout. |
| `CLAUDE_KB_PUSH` | `1` | Commit + push after each capture. |
| `CLAUDE_KB_LLM` | `0` | Also generate the LLM narrative via `claude -p`. |
