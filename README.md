# UW-Signals

Live options-flow signal research and alert-system workspace built around **Unusual Whales API Advanced + Python + dashboards + outcome tracking**.

> Educational trading/research project only. This is not financial advice. No signal is guaranteed. Every alert model must be validated with paper trading and outcome tracking before real-money use.

## Official roadmap

The single source of truth is:

```text
00-HOLY-GRAIL-UW-OPTIONS-SYSTEM.md
```

Start there before changing architecture, scoring rules, API assumptions, or implementation priorities.

## Active strategy focus

```text
SPX 0DTE
SPY 0DTE
QQQ 0DTE
IWM 0DTE
TSLA / NVDA / AAPL / AMD / META / MSFT / AMZN options
```

## Core decision stack

Every alert must pass this stack:

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

No single data point creates a trade.

## Planned stack

```text
Unusual Whales API Advanced
+ Python live data engine
+ SQLite/Postgres database
+ Streamlit/FastAPI dashboard
+ Discord/Telegram alerts
+ TradingView visualization only
+ manual broker execution first
```

## Repository map

| Path | Purpose |
|---|---|
| `00-HOLY-GRAIL-UW-OPTIONS-SYSTEM.md` | Master roadmap and system reference |
| `docs/` | Architecture, API research, scoring, and risk documentation |
| `src/` | Future Python implementation modules |
| `templates/` | Journal/checklist templates |
| `archive/reference/` | Superseded decisions preserved for context |
| `archive/legacy-pine/` | Legacy TradingView/Pine reference material |

## Pre-purchase gate

Before subscribing to UW API Advanced:

```text
[ ] Review the master roadmap.
[ ] Send UW support the endpoint/access confirmation question from Section 12.
[ ] Confirm WebSocket and REST coverage for required endpoints.
[ ] Confirm no $250 historical option-trades add-on is required for the MVP.
[ ] Confirm private personal-use alerting and local storage are allowed.
```

## First implementation phase after purchase

```text
1. Authenticate with bearer token.
2. Pull stock state for SPY/QQQ/NVDA.
3. Pull option chains for SPY/QQQ/NVDA.
4. Pull recent flows.
5. Pull Market Tide / ETF Tide / Net Flow.
6. Pull GEX / Greek exposure.
7. Connect to live WebSocket streams.
8. Write raw events to SQLite.
9. Build SPX/SPY/QQQ 0DTE APEX alerts.
10. Track every alert outcome before real-money execution.
```
