# 0012 · M3 answer key read by code, without AI

Date: 2026-11-01 · Status: accepted (Imane: "the answer key built by code"; option B of the
M3 plan, question 3)

**Context.** The M3 checklist scores the extraction against a labelled answer key. The spec has
Imane label it by hand; Imane asked for it to be built by code, as for the gate 1 model
(decision 0009).

**What was done to keep it independent** (`spikes/m3/answer_key.py`):
- **No AI, and none of the extraction code.** Its own text conversion (a plain tag stripper,
  `pdftotext` for PDFs), its own number reader, no section locator and no grounding checks.
- **Fixed anchors.** Each figure is found by the words printed around it in the report, written
  down by reading the report. An anchor must match exactly once, or the build stops: nothing
  is guessed.
- **Written first.** The key was built and committed before the AI read any report, and not
  changed after seeing its answers (the git history shows the order).
- **Checkable.** For every line, `docs/m3/answer_key.csv` keeps the number as printed, the
  page and the text around it: search the report for that text to check it.

**What is in it.** 25 figures for the six airlines, latest report with operating figures:
passengers, ASK, RPK, fleet, fuel hedge ratio, undrawn committed facilities. Air France-KLM is
read from its FY2024 report, because the FY2025 PDF holds the financial statements only. A
figure is in the key only when the report prints it as one number on the scope wanted. Left
out, with the reason in the code:

| Missing from the key | Why |
| --- | --- |
| Air France-KLM group ASK and RPK | printed per business (Réseaux, Transavia), not for the group |
| Norwegian group ASK and RPK | printed per airline (Norwegian, Widerøe), not for the group |
| Hedge ratio: Air France-KLM, IAG | only the policy ("up to 75%"), not the position at year end |
| Hedge ratio: Finnair, easyJet, Wizz Air | printed per half-year (e.g. 79% H1, 51% H2), not for twelve months |
| Undrawn facilities: Norwegian, Wizz Air | no undrawn facility given |

Two lines need arithmetic, both shown in the file: Finnair's fleet adds the two printed fleet
totals (55 on Finnair's own certificate + 24 flown by Norra), as the scope asks for all
aircraft operated for Finnair; easyJet's $1.7 billion facility is converted to pounds at the
ECB rate for September 2025 (decision 0002), as the tool does.

**Limit.** The anchors were written by reading the report, by the same assistant that built
the tool, though a different AI from the one doing the extraction (DeepSeek). A misreading of
scope by the person writing an anchor would be shared with Imane's review only if she does
not spot-check it. Recommendation: Imane spot-checks five lines (about ten minutes).
