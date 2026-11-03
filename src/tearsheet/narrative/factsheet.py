"""Fact sheet: everything the AI may talk about for one company and fiscal year.

Each item has an id the AI writes as a blank, for example:

    net_leverage@FY2025                the level for the year
    net_leverage@FY2024                the prior year
    net_leverage.change@FY2025         the change from FY2024, with direction and assessment
    net_leverage.peer_median@2025      the peer group's median for peer year 2025
    net_leverage.peer_rank@2025        the company's rank in its peer group (1 = strongest)

Only verified figures (or figures Imane approved) become items. Anything unverified, missing or
not meaningful is listed as "not available, do not discuss", with its reason, so the AI
cannot build a sentence on it and the verifier can tell it apart from a made-up id.

Directions are computed here, never by the AI: "up", "down" or "flat" against the threshold in
`catalog.yaml`, then "better", "worse" or "neutral" from the metric's "higher is better" flag.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import date
from decimal import Decimal
from pathlib import Path
from statistics import median

import yaml

from tearsheet.config import CONFIG, Issuer
from tearsheet.metrics.engine import labels, load_catalog, load_flat_thresholds
from tearsheet.metrics.peers import fiscal_label, peer_year
from tearsheet.narrative import render

NARRATIVE = CONFIG / "narrative.yaml"
PEERS = CONFIG / "peers.yaml"
NOT_VERIFIED = "not verified yet: waiting for Imane's review"
NOT_REPORTED = "no figure for this year"
PEER_UNVERIFIED = "the peer median would use a figure not verified yet"
TOO_FEW_PEERS = "fewer than two companies in the peer group have a value"


@dataclass(frozen=True)
class Spec:
    """What the fact sheet needs to know about a metric or statement line."""

    id: str
    label: str
    unit: str  # amount x pct count years per_km per_passenger
    higher_is_better: bool | None
    threshold: dict  # {"absolute": d} or {"relative": d}
    applies_to: tuple[str, ...] = ()


@dataclass(frozen=True)
class Figure:
    """One value from the facts database (or why there is none)."""

    issuer: str
    concept: str
    fiscal_year: int
    period_end: date
    value: Decimal | None
    status: str | None  # verified | unverified | overridden; None when there is no value
    reason: str | None = None  # why there is no value


@dataclass(frozen=True)
class Item:
    id: str
    metric: str
    kind: str  # value | change | peer_median | peer_rank
    label: str
    unit: str  # metric unit; for changes: x points relative years; for ranks: rank
    value: Decimal
    rendered: str
    period: str  # "FY2025", "FY2024 to FY2025", "peer year 2025"
    direction: str | None = None  # up | down | flat (current-year level and change)
    assessment: str | None = None  # better | worse | neutral
    vs_peers: str | None = None  # above | below | in_line (current-year level and median)
    peer_assessment: str | None = None  # better | worse | in_line | neutral
    rank: int | None = None
    rank_of: int | None = None
    note: str = ""


@dataclass
class FactSheet:
    issuer: str
    name: str
    type: str
    currency: str
    fiscal_year: int
    period_label: str  # FY2025 (Oct 2024 to Sep 2025)
    peer_year: int
    peer_group: str  # label, e.g. "Network airlines"
    peer_members: list[str]
    items: dict[str, Item] = field(default_factory=dict)
    unavailable: dict[str, str] = field(default_factory=dict)  # id -> reason
    higher_is_better: dict[str, bool | None] = field(default_factory=dict)  # metric -> flag
    labels: dict[str, str] = field(default_factory=dict)  # metric -> label

    @property
    def key(self) -> str:
        return f"{self.issuer}_FY{self.fiscal_year}"

    def rendered(self) -> dict[str, str]:
        return {i: item.rendered for i, item in self.items.items()}

    def to_dict(self) -> dict:
        out = asdict(self)
        out["items"] = {
            k: {kk: (str(vv) if isinstance(vv, Decimal) else vv) for kk, vv in asdict(v).items()}
            for k, v in self.items.items()
        }
        return out

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=1, ensure_ascii=False, sort_keys=True) + "\n"

    @classmethod
    def from_dict(cls, data: dict) -> FactSheet:
        data = dict(data)
        items = {}
        for k, v in data.pop("items").items():
            v = dict(v)
            v["value"] = Decimal(v["value"])
            items[k] = Item(**v)
        return cls(**data, items=items)

    @classmethod
    def from_json(cls, path: Path) -> FactSheet:
        return cls.from_dict(json.loads(path.read_text()))

    def fingerprint(self) -> str:
        return hashlib.sha256(self.to_json().encode()).hexdigest()


def load_narrative(path: Path = NARRATIVE) -> dict:
    return yaml.safe_load(path.read_text())


def load_specs(narrative: dict | None = None) -> dict[str, Spec]:
    """Catalog metrics, then the statement lines offered to the AI (config/narrative.yaml)."""
    narrative = narrative or load_narrative()
    catalog = load_catalog()
    thresholds = load_flat_thresholds()
    names = labels(catalog)
    specs = {}
    for metric, spec in catalog.items():
        specs[metric] = Spec(
            metric,
            spec["label"],
            spec["unit"],
            spec["higher_is_better"],
            spec.get("flat_threshold") or thresholds[spec["unit"]],
            tuple(spec.get("applies_to") or ()),
        )
    for line, better in narrative["statement_lines"].items():
        specs[line] = Spec(line, names[line], "amount", better, thresholds["amount"])
    return specs


# --- Directions --------------------------------------------------------------------------


def movement(spec: Spec, prior: Decimal, current: Decimal) -> tuple[str, Decimal | None, str]:
    """Direction (up, down, flat), the change to print (None if not meaningful) and its unit.

    Absolute thresholds (multiples, percentages): the change is the difference.
    Relative thresholds (amounts, traffic, unit revenue): the change is a share of the prior
    year, meaningful only when both years are positive."""
    diff = current - prior
    if "absolute" in spec.threshold:
        limit = Decimal(str(spec.threshold["absolute"]))
        direction = "flat" if abs(diff) < limit else ("up" if diff > 0 else "down")
        unit = {"x": "x", "pct": "points", "years": "years"}.get(spec.unit, spec.unit)
        return direction, abs(diff), unit
    limit = Decimal(str(spec.threshold["relative"]))
    if prior == 0:
        return ("flat" if diff == 0 else ("up" if diff > 0 else "down")), None, "relative"
    relative = diff / abs(prior)
    direction = "flat" if abs(relative) < limit else ("up" if diff > 0 else "down")
    meaningful = prior > 0 and current > 0
    return direction, (abs(relative) if meaningful else None), "relative"


def assess(direction: str, higher_is_better: bool | None) -> str:
    if direction == "flat" or higher_is_better is None:
        return "neutral"
    good = (direction == "up") == bool(higher_is_better)
    return "better" if good else "worse"


def against_median(spec: Spec, value: Decimal, mid: Decimal) -> tuple[str, str]:
    """(above | below | in_line, better | worse | in_line | neutral)."""
    diff = value - mid
    if "absolute" in spec.threshold:
        close = abs(diff) < Decimal(str(spec.threshold["absolute"]))
    else:
        close = mid != 0 and abs(diff / mid) < Decimal(str(spec.threshold["relative"]))
    if close or diff == 0:
        return "in_line", "in_line"
    side = "above" if diff > 0 else "below"
    if spec.higher_is_better is None:
        return side, "neutral"
    return side, "better" if (side == "above") == bool(spec.higher_is_better) else "worse"


# --- Building ----------------------------------------------------------------------------


def _usable(f: Figure | None) -> bool:
    return f is not None and f.value is not None and f.status in ("verified", "overridden")


def _why_not(f: Figure | None) -> str:
    if f is None:
        return NOT_REPORTED
    if f.value is None:
        return f.reason or NOT_REPORTED
    return NOT_VERIFIED


def peer_group(issuer_id: str, narrative: dict, peers: dict) -> tuple[str, list[str]]:
    for group in narrative["peer_groups"]:
        if issuer_id in peers["groups"][group]["members"]:
            return peers["groups"][group]["label"], list(peers["groups"][group]["members"])
    raise KeyError(f"{issuer_id} is in none of the peer groups {narrative['peer_groups']}")


def build(
    issuer: Issuer,
    fiscal_year: int,
    figures: list[Figure],
    specs: dict[str, Spec] | None = None,
    narrative: dict | None = None,
    peers: dict | None = None,
) -> FactSheet:
    """The fact sheet for `issuer` and `fiscal_year`, from every company's figures (the peer
    group's are needed for medians and ranks)."""
    narrative = narrative or load_narrative()
    specs = specs or load_specs(narrative)
    peers = peers or yaml.safe_load(PEERS.read_text())
    index = {(f.issuer, f.concept, f.fiscal_year): f for f in figures}
    ends = {}
    for f in figures:
        key = (f.issuer, f.fiscal_year)
        ends[key] = max(ends.get(key, f.period_end), f.period_end)
    end = ends[(issuer.id, fiscal_year)]
    group_label, members = peer_group(issuer.id, narrative, peers)
    sheet = FactSheet(
        issuer=issuer.id,
        name=issuer.name,
        type=issuer.type,
        currency=issuer.currency,
        fiscal_year=fiscal_year,
        period_label=fiscal_label(fiscal_year, end),
        peer_year=peer_year(end),
        peer_group=group_label,
        peer_members=members,
    )
    prior_year = fiscal_year - 1
    for metric, spec in specs.items():
        if spec.applies_to and issuer.type not in spec.applies_to:
            continue
        sheet.higher_is_better[metric] = spec.higher_is_better
        sheet.labels[metric] = spec.label
        cur = index.get((issuer.id, metric, fiscal_year))
        pri = index.get((issuer.id, metric, prior_year))
        cur_id, pri_id = f"{metric}@FY{fiscal_year}", f"{metric}@FY{prior_year}"
        change_id = f"{metric}.change@FY{fiscal_year}"
        for fid, fig, year in ((cur_id, cur, fiscal_year), (pri_id, pri, prior_year)):
            if _usable(fig):
                sheet.items[fid] = _level(fid, spec, fig, sheet.currency, f"FY{year}")
            else:
                sheet.unavailable[fid] = _why_not(fig)
        if _usable(cur) and _usable(pri):
            direction, change, unit = movement(spec, pri.value, cur.value)
            quality = assess(direction, spec.higher_is_better)
            sheet.items[cur_id] = _with(
                sheet.items[cur_id], direction=direction, assessment=quality
            )
            if change is not None:
                sheet.items[change_id] = Item(
                    id=change_id,
                    metric=metric,
                    kind="change",
                    label=f"change in {spec.label}, FY{prior_year} to FY{fiscal_year}",
                    unit=unit,
                    value=change,
                    rendered=(
                        render.change_text(change, unit)
                        if unit == "relative"
                        else render.change_between(pri.value, cur.value, unit)
                    ),
                    period=f"FY{prior_year} to FY{fiscal_year}",
                    direction=direction,
                    assessment=quality,
                    note="printed without a sign: say the direction in words",
                )
            else:
                sheet.unavailable[change_id] = (
                    "a percentage change is not meaningful (a year is negative or zero); "
                    f"the direction is still {direction}, on {cur_id}"
                )
        else:
            sheet.unavailable[change_id] = "needs both years verified"
        if metric in peers["metrics"]:
            _peer_items(sheet, spec, metric, cur, index, ends, members)
    return sheet


