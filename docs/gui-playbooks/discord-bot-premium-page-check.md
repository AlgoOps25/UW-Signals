# Discord Bot Premium Page Check

## Page checked

```text
https://unusualwhales.com/discord-bot#premium
```

## Result

The public text fetched from the page did not expose the full premium-plan feature table because the page appears to render dynamically.

However, the user-provided plan details plus official UW Discord bot docs clarify the likely role of the Server plan.

## What the Server plan appears to provide

From the user-provided premium section:

```text
$125/month
Unlimited command usage
Enhanced commands with additional functionality
View automatic posts in Discord
Real time live options flow data
Customize and send automatic posts to your Discord
Personalized setup and troubleshooting
```

## What official UW docs confirm

Official Discord bot docs confirm:

```text
The bot uses slash commands to retrieve options and stock data.
/followtheflow sets up automatic posts.
Automatic post topics include economic news updates, market updates, OI feed updates, market halts/unhalts, ticker updates for up to 10 custom stocks, highest-volume options contracts, and selected UW Twitter feeds.
The bot needs permissions to include embeds and files.
Support contact: support@unusualwhales.com
```

## What this means for UW-Signals

This strongly supports a Discord-first MVP:

```text
Server Plan
→ UW automatic posts and live flow in private Discord
→ Custom Alert templates if included
→ Layer 8 Python Discord listener
→ parse embeds/messages
→ 1m/5m/15m summaries
→ manual A+ confirmation
```

## What this still does not prove 100%

The premium page details do not, by themselves, fully prove:

```text
Which exact custom-alert filters are included.
Whether every custom alert template can be posted to Discord.
Whether the message/embed payload includes all fields needed for parsing.
Whether UW permits a second private bot to store and summarize posts locally.
Whether Market Tide, Net Flow, GEX, Periscope, or SPX Market Maker Exposure are included in Server.
```

## Decision impact

This page makes the Server plan the best first purchase candidate if the goal is to avoid API Advanced.

The remaining support question is now narrower:

```text
Can I use the Server plan to send my own custom options-flow alerts into my private Discord server, and can I run a private bot in that server to read and summarize those posts for personal use only?
```

## Current recommendation

Start with Server plan if month-to-month is available.

Upgrade only if:

```text
Server does not include required custom-alert posting.
Discord posts are not parseable.
UW does not allow private bot summarization.
Professional GUI context is needed.
API automation is needed.
```
