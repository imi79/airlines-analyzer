# M5 plan: the web app, where the tearsheet is read, audited and finished

Status: **draft, waiting for Imane's approval.** No app code is written until the plan is
approved (working rules). Starting point: `main` at the M4 close, 381 tests green.

## What M5 is for

M1 to M4 built every piece of the tearsheet: the figures, the ratios and peers, the operating
figures read from the reports, and the commentary drafted by the AI and checked by code. Today
they live in report pages under `docs/`. M5 puts them in front of a reader: a web app where a
recruiter or an analyst picks a company and a year, reads the tearsheet, clicks any figure to
see where it came from, and where you edit the commentary and write your own view.

Think of it as moving from the working papers to the client-facing deliverable, with the
working papers one click behind every number.

## The four pages (spec)

1. **Tearsheet.** Header: company, type (network airline, low-cost airline, airport), fiscal
   year with its months ("FY2025 (Apr 2024 to Mar 2025)" for Wizz Air), currency. No rating
   (decision 0008). Then KPI cards (EBITDA margin, net leverage, interest coverage, liquidity
   to revenue, and passengers), a four-year KPI table, two charts (net leverage, and liquidity
   against revenue, over four years), and the six commentary sections. Below them, the
   **analyst view**: an empty box only you fill. You can edit any commentary sentence.
2. **Peers.** The peer table for the company's group (network, low-cost, airports, all
   airlines), with the median and each company's rank, sortable by any metric. A scatter of
   net leverage against EBITDA margin. Companies whose year end differs from the group's by
   more than three months are flagged (easyJet, Wizz Air), as in `docs/m2/peers.md`.
3. **Data and audit.** Every figure for the company and year: where it comes from (tagged in
   the filing, computed, read from the report text, entered by hand) and its status (verified,
   unverified, overridden). Figures read from the report text show their quote and page. A
   link to the filing in the iXBRL viewer. The run record of the draft (model, prompt version,
   tokens, filings used). This is where you **approve or correct** an unverified figure, with
   a reason, exactly as you would in `config/extraction_reviews.yaml` today.
4. **Method.** Every metric's definition (from `catalog.yaml`), the data sources, the limits
   (no pension or hybrid adjustments, annual only, our own definitions differ from company and
   agency figures) and the disclaimer "Not investment advice".

## Clicking a figure: the source card

Every figure on screen opens a **source card**, the audit trail of that one number:

| Figure is... | The card shows |
| --- | --- |
| Tagged in the filing | the filing, the IFRS line it was tagged as, the value as tagged, the period, the filing's fingerprint, and a link to the iXBRL viewer |
| Computed (a ratio, EBITDA, net debt...) | the formula in words, each input with its value, and each input clickable in turn, down to the filing |
| Read from the report text | the quote, the page, the document, the checks it passed, and who approved it if you did |
| Entered by hand | who entered it, when, from which document and why |
| A change, a peer median or a rank | the two values compared, or the peer values behind the median and the rank |

In the commentary, every figure is highlighted and each sentence has a small **sources**
button that opens the cards of all its figures (see question 1 on why per sentence).

## Two modes (spec)

- **Demo mode** (the default, and what the public link will run): reads pre-built tearsheets
  committed in `samples/`. No API key, no database, no internet needed. This matters because
  the database (`data/`) is not in the repository: it is rebuilt from the filings, which needs
  the internet. A fresh machine, like the free Streamlit hosting, cannot do that quickly.
- **Live mode** (on your machine or a cloud session where the database is built): reads the
  database directly, applies your approvals and edits, and can ask the AI to redraft a
  tearsheet. The API key comes from the environment (or Streamlit secrets), or is typed into
  the app for the session only: it is kept in memory, never written to a file, and the AI
  layer and verifier are unchanged (same provider choice in `config/models.yaml`).

