# Groupe ADP, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v7`, fact sheet `71b0da6dc4ff` ([fact sheet](../factsheets/adp_FY2025.md)). Tokens: 44,782 in, 7,727 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the Paris airport group that also consolidates TAV Airports, grew revenue by 8.9% to EUR 6.7bn in FY2025, with the Ankara Esenboga concession renewal entering service during the year.
The EBITDA margin widened by 1.0 point to 34.7%, and net leverage fell by 0.45x to 3.68x.
The point to watch is cash liquidity, which fell by 3.9 points to 30.1% of revenue, the weakest of the airport peers (3rd of 3).

> Event `event:capacity_and_network`: TAV Airports' renewed concession for Ankara Esenboga airport took effect, covering investments to raise capacity in exchange for operating rights for a long period. Quote (page 14): "Dans le cadre d’un appel d’offres publics en 2022, TAV Airports, filiale du Groupe ADP (Aéroports de Paris) détenue à 46 %, a remporté l’appel d’offres pour le renouvellement de la concession de l’aéroport de la capitale turque Ankara à partir du 24 mai 2025."

## Credit metrics

EBITDA increased by 12.1% to EUR 2.3bn, and operating profit rose by 16.7% to EUR 1.2bn despite depreciation, amortisation and impairment rising by 26.8%.
Interest coverage improved by 0.92x to 7.89x even as finance costs rose by 11.4% to EUR 663m.
FFO rose by 11.2% to EUR 1.7bn, lifting FFO to debt by 1.7 points to 15.7%, while free cash flow increased by 18.3% to EUR 420m as capex intensity eased by 0.8 points to 18.2%.

> verifier: [rule style] credit_metrics, sentence 3: ffo_to_debt@FY2025 is already given in peer_positioning, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

> verifier: [rule style] credit_metrics, sentence 3: fcf@FY2025 is already given in liquidity_funding, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)

> removed by the verifier (still broke a rule after two retries): "Total debt was broadly unchanged at {{total_debt@FY2025}} and net debt at {{net_debt@FY2025}}, so the earnings growth took gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}." ('growth' needs a 'up' claim on a figure in the same clause)

## Operating performance

Passengers reached 107.0m, up 3.5%, with traffic growth of 3.5%.
Revenue rose by 8.9% to EUR 6.7bn, faster than passenger volumes, helped by the international portfolio.
Depreciation, amortisation and impairment charges rose, reflecting an unfavourable base effect after the prior year's impairment reversal on the Amman concession.
The Ankara Esenboga concession renewal entered service in May 2025, adding operating rights in exchange for capacity investment.

> Event `event:costs`: Depreciation and impairment charges rose, reflecting an unfavourable base effect from an impairment reversal recorded the previous year after the extension of the Amman airport concession. Quote (page 19): "Les dotations aux amortissements et dépréciations d’actifs s’établissent à -1 003 millions d’euros, en hausse de 27 % (211 millions d’euros) en raison d’un effet de base défavorable lié à la reprise de dépréciation de 152 millions d’euros enregistrée en 2024, suite à l’extension de la durée de concession de l’aéroport d’Amman."

> Event `event:capacity_and_network`: TAV Airports' renewed concession for Ankara Esenboga airport took effect, covering investments to raise capacity in exchange for operating rights for a long period. Quote (page 14): "Dans le cadre d’un appel d’offres publics en 2022, TAV Airports, filiale du Groupe ADP (Aéroports de Paris) détenue à 46 %, a remporté l’appel d’offres pour le renouvellement de la concession de l’aéroport de la capitale turque Ankara à partir du 24 mai 2025."

## Liquidity and funding

Cash and cash-like investments fell by 3.8% to EUR 2.0bn, taking cash liquidity to revenue down by 3.9 points to 30.1%.
Cash from operations rose by 7.5% to EUR 1.6bn, covering capex of EUR 1.2bn and leaving free cash flow of EUR 420m.
The TAV group's guarantee of part of the Antalya concession bank loan no longer exists at year-end after the refinancing of that loan.

> Event `event:funding_and_rating`: The TAV group had guaranteed part of the bank loan financing the initial Antalya concession payment, and this guarantee no longer exists at year-end because of the refinancing of the previous bank loan. Quote (page 79): "Le groupe TAV s’est porté garant de 50 % de l’emprunt bancaire utilisé pour le financement du paiement initial pour un montant de 1 097 millions d’euros. Ce paiement initial correspond à la quote-part du groupe TAV dans les avances de 25 % payées pour le renouvellement de la concession Antalya, dont le montant net des redevances à horizon 2052 s’élève à 5,4 milliards d’euros. Cette garantie n’existe plus à fin 2025 en raison du refinancement de l'emprunt bancaire précédent."

> verifier: [rule style] liquidity_funding, sentence 2: fcf@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

## Peer positioning

