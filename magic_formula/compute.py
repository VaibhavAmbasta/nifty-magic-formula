"""Steps 3-5: filter, compute Greenblatt metrics, rank.

Greenblatt ("The Little Book That Beats the Market") ranks companies on two
numbers and adds the ranks:

  Return on Capital (ROC) = EBIT / (Net Working Capital + Net Fixed Assets)
      -> how much operating profit the business earns on the tangible
         capital it actually needs to run. Measures *quality*.

  Earnings Yield (EY)     = EBIT / Enterprise Value
      -> how much operating profit you get per rupee paid for the whole
         business (equity + debt - cash). Measures *cheapness*.

  Combined rank = rank(ROC) + rank(EY); lowest combined rank is best.

All functions here are pure (DataFrame in, DataFrame out) so they can be unit
tested with synthetic numbers; see tests/test_compute.py.
"""
from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

CRORE = 1e7  # 1 crore = 10,000,000 INR

# Greenblatt excludes financials and utilities: their balance sheets
# (deposits/loans, regulated asset bases) make ROC and EV meaningless.
EXCLUDED_NSE_INDUSTRIES = {"Financial Services", "Power"}
EXCLUDED_YF_SECTORS = {"Financial Services", "Utilities"}

STATEMENT_FIELDS = [
    "revenue", "operating_income", "ebit_reported", "net_income", "current_assets",
    "current_liabilities", "cash_and_st_investments", "current_debt", "total_debt",
    "net_ppe", "minority_interest", "preferred_equity",
]


PLAUSIBLE_PRICE_TO_SALES = (0.05, 50.0)


def needs_fx(df: pd.DataFrame) -> pd.Series:
    """True where statement figures are genuinely in a foreign currency.

    Yahoo's `financialCurrency` label is unreliable for Indian stocks: in the
    2026-09 run HCLTech was labelled USD but reported in INR, while Infosys was
    labelled USD and really was in USD. So the label alone is not trusted. If
    market cap / revenue is a plausible price-to-sales ratio when the
    statements are read as INR, they are INR whatever the label says.
    """
    labelled_foreign = df["financialCurrency"].notna() & (df["financialCurrency"] != "INR")
    ps_if_inr = df["marketCap"] / df["revenue"]
    lo, hi = PLAUSIBLE_PRICE_TO_SALES
    looks_inr = ps_if_inr.between(lo, hi)
    return labelled_foreign & ~looks_inr


