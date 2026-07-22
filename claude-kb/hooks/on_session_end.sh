#!/usr/bin/env bash
#
# Claude Code SessionEnd / Stop hook: distill the finished session into the
# knowledge base and (optionally) commit + push it.
#
# Wire it up in settings.json (see claude-kb/settings/). Claude Code passes the
# hook a JSON object on stdin that includes `transcript_path`, `session_id`,
# and `cwd`. We read that, distill the transcript, regenerate KNOWLEDGE.md, and
# persist. The hook is deliberately best-effort and ALWAYS exits 0 so it can
# never block or fail a session.
#
# Config via environment:
#   CLAUDE_KB_DIR    Path to your local knowledge-base checkout.
#                    Defaults to the repo this script lives in.
#   CLAUDE_KB_PUSH   If "1", git add/commit/push after updating (default: 1).
#   CLAUDE_KB_LLM    If "1", also generate the LLM narrative (default: 0).
#
set -u

log() { printf '[claude-kb] %s\n' "$*" >&2; }

# --- Resolve the knowledge-base directory -----------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KB_DIR="${CLAUDE_KB_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
SCRIPTS="$KB_DIR/scripts"
ENTRIES="$KB_DIR/entries"
OUT="$KB_DIR/KNOWLEDGE.md"
PUSH="${CLAUDE_KB_PUSH:-1}"
USE_LLM="${CLAUDE_KB_LLM:-0}"

mkdir -p "$ENTRIES"

# --- Read hook payload from stdin -------------------------------------------
PAYLOAD="$(cat 2>/dev/null || true)"
TRANSCRIPT=""
if [ -n "$PAYLOAD" ]; then
  TRANSCRIPT="$(printf '%s' "$PAYLOAD" | python3 -c \
    'import sys,json;
try:
    print(json.load(sys.stdin).get("transcript_path",""))
except Exception:
    print("")' 2>/dev/null)"
fi

# Fallback: newest transcript under ~/.claude/projects
if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
  TRANSCRIPT="$(ls -t "$HOME"/.claude/projects/*/*.jsonl 2>/dev/null | head -n1)"
fi

if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
  log "no transcript found; nothing to distill"
  exit 0
fi

# --- Distill + synthesize ----------------------------------------------------
if ! python3 "$SCRIPTS/distill_session.py" "$TRANSCRIPT" --out-dir "$ENTRIES" >/dev/null 2>&1; then
  log "distill failed for $TRANSCRIPT"
  exit 0
fi

SYN_ARGS=(--entries-dir "$ENTRIES" --out "$OUT")
[ "$USE_LLM" = "1" ] && SYN_ARGS+=(--llm)
python3 "$SCRIPTS/synthesize.py" "${SYN_ARGS[@]}" >/dev/null 2>&1 || log "synthesize warning"

log "knowledge base updated from $(basename "$TRANSCRIPT")"

# --- Persist -----------------------------------------------------------------
if [ "$PUSH" = "1" ] && [ -d "$KB_DIR/.git" ]; then
  (
    cd "$KB_DIR" || exit 0
    git add entries KNOWLEDGE.md >/dev/null 2>&1 || exit 0
    if ! git diff --cached --quiet 2>/dev/null; then
      git commit -m "kb: capture session $(basename "$TRANSCRIPT" .jsonl | cut -c1-8)" >/dev/null 2>&1
      for attempt in 1 2 3 4; do
        if git push >/dev/null 2>&1; then
          log "pushed knowledge base update"
          break
        fi
        sleep $((attempt * 2))
      done
    fi
  )
fi

exit 0
