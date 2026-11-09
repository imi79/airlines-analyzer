# Groupe ADP, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `d950997f7d3f` ([fact sheet](../factsheets/adp_FY2024.md)). Tokens: 41,330 in, 6,866 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the Paris airport group with international operations through TAV Airports and GMR Airports, grew revenue by 12.1% to EUR 6.2bn in FY2024, while the acquisitions of Paris Experience Group and P/S extended the Extime offering beyond Paris.
The EBITDA margin narrowed by 2.0 points to 33.7%, and net leverage was broadly unchanged at 4.13x.
The point to watch is cash generation: free cash flow fell by 50.3% to EUR 355m as capex intensity rose to 19.0%, leaving cash liquidity to revenue at 34.0%.

> Event `event:acquisitions_and_disposals`: In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond Paris airports. Quote (page 17): "En octobre 2024, le Groupe ADP a acquis, d’une part, Paris Expérience Group et, d’autre part, P/S, élargissant ainsi l'offre d'Extime au-delà des aéroports parisiens et renforçant ses perspectives de croissance à l'international ;"

## Credit metrics

Total debt rose by 2.7% to EUR 10.7bn and net debt by 8.2% to EUR 8.6bn, so net leverage was stable at 4.13x while gross leverage eased to 5.14x.
Interest coverage improved to 6.97x, up 0.23x, but FFO to debt was broadly unchanged at 14.0% with FFO flat at EUR 1.5bn.
Free cash flow fell by 50.3% to EUR 355m, taking FCF to debt down by 3.6 points to 3.3%, as capex intensity rose by 3.1 points to 19.0%.

> removed by the verifier (still broke a rule after two retries): "EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, but operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} as depreciation increased." ('increased' needs a 'up' claim on a figure in the same clause)

## Operating performance

The Paris airports handled 103.4m passengers in FY2024.
Group revenue rose by 12.1% to EUR 6.2bn, with the international operations and the Extime retail and hospitality activities contributing alongside the Paris aviation segment.
Impairment tests on equity-accounted holdings and related loans led to a depreciation charge, and profit for the year fell by 34.2% to EUR 516m.

> Event `event:acquisitions_and_disposals`: In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond Paris airports. Quote (page 17): "En octobre 2024, le Groupe ADP a acquis, d’une part, Paris Expérience Group et, d’autre part, P/S, élargissant ainsi l'offre d'Extime au-delà des aéroports parisiens et renforçant ses perspectives de croissance à l'international ;"

> Event `event:one_offs`: Impairment tests on equity-accounted holdings and related loans led the group to book an impairment. Quote (page 577): "Les tests menés sur les titres mis en équivalence et les prêts consentis aux sociétés testées ont conclu à la nécessité de constater une dépréciation de 47 millions d’euros."

> removed by the verifier (still broke a rule after two retries): "The EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, so EBITDA grew more slowly than revenue." ('grew' needs a 'up' claim on a figure in the same clause)

## Liquidity and funding

Cash and cash-like investments fell by 14.8% to EUR 2.1bn, and cash liquidity declined by the same 14.8% to EUR 2.1bn.
Cash liquidity to revenue fell by 10.8 points to 34.0%, a thinner buffer against the debt stock.
The group raised bond funding in May 2024, with the issue proceeds among the cash flows of the year.

> Event `event:funding_and_rating`: The report mentions the proceeds of the bond issue among the group's cash flows. Quote (page 530): "Les flux de trésorerie opérationnels s'établissent à 1 524 millions d'euros et les produits de l'émission obligataire du 7 mai 2024 par"

## Peer positioning

Groupe ADP has the weakest EBITDA margin of the airport peers (3rd of 3), against a median of 42.0%.
Leverage is the weakest in the group, with net leverage ranking 3rd of 3 against a net leverage median of 1.57x and gross leverage ranking 3rd of 3 against a gross leverage median of 2.08x.
Cash liquidity to revenue sits in the middle of the group (2nd of 3), while capex intensity is above the peer median of 16.1%.

## Watch items

