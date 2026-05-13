# Unusual Whales Endpoint Map

## Purpose

This document maps the Unusual Whales API documentation to the UW-Signals system before buying API Advanced.

Official references:

```text
https://api.unusualwhales.com/docs
https://api.unusualwhales.com/api/openapi
https://docs.unusualwhales.com/features/2-options-flow/
https://unusualwhales.com/pricing?product=api#monthly
```

## Investigation result

The public API documentation confirms that the UW API has the endpoint groups we need for the system design.

The docs do not fully prove which exact endpoint groups are included in API Basic vs API Advanced. The user's pricing screenshot showed Advanced includes WebSocket streaming, 50,000 REST requests/day, 90-day lookback, and premium endpoints. This still needs final support confirmation before purchase.

## Confirmed API foundation from docs

```text
Base URL: https://api.unusualwhales.com
Authentication: Bearer YOUR_API_KEY
API methods: REST, WebSocket, Kafka, MCP
OpenAPI spec: https://api.unusualwhales.com/api/openapi
Historical full-market option trades add-on: $250/month
API support: dev@unusualwhales.com
```

## Confirmed endpoint groups relevant to UW-Signals

| UW docs group | Confirmed docs count | Key endpoints named in docs | UW-Signals role |
|---|---:|---|---|
| Gex/Greeks | 10 | Greek Exposure, exposure by expiry/strike, Greek Flow, Spot GEX exposures | Dealer regime / walls / hedge pressure |
| Market | 12 | Market Tide, OI Change, Sector ETFs, Top Net Impact, Total Options Volume, Sector Tide, ETF Tide, Net Flow Expiry, Economic Calendar | Market confirmation / macro risk |
| Option Contract | 6 | Flow Data, Historic Data, Intraday Data, Volume Profile, Expiry Breakdown, Option Contracts | Contract selection / liquidity / lifecycle |
| Option Trade | 3 | Flow Alerts, Flow Alert by ID, Full Tape | Raw options flow and curated triggers |
| Stock | 37 | Flow Alerts, flow per expiry, flow per strike, flow per strike intraday, recent flows, Greeks, IV Rank, Max Pain, OHLC, OI Change, OI per Expiry, OI per Strike, Option Chains, Option Price Levels, Volume & OI per Expiry, Options Volume, Stock State, Technical Indicator, Realized Volatility, Volatility Statistics, IV Term Structure | Single-ticker options engine / price confirmation / volatility filters |
| WebSocket | 14 | WebSocket channels, Flow Alerts, GEX, Market Tide, Net Flow, News, Option Trades, Price, Trading Halts, Lit Trades, Off-lit Trades | Live system backbone |
| News | 1 | News Headlines | Headline risk filter |
| Earnings | 3 | Afterhours, Premarket, Historical Ticker Earnings | Earnings risk filter |
| Darkpool | 2 | Recent Darkpool Trades, Ticker Darkpool Trades | Secondary institutional equity confirmation |
| Lit Flow | 2 | Recent Lit Flow Trades, Ticker Lit Flow Trades | Secondary equity tape confirmation |
| ETF | 5 | Exposure, Holdings, Inflow/Outflow, Information, Sector/Country Weights | ETF context / sector confirmation |
| Economy | 1 | Economic Indicator | Macro context |
| Screener / Intel | 8 combined | Hottest Chains, Stock Screener, Sliding/Fixed Window Analytics, Top Movers | Discovery and later research |

## MVP endpoint priority

### Tier 1 — Required for first useful 0DTE MVP

```text
Option Trade: Flow Alerts
Option Trade: Full Tape
WebSocket: Option Trades
WebSocket: Flow Alerts
WebSocket: Price
WebSocket: Market Tide
WebSocket: Net Flow
Market: Market Tide
Market: ETF Tide
Market: Net Flow Expiry
Stock: Option Chains
Stock: Stock State
Stock: OHLC
Stock: Recent flows
Stock: Flow per expiry
Stock: Flow per strike
Stock: Flow per strike intraday
Stock: Greeks
Stock: IV Rank
Stock: OI per Expiry
Stock: OI per Strike
Gex/Greeks: Greek Exposure
Gex/Greeks: Greek Flow
Gex/Greeks: Spot GEX exposures
News: News Headlines
Market: Economic calendar
Earnings: Historical Ticker Earnings
WebSocket: Trading Halts
```

### Tier 2 — Useful after MVP works

