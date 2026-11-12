"""The watchlist (M9, decision 0023): credit triggers set by the analyst, checked by code.

The triggers live in config/watchlist.yaml, written as the analyst reads them ("net leverage
above 3.0x", "EBITDA margin down more than 3 points"). Every company and year is checked
against every trigger that applies to it, from the figure library only, so demo mode and live
mode give the same answer and every result leads to the figures behind it.

Each check ends in one of three states:

    fired           the figure crossed the threshold (strictly: exactly at it does not fire)
    clear           it did not
    cannot_assess   the figure is missing, not meaningful or awaiting review: the reason is
                    shown, and the trigger is never counted as clear (plan question 4)

The comparison uses the stored values, with all their decimals; rounding is for printing only.
Nothing here is a new financial figure: a level is read from the library, a move is the
difference between two stored years, as the fact sheet computes it.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from functools import cache
from pathlib import Path

import yaml

from tearsheet.config import CONFIG
from tearsheet.metrics.engine import load_catalog
from tearsheet.narrative import render
from tearsheet.render.library import Library, key, members_year, small_debt

WATCHLIST = CONFIG / "watchlist.yaml"

FIRED, CLEAR, CANNOT = "fired", "clear", "cannot_assess"
STATUS_WORDS = {FIRED: "fired", CLEAR: "clear", CANNOT: "cannot assess"}
KINDS = {"level": ("above", "below"), "move": ("up", "down")}
TYPES = ("all", "airline", "airport")
# the threshold's written unit, by kind and the metric's unit
UNITS = {
    ("level", "x"): "x",
    ("level", "pct"): "%",
    ("level", "amount"): "",
    ("move", "x"): "x",
    ("move", "pct"): "points",
}
CHANGE_UNIT = {"x": "x", "pct": "points"}


@dataclass(frozen=True)
class Trigger:
    id: str
    label: str
    kind: str  # level | move
    metric: str
    condition: str  # above | below | up | down
    threshold: Decimal  # in the stored unit: 0.20 for 20%, 0.03 for 3 points
    written: str  # as written in the file: "20%", "3 points"
    applies_to: str  # all | airline | airport
    reason: str
    set_by: str
    set_on: str
    floor: str | None = None

    def applies(self, company_type: str) -> bool:
        return self.applies_to in ("all", company_type)

    @property
    def short(self) -> str:
        """The label inside a sentence: "net leverage above 3.0x" (EBITDA keeps its capitals)."""
        lab = self.label
        return lab[0].lower() + lab[1:] if lab[1:2].islower() else lab


@dataclass(frozen=True)
class Check:
    trigger: str
    issuer: str
    fiscal_year: int
    status: str  # fired | clear | cannot_assess
    shown: str  # the figure as printed: "3.68x", "down 3.4 points", "n.a."
    detail: str  # one line in plain words: the figure against the threshold, or the reason
    keys: tuple[str, ...] = ()  # the library figures behind the result

    @property
    def ref(self) -> dict:
        return ref(self.trigger, self.issuer, self.fiscal_year)


def ref(trigger_id: str, issuer: str, fiscal_year: int) -> dict:
    """A source-card reference to one check (rendered by sources.card)."""
    return {"watch": trigger_id, "issuer": issuer, "year": fiscal_year}


# --- Loading the triggers ------------------------------------------------------------------------


def parse_threshold(written, kind: str, metric_unit: str) -> Decimal:
    """ "3.0x" -> 3.0; "20%" -> 0.20; "3 points" -> 0.03; 0 -> 0 (an amount)."""
    unit = UNITS.get((kind, metric_unit))
    if unit is None:
        raise ValueError(f"a {kind} trigger cannot use a metric in {metric_unit}")
    text = str(written).strip()
    if unit and not text.endswith(unit):
        raise ValueError(f"threshold {text!r}: write it in {unit!r}, like the metric")
    number = Decimal(text.removesuffix(unit).strip()) if unit else Decimal(text)
    if unit in ("%", "points"):
        number = number / 100
    if kind == "move" and number <= 0:
        raise ValueError(f"threshold {text!r}: a move is a size, above zero")
    return number


def load(path: Path = WATCHLIST) -> list[Trigger]:
    data = yaml.safe_load(path.read_text())
    catalog = load_catalog()
    out = []
    for tid, spec in (data.get("triggers") or {}).items():
        kind, metric, condition = spec["kind"], spec["metric"], spec["condition"]
        if kind not in KINDS or condition not in KINDS[kind]:
            raise ValueError(f"{tid}: {kind!r} with {condition!r} is not a trigger kind")
        for m in [metric] + ([spec["floor"]] if spec.get("floor") else []):
            if m not in catalog:
                raise ValueError(f"{tid}: {m!r} is not in catalog.yaml")
        if spec.get("applies_to", "all") not in TYPES:
            raise ValueError(f"{tid}: applies_to must be one of {TYPES}")
        if spec.get("floor") and (kind, condition) != ("level", "below"):
            raise ValueError(f"{tid}: a floor only makes sense for a 'below' level trigger")
        for field in ("label", "reason", "set_by", "set_on"):
            if not spec.get(field):
                raise ValueError(f"{tid}: {field} is required")
        unit = catalog[metric]["unit"]
        out.append(
            Trigger(
                id=tid,
                label=str(spec["label"]),
                kind=kind,
                metric=metric,
                condition=condition,
                threshold=parse_threshold(spec["threshold"], kind, unit),
                written=str(spec["threshold"]),
                applies_to=spec.get("applies_to", "all"),
                reason=" ".join(str(spec["reason"]).split()),
                set_by=str(spec["set_by"]),
                set_on=str(spec["set_on"]),
                floor=spec.get("floor"),
            )
        )
    return out


@cache
def triggers() -> tuple[Trigger, ...]:
    return tuple(load())


def by_id() -> dict[str, Trigger]:
    return {t.id: t for t in triggers()}


# --- Checking -------------------------------------------------------------------------------------


def standing(lib: Library, figure_key: str) -> tuple[Decimal | None, str | None]:
    """The figure's value if the tearsheet would print it, else None and why not: the same
    rules as the tearsheet's cells (verified or approved; not meaningful; awaiting review)."""
    f = lib.figure(figure_key)
    if f is None:
        return None, lib.why_missing(figure_key)
    tiny = small_debt(lib, f["issuer"], f["concept"], f["fiscal_year"])
    if tiny:
        return None, tiny
    if f["status"] not in ("verified", "overridden"):
        return None, "read from the report but not verified yet: awaiting Imane's review"
    return Decimal(f["value"]), None


