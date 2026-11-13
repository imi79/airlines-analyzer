# ruff: noqa: E501  (the statement pages below are laid out as the reports print them)
"""Half-year statements (M10): reading rows, naming columns and the controls against the
database. No network and no AI call: the pages and the AI's answers are written here."""

from datetime import date
from decimal import Decimal

import pytest

from tearsheet.extract import half_year as h
from tearsheet.extract.documents import Document
from tearsheet.extract.half_year import RawComponent, RawLine

M = Decimal(1_000_000)
SETTINGS = h.load_settings()
REPORT = h.Report(
    "x-h1", "finnair", date(2026, 6, 30), 2025, "en", "Half-year report", "x.pdf", "0" * 64
)

INCOME = """CONSOLIDATED INCOME STATEMENT
EUR in millions                         Note   Q2 2026    Q2 2025     Q1-Q2 2026    Q1-Q2 2025      2025
Revenue                                   4      916.7      787.7        1,694.8       1,481.9    3,106.2
Fuel costs                                      -236.7     -227.4         -463.9        -441.1    -879.0
Depreciation and impairment               7      -83.7      -87.0         -170.1        -172.8    -343.7
Operating result                                  86.6       19.2           90.2         -34.2       64.2
Financial expenses                               -20.8      -21.4          -41.1         -44.8      -81.9
Result for the period                             58.4       12.5           49.2         -38.4       18.4
"""
BALANCE = """CONSOLIDATED BALANCE SHEET
EUR in millions                         Note    30 Jun 2026    30 Jun 2025    31 Dec 2025
Other financial assets                   10         1,017.8          592.7          531.4
Cash and cash equivalents                             234.2          174.7          529.6
Assets total                                        4,043.5        3,534.3        3,686.9
Equity total                                          810.0          550.6          636.7
Lease liabilities                        14           604.4          701.7          632.3
Other interest-bearing liabilities       14           958.3          684.5          968.6
Lease liabilities                        14           127.0          138.4          130.4
Other interest-bearing liabilities       14            21.2           56.9           51.5
Equity and liabilities total                        4,043.5        3,534.3        3,686.9
"""
CASH = """CONSOLIDATED CASH FLOW STATEMENT
EUR in millions                                Q2 2026    Q2 2025    Q1-Q2 2026    Q1-Q2 2025     2025
Net cash flow from operating activities          182.6       43.7         456.5         235.8    401.9
Investments in fleet                             -66.4      -68.6        -164.4        -118.2   -193.3
Investments in other fixed assets                 -5.2       -3.6          -8.9          -6.2    -15.7
Repayments of lease liabilities                  -33.6      -37.2         -66.3         -78.3   -150.4
Change in cash flows                            -122.2     -155.5        -141.6        -117.9    182.8
Liquid funds, at beginning                       807.2      681.4         826.7         643.8    643.8
Liquid funds, at end                             685.0      525.9         685.0         525.9    826.7
"""
HELD = {
    "revenue": Decimal("3106.2") * M,
    "fuel_cost": Decimal("879.0") * M,
    "dda": Decimal("343.7") * M,
    "operating_profit": Decimal("64.2") * M,
    "finance_costs": Decimal("81.9") * M,
    "profit": Decimal("18.4") * M,
    "cash": Decimal("529.6") * M,
    "other_current_financial_assets": Decimal("531.4") * M,
    "total_assets": Decimal("3686.9") * M,
    "equity": Decimal("636.7") * M,
    "borrowings_current": Decimal("51.5") * M,
    "borrowings_noncurrent": Decimal("968.6") * M,
    "lease_liabilities_current": Decimal("130.4") * M,
    "lease_liabilities_noncurrent": Decimal("632.3") * M,
    "cfo": Decimal("401.9") * M,
    "capex": Decimal("209.0") * M,
    "lease_payments": Decimal("150.4") * M,
}


def pad(page: str, rows: int = 14, cols: int = 5) -> str:
    """A statement page long enough to count as one (filler rows of amounts)."""
    amounts = "   ".join(f"{k}.0" for k in range(1, cols + 1))
    filler = "\n".join(f"Other row {n}                              {amounts}" for n in range(rows))
    return page + filler + "\n"


