# Server Plan Discord Ingestion Design

## Purpose

Evaluate whether UW Server plan Discord posts can be read by a private Python Discord bot and summarized every few minutes.

## Conclusion

This may be technically possible if:

```text
1. UW Server plan posts enough structured flow information into your Discord server.
2. A private Discord bot has permission to read the target channels.
3. The bot can access message content and embeds.
4. UW terms allow private local processing of those Discord posts.
5. The message format is consistent enough to parse.
```

This is not equivalent to API Advanced, but it can be a lower-cost bridge.

## Best role

```text
UW Server plan
→ Discord automatic posts
→ private Python Discord listener
→ parse message embeds
→ summarize every 1–5 minutes
→ manually validate A+ calls/puts
```

## Technical architecture

```text
Unusual Whales Server Plan
    ↓
UW bot automatic posts in Discord
    ↓
Private Discord channel(s)
    ↓
Layer 8 Python Discord listener bot
    ↓
Parse content / embeds / fields
    ↓
SQLite raw_discord_messages table
    ↓
Rolling 1m / 5m / 15m summarizer
    ↓
A+ candidate summary post
    ↓
Manual confirmation in UW GUI / TradingView
```

## Discord requirements

Discord message objects include fields such as:

```text
content
embeds
attachments
components
```

Discord states these fields require Message Content privileged intent when applicable.

For a private bot in one personal server, this may be simpler than a public bot, but the setting still needs to be enabled in the Discord Developer Portal and requested in code.

## What we can process

If the UW bot posts structured embeds with useful fields, we can parse:

```text
ticker
contract
expiration
strike
call/put
premium
volume
open interest
bid/ask if displayed
side / aggressor label if displayed
headline / market update text
halt/unhalt updates
highest-volume contracts
```

## What we may not get

Discord posts may not include every field available in the API or GUI.

Possible missing fields:

```text
full option-chain snapshots
complete full tape
GEX / Greeks detail
Market Tide / Net Flow raw values
bid/ask details
underlying price snapshots
complete historical lookback
clean machine-readable IDs
```

## Main risk

The Discord bot output is not guaranteed to be a stable machine-readable API.

UW can change message formatting, embed fields, or command outputs.

Therefore this should be treated as:

```text
low-cost experimental ingestion
```

not:

```text
production-grade data feed
```

## Compliance question for UW

Before building this, ask UW:

```text
If I subscribe to the Server plan and configure automatic posts to my private Discord server, am I allowed to run my own private Discord bot in that same server to read those UW posts, store them locally, and summarize them every few minutes for my own personal trading use only, with no redistribution or resale?
```

## MVP test checklist

```text
[ ] Subscribe to Server plan month-to-month if available.
[ ] Create private Discord server.
[ ] Add UW bot.
[ ] Configure /followtheflow automatic posts.
[ ] Create dedicated channels for SPX/QQQ/stocks/news/halts.
[ ] Add private Layer 8 listener bot.
[ ] Enable Message Content intent if required.
[ ] Confirm Python can read content/embeds.
[ ] Store raw Discord messages in SQLite.
[ ] Build 5-minute summary report.
[ ] Manually compare Discord summary with UW GUI.
[ ] Decide if Server plan provides enough information.
```

## Summary cadence

Recommended summaries:

```text
Every 1 minute: urgent A+ candidates only
Every 5 minutes: flow clusters and ticker summaries
Every 15 minutes: market regime summary
End of day: outcome review
```

## Final decision rule

Use Server + Discord ingestion if:

```text
UW posts include enough structured flow data.
UW permits private local processing.
Manual confirmation remains acceptable.
```

Upgrade to Professional if:

```text
Discord posts lack enough context and the GUI is needed.
```

Upgrade to API Advanced if:

```text
Discord formatting is too unstable, missing too many fields, or automation/outcome tracking becomes critical.
```
