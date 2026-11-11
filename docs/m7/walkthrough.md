# M7 walkthrough: the portfolio piece, live

**What M7 built.** Everything a recruiter or an interviewer needs to see the tool working and
understand it in a few minutes: the public link, the README, three sample PDFs, a way to watch
the verifier work, the demo script, and the words to talk about it.

## What's where

| You want to | Go to |
| --- | --- |
| Show the tool | https://airlines-analyzer.streamlit.app (no login, no key) |
| Send the code | https://github.com/imi79/airlines-analyzer (the README explains the design and the results) |
| Send a sample | `samples/pdf/`: Air France-KLM, easyJet, Aena FY2025, with your analyst views |
| Prepare a demo | `docs/m7/demo_script.md`: three minutes, five beats, what to click and say |
| Prepare an interview | `docs/m7/pipeline_explained.md`: the seven stages and ten questions with key points |
| Post about it | `docs/m7/linkedin_post.md` (draft to put in your own words) |
| Update your CV | `docs/m7/cv_line.md` (three versions) |

## New in the app: watch the verifier work

- **Data and audit → How the AI's draft was checked.** Each try the AI made, the sentences the
  verifier rejected and why. easyJet FY2025 is the best example: ten sentences rejected at the
  first try.
- **Method → Try the verifier.** Pick a faulty sentence (a number typed by the AI, the wrong
  direction, a figure that doesn't exist or awaits review) or write your own, and see which
  rule catches it. The examples are built from the tearsheet on screen.

## Behind the scenes

- **Tested before deploying.** A copy of Streamlit's hosting setup ran the full browser tour
  before you deployed; it caught one real bug (the PDF's font on a clean machine), fixed and now
  tested on all 18 PDFs.
- **A Dockerfile**, so the app can run on any host later.
- **Checks on GitHub** on every change: the tests, the code style, and a scan for leaked keys
  across the whole history. Before going public, the whole history was scanned: no leak.
- **The history was tidied** on your go-ahead: every commit carries your GitHub noreply
  address; the company PDFs stayed.
- **One correction to the record**: gate 2 had 11 drafts in a row, not 17 (still a pass).

## Results

| M7 checklist | Result | |
| --- | --- | --- |
| Public link works in a fresh browser with no key (gate 3) | Every page, a figure followed to its source, a two-page PDF download and the verifier demo, from a fresh browser, not signed in (`docs/m7/gate3.md`) | ✓ |
| Imane can explain every stage of the pipeline without notes | Rehearsal of nine interview questions, every stage explained correctly; ticked by you | ✓ |

**From the rehearsal, to practise:** give each answer the same four parts: the principle, an
example, a number, a limit. Stages 1 and 4 are the ones where the best examples are easiest to
forget: the hand-entered Air France-KLM FY2025 figures (36 of 36 controls), and the 98.0 million
passengers quoted from page 30 of the 2024 report.

**v1 is complete:** gates 1, 2 and 3 passed; the two targets missed (extraction 80%, commentary
4 of 5) are stated in the README and closed by you on the safety result.

## Small things left for you

- Delete the three `claude/...` branches on GitHub (Branches page): they are public now and hold
  nothing that isn't in `main`.
- Add your full name to `LICENSE` if you want more than "Imane".
- Open the link once in a private window on your phone.
- If the app hasn't had visitors for 12 hours, open it a few minutes before an interview.

## Next

Candidates for an M8, from comparing the tearsheet with a sell-side credit note: cash flow after
lease payments and net capex; the debt maturity wall with liquidity against maturities; rating
trigger headroom and a ratings box (entered by hand, with source and date). Each fits the
current controls (tagged figures, quoted and checked figures, or hand entries with a source).
