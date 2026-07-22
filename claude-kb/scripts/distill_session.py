#!/usr/bin/env python3
"""
Distill a single Claude Code session transcript (JSONL) into a structured
"learning entry": what the session was about, which tools/files/commands were
used, decisions made, and errors hit. Deterministic, no LLM required.

Usage:
    distill_session.py TRANSCRIPT.jsonl [--out-dir DIR] [--print]

If --out-dir is given, writes two files:
    DIR/<session-id>.json   machine-readable entry
    DIR/<session-id>.md     human-readable entry
Otherwise prints the markdown to stdout.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone


# Text that is noise for "what did we learn" purposes: slash-command plumbing,
# system reminders, caveats injected by the harness, etc.
_NOISE_PATTERNS = [
    re.compile(r"<local-command-caveat>.*?</local-command-caveat>", re.S),
    re.compile(r"<command-name>.*?</command-name>", re.S),
    re.compile(r"<command-message>.*?</command-message>", re.S),
    re.compile(r"<command-args>.*?</command-args>", re.S),
    re.compile(r"<local-command-stdout>.*?</local-command-stdout>", re.S),
    re.compile(r"<system-reminder>.*?</system-reminder>", re.S),
    re.compile(r"<bash-input>.*?</bash-input>", re.S),
    re.compile(r"<bash-stdout>.*?</bash-stdout>", re.S),
    re.compile(r"<bash-stderr>.*?</bash-stderr>", re.S),
]


def _clean(text: str) -> str:
    for pat in _NOISE_PATTERNS:
        text = pat.sub("", text)
    return text.strip()


def _iter_records(path: str):
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def _content_blocks(rec: dict):
    """Yield content blocks from a user/assistant record, normalizing shapes."""
    msg = rec.get("message", {})
    content = msg.get("content")
    if isinstance(content, str):
        yield {"type": "text", "text": content}
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                yield block


def distill(path: str) -> dict:
    session_id = None
    cwd = None
    git_branch = None
    version = None
    first_ts = None
    last_ts = None
    models = set()

    user_prompts: list[str] = []
    assistant_texts: list[str] = []
    tool_counts: Counter = Counter()
    bash_commands: list[str] = []
    files_touched: set[str] = set()
    errors: list[str] = []

    for rec in _iter_records(path):
        session_id = session_id or rec.get("sessionId")
        cwd = cwd or rec.get("cwd")
        git_branch = git_branch or rec.get("gitBranch")
        version = version or rec.get("version")
        ts = rec.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts

        rtype = rec.get("type")
        msg = rec.get("message", {}) if isinstance(rec.get("message"), dict) else {}
        if msg.get("model"):
            models.add(msg["model"])

        if rtype == "user":
            for block in _content_blocks(rec):
                if block.get("type") == "text":
                    cleaned = _clean(block.get("text", ""))
                    # Skip empty-after-cleaning (pure command/system plumbing).
                    if cleaned and len(cleaned) > 1:
                        user_prompts.append(cleaned)
                elif block.get("type") == "tool_result":
                    # Detect errors surfaced back to the model.
                    if block.get("is_error"):
                        payload = block.get("content", "")
                        if isinstance(payload, list):
                            payload = " ".join(
                                b.get("text", "") for b in payload if isinstance(b, dict)
                            )
                        snippet = _clean(str(payload))[:200]
                        if snippet:
                            errors.append(snippet)

        elif rtype == "assistant":
            for block in _content_blocks(rec):
                btype = block.get("type")
                if btype == "text":
                    cleaned = _clean(block.get("text", ""))
                    if cleaned:
                        assistant_texts.append(cleaned)
                elif btype == "tool_use":
                    name = block.get("name", "unknown")
                    tool_counts[name] += 1
                    inp = block.get("input", {}) or {}
                    if name == "Bash" and inp.get("command"):
                        bash_commands.append(inp["command"].strip())
                    for key in ("file_path", "path", "notebook_path"):
                        if inp.get(key):
                            files_touched.add(inp[key])

    def _fmt(ts):
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00")).isoformat()
        except (ValueError, AttributeError):
            return ts

    entry = {
        "schema": 1,
        "source": "cli",
        "session_id": session_id,
        "transcript_path": os.path.abspath(path),
        "cwd": cwd,
        "git_branch": git_branch,
        "cli_version": version,
        "models": sorted(models),
        "started_at": _fmt(first_ts),
        "ended_at": _fmt(last_ts),
        "distilled_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            "user_prompts": len(user_prompts),
            "assistant_messages": len(assistant_texts),
            "tool_calls": sum(tool_counts.values()),
        },
        "tools_used": dict(tool_counts.most_common()),
        "topics": user_prompts,
        "bash_commands": bash_commands,
        "files_touched": sorted(files_touched),
        "errors": errors,
        # Highlights = the assistant's own summary text, which is where the
        # "what we learned / decided" content actually lives.
        "highlights": assistant_texts,
    }
    return entry


def _first_line(text: str, limit: int = 100) -> str:
    line = text.strip().splitlines()[0] if text.strip() else ""
    return (line[:limit] + "…") if len(line) > limit else line


def to_markdown(entry: dict) -> str:
    lines: list[str] = []
    date = (entry.get("started_at") or entry.get("distilled_at") or "")[:10]
    lines.append(f"## Session {entry.get('session_id','?')[:8]} — {date}")
    lines.append("")
    meta = []
    if entry.get("cwd"):
        meta.append(f"**Project:** `{entry['cwd']}`")
    if entry.get("git_branch"):
        meta.append(f"**Branch:** `{entry['git_branch']}`")
    if entry.get("models"):
        meta.append(f"**Model(s):** {', '.join(entry['models'])}")
    if meta:
        lines.append("  ".join(meta))
        lines.append("")

    if entry.get("topics"):
        lines.append("### What was asked")
        for t in entry["topics"]:
            lines.append(f"- {_first_line(t, 160)}")
        lines.append("")

    if entry.get("tools_used"):
        lines.append("### Tools used")
        tu = ", ".join(f"`{k}`×{v}" for k, v in entry["tools_used"].items())
        lines.append(tu)
        lines.append("")

    if entry.get("files_touched"):
        lines.append("### Files touched")
        for f in entry["files_touched"]:
            lines.append(f"- `{f}`")
        lines.append("")

    if entry.get("bash_commands"):
        lines.append("### Commands run")
        lines.append("```sh")
        for c in entry["bash_commands"][:40]:
            lines.append(c if len(c) < 200 else c[:200] + " …")
        lines.append("```")
        lines.append("")

    if entry.get("errors"):
        lines.append("### Errors / friction encountered")
        for e in entry["errors"][:15]:
            lines.append(f"- {e}")
        lines.append("")

    if entry.get("highlights"):
        lines.append("### Key takeaways (assistant summaries)")
        for h in entry["highlights"]:
            # Keep concise: first paragraph of each assistant summary.
            para = h.strip().split("\n\n")[0]
            lines.append(f"- {_first_line(para, 240)}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("transcript", help="Path to a session .jsonl transcript")
    ap.add_argument("--out-dir", help="Directory to write <id>.json and <id>.md")
    ap.add_argument("--print", action="store_true", help="Print markdown to stdout")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.transcript):
        print(f"error: no such transcript: {args.transcript}", file=sys.stderr)
        return 2

    entry = distill(args.transcript)
    md = to_markdown(entry)

    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)
        sid = entry.get("session_id") or os.path.splitext(os.path.basename(args.transcript))[0]
        with open(os.path.join(args.out_dir, f"{sid}.json"), "w", encoding="utf-8") as fh:
            json.dump(entry, fh, indent=2, ensure_ascii=False)
        with open(os.path.join(args.out_dir, f"{sid}.md"), "w", encoding="utf-8") as fh:
            fh.write(md)
        print(f"wrote {args.out_dir}/{sid}.json and {sid}.md", file=sys.stderr)

    if args.print or not args.out_dir:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
