# UW Decision Archive

This file preserves the important reference value from the original UW transition documents.

The official roadmap is now:

```text
00-HOLY-GRAIL-UW-OPTIONS-SYSTEM.md
```

Do not treat the archived notes below as active implementation instructions unless the master roadmap points back to them.

---

## Archived: 47-options-data-vendor-decision.md

Original purpose: choose the best options-flow / dealer-positioning data source for building a custom Python alert system.

Key preserved decisions:

```text
Best single-vendor path: Unusual Whales API
Best practical stack if expanded: Unusual Whales API + FlashAlpha Basic/Growth
Best UI-only alternative: Skylit Initiate
Best professional reference: SpotGamma
Raw-data rebuild candidates: Polygon, ORATS, ThetaData
```

Reasoning preserved:

```text
Unusual Whales is the most API-first and automation-friendly option found for this project.
It offers REST/WebSocket-style automation potential, options flow, GEX/Greeks, Greek flow, market tide, net flow, dark pool, flow alerts, full tape, and WebSocket channels.
Raw-data providers can be cheaper but require rebuilding analytics internally.
```

---

## Archived: 48-unusual-whales-live-alert-system-blueprint.md

Original purpose: define a live-data-driven alert system for NQ/MNQ context and options plays.

Key preserved architecture:

```text
Unusual Whales API/WebSocket
→ Python ingestion service
→ Normalization layer
→ SQLite/Postgres database
→ Feature calculator
→ Scoring engine
→ Alert engine
→ Discord/Telegram/SMS/email
→ Dashboard
```

Key preserved alert types:

```text
NQ LONG CONTEXT
NQ SHORT CONTEXT
RANGE / FADE CONTEXT
CAUTION / NO TRADE
```

This has been superseded by the options-only roadmap in the Holy Grail document, but the architecture pattern remains valid.

---

## Archived: 49-options-data-stack-decision-uw-vs-alternatives.md

Original purpose: decide whether UW API Advanced is the most advanced and cheapest possible solution.

Key preserved decision:

```text
Unusual Whales API Advanced is not the cheapest.
It is the best single-provider shortcut for the current goal.
ThetaData Options Pro or Polygon Options Advanced may be cheaper raw-data alternatives but require more engineering.
```

Preserved rule:

```text
Do not optimize subscription cost before validating the trading edge.
```

---

## Archived: 50-unusual-whales-component-usage-map.md

Original purpose: map every useful UW component to a trading-system role.

Key preserved rule:

```text
No single component creates a trade.
A trade opportunity is valid only when multiple independent components align:
Market regime + Flow direction + Greek/GEX context + Contract quality + Price confirmation + Risk filter
```

Component roles preserved:

```text
Full Tape / Option Trades = raw live transaction trigger
Flow Alerts = curated watchlist trigger
Option Contract Flow = contract-level accumulation
Flow per Expiry = 0DTE isolation
Flow per Strike = strike clustering
Greeks = contract risk
GEX / Greek Exposure = dealer regime
Greek Flow = hedge-pressure confirmation
Market Tide / ETF Tide / Net Flow = broad confirmation
Stock OHLC / Price WS = price confirmation
IV / Realized Volatility = volatility filter
News / Economic / Earnings / Halts = risk kill-switch layer
Darkpool / Lit Flow = secondary institutional context
Outcome tracking = learning layer
```

---

## Archive policy

Going forward:

```text
1. Update 00-HOLY-GRAIL-UW-OPTIONS-SYSTEM.md first.
2. Add implementation files only when they support a specific roadmap phase.
3. Put historical decisions in archive/reference only when they are superseded.
4. Keep the root folder focused on the active roadmap and build files.
```
