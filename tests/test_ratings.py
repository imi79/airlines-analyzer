"""The ratings box (M8): entries copied by hand, checked against the report's own sentence."""

from datetime import date

from tearsheet.ratings import Rating, RatingEntry, check_entry, load_entries

REPORT = (
    "Building on this profit growth, the group continues to have one of the strongest\n"
    "balance sheets (Baa2/stable from Moody’s and BBB+/stable from Standard & Poor’s)."
)


def entry(ratings, quote="(Baa2/stable from Moody’s and BBB+/stable from Standard & Poor’s)",
          **kw):  # fmt: skip
    data = dict(issuer="abc", as_at=date(2025, 9, 30), ratings=ratings, document="R1",
                fiscal_year=2025, location="page 33", quote=quote, entered_by="AI assistant",
                entered_on=date(2026, 11, 11), reviewed_by=None)  # fmt: skip
    data.update(kw)
    return RatingEntry(**data)


GOOD = [Rating("Moody's", "Baa2", "stable"), Rating("S&P", "BBB+", "stable")]


def test_a_correct_entry_passes_the_checks_but_waits_for_review():
    e = check_entry(entry(GOOD), REPORT)
    assert e.failures == []
    assert e.status == "unverified" and "Imane" in e.reason
    e.reviewed_by = "Imane (2026-11-12)"
    assert e.status == "verified"
    assert e.text() == "Moody's Baa2 (stable), S&P BBB+ (stable)"


def test_a_quote_not_in_the_report_is_rejected():
    e = check_entry(entry(GOOD, quote="(Baa1/stable from Moody’s)"), REPORT)
    assert "quote not found word for word in the report" in e.failures


def test_a_rating_not_in_the_quote_is_rejected():
    e = check_entry(entry([Rating("S&P", "BBB", "stable")]), REPORT)
    assert any("does not show the S&P rating BBB" in f for f in e.failures)


def test_a_rating_off_the_agency_scale_is_rejected():
    e = check_entry(entry([Rating("Moody's", "BBB+", "stable")]), REPORT)
    assert any("not on the Moody's rating scale" in f for f in e.failures)


def test_an_outlook_not_in_the_quote_is_rejected():
    e = check_entry(entry([Rating("S&P", "BBB+", "negative")]), REPORT)
    assert any("negative outlook" in f for f in e.failures)


def test_an_entry_older_than_a_year_is_flagged_stale():
    e = entry(GOOD)
    assert e.stale(date(2026, 11, 11)) and not e.stale(date(2026, 6, 30))


def test_a_report_without_a_rating_says_so_and_does_not_claim_unrated():
    e = check_entry(entry([], quote="", not_stated=True), None)
    assert e.failures == []
    assert e.text() == "No rating given in the FY2025 annual report"


def test_every_configured_entry_has_a_source_and_a_date():
    for e in load_entries():
        assert e.document and e.location and e.as_at and e.entered_by
        assert e.not_stated or (e.ratings and e.quote)
