# SSEI FRM Content Inventory (WebSearch-only reconnaissance)

**Compiled:** 2026-09-22
**Method:** `WebSearch` only. Direct HTTP access to `ssei.co.in` / `courses.ssei.co.in` is blocked by
the environment egress proxy (403 CONNECT / EGRESS_BLOCKED), so **no page was ever fetched or rendered.**
Everything below is derived from search-engine result links and result snippets/summaries.

**Evidence grading used throughout:**

| Tag | Meaning |
|---|---|
| **CONFIRMED** | The URL was returned by a search engine as an actual result link, with a title. The page exists (or existed at index time). |
| **INFERRED** | The URL was never seen in any result. It is a guess extrapolated from an observed routing pattern or a truncated string. Treat as unverified. |
| **VERBATIM** | Text appeared inside quotation marks in the search output, or as a distinctly page-shaped string (title-cased feature list, slogan). High confidence it is real page copy. |
| **PARAPHRASE** | The search engine's own summariser restated the page. Wording is NOT the site's. Do not quote to a user as site copy. |

A caveat that applies to the whole document: the search result summaries are machine-generated
abstractions over page text. Only items marked VERBATIM should be treated as recoverable page copy.

---

## 1. FRM URL inventory

### 1a. FRM-specific pages — CONFIRMED

| # | URL | Page title as returned | Surfacing query | Status |
|---|---|---|---|---|
| 1 | `https://www.ssei.co.in/courses/frm` | Sanjay Saraf Educational Institute (SSEI) | `site:ssei.co.in FRM` | CONFIRMED |
| 2 | `https://ssei.co.in/courses/195` | FRM Part 1 / "Sanjay Saraf Educational Institute (SSEI)" | `site:ssei.co.in FRM` | CONFIRMED |
| 3 | `https://www.ssei.co.in/product/frmpart1` | FRM Part 1 / "Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI" | `ssei.co.in FRM Part 1 syllabus hours Sanjay Saraf` | CONFIRMED |
| 4 | `https://courses.ssei.co.in/product/frm-part-1` | FRM Part 1 \| SSEI | `site:ssei.co.in FRM` | CONFIRMED |
| 5 | `https://www.ssei.co.in/product/frmpart1new` | Sanjay Saraf Educational Institute (SSEI) | `"ssei.co.in/courses/195" FRM Part 1` | CONFIRMED |
| 6 | `https://www.ssei.co.in/product/frm-part-2` | FRM Part 2 | `site:ssei.co.in FRM` | CONFIRMED |
| 7 | `https://courses.ssei.co.in/product/frm-part-2` | FRM Part 2 | `site:courses.ssei.co.in FRM` | CONFIRMED |
| 8 | `https://www.ssei.co.in/product/frmpart2` | All Courses | `ssei.co.in FRM Part 2 fees price rupees` | CONFIRMED |
| 9 | `https://courses.ssei.co.in/product/frmpart1&part2combo` | FRM Part 1 and FRM Part 2 Combo | `site:ssei.co.in FRM` | CONFIRMED |
| 10 | `https://www.ssei.co.in/product/frmpart1&part2combo` | FRM Part 1 and FRM Part 2 Combo | `site:ssei.co.in FRM Part 2 GARP curriculum course` | CONFIRMED |
| 11 | `https://www.ssei.co.in/product/frmpart1-returningstudent-module` | FRM Part 1 - Returning Student Module \| SSEI | `site:ssei.co.in FRM` | CONFIRMED |
| 12 | `https://courses.ssei.co.in/product/frmpart1-returningstudent-module` | FRM Part 1 - Returning Student Module \| SSEI | `site:courses.ssei.co.in FRM` | CONFIRMED |
| 13 | `https://www.ssei.co.in/product/frm-part-1-for-cfa-students` | FRM Part 1 for CFA Students | `site:ssei.co.in FRM` | CONFIRMED |
| 14 | `https://courses.ssei.co.in/product/frm-part-1-for-cfa-students` | FRM Part 1 for CFA Students | `site:courses.ssei.co.in FRM` | CONFIRMED |
| 15 | `https://courses.ssei.co.in/product/cfal1forfrmstudents` | Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI (= "CFA Level 1 for FRM Students") | `site:courses.ssei.co.in FRM` / `"cfal1forfrmstudents" SSEI` | CONFIRMED |
| 16 | `https://www.ssei.co.in/product/frm-stock-market` | Stock Market Programs for FRM Students | `site:ssei.co.in FRM` | CONFIRMED |
| 17 | `https://www.ssei.co.in/products/FRM` | Explore FRM Products \| SSEI | `ssei.co.in FRM Part 1 syllabus hours Sanjay Saraf` | CONFIRMED |
| 18 | `https://courses.ssei.co.in/products/FRM` | Explore FRM Products \| SSEI (one result rendered its title as "FRM Part 2") | `site:courses.ssei.co.in FRM` | CONFIRMED |
| 19 | `https://www.ssei.co.in/courses?programme=frm` | All Courses | `ssei.co.in courses programme=frm all courses list` | CONFIRMED |
| 20 | `https://ssei.co.in/courses?level=frm-part-2&programme=frm` | All Courses | `ssei.co.in "courses/frm" FRM programme page` | CONFIRMED |
| 21 | `https://www.ssei.co.in/blogs/Global-Exams-Experience-Exam-Tips` | AN HONOURED TURNING POINT: FRM \| Global Exams \| Experience \| Exam Tips \| SSEI | `site:ssei.co.in FRM` | CONFIRMED |
| 22 | `https://www.ssei.co.in/battleground-finance-cfa-vs-frm` | Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI | `site:ssei.co.in FRM` | CONFIRMED |
| 23 | `https://www.ssei.co.in/mock-tests` | SSEI Mock Tests. Full-length CBT Mocks for CFA, FRM, CA Final | `SSEI FRM mock test QForum results toppers` | CONFIRMED |

