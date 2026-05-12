# MVP Scoring Rules

## Purpose

Every opportunity receives a 0–100 score.

The score is not a guarantee. It is a structured way to decide whether enough independent evidence aligns to justify an alert.

## Score weights

| Category | Max points | Source modules |
|---|---:|---|
| Directional flow | 25 | `features_flow.py` |
| Market confirmation | 20 | UW Market Tide, ETF Tide, Net Flow |
| Dealer/GEX context | 20 | `features_gex.py` |
| Contract quality | 15 | `features_contract.py` |
| Price action | 10 | `features_price.py` |
| Risk filter | 10 | `risk_filters.py` |

## Alert bands

```text
90–100 = Apex alert
85–89  = Strong alert
78–84  = Watch only
Below 78 = No alert
```

## Directional flow — 25 points

Use:

```text
Full Tape / Option Trades
Flow Alerts
Flow per Expiry
Flow per Strike
Flow per Strike Intraday
Recent Flows
Greek Flow
```

Evidence:

```text
Aggressive call/put premium
Repeated same-direction flow
Same-strike clustering
0DTE concentration
Volume acceleration
Premium concentration
```

## Market confirmation — 20 points

Use:

```text
Market Tide
ETF Tide
Net Flow
Sector/ETF confirmation for single stocks
```

Evidence:

```text
SPY/QQQ/IWM tide agrees with trade direction
Net Flow agrees over 5m/15m windows
Single-stock flow aligns with sector/index pressure
```

## Dealer/GEX context — 20 points

Use:

```text
GEX / Greek Exposure
Spot GEX exposures
Greek Flow
Gamma flip / wall proximity if available
```

Evidence:

```text
Continuation regime supports breakout
Range/pin regime supports fade
Room exists to next opposing wall
Price is not chasing directly into resistance/support wall
```

## Contract quality — 15 points

Use:

```text
Option Chain
Greeks
Bid/ask spread
Volume
Open interest
IV
```

Evidence:

```text
Spread acceptable
Volume/OI sufficient
Delta usable
Theta risk manageable
IV expansion supports the setup
Exit liquidity likely exists
```

## Price action — 10 points

Use:

```text
Stock price stream / OHLC
VWAP
Prior high/low
Breakout/retest levels
```

Evidence:

```text
Underlying confirms direction
Breakout/retest confirms flow
There is room to target
Price is not trapped between walls
```

## Risk filter — 10 points

Use:

```text
News headlines
Economic calendar
Earnings calendar
Trading halt stream
Spread
Time of day
Recent failed alerts
```

Risk blocks:

```text
Wide spreads
Headline/macro event risk
Earnings risk
Halt risk
Late-day theta danger
Two failed same-direction alerts
Mixed flow
```

## Final rule

No signal should be sent just because one category scores highly.

A valid alert requires balanced evidence across flow, market confirmation, GEX/dealer context, contract quality, price confirmation, and risk controls.
