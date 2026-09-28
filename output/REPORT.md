# Magic Formula screen — Indian equities

Generated 2026-09-28 · universe: NSE Nifty 500 (https://archives.nseindia.com/content/indices/ind_nifty500list.csv) · data: Yahoo Finance (latest annual statements, current market cap)

## Method (Joel Greenblatt, *The Little Book That Beats the Market*)

| Metric | Formula | What it measures |
|---|---|---|
| Return on capital (ROC) | EBIT ÷ (Net working capital + Net fixed assets) | Quality: profit per rupee of tangible capital the business needs |
| Earnings yield (EY) | EBIT ÷ Enterprise value | Price: profit per rupee paid for the whole business |
| Combined score | ROC rank + EY rank | Lowest = good business at a cheap price |

Parameters: minimum market cap Rs 5,000 cr · statements no older than 550 days · financials and utilities excluded · holding companies excluded where book minority interest > 20% of market cap.

## Funnel: how 501 companies became 350

| Step | Companies removed | Remaining |
|---|---:|---:|
| Starting universe | – | 501 |
| financial / utility (excluded by method) | 123 | 378 |
| market cap below Rs 5,000 cr | 1 | 377 |
| missing market cap | 1 | 376 |
| missing balance-sheet items for ROC | 1 | 375 |
| EBIT <= 0 (loss-making at operating level) | 20 | 355 |
| holding company: minority interest > 20% of market cap (EV unreliable) | 5 | 350 |
| **Ranked** | | **350** |

Full list of exclusions with reasons: `output/03_exclusions.csv`.

## Top 20

| # | Company | Symbol | Sector | Mkt cap (cr) | EBIT (cr) | ROC | ROC rank | EY | EY rank | Score |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | HCL Technologies Ltd. | HCLTECH | Information Technology | 337,626 | 40,819 | 221.6% | 14 | 13.1% | 14 | 28 |
| 2 | Sonata Software Ltd. | SONATSOFTW | Information Technology | 7,617 | 690 | 336.9% | 4 | 8.9% | 31 | 35 |
| 3 | Zensar Technolgies Ltd. | ZENSARTECH | Information Technology | 9,926 | 839 | 160.4% | 25 | 11.3% | 18 | 43 |
| 4 | Birlasoft Ltd. | BSOFT | Information Technology | 7,675 | 803 | 97.0% | 45 | 14.9% | 7 | 52 |
| 5 | BLS International Services Ltd. | BLS | Consumer Services | 9,167 | 756 | 165.1% | 22 | 9.0% | 30 | 52 |
| 6 | KPIT Technologies Ltd. | KPITTECH | Information Technology | 13,877 | 1,045 | 166.7% | 21 | 7.9% | 38 | 59 |
| 7 | Castrol India Ltd. | CASTROLIND | Oil Gas & Consumable Fuels | 19,971 | 1,249 | 308.6% | 7 | 6.6% | 53 | 60 |
| 8 | Wipro Ltd. | WIPRO | Information Technology | 160,866 | 14,913 | 90.8% | 48 | 11.7% | 16 | 64 |
| 9 | Sun TV Network Ltd. | SUNTV | Media Entertainment & Publication | 20,546 | 1,498 | 94.0% | 46 | 10.7% | 20 | 66 |
| 10 | Infosys Ltd. | INFY | Information Technology | 405,196 | 38,582 | 101.4% | 44 | 10.2% | 23 | 67 |
| 11 | Tata Consultancy Services Ltd. | TCS | Information Technology | 750,970 | 67,022 | 111.1% | 39 | 9.3% | 29 | 68 |
| 12 | Pfizer Ltd. | PFIZER | Healthcare | 18,160 | 847 | 304.2% | 8 | 5.6% | 76 | 84 |
| 13 | ITC Ltd. | ITC | Fast Moving Consumer Goods | 333,625 | 25,596 | 79.1% | 55 | 8.2% | 33 | 88 |
| 14 | Hexaware Technologies Ltd. | HEXT | Information Technology | 29,855 | 1,841 | 129.2% | 31 | 6.5% | 57 | 88 |
| 15 | Hindustan Zinc Ltd. | HINDZINC | Metals & Mining | 241,984 | 18,495 | 76.8% | 57 | 7.8% | 40 | 97 |
| 16 | Hero MotoCorp Ltd. | HEROMOTOCO | Automobile and Auto Components | 107,276 | 6,204 | 104.8% | 41 | 6.5% | 56 | 97 |
| 17 | National Aluminium Co. Ltd. | NATIONALUM | Metals & Mining | 63,805 | 7,212 | 50.8% | 84 | 13.0% | 15 | 99 |
| 18 | RITES Ltd. | RITES | Construction | 9,475 | 499 | 74.6% | 62 | 7.5% | 44 | 106 |
| 19 | MphasiS Ltd. | MPHASIS | Information Technology | 42,554 | 2,428 | 117.5% | 36 | 5.8% | 71 | 107 |
| 20 | Ashok Leyland Ltd. | ASHOKLEY | Capital Goods | 91,744 | 11,001 | 55.4% | 78 | 7.7% | 42 | 120 |

## Findings

- **Top 20 vs ranked universe (medians):** ROC 107.9% vs 24.1%; EY 8.6% vs 3.4%.
- **ROC and EY ranks are positively correlated (Spearman +0.17).** Positive means high-quality businesses are not systematically priced higher here, which makes it easier to find names good on both.
- **Sector concentration of the top 20:**
- Information Technology: 10
- Metals & Mining: 2
- Consumer Services: 1
- Oil Gas & Consumable Fuels: 1
- Media Entertainment & Publication: 1
- Healthcare: 1
- Fast Moving Consumer Goods: 1
- Automobile and Auto Components: 1
- Construction: 1
- Capital Goods: 1
- **High ROC but too expensive to make the top 20:**
- Oracle Financial Services Software Ltd. (OFSS): ROC 328.6% (rank 5), EY 3.9% (rank 143) → overall #39
- Abbott India Ltd. (ABBOTINDIA): ROC 421.0% (rank 2), EY 3.3% (rank 178) → overall #60
- Inventurus Knowledge Solutions Ltd. (IKS): ROC 327.5% (rank 6), EY 3.0% (rank 196) → overall #71
- Glaxosmithkline Pharmaceuticals Ltd. (GLAXO): ROC 407.1% (rank 3), EY 2.7% (rank 230) → overall #83
- Affle 3i Ltd. (AFFLE): ROC 289.4% (rank 10), EY 2.5% (rank 248) → overall #100
- TBO Tek Ltd. (TBOTEK): ROC 303.4% (rank 9), EY 2.0% (rank 277) → overall #122
- Indiamart Intermesh Ltd. (INDIAMART): ROC 2,343.5% (rank 1), EY 0.5% (rank 344) → overall #170
- **Cheap but low quality, so they miss the top 20:**
- Chennai Petroleum Corporation Ltd. (CHENNPETRO): ROC 35.8% (rank 119), EY 20.4% (rank 3) → overall #21
- Bharat Petroleum Corporation Ltd. (BPCL): ROC 34.2% (rank 127), EY 22.9% (rank 1) → overall #23
- NMDC Ltd. (NMDC): ROC 33.4% (rank 129), EY 13.6% (rank 10) → overall #31
- Coal India Ltd. (COALINDIA): ROC 28.1% (rank 153), EY 14.5% (rank 8) → overall #47
- Indian Oil Corporation Ltd. (IOC): ROC 23.4% (rank 179), EY 21.6% (rank 2) → overall #61
- Hindustan Petroleum Corporation Ltd. (HINDPETRO): ROC 23.0% (rank 185), EY 19.6% (rank 4) → overall #63
- Chambal Fertilizers & Chemicals Ltd. (CHAMBLFERT): ROC 21.8% (rank 193), EY 14.2% (rank 9) → overall #70
- NCC Ltd. (NCC): ROC 20.6% (rank 203), EY 16.6% (rank 6) → overall #73
- Oil & Natural Gas Corporation Ltd. (ONGC): ROC 18.2% (rank 231), EY 17.5% (rank 5) → overall #87
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
  Market cap                             337,626
+ Total debt                               5,215
+ Minority interest                           32
+ Preferred equity                             0
- Cash & short-term investments           30,615
= Enterprise value                       312,258
```

**6. Earnings yield** = 40,819 / 312,258 = **13.1%** → EY rank **14**

**7. Combined score** = 14 + 14 = **28** → overall rank **#1**


To audit any other company: find its row in `output/04_metrics.csv` (every intermediate column), then its source line items in `output/02_raw_financials.csv` (the `__src` columns name the Yahoo row each value came from).

## Caveats — read before acting on this

1. **Consolidated finance arms distort some names.** Companies that consolidate a lending subsidiary (e.g. Ashok Leyland → Hinduja Leyland Finance) carry that lender's borrowings in total debt and its interest income in EBIT. Check these against standalone figures.
1. **Yahoo Finance data is unaudited and sometimes wrong** for Indian companies (misclassified line items, missing current debt, consolidated vs standalone mix-ups). Check any name you intend to buy against its annual report.
2. **Annual, not trailing-twelve-month, EBIT.** Greenblatt uses TTM. By September the March-year figures are six months old.
3. **Cyclicals look best at the peak.** Metals, oil & gas, and commodity names show high EY exactly when earnings are at their top. A one-year EBIT snapshot cannot tell peak from normal earnings.
4. **PSUs.** State-owned companies often screen cheap for structural reasons (government ownership, policy-driven pricing, dividend extraction). The formula does not account for that.
5. **The strategy's edge depends on holding a basket** (Greenblatt: 20–30 names, rebalanced yearly, held through years of underperformance). A single screen is a starting list for research, not a portfolio.