**23 FRM-specific CONFIRMED URLs.**

### 1b. Supporting / site-wide pages that carry FRM mentions — CONFIRMED

| URL | Title as returned | Surfacing query |
|---|---|---|
| `https://www.ssei.co.in/` | SSEI: Sanjay Saraf Educational Institute - CA, CFA & FRM Coaching | multiple |
| `https://courses.ssei.co.in/` | Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI | `site:courses.ssei.co.in FRM` |
| `https://www.ssei.co.in/courses` | All Courses | `ssei.co.in FRM Part 1 syllabus hours Sanjay Saraf` |
| `https://courses.ssei.co.in/store` | Store \| SSEI | `"ssei.co.in/courses/196"` |
| `https://courses.ssei.co.in/contact` | Contact Us \| SSEI | `"ssei.co.in/courses/196"` |
| `https://courses.ssei.co.in/profile` | Your Profile \| SSEI | `"ssei.co.in/courses/196"` |
| `https://www.ssei.co.in/profile` | Sanjay Saraf Educational Institute (SSEI) | `SSEI FRM batch schedule start date live online Kolkata 2026` |
| `https://www.ssei.co.in/address` | Address List \| SSEI | `ssei.co.in courses programme=frm all courses list` |
| `https://ssei.co.in/contact-us` | Contact SSEI \| Speak to Counsellors, Visit Kolkata, Mumbai, or Delhi | `SSEI contact address phone email Kolkata FRM office` |
| `https://www.ssei.co.in/contact.php` | Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI | `SSEI contact address phone email …` |
| `https://www.ssei.co.in/classroom-schedule.php` | Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI | `SSEI FRM batch schedule start date live online Kolkata 2026` |
| `https://www.ssei.co.in/about` | About Us \| SSEI | `SSEI contact address phone email …` |
| `https://www.ssei.co.in/privacy` | Privacy Policy \| SSEI | `SSEI contact address phone email …` |
| `https://www.ssei.co.in/blogs` | SSEI Blog: Finance Writing for CFA, FRM & CA Aspirants | `SSEI blog FRM battleground finance CFA vs FRM` |
| `https://www.ssei.co.in/blog` | Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI | `site:ssei.co.in blogs FRM exam tips career` |
| `https://www.ssei.co.in/happy-students` | Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI | `SSEI FRM testimonials students reviews …` |
| `https://www.ssei.co.in/sseicourse` | Catalyzing careers, transforming lives by Sanjay Saraf \| SSEI | `"sseiadmission.ssei.co.in" frm registration` |
| `https://www.ssei.co.in/blogs/Exploring-Careers-in-Finance-Hierarchies-Roles-and-Certifications` | Exploring Careers in Finance: Hierarchies, Roles, and Certifications \| SSEI | `site:ssei.co.in blogs FRM exam tips career` |
| `https://www.ssei.co.in/blogs/My-Take-On-Examination-Success` | TO BE OR NOT TO BE: My Take On Examination Success \| SSEI | `SSEI FRM testimonials …` |

### 1c. Other `*.ssei.co.in` subdomains discovered — CONFIRMED (none FRM-specific so far)

| URL | Title | Notes |
|---|---|---|
| `https://sseiadmission.ssei.co.in/cfa/` | CFA Level 1 / "SSEI" | Admission/lead-capture microsite. CFA variant only. |
| `https://sseiadmission.ssei.co.in/cfa2/` | Jump Into CFA Level 2 Prep / "SSEI" | Same microsite family. |
| `https://sseischolarship.ssei.co.in/` | SSEI Scholarship Exam | |
| `https://cfaresults.ssei.co.in/` | Your CFA Result Is Here \| Personalized Blueprint & Guidance \| SSEI | CFA-only equivalent; an FRM twin was never seen. |

