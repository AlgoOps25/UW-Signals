# 00 — Holy Grail: Unusual Whales Options Trading System Master Roadmap

> Purpose: This is the single source of truth for the Layer 8 Works options-flow trading system before purchasing Unusual Whales API Advanced.
>
> Scope: Build a professional-grade, live-data-driven alert and decision system focused on SPX/SPY/QQQ/IWM 0DTE options and selected liquid single-stock options such as TSLA, NVDA, AAPL, AMD, META, MSFT, and AMZN.
>
> Status: Planning / pre-subscription. Do not purchase additional tools or start coding until this document is reviewed and accepted.

---

## 1. Final strategic direction

We are moving away from a QuantVue-first indicator workflow and toward a data-first options-flow system.

The preferred stack is:

```text
Unusual Whales API Advanced
+ Python live data engine
+ SQLite/Postgres database
+ Streamlit/FastAPI dashboard
+ Discord/Telegram alerting
+ TradingView for visualization only
+ manual broker execution at first
```

The system should focus on:

```text
SPX 0DTE
SPY 0DTE
QQQ 0DTE
IWM 0DTE
TSLA / NVDA / AAPL / AMD / META / MSFT / AMZN weekly and 0DTE options where available
```

The goal is not to create a guaranteed buy/sell machine. The goal is to create a probability-ranked decision engine that only alerts when multiple independent live data streams agree.

Core decision hierarchy:

```text
Regime → Flow → Dealer/GEX Context → Contract Quality → Price Confirmation → Risk Filter → Alert → Outcome Tracking
```

---

## 2. Official Unusual Whales source references

Use these references before relying on assumptions:

```text
API docs:
https://api.unusualwhales.com/docs

OpenAPI spec:
https://api.unusualwhales.com/api/openapi

Options Flow documentation:
https://docs.unusualwhales.com/features/2-options-flow/

Pricing / API token page:
https://unusualwhales.com/pricing?product=api#monthly

API support:
dev@unusualwhales.com
```

Important official notes from the docs:

```text
The API provides 100+ endpoints for options flow, dark pool, congressional trading, Greek exposure, volatility, and more.
API access supports REST, WebSocket, Kafka, and MCP.
Authentication uses Bearer YOUR_API_KEY.
Historical option trades are a separate add-on at $250/month for the full market.
Options flow side labels are estimations based on fill location versus NBBO.
Do not trade off emojis / buy-sell side labels alone.
Not all BUY orders are buy-to-open and not all SELL orders are sell-to-open.
Trades can be multi-leg.
```

---

## 3. Plan decision: Which Unusual Whales plan?

Based on the user's pricing screenshots:

```text
API Basic: $150/month
- Lower request limit
- No WebSocket live streaming

API Advanced: $375/month
- 50,000 REST requests/day
- 90-day historical lookback
- Premium endpoints
- WebSocket live data streaming
```

Decision:

```text
Use API Advanced if we build the live alert engine.
Do not purchase the historical full-market option-trades add-on yet.
```

Why Advanced:

```text
The system depends on live streaming events, not slow polling only.
WebSocket access is required for professional live alerting.
```

When Basic is acceptable:

```text
Only if building a slow dashboard that polls every few minutes.
Not recommended for the intended live alert system.
```

---

## 4. What every Unusual Whales component is used for

Every useful UW component must have a defined job. No endpoint should be pulled just because it exists.

