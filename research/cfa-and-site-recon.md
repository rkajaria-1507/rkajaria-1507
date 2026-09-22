# SSEI CFA Landing Page + Sitewide Recon (WebSearch-only)

**Date:** 2026-09-22
**Method:** `WebSearch` only. All direct HTTP access was blocked.
**Blocked hosts confirmed this session (EGRESS_BLOCKED / 403):**
`ssei.co.in`, `courses.ssei.co.in`, `www.sanjaysaraf.com`, `cfa.sanjaysaraf.com`,
`ssei-beta.vercel.app`, `betassei.co.in`, `www-ssei-co-in.translate.goog`,
`website.informer.com`, `ssei.co.in.usitestat.com`.
→ The egress block is **broader than the two hosts named in the brief**: every mirror,
staging host, translate-proxy and third-party site-profiler I tried was also blocked.
No DOM/HTML was ever retrieved. Everything below comes from search-result titles,
URLs, and the search engine's summarisation of indexed page text.

**Evidence grading used throughout:**
- **CONFIRMED** — the URL was returned by a search engine as an actual indexed result
  (title + URL pair). The URL exists / existed and was crawlable.
- **QUOTED** — text the search engine surfaced as page content, attributed to a URL.
  Reliable as *indexed text*, but I could not verify it byte-for-byte against the live DOM.
- **PARAPHRASE** — the search tool's own restatement, not page text.
- **INFERRED** — my reasoning. Never treat as fact.

---

## 1. CFA URL inventory

### 1.1 Primary CFA hub / landing pages

| URL | Indexed title | Status | Source query |
|---|---|---|---|
| `https://www.ssei.co.in/products/CFA` | "Explore CFA Products \| SSEI" | **CONFIRMED** | `site:ssei.co.in CFA` |
| `https://courses.ssei.co.in/products/CFA` | "Explore CFA Products \| SSEI" | **CONFIRMED** | `site:courses.ssei.co.in` |
| `https://www.ssei.co.in/cfacourse` | "Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI" | **CONFIRMED** | `ssei.co.in/cfa Sanjay Saraf CFA course` |
| `https://www.ssei.co.in/s/cfacourse` | "Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI" | **CONFIRMED** | `ssei.co.in cfacourse "Catalyzing careers…"` |
| `https://www.ssei.co.in/chartered-financial-analyst-cfa-program` | "Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI" | **CONFIRMED** | `"ssei.co.in/cfa" CFA landing page` |
| `https://www.ssei.co.in/battleground-finance-cfa-vs-frm` | "Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI" | **CONFIRMED** | `site:ssei.co.in FRM` |
| `https://www.ssei.co.in/cfa-institute-eligibility-norm-for-cfa-level-1` | "Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI" | **CONFIRMED** | `sseiadmission… enquiry form` |
| `https://www.ssei.co.in/courses/cfa-coaching-classes-in-kolkata` | "Sanjay Saraf Educational Institute (SSEI)" | **CONFIRMED** | `ssei.co.in/cfa Sanjay Saraf CFA course` |

> **Note on the brief's target URL `https://ssei.co.in/cfa/`:** I never saw
> `ssei.co.in/cfa` or `ssei.co.in/cfa/` returned as an indexed result in ~26 queries.
> What *does* exist and is indexed is `sseiadmission.ssei.co.in/cfa/` (below) plus the
> `/cfacourse`, `/s/cfacourse` and `/products/CFA` routes on the apex/www host.
> Whether `ssei.co.in/cfa/` is a live route, a redirect, or 404 is **UNVERIFIED**.

### 1.2 CFA campaign / admission subdomain landers (closest analogue to a "CFA landing page")

| URL | Indexed title | Status |
|---|---|---|
| `https://sseiadmission.ssei.co.in/cfa/` | "CFA Level 1" | **CONFIRMED** |
| `https://sseiadmission.ssei.co.in/cfa2/` | "Jump Into CFA Level 2 Prep" | **CONFIRMED** |
| `https://cfaresults.ssei.co.in/` | "Your CFA Result Is Here \| Personalized Blueprint & Guidance \| SSEI" | **CONFIRMED** |
| `https://cfa.sanjaysaraf.com/CFA` | "Finance Futures Start Here" | **CONFIRMED** |
| `https://betassei.co.in/exam/cfa/level-2` | "CFA Level II Course - SSEI" | **CONFIRMED** |

Source queries: `site:ssei.co.in CFA`, `site:sseiadmission.ssei.co.in`, `site:sanjaysaraf.com courses`, `site:betassei.co.in`.

### 1.3 CFA course pages — numeric `/courses/{id}` scheme

All **CONFIRMED** (each appeared as an indexed result on `www.ssei.co.in` and/or `ssei.co.in`):

