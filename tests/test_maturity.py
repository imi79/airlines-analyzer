"""The maturity wall (M8): column labels read by code, the checks on each table, the buckets.

The example report (FY2025, year end 31 December 2025) prints:

    Maturity of borrowings (€ million)
    Less than 1 year 1-2 years 2-5 years More than 5 years Total
    Bonds and bank loans 500 700 1,800 1,000 4,000

and the balance sheet shows current borrowings of 510 and total borrowings of 4,050.
"""

from datetime import date
from decimal import Decimal

import pytest

from tearsheet.config import Issuer
from tearsheet.extract.documents import Document
from tearsheet.extract.grounding import DocumentIndex
from tearsheet.extract.maturity import (
    RawCell,
    RawRow,
    RawTable,
    Span,
    check_table,
    covers_everything,
    load_config,
    parse_label,
    parse_labels,
    standard_buckets,
)

DEC = date(2025, 12, 31)
D = Decimal


@pytest.mark.parametrize(
    "label, start, end",
    [
        ("Less than 1 year", 0, 1),
        ("Within one year", 0, 1),
        ("Less than one year", 0, 1),
        ("< 1 year", 0, 1),
        ("1-2 years", 1, 2),
        ("One to two years", 1, 2),
        ("Between 1 and 2 years", 1, 2),
        ("2-5 years", 2, 5),
        ("Two to five years", 2, 5),
        ("More than 5 years", 5, None),
        ("Over five years", 5, None),
        ("5+ years", 5, None),
        ("+5 years", 5, None),
        ("Moins d'un an", 0, 1),
        ("De 1 à 5 ans", 1, 5),
        ("Plus de 5 ans", 5, None),
        ("Menos de 1 año", 0, 1),
        ("Más de 5 años", 5, None),
        ("bis 1 Jahr", 0, 1),
        ("1 bis 5 Jahre", 1, 5),
        ("über 5 Jahre", 5, None),
        ("less than 12 months", 0, 1),
        ("13–24 months", D(13) / 12, 2),
        ("2026", 0, 1),
        ("2027", 1, 2),
        ("2031 and after", 5, None),
        ("Beyond 2030", 5, None),
        ("Au-delà de 2030", 5, None),
        ("N+1", 0, 1),
        ("Y+2", 1, 2),
        ("N+2 à N+5", 1, 5),
        ("Au-delà de N+5", 5, None),
        ("Au delà de 5 ans", 5, None),
    ],
)
def test_column_labels_are_read_by_code(label, start, end):
    span = parse_label(label, DEC)
    assert span is not None, label
    assert span.start == D(start)
    assert span.end == (None if end is None else D(end))


@pytest.mark.parametrize("label", ["Total", "Current", "Fair value", "Nominal", "1 234"])
def test_labels_that_are_not_time_spans_are_refused(label):
    assert parse_label(label, DEC) is None


def test_calendar_year_columns_need_a_december_year_end():
    assert parse_label("2027", date(2026, 3, 31)) is None


def test_columns_must_cover_the_whole_debt():
    ok = [Span(D(0), D(1)), Span(D(1), D(5)), Span(D(5), None)]
    assert covers_everything(ok) is None
    assert "gap" in covers_everything([Span(D(0), D(1)), Span(D(2), None)])
    assert "missing" in covers_everything([Span(D(0), D(1)), Span(D(1), D(5))])
    assert "start" in covers_everything([Span(D(1), D(5)), Span(D(5), None)])


def test_narrow_columns_add_into_standard_buckets():
    columns = [
        (Span(D(0), D(1)), D(10)),
        (Span(D(1), D(2)), D(20)),
        (Span(D(2), D(3)), D(30)),
        (Span(D(3), D(4)), D(40)),
        (Span(D(4), D(5)), D(50)),
        (Span(D(5), None), D(60)),
    ]
    assert standard_buckets(columns, [0, 1, 2, 5]) == [
        (D(0), D(1), D(10)),
        (D(1), D(2), D(20)),
        (D(2), D(5), D(120)),
        (D(5), None, D(60)),
    ]


def test_a_wide_column_merges_the_buckets_it_spans():
    columns = [(Span(D(0), D(1)), D(10)), (Span(D(1), D(5)), D(90)), (Span(D(5), None), D(5))]
    assert standard_buckets(columns, [0, 1, 2, 5]) == [
        (D(0), D(1), D(10)),
        (D(1), D(5), D(90)),
        (D(5), None, D(5)),
    ]