def doc(*pages: str, language: str = "en") -> Document:
    return Document(
        "x-h1",
        "finnair",
        2026,
        language,
        "half-year report (PDF)",
        "x.pdf",
        "0" * 64,
        tuple(pages),
        "page",
    )


def row(line: str, label: str, quote: str | None = None, operation: str = "add") -> RawLine:
    return RawLine(
        line=line, components=[RawComponent(label=label, quote=quote or label, operation=operation)]
    )


def run(lines, document=None, held=None, annual=(), report=REPORT):
    document = document or doc(pad(INCOME), pad(BALANCE), pad(CASH))
    regions = h.find_statements(document, SETTINGS)
    assert set(regions) == {"income", "balance", "cash_flow"}
    return h.check(
        report, document, regions, lines, HELD if held is None else held, list(annual), M, SETTINGS
    )


# --- Cells and rows ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text, language, value",
    [
        ("1,694.8", "en", "1694.8"),
        ("-34.2", "en", "-34.2"),
        ("(1 045)", "fr", "-1045"),
        ("3 215", "fr", "3215"),
        ("12.386.403", "es", "12386403"),
        ("–", "en", "0"),
        ("(3,887)", "en", "-3887"),
    ],
)
def test_parse_cell(text, language, value):
    assert h.parse_cell(text, language) == Decimal(value)


@pytest.mark.parametrize("text", ["4&8", "31,6 %", "Revenue", "13 & 28", ""])
def test_parse_cell_rejects_what_is_not_an_amount(text):
    assert h.parse_cell(text, "fr") is None


def test_value_cells_reads_the_amounts_at_the_end_of_a_row():
    line = "Revenue                                   4      916.7      787.7        1,694.8"
    assert [c.value for c in h.value_cells(line, "en")] == [
        4,
        Decimal("916.7"),
        Decimal("787.7"),
        Decimal("1694.8"),
    ]


def test_value_cells_french_thousands_are_one_amount():
    line = "Chiffre d'affaires                             4           3 215          3 163"
    assert [c.value for c in h.value_cells(line, "fr")] == [4, 3215, 3163]


def test_value_cells_two_amounts_one_space_apart():
    line = "Trade and other payables              (1,591) (1,654)"
    assert [c.value for c in h.value_cells(line, "en")] == [-1591, -1654]


def test_a_header_of_years_is_not_a_row():
    assert not h.is_value_row("€ million                         2026         2025", "en")
    assert h.is_value_row("Total revenue                    16,064       15,906", "en")


# --- Finding the statements --------------------------------------------------------------------


def test_statements_found_with_their_pages():
    regions = h.find_statements(doc("Cover page", pad(INCOME), pad(BALANCE), pad(CASH)))
    assert {k: r.page for k, r in regions.items()} == {"income": 1, "balance": 2, "cash_flow": 3}


def test_a_summary_in_the_management_report_is_not_the_statement():
    summary = pad(INCOME.replace("1,694.8", "9,999.9"))
    pages = [summary] + ["text"] * 12 + [pad(INCOME), pad(BALANCE), pad(CASH)]
    regions = h.find_statements(doc(*pages))
    assert regions["income"].page == 13


def test_table_of_contents_and_sentences_are_not_titles():
    assert not h._title_at("Consolidated income statement ........ 33", "income")
    assert not h._title_at("2.2.1   Consolidated income statement                 33", "income")
    assert not h._title_at("shown in the consolidated income statement.", "income")
    assert h._title_at("2.2.1              CONSOLIDATED INCOME STATEMENT", "income")
    assert h._title_at("Estado de situación financiera intermedio a 30 de junio de 2026", "balance")


def test_the_income_region_stops_at_the_statement_of_comprehensive_income():
    page = (
        INCOME
        + "CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME\n"
        + "Result for the period                             58.4       12.5           49.2"
        "         -38.4       18.4\n"
    )
    regions = h.find_statements(doc(pad(page), pad(BALANCE), pad(CASH)))
    texts = [t for _, _, t in regions["income"].lines]
    assert sum(t.startswith("Result for the period") for t in texts) == 1