| ID | Indexed title |
|---|---|
| 113 | "CFA Level 1 Coaching \| Full Immersion Course \| SSEI" / "CFA Level 1 - Full Immersion - Learn the Language of …" |
| 117 | "CFA Level 1 Full Immersion (for CA / CMA / MBA Finance Students) - Your Finance Background Meets Structured CFA Preparation" |
| 118 | "CFA Level 1 - Fast Track / Review Class" |
| 121 | "CFA Level 2 - Full Immersion - Turn Complex Cases Into Clear Decisions" |
| 122 | "CFA Level 2 - Review Class - Make Your Final Revision Count" |
| 139 | "CFA Level 1 for Engineers / Eco / Stats / Maths Honours …" |
| 141 | "CFA Level 3 Common Core - Prepare for the Final …" |
| 160 | "CFA Level 3 & Analyst Stack Combo" |
| 199 | "CFA Level 2 - Partial Topics" |
| 202 | "CFA Level 3 - Partial Topics" |
| 205 | "CFA Level 1 Coaching \| Accelerate Batch \| SSEI" |

Non-CFA IDs seen in the same namespace (useful for range inference): **125** CA Final AFM,
**161** CA Final AFM & Analyst Stack Combo, **172** Financial Modeling & Valuation,
**195** FRM Part 1, **196** CA Final AFM Fast Track.
→ **INFERRED:** IDs are a single flat sequence across all programmes, roughly 113–205+,
so FRM pages will be sparse integers in that same range, not a separate series.
Only 195 is confirmed for FRM.

### 1.4 CFA commerce pages — `/product/{slug}` scheme

All **CONFIRMED** as indexed results. Host varies between `www.ssei.co.in`,
`ssei.co.in` and `courses.ssei.co.in` — the same slug appears under multiple hosts.

Level 1:
- `/product/cfa-level-1` — "All Courses" (also on `courses.ssei.co.in`)
- `/product/cfa-level-1-review-class` (on `courses.ssei.co.in`) — "CFA Level 1 - Review Class"
- `/product/cfal1-returningstudentmodule` — "CFA Level 1 - Returning Student Module"
- `/product/cfal1accelerateprogram` — "CFA Level 1 Accelerate Program | SSEI"
- `/product/engcfal1` — "CFA Level 1 - Special CFA Level 1 Batch for Engineers/ Eco Honours/ Stats Honours/ Maths Honours Students | SSEI"
- `/product/cfa-level-1-for-ca-cma-cs-mba-finance-students` — "CFA Level 1 for CA / CMA / MBA Finance Students"
- `/product/newbatch2026` — "CFA Level 1 LIVE 2026 - New Batch starts 15th Sep'25"
- `/product/cfal1_books` — "CFA Level 1 2026 Books | SSEI"
- `/product/cfal1extension` — "Ssei"

Level 2:
- `/product/cfa-level-2` — "CFA Level 2"
- `/product/cfa-level-2-partial-topics` — "Ssei"
- `/product/cfa-level-2-review-class` — "CFA Level 2 - Review Class | SSEI"
- `/product/cfal2` — "CFA Level 2 starts 15th Oct'25 | SSEI"
- `/product/cfal2newbatch` — "CFA Level 2 - Full Immersion - Turn Complex Cases Into Clear Decisions"
- `/product/cfal2-provisional` — "CFA Level 2 - Provisional | SSEI"
- `/product/cfal2-balance-payment` — "CFA Level 2 - Balance Payment | SSEI"

Level 3:
- `/product/cfal3` — "CFA Level 3 Common Core with Specialized Pathway Portfolio Management for 2026/2027 New Entry Window - 26th July'26 | SSEI"
- `/product/cfal3-commoncore2025` — "CFA Level 3 Common Core for 2025"
- `/product/cfal3-commoncore2026` — "Ssei"
- `/product/cfalevel3commoncorewithpm2025`
- `/product/cfa-level-3-partial-topics` — "CFA Level 3 - Partial Topics | SSEI"
- `/product/cfal3-balance-payment` — "CFA Level 3 - Balance Payment | SSEI"

Cross-level / admin SKUs:
- `/product/cfal2-l3extension` — "Validity Extension - CFA Level 2 & CFA Level 3 | SSEI"
- `/product/cfal1and2packageupdation` — "Package Updation - CFA Level 1 & CFA Level 2 | SSEI"

→ **INFERRED (high confidence):** slug convention is inconsistent by design — hand-authored
per campaign (`cfal2newbatch`, `newbatch2026`, `cfal3-commoncore2026`), i.e. a marketer
creates a new product record per batch rather than versioning one page. Expect the same
for FRM.

### 1.5 CFA-adjacent blog URLs (`/blogs/{Title-Case-Slug}`) — all **CONFIRMED**

- `/blogs/Why-Consider-CFA-Over-CA`
- `/blogs/Why-does-it-make-sense-to-pursue-the-CFA-Program-right-after-school`
- `/blogs/Why-CA-Students-Should-Pursue-the-CFA-Program-Post-Intermediate-Exams`
- `/blogs/A-Strategic-Approach-for-Indian-Students`
- `/blogs/Exploring-Careers-in-Finance-Hierarchies-Roles-and-Certifications`
- `/blogs/Global-Exams-Experience-Exam-Tips`
- `/blogs/Allegations-and-Market-Manipulation-Analyzing-Rahul-Gandhis-Claims`
- `/blogs/Cherry-Picking-is-Dangerous-in-Education`
- `/blogs/The-Road-Less-Travelled`

Note the slug casing: hyphenated **Title Case**, not lowercase. Load-bearing if rebuilding routing.

---

## 2. CFA page content fragments

