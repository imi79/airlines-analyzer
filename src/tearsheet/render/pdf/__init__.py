"""The two-page A4 PDF tearsheet (M6): an HTML page laid out for print, made into a PDF by
WeasyPrint, with the charts drawn by Altair (vl-convert) in the bundled Inter font.

Page 1: header, snapshot, key figures, the two charts, credit metrics.
Page 2: operating metrics, peers, liquidity and funding, watch items, the analyst view,
footnotes (definitions, filings, manifest line, disclaimer).

Figures come from the same library and tearsheet record as the app; the commentary is the
verifier-checked text with the analyst's edits. A figure awaiting review prints as "pending",
never as a number. If the tearsheet would run onto a third page, the body text steps down
(8.5, 8.0, 7.5 point); still too long is an error, never a silent cut (decision 0020).
"""

from __future__ import annotations

import base64
import html
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import cache
from pathlib import Path

import jinja2

from tearsheet.narrative.factsheet import load_narrative
from tearsheet.narrative.render import PLACEHOLDER, SMALL_UNITS
from tearsheet.ratings import header_text
from tearsheet.render import charts, notes
from tearsheet.render.library import Library, key
from tearsheet.render.manifest import summary_line
from tearsheet.render.tearsheet import (
    chart_series,
    kpi_table,
    load_app_config,
    peer_table_for,
)

HERE = Path(__file__).parent
FONTS = HERE / "fonts"
KIND_WORDS = {"network": "Network airline", "low_cost": "Low-cost airline"}
PAGES = 2


class Overflow(RuntimeError):
    """The tearsheet does not fit two pages even at the smallest text size."""


@dataclass
class Rendered:
    pdf: bytes
    font_size: float
    pages: int
    anchors: dict[str, int]  # section id -> page number (1-based)
    view_truncated: bool
    fonts: tuple[str, ...] = ()  # font families embedded (the bundled one: "Tearsheet Inter")


@cache
def _env() -> jinja2.Environment:
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(HERE), autoescape=True, trim_blocks=True,
        lstrip_blocks=True,
    )  # fmt: skip


@cache
def _register_fonts() -> None:
    import vl_convert

    vl_convert.register_font_directory(str(FONTS))


# --- Pieces of the page ---------------------------------------------------------------------


def sentence_html(text_blanks: str, rendered: dict[str, str]) -> str:
    """Escaped text, every figure in bold, filled from the fact sheet."""
    out, last = [], 0
    for m in PLACEHOLDER.finditer(text_blanks):
        out.append(html.escape(text_blanks[last : m.start()]))
        out.append(f"<b>{html.escape(rendered.get(m.group(1), 'n.a.'))}</b>")
        last = m.end()
    out.append(html.escape(text_blanks[last:]))
    return "".join(out)


def _section(ts: dict, name: str, note: dict, rendered: dict, marks: set) -> dict:
    sec = ts["commentary"].get(name) or {"title": name, "status": "not_drafted", "sentences": []}
    out = []
    edits = (note.get("edits") or {}).get(name, {})
    for n, s in enumerate(sec["sentences"], start=1):
        edit = edits.get(n)
        text = sentence_html(edit["text"] if edit else s["text_blanks"], rendered)
        if edit and edit.get("untraced"):
            text += '<span class="mark">†</span>'
            marks.add("untraced")
        out.append(text)
    draft_note = None
    if sec["status"] == "not_drafted":
        draft_note = "Not drafted for this year."
    elif sec["status"] != "passed":
        draft_note = "‡ Draft section not cleared by the verifier: edit before use."
        marks.add("draft")
    return {"title": sec["title"], "sentences": out, "note": draft_note}


def minus(text: str) -> str:
    """A typographic minus for negative figures in tables: EUR −232m, −1.6%."""
    return re.sub(r"(?<![\w])-(?=\d)", "\u2212", text)


def _cell(c, marks: set) -> dict:
    if c.status in ("verified", "overridden"):
        return {"text": html.escape(minus(c.rendered)), "cls": ""}
    word = {"unverified": "pending", "not_meaningful": "n.m.", "missing": "n.a."}[c.status]
    marks.add(c.status)
    return {"text": word, "cls": "flag"}


def _figures_table(lib: Library, ts: dict, table: dict, marks: set) -> dict:
    """Unit revenue and cost (per seat-km) print as numbers, with the unit in the label, so
    the table keeps to its column: "RASK (euro cents)" and 4.33."""
    small = SMALL_UNITS.get(ts["currency"], ts["currency"] + " cents")
    rows = []
    for r in table["rows"]:
        cells = [_cell(c, marks) for c in r["cells"]]
        label = r["label"]
        if lib.unit.get(r["metric"]) == "per_km":
            label = f"{label} ({small})"
            for cell in cells:
                cell["text"] = cell["text"].replace(f" {small}", "")
        rows.append({"label": label, "cells": cells})
    return {"first": "", "labels": [x.split(" (")[0] for x in table["labels"]], "rows": rows}


