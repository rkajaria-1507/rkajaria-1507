"""Structural teardown of a landing page, for rebuilding an analogue.

This answers "what is this page made of, and what does it talk to?" -- the
section skeleton, the reusable block types, and every backend surface the page
exposes (forms, endpoints, embedded config, third-party scripts).
"""
from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urlsplit

from bs4 import BeautifulSoup

from .extract import clean_text, dom_path

# Endpoint-ish strings inside inline JS: "/api/x", "https://host/path".
_ENDPOINT = re.compile(r"""["'](/(?:api|graphql|ajax|wp-json)[^"'\s]*|https?://[^"'\s]+)["']""")
_FRAMEWORK_HINTS = {
    "next.js": (re.compile(r"__NEXT_DATA__|/_next/static"), "Next.js"),
    "nuxt": (re.compile(r"__NUXT__|/_nuxt/"), "Nuxt"),
    "react": (re.compile(r"react(?:-dom)?(?:\.production)?\.min\.js|data-reactroot"), "React"),
    "wordpress": (re.compile(r"/wp-content/|/wp-includes/|wp-json"), "WordPress"),
    "gtm": (re.compile(r"googletagmanager\.com|dataLayer"), "Google Tag Manager"),
    "ga": (re.compile(r"google-analytics\.com|gtag\("), "Google Analytics"),
    "fbq": (re.compile(r"connect\.facebook\.net|fbq\("), "Meta Pixel"),
    "razorpay": (re.compile(r"checkout\.razorpay\.com|Razorpay"), "Razorpay"),
    "stripe": (re.compile(r"js\.stripe\.com|Stripe\("), "Stripe"),
    "cashfree": (re.compile(r"cashfree"), "Cashfree"),
    "cloudflare": (re.compile(r"cdn-cgi/"), "Cloudflare"),
    "jquery": (re.compile(r"jquery(?:\.min)?\.js"), "jQuery"),
    "bootstrap": (re.compile(r"bootstrap(?:\.min)?\.(?:js|css)"), "Bootstrap"),
    "tailwind": (re.compile(r"tailwind|(?:\s|\")(?:flex|grid)\s+(?:items-|justify-)"), "Tailwind CSS"),
}

# Block-type classifier: class/id substrings -> a semantic block name.
_BLOCK_TYPES = [
    ("hero", ("hero", "banner", "masthead", "jumbotron")),
    ("faq", ("faq", "accordion", "question")),
    ("testimonial", ("testimonial", "review", "student-say", "feedback")),
    ("pricing", ("pricing", "price", "plan", "package", "tier")),
    ("faculty", ("faculty", "instructor", "teacher", "mentor", "author")),
    ("curriculum", ("curriculum", "syllabus", "module", "chapter", "topic")),
    ("feature", ("feature", "benefit", "why-", "highlight", "usp")),
    ("cta", ("cta", "enroll", "enrol", "register", "signup", "buy")),
    ("stats", ("stat", "counter", "number", "metric", "achievement")),
    ("form", ("form", "lead", "contact", "enquiry", "inquiry")),
    ("footer", ("footer",)),
    ("nav", ("nav", "menu", "header")),
    ("carousel", ("carousel", "slider", "swiper", "slick")),
    ("video", ("video", "youtube", "vimeo", "player")),
]


def classify_block(node: Any) -> str | None:
    token = " ".join((node.get("class") or []) + [node.get("id") or ""]).lower()
    if not token.strip():
        return None
    for name, needles in _BLOCK_TYPES:
        if any(n in token for n in needles):
            return name
    return None


def teardown(html: str, url: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "lxml")

    scripts = [s.get("src") for s in soup.find_all("script", src=True)]
    styles = [l.get("href") for l in soup.find_all("link", rel=lambda v: v and "stylesheet" in v)]
    inline_js = "\n".join(s.string or "" for s in soup.find_all("script") if not s.get("src"))
    whole = html

    detected = sorted({
        label for _, (pattern, label) in _FRAMEWORK_HINTS.items() if pattern.search(whole)
    })

    endpoints = sorted({m.group(1) for m in _ENDPOINT.finditer(inline_js)})
    third_party = sorted({
        urlsplit(s).netloc for s in scripts + styles
        if s and urlsplit(s).netloc and urlsplit(s).netloc != urlsplit(url).netloc
    })

    blocks: list[dict[str, Any]] = []
    for node in soup.find_all(["section", "div", "header", "footer", "main", "aside", "nav"]):
        kind = classify_block(node)
        if not kind:
            continue
        heading = node.find(["h1", "h2", "h3"])
        blocks.append({
            "type": kind,
            "tag": node.name,
            "classes": node.get("class") or [],
            "id": node.get("id"),
            "heading": clean_text(heading.get_text(" ")) if heading else None,
            "location": dom_path(node),
            "text_chars": len(clean_text(node.get_text(" "))),
            "child_count": len(node.find_all(recursive=False)),
        })

    # Keep only outermost blocks of each type to avoid reporting a hero and
    # its six nested divs as seven heroes.
    pruned: list[dict[str, Any]] = []
    for block in blocks:
        if not any(
            other is not block
            and block["location"].startswith(other["location"] + " > ")
            and other["type"] == block["type"]
            for other in blocks
        ):
            pruned.append(block)

    return {
        "url": url,
        "detected_technologies": detected,
        "third_party_hosts": third_party,
        "script_sources": [s for s in scripts if s],
        "stylesheets": [s for s in styles if s],
        "inline_endpoints": endpoints,
        "block_skeleton": pruned,
        "block_type_counts": {
            t: sum(1 for b in pruned if b["type"] == t)
            for t in sorted({b["type"] for b in pruned})
        },
        "iframes": [i.get("src") for i in soup.find_all("iframe", src=True)],
        "meta_tags": [
            {k: v for k, v in m.attrs.items()} for m in soup.find_all("meta")
        ],
    }


def teardown_to_markdown(data: dict[str, Any]) -> str:
    out = [f"# Page structure teardown: {data['url']}", ""]
    out += ["## Detected technologies", ""]
    out += [f"- {t}" for t in data["detected_technologies"]] or ["_no known signatures matched_"]
    out += ["", "## Third-party hosts", ""]
    out += [f"- `{h}`" for h in data["third_party_hosts"]] or ["_none_"]
    out += ["", "## Endpoints referenced in inline JS", ""]
    out += [f"- `{e}`" for e in data["inline_endpoints"]] or ["_none found_"]
    out += ["", "## Block skeleton (section order)", ""]
    for b in data["block_skeleton"]:
        head = f" - {b['heading']!r}" if b["heading"] else ""
        out.append(f"- **{b['type']}** `<{b['tag']}>`{head}  ({b['text_chars']} chars)")
        out.append(f"  `{b['location']}`")
    out += ["", "## Block type counts", ""]
    out += [f"- {k}: {v}" for k, v in data["block_type_counts"].items()] or ["_none_"]
    out += ["", "## Stylesheets", ""] + [f"- `{s}`" for s in data["stylesheets"]]
    out += ["", "## Scripts", ""] + [f"- `{s}`" for s in data["script_sources"]]
    out += ["", "## Embeds", ""] + ([f"- `{i}`" for i in data["iframes"]] or ["_none_"])
    return "\n".join(out)