Everything here is **QUOTED** = surfaced by the search engine as indexed page text.
It is *not* verified against the live DOM. Anything I restate is marked PARAPHRASE.

### From `www.ssei.co.in/` (home)
- QUOTED (meta title): "SSEI: Sanjay Saraf Educational Institute - CA, CFA & FRM Coaching"
- QUOTED: "SSEI offers expert-led CA, CFA and FRM coaching with live and recorded classes, top faculty and proven exam results."
- QUOTED: "Sanjay Saraf Sir … began teaching at 16, and turned that passion into one of India's most trusted finance prep institutes."
- QUOTED: "nationwide presence across 100+ locations"

### From `www.ssei.co.in/products/CFA` ("Explore CFA Products | SSEI")
- QUOTED: "CFA Programs built for the next phase of your CFA journey"
- QUOTED: "Level 2 and Level 3 programs are designed for deeper application, sharper thinking, and exam-focused mastery."

### From `www.ssei.co.in/courses/113` (CFA Level 1 — Full Immersion)
- QUOTED (title): "CFA Level 1 Coaching | Full Immersion Course | SSEI"
- QUOTED (alt title seen in another result): "CFA Level 1 - Full Immersion - Learn the Language of …" (truncated by SERP)
- QUOTED: "a complete preparation program covering the full syllabus through detailed concept teaching, structured practice, revision support, and mock preparation"
- QUOTED: "600+ hour live-led programme with daily live classes — best for first-time candidates who want maximum repetition and live cadence."
- QUOTED: "You can watch the complete course content for up to one-and-a-half times of its total class duration."
- QUOTED: "Sanjay Saraf Sir brings over 30+ years of teaching depth, Budhaditya Sir adds the market lens, and Anurag Sir brings experience from Big Four consulting and investment banking."
- PARAPHRASE: the page has an "upcoming batches" element; specific dates were not surfaced.

### From `ssei.co.in/courses/205` (CFA Level 1 — Accelerate Batch)
- QUOTED (title): "CFA Level 1 Coaching | Accelerate Batch | SSEI"
- QUOTED: "self-paced under-300-hour route compressed into a focused study roadmap, with weekend live problem-solving workshops instead of daily live classes"
- QUOTED (from `/product/cfal1accelerateprogram`): "The CFA L1 Accelerate Program is SSEI's self-paced route to CFA Level 1, built specifically for working professionals, career-switchers, and serious aspirants who cannot commit to a fixed live batch schedule."
- QUOTED: "the complete library of acclaimed live-taught video lectures—under 300 hours that have powered hundreds of CFA L1 passes, restructured into a guided, week-by-week study roadmap."
- QUOTED: "You study on your own time, at your own pace, and every weekend you join a live problem-solving workshop where faculty works through practice questions on exactly the topics the roadmap assigned that week."

### From `www.ssei.co.in/courses/117` (L1 for CA/CMA/MBA Finance)
- QUOTED (title): "CFA Level 1 Full Immersion (for CA / CMA / MBA Finance Students) - Your Finance Background Meets Structured CFA Preparation"
- QUOTED: "designed for students who already have a background in accounting, finance, or business."

### From `www.ssei.co.in/courses/118` / `/cfacourse` (Fast Track framing)
- QUOTED: "Ideal for students who have limited time before the exam, are repeating the subject, already have a basic understanding of the CFA Program, or prefer quick and focused revisions over detailed concept-building sessions."
- QUOTED: "While the Regular Batch focuses on in-depth, foundational learning, the Fast Track Batch is more exam-oriented."

### From `www.ssei.co.in/cfacourse` and `/s/cfacourse` (CFA programme hub)
- QUOTED: "anyone serious about a career in finance — including fresh graduates, working professionals, CA/CMA/MBA students, or STEM graduates looking to transition, with no prior finance background needed for Level 1."
- QUOTED: "CFA Institute offers four examination windows annually: February, May, August, and November"
- QUOTED: "SSEI's curriculum, materials, and methodology are verified by CFA Institute"
- QUOTED: "Flexible EMI plans are available."
- QUOTED (contact CTA): "+91 7595053300" / WhatsApp

### From `/courses/121`, `/courses/122`, `/product/cfa-level-2*` (Level 2)
- QUOTED (title 121): "CFA Level 2 - Full Immersion - Turn Complex Cases Into Clear Decisions"
- QUOTED (title 122): "CFA Level 2 - Review Class - Make Your Final Revision Count"
- QUOTED: "The batch includes conceptual lectures, summary notes, intense application of SSEI's Segment and Strike approach to solving any item set, multiple item set solving, topicwise tests, mock exams, and regular performance tracking."
- QUOTED: "approximately 100 hours of core learning content"
- QUOTED: "SSEI provides two hard-copy books of topic-wise mock tests"

### From `/courses/202` + `/product/cfa-level-3-partial-topics` (Level 3 Partial Topics)
- QUOTED: "CFA Level 3 Partial Topics is SSEI's flexible option for students who do not need the full Level 3 course. Choose only the topics you want, from Portfolio Management, Equity, Fixed Income, or all 12 topics."

