"""Checks of the M0 filing selection and gap-year logic."""

from datetime import date

from spikes.m0.coverage import fiscal_years_to_check


def row(issuer, fy, period_end):
    return {"issuer": issuer, "fiscal_year": fy, "period_end": period_end, "chosen": "yes"}


def test_missing_year_is_read_from_next_years_comparatives():
    rows = [row("x", 2022, "2022-12-31"), row("x", 2024, "2024-12-31")]
    jobs = [(fy, end, source) for _, fy, end, source in fiscal_years_to_check(rows, 2021)]
    assert jobs == [
        (2021, date(2021, 12, 31), "comparative in FY2022 filing"),
        (2022, date(2022, 12, 31), ""),
        (2023, date(2023, 12, 31), "comparative in FY2024 filing"),
        (2024, date(2024, 12, 31), ""),
    ]


def test_no_comparative_before_the_first_year_in_scope():
    rows = [row("x", 2021, "2021-03-31")]
    assert [job[1] for job in fiscal_years_to_check(rows, 2021)] == [2021]
