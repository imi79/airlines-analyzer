# Groupe ADP, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `64c44771e649` ([fact sheet](../factsheets/adp_FY2025.md)). Tokens: 43,387 in, 8,036 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the Paris airport group that also consolidates TAV Airports, grew revenue by 8.9% to EUR 6.7bn in FY2025, with the renewed Ankara Esenboga concession entering service during the year.
EBITDA rose by 12.1% to EUR 2.3bn, which brought net leverage down by 0.45x to 3.68x, while the EBITDA margin widened by 1.0 point to 34.7%.
The point to watch is cash liquidity, which fell by 3.9 points to 30.1% of revenue and sits below the peer median.

> Event `event:capacity_and_network`: TAV Airports' renewed concession for Ankara Esenboga airport took effect, covering investments to raise capacity in exchange for operating rights for a long period. Quote (page 14): "Dans le cadre d’un appel d’offres publics en 2022, TAV Airports, filiale du Groupe ADP (Aéroports de Paris) détenue à 46 %, a remporté l’appel d’offres pour le renouvellement de la concession de l’aéroport de la capitale turque Ankara à partir du 24 mai 2025."

## Credit metrics

EBITDA increased by 12.1% to EUR 2.3bn, and operating profit rose by 16.7% to EUR 1.2bn despite higher depreciation charges.
Interest coverage improved by 0.92x to 7.89x, and FFO rose by 11.2% to EUR 1.7bn, lifting FFO to debt by 1.7 points to 15.7%.
Free cash flow rose by 18.3% to EUR 420m, taking FCF to debt up by 0.7 points to 4.0%, with capex intensity easing by 0.8 points to 18.2%.

> Event `event:costs`: Depreciation and impairment charges rose, reflecting an unfavourable base effect from an impairment reversal recorded the previous year after the extension of the Amman airport concession. Quote (page 19): "Les dotations aux amortissements et dépréciations d’actifs s’établissent à -1 003 millions d’euros, en hausse de 27 % (211 millions d’euros) en raison d’un effet de base défavorable lié à la reprise de dépréciation de 152 millions d’euros enregistrée en 2024, suite à l’extension de la durée de concession de l’aéroport d’Amman."

> verifier: [rule style] credit_metrics, sentence 3: capex_intensity@FY2025 is already given in peer_positioning, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

> removed by the verifier (still broke a rule after two retries): "Total debt was stable at {{total_debt@FY2025}} and net debt stable at {{net_debt@FY2025}}, so the EBITDA increase took net leverage down by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} and gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}." ('increase' needs a 'up' claim on a figure in the same clause)

## Operating performance

Passengers rose by 3.5% to 107.0m, with traffic growth of 3.5%.
Revenue grew by 8.9% to EUR 6.7bn, faster than passenger volumes, reflecting the international airport portfolio as well as Paris traffic.
The tariff period ran in a legal framework without an economic regulation contract, so tariffs remain subject to user consultation and regulatory approval.

> Event `event:regulation_and_tariffs`: The tariff period took place in a legal framework without an economic regulation contract, with the annual tariff-setting procedure still requiring user consultation and regulatory approval. Quote (page 21): "Même si la régulation économique d’Aéroports de Paris repose de manière préférentielle sur des contrats de régulation économique (CRE), la période tarifaire 2025 se déroule dans un cadre juridique hors CRE."

## Liquidity and funding

Cash and cash-like investments fell by 3.8% to EUR 2.0bn, and cash liquidity fell by 3.8% to EUR 2.0bn.
Cash liquidity to revenue fell by 3.9 points to 30.1%, a thinner buffer against the debt stock.
The TAV group's guarantee of part of the Antalya concession bank loan no longer exists at year-end after the refinancing of the previous loan.

> Event `event:funding_and_rating`: The TAV group had guaranteed part of the bank loan financing the initial Antalya concession payment, and this guarantee no longer exists at year-end because of the refinancing of the previous bank loan. Quote (page 79): "Le groupe TAV s’est porté garant de 50 % de l’emprunt bancaire utilisé pour le financement du paiement initial pour un montant de 1 097 millions d’euros. Ce paiement initial correspond à la quote-part du groupe TAV dans les avances de 25 % payées pour le renouvellement de la concession Antalya, dont le montant net des redevances à horizon 2052 s’élève à 5,4 milliards d’euros. Cette garantie n’existe plus à fin 2025 en raison du refinancement de l'emprunt bancaire précédent."

## Peer positioning

Groupe ADP has the weakest EBITDA margin of the airport group (3rd of 3), at 34.7% against a peer median of 36.5%.
Leverage is the weakest in the group, with net leverage ranking 3rd of 3 against a peer median of 1.46x and gross leverage ranking 3rd of 3 against a peer median of 2.00x.
Cash generation also trails the group, with FFO to debt and FCF to debt both below the peer medians of 27.7% and 13.4%, while capex intensity of 18.2% sits in the middle of the group.

> verifier: [rule style] peer_positioning, sentence 3: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

## Watch items

- Liquidity: cash liquidity to revenue fell by 3.9 points to 30.1%, the weakest of the group (3rd of 3), with cash and cash-like investments down by 3.8% to EUR 2.0bn.
- Cash generation: FFO to debt of 15.7% and FCF to debt of 4.0% are both below the peer medians of 27.7% and 13.4%, leaving limited headroom for the investment programme.
- Contingencies: a dispute before Turkish courts over the withholding tax rate on dividends from a Turkish subsidiary remains a contingent liability.