def _level(fid: str, spec: Spec, fig: Figure, currency: str, period: str) -> Item:
    return Item(
        id=fid,
        metric=spec.id,
        kind="value",
        label=f"{spec.label}, {period}",
        unit=spec.unit,
        value=fig.value,
        rendered=render.value_text(fig.value, spec.unit, currency),
        period=period,
    )


def _with(item: Item, **changes) -> Item:
    return Item(**(asdict(item) | changes))


def _peer_items(sheet, spec, metric, cur, index, ends, members) -> None:
    py = sheet.peer_year
    median_id, rank_id = f"{metric}.peer_median@{py}", f"{metric}.peer_rank@{py}"
    if not _usable(cur):
        reason = "the company's own figure is not available"
        sheet.unavailable[median_id] = sheet.unavailable[rank_id] = reason
        return
    values, unverified = {}, []
    for member in members:
        years = [y for (i, y) in ends if i == member and peer_year(ends[(i, y)]) == py]
        fig = index.get((member, metric, years[0])) if years else None
        if fig is None or fig.value is None:
            continue
        if fig.status not in ("verified", "overridden"):
            unverified.append(member)
            continue
        values[member] = fig.value
    if unverified:
        sheet.unavailable[median_id] = sheet.unavailable[rank_id] = (
            f"{PEER_UNVERIFIED} ({', '.join(unverified)})"
        )
        return
    if len(values) < 2:
        sheet.unavailable[median_id] = sheet.unavailable[rank_id] = TOO_FEW_PEERS
        return
    mid = median(values.values())
    side, quality = against_median(spec, cur.value, mid)
    group = f"{sheet.peer_group.lower()}, peer year {py}"
    sheet.items[median_id] = Item(
        id=median_id,
        metric=metric,
        kind="peer_median",
        label=f"{spec.label}, median of {group} ({len(values)} companies)",
        unit=spec.unit,
        value=mid,
        rendered=render.value_text(mid, spec.unit, sheet.currency),
        period=f"peer year {py}",
        vs_peers=side,
        peer_assessment=quality,
    )
    cur_id = f"{metric}@FY{sheet.fiscal_year}"
    sheet.items[cur_id] = _with(sheet.items[cur_id], vs_peers=side, peer_assessment=quality)
    if spec.higher_is_better is None:
        sheet.unavailable[rank_id] = "not ranked: neither higher nor lower is better"
        return
    ordered = sorted(values, key=lambda i: values[i], reverse=bool(spec.higher_is_better))
    rank = ordered.index(sheet.issuer) + 1
    sheet.items[rank_id] = Item(
        id=rank_id,
        metric=metric,
        kind="peer_rank",
        label=f"{spec.label}, rank in {group} (1st = strongest)",
        unit="rank",
        value=Decimal(rank),
        rendered=render.rank_text(rank, len(values)),
        period=f"peer year {py}",
        rank=rank,
        rank_of=len(values),
        note="best in the group" if rank == 1 else ("weakest" if rank == len(values) else ""),
    )


