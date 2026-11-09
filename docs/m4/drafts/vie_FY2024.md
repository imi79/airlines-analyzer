# Flughafen Wien, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v6`, fact sheet `890f33799e29` ([fact sheet](../factsheets/vie_FY2024.md)). Tokens: 26,343 in, 3,591 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport group, grew revenue by 13.0% to EUR 1.1bn in FY2024, and the full repayment of interest-bearing financial liabilities leaves it with net cash of EUR 512m.
Net leverage fell by 0.24x to -1.16x, a net cash position, while the EBITDA margin was broadly unchanged at 42.0%.
The point to watch is cash generation: free cash flow declined by 4.6% to EUR 274m as capex intensity rose by 5.6 points to 16.1%.

> Event `event:funding_and_rating`: The report states that the complete elimination of interest-bearing financial liabilities has greatly reduced the potential effects of interest rate changes on the company. Quote (part 24): "Der vollständige Abbau zinstragender Finanzverbindlichkeiten hat die potenziellen Auswirkungen einer Zinsänderung auf die FWAG massiv reduziert."

## Credit metrics

EBITDA increased by 12.3% to EUR 442m on revenue up 13.0%, and operating profit rose by 16.9% to EUR 306m.
Total debt was stable at EUR 55.6m, so gross leverage held at 0.13x and net cash rose by 41.4% to EUR 512m.
FFO increased by 3.4% to EUR 358m, but free cash flow fell by 4.6% to EUR 274m as capex intensity rose by 5.6 points to 16.1%.

## Operating performance

Passengers rose by 7.3% to 31.7m, but traffic growth of 7.3% was below the peer median of 8.3% and down by 17.4 points on the prior year.
Aeronautical revenue per passenger increased by 7.6% to EUR 15.57, with airport charges temporarily adjusted by average inflation under the amended airport charges act.

> Event `event:regulation_and_tariffs`: Airport charges at Vienna Airport are temporarily adjusted by average inflation under the amended airport charges act, with this rule ending at the end of 2026. Quote (part 9): "Die Flughafenentgelte am Flughafen Wien werden gemäß § 17a FEG vorübergehend um die durchschnittliche Inflation (gerechnet von 1.8. bis 31.7.) angepasst. Diese Regelung endet mit 31. Dezember 2026, wodurch die Flughäfen im Entgeltantrag 2026 zur bestehenden Formel zurückkehren und diese mit 1. Jänner 2027 wieder anwenden."

## Liquidity and funding

Cash and cash-like investments rose by 36.0% to EUR 567m, taking cash liquidity to revenue up by 9.1 points to 53.9%.
Cash liquidity of EUR 567m covers the group's debt many times over, and the group repaid its interest-bearing financial liabilities in full during the year.
A financing commitment was given for the City Air Terminal joint venture's new train sets, part of which was drawn as a loan in the year.

> Event `event:funding_and_rating`: The report states that the complete elimination of interest-bearing financial liabilities has greatly reduced the potential effects of interest rate changes on the company. Quote (part 24): "Der vollständige Abbau zinstragender Finanzverbindlichkeiten hat die potenziellen Auswirkungen einer Zinsänderung auf die FWAG massiv reduziert."

> Event `event:funding_and_rating-2`: A financing commitment was given for the joint venture City Air Terminal for the procurement of new train sets, part of which was drawn as a loan in the reporting year. Quote (part 77): "Es gibt für das Gemeinschaftsunternehmen City Air Terminal Betriebsgesellschaft m.b.H. eine Finanzierungszusage für die Beschaffung neuer Zuggarnituren in Höhe von rund € 30,0 Mio., im laufenden Geschäftsjahr wurden davon T€ 1.002,0 als Darlehen in Anspruch genommen."

## Peer positioning

Flughafen Wien has the lowest net leverage of the airport group (1st of 3), against a peer median of 1.57x, and the lowest gross leverage (1st of 3).
Cash liquidity to revenue is the strongest of the group (1st of 3), above the peer median of 34.0%.
The EBITDA margin sits in the middle of the group, and capex intensity is in line with the peer median of 16.1%.

## Watch items

