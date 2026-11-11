"""The tearsheet's two charts, drawn the same way in the app and in the PDF (Altair)."""

from __future__ import annotations

import altair as alt
import pandas as pd

FONT = "Inter"


def leverage(points: list[dict]) -> alt.Chart:
    data = pd.DataFrame(points)
    return (
        alt.Chart(data)
        .mark_line(point=alt.OverlayMarkDef(size=60))
        .encode(
            x=alt.X("year:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("value:Q", title="x EBITDA"),
            color=alt.Color("metric:N", title=None, legend=alt.Legend(orient="bottom")),
            tooltip=["year", "metric", "rendered"],
        )
    )


def liquidity(points: list[dict], currency: str) -> alt.Chart:
    """Stacked bars in the order given: the liquidity bar, then the maturities (M8)."""
    data = pd.DataFrame(points)
    data["millions"] = data["value"] / 1e6
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("year:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("millions:Q", title=f"{currency} m", stack="zero"),
            color=alt.Color("metric:N", title=None, legend=alt.Legend(orient="bottom")),
            tooltip=["year", "metric", "rendered"],
        )
    )


def for_print(chart: alt.Chart, width: int, height: int) -> dict:
    """The chart as a Vega-Lite spec sized and styled for the PDF."""
    styled = (
        chart.properties(width=width, height=height)
        .configure(font=FONT)
        .configure_axis(labelFontSize=9, titleFontSize=9, grid=True, gridColor="#e3e8ee")
        .configure_legend(labelFontSize=9, symbolSize=60)
        .configure_view(strokeWidth=0)
    )
    return styled.to_dict()
