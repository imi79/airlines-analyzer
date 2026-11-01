"""From checked figures to facts: cross-checks across reports, reviews, one value per year.

Cross-checks (a figure that fails one stays unverified):
- agreement: the same figure for the same year read from two reports (the year's own report
  and the next year's comparative) must agree within the rounding of what is printed;
- load factor: RPK ÷ ASK must equal the load factor the company prints, within rounding;
- year on year: a figure may not jump beyond the item's `max_change` between two years.
Then Imane's reviews (config/extraction_reviews.yaml) approve or correct figures; a correction
is stored as an override with author, date and reason.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date
from decimal import Decimal
from pathlib import Path

import yaml

from tearsheet.config import CONFIG, Issuer
from tearsheet.extract.fx import Converter
from tearsheet.extract.grounding import Checked
from tearsheet.normalize.mapper import MappedFact

REVIEWS = CONFIG / "extraction_reviews.yaml"


@dataclass
class Candidate:
    """One value for an issuer, year and figure, from one report (or a sum of components)."""

    item: str
    fiscal_year: int
    value: Decimal | None
    decimals: int | None
    figures: list[Checked]  # one, or the components summed
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    status: str = "unverified"  # verified | unverified | overridden
    primary: bool = False
    review: dict | None = None

    @property
    def doc(self):
        return self.figures[0].doc

    @property
    def own_report(self) -> bool:
        return self.doc.fiscal_year == self.fiscal_year

    def tolerance(self, unit: str) -> Decimal:
        """Half a unit of the last printed digit."""
        if unit == "pct":
            printed = self.figures[0].raw.printed_value or ""
            places = (
                len(printed.replace(",", ".").split(".")[1])
                if "." in printed.replace(",", ".")
                else 0
            )
            return Decimal(5) / Decimal(10) ** (places + 3)
        if unit == "years":
            return Decimal("0.05")
        if self.decimals is None:
            return Decimal(0)
        return Decimal(5) * Decimal(10) ** (-self.decimals - 1) * len(self.figures)


def build_candidates(
    figures: list[Checked],
    issuer: Issuer,
    items: dict[str, dict],
    period_end: dict[int, date],
    revenue: dict[int, Decimal],
    convert: Converter | None,
) -> list[Candidate]:
    """One candidate per report, year and figure; components of a total are summed."""
    groups: dict[tuple[str, int, str], list[Checked]] = {}
    for f in figures:
        groups.setdefault((f.doc.doc_id, f.fiscal_year, f.item), []).append(f)
    candidates = []
    for (_, year, item_id), group in groups.items():
        item = items[item_id]
        totals = [f for f in group if not f.raw.component]
        parts = [f for f in group if f.raw.component]
        if totals:
            # Several totals for one figure from one report: keep the verified one if only
            # one is; otherwise they must agree.
            verified = [f for f in totals if f.verified]
            chosen = verified[0] if len(verified) == 1 else totals[0]
            c = _candidate(item_id, year, [chosen])
            values = {f.value for f in (verified or totals) if f.value is not None}
            if len(values) > 1:
                c.failures.append("the report gives different values for this figure")
            if parts:
                c.notes.append("components also recorded; the total is used")
        else:
            c = _candidate(item_id, year, parts)
            if len(parts) > 1:
                currencies = {f.currency for f in parts}
                if len(currencies) > 1:
                    c.failures.append("components in different currencies")
                    c.value = None
        if item["unit"] == "amount" and c.value is not None:
            _to_reporting_currency(c, issuer, year, period_end, convert)
            _range_after_conversion(c, item, revenue.get(year))
        c.status = "verified" if c.value is not None and not c.failures else "unverified"
        candidates.append(c)
    return candidates


def _candidate(item_id: str, year: int, figures: list[Checked]) -> Candidate:
    failures = [f"{x}" for f in figures for x in f.failures]
    notes = [n for f in figures for n in f.notes]
    values = [f.value for f in figures]
    value = sum(values, Decimal(0)) if all(v is not None for v in values) else None
    decimals = [f.decimals for f in figures if f.decimals is not None]
    if len(figures) > 1 and value is not None:
        notes.append(f"sum of {len(figures)} facilities")
    return Candidate(item_id, year, value, min(decimals) if decimals else None, figures,
                     failures, notes)  # fmt: skip


def _to_reporting_currency(c, issuer, year, period_end, convert) -> None:
    currency = c.figures[0].currency or issuer.currency
    if currency == issuer.currency:
        return
    if convert is None or year not in period_end:
        c.failures.append(f"reported in {currency}; no exchange rate available")
        return
    try:
        c.value, note = convert(c.value, currency, issuer.currency, period_end[year])
    except (KeyError, FileNotFoundError) as exc:
        c.failures.append(f"reported in {currency}; no exchange rate ({exc.args[0]})")
        return
    c.decimals = None
    c.notes.append(note)


def _range_after_conversion(c: Candidate, item: dict, revenue: Decimal | None) -> None:
    if "range_of_revenue" not in item or revenue is None or revenue <= 0 or c.value is None:
        return
    if not any(n.startswith("converted") for n in c.notes):
        return  # already checked in grounding, in the reporting currency
    low, high = (Decimal(str(x)) for x in item["range_of_revenue"])
    share = c.value / revenue
    if not (low <= share <= high):
        c.failures.append(f"value is {share:.0%} of revenue, outside the plausible range")


def cross_check(
    candidates: list[Candidate], items: dict[str, dict], load_factor_basis: str = "rpk_ask"
) -> None:
    """`load_factor_basis` 'seats' means the company prints seats sold ÷ seats offered, so the
    RPK ÷ ASK check does not apply (config/extraction.yaml)."""
    by_key: dict[tuple[int, str], list[Candidate]] = {}
    for c in candidates:
        by_key.setdefault((c.fiscal_year, c.item), []).append(c)

    # Agreement between reports.
    for (year, item_id), group in by_key.items():
        verified = [c for c in group if c.status == "verified"]
        unit = items[item_id]["unit"]
        for a in verified:
            for b in verified:
                if a is b or a.doc.doc_id >= b.doc.doc_id:
                    continue
                if abs(a.value - b.value) > max(a.tolerance(unit), b.tolerance(unit)):
                    msg = (
                        f"reports disagree for FY{year}: {_show(a.value, unit)} in the "
                        f"FY{a.doc.fiscal_year} report, {_show(b.value, unit)} in the "
                        f"FY{b.doc.fiscal_year} report (restated?)"
                    )
                    for c in (a, b):
                        c.failures.append(msg)
                        c.status = "unverified"
                else:
                    for c in (a, b):
                        other = b if c is a else a
                        c.notes.append(f"matches the FY{other.doc.fiscal_year} report")

    # Choose one value per year and figure.
    primary: dict[tuple[int, str], Candidate] = {}
    for key, group in by_key.items():
        ordered = sorted(
            group,
            key=lambda c: (c.status != "verified", not c.own_report, -c.doc.fiscal_year),
        )
        ordered[0].primary = True
        primary[key] = ordered[0]

    # RPK ÷ ASK against the printed load factor.
    for (year, item_id), lf in list(primary.items()):
        if item_id != "load_factor" or lf.status != "verified":
            continue
        if load_factor_basis == "seats":
            for key in ((year, "ask"), (year, "rpk")):
                if key in primary:
                    primary[key].notes.append(
                        "RPK ÷ ASK not checked against the printed load factor: the company "
                        "computes it as seats sold ÷ seats offered"
                    )
            continue
        ask, rpk = primary.get((year, "ask")), primary.get((year, "rpk"))
        if not (ask and rpk and ask.status == rpk.status == "verified"):
            continue
        computed = rpk.value / ask.value
        slack = lf.tolerance("pct") + computed * (
            ask.tolerance("count") / ask.value + rpk.tolerance("count") / rpk.value
        )
        if rpk.value > ask.value or abs(computed - lf.value) > slack:
            msg = (
                f"RPK ÷ ASK = {computed:.1%} but the report prints a load factor of {lf.value:.1%}"
            )
            for c in (ask, rpk):
                c.failures.append(msg)
                c.status = "unverified"
        else:
            for c in (ask, rpk):
                c.notes.append(f"RPK ÷ ASK = {computed:.1%} matches the printed load factor")

    # Year-on-year jumps.
    for (year, item_id), c in primary.items():
        limit = items[item_id].get("max_change")
        before = primary.get((year - 1, item_id))
        if not limit or not before or before.status != "verified" or c.status != "verified":
            continue
        if before.value <= 0 or c.value <= 0:
            continue
        ratio = c.value / before.value
        if ratio > limit or ratio < Decimal(1) / Decimal(limit):
            msg = (
                f"moves from {_show(before.value, items[item_id]['unit'])} in FY{year - 1} to "
                f"{_show(c.value, items[item_id]['unit'])} in FY{year}: implausible jump"
            )
            for x in (before, c):
                x.failures.append(msg)
                x.status = "unverified"


def _show(value: Decimal, unit: str) -> str:
    if unit == "pct":
        return f"{value:.1%}"
    if unit == "years":
        return f"{value:.1f} years"
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:,.2f}bn"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.1f}m"
    return f"{value:,.0f}"


def load_reviews(path: Path = REVIEWS) -> list[dict]:
    if not path.exists():
        return []
    return (yaml.safe_load(path.read_text()) or {}).get("reviews") or []


def apply_reviews(issuer: Issuer, candidates: list[Candidate], reviews: list[dict]) -> list[str]:
    """Apply Imane's approvals and corrections. Returns reviews that matched nothing."""
    unmatched = []
    for r in reviews:
        if r["issuer"] != issuer.id:
            continue
        target = next(
            (
                c
                for c in candidates
                if c.primary and c.fiscal_year == int(r["fiscal_year"]) and c.item == r["item"]
            ),
            None,
        )
        who = f"{r['by']} on {r['on']}: {r['reason']}"
        if target is None:
            unmatched.append(f"{issuer.id} FY{r['fiscal_year']} {r['item']}")
            continue
        target.review = r
        if r["action"] == "approve":
            if target.value is None:
                unmatched.append(f"{issuer.id} FY{r['fiscal_year']} {r['item']} (no value)")
                continue
            target.status = "verified"
            target.notes.append(f"approved by {who}")
        elif r["action"] == "correct":
            target.value = Decimal(str(r["value"]))
            target.decimals = None
            target.status = "overridden"
            target.notes.append(f"corrected by {who}")
        else:
            raise ValueError(f"extraction_reviews.yaml: unknown action {r['action']}")
    return unmatched


