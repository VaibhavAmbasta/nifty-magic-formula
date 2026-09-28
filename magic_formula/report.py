"""Step 6: write REPORT.md explaining how the top 20 were arrived at."""
from __future__ import annotations

from datetime import date

import pandas as pd


def _pct(x: float) -> str:
    return f"{x * 100:,.1f}%"


def _cr(x: float) -> str:
    return "0" if pd.isna(x) else f"{x:,.0f}"


def _funnel(universe_n: int, excluded: pd.DataFrame, ranked_n: int) -> str:
    lines = ["| Step | Companies removed | Remaining |", "|---|---:|---:|"]
    remaining = universe_n
    lines.append(f"| Starting universe | – | {remaining} |")
    for reason, n in excluded["exclusion_reason"].value_counts(sort=False).items():
        remaining -= n
        lines.append(f"| {reason} | {n} | {remaining} |")
    assert remaining == ranked_n, (remaining, ranked_n)
    lines.append(f"| **Ranked** | | **{ranked_n}** |")
    return "\n".join(lines)


def _worked_example(r: pd.Series) -> str:
    return f"""### Worked example: #{r.magic_formula_rank} {r.company} ({r.symbol})

Every number below is in INR crore, from Yahoo Finance annual statements dated {r.balance_sheet_date}{'' if r.fx_applied == 1 else f' (reported in {r.statement_currency}, converted at {r.fx_applied:.2f} INR)'}.

**1. EBIT** ({r.ebit_source}) = **{_cr(r.ebit_cr)}**

**2. Net working capital**
```
  Current assets                    {_cr(r.current_assets_cr):>12}
- Cash & short-term investments     {_cr(r.cash_and_st_investments_cr):>12}
- Current liabilities               {_cr(r.current_liabilities_cr):>12}
+ Short-term debt (financing, not operating)  {_cr(r.current_debt_cr):>12}
= NWC (raw)                         {_cr(r.nwc_raw_cr):>12}
  NWC used (floored at 0)           {_cr(r.nwc_cr):>12}
```

**3. Capital employed** = NWC {_cr(r.nwc_cr)} + Net fixed assets (Net PP&E) {_cr(r.net_fixed_assets_cr)} = **{_cr(r.capital_employed_cr)}**

**4. Return on capital** = {_cr(r.ebit_cr)} / {_cr(r.capital_employed_cr)} = **{_pct(r.roc)}** → ROC rank **{r.roc_rank}**

**5. Enterprise value**
```
  Market cap                        {_cr(r.marketCap_cr):>12}
+ Total debt                        {_cr(r.total_debt_cr):>12}
+ Minority interest                 {_cr(r.minority_interest_cr):>12}
+ Preferred equity                  {_cr(r.preferred_equity_cr):>12}
- Cash & short-term investments     {_cr(r.cash_and_st_investments_cr):>12}
= Enterprise value                  {_cr(r.enterprise_value_cr):>12}
```

**6. Earnings yield** = {_cr(r.ebit_cr)} / {_cr(r.enterprise_value_cr)} = **{_pct(r.earnings_yield)}** → EY rank **{r.ey_rank}**

**7. Combined score** = {r.roc_rank} + {r.ey_rank} = **{r.combined_score}** → overall rank **#{r.magic_formula_rank}**
"""