| Component | System role | Primary use |
|---|---|---|
| Full Tape / Option Trades | Opportunity trigger | Raw live 0DTE and single-stock options transactions |
| Flow Alerts | Opportunity trigger | Curated unusual-flow events and fast watchlist pings |
| Option Contract Flow | Confirmation | Contract-level accumulation and repeated buying/selling |
| Flow per Expiry | 0DTE isolation | Separates 0DTE from weekly/monthly flow |
| Flow per Strike | Strike clustering | Finds concentrated activity around important strikes |
| Flow per Strike Intraday | Acceleration | Detects intraday same-strike momentum bursts |
| Recent Flows | Ticker confirmation | Confirms current flow direction for a ticker |
| Option Chain | Contract universe | Finds available strikes/expirations/liquidity |
| Greeks | Contract risk | Delta/gamma/theta/vega suitability |
| GEX / Greek Exposure | Dealer regime | Range vs trend, pinning vs acceleration |
| Spot GEX Exposures | Strike-level walls | Call walls, put walls, magnets, squeeze zones |
| Greek Flow | Hedge-pressure confirmation | Whether flow creates meaningful delta/gamma pressure |
| Market Tide | Broad confirmation | Broad options pressure across the market |
| ETF Tide | Ticker/index confirmation | QQQ/SPY/IWM directional pressure |
| Net Flow | Aggregate direction | Bullish/bearish premium pressure over windows |
| Stock OHLC / Stock State / Price WS | Price confirmation | Underlying confirms or rejects options flow |
| IV / IV Rank / Term Structure | Volatility risk | Avoid IV crush; confirm volatility expansion |
| Realized Volatility | Movement validation | Is underlying moving enough to justify premium? |
| OI / Volume / OI Change | Position context | Avoid dead contracts; detect opening interest later |
| Darkpool / Off-lit | Institutional stock context | Confirms underlying accumulation/distribution |
| Lit Flow | Equity tape context | Confirms stock buying/selling behind options |
| News Headlines | Risk filter | Blocks headline traps |
| Economic Calendar | Risk filter | Blocks FOMC/CPI/NFP and other macro windows |
| Earnings Calendar | Stock risk filter | Blocks or flags earnings/event risk |
| Trading Halts WS | Kill switch | Blocks trading around halts |
| Sector Tide / Sector ETFs | Stock confirmation | Confirms single-stock flow with sector pressure |
| Top Net Impact | Discovery | Finds tickers driving market options pressure |
| Correlations | Context | Confirms stock/index alignment |
| Seasonality | Research only | Backdrop, not intraday trigger |
| Congress/Insider/Institutional | Long-term context | Not an intraday 0DTE signal |

---

## 5. System architecture

### 5.1 High-level flow

```text
Unusual Whales API Advanced
    REST endpoints
    WebSocket streams
        ↓
Python ingestion services
        ↓
Normalizer + validator
        ↓
SQLite/Postgres database
        ↓
Feature engineering layer
        ↓
Regime + flow + contract scoring engine
        ↓
Risk filter / kill switch
        ↓
Alert engine
        ↓
Discord / Telegram / Email / SMS
        ↓
Dashboard + trade journal + outcome tracker
```

### 5.2 Core Python modules

```text
src/config.py              # symbols, risk settings, thresholds, API keys
src/uw_rest_client.py      # REST calls
src/uw_ws_client.py        # WebSocket subscriptions
src/models.py              # typed event/data models
src/storage.py             # SQLite/Postgres writes and reads
src/features_flow.py       # premium imbalance, clustering, flow windows
src/features_gex.py        # regime, walls, gamma context
src/features_contract.py   # spread, Greeks, OI, volume, liquidity
src/features_price.py      # price confirmation, VWAP/levels, trend
src/risk_filters.py        # news, spread, theta, IV, time, halt filters
src/scoring.py             # 0–100 opportunity scoring
src/alerts.py              # Discord/Telegram/email/SMS
src/outcomes.py            # post-alert performance tracking
src/dashboard.py           # Streamlit/FastAPI dashboard
src/jobs_daily.py          # startup, reset, daily prep
```

### 5.3 Recommended storage

Start local:

```text
SQLite
```

Upgrade later:

```text
Postgres + TimescaleDB
```

Key tables:

```text
raw_option_trades
flow_alerts
market_tide_snapshots
etf_tide_snapshots
net_flow_snapshots
gex_snapshots
greek_flow_snapshots
option_chain_snapshots
contract_metrics
stock_price_bars
news_events
economic_events
system_alerts
trade_alerts
alert_outcomes
manual_trades
```

---

## 6. Trading universe

### 6.1 Index / ETF 0DTE engine

Start with:

```text
SPX
SPY
QQQ
IWM
```

Primary focus:

```text
SPX 0DTE directional opportunities
QQQ 0DTE Nasdaq-style directional opportunities
SPY 0DTE liquid broad-market opportunities
IWM only after SPX/SPY/QQQ models work
```