### 1d. Explicitly ruled OUT (looked FRM-adjacent, is not)

| URL | Actual content | How ruled out |
|---|---|---|
| `https://www.ssei.co.in/courses/196` | CA Final AFM Fast Track | `"ssei.co.in/courses/196"` returned CA Final AFM description. **Not the FRM Part 2 numeric ID.** |
| `https://www.ssei.co.in/courses/125` | CA Final AFM Classes | non-FRM |
| `https://www.ssei.co.in/courses/113` | CFA Level 1 Coaching — Full Immersion | non-FRM |
| `https://ssei.co.in/courses/205` | CFA Level 1 Coaching — Accelerate Batch | non-FRM |
| `https://ssei.co.in/courses/172` | Financial Modeling & Valuation | non-FRM |

### 1e. INFERRED — guessed, never observed. Do not cite as real.

| Inferred URL | Basis for the guess | Why still unverified |
|---|---|---|
| `https://ssei.co.in/courses/frm/part-1` (or `/part1`) | A Telegram-sourced snippet contained a **truncated** registration link rendered as `ssei.co.in/courses/frm/pa…`. | The truncation was never resolved. An explicit query for `"ssei.co.in/courses/frm/part-1" OR "…/part1"` returned **zero** matching links — only the already-known product pages. INFERRED, and weakly so. |
| `https://ssei.co.in/courses/<id>` for FRM Part 2 | FRM Part 1 = `/courses/195`, so Part 2 plausibly has an adjacent numeric id. | 196 was tested and is CA Final AFM. No other id was ever surfaced. INFERRED — the actual number is unknown. |
| `https://courses.ssei.co.in/product/frmpart1` / `…/frmpart1new` / `…/frm-stock-market` | Every other product slug was observed on **both** `www.ssei.co.in` and `courses.ssei.co.in`, suggesting a full mirror. | These specific host+slug pairs were never returned. INFERRED. |
| `https://www.ssei.co.in/product/frm-part-2-returningstudent-module` | A Part 1 returning-student module exists. | Explicitly searched for; **no such page appeared.** Likely does not exist. INFERRED-NEGATIVE. |
| `https://sseiadmission.ssei.co.in/frm/` | `/cfa/` and `/cfa2/` exist on that host. | Explicitly searched; never returned. INFERRED. |
| `https://frmresults.ssei.co.in/` | `cfaresults.ssei.co.in` exists. | Never returned. INFERRED. |

### 1f. Adjacent SSEI-operated domains (outside ssei.co.in, recorded for completeness)

`forum.sseiqforum.com` · `ask.sseiqforum.com/question-tag/frm/` · `mocktest.sseiqforum.com/learn` ·
`www.sanjaysaraf.com` (incl. `/faculties`, `/faqs`, `/courses/113`) · `www.sseimarkets.com` ·
`courses.sseimarkets.com` · `nseacademy.sseimarkets.com` · `sseimarkets.in`.
`mocktest.sseiqforum.com/learn/FRM-PART-2---CBT-MOCK---19th-to-22nd-Nov-2021` is an FRM Part 2 CBT
mock listing — CONFIRMED, but on the QForum domain, not ssei.co.in.

Third-party resellers of SSEI FRM lectures that surfaced (not SSEI-owned): `ulurn.in`,
`lecturespoint.com`, `evaraeducation.com`, `vihaaneducations.com`, `zeroinfy.in`, `studyathome.org`.

---

## 2. Content fragments captured

Strings below are reproduced exactly as they came back from the search tool. Attribution is to the
URL(s) the engine associated with the claim; where the engine pooled several results I say so.

### From `https://ssei.co.in/courses/195` and/or `https://courses.ssei.co.in/product/frm-part-1` (FRM Part 1)

> **VERBATIM** (quoted as a slogan in results): "No concept is too complex to explain."
> Context given: *After 9 years, Sanjay Saraf Sir returns to teach FRM with the same belief that has defined his classrooms for over three decades.*

> **VERBATIM** (title-cased page feature list, appeared identically across 4 separate queries):
> "Lectures, Handwritten Notes, Spreadsheets, Question Solving, Building Blocks, Complementary FREE courses: Basic & Advanced Excel, Python For Finance."

> **VERBATIM-ish** (repeated identically across ≥6 queries; strongly page-shaped):
> "builds a strong foundation in global risk management" … "teaches the full GARP Part 1 syllabus in around 230 hours" … "delivered live online and offline in Kolkata, with handwritten notes, spreadsheet-based modeling, and Telegram doubt support."

