# UW Server Plan Discord Workflow Assessment

## Purpose

Evaluate whether the Unusual Whales Server plan can replace the Professional GUI plan or API Advanced plan for UW-Signals.

## Current conclusion

The Server plan is useful, but it should not be the primary replacement for API Advanced or the Professional GUI workflow.

Best role:

```text
Cheapest Discord-based live options-flow triage and automatic-post layer
```

Not best role:

```text
Full manual GUI decision terminal
Full Python/API automation engine
Full A+ multi-factor scoring system
```

## Why it matters

The Server plan appears designed around Discord server usage:

```text
Unlimited command usage
Enhanced bot commands
Automatic posts in Discord
Real-time live options-flow data
Custom automatic posts to Discord
Personalized setup / troubleshooting
```

This makes it valuable if the goal is to get flow and market updates into a private Discord channel.

## Official docs support

Unusual Whales docs say the Discord bot uses slash commands to retrieve options and stock data.

The docs also say the `/followtheflow` command can set up automatic posts for:

```text
Economic News Updates
Market Updates including Open Interest Feed updates and market halts/unhalts
Ticker Updates for up to 10 custom stocks
Highest Volume Options Contracts
Tweets from Unusual Whales feeds
```

The docs note the bot can be added to a server by a user with administrative privileges and that permissions must allow embeds/files.

## What the Server plan can approximate

| UW-Signals layer | Server plan approximation | Quality |
|---|---|---|
| Live flow awareness | Real-time live options-flow posts / commands | Good |
| Watchlist monitoring | Ticker updates / automatic posts | Good, but likely less flexible than GUI |
| Macro risk | Economic news and market updates | Useful |
| Halt risk | Market halt/unhalt updates | Useful |
| Contract discovery | Highest-volume option-contract posts | Useful |
| Alerts | Discord automatic posts | Useful |
| Collaboration / journaling | Discord channel workflow | Good |

## What the Server plan likely cannot fully replace

| Need | Why Server plan is not enough |
|---|---|
| Full GUI workflow | Does not appear to include the same full web dashboard workflow as Professional |
| Periscope / SPX exposure | Not listed in the Server-plan description provided by user |
| Unlimited watchlists / Super Flow dashboards | Not listed in Server-plan description provided by user |
| Greeks/volatility dashboards | Not listed in Server-plan description provided by user |
| Custom multi-condition scoring | Discord posts/commands are not the same as Python scoring |
| Local database storage | No API/local ingestion |
| Automatic outcome tracking | Not available without custom system or manual journal |
| Flexible saved flow filters | Likely less robust than Professional GUI saved filters |

## Best use case

Use Server if the goal is:

```text
lowest-cost live flow notifications in Discord
semi-automated Discord watch channel
fast scan of high-volume contracts and ticker updates
market/news/halt awareness
manual decision-making outside the UW web GUI
```

Do not use Server alone if the goal is:

```text
Professional GUI dashboard workflow
Periscope/GEX/SPX exposure analysis
Greeks/volatility dashboard review
custom A+ score computation
local database and outcome tracking
```

## Recommended decision

### Cheapest test path

```text
Server plan first
```

Use it to test whether live flow and automatic Discord posts are useful.

### Better manual trading workflow

```text
Professional plan first
```

Use it if Periscope, Greeks/volatility dashboards, custom alerts, Super Flow dashboards, unlimited watchlists, and GUI filtering matter.

### Full automation path

```text
API Advanced
```

Use it only when Python automation, local storage, custom scoring, and outcome tracking are needed.

## Practical recommendation for UW-Signals

If the user wants the lowest-cost starting point:

```text
Start with Server for one month if month-to-month is available.
Build a Discord alert room.
Manually score only the best posts.
Upgrade to Professional if the missing GUI context creates too much uncertainty.
Upgrade to API Advanced only after the workflow proves useful and automation is required.
```

If the user wants the strongest manual decision system immediately:

```text
Start with Professional instead of Server.
```

## Server-based Discord room layout

Recommended private Discord channels:

```text
#uw-flow-spx-0dte
#uw-flow-qqq-0dte
#uw-flow-watchlist-stocks
#uw-market-news-halts
#uw-a-plus-candidates
#uw-trade-journal
#uw-outcome-review
```

## Manual A+ decision rule using Server

A Discord post is only a trigger.

Before trading, confirm manually:

```text
Flow repeats or clusters.
Ticker matches approved universe.
Expiration is 0DTE or current weekly.
Contract spread is acceptable.
Volume/OI context is strong.
Underlying price confirms.
Market direction confirms.
No major news/macro/earnings trap.
```

Final rule:

```text
Server plan can surface opportunities, but the trader must still validate the setup before entry.
```
