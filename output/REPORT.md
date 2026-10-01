# Magic Formula screen — Indian equities

Generated 2026-10-01 · universe: NSE Nifty 500 (https://archives.nseindia.com/content/indices/ind_nifty500list.csv) · data: Yahoo Finance (latest annual statements, current market cap)

## Method (Joel Greenblatt, *The Little Book That Beats the Market*)

| Metric | Formula | What it measures |
|---|---|---|
| Return on capital (ROC) | EBIT ÷ (Net working capital + Net fixed assets) | Quality: profit per rupee of tangible capital the business needs |
| Earnings yield (EY) | EBIT ÷ Enterprise value | Price: profit per rupee paid for the whole business |
| Combined score | ROC rank + EY rank | Lowest = good business at a cheap price |

Parameters: minimum market cap Rs 5,000 cr · statements no older than 550 days · financials and utilities excluded · holding companies excluded where book minority interest > 20% of market cap.

## Funnel: how 501 companies became 349

| Step | Companies removed | Remaining |
|---|---:|---:|
| Starting universe | – | 501 |
| financial / utility (excluded by method) | 122 | 379 |
| missing market cap | 4 | 375 |
| missing balance-sheet items for ROC | 1 | 374 |
| EBIT <= 0 (loss-making at operating level) | 21 | 353 |
| holding company: minority interest > 20% of market cap (EV unreliable) | 4 | 349 |
| **Ranked** | | **349** |

Full list of exclusions with reasons: `output/03_exclusions.csv`.

## Top 20

| # | Company | Symbol | Sector | Mkt cap (cr) | EBIT (cr) | ROC | ROC rank | EY | EY rank | Score |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | HCL Technologies Ltd. | HCLTECH | Information Technology | 336,354 | 40,819 | 221.6% | 13 | 13.1% | 15 | 28 |
| 2 | Zensar Technolgies Ltd. | ZENSARTECH | Information Technology | 9,851 | 839 | 160.4% | 21 | 11.4% | 18 | 39 |
| 3 | Birlasoft Ltd. | BSOFT | Information Technology | 7,543 | 803 | 97.0% | 41 | 15.3% | 7 | 48 |
| 4 | BLS International Services Ltd. | BLS | Consumer Services | 8,910 | 756 | 165.1% | 19 | 9.3% | 29 | 48 |
| 5 | KPIT Technologies Ltd. | KPITTECH | Information Technology | 13,394 | 1,045 | 166.7% | 18 | 8.2% | 35 | 53 |
| 6 | Wipro Ltd. | WIPRO | Information Technology | 157,650 | 14,913 | 90.8% | 44 | 12.0% | 16 | 60 |
| 7 | Castrol India Ltd. | CASTROLIND | Oil Gas & Consumable Fuels | 19,687 | 1,249 | 308.6% | 7 | 6.7% | 53 | 60 |
| 8 | Tata Consultancy Services Ltd. | TCS | Information Technology | 750,753 | 67,022 | 111.1% | 35 | 9.3% | 28 | 63 |
| 9 | Infosys Ltd. | INFY | Information Technology | 419,211 | 38,582 | 101.4% | 40 | 9.8% | 24 | 64 |
| 10 | Sun TV Network Ltd. | SUNTV | Media Entertainment & Publication | 23,641 | 1,498 | 94.0% | 42 | 8.7% | 30 | 72 |
| 11 | ITC Ltd. | ITC | Fast Moving Consumer Goods | 320,656 | 25,596 | 79.1% | 50 | 8.5% | 31 | 81 |
| 12 | Hexaware Technologies Ltd. | HEXT | Information Technology | 29,907 | 1,841 | 129.2% | 27 | 6.5% | 58 | 85 |
| 13 | Hero MotoCorp Ltd. | HEROMOTOCO | Automobile and Auto Components | 103,433 | 6,204 | 104.8% | 37 | 6.8% | 51 | 88 |
| 14 | Hindustan Zinc Ltd. | HINDZINC | Metals & Mining | 234,526 | 18,495 | 76.8% | 52 | 8.1% | 39 | 91 |
| 15 | National Aluminium Co. Ltd. | NATIONALUM | Metals & Mining | 61,509 | 7,212 | 50.8% | 79 | 13.5% | 13 | 92 |
| 16 | MphasiS Ltd. | MPHASIS | Information Technology | 42,938 | 2,428 | 117.5% | 32 | 5.7% | 71 | 103 |
| 17 | RITES Ltd. | RITES | Construction | 10,068 | 499 | 74.6% | 57 | 6.9% | 49 | 106 |
| 18 | Avanti Feeds Ltd. | AVANTIFEED | Fast Moving Consumer Goods | 9,695 | 689 | 53.3% | 75 | 8.1% | 38 | 113 |
| 19 | Ashok Leyland Ltd. | ASHOKLEY | Capital Goods | 88,390 | 11,001 | 55.4% | 72 | 7.9% | 42 | 114 |
| 20 | Chennai Petroleum Corporation Ltd. | CHENNPETRO | Oil Gas & Consumable Fuels | 20,049 | 4,460 | 35.8% | 112 | 21.4% | 3 | 115 |

## Findings

- **Top 20 vs ranked universe (medians):** ROC 99.2% vs 24.0%; EY 8.6% vs 3.3%.
- **ROC and EY ranks are positively correlated (Spearman +0.18).** Positive means high-quality businesses are not systematically priced higher here, which makes it easier to find names good on both.
- **Sector concentration of the top 20:**
- Information Technology: 9
- Oil Gas & Consumable Fuels: 2
- Fast Moving Consumer Goods: 2
- Metals & Mining: 2
- Consumer Services: 1
- Media Entertainment & Publication: 1
- Automobile and Auto Components: 1
- Construction: 1
- Capital Goods: 1
- **High ROC but too expensive to make the top 20:**
- Brookfield India Real Estate Trust (BIRET): ROC 1,687.2% (rank 2), EY 4.3% (rank 123) → overall #27
- Oracle Financial Services Software Ltd. (OFSS): ROC 328.6% (rank 5), EY 4.0% (rank 131) → overall #36
- Abbott India Ltd. (ABBOTINDIA): ROC 421.0% (rank 3), EY 3.3% (rank 183) → overall #63
- Inventurus Knowledge Solutions Ltd. (IKS): ROC 327.5% (rank 6), EY 3.0% (rank 196) → overall #67
- Glaxosmithkline Pharmaceuticals Ltd. (GLAXO): ROC 407.1% (rank 4), EY 2.8% (rank 214) → overall #75
- Affle 3i Ltd. (AFFLE): ROC 289.4% (rank 9), EY 2.7% (rank 225) → overall #87
- TBO Tek Ltd. (TBOTEK): ROC 303.4% (rank 8), EY 2.0% (rank 270) → overall #117
- Info Edge (India) Ltd. (NAUKRI): ROC 282.2% (rank 10), EY 1.4% (rank 311) → overall #146
- Indiamart Intermesh Ltd. (INDIAMART): ROC 2,343.5% (rank 1), EY 0.5% (rank 342) → overall #174
- **Cheap but low quality, so they miss the top 20:**
- Bharat Petroleum Corporation Ltd. (BPCL): ROC 34.2% (rank 121), EY 23.0% (rank 1) → overall #23
- NMDC Ltd. (NMDC): ROC 33.4% (rank 124), EY 14.4% (rank 10) → overall #32
- Coal India Ltd. (COALINDIA): ROC 28.1% (rank 152), EY 14.7% (rank 9) → overall #48
- Indian Oil Corporation Ltd. (IOC): ROC 23.4% (rank 178), EY 21.9% (rank 2) → overall #61
- Hindustan Petroleum Corporation Ltd. (HINDPETRO): ROC 23.0% (rank 184), EY 19.6% (rank 4) → overall #64
- Chambal Fertilizers & Chemicals Ltd. (CHAMBLFERT): ROC 21.8% (rank 193), EY 14.8% (rank 8) → overall #65
- NCC Ltd. (NCC): ROC 20.6% (rank 201), EY 16.7% (rank 6) → overall #70
- Oil & Natural Gas Corporation Ltd. (ONGC): ROC 18.2% (rank 229), EY 18.0% (rank 5) → overall #85
- Statement dates behind the top 20: {'2026-03-31': 18, '2025-12-31': 2}. EBIT fell back to Yahoo's EBIT line (includes other income) for 0 of them.

## How to check a number

### Worked example: #1 HCL Technologies Ltd. (HCLTECH)

Every number below is in INR crore, from Yahoo Finance annual statements dated 2026-03-31.

**1. EBIT** (Operating Income) = **40,819**

**2. Net working capital**
```
  Current assets                          70,542
- Cash & short-term investments           30,615
- Current liabilities                     31,826
+ Short-term debt (financing, not operating)         1,998
= NWC (raw)                               10,099
  NWC used (floored at 0)                 10,099
```

**3. Capital employed** = NWC 10,099 + Net fixed assets (Net PP&E) 8,321 = **18,420**

**4. Return on capital** = 40,819 / 18,420 = **221.6%** → ROC rank **13**

**5. Enterprise value**
```
  Market cap                             336,354
+ Total debt                               5,215
+ Minority interest                           32
+ Preferred equity                             0
- Cash & short-term investments           30,615
= Enterprise value                       310,986
```

**6. Earnings yield** = 40,819 / 310,986 = **13.1%** → EY rank **15**

**7. Combined score** = 13 + 15 = **28** → overall rank **#1**


To audit any other company: find its row in `output/04_metrics.csv` (every intermediate column), then its source line items in `output/02_raw_financials.csv` (the `__src` columns name the Yahoo row each value came from).

## Caveats — read before acting on this

1. **Consolidated finance arms distort some names.** Companies that consolidate a lending subsidiary (e.g. Ashok Leyland → Hinduja Leyland Finance) carry that lender's borrowings in total debt and its interest income in EBIT. Check these against standalone figures.
1. **Yahoo Finance data is unaudited and sometimes wrong** for Indian companies (misclassified line items, missing current debt, consolidated vs standalone mix-ups). Check any name you intend to buy against its annual report.
2. **Annual, not trailing-twelve-month, EBIT.** Greenblatt uses TTM. By September the March-year figures are six months old.
3. **Cyclicals look best at the peak.** Metals, oil & gas, and commodity names show high EY exactly when earnings are at their top. A one-year EBIT snapshot cannot tell peak from normal earnings.
4. **PSUs.** State-owned companies often screen cheap for structural reasons (government ownership, policy-driven pricing, dividend extraction). The formula does not account for that.
5. **The strategy's edge depends on holding a basket** (Greenblatt: 20–30 names, rebalanced yearly, held through years of underperformance). A single screen is a starting list for research, not a portfolio.
