# M3 plan: reading what the filings don't tag, and proving every figure

Status: **approved by Imane** (2026-11-01). Her answers to the questions at the end: 1. DeepSeek, key
set as a secret of the cloud environment; 2. she supplied the two 2025 PDFs; 3. the answer key is
built by code (decision 0012); 4. the work is on the branch `m3-extraction-grounding`.

## What M3 is for

The tagged statements give us the balance sheet, P&L and cash flow. They do not give us the
operating figures a credit analyst needs for an airline or airport: passengers, ASK, RPK, fleet,
fuel hedging, undrawn credit lines, and aeronautical revenue. These sit in the text of the annual
report. Today 16 catalog metrics show as "missing, needs M3" because of this.

M3 adds a reader for that text. The AI model does the reading; code does the checking. Think of
the AI as a junior analyst who must staple a photocopy of the page to every figure they hand in,
and the code as the reviewer who checks the photocopy against the original report before the
figure is allowed into the model.

## What the AI will extract

| Figure | Who | Feeds |
| --- | --- | --- |
| Passengers carried / handled | all 9 | passengers, traffic growth, revenue per passenger |
| ASK, RPK | 6 airlines | load factor, RASK, CASK, CASK ex-fuel, passenger yield |
| Passenger revenue (if not tagged) | 6 airlines | passenger yield |
| Fleet in operation at year end, average age | 6 airlines | fleet |
| Fuel hedge ratio for the next 12 months | 6 airlines | fuel hedge ratio |
| Undrawn committed credit facilities | all 9 | liquidity, liquidity to revenue (completes the "partial" figure) |
| Aeronautical and non-aeronautical revenue | 3 airports | aero revenue per passenger, non-aero share |
| Company-reported load factor | 6 airlines | cross-check only (see check 5) |

For every year we hold, FY2021 to FY2025 (Wizz Air to FY2026).

## How it works, step by step

1. **Get the report text.** Each electronic filing already contains the full annual report as a
   web page; we downloaded it in M1. Code turns it into plain text, removing pictures and layout.
2. **Find the right pages (section locator).** Code searches the text for the terms that signal
   each figure ("available seat kilometres", "load factor", "undrawn", "revolving credit
   facility", "hedged"…) and keeps only the passages around them. The AI sees a few pages, not
   the 300-page report: cheaper, faster, and less room to wander.
3. **AI reading through a form (tool use).** The model must answer by filling a fixed form, one
   line per figure: which figure, value, unit, which year, the exact sentence it read it from,
   and where. It can also answer "not found". It cannot write free text.
4. **Code checks every line (grounding checks).** A figure is marked **verified** only if all of
   these pass:
   1. **The quote is real.** The sentence appears word for word in the report (spaces ignored,
      because some reports split words, e.g. "tr affic capac ity").
   2. **The number is in the quote.** The value appears in that sentence once units are put on
      the same basis ("134,451 million" = "134.5 billion"; French "8,7 %" = 8.7%).
   3. **The year is right.** The figure belongs to the fiscal year being read, not the
      comparative. Many reports print both, for example "93.4 million passengers (2024: 89.7
      million)"; code rejects a value that sits in the bracketed prior-year part.
   4. **It agrees with next year's report.** Where the following year's report also shows this
      year as its comparative, the two must match (a restatement is shown, not hidden). This is
      the same control as the prior-year column check in M1.
   5. **It adds up.** RPK ÷ ASK must equal the load factor the company prints (within the
      rounding of the printed figure); values must sit in a sensible range (load factor 50-100%, hedge ratio 0-100%, fleet
      not halving year on year without a stated reason).
5. **Anything that fails stays unverified.** It is stored with the reason it failed, kept off
   the tearsheet, and marked with * in every report, like the hand-entered figures in M2. You
   approve or correct it in a review file (`config/extraction_reviews.yaml`), and every
   correction is kept as an override with your name, the date and the reason. (The click-to-
   approve screen comes with the web app in M5.)
6. **Ratios update.** The 16 waiting metrics are computed from the extracted figures, each with
   its working (for RASK: "revenue ÷ ASK = cents per seat-kilometre", with both figures shown), and the peer tables gain the
   operating metrics.

