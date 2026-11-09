# Air France-KLM, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v6`, fact sheet `d79139566d3d` ([fact sheet](../factsheets/afkl_FY2024.md)). Tokens: 27,504 in, 4,764 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Air France-KLM, the Franco-Dutch network airline, grew revenue by 4.8% to EUR 31.5bn in FY2024 while EBITDA was broadly unchanged at EUR 4.1bn.
Net leverage rose by 0.59x to 1.88x as net debt increased by 43.5% to EUR 7.7bn.
The point to watch is cash generation: free cash flow turned negative at EUR -232m and cash liquidity to revenue fell by 5.5 points to 22.0%.

## Credit metrics

EBITDA was stable at EUR 4.1bn on revenue up 4.8% to EUR 31.5bn, but operating profit fell by 12.6% to EUR 1.5bn.
Total debt increased by 7.4% to EUR 14.6bn, lifting gross leverage by 0.29x to 3.56x.
FFO rose by 2.1% to EUR 3.4bn, but FFO to debt fell by 1.2 points to 23.4% as total debt increased by 7.4%.
Free cash flow fell to EUR -232m from EUR 55.0m in FY2023, taking FCF to debt down by 2.0 points to -1.6%.
Interest coverage eased by 0.45x to 6.51x, with capex intensity broadly unchanged at 11.9%.

## Operating performance

Passengers rose by 4.7% to 98.0m, while the fleet grew by 4.3% to 564 aircraft.
The average fleet age was stable at 12.1 years, with fleet renewal delayed by supply chain constraints and engine problems on part of the new-generation fleet.
The operating result included a payment to Virgin in a contract renegotiation and a net provision for the restructuring of the domestic offer from Orly and of call centres.
The group completed the acquisition of a minority stake in SAS AB and began a deepened commercial cooperation with the airline.

> Event `event:fleet_and_engines`: Fleet renewal was delayed by supply chain constraints and engine problems on part of the new-generation fleet, preventing the group from operating those aircraft at maximum capacity. Quote (page 5): "En 2024, l’intensité GES s’est améliorée (- 1 %) par rapport à 2023 dans un contexte de retards dans le renouvellement de la flotte, en raison de contraintes dans la chaîne d’approvisionnement, de problèmes de moteurs sur une partie de la flotte d’avions de nouvelle génération ne permettant pas au Groupe de les exploiter à leur capacité maximale"

> Event `event:costs`: Operating result for the year included a payment to Virgin as part of the renegotiation of a contract. Quote (page 369): "un versement de (115) millions d’euros à Virgin dans le cadre de la renégociation d’un contrat ;"

> Event `event:capacity_and_network`: A net provision was recorded for the restructuring of the domestic offer from Orly and of call centres. Quote (page 369): "une provision nette de (49) millions liée à la restructuration de l’offre domestique au départ d’Orly et des centres d’appel."

> Event `event:acquisitions_and_disposals`: The group completed the acquisition of a minority stake in SAS AB and began a deepened commercial cooperation with the airline. Quote (page 371): "Après l’obtention d’autorisations réglementaires en Europe et aux États-Unis, le groupe Air France-KLM a donc finalisé le 28 août 2024 l’acquisition d’une participation minoritaire de 19,90 % dans le capital de SAS AB."

## Liquidity and funding

Cash and cash-like investments fell by 16.0% to EUR 6.9bn, taking cash liquidity to revenue down by 5.5 points to 22.0%.
Customer prepayments rose: contract liabilities increased by 6.2% to EUR 4.1bn, and advance ticket cover rose by 12.4 points to 59.1%.
On the funding side, the group launched a cash tender offer on existing bond tranches and announced its intention to issue new bonds to refinance part of its existing debt.

> Event `event:funding_and_rating`: The company launched a cash tender offer on existing bond tranches and announced its intention to issue new bonds to refinance part of its existing debt. Quote (page 12): "Air France-KLM annonce le lancement d’une offre de rachat sur deux souches obligataires existantes et son intention de procéder à une nouvelle émission obligataire"

## Peer positioning

