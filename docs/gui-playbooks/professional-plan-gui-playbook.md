# UW Professional Plan GUI Playbook

## Purpose

Translate the original API-based UW-Signals roadmap into a manual/semi-manual workflow inside the Unusual Whales Professional GUI.

This playbook is for validating the trading logic before paying for API Advanced.

## Core conclusion

The Professional plan cannot replace API automation, but it can approximate the decision process manually using:

```text
Options Flow filters
Flow Alerts
Custom Alerts
Super Flow Dashboards
Watchlists
Periscope / SPX market maker exposure and delta flow
Greeks and volatility dashboards
Dark pool data
Nasdaq real-time equities data
Discord/mobile push workflow
Manual trade journal
```

## Key limitation

The GUI cannot calculate a fully custom 0–100 score automatically across all layers.

Instead, we create saved filters and dashboards that visually represent the same layers:

```text
Regime → Flow → Dealer/GEX Context → Contract Quality → Price Confirmation → Risk Filter → Alert → Manual Outcome Log
```

## Official documentation anchors

Unusual Whales docs state:

```text
The Options Flow tool catches and displays trade details for all options orders across all options exchanges.
Flow fields include ticker, contract, bid-ask, spot, size, premium, OI, volume, IV, code, flags, DTE, and % diff.
BUY/SELL side labels are estimates based on fill location versus NBBO.
Not all BUY orders are buy-to-open and not all SELL orders are sell-to-open.
Trades may be part of multi-leg strategies.
A green flow status means all trades matching current filters are pushed live, except possible extreme open/close volume.
UW alerts are not buy/sell signals and do not provide entries/exits.
```

## Workflow translation table

| API system layer | GUI replacement | Manual action |
|---|---|---|
| REST/WebSocket option trades | Live Options Flow feed | Use saved filters and keep Flow Status green/yellow |
| Flow Alerts endpoint | Flow Alerts feed / custom alerts | Use as triggers, not entries |
| Market Tide / ETF Tide / Net Flow | Market/ETF tide widgets, Super Flow, dashboards | Confirm broad direction |
| GEX / Greek exposure | Periscope / SPX exposure / delta flow / Greeks dashboards | Determine trend/range/pin context |
| Contract quality scoring | Option chain / contract page / alert page | Check spread, volume, OI, IV, Greeks |
| Price confirmation | UW chart / TradingView chart | Confirm breakout/retest/VWAP/level behavior |
| Risk filters | News, earnings, economic calendar, time of day | Manually block poor conditions |
| Alert engine | UW custom alerts + mobile/Discord notifications | Push only high-signal conditions |
| Outcome tracker | Manual trade journal | Log 5m/15m/30m/60m results |

## Required watchlists

Create these watchlists in UW:

```text
Index 0DTE Core:
SPX, SPY, QQQ, IWM

Single Stock Core:
TSLA, NVDA, AAPL, AMD, META, MSFT, AMZN

Semis / AI Confirmation:
NVDA, AMD, AVGO, ARM, SMCI, MU, TSM

Mega-Cap Confirmation:
AAPL, MSFT, AMZN, META, GOOGL, NVDA, TSLA
```

## Required saved flow filters

### Filter 1 — SPX 0DTE Call Pressure

Purpose:

```text
Find aggressive bullish SPX 0DTE call flow.
```

Settings:

```text
Ticker: SPX
DTE: 0
Type: Calls
Side: Ask / Buy side when available
Minimum premium: start at $50,000
OTM only: On for breakout searches; Off for ATM continuation searches
Volume > OI: preferred
Size > OI: preferred
Exclude obvious multi-leg/spread trades when possible
Sort: Premium or Time
Flow Status: Green or Yellow preferred
```

A+ interpretation:

```text
Multiple ask-side call prints appear within a short window.
Premium clusters around the same or nearby strikes.
Volume exceeds OI or is building rapidly.
SPX is breaking/retesting a key level.
Periscope / market maker exposure does not show immediate upside wall rejection.
Market Tide / Net Flow supports bullish direction.
```

### Filter 2 — SPX 0DTE Put Pressure

Settings:

```text
Ticker: SPX
DTE: 0
Type: Puts
Side: Ask / Buy side when available
Minimum premium: start at $50,000
OTM only: On for breakdown searches; Off for ATM continuation searches
Volume > OI: preferred
Size > OI: preferred
Exclude obvious multi-leg/spread trades when possible
Sort: Premium or Time
Flow Status: Green or Yellow preferred
```

A+ interpretation:

```text
Multiple ask-side put prints appear within a short window.
Premium clusters around same or nearby strikes.
Volume exceeds OI or accelerates rapidly.
SPX breaks/retests support.
VIX/volatility pressure supports downside.
Market Tide / Net Flow confirms bearish direction.
```

### Filter 3 — QQQ 0DTE Call Pressure

Settings:

```text
Ticker: QQQ
DTE: 0
Type: Calls
Side: Ask / Buy side
Minimum premium: $25,000 to $50,000
OTM only: On for breakouts; Off for ATM scalps
Volume > OI: preferred
Size > OI: preferred
Sort: Premium or Time
Flow Status: Green or Yellow preferred
```

Confirmation:

```text
NVDA/TSLA/META/MSFT/AAPL flow supports Nasdaq direction.
QQQ price confirms through VWAP/high-of-day/retest.
SPY/SPX are not strongly fighting the move.
```

### Filter 4 — QQQ 0DTE Put Pressure

Settings:

```text
Ticker: QQQ
DTE: 0
Type: Puts
Side: Ask / Buy side
Minimum premium: $25,000 to $50,000
OTM only: On for breakdowns; Off for ATM scalps
Volume > OI: preferred
Size > OI: preferred
Sort: Premium or Time
Flow Status: Green or Yellow preferred
```

### Filter 5 — Single-Stock Call Momentum

Symbols:

```text
TSLA, NVDA, AAPL, AMD, META, MSFT, AMZN
```

Settings:

```text
Ticker: one symbol at a time or watchlist if GUI supports it
Expiration: 0DTE where available, otherwise current weekly
Type: Calls
Side: Ask / Buy side
Minimum premium: $50,000 for NVDA/TSLA; $25,000 for others
Volume > OI: preferred
Size > OI: preferred
OTM only: On for breakout momentum; Off for ATM continuation
Exclude multi-leg when possible
Sort: Premium or Time
```

A+ interpretation:

```text
Ask-side calls repeat in same or nearby strikes.
Volume exceeds OI.
Underlying breaks VWAP/high-of-day/resistance.
QQQ or sector confirms.
No earnings/news trap.
Spread remains acceptable.
```

### Filter 6 — Single-Stock Put Breakdown

Same as above, but:

```text
Type: Puts
Direction: bearish
Confirmation: underlying below VWAP/support, QQQ/sector weak, IV expanding but not absurd
```

## Custom alert families

Use the 100 custom alerts carefully. Do not waste alerts on weak conditions.

Recommended alert families:

```text
SPX 0DTE Call Flow — A+ Watch
SPX 0DTE Put Flow — A+ Watch
QQQ 0DTE Call Flow — A+ Watch
QQQ 0DTE Put Flow — A+ Watch
SPY 0DTE Call Flow — Confirmation
SPY 0DTE Put Flow — Confirmation
NVDA Call Momentum
NVDA Put Breakdown
TSLA Call Momentum
TSLA Put Breakdown
AMD Call Momentum
AMD Put Breakdown
META/MSFT/AAPL/AMZN Call Momentum
META/MSFT/AAPL/AMZN Put Breakdown
High Premium 0DTE Index Flow
Volume > OI 0DTE Flow
Size > OI 0DTE Flow
```

## Manual A+ call checklist

Only mark an A+ CALL when all required layers align.

### Required call layers

```text
[ ] Flow: ask-side call premium dominates.
[ ] Flow: repeated prints or same-strike clustering.
[ ] Expiry: 0DTE for SPX/SPY/QQQ/IWM or current weekly for stock momentum.
[ ] Contract: volume > OI or volume is accelerating strongly.
[ ] Contract: bid/ask spread is acceptable.
[ ] Contract: IV is not already absurdly expanded unless trading volatility expansion intentionally.
[ ] Market: Market Tide / Net Flow is bullish or at least not bearish.
[ ] ETF: QQQ/SPY confirms the direction.
[ ] Dealer/GEX: no immediate major call wall rejection unless breakout is confirmed.
[ ] Price: underlying breaks and holds VWAP, high-of-day, OR high, or key resistance.
[ ] Risk: no imminent FOMC/CPI/NFP/headline/earnings trap.
[ ] Timing: avoid first 5–15 minutes unless intentionally trading open momentum; avoid late-day theta unless planned.
```

A+ CALL result:

```text
Take only on price confirmation: pullback/retest, break-and-hold, or continuation after consolidation.
Do not chase after premium has already expanded vertically.
```

## Manual A+ put checklist

Only mark an A+ PUT when all required layers align.

```text
[ ] Flow: ask-side put premium dominates.
[ ] Flow: repeated prints or same-strike clustering.
[ ] Expiry: 0DTE for SPX/SPY/QQQ/IWM or current weekly for stock momentum.
[ ] Contract: volume > OI or volume is accelerating strongly.
[ ] Contract: bid/ask spread is acceptable.
[ ] Market: Market Tide / Net Flow is bearish or strongly deteriorating.
[ ] ETF: QQQ/SPY confirms weakness.
[ ] Dealer/GEX: no immediate major put-wall bounce unless breakdown is confirmed.
[ ] Price: underlying loses VWAP, low-of-day, OR low, or key support.
[ ] Volatility: IV/VIX is expanding or supportive.
[ ] Risk: no imminent macro/news trap unless that is the explicit thesis.
[ ] Timing: avoid late-day chop unless momentum is clean.
```