# --- Which column is which ---------------------------------------------------------------------


def columns(page: str, kind: str = "income", report=REPORT, cols: int = 2):
    lines = pad(page, cols=cols).split("\n")
    region = h.Region(kind, 0, tuple((0, n, t) for n, t in enumerate(lines)))
    return h.flow_columns(region, report, SETTINGS)


def test_five_columns_quarter_half_and_full_year():
    c = columns(INCOME, cols=5)
    assert (c.count, c.current, c.prior, c.base) == (5, 2, 3, 4)


def test_two_columns_under_six_months():
    page = """CONSOLIDATED INCOME STATEMENT
                                          Six months to 30 June
€ million                                    2026         2025
Total revenue                              16,064       15,906
Operating profit                            1,608        1,878
"""
    c = columns(page)
    assert (c.count, c.current, c.prior, c.base) == (2, 0, 1, None)


def test_prior_year_first_is_read_from_the_header_not_assumed():
    page = """CONSOLIDATED INCOME STATEMENT
                                          Six months to 30 June
€ million                                    2025         2026
Total revenue                              15,906       16,064
"""
    c = columns(page)
    assert (c.current, c.prior) == (1, 0)


def test_three_columns_under_each_year_reads_the_total():
    page = """Condensed consolidated income statement (unaudited)
                                              Six months ended 31 March
                                        2026                                2025
                            Headline  Non-headline     Total    Headline  Non-headline     Total
Total revenue                  3,954             -     3,954       3,534             -     3,534
Other costs                    (396)             -     (396)       (316)           (7)     (323)
"""
    report = h.Report("e", "easyjet", date(2026, 3, 31), 2025, "en", "d", "f", "0")
    c = columns(page, report=report, cols=6)
    assert (c.count, c.current, c.prior) == (6, 2, 5)


def test_years_without_six_months_in_the_header_are_not_trusted():
    page = """CONSOLIDATED INCOME STATEMENT
€ million                                    2026         2025
Total revenue                              16,064       15,906
"""
    c = columns(page)
    assert c.current is None and c.failures


def test_quarter_columns_alone_do_not_pass_for_a_half_year():
    page = """CONSOLIDATED INCOME STATEMENT
€ million                                 Q2 2026      Q2 2025
Total revenue                              16,064       15,906
"""
    assert columns(page).current is None


def test_staggered_header_lines_are_ordered_left_to_right():
    gap = " " * 60
    page = "\n".join(
        [
            "Condensed consolidated interim statement of comprehensive income",
            "For the six months ended 30 September 2026 (unaudited)",
            f"{gap}                        Six months ended",
            f"{gap}                       30 September 2026      Six months ended",
            f"{gap}                                             30 September 2025",
            f"{gap}             Note              € million           € million",
            f"Total revenue{gap}6, 7                3,801.8             3,342.1",
            f"Fuel costs   {gap}                  (1,241.4)             (928.3)",
        ]
    )
    report = h.Report("w", "wizz", date(2026, 9, 30), 2026, "en", "d", "f", "0")
    region = h.Region("income", 0, tuple((0, n, x) for n, x in enumerate(page.split("\n"))))
    c = h.flow_columns(region, report, SETTINGS)
    assert (c.count, c.current, c.prior) == (2, 0, 1)


# --- The controls ------------------------------------------------------------------------------

FINNAIR_LINES = [
    row("revenue", "Revenue"),
    row("operating_profit", "Operating result"),
    row("dda", "Depreciation and impairment"),
    row("profit", "Result for the period"),
    row("cash", "Cash and cash equivalents"),
    row("other_current_financial_assets", "Other financial assets"),
    row("total_assets", "Assets total"),
    row("equity", "Equity total"),
    row("borrowings_noncurrent", "x", "Other interest-bearing liabilities 14 958.3 684.5 968.6"),
    row("borrowings_current", "x", "Other interest-bearing liabilities 14 21.2 56.9 51.5"),
    row("cfo", "Net cash flow from operating activities"),
    RawLine(
        line="capex",
        components=[
            RawComponent(label="Investments in fleet", quote="Investments in fleet"),
            RawComponent(
                label="Investments in other fixed assets", quote="Investments in other fixed assets"
            ),
        ],
    ),
    row("control_total_equity_and_liabilities", "Equity and liabilities total"),
    row("control_cash_start", "Liquid funds, at beginning"),
    row("control_cash_movements", "Change in cash flows"),
    row("control_cash_end", "Liquid funds, at end"),
]


