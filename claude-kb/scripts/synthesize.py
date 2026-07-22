#!/usr/bin/env python3
"""
Aggregate all distilled entries into a single readable knowledge base.

Reads every *.json entry in the entries dir (produced by distill_session.py and
ingest_app_export.py) and writes KNOWLEDGE.md: a rolling digest of what you've
worked on and learned across every session, CLI and app.

Usage:
    synthesize.py --entries-dir DIR --out KNOWLEDGE.md [--llm]

With --llm, the per-session takeaways are additionally passed to `claude -p`
(headless Claude Code) to produce a short narrative "what we learned" section.
Without it, you still get a complete deterministic digest (tools leaderboard,
timeline, topics, errors) at zero cost — this is what the automatic hook uses.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone


def load_entries(entries_dir: str) -> list[dict]:
    entries = []
    for path in glob.glob(os.path.join(entries_dir, "*.json")):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                entries.append(json.load(fh))
        except (json.JSONDecodeError, OSError):
            continue

    def _key(e):
        return e.get("started_at") or e.get("created_at") or e.get("distilled_at") or ""

    return sorted(entries, key=_key)


def _sesh_date(e: dict) -> str:
    return (e.get("started_at") or e.get("created_at") or e.get("distilled_at") or "")[:10]


def build_digest(entries: list[dict], llm: bool) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    cli = [e for e in entries if e.get("source") == "cli"]
    app = [e for e in entries if e.get("source") == "app"]

    tool_totals: Counter = Counter()
    for e in cli:
        for name, n in (e.get("tools_used") or {}).items():
            tool_totals[name] += n

    total_tool_calls = sum(tool_totals.values())
    all_errors = [(e, err) for e in entries for err in (e.get("errors") or [])]

    out: list[str] = []
    out.append("# Claude Knowledge Base")
    out.append("")
    out.append(f"_Auto-generated digest of what we've built and learned. Last updated {now}._")
    out.append("")
    out.append("## At a glance")
    out.append("")
    out.append(f"- **Sessions captured:** {len(entries)}  ({len(cli)} CLI, {len(app)} app)")
    if entries:
        span = f"{_sesh_date(entries[0])} → {_sesh_date(entries[-1])}"
        out.append(f"- **Span:** {span}")
    out.append(f"- **Total tool calls (CLI):** {total_tool_calls}")
    out.append(f"- **Errors / friction logged:** {len(all_errors)}")
    out.append("")

    if tool_totals:
        out.append("## Tool leaderboard")
        out.append("")
        out.append("| Tool | Calls |")
        out.append("| --- | ---: |")
        for name, n in tool_totals.most_common(20):
            out.append(f"| `{name}` | {n} |")
        out.append("")

    # Recurring topics: naive keyword frequency across prompts.
    topic_words: Counter = Counter()
    stop = set(
        "the a an and or to of in on for with i you we it this that is are be do "
        "want need make please can how what why when should would could my our "
        "so but if then me your all over from into out up now go let".split()
    )
    for e in entries:
        for t in e.get("topics") or []:
            for w in "".join(c.lower() if c.isalnum() or c.isspace() else " " for c in t).split():
                if len(w) > 3 and w not in stop:
                    topic_words[w] += 1
    if topic_words:
        out.append("## Recurring themes")
        out.append("")
        themes = ", ".join(f"{w} ({n})" for w, n in topic_words.most_common(15))
        out.append(themes)
        out.append("")

    if llm:
        narrative = _llm_narrative(entries)
        if narrative:
            out.append("## What we learned (synthesized)")
            out.append("")
            out.append(narrative.strip())
            out.append("")

    out.append("## Timeline")
    out.append("")
    for e in reversed(entries):  # newest first
        date = _sesh_date(e)
        if e.get("source") == "app":
            title = e.get("title", "(untitled)")
            out.append(f"### {date} · [app] {title}")
        else:
            sid = (e.get("session_id") or "?")[:8]
            branch = e.get("git_branch") or ""
            out.append(f"### {date} · [cli] {sid}" + (f" · `{branch}`" if branch else ""))
        out.append("")
        topics = e.get("topics") or []
        if topics:
            for t in topics[:5]:
                first = t.strip().splitlines()[0] if t.strip() else ""
                out.append(f"- {first[:160]}")
        highlights = e.get("highlights") or []
        if highlights:
            para = highlights[-1].strip().split("\n\n")[0]
            first = para.splitlines()[0] if para else ""
            if first:
                out.append(f"  - _takeaway:_ {first[:220]}")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def _llm_narrative(entries: list[dict]) -> str | None:
    """Optionally use headless Claude Code to write a narrative summary."""
    if not shutil.which("claude"):
        print("note: --llm requested but `claude` not on PATH; skipping", file=sys.stderr)
        return None
    bullets = []
    for e in entries[-40:]:
        date = _sesh_date(e)
        topic = ""
        if e.get("topics"):
            topic = e["topics"][0].strip().splitlines()[0][:200]
        take = ""
        if e.get("highlights"):
            take = e["highlights"][-1].strip().split("\n\n")[0].splitlines()[0][:200]
        bullets.append(f"- {date} [{e.get('source')}] {topic} :: {take}")
    prompt = (
        "Below are one-line summaries of recent Claude sessions (CLI and app). "
        "Write a concise 'what we learned' brief: 4-8 bullets grouping recurring "
        "themes, tools/workflows that worked, and open threads. No preamble.\n\n"
        + "\n".join(bullets)
    )
    try:
        res = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True, text=True, timeout=180,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
        print(f"note: claude -p failed ({res.returncode}); skipping narrative", file=sys.stderr)
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"note: claude -p error: {e}; skipping narrative", file=sys.stderr)
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entries-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--llm", action="store_true", help="Add an LLM-written narrative via `claude -p`")
    args = ap.parse_args(argv)

    entries = load_entries(args.entries_dir)
    digest = build_digest(entries, llm=args.llm)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(digest)
    print(f"wrote {args.out} from {len(entries)} entr(y/ies)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