- Cash generation: FCF to debt fell by 3.6 points to 3.3%, below the peer median of 14.8%, as capex intensity rose to 19.0%.
- Leverage: net leverage of 4.13x is above the peer median of 1.57x, with net debt up 8.2% to EUR 8.6bn.
- Liquidity: cash liquidity to revenue fell by 10.8 points to 34.0%, with cash and cash-like investments down 14.8% to EUR 2.1bn.
- Coverage: interest coverage of 6.97x remains below the peer median of 9.65x, and FFO to debt of 14.0% is also below the median of 26.5%.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 12 errors | 12,204 / 3,155 |
| 2 | credit_metrics, operating_performance, liquidity_funding, peer_positioning | 7 errors | 14,764 / 1,907 |
| 3 | credit_metrics, operating_performance, liquidity_funding, peer_positioning | 2 errors | 14,362 / 1,804 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule style] operating_performance, sentence 2: revenue.change@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] operating_performance, sentence 3: 'grew' needs a 'up' claim on a figure in the same clause
- [rule style] operating_performance, sentence 3: ebitda@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 2: total_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: net_debt.change@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: net_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 1: ebitda_margin@FY2024 is already given in operating_performance, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: net_leverage@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2024 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

Try 2:

- [rule 4] credit_metrics, sentence 1: 'increased' needs a 'up' claim on a figure in the same clause
- [rule style] operating_performance, sentence 2: revenue.change@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] operating_performance, sentence 3: 'grew' needs a 'up' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 3: net_debt.change@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: net_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue.peer_rank@FY2024 is listed in the form but not used in the text
- [rule 4] peer_positioning, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause

Try 3:

- [rule 4] credit_metrics, sentence 1: 'increased' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 3: 'grew' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the Paris airport group with international operations through TAV Airports and GMR Airports, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, while the acquisitions of Paris Experience Group and P/S extended the Extime offering beyond Paris.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, and net leverage was broadly unchanged at {{net_leverage@FY2024}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose to {{capex_intensity@FY2024}}, leaving cash liquidity to revenue at {{cash_liquidity_to_revenue@FY2024}}.

`credit_metrics`

- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, so net leverage was stable at {{net_leverage@FY2024}} while gross leverage eased to {{gross_leverage@FY2024}}.
- Interest coverage improved to {{interest_coverage@FY2024}}, up {{interest_coverage.change@FY2024}}, but FFO to debt was broadly unchanged at {{ffo_to_debt@FY2024}} with FFO flat at {{ffo@FY2024}}.
- Free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}}, taking FCF to debt down by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- The Paris airports handled {{passengers@FY2024}} passengers in FY2024.
- Group revenue rose by {{revenue.change@FY2024}} to {{revenue@FY2024}}, with the international operations and the Extime retail and hospitality activities contributing alongside the Paris aviation segment.
- Impairment tests on equity-accounted holdings and related loans led to a depreciation charge, and profit for the year fell by {{profit.change@FY2024}} to {{profit@FY2024}}.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity declined by the same {{cash_liquidity.change@FY2024}} to {{cash_liquidity@FY2024}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, a thinner buffer against the debt stock.
- The group raised bond funding in May 2024, with the issue proceeds among the cash flows of the year.

`peer_positioning`

- Groupe ADP has the weakest EBITDA margin of the airport peers ({{ebitda_margin.peer_rank@FY2024}}), against a median of {{ebitda_margin.peer_median@FY2024}}.
- Leverage is the weakest in the group, with net leverage ranking {{net_leverage.peer_rank@FY2024}} against a net leverage median of {{net_leverage.peer_median@FY2024}} and gross leverage ranking {{gross_leverage.peer_rank@FY2024}} against a gross leverage median of {{gross_leverage.peer_median@FY2024}}.
- Cash liquidity to revenue sits in the middle of the group ({{cash_liquidity_to_revenue.peer_rank@FY2024}}), while capex intensity is above the peer median of {{capex_intensity.peer_median@FY2024}}.

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, below the peer median of {{fcf_to_debt.peer_median@FY2024}}, as capex intensity rose to {{capex_intensity@FY2024}}.
- Leverage: net leverage of {{net_leverage@FY2024}} is above the peer median of {{net_leverage.peer_median@FY2024}}, with net debt up {{net_debt.change@FY2024}} to {{net_debt@FY2024}}.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, with cash and cash-like investments down {{cash_like.change@FY2024}} to {{cash_like@FY2024}}.
- Coverage: interest coverage of {{interest_coverage@FY2024}} remains below the peer median of {{interest_coverage.peer_median@FY2024}}, and FFO to debt of {{ffo_to_debt@FY2024}} is also below the median of {{ffo_to_debt.peer_median@FY2024}}.
