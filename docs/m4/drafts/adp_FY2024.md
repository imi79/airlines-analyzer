# Groupe ADP, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v5`, fact sheet `69b8381c64c6` ([fact sheet](../factsheets/adp_FY2024.md)). Tokens: 25,151 in, 4,431 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the Paris airport group, grew revenue by 12.1% to EUR 6.2bn in FY2024, but the EBITDA margin narrowed by 2.0 points to 33.7%.
Net leverage was broadly unchanged at 4.13x, with net debt up 8.2% to EUR 8.6bn as capital spending rose.
The point to watch is cash generation: free cash flow fell by 50.3% to EUR 355m and cash liquidity to revenue dropped by 10.8 points to 34.0%.

## Credit metrics

EBITDA rose by 6.0% to EUR 2.1bn, while operating profit fell by 20.0% to EUR 994m on impairment tests on equity-accounted holdings.
Total debt increased by 2.7% to EUR 10.7bn, but gross leverage eased by 0.16x to 5.14x.
Interest coverage improved by 0.23x to 6.97x, while FFO was stable at EUR 1.5bn and FFO to debt broadly unchanged at 14.0%.
Free cash flow fell by 50.3% to EUR 355m, taking FCF to debt down by 3.6 points to 3.3%, as capex intensity rose by 3.1 points to 19.0%.

> Event `event:one_offs`: Impairment tests on equity-accounted holdings and related loans led the group to book an impairment. Quote (page 577): "Les tests menés sur les titres mis en équivalence et les prêts consentis aux sociétés testées ont conclu à la nécessité de constater une dépréciation de 47 millions d’euros."

## Operating performance

The Paris airports handled 103.4m passengers in FY2024.
Group revenue rose by 12.1% to EUR 6.2bn, with the EBITDA margin narrowing by 2.0 points to 33.7%.
In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond the Paris airports, and since the GMR Airports merger it holds a lower economic interest in GMR Airports.

> Event `event:acquisitions_and_disposals`: In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond Paris airports. Quote (page 17): "En octobre 2024, le Groupe ADP a acquis, d’une part, Paris Expérience Group et, d’autre part, P/S, élargissant ainsi l'offre d'Extime au-delà des aéroports parisiens et renforçant ses perspectives de croissance à l'international ;"

> Event `event:acquisitions_and_disposals-3`: Following the merger of GMR Airports Infrastructures Ltd and GMR Airports Ltd, the group holds a lower economic interest in GMR Airports. Quote (page 17): "Depuis le 25 juillet 2024, suite à la fusion de GMR Airports Infrastructures Ltd et de GMR Airports Ltd, le Groupe ADP détient un intérêt économique de 45,7 % dans GMR Airports (contre 49,0 % précédemment)."

## Liquidity and funding

Cash and cash-like investments fell by 14.8% to EUR 2.1bn, and cash liquidity declined by the same 14.8% to EUR 2.1bn.
Cash liquidity to revenue fell by 10.8 points to 34.0%, a thinner buffer against the debt stack.
The group raised bond proceeds in May 2024, which supported the funding of the investment programme alongside operating cash flow.

> Event `event:funding_and_rating`: The report mentions the proceeds of the bond issue among the group's cash flows. Quote (page 530): "Les flux de trésorerie opérationnels s'établissent à 1 524 millions d'euros et les produits de l'émission obligataire du 7 mai 2024 par"

## Peer positioning

Groupe ADP has the weakest EBITDA margin of the airport peers (3rd of 3), against a median of 42.0%.
Gross leverage is the highest of the group (3rd of 3), well above the peer median of 2.08x.
Interest coverage, FFO to debt and FCF to debt all rank last among the peers (2nd of 2, 2nd of 2 and 2nd of 2), below medians of 9.65x, 26.5% and 14.8% respectively.
Capex intensity is above the peer median of 16.1%, consistent with the group's investment cycle.

## Watch items

