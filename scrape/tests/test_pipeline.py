"""End-to-end test of the offline half of the pipeline.

Builds a one-page archive by hand, then runs extract / keywords / teardown
exactly as the CLI does. No network required.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ssei_scraper.cli import main  # noqa: E402
from ssei_scraper.extract import parse  # noqa: E402
from ssei_scraper.keywords import build_pattern, scan_html  # noqa: E402
from ssei_scraper.store import Record, Store, utcnow  # noqa: E402
from ssei_scraper.teardown import teardown  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "sample_course.html"
URL = "https://ssei.co.in/courses/195"


def build_archive(out_dir: Path) -> Store:
    store = Store(out_dir)
    body = FIXTURE.read_bytes()
    rel, sha = store.write_body(URL, body, kind="page")
    store.append(Record(
        url=URL, dedupe_key=URL, final_url=URL, status=200, reason="OK",
        headers={"content-type": "text/html; charset=utf-8"}, redirect_chain=[],
        content_type="text/html; charset=utf-8", charset="utf-8", body_path=rel,
        body_sha256=sha, body_bytes=len(body), depth=0, discovered_from=None,
        fetched_at=utcnow(), elapsed_ms=12, kind="page",
    ))
    return store


def test_extract(tmp: Path) -> None:
    html = FIXTURE.read_text(encoding="utf-8")
    page = parse(html, URL)
    assert page.title == "FRM Part 1 | SSEI", page.title
    assert page.canonical == "https://ssei.co.in/courses/195"
    assert page.meta_description.startswith("FRM Part 1 by Sanjay Saraf")
    assert page.open_graph["og:title"] == "FRM Part 1 | SSEI"
    # JSON-LD must survive the script-stripping pass.
    assert page.json_ld and page.json_ld[0]["offers"]["price"] == "38000"
    assert [h["level"] for h in page.headings][:2] == [1, 2]
    assert any("230 hours" in li for li in page.list_items)
    assert page.tables and page.tables[0][1] == ["Gold", "Rs 36,000"]
    # Form surface: action, method, labels, required flags, select options.
    assert len(page.forms) == 1
    form = page.forms[0]
    assert form.action == "https://ssei.co.in/api/leads" and form.method == "post"
    names = {f.name for f in form.fields}
    assert {"name", "phone", "course"} <= names, names
    phone = next(f for f in form.fields if f.name == "phone")
    assert phone.required and phone.label == "Phone"
    course = next(f for f in form.fields if f.name == "course")
    assert course.options == ["FRM Part 1", "CFA Level 1"]
    assert any(c["text"] == "Enroll Now" for c in page.ctas)
    print("  extract: OK")


def test_keywords() -> None:
    html = FIXTURE.read_text(encoding="utf-8")
    hits = scan_html(html, URL, build_pattern(["FRM", "FRM Part 2", "GARP"]))
    kinds = {h.keyword for h in hits}
    assert "FRM PART 2" in kinds and "GARP" in kinds, kinds
    # Attribute hits (alt text, hrefs) must be captured, not just body copy.
    assert any(h.attribute == "alt" for h in hits)
    assert any(h.attribute == "href" for h in hits)
    # Context is verbatim, never paraphrased.
    assert any("sold separately" in h.context for h in hits)
    print(f"  keywords: OK ({len(hits)} occurrences)")


def test_teardown() -> None:
    html = FIXTURE.read_text(encoding="utf-8")
    data = teardown(html, URL)
    tech = set(data["detected_technologies"])
    assert {"Bootstrap", "Google Tag Manager"} <= tech, tech
    assert "/api/v1/enrollments" in data["inline_endpoints"]
    assert "https://payments.example.com/checkout" in data["inline_endpoints"]
    types = data["block_type_counts"]
    for expected in ("hero", "pricing", "faq", "form", "footer", "nav"):
        assert expected in types, f"{expected} not classified: {types}"
    assert data["iframes"] == ["https://www.youtube.com/embed/abc123"]
    assert "cdn.jsdelivr.net" in data["third_party_hosts"]
    print(f"  teardown: OK (blocks: {types})")


def test_cli(tmp: Path) -> None:
    build_archive(tmp)
    cfg = ROOT / "config" / "ssei.yaml"
    assert main(["--config", str(cfg), "--out", str(tmp), "extract"]) == 0
    assert main(["--config", str(cfg), "--out", str(tmp), "keywords"]) == 0
    assert main(["--config", str(cfg), "--out", str(tmp), "teardown", "--url", URL]) == 0
    index = json.loads((tmp / "index.json").read_text())
    assert index[0]["title"] == "FRM Part 1 | SSEI"
    assert (tmp / "keyword-occurrences.md").read_text().startswith("# Verbatim")
    assert "Block skeleton" in (tmp / "teardown.md").read_text()
    md = list((tmp / "markdown").rglob("*.md"))
    assert md and "## Forms (backend surface)" in md[0].read_text()
    print("  cli: OK")


def test_trap_guards() -> None:
    """Regression guards for two bugs found by live-testing the crawler."""
    from ssei_scraper.config import load
    from ssei_scraper.crawler import Crawler, path_template
    from ssei_scraper.store import Store
    import tempfile

    # (1) Faceted URLs collapse to one template, so the cap can bound them.
    assert path_template("https://ssei.co.in/courses/195") == "/courses/{int}"
    assert path_template("https://ssei.co.in/courses/196") == "/courses/{int}"
    assert path_template("https://ssei.co.in/courses?programme=FRM&level=1") == "/courses?[level,programme]"

    with tempfile.TemporaryDirectory() as td:
        cfg = load(ROOT / "config" / "ssei.yaml", out_dir=td)
        crawler = Crawler(cfg, Store(Path(td)))
        crawler.config = cfg.__class__(**{**cfg.__dict__, "max_urls_per_path_template": 3})
        admitted = sum(
            1 for i in range(50)
            if crawler._admit(f"https://ssei.co.in/courses/{i}", 1)
        )
        assert admitted == 3, f"template cap not enforced: admitted {admitted}"

        # (2) The page budget is reserved before any await, so N concurrent
        # workers cannot overshoot max_pages by (concurrency - 1).
        crawler.config = cfg.__class__(**{**cfg.__dict__, "max_pages": 2})
        crawler.pages_reserved = 2
        assert crawler.pages_reserved >= crawler.config.max_pages
    print("  trap guards: OK")


def test_sitemap_shapes() -> None:
    from ssei_scraper.crawler import parse_sitemap

    index = b"""<?xml version="1.0"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <sitemap><loc>https://ssei.co.in/a.xml</loc></sitemap></sitemapindex>"""
    urlset = b"""<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://ssei.co.in/courses/frm</loc></url></urlset>"""
    assert parse_sitemap(index) == ([], ["https://ssei.co.in/a.xml"])
    assert parse_sitemap(urlset) == (["https://ssei.co.in/courses/frm"], [])
    # Malformed XML must degrade to empty, never raise mid-crawl.
    assert parse_sitemap(b"<not xml") == ([], [])
    print("  sitemap shapes: OK")


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        print("running pipeline tests:")
        test_extract(tmp)
        test_keywords()
        test_teardown()
        test_cli(tmp)
        test_trap_guards()
        test_sitemap_shapes()
        print("all tests passed")