def to_facts(issuer: Issuer, candidates: list[Candidate], period_end: dict[int, date],
             scopes: dict[str, str]) -> list[MappedFact]:  # fmt: skip
    facts = []
    for c in sorted(candidates, key=lambda c: (c.fiscal_year, c.item, not c.primary)):
        if c.value is None or c.fiscal_year not in period_end:
            continue
        first = c.figures[0]
        r = first.raw
        quotes = tuple(f.raw.quote or "" for f in c.figures)
        locations = tuple(f.location or "" for f in c.figures)
        printed = " + ".join(f"{f.raw.printed_value} {f.raw.scale}" for f in c.figures)
        note = (
            f"Read from the FY{c.doc.fiscal_year} report ({', '.join(locations)}): "
            f"“{quotes[0].strip()}”" + (f" and {len(quotes) - 1} more" if len(quotes) > 1 else "")
        )
        facts.append(
            MappedFact(
                issuer=issuer.id,
                fiscal_year=c.fiscal_year,
                period_end=period_end[c.fiscal_year],
                line=c.item,
                value=c.value,
                value_tagged=sum((f.value or Decimal(0) for f in c.figures), Decimal(0)),
                decimals=c.decimals,
                currency=issuer.currency,
                filing_id=c.doc.doc_id,
                comparative=not c.own_report,
                concepts=quotes,
                fact_ids=locations,
                rule_source="extracted",
                sign=1,
                note=note,
                footnote=scopes.get(c.item),
                primary=c.primary,
                warnings=tuple(c.failures),
                source_type="extracted",
                status=c.status,
                ref={
                    "document": c.doc.doc_id,
                    "document_sha256": c.doc.sha256,
                    "source": c.doc.source,
                    "locations": list(locations),
                    "quotes": list(quotes),
                    "printed": printed,
                    "currency_printed": first.currency,
                    "scope": r.scope,
                    "checks_failed": list(c.failures),
                    "notes": list(c.notes),
                    "review": c.review,
                },
            )
        )
    return facts


def with_model(facts: list[MappedFact], model_by_doc: dict[str, dict]) -> list[MappedFact]:
    """Add the provider, model, prompt version and request fingerprint to each fact's record."""
    out = []
    for f in facts:
        ref = dict(f.ref or {})
        ref.update(model_by_doc.get(f.filing_id, {}))
        out.append(replace(f, ref=ref))
    return out
