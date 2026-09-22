"""HTML -> structured content model, and link discovery.

Everything the rebuild needs is captured *with its location in the document*,
so a later diff can answer "which section did this sentence come from?".
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Iterable

from bs4 import BeautifulSoup, Tag

from .urls import absolutise, is_asset_path

_META_CHARSET = re.compile(rb"""<meta[^>]+charset=["']?\s*([A-Za-z0-9_\-]+)""", re.IGNORECASE)
_WS = re.compile(r"[ \t\r\f\v]+")

# Elements whose text is markup plumbing, never page copy.
_NON_CONTENT = ("script", "style", "noscript", "template", "svg")


def decode(body: bytes, content_type_charset: str | None) -> tuple[str, str]:
    """Decode response bytes to text, returning (text, charset_used).

    Order follows the HTML spec's sniffing priority: transport charset first,
    then an in-document meta charset, then utf-8. We never raise -- a page we
    cannot decode cleanly is still worth archiving with replacement chars, and
    the charset actually used is recorded so the loss is visible.
    """
    candidates: list[str] = []
    if content_type_charset:
        candidates.append(content_type_charset)
    m = _META_CHARSET.search(body[:4096])
    if m:
        try:
            candidates.append(m.group(1).decode("ascii"))
        except UnicodeDecodeError:
            pass
    candidates.append("utf-8")

    for enc in candidates:
        try:
            return body.decode(enc), enc
        except (UnicodeDecodeError, LookupError):
            continue
    return body.decode("utf-8", errors="replace"), "utf-8+replace"


def clean_text(value: str | None) -> str:
    """Collapse horizontal whitespace but preserve line structure.

    Blanket ``\\s+`` collapsing would weld list items and headings into one
    run-on line, destroying exactly the structure we are here to capture.
    """
    if not value:
        return ""
    lines = [_WS.sub(" ", ln).strip() for ln in value.splitlines()]
    return "\n".join(ln for ln in lines if ln).strip()


def dom_path(node: Tag) -> str:
    """A readable CSS-ish path, e.g. ``body > section.hero:nth-of-type(2) > h1``."""
    parts: list[str] = []
    cur: Tag | None = node
    while isinstance(cur, Tag) and cur.name not in (None, "[document]"):
        seg = cur.name
        classes = cur.get("class") or []
        if classes:
            seg += "." + ".".join(classes[:2])
        elif cur.get("id"):
            seg += f"#{cur['id']}"
        siblings = [s for s in cur.parent.find_all(cur.name, recursive=False)] if cur.parent else []
        if len(siblings) > 1:
            seg += f":nth-of-type({siblings.index(cur) + 1})"
        parts.append(seg)
        cur = cur.parent
    return " > ".join(reversed(parts[:-1])) if len(parts) > 1 else (parts[0] if parts else "")


@dataclass
class Link:
    href: str
    text: str
    rel: str | None
    location: str


@dataclass
class FormField:
    name: str | None
    field_type: str
    label: str
    required: bool
    options: list[str] = field(default_factory=list)


@dataclass
class Form:
    action: str | None
    method: str
    fields: list[FormField]
    submit_labels: list[str]
    location: str


@dataclass
class Section:
    heading: str
    level: int
    location: str
    paragraphs: list[str] = field(default_factory=list)
    list_items: list[str] = field(default_factory=list)


