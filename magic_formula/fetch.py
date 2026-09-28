"""Step 2: pull raw fundamentals for every ticker in the universe.

Source: Yahoo Finance via the `yfinance` package. For each company we take the
most recent *annual* income statement and balance sheet (for Indian companies
that is normally the March fiscal year-end) plus the current market cap.

Nothing is computed here. Every raw number is written to
output/02_raw_financials.csv together with the Yahoo line item it came from,
so any figure in the final ranking can be traced back to its source row.
"""
from __future__ import annotations

import math
import time

import pandas as pd

# Each field is looked up by trying Yahoo line-item names in order; the first
# one present wins and its name is recorded in `<field>__src`.
INCOME_FIELDS = {
    "revenue": ["Total Revenue", "Operating Revenue"],
    # Operating income excludes "other income" (treasury/interest income),
    # which matters in India: cash-rich firms book large other income. Since
    # cash is subtracted from EV, including it in EBIT would double count.
    "operating_income": ["Operating Income"],
    "ebit_reported": ["EBIT"],
    "net_income": ["Net Income", "Net Income Common Stockholders"],
}
BALANCE_FIELDS = {
    "current_assets": ["Current Assets"],
    "current_liabilities": ["Current Liabilities"],
    "cash_and_st_investments": [
        "Cash Cash Equivalents And Short Term Investments",
        "Cash And Cash Equivalents",
    ],
    "current_debt": [
        "Current Debt And Capital Lease Obligation",
        "Current Debt",
    ],
    "total_debt": ["Total Debt"],
    "net_ppe": ["Net PPE"],
    "minority_interest": ["Minority Interest"],
    "preferred_equity": ["Preferred Stock Equity", "Preferred Stock"],
}
INFO_FIELDS = ["marketCap", "sector", "industry", "longName", "currency", "financialCurrency"]


def _pick(frame: pd.DataFrame, candidates: list[str]) -> tuple[float | None, str | None]:
    """Return (value, line_item_name) for the latest column, or (None, None)."""
    if frame is None or frame.empty:
        return None, None
    col = frame.columns[0]  # yfinance orders columns newest first
    for name in candidates:
        if name in frame.index:
            val = frame.at[name, col]
            if val is not None and not (isinstance(val, float) and math.isnan(val)):
                return float(val), name
    return None, None


def fetch_one(yf_ticker: str) -> dict:
    import yfinance as yf

    t = yf.Ticker(yf_ticker)
    row: dict = {"yf_ticker": yf_ticker}
    info = t.info or {}
    for k in INFO_FIELDS:
        row[k] = info.get(k)

    inc = t.income_stmt
    bal = t.balance_sheet
    row["income_stmt_date"] = str(inc.columns[0].date()) if inc is not None and not inc.empty else None
    row["balance_sheet_date"] = str(bal.columns[0].date()) if bal is not None and not bal.empty else None

    for field, names in INCOME_FIELDS.items():
        row[field], row[f"{field}__src"] = _pick(inc, names)
    for field, names in BALANCE_FIELDS.items():
        row[field], row[f"{field}__src"] = _pick(bal, names)

    # Some companies (e.g. Infosys, HCLTech) report to Yahoo in USD while their
    # market cap is in INR. Record the exchange rate at the balance-sheet date
    # so compute.py can convert; the rate and its date are kept for audit.
    fc = row.get("financialCurrency") or "INR"
    row["fx_to_inr"], row["fx_date"] = (1.0, None) if fc == "INR" else _fx_to_inr(fc, row["balance_sheet_date"])
    return row


def _fx_to_inr(currency: str, on: str | None) -> tuple[float | None, str | None]:
    import yfinance as yf

    if not on:
        return None, None
    end = pd.Timestamp(on) + pd.Timedelta(days=1)
    hist = yf.Ticker(f"{currency}INR=X").history(start=end - pd.Timedelta(days=10), end=end)
    if hist.empty:
        return None, None
    return float(hist["Close"].iloc[-1]), str(hist.index[-1].date())


def fetch_all(tickers: list[str], pause: float = 0.4, retries: int = 2) -> pd.DataFrame:
    rows = []
    for i, tk in enumerate(tickers, 1):
        for attempt in range(retries + 1):
            try:
                row = fetch_one(tk)
                row["fetch_error"] = None
                break
            except Exception as exc:  # noqa: BLE001
                row = {"yf_ticker": tk, "fetch_error": f"{type(exc).__name__}: {exc}"[:200]}
                time.sleep(2 ** attempt)
        rows.append(row)
        if i % 25 == 0:
            print(f"[fetch] {i}/{len(tickers)}")
        time.sleep(pause)
    return pd.DataFrame(rows)