def _exact(value: Decimal, unit: str) -> str:
    """The stored value with more decimals, for a figure that prints as the threshold."""
    if unit in ("pct", "points"):
        return f"{value * 100:.4f}%" if unit == "pct" else f"{value * 100:.4f} points"
    return f"{value:.4f}x" if unit == "x" else f"{value:,.0f}"


def check(lib: Library, trigger: Trigger, issuer: str, fiscal_year: int) -> Check:
    if trigger.kind == "level":
        return _level(lib, trigger, issuer, fiscal_year)
    return _move(lib, trigger, issuer, fiscal_year)


def _level(lib: Library, t: Trigger, issuer: str, year: int) -> Check:
    k = key(issuer, t.metric, year)
    value, why = standing(lib, k)
    label = lib.label.get(t.metric, t.metric)
    if value is None:
        if t.floor:
            return _floor(lib, t, issuer, year, label, why or "")
        keys = (k,) if k in lib.figures else ()
        return Check(t.id, issuer, year, CANNOT, "n.a.", f"{label}: {why}", keys)
    f = lib.figures[k]
    fired = value > t.threshold if t.condition == "above" else value < t.threshold
    words = t.condition if fired else f"not {t.condition}"
    detail = f"{label} {f['rendered']}, {words} {t.written}"
    unit = lib.unit.get(t.metric, "")
    if f["rendered"] == render.value_text(t.threshold, unit, f["currency"]):
        detail += f" (stored value {_exact(value, unit)})"
    return Check(t.id, issuer, year, FIRED if fired else CLEAR, f["rendered"], detail, (k,))


def _floor(lib: Library, t: Trigger, issuer: str, year: int, label: str,
           why: str) -> Check:  # fmt: skip
    """A 'below' trigger whose figure is not available, decided from a verified figure that can
    only be lower (decision 0023): the cash-only ratios leave out the undrawn credit lines, so if
    one is already at or above the threshold, the full ratio is too. Below it, nothing can be
    said; without it, both reasons are shown."""
    fk = key(issuer, t.floor or "", year)
    floor, floor_why = standing(lib, fk)
    if floor is None:  # the floor is not available either: say so with the main reason
        floor_label = lib.label.get(t.floor or "", t.floor or "")
        k = key(issuer, t.metric, year)
        detail = f"{label}: {why}. {floor_label}: {floor_why}"
        return Check(t.id, issuer, year, CANNOT, "n.a.", detail, (k,) if k in lib.figures else ())
    f = lib.figures[fk]
    floor_label = lib.label.get(t.floor or "", t.floor or "")
    if floor >= t.threshold:
        detail = (f"{label}: {why}. {floor_label} is {f["rendered"]}, already at or above "
                  f"{t.written}; the undrawn credit lines can only add to it")  # fmt: skip
        return Check(t.id, issuer, year, CLEAR, f"≥ {f['rendered']}", detail, (fk,))
    detail = (f"{label}: {why}. {floor_label} is {f["rendered"]}, below {t.written}, so "
              "the undrawn credit lines decide")  # fmt: skip
    k = key(issuer, t.metric, year)
    keys = ((k,) if k in lib.figures else ()) + (fk,)
    return Check(t.id, issuer, year, CANNOT, "n.a.", detail, keys)