def test_lines_verified_against_the_full_year_and_year_end_columns():
    r = run(FINNAIR_LINES)
    assert not r.statement_failures
    got = {x.line: x for x in r.lines}
    assert all(x.status == "verified" for x in r.lines if not x.line.startswith("control_"))
    assert got["revenue"].current == Decimal("1694.8") * M
    assert got["revenue"].prior == Decimal("1481.9") * M
    assert got["operating_profit"].prior == Decimal("-34.2") * M  # a loss keeps its sign
    assert got["dda"].current == Decimal("170.1") * M  # a cost is stored positive
    assert got["capex"].current == Decimal("173.3") * M  # two rows added
    assert got["capex"].base == Decimal("209.0") * M
    assert got["cash"].current == Decimal("234.2") * M and got["cash"].prior is None
    assert "full-year column" in got["revenue"].control
    assert "year-end column" in got["cash"].control


def test_the_same_label_twice_is_told_apart_by_the_quote():
    r = run(FINNAIR_LINES)
    got = {x.line: x for x in r.lines}
    assert got["borrowings_current"].current == Decimal("21.2") * M
    assert got["borrowings_noncurrent"].current == Decimal("958.3") * M


def test_a_wrong_row_is_flagged_with_both_values():
    lines = [x for x in FINNAIR_LINES if x.line != "revenue"] + [row("revenue", "Operating result")]
    r = run(lines)
    revenue = r.get("revenue")
    assert revenue.status == "unverified"
    assert "64.2" in revenue.failures[0] and "3,106.2" in revenue.failures[0]


def test_a_row_that_is_not_on_the_page_is_flagged():
    r = run(FINNAIR_LINES + [row("fuel_cost", "Jet fuel and oil")])
    fuel = r.get("fuel_cost")
    assert fuel.status == "unverified" and fuel.current is None
    assert "not found" in fuel.failures[0]


def test_a_line_the_database_does_not_hold_cannot_be_verified():
    held = {k: v for k, v in HELD.items() if k != "profit"}
    r = run(FINNAIR_LINES, held=held)
    assert r.get("profit").status == "unverified"


def test_no_year_end_column_agreeing_with_the_database_fails_the_balance_sheet():
    held = dict(HELD) | {
        k: HELD[k] + 7 * M
        for k in (
            "cash",
            "total_assets",
            "equity",
            "other_current_financial_assets",
            "borrowings_current",
            "borrowings_noncurrent",
        )
    }
    r = run(FINNAIR_LINES, held=held)
    assert r.columns["balance"].current is None
    assert r.get("cash").status == "unverified" and r.get("cash").current is None


def test_balance_sheet_that_does_not_add_up_is_flagged():
    broken = BALANCE.replace(
        "Equity and liabilities total                        4,043.5",
        "Equity and liabilities total                        4,143.5",
    )
    r = run(FINNAIR_LINES, doc(pad(INCOME), pad(broken), pad(CASH)))
    assert "balance" in r.statement_failures
    assert r.get("cash").status == "unverified"
    assert r.get("revenue").status == "verified"  # the other statements are not touched


def test_cash_flow_that_does_not_add_up_is_flagged():
    broken = CASH.replace("-141.6        -117.9    182.8", "-111.6        -117.9    182.8")
    r = run(FINNAIR_LINES, doc(pad(INCOME), pad(BALANCE), pad(broken)))
    assert "cash_flow" in r.statement_failures and r.get("cfo").status == "unverified"


