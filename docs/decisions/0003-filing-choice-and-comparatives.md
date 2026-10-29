# 0003 · Which filing to use, and filling gap years (M0)

Date: 2026-10-29 · Status: accepted for M0, to confirm in M1

**One filing per issuer and year.** The database often holds the same report twice (a French or
Spanish version next to the English one, or a corrected re-filing). The rule is: English if
available, then fewest validation errors, then the most recently added. Interim reports are
ignored. Every choice and its reason is in `docs/m0/filings.csv`.

**Gap years from comparatives.** When a year's filing is missing but the next year's filing
exists, the year is read from the comparative column of the next year's filing. These figures
are as reported a year later, so they may be restated. The matrix labels them
"comparative in FYxxxx filing". This recovered FY2023 for Air France-KLM and ADP, FY2021 for
easyJet and FY2024 for Wizz Air.
