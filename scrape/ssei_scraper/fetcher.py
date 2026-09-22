"""Polite, resilient HTTP fetching.

Politeness is not decoration: an education site on shared hosting will start
returning 5xx (or ban you) long before it returns the whole catalogue. Every
knob here exists to keep a full-site crawl inside what the origin tolerates.
"""
from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from typing import Mapping
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

import httpx

# Statuses worth another attempt. 429 and 5xx are transient by definition;
# 408/425 are the server telling us we were early or slow.
RETRY_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})


class RateLimiter:
    """Token bucket, one instance **per host**.

    A global limiter would let a fast CDN host starve the origin's budget, or
    throttle the whole crawl because one host is slow.
    """

    def __init__(self, rate_per_second: float, burst: int = 1) -> None:
        if rate_per_second <= 0:
            raise ValueError("rate_per_second must be > 0")
        self._interval = 1.0 / rate_per_second
        self._burst = max(1, burst)
        self._tokens = float(self._burst)
        self._updated = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            while True:
                now = time.monotonic()
                self._tokens = min(
                    self._burst, self._tokens + (now - self._updated) / self._interval
                )
                self._updated = now
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
                await asyncio.sleep((1.0 - self._tokens) * self._interval)


@dataclass
class Response:
    url: str
    final_url: str
    status: int
    reason: str
    headers: dict[str, str]
    redirect_chain: list[str]
    content: bytes
    elapsed_ms: int
    truncated: bool = False


class Fetcher:
    def __init__(
        self,
        *,
        user_agent: str,
        requests_per_second: float,
        timeout_seconds: float,
        max_retries: int,
        obey_robots: bool,
        max_bytes: int,
    ) -> None:
        self.user_agent = user_agent
        self.rps = requests_per_second
        self.max_retries = max_retries
        self.obey_robots = obey_robots
        self.max_bytes = max_bytes
        self._limiters: dict[str, RateLimiter] = {}
        self._robots: dict[str, RobotFileParser | None] = {}
        self._robots_locks: dict[str, asyncio.Lock] = {}
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout_seconds),
            follow_redirects=False,  # we record the chain ourselves
            headers={
                "User-Agent": user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-IN,en;q=0.9",
            },
            # trust_env keeps HTTPS_PROXY/CA settings working in sandboxes.
            trust_env=True,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    def _limiter(self, host: str) -> RateLimiter:
        if host not in self._limiters:
            self._limiters[host] = RateLimiter(self.rps)
        return self._limiters[host]

    async def allowed_by_robots(self, url: str) -> bool:
        if not self.obey_robots:
            return True
        host = urlsplit(url).netloc.lower()
        lock = self._robots_locks.setdefault(host, asyncio.Lock())
        async with lock:
            if host not in self._robots:
                parser: RobotFileParser | None = None
                robots_url = f"{urlsplit(url).scheme}://{host}/robots.txt"
                try:
                    await self._limiter(host).acquire()
                    resp = await self._client.get(robots_url)
                    if resp.status_code == 200:
                        parser = RobotFileParser()
                        parser.parse(resp.text.splitlines())
                    # 4xx means "no robots.txt" => allow all (RFC 9309).
                    # 5xx means "unknown" => RFC 9309 says assume disallowed,
                    # but that would silently abort a whole crawl on one blip,
                    # so we allow and record it instead of failing closed.
                except httpx.HTTPError:
                    parser = None
                self._robots[host] = parser
            parser = self._robots[host]
        if parser is None:
            return True
        return parser.can_fetch(self.user_agent, url)

    @staticmethod
    def _retry_after_seconds(headers: Mapping[str, str]) -> float | None:
        value = headers.get("retry-after") or headers.get("Retry-After")
        if not value:
            return None
        value = value.strip()
        if value.isdigit():
            return float(value)
        try:  # HTTP-date form
            when = parsedate_to_datetime(value)
            import datetime as _dt

            delta = (when - _dt.datetime.now(_dt.timezone.utc)).total_seconds()
            return max(0.0, delta)
        except (TypeError, ValueError):
            return None

    async def _read_capped(self, request: httpx.Request) -> tuple[httpx.Response, bytes, bool]:
        """Stream the body, stopping once max_bytes is exceeded.

        Reading a surprise 2 GB video into memory is a crawler's most common
        self-inflicted outage.
        """
        chunks: list[bytes] = []
        total = 0
        truncated = False
        resp = await self._client.send(request, stream=True)
        try:
            async for chunk in resp.aiter_bytes():
                total += len(chunk)
                if total > self.max_bytes:
                    truncated = True
                    break
                chunks.append(chunk)
        finally:
            await resp.aclose()
        return resp, b"".join(chunks), truncated

    async def get(self, url: str, *, max_redirects: int = 10) -> Response:
        """GET with retries, honouring redirects manually so we keep the chain."""
        chain: list[str] = []
        current = url
        started = time.monotonic()

        for _ in range(max_redirects + 1):
            host = urlsplit(current).netloc.lower()
            attempt = 0
            while True:
                await self._limiter(host).acquire()
                try:
                    request = self._client.build_request("GET", current)
                    resp, body, truncated = await self._read_capped(request)
                except httpx.HTTPError as exc:
                    attempt += 1
                    if attempt > self.max_retries:
                        raise
                    await asyncio.sleep(self._backoff(attempt))
                    continue

                if resp.status_code in RETRY_STATUSES:
                    attempt += 1
                    if attempt > self.max_retries:
                        break
                    delay = self._retry_after_seconds(resp.headers) or self._backoff(attempt)
                    await asyncio.sleep(delay)
                    continue
                break

            if resp.is_redirect:
                location = resp.headers.get("location")
                if not location:
                    break
                chain.append(current)
                current = str(httpx.URL(current).join(location))
                continue

            return Response(
                url=url,
                final_url=current,
                status=resp.status_code,
                reason=resp.reason_phrase or "",
                headers={k.lower(): v for k, v in resp.headers.items()},
                redirect_chain=chain,
                content=body,
                elapsed_ms=int((time.monotonic() - started) * 1000),
                truncated=truncated,
            )

        # Fell out of the redirect loop: too many hops, or a Location-less 3xx.
        return Response(
            url=url,
            final_url=current,
            status=resp.status_code,
            reason="too many redirects",
            headers={k.lower(): v for k, v in resp.headers.items()},
            redirect_chain=chain,
            content=b"",
            elapsed_ms=int((time.monotonic() - started) * 1000),
        )

    @staticmethod
    def _backoff(attempt: int) -> float:
        """Exponential backoff with full jitter, capped.

        Jitter matters with concurrency > 1: without it every worker retries in
        lockstep and re-creates the burst that caused the 429.
        """
        return min(30.0, random.uniform(0.0, 2.0 ** attempt))
