"""Breadth-first crawl with trap guards and resumability."""
from __future__ import annotations

import asyncio
import re
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urlsplit

import httpx

from .config import Config
from .extract import decode, extract_links
from .fetcher import Fetcher
from .store import Record, Store, utcnow
from .urls import is_asset_path

_NUMERIC = re.compile(r"^\d+$")
_CHARSET = re.compile(r"charset=([A-Za-z0-9_\-]+)", re.IGNORECASE)


def path_template(url: str) -> str:
    """Collapse a URL to a structural template for trap detection.

    ``/courses/195?programme=FRM`` -> ``/courses/{int}?[programme]``

    Faceted navigation (``?programme=&level=&subjectNames=``) multiplies into a
    combinatorial URL space that is effectively infinite. Capping per-template
    keeps a crawl bounded without hand-maintaining a blocklist.
    """
    parts = urlsplit(url)
    segs = [
        "{int}" if _NUMERIC.match(s) else s
        for s in (parts.path or "/").split("/")
    ]
    keys = sorted({k for k, _ in (p.split("=", 1) if "=" in p else (p, "") for p in parts.query.split("&") if p)})
    tmpl = "/".join(segs) or "/"
    return f"{tmpl}?[{','.join(keys)}]" if keys else tmpl


@dataclass
class Task:
    url: str
    depth: int
    discovered_from: str | None


def parse_sitemap(xml_bytes: bytes) -> tuple[list[str], list[str]]:
    """Return (page_urls, nested_sitemap_urls) from a sitemap or sitemap index."""
    pages: list[str] = []
    nested: list[str] = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return pages, nested
    # Sitemaps are namespaced; match on the local tag name to stay robust.
    for elem in root.iter():
        tag = elem.tag.rsplit("}", 1)[-1]
        if tag != "loc" or not (elem.text or "").strip():
            continue
        loc = elem.text.strip()
        # ElementTree exposes no parent pointer, so the document's own root
        # tag decides how to read every <loc> in it.
        if root.tag.rsplit("}", 1)[-1] == "sitemapindex":
            nested.append(loc)
        else:
            pages.append(loc)
    return pages, nested


