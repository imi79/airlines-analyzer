# Air France-KLM, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v5`, fact sheet `32d65e3643a3` ([fact sheet](../factsheets/afkl_FY2024.md)). Tokens: 27,901 in, 5,926 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Air France-KLM, the Franco-Dutch network airline, grew revenue by 4.8% to EUR 31.5bn in FY2024, but net leverage rose by 0.59x to 1.88x as net debt increased.
The EBITDA margin narrowed by 0.8 points to 13.1%, with EBITDA broadly unchanged at EUR 4.1bn.
The point to watch is liquidity: cash liquidity to revenue fell by 5.5 points to 22.0%, the weakest of the network peers (3rd of 3), while free cash flow turned negative at EUR -232m.

## Credit metrics

EBITDA was broadly unchanged at EUR 4.1bn, a move of 1.5%, while operating profit fell by 12.6% to EUR 1.5bn after a payment to Virgin in a contract renegotiation and a restructuring provision at Orly.
Total debt rose by 7.4% to EUR 14.6bn and net debt by 43.5% to EUR 7.7bn, lifting gross leverage to 3.56x from 3.27x.
FFO rose by 2.1% to EUR 3.4bn, but FFO to debt fell by 1.2 points to 23.4% as total debt increased by 7.4%.
Free cash flow turned negative at EUR -232m from EUR 55.0m in FY2023, taking FCF to debt down by 2.0 points to -1.6%, with capex intensity broadly unchanged at 11.9%.
Interest coverage fell by 0.45x to 6.51x, still in line with the peer median.

> Event `event:costs`: Operating result for the year included a payment to Virgin as part of the renegotiation of a contract. Quote (page 369): "un versement de (115) millions d’euros à Virgin dans le cadre de la renégociation d’un contrat ;"

> Event `event:capacity_and_network`: A net provision was recorded for the restructuring of the domestic offer from Orly and of call centres. Quote (page 369): "une provision nette de (49) millions liée à la restructuration de l’offre domestique au départ d’Orly et des centres d’appel."

## Operating performance

Passengers rose by 4.7% to 98.0m, with revenue up 4.8% to EUR 31.5bn.
The fleet grew by 4.3% to 564 aircraft, with an average age broadly unchanged at 12.1 years.
Fleet renewal was delayed by supply chain constraints and engine problems on part of the new-generation fleet, which the group could not operate at maximum capacity.
The group completed the acquisition of a minority stake in SAS and began a deepened commercial cooperation with the airline.

> Event `event:fleet_and_engines`: Fleet renewal was delayed by supply chain constraints and engine problems on part of the new-generation fleet, preventing the group from operating those aircraft at maximum capacity. Quote (page 5): "En 2024, l’intensité GES s’est améliorée (- 1 %) par rapport à 2023 dans un contexte de retards dans le renouvellement de la flotte, en raison de contraintes dans la chaîne d’approvisionnement, de problèmes de moteurs sur une partie de la flotte d’avions de nouvelle génération ne permettant pas au Groupe de les exploiter à leur capacité maximale"

> Event `event:acquisitions_and_disposals`: The group completed the acquisition of a minority stake in SAS AB and began a deepened commercial cooperation with the airline. Quote (page 371): "Après l’obtention d’autorisations réglementaires en Europe et aux États-Unis, le groupe Air France-KLM a donc finalisé le 28 août 2024 l’acquisition d’une participation minoritaire de 19,90 % dans le capital de SAS AB."

## Liquidity and funding

Cash and cash-like investments fell by 16.0% to EUR 6.9bn, and cash liquidity to revenue declined by 5.5 points to 22.0%.
Advance ticket cover rose by 12.4 points to 59.1%, and contract liabilities increased by 6.2% to EUR 4.1bn, so a larger share of the cash balance is customers' prepayments.
The group launched a cash tender offer on existing bond tranches and announced its intention to issue new bonds to refinance part of its existing debt.

> Event `event:funding_and_rating`: The company launched a cash tender offer on existing bond tranches and announced its intention to issue new bonds to refinance part of its existing debt. Quote (page 12): "Air France-KLM annonce le lancement d’une offre de rachat sur deux souches obligataires existantes et son intention de procéder à une nouvelle émission obligataire"

## Peer positioning

The EBITDA margin of 13.1% is the weakest of the network airlines (3rd of 3), below the peer median of 14.6%.
On leverage and coverage the group sits in the middle of the group: net leverage ranks 2nd of 3, gross leverage 2nd of 3, interest coverage 2nd of 3 and FFO to debt 2nd of 3.
FCF to debt is the weakest of the group (3rd of 3), against a peer median of 20.3%, and cash liquidity to revenue is also the lowest (3rd of 3).
Advance ticket cover is the lowest of the group (1st of 3), which is the better position for credit, while capex intensity is above the peer median of 8.8%.