TWO_COL_INCOME = """CONSOLIDATED INCOME STATEMENT
                                          Six months to 30 June
€ million                                    2026         2025
Total revenue                              16,064       15,906
Operating loss                              (533)        (376)
Loss for the period                         (377)        (297)
"""
ANNUAL = Document(
    "annual",
    "finnair",
    2025,
    "en",
    "filings.xbrl.org report",
    "u",
    None,
    (
        "Consolidated income statement Total revenue 33,213 32,100 Operating profit "
        "5,024 4,283 Profit for the year 3,342 2,732",
    ),
    "page",
)


def two_col(lines, annual=(ANNUAL,)):
    held = {
        "revenue": 33213 * M,
        "operating_profit": 5024 * M,
        "profit": 3342 * M,
        "cash": Decimal("529.6") * M,
    }
    return run(lines, doc(pad(TWO_COL_INCOME, cols=2), pad(BALANCE), pad(CASH)), held, annual)


def test_without_a_full_year_column_the_annual_report_label_confirms_the_row():
    r = two_col([row("revenue", "Total revenue")])
    revenue = r.get("revenue")
    assert revenue.status == "verified" and revenue.base is None
    assert "annual report" in revenue.control


def test_a_row_whose_label_does_not_carry_the_database_figure_is_flagged():
    r = two_col([row("revenue", "Operating loss")])
    assert r.get("revenue").status == "unverified"
    assert "cannot be confirmed" in r.get("revenue").failures[0]


def test_loss_for_the_period_matches_profit_for_the_year():
    r = two_col([row("operating_profit", "Operating loss"), row("profit", "Loss for the period")])
    assert r.get("operating_profit").status == "verified"
    assert r.get("operating_profit").current == -533 * M
    assert r.get("profit").status == "verified"


def test_the_figure_must_stand_right_after_the_label_not_some_rows_further():
    # "Total revenue" is followed, three amounts later, by the operating profit of 5,024.
    r = two_col([row("operating_profit", "Total revenue")])
    assert r.get("operating_profit").status == "unverified"


def test_a_label_that_only_starts_a_longer_label_does_not_confirm():
    annual = Document(
        "a",
        "finnair",
        2025,
        "en",
        "r",
        "u",
        None,
        ("Amortization, depreciation and provisions 3,054 2,643",),
        "page",
    )
    held = {"dda": 3054 * M}
    page = TWO_COL_INCOME + "Amortization                                1,641        1,564\n"
    document = doc(pad(page, cols=2), pad(BALANCE), pad(CASH))
    r = run([row("dda", "Amortization")], document, held, (annual,))
    assert r.get("dda").status == "unverified"
    full = page.replace("Amortization      ", "Amortization, depreciation and provisions")
    document = doc(pad(full, cols=2), pad(BALANCE), pad(CASH))
    r = run([row("dda", "Amortization, depreciation and provisions")], document, held, (annual,))
    assert r.get("dda").status == "verified"


def test_no_annual_report_no_confirmation():
    r = two_col([row("revenue", "Total revenue")], annual=())
    assert r.get("revenue").status == "unverified"


def test_borrowings_and_leases_printed_as_one_row_become_debt_including_leases():
    condensed = """Consolidated statement of financial position
(unaudited in NOK million)              Note     30 June 2026    30 June 2025   31 December 2025
Cash and cash equivalents                              234.2           174.7              529.6
Total assets                                         4,043.5         3,534.3            3,686.9
Total equity                                           810.0           550.6              636.7
Non-current debt                                     1,562.7         1,386.2            1,600.9
Current debt                                           148.2           195.3              181.9
"""
    lines = [
        row("cash", "Cash and cash equivalents"),
        row("total_assets", "Total assets"),
        row("equity", "Total equity"),
        row("borrowings_noncurrent", "Non-current debt"),
        row("borrowings_current", "Current debt"),
    ]
    r = run(lines, doc(pad(INCOME), pad(condensed, cols=3), pad(CASH)))
    debt = r.get("debt_including_leases")
    assert debt.status == "verified" and debt.current == Decimal("1710.9") * M
    assert r.get("borrowings_current") is None and "borrowings_current" in r.not_found