> **VERBATIM** (feature bullets): "1.5x Views", "24-month validity", "direct Telegram doubt-solving with Sanjay Sir"

> **PARAPHRASE**: Students practice with questions from GARP® Candidate Resources, end-of-chapter exercises, and SSEI's exclusive question bank.

> **PARAPHRASE**: Candidates are provided PDF class notes; access to QForum, a state-of-the-art doubt solving and knowledge sharing platform where all queries are attended to in a structured and efficient manner.

> **PARAPHRASE**: Sanjay Sir and Budhaditya "have taught engineers, statisticians, and physics graduates who cleared FRM with excellent scores."

> **PARAPHRASE**: SSEI's faculties have "a rich legacy of 20+ years teaching specifically for FRM and 30+ years of teaching finance education in general."

> **PARAPHRASE**: A key strength is emphasis on handwritten notes, board-based explanation, and step-by-step concept building; for a demanding program like FRM they integrate spreadsheets, financial models, and practical analytical frameworks.

> **PARAPHRASE** (discount): An INR 9,000 discount for current or past CA Final SFM students, code **`SSEISFM9K`**. NOTE: this surfaced via a Telegram channel mirror (`t.me/s/SSEIDirect`) and pointed to `ULURN.in`, not to an ssei.co.in page. Provenance is weak — treat as unconfirmed for the SSEI site itself.

### From `https://www.ssei.co.in/product/frmpart1-returningstudent-module` (FRM Part 1 Returning Student Module)

> **PARAPHRASE**: "This course is only for students who took the Aug 24 FRM exam but didn't pass. After signing up for the course, you need to send your Aug 24 FRM exam mark sheet."

> **PARAPHRASE**: Spread over approximately 230 hours of core learning content, with learning objectives and readings conceptually explained and deliberated on.

> **PARAPHRASE**: Includes lectures, handwritten notes, spreadsheets, question solving, building blocks, and complementary free courses in basic and advanced Excel; PDF class notes; QForum access; extensive question solving from candidate resources and SSEI's question bank.

### From `https://www.ssei.co.in/product/frm-part-2` / `https://courses.ssei.co.in/products/FRM` (FRM Part 2)

> **PARAPHRASE** (hours — **CONFLICTING, see Gaps**): "spread over approximately 360 hours of core learning content where the learning objectives and readings are conceptually explained and deliberated on. Additionally, comprehensive revision of the entire curriculum is provided in approximately 65 hours."
> Source query: `"FRM Part 2" SSEI "Sanjay Saraf" course hours what you get`

> **PARAPHRASE** (hours — competing figure): "FRM Part 2 features ~250 hours of core learning content with deliverables including a questions bank, Python and SQL classes, PDF class notes, and doubt resolution through QForum."
> Source queries: `"Explore FRM Products" SSEI store products FRM list` and `"FRM Part 2" "Returning Student Module" …`

> **PARAPHRASE** (deliverables list, consistent across two queries): "Questions Bank", "Classes for Python and SQL", "Class Notes provided as PDFs", "Doubt Resolution through QForum".

> **PARAPHRASE**: "In-class extensive question solving from Candidate Resources, End of Chapter questions, and SSEI question bank to reinforce core concepts."

> **PARAPHRASE**: "Privileged access to full CBT Mock with a state-of-the-art CBT interface that mimics the actual exam with percentile ranking"; "Subject-wise quizzes consolidated across GARP Institute content and SSEI resource pool."

### From `https://www.ssei.co.in/happy-students` (and/or FRM product pages — engine pooled them)

> **VERBATIM** (quoted testimonial): "The FRM notes from SSEI helped me revise better, understand concepts clearly, and made my attempt much easier than expected."

> **VERBATIM**: "SSEI's practical Excel-based approach made FRM far more enjoyable, helping me understand derivatives, Monte Carlo simulations, and risk models beyond textbook theory."

> **VERBATIM**: "SSEI's FRM classes helped me connect theory with real understanding. The way Sanjay Sir explained concepts made it easier to visualise the graphs, applications, and logic behind them."

> **VERBATIM**: "The Excel files that Sanjay Sir provided, made FRM Part 2 much easier to understand. His practical approach helped me see even theoretical topics visually."

> **VERBATIM**: "innovative teaching methods have transformed the lives of over 10 lakh students, building a legacy of success that continues to grow."

### From `https://www.ssei.co.in/mock-tests`

