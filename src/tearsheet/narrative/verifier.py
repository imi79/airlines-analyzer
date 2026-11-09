"""The verifier: code reads every sentence the AI drafted before anything reaches the page.

A sentence is rejected if it breaks any of the five rules of the M4 plan:

1. a number written outside a blank (digits, %, currency signs, "bn", or words such as
   "doubled", "a third", "record"); fiscal-year labels, years and names such as "IFRS 16" or
   "A321neo" are allowed;
2. a blank whose id is not in the fact sheet, or points to a figure that is not available;
3. a claimed direction that contradicts the one computed by code;
4. a direction word in the prose ("rose", "improved", "lowest") not backed by a matching
   claim on a figure of the same clause, so the form and the sentence cannot disagree (a
   clause with no blank that states a scenario, "if bookings slow", is not a statement about
   a reported figure and is not read, nor is a clause with no blank that describes a cited
   event and names no figure, "Fitch upgraded the rating": decision 0018);
5. ids listed in the form that the sentence doesn't use, or the reverse (an event of the
   year, `event:...`, is listed but never written as a blank: it has no figure);
6. a figure from an earlier year used on its own, without its year in the sentence ("the
   fleet stood at {{fleet@FY2024}}" in an FY2025 note must say "in FY2024") (decision 0018).

Plus the form itself ("form"): every section present, with the number of sentences the
tearsheet allows (the snapshot has exactly three).

Style notes ("style", decision 0018) are not rejections: each figure in one body section
only (the snapshot and the watch items may restate it). They go back to the AI with a retry,
and a rewrite is kept only if it breaks no rule above.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from tearsheet.narrative.factsheet import FactSheet, load_narrative
from tearsheet.narrative.render import PLACEHOLDER

VOCABULARY = Path(__file__).with_name("vocabulary.yaml")
CLAIMS = (
    "up",
    "down",
    "flat",
    "better",
    "worse",
    "above_peers",
    "below_peers",
    "in_line_with_peers",
    "better_than_peers",
    "worse_than_peers",
    "best_in_group",
    "worst_in_group",
)
YEAR = r"(?:201[5-9]|202\d|203[0-5])"
EVENT = "event:"
STYLE = "style"  # a note on the writing (repetition): fed back, never a rejection
SUMMARY_SECTIONS = ("snapshot", "watch_items")  # may restate a figure (decision 0018)
HYPOTHETICAL = re.compile(r"\b(?:if|unless|would|could|might|should)\b", re.I)
CLAUSE_BREAK = re.compile(  # brackets don't split: "(rank)" belongs to its clause
    r"[,;:\u2013\u2014]|\b(?:while|whereas|but|although|though|and|yet)\b", re.I
)


@dataclass(frozen=True)
class Ref:
    id: str
    claims: tuple[str, ...] = ()


@dataclass(frozen=True)
class Sentence:
    text: str
    facts: tuple[Ref, ...] = ()


@dataclass
class Draft:
    sections: dict[str, list[Sentence]]

    def to_dict(self) -> dict:
        return {
            name: [
                {"text": s.text, "facts": [{"id": r.id, "claims": list(r.claims)} for r in s.facts]}
                for s in sentences
            ]
            for name, sentences in self.sections.items()
        }

    @classmethod
    def from_dict(cls, data: dict) -> Draft:
        draft, errors = parse_sections(data)
        if errors:
            raise ValueError("; ".join(e.message for e in errors))
        return draft


@dataclass(frozen=True)
class Error:
    section: str
    sentence: int | None  # 1-based; None for the section as a whole
    rule: str  # "1" to "5", or "form"
    message: str

    def __str__(self) -> str:
        where = self.section + (f", sentence {self.sentence}" if self.sentence else "")
        return f"[rule {self.rule}] {where}: {self.message}"

    @property
    def blocking(self) -> bool:
        """Safety rules reject; a style note (repetition) is fed back but rejects nothing."""
        return self.rule != STYLE


@dataclass
class Report:
    errors: list[Error] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """No safety error (style notes do not count)."""
        return not any(e.blocking for e in self.errors)

    def sections_failed(self) -> list[str]:
        return list(dict.fromkeys(e.section for e in self.errors if e.blocking))

    def for_section(self, section: str) -> list[Error]:
        return [e for e in self.errors if e.section == section]


# --- Reading the form ----------------------------------------------------------------------


def parse_sections(data: dict) -> tuple[Draft, list[Error]]:
    """The filled form -> Draft. Lines that break the form's shape become "form" errors."""
    sections, errors = {}, []
    for name, sentences in (data or {}).items():
        out = []
        if not isinstance(sentences, list):
            errors.append(Error(name, None, "form", "expected a list of sentences"))
            sections[name] = out
            continue
        for n, raw in enumerate(sentences, start=1):
            if not isinstance(raw, dict) or not isinstance(raw.get("text"), str):
                errors.append(Error(name, n, "form", "each sentence needs a text"))
                continue
            refs = []
            for ref in raw.get("facts") or []:
                if not isinstance(ref, dict) or not isinstance(ref.get("id"), str):
                    errors.append(Error(name, n, "form", f"malformed fact entry: {ref!r}"))
                    continue
                claims = ref.get("claims") or []
                if isinstance(claims, str):
                    claims = [claims]
                refs.append(Ref(ref["id"].strip(), tuple(str(c) for c in claims)))
            out.append(Sentence(raw["text"].strip(), tuple(refs)))
        sections[name] = out
    return Draft(sections), errors


