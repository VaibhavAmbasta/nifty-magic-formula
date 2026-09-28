"""Step 1: build the investable universe.

Primary source is NSE's official Nifty 500 constituent file. If NSE blocks the
request (it often rejects non-browser traffic), we fall back to a bundled list
of large NSE names in data/fallback_universe.csv. Whichever source is used is
recorded in the output so the report states where the universe came from.
"""
from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import requests

NSE_URLS = [
    "https://archives.nseindia.com/content/indices/ind_nifty500list.csv",
    "https://www.niftyindices.com/IndexConstituent/ind_nifty500list.csv",
]
FALLBACK = Path(__file__).resolve().parent.parent / "data" / "fallback_universe.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/csv,*/*",
}


def _normalise(df: pd.DataFrame, source: str) -> pd.DataFrame:
    df = df.rename(columns=lambda c: c.strip())
    out = pd.DataFrame(
        {
            "symbol": df["Symbol"].str.strip(),
            "company": df["Company Name"].str.strip(),
            "nse_industry": df["Industry"].str.strip(),
        }
    )
    out["yf_ticker"] = out["symbol"] + ".NS"
    out["universe_source"] = source
    return out.drop_duplicates("symbol").reset_index(drop=True)


def load_universe() -> pd.DataFrame:
    for url in NSE_URLS:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            df = pd.read_csv(io.StringIO(r.text))
            if {"Symbol", "Company Name", "Industry"} <= set(c.strip() for c in df.columns):
                return _normalise(df, f"NSE Nifty 500 ({url})")
        except Exception as exc:  # noqa: BLE001 - any failure means "try next source"
            print(f"[universe] {url} failed: {exc}")
    print("[universe] falling back to bundled list")
    return _normalise(pd.read_csv(FALLBACK), f"bundled fallback ({FALLBACK.name})")