> **PARAPHRASE**: Full-length CBT mocks for CFA Level 1, 2, 3, **FRM Part 1**, and CA Final AFM; includes exam-pattern questions, topic-wise diagnostics, and percentile ranking.
> (Note: FRM **Part 2** was not named in the mock-tests listing snippet.)

### From `https://www.ssei.co.in/blogs`

> **PARAPHRASE**: "faculty-written insights on CFA, FRM, CA Final, and Analyst Stack, covering exam strategy, concept deep-dives, and career guidance"; publishes "every Sunday with one deep article, one exam tip, and one career insight"; "over 320 pieces written by India's top finance educators with no clickbait."

### From `https://www.ssei.co.in/product/frm-stock-market`

> **PARAPHRASE**: FRM programs with "Hindi & English instruction, mobile and laptop support, and free access to regular practice courses."
> (Low confidence — the summariser may have blended this with `sseimarkets.com` copy.)

### From `https://www.ssei.co.in/` (homepage)

> **VERBATIM-ish** (meta description shape): "SSEI offers expert-led CA, CFA and FRM coaching with live and recorded classes, top faculty and proven exam results."

> **PARAPHRASE**: "SSEI, founded by Sanjay Saraf and based in Kolkata, is a top finance coaching institute offering CFA, CA, FRM and other courses, known for structured teaching, timely completion, and real market training via SSEI Markets." Founder has "been imparting education in the field of finance … for the past 25 years", expertise in "financial treasury, risk management, volatility trading and business valuation."

### From `https://courses.ssei.co.in/product/cfal1forfrmstudents`

> **PARAPHRASE**: CFA Level 1 course designed for FRM students; "extensive question solving … approximately 3,000 questions."

---

## 3. Facts gathered

### Faculty

| Fact | Source URL |
|---|---|
| **Sanjay Saraf** — lead instructor, FRM Part 1. Returns to teaching FRM "after 9 years". | `ssei.co.in/courses/195`, `courses.ssei.co.in/product/frm-part-1` |
| Sanjay Saraf is a **CFA and FRM charterholder, MS in Finance from ICFAI Hyderabad, 30+ years teaching**, founder of SSEI, began teaching at 16. | `ssei.co.in/courses/195` / `www.ssei.co.in/` |
| **Budhaditya Debnath** — Lead Instructor, FRM Part 1, alongside Sanjay Saraf. Background in equity research and portfolio management; works inside a family office; "helping students connect FRM concepts to the way risk is measured and managed in real markets." | `ssei.co.in/courses/195`, `courses.ssei.co.in/product/frm-part-1` |
| Budhaditya Debnath external profile: CFA (all levels cleared), FRM Part 1, Equity Research Analyst; formerly Research Assistant at SSEI. | LinkedIn (third-party, not ssei.co.in) |
| Faculty legacy claim: 20+ years teaching FRM specifically, 30+ years finance teaching overall. | FRM Part 1 pages |

### Course hours / structure

| Fact | Source URL |
|---|---|
| **FRM Part 1: ~230 hours** of core learning content; full GARP Part 1 syllabus. Repeated across 8+ independent queries — highest-confidence number in this document. | `ssei.co.in/courses/195`, `courses.ssei.co.in/product/frm-part-1`, `www.ssei.co.in/products/FRM` |
| **FRM Part 1 Returning Student Module: ~230 hours** (same figure). | `www.ssei.co.in/product/frmpart1-returningstudent-module` |
| **FRM Part 2: ~360 hours** core + **~65 hours** full-curriculum revision. | `www.ssei.co.in/product/frm-part-2` (via query on Part 2 hours) |
| **FRM Part 2: ~250 hours** core — *contradicts the 360h figure*. | `courses.ssei.co.in/products/FRM` / `www.ssei.co.in/products/FRM` |
| CFA Level 1 comparator (for scale): ~505 h Gold package, ~562 h Platinum & Platinum Plus. | `www.ssei.co.in/courses/113` |

### Delivery / access terms

| Fact | Source URL |
|---|---|
| Delivered **live online and offline in Kolkata**. | FRM Part 1 pages |
| **1.5x views**, **24-month validity**. | FRM Part 1 pages |
| **Direct Telegram doubt-solving with Sanjay Sir**. | FRM Part 1 pages |
| **QForum** — structured doubt-solving / knowledge-sharing platform, included. | FRM Part 1 & Part 2 pages |
| PDF class notes provided. | FRM Part 1 & Part 2 pages |
| Handwritten notes + spreadsheet-based financial modeling. | FRM Part 1 pages |
| Complementary FREE courses bundled: **Basic & Advanced Excel**, **Python For Finance**. | FRM Part 1 pages |
| FRM Part 2 additionally bundles **Python and SQL classes**. | FRM Part 2 pages |
| Full CBT mock with exam-mimicking interface + percentile ranking. | FRM Part 2 page; `www.ssei.co.in/mock-tests` |
| Question sources: GARP® Candidate Resources, End-of-Chapter questions, SSEI question bank. | FRM Part 1 & Part 2 pages |
| CA Final AFM packages come in "with books" / "without books" variants and 1.5x total-duration viewing — a **packaging pattern likely mirrored on FRM**, but never observed on an FRM page. INFERRED. | `www.ssei.co.in/courses/196` |