def _move(lib: Library, t: Trigger, issuer: str, year: int) -> Check:
    k, pk = key(issuer, t.metric, year), key(issuer, t.metric, year - 1)
    label = lib.label.get(t.metric, t.metric)
    value, why = standing(lib, k)
    prior, prior_why = standing(lib, pk)
    if value is None or prior is None:
        reasons = []
        if value is None:
            reasons.append(f"FY{year}: {why}")
        if prior is None:
            reasons.append(f"FY{year - 1}: {prior_why}")
        keys = tuple(x for x in (pk, k) if x in lib.figures)
        return Check(t.id, issuer, year, CANNOT, "n.a.", f"{label}: " + "; ".join(reasons), keys)
    unit = CHANGE_UNIT[lib.unit.get(t.metric, "x")]
    diff = value - prior
    fired = diff > t.threshold if t.condition == "up" else -diff > t.threshold
    size = render.change_between(prior, value, unit)
    direction = "up" if diff > 0 else ("down" if diff < 0 else "unchanged")
    shown = f"{direction} {size}" if diff else "unchanged"
    before, now = lib.figures[pk]["rendered"], lib.figures[k]["rendered"]
    words = f"{t.condition} more than" if fired else f"not {t.condition} more than"
    detail = f"{label} {before} in FY{year - 1} to {now}: {shown}, {words} {t.written}"
    if size == render.change_text(t.threshold, unit):
        detail += f" (stored change {_exact(abs(diff), unit)})"
    return Check(t.id, issuer, year, FIRED if fired else CLEAR, shown, detail, (pk, k))


def checks_for(lib: Library, issuer: str, fiscal_year: int) -> list[Check]:
    """Every trigger that applies to the company, in the file's order."""
    company_type = lib.issuers[issuer]["type"]
    return [check(lib, t, issuer, fiscal_year) for t in triggers() if t.applies(company_type)]


def summary(checks: list[Check]) -> str:
    """The tearsheet line: "Watchlist: 2 triggers fired (net leverage above 3.0x; ...); 4 clear,
    1 cannot be assessed"."""
    names = by_id()
    fired = [names[c.trigger].short for c in checks if c.status == FIRED]
    clear = sum(1 for c in checks if c.status == CLEAR)
    cannot = sum(1 for c in checks if c.status == CANNOT)
    if fired:
        head = f"{len(fired)} trigger{'s' if len(fired) > 1 else ''} fired ({'; '.join(fired)})"
    else:
        head = "no trigger fired"
    tail = f"{clear} clear" + (f", {cannot} cannot be assessed" if cannot else "")
    return f"Watchlist: {head}; {tail}"


# --- The Watchlist page -----------------------------------------------------------------------


def board(lib: Library, peer_year: int, order: list[str]) -> list[dict]:
    """One row per company for a peer year (its fiscal year falling in it, decision 0008):
    the check of every trigger (None where the trigger does not apply), and which fired
    triggers are new (not fired the year before)."""
    rows = []
    for issuer in order:
        fy = members_year(lib, issuer, peer_year)
        if fy is None:
            continue
        company_type = lib.issuers[issuer]["type"]
        cells: dict[str, Check | None] = {}
        new: dict[str, str] = {}
        for t in triggers():
            if not t.applies(company_type):
                cells[t.id] = None
                continue
            c = check(lib, t, issuer, fy)
            cells[t.id] = c
            if c.status == FIRED:
                before = check(lib, t, issuer, fy - 1).status
                if before != FIRED:
                    new[t.id] = before
        rows.append({"issuer": issuer, "fiscal_year": fy,
                     "period_label": lib.period_label(issuer, fy), "cells": cells,
                     "new": new})  # fmt: skip
    return rows


# --- The source card of a check -----------------------------------------------------------------


def card(lib: Library, watch_ref: dict) -> dict:
    """The card a click on a trigger opens: the result, the figure against the threshold, and
    the figures behind it (followed down to the filing, like any other card)."""
    t = by_id()[watch_ref["watch"]]
    issuer, year = watch_ref["issuer"], int(watch_ref["year"])
    c = check(lib, t, issuer, year)
    name = lib.issuers.get(issuer, {}).get("name", issuer)
    return {
        "kind": "watch",
        "title": f"{t.label}, {name} {lib.period_label(issuer, year)}",
        "rendered": STATUS_WORDS[c.status].capitalize(),
        "how": f"Checked by code against the trigger set by {t.set_by} on {t.set_on} "
        "(config/watchlist.yaml); verified figures only",
        "lines": [c.detail, f"Why it matters: {t.reason}"],
        "inputs": [{"key": k} for k in c.keys],
    }
