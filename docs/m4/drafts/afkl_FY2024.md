# Air France-KLM, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `32d65e3643a3` ([fact sheet](../factsheets/afkl_FY2024.md)). Tokens: 43,813 in, 8,158 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Air France-KLM, the network airline group spanning Air France, KLM and Transavia, grew revenue by 4.8% to EUR 31.5bn in FY2024, while EBITDA was broadly unchanged at EUR 4.1bn.
Net leverage rose by 0.59x to 1.88x as net debt increased by 43.5% to EUR 7.7bn, and the EBITDA margin narrowed by 0.8 points to 13.1%.
The point to watch is cash generation: free cash flow turned negative at EUR -232m and cash liquidity to revenue fell by 5.5 points to 22.0%, the weakest of the network peers (3rd of 3).

## Credit metrics

EBITDA was broadly unchanged, 1.5% to EUR 4.1bn, on revenue up 4.8% at EUR 31.5bn, while operating profit fell by 12.6% to EUR 1.5bn after a payment to Virgin in a contract renegotiation and a restructuring provision for the Orly domestic offer.
Total debt rose by 7.4% to EUR 14.6bn and net debt by 43.5% to EUR 7.7bn, lifting gross leverage by 0.29x to 3.56x and net leverage by 0.59x to 1.88x.
FFO rose by 2.1% to EUR 3.4bn, but FFO to debt fell by 1.2 points to 23.4% and interest coverage eased by 0.45x to 6.51x.
Free cash flow fell to EUR -232m from EUR 55.0m in FY2023, taking FCF to debt down by 2.0 points to -1.6%, with capex intensity broadly unchanged at 11.9%.

> Event `event:costs`: Operating result for the year included a payment to Virgin as part of the renegotiation of a contract. Quote (page 369): "un versement de (115) millions d’euros à Virgin dans le cadre de la renégociation d’un contrat ;"

> Event `event:capacity_and_network`: A net provision was recorded for the restructuring of the domestic offer from Orly and of call centres. Quote (page 369): "une provision nette de (49) millions liée à la restructuration de l’offre domestique au départ d’Orly et des centres d’appel."

## Operating performance

Passengers rose by 4.7% to 98.0m, with the fleet up by 4.3% to 564 aircraft and an average age broadly unchanged at 12.1 years.
Fleet renewal was delayed by supply chain constraints and engine problems on part of the new-generation fleet, which the group could not operate at maximum capacity.
The group completed the acquisition of a minority stake in SAS AB and began a deepened commercial cooperation with the airline.

> Event `event:fleet_and_engines`: Fleet renewal was delayed by supply chain constraints and engine problems on part of the new-generation fleet, preventing the group from operating those aircraft at maximum capacity. Quote (page 5): "En 2024, l’intensité GES s’est améliorée (- 1 %) par rapport à 2023 dans un contexte de retards dans le renouvellement de la flotte, en raison de contraintes dans la chaîne d’approvisionnement, de problèmes de moteurs sur une partie de la flotte d’avions de nouvelle génération ne permettant pas au Groupe de les exploiter à leur capacité maximale"

> Event `event:acquisitions_and_disposals`: The group completed the acquisition of a minority stake in SAS AB and began a deepened commercial cooperation with the airline. Quote (page 371): "Après l’obtention d’autorisations réglementaires en Europe et aux États-Unis, le groupe Air France-KLM a donc finalisé le 28 août 2024 l’acquisition d’une participation minoritaire de 19,90 % dans le capital de SAS AB."

## Liquidity and funding

Cash and cash-like investments fell by 16.0% to EUR 6.9bn, so cash liquidity declined by 16.0% to EUR 6.9bn.
Cash liquidity to revenue fell by 5.5 points to 22.0%, a thinner buffer against the group's debt service.
Customer prepayments rose: contract liabilities increased by 6.2% to EUR 4.1bn, and advance ticket cover climbed by 12.4 points to 59.1%.
The group launched a cash tender offer on existing bond tranches and announced its intention to issue new bonds to refinance part of its existing debt.

> Event `event:funding_and_rating`: The company launched a cash tender offer on existing bond tranches and announced its intention to issue new bonds to refinance part of its existing debt. Quote (page 12): "Air France-KLM annonce le lancement d’une offre de rachat sur deux souches obligataires existantes et son intention de procéder à une nouvelle émission obligataire"

## Peer positioning

Air France-KLM is weakest on profitability and cash generation: the EBITDA margin of 13.1% is below the peer median of 14.6% and ranks 3rd of 3, and FCF to debt ranks 3rd of 3 against a peer median of 20.3%.
Leverage and coverage sit in the middle of the group, with net leverage ranking 2nd of 3, gross leverage 2nd of 3, interest coverage 2nd of 3 and FFO to debt 2nd of 3.
Capital spending is the other outlier: capex intensity of 11.9% is above the peer median of 8.8%.

> verifier: [rule style] peer_positioning, sentence 3: capex_intensity@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

## Watch items

- Cash generation: free cash flow turned negative at EUR -232m and FCF to debt fell by 2.0 points to -1.6%, the weakest of the network peers (3rd of 3).
- Leverage: net debt rose by 43.5% to EUR 7.7bn, taking net leverage up by 0.59x to 1.88x.
- Liquidity: cash liquidity to revenue fell by 5.5 points to 22.0%, below the peer median of 29.0% and the lowest of the group (3rd of 3).
- Margins: the EBITDA margin narrowed by 0.8 points to 13.1%, below the peer median of 14.6%, with fleet renewal delayed by engine problems on part of the new-generation fleet.