# --- The verifier ----------------------------------------------------------------------------


class Verifier:
    def __init__(self, narrative: dict | None = None, vocabulary: dict | None = None):
        self.narrative = narrative or load_narrative()
        voc = vocabulary or yaml.safe_load(VOCABULARY.read_text())
        names = "|".join(f"(?:{p})" for p in self.narrative["allowed_names"])
        self.allowed = re.compile(rf"\bFY{YEAR}\b|\b{YEAR}\b|(?<![\w.]){names}(?![\w])", re.I)
        self.number_words = re.compile(
            r"\b(?:" + "|".join(f"(?:{w})" for w in voc["number_words"]) + r")\b", re.I
        )
        self.allowed_phrases = re.compile(
            r"\b(?:" + "|".join(voc["allowed_phrases"]) + r")\b", re.I
        )
        self.symbols = re.compile(voc["symbols"])
        self.figure_words = re.compile(rf"\b(?:{voc['figure_words']})\b", re.I)
        self.ignored = re.compile(r"\b(?:" + "|".join(voc["ignored_phrases"]) + r")\b", re.I)
        self.directions = {
            name: (re.compile(rf"\b(?:{d['words']})\b", re.I), tuple(d["claims"]))
            for name, d in voc["directions"].items()
        }

    def check(
        self,
        sheet: FactSheet,
        draft: Draft,
        sections: list[str] | None = None,
        others: dict[str, list[Sentence]] | None = None,
    ) -> Report:
        """Check the draft's `sections` (all sections of config/narrative.yaml by default).
        `others`: the note's sections already accepted, counted for repeated figures."""
        expected = self.narrative["sections"]
        wanted = sections or list(expected)
        report = Report()
        first_use: dict[str, str] = {}
        for other, sentences in (others or {}).items():
            if other in SUMMARY_SECTIONS:
                continue
            for n, sentence in enumerate(sentences, start=1):
                for fid in self.counted(sheet, sentence):
                    first_use.setdefault(fid, f"{other}, sentence {n}")
        for name in draft.sections:
            if name not in expected:
                report.errors.append(Error(name, None, "form", "not a drafted section"))
        for name in wanted:
            sentences = draft.sections.get(name)
            if sentences is None:
                report.errors.append(Error(name, None, "form", "section missing"))
                continue
            low, high = expected[name]["sentences"]
            if not low <= len(sentences) <= high:
                span = f"exactly {low}" if low == high else f"{low} to {high}"
                report.errors.append(
                    Error(name, None, "form", f"{len(sentences)} sentences; needs {span}")
                )
            for n, sentence in enumerate(sentences, start=1):
                for rule, message in self.check_sentence(sheet, sentence):
                    report.errors.append(Error(name, n, rule, message))
                if name in SUMMARY_SECTIONS:
                    continue
                for fid in self.counted(sheet, sentence):
                    where = f"{name}, sentence {n}"
                    if fid in first_use and not first_use[fid].startswith(f"{name},"):
                        report.errors.append(Error(name, n, STYLE, (
                            f"{fid} is already given in {first_use[fid]}: give each figure in "
                            "one body section only (the snapshot and watch items may restate it)"
                        )))  # fmt: skip
                    first_use.setdefault(fid, where)
        return report

    @staticmethod
    def counted(sheet: FactSheet, s: Sentence) -> list[str]:
        """The figures of a sentence that count towards repetition (not events)."""
        return [
            fid
            for fid in dict.fromkeys(m.group(1) for m in PLACEHOLDER.finditer(s.text))
            if fid in sheet.items and sheet.items[fid].kind != "event"
        ]

    def check_sentence(self, sheet: FactSheet, s: Sentence) -> list[tuple[str, str]]:
        errors: list[tuple[str, str]] = []
        used = [m.group(1) for m in PLACEHOLDER.finditer(s.text)]
        prose = PLACEHOLDER.sub(" ", s.text)
        # Rule 2: blanks (and listed ids) must be items of the fact sheet
        if "{" in prose or "}" in prose:
            errors.append(("2", "a blank is malformed: write it as {{id}}"))
        for fid in dict.fromkeys(used + [r.id for r in s.facts]):
            if fid in sheet.items:
                continue
            if fid in sheet.unavailable:
                errors.append(("2", f"{fid} is not available ({sheet.unavailable[fid]})"))
            else:
                errors.append(("2", f"{fid} is not in the fact sheet"))
        # Rule 1: no number outside a blank
        errors += [("1", m) for m in self.numbers(prose)]
        # Rule 5: the form and the sentence list the same ids
        listed = [r.id for r in s.facts]
        for fid in dict.fromkeys(used):
            if fid not in listed:
                errors.append(("5", f"{fid} is in the text but not listed in the form"))
        for fid in dict.fromkeys(listed):
            if fid not in used and not fid.startswith(EVENT):
                errors.append(("5", f"{fid} is listed in the form but not used in the text"))
        for fid in dict.fromkeys(used):
            if fid.startswith(EVENT):
                errors.append(("5", f"{fid} is an event, not a figure: list it, no blank"))
        # Rule 6: a figure from an earlier year, used on its own, names its year
        current = f"FY{sheet.fiscal_year}"
        for fid in dict.fromkeys(used):
            item = sheet.items.get(fid)
            if item is None or item.kind != "value" or item.period == current:
                continue
            same = [
                sheet.items[u]
                for u in used
                if u in sheet.items
                and sheet.items[u].metric == item.metric
                and sheet.items[u].kind in ("value", "change")
                and sheet.items[u].period != item.period
            ]
            year = item.period.removeprefix("FY")
            if not same and not re.search(rf"\b(?:FY)?{year}\b", prose):
                errors.append(("6", (
                    f"{fid} is a {item.period} figure: say so in the sentence "
                    f"('in {item.period}'), or pair it with the {current} figure"
                )))  # fmt: skip
        # Rule 3: each claim against the computed direction
        for ref in s.facts:
            for claim in ref.claims:
                message = self.claim_error(sheet, ref.id, claim)
                if message:
                    errors.append(("3", message))
        # Rule 4: direction words in the prose need a matching claim
        errors += [("4", m) for m in self.direction_words(sheet, s)]
        return errors

    # --- rule 1
    def numbers(self, prose: str) -> list[str]:
        out = []
        text = self.allowed.sub(" ", prose)
        for token in re.findall(r"\S*\d\S*", text):
            out.append(f"number written outside a blank: '{token.strip('.,;:')}'")
        for sym in self.symbols.findall(text):
            out.append(f"symbol written outside a blank: '{sym}'")
        words = self.allowed_phrases.sub(" ", text)
        for word in self.number_words.findall(words):
            out.append(f"word that states a number: '{word}'")
        return out

    # --- rule 3
    @staticmethod
    def claim_error(sheet: FactSheet, fid: str, claim: str) -> str | None:
        if claim not in CLAIMS:
            return f"unknown claim '{claim}' on {fid}"
        item = sheet.items.get(fid)
        if item is None:
            return None  # reported under rule 2
        if claim in ("up", "down", "flat"):
            if item.direction is None:
                return (
                    f"'{claim}' claimed on {fid}, which has no computed direction "
                    "(use the current-year figure or its .change)"
                )
            if item.direction != claim:
                return f"'{claim}' claimed on {fid}, but it moved {item.direction}"
        elif claim in ("better", "worse"):
            if item.assessment is None:
                return f"'{claim}' claimed on {fid}, which has no computed direction"
            if item.assessment != claim:
                what = {"neutral": "neither better nor worse"}.get(item.assessment, "")
                return f"'{claim}' claimed on {fid}, but it is {what or item.assessment}"
        elif claim in ("above_peers", "below_peers", "in_line_with_peers"):
            side = claim.removesuffix("_peers").removesuffix("_with")
            if item.vs_peers is None:
                return f"'{claim}' claimed on {fid}, which has no peer comparison"
            if item.vs_peers != side:
                return f"'{claim}' claimed on {fid}, but it is {item.vs_peers.replace('_', ' ')}"
        elif claim in ("better_than_peers", "worse_than_peers"):
            side = claim.removesuffix("_than_peers")
            if item.peer_assessment is None:
                return f"'{claim}' claimed on {fid}, which has no peer comparison"
            if item.peer_assessment != side:
                return (
                    f"'{claim}' claimed on {fid}, but against peers it is "
                    f"{item.peer_assessment.replace('_', ' ')}"
                )
        else:  # best_in_group, worst_in_group
            if item.kind != "peer_rank":
                return f"'{claim}' needs the rank id (.peer_rank), not {fid}"
            target = 1 if claim == "best_in_group" else item.rank_of
            if item.rank != target:
                return f"'{claim}' claimed on {fid}, but the rank is {item.rendered}"
        return None

    # --- rule 4
    def direction_words(self, sheet: FactSheet, s: Sentence) -> list[str]:
        """Each direction word must be backed by a matching claim on a figure of its clause.
        A clause's figures include the sentence's other figures for the same metric: in
        "FCF to debt rose to {{a}}, below the median of {{b}}", "below" may rest on {{a}}."""
        claims = {r.id: set(r.claims) for r in s.facts}
        cites_event = any(r.id.startswith(EVENT) for r in s.facts)
        text = PLACEHOLDER.sub(lambda m: f" \u27e6{m.group(1)}\u27e7 ", s.text)
        text = self.ignored.sub(" ", text)
        out = []
        for clause in _clauses(text):
            ids = re.findall(r"\u27e6([^\u27e7]*)\u27e7", clause)
            if not ids and HYPOTHETICAL.search(clause):
                continue  # "if bookings slow": a scenario, not a statement about a figure
            if not ids and cites_event and not self.figure_words.search(clause):
                continue  # describes a cited event ("Fitch upgraded"), names no figure
            metrics = {_metric(sheet, fid) for fid in ids}
            scope = [f for f in claims if f in ids or _metric(sheet, f) in metrics] or list(claims)
            words_text = re.sub(r"\u27e6[^\u27e7]*\u27e7", " ", clause)
            for name, (pattern, backing) in self.directions.items():
                for word in pattern.findall(words_text):
                    backed = [f for f in scope if claims.get(f, set()) & set(backing)]
                    if name == "extreme":
                        fits = [f for f in backed if _extreme_ok(sheet, f, word, claims[f])]
                        if backed and not fits:
                            out.append(_extreme_message(sheet, backed[0], word))
                            continue
                        backed = fits
                    if not backed:
                        need = " or ".join(f"'{c}'" for c in backing)
                        out.append(f"'{word}' needs a {need} claim on a figure in the same clause")
        return out