### Batch / registration

| Fact | Source URL |
|---|---|
| Registration open for the **August 2026 FRM exam**. | Telegram mirror `t.me/s/sseidirect` (not ssei.co.in) |
| **25th April** — registration deadline via SSEI for FRM Part 1 & Part 2 candidates sitting the August 2026 exams. | attributed to `www.ssei.co.in/courses/frm` in results; provenance partly Telegram |
| Registration flow: complete registration form → receive email with the product link to access the course. | attributed to `www.ssei.co.in/courses/frm` |
| Registration phone for FRM: **8100300400**. | attributed to `www.ssei.co.in/courses/frm` |
| No FRM batch **start date** was recoverable from any query. | — |
| `www.ssei.co.in/classroom-schedule.php` exists and is the likely home of batch timing. Contents never retrieved. | CONFIRMED URL, contents unknown |

### Pricing

| Fact | Source | Confidence |
|---|---|---|
| **No SSEI-published FRM price of any kind was recoverable.** Five separate pricing-targeted queries returned nothing from ssei.co.in. | — | high (negative result) |
| "FRM Part 2 by SSEI priced ₹36,000–₹39,000" | `evaraeducation.com` — **third-party reseller**, not SSEI | low; reseller pricing ≠ SSEI pricing |
| INR 9,000 discount, code `SSEISFM9K`, for current/past CA Final SFM students | Telegram mirror, pointing at `ULURN.in` | low |
| GARP exam fees (separate from coaching): USD 1,000 early / USD 1,200 standard for a first-time Part 1 candidate | `garp.org` / `zelleducation.com` | not SSEI data |

### Contact details

| Fact | Source URL |
|---|---|
| Email **info@ssei.co.in** | `ssei.co.in/contact-us`, `courses.ssei.co.in/contact` |
| Phone **+91 7595053300** | `courses.ssei.co.in/contact` |
| Phone **9830023636** | `www.ssei.co.in/` / contact pages |
| Phone **8100300400** (FRM registration) | FRM registration snippet |
| Phone **033 6535-1522** (as returned: "0336535-1522") | `ssei.co.in/contact-us` |
| Address: **6A, Elgin Road, near Bhowanipore College, Sreepally, Bhowanipore, Kolkata, West Bengal 700020** | `ssei.co.in/contact-us` / `www.ssei.co.in/address` |
| Registered office: **6A, Lala Lajpat Rai Sarani, 2nd Floor, Bhowanipore, Kolkata – 700020** | `www.ssei.co.in/address` |
| Counsellors available **Mon–Sat, 9 AM – 8 PM IST** | `ssei.co.in/contact-us` |
| Contact page title advertises **Kolkata, Mumbai, Delhi** locations | `ssei.co.in/contact-us` |
| QForum support email **QForum@ssei.co.in** | QForum pages |
| SSEI is a **GARP-listed FRM Exam Preparation Provider** | `garp.org/frm/exam-preparation-provider/sanjay-saraf-educational-institute` |

---

## 4. Observed URL patterns

Five distinct route families were observed on ssei.co.in. They are **not** alternative spellings of one
router — they behave like different generations of the site layered on top of each other.

**A. `/<host>/product/<slug>` — the primary product/detail route.**
Present on **both** `www.ssei.co.in` and `courses.ssei.co.in` with identical slugs
(`frm-part-1`, `frm-part-2`, `frmpart1-returningstudent-module`, `frm-part-1-for-cfa-students`,
`frmpart1&part2combo`, `cfal1forfrmstudents`, `frm-stock-market`, `frmpart1`, `frmpart1new`, `frmpart2`).
Implication: one product catalogue served under two hostnames — `courses.` is the
commerce/LMS face, `www.` the marketing face. Slugs are **inconsistently formatted**: hyphenated
(`frm-part-1`) and squashed (`frmpart1`) variants of apparently the same product coexist, plus a
`new` suffix (`frmpart1new`) and a literal `&` inside a path segment (`frmpart1&part2combo`) — an
unescaped ampersand in a URL path, which suggests slugs are stored free-form rather than generated.
The `frmpart1` / `frm-part-1` / `frmpart1new` trio most likely represents **successive batch
re-launches of the same course**, with old slugs left live. Titles support this: `product/frmpart2`
returns the generic title "All Courses" while `product/frm-part-2` returns "FRM Part 2", i.e. the
squashed slugs look like **stale or redirect-only** entries.