def test_facts_carry_the_period_the_rows_and_the_checks():
    r = run(FINNAIR_LINES)
    facts = h.to_facts(
        next(
            i
            for i in __import__("tearsheet.config", fromlist=["x"]).load_issuers()
            if i.id == "finnair"
        ),
        r,
    )
    revenue = {f.rule_source: f for f in facts if f.line == "revenue"}
    assert set(revenue) == {"H1", "H1_prior"}
    assert revenue["H1"].period_end == date(2026, 6, 30)
    assert revenue["H1_prior"].period_end == date(2025, 6, 30)
    assert revenue["H1"].ref["audit"] == "unaudited" and revenue["H1"].ref["quotes"]
    assert not any(f.line.startswith("control_") for f in facts)
    assert {f.rule_source for f in facts if f.line == "cash"} == {"H1"}


# --- Hand entries and reviews ------------------------------------------------------------------


def hand(tmp_path, reviewed="", cash_base=29777.2):
    path = tmp_path / "entries.yaml"
    path.write_text(f"""
entries:
  - report: v-h1
    reviewed_by: {reviewed}
    scale: 1000
    printed_unit: 0.1
    lines:
      revenue: [529349.8, 524442.5, null, 28, "Revenue"]
      cash: [16326.3, null, {cash_base}, 30, "Cash and cash equivalents"]
""")
    report = h.Report("v-h1", "vie", date(2026, 6, 30), 2025, "en", "d", "f", "0", read_by="hand")
    held = {"revenue": Decimal("1128950000"), "cash": Decimal("29777200")}
    return h.hand_run(report, held, SETTINGS, path)


def test_hand_entries_wait_for_review(tmp_path):
    r = hand(tmp_path)
    assert all(x.status == "unverified" for x in r.lines)
    assert r.get("cash").current == Decimal("16326300")
    assert "year-end column" in r.get("cash").control


def test_reviewed_hand_entries_are_verified(tmp_path):
    assert all(x.status == "verified" for x in hand(tmp_path, "Imane (2026-11-14)").lines)


def test_a_typing_error_shows_against_the_database(tmp_path):
    r = hand(tmp_path, "Imane (2026-11-14)", cash_base=29177.2)
    assert r.get("cash").status == "unverified" and r.get("revenue").status == "verified"


def test_reviews_approve_and_correct():
    r = two_col([row("revenue", "Operating loss"), row("operating_profit", "Total revenue")])
    reviews = [
        {
            "report": "x-h1",
            "line": "revenue",
            "action": "correct",
            "current": 16064,
            "prior": 15906,
            "by": "Imane",
            "on": "2026-11-14",
            "reason": "wrong row",
        },
        {
            "report": "x-h1",
            "line": "operating_profit",
            "action": "approve",
            "by": "Imane",
            "on": "2026-11-14",
            "reason": "checked",
        },
    ]
    h.apply_reviews(r, reviews)
    assert r.get("revenue").status == "overridden" and r.get("revenue").current == 16064 * M
    assert r.get("operating_profit").status == "verified"
    assert r.get("operating_profit").failures  # the failed check stays on record


# --- The register ------------------------------------------------------------------------------


def test_every_registered_report_is_in_the_repository_with_its_fingerprint():
    from tearsheet.extract.documents import file_sha256

    reports = h.load_reports()
    assert len(reports) == 9 and len({r.issuer for r in reports}) == 9
    for r in reports:
        assert file_sha256(h.DOCUMENT_DIR / r.file) == r.sha256
        assert r.audit == "unaudited"


def test_a_changed_file_is_refused(tmp_path):
    (tmp_path / "x.pdf").write_bytes(b"not the registered file")
    with pytest.raises(ValueError, match="fingerprint"):
        h.document(REPORT, tmp_path)


def test_period_labels():
    wizz = h.Report("w", "wizz", date(2026, 9, 30), 2026, "en", "d", "f", "0")
    assert (REPORT.ltm_label, wizz.ltm_label) == ("LTM Jun 2026", "LTM Sep 2026")
    assert wizz.prior_end == date(2025, 9, 30)


def test_the_prompt_of_the_version_in_use_exists():
    assert "code reads the" in h.system_prompt()
    assert h.PROMPT_VERSION == "halfyear-v1"