Groupe ADP has the weakest EBITDA margin of the airport group (3rd of 3), at 34.7% against a peer median of 36.5%.
Leverage is the weakest in the group, with net leverage of 3.68x against a peer median of 1.46x (3rd of 3).
Capex intensity sits in the middle of the group, while FFO to debt of 15.7% and FCF to debt of 4.0% are below the peer medians of 27.7% and 13.4%.

> verifier: [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

## Watch items

- Liquidity: cash liquidity to revenue of 30.1% is below the peer median of 32.6% and the weakest of the group (3rd of 3), with cash and cash-like investments down by 3.8% to EUR 2.0bn.
- Leverage: net leverage of 3.68x remains above the peer median of 1.46x, leaving limited headroom if EBITDA growth stalls.
- Cash generation: FFO to debt of 15.7% and FCF to debt of 4.0% sit below the peer medians, with capex of EUR 1.2bn absorbing most of the cash from operations.
- Regulation: the tariff period ran outside an economic regulation contract, so the annual tariff-setting procedure depends on user consultation and regulatory approval.

> Event `event:regulation_and_tariffs`: The tariff period took place in a legal framework without an economic regulation contract, with the annual tariff-setting procedure still requiring user consultation and regulatory approval. Quote (page 21): "Même si la régulation économique d’Aéroports de Paris repose de manière préférentielle sur des contrats de régulation économique (CRE), la période tarifaire 2025 se déroule dans un cadre juridique hors CRE."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 13,145 / 2,959 |
| 2 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 16,384 / 2,916 |
| 3 | credit_metrics, operating_performance, liquidity_funding, peer_positioning | 3 errors | 15,253 / 1,852 |

### Errors found, by try

Try 1:

- [rule 5] snapshot, sentence 3: cash_liquidity_to_revenue.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 4] credit_metrics, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause
- [rule style] operating_performance, sentence 3: dda.change@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 2: fcf@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] watch_items, sentence 1: cash_liquidity_to_revenue.peer_rank@FY2025 is listed in the form but not used in the text

Try 2:

- [rule 4] credit_metrics, sentence 2: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] operating_performance, sentence 3: dda.change@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 2: fcf@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

Try 3:

- [rule 4] credit_metrics, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 2: fcf@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the Paris airport group that also consolidates TAV Airports, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, with the Ankara Esenboga concession renewal entering service during the year.
- The EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, and net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- The point to watch is cash liquidity, which fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} of revenue, the weakest of the airport peers ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit rose by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} despite depreciation, amortisation and impairment rising by {{dda.change@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}} even as finance costs rose by {{finance_costs.change@FY2025}} to {{finance_costs@FY2025}}.
- FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, lifting FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, while free cash flow increased by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity eased by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers reached {{passengers@FY2025}}, up {{passengers.change@FY2025}}, with traffic growth of {{traffic_growth@FY2025}}.
- Revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}}, faster than passenger volumes, helped by the international portfolio.
- Depreciation, amortisation and impairment charges rose, reflecting an unfavourable base effect after the prior year's impairment reversal on the Amman concession.
- The Ankara Esenboga concession renewal entered service in May 2025, adding operating rights in exchange for capacity investment.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Cash from operations rose by {{cfo.change@FY2025}} to {{cfo@FY2025}}, covering capex of {{capex@FY2025}} and leaving free cash flow of {{fcf@FY2025}}.
- The TAV group's guarantee of part of the Antalya concession bank loan no longer exists at year-end after the refinancing of that loan.

`peer_positioning`

- Groupe ADP has the weakest EBITDA margin of the airport group ({{ebitda_margin.peer_rank@FY2025}}), at {{ebitda_margin@FY2025}} against a peer median of {{ebitda_margin.peer_median@FY2025}}.
- Leverage is the weakest in the group, with net leverage of {{net_leverage@FY2025}} against a peer median of {{net_leverage.peer_median@FY2025}} ({{net_leverage.peer_rank@FY2025}}).
- Capex intensity sits in the middle of the group, while FFO to debt of {{ffo_to_debt@FY2025}} and FCF to debt of {{fcf_to_debt@FY2025}} are below the peer medians of {{ffo_to_debt.peer_median@FY2025}} and {{fcf_to_debt.peer_median@FY2025}}.

`watch_items`

- Liquidity: cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}} and the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), with cash and cash-like investments down by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}.
- Leverage: net leverage of {{net_leverage@FY2025}} remains above the peer median of {{net_leverage.peer_median@FY2025}}, leaving limited headroom if EBITDA growth stalls.
- Cash generation: FFO to debt of {{ffo_to_debt@FY2025}} and FCF to debt of {{fcf_to_debt@FY2025}} sit below the peer medians, with capex of {{capex@FY2025}} absorbing most of the cash from operations.
- Regulation: the tariff period ran outside an economic regulation contract, so the annual tariff-setting procedure depends on user consultation and regulatory approval.
