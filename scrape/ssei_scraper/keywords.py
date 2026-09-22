"""Verbatim keyword occurrence scanning.

The brief is "every single mention of FRM, word for word". That means an
occurrence report where each hit carries its exact surrounding sentence and
its position in the document -- not a summary, and not a bag of pages.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any, Iterable

from bs4 import BeautifulSoup

from .extract import clean_text, dom_path, _NON_CONTENT


@dataclass
class Occurrence:
    url: str
    keyword: str
    matched_text: str      # the exact substring matched
    context: str           # verbatim surrounding text
    element: str           # tag name the hit sits in
    location: str          # DOM path
    attribute: str | None  # set when the hit is in an attribute, not text

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_pattern(keywords: Iterable[str]) -> re.Pattern[str]:
    r"""Word-boundary alternation over the keywords.

    ``\b`` around ``FRM`` is what stops "conFRMation"-style false positives
    while still catching "FRM," "FRM-Part1" and "(FRM)". Longest-first
    alternation keeps "FRM Part 2" from being reported as bare "FRM".
    """
    ordered = sorted({k for k in keywords if k}, key=len, reverse=True)
    if not ordered:
        raise ValueError("at least one keyword is required")
    return re.compile(r"\b(" + "|".join(re.escape(k) for k in ordered) + r")\b", re.IGNORECASE)


def _context_window(text: str, start: int, end: int, width: int = 160) -> str:
    """Widen the match to sentence-ish boundaries, capped at *width* each side."""
    left = max(0, start - width)
    right = min(len(text), end + width)
    snippet = text[left:right]
    if left > 0:
        snippet = "..." + snippet
    if right < len(text):
        snippet = snippet + "..."
    return clean_text(snippet)


def scan_html(html: str, url: str, pattern: re.Pattern[str]) -> list[Occurrence]:
    """Find every keyword hit in visible text *and* in meaningful attributes.

    Attribute hits matter: an ``alt="FRM Part 1 batch"`` or a
    ``href="/courses/frm"`` is real FRM content the page renders or routes to,
    and a text-only scan would miss both.
    """
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(_NON_CONTENT):
        tag.decompose()

    out: list[Occurrence] = []
    seen: set[tuple[str, str, str]] = set()

    for node in soup.find_all(string=True):
        text = str(node)
        if not text.strip():
            continue
        parent = node.parent
        for m in pattern.finditer(text):
            key = (m.group(0), dom_path(parent), text[:80])
            if key in seen:
                continue
            seen.add(key)
            out.append(
                Occurrence(
                    url=url, keyword=m.group(0).upper(), matched_text=m.group(0),
                    context=_context_window(text, m.start(), m.end()),
                    element=parent.name if parent else "", location=dom_path(parent) if parent else "",
                    attribute=None,
                )
            )

    for attr in ("alt", "title", "aria-label", "placeholder", "value", "href", "content"):
        for node in soup.find_all(attrs={attr: True}):
            value = str(node.get(attr) or "")
            for m in pattern.finditer(value):
                out.append(
                    Occurrence(
                        url=url, keyword=m.group(0).upper(), matched_text=m.group(0),
                        context=clean_text(value)[:400], element=node.name,
                        location=dom_path(node), attribute=attr,
                    )
                )
    return out
