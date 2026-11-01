"""Read numbers, scale words and years in report text, in English, French, Spanish and German.

Used by the grounding checks to confirm, in code, what the AI says it read.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

SPACES = "     "  # normal, no-break, narrow no-break, thin, figure space

# A number as printed: digits, thousands separators used consistently, optional decimals.
# Separators depend on the report language (a space separates thousands in French, but
# separates table columns in English).
_SEPARATORS = {
    "en": (",", "."),
    "fr": ("    .", ","),
    "es": (".  ", ","),
    "de": (".  '", ","),
}


def _number_pattern(language: str | None) -> re.Pattern:
    thousands, decimal = _SEPARATORS.get(language or "en", _SEPARATORS["en"])
    sep = re.escape(thousands)
    return re.compile(
        rf"(?<![\w.,])(?:\d{{1,3}}(?:([{sep}])\d{{3}})(?:\1\d{{3}})*|\d+)"
        rf"(?:[{re.escape(decimal)}]\d+)?(?![\w]|[.,]\d)"
    )


NUMBER_PATTERNS = {lang: _number_pattern(lang) for lang in _SEPARATORS}

SCALE_FACTORS = {
    "one": Decimal(1),
    "thousand": Decimal(1_000),
    "million": Decimal(1_000_000),
    "billion": Decimal(1_000_000_000),
}

# Words that show a scale, by scale. Matched case-insensitively, spaces ignored.
SCALE_WORDS = {
    "thousand": [
        "thousand",
        "'000",
        "’000",
        "‘000",
        "000s",
        "(000)",
        "milliers",
        "miles",
        "tausend",
        "tsd",
        "teur",
        "k€",
        "keur",
    ],
    "million": [
        "million",
        "millions",
        "mn",
        "€m",
        "£m",
        "$m",
        "eurm",
        "gbpm",
        "usdm",
        "nokm",
        "m€",
        "meur",
        "millones",
        "mio",
        "mill",
        "(m)",
        "m.",
        " m ",
    ],
    "billion": [
        "billion",
        "bn",
        "milliard",
        "milliards",
        "mrd",
        "md€",
        "md",
        "mil millones",
        "€bn",
        "£bn",
        "$bn",
    ],
}

CURRENCY_WORDS = {
    "EUR": ["€", "eur", "euro"],
    "GBP": ["£", "gbp", "sterling", "pound"],
    "USD": ["$", "usd", "us dollar", "dollar"],
    "NOK": ["nok", "kroner", "norwegian krone"],
}

PERCENT_WORDS = ["%", "per cent", "percent", "pour cent", "por ciento", "prozent", "pct"]

# Years: 2025, FY2025, FY25, F25, 2024/25, 2024-25.
YEAR = re.compile(
    r"(?<![\d])(?:(?:FY|F|H[12]\s?FY|Q[1-4]\s?)?(20[12]\d)(?:\s?[/-]\s?(\d{2}))?|"
    r"(?:FY|F)\s?'?(\d{2}))(?![\d])"
)


def squash(text: str) -> str:
    """Text without any whitespace, lower case, with typographic quotes unified: the form in
    which quotes are compared (some reports split words, e.g. 'tr affic')."""
    text = text.replace("’", "'").replace("‘", "'").replace("`", "'")
    text = text.replace("–", "-").replace("—", "-").replace("−", "-")
    return re.sub(r"\s+", "", text).lower()


@dataclass(frozen=True)
class Token:
    text: str  # as printed
    value: Decimal
    start: int
    end: int


def parse_number(printed: str, language: str | None) -> Decimal | None:
    """'134,451' (en) -> 134451; '107,0' (fr) -> 107.0; '1.405,5' (de/es) -> 1405.5;
    '1 405' (fr) -> 1405. Returns None if the text is not a single number."""
    s = printed.strip().strip("%").strip()
    for ch in SPACES:
        s = s.replace(ch, "")
    s = s.replace("'", "").replace("’", "")
    if not s or not re.fullmatch(r"[\d.,]+", s) or not s[0].isdigit() or not s[-1].isdigit():
        return None
    comma_decimal = language in ("fr", "es", "de", "it", "pt", "nl", "fi", "no")
    if "," in s and "." in s:
        # whichever separator comes last is the decimal mark
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        parts = s.split(",")
        groups_of_three = len(parts) > 1 and all(len(p) == 3 for p in parts[1:])
        if comma_decimal and not (len(parts) > 2 and groups_of_three):
            s = s.replace(",", ".") if len(parts) == 2 else s
        elif groups_of_three:
            s = s.replace(",", "")
        elif len(parts) == 2:
            s = s.replace(",", ".")
    elif "." in s:
        parts = s.split(".")
        groups_of_three = len(parts) > 1 and all(len(p) == 3 for p in parts[1:])
        if len(parts) > 2 and groups_of_three:
            s = s.replace(".", "")
        elif comma_decimal and groups_of_three and len(parts) == 2:
            s = s.replace(".", "")  # '1.405' in a German or Spanish report is 1405
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def number_tokens(text: str, language: str | None) -> list[Token]:
    tokens = []
    pattern = NUMBER_PATTERNS.get(language or "en", NUMBER_PATTERNS["en"])
    for match in pattern.finditer(text):
        printed = match.group(0)
        value = parse_number(printed, language)
        if value is not None:
            tokens.append(Token(printed, value, match.start(), match.end()))
    return tokens


def decimals_of(printed: str, language: str | None, scale: str) -> int:
    """XBRL-style decimals for a printed figure: '37.6' billion -> -8; '134,451' million -> -6."""
    value = parse_number(printed, language)
    if value is None:
        return 0
    exponent = value.normalize().as_tuple().exponent if value != value.to_integral() else 0
    places = -int(exponent) if exponent < 0 else 0
    shift = {"one": 0, "thousand": 3, "million": 6, "billion": 9}[scale]
    return places - shift


@dataclass(frozen=True)
class YearMark:
    year: int
    start: int
    end: int


def year_marks(text: str) -> list[YearMark]:
    marks = []
    for m in YEAR.finditer(text):
        if m.group(1):
            year = int(m.group(1))
            if m.group(2):  # 2024/25 -> the year the period ends
                year = 2000 + int(m.group(2))
        else:
            year = 2000 + int(m.group(3))
        if 2015 <= year <= 2030:
            marks.append(YearMark(year, m.start(), m.end()))
    return marks


def contains_any(text: str, words: list[str]) -> bool:
    flat = squash(text)
    return any(squash(w) in flat for w in words if squash(w))


def scale_words_near(text: str, end: int, window: int = 18) -> set[str]:
    """Scales named right after a number ('134,451 million', '37.6bn', '2,5 Mrd.')."""
    after = text[end : end + window].lower()
    found = set()
    for scale, words in SCALE_WORDS.items():
        for w in words:
            w = w.lower().strip()
            if not w or w in ("m.", "(m)"):
                continue
            pattern = rf"^[\s  ]*(?:de\s|d')?{re.escape(w)}(?![a-zà-ÿ])"
            if re.search(pattern, after):
                found.add(scale)
    if re.match(r"^[\s ]*m(?![a-zà-ÿ])", after):
        found.add("million")
    if re.match(r"^[\s ]*k(?![a-zà-ÿ])", after):
        found.add("thousand")
    return found


def scale_named(text: str, scale: str) -> bool:
    """True if the text names this scale anywhere (column headers: '(’000 km)', 'en millions')."""
    if scale == "one":
        return True
    lowered = text.lower()
    for w in SCALE_WORDS[scale]:
        w = w.lower()
        if w.strip() in ("m", "(m)", "m.", "mn"):
            if re.search(r"(?<![a-zà-ÿ])(?:\(m\)|mn|m)(?![a-zà-ÿ])", lowered):
                return True
            continue
        if squash(w) and squash(w) in squash(text):
            return True
    return False