> Event `event:other`: The main litigation and arbitration constituting a contingent liability is a dispute before Turkish courts over the withholding tax rate applied to dividends paid by a Turkish subsidiary. Quote (page 80): "Le principal litige et arbitrage constituant un passif éventuel est un contentieux pendant devant les tribunaux turcs concernant le taux de retenue à la source appliqué aux dividendes versés par une filiale turque."

> removed by the verifier (still broke a rule after two retries): "Leverage: net leverage of {{net_leverage@FY2025}} remains well above the peer median of {{net_leverage.peer_median@FY2025}}, even though it came down over the year." ('down' needs a 'down' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 17 errors | 12,606 / 3,003 |
| 2 | snapshot, credit_metrics, liquidity_funding, peer_positioning, watch_items | 7 errors | 15,891 / 2,628 |
| 3 | snapshot, credit_metrics, peer_positioning, watch_items | 3 errors | 14,890 / 2,405 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] credit_metrics, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 2: total_debt@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 3] peer_positioning, sentence 1: 'worse' claimed on ebitda_margin@FY2025, but it is better
- [rule 3] peer_positioning, sentence 2: 'worse' claimed on net_leverage@FY2025, but it is better
- [rule 3] peer_positioning, sentence 2: 'worse' claimed on gross_leverage@FY2025, but it is better
- [rule style] peer_positioning, sentence 2: net_leverage@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: capex_intensity@FY2025 is listed in the form but not used in the text
- [rule 3] peer_positioning, sentence 3: 'worse' claimed on ffo_to_debt@FY2025, but it is better
- [rule 3] peer_positioning, sentence 3: 'worse' claimed on fcf_to_debt@FY2025, but it is better
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: fcf_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 3] watch_items, sentence 2: 'worse' claimed on net_leverage@FY2025, but it is better
- [rule 4] watch_items, sentence 2: 'reduction' needs a 'down' claim on a figure in the same clause
- [rule 3] watch_items, sentence 3: 'worse' claimed on ffo_to_debt@FY2025, but it is better
- [rule 3] watch_items, sentence 3: 'worse' claimed on fcf_to_debt@FY2025, but it is better

Try 2:

- [rule 4] snapshot, sentence 2: 'Higher' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 4] credit_metrics, sentence 2: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 5] peer_positioning, sentence 3: capex_intensity@FY2025 is listed in the form but not used in the text
- [rule 3] watch_items, sentence 2: 'worse' claimed on net_leverage@FY2025, but it is better
- [rule 4] watch_items, sentence 2: 'fall' needs a 'down' claim on a figure in the same clause
- [rule 3] watch_items, sentence 3: 'worse' claimed on ffo_to_debt@FY2025, but it is better
- [rule 3] watch_items, sentence 3: 'worse' claimed on fcf_to_debt@FY2025, but it is better

Try 3:

- [rule 4] credit_metrics, sentence 2: 'increase' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 2: 'down' needs a 'down' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the Paris airport group that also consolidates TAV Airports, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, with the renewed Ankara Esenboga concession entering service during the year.
- EBITDA rose by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, which brought net leverage down by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, while the EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- The point to watch is cash liquidity, which fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} of revenue and sits below the peer median.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit rose by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} despite higher depreciation charges.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, and FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, lifting FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}.
- Free cash flow rose by {{fcf.change@FY2025}} to {{fcf@FY2025}}, taking FCF to debt up by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, with capex intensity easing by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, with traffic growth of {{traffic_growth@FY2025}}.
- Revenue grew by {{revenue.change@FY2025}} to {{revenue@FY2025}}, faster than passenger volumes, reflecting the international airport portfolio as well as Paris traffic.
- The tariff period ran in a legal framework without an economic regulation contract, so tariffs remain subject to user consultation and regulatory approval.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity fell by {{cash_liquidity.change@FY2025}} to {{cash_liquidity@FY2025}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, a thinner buffer against the debt stock.
- The TAV group's guarantee of part of the Antalya concession bank loan no longer exists at year-end after the refinancing of the previous loan.

`peer_positioning`

- Groupe ADP has the weakest EBITDA margin of the airport group ({{ebitda_margin.peer_rank@FY2025}}), at {{ebitda_margin@FY2025}} against a peer median of {{ebitda_margin.peer_median@FY2025}}.
- Leverage is the weakest in the group, with net leverage ranking {{net_leverage.peer_rank@FY2025}} against a peer median of {{net_leverage.peer_median@FY2025}} and gross leverage ranking {{gross_leverage.peer_rank@FY2025}} against a peer median of {{gross_leverage.peer_median@FY2025}}.
- Cash generation also trails the group, with FFO to debt and FCF to debt both below the peer medians of {{ffo_to_debt.peer_median@FY2025}} and {{fcf_to_debt.peer_median@FY2025}}, while capex intensity of {{capex_intensity@FY2025}} sits in the middle of the group.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), with cash and cash-like investments down by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}.
- Cash generation: FFO to debt of {{ffo_to_debt@FY2025}} and FCF to debt of {{fcf_to_debt@FY2025}} are both below the peer medians of {{ffo_to_debt.peer_median@FY2025}} and {{fcf_to_debt.peer_median@FY2025}}, leaving limited headroom for the investment programme.
- Contingencies: a dispute before Turkish courts over the withholding tax rate on dividends from a Turkish subsidiary remains a contingent liability.