ISSUER = Issuer(
    id="abc",
    name="Example Air",
    type="airline",
    lei="X",
    currency="EUR",
    fiscal_year_end="12-31",
    country="FR",
    status="v1",
)
CAPTION = "Maturity of borrowings (€ million)"
HEADER = "Less than 1 year 1-2 years 2-5 years More than 5 years Total"
ROW = "Bonds and bank loans 500 700 1,800 1,000 4,000"
PAGE = f"Note 20 Borrowings\n{CAPTION}\n{HEADER}\n{ROW}\nAt 31 December 2024 the debt was lower."
DOC = Document("R1", "abc", 2025, "en", "test", "test", None, ("Intro", PAGE), "page")
TAGGED = {"current": D(510_000_000), "total": D(4_050_000_000)}


def table(**changes):
    values = [("Less than 1 year", "500"), ("1-2 years", "700"), ("2-5 years", "1,800"),
              ("More than 5 years", "1,000")]  # fmt: skip
    data = {
        "layer": "borrowings",
        "basis": "principal",
        "fiscal_year": 2025,
        "caption": CAPTION,
        "header": HEADER,
        "scale": "million",
        "currency": "EUR",
        "rows": [
            RawRow(
                name="Bonds and bank loans",
                columns=[RawCell(label=k, printed_value=v, quote=ROW) for k, v in values],
                total=RawCell(label="Total", printed_value="4,000", quote=ROW),
            )
        ],
    }
    data.update(changes)
    return RawTable(**data)


def check(raw, tagged=TAGGED):
    return check_table(raw, DocumentIndex(DOC), ISSUER, DEC, tagged, load_config())


def test_a_correct_table_is_verified_and_bucketed():
    t = check(table())
    assert t.verified, t.failures
    assert t.total == D(4_000_000_000)
    assert [b[2] for b in t.buckets] == [D(500e6), D(700e6), D(1800e6), D(1000e6)]


def test_a_value_not_in_the_quote_is_rejected():
    raw = table()
    raw.rows[0].columns[1] = RawCell(label="1-2 years", printed_value="750", quote=ROW)
    t = check(raw)
    assert not t.verified
    assert any("750 is not printed" in f for f in t.failures)


def test_a_table_that_does_not_foot_is_rejected():
    raw = table()
    raw.rows[0].columns[3] = RawCell(label="More than 5 years", printed_value="1,800", quote=ROW)
    t = check(raw)
    assert any("add up to" in f for f in t.failures)


def test_a_missing_column_is_rejected():
    raw = table()
    raw.rows[0].columns.pop()
    t = check(raw)
    assert any("debt beyond is missing" in f for f in t.failures)


def test_disagreement_with_the_balance_sheet_is_rejected():
    t = check(table(), {"current": D(900_000_000), "total": D(4_050_000_000)})
    assert any("does not agree with the current borrowings" in f for f in t.failures)
    t = check(table(), {"current": D(510_000_000), "total": D(6_000_000_000)})
    assert any("table total" in f for f in t.failures)


def test_without_tagged_debt_the_table_stays_unverified():
    t = check(table(), {"current": None, "total": None})
    assert any("no tagged" in f for f in t.failures)


def test_the_prior_year_table_is_refused():
    t = check(table(fiscal_year=2024))
    assert not t.verified and "only the report's own year end" in t.failures[0]


def test_a_quote_not_in_the_report_is_rejected():
    raw = table()
    raw.rows[0].columns[0] = RawCell(label="Less than 1 year", printed_value="500",
                                     quote="Bonds 500 700")  # fmt: skip
    t = check(raw)
    assert any("not found word for word" in f for f in t.failures)


def test_a_label_the_code_cannot_read_is_rejected():
    raw = table()
    raw.rows[0].columns[0] = RawCell(label="Bonds and bank loans", printed_value="500", quote=ROW)
    t = check(raw)
    assert any("cannot read the label" in f for f in t.failures)


def test_contractual_cash_flows_may_exceed_the_debt_by_interest():
    raw = table(basis="contractual_cash_flows")
    t = check(raw, {"current": D(480_000_000), "total": D(3_900_000_000)})
    assert t.verified, t.failures
    t = check(raw, {"current": D(600_000_000), "total": D(3_900_000_000)})  # 500 < 90% of 600
    assert any("with interest" in f for f in t.failures)


