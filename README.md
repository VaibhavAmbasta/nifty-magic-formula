# nifty-magic-formula

Joel Greenblatt's Magic Formula (*The Little Book That Beats the Market*) applied to Indian equities. It ranks the Nifty 500, excluding financials and utilities, on **return on capital** and **earnings yield** and outputs the top 20.

**Latest results:** [`output/REPORT.md`](output/REPORT.md)

## The idea in two numbers

| | Formula | Question it answers |
|---|---|---|
| Return on capital | EBIT ÷ (net working capital + net fixed assets) | Is this a good business? |
| Earnings yield | EBIT ÷ enterprise value | Is it cheap? |

Each company is ranked on both measures, and the two ranks are added together. The lowest total wins. The combination rewards good businesses at cheap prices, and penalises companies that score well on only one of the two.

## Pipeline: each step writes its own file

| Step | Code | Output |
|---|---|---|
| 1. Universe: Nifty 500 from NSE (falls back to a bundled list) | `magic_formula/universe.py` | `output/01_universe.csv` |
| 2. Raw fundamentals from Yahoo Finance, recording the source line item for each value | `magic_formula/fetch.py` | `output/02_raw_financials.csv` |
| 3. Filters: financials/utilities, market cap, stale statements, missing data | `compute.apply_filters` | `output/03_exclusions.csv` |
| 4. Metrics: EBIT, NWC, capital employed, EV, ROC, EY | `compute.compute_metrics` | `output/04_metrics.csv` |
| 5. Ranking | `compute.rank` | `output/05_top20.csv` |
| 6. Report: funnel, top 20, findings, worked example | `magic_formula/report.py` | `output/REPORT.md` |

### Definitions and why

- **EBIT** is Yahoo's *Operating Income*, which excludes "other income". Many Indian companies earn a lot of treasury income on their cash. That cash is already subtracted from EV, so counting its income in EBIT as well would double count it. If Operating Income is missing, the pipeline falls back to Yahoo's *EBIT* line and flags it.
- **Net working capital** = (current assets − cash & short-term investments) − (current liabilities − short-term debt), floored at 0 (Greenblatt's convention).
- **Net fixed assets** = Net PP&E. Goodwill and intangibles are excluded because the method measures return on the *tangible* capital a business needs.
- **Enterprise value** = market cap + total debt + minority interest + preferred equity − cash & short-term investments.
- **Excluded:** financials and utilities (their balance sheets make ROC/EV meaningless), market cap below ₹5,000 cr, companies with EBIT ≤ 0 or EV ≤ 0, and statements older than about 18 months.

## Running it

**On GitHub (recommended):** open Actions → *Run Magic Formula screen* → *Run workflow*. The job runs the tests, fetches live data, and commits the refreshed `output/`. It also runs automatically on the 1st of each month.

**Locally:**
```bash
pip install -r requirements.txt
python -m pytest -q          # arithmetic checked against hand-worked examples
python run.py                # fetches about 500 companies, takes roughly 10 minutes
python run.py --offline      # re-rank from saved raw data without re-fetching
python run.py --min-mcap-cr 20000 --top 30
```

## Limitations

Yahoo Finance data for Indian companies is free, unaudited, and sometimes misclassified. The screen uses the latest *annual* EBIT, whereas Greenblatt uses trailing twelve months. A single year's EBIT makes cyclicals look cheapest right at their earnings peak. Use the output as a research shortlist, not a buy list. See the caveats section of the report.
