# Custom Alert Builder Screenshot Findings

## Source

User-provided screenshot of the Unusual Whales custom alert builder primer / UI.

## What the screenshot confirms

The screenshot confirms that the UW custom alert builder supports a meaningful set of quantitative contract-level filters.

Visible left-side alert categories:

```text
Options
- Chain OI Change
- Flow alerts
- Contract alert
- Interval alert
- Option Trade alert

Stocks
Macro & Other
AI Alert Builder
```

Visible targeting modes:

```text
All
Ticker
Watchlist
Portfolio
Option Chains
```

Visible Contract Alert filters:

```text
Avg Fill $
Close $
Days of Vol > OI
Days of OI Increase
Days To Expiry
Earnings Report
From Low
From High
Market Cap
OI Change
OI Change %
Open Interest
Premium
Spread
Stock Price
Strike Price
Volume
Volume / OI Ratio
Bearish Prem %
Bullish Prem %
Daily % Change
```

## Why this matters

This clears up a major question: the GUI custom alert builder can approximate a large portion of the original API scoring model without code.

The visible filters map directly to UW-Signals components:

| UW-Signals need | Custom Alert field |
|---|---|
| DTE filter | Days To Expiry |
| Premium threshold | Premium |
| Spread / execution quality | Spread |
| Liquidity | Volume, Open Interest |
| Unusual volume | Volume / OI Ratio, Days of Vol > OI |
| OI confirmation | OI Change, OI Change %, Days of OI Increase |
| Directional premium bias | Bullish Prem %, Bearish Prem % |
| Underlying level context | Stock Price |
| Strike targeting | Strike Price |
| Momentum / distance context | From Low, From High, Daily % Change |
| Earnings risk | Earnings Report |
| Market-cap filter | Market Cap |
| Targeting specific symbols | Ticker / Watchlist |
| Targeting option chains | Option Chains |

## What remains unknown from screenshot alone

The screenshot does not fully confirm:

```text
Whether the Server plan can post these custom alerts automatically to Discord.
Whether alert results are posted with enough structured detail for a Python Discord parser.
Whether Option Trade Alert includes ask/bid-side, multi-leg, sweep/block, OTM, call/put, and ticker/watchlist filters.
Whether Flow Alerts have a separate filter set with side, DTE, premium, and flags.
Whether Market Tide / Net Flow can be combined directly with contract alerts in one alert.
Whether alerts can require multiple categories at once or must be built as separate alert templates.
```

## Interpretation

This screenshot strongly supports trying the lower-cost GUI/Server workflow before API Advanced.

The GUI can likely create high-signal alert templates around:

```text
0DTE
premium threshold
spread control
volume/open-interest confirmation
bullish/bearish premium concentration
volume/OI ratio
OI change
watchlist/ticker targeting
```

## Practical alert-builder direction

### SPX 0DTE A+ Call Contract Alert

```text
For: Ticker = SPX
Days To Expiry: Min 0 / Max 0
Premium: Min 50000
Spread: Max user-defined acceptable value after observing SPX spreads
Volume / OI Ratio: Min 1.5 or 2.0
Bullish Prem %: Min 70
Bearish Prem %: Max 30
Earnings Report: ignore for SPX
From High: use cautiously after observing scale
```

### SPX 0DTE A+ Put Contract Alert

```text
For: Ticker = SPX
Days To Expiry: Min 0 / Max 0
Premium: Min 50000
Spread: Max user-defined acceptable value after observing SPX spreads
Volume / OI Ratio: Min 1.5 or 2.0
Bearish Prem %: Min 70
Bullish Prem %: Max 30
```

### QQQ 0DTE A+ Call Contract Alert

```text
For: Ticker = QQQ
Days To Expiry: Min 0 / Max 0
Premium: Min 25000
Spread: Max user-defined acceptable value
Volume / OI Ratio: Min 1.5 or 2.0
Bullish Prem %: Min 70
Bearish Prem %: Max 30
```

### QQQ 0DTE A+ Put Contract Alert

```text
For: Ticker = QQQ
Days To Expiry: Min 0 / Max 0
Premium: Min 25000
Spread: Max user-defined acceptable value
Volume / OI Ratio: Min 1.5 or 2.0
Bearish Prem %: Min 70
Bullish Prem %: Max 30
```

### NVDA / TSLA Momentum Contract Alert

```text
For: Ticker = NVDA or TSLA
Days To Expiry: Min 0 / Max 7
Premium: Min 50000
Spread: Max user-defined acceptable value
Volume / OI Ratio: Min 1.5 or 2.0
Open Interest: Min 100 or 250 depending on ticker
Bullish Prem % Min 70 for call-bias alert
Bearish Prem % Min 70 for put-bias alert
Earnings Report: exclude or handle separately
```

## Revised plan

The lower-cost path is now:

```text
Server or Professional plan
→ custom alert templates
→ Discord/mobile alert delivery
→ optional Python Discord parser
→ manual/semiautomated 5-minute summaries
→ upgrade to API only if GUI/Discord limitations become blockers
```

## Final note

This screenshot does not prove every API feature is replaceable, but it proves the custom alert builder has enough quantitative contract filters to justify testing the cheaper plan first.