def _metric(sheet: FactSheet, fid: str) -> str:
    item = sheet.items.get(fid)
    return item.metric if item else fid.split("@")[0].split(".")[0]


def _extreme_message(sheet: FactSheet, fid: str, word: str) -> str:
    item = sheet.items.get(fid)
    better = sheet.higher_is_better.get(item.metric) if item else None
    if item is None or better is None:
        return f"'{word}' cannot be checked on {fid}"
    rule = "higher is better" if better else "lower is better"
    side = "highest" if better else "lowest"
    return (
        f"'{word}' does not fit {fid} ({item.rendered}): for {sheet.labels.get(item.metric)} "
        f"{rule}, so 1st is the {side}"
    )


def _clauses(text: str) -> list[str]:
    return [c for c in CLAUSE_BREAK.split(text) if c and c.strip()]


def _extreme_ok(sheet: FactSheet, fid: str, word: str, claims: set[str]) -> bool:
    """'lowest' means best only where lower is better (leverage), worst where higher is."""
    item = sheet.items.get(fid)
    if item is None:
        return False
    better = sheet.higher_is_better.get(item.metric)
    low = word.lower() in ("lowest", "smallest")
    if better is None:
        return False
    best_means_low = not better
    if "best_in_group" in claims and low == best_means_low:
        return True
    return "worst_in_group" in claims and low != best_means_low