### From `sseiadmission.ssei.co.in/cfa/`
- QUOTED: "approximately 125 hours of core learning content with conceptually explained learning objectives and readings"
- QUOTED: "structured, weekly classes with timely syllabus completion"
- QUOTED: "SSEI CFA Level 1 students are eligible for 20% off on course fees"
- QUOTED: "SSEI's Level 1 batch is structured to be flexible for working candidates with weekend or evening access and recorded sessions available 24/7."
- QUOTED: "100+ locations in India offering both domestic and Indian and international qualifications"

### From `/product/engcfal1` (Engineers/Eco/Stats/Maths batch) — package tiering
- QUOTED: "~505 hours of core learning content in Gold Package & 562 hours in Platinum & Platinum Plus Package"
→ **CONFIRMED package-tier naming: Gold / Platinum / Platinum Plus.** Reusable for FRM.

### Testimonials (surfaced against `betassei.co.in/exam/cfa/level-2`)
- QUOTED: "All I studied was the study material provided by SSEI, and what was taught in class was enough to help me clear all 3 CFA levels."
- QUOTED: "The classes and mocks from SSEI were extremely helpful and gave me the confidence and support I needed to clear CFA Level I."

### Pricing
- **No SSEI rupee price for any CFA product was ever surfaced.** One third-party
  (`cfapoint.com`) mentioned ₹10,000–₹40,000 for a 9-Mar-2026 L1 batch incl. material —
  **third-party, unverified, do not rely on it.**
- Every USD figure found (USD 1,140 / 1,490 / 1,240 / 1,590) is **CFA Institute exam
  registration fee**, explicitly stated by SSEI as "paid to CFA Institute and …
  independent of any SSEI programme fee."
- `/courses` filter buckets do expose the price ladder → see §3.

### Compliance / legal copy worth mirroring on an FRM page
- QUOTED: "Testimonials, results, salary references, student stories, or success examples shown on the website are individual outcomes and should not be treated as guarantees."
- QUOTED (refund): "Purchases … cannot be cancelled or refunded … except for delivery failures within 15 days from the committed shipment date"; "refunds cannot be provided for validity extensions under any circumstances."

---

## 3. Sitewide structure

### 3.1 Hosts

**`ssei.co.in` apex + `www.ssei.co.in`** — both serve the same paths; search results mix them
freely. **INFERRED:** one canonicalises to the other; which direction is UNVERIFIED.

**Subdomains — all CONFIRMED (each returned at least one indexed page):**

| Host | Role (from indexed titles) |
|---|---|
| `courses.ssei.co.in` | Commerce/LMS storefront. Serves `/`, `/store`, `/contact`, `/refund`, `/products/{Cat}`, `/product/{slug}`, `/s/{slug}` — **the same path shapes as www**. |
| `sseiadmission.ssei.co.in` | Campaign landers: `/cfa/`, `/cfa2/` |
| `sseischolarship.ssei.co.in` | "SSEI Scholarship Exam"; also `/terms.pdf` (static PDF) |
| `cfaresults.ssei.co.in` | "Your CFA Result Is Here \| Personalized Blueprint & Guidance" |
| `analyststack.ssei.co.in` | "SSEI Analyst Stack - Transform Your Finance Career" |
| `fixmycv.ssei.co.in` | "FixMyCV — by SSEI" |
| `store.ssei.co.in` | Multi-brand store — see §4, this one is the biggest tech tell |

**Related domains (CONFIRMED):**
`sanjaysaraf.com` / `www.sanjaysaraf.com` (mirrors www paths incl. `/courses/113`),
`cfa.sanjaysaraf.com`, `sseimarkets.com` / `www.sseimarkets.com`, `courses.sseimarkets.com`,
`forum.sseiqforum.com`, `mocktest.sseiqforum.com`, `ulurn.in`,
`betassei.co.in` + `lms.betassei.co.in`, `ssei-beta.vercel.app`.

### 3.2 Path patterns on `ssei.co.in` / `www.ssei.co.in`

**A. Top-level site pages** (all CONFIRMED)
```
/                         SSEI: Sanjay Saraf Educational Institute - CA, CFA & FRM Coaching
/about                    About Us | SSEI
/profile                  Sanjay Saraf Educational Institute (SSEI)
/courses                  All Courses
/blogs                    SSEI Blog: Finance Writing for CFA, FRM & CA Aspirants / "Our Blogs"
/contact-us               Contact SSEI | Speak to Counsellors, Visit Kolkata, Mumbai, or Delhi
/address                  Address List | SSEI
/centre-locator           (default title)
/faculty                  (default title)
/happy-students           (default title)
/mock-tests               SSEI Mock Tests. Full-length CBT Mocks for CFA, FRM, CA Final
/privacy                  Privacy Policy | SSEI
/terms                    Terms and Conditions | SSEI
/terms-and-conditions     Terms and Conditions | SSEI      ← duplicate of /terms
/resources/               Resources | SSEI SSEI            ← trailing slash, doubled title
/contact.php              (default title)                  ← legacy extension, see §4
```

**B. Legacy/WordPress-shaped article slug** (CONFIRMED, 1 example)
```
/top-five-businesses-accounting-and-bookkeeping-blogs-you-should-be-following-online/
```

