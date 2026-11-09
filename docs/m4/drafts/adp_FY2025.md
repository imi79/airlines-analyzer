# Groupe ADP, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v5`, fact sheet `7ae28fa0e90c` ([fact sheet](../factsheets/adp_FY2025.md)). Tokens: 40,224 in, 6,109 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the Paris airport group that also consolidates TAV Airports, grew revenue by 8.9% to EUR 6.7bn in FY2025, with the renewed Ankara Esenboga concession entering service during the year.
The EBITDA margin widened by 1.0 point to 34.7% and net leverage fell by 0.45x to 3.68x.
The point to watch is liquidity: cash liquidity to revenue fell by 3.9 points to 30.1%, while gross leverage sits above the airport peer median of 2.00x and FFO to debt remains below the peer median of 27.7%.

> Event `event:capacity_and_network`: TAV Airports' renewed concession for Ankara Esenboga airport took effect, covering investments to raise capacity in exchange for operating rights for a long period. Quote (page 14): "Dans le cadre d’un appel d’offres publics en 2022, TAV Airports, filiale du Groupe ADP (Aéroports de Paris) détenue à 46 %, a remporté l’appel d’offres pour le renouvellement de la concession de l’aéroport de la capitale turque Ankara à partir du 24 mai 2025."

## Credit metrics

EBITDA increased by 12.1% to EUR 2.3bn, and operating profit rose by 16.7% to EUR 1.2bn, although depreciation charges rose on an unfavourable base effect.
Total debt was stable at EUR 10.6bn and net debt was stable at EUR 8.6bn, so gross leverage fell by 0.59x to 4.55x as EBITDA grew by 12.1%.
Interest coverage improved by 0.92x to 7.89x, and FFO to debt rose by 1.7 points to 15.7%.
Free cash flow increased by 18.3% to EUR 420m, lifting FCF to debt to 4.0%, while capex intensity eased by 0.8 points to 18.2%.

> Event `event:costs`: Depreciation and impairment charges rose, reflecting an unfavourable base effect from an impairment reversal recorded the previous year after the extension of the Amman airport concession. Quote (page 19): "Les dotations aux amortissements et dépréciations d’actifs s’établissent à -1 003 millions d’euros, en hausse de 27 % (211 millions d’euros) en raison d’un effet de base défavorable lié à la reprise de dépréciation de 152 millions d’euros enregistrée en 2024, suite à l’extension de la durée de concession de l’aéroport d’Amman."

## Operating performance

Passengers rose by 3.5% to 107.0m, with traffic growth of 3.5%.
Revenue grew by 8.9% to EUR 6.7bn, faster than passenger volumes, reflecting the international airport portfolio as well as Paris traffic.
The tariff period ran in a legal framework outside an economic regulation contract, with the annual tariff-setting procedure still requiring user consultation and regulatory approval.

> Event `event:regulation_and_tariffs`: The tariff period took place in a legal framework without an economic regulation contract, with the annual tariff-setting procedure still requiring user consultation and regulatory approval. Quote (page 21): "Même si la régulation économique d’Aéroports de Paris repose de manière préférentielle sur des contrats de régulation économique (CRE), la période tarifaire 2025 se déroule dans un cadre juridique hors CRE."

## Liquidity and funding

Cash and cash-like investments fell by 3.8% to EUR 2.0bn, and cash liquidity fell by 3.8% to EUR 2.0bn.
Cash liquidity to revenue fell by 3.9 points to 30.1%, a thinner buffer against the group's debt stock.
The TAV group's guarantee of part of the Antalya concession bank loan no longer exists at year-end after the refinancing of the previous bank loan.

> Event `event:funding_and_rating`: The TAV group had guaranteed part of the bank loan financing the initial Antalya concession payment, and this guarantee no longer exists at year-end because of the refinancing of the previous bank loan. Quote (page 79): "Le groupe TAV s’est porté garant de 50 % de l’emprunt bancaire utilisé pour le financement du paiement initial pour un montant de 1 097 millions d’euros. Ce paiement initial correspond à la quote-part du groupe TAV dans les avances de 25 % payées pour le renouvellement de la concession Antalya, dont le montant net des redevances à horizon 2052 s’élève à 5,4 milliards d’euros. Cette garantie n’existe plus à fin 2025 en raison du refinancement de l'emprunt bancaire précédent."

## Peer positioning

Groupe ADP has the weakest EBITDA margin of the airport peers (3rd of 3), at 34.7% against a median of 36.5%.
Gross leverage is above the peer median of 2.00x and ranks 3rd of 3 in the group.
Interest coverage and FFO to debt both sit below the peer medians of 11.31x and 27.7%, ranking 2nd of 2 and 2nd of 2 respectively.
Capex intensity puts the group in the middle of the airport peers.

