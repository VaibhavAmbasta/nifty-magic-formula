# Magic Formula screen — Indian equities

Generated 2026-09-28 · universe: NSE Nifty 500 (https://archives.nseindia.com/content/indices/ind_nifty500list.csv) · data: Yahoo Finance (latest annual statements, current market cap)

## Method (Joel Greenblatt, *The Little Book That Beats the Market*)

| Metric | Formula | What it measures |
|---|---|---|
| Return on capital (ROC) | EBIT ÷ (Net working capital + Net fixed assets) | Quality: profit per rupee of tangible capital the business needs |
| Earnings yield (EY) | EBIT ÷ Enterprise value | Price: profit per rupee paid for the whole business |
| Combined score | ROC rank + EY rank | Lowest = good business at a cheap price |

Parameters: minimum market cap Rs 5,000 cr · statements no older than 550 days · financials and utilities excluded.

## Funnel: how 501 companies became 353

| Step | Companies removed | Remaining |
|---|---:|---:|
| Starting universe | – | 501 |
| financial / utility (excluded by method) | 123 | 378 |
| market cap below Rs 5,000 cr | 1 | 377 |
| missing market cap | 1 | 376 |
| statements not in INR | 2 | 374 |
| missing balance-sheet items for ROC | 1 | 373 |
| EBIT <= 0 (loss-making at operating level) | 20 | 353 |
| **Ranked** | | **353** |

Full list of exclusions with reasons: `output/03_exclusions.csv`.

## Top 20

| # | Company | Symbol | Sector | Mkt cap (cr) | EBIT (cr) | ROC | ROC rank | EY | EY rank | Score |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | Sonata Software Ltd. | SONATSOFTW | Information Technology | 7,615 | 690 | 336.9% | 4 | 8.9% | 32 | 36 |
| 2 | Bombay Burmah Trading Corporation Ltd. | BBTC | Fast Moving Consumer Goods | 9,901 | 3,142 | 111.9% | 37 | 27.1% | 1 | 38 |
| 3 | Zensar Technolgies Ltd. | ZENSARTECH | Information Technology | 9,915 | 839 | 160.4% | 24 | 11.3% | 20 | 44 |
| 4 | Birlasoft Ltd. | BSOFT | Information Technology | 7,693 | 803 | 97.0% | 44 | 14.9% | 8 | 52 |
| 5 | BLS International Services Ltd. | BLS | Consumer Services | 9,155 | 756 | 165.1% | 21 | 9.0% | 31 | 52 |
| 6 | KPIT Technologies Ltd. | KPITTECH | Information Technology | 13,878 | 1,045 | 166.7% | 20 | 7.9% | 39 | 59 |
| 7 | Castrol India Ltd. | CASTROLIND | Oil Gas & Consumable Fuels | 19,931 | 1,249 | 308.6% | 7 | 6.6% | 54 | 61 |
| 8 | Wipro Ltd. | WIPRO | Information Technology | 160,935 | 14,913 | 90.8% | 47 | 11.7% | 17 | 64 |
| 9 | Sun TV Network Ltd. | SUNTV | Media Entertainment & Publication | 20,530 | 1,498 | 94.0% | 45 | 10.7% | 22 | 67 |
| 10 | Tata Consultancy Services Ltd. | TCS | Information Technology | 750,319 | 67,022 | 111.1% | 39 | 9.3% | 30 | 69 |
| 11 | Pfizer Ltd. | PFIZER | Healthcare | 18,153 | 847 | 304.2% | 8 | 5.6% | 77 | 85 |
| 12 | Hexaware Technologies Ltd. | HEXT | Information Technology | 29,868 | 1,841 | 129.2% | 30 | 6.5% | 58 | 88 |
| 13 | ITC Ltd. | ITC | Fast Moving Consumer Goods | 334,126 | 25,596 | 79.1% | 54 | 8.2% | 36 | 90 |
| 14 | Hindustan Zinc Ltd. | HINDZINC | Metals & Mining | 242,745 | 18,495 | 76.8% | 56 | 7.8% | 41 | 97 |
| 15 | Hero MotoCorp Ltd. | HEROMOTOCO | Automobile and Auto Components | 107,116 | 6,204 | 104.8% | 41 | 6.5% | 57 | 98 |
| 16 | National Aluminium Co. Ltd. | NATIONALUM | Metals & Mining | 63,547 | 7,212 | 50.8% | 83 | 13.0% | 16 | 99 |
| 17 | RITES Ltd. | RITES | Construction | 9,458 | 499 | 74.6% | 61 | 7.5% | 45 | 106 |
| 18 | MphasiS Ltd. | MPHASIS | Information Technology | 42,478 | 2,428 | 117.5% | 35 | 5.8% | 72 | 107 |
| 19 | Ashok Leyland Ltd. | ASHOKLEY | Capital Goods | 91,750 | 11,001 | 55.4% | 77 | 7.7% | 43 | 120 |
| 20 | Chennai Petroleum Corporation Ltd. | CHENNPETRO | Oil Gas & Consumable Fuels | 21,175 | 4,460 | 35.8% | 118 | 20.3% | 4 | 122 |

## Findings

- **Top 20 vs ranked universe (medians):** ROC 107.9% vs 23.6%; EY 8.5% vs 3.4%.
- **ROC and EY ranks are positively correlated (Spearman +0.16).** Positive means high-quality businesses are not systematically priced higher here, which makes it easier to find names good on both.
- **Sector concentration of the top 20:**
- Information Technology: 8
- Fast Moving Consumer Goods: 2
- Oil Gas & Consumable Fuels: 2
- Metals & Mining: 2
- Consumer Services: 1
- Media Entertainment & Publication: 1
- Healthcare: 1
- Automobile and Auto Components: 1
- Construction: 1
- Capital Goods: 1
- **High ROC but too expensive to make the top 20:**
- Oracle Financial Services Software Ltd. (OFSS): ROC 328.6% (rank 5), EY 3.9% (rank 144) → overall #39
- Abbott India Ltd. (ABBOTINDIA): ROC 421.0% (rank 2), EY 3.3% (rank 180) → overall #60
- Inventurus Knowledge Solutions Ltd. (IKS): ROC 327.5% (rank 6), EY 3.0% (rank 198) → overall #72
- Glaxosmithkline Pharmaceuticals Ltd. (GLAXO): ROC 407.1% (rank 3), EY 2.7% (rank 232) → overall #84
- Affle 3i Ltd. (AFFLE): ROC 289.4% (rank 10), EY 2.5% (rank 250) → overall #102
- TBO Tek Ltd. (TBOTEK): ROC 303.4% (rank 9), EY 2.0% (rank 279) → overall #123
- Indiamart Intermesh Ltd. (INDIAMART): ROC 2,343.5% (rank 1), EY 0.5% (rank 347) → overall #171
- **Cheap but low quality, so they miss the top 20:**
- Bharat Petroleum Corporation Ltd. (BPCL): ROC 34.2% (rank 126), EY 22.8% (rank 2) → overall #22
- Coal India Ltd. (COALINDIA): ROC 28.1% (rank 152), EY 14.5% (rank 9) → overall #46
- Indian Oil Corporation Ltd. (IOC): ROC 23.4% (rank 178), EY 21.6% (rank 3) → overall #59
- Hindustan Petroleum Corporation Ltd. (HINDPETRO): ROC 23.0% (rank 184), EY 19.6% (rank 5) → overall #63
- Chambal Fertilizers & Chemicals Ltd. (CHAMBLFERT): ROC 21.8% (rank 193), EY 14.2% (rank 10) → overall #70
- NCC Ltd. (NCC): ROC 20.6% (rank 203), EY 16.6% (rank 7) → overall #73
- Oil & Natural Gas Corporation Ltd. (ONGC): ROC 18.2% (rank 231), EY 17.5% (rank 6) → overall #89
- Statement dates behind the top 20: {'2026-03-31': 18, '2025-12-31': 2}. EBIT fell back to Yahoo's EBIT line (includes other income) for 0 of them.

## How to check a number

### Worked example: #1 Sonata Software Ltd. (SONATSOFTW)

Every number below is in INR crore, from Yahoo Finance annual statements dated 2026-03-31.

**1. EBIT** (Operating Income) = **690**

**2. Net working capital**
```
  Current assets                           2,773
- Cash & short-term investments              604
- Current liabilities                      2,633
+ Short-term debt (financing, not operating)           315
= NWC (raw)                                 -149
  NWC used (floored at 0)                      0
```

**3. Capital employed** = NWC 0 + Net fixed assets (Net PP&E) 205 = **205**

**4. Return on capital** = 690 / 205 = **336.9%** → ROC rank **4**

**5. Enterprise value**
```
  Market cap                               7,615
+ Total debt                                 723
+ Minority interest                          nan
+ Preferred equity                           nan
- Cash & short-term investments              604
= Enterprise value                         7,733
```

**6. Earnings yield** = 690 / 7,733 = **8.9%** → EY rank **32**

**7. Combined score** = 4 + 32 = **36** → overall rank **#1**


To audit any other company: find its row in `output/04_metrics.csv` (every intermediate column), then its source line items in `output/02_raw_financials.csv` (the `__src` columns name the Yahoo row each value came from).

## Caveats — read before acting on this

1. **Yahoo Finance data is unaudited and sometimes wrong** for Indian companies (misclassified line items, missing current debt, consolidated vs standalone mix-ups). Check any name you intend to buy against its annual report.
2. **Annual, not trailing-twelve-month, EBIT.** Greenblatt uses TTM. By September the March-year figures are six months old.
3. **Cyclicals look best at the peak.** Metals, oil & gas, and commodity names show high EY exactly when earnings are at their top. A one-year EBIT snapshot cannot tell peak from normal earnings.
4. **PSUs.** State-owned companies often screen cheap for structural reasons (government ownership, policy-driven pricing, dividend extraction). The formula does not account for that.
5. **The strategy's edge depends on holding a basket** (Greenblatt: 20–30 names, rebalanced yearly, held through years of underperformance). A single screen is a starting list for research, not a portfolio.
