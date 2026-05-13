# Custom Alerts Page Investigation

## Page checked

```text
https://unusualwhales.com/custom-alerts?template=true
```

## Result

The page is a JavaScript app page titled:

```text
Create Custom Stock & Options Alerts | Unusual Whales
```

The public HTML did not expose a full text list of all alert-condition fields without login/session interaction.

## What this likely means

The custom alerts page may be exactly where a Professional/Server user can create reusable option-flow alert templates.

If the page allows alert templates based on the same fields shown in the UW Options Flow documentation, then it can replicate a meaningful portion of the API plan without code.

## Official docs supporting field availability

UW Options Flow docs confirm the flow feed contains:

```text
Ticker
Contract
Bid-Ask
Spot
Size
Premium
OI
Volume
IV
Code
Flags
DTE
% Diff
Side based on NBBO bid/ask proximity
```

The flow status docs confirm users can input custom filters and that GREEN/YELLOW/RED flow status indicates whether all/most/not all filtered trades are pushed live.

The flow status docs specifically mention base filters that can produce GREEN flow status:

```text
Size > OI + Minimum Premium of $5,000
Vol > OI + Minimum Premium of $5,000
Minimum Premium of $50,000
Minimum Premium of $10,000 + OTM only
```

## Implication for UW-Signals

If Custom Alerts supports these fields, we can create a GUI alert-template layer that maps closely to the original API scoring system.

Best alert-template families:

```text
SPX 0DTE Call A+ Watch
SPX 0DTE Put A+ Watch
QQQ 0DTE Call A+ Watch
QQQ 0DTE Put A+ Watch
SPY 0DTE Call Confirmation
SPY 0DTE Put Confirmation
NVDA Call Momentum
NVDA Put Breakdown
TSLA Call Momentum
TSLA Put Breakdown
Mega-cap Call Momentum
Mega-cap Put Breakdown
High Premium 0DTE Index Flow
Volume > OI 0DTE Flow
Size > OI 0DTE Flow
```

## Recommended A+ custom-alert logic

### Index 0DTE Call template

```text
Ticker: SPX or QQQ
DTE: 0
Option Type: Call
Side: Ask / Buy side
Premium: >= $50,000 for SPX, >= $25,000-$50,000 for QQQ
Volume > OI: enabled if available
Size > OI: enabled if available
OTM only: enabled for breakout watch, disabled for ATM continuation
Exclude multi-leg/spread flags if available
```

### Index 0DTE Put template

```text
Ticker: SPX or QQQ
DTE: 0
Option Type: Put
Side: Ask / Buy side
Premium: >= $50,000 for SPX, >= $25,000-$50,000 for QQQ
Volume > OI: enabled if available
Size > OI: enabled if available
OTM only: enabled for breakdown watch, disabled for ATM continuation
Exclude multi-leg/spread flags if available
```

### Single-stock call momentum template

```text
Ticker: NVDA, TSLA, AAPL, AMD, META, MSFT, AMZN
DTE: 0 or current weekly
Option Type: Call
Side: Ask / Buy side
Premium: >= $50,000 for NVDA/TSLA, >= $25,000 for others
Volume > OI: preferred
Size > OI: preferred
OTM only: enabled for breakout momentum
```

### Single-stock put breakdown template

```text
Ticker: NVDA, TSLA, AAPL, AMD, META, MSFT, AMZN
DTE: 0 or current weekly
Option Type: Put
Side: Ask / Buy side
Premium: >= $50,000 for NVDA/TSLA, >= $25,000 for others
Volume > OI: preferred
Size > OI: preferred
OTM only: enabled for breakdown momentum
```

## Remaining validation once logged in

Check whether custom alerts can filter by:

```text
DTE
Option type call/put
Side ask/bid
Premium minimum
Size minimum
Volume > OI
Size > OI
OTM only
Ticker/watchlist
Multi-leg/spread exclusion
Discord/web/mobile delivery
Custom alert template naming
```

## Decision impact

If these fields are available, then the best low-cost path becomes:

```text
Server or Professional plan
+ UW Custom Alerts templates
+ Discord/mobile alerts
+ optional private Python Discord parser
+ manual scorecard/outcome journal
```

API Advanced is only required when:

```text
Custom alerts cannot express the needed logic
Discord posts are missing data
Automatic scoring/outcome tracking becomes required
Local database ingestion is required
```