**The pre-built tearsheets.** A new command, `uv run tearsheet samples`, writes one file per
company and year into `samples/` with everything the four pages need: header, KPI table, chart
series, commentary (with its blanks, the printed text and the verifier's report), every
source card, the peer tables and the run record. It is a readable text file (JSON), so any
change shows up in the history. Think of it as the printed board pack produced from the live
model: the demo shows the pack, live mode opens the model.

## Your edits and approvals

- **Approving or correcting a figure** writes to `config/extraction_reviews.yaml` (the file
  you already use), with your name, the date and the reason, then rebuilds the figures. The
  approved figure then becomes available to the commentary at the next draft.
- **Editing the commentary and writing the analyst view** saves to `notes/<company>_FY<year>.yaml`
  (new folder), kept separate from the AI's text. Edited sentences are marked "edited by the
  analyst". The verifier also reads your edits and **warns** if you typed a figure that is not
  linked to a source (question 3).
- **In demo mode**, edits and approvals last for the visitor's session only and are never
  saved, so a visitor cannot change the public tearsheet.

## How we know it works (the M5 checklist)

- [ ] **A pre-generated tearsheet opens in under ten seconds.** Measured in a real browser on
      the 18 tearsheets, from opening the page to the commentary on screen; times recorded in
      `docs/m5/timing.md`.
- [ ] **Every figure on screen shows its source on click.** A test walks through every figure
      the four pages display, for every tearsheet, and checks each has a source card that
      leads down to a filing, a quote or a named hand entry. Plus screenshots of a click-through
      for one tagged, one computed and one quoted figure.
- [ ] **Demo mode works without a key.** A test opens all four pages with no API key, no
      `data/` folder and the internet blocked.

Other tests: the approve and correct form refuses a missing reason or a malformed value; the
typed key never reaches a file or a log; every page renders for all nine companies. The app
is tested with Streamlit's own page tester, which runs the pages without a browser, so the
tests stay fast and offline.

## Order of work

1. The pre-built tearsheet files and the `samples` command, with tests (no app yet).
2. The source cards, with the "every figure has a source" test.
3. App frame: page menu, company and year picker, demo and live modes; the Method page.
4. Tearsheet page: header, KPI cards and table, the two charts, commentary with sources,
   editing and the analyst view.
5. Peers page.
6. Data and audit page, with approve and correct.
7. Live mode: the key, redrafting one tearsheet through the existing drafting and verifier.
8. Timing in a browser, screenshots, walkthrough, decision notes, checklist.

No AI tokens are needed except one optional live redraft at step 7 to show the mode works
(about 50,000 tokens).

## New software

Streamlit (the web app) and Altair (the charts) are both in the spec's stack table, so no new
choice; they are added to `pyproject.toml` at step 3. Nothing else.

## Known difficulties

- **Clicking a number inside a sentence.** Streamlit, the app framework chosen in the spec,
  makes buttons, table rows and chart points clickable, but not a word in the middle of a
  paragraph. Hence the per-sentence sources button (question 1).
- **Every click redraws the page.** Streamlit reruns the page on each interaction. Edits are
  kept in the session so nothing typed is lost; the pre-built files keep each redraw quick.
- **The free hosting forgets files.** Streamlit Community Cloud wipes any file the app writes
  when it restarts. That is why demo mode saves nothing, and saving edits is a live-mode,
  own-machine feature. Deployment itself is M7.
- **Unverified figures** still wait for your review (for example Air France-KLM's undrawn
  facilities and IAG's load factor). On the tearsheet they show as "awaiting review", never as
  a number; the Data and audit page is where you clear them.
- **Older years.** Commentary exists for each company's latest two years (the 18 M4 drafts).
  Earlier years have figures but no commentary (question 2).

## Questions for Imane

1. **Clicking figures in the commentary.** (a) One "sources" button per sentence that opens
   the cards of all its figures, built with Streamlit's standard pieces; or (b) each number in
   the sentence clickable on its own, which needs a small custom web component (more code to
   build and maintain). Figures in tables, cards and charts are clickable on their own either
   way. Recommendation: (a) for v1.
2. **Years in the demo.** (a) The 18 tearsheets with commentary (latest two years per
   company); or (b) also the earlier years, figures only, marked "no commentary drafted".
   Recommendation: (a), the tearsheet is the commentary plus the figures.
3. **A figure you type into the commentary yourself.** The analyst owns the text, but a typed
   number has no source card. (a) Warn and mark the sentence "contains a figure not traced to
   a source"; or (b) refuse to save it until you use a blank. Recommendation: (a).
4. **Live mode on the public link** (open question in the spec). (a) Closed: the public link
   is demo only, live mode runs where the database is built; or (b) open with each visitor's
   own key. Recommendation: (a) for v1; (b) would need the database and the filings on the
   free hosting.
5. **Working branch.** The project rules say branches are named after the work and never
   contain "claude"; this session was opened on `claude/confident-darwin-jdok3e`.
   Recommendation: build M5 on `m5-web-app`, following the project rules, and merge into
   `main` when the checklist is green.

Working rule reminder: one milestone per session. Once you approve, I'd start building M5 in a
fresh session (or this one, if you prefer), on the branch you choose in question 5.