class Crawler:
    def __init__(self, config: Config, store: Store) -> None:
        self.config = config
        self.store = store
        self.policy = config.url_policy
        self.fetcher = Fetcher(
            user_agent=config.user_agent,
            requests_per_second=config.requests_per_second,
            timeout_seconds=config.timeout_seconds,
            max_retries=config.max_retries,
            obey_robots=config.obey_robots,
            max_bytes=max(config.max_page_bytes, config.max_asset_bytes),
        )
        self.seen: set[str] = set()
        self.template_counts: dict[str, int] = defaultdict(int)
        self.pages_done = 0
        # Slots reserved before fetching. pages_done alone cannot bound the
        # crawl: every worker would pass the budget check during the awaits
        # that precede the first increment, overshooting by up to
        # (concurrency - 1) pages. Reserving is the atomic step.
        self.pages_reserved = 0
        self.assets: set[str] = set()
        self.skipped: list[tuple[str, str]] = []

    async def discover_sitemaps(self) -> list[str]:
        """Seed from sitemap.xml where available -- far cheaper and more
        complete than link-following, and it surfaces orphan pages.

        Hard-bounded on purpose. A sitemap *index* can fan out to hundreds of
        nested sitemaps holding millions of URLs (pypi.org has ~256). Without
        a cap, discovery alone exhausts the run before a single page is
        fetched -- max_pages bounds pages crawled, not documents discovered.
        """
        found: list[str] = []
        fetched = 0
        hosts = {urlsplit(s).netloc for s in self.config.seeds}
        for host in hosts:
            queue = deque([f"https://{host}/sitemap.xml", f"https://{host}/sitemap_index.xml"])
            seen_sm: set[str] = set()
            while queue:
                if fetched >= self.config.max_sitemaps:
                    self.skipped.append((host, f"sitemap cap ({self.config.max_sitemaps}) reached"))
                    break
                if len(found) >= self.config.max_sitemap_urls:
                    self.skipped.append((host, f"sitemap URL cap ({self.config.max_sitemap_urls}) reached"))
                    break
                sm_url = queue.popleft()
                if sm_url in seen_sm:
                    continue
                seen_sm.add(sm_url)
                fetched += 1
                try:
                    resp = await self.fetcher.get(sm_url)
                except httpx.HTTPError as exc:
                    self.skipped.append((sm_url, f"sitemap fetch failed: {exc}"))
                    continue
                if resp.status != 200 or not resp.content:
                    continue
                rel, sha = self.store.write_body(sm_url, resp.content, kind="sitemap")
                self.store.append(
                    Record(
                        url=sm_url, dedupe_key=self.policy.dedupe_key(sm_url),
                        final_url=resp.final_url, status=resp.status, reason=resp.reason,
                        headers=resp.headers, redirect_chain=resp.redirect_chain,
                        content_type=resp.headers.get("content-type", ""), charset=None,
                        body_path=rel, body_sha256=sha, body_bytes=len(resp.content),
                        depth=0, discovered_from=None, fetched_at=utcnow(),
                        elapsed_ms=resp.elapsed_ms, kind="sitemap",
                    )
                )
                pages, nested = parse_sitemap(resp.content)
                room = self.config.max_sitemap_urls - len(found)
                found.extend([p for p in pages if self.policy.in_scope(p)][:room])
                queue.extend(n for n in nested if n not in seen_sm)
        if found:
            print(f"sitemap discovery: {len(found)} URLs from {fetched} sitemap document(s)")
        return found

    def _admit(self, url: str, depth: int) -> bool:
        """Scope, dedupe and trap checks. Returns True if queued."""
        if not self.policy.in_scope(url):
            return False
        key = self.policy.dedupe_key(url)
        if key in self.seen:
            return False
        tmpl = path_template(url)
        if self.template_counts[tmpl] >= self.config.max_urls_per_path_template:
            self.skipped.append((url, f"template cap hit for {tmpl}"))
            return False
        self.seen.add(key)
        self.template_counts[tmpl] += 1
        return True

    async def run(self, *, resume: bool = False) -> None:
        if resume:
            self.seen |= self.store.completed_keys()
            print(f"resume: {len(self.seen)} URLs already archived")

        queue: asyncio.Queue[Task] = asyncio.Queue()
        seeded = 0
        for url in list(self.config.seeds) + await self.discover_sitemaps():
            if self._admit(url, 0):
                queue.put_nowait(Task(url, 0, None))
                seeded += 1
        print(f"seeded {seeded} URLs ({len(self.config.seeds)} configured + sitemap)")

        stop = asyncio.Event()

        async def worker(worker_id: int) -> None:
            while not stop.is_set():
                try:
                    task = await asyncio.wait_for(queue.get(), timeout=2.0)
                except asyncio.TimeoutError:
                    return
                try:
                    await self._process(task, queue, stop)
                except Exception as exc:  # one bad page must not kill the crawl
                    self.store.append(self._error_record(task, exc))
                    print(f"  error {task.url}: {type(exc).__name__}: {exc}")
                finally:
                    queue.task_done()

        workers = [asyncio.create_task(worker(i)) for i in range(self.config.concurrency)]
        await asyncio.gather(*workers)
        await self.fetcher.aclose()
        print(f"done: {self.pages_done} pages, {len(self.assets)} assets, {len(self.skipped)} skipped")

    def _error_record(self, task: Task, exc: Exception) -> Record:
        return Record(
            url=task.url, dedupe_key=self.policy.dedupe_key(task.url), final_url=task.url,
            status=0, reason="", headers={}, redirect_chain=[], content_type="", charset=None,
            body_path=None, body_sha256=None, body_bytes=0, depth=task.depth,
            discovered_from=task.discovered_from, fetched_at=utcnow(), elapsed_ms=0,
            error=f"{type(exc).__name__}: {exc}",
        )

    async def _process(self, task: Task, queue: asyncio.Queue, stop: asyncio.Event) -> None:
        is_asset = is_asset_path(urlsplit(task.url).path)
        if is_asset and not self.config.fetch_assets:
            return

        # Reserve the page slot synchronously, before the first await, so the
        # budget holds no matter how many workers are running. Assets are not
        # charged against max_pages.
        reserved = False
        if not is_asset:
            if self.pages_reserved >= self.config.max_pages:
                stop.set()
                return
            self.pages_reserved += 1
            reserved = True

        if not await self.fetcher.allowed_by_robots(task.url):
            self.skipped.append((task.url, "disallowed by robots.txt"))
            if reserved:
                self.pages_reserved -= 1  # not fetched; give the slot back
            return

        resp = await self.fetcher.get(task.url)
        ctype = resp.headers.get("content-type", "")
        charset_match = _CHARSET.search(ctype)
        kind = "asset" if is_asset or "text/html" not in ctype.lower() else "page"

        body_path = sha = None
        if resp.content:
            body_path, sha = self.store.write_body(task.url, resp.content, kind=kind)

        charset = None
        if kind == "page" and resp.content:
            _, charset = decode(resp.content, charset_match.group(1) if charset_match else None)

        self.store.append(
            Record(
                url=task.url, dedupe_key=self.policy.dedupe_key(task.url),
                final_url=resp.final_url, status=resp.status, reason=resp.reason,
                headers=resp.headers, redirect_chain=resp.redirect_chain,
                content_type=ctype, charset=charset, body_path=body_path,
                body_sha256=sha, body_bytes=len(resp.content), depth=task.depth,
                discovered_from=task.discovered_from, fetched_at=utcnow(),
                elapsed_ms=resp.elapsed_ms, kind=kind,
                notes=["truncated at max_bytes"] if resp.truncated else [],
            )
        )

        if kind == "asset":
            self.assets.add(task.url)
            if reserved:
                self.pages_reserved -= 1  # content-type says it was never a page
            return

        self.pages_done += 1
        print(f"  [{self.pages_done}] {resp.status} d{task.depth} {task.url}")

        if resp.status != 200 or task.depth >= self.config.max_depth or not resp.content:
            return

        html, _ = decode(resp.content, charset_match.group(1) if charset_match else None)
        # Links resolve against the FINAL url: a redirect changes the base.
        for link in extract_links(html, resp.final_url):
            if self._admit(link.href, task.depth + 1):
                queue.put_nowait(Task(link.href, task.depth + 1, task.url))
