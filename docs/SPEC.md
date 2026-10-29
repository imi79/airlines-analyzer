# Airline Credit Tearsheet Spec

Oct 29, 2026 · @Mohamed El Mehdi

## Summary

The tool turns a European airline's or airport's annual filing into a two-page credit tearsheet in minutes, with every figure traced to its source and checked before it reaches the page. It is first a portfolio piece for Imane's job search in aviation finance and credit, built so it can grow into a daily analyst tool or a niche product.

Decisions taken for v1:

- **Purpose:** portfolio first, with an architecture that can carry daily use and a commercial version later.
- **Coverage:** European listed airlines and airports, using free structured filings (ESEF and UKSEF).
- **Interface:** a web app with PDF and Excel export.
- **Division of labour:** code computes every number; Claude extracts what the filings don't tag and drafts the commentary; a verifier checks every figure Claude touches.
- **Working name:** Airline Credit Tearsheet.

## Why this tool, and where it stands apart

AI-drafted credit reports are already routine at large firms, so the tool wins on sector depth and verifiability, not on drafting itself. [Robeco](https://www.robeco.com/en-int/insights/2026/08/how-ai-can-strengthen-credit-research) generates preliminary issuer reports with an in-house platform, [Moody's](https://www.businesswire.com/news/home/20260409047490/en/Moodys-Brings-Credit-and-Compliance-Workflows-Directly-into-Anthropics-Claude) offers memo generation and peer comparison agents inside Claude, and [Claude's finance offering](https://claude.com/solutions/finance) ships credit memo templates.

|  | Generic AI credit tools | This tool |
| --- | --- | --- |
| Sector logic | Same template for every corporate | Airline and airport metrics: lease-adjusted leverage, advance ticket sales, ASK, RASK, CASK, revenue per passenger |
| Figures | Written by the model, checked by the reader | Computed by code; the model can only reference them; a verifier blocks anything unchecked |
| Data | Paid feeds and terminals | Free regulatory filings in v1 |
| Analyst's role | Reviews a finished memo | Owns the view; the tool prepares the evidence |

For Imane, the value is a live demo that proves three things at once: she understands aviation credit, she can design an AI workflow, and she knows where AI output must be controlled. Commercially, the opening is coverage the big platforms neglect (MENA and African aviation and infrastructure), which later versions address.

## Goals and non-goals for v1

V1 succeeds if a recruiter can open a public link, pick an issuer and get a correct, sourced tearsheet without any setup.

Goals:

1. Produce a two-page tearsheet for any v1 issuer and fiscal year, in under a minute when the filing is cached.
2. Make every figure traceable: one click shows the filing fact, the formula or the quoted sentence behind it.
3. Let no AI-written figure reach the page without passing the verifier.
4. Run a demo mode with pre-generated tearsheets, so the public link works without an API key.
5. Keep the codebase clean enough to walk through in an interview: README, tests, architecture diagram.

Non-goals:

- Investment recommendations or ratings. The analyst writes the view.
- Paid data such as bond prices, spreads or rating feeds.
- Unlisted or non-European issuers (Royal Air Maroc, Gulf carriers, TAP). These move to v2.
- Half-year, quarterly or LTM figures. ESEF covers annual reports, so v1 is annual only.
- Logins, teams, alerts and monitoring.

## Users and core use cases

Imane is the v1 user and the demo owner; interviewers are the audience; credit and aviation finance analysts are the later market.

1. **Results review.** Pick an issuer and a fiscal year, read the draft, edit the commentary, write the analyst view, export the PDF.
2. **Peer positioning.** Compare leverage, liquidity and margins across the peer group, with the median and the issuer's rank.
3. **Audit a figure.** Click any number to see its source: the tagged filing fact with a link to the iXBRL viewer, the formula and its inputs, or the quoted sentence from the report.
4. **Interview demo.** A three-minute walkthrough on the public link: tearsheet, one audited figure, the verifier rejecting a bad draft.

## Issuer coverage

V1 covers nine issuers, six airlines and three airports, each confirmed in milestone M0 with at least three years of filings with the core statements tagged.

| Issuer | Type | Listing and format | Fiscal year end | Currency |
| --- | --- | --- | --- | --- |
| Air France-KLM | Network airline | Euronext Paris, ESEF | 31 Dec | EUR |
| International Airlines Group | Network airline group | Madrid, ESEF | 31 Dec | EUR |
| Finnair | Network airline | Helsinki, ESEF | 31 Dec | EUR |
| easyJet | Low-cost airline | London, UKSEF | 30 Sep | GBP |
| Norwegian Air Shuttle | Low-cost airline | Oslo, ESEF | 31 Dec | NOK |
| Wizz Air Holdings | Low-cost airline | London, UKSEF | 31 Mar | EUR |
| Groupe ADP | Airport | Euronext Paris, ESEF | 31 Dec | EUR |
| Aena | Airport | Madrid, ESEF | 31 Dec | EUR |
| Flughafen Wien | Airport | Vienna, ESEF | 31 Dec | EUR |

**Changed after M0** ([decision 0001](decisions/0001-issuer-go-no-go.md)). Deutsche Lufthansa, Ryanair and Fraport were in the original ten candidates but are not on filings.xbrl.org, which holds no German or Irish filings. Norwegian and Wizz Air replace Ryanair as the low-cost peers. Icelandair passed M0 and is kept in reserve.

**History.** All available fiscal years from FY2021, with the last three shown by default. Pre-2021 years predate the ESEF mandate and are out of scope.

**Fiscal years.** Issuers are compared on their fiscal year as reported, labelled with calendar months, for example "FY2025 (Apr 2024 to Mar 2025)" for Wizz Air. Peer views flag any issuer whose year end differs from the group's by more than three months.

**Currency.** Ratios need no conversion. Absolute amounts are shown in reporting currency on the tearsheet; peer size charts convert to EUR at the ECB average rate for income and cash flow items and the period-end rate for balance sheet items.

## Data sources

One free source carries v1: the annual filing itself, read twice, once as tagged numbers and once as text.

| Source | Provides | Access |
| --- | --- | --- |
| [filings.xbrl.org API](https://filings.xbrl.org/about.html) | ESEF and UKSEF annual reports: report package, xBRL-JSON facts, link to the iXBRL viewer | Free JSON:API, no key |
| [xbrl-filings-api](https://pypi.org/project/xbrl-filings-api) | Python client for the same API, with pandas output | pip; optional, the API can be called directly |
| Report text inside the iXBRL file | Traffic and fleet figures, undrawn credit facilities, fuel hedging | Same filing, read by Claude with a grounding check |
| ECB reference rates | EUR exchange rates for peer size charts | Free; endpoint confirmed in M0 |
| Manual inputs (YAML in the repo) | Peer groups, ratings if shown, per-issuer overrides | Maintained by Imane, each entry with a source and a date |

Three constraints shape the design:

- Primary statements are tagged figure by figure, but notes are tagged only as text blocks. Anything that lives in the notes, such as segment revenue or undrawn facilities, comes from text extraction.
- EBITDA, net debt and traffic metrics are non-IFRS and rarely tagged. The tool computes them with its own published definitions and shows the company's figure beside them when it can extract it.
- Issuers use company-specific extension elements for some lines. Mapping uses standard IFRS concepts first, then per-issuer overrides recorded in the repo.

## Metrics catalog

Every metric has one definition applied identically across issuers, so peers compare cleanly; the tearsheet footnote states that these differ from company-reported and agency-adjusted figures (no pension or hybrid adjustments in v1).

Credit metrics, for airlines and airports:

| Metric | Definition | Unit | Source |
| --- | --- | --- | --- |
| EBITDA | Operating profit + depreciation, amortisation and impairment | EUR m | Computed |
| EBITDA margin | EBITDA ÷ revenue | % | Computed |
| Total debt | Borrowings + lease liabilities, current and non-current | EUR m | Computed from tagged |
| Net debt | Total debt − cash and equivalents − liquid investments (defined per issuer) | EUR m | Computed |
| Net leverage | Net debt ÷ EBITDA | x | Computed |
| Gross leverage | Total debt ÷ EBITDA | x | Computed |
| Interest coverage | EBITDA ÷ interest expense, lease interest included | x | Computed |
| FFO | EBITDA − interest paid − income tax paid | EUR m | Computed |
| FFO to debt | FFO ÷ total debt | % | Computed |
| Free cash flow | Cash from operations − purchases of PP&E and intangibles | EUR m | Computed |
| FCF to debt | Free cash flow ÷ total debt | % | Computed |
| Capex intensity | Purchases of PP&E and intangibles ÷ revenue | % | Computed |
| Liquidity | Cash + liquid investments + undrawn committed facilities | EUR m | Computed and extracted |
| Liquidity to revenue | Liquidity ÷ revenue | % | Computed |
| Advance ticket cover (airlines) | Advance ticket sales ÷ (cash + liquid investments) | % | Tagged or override |

Airline operating metrics:

| Metric | Definition | Unit | Source |
| --- | --- | --- | --- |
| Passengers | Passengers carried | m | Extracted |
| ASK | Available seat kilometres | bn | Extracted |
| RPK | Revenue passenger kilometres | bn | Extracted |
| Load factor | RPK ÷ ASK | % | Computed |
| Passenger yield | Passenger revenue ÷ RPK | EUR cents | Computed |
| RASK | Revenue ÷ ASK | EUR cents | Computed |
| CASK | (Revenue − operating profit) ÷ ASK | EUR cents | Computed |
| CASK ex-fuel | (Revenue − operating profit − fuel cost) ÷ ASK | EUR cents | Computed |
| Fuel share of costs | Fuel cost ÷ (revenue − operating profit) | % | Computed |
| Fleet | Aircraft in operation and average age | count, years | Extracted |
| Fuel hedge ratio | Share of next twelve months' fuel needs hedged | % | Extracted |

Airport operating metrics:

| Metric | Definition | Unit | Source |
| --- | --- | --- | --- |
| Passengers | Passengers handled, scope defined per issuer (group or main hub) | m | Extracted |
| Traffic growth | Passengers ÷ prior-year passengers − 1 | % | Computed |
| Revenue per passenger | Revenue ÷ passengers | EUR | Computed |
| Aeronautical revenue per passenger | Aeronautical segment revenue ÷ passengers | EUR | Extracted and computed |
| Non-aeronautical share | Non-aeronautical revenue ÷ revenue | % | Extracted and computed |

In the repo, each metric lives in `metrics/catalog.yaml` with its id, label, inputs, unit, display format, a "higher is better" flag for peer colouring and a one-line definition that the tearsheet footnote reuses. A metric that can't be computed for an issuer shows as missing with a reason, never as zero.

## System design

Seven stages run in sequence around one facts store, and every number in the system is a fact that carries its provenance.

&#91;embedded content: pipeline · 7 stages around one facts store\]

Stages 1 to 3 are plain code. Stages 4 and 5 use Claude, and nothing they produce reaches the store or the page without a check in code.

**Data model.** Three tables in a local DuckDB file:

- `facts`: issuer, fiscal year, period end, canonical concept, value as reported, decimals, currency, source type (tagged, computed, extracted, manual), source reference (filing hash and XBRL concept; formula id and input fact ids; document location and quote; or override author and reason), status (verified, unverified, overridden).
- `drafts`: issuer, fiscal year, section, text with placeholders, model, prompt version, input hash, verifier report.
- `runs`: one manifest per tearsheet with filing hashes, model ids, prompt versions, token use, cost and timestamp.

| Layer | Choice | Reason |
| --- | --- | --- |
| Language and tooling | Python 3.12, uv, ruff | Quick setup, one lockfile |
| Filing access | httpx against the filings.xbrl.org API | Free JSON, no key |
| Storage | DuckDB file, raw xBRL-JSON cached on disk | SQL without a server, offline reruns |
| Data handling | pandas, Pydantic models, YAML config | Familiar to analysts, typed boundaries |
| LLM | Anthropic Python SDK: `claude-sonnet-5-5` drafts, `claude-haiku-5-5` extracts, both configurable | Structured output through tool use |
| Web app | Streamlit | Fastest path to a shareable demo |
| Charts | Altair, with vl-convert for static images | One library for app and PDF, no browser needed |
| PDF | Jinja2 HTML template and WeasyPrint | Print-quality A4 from HTML and CSS |
| Excel | XlsxWriter | Writes live formulas |
| Tests and CI | pytest, recorded API fixtures, GitHub Actions | No network calls in tests |

Repo layout:

```text
airline-credit-tearsheet/
  pyproject.toml
  CLAUDE.md
  docs/            SPEC.md, metrics.md, decisions/, progress.md
  config/          issuers.yaml, peers.yaml, models.yaml
  src/tearsheet/
    ingest/        filings.xbrl.org client, cache
    normalize/     concept_map.yaml, overrides/<issuer>.yaml, mapper
    store/         DuckDB schema and access
    metrics/       catalog.yaml, formulas, peers
    extract/       section locator, Claude extraction, grounding check
    narrative/     prompts/, fact sheet builder, drafting, verifier
    render/        PDF template, Excel writer, charts
    app/           Streamlit pages
  tests/           unit, golden files, verifier adversarial cases, fixtures/
  samples/         pre-generated tearsheets for demo mode
  data/            local cache (gitignored)
```

## AI layer and figure verification

Claude never writes a number into the tearsheet: it either extracts a figure with a quote that code then checks, or references figures by id in prose that code fills in.

**Job 1: extracting what the filing doesn't tag.**

1. A section locator searches the report text for the relevant passages (for example "available seat kilometres", "load factor", "undrawn") and sends only those to Claude, which keeps cost low.
2. Claude returns structured output through tool use: metric id, value, unit, period, verbatim quote, location in the document.
3. Code checks that the quote appears verbatim in the document (whitespace normalised), that the value appears in the quote after unit normalisation, and that the period matches the fiscal year.
4. A value that passes is marked verified. One that fails is marked unverified and stays off the tearsheet until the analyst approves or corrects it in the app; every correction is stored as an override with author, date and reason.

**Job 2: drafting the commentary.**

1. A fact sheet builder hands Claude a JSON payload: metric ids and values, prior-year values, peer medians, and precomputed changes with their direction (up, down or flat, against a threshold per metric).
2. Claude writes each section with placeholders such as `{{net_leverage@FY2025}}` and returns, for each sentence, the fact ids it relies on and the direction it claims.
3. A renderer replaces placeholders with formatted values (2.4x, 18.3%, EUR 1.2bn), so formatting is consistent everywhere.

The verifier rejects a draft when it finds a number written outside a placeholder (fiscal year labels and names such as "IFRS 16" are allowed), an unknown placeholder, or a claimed direction that contradicts the computed change. Rejection triggers up to two retries with the error list fed back; after that the draft goes to the app flagged for manual editing.

Drafted sections: snapshot (three sentences), credit metrics, operating performance, liquidity and funding, peer positioning, watch items. The **analyst view** is never drafted: the app shows an empty box that only the analyst fills.

Prompts live in versioned files. Imane writes two example notes in her own sell-side style, used as few-shot examples, so the output reads like her work. Every output stores the model, the prompt version and an input hash, and identical inputs are served from cache.

## Web app and exports

The app has four pages and two modes; the PDF and the Excel file are generated from the same facts the screen shows.

| Page | What it shows | What the analyst can do |
| --- | --- | --- |
| Tearsheet | Header (issuer, type, fiscal year with calendar months, currency, rating if entered), KPI cards, net leverage and liquidity charts, commentary | Edit commentary, write the analyst view, click any figure for its source, export PDF and Excel |
| Peers | Metrics across the peer group with median and rank; net leverage against EBITDA margin as a scatter | Switch peer group, sort by any metric |
| Data and audit | Every fact for the issuer and year with source type and status; extracted values with their quotes; link to the iXBRL viewer; run manifest | Approve or correct unverified values, with a reason |
| Method | Definitions, data sources, limits, disclaimer | Read only |

**Modes.** Demo mode serves pre-generated tearsheets from the repo and needs no API key. Live mode generates new drafts and needs a key from Streamlit secrets or entered for the session only, never stored.

**PDF tearsheet, two A4 pages.** Page 1: header, snapshot, a four-year KPI table, two charts, credit metrics commentary. Page 2: operating metrics, peer table, liquidity and funding, watch items, analyst view, then footnotes with definitions, filing links and the line "Draft prepared with AI assistance. Figures computed from regulatory filings and checked automatically. Not investment advice."

**Excel backup.** Sheets: Inputs (tagged and extracted facts with sources), Metrics (live formulas that reference Inputs, so a reviewer can trace each ratio), Peers, Extracted (values with their quotes), Manifest. Recalculated in Excel, every metric must equal the app's value.

## Quality, testing and evaluation

Imane's own hand-built model is the reference: the tool is right when it matches what a credit analyst computes manually from the same filing.

| Check | How | Pass mark |
| --- | --- | --- |
| Reconciliation | Imane models two issuers she knows (Air France-KLM and Groupe ADP) over two years by hand | Leverage within 0.05x, margins and ratios within 0.1 point |
| Formulas | One unit test per metric, with hand-calculated fixtures | All green in CI |
| Normalisation | Golden files per issuer: mapped statement lines for each year | No unexplained diff |
| Extraction | A labelled set of about 30 traffic and fleet values across the six airlines, labelled by Imane | No wrong value marked verified; at least 80% verified automatically |
| Verifier | Adversarial drafts with wrong numbers, wrong directions and unknown placeholders | 100% rejected |
| Commentary | Imane scores 10 drafts from 1 to 5 on accuracy, relevance, concision and credit insight | Average of 4 or more before the public demo |

Unit tests never call the network; they run on recorded API responses stored in `tests/fixtures/`.

## Security, cost, deployment and legal

The public demo spends no API budget and exposes no secret; live generation stays behind a key.

- **Secrets.** The API key comes from an environment variable or Streamlit secrets only. A pre-commit hook and a CI step (gitleaks) block any committed secret.
- **Cost.** Every run logs tokens and cost in its manifest. Identical inputs hit the cache, so regenerating a tearsheet costs nothing. A per-run budget is set after M4, once real usage is measured.
- **Deployment.** Public demo on Streamlit Community Cloud from the GitHub repo, demo mode by default. A Dockerfile is added in M7 so the app can later run on any host.
- **Legal.** Data comes from public regulatory filings. Ratings, if shown, are entered by hand with agency name and date; no agency research is reproduced. The method page and the PDF carry a "not investment advice" disclaimer. No personal data is processed.

## Milestones

Eight milestones in three phases, each phase closed by a gate that must pass before the next one starts; sizes are relative (S, M, L) until M0 shows how clean the data really is.

&#91;embedded content: roadmap · 3 phases, 3 gates\]

Gate 1 sits at the end of M2, gate 2 at the end of M4, gate 3 at the end of M7; the checklists below are the acceptance criteria for each milestone.

### M0 · Data feasibility spike (S)

Builds: a notebook and a coverage matrix (issuer × year × core concept: found, extension, missing), the list of extension concepts per issuer, the ECB rates endpoint.

- [ ] Matrix covers all ten candidates
- [ ] At least eight issuers confirmed with three or more years
- [ ] Go or no-go per issuer recorded in `docs/decisions/`

### M1 · Ingestion and normalisation (M)

Builds: filing download and cache, xBRL-JSON parser, canonical concept map with per-issuer overrides, facts table with provenance.

- [ ] Core statement lines loaded for every v1 issuer and year
- [ ] Two issuers × two years spot-checked against the published statements: 100% match
- [ ] A rerun from cache works offline and changes nothing

### M2 · Metrics engine and peers (M)

Builds: `catalog.yaml`, formula functions, peer groups, medians and ranks.

- [ ] Every catalog metric computed, or missing with a stated reason
- [ ] Unit tests green
- [ ] Reconciliation with Imane's hand model within tolerance (gate 1)

### M3 · Extraction with grounding (M)

Builds: section locator, Claude extraction through tool use, grounding checks, review statuses.

- [ ] No wrong value marked verified on the labelled set
- [ ] At least 80% of labelled values verified automatically
- [ ] Every unverified value visibly flagged

### M4 · Drafting and verifier (L)

Builds: fact sheet builder, prompts and few-shot examples, placeholder renderer, verifier, retries, prompt versioning, cache.

- [ ] Adversarial suite 100% rejected
- [ ] Ten consecutive drafts across issuers with zero unreferenced numbers (gate 2)
- [ ] Commentary score of 4 or more

### M5 · Web app (M)

Builds: the four pages, demo and live modes, overrides, analyst view.

- [ ] A pre-generated tearsheet opens in under ten seconds
- [ ] Every figure on screen shows its source on click
- [ ] Demo mode works without a key

### M6 · Exports (M)

Builds: two-page PDF, Excel with live formulas, run manifest.

- [ ] PDF fits two pages for every v1 issuer, with no overflow
- [ ] Excel recalculates to the app's values
- [ ] Manifest lists filing hashes, model and prompt version

### M7 · Portfolio packaging (S)

Builds: public deployment, Dockerfile, README with the architecture diagram and design choices, three sample PDFs, a three-minute demo script, a LinkedIn post draft, the CV line.

- [ ] Public link works in a fresh browser with no key (gate 3)
- [ ] Imane can explain every stage of the pipeline without notes

## Beyond v1

The v1 architecture already separates sources, metrics and narrative, so later versions add inputs and features without a rewrite.

**v2, daily use.** PDF ingestion for issuers outside ESEF (Royal Air Maroc, Gulf carriers, unlisted European groups), half-year reports and monthly traffic releases, LTM figures, a watchlist that flags a metric crossing a threshold, covenant headroom tracking.

**v3, commercial.** The angle is coverage the big platforms neglect: MENA and African aviation and infrastructure issuers, with verified figures as the selling point. Further templates can follow the same pattern, starting with real estate from Imane's Natixis work. Before building v3, test willingness to pay through five conversations with aviation finance or credit teams, and try selling tearsheets as a service first.

## Open questions

Seven decisions are still open; the first three should be settled before M2.

- [ ] Peer groups: one airline group, or network carriers and low-cost carriers compared separately?
- [ ] Liquid investments: which current financial assets count as cash-like, issuer by issuer?
- [ ] Ratings: show hand-entered agency ratings with source and date, or leave them out of v1?
- [ ] Repository owner: Imane's GitHub account, so the portfolio is clearly hers?
- [ ] License: MIT for visibility, or source-available to keep the commercial option open?
- [ ] Commentary language: English only, or an English and French toggle?
- [ ] Live mode on the public link: closed, or open with each visitor's own key?

## Working instructions for Claude Code

Export this doc as Markdown to `docs/SPEC.md`, then build one milestone per session, never two at once.

Rules to copy into `CLAUDE.md` at the repo root:

- Start each milestone with a written plan and wait for approval before coding.
- End each milestone with tests green, its checklist ticked in `docs/progress.md`, and a short walkthrough Imane can follow.
- Never hardcode a financial figure. Every metric lives in `catalog.yaml` and has a unit test.
- Store values as reported with their decimals; round only when rendering.
- No network calls in unit tests; use recorded fixtures.
- No LLM output reaches the tearsheet without the verifier. Any prompt change bumps the prompt version.
- Secrets only from the environment. Ask before adding a dependency that isn't in the stack table.
- Record every non-obvious choice as a short note in `docs/decisions/`.

First prompt for Claude Code:

```text
Read docs/SPEC.md. We are starting milestone M0 only (data feasibility spike).
Propose a plan first: how you will query filings.xbrl.org for the ten candidate issuers,
which core IFRS concepts you will check per filing, and the shape of the coverage matrix.
Do not write application code yet. Wait for my approval of the plan.
```
