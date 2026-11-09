# 0019 · M5: the web app, its two modes and how a figure shows its source

Date: 2026-11-09 · Status: plan approved by Imane with every recommendation ("approved with
all recommendations, go ahead on m5-web-app")

**Choices approved with the plan** (`docs/m5/plan.md`):

1. **Commentary sources per sentence.** Each sentence has one sources button that opens the
   cards of all its figures. Figures in the KPI cards, tables and charts open on their own
   (a click on the card's button, the table row or the chart point). Streamlit cannot make a
   word inside a paragraph clickable without a custom web component.
2. **The demo holds the 18 drafted tearsheets** (each company's latest two years). Live mode
   offers every year in the database, with "not drafted" for years without commentary.
3. **A figure typed by the analyst is flagged, not refused.** An edited sentence keeps its
   links wherever the printed figure ("1.71x") is left as it was; any other number is marked
   "contains a figure not traced to a source", found by the verifier's own number finder.
4. **The public link is demo only** (closes the spec's open question on live mode). Live mode
   appears only where the database exists, and never with `TEARSHEET_DEMO_ONLY=1`.
5. **Branch `m5-web-app`**, following the project rules (no "claude" in branch names).

**Choices made while building:**

- **Demo files: one shared figure file plus one file per tearsheet**, not one self-contained
  file per tearsheet as the plan said. `samples/figures.json` holds every figure of the nine
  companies with its source (1,986 figures, 2.2 MB); `samples/tearsheets/` holds the 18
  tearsheets (commentary, fact sheet, events, run record, about 80 KB each). The Peers page
  and every source card need other companies' figures, so a self-contained file would repeat
  them 18 times. Both are text files, rebuilt by `uv run tearsheet samples`, and a test
  checks they equal what today's database gives.
- **One code path for both modes.** The app reads a "figure library" built either from the
  database (live) or from the demo file; the pages, cards and tests use the same functions.
- **The commentary is checked against today's figures.** Each tearsheet compares the
  fingerprint of its fact sheet with the one the draft was written from; if a review has
  changed a figure since, the page says the commentary needs a redraft.
- **Ratios to a very small debt show as "n.m."** (not meaningful) in the tables, cards and
  peer views, and are left out of peer medians and ranks, using the rule the M4 fact sheets
  already apply (gross leverage below 0.5x, decision 0018). Vienna's FFO to debt is 442%: a
  real calculation, but no credit signal. Without this, the Peers page median would differ
  from the median quoted in the commentary. The figure itself still opens its source card.
  The M2 peer report (`docs/m2/peers.md`) is unchanged and still includes them.
- **Peer medians and ranks on the Peers page use verified figures only**, like the fact
  sheets; a figure awaiting review is shown as "awaiting review", never as a number. The M2
  report marks such figures with a star and counts them.
- **Approvals in live mode** go to `config/extraction_reviews.yaml` (the file Imane already
  uses), then a "Rebuild the figures" button runs `tearsheet all --offline`. **Redrafting**
  runs `tearsheet draft --issuer <company>`, which replays recorded answers for free and only
  asks the AI where the figures changed. A key typed into the app is passed to that run in
  memory only; a test checks it is never written to a record.
- **In demo mode an approval updates the figure and the ratios built on it for the visitor's
  session**; a correction changes the figure only (ratios are recomputed in live mode).
- **A link opens a given tearsheet**: `?company=wizz&year=2026`, for the demo script (M7).
- **New software:** Streamlit 1.67 and Altair 6.3, both in the spec's stack table.