- Cash generation: free cash flow fell by 4.6% to EUR 274m as capex intensity rose by 5.6 points to 16.1%, in line with the peer median of 16.1%.
- Traffic: traffic growth of 7.3% is below the peer median of 8.3% and the weakest of the group (2nd of 2), which limits the operating leverage behind the earnings base.
- Regulation: airport charges are temporarily adjusted by average inflation, a rule that ends at the end of 2026, so revenue per passenger depends on the tariff formula that follows.
- Third runway: complaints were filed against the extension of the construction completion deadline and the single-party procedure, without suspensive effect.

> Event `event:regulation_and_tariffs`: Airport charges at Vienna Airport are temporarily adjusted by average inflation under the amended airport charges act, with this rule ending at the end of 2026. Quote (part 9): "Die Flughafenentgelte am Flughafen Wien werden gemäß § 17a FEG vorübergehend um die durchschnittliche Inflation (gerechnet von 1.8. bis 31.7.) angepasst. Diese Regelung endet mit 31. Dezember 2026, wodurch die Flughäfen im Entgeltantrag 2026 zur bestehenden Formel zurückkehren und diese mit 1. Jänner 2027 wieder anwenden."

> Event `event:regulation_and_tariffs-2`: Several complaints without suspensive effect were filed against the extension of the construction completion deadline and the single-party procedure for the third runway. Quote (part 24): "Gegen die Verlängerung der Bauvollendungsfrist und die Abwicklung im Einparteienverfahren wurden mehrere Beschwerden ohne aufschiebende Wirkung eingebracht."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 12,646 / 2,433 |
| 2 | liquidity_funding, peer_positioning, watch_items | passed | 13,697 / 1,158 |

### Errors found, by try

Try 1:

- [rule style] liquidity_funding, sentence 2: total_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] peer_positioning, sentence 2: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 5] watch_items, sentence 1: capex_intensity.peer_median@FY2024 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport group, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, and the full repayment of interest-bearing financial liabilities leaves it with net cash of {{net_cash@FY2024}}.
- Net leverage fell by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}, a net cash position, while the EBITDA margin was broadly unchanged at {{ebitda_margin@FY2024}}.
- The point to watch is cash generation: free cash flow declined by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}}, and operating profit rose by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Total debt was stable at {{total_debt@FY2024}}, so gross leverage held at {{gross_leverage@FY2024}} and net cash rose by {{net_cash.change@FY2024}} to {{net_cash@FY2024}}.
- FFO increased by {{ffo.change@FY2024}} to {{ffo@FY2024}}, but free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, but traffic growth of {{traffic_growth@FY2024}} was below the peer median of {{traffic_growth.peer_median@FY2024}} and down by {{traffic_growth.change@FY2024}} on the prior year.
- Aeronautical revenue per passenger increased by {{aero_revenue_per_passenger.change@FY2024}} to {{aero_revenue_per_passenger@FY2024}}, with airport charges temporarily adjusted by average inflation under the amended airport charges act.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue up by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Cash liquidity of {{cash_liquidity@FY2024}} covers the group's debt many times over, and the group repaid its interest-bearing financial liabilities in full during the year.
- A financing commitment was given for the City Air Terminal joint venture's new train sets, part of which was drawn as a loan in the year.

`peer_positioning`

- Flughafen Wien has the lowest net leverage of the airport group ({{net_leverage.peer_rank@FY2024}}), against a peer median of {{net_leverage.peer_median@FY2024}}, and the lowest gross leverage ({{gross_leverage.peer_rank@FY2024}}).
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2024}}), above the peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}}.
- The EBITDA margin sits in the middle of the group, and capex intensity is in line with the peer median of {{capex_intensity.peer_median@FY2024}}.

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, in line with the peer median of {{capex_intensity.peer_median@FY2024}}.
- Traffic: traffic growth of {{traffic_growth@FY2024}} is below the peer median of {{traffic_growth.peer_median@FY2024}} and the weakest of the group ({{traffic_growth.peer_rank@FY2024}}), which limits the operating leverage behind the earnings base.
- Regulation: airport charges are temporarily adjusted by average inflation, a rule that ends at the end of 2026, so revenue per passenger depends on the tariff formula that follows.
- Third runway: complaints were filed against the extension of the construction completion deadline and the single-party procedure, without suspensive effect.
