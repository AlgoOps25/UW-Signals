# UW-Signals Implementation Checklist

## Purpose

This checklist turns the Holy Grail roadmap into an executable build path.

Do not skip the pre-purchase validation steps. The system should be built only after confirming that Unusual Whales API Advanced includes the REST and WebSocket access required for the MVP.

---

## Phase 0 — Repo and documentation foundation

Status: mostly complete.

```text
[x] Create UW-Signals repo
[x] Add README.md
[x] Add 00-HOLY-GRAIL-UW-OPTIONS-SYSTEM.md
[x] Add archive/reference documentation
[x] Add .gitignore
[x] Add .env.example
[x] Add requirements.txt
[x] Add source package skeleton
[x] Add architecture docs
[x] Add endpoint map
[x] Add scoring docs
[x] Add risk docs
```

---

## Phase 1 — Pre-purchase validation

Before purchasing UW API Advanced, confirm these items with UW support.

```text
[ ] API Advanced includes required REST endpoints.
[ ] API Advanced includes required WebSocket streams.
[ ] Option trades / full tape streaming is included or available enough for MVP.
[ ] Flow Alerts are included.
[ ] Market Tide is included.
[ ] ETF Tide is included.
[ ] Net Flow is included.
[ ] GEX / Greek Exposure endpoints are included.
[ ] Spot GEX exposure / wall data is included if available.
[ ] Greek Flow is included.
[ ] Option Chain / option-contract endpoints are included.
[ ] Stock state / OHLC / price endpoints are included.
[ ] News, economic calendar, earnings calendar, and trading halt data are included or accessible.
[ ] SPX, SPY, QQQ, IWM, TSLA, NVDA, AAPL, AMD, META, MSFT, and AMZN are supported.
[ ] The $250/month historical option-trades add-on is not required for the MVP.
[ ] Private personal-use alerting and local data storage are allowed.
```

Support question:

```text
I am considering API Advanced for a private Python alert system for my own trading. I need live WebSocket access for option trades, flow alerts, market tide, net flow, price, GEX/Greek-related data if available, and REST access for option chain, Greeks, GEX/Greek exposure, ETF tide, stock recent flows, flow per strike/expiry, IV, OI, earnings/news/economic calendar, and stock OHLC. Does API Advanced include these endpoints for SPX, SPY, QQQ, IWM, TSLA, NVDA, AAPL, AMD, META, MSFT, and AMZN without requiring the separate $250/month historical option-trades add-on?
```

---

## Phase 2 — Local environment setup

```text
[ ] Clone repo locally.
[ ] Create Python virtual environment.
[ ] Install requirements.
[ ] Copy .env.example to .env.
[ ] Add UW_API_KEY after subscription.
[ ] Add Discord webhook URL if using Discord alerts.
[ ] Run database initializer.
[ ] Run Streamlit dashboard shell.
```

Commands:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/init_db.py
streamlit run src/dashboard.py
```

---

## Phase 3 — API connection proof of concept

Goal: prove we can authenticate and pull low-cost endpoint data.

```text
[ ] Confirm bearer-token authentication.
[ ] Confirm REST base URL.
[ ] Add first confirmed REST endpoint to src/uw_rest_client.py.
[ ] Pull stock state for SPY.
[ ] Pull stock state for QQQ.
[ ] Pull stock state for NVDA.
[ ] Pull option chain for SPY.
[ ] Pull option chain for QQQ.
[ ] Pull option chain for NVDA.
[ ] Save raw responses to raw_events.
```

Deliverable:

```text
Local SQLite contains raw UW payloads from at least 3 symbols.
```

---

## Phase 4 — WebSocket proof of concept

Goal: prove we can receive live events.

```text
[ ] Confirm UW WebSocket URL and auth format.
[ ] Connect to a low-noise test stream.
[ ] Add heartbeat/reconnect logic.
[ ] Save live raw messages to raw_events.
[ ] Confirm timestamps are stored correctly.
[ ] Confirm duplicate events are not repeatedly stored.
```

Deliverable:

```text
Terminal prints live UW WebSocket events and SQLite stores them.
```

---

## Phase 5 — Index 0DTE MVP

Symbols:

```text
SPX
SPY
QQQ
```

Build:

```text
[ ] Normalize option-flow events into OptionFlowEvent.
[ ] Filter for 0DTE.
[ ] Calculate bullish/bearish premium imbalance.
[ ] Detect same-strike clusters.
[ ] Pull Market Tide / ETF Tide / Net Flow.
[ ] Pull GEX / Greek Exposure.
[ ] Score SPX/SPY/QQQ call and put contexts.
[ ] Apply risk filters.
[ ] Generate alert only if score >= 85.
[ ] Send Discord test alert.
[ ] Store alert in signal_alerts.
```

Deliverable:

```text
The system can produce SPX/SPY/QQQ 0DTE watch/strong/apex alerts in paper mode.
```

---

## Phase 6 — Outcome tracking

```text
[ ] Record alert timestamp, ticker, contract, score, direction, reasons, and risk flags.
[ ] Capture 5-minute outcome.
[ ] Capture 15-minute outcome.
[ ] Capture 30-minute outcome.
[ ] Capture 60-minute outcome.
[ ] Track max favorable excursion.
[ ] Track max adverse excursion.
[ ] Classify whether target hit before invalidation.
[ ] Export outcome report to CSV.
```

Deliverable:

```text
Every alert has measurable evidence of usefulness or failure.
```

---

## Phase 7 — Single-stock options MVP

Symbols:

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
[ ] Add ticker-specific flow filters.
[ ] Add weekly/0DTE expiration filters.
[ ] Add sector/ETF confirmation if available.
[ ] Add earnings/news risk filters.
[ ] Add CALL MOMENTUM alerts.
[ ] Add PUT BREAKDOWN alerts.
[ ] Add FLOW TRAP / NO TRADE alerts.
[ ] Track outcomes separately from index 0DTE.
```

Deliverable:

```text
The system can distinguish index 0DTE setups from single-stock momentum setups.
```

---

## Phase 8 — Threshold tuning

Only after 30 trading days of paper/live-observed data:

```text
[ ] Review every alert >= 85.
[ ] Compare apex vs strong vs watch-only outcomes.
[ ] Identify which score categories matter most.
[ ] Remove noisy features.
[ ] Tighten spread thresholds.
[ ] Separate morning vs afternoon rules.
[ ] Separate index vs single-stock rules.
[ ] Decide whether UW Advanced is worth keeping.
```

Deliverable:

```text
A data-backed decision on whether to keep, cancel, or replace UW Advanced.
```

---

## Phase 9 — Production hardening

```text
[ ] Add structured logging.
[ ] Add error handling for every REST call.
[ ] Add WebSocket reconnect and heartbeat monitoring.
[ ] Add rate-limit handling.
[ ] Add duplicate-event detection.
[ ] Add config-based thresholds.
[ ] Add tests for scoring/risk functions.
[ ] Add daily reset job.
[ ] Add dashboard performance views.
[ ] Add exportable journal/reporting.
```

---

## Final operating rule

```text
No real-money execution until the alert outcome tracker proves the model is useful.
```

The first version is for observation, scoring, and paper trading only.
