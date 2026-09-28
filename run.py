"""Run the full Magic Formula pipeline for Indian equities.

    python run.py                 # fetch live data, rank, write output/
    python run.py --offline       # re-rank from output/02_raw_financials.csv (no network)

Outputs (each step writes its own file so the process can be audited):
    output/01_universe.csv        companies considered and where the list came from
    output/02_raw_financials.csv  raw Yahoo numbers + the line item each came from
    output/03_exclusions.csv      every company dropped, with the reason
    output/04_metrics.csv         every intermediate calculation, ranked
    output/05_top20.csv           the final list
    output/REPORT.md              narrative: method, funnel, top 20, findings, worked example
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from magic_formula import compute, report
from magic_formula.universe import load_universe

OUT = Path(__file__).resolve().parent / "output"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--offline", action="store_true", help="reuse output/02_raw_financials.csv")
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--min-mcap-cr", type=float, default=5000, help="minimum market cap, INR crore")
    p.add_argument("--max-age-days", type=int, default=550, help="max age of latest annual statements")
    p.add_argument("--max-minority-ratio", type=float, default=0.2,
                   help="exclude if book minority interest / market cap exceeds this")
    p.add_argument("--limit", type=int, default=None, help="only fetch first N tickers (debugging)")
    a = p.parse_args()
    OUT.mkdir(exist_ok=True)

    # Step 1 - universe
    if a.offline:
        universe = pd.read_csv(OUT / "01_universe.csv")
        raw = pd.read_csv(OUT / "02_raw_financials.csv")
    else:
        universe = load_universe()
        if a.limit:
            universe = universe.head(a.limit)
        universe.to_csv(OUT / "01_universe.csv", index=False)
        print(f"[1] universe: {len(universe)} companies from {universe['universe_source'].iloc[0]}")

        # Step 2 - raw fundamentals
        from magic_formula.fetch import fetch_all
        raw = fetch_all(universe["yf_ticker"].tolist())
        raw.to_csv(OUT / "02_raw_financials.csv", index=False)
        print(f"[2] fetched {len(raw)} (errors: {raw['fetch_error'].notna().sum()})")

    df = universe.merge(raw, on="yf_ticker", how="left")

    # Step 3 - pre-metric filters
    params = {"min_market_cap_cr": a.min_mcap_cr, "max_statement_age_days": a.max_age_days,
              "max_minority_ratio": a.max_minority_ratio}
    kept, excl1 = compute.apply_filters(df, a.min_mcap_cr, a.max_age_days)
    print(f"[3] filters: kept {len(kept)}, excluded {len(excl1)}")

    # Step 4 - metrics, then drop undefined ones
    metrics = compute.compute_metrics(kept)
    valid, excl2 = compute.post_metric_filters(metrics, a.max_minority_ratio)
    excluded = pd.concat([excl1, excl2], ignore_index=True)
    excluded[["symbol", "company", "nse_industry", "exclusion_reason"]].to_csv(OUT / "03_exclusions.csv", index=False)
    print(f"[4] metrics: {len(valid)} valid, {len(excl2)} dropped")

    # Step 5 - rank
    ranked = compute.rank(valid)
    cols = ["magic_formula_rank", "symbol", "company", "nse_industry", "balance_sheet_date", "ebit_source", "financialCurrency", "statement_currency", "fx_applied",
            "marketCap_cr", "revenue_cr", "ebit_cr", "current_assets_cr", "cash_and_st_investments_cr",
            "current_liabilities_cr", "current_debt_cr", "nwc_raw_cr", "nwc_cr", "net_fixed_assets_cr",
            "capital_employed_cr", "total_debt_cr", "minority_interest_cr", "preferred_equity_cr",
            "enterprise_value_cr", "roc", "roc_rank", "earnings_yield", "ey_rank", "combined_score"]
    ranked[cols].round(4).to_csv(OUT / "04_metrics.csv", index=False)
    ranked[cols].head(a.top).round(4).to_csv(OUT / "05_top20.csv", index=False)

    # Step 6 - report
    (OUT / "REPORT.md").write_text(report.build_report(universe, excluded, ranked, a.top, params))
    print(f"[5] top {a.top}:")
    print(ranked[["magic_formula_rank", "symbol", "roc", "earnings_yield", "combined_score"]].head(a.top).to_string(index=False))


if __name__ == "__main__":
    main()