```text
WebSocket: GEX
WebSocket: News
WebSocket: Lit trades
WebSocket: Off-lit trades
Darkpool: Recent / ticker darkpool trades
Lit Flow: Recent / ticker lit-flow trades
Stock: Realized Volatility
Stock: Volatility Statistics
Stock: Implied Volatility Term Structure
Stock: Max Pain
Stock: Option Price Levels
Market: Sector Tide
Market: Sector ETFs
Market: Top Net Impact
```

### Tier 3 — Research only, not live 0DTE trigger

```text
Congress
Insiders
Institution
Seasonality
Short interest / FTD
Company fundamentals
Analyst ratings
```

## Endpoint groups to validate before purchase

| UW component | Expected role | System layer | Required for MVP? | Docs status |
|---|---|---|---|---|
| Option trades / Full Tape | Raw options transaction stream | Flow trigger | Yes | Confirmed endpoint group exists |
| Flow Alerts | Curated unusual-flow signal stream | Flow trigger / watchlist | Yes | Confirmed REST + WebSocket groups exist |
| Option contract data | Contract-level state | Contract selection | Yes | Confirmed endpoint group exists |
| Option chain | Expiration/strike universe | Contract selection | Yes | Confirmed under Stock |
| Market Tide | Broad market options pressure | Market confirmation | Yes | Confirmed REST + WebSocket groups exist |
| ETF Tide | ETF-specific pressure for SPY/QQQ/IWM | Market confirmation | Yes | Confirmed under Market |
| Net Flow | Aggregate bullish/bearish premium | Market confirmation | Yes | Confirmed REST/WebSocket-related groups exist |
| GEX / Greeks | Dealer exposure / Greek state | Regime | Yes | Confirmed REST + WebSocket groups exist |
| Spot GEX exposures | Strike walls / magnets | Regime / risk | Yes | Confirmed under Gex/Greeks |
| Greek Flow | Delta/gamma hedge pressure | Confirmation | Yes | Confirmed under Gex/Greeks / group_flow |
| Stock price / state / OHLC | Underlying price confirmation | Price confirmation | Yes | Confirmed under Stock + WebSocket Price |
| WebSocket price stream | Live price updates | Price confirmation | Yes | Confirmed docs group exists |
| News headlines | Headline risk | Risk filter | Yes | Confirmed REST + WebSocket News exists |
| Economic calendar | Macro risk | Risk filter | Yes | Confirmed under Market |
| Earnings calendar/history | Single-stock event risk | Risk filter | Yes | Confirmed under Earnings / Stock Earnings History |
| Trading halts WebSocket | Kill switch | Risk filter | Yes | Confirmed WebSocket group exists |
| Dark pool / off-lit trades | Institutional equity context | Secondary confirmation | Later | Confirmed REST + WebSocket groups exist |
| Lit flow | Equity tape context | Secondary confirmation | Later | Confirmed REST + WebSocket groups exist |
| Congress / insider / institution data | Long-term context | Research only | No | Confirmed docs groups exist |
| Seasonality | Research backdrop | Research only | No | Confirmed docs group exists |

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

## Updated pre-purchase support question

```text
I am considering API Advanced for a private Python alert system for my own trading. I reviewed https://api.unusualwhales.com/docs and need to confirm API Advanced includes the following without requiring Enterprise or the separate $250/month historical option-trades add-on:

REST:
- Option Trade: Flow Alerts, Full Tape
- Option Contract: Flow Data, Intraday Data, Volume Profile, Expiry Breakdown, Option Contracts
- Stock: Option Chains, Stock State, OHLC, Recent flows, Flow per expiry, Flow per strike, Flow per strike intraday, Greeks, IV Rank, OI Change, OI per Expiry, OI per Strike, Options Volume, Realized Volatility, IV Term Structure
- Market: Market Tide, ETF Tide, Net Flow Expiry, Sector Tide, Top Net Impact, Economic Calendar
- Gex/Greeks: Greek Exposure, Greek Flow, Spot GEX exposures
- News: News Headlines
- Earnings: earnings calendar/history data

WebSocket:
- Option Trades
- Flow Alerts
- Price
- Market Tide
- Net Flow
- GEX
- News
- Trading Halts

Symbols:
- SPX, SPY, QQQ, IWM, TSLA, NVDA, AAPL, AMD, META, MSFT, AMZN

Use:
- private personal-use alerts
- local database storage
- no redistribution

Can you confirm these are included in API Advanced?
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

## Current conclusion

The public documentation strongly supports the UW-Signals architecture. The docs confirm the required endpoint categories exist.

The only remaining purchase blocker is plan entitlement: confirm API Advanced includes these exact endpoint groups and WebSocket channels without needing Enterprise or the separate historical-trades add-on.
