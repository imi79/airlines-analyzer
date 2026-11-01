# 0011 · M3: scope of each operating figure, and which ratios join the peer tables

Date: 2026-11-01 · Status: accepted (follows the M3 plan, "known difficulties")

**Scope per company** (`config/extraction.yaml`). Companies count passengers and fleet on
different perimeters, much as they define net debt differently (decision 0008). The scope we
want is written per company, sent to the AI with the request, and used as the tearsheet
footnote:

- Airlines: the group total (Air France-KLM with Transavia, IAG all airlines, Norwegian with
  Widerøe from 2024 where the group total is printed).
- Airports: passengers on the same perimeter as the aeronautical revenue, so that aeronautical
  revenue per passenger compares like with like. ADP: Paris airports only (not TAV and the
  international network). Aena: the Spanish network only (not Luton or Brazil). Flughafen
  Wien: Vienna only (not Malta and Košice).

If the report only gives another perimeter, the AI must say "not found" and describe what it
saw; it may not substitute.

**Peer tables.** Load factor, fuel hedge ratio, traffic growth and non-aeronautical share join
the peer tables: they are percentages, so they compare across currencies. Unit revenues and
costs (RASK, CASK, yield, revenue per passenger) stay on each company's page in its own
currency and join the peer tables when the peer page converts currencies (M5).
