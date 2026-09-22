"""On-disk archive: byte-exact bodies + an append-only manifest.

Fidelity rule: we persist the response **bytes**, never a decoded string.
"Word for word" is only defensible if the artefact on disk is what the server
actually sent; decoding is a lossy, charset-dependent interpretation applied
later and recorded separately.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlsplit, unquote

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass
class Record:
    """One archived HTTP response."""

    url: str                     # URL as fetched
    dedupe_key: str              # canonical identity
    final_url: str               # after redirects
    status: int
    reason: str
    headers: dict[str, str]
    redirect_chain: list[str]
    content_type: str
    charset: str | None
    body_path: str | None        # relative to out_dir
    body_sha256: str | None
    body_bytes: int
    depth: int
    discovered_from: str | None
    fetched_at: str
    elapsed_ms: int
    error: str | None = None
    kind: str = "page"           # page | asset | robots | sitemap
    notes: list[str] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, sort_keys=True)


def safe_relpath(url: str, *, kind: str = "page") -> str:
    """Map a URL to a readable, collision-free relative path.

    Readability is a real requirement (a human greps this tree), but
    readability alone collides: ``/a/b`` and ``/a%2Fb`` flatten to the same
    name, and long or unicode paths blow past filesystem limits. So the name
    is a truncated readable stem plus a hash of the *full* URL.
    """
    parts = urlsplit(url)
    host = (parts.hostname or "unknown").lower()
    path = unquote(parts.path or "/")
    stem = _UNSAFE.sub("-", path).strip("-") or "index"
    if parts.query:
        stem = f"{stem}--{_UNSAFE.sub('-', unquote(parts.query)).strip('-')}"
    stem = stem[:120]
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    ext = ".html" if kind == "page" else ""
    if kind in {"robots", "sitemap"}:
        ext = ".txt" if kind == "robots" else ".xml"
    return f"{kind}/{host}/{stem}.{digest}{ext}"


def _atomic_write(target: Path, data: bytes) -> None:
    """Write via a temp file in the same directory, then rename.

    A crawl is long and interruptible; a half-written body that still looks
    complete would poison every later parse.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(target.parent), suffix=".part")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, target)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


class Store:
    def __init__(self, out_dir: Path) -> None:
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.out_dir / "manifest.jsonl"

    def write_body(self, url: str, data: bytes, *, kind: str = "page") -> tuple[str, str]:
        rel = safe_relpath(url, kind=kind)
        _atomic_write(self.out_dir / rel, data)
        return rel, hashlib.sha256(data).hexdigest()

    def append(self, record: Record) -> None:
        with self.manifest_path.open("a", encoding="utf-8") as fh:
            fh.write(record.to_json() + "\n")
            fh.flush()

    def read_manifest(self) -> Iterator[dict[str, Any]]:
        if not self.manifest_path.exists():
            return iter(())
        def _gen() -> Iterator[dict[str, Any]]:
            with self.manifest_path.open("r", encoding="utf-8") as fh:
                for line_no, line in enumerate(fh, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        # A torn final line from a killed run is recoverable;
                        # refusing to load the whole manifest is not.
                        print(f"warning: skipping malformed manifest line {line_no}")
        return _gen()

    def completed_keys(self) -> set[str]:
        """Dedupe keys already fetched successfully -- powers --resume."""
        return {
            row["dedupe_key"]
            for row in self.read_manifest()
            if row.get("error") is None and row.get("body_path")
        }


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")