**B. `/products/<PROGRAMME>` — programme landing/category route.**
`www.ssei.co.in/products/FRM`, `courses.ssei.co.in/products/FRM`, `www.ssei.co.in/products/CFA`,
`www.ssei.co.in/products/CA%20Inter`. The segment is a **display-cased programme name, not a slug**
(note the URL-encoded space in `CA%20Inter`). Singular `/product/` = one item; plural `/products/` =
a programme's catalogue. Easy to confuse; worth flagging to anyone writing scrapers.

**C. `/courses/<numeric id>` — a separate, older course-detail route.**
Confirmed ids: **195 = FRM Part 1**, 196 = CA Final AFM Fast Track, 125 = CA Final AFM,
113 = CFA Level 1 Full Immersion, 205 = CFA Level 1 Accelerate, 172 = Financial Modeling & Valuation.
Ids are **not grouped by programme** (195 FRM sits directly beside 196 CA Final), so they are
allocated sequentially by creation date. This is the strongest single signal in the inventory: FRM
Part 1's id-195 page is newly created relative to CFA-113, matching the "Sanjay Saraf returns to FRM
after 9 years" positioning. The same numeric scheme appears on the sibling domain
`sanjaysaraf.com/courses/113`, so `/courses/<id>` predates the current ssei.co.in front end.

**D. `/courses/<programme-slug>` and `/courses?<filters>` — programme hub + faceted listing.**
`www.ssei.co.in/courses/frm` (hub), `www.ssei.co.in/courses` (all), and query-string facets:
`?programme=frm`, `?level=frm-part-2&programme=frm`, `?programme=cfa&subjectNames=CFA+Level+1`.
Facet keys observed: `programme`, `level`, `subjectNames`. **Note the collision**: `/courses/frm`
(string) and `/courses/195` (integer) occupy the same path position, so the router must be
type-discriminating on that segment.

**E. `.php` legacy leftovers.** `www.ssei.co.in/contact.php`, `www.ssei.co.in/classroom-schedule.php`
sit alongside extensionless equivalents (`/contact-us`, `/about`, `/privacy`, `/address`,
`/happy-students`, `/sseicourse`, `/profile`, `/mock-tests`). Evidence of a PHP-era site still
partially indexed under a newer framework.

**F. Blog route.** `/blogs` (index) + `/blogs/<Title-Case-Hyphenated-Slug>`, e.g.
`/blogs/Global-Exams-Experience-Exam-Tips`. Capitalised slugs — likely case-sensitive. A bare
`/blog` also resolves. A standalone editorial page exists outside `/blogs/`:
`/battleground-finance-cfa-vs-frm` sits at the site root.

**G. Subdomain-per-campaign.** `sseiadmission.` (with a path-per-programme: `/cfa/`, `/cfa2/`),
`sseischolarship.`, `cfaresults.`, `courses.`. Campaign microsites are spun up per programme —
**every one found is CFA**. Either the FRM equivalents do not exist yet, or they are unindexed.

---

## 5. Gaps — what could not be obtained without direct page access

1. **All pricing.** Not a single SSEI-published rupee figure for any FRM product. Package tiers
   (Gold / Platinum / Platinum Plus exist for CFA and CA Final — presumably for FRM too), EMI
   options, book/no-book variants, and current offers are all unknown. The only numbers found are
   third-party reseller prices and a Telegram discount code, neither of which can be relied on.
2. **Batch start dates and the class timetable.** `classroom-schedule.php` is confirmed to exist but
   its contents never surfaced. No FRM batch commencement date was recoverable.
3. **The FRM Part 2 hours figure is genuinely contradictory** — 360h+65h from one query, 250h from
   another, both attributed to SSEI pages. One of these is wrong (or they describe different
   packages/vintages). Unresolvable without reading the page.
4. **The full product list on `/products/FRM`.** Only the products that independently ranked in search
   are in this inventory. A category page almost certainly lists more (books, notes-only, revision-only,
   mock-only SKUs — all of which exist for CFA). Likely under-counted.
5. **The FRM Part 2 `/courses/<id>` number.** 196 was tested and disproved. The id is unknown.
6. **Which of `frmpart1` / `frm-part-1` / `frmpart1new` is canonical**, and whether the others 301 or
   serve stale content. Requires following redirects.
7. **Page structure and section headings.** No DOM, no navigation tree, no breadcrumb. The route
   families in §4 are reconstructed from URL shapes alone, not from the site's own IA.
