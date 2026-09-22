"""Command line entry points.

    python -m ssei_scraper crawl    --config config/ssei.yaml
    python -m ssei_scraper extract  --config config/ssei.yaml
    python -m ssei_scraper keywords --config config/ssei.yaml
    python -m ssei_scraper teardown --config config/ssei.yaml --url https://ssei.co.in/cfa/

`crawl` is the only step that touches the network. Everything after it runs
off the on-disk archive, so extraction can be re-run and corrected without
re-hitting the origin.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any

from . import config as config_mod
from .crawler import Crawler
from .extract import decode, parse
from .keywords import build_pattern, scan_html
from .render import occurrences_to_markdown, page_to_markdown
from .store import Store, safe_relpath
from .teardown import teardown, teardown_to_markdown

_CHARSET = re.compile(r"charset=([A-Za-z0-9_\-]+)", re.IGNORECASE)


def _html_rows(store: Store) -> list[dict[str, Any]]:
    """Successful HTML pages from the manifest, newest record per dedupe key.

    A re-crawl appends rather than overwrites, so the manifest can hold several
    records for one page. Taking the last occurrence makes every downstream
    step reflect the most recent successful fetch.
    """
    latest: dict[str, dict[str, Any]] = {}
    for row in store.read_manifest():
        if row.get("kind") != "page" or row.get("error") or not row.get("body_path"):
            continue
        if row.get("status") != 200:
            continue
        latest[row["dedupe_key"]] = row
    return list(latest.values())


def _load_html(store: Store, row: dict[str, Any]) -> str:
    body = (store.out_dir / row["body_path"]).read_bytes()
    m = _CHARSET.search(row.get("content_type") or "")
    html, _ = decode(body, m.group(1) if m else None)
    return html


def cmd_crawl(args: argparse.Namespace) -> int:
    cfg = config_mod.load(args.config, out_dir=args.out)
    store = Store(cfg.out_dir)
    crawler = Crawler(cfg, store)
    asyncio.run(crawler.run(resume=args.resume))
    if crawler.skipped:
        skipped_path = cfg.out_dir / "skipped.json"
        skipped_path.write_text(
            json.dumps([{"url": u, "reason": r} for u, r in crawler.skipped], indent=2),
            encoding="utf-8",
        )
        print(f"wrote {skipped_path}")
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    cfg = config_mod.load(args.config, out_dir=args.out)
    store = Store(cfg.out_dir)
    rows = _html_rows(store)
    if not rows:
        print("no archived HTML pages found -- run `crawl` first", file=sys.stderr)
        return 1

    json_dir = cfg.out_dir / "structured"
    md_dir = cfg.out_dir / "markdown"
    json_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)

    index: list[dict[str, Any]] = []
    for row in rows:
        html = _load_html(store, row)
        page = parse(html, row["final_url"] or row["url"])
        stem = Path(safe_relpath(row["url"])).with_suffix("")
        (json_dir / stem).parent.mkdir(parents=True, exist_ok=True)
        (md_dir / stem).parent.mkdir(parents=True, exist_ok=True)
        (json_dir / stem).with_suffix(".json").write_text(
            json.dumps(page.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (md_dir / stem).with_suffix(".md").write_text(page_to_markdown(page), encoding="utf-8")
        index.append({
            "url": page.url,
            "title": page.title,
            "headings": len(page.headings),
            "sections": len(page.sections),
            "forms": len(page.forms),
            "ctas": len(page.ctas),
            "text_chars": len(page.text),
            "json": str((json_dir / stem).with_suffix(".json").relative_to(cfg.out_dir)),
            "markdown": str((md_dir / stem).with_suffix(".md").relative_to(cfg.out_dir)),
        })

    (cfg.out_dir / "index.json").write_text(
        json.dumps(sorted(index, key=lambda r: r["url"]), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"extracted {len(index)} pages -> {json_dir} and {md_dir}")
    return 0


def cmd_keywords(args: argparse.Namespace) -> int:
    cfg = config_mod.load(args.config, out_dir=args.out)
    store = Store(cfg.out_dir)
    keywords = args.keyword or list(cfg.keywords)
    pattern = build_pattern(keywords)

    rows = _html_rows(store)
    if not rows:
        print("no archived HTML pages found -- run `crawl` first", file=sys.stderr)
        return 1

    occurrences: list[dict[str, Any]] = []
    for row in rows:
        html = _load_html(store, row)
        for occ in scan_html(html, row["final_url"] or row["url"], pattern):
            occurrences.append(occ.to_dict())

    label = ", ".join(keywords)
    (cfg.out_dir / "keyword-occurrences.json").write_text(
        json.dumps(occurrences, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (cfg.out_dir / "keyword-occurrences.md").write_text(
        occurrences_to_markdown(occurrences, label), encoding="utf-8"
    )
    pages = len({o["url"] for o in occurrences})
    print(f"{len(occurrences)} occurrences of [{label}] across {pages} pages")
    print(f"wrote {cfg.out_dir / 'keyword-occurrences.md'}")
    return 0


def cmd_teardown(args: argparse.Namespace) -> int:
    cfg = config_mod.load(args.config, out_dir=args.out)
    store = Store(cfg.out_dir)
    policy = cfg.url_policy
    want = policy.dedupe_key(args.url)

    for row in _html_rows(store):
        if policy.dedupe_key(row["url"]) == want or policy.dedupe_key(row["final_url"]) == want:
            html = _load_html(store, row)
            data = teardown(html, row["final_url"] or row["url"])
            out_json = cfg.out_dir / "teardown.json"
            out_md = cfg.out_dir / "teardown.md"
            out_json.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            out_md.write_text(teardown_to_markdown(data), encoding="utf-8")
            print(f"wrote {out_md}")
            return 0

    print(f"{args.url} is not in the archive -- crawl it first", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ssei_scraper", description=__doc__)
    parser.add_argument("--config", default="config/ssei.yaml")
    parser.add_argument("--out", default=None, help="override out_dir from config")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("crawl", help="fetch and archive (the only networked step)")
    p.add_argument("--resume", action="store_true", help="skip URLs already archived")
    p.set_defaults(func=cmd_crawl)

    p = sub.add_parser("extract", help="archive -> structured JSON + markdown")
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser("keywords", help="verbatim keyword occurrence report")
    p.add_argument("--keyword", action="append", help="repeatable; defaults to config")
    p.set_defaults(func=cmd_keywords)

    p = sub.add_parser("teardown", help="structural teardown of one archived page")
    p.add_argument("--url", required=True)
    p.set_defaults(func=cmd_teardown)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