def test_a_transposed_table_takes_the_fiscal_year_column():
    page = (
        "Maturity of lease liabilities € million\n2025 2024\nWithin one year 6 2\n"
        "One to two years 5 6\nTwo to five years 3 –\nMore than five years – –\nTotal 14 8"
    )
    doc = Document("R2", "abc", 2025, "en", "t", "t", None, (page,), "page")

    def cell(label, value, row):
        return RawCell(label=label, printed_value=value, quote=row)

    raw = RawTable(
        layer="leases",
        basis="contractual_cash_flows",
        fiscal_year=2025,
        caption="Maturity of lease liabilities € million",
        header="2025 2024",
        scale="million",
        currency="EUR",
        rows=[
            RawRow(
                name="Lease liabilities",
                columns=[
                    cell("Within one year", "6", "Within one year 6 2"),
                    cell("One to two years", "5", "One to two years 5 6"),
                    cell("Two to five years", "3", "Two to five years 3 –"),
                    cell("More than five years", "–", "More than five years – –"),
                ],
                total=cell("Total", "14", "Total 14 8"),
            )
        ],
    )
    ok = check_table(raw, DocumentIndex(doc), ISSUER, DEC,
                     {"current": D(5_500_000), "total": D(12_000_000)}, load_config())  # fmt: skip
    assert ok.verified, ok.failures
    wrong = raw.model_copy(deep=True)
    wrong.rows[0].columns[0] = cell("Within one year", "2", "Within one year 6 2")
    bad = check_table(wrong, DocumentIndex(doc), ISSUER, DEC,
                      {"current": D(5_500_000), "total": D(12_000_000)}, load_config())  # fmt: skip
    assert any("ties the value to 2024" in f for f in bad.failures)


def test_a_layer_printed_in_several_rows_is_added_up_by_code():
    page = (
        "Liquidity risk € million\nWithin 1 year 1-2 years 2-5 years More than 5 years Total\n"
        "Bank loans (100) (50) (200) – (350)\nBonds (10) (300) (400) (500) (1,210)"
    )
    doc = Document("R3", "abc", 2025, "en", "t", "t", None, (page,), "page")
    header = "Within 1 year 1-2 years 2-5 years More than 5 years Total"

    def row(name, quote, values, total):
        labels = ["Within 1 year", "1-2 years", "2-5 years", "More than 5 years"]
        cells = [
            RawCell(label=k, printed_value=v, quote=quote)
            for k, v in zip(labels, values, strict=True)
        ]
        return RawRow(name=name, columns=cells,
                      total=RawCell(label="Total", printed_value=total, quote=quote))  # fmt: skip

    raw = RawTable(
        layer="borrowings", basis="principal", fiscal_year=2025, caption="Liquidity risk € million",
        header=header, scale="million", currency="EUR",
        rows=[row("Bank loans", "Bank loans (100) (50) (200) – (350)",
                  ["(100)", "(50)", "(200)", "–"], "(350)"),
              row("Bonds", "Bonds (10) (300) (400) (500) (1,210)",
                  ["(10)", "(300)", "(400)", "(500)"], "(1,210)")],
    )  # fmt: skip
    tagged = {"current": D(110_000_000), "total": D(1_560_000_000)}
    t = check_table(raw, DocumentIndex(doc), ISSUER, DEC, tagged, load_config())
    assert t.verified, t.failures
    assert t.total == D(1_560_000_000)
    assert [b[2] for b in t.buckets] == [D(110e6), D(350e6), D(600e6), D(500e6)]


def test_later_starts_where_the_column_before_ends():
    labels = ["2026", "2027", "2028", "2029", "2030", "Later"]
    spans = parse_labels(labels, DEC)
    assert spans[0] == Span(D(0), D(1))
    assert spans[4] == Span(D(4), D(5))
    assert spans[5] == Span(D(5), None)
    assert parse_labels(["Later"], DEC) == [None]
    assert parse_labels(["2030", "Siguientes"], DEC)[1] == Span(D(5), None)


def test_an_approved_table_is_shown_with_its_failed_checks_kept():
    from tearsheet.extract.maturity import MaturityRun, apply_reviews

    t = check(table(), {"current": D(900_000_000), "total": D(4_050_000_000)})
    assert not t.verified and t.status == "unverified"
    run = MaturityRun(DOC, tables=[t])
    review = {"issuer": "abc", "fiscal_year": 2025, "item": "maturity_borrowings",
              "action": "approve", "by": "Imane", "on": "2026-11-12",
              "reason": "checked"}  # fmt: skip
    apply_reviews(ISSUER, run, [review])
    assert t.status == "verified" and t.failures  # shown, the failed check still on record
    assert any("approved by Imane" in n for n in t.notes)
    other = {**review, "fiscal_year": 2024}
    t2 = check(table(), {"current": D(900_000_000), "total": D(4_050_000_000)})
    apply_reviews(ISSUER, MaturityRun(DOC, tables=[t2]), [other])
    assert t2.status == "unverified"


def test_the_review_date_survives_yaml(tmp_path):
    from tearsheet.extract.consolidate import load_reviews

    path = tmp_path / "reviews.yaml"
    path.write_text("reviews:\n  - issuer: iag\n    on: 2026-11-12\n    by: Imane\n")
    assert str(load_reviews(path)[0]["on"]) == "2026-11-12"
