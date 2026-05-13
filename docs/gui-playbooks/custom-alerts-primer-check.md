# Custom Alerts Primer Check

## Page checked

```text
https://unusualwhales.com/information/custom-alerts-primer
```

## Result

The fetched page did not expose the full primer text in the public HTML. It returned AI/API reference instructions and pointed to the official API docs, OpenAPI spec, MCP server, AI skills, and API pricing page.

Because the full custom-alerts primer content appears to be rendered by the web app or gated behind interactive/session behavior, the exact GUI field list could not be confirmed from this URL alone.

## Useful confirmation from official API docs

The official API docs confirm a WebSocket endpoint group for:

```text
Custom alerts
Flow alerts
Option trades
Price
Market tide
Net flow
GEX
News
Trading halts
```

This matters because it confirms custom alerts are a first-class API/WebSocket concept, not just a UI-only feature.

## Useful confirmation from changelog search results

Search results show Unusual Whales changelog entries titled:

```text
Discord Server Bot - Enabled Custom Alerts
Added Market Tide alerts for the Custom Alert menu
Heat Map added to Super Flow + Custom Alert Update
```

The public page bodies were not exposed in fetchable text, but the titles strongly support that custom alerts can integrate with the Discord server bot and that Market Tide was added to the custom-alert menu.

## Practical implication

The Server plan + custom alerts + Discord ingestion path is now more plausible.

Possible architecture:

```text
UW Custom Alerts
→ Discord server bot automatic posts
→ private Discord channels
→ Layer 8 Python Discord listener
→ parse content/embeds
→ summarize every 1/5/15 minutes
→ manual A+ confirmation
```

## Remaining GUI validation checklist

Once logged in, verify the alert builder supports:

```text
Ticker / watchlist
Call / put
DTE
Premium threshold
Volume > OI
Size > OI
OTM only
Bid / ask side
Multi-leg/spread filters
Market Tide alerts
Flow Alerts delivery to Discord
Server bot custom-alert posts
Custom alert template naming
```

## Current decision

The Server plan is worth testing first if it is month-to-month and if custom alerts can be posted to Discord with enough structured detail.

API Advanced should wait until:

```text
Discord custom alerts are missing fields
Discord message format is too unstable
Automatic scoring/outcome tracking becomes mandatory
Custom local data ingestion is required
```
