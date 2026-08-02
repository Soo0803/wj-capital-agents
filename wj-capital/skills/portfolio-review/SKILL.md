---
name: portfolio-review
description: >
  This skill should be used when the user wants to review the portfolio — "portfolio
  review", "review my holdings", "how are we positioned", "check my positions", monthly
  or quarterly reviews, or after large market moves. Covers thesis health, sizing drift,
  correlations, cash, and watchlist readiness.
metadata:
  version: "0.1.0"
---

# Portfolio Review

Load the firm-doctrine skill (ground-rules + sizing-and-selling).

## Inputs

Read `wj-records/portfolio.md` and `wj-records/watchlist.md` if they exist. If they do
not, ask the user for current holdings (ticker, shares or weight, cost basis, buy date)
and have the **scribe** create the files first — the review is only as good as the record.

## Procedure

1. Dispatch **risk-officer** with the portfolio file and the objective: full review —
   current weights and prices (tool-fetched), price vs each memo's intrinsic-value range,
   concentration and hidden-correlation analysis, liquidity, FX mix, cash level,
   doctrine-drift check, and the drawdown-preparedness check (is the watchlist stocked
   with buy-below prices?).
2. In parallel, for each holding whose memo lists pre-committed falsifiers, have the
   risk-officer check headline-level whether any appear to have fired; anything
   suspicious gets a targeted **red-team** follow-up (separate dispatch per name, only
   where warranted — effort scaling, not blanket re-research).
3. On return, synthesize inline: the state of the portfolio in ≤1 page, verdict-first.

## Output (to the user)

- Portfolio table: weight / cost / price [source] / vs intrinsic range / thesis health /
  next re-underwrite date
- Concerns ranked by potential PERMANENT loss (not volatility)
- Any sell-discipline or ground-rule trigger in bold (with the rule quoted) — decision
  left to the founder, no urgency
- Cash and watchlist readiness: which watchlist names are near buy-below prices
- Suggested follow-ups (re-underwrites due, UNVERIFIED items to close)
- Have the **scribe** update `portfolio.md` with the review date and findings.

Never suggest trading because prices moved. Quotes don't kill theses; facts do.