8. **Verbatim body copy.** Almost everything in §2 is a search-engine paraphrase. Only ~9 fragments
   are safely quotable. The site's actual marketing copy for FRM is largely unrecovered.
9. **Syllabus detail.** "Full GARP Part 1 syllabus" is as granular as it gets — no module list, no
   topic weightings, no reading-by-reading breakdown.
10. **Faculty roster beyond two names.** Only Sanjay Saraf and Budhaditya Debnath were identified for
    FRM. `sanjaysaraf.com/faculties` exists and would likely resolve this.
11. **Whether FRM campaign microsites exist** (`sseiadmission.ssei.co.in/frm/`, an FRM results page).
    Searched for directly; absent from the index. Absence of evidence only.
12. **Anything behind login** — `courses.ssei.co.in/profile`, `/store` cart contents, enrolment forms.

### Recommended next step if page access is ever restored
Fetch in this order for maximum marginal information: `www.ssei.co.in/products/FRM` (complete SKU
list + prices in one page) → `ssei.co.in/courses/195` (richest single FRM page) →
`www.ssei.co.in/product/frm-part-2` (resolves the hours contradiction) →
`www.ssei.co.in/classroom-schedule.php` (batch dates) → `www.ssei.co.in/courses?programme=frm`
(catches any SKU that never ranked in search).

---

## Appendix: queries run (18)

`site:ssei.co.in FRM` · `site:courses.ssei.co.in FRM` · `site:www.ssei.co.in FRM` ·
`ssei.co.in FRM Part 1 syllabus hours Sanjay Saraf` · `ssei.co.in FRM Part 2 fees price rupees` ·
`SSEI FRM Budhaditya Debnath faculty` · `"ssei.co.in/courses/195" FRM Part 1` ·
`SSEI FRM Part 1 returning student module Aug 24 exam` ·
`SSEI FRM batch schedule start date live online Kolkata 2026` ·
`SSEI FRM Part 1 validity views doubt Telegram demo lecture` · `"ssei.co.in/courses/196"` ·
`site:ssei.co.in FRM Part 2 GARP curriculum course` · `"ssei.co.in/product/frm" FRM course details` ·
`SSEI FRM Part 1 and Part 2 combo price enrol` · `SSEI "FRM Part 1 for CFA Students" course` ·
`SSEI "CFA Level 1 for FRM Students" course` · `"cfal1forfrmstudents" SSEI` ·
`SSEI "Stock Market Programs for FRM Students"` · `ssei.co.in courses programme=frm all courses list` ·
`SSEI blog FRM battleground finance CFA vs FRM Sanjay Saraf` ·
`site:ssei.co.in blogs FRM exam tips career` · `SSEI FRM mock test QForum results toppers` ·
`"FRM Part 2" SSEI "Sanjay Saraf" course hours what you get` ·
`ssei.co.in "courses/frm" FRM programme page` · `SSEI FRM Part 1 package gold platinum price ₹ enrol now` ·
`sseiadmission.ssei.co.in FRM admission form` · `"sseiadmission.ssei.co.in" frm registration` ·
`SSEI FRM Part 1 "No concept is too complex to explain" …` ·
`"ssei.co.in/courses/frm/part-1" OR "ssei.co.in/courses/frm/part1"` ·
`SSEI FRM Part 1 building blocks spreadsheets handwritten notes Python for Finance Excel` ·
`"Explore FRM Products" SSEI store products FRM list` · `SSEI FRM Part 1 course fee EMI discount offer 2026 admission` ·
`"frmpart2" SSEI product page FRM Part 2 deliverables` · `SSEI FRM Part 2 "Python" "SQL" classes question bank deliverables` ·
`"frmpart1new" SSEI FRM Part 1 new batch` · `ssei.co.in/courses/frm "FRM" programme overview why FRM career` ·
`ssei.co.in courses numeric id FRM Part 2 course page 19` · `SSEI FRM testimonials students reviews success stories site:ssei.co.in` ·
`SSEI FRM Part 1 batch starts registration August 2026 exam Sanjay Saraf enrol date` ·
`SSEI FRM Part 1 "24 months" validity "1.5x" views doubt solving Sanjay Sir` ·
`SSEI contact address phone email Kolkata FRM office ssei.co.in/address` ·
`"FRM Part 2" "Returning Student Module" OR "frm-part-2" ssei courses.ssei.co.in product` ·
`SSEI FRM Part 1 course price INR 45000 OR 50000 OR 35000 Sanjay Saraf fees` ·
`site:ssei.co.in "FRM" store buy product code` · `"SSEISFM9K" SSEI FRM discount code` ·
`SSEI FRM Part 1 "230 hours" GARP syllabus lead instructors live online offline Kolkata`