A+ PUT result:

```text
Take only on failed bounce, breakdown retest, or confirmed momentum continuation.
Do not enter because of one large put print alone.
```

## Undeniably A+ patterns

No setup is guaranteed. In this playbook, “undeniably A+” means every available GUI layer agrees.

### A+ Pattern 1 — Index 0DTE Call Continuation

```text
SPX/QQQ 0DTE ask-side calls cluster.
Flow Status is green/yellow.
Market Tide bullish.
Net Flow bullish.
ETF Tide bullish for SPY/QQQ.
Periscope / exposure shows room before major call resistance.
Price breaks and retests VWAP/HOD/OR high.
Contract spread is tight enough to execute.
No imminent macro headline.
```

### A+ Pattern 2 — Index 0DTE Put Expansion

```text
SPX/QQQ 0DTE ask-side puts cluster.
Market Tide turns bearish.
Net Flow bearish.
VIX/volatility rising.
Price loses VWAP/LOD/OR low and retests from below.
Dealer/GEX context supports continuation, not immediate put-wall bounce.
Spread acceptable.
```

### A+ Pattern 3 — Single-Stock Call Momentum

```text
NVDA/TSLA/etc. ask-side calls repeat.
Same-strike or nearby-strike concentration.
Volume > OI.
Underlying breaks high-of-day/resistance.
QQQ/sector confirms.
No earnings/news trap.
Spread acceptable.
```

### A+ Pattern 4 — Single-Stock Put Breakdown

```text
Ask-side puts repeat.
Volume > OI.
Underlying loses VWAP/support.
QQQ/sector confirms downside.
News is either absent or directly supports bearish catalyst.
Spread acceptable.
```

### A+ Pattern 5 — Range Fade / Pin

```text
Positive/pinned exposure context.
Price hits call wall/put wall.
Directional flow stalls.
Opposite-side flow appears at the wall.
Market Tide is neutral or fading.
IV is not expanding.
```

## No-trade conditions

Do not trade when:

```text
Only one large print appears with no follow-through.
Trade is clearly multi-leg and direction is uncertain.
Flow is bullish but Market Tide / Net Flow is bearish.
Flow is bearish but QQQ/SPY is ripping higher.
Price is directly into a known wall and stalling.
Spread is too wide.
Volume is low and OI is low.
IV has already exploded and price is not moving.
Macro/news event is imminent.
Earnings risk is unmanaged.
The first attempt in the same direction just failed twice.
```

## Manual scorecard

Use this checklist until the API scoring engine exists.

| Category | Max | Manual score |
|---|---:|---:|
| Directional flow | 25 | __ / 25 |
| Market confirmation | 20 | __ / 20 |
| Dealer/GEX context | 20 | __ / 20 |
| Contract quality | 15 | __ / 15 |
| Price action | 10 | __ / 10 |
| Risk filter | 10 | __ / 10 |
| Total | 100 | __ / 100 |

Interpretation:

```text
90–100 = A+ candidate
85–89 = Strong watch
78–84 = Watch only
Below 78 = No trade
```

## Daily workflow

### Premarket

```text
1. Check economic calendar and major news.
2. Mark no-trade windows.
3. Review SPX/QQQ exposure / Periscope context.
4. Prepare index and single-stock watchlists.
5. Open saved filters and verify Flow Status.
```

### Market open

```text
1. Avoid forcing trades in first 5–15 minutes.
2. Watch first flow clusters but wait for price confirmation.
3. Identify whether day is trend, range, or caution.
```

### Main session

```text
1. Use alerts as triggers.
2. Confirm with Market Tide / Net Flow / ETF Tide.
3. Confirm with exposure / GEX context.
4. Confirm contract quality.
5. Enter only on price confirmation.
6. Log every alert/trade manually.
```

### End of day

```text
1. Record max gain/loss for watched contracts.
2. Record whether alert was actionable.
3. Record what failed.
4. Adjust filters only after enough samples.
```

## Recommended starting screen layout

```text
Screen 1: SPX/QQQ chart + Periscope / Market Maker Exposure
Screen 2: Options Flow with saved 0DTE filters
Screen 3: Market Tide / Net Flow / ETF Tide / Super Flow Dashboards
Screen 4: Watchlists + custom alerts + journal
```

## Upgrade decision

Stay on Professional GUI if:

```text
Manual workflow is enough.
UW alerts/filters are clear.
You can journal consistently.
You do not need custom automation yet.
```

Upgrade to API Advanced if:

```text
You need automatic scoring.
You need local database storage.
You need custom Discord/Telegram routing.
You need automatic outcome tracking.
You need to combine conditions the GUI cannot combine.
```