> Event `event:fleet_and_engines`: Fleet renewal was delayed by supply chain constraints and engine problems on part of the new-generation fleet, preventing the group from operating those aircraft at maximum capacity. Quote (page 5): "En 2024, l’intensité GES s’est améliorée (- 1 %) par rapport à 2023 dans un contexte de retards dans le renouvellement de la flotte, en raison de contraintes dans la chaîne d’approvisionnement, de problèmes de moteurs sur une partie de la flotte d’avions de nouvelle génération ne permettant pas au Groupe de les exploiter à leur capacité maximale"

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 12 errors | 12,969 / 3,409 |
| 2 | snapshot, credit_metrics, liquidity_funding, peer_positioning, watch_items | 2 errors | 16,474 / 3,258 |
| 3 | credit_metrics, peer_positioning | passed | 14,370 / 1,491 |

### Errors found, by try

Try 1:

- [rule 5] snapshot, sentence 3: cash_liquidity_to_revenue.peer_rank@FY2024 is listed in the form but not used in the text
- [rule 4] credit_metrics, sentence 1: 'down' needs a 'down' claim on a figure in the same clause
- [rule 1] liquidity_funding, sentence 4: word that states a number: 'two'
- [rule 3] peer_positioning, sentence 1: 'better' claimed on advance_ticket_cover@FY2024, but it is worse
- [rule style] peer_positioning, sentence 1: advance_ticket_cover@FY2024 is already given in liquidity_funding, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: fcf_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: net_leverage.peer_rank@FY2024 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: gross_leverage.peer_rank@FY2024 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: interest_coverage.peer_rank@FY2024 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: ffo_to_debt.peer_rank@FY2024 is listed in the form but not used in the text
- [rule 5] watch_items, sentence 1: fcf_to_debt.peer_rank@FY2024 is listed in the form but not used in the text
- [rule 5] watch_items, sentence 3: cash_liquidity_to_revenue.peer_rank@FY2024 is listed in the form but not used in the text

Try 2:

- [rule 4] credit_metrics, sentence 1: 'down' needs a 'down' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 1: advance_ticket_cover@FY2024 is already given in liquidity_funding, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

Try 3:

- [rule style] peer_positioning, sentence 3: capex_intensity@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- Air France-KLM, the network airline group spanning Air France, KLM and Transavia, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, while EBITDA was broadly unchanged at {{ebitda@FY2024}}.
- Net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} as net debt increased by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, and the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- The point to watch is cash generation: free cash flow turned negative at {{fcf@FY2024}} and cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, the weakest of the network peers ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).

`credit_metrics`

- EBITDA was broadly unchanged, {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, on revenue up {{revenue.change@FY2024}} at {{revenue@FY2024}}, while operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} after a payment to Virgin in a contract renegotiation and a restructuring provision for the Orly domestic offer.
- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, lifting gross leverage by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}} and net leverage by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}.
- FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, but FFO to debt fell by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}} and interest coverage eased by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}.
- Free cash flow fell to {{fcf@FY2024}} from {{fcf@FY2023}} in FY2023, taking FCF to debt down by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, with capex intensity broadly unchanged at {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, with the fleet up by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft and an average age broadly unchanged at {{fleet_age@FY2024}}.
- Fleet renewal was delayed by supply chain constraints and engine problems on part of the new-generation fleet, which the group could not operate at maximum capacity.
- The group completed the acquisition of a minority stake in SAS AB and began a deepened commercial cooperation with the airline.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, so cash liquidity declined by {{cash_liquidity.change@FY2024}} to {{cash_liquidity@FY2024}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, a thinner buffer against the group's debt service.
- Customer prepayments rose: contract liabilities increased by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, and advance ticket cover climbed by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}.
- The group launched a cash tender offer on existing bond tranches and announced its intention to issue new bonds to refinance part of its existing debt.

`peer_positioning`

- Air France-KLM is weakest on profitability and cash generation: the EBITDA margin of {{ebitda_margin@FY2024}} is below the peer median of {{ebitda_margin.peer_median@FY2024}} and ranks {{ebitda_margin.peer_rank@FY2024}}, and FCF to debt ranks {{fcf_to_debt.peer_rank@FY2024}} against a peer median of {{fcf_to_debt.peer_median@FY2024}}.
- Leverage and coverage sit in the middle of the group, with net leverage ranking {{net_leverage.peer_rank@FY2024}}, gross leverage {{gross_leverage.peer_rank@FY2024}}, interest coverage {{interest_coverage.peer_rank@FY2024}} and FFO to debt {{ffo_to_debt.peer_rank@FY2024}}.
- Capital spending is the other outlier: capex intensity of {{capex_intensity@FY2024}} is above the peer median of {{capex_intensity.peer_median@FY2024}}.

`watch_items`

- Cash generation: free cash flow turned negative at {{fcf@FY2024}} and FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, the weakest of the network peers ({{fcf_to_debt.peer_rank@FY2024}}).
- Leverage: net debt rose by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, taking net leverage up by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}} and the lowest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).
- Margins: the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, below the peer median of {{ebitda_margin.peer_median@FY2024}}, with fleet renewal delayed by engine problems on part of the new-generation fleet.