### 6.2 Single-stock options engine

Start with:

```text
TSLA
NVDA
AAPL
AMD
META
MSFT
AMZN
```

Primary focus:

```text
TSLA and NVDA first
Then AAPL/AMD/META/MSFT/AMZN
```

Do not monitor hundreds of tickers during the MVP. Too many tickers creates noisy alerts and makes edge validation impossible.

---

## 7. Professional decision stack

A signal must pass all stages.

### Stage 1 — Universe and liquidity filter

Reject if:

```text
Ticker not in approved universe
Expiration not 0DTE or current weekly according to strategy
Bid/ask spread too wide
Volume too low
Open interest context weak
Contract too far OTM without catalyst
No underlying price confirmation
Known earnings/news/macro risk unmanaged
```

### Stage 2 — Regime engine

Uses:

```text
GEX / Greek Exposure
Spot GEX exposures
Market Tide
ETF Tide
Net Flow
VIX / volatility proxies
Realized volatility
```

Outputs:

```text
TREND UP
TREND DOWN
RANGE / PIN
VOL EXPANSION
CAUTION / NO TRADE
```

### Stage 3 — Flow engine

Uses:

```text
Full Tape
Flow Alerts
Contract Flow Data
Recent Flows
Flow per Expiry
Flow per Strike
Flow per Strike Intraday
Greek Flow
```

Detects:

```text
Call sweep burst
Put sweep burst
Same-strike accumulation
Repeated aggressive ask-side buying
Large premium clusters
Flow divergence against price
Flow alignment with tide
```

### Stage 4 — Contract-quality engine

Uses:

```text
Option Chain
Greeks
Bid/ask spread
Volume
Open interest
IV / IV Rank
Contract intraday data
```

Scores:

```text
Liquidity
Spread quality
Delta suitability
Gamma explosiveness
Theta danger
IV expansion/crush risk
Exit feasibility
```

### Stage 5 — Price confirmation engine

Uses:

```text
Stock price stream / OHLC
VWAP / EMA / technical endpoint if needed
Prior high/low
Option price levels
Lit/off-lit flow
```

Requires:

```text
Underlying confirms direction
There is room to target
Price is not directly into a wall unless breakout regime supports it
No failed breakout against the signal
```

### Stage 6 — Risk engine

Uses:

```text
Spread
IV
theta
time of day
macro/news calendar
earnings calendar
halt stream
recent failed alerts
max daily alert count
position sizing rules
```

Blocks:

```text
Wide spreads
Late-day theta traps
IV crush risk
News windows
Mixed flow
Overtrading
Two failed same-direction alerts
Halts
Abnormal spread expansion
```

---

## 8. Scoring model

All alerts are probability/context scores, not guaranteed signals.

### 8.1 Universal 0–100 score

| Category | Points | Description |
|---|---:|---|
| Directional flow | 25 | Aggressive calls/puts, premium, sweeps, clustering |
| Market confirmation | 20 | Market Tide, ETF Tide, Net Flow, sector/index agreement |
| Dealer/GEX context | 20 | Gamma regime, GEX walls, Greek flow, room to next wall |
| Contract quality | 15 | Spread, volume, OI, Greeks, IV, exit liquidity |
| Price action | 10 | Underlying trend, breakout/retest, VWAP/level confirmation |
| Risk filter | 10 | News, earnings, time, halts, recent failures |

### 8.2 Alert bands

```text
90–100 = Apex alert
85–89  = Strong alert
78–84  = Watch only
Below 78 = No alert
```

### 8.3 Action rules

```text
Apex alert: Eligible for active trade plan, still requires execution confirmation.
Strong alert: Watch for pullback/retest, smaller size.
Watch only: Log and observe, no trade unless discretionary A+ context.
No alert: Ignore.
```

---

## 9. Strategy models

### Model A — SPX/QQQ 0DTE Trend Continuation

Use when:

```text
Market Tide agrees with direction
ETF Tide agrees
Net Flow agrees
GEX/regime supports continuation
Underlying breaks and retests a level
Aggressive 0DTE flow clusters in same direction
Contract spread and Greeks are acceptable
```