def _peers(lib: Library, ts: dict, config: dict, marks: set) -> dict:
    table = peer_table_for(lib, ts)
    short = config.get("short_names", {})
    members = table["members"]
    labels = [short.get(m, lib.issuers[m]["name"]) for m in members] + ["Median"]
    rows = []
    for r in table["rows"]:
        cells = []
        for m in members:
            c = r["cells"][m]
            cls = "own" if m == ts["issuer"] else ""
            if c.get("rendered"):
                rank = f' <span class="rank">({c["rank"]})</span>' if c.get("rank") else ""
                cells.append({"text": html.escape(minus(c["rendered"])) + rank, "cls": cls})
            else:
                word = "n.m." if c.get("nm") else ("pending" if c.get("key") else "n.a.")
                marks.add({"n.m.": "not_meaningful", "pending": "unverified"}.get(word, "missing"))
                cells.append({"text": word, "cls": f"{cls} flag".strip()})
        cells.append({"text": html.escape(minus(r["median_rendered"] or "n.a.")), "cls": ""})
        rows.append({"label": r["label"], "cells": cells})
    return {
        "label": table["label"],
        "peer_year": table["peer_year"],
        "table": {"first": "", "labels": labels, "rows": rows},
        "metrics": [r["metric"] for r in table["rows"]],
    }


def _chart(lib: Library, ts: dict, chart_id: str, config: dict) -> dict:
    import vl_convert

    spec = config["charts"][chart_id]
    points = chart_series(lib, ts, chart_id, config)
    if not points:
        return {"title": spec["title"], "img": None}
    _register_fonts()
    chart = charts.leverage(points) if chart_id == "leverage" else charts.liquidity(
        points, ts["currency"])  # fmt: skip
    png = vl_convert.vegalite_to_png(charts.for_print(chart, 250, 105), scale=3)
    return {
        "title": spec["title"],
        "img": "data:image/png;base64," + base64.b64encode(png).decode(),
    }


