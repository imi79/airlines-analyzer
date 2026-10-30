# 0009 · Gate 1 checked with a second-source model built by the AI (M2)

Date: 2026-10-30 · Status: accepted (Imane: "you can build the model yourself")

**Context.** The spec makes Imane's hand-built model the reference for gate 1 (leverage within
0.05x, margins and ratios within 0.1 point; Air France-KLM and Groupe ADP, two years). Imane
asked the AI to build that model.

**What was done to keep it as independent as possible** (`spikes/m2/hand_model.py`):
- **Different data path.** Inputs are read mechanically from the text of the published 2025
  statements (PDF), with the page and the line as printed recorded for each
  (`docs/m2/hand_model_inputs.csv`). They don't come from the XBRL filings the tool uses, nor
  from the hand entries in `config/manual_figures.yaml`.
- **Different calculator.** Every metric is a visible Excel formula on those inputs
  (`docs/m2/hand_model.xlsx`), recalculated by LibreOffice, not by the tool's code.
- **The check can fail.** Fed figures 0.09x or 0.2 point off, it reports ✗.

**Result.** 62 of 62 comparisons are within tolerance: 16 metrics for Air France-KLM and 15 for
ADP, in FY2024 and FY2025 (`docs/m2/gate1.md`). Every difference is exactly zero, as expected
when the same published figures go through the same definitions.

**Limit.** Data and arithmetic are checked independently; the definitions are not. Both models
apply the definitions on the reconciliation's "Definitions" sheet, so a definition Imane would
disagree with is not caught. Imane can still fill `docs/m2/reconciliation.xlsx` with her own
model at any time.

**Side results.**
- The machine reading of the four PDFs confirms the 8 figures entered by hand in M2 (Air
  France-KLM interest expense 2025 and note 32 items for 2023-2025; ADP associates 2025 and
  restricted bank balances for 2023-2025).
- Building the model surfaced three reading traps, now handled and tested: a digit swallowed
  by a pattern, a table-of-contents line taken for a heading, and a footnote marker "(4)" read
  as a negative number.
