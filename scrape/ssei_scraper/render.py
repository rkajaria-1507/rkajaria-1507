"""Structured page model -> human-reviewable markdown."""
from __future__ import annotations

import json
from typing import Any

from .extract import Page


def _fence(value: Any) -> str:
    return "```json\n" + json.dumps(value, indent=2, ensure_ascii=False) + "\n```"


def page_to_markdown(page: Page) -> str:
    out: list[str] = [f"# {page.title or '(untitled)'}", "", f"**URL:** {page.url}  "]
    if page.canonical:
        out.append(f"**Canonical:** {page.canonical}  ")
    if page.lang:
        out.append(f"**Lang:** {page.lang}  ")
    if page.robots_meta:
        out.append(f"**Robots:** {page.robots_meta}  ")
    if page.meta_description:
        out += ["", "**Meta description:**", "", f"> {page.meta_description}"]

    if page.open_graph:
        out += ["", "## Open Graph", ""]
        out += [f"- `{k}`: {v}" for k, v in sorted(page.open_graph.items())]
    if page.twitter:
        out += ["", "## Twitter card", ""]
        out += [f"- `{k}`: {v}" for k, v in sorted(page.twitter.items())]

    if page.json_ld:
        out += ["", "## JSON-LD (schema.org)", "", _fence(page.json_ld)]

    out += ["", "## Heading outline", ""]
    out += [f"{'  ' * (h['level'] - 1)}- H{h['level']}: {h['text']}" for h in page.headings] or ["_none_"]

    out += ["", "## Sections (verbatim copy)", ""]
    if not page.sections:
        out.append("_no headings; see Full text below_")
    for sec in page.sections:
        out += [f"### {'#' * min(sec.level, 4)} {sec.heading}".replace("### #", "###"), ""]
        out += [f"`{sec.location}`", ""]
        out += [p for p in sec.paragraphs]
        if sec.list_items:
            out += [""] + [f"- {li}" for li in sec.list_items]
        out.append("")

    if page.tables:
        out += ["## Tables", ""]
        for i, rows in enumerate(page.tables, 1):
            out.append(f"**Table {i}**")
            out.append("")
            if rows:
                out.append("| " + " | ".join(rows[0]) + " |")
                out.append("|" + "---|" * len(rows[0]))
                for row in rows[1:]:
                    out.append("| " + " | ".join(row) + " |")
            out.append("")

    if page.ctas:
        out += ["## Calls to action", ""]
        out += [f"- **{c['text']}** -> `{c['href'] or '(no href)'}`  `{c['location']}`" for c in page.ctas]
        out.append("")

    if page.forms:
        out += ["## Forms (backend surface)", ""]
        for i, form in enumerate(page.forms, 1):
            out += [f"**Form {i}** - `{form.method.upper()}` -> `{form.action or '(same page)'}`  `{form.location}`", ""]
            for f in form.fields:
                req = " *(required)*" if f.required else ""
                opts = f" options={f.options}" if f.options else ""
                out.append(f"- `{f.name or '(unnamed)'}` [{f.field_type}] label={f.label!r}{req}{opts}")
            if form.submit_labels:
                out.append(f"- submit: {', '.join(form.submit_labels)}")
            out.append("")

    if page.images:
        out += ["## Images", ""]
        out += [f"- `{i['src']}` alt={i['alt']!r}" for i in page.images]
        out.append("")

    out += ["## Full visible text (verbatim)", "", "```text", page.text, "```", ""]
    return "\n".join(out)


def occurrences_to_markdown(rows: list[dict], keyword_label: str) -> str:
    by_url: dict[str, list[dict]] = {}
    for row in rows:
        by_url.setdefault(row["url"], []).append(row)

    out = [
        f"# Verbatim `{keyword_label}` occurrence report",
        "",
        f"**Total occurrences:** {len(rows)} across {len(by_url)} pages.",
        "",
        "Every hit below is quoted exactly as the page renders it. `attribute` "
        "hits come from markup attributes (alt text, link targets, meta tags) "
        "rather than body copy.",
        "",
    ]
    for url in sorted(by_url):
        hits = by_url[url]
        out += [f"## {url}", "", f"{len(hits)} occurrence(s)", ""]
        for h in hits:
            where = f"@{h['attribute']}" if h["attribute"] else ""
            out += [f"- `<{h['element']}{where}>` `{h['location']}`", f"  > {h['context']}", ""]
    return "\n".join(out)