- Cash generation: FCF to debt fell by 3.6 points to 3.3%, the weakest of the peer group (2nd of 2), as capex intensity rose to 19.0%.
- Liquidity: cash liquidity to revenue fell by 10.8 points to 34.0%, leaving less headroom against net debt of EUR 8.6bn.
- Profitability: the EBITDA margin of 33.7% is the lowest of the airport peers (3rd of 3) and below the median of 42.0%, with operating profit down 20.0% to EUR 994m.
- Regulation: DIAL filed its tariff proposal for the next regulatory period, with final tariffs published and effective in April 2025, which will shape the Delhi revenue base.

> Event `event:regulation_and_tariffs`: DIAL filed its tariff proposal for the upcoming regulatory period, with final tariffs published later and effective in April 2025. Quote (page 86): "DIAL a déposé en mai 2024 sa proposition tarifaire pour la quatrième période de régulation. Les tarifs finaux ont été publiés le 28 mars 2025 et entreront en vigueur le 16 avril 2025, marquant une hausse notable par rapport à la période de régulation précédente et, pour la première fois en Inde, l’introduction d’une structure tarifaire différenciée."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 5 errors | 11,807 / 2,917 |
| 2 | liquidity_funding, peer_positioning, watch_items | passed | 13,344 / 1,514 |

### Errors found, by try

Try 1:

- [rule style] liquidity_funding, sentence 2: total_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: ffo@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 4: capex_intensity@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 3] watch_items, sentence 1: 'worst_in_group' needs the rank id (.peer_rank), not fcf_to_debt@FY2024
- [rule 3] watch_items, sentence 3: 'worst_in_group' needs the rank id (.peer_rank), not ebitda_margin@FY2024

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the Paris airport group, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, but the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Net leverage was broadly unchanged at {{net_leverage@FY2024}}, with net debt up {{net_debt.change@FY2024}} to {{net_debt@FY2024}} as capital spending rose.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} and cash liquidity to revenue dropped by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, while operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} on impairment tests on equity-accounted holdings.
- Total debt increased by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, but gross leverage eased by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, while FFO was stable at {{ffo@FY2024}} and FFO to debt broadly unchanged at {{ffo_to_debt@FY2024}}.
- Free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}}, taking FCF to debt down by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- The Paris airports handled {{passengers@FY2024}} passengers in FY2024.
- Group revenue rose by {{revenue.change@FY2024}} to {{revenue@FY2024}}, with the EBITDA margin narrowing by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond the Paris airports, and since the GMR Airports merger it holds a lower economic interest in GMR Airports.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity declined by the same {{cash_liquidity.change@FY2024}} to {{cash_liquidity@FY2024}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, a thinner buffer against the debt stack.
- The group raised bond proceeds in May 2024, which supported the funding of the investment programme alongside operating cash flow.

`peer_positioning`

- Groupe ADP has the weakest EBITDA margin of the airport peers ({{ebitda_margin.peer_rank@FY2024}}), against a median of {{ebitda_margin.peer_median@FY2024}}.
- Gross leverage is the highest of the group ({{gross_leverage.peer_rank@FY2024}}), well above the peer median of {{gross_leverage.peer_median@FY2024}}.
- Interest coverage, FFO to debt and FCF to debt all rank last among the peers ({{interest_coverage.peer_rank@FY2024}}, {{ffo_to_debt.peer_rank@FY2024}} and {{fcf_to_debt.peer_rank@FY2024}}), below medians of {{interest_coverage.peer_median@FY2024}}, {{ffo_to_debt.peer_median@FY2024}} and {{fcf_to_debt.peer_median@FY2024}} respectively.
- Capex intensity is above the peer median of {{capex_intensity.peer_median@FY2024}}, consistent with the group's investment cycle.

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, the weakest of the peer group ({{fcf_to_debt.peer_rank@FY2024}}), as capex intensity rose to {{capex_intensity@FY2024}}.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, leaving less headroom against net debt of {{net_debt@FY2024}}.
- Profitability: the EBITDA margin of {{ebitda_margin@FY2024}} is the lowest of the airport peers ({{ebitda_margin.peer_rank@FY2024}}) and below the median of {{ebitda_margin.peer_median@FY2024}}, with operating profit down {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Regulation: DIAL filed its tariff proposal for the next regulatory period, with final tariffs published and effective in April 2025, which will shape the Delhi revenue base.