def apply_filters(
    df: pd.DataFrame,
    min_market_cap_cr: float,
    max_statement_age_days: int,
    today: date | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (kept, excluded). `excluded` has an `exclusion_reason` column.

    Filters are applied in order and each company is excluded for the FIRST
    reason it fails, so the funnel counts in the report add up.
    """
    today = today or date.today()
    df = df.copy()
    df["exclusion_reason"] = None

    def mark(mask: pd.Series, reason: str) -> None:
        m = mask & df["exclusion_reason"].isna()
        df.loc[m, "exclusion_reason"] = reason

    mark(df.get("fetch_error").notna() if "fetch_error" in df else pd.Series(False, index=df.index),
         "data fetch failed")
    mark(df["nse_industry"].isin(EXCLUDED_NSE_INDUSTRIES) | df["sector"].isin(EXCLUDED_YF_SECTORS),
         "financial / utility (excluded by method)")
    fx = df["fx_to_inr"] if "fx_to_inr" in df else pd.Series(np.nan, index=df.index)
    mark(needs_fx(df) & fx.isna(), "statements in foreign currency and no FX rate")
    mark(df["marketCap"].isna(), "missing market cap")
    mark(df["marketCap"] < min_market_cap_cr * CRORE,
         f"market cap below Rs {min_market_cap_cr:,.0f} cr")

    stmt_date = pd.to_datetime(df["balance_sheet_date"], errors="coerce")
    age = (pd.Timestamp(today) - stmt_date).dt.days
    mark(stmt_date.isna() | (age > max_statement_age_days),
         f"latest annual statements older than {max_statement_age_days} days")

    ebit_missing = df["operating_income"].isna() & df["ebit_reported"].isna()
    mark(ebit_missing, "missing EBIT / operating income")
    need = ["current_assets", "current_liabilities", "net_ppe"]
    mark(df[need].isna().any(axis=1), "missing balance-sheet items for ROC")

    kept = df[df["exclusion_reason"].isna()].drop(columns="exclusion_reason")
    excluded = df[df["exclusion_reason"].notna()]
    return kept.reset_index(drop=True), excluded.reset_index(drop=True)


def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Add every intermediate quantity as its own column (all in INR crore)."""
    d = df.copy()

    # Convert statement figures to INR where Yahoo reports them in another
    # currency (market cap is already INR). Rate is from the balance-sheet date.
    fx = d["fx_to_inr"] if "fx_to_inr" in d else pd.Series(np.nan, index=d.index)
    foreign = needs_fx(d)
    d["fx_applied"] = np.where(foreign, fx, 1.0)
    d["statement_currency"] = np.where(foreign, d["financialCurrency"], "INR")
    for c in STATEMENT_FIELDS:
        d[c] = d[c] * d["fx_applied"]

    z = lambda col: d[col].fillna(0.0)  # noqa: E731 - missing debt/cash/MI treated as 0

    # EBIT: prefer operating income (excludes other income); fall back to
    # Yahoo's EBIT line and record which one was used.
    d["ebit"] = d["operating_income"].where(d["operating_income"].notna(), d["ebit_reported"])
    d["ebit_source"] = np.where(d["operating_income"].notna(), "Operating Income", "EBIT (incl. other income)")

    # Net working capital = (current assets - cash) - (current liabilities - short-term debt).
    # Cash is removed because it is not needed to run the business (it goes
    # into EV instead); short-term debt is removed because it is financing,
    # not an operating liability. Floored at 0, as Greenblatt does, so a
    # company funded by suppliers is not rewarded with a negative denominator.
    d["nwc_raw"] = (d["current_assets"] - z("cash_and_st_investments")) - (
        d["current_liabilities"] - z("current_debt")
    )
    d["nwc"] = d["nwc_raw"].clip(lower=0)
    d["net_fixed_assets"] = d["net_ppe"]
    d["capital_employed"] = d["nwc"] + d["net_fixed_assets"]

    # Enterprise value = what it costs to buy the whole business.
    d["enterprise_value"] = (
        d["marketCap"] + z("total_debt") + z("minority_interest") + z("preferred_equity")
        - z("cash_and_st_investments")
    )

    d["roc"] = np.where(d["capital_employed"] > 0, d["ebit"] / d["capital_employed"], np.nan)
    d["earnings_yield"] = np.where(d["enterprise_value"] > 0, d["ebit"] / d["enterprise_value"], np.nan)

    money = [
        "marketCap", "revenue", "ebit", "net_income", "current_assets", "current_liabilities",
        "cash_and_st_investments", "current_debt", "total_debt", "net_ppe", "minority_interest",
        "preferred_equity", "nwc_raw", "nwc", "net_fixed_assets", "capital_employed", "enterprise_value",
    ]
    for c in money:
        if c in d:
            d[c + "_cr"] = d[c] / CRORE
    return d


def post_metric_filters(d: pd.DataFrame, max_minority_ratio: float = 0.2) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Drop rows where the metrics are undefined or economically meaningless.

    Holding companies that consolidate a listed subsidiary (BBTC -> Britannia,
    Grasim -> UltraTech, Vedanta -> Hindustan Zinc) book the outside
    shareholders' stake at *book* value. Its market value is usually several
    times larger, so EV is understated and earnings yield is badly overstated.
    When book minority interest exceeds `max_minority_ratio` of market cap,
    the EV is not trustworthy and the company is excluded.
    """
    d = d.copy()
    reason = pd.Series(None, index=d.index, dtype=object)
    reason[d["ebit"] <= 0] = "EBIT <= 0 (loss-making at operating level)"
    reason[reason.isna() & (d["enterprise_value"] <= 0)] = "enterprise value <= 0 (net cash > market cap)"
    reason[reason.isna() & (d["capital_employed"] <= 0)] = "capital employed <= 0"
    mi_ratio = d["minority_interest"].fillna(0) / d["marketCap"]
    reason[reason.isna() & (mi_ratio > max_minority_ratio)] = (
        f"holding company: minority interest > {max_minority_ratio:.0%} of market cap (EV unreliable)"
    )
    d["exclusion_reason"] = reason
    kept = d[reason.isna()].drop(columns="exclusion_reason").reset_index(drop=True)
    return kept, d[reason.notna()].reset_index(drop=True)


def rank(d: pd.DataFrame) -> pd.DataFrame:
    """Rank 1 = best on each metric; combined = sum; ties broken by EY."""
    d = d.copy()
    d["roc_rank"] = d["roc"].rank(ascending=False, method="min").astype(int)
    d["ey_rank"] = d["earnings_yield"].rank(ascending=False, method="min").astype(int)
    d["combined_score"] = d["roc_rank"] + d["ey_rank"]
    d = d.sort_values(["combined_score", "ey_rank"]).reset_index(drop=True)
    d["magic_formula_rank"] = np.arange(1, len(d) + 1)
    return d
