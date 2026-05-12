# MVP Risk Filters

## Purpose

Risk filters prevent the system from sending attractive-looking alerts when execution conditions are poor or the market context is dangerous.

The risk engine should block or downgrade alerts before they reach the trader.

## Primary risk filters

| Filter | Action | Reason |
|---|---|---|
| Wide spread | Block or downgrade | 0DTE options can lose edge immediately through poor fills |
| Missing spread | Downgrade | System cannot evaluate execution quality |
| News headline risk | Block | Headline moves can reverse quickly and invalidate flow logic |
| Economic event risk | Block | CPI/FOMC/NFP and similar events can overwhelm flow/GEX context |
| Earnings risk | Block for normal strategy | Single-stock options behave differently around earnings |
| Halt risk | Block | Cannot safely manage option contracts around halts |
| Late-day theta danger | Downgrade or block | 0DTE premium decays aggressively late in the session |
| Mixed flow | Downgrade | Conflicting evidence reduces probability |
| Two failed same-direction alerts | Block | Prevents repeated losses in a changing regime |

## Current implementation

Module:

```text
src/risk_filters.py
```

Function:

```python
evaluate_basic_risk_filters()
```

Current MVP behavior:

```text
spread_pct > 12%       = block
spread_pct 8%–12%      = downgrade
headline/news risk     = block
earnings risk          = block
halt risk              = block
>=2 failed same-side alerts = block
after 3:30 PM          = downgrade for theta danger
```

## Why risk filters come after scoring inputs

A trade may score well on flow, GEX, and price action, but still be untradable if:

```text
The spread is too wide.
A macro event is imminent.
The contract is illiquid.
The alert comes too late in the session.
The same setup already failed twice.
```

## Future enhancements

```text
Dynamic spread thresholds by ticker
Separate SPX/SPY/QQQ/stock risk profiles
News severity scoring
Economic calendar integration
Earnings-event mode instead of full block
Max daily alert count
Max daily loss / lockout state
Broker execution slippage tracking
Real-time halt subscription handling
```

## Final rule

The system should prefer missing a trade over alerting on a low-quality, high-risk setup.
