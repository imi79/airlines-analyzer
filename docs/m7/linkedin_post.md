# LinkedIn post: draft for Imane to rewrite in her own voice

About 220 words. Add the live link and the repository link where marked; a screenshot of the
tearsheet with a source card open works well as the image.

---

AI can draft a credit note in seconds. The question every credit analyst asks next: can I trust
the numbers?

So I built a tool where the AI never writes a number.

**Airline Credit Tearsheet** turns a European airline's or airport's annual regulatory filing
(ESEF) into a two-page credit tearsheet:

✈️ Code computes every metric (lease-adjusted leverage, interest coverage, FFO to debt,
liquidity, RASK and CASK) from the tagged filing, with one definition for all nine issuers.

🔎 The AI reads what the filing doesn't tag (traffic, fleet, fuel hedging, undrawn credit
lines), and every figure must come with the exact sentence it was read from. Code checks it.

✍️ The AI drafts the commentary with blanks where the figures go; code fills them in, and a
verifier rejects any sentence with a number the AI typed itself or a direction that contradicts
the data.

📎 Click any figure and follow it down to the filing. The Excel backup recalculates every ratio
with live formulas.

What I learned: the hard part isn't getting AI to write. It's deciding where it must not, and
building the controls that prove it didn't.

Live demo (no login): [link]
Code and design notes: [link]

#CreditAnalysis #AviationFinance #AI #LeveragedFinance #FinancialModelling

---

**Notes for you**

- Keep or drop the emojis to match how you usually post.
- If you mention the results, the safe ones are: every figure traced (1,986 of 1,986), the
  verifier catching 47 of 47 planted errors, and the Excel recalculating exactly. The
  commentary score (3.78 of 5) is better kept for the interview, with its context.
