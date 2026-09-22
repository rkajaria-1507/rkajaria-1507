# SSEI content audit toolkit

Collects SSEI site content for the FRM landing-page project: a byte-exact HTML
archive, structured JSON, readable markdown, a verbatim FRM occurrence report,
and a structural teardown of the CFA landing page.

> **Status:** the pipeline is complete and tested, but **no SSEI content has
> been collected yet** — the environment it was built in blocks outbound
> requests to `ssei.co.in`. See [Running it](#running-it).

## Design

Four stages, and only the first touches the network:

| Stage | Command | Output |
|---|---|---|
| Archive | `crawl` | `data/page/…`, `data/asset/…`, `manifest.jsonl` |
| Parse | `extract` | `data/structured/*.json`, `data/markdown/*.md`, `index.json` |
| Keyword audit | `keywords` | `keyword-occurrences.{json,md}` |
| Structure | `teardown --url …` | `teardown.{json,md}` |

Separating fetch from parse is deliberate: extraction is where the rules change
most often, and re-parsing the archive costs nothing while re-crawling costs
goodwill with the origin. The archive stores **response bytes**, not decoded
strings — "word for word" is only defensible if what is on disk is what the
server sent. Decoding happens later and the charset used is recorded.

### Correctness details that matter

- **Fetch URL vs dedupe key are distinct.** The URL is sent as discovered;
  canonicalisation (host aliases, tracking-param removal, param ordering)
  applies only to the identity used for "seen this already?". Normalising the
  fetched URL is how crawlers end up requesting pages the server does not serve.
- **Bounded discovery.** A sitemap *index* can fan out to hundreds of nested
  documents; `max_sitemaps` / `max_sitemap_urls` cap it. Found by testing
  against pypi.org, whose index has ~256 nested sitemaps.
- **Atomic page budget.** The `max_pages` slot is reserved *before* the first
  `await`. Checking a counter that increments after I/O lets every concurrent
  worker pass the check at once and overshoot by `concurrency - 1`.
- **Faceted-URL guard.** `/courses?programme=&level=&subjectNames=` is a
  combinatorial, effectively infinite URL space. URLs are collapsed to a
  structural template (`/courses/{int}`, `/courses?[level,programme]`) and
  capped per template, so no hand-maintained blocklist is needed.
- **Politeness.** Token bucket **per host**, `robots.txt` honoured, retries
  with full-jitter exponential backoff, `Retry-After` respected. Without
  jitter, concurrent workers retry in lockstep and recreate the burst that
  caused the 429.
- **Bounded reads.** Bodies stream with a size cap, so one unexpected large
  file cannot exhaust memory.
- **Crash safety.** Bodies are written to a temp file and renamed; the
  manifest is append-only JSONL, so `--resume` picks up after an interruption
  and a torn final line is skipped rather than failing the whole load.
- **Scope safety.** Host matching is dot-anchored, so an allowance for
  `ssei.co.in` does not match `ssei.co.in.attacker.com`.

## Running it

```bash
pip install -r requirements.txt

python -m ssei_scraper --config config/ssei.yaml crawl
python -m ssei_scraper --config config/ssei.yaml extract
python -m ssei_scraper --config config/ssei.yaml keywords
python -m ssei_scraper --config config/ssei.yaml teardown --url https://ssei.co.in/cfa/
```

`crawl --resume` skips anything already archived.

Defaults are deliberately gentle: 1 request/second per host, 3 workers,
`robots.txt` obeyed. Raise them only against an origin you own.

## Tests

```bash
python3 tests/test_pipeline.py
```

Runs fully offline against a fixture page: extraction, the keyword scanner,
the teardown classifier, the CLI end to end, and regression guards for the two
bugs above.

## Configuration

See [`config/ssei.yaml`](config/ssei.yaml). Seeds are annotated with whether
each URL was **confirmed** to exist via search-index recon or is unverified.
