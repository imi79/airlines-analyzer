# 0023 · M9: a watchlist of credit triggers

Date: 2026-11-12 · Status: plan approved by Imane with every recommendation (recorded in
`docs/m9/plan.md` and `docs/progress.md`); built on `m9-watchlist`, waiting for her go-ahead to
merge into `main`

**Choices approved with the plan** (`docs/m9/plan.md`):

1. **Scope A, the watchlist**: no new data source, no AI tokens; half-year figures (B) are the
   natural M10.
2. **Seven triggers, the same for every company**, except liquidity to revenue for airlines
   only. Thresholds to be adjusted by Imane after the first results.
3. **Flags on a Watchlist page and a line on each tearsheet and PDF.**
4. **Missing, not meaningful or unverified figures show as "cannot assess"**, with the reason,
   never as clear.

**How the check works.**

- **The triggers live in `config/watchlist.yaml`**, written as the analyst reads them ("3.0x",
  "20%", "3 points", 0 for an amount), each with its reason, `set_by` and `set_on`. Code turns
  the written threshold into the stored unit (20% is 0.20) and refuses a threshold in the wrong
  unit or a metric not in `catalog.yaml`. No financial figure is written in code.
- **Two kinds.** A *level* compares the year's figure with the threshold; a *move* compares the
  change on the prior fiscal year, as the fact sheet computes it (the difference; for a
  percentage, in points). No new metric: both read stored figures from the library.
- **Strict thresholds.** "Above 3.0x" fires only above it: a figure exactly at the threshold
  does not fire. The comparison uses the stored value with all its decimals, so Aena FY2022's
  net leverage of 3.0031x fires although it prints as "3.00x"; the card then says "stored value
  3.0031x" so the reader is not left puzzled.
- **The same rules as the tearsheet's cells.** A figure is used only if the tearsheet would
  print it: verified, or approved by Imane. Missing (with the stored reason, for example
  "n.m.: EBITDA is negative"), not meaningful (ratios to a very small debt, M4's rule) and
  awaiting review give "cannot assess" with that reason. A move needs both years usable.
- **One library for both modes.** The check reads the figure library, so demo mode and live
  mode agree, and a session approval in demo mode reaches the watchlist at once (nothing is
  saved). The tearsheet line is computed when the page or PDF is drawn, not stored in the
  sample files: changing a threshold needs no rebuild.

**One choice beyond the plan: a floor for the liquidity trigger.** Liquidity = cash and liquid
investments + undrawn committed credit lines. Where liquidity is missing or awaiting review
(the undrawn lines are the usual gap), but *cash liquidity* (the same without the undrawn
lines) is verified and already at or above 20% of revenue, liquidity is necessarily above 20%
too: the undrawn lines can only add. The trigger is then **clear**, and its card says it was
decided on cash alone. If cash liquidity is below 20%, the undrawn lines decide, and the
trigger stays "cannot assess". The floor can only clear a "below" trigger, never fire one, and
is never used when liquidity itself is verified. It is written in the triggers file
(`floor: cash_liquidity_to_revenue`), so Imane can remove it. Without it, 7 of the 12 airline
tearsheets could not be assessed on liquidity although the answer is not in doubt. The same
reasoning would work for short-term debt cover (cash ÷ debt due within a year), but that ratio
is not in the catalog; adding it is a new metric, left for Imane to decide.

**"New warning".** A trigger that fired this year and did not fire the year before (clear, or
not assessable then). Shown with the prior year's state, so "new, cannot assess the year
before" is not mistaken for a fresh deterioration.

**Where it shows.**

- **Watchlist page** (`/watchlist`): companies down the side for one peer year (each company's
  fiscal year as on the Peers page, decision 0008), triggers across the top, each cell fired,
  clear or cannot assess with the figure; filters for "with a trigger fired" and "with a new
  warning"; every fired trigger listed with a source button; the cannot-assess list with
  reasons; the triggers with their owner and date.
- **Tearsheet and PDF**: one line under the ratings, "Watchlist: 1 trigger fired (net leverage
  above 3.0x); 4 clear, 1 cannot be assessed". In the app, a source button opens the fired
  triggers' cards and a link opens the page. The commentary is not redrafted and does not
  mention the triggers: they are shown beside it.
- **Source card** of a trigger: the result, the figure against the threshold (and last year's
  for a move), why the trigger matters, who set it and when, and the figures behind it, each
  followed down to the filing fact, quote or hand entry. The fired triggers are part of the
  page's figures, so the export manifest lists their sources too.

**Results at M9** (18 tearsheets, 120 checks): 9 fired, 97 clear, 14 cannot assess (12 of them
short-term debt cover, where the undrawn lines are missing or awaiting review; 2 interest
coverage at Flughafen Wien, whose debt is very small). PDF: 18 of 18 on two pages; the line
changes no tearsheet's text size (11 at 8.5 point, 7 at 8.0, as before M9).
