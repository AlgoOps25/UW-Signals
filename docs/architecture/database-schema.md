# Database Schema

## Purpose

The database stores raw UW events, normalized alerts, and post-alert outcomes so every signal can be audited and improved.

Start simple with SQLite. Upgrade to Postgres/TimescaleDB only after the MVP proves useful.

## Current MVP tables

Defined in:

```text
src/storage.py
```

Initialized with:

```bash
python scripts/init_db.py
```

## raw_events

Stores vendor payloads before we fully normalize them.

| Column | Purpose |
|---|---|
| `id` | Auto-increment primary key |
| `source` | Source system, initially `unusual_whales` |
| `event_type` | Type such as `option_trade`, `flow_alert`, `market_tide`, `gex_snapshot` |
| `ticker` | Symbol when available |
| `event_timestamp` | Timestamp from UW payload when available |
| `received_timestamp` | Local received timestamp |
| `payload_json` | Original raw JSON payload |

## signal_alerts

Stores generated alerts after scoring and risk filtering.

| Column | Purpose |
|---|---|
| `id` | Auto-increment primary key |
| `alert_timestamp` | Time the alert was generated |
| `ticker` | Underlying symbol |
| `title` | Human-readable alert title |
| `direction` | `bullish`, `bearish`, `neutral`, `mixed`, or `unknown` |
| `regime` | `trend_up`, `trend_down`, `range_pin`, `vol_expansion`, `caution`, or `unknown` |
| `score` | Final 0–100 score |
| `payload_json` | Full alert details, reasons, contract, and risk flags |

## alert_outcomes

Stores what happened after alerts.

| Column | Purpose |
|---|---|
| `id` | Auto-increment primary key |
| `alert_id` | Related alert ID |
| `check_timestamp` | Time outcome was measured |
| `window_minutes` | Measurement window, such as 5, 15, 30, 60 |
| `underlying_price` | Underlying price at check time |
| `option_price` | Option premium at check time, if available |
| `max_favorable_excursion` | Best movement after alert |
| `max_adverse_excursion` | Worst movement after alert |
| `notes` | Manual or automatic notes |

## Future tables

After API fields are confirmed, expand into:

```text
option_trades_normalized
flow_alerts_normalized
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
earnings_events
risk_state_snapshots
manual_trades
```

## Design principle

Always keep raw payloads.

Even if normalized fields change later, the raw data lets us rebuild features without losing historical context.
