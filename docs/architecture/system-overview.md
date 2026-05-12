# System Overview

## Purpose

UW-Signals is a live options-flow decision system focused on:

```text
SPX 0DTE
SPY 0DTE
QQQ 0DTE
IWM 0DTE
TSLA / NVDA / AAPL / AMD / META / MSFT / AMZN options
```

The system is not designed to create guaranteed buy/sell calls.

It is designed to create probability-ranked alerts when live data streams align.

## Official data-source assumptions

Primary source:

```text
Unusual Whales API Advanced
```

Official references:

```text
https://api.unusualwhales.com/docs
https://api.unusualwhales.com/api/openapi
https://docs.unusualwhales.com/features/2-options-flow/
https://unusualwhales.com/pricing?product=api#monthly
```

UW options-flow documentation states that trade details include ticker, contract, bid/ask, spot, size, premium, open interest, volume, flags, DTE, and related calculated values. It also states that side labels are estimated from where trades occur relative to NBBO and that emojis / buy-sell side labels should not be traded alone.

## Core architecture

```text
Unusual Whales API Advanced
    REST endpoints
    WebSocket streams
        ↓
Python ingestion clients
        ↓
Normalization models
        ↓
SQLite/Postgres storage
        ↓
Feature engines
        ↓
Scoring engine
        ↓
Risk filters / kill switches
        ↓
Alert delivery
        ↓
Dashboard + outcome tracker
```

## Decision stack

Every alert must pass this sequence:

```text
Regime
→ Flow
→ Dealer/GEX context
→ Contract quality
→ Price confirmation
→ Risk filter
→ Alert
→ Outcome tracking
```

## Component responsibilities

| Layer | Current module | Purpose |
|---|---|---|
| Config | `src/config.py` | Environment variables, API keys, symbols, database URL |
| REST | `src/uw_rest_client.py` | Pull snapshots/endpoints after subscription |
| WebSocket | `src/uw_ws_client.py` | Stream live data after subscription |
| Models | `src/models.py` | Normalize vendor data into internal structures |
| Storage | `src/storage.py` | SQLite/Postgres initialization and persistence |
| Flow features | `src/features_flow.py` | Premium imbalance, directional estimates, clustering |
| GEX features | `src/features_gex.py` | Dealer regime and wall-distance context |
| Contract features | `src/features_contract.py` | Liquidity, spread, Greeks, OI, volume scoring |
| Price features | `src/features_price.py` | Underlying confirmation scoring |
| Risk filters | `src/risk_filters.py` | Spread/news/earnings/halt/time-of-day blocks |
| Scoring | `src/scoring.py` | 0–100 opportunity score and alert bands |
| Alerts | `src/alerts.py` | Discord/Telegram/email formatting and delivery |
| Outcomes | `src/outcomes.py` | Post-alert classification and usefulness tracking |
| Dashboard | `src/dashboard.py` | Streamlit dashboard shell |

## Initial MVP behavior

The first MVP should only do this:

```text
1. Connect to UW REST and WebSocket APIs.
2. Store raw events in SQLite.
3. Track SPX/SPY/QQQ 0DTE flow.
4. Score directional call/put opportunity context.
5. Apply risk filters.
6. Send Discord alerts only when the score is high enough.
7. Track every alert outcome.
```

## Alert bands

```text
90–100 = Apex alert
85–89  = Strong alert
78–84  = Watch only
Below 78 = No alert
```

## Final operating principle

```text
No single print creates a trade.
No single endpoint creates a trade.
A trade idea only becomes an alert when flow, market confirmation, GEX/dealer context, contract quality, price action, and risk filters agree.
```
