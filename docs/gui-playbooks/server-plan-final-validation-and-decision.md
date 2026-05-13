# Server Plan Final Validation and Decision

## Purpose

Consolidate the public-docs/tutorial research around using the Unusual Whales Server plan as the first MVP path instead of API Advanced.

## Current decision

The best cost-conscious first test is now:

```text
Unusual Whales Server plan
+ Custom Alert Builder
+ Discord automatic alert posts
+ private Python Discord listener
+ manual A+ scoring checklist
+ local SQLite message/summary storage
```

API Advanced should not be purchased first unless Server/Discord proves too limited.

## Why Server is now viable

Public docs/tutorial research indicates:

```text
Server subscription is marketed for pushing custom alerts into your own Discord server.
Custom alerts can be configured on the UW website and mapped to Discord channels.
UW bot supports automatic Discord posts.
Options flow fields include enough data to create meaningful 0DTE filters.
Discord alert messages appear to be normal bot messages/embeds that a private listener can parse.
```

## What remains to confirm with UW support

The main unresolved issue is licensing/terms.

Ask UW to confirm:

```text
Can I run my own private Discord bot in my own private server to read UW custom alert posts, store them locally, and summarize them every few minutes for my own personal trading use only, with no redistribution, resale, public sharing, or commercial use?
```

## Minimum viable setup

### Discord server channels

```text
#uw-spx-0dte-alerts
#uw-qqq-0dte-alerts
#uw-spy-iwm-confirmation
#uw-stock-momentum
#uw-market-news-halts
#uw-a-plus-summary
#uw-trade-journal
#uw-outcome-review
```

### Initial custom alert templates

```text
SPX 0DTE Call A+ Watch
SPX 0DTE Put A+ Watch
QQQ 0DTE Call A+ Watch
QQQ 0DTE Put A+ Watch
SPY/IWM Confirmation Flow
NVDA Call Momentum
NVDA Put Breakdown
TSLA Call Momentum
TSLA Put Breakdown
Mega-cap Call Momentum
Mega-cap Put Breakdown
```

### Python listener MVP

```text
Discord messages/embeds
→ raw_discord_messages table
→ parse ticker/contract/premium/volume/OI/side/DTE if present
→ rolling 1m/5m/15m summary
→ post A+ candidate summary back to Discord
→ manual confirmation before any trade
```

## Success criteria

The Server plan is enough for MVP if:

```text
Custom alerts can target ticker/watchlist, DTE, calls/puts, premium, volume/OI, spread, bullish/bearish premium, and expiry.
Custom alerts can post automatically to private Discord channels.
Discord posts contain enough structured message/embed fields to parse.
UW support approves private personal-use summarization by our own bot.
Manual scorecard provides actionable results after 2–4 weeks.
```

## Failure criteria

Upgrade to Professional if:

```text
Server has alert posting but lacks GUI context needed to validate trades.
Periscope, SPX exposure, Greeks/volatility dashboards, or Super Flow dashboards are needed for confidence.
```

Upgrade to API Advanced if:

```text
Discord posts are too incomplete.
Message formats are too unstable.
Local database/outcome tracking cannot work from Discord posts.
A fully automated multi-factor score is required.
```

## Final operating rule

Server plan posts are triggers, not entries.

A+ CALL/PUT status still requires:

```text
Flow cluster
0DTE/current-week expiry
Premium threshold
Volume/OI confirmation
Spread acceptable
Market confirmation
Price confirmation
No news/macro/earnings trap
Manual outcome logging
```
