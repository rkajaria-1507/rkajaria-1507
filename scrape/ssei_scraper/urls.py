"""URL normalisation and crawl-scope rules.

Two properties matter here and they are NOT the same thing:

* the **fetch URL** - sent to the server byte-for-byte as discovered, because
  changing it can change the response (or 404 outright);
* the **dedupe key** - a canonical form used only to decide "have we already
  seen this page?".

Conflating the two is the classic crawler bug: you either re-fetch the same
page under a hundred spellings, or you normalise a URL into one the server
does not serve.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

# Schemes we will follow. Anything else (mailto:, tel:, javascript:, data:)
# is a dead end for a crawler but is still worth recording as an outlink.
FOLLOWABLE_SCHEMES = frozenset({"http", "https"})

DEFAULT_PORTS = {"http": 80, "https": 443}

# Path segments that are never worth fetching as HTML.
_ASSET_RE = re.compile(
    r"\.(?:png|jpe?g|gif|webp|avif|svg|ico|bmp|tiff?"
    r"|pdf|docx?|xlsx?|pptx?|csv|zip|rar|7z"
    r"|mp[34]|m4[av]|mov|avi|webm|ogg|wav"
    r"|css|js|mjs|map|woff2?|ttf|eot|otf)$",
    re.IGNORECASE,
)


def is_asset_path(path: str) -> bool:
    return bool(_ASSET_RE.search(path))


def strip_fragment(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit(parts._replace(fragment=""))


def absolutise(base: str, href: str) -> str | None:
    """Resolve *href* against *base*, or None if it is not followable.

    Note: ``urljoin`` already resolves dot-segments, so we do not hand-roll
    that. We only reject schemes we cannot crawl.
    """
    href = (href or "").strip()
    if not href:
        return None
    # Protocol-relative URLs inherit the base scheme; urljoin handles this.
    joined = urljoin(base, href)
    scheme = urlsplit(joined).scheme.lower()
    if scheme not in FOLLOWABLE_SCHEMES:
        return None
    return strip_fragment(joined)


def canonical_host(host: str, aliases: dict[str, str]) -> str:
    """Fold host aliases (``www.ssei.co.in`` -> ``ssei.co.in``).

    Applied to the dedupe key only. The fetch URL keeps the original host,
    because a vhost that merely *usually* mirrors another may not always.
    """
    host = (host or "").lower().rstrip(".")
    return aliases.get(host, host)


def registrable_suffix_match(host: str, allowed: Iterable[str]) -> bool:
    """True if *host* equals, or is a subdomain of, any entry in *allowed*.

    Subdomain matching is anchored on a dot so that ``notssei.co.in`` does not
    match an allowance for ``ssei.co.in``.
    """
    host = (host or "").lower().rstrip(".")
    for entry in allowed:
        entry = entry.lower().lstrip(".")
        if host == entry or host.endswith("." + entry):
            return True
    return False


@dataclass(frozen=True)
class UrlPolicy:
    """Scope + canonicalisation rules for one crawl."""

    allowed_hosts: frozenset[str]
    host_aliases: dict[str, str]
    # Query parameters dropped when building the dedupe key. These are the
    # faceted-navigation parameters that generate an unbounded URL space.
    drop_params: frozenset[str]
    # If True, "/x" and "/x/" collapse to one key. Off by default: a server is
    # free to serve different bodies for the two, and SSEI's own /cfa/ is
    # advertised with the trailing slash.
    collapse_trailing_slash: bool = False

    def in_scope(self, url: str) -> bool:
        parts = urlsplit(url)
        if parts.scheme.lower() not in FOLLOWABLE_SCHEMES:
            return False
        return registrable_suffix_match(parts.hostname or "", self.allowed_hosts)

    def dedupe_key(self, url: str) -> str:
        """Canonical identity of a page, for "have I seen this?" only."""
        parts = urlsplit(url)
        host = canonical_host(parts.hostname or "", self.host_aliases)

        port = parts.port
        netloc = host
        if port is not None and port != DEFAULT_PORTS.get(parts.scheme.lower()):
            netloc = f"{host}:{port}"

        path = parts.path or "/"
        if self.collapse_trailing_slash and len(path) > 1:
            path = path.rstrip("/") or "/"

        # keep_blank_values: "?programme=" carries meaning on this site
        # (it is a real, distinct faceted view), so we must not silently drop
        # empty values -- we drop them by NAME below if configured.
        pairs = [
            (k, v)
            for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if k.lower() not in self.drop_params
        ]
        # Sort for order-independence: ?a=1&b=2 and ?b=2&a=1 are one page.
        query = urlencode(sorted(pairs), doseq=False)

        # Scheme is normalised to https for identity because http:// URLs on
        # this site redirect to https and would otherwise double-count.
        return urlunsplit(("https", netloc, path, query, ""))