**C. Course catalogue — numeric** `/courses/{int}` (CONFIRMED, 16 distinct IDs)
```
113 117 118 121 122 125 139 141 160 161 172 195 196 199 202 205
```

**D. Course catalogue — slug** `/courses/{slug}` (CONFIRMED)
```
/courses/frm                                   Sanjay Saraf Educational Institute (SSEI)
/courses/cfa-coaching-classes-in-kolkata       (SEO/local landing page)
```
→ **INFERRED:** `/courses/frm` is the FRM programme hub and the direct structural analogue
of `/cfacourse` / `/products/CFA`. Best starting model for a new FRM landing page.
`/courses/cfa-coaching-classes-in-kolkata` shows an SEO-geo variant exists —
an FRM equivalent (`/courses/frm-coaching-classes-in-kolkata`) is **INFERRED, unverified**.

**E. Course catalogue — filtered list** (CONFIRMED URL)
```
/courses?level=cfa-level-1&programme=cfa
```
Indexed facet data from `/courses` (**QUOTED**):
- "53 total courses"
- Programme: CFA (29), FRM (7), CA (8), ACCA (10), Financial Modelling (11), Analyst Stack (8), Prudentia (1)
  *(counts sum to 74 > 53 → courses carry multiple programme tags)*
- Mode: Live + Recorded / Recorded Only / Live Only
- Course Type: Full Course / Partial Topics / Fast-track / Combos / Books / Validity Extension
- Price: ₹<15k / ₹15k–₹30k / ₹30k–₹50k / ₹50k+
- Batch Type: New Batches Only
- Sort: Recommended / Most popular / Newest first / Price (Low to High) / Price (High to Low)
→ Query params `?level=` and `?programme=` are CONFIRMED; `mode`, `type`, `price`,
`sort` param names are **INFERRED**.

**F. Product category listing** `/products/{Category}` — URL-encoded spaces (CONFIRMED)
```
/products/CFA
/products/FRM
/products/CA%20Final
/products/CA%20Inter
/products/Analyst%20Stack
```
On `store.ssei.co.in` the same route takes filter params (CONFIRMED):
```
/products/CA%20Final?authorNames=CA+Sankalp+Kanstiya&page=2
/products/CA%20Inter?subjectNames=FM,Cost&authorNames=CA+Sankalp+Kanstiya
/products/CA%20Final?subjectNames=Law,Audit&authorNames=CA+Manan+Pujara,CA+Karan+Kumar,Shubham+Keswani
```
→ Params: `subjectNames` (comma-joined), `authorNames` (comma-joined, `+`-encoded), `page`.

**G. Product detail** `/product/{slug}` — the single largest namespace. Non-CFA examples (CONFIRMED):
```
FRM:  /product/frmpart1              /product/frmpart1new
      /product/frmpart2              /product/frm-part-2
      /product/frm-part-1
      /product/frmpart1&part2combo   ← literal "&" inside the slug
      /product/frmpart1-returningstudent-module
      /product/frm-part-1-for-cfa-students
      /product/frm-stock-market
CA:   /product/ca-inter-fm           /product/cainterextension
      /product/cafinalafmnewbatch    /product/newbatchcafinalafm
      /product/ca_final_afm_regular  ← underscores, not hyphens
      /product/ca-final-afm-revision /product/ca-final-afm-updates
      /product/ca-final-afm-fast-track
      /product/cafinalextension
AS:   /product/liveonlineanalyststack
```
→ **Slug conventions are wildly inconsistent** (hyphen / none / underscore / `&`).
Strong evidence slugs are free-text fields, not generated.

**H. Blog detail** `/blogs/{Hyphenated-Title-Case}` — see §1.5.

**I. `/s/{slug}` alias namespace** (CONFIRMED, 2 examples)
```
www.ssei.co.in/s/cfacourse
courses.ssei.co.in/s/ca        "Best Positive NPV Coaching Classes by Sanjay Saraf : SSEI"
```
→ **INFERRED:** `/s/` = marketing "sections"/landing pages; `/cfacourse` and `/s/cfacourse`
are likely the same page served at both a bare and prefixed path.
**INFERRED, unverified:** an `/s/frm` or `/s/frmcourse` may exist.

**J. Free-slug marketing/SEO pages at root** (CONFIRMED)
```
/cfacourse
/chartered-financial-analyst-cfa-program
/battleground-finance-cfa-vs-frm
/cfa-institute-eligibility-norm-for-cfa-level-1
/centre-locator  /faculty  /happy-students
```
All share the **generic title** "Catalyzing careers, transforming lives by Sanjay Saraf | SSEI".

**K. Commerce/account routes — confirmed on `store.ssei.co.in`, same shape on `courses.`**
```
/store             /profile           /courses (= "My Enrollments")
/support-tickets   /contact           /refund
```

### 3.3 `betassei.co.in` — the next-generation route scheme (CONFIRMED)