## Watch items

- Liquidity: cash liquidity to revenue fell by 5.5 points to 22.0%, the weakest of the network peers (3rd of 3), as cash and cash-like investments declined by 16.0%.
- Cash generation: free cash flow was negative at EUR -232m, taking FCF to debt to -1.6%, the weakest of the group (3rd of 3).
- Leverage: net leverage rose by 0.59x to 1.88x as net debt increased by 43.5%, leaving the group in the middle of the peer group.
- Margins: the EBITDA margin of 13.1% is the weakest of the network airlines (3rd of 3), with capex intensity of 11.9% above the peer median of 8.8%.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 12,697 / 3,348 |
| 2 | credit_metrics, liquidity_funding, peer_positioning, watch_items | passed | 15,204 / 2,578 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 3: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 1] liquidity_funding, sentence 3: word that states a number: 'two'
- [rule style] peer_positioning, sentence 4: capex_intensity@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Air France-KLM, the Franco-Dutch network airline, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, but net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} as net debt increased.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, with EBITDA broadly unchanged at {{ebitda@FY2024}}.
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, the weakest of the network peers ({{cash_liquidity_to_revenue.peer_rank@FY2024}}), while free cash flow turned negative at {{fcf@FY2024}}.

`credit_metrics`

- EBITDA was broadly unchanged at {{ebitda@FY2024}}, a move of {{ebitda.change@FY2024}}, while operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} after a payment to Virgin in a contract renegotiation and a restructuring provision at Orly.
- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, lifting gross leverage to {{gross_leverage@FY2024}} from {{gross_leverage@FY2023}}.
- FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, but FFO to debt fell by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}} as total debt increased by {{total_debt.change@FY2024}}.
- Free cash flow turned negative at {{fcf@FY2024}} from {{fcf@FY2023}} in FY2023, taking FCF to debt down by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, with capex intensity broadly unchanged at {{capex_intensity@FY2024}}.
- Interest coverage fell by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, still in line with the peer median.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, with revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}}.
- The fleet grew by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft, with an average age broadly unchanged at {{fleet_age@FY2024}}.
- Fleet renewal was delayed by supply chain constraints and engine problems on part of the new-generation fleet, which the group could not operate at maximum capacity.
- The group completed the acquisition of a minority stake in SAS and began a deepened commercial cooperation with the airline.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, and contract liabilities increased by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, so a larger share of the cash balance is customers' prepayments.
- The group launched a cash tender offer on existing bond tranches and announced its intention to issue new bonds to refinance part of its existing debt.

`peer_positioning`

- The EBITDA margin of {{ebitda_margin@FY2024}} is the weakest of the network airlines ({{ebitda_margin.peer_rank@FY2024}}), below the peer median of {{ebitda_margin.peer_median@FY2024}}.
- On leverage and coverage the group sits in the middle of the group: net leverage ranks {{net_leverage.peer_rank@FY2024}}, gross leverage {{gross_leverage.peer_rank@FY2024}}, interest coverage {{interest_coverage.peer_rank@FY2024}} and FFO to debt {{ffo_to_debt.peer_rank@FY2024}}.
- FCF to debt is the weakest of the group ({{fcf_to_debt.peer_rank@FY2024}}), against a peer median of {{fcf_to_debt.peer_median@FY2024}}, and cash liquidity to revenue is also the lowest ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).
- Advance ticket cover is the lowest of the group ({{advance_ticket_cover.peer_rank@FY2024}}), which is the better position for credit, while capex intensity is above the peer median of {{capex_intensity.peer_median@FY2024}}.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, the weakest of the network peers ({{cash_liquidity_to_revenue.peer_rank@FY2024}}), as cash and cash-like investments declined by {{cash_like.change@FY2024}}.
- Cash generation: free cash flow was negative at {{fcf@FY2024}}, taking FCF to debt to {{fcf_to_debt@FY2024}}, the weakest of the group ({{fcf_to_debt.peer_rank@FY2024}}).
- Leverage: net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} as net debt increased by {{net_debt.change@FY2024}}, leaving the group in the middle of the peer group.
- Margins: the EBITDA margin of {{ebitda_margin@FY2024}} is the weakest of the network airlines ({{ebitda_margin.peer_rank@FY2024}}), with capex intensity of {{capex_intensity@FY2024}} above the peer median of {{capex_intensity.peer_median@FY2024}}.