Alert examples:

```text
SPX 0DTE CALL CONTINUATION — 92/100
QQQ 0DTE PUT CONTINUATION — 88/100
```

### Model B — 0DTE Gamma Squeeze / Acceleration

Use when:

```text
Negative gamma or acceleration-prone regime
Spot GEX shows weak resistance above or weak support below
Same-side aggressive flow accelerates
Greek flow confirms delta/gamma pressure
Underlying confirms breakout
```

Avoid when:

```text
Price is directly into a major call wall / put wall
Flow is one-off with no follow-through
VIX/volatility context fights the move
```

### Model C — 0DTE Range Fade / Pin

Use when:

```text
Positive gamma / pinned regime
Price reaches major wall
Flow stalls or reverses at wall
Market Tide is not strongly directional
IV is not expanding
```

Alert example:

```text
SPY 0DTE RANGE FADE — 86/100
```

### Model D — Single-Stock Flow Momentum

Use when:

```text
Ticker-specific flow clusters
Premium is large relative to normal
Volume exceeds OI context
Underlying confirms move
Sector/ETF confirms
No earnings/news trap unless intentionally trading catalyst
```

Alert examples:

```text
NVDA CALL MOMENTUM — 89/100
TSLA PUT BREAKDOWN — 86/100
```

### Model E — Volatility Expansion Put/Call

Use when:

```text
VIX/volatility rising
IV expanding
Put or call flow accelerates aggressively
Underlying breaks key level
Market Tide confirms
```

---

## 10. Example alert formats

### 10.1 SPX 0DTE Apex Call

```text
🚨 SPX 0DTE CALL APEX — 93/100

Why:
- 0DTE call premium cluster detected
- Market Tide bullish
- SPY/QQQ ETF Tide confirms
- Net Flow positive over 5m/15m
- GEX shows room to next upside wall
- Contract spread acceptable
- Underlying broke/retested key level

Contract:
SPX [expiration] [strike]C

Plan:
Entry only on pullback/retest or break-hold confirmation.
Do not chase if premium expands too far.

Invalidation:
Market Tide flips negative, VIX spikes, or SPX rejects wall.
```

### 10.2 NVDA Call Momentum

```text
🚨 NVDA CALL MOMENTUM — 88/100

Why:
- Ask-side call premium dominant
- Repeated sweeps near same strike
- Volume > OI context
- NVDA price confirms breakout
- QQQ/sector confirms
- Spread acceptable

Contract:
NVDA [expiration] [strike]C

Plan:
Entry only on pullback/retest.

Invalidation:
QQQ flow flips bearish, NVDA loses breakout level, or spread widens.
```

### 10.3 No Trade / Caution

```text
⚠️ CAUTION / NO TRADE

Why:
- Flow conflicts across QQQ/SPY/SPX
- VIX rising against long idea
- Price trapped between major GEX walls
- Upcoming macro/news event

Action:
No trade until alignment improves.
```

---

## 11. Dashboard design

### 11.1 Main dashboard panels

```text
Current Regime: TREND UP / TREND DOWN / RANGE / CAUTION
Top Index Alert: SPX / SPY / QQQ / IWM
Top Stock Alert: TSLA / NVDA / etc.
Long Score
Short Score
Market Tide
ETF Tide
Net Flow
GEX wall map
Greek Flow summary
VIX / volatility context
Top 0DTE contracts
Top single-stock contracts
Risk flags
Latest alerts
Outcome tracker
```

### 11.2 Screens

```text
Screen 1: Morning Prep / Regime
Screen 2: Live Alerts
Screen 3: Contract Drilldown
Screen 4: Flow Clustering
Screen 5: GEX / Walls
Screen 6: Outcomes / Analytics
Screen 7: Settings / Thresholds
```

---

## 12. Roadmap before purchase

### Phase 0 — Documentation freeze

Goal:

```text
Consolidate all UW/Skylit/QuantVue decision docs into this master document.
Stop adding new strategy documents unless they update this one.
```

Status:

```text
This document becomes the reference source.
```

