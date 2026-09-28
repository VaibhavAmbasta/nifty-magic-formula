# Magic Formula screen — Indian equities

Generated 2026-09-28 · universe: NSE Nifty 500 (https://archives.nseindia.com/content/indices/ind_nifty500list.csv) · data: Yahoo Finance (latest annual statements, current market cap)

## Method (Joel Greenblatt, *The Little Book That Beats the Market*)

| Metric | Formula | What it measures |
|---|---|---|
| Return on capital (ROC) | EBIT ÷ (Net working capital + Net fixed assets) | Quality: profit per rupee of tangible capital the business needs |
| Earnings yield (EY) | EBIT ÷ Enterprise value | Price: profit per rupee paid for the whole business |
| Combined score | ROC rank + EY rank | Lowest = good business at a cheap price |

Parameters: minimum market cap Rs 5,000 cr · statements no older than 550 days · financials and utilities excluded · holding companies excluded where book minority interest > 20% of market cap.

## Funnel: how 501 companies became 340

| Step | Companies removed | Remaining |
|---|---:|---:|
| Starting universe | – | 501 |
| financial / utility (excluded by method) | 123 | 378 |
| missing market cap | 11 | 367 |
| market cap below Rs 5,000 cr | 1 | 366 |
| missing balance-sheet items for ROC | 1 | 365 |
| EBIT <= 0 (loss-making at operating level) | 20 | 345 |
| holding company: minority interest > 20% of market cap (EV unreliable) | 5 | 340 |
| **Ranked** | | **340** |

Full list of exclusions with reasons: `output/03_exclusions.csv`.

## Top 20

| # | Company | Symbol | Sector | Mkt cap (cr) | EBIT (cr) | ROC | ROC rank | EY | EY rank | Score |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | HCL Technologies Ltd. | HCLTECH | Information Technology | 337,788 | 40,819 | 221.6% | 14 | 13.1% | 13 | 27 |
| 2 | Sonata Software Ltd. | SONATSOFTW | Information Technology | 7,624 | 690 | 336.9% | 4 | 8.9% | 29 | 33 |
| 3 | Zensar Technolgies Ltd. | ZENSARTECH | Information Technology | 9,977 | 839 | 160.4% | 25 | 11.2% | 17 | 42 |
| 4 | Birlasoft Ltd. | BSOFT | Information Technology | 7,679 | 803 | 97.0% | 43 | 14.9% | 6 | 49 |
| 5 | BLS International Services Ltd. | BLS | Consumer Services | 9,160 | 756 | 165.1% | 22 | 9.0% | 28 | 50 |
| 6 | KPIT Technologies Ltd. | KPITTECH | Information Technology | 13,908 | 1,045 | 166.7% | 21 | 7.9% | 35 | 56 |
| 7 | Castrol India Ltd. | CASTROLIND | Oil Gas & Consumable Fuels | 19,980 | 1,249 | 308.6% | 7 | 6.6% | 50 | 57 |
| 8 | Wipro Ltd. | WIPRO | Information Technology | 160,885 | 14,913 | 90.8% | 46 | 11.7% | 15 | 61 |
| 9 | Sun TV Network Ltd. | SUNTV | Media Entertainment & Publication | 20,524 | 1,498 | 94.0% | 44 | 10.7% | 19 | 63 |
| 10 | Infosys Ltd. | INFY | Information Technology | 405,439 | 38,582 | 101.4% | 42 | 10.2% | 22 | 64 |
| 11 | Pfizer Ltd. | PFIZER | Healthcare | 18,148 | 847 | 304.2% | 8 | 5.6% | 72 | 80 |
| 12 | Hexaware Technologies Ltd. | HEXT | Information Technology | 29,874 | 1,841 | 129.2% | 30 | 6.5% | 54 | 84 |
| 13 | ITC Ltd. | ITC | Fast Moving Consumer Goods | 333,688 | 25,596 | 79.1% | 53 | 8.2% | 32 | 85 |
| 14 | Hero MotoCorp Ltd. | HEROMOTOCO | Automobile and Auto Components | 107,086 | 6,204 | 104.8% | 39 | 6.5% | 53 | 92 |
| 15 | Hindustan Zinc Ltd. | HINDZINC | Metals & Mining | 242,660 | 18,495 | 76.8% | 55 | 7.8% | 38 | 93 |
| 16 | National Aluminium Co. Ltd. | NATIONALUM | Metals & Mining | 63,832 | 7,212 | 50.8% | 81 | 13.0% | 14 | 95 |
| 17 | RITES Ltd. | RITES | Construction | 9,462 | 499 | 74.6% | 60 | 7.5% | 41 | 101 |
| 18 | MphasiS Ltd. | MPHASIS | Information Technology | 42,617 | 2,428 | 117.5% | 35 | 5.8% | 67 | 102 |
| 19 | Chennai Petroleum Corporation Ltd. | CHENNPETRO | Oil Gas & Consumable Fuels | 21,147 | 4,460 | 35.8% | 116 | 20.3% | 2 | 118 |
| 20 | Newgen Software Technologies Ltd. | NEWGEN | Information Technology | 6,790 | 378 | 63.5% | 71 | 6.6% | 48 | 119 |

## Findings

- **Top 20 vs ranked universe (medians):** ROC 103.1% vs 24.1%; EY 8.5% vs 3.3%.
- **ROC and EY ranks are positively correlated (Spearman +0.16).** Positive means high-quality businesses are not systematically priced higher here, which makes it easier to find names good on both.
- **Sector concentration of the top 20:**
- Information Technology: 10
- Oil Gas & Consumable Fuels: 2
- Metals & Mining: 2
- Consumer Services: 1
- Media Entertainment & Publication: 1
- Healthcare: 1
- Fast Moving Consumer Goods: 1
- Automobile and Auto Components: 1
- Construction: 1
- **High ROC but too expensive to make the top 20:**
- Oracle Financial Services Software Ltd. (OFSS): ROC 328.6% (rank 5), EY 3.9% (rank 138) → overall #37
- Abbott India Ltd. (ABBOTINDIA): ROC 421.0% (rank 2), EY 3.3% (rank 172) → overall #58
- Inventurus Knowledge Solutions Ltd. (IKS): ROC 327.5% (rank 6), EY 3.0% (rank 190) → overall #69
- Glaxosmithkline Pharmaceuticals Ltd. (GLAXO): ROC 407.1% (rank 3), EY 2.7% (rank 224) → overall #82
- Affle 3i Ltd. (AFFLE): ROC 289.4% (rank 10), EY 2.5% (rank 241) → overall #99
- TBO Tek Ltd. (TBOTEK): ROC 303.4% (rank 9), EY 2.0% (rank 269) → overall #118
- Indiamart Intermesh Ltd. (INDIAMART): ROC 2,343.5% (rank 1), EY 0.5% (rank 335) → overall #166
- **Cheap but low quality, so they miss the top 20:**
- Bharat Petroleum Corporation Ltd. (BPCL): ROC 34.2% (rank 124), EY 22.8% (rank 1) → overall #22
- NMDC Ltd. (NMDC): ROC 33.4% (rank 126), EY 13.6% (rank 9) → overall #31
- Coal India Ltd. (COALINDIA): ROC 28.1% (rank 149), EY 14.5% (rank 7) → overall #45
- Hindustan Petroleum Corporation Ltd. (HINDPETRO): ROC 23.0% (rank 179), EY 19.6% (rank 3) → overall #59
- Chambal Fertilizers & Chemicals Ltd. (CHAMBLFERT): ROC 21.8% (rank 187), EY 14.2% (rank 8) → overall #67
- NCC Ltd. (NCC): ROC 20.6% (rank 197), EY 16.6% (rank 5) → overall #70
- Mangalore Refinery & Petrochemicals Ltd. (MRPL): ROC 20.2% (rank 202), EY 13.4% (rank 10) → overall #75
- Oil & Natural Gas Corporation Ltd. (ONGC): ROC 18.2% (rank 225), EY 17.5% (rank 4) → overall #85
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

**4. Return on capital** = 40,819 / 18,420 = **221.6%** → ROC rank **14**

**5. Enterprise value**
```
  Market cap                             337,788
+ Total debt                               5,215
+ Minority interest                           32
+ Preferred equity                             0
- Cash & short-term investments           30,615
= Enterprise value                       312,420
```

**6. Earnings yield** = 40,819 / 312,420 = **13.1%** → EY rank **13**

**7. Combined score** = 14 + 13 = **27** → overall rank **#1**


To audit any other company: find its row in `output/04_metrics.csv` (every intermediate column), then its source line items in `output/02_raw_financials.csv` (the `__src` columns name the Yahoo row each value came from).

## Caveats — read before acting on this

1. **Consolidated finance arms distort some names.** Companies that consolidate a lending subsidiary (e.g. Ashok Leyland → Hinduja Leyland Finance) carry that lender's borrowings in total debt and its interest income in EBIT. Check these against standalone figures.
1. **Yahoo Finance data is unaudited and sometimes wrong** for Indian companies (misclassified line items, missing current debt, consolidated vs standalone mix-ups). Check any name you intend to buy against its annual report.
2. **Annual, not trailing-twelve-month, EBIT.** Greenblatt uses TTM. By September the March-year figures are six months old.
3. **Cyclicals look best at the peak.** Metals, oil & gas, and commodity names show high EY exactly when earnings are at their top. A one-year EBIT snapshot cannot tell peak from normal earnings.
4. **PSUs.** State-owned companies often screen cheap for structural reasons (government ownership, policy-driven pricing, dividend extraction). The formula does not account for that.
5. **The strategy's edge depends on holding a basket** (Greenblatt: 20–30 names, rebalanced yearly, held through years of underperformance). A single screen is a starting list for research, not a portfolio.