def _view(note: dict, config: dict, font_size: float | None = None) -> tuple[list[str], bool]:
    """The analyst view as paragraphs that fit the box (about eight lines), and whether it
    had to be cut. Lines are estimated from the text size; the layout check confirms."""
    text = (note.get("analyst_view") or "").strip()
    if not text:
        return [], False
    pdf_conf = config["pdf"]
    size = font_size or pdf_conf["font_sizes"][0]
    per_line = int(pdf_conf["analyst_view_chars_per_line"] * pdf_conf["font_sizes"][0] / size)
    budget = pdf_conf["analyst_view_max_lines"]
    kept, cut = [], False
    for p in (p.strip() for p in text.splitlines() if p.strip()):
        lines = -(-len(p) // per_line)  # rounded up
        if lines <= budget:
            kept.append(p)
            budget -= lines
            continue
        room = budget * per_line - len(" … (continued in the app)")
        if room > 20:
            kept.append(p[:room].rsplit(" ", 1)[0])
        cut = True
        break
    if cut:
        if not kept:
            kept = [""]
        kept[-1] = kept[-1].rstrip(" .,;") + " … (continued in the app)"
    return kept, cut


def view_fits(note: dict, config: dict | None = None) -> bool:
    """False when the analyst view is longer than the PDF's box (the app warns before export)."""
    return not _view(note, config or load_app_config())[1]


def _filings(lib: Library, ts: dict, manifest: dict) -> list[dict]:
    """The company's own filings and documents behind the figures (peers': in the Excel)."""
    out = []
    for fid, e in manifest["filings"].items():
        if e["company"] != ts["issuer"]:
            continue
        rec = lib.filings.get(fid, {})
        hand = not e.get("link")
        label = (f"FY{e['fiscal_year']} statements entered by hand (PDF)" if hand
                 else f"FY{e['fiscal_year']} filing")  # fmt: skip
        out.append({"year": e["fiscal_year"] or 0, "link": e.get("link"), "label": label,
                    "id": fid, "origin": rec.get("origin")})  # fmt: skip
    for doc, e in manifest["documents"].items():
        if e["kind"] == "report supplied by Imane" and doc.startswith(ts["issuer"] + "-"):
            out.append({"year": 9999, "link": None, "label": f"report {e.get('file')}", "id": doc})
    return sorted(out, key=lambda f: (f["year"], f["label"]))


NOTE_TEXT = {
    "unverified": "<b>pending</b>: a figure read from the report text that has not passed every "
    "check, awaiting the analyst's review; never printed as a number.",
    "not_meaningful": "<b>n.m.</b>: not meaningful (for example a ratio to a very small debt, "
    "or leverage on negative EBITDA).",
    "missing": "<b>n.a.</b>: not available for that year.",
    "untraced": "<b>†</b> Sentence edited by the analyst with a figure not traced to a filing.",
    "draft": "<b>‡</b> Section the verifier did not clear after two retries: to be edited by "
    "the analyst.",
}


def context(lib: Library, ts: dict, note: dict | None, manifest: dict, font_size: float,
            config: dict | None = None) -> dict:  # fmt: skip
    config = config or load_app_config()
    note = note or notes.empty(ts["issuer"], ts["fiscal_year"])
    rendered = {k: v["rendered"] for k, v in ts["factsheet"]["items"].items()}
    marks: set[str] = set()
    sections = {
        name: _section(ts, name, note, rendered, marks) for name in load_narrative()["sections"]
    }
    credit = kpi_table(lib, ts, config, part="credit")
    operating = kpi_table(lib, ts, config, part="operating")
    peers = _peers(lib, ts, config, marks)
    view, _ = _view(note, config, font_size)
    page1 = list(dict.fromkeys(r["metric"] for r in credit["rows"]))
    page2 = [m for m in dict.fromkeys([r["metric"] for r in operating["rows"]] + peers["metrics"])
             if m not in page1]  # fmt: skip

    def defs(metrics):
        return [(lib.label[m], lib.definition[m]) for m in metrics if lib.definition.get(m)]

    info = lib.issuers[ts["issuer"]]
    exported = datetime.fromisoformat(manifest["exported_at"]).astimezone(UTC)
    return {
        "fs": font_size,
        "name": ts["name"],
        "period": ts["period_label"],
        "kind": KIND_WORDS.get(info.get("segment") or "", info["type"].capitalize()),
        "currency": ts["currency"],
        "peer_group": ts["peer_group"],
        "rating": header_text(ts.get("rating")),
        "exported": f"{exported:%d %b %Y}",
        "prepared_by": config.get("analyst") if (note.get("analyst_view") or "").strip() else None,
        "snapshot": sections["snapshot"],
        "credit": sections["credit_metrics"],
        "operating": sections["operating_performance"],
        "liquidity": sections["liquidity_funding"],
        "peer_text": sections["peer_positioning"],
        "watch": sections["watch_items"],
        "kpi": _figures_table(lib, ts, credit, marks),
        "operating_table": _figures_table(lib, ts, operating, marks),
        "charts": [_chart(lib, ts, c, config) for c in config["charts"]],
        "peers": peers,
        "view": view,
        "definitions_p1": defs(page1),
        "definitions": defs(page2),
        "notes": [NOTE_TEXT[m] for m in NOTE_TEXT if m in marks],
        "filings": _filings(lib, ts, manifest),
        "manifest_line": summary_line(manifest),
    }


def html_page(ctx: dict) -> str:
    return _env().get_template("tearsheet.html.j2").render(**ctx)


def layout_problems(doc) -> list[str]:
    """Overflow the page count cannot see: a box wider than the column it sits in (a table
    pushed sideways), or a clipped box whose content is taller than the box."""
    problems: list[str] = []

    def name(box) -> str:
        el = getattr(box, "element", None)
        cls = el.get("class") if el is not None else None
        return f"{getattr(box, 'element_tag', '?')}{'.' + cls if cls else ''}"

    def walk(box, parent, page_no):
        width = getattr(box, "width", None)
        if (
            parent is not None
            and isinstance(width, int | float)
            and hasattr(parent, "content_box_x")
        ):
            right = box.position_x + box.margin_width()
            limit = parent.content_box_x() + parent.width
            if isinstance(parent.width, int | float) and right > limit + 0.5:
                problems.append(f"page {page_no}: {name(box)} is {right - limit:.0f}px wider "
                                f"than {name(parent)}")  # fmt: skip
        if getattr(box, "style", None) is not None and box.style["overflow"] == "hidden":
            inside = sum(c.margin_height() for c in getattr(box, "children", []))
            if inside > box.height + 0.5:
                problems.append(f"page {page_no}: {name(box)} cuts off its last lines")
        for child in getattr(box, "children", []):
            walk(child, box, page_no)

    for n, page in enumerate(doc.pages, start=1):
        walk(page._page_box, None, n)
    return problems


def render(lib: Library, ts: dict, note: dict | None, manifest: dict,
           config: dict | None = None) -> Rendered:  # fmt: skip
    """The PDF at the largest text size that fits two pages with nothing pushed out of place."""
    import weasyprint

    config = config or load_app_config()
    from weasyprint.text.fonts import FontConfiguration

    fonts = FontConfiguration()  # without it, the bundled fonts (@font-face) are ignored
    css = weasyprint.CSS(
        filename=str(HERE / "tearsheet.css"), base_url=str(HERE), font_config=fonts
    )
    found: list[str] = []
    for size in config["pdf"]["font_sizes"]:
        ctx = context(lib, ts, note, manifest, size, config)
        doc = weasyprint.HTML(string=html_page(ctx), base_url=str(HERE)).render(
            stylesheets=[css], font_config=fonts
        )
        found = layout_problems(doc)
        if len(doc.pages) <= PAGES and not found:
            anchors = {a: n for n, page in enumerate(doc.pages, start=1) for a in page.anchors}
            _, cut = _view(note or {}, config, size)
            data = doc.write_pdf()
            families = tuple(sorted({str(f.family) for f in doc.fonts.values()}))
            return Rendered(data, size, len(doc.pages), anchors, cut, families)
    raise Overflow(
        f"{ts['name']} {ts['period_label']}: {len(doc.pages)} pages at {size} point"
        + (f"; {'; '.join(found[:3])}" if found else "")
    )


__all__ = ["Overflow", "Rendered", "key", "render", "view_fits"]