```
https://betassei.co.in/
https://betassei.co.in/courses
https://betassei.co.in/exam/cfa/level-2      "CFA Level II Course - SSEI"
https://lms.betassei.co.in/                  "SSEI"
```
→ **This is the single most useful structural finding for a rebuild.** The staging site
uses `/exam/{programme}/{level}` instead of `/courses/{int}`.
**INFERRED (high confidence, unverified):** the FRM analogues are
`/exam/frm/part-1` and `/exam/frm/part-2`, and CFA is `/exam/cfa/level-1|2|3`.
QUOTED content indexed under betassei:
- "Sanjay Saraf Educational Institute (SSEI), an official CFA Institute Prep Provider, offers focused CFA Level 2 coaching designed to help you build strong fundamentals and ace the exam with confidence."
- "complete GARP-aligned program that builds crystal-clear concepts, exam-focused preparation, and practical problem-solving to help you clear both levels with confidence" (FRM)
- "blends clear explanations with case-based practice and strategy to help students clear the exam on their first attempt" (FRM Part 2)
- "FRM Part I and FRM Part II admissions are ongoing"; "new CFA Level 2 batch starting on November 24th"

### 3.4 `sanjaysaraf.com` — mirror with extra routes (CONFIRMED)
```
/                 /about        /blogs        /courses/113
/tools            "Free Finance Resources & Career Tools | SSEI"
/events           "SSEI Events — Workshops, Webinars, Mock-Test Days & City Meetups"
/faculties        "Our Faculty"
/media            "SSEI Media — Press Coverage, YouTube Appearances & Awards"
/partner          "Partner With SSEI — Franchise & Institutional Partnerships"
```
→ **INFERRED (medium-high):** `sanjaysaraf.com` and `ssei.co.in` serve the **same
application** (identical `/courses/113` route and title). So `/tools`, `/events`,
`/faculties`, `/media`, `/partner` very likely exist on `ssei.co.in` too — but I only
CONFIRMED them on the `sanjaysaraf.com` host. Note `/faculties` (sanjaysaraf) vs
`/faculty` (ssei.co.in) — both indexed; possibly a rename in flight.

### 3.5 FRM inventory found (target-relevant)
```
CONFIRMED pages:
  /courses/frm                                    programme hub
  /courses/195                                    "FRM Part 1"
  /products/FRM                                   "Explore FRM Products | SSEI"
  /product/frmpart1, /product/frmpart1new, /product/frm-part-1
  /product/frmpart2, /product/frm-part-2
  /product/frmpart1&part2combo
  /product/frmpart1-returningstudent-module
  /product/frm-part-1-for-cfa-students
  /product/frm-stock-market
  /blogs/Global-Exams-Experience-Exam-Tips
  /battleground-finance-cfa-vs-frm
  https://www.garp.org/frm/exam-preparation-provider/sanjay-saraf-educational-institute  (external)
  https://www.garp.org/rai/exam-preparation-provider/sanjay-saraf-educational-institute  (external)
NOT FOUND (no indexed result):
  a /courses/{id} page for FRM Part 2
  an /frm or /frmcourse root lander equivalent to /cfacourse
```
QUOTED FRM copy worth reusing:
- "After 9 years, Sanjay Saraf Sir returns to teach FRM" / "No concept is too complex to explain."
- "the full GARP Part 1 syllabus in around 230 hours"
- "delivered live online and offline in Kolkata, with handwritten notes, spreadsheet-based modeling, and Telegram doubt support"
- "Lectures, Handwritten Notes, Spreadsheets, Question Solving, Building Blocks, Complementary FREE courses: Basic & Advanced Excel, Python For Finance"
- "Privileged Access of Full CBT Mock at Qforum with a State-of-the-art CBT Interface that mimics the actual exam with %ile ranking"
- "Budhaditya Debnath Sir brings experience from equity research and portfolio management"
- FRM phone: "+917595053300"; Stock Market: "+91 7595052200"

---

## 4. Tech / backend signals

**Everything in this section is INFERENCE from public artefacts.** No HTML, header,
JS bundle or API response was retrieved. Confidence is stated per signal.

### 4.1 `ssei-beta.vercel.app` exists — **CONFIRMED artefact, INFERRED meaning**
An indexed page titled "Sanjay Saraf Educational Institute" lives at
`https://ssei-beta.vercel.app/`.
- Confidence the marketing site is deployed on **Vercel**: **medium-high**. A
  `*.vercel.app` preview carrying SSEI's own branding is close to conclusive that
  Vercel is in the build/deploy pipeline.
- Confidence the framework is **Next.js**: **low-medium**. Vercel is Next.js's vendor
  and its overwhelmingly common payload, but Vercel also hosts Vite/Astro/Remix/SvelteKit.
  **I saw zero `_next/`, `__NEXT_DATA__`, or build-id evidence. Do not state Next.js as fact.**

### 4.2 `betassei.co.in` + `lms.betassei.co.in` — **CONFIRMED artefacts**
A separate, publicly crawlable staging environment on its own domain, with a different
IA (`/exam/{programme}/{level}`) and a split marketing-vs-LMS host.
- Confidence there is an active site rebuild in flight: **high**.
- Confidence the new IA will ship as `/exam/...`: **medium** (it is staging; may change).