def build_report(
    universe: pd.DataFrame,
    excluded: pd.DataFrame,
    ranked: pd.DataFrame,
    top_n: int,
    params: dict,
) -> str:
    top = ranked.head(top_n)
    n = len(ranked)

    table = ["| # | Company | Symbol | Sector | Mkt cap (cr) | EBIT (cr) | ROC | ROC rank | EY | EY rank | Score |",
             "|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in top.itertuples():
        table.append(
            f"| {r.magic_formula_rank} | {r.company} | {r.symbol} | {r.nse_industry} | {_cr(r.marketCap_cr)} | "
            f"{_cr(r.ebit_cr)} | {_pct(r.roc)} | {r.roc_rank} | {_pct(r.earnings_yield)} | {r.ey_rank} | {r.combined_score} |"
        )

    sectors = top["nse_industry"].value_counts()
    sector_lines = "\n".join(f"- {s}: {c}" for s, c in sectors.items())

    med_all = ranked[["roc", "earnings_yield"]].median()
    med_top = top[["roc", "earnings_yield"]].median()
    rank_corr = ranked["roc_rank"].corr(ranked["ey_rank"])  # Pearson on ranks = Spearman
    ebit_fallback = (top["ebit_source"] != "Operating Income").sum()
    stmt_dates = top["balance_sheet_date"].value_counts().to_dict()

    # Names that are excellent on one axis but miss the top N on the other:
    # these show what the combination is doing.
    best_roc_missed = ranked[(ranked["roc_rank"] <= 10) & (ranked["magic_formula_rank"] > top_n)]
    best_ey_missed = ranked[(ranked["ey_rank"] <= 10) & (ranked["magic_formula_rank"] > top_n)]

    def _missed(df: pd.DataFrame) -> str:
        if df.empty:
            return "- none"
        return "\n".join(
            f"- {r.company} ({r.symbol}): ROC {_pct(r.roc)} (rank {r.roc_rank}), "
            f"EY {_pct(r.earnings_yield)} (rank {r.ey_rank}) → overall #{r.magic_formula_rank}"
            for r in df.itertuples()
        )

    return f"""# Magic Formula screen — Indian equities

Generated {date.today().isoformat()} · universe: {universe['universe_source'].iloc[0]} · data: Yahoo Finance (latest annual statements, current market cap)

## Method (Joel Greenblatt, *The Little Book That Beats the Market*)

| Metric | Formula | What it measures |
|---|---|---|
| Return on capital (ROC) | EBIT ÷ (Net working capital + Net fixed assets) | Quality: profit per rupee of tangible capital the business needs |
| Earnings yield (EY) | EBIT ÷ Enterprise value | Price: profit per rupee paid for the whole business |
| Combined score | ROC rank + EY rank | Lowest = good business at a cheap price |

Parameters: minimum market cap Rs {params['min_market_cap_cr']:,.0f} cr · statements no older than {params['max_statement_age_days']} days · financials and utilities excluded · holding companies excluded where book minority interest > {params.get('max_minority_ratio', 0.2):.0%} of market cap.

## Funnel: how {len(universe)} companies became {n}

{_funnel(len(universe), excluded, n)}

Full list of exclusions with reasons: `output/03_exclusions.csv`.

## Top {top_n}

{chr(10).join(table)}

## Findings

- **Top {top_n} vs ranked universe (medians):** ROC {_pct(med_top.roc)} vs {_pct(med_all.roc)}; EY {_pct(med_top.earnings_yield)} vs {_pct(med_all.earnings_yield)}.
- **ROC and EY ranks are {'positively' if rank_corr > 0 else 'negatively'} correlated (Spearman {rank_corr:+.2f}).** {'Negative means the market mostly prices quality correctly — high-ROC businesses tend to be expensive, so few names are strong on both, and the formula is picking the exceptions.' if rank_corr < 0 else 'Positive means high-quality businesses are not systematically priced higher here, which makes it easier to find names good on both.'}
- **Sector concentration of the top {top_n}:**
{sector_lines}
- **High ROC but too expensive to make the top {top_n}:**
{_missed(best_roc_missed)}
- **Cheap but low quality, so they miss the top {top_n}:**
{_missed(best_ey_missed)}
- Statement dates behind the top {top_n}: {stmt_dates}. EBIT fell back to Yahoo's EBIT line (includes other income) for {ebit_fallback} of them.

## How to check a number

{_worked_example(top.iloc[0])}

To audit any other company: find its row in `output/04_metrics.csv` (every intermediate column), then its source line items in `output/02_raw_financials.csv` (the `__src` columns name the Yahoo row each value came from).

## Caveats — read before acting on this

1. **Consolidated finance arms distort some names.** Companies that consolidate a lending subsidiary (e.g. Ashok Leyland → Hinduja Leyland Finance) carry that lender's borrowings in total debt and its interest income in EBIT. Check these against standalone figures.
1. **Yahoo Finance data is unaudited and sometimes wrong** for Indian companies (misclassified line items, missing current debt, consolidated vs standalone mix-ups). Check any name you intend to buy against its annual report.
2. **Annual, not trailing-twelve-month, EBIT.** Greenblatt uses TTM. By September the March-year figures are six months old.
3. **Cyclicals look best at the peak.** Metals, oil & gas, and commodity names show high EY exactly when earnings are at their top. A one-year EBIT snapshot cannot tell peak from normal earnings.
4. **PSUs.** State-owned companies often screen cheap for structural reasons (government ownership, policy-driven pricing, dividend extraction). The formula does not account for that.
5. **The strategy's edge depends on holding a basket** (Greenblatt: 20–30 names, rebalanced yearly, held through years of underperformance). A single screen is a starting list for research, not a portfolio.
"""