### Phase 1 — Pre-purchase validation

Before buying UW Advanced, verify:

```text
[ ] API Advanced includes WebSocket streams for option trades, flow alerts, price, net flow, market tide, and GEX if required.
[ ] API Advanced includes the endpoints needed for SPX/SPY/QQQ/IWM/TSLA/NVDA.
[ ] Advanced does not require the $250 historical add-on for 90-day endpoint lookback.
[ ] Rate limit of 50,000 REST/day is enough for MVP.
[ ] Terms allow private personal-use alerting and local storage.
[ ] No redistribution issues if alerts only go to the user.
```

Support question to send:

```text
I am considering API Advanced for a private Python alert system for my own trading. I need live WebSocket access for option trades, flow alerts, market tide, net flow, price, GEX/Greek-related data if available, and REST access for option chain, Greeks, GEX/Greek exposure, ETF tide, stock recent flows, flow per strike/expiry, IV, OI, earnings/news/economic calendar, and stock OHLC. Does API Advanced include these endpoints for SPX, SPY, QQQ, IWM, TSLA, NVDA, AAPL, AMD, META, MSFT, and AMZN without requiring the separate $250/month historical option-trades add-on?
```

### Phase 2 — Local API proof of concept

After purchase:

```text
[ ] Authenticate with bearer token.
[ ] Pull stock state for SPY/QQQ/NVDA.
[ ] Pull option chain for SPY/QQQ/NVDA.
[ ] Pull recent flows.
[ ] Pull market tide.
[ ] Pull ETF tide.
[ ] Pull GEX/Greek exposure.
[ ] Connect to WebSocket price stream.
[ ] Connect to option trades stream.
[ ] Write raw events to SQLite.
```

Deliverable:

```text
Terminal confirms live events + SQLite stores data.
```

### Phase 3 — Index 0DTE MVP

Build only:

```text
SPX/SPY/QQQ 0DTE Call/Put APEX alerts
CAUTION / NO TRADE alerts
```

No single stocks yet.

### Phase 4 — Single-stock MVP

Add:

```text
TSLA
NVDA
AAPL
AMD
META
MSFT
AMZN
```

Build:

```text
CALL MOMENTUM
PUT BREAKDOWN
FLOW TRAP / NO TRADE
```

### Phase 5 — Outcome tracker

For every alert, record:

```text
Underlying price at alert
Option premium at alert
5m / 15m / 30m outcome
Max favorable excursion
Max adverse excursion
Did target hit before invalidation?
Was the alert actionable?
```

### Phase 6 — Threshold tuning

After 30 trading days:

```text
Remove weak features
Raise/lower score thresholds
Separate index vs stock rules
Separate morning vs afternoon rules
Evaluate whether UW Advanced remains worth $375/month
```

---

## 13. What old docs this replaces

This master document consolidates the intent from:

```text
47-options-data-vendor-decision.md
48-unusual-whales-live-alert-system-blueprint.md
49-options-data-stack-decision-uw-vs-alternatives.md
50-unusual-whales-component-usage-map.md
Earlier QuantVue/Skylit decision documents where relevant
```

Keep old docs only as archives. Going forward, update this document first.

---

## 14. Open questions before purchase

Need to confirm with UW or test after purchase:

```text
1. Which WebSocket channels are included in API Advanced vs Enterprise?
2. Is GEX available via WebSocket or REST only?
3. Are SPX index options fully supported the same way as ETF/equity options?
4. Does the API return bid/ask spread and NBBO fields consistently enough for live contract filtering?
5. Is 90-day historical lookback available for all endpoints or only selected ones?
6. How strict are rate limits by endpoint?
7. Are flow-alert endpoints sufficient to reduce raw tape processing?
8. Can alerts be used privately without redistribution concerns?
```

---

## 15. Final operating principle

The system should never say:

```text
Buy now, guaranteed.
```

It should say:

```text
Live options data strongly favors this context. Trade only if execution, spread, risk, and price confirmation are acceptable.
```

The edge comes from:

```text
Using many live data components together,
rejecting weak trades,
tracking every alert outcome,
and constantly removing rules that do not prove themselves.
```