Air France-KLM has the weakest EBITDA margin of the network airlines (3rd of 3), at 13.1% against a peer median of 14.6%.
FCF to debt is also the weakest of the group (3rd of 3), and cash liquidity to revenue ranks 3rd of 3.
Leverage and coverage sit in the middle of the group, with net leverage, gross leverage, interest coverage and FFO to debt all in line with the peer medians of 1.88x, 3.56x, 6.51x and 23.4% respectively, while advance ticket cover is the lowest of the group (1st of 3).

## Watch items

- Cash generation: free cash flow was negative at EUR -232m and FCF to debt fell by 2.0 points to -1.6%, below the peer median of 20.3%.
- Leverage: net debt rose by 43.5% to EUR 7.7bn, taking net leverage up by 0.59x to 1.88x.
- Liquidity: cash liquidity to revenue fell by 5.5 points to 22.0%, below the peer median of 29.0%.
- Margins: the EBITDA margin fell by 0.8 points to 13.1%, below the peer median of 14.6%.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 12,938 / 3,024 |
| 2 | credit_metrics, liquidity_funding, peer_positioning | passed | 14,566 / 1,740 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 3: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 1] liquidity_funding, sentence 3: word that states a number: 'two'
- [rule 5] peer_positioning, sentence 3: net_leverage.peer_median@FY2024 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: gross_leverage.peer_median@FY2024 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: interest_coverage.peer_median@FY2024 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: ffo_to_debt.peer_median@FY2024 is listed in the form but not used in the text

### Text with blanks (as the AI wrote it)

`snapshot`

- Air France-KLM, the Franco-Dutch network airline, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024 while EBITDA was broadly unchanged at {{ebitda@FY2024}}.
- Net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} as net debt increased by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}.
- The point to watch is cash generation: free cash flow turned negative at {{fcf@FY2024}} and cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.

`credit_metrics`

- EBITDA was stable at {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}}, but operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Total debt increased by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, lifting gross leverage by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}.
- FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, but FFO to debt fell by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}} as total debt increased by {{total_debt.change@FY2024}}.
- Free cash flow fell to {{fcf@FY2024}} from {{fcf@FY2023}} in FY2023, taking FCF to debt down by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}.
- Interest coverage eased by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, with capex intensity broadly unchanged at {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, while the fleet grew by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft.
- The average fleet age was stable at {{fleet_age@FY2024}}, with fleet renewal delayed by supply chain constraints and engine problems on part of the new-generation fleet.
- The operating result included a payment to Virgin in a contract renegotiation and a net provision for the restructuring of the domestic offer from Orly and of call centres.
- The group completed the acquisition of a minority stake in SAS AB and began a deepened commercial cooperation with the airline.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Customer prepayments rose: contract liabilities increased by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}.
- On the funding side, the group launched a cash tender offer on existing bond tranches and announced its intention to issue new bonds to refinance part of its existing debt.

`peer_positioning`

- Air France-KLM has the weakest EBITDA margin of the network airlines ({{ebitda_margin.peer_rank@FY2024}}), at {{ebitda_margin@FY2024}} against a peer median of {{ebitda_margin.peer_median@FY2024}}.
- FCF to debt is also the weakest of the group ({{fcf_to_debt.peer_rank@FY2024}}), and cash liquidity to revenue ranks {{cash_liquidity_to_revenue.peer_rank@FY2024}}.
- Leverage and coverage sit in the middle of the group, with net leverage, gross leverage, interest coverage and FFO to debt all in line with the peer medians of {{net_leverage.peer_median@FY2024}}, {{gross_leverage.peer_median@FY2024}}, {{interest_coverage.peer_median@FY2024}} and {{ffo_to_debt.peer_median@FY2024}} respectively, while advance ticket cover is the lowest of the group ({{advance_ticket_cover.peer_rank@FY2024}}).

`watch_items`

- Cash generation: free cash flow was negative at {{fcf@FY2024}} and FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, below the peer median of {{fcf_to_debt.peer_median@FY2024}}.
- Leverage: net debt rose by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, taking net leverage up by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}}.
- Margins: the EBITDA margin fell by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, below the peer median of {{ebitda_margin.peer_median@FY2024}}.
