# M5 timing: a pre-built tearsheet opens in under ten seconds

Measured on 2026-11-09 in a real browser (Chromium, driven by Playwright), demo mode, the app
started fresh (`TEARSHEET_DEMO_ONLY=1 uv run tearsheet app`, nothing in memory yet). Each
tearsheet was opened in a **new browser tab with an empty session**, from its own link
(`?company=wizz&year=2026`). The clock runs from asking for the page to the company name, the
snapshot commentary and the KPI cards all being on screen.

| Tearsheet | Seconds |
| --- | ---: |
| Air France-KLM FY2025 (first, nothing in memory) | 2.0 |
| Air France-KLM FY2024 | 1.8 |
| International Airlines Group FY2025 | 1.8 |
| International Airlines Group FY2024 | 1.8 |
| Finnair FY2025 | 1.7 |
| Finnair FY2024 | 1.7 |
| easyJet FY2025 (Oct 2024 to Sep 2025) | 1.7 |
| easyJet FY2024 (Oct 2023 to Sep 2024) | 1.7 |
| Groupe ADP FY2025 | 1.7 |
| Groupe ADP FY2024 | 1.8 |
| Aena FY2025 | 1.8 |
| Aena FY2024 | 1.6 |
| Flughafen Wien FY2025 | 1.6 |
| Flughafen Wien FY2024 | 1.7 |
| Norwegian Air Shuttle FY2025 | 1.7 |
| Norwegian Air Shuttle FY2024 | 1.7 |
| Wizz Air Holdings FY2026 (Apr 2025 to Mar 2026) | 1.6 |
| Wizz Air Holdings FY2025 (Apr 2024 to Mar 2025) | 1.7 |

**Result: 18 of 18 under ten seconds; the slowest 2.0 seconds**, the first one, which also
loads the figure file into memory. The app server itself was ready 0.7 seconds after start.

Not measured here: the free hosting (Streamlit Community Cloud) wakes a sleeping app in
roughly half a minute after a period without visitors. That is the host, not the tearsheet,
and it is checked with the public link in M7.

For comparison, live mode builds a tearsheet from the database instead of the pre-built file:
the redraft button replayed Flughafen Wien's recorded drafts in 15 seconds (no AI tokens, the
figures had not changed).