### 4.3 The generic `<title>` fallback — **INFERRED, medium confidence**
Many structurally distinct routes (`/cfacourse`, `/faculty`, `/centre-locator`,
`/happy-students`, `/battleground-finance-cfa-vs-frm`, `/chartered-financial-analyst-cfa-program`,
`/product/frmpart1`, `/product/cfal2-provisional`, `/contact.php`) are indexed under the
identical title "Catalyzing careers, transforming lives by Sanjay Saraf | SSEI",
while *other* routes have specific titles. Several product pages are indexed as bare
"Ssei" or "All Courses".
- Reading: a client-rendered app where the crawler sometimes got the shell's default
  `<title>` before route-level metadata was applied, or routes that fall through to a
  default. **Confidence in "client-side routing with inconsistent per-route metadata":
  medium.** This is an SEO defect worth not reproducing on the FRM page.

### 4.4 `store.ssei.co.in` is a **multi-tenant white-label commerce/LMS SaaS** — **high confidence**
Indexed pages on that one host carry four different brand names in `<title>`:
```
store.ssei.co.in/store             → "Store | CA PRANAV POPAT"
store.ssei.co.in/profile           → "Your Profile | CA PRANAV POPAT"
store.ssei.co.in/courses           → "My Enrollments | CA PRANAV POPAT"
store.ssei.co.in/support-tickets   → "Support Tickets List | CA PRANAV POPAT"
store.ssei.co.in/products/CA Final → "... | MEPL Classes"
store.ssei.co.in/product/...       → "... | BB Virtuals Pvt. Ltd."
store.ssei.co.in/contact           → "Contact Us | Lifelong Learners"
```
A single host cannot legitimately be four coaching brands; this is the fingerprint of a
shared SaaS whose tenant branding leaked into the crawl (shared origin / mis-set
tenant resolution).
- **The vendor was NOT identified.** I found no product name. Do not guess one.
- `courses.ssei.co.in` and `www.ssei.co.in` expose **the same route vocabulary**
  (`/store`, `/profile`, `/courses`, `/product/{slug}`, `/products/{Cat}`, `/refund`,
  `/contact`, `/s/{slug}`) → **inference (medium-high) that SSEI's commerce layer is that
  same third-party SaaS**, with the marketing site layered on top or beside it.
  **This matters for the rebuild: the product/checkout pages may not be SSEI's code to change.**

### 4.5 Android package naming corroborates 4.4 — **medium confidence**
- `in.sseimarkets.store` — "SSEI Markets" on Google Play
- `in.bbvirtuals.store` — "BB Virtuals Prep" on Google Play
Identical `in.{brand}.store` convention across two unrelated coaching brands →
same white-label app vendor as the `store.` web platform.
Also CONFIRMED: **"SSEI Learn"** on the Apple App Store (`id6760988798`).

### 4.6 ULURN = the in-house video delivery app — **high confidence (QUOTED)**
- QUOTED: "Classes are conducted on SSEI's in-house application, 'Ulurn'."
- `ulurn.in` has its own course routes: `ulurn.in/course/{slug}`, `ulurn.in/search?q=`
- Play Store package `com.ulurn`
- QUOTED constraints: "Windows 8.1 & above with 4GB RAM"; "Android 7.0 & beyond";
  iOS "in Beta Testing mode"; "Simultaneous login on both Android App and Laptop is not
  permitted"; "the machine on which the application is installed once cannot be changed."
- **INFERRED:** device-bound DRM on a native desktop/mobile client, i.e. **video is not
  served to the browser from the marketing site**. An FRM landing page therefore only
  needs to sell + hand off, not host playback.

### 4.7 QForum = doubt forum + CBT mock engine — **high confidence (CONFIRMED hosts)**
```
forum.sseiqforum.com/question/{slug}     e.g. /question/ulurn/, /question/ulurn-app-6/
mocktest.sseiqforum.com/learn            "Welcome to SSEI - Course & Mock Test Platform"
```
- The `/question/{slug}/` route shape is characteristic of a **WordPress Q&A plugin**.
  **Confidence: low-medium. Inference only — no `wp-` path was ever observed.**

### 4.8 Legacy-stack residue — **low-medium confidence**
- `www.ssei.co.in/contact.php` is indexed → a **PHP** site existed on this domain.
  Whether it still resolves is UNVERIFIED.
- `/resources/` and `/top-five-...-online/` use trailing-slash, date-less post slugs and
  `/resources/` renders a doubled title "Resources | SSEI SSEI" → classic
  WordPress-with-SEO-plugin signature. **Inference only.**
- Net reading: an older PHP/WordPress site was replaced by a JS app, and some legacy URLs
  remain indexed. **Confidence in "there was a legacy PHP/WP site": medium.
  Confidence it is still the live stack: low — the modern routes argue against it.**

### 4.9 Payment provider — **NO EVIDENCE**
I ran a targeted search for a payment gateway on ssei.co.in. Nothing was found —
no Razorpay, PayU, CCAvenue, Cashfree or Stripe reference anywhere in the index.
QUOTED: "Flexible EMI plans are available" (marketing copy only, no provider named).
**Do not assume a gateway.**

### 4.10 Job postings / engineering hiring — **NO EVIDENCE**
A search for SSEI software/frontend roles returned nothing from SSEI. No careers page,
no job post, no stack mention. **There is no public hiring signal for their tech stack.**

