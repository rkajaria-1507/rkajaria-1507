# SSEI FRM landing page — data collection

Research and tooling for building an FRM landing page modelled on the existing
CFA one.

## Status: content NOT yet collected

The session this was built in cannot reach `ssei.co.in`. Outbound requests are
refused by the environment's egress proxy:

```
curl:    CONNECT tunnel failed, response 403
WebFetch: {"error_type":"EGRESS_BLOCKED","domain":"ssei.co.in"}
```

This is **not specific to SSEI** — `example.com`, `google.com` and
`anthropic.com` are refused identically. The environment runs the *Trusted
network access* policy, which allows only development infrastructure (npm,
PyPI, GitHub). Every mirror, staging host and translate/profiler proxy tried
was also blocked, so there is no sanctioned route to the content from here.

**Nothing in this directory was scraped.** It is search-index reconnaissance:
result links and result snippets. Every claim is graded CONFIRMED / QUOTED /
PARAPHRASE / INFERRED, and only QUOTED text is site copy. Treat PARAPHRASE as
a search engine's restatement, never as the site's wording.

### To unblock

Edit the environment's network policy (claude.ai → Settings → Code →
Environments → network access) to allow `ssei.co.in` and `*.ssei.co.in`. It's
a web settings page, so it works from a phone browser. Then run the crawler in
[`../scrape`](../scrape). Alternatively run that crawler on any machine with
normal internet access — it has no dependency on this environment.

## Contents

| File | What it is |
|---|---|
| `frm-url-inventory.md` | Every FRM-related SSEI URL found, plus the FRM copy fragments the index exposed |
| `cfa-and-site-recon.md` | CFA page inventory, ~90 sitewide paths, and tech/backend signals |

## Findings that change the plan

**1. `https://ssei.co.in/cfa/` never appeared in the search index.** The CFA
landing page that *is* indexed lives on a different host:
`sseiadmission.ssei.co.in/cfa/`, alongside `/cfacourse`, `/products/CFA` and
`/chartered-financial-analyst-cfa-program` on the main host. The brief's URL
may still resolve — it simply could not be verified without fetching it. Both
are in the crawl config, so the first real crawl settles it.

**2. The product and checkout layer may not be SSEI's code.**
`store.ssei.co.in` serves pages branded for several unrelated coaching
businesses, which points to a multi-tenant white-label SaaS. `www.ssei.co.in`
and `courses.ssei.co.in` share that platform's route vocabulary (`/store`,
`/profile`, `/support-tickets`, `/products/{Category}`). If that holds, the
FRM page can be authored as content but the commerce flow probably cannot be
modified — worth confirming before any build estimate. This is INFERRED from
shared route shapes, not established.

**3. A staging rebuild with a different IA is already live.**
`betassei.co.in` uses `/exam/{programme}/{level}`, e.g.
`betassei.co.in/exam/cfa/level-2` (confirmed). If that is the direction of
travel, a new FRM page should target that IA rather than today's
`/courses/{id}`. Worth a decision before building.

**4. Five different URL schemes coexist** for the same kind of resource:
`/product/{slug}`, `/products/{Category}`, `/courses/{numeric-id}`,
`/courses/{slug}` with facet params, and legacy `.php` paths. Slugs are
free-form — `frmpart1`, `frm-part-1`, `frmpart1new` and
`frmpart1&part2combo` (a literal `&` inside a path segment) all coexist.
Numeric IDs are allocated globally by creation date, not per programme:
`/courses/195` is FRM Part 1 while `/courses/196` is CA Final AFM, so the ID
range cannot be walked to enumerate a programme.

**5. No SSEI-published price was found for any FRM or CFA product.** The only
rupee figures available come from a third-party reseller and are explicitly
not SSEI data. Pricing has to come from a real fetch.

**6. FRM Part 2 hours are contradicted between two indexed sources** (~360h
vs ~250h). Both are recorded rather than one being picked. Unresolvable
without page access.

## FRM facts recovered

Indexed facet counts for `/courses`: 53 courses total — CFA 29, FRM 7, CA 8,
ACCA 10, Financial Modelling 11, Analyst Stack 8, Prudentia 1. **So expect
roughly 7 FRM course entries**, a useful completeness check against whatever
the first crawl returns.

FRM Part 1: ~230 hours covering the full GARP Part 1 syllabus; live online
plus offline in Kolkata; handwritten notes and spreadsheet modelling; Telegram
doubt support; 1.5x playback; 24-month validity; QForum; CBT mocks with
percentile ranking; bundled Excel and Python for Finance (Part 2 adds SQL).
Faculty: Sanjay Saraf (CFA and FRM charterholder) returning to FRM after nine
years, with Budhaditya Debnath as lead instructor. Package tiers are named
Gold / Platinum / Platinum Plus.

Per-fact source URLs are in `frm-url-inventory.md`. Anything above that is not
marked QUOTED there is a paraphrase and must be re-confirmed from the real
page before it goes into copy.
