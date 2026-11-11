# The pipeline in seven stages

For the second M7 checklist item: being able to explain every stage without notes. For each
stage: what goes in, what comes out, what can go wrong, and what checks it. Then ten questions
an interviewer might ask, with the answer's key points. A finance analogy for each stage in
brackets.

## 1 · Ingest (collecting the data room)

- **In:** the company's annual filing on filings.xbrl.org, in ESEF or UKSEF format: the
  statements tagged figure by figure (xBRL-JSON). Two FY2025 statements not yet in the database
  (Air France-KLM, ADP) were entered by hand from the PDFs and reviewed by you.
- **Out:** every tagged figure, exactly as filed, cached on disk; a fingerprint (SHA-256) of each
  filing.
- **Can go wrong:** a filing missing from the database (Lufthansa, Ryanair, Fraport); a company
  restating a year.
- **Checked by:** the spot check against the published statements (68 of 68); the prior-year
  column of each hand entry compared with the database (36 of 36).

## 2 · Normalise (mapping to a standard chart of accounts)

- **In:** the tagged figures, under IFRS names or company-specific ones.
- **Out:** canonical lines (revenue, borrowings, lease liabilities, cash...) with their source,
  in one facts store (a small database), values kept with their decimals.
- **Can go wrong:** a company tagging a line under its own name, or with the opposite sign.
- **Checked by:** the concept map tries standard IFRS concepts first, then per-company overrides
  written with evidence; golden files catch any unexplained change.

## 3 · Compute (the model)

- **In:** the canonical lines.
- **Out:** every metric in `catalog.yaml`, one definition for all issuers: EBITDA, net debt
  (each company's own cash-like list), leverage, coverage, FFO to debt, liquidity, RASK,
  CASK...; peer medians and ranks on aligned fiscal years (easyJet to September, Wizz Air to
  March).
- **Can go wrong:** a ratio that means nothing (leverage on negative EBITDA, ratios to a tiny
  debt): shown as n.m., never as a number; a missing input: shown as n.a. with the reason.
- **Checked by:** one unit test per metric; gate 1, a second-source model rebuilt from the PDFs
  and recalculated in a spreadsheet (62 of 62 within 0.05x and 0.1 point); in M6 every metric
  as a live Excel formula, recalculated to the app's value (2,044 of 2,044).

## 4 · Extract, with AI (reading the notes)

- **In:** the annual report text, cut down to the passages that matter (traffic, fleet,
  hedging, undrawn facilities, airport segments).
- **Out:** each figure with the exact sentence it came from and the page.
- **Can go wrong:** the AI reads the wrong year, the wrong scope, or a figure from the next
  column.
- **Checked by:** code, the grounding checks: the quote must be in the report, the value in the
  quote, the year right. A figure that fails waits for your review ("pending") and never
  reaches the page. On 93 hand-labelled figures, none wrong was marked verified; but only 59% to
  78% pass automatically, short of the 80% goal; the rest come to you.

## 5 · Draft, with AI (the junior's first draft)

- **In:** a fact sheet: only the verified figures, each with an id, the change computed by code
  and its direction (up, down, flat; better or worse), the peer median and rank, the events of
  the year read from the report.
- **Out:** six sections of sentences with blanks (`{{net_leverage@FY2025}}`) and, for each
  figure, the direction the AI claims. Never a number.
- **Can go wrong:** the AI types a number, invents a figure, or says "improved" when it worsened.
- **Checked by:** stage 6.

## 6 · Verify (the senior's review)

- **In:** the AI's draft and the fact sheet.
- **Out:** each sentence passed or rejected, with the rule: no number outside a blank (1); only
  known, verified figures (2); claimed directions must match code (3); direction words must be
  backed by a claim (4); the form and the sentence must list the same figures (5); an earlier
  year must be named (6).
- **Can go wrong:** a sentence can be safe but weak (the commentary scored 3.78 of 5); a clause
  can borrow the claim of another figure in the same sentence.
- **Checked by:** the adversarial suite, 47 planted faulty sentences, all rejected for the right
  rule, and correct sentences all passing. Rejected sections go back to the AI twice at most;
  a sentence still wrong is removed.

## 7 · Publish (the deliverable)

- **In:** the facts and the checked draft, your edits and your analyst view.
- **Out:** the web app (every figure clickable down to its source), the two-page PDF, the Excel
  backup with live formulas, the run manifest (filing fingerprints, models, prompt versions).
- **Can go wrong:** a page overflowing; a figure awaiting review printed as a number.
- **Checked by:** tests: 18 of 18 PDFs on two pages with no overflow, measured on the laid-out
  page; "pending" never printed as a number; every figure on screen traced (1,986 of 1,986).

## Ten questions, with the key points

1. **Why not let the AI write numbers and check them after?** Checking means finding each
   number's source; here every number has one by construction, and the AI can't introduce one.
2. **What does the AI do that code can't?** Read unstructured text (traffic, fleet, hedging,
   undrawn lines) and write fluent prose. Both are checked by code.
3. **How do you know a figure read from the report is right?** The quote must be in the report,
   the value in the quote, the year right; otherwise it waits for an analyst. Tested on 93
   labelled figures: none wrong was verified.
4. **What happens when the AI gets a direction wrong?** Rule 3 or 4 rejects the sentence; the
   AI gets the errors back, twice at most; after that the sentence is removed or the section
   flagged for manual editing.
5. **Why are your metrics different from the company's?** One definition for all issuers, so
   peers compare; no pension or hybrid adjustments in v1. The footnotes say so.
6. **How do you compare easyJet (September) with Air France-KLM (December)?** Each fiscal year is
   placed in the peer year whose 31 December falls within six months of its year end; the
   difference is shown.
7. **What is the weakest part?** The commentary's insight (3.78 of 5) and the extraction rate
   (below 80%): the safety controls hold, the productivity targets were not fully met.
8. **What if the AI provider changes?** One configuration line; every answer is recorded with
   the model and prompt version, so results are reproducible and auditable.
9. **What does it cost to run?** The public demo costs nothing: it serves pre-built tearsheets.
   Identical requests are replayed from the record, so rebuilding is free.
10. **What would you build next?** Half-year and monthly traffic data, covenant headroom, and
    issuers outside ESEF (MENA and African aviation) from PDFs, the coverage the big platforms
    neglect.
