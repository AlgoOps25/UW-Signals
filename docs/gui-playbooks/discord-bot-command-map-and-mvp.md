# Discord Bot Command Map and MVP Plan

## Purpose

Use Unusual Whales Premium/Server Discord Bot functionality as the cheapest first MVP path before API Advanced.

## Key conclusion

The Discord bot command list significantly improves confidence that the Server/Premium Bot path can support a meaningful MVP.

The bot appears to provide:

```text
100 commands
19 premium-exclusive commands
no rate limit / no wait between commands on Premium Bot
live data instead of delayed/LVE data on Premium Bot
extended outputs
user watchlist commands
custom automatic posts via /configure
live options flow automatic posts
market updates, economic news, ticker updates, highest-volume contracts
Greeks, net flow, market tide, weekly/0DTE tide, flow, flow alerts, OI, volume, darkpool, chart, implied, max pain, and more
```

This does not fully replace API Advanced, but it gives enough command and automatic-post coverage to justify building a Discord-first MVP.

## Important official-doc anchors

Official docs confirm:

```text
The Discord bot uses slash commands to retrieve options and stock data.
Automatic posts can be configured with /followtheflow.
Automatic topics include economic news, market updates, OI feed updates, market halts/unhalts, ticker updates for up to 10 custom stocks, highest-volume options contracts, and UW feed posts.
The bot requires permissions for embeds/files.
Flow Status docs confirm that filtered live flow can be GREEN/YELLOW/RED based on whether all/most/not all matching trades are pushed live.
Unusual Options Alerts are not buy/sell signals; entries/exits are not provided.
Discord alerts can display contract theta and delta values.
```

## Command groups useful for UW-Signals

### Regime / market confirmation

```text
/market_tide
/weekly0dte
/net_impact
/heatmaps
/sectorflow
/sectorflowtop
/futures
/greeks spot_exposure
/greeks spot_intraday
```

### Flow trigger layer

```text
/flow
/flow_ticker
/customflow
/contractflow
/flow_alerts
/flow_expiry
/watchlist flow
/watchlist flow_alerts
/watchlist customflow
/watchlist bigflow
/watchlist hugeflow
/watchlist smallflow
```

### Contract quality / liquidity

```text
/highest_volume_contracts
/options_volume
/contract_volume
/cumulative_volume
/trading_above_average
/oi_change
/oi_increase
/oi_decrease
/oi_highest
/oi_expiry
/oi_strike
/uoa_voloi
/max_pain
/implied
```

### Risk filters

```text
/economic_calendar
/earnings
/earnings_premarket
/earnings_afterhours
/news
/news_latest
/fda_calendar
/market_holiday
/short failures_to_deliver
```

### Price confirmation

```text
/price
/chart
/cc
/cd
/cw
/cm
```

### Secondary confirmation

```text
/darkpool levels
/darkpool recent
/darkpool ticker
/etf perf
/etf weight
/sectorview
```

## Automatic post topics useful for MVP

```text
Economic News
Market Updates
Ticker Updates
Highest Volume Contracts
Live Options Flow
Analyst Ratings
Insider Trades
Stock Updates
Congress Trade Filings
```

## Recommended Discord channel layout

```text
#uw-auto-live-options-flow
#uw-auto-highest-volume-contracts
#uw-auto-market-updates
#uw-auto-economic-news
#uw-auto-ticker-updates
#uw-spx-qqq-regime
#uw-watchlist-flow
#uw-a-plus-candidates
#uw-trade-journal
#uw-outcome-review
```

## Command workflow for A+ Call

```text
1. Automatic Live Options Flow post or custom alert triggers.
2. Run /flow_ticker or /customflow for the ticker.
3. Run /flow_expiry to confirm expiry concentration.
4. Run /uoa_voloi or /options_volume to confirm unusual volume/OI.
5. Run /market_tide and /weekly0dte for market confirmation.
6. Run /net_impact for broad directional pressure.
7. Run /greeks spot_exposure or /greeks spot_intraday for GEX/dealer context if available.
8. Run /price or /chart to confirm price behavior.
9. Check /economic_calendar, /news, and /earnings where relevant.
10. Manually score the setup before entry.
```

## Command workflow for A+ Put

Same process, but require:

```text
put-side flow dominance
bearish market tide / net impact
price breakdown confirmation
volatility or downside pressure support
no immediate support-wall / bounce risk
```

## Server plan MVP conclusion

The Discord command surface is broad enough to support a serious manual/semi-automated MVP.

The API plan is still better for:

```text
stable machine-readable ingestion
full local database
automatic scoring
WebSocket event streams
automated outcome tracking
```

But the Server/Premium Bot path is now the preferred first test because it is cheaper and includes enough commands/automatic posts to validate edge before buying API Advanced.

## Remaining support question

```text
Am I allowed to run my own private Discord bot in my own private server to read UW bot/custom-alert posts, store them locally, and summarize them every few minutes for my personal trading use only, with no redistribution or resale?
```