### 4.11 Analytics / tag manager / CDN / CMS — **NO EVIDENCE**
No GTM, GA4, Meta Pixel, Cloudflare, or CMS identification was obtainable. Every
third-party technology profiler I tried (`builtwith.com` results absent for this domain;
`website.informer.com` and `ssei.co.in.usitestat.com` both egress-blocked) was unusable.

### 4.12 Third-party validation (CONFIRMED, external)
- GARP lists SSEI as an FRM exam-preparation provider:
  `https://www.garp.org/frm/exam-preparation-provider/sanjay-saraf-educational-institute`
  and an RAI provider at `/rai/exam-preparation-provider/...`
- QUOTED from SSEI: "official CFA Institute Prep Provider" / "curriculum, materials, and
  methodology are verified by CFA Institute"
- Social/owned: `t.me/s/SSEIDirect`, `youtube.com/@sseiinstitute`,
  `instagram.com/sseieducation`, `x.com/SSEI_Education` + `x.com/sseieducation`,
  `facebook.com/SanjaySarafEducationalInstitute`,
  `linkedin.com/company/sanjay-saraf-educational-institute`,
  `medium.com/@sseiducationalinstitute`, `pinterest.com/sseiducationalinstitute`

### 4.13 Business facts (QUOTED, useful as landing-page content)
- Kolkata centre: "6A, Elgin Road, near Bhowanipore College, Sreepally, Bhowanipore, Kolkata, West Bengal 700020"
- Centres: Kolkata, Mumbai, Delhi. "face-to-face sessions at their Kolkata, Delhi, and Mumbai centres, as well as live online classes"
- Counselling hours: "Monday–Saturday, 9 AM – 8 PM IST" (site) / "Monday to Saturday 10 AM to 7 PM" (courses. subdomain — the two hosts disagree)
- Email `info@ssei.co.in`; phone `+91 7595053300`; markets `+91 7595052200`
- Founder: Sanjay Saraf — "CFA and FRM charterholder with an MS in Finance from ICFAI Hyderabad", "over 30 years of teaching experience"
- CEO: Vidyut Kauntia — "9+ years across high-growth businesses … Uber India, Swvl, and SSEI"
- Other named faculty: Budhaditya Debnath (equity research / portfolio management), Anurag (Big Four consulting + IB)
- Blog scale: "over 320 pieces"
- Catalogue scale: "53 total courses"
- Outcome claim: "average CTC … ₹8–20 LPA"

---

## 5. Gaps — what still requires direct page access

Nothing structural about the *rendering* of the CFA page was obtainable. Specifically:

1. **The actual DOM of `/cfacourse` / `/products/CFA` / `/courses/113`** — section order,
   hero composition, how many sections, where the CTA sits, sticky elements, accordions.
   Search gave me copy, never layout.
2. **CSS / design tokens** — colour palette, typography, spacing scale, breakpoints,
   whether Tailwind or a component library is used. Zero evidence either way.
3. **JS bundle fingerprints** — `_next/static/`, `__NEXT_DATA__`, `build-id`, chunk names,
   `<meta name="generator">`. These would settle Next.js vs. anything else in one fetch
   and are the highest-value single missing item.
4. **API endpoints** — how `/courses?level=&programme=` fetches (SSR vs client fetch),
   the course JSON shape, the product/price endpoint, whether prices come from the
   `store.` SaaS or SSEI's own backend.
5. **Form handlers** — the enquiry/lead form on `sseiadmission.ssei.co.in/cfa/`: action URL,
   field names, validation, CRM/webhook target, OTP flow. Needed to replicate lead capture.
6. **Checkout** — where "Enrol" goes, whether it leaves the domain, and the payment provider
   (§4.9: completely unknown).
7. **Meta tags & schema.org** — canonical tags, OG/Twitter cards, `Course`/`Organization`/
   `FAQPage`/`BreadcrumbList` JSON-LD. The `/courses/{id}` pages almost certainly emit
   `Course` markup, but this is unverified.
8. **`robots.txt` and `sitemap.xml`** — would give the *complete* URL set in one request
   and make §3 exhaustive instead of sample-based.
9. **Whether `ssei.co.in/cfa/` (the brief's target) actually resolves** — status code and
   redirect target unknown. It may be a 404, a redirect to `/cfacourse`, or a route that
   exists but was never indexed.
10. **Actual INR pricing and the package-tier matrix** (Gold / Platinum / Platinum Plus) —
    prices are almost certainly rendered client-side from an API and were never indexed.
11. **The `/exam/{programme}/{level}` staging pages** — `betassei.co.in/exam/frm/part-1`
    is the most likely single page to copy for an FRM rebuild, and it is inferred, not seen.
12. **Response headers** — `server`, `x-powered-by`, `x-vercel-id`, `cf-ray`, CSP.
    One `curl -I` would resolve §4.1, §4.3 and §4.8 at once.

**Suggested unblocking:** ask the user to paste `view-source:` output (or run
`curl -sSL <url> -o file.html`) from their own machine for, in priority order:
`https://ssei.co.in/robots.txt`, `https://ssei.co.in/sitemap.xml`,
`https://ssei.co.in/courses/frm`, `https://ssei.co.in/cfacourse`,
`https://ssei.co.in/courses/113`, `https://betassei.co.in/exam/cfa/level-2`.
