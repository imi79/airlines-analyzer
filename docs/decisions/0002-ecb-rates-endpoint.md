# 0002 · ECB exchange-rate source (M0)

Date: 2026-10-29 · Status: accepted

Peer size charts convert to EUR with ECB reference rates from the free ECB data API:

    https://data-api.ecb.europa.eu/service/data/EXR/M.<CCY>.EUR.SP00.<A|E>?format=csvdata

- `A` = monthly average (for income statement and cash flow items)
- `E` = end of month (for balance sheet items)
- The rate is units of the foreign currency per 1 EUR, so divide by it to convert to EUR.
- Confirmed in M0 for GBP, NOK, USD and DKK, monthly from 2020-01 (81 months, to 2026-09).

**Fiscal-year average.** For an issuer whose year doesn't end in December (easyJet to
September, Wizz Air to March), the average rate is the mean of the twelve monthly averages in
its fiscal year, not the calendar-year rate. This approximates the daily average closely
enough for a size chart; ratios never need conversion.
