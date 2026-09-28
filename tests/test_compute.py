"""Hand-checkable tests for the Magic Formula arithmetic (all inputs in crore)."""
from datetime import date

import pandas as pd
import pytest

from magic_formula import compute, report

CR = compute.CRORE


def company(symbol, industry="Information Technology", **kw):
    base = dict(
        symbol=symbol, company=f"{symbol} Ltd", nse_industry=industry, yf_ticker=f"{symbol}.NS",
        universe_source="test", sector="Technology", financialCurrency="INR", fetch_error=None,
        balance_sheet_date="2026-03-31", marketCap=10_000 * CR, revenue=5_000 * CR,
        operating_income=1_000 * CR, ebit_reported=1_200 * CR, net_income=700 * CR,
        current_assets=3_000 * CR, current_liabilities=1_500 * CR, cash_and_st_investments=1_000 * CR,
        current_debt=200 * CR, total_debt=500 * CR, net_ppe=2_000 * CR,
        minority_interest=0.0, preferred_equity=None,
    )
    base.update({k: (v * CR if isinstance(v, (int, float)) and k not in ("fetch_error",) else v) for k, v in kw.items()})
    return base


def test_metrics_by_hand():
    d = compute.compute_metrics(pd.DataFrame([company("AAA")])).iloc[0]
    # NWC = (3000 - 1000) - (1500 - 200) = 700
    assert d.nwc_cr == pytest.approx(700)
    # capital = 700 + 2000 = 2700 ; ROC = 1000 / 2700
    assert d.roc == pytest.approx(1000 / 2700)
    # EV = 10000 + 500 + 0 + 0 - 1000 = 9500 ; EY = 1000 / 9500
    assert d.enterprise_value_cr == pytest.approx(9500)
    assert d.earnings_yield == pytest.approx(1000 / 9500)
    assert d.ebit_source == "Operating Income"


def test_negative_nwc_floored_and_ebit_fallback():
    row = company("BBB", current_liabilities=5_000, operating_income=None)
    row["operating_income"] = None
    d = compute.compute_metrics(pd.DataFrame([row])).iloc[0]
    assert d.nwc_raw_cr < 0 and d.nwc_cr == 0
    assert d.capital_employed_cr == pytest.approx(2000)
    assert d.ebit_cr == pytest.approx(1200)
    assert d.ebit_source.startswith("EBIT")


def test_filters_first_reason_wins():
    rows = [
        company("OK"),
        company("BANK", industry="Financial Services"),
        company("TINY", marketCap=100),
        company("OLD", balance_sheet_date="2023-03-31"),
        company("USD", financialCurrency="USD"),
    ]
    rows[-1]["financialCurrency"] = "USD"
    kept, excl = compute.apply_filters(pd.DataFrame(rows), 5000, 550, today=date(2026, 9, 28))
    assert kept["symbol"].tolist() == ["OK"]
    reasons = dict(zip(excl.symbol, excl.exclusion_reason))
    assert reasons["BANK"].startswith("financial")
    assert reasons["TINY"].startswith("market cap below")
    assert reasons["OLD"].startswith("latest annual")
    assert reasons["USD"] == "statements not in INR"


def test_post_filters_and_ranking():
    rows = [
        company("QUALITY", net_ppe=500),            # very high ROC, average EY
        company("CHEAP", marketCap=4_000),          # high EY, average ROC
        company("BOTH", net_ppe=500, marketCap=5_000),  # ROC ties best, EY 2nd -> wins
        company("LOSS", operating_income=-50),
    ]
    rows[3]["operating_income"] = -50 * CR
    m = compute.compute_metrics(pd.DataFrame(rows))
    valid, excl = compute.post_metric_filters(m)
    assert excl.symbol.tolist() == ["LOSS"]
    r = compute.rank(valid)
    assert r.iloc[0].symbol == "BOTH"
    assert (r.combined_score == r.roc_rank + r.ey_rank).all()


def test_report_renders_and_funnel_adds_up():
    rows = [company(f"C{i}", marketCap=6_000 + 500 * i, net_ppe=1_000 + 100 * i) for i in range(25)]
    rows.append(company("BANK", industry="Financial Services"))
    df = pd.DataFrame(rows)
    kept, ex1 = compute.apply_filters(df, 5000, 550, today=date(2026, 9, 28))
    valid, ex2 = compute.post_metric_filters(compute.compute_metrics(kept))
    ranked = compute.rank(valid)
    md = report.build_report(df, pd.concat([ex1, ex2]), ranked, 20,
                             {"min_market_cap_cr": 5000, "max_statement_age_days": 550})
    assert "## Top 20" in md and "Worked example" in md