# --- Reading the facts database ------------------------------------------------------------


def load_figures(con, concepts: set[str]) -> list[Figure]:
    """Every company's primary value per concept and year, plus the reason for each gap."""
    rows = con.execute(
        "SELECT issuer, concept, fiscal_year, period_end, value, status FROM facts "
        "WHERE is_primary ORDER BY issuer, concept, fiscal_year"
    ).fetchall()
    out = [
        Figure(i, c, int(y), end, Decimal(str(v)), s)
        for i, c, y, end, v, s in rows
        if c in concepts
    ]
    have = {(f.issuer, f.concept, f.fiscal_year) for f in out}
    ends = {(f.issuer, f.fiscal_year): f.period_end for f in out}
    for i, y, c, reason in con.execute(
        "SELECT issuer, fiscal_year, concept, reason FROM gaps ORDER BY 1, 2, 3"
    ).fetchall():
        if c in concepts and (i, c, y) not in have and (i, y) in ends:
            out.append(Figure(i, c, int(y), ends[(i, y)], None, None, reason))
            have.add((i, c, y))
    return out


# --- The fact sheet as the AI (and Imane) reads it -------------------------------------------

QUIET_REASONS = ("needs both years verified", "the company's own figure is not available")


def _computed(item: Item) -> str:
    parts = []
    if item.direction:
        quality = f", {item.assessment}" if item.assessment != "neutral" else ""
        parts.append(f"{item.direction}{quality} vs prior year")
    if item.vs_peers:
        side = {"in_line": "in line with", "above": "above", "below": "below"}[item.vs_peers]
        quality = f", {item.peer_assessment}" if item.peer_assessment in ("better", "worse") else ""
        parts.append(f"company {side} peer median{quality}")
    if item.note:
        parts.append(item.note)
    return "; ".join(parts)


