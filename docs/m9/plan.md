# M9 plan: a watchlist of credit triggers

Status: **waiting for Imane's approval** (written 2026-11-12). Branch: `m9-watchlist` (renamed if
another scope is chosen in question 1).

## What M9 is for

The spec's v2 ("daily use") lists a watchlist that flags a metric crossing a threshold. After
M8, the tool holds the figures such a watchlist needs (leverage, coverage, liquidity, debt due
within a year, cash flow after leases), all checked. M9 turns them into the first thing a credit
analyst looks at each morning: **which of my names crossed a trigger, and why?**

Think of it as covenant-style triggers that you set yourself: "net leverage above 3.0x",
"liquidity below the debt due within a year", "cash flow after leases negative". The tool checks
every company and year against them, and shows which triggers fired, with the figures behind
each, one click from their sources.

## Why this and not the other candidates

I checked the reports before choosing:

| Candidate | What I found | Size |
| --- | --- | --- |
| **A. Watchlist of triggers** (recommended) | Uses figures already verified; no new data source; no AI tokens; a page a recruiter understands in ten seconds | M |
| B. Half-year and last-twelve-months figures | ESEF holds annual reports only: half-year reports are PDFs, so this needs PDF ingestion first (the spec's v2 starting point) | L |
| C. Covenant headroom | Little to track: IAG states it has no financial covenants on its loans; easyJet and Wizz Air state none; Finnair has one (net debt to EBITDA of at most 3x on its credit facility); ADP's and Aena's sit in subsidiaries' project loans | S, low value |
| D. Icelandair as a tenth company | Passed M0, kept in reserve: shows the pipeline extends; about 300,000 tokens | M |
| E. Commentary score to 4 of 5 | The v1 miss (3.78); needs a new prompt round and your scoring | M |
| F. Maturity wall coverage (prompt round 2) | Raises the 6 of 18 tearsheets with a wall; judged on fresh reports | S |

## What gets built (option A)

1. **Triggers you set** in `config/watchlist.yaml`: metric, condition, threshold, which companies
   (all, airlines, airports), and a one-line reason, with your name and date. Two kinds:
   - **level**: net leverage above 3.0x, interest coverage below 3.0x, short-term debt cover below
     1.0x, FCF after leases below zero, liquidity to revenue below 20%;
   - **move**: net leverage up by more than 0.5x on the year, EBITDA margin down by more than
     3 points.
   I propose these defaults (question 2); you change them.
2. **The check, in code**: every company and year against every trigger, from verified figures
   only. A trigger whose figure is missing, not meaningful or awaiting review shows as **cannot
   assess**, never as passed, with the reason.
3. **A Watchlist page** in the app: companies down the side, triggers across the top, each cell
   fired / clear / cannot assess. Click a fired cell for the figure, the threshold, last year's
   value and the source card. A filter for "fired this year, not last year" (new warnings).
4. **On the tearsheet**: a line under the ratings, "Watchlist: 2 triggers fired (net leverage
   above 3.0x; cash flow after leases negative)", linking to the page. The PDF gets the same line
   (question 3).
5. **Tests and records**: one test per trigger kind, one for "cannot assess", one that every
   fired cell traces to a source; decision 0023; walkthrough.

No new software, no AI tokens. The commentary is not redrafted: triggers are shown beside it,
not written into it.

## How we know it works (the M9 checklist)

- [ ] Every trigger in `config/watchlist.yaml` evaluated for every company and year shown, from
      verified figures only; missing or unverified figures shown as "cannot assess" with the reason
- [ ] Every fired trigger traces to the figure behind it on click (test over all 18 tearsheets)
- [ ] Unit tests for each trigger kind, the edges (exactly at the threshold) and "cannot assess"
- [ ] The PDF still fits two pages for all 18 tearsheets

## What you do

1. Answer the five questions below, including the triggers you want (question 2).
2. Read the Watchlist page once it's built, and tell me if a fired trigger surprises you.
3. Say go to merge into `main`.

## Questions for Imane

1. **Scope.** (A) Watchlist of triggers; (B) half-year and last-twelve-months figures, which
   needs PDF ingestion and is a large milestone; (D) Icelandair as a tenth company; (E) commentary
   score; (F) maturity coverage. Recommendation: **A**: it makes daily use of everything built so
   far, costs no tokens, and is easy to demonstrate. B is the natural M10.
2. **The triggers.** Recommendation: start with the seven above, the same for every company,
   except liquidity to revenue for airlines only (airports carry less liquidity by design); you
   adjust thresholds after seeing the first results.
3. **Where the flags show.** (a) The Watchlist page only; (b) the page and a line on each
   tearsheet and PDF. Recommendation: (b).
4. **Missing or unverified figures.** Recommendation: shown as "cannot assess" with the reason,
   never as clear (a watchlist that silently passes what it cannot see is worse than none).
5. **Which session.** Your rules say one milestone per session, and this session built M8.
   Recommendation: approve here, and I build M9 in a fresh session, starting from this plan.
