"""Declarative crawl configuration (YAML-backed, validated on load)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .urls import UrlPolicy


class ConfigError(ValueError):
    """Raised for a config that would produce a wrong or unsafe crawl."""


@dataclass(frozen=True)
class Config:
    seeds: tuple[str, ...]
    allowed_hosts: frozenset[str]
    host_aliases: dict[str, str]
    drop_params: frozenset[str]
    collapse_trailing_slash: bool

    max_pages: int
    max_depth: int
    max_urls_per_path_template: int
    max_sitemaps: int
    max_sitemap_urls: int

    requests_per_second: float
    concurrency: int
    timeout_seconds: float
    max_retries: int
    user_agent: str
    obey_robots: bool

    fetch_assets: bool
    max_asset_bytes: int
    max_page_bytes: int

    keywords: tuple[str, ...]
    out_dir: Path

    @property
    def url_policy(self) -> UrlPolicy:
        return UrlPolicy(
            allowed_hosts=self.allowed_hosts,
            host_aliases=self.host_aliases,
            drop_params=self.drop_params,
            collapse_trailing_slash=self.collapse_trailing_slash,
        )


def _require(raw: dict[str, Any], key: str) -> Any:
    if key not in raw:
        raise ConfigError(f"missing required config key: {key!r}")
    return raw[key]


def load(path: str | Path, *, out_dir: str | Path | None = None) -> Config:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}

    seeds = tuple(_require(raw, "seeds"))
    if not seeds:
        raise ConfigError("seeds must not be empty")

    allowed = frozenset(h.lower() for h in _require(raw, "allowed_hosts"))
    if not allowed:
        raise ConfigError("allowed_hosts must not be empty -- an unbounded crawl is never what you want")

    aliases = {k.lower(): v.lower() for k, v in (raw.get("host_aliases") or {}).items()}
    # An alias whose target is not itself allowed would silently drop pages
    # from the crawl: every fetched URL folds onto an out-of-scope key.
    for src, dst in aliases.items():
        from .urls import registrable_suffix_match

        if not registrable_suffix_match(dst, allowed):
            raise ConfigError(
                f"host_aliases maps {src!r} -> {dst!r}, but {dst!r} is not in allowed_hosts"
            )

    rps = float(raw.get("requests_per_second", 1.0))
    if rps <= 0:
        raise ConfigError("requests_per_second must be > 0")

    concurrency = int(raw.get("concurrency", 4))
    if concurrency < 1:
        raise ConfigError("concurrency must be >= 1")

    return Config(
        seeds=seeds,
        allowed_hosts=allowed,
        host_aliases=aliases,
        drop_params=frozenset(p.lower() for p in (raw.get("drop_params") or [])),
        collapse_trailing_slash=bool(raw.get("collapse_trailing_slash", False)),
        max_pages=int(raw.get("max_pages", 2000)),
        max_depth=int(raw.get("max_depth", 6)),
        max_urls_per_path_template=int(raw.get("max_urls_per_path_template", 200)),
        max_sitemaps=int(raw.get("max_sitemaps", 50)),
        max_sitemap_urls=int(raw.get("max_sitemap_urls", 10_000)),
        requests_per_second=rps,
        concurrency=concurrency,
        timeout_seconds=float(raw.get("timeout_seconds", 30.0)),
        max_retries=int(raw.get("max_retries", 4)),
        user_agent=str(raw.get("user_agent", "ssei-content-audit/1.0")),
        obey_robots=bool(raw.get("obey_robots", True)),
        fetch_assets=bool(raw.get("fetch_assets", True)),
        max_asset_bytes=int(raw.get("max_asset_bytes", 25 * 1024 * 1024)),
        max_page_bytes=int(raw.get("max_page_bytes", 10 * 1024 * 1024)),
        keywords=tuple(raw.get("keywords") or ["FRM"]),
        out_dir=Path(out_dir or raw.get("out_dir", "data")),
    )