## Watch items

- Liquidity: cash liquidity to revenue fell by 3.9 points to 30.1%, leaving less headroom against a debt stock that was stable at EUR 10.6bn.
- Contingencies: a dispute before the Turkish courts over the withholding tax rate on dividends from a Turkish subsidiary remains a contingent liability.

> Event `event:other`: The main litigation and arbitration constituting a contingent liability is a dispute before Turkish courts over the withholding tax rate applied to dividends paid by a Turkish subsidiary. Quote (page 80): "Le principal litige et arbitrage constituant un passif éventuel est un contentieux pendant devant les tribunaux turcs concernant le taux de retenue à la source appliqué aux dividendes versés par une filiale turque."

> removed by the verifier (still broke a rule after two retries): "Cash flow against debt: FCF to debt of {{fcf_to_debt@FY2025}} is below the peer median of {{fcf_to_debt.peer_median@FY2025}}, so any reduction in debt depends on further earnings." ('reduction' needs a 'down' claim on a figure in the same clause)

> removed by the verifier (still broke a rule after two retries): "Profit: profit for the year fell by {{profit.change@FY2025}} to {{profit@FY2025}} as depreciation charges increased." ('increased' needs a 'up' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 11 errors | 12,236 / 2,672 |
| 2 | snapshot, credit_metrics, liquidity_funding, peer_positioning, watch_items | 3 errors | 14,973 / 2,338 |
| 3 | credit_metrics, watch_items | 2 errors | 13,015 / 1,099 |

### Errors found, by try

Try 1:

- [rule 5] snapshot, sentence 3: gross_leverage.peer_median@FY2025 is listed in the form but not used in the text
- [rule 5] snapshot, sentence 3: ffo_to_debt.peer_median@FY2025 is listed in the form but not used in the text
- [rule 3] snapshot, sentence 3: 'below_peers' claimed on gross_leverage.peer_median@FY2025, but it is above
- [rule 4] credit_metrics, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 2: total_debt@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: interest_coverage@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 4: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 2: 'reduction' needs a 'down' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'rose' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] credit_metrics, sentence 2: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 4] watch_items, sentence 2: 'reduction' needs a 'down' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'rose' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] watch_items, sentence 2: 'reduction' needs a 'down' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the Paris airport group that also consolidates TAV Airports, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, with the renewed Ankara Esenboga concession entering service during the year.
- The EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}} and net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, while gross leverage sits above the airport peer median of {{gross_leverage.peer_median@FY2025}} and FFO to debt remains below the peer median of {{ffo_to_debt.peer_median@FY2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit rose by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, although depreciation charges rose on an unfavourable base effect.
- Total debt was stable at {{total_debt@FY2025}} and net debt was stable at {{net_debt@FY2025}}, so gross leverage fell by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} as EBITDA grew by {{ebitda.change@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, and FFO to debt rose by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}.
- Free cash flow increased by {{fcf.change@FY2025}} to {{fcf@FY2025}}, lifting FCF to debt to {{fcf_to_debt@FY2025}}, while capex intensity eased by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, with traffic growth of {{traffic_growth@FY2025}}.
- Revenue grew by {{revenue.change@FY2025}} to {{revenue@FY2025}}, faster than passenger volumes, reflecting the international airport portfolio as well as Paris traffic.
- The tariff period ran in a legal framework outside an economic regulation contract, with the annual tariff-setting procedure still requiring user consultation and regulatory approval.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity fell by {{cash_liquidity.change@FY2025}} to {{cash_liquidity@FY2025}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, a thinner buffer against the group's debt stock.
- The TAV group's guarantee of part of the Antalya concession bank loan no longer exists at year-end after the refinancing of the previous bank loan.

`peer_positioning`

- Groupe ADP has the weakest EBITDA margin of the airport peers ({{ebitda_margin.peer_rank@FY2025}}), at {{ebitda_margin@FY2025}} against a median of {{ebitda_margin.peer_median@FY2025}}.
- Gross leverage is above the peer median of {{gross_leverage.peer_median@FY2025}} and ranks {{gross_leverage.peer_rank@FY2025}} in the group.
- Interest coverage and FFO to debt both sit below the peer medians of {{interest_coverage.peer_median@FY2025}} and {{ffo_to_debt.peer_median@FY2025}}, ranking {{interest_coverage.peer_rank@FY2025}} and {{ffo_to_debt.peer_rank@FY2025}} respectively.
- Capex intensity puts the group in the middle of the airport peers.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, leaving less headroom against a debt stock that was stable at {{total_debt@FY2025}}.
- Contingencies: a dispute before the Turkish courts over the withholding tax rate on dividends from a Turkish subsidiary remains a contingent liability.
