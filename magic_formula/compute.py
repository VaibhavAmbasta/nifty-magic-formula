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
    mark(df["financialCurrency"].notna() & (df["financialCurrency"] != "INR"),
         "statements not in INR")
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


def post_metric_filters(d: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Drop rows where the metrics are undefined or economically meaningless."""
    d = d.copy()
    reason = pd.Series(None, index=d.index, dtype=object)
    reason[d["ebit"] <= 0] = "EBIT <= 0 (loss-making at operating level)"
    reason[reason.isna() & (d["enterprise_value"] <= 0)] = "enterprise value <= 0 (net cash > market cap)"
    reason[reason.isna() & (d["capital_employed"] <= 0)] = "capital employed <= 0"
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
