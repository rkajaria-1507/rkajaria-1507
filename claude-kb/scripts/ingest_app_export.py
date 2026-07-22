#!/usr/bin/env python3
"""
Ingest a claude.ai data export into learning entries.

The app cannot be scraped live — the only supported path is the manual export:
  claude.ai → Settings → Privacy → "Export data".
Anthropic emails you a .zip / .json dump. Point this script at the
`conversations.json` file inside it.

Usage:
    ingest_app_export.py conversations.json --out-dir DIR [--since YYYY-MM-DD]

Writes one entry per conversation:
    DIR/app-<conversation-id>.json
    DIR/app-<conversation-id>.md

The export schema has shifted over time, so this parser is defensive: it looks
for a list of conversations, each with a name/title, timestamps, and a list of
messages that each carry a sender/role and text.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone


def _load(path: str):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    # Export may be a bare list, or {"conversations": [...]}.
    if isinstance(data, dict):
        for key in ("conversations", "chat_conversations", "data"):
            if isinstance(data.get(key), list):
                return data[key]
        # Single conversation object.
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("unrecognized export shape")


def _get(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k]
    return default


def _messages(conv: dict):
    for key in ("chat_messages", "messages", "mapping"):
        val = conv.get(key)
        if isinstance(val, list):
            return val
        if isinstance(val, dict):  # some exports keyed by id
            return list(val.values())
    return []


def _msg_text(msg: dict) -> str:
    # Direct text field.
    txt = _get(msg, "text", "content", default="")
    if isinstance(txt, str) and txt.strip():
        return txt.strip()
    # content as list of blocks.
    if isinstance(txt, list):
        parts = []
        for b in txt:
            if isinstance(b, dict):
                parts.append(_get(b, "text", default=""))
            elif isinstance(b, str):
                parts.append(b)
        return "\n".join(p for p in parts if p).strip()
    return ""


def _msg_role(msg: dict) -> str:
    role = _get(msg, "sender", "role", default="")
    return str(role).lower()


def _parse_date(val):
    if not val:
        return None
    try:
        return datetime.fromisoformat(str(val).replace("Z", "+00:00"))
    except ValueError:
        return None


def conv_to_entry(conv: dict) -> dict:
    cid = str(_get(conv, "uuid", "id", "conversation_id", default="unknown"))
    title = _get(conv, "name", "title", default="(untitled)")
    created = _get(conv, "created_at", "create_time")
    updated = _get(conv, "updated_at", "update_time")

    human, assistant = [], []
    for m in _messages(conv):
        if not isinstance(m, dict):
            continue
        role = _msg_role(m)
        text = _msg_text(m)
        if not text:
            continue
        if role in ("human", "user"):
            human.append(text)
        elif role in ("assistant", "claude"):
            assistant.append(text)

    return {
        "schema": 1,
        "source": "app",
        "session_id": f"app-{cid}",
        "title": title,
        "created_at": str(created) if created else None,
        "updated_at": str(updated) if updated else None,
        "distilled_at": datetime.now(timezone.utc).isoformat(),
        "counts": {"human_messages": len(human), "assistant_messages": len(assistant)},
        "topics": human,
        "highlights": assistant,
    }


def to_markdown(entry: dict) -> str:
    lines = []
    date = (entry.get("created_at") or "")[:10]
    lines.append(f"## [app] {entry.get('title','(untitled)')} — {date}")
    lines.append("")
    if entry.get("topics"):
        lines.append("### What was asked")
        for t in entry["topics"][:20]:
            first = t.strip().splitlines()[0]
            lines.append(f"- {first[:200]}")
        lines.append("")
    if entry.get("highlights"):
        lines.append("### Key takeaways")
        for h in entry["highlights"][:20]:
            para = h.strip().split("\n\n")[0]
            first = para.splitlines()[0] if para else ""
            lines.append(f"- {first[:240]}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("export", help="Path to conversations.json from a data export")
    ap.add_argument("--out-dir", required=True, help="Directory to write entries")
    ap.add_argument("--since", help="Only ingest conversations updated on/after YYYY-MM-DD")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.export):
        print(f"error: no such file: {args.export}", file=sys.stderr)
        return 2

    try:
        convs = _load(args.export)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"error: could not parse export: {e}", file=sys.stderr)
        return 2

    since = _parse_date(args.since) if args.since else None
    os.makedirs(args.out_dir, exist_ok=True)
    written = 0
    for conv in convs:
        if not isinstance(conv, dict):
            continue
        entry = conv_to_entry(conv)
        if since:
            upd = _parse_date(entry.get("updated_at") or entry.get("created_at"))
            if upd and upd < since:
                continue
        sid = entry["session_id"]
        with open(os.path.join(args.out_dir, f"{sid}.json"), "w", encoding="utf-8") as fh:
            json.dump(entry, fh, indent=2, ensure_ascii=False)
        with open(os.path.join(args.out_dir, f"{sid}.md"), "w", encoding="utf-8") as fh:
            fh.write(to_markdown(entry))
        written += 1

    print(f"ingested {written} conversation(s) into {args.out_dir}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
