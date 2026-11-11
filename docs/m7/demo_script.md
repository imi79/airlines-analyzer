# Three-minute demo script

For an interview or a call with screen sharing. Five beats, timed; what to click, and what to
say in your own words (the lines below are a guide, not a script to read).

**Before the call (5 minutes before).** Open the public link once: a free app sleeps after 12
hours without visitors and takes about half a minute to wake ("Yes, get this app back up!").
Leave it on **Air France-KLM FY2025**. Have one PDF downloaded, in case the connection drops.

## 0:00 · The problem (30 seconds)

No clicks. "Credit analysts spend hours rebuilding the same tables from annual reports, and
AI tools that draft credit notes have one big weakness: you can't trust their numbers. I built
a tool where the AI never writes a number. Code computes every figure from the regulatory
filing, the AI only writes the words around them, and a checker reads every sentence."

## 0:30 · The tearsheet (45 seconds)

Tearsheet page, Air France-KLM FY2025.

- Point at the header: "FY2025, network airline, compared with IAG and Finnair."
- The snapshot: "Three sentences, drafted by the AI; every number in bold was put there by code."
- The KPI cards and the table: "Net leverage down from 1.88x to 1.71x; four years of history."
- The charts: "Leverage and liquidity. Liquidity shows 'pending' here, and that's deliberate: one
  figure, the undrawn credit lines, is waiting for my review, so it isn't shown as a number."

## 1:15 · One figure, audited (30 seconds)

Click **Source** under Net leverage.

- "1.71x: computed, net debt over EBITDA." Click **Net debt** → **Total debt** → a borrowings
  line. "Down to the filing: the IFRS tag, the value exactly as filed, the filing's fingerprint,
  and a button that opens the official filing viewer."
- If time: on a passenger figure, the quote from the annual report with its page.

## 1:45 · The verifier rejecting a bad draft (45 seconds)

In the sidebar, switch to **easyJet FY2025**; **Data and audit** page, scroll to **How the
AI's draft was checked**, **Try 1** (open by default). (Air France-KLM's draft passed at the
first try, so it has nothing to show here.)

- "This is the AI's first attempt for easyJet. The verifier rejected ten sentences: here it
  claimed the EBITDA margin got 'worse' when code computes no meaningful change; here it listed
  figures it didn't use. The sections went back to the AI with the reasons; after two more tries
  only checked sentences are on the page."
- Then **Method** page, **Try the verifier**: pick "The wrong direction", click **Check**:
  "The sentence says the figure moved the opposite way to what code computed: rule 4 stops it."
  Pick "A number typed by the AI": "and a number typed by the AI is never allowed."

## 2:30 · The deliverables (20 seconds)

Back to the Tearsheet page (easyJet, or Air France-KLM again), bottom: **Prepare the PDF and
the Excel backup**.

- "Two A4 pages for the reader; my analyst view goes in this box, never drafted by the AI."
- "And the Excel backup: every ratio is a live formula on the filing figures, so a reviewer can
  redo every sum. All 18 workbooks recalculate exactly to the app."

## 2:50 · Close (10 seconds)

"Nine European airlines and airports, free regulatory data, every figure traced. The design
choices and the test results, misses included, are in the repository."

## If something goes wrong

- **App asleep**: say "free hosting, it's waking up", and talk through beat 1 meanwhile.
- **No connection**: open the PDF you downloaded and the screenshots in the README.
- **A question you can't answer on the spot**: "It's in the decision notes, I'll send you the
  link": every choice has a short note in `docs/decisions/`.

## Likely follow-up questions

- *Why not let the AI write the numbers and check them afterwards?* Checking a number someone
  else wrote means finding its source; here every number comes from a source by construction.
- *What does the AI actually add?* Reading what filings don't tag (traffic, fleet, hedging,
  undrawn lines) with a quote, and drafting the words; both checked by code.
- *How good is the commentary?* 3.78 out of 5 against the annual reports: safe and accurate, a
  bit short on insight, which is where the analyst comes in.
- *Which AI?* Any: the provider is a configuration line; the drafts here were made with DeepSeek.