def as_text(sheet: FactSheet, narrative: dict | None = None) -> str:
    """Markdown tables: the figures by section, then what is not available and why."""
    narrative = narrative or load_narrative()
    lines = [
        f"# Fact sheet: {sheet.name}, {sheet.period_label}",
        "",
        f"Company type: {sheet.type}. Reporting currency: {sheet.currency}. "
        f"Peer group: {sheet.peer_group} ({', '.join(sheet.peer_members)}), "
        f"peer year {sheet.peer_year}.",
        "",
    ]
    placed: set[str] = set()
    for name, section in narrative["sections"].items():
        uses = section["uses"]
        if name == "peer_positioning":
            chosen = [i for i in sheet.items.values() if i.kind in ("peer_median", "peer_rank")]
        else:
            chosen = [
                i
                for i in sheet.items.values()
                if i.metric in uses and i.kind in ("value", "change") and i.id not in placed
            ]
        if not chosen:
            continue
        lines += [
            f"## {section['title']}",
            "",
            "| id | what it is | prints as | computed by code |",
            "| --- | --- | --- | --- |",
        ]
        for item in chosen:
            placed.add(item.id)
            lines.append(f"| {item.id} | {item.label} | {item.rendered} | {_computed(item)} |")
        lines.append("")
    others = [i for i in sheet.items.values() if i.id not in placed]
    if others:
        lines += ["## Other figures", "", "| id | what it is | prints as | computed by code |",
                  "| --- | --- | --- | --- |"]  # fmt: skip
        lines += [f"| {i.id} | {i.label} | {i.rendered} | {_computed(i)} |" for i in others]
        lines.append("")
    shown = {k: v for k, v in sheet.unavailable.items() if v not in QUIET_REASONS}
    lines += [
        "## Not available: do not discuss",
        "",
        "These figures are missing, not meaningful or not verified yet. Do not write about them, "
        "even without a blank.",
        "",
    ]
    lines += [f"- {k}: {v}" for k, v in shown.items()]
    return "\n".join(lines) + "\n"