## The AI layer, any provider (decision 0005)

- One small module, `src/tearsheet/llm/`, with two connectors: Anthropic, and "OpenAI-compatible"
  (DeepSeek, OpenRouter, Mistral, Azure, local models…). `config/models.yaml` names the provider,
  the model for each job and the name of the environment variable holding the key. Switching
  provider is a one-line config change.
- **No new library needed.** Both connectors talk to the provider over plain web requests with
  `httpx`, which we already use for the filings database. This settles the open point in
  decision 0005. Form checking uses Pydantic, which is already in the agreed stack.
- **Prompts are versioned files** (`extract/prompts/extract_v1.md`). Every extracted figure
  records the provider, model, prompt version and a fingerprint of what was sent. Identical
  inputs are served from a local cache, so a rerun costs nothing and changes nothing.
- **Cost is logged** for every run (tokens in and out); I report it after the first full run.

## How we know it works (the M3 checklist)

**A labelled answer key.** About 30 figures across the six airlines, latest year: passengers,
ASK, RPK, fleet, fuel hedge ratio, undrawn facilities. Each one is read by a person from the
report, independently of the AI. The tool's output is scored against it:

- [ ] **No wrong value marked verified** on the answer key. A wrong figure that the checks catch
      (unverified) is acceptable; a wrong figure that slips through is not.
- [ ] **At least 80% of the answer key verified automatically.**
- [ ] **Every unverified value visibly flagged** in the reports and the review file.

We also run the answer key for each provider you want to use, and record the scores.

**Tests, no internet.** Recorded AI answers stand in for the real model in the unit tests,
including deliberately wrong ones: a made-up quote, a number not in its quote, last year's
figure passed off as this year's, a load factor that doesn't add up. Each must come out
unverified. One unit test per new metric, as in M2.

## Order of work

1. Report text and section locator, tested on all nine issuers (no AI yet; shows which passages
   would be sent).
2. AI layer with both connectors, the form, config and cache; tests on recorded answers.
3. Grounding checks 1-5 with the adversarial tests.
4. Extraction run on all issuers and years; extracted facts stored with quote and status.
5. The 16 metrics, peer tables, review file and overrides.
6. Answer key scoring, `docs/m3/` results, decision notes, walkthrough, checklist.

## Known difficulties

- **Air France-KLM's report is in French** (sièges-kilomètres offerts, passagers-kilomètres
  transportés, coefficient d'occupation, flotte). The locator gets French terms and the checks
  read French number formats. Quotes stay in French, as printed.
- **Air France-KLM and ADP FY2025 have no electronic filing** (decision 0007), so there is no
  report text for that year in the database. See question 2.
- **Some reports are scrambled** by the converter that produced them (split words, pictures
  embedded as text in Norwegian's). Handled in step 1; any figure that can't be grounded stays
  unverified rather than guessed.
- **Scope of "passengers" and "fleet" differs** between companies (group vs main brand; owned,
  leased and wet-leased aircraft). The scope chosen per issuer is recorded with its quote, as we
  did for net debt in M2.

## Questions for Imane

1. **Which AI provider and key?** The tool needs an API key for real runs (none is set in this
   workspace). Anthropic, DeepSeek, or an OpenRouter-type gateway: which one do you have or want?
   The key is added as a secret of the cloud environment, never written in the repo.
2. **Air France-KLM and ADP FY2025 text.** Either you supply the 2025 universal registration
   documents (PDF) and I read them the same way, or FY2025 operating figures for those two stay
   "missing" until their electronic filings appear. Recommendation: supply the PDFs.
3. **Who builds the answer key?** The spec says you label it. Recommendation: I prepare a sheet
   listing the ~30 figures with a link to each report and where to look, values left blank; you
   type each value (about an hour). Alternative, as in gate 1: a code-only reader (no AI) builds
   it and you spot-check. Weaker, because code and AI may then share a blind spot.
4. **Branch name.** Your rule bans "claude" in branch names, but this cloud session is tied to the
   branch `claude/ecstatic-carson-asjf17`. May I do M3 on `m3-extraction` instead?
