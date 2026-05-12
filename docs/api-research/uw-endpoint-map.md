# Unusual Whales Endpoint Map

## Purpose

This document maps the Unusual Whales components we expect to use to their system roles before buying API Advanced.

Official references:

```text
https://api.unusualwhales.com/docs
https://api.unusualwhales.com/api/openapi
https://docs.unusualwhales.com/features/2-options-flow/
```

## Endpoint groups to validate before purchase

| UW component | Expected role | System layer | Required for MVP? |
|---|---|---|---|
| Option trades / Full Tape | Raw options transaction stream | Flow trigger | Yes |
| Flow Alerts | Curated unusual-flow signal stream | Flow trigger / watchlist | Yes |
| Option contract data | Contract-level state | Contract selection | Yes |
| Option chain | Expiration/strike universe | Contract selection | Yes |
| Market Tide | Broad market options pressure | Market confirmation | Yes |
| ETF Tide | ETF-specific pressure for SPY/QQQ/IWM | Market confirmation | Yes |
| Net Flow | Aggregate bullish/bearish premium | Market confirmation | Yes |
| GEX / Greeks | Dealer exposure / Greek state | Regime | Yes |
| Spot GEX exposures | Strike walls / magnets | Regime / risk | Yes |
| Greek Flow | Delta/gamma hedge pressure | Confirmation | Yes |
| Stock price / state / OHLC | Underlying price confirmation | Price confirmation | Yes |
| WebSocket price stream | Live price updates | Price confirmation | Yes, if available |
| News headlines | Headline risk | Risk filter | Yes |
| Economic calendar | Macro risk | Risk filter | Yes |
| Earnings calendar | Single-stock event risk | Risk filter | Yes |
| Trading halts WebSocket | Kill switch | Risk filter | Yes |
| Dark pool / off-lit trades | Institutional equity context | Secondary confirmation | Later |
| Lit flow | Equity tape context | Secondary confirmation | Later |
| Congress / insider / institution data | Long-term context | Research only | No |
| Seasonality | Research backdrop | Research only | No |

## MVP endpoint validation checklist

Before subscribing, confirm with UW support:

```text
[ ] API Advanced includes WebSocket streams for option trades or flow alerts.
[ ] API Advanced includes WebSocket streams for price or stock-state data.
[ ] API Advanced includes Market Tide / ETF Tide / Net Flow endpoints.
[ ] API Advanced includes GEX / Greek Exposure endpoints.
[ ] API Advanced includes option-chain and contract-level data.
[ ] API Advanced supports SPX, SPY, QQQ, IWM, TSLA, NVDA, AAPL, AMD, META, MSFT, AMZN.
[ ] API Advanced does not require the $250/month historical full-market option-trades add-on for the MVP.
[ ] API terms allow private personal-use alerting and local data storage.
```

## Pre-purchase support question

```text
I am considering API Advanced for a private Python alert system for my own trading. I need live WebSocket access for option trades, flow alerts, market tide, net flow, price, GEX/Greek-related data if available, and REST access for option chain, Greeks, GEX/Greek exposure, ETF tide, stock recent flows, flow per strike/expiry, IV, OI, earnings/news/economic calendar, and stock OHLC. Does API Advanced include these endpoints for SPX, SPY, QQQ, IWM, TSLA, NVDA, AAPL, AMD, META, MSFT, and AMZN without requiring the separate $250/month historical option-trades add-on?
```

## Implementation mapping

| Endpoint group | Initial module |
|---|---|
| REST snapshots | `src/uw_rest_client.py` |
| WebSocket streams | `src/uw_ws_client.py` |
| Raw payload storage | `src/storage.py` |
| Normalized option-flow event | `src/models.py` |
| Flow calculations | `src/features_flow.py` |
| GEX calculations | `src/features_gex.py` |
| Contract quality | `src/features_contract.py` |
| Price confirmation | `src/features_price.py` |
| Risk filters | `src/risk_filters.py` |
| Scoring | `src/scoring.py` |
| Alerting | `src/alerts.py` |
| Outcomes | `src/outcomes.py` |