@dataclass
class Page:
    url: str
    title: str
    meta_description: str
    canonical: str | None
    lang: str | None
    robots_meta: str | None
    open_graph: dict[str, str]
    twitter: dict[str, str]
    json_ld: list[Any]
    headings: list[dict[str, Any]]
    sections: list[Section]
    paragraphs: list[str]
    list_items: list[str]
    tables: list[list[list[str]]]
    ctas: list[dict[str, str]]
    forms: list[Form]
    images: list[dict[str, str]]
    links: list[Link]
    text: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _visible_soup(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(_NON_CONTENT):
        tag.decompose()
    return soup


def extract_json_ld(html: str) -> list[Any]:
    """JSON-LD is parsed from the *original* HTML, before script removal.

    Schema.org blocks are the highest-value structured data on a marketing
    page (FAQPage, Course, Offer/price, BreadcrumbList) and they live inside
    <script>, which the content pass deletes.
    """
    blocks: list[Any] = []
    soup = BeautifulSoup(html, "lxml")
    for node in soup.find_all("script", attrs={"type": re.compile("ld\\+json", re.I)}):
        raw = node.string or node.get_text() or ""
        try:
            blocks.append(json.loads(raw))
        except json.JSONDecodeError:
            # Trailing commas and stray HTML comments are common in the wild.
            cleaned = re.sub(r"^\s*<!--|-->\s*$", "", raw.strip())
            cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
            try:
                blocks.append(json.loads(cleaned))
            except json.JSONDecodeError:
                blocks.append({"_unparsed": raw[:2000]})
    return blocks


def extract_links(html: str, base_url: str) -> list[Link]:
    soup = BeautifulSoup(html, "lxml")
    out: list[Link] = []
    for a in soup.find_all("a"):
        raw = a.get("href")
        resolved = absolutise(base_url, raw)
        if resolved is None:
            continue
        rel = a.get("rel")
        out.append(
            Link(
                href=resolved,
                text=clean_text(a.get_text(" ")),
                rel=" ".join(rel) if isinstance(rel, list) else rel,
                location=dom_path(a),
            )
        )
    return out


def _nearest_label(soup: BeautifulSoup, node: Tag) -> str:
    """Resolve a field's human label: for=, wrapping <label>, aria-label, placeholder."""
    field_id = node.get("id")
    if field_id:
        lab = soup.find("label", attrs={"for": field_id})
        if lab:
            return clean_text(lab.get_text(" "))
    parent_label = node.find_parent("label")
    if parent_label:
        return clean_text(parent_label.get_text(" "))
    for attr in ("aria-label", "placeholder", "title", "name"):
        if node.get(attr):
            return clean_text(str(node.get(attr)))
    return ""


def extract_forms(soup: BeautifulSoup, base_url: str) -> list[Form]:
    forms: list[Form] = []
    for f in soup.find_all("form"):
        fields: list[FormField] = []
        for node in f.find_all(["input", "select", "textarea"]):
            ftype = (
                node.get("type", "text")
                if node.name == "input"
                else node.name
            )
            options = (
                [clean_text(o.get_text(" ")) for o in node.find_all("option")]
                if node.name == "select"
                else []
            )
            fields.append(
                FormField(
                    name=node.get("name"),
                    field_type=str(ftype).lower(),
                    label=_nearest_label(soup, node),
                    required=node.has_attr("required"),
                    options=options,
                )
            )
        submits = [
            clean_text(b.get_text(" ")) or clean_text(str(b.get("value") or ""))
            for b in f.find_all(["button"]) + f.find_all("input", attrs={"type": re.compile("submit|button", re.I)})
        ]
        action = f.get("action")
        forms.append(
            Form(
                action=absolutise(base_url, action) if action else None,
                method=(f.get("method") or "get").lower(),
                fields=fields,
                submit_labels=[s for s in submits if s],
                location=dom_path(f),
            )
        )
    return forms


def _is_cta(node: Tag) -> bool:
    """Heuristic: a CTA is a button, or a link styled/roled as one."""
    if node.name == "button":
        return True
    if node.get("role") == "button":
        return True
    classes = " ".join(node.get("class") or []).lower()
    return any(k in classes for k in ("btn", "button", "cta", "enroll", "buy", "register"))


def parse(html: str, url: str) -> Page:
    raw_soup = BeautifulSoup(html, "lxml")
    soup = _visible_soup(html)
    body = soup.body or soup

    def meta(name: str, attr: str = "name") -> str | None:
        node = raw_soup.find("meta", attrs={attr: re.compile(f"^{re.escape(name)}$", re.I)})
        return node.get("content") if node else None

    og = {
        (m.get("property") or "").lower(): m.get("content", "")
        for m in raw_soup.find_all("meta", attrs={"property": re.compile("^og:", re.I)})
    }
    tw = {
        (m.get("name") or "").lower(): m.get("content", "")
        for m in raw_soup.find_all("meta", attrs={"name": re.compile("^twitter:", re.I)})
    }

    headings: list[dict[str, Any]] = []
    sections: list[Section] = []
    current: Section | None = None
    for node in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]):
        text = clean_text(node.get_text(" "))
        if not text:
            continue
        if node.name.startswith("h") and len(node.name) == 2 and node.name[1].isdigit():
            level = int(node.name[1])
            headings.append({"level": level, "text": text, "location": dom_path(node)})
            current = Section(heading=text, level=level, location=dom_path(node))
            sections.append(current)
        elif current is not None:
            (current.paragraphs if node.name == "p" else current.list_items).append(text)

    tables: list[list[list[str]]] = []
    for table in body.find_all("table"):
        rows: list[list[str]] = []
        for tr in table.find_all("tr"):
            cells = [clean_text(td.get_text(" ")) for td in tr.find_all(["td", "th"])]
            if any(cells):
                rows.append(cells)
        if rows:
            tables.append(rows)

    ctas = [
        {"text": clean_text(n.get_text(" ")), "href": absolutise(url, n.get("href")) or "", "location": dom_path(n)}
        for n in body.find_all(["a", "button"])
        if _is_cta(n) and clean_text(n.get_text(" "))
    ]

    images = [
        {
            "src": absolutise(url, i.get("src") or i.get("data-src") or "") or "",
            "alt": clean_text(i.get("alt")),
            "location": dom_path(i),
        }
        for i in body.find_all("img")
    ]

    canonical_node = raw_soup.find("link", attrs={"rel": re.compile("^canonical$", re.I)})

    return Page(
        url=url,
        title=clean_text(raw_soup.title.get_text()) if raw_soup.title else "",
        meta_description=clean_text(meta("description") or ""),
        canonical=absolutise(url, canonical_node.get("href")) if canonical_node else None,
        lang=(raw_soup.html.get("lang") if raw_soup.html else None),
        robots_meta=meta("robots"),
        open_graph=og,
        twitter=tw,
        json_ld=extract_json_ld(html),
        headings=headings,
        sections=sections,
        paragraphs=[clean_text(p.get_text(" ")) for p in body.find_all("p") if clean_text(p.get_text(" "))],
        list_items=[clean_text(li.get_text(" ")) for li in body.find_all("li") if clean_text(li.get_text(" "))],
        tables=tables,
        ctas=ctas,
        forms=extract_forms(soup, url),
        images=[i for i in images if i["src"]],
        links=extract_links(html, url),
        text=clean_text(body.get_text("\n")),
    )
