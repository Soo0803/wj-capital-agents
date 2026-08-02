---
name: record-decision
description: >
  This skill should be used immediately when the user reports an investment decision or
  trade — "I bought X", "I sold Y", "I decided to pass on Z", "journal this decision".
  It writes the same-day decision-journal entry and updates the firm records, per ground
  rule 9.
metadata:
  version: "0.1.0"
---

# Record Decision — the same-day journal

Load the firm-doctrine skill (ground-rules).

## Procedure

1. Collect from the user in ONE question round (only what's missing from context):
   action (buy/sell/add/trim/pass), ticker, size (%, shares) and price, date, and — in
   his own words, 2–4 sentences — WHY NOW, expected holding period, and how he feels
   (calm / excited / fearful / bored). The emotional state matters: it is tomorrow's
   post-mortem data.
2. Cross-check the record: does a memo exist for this name in `wj-records/memos/`?
   Was the checklist gate passed? Red-team verdict? If any is missing for a BUY,
   record the journal entry anyway BUT flag prominently: "Ground rule 8 (no memo, no
   trade) was not satisfied — this is a process violation and will be reviewed in the
   quarterly letter." Do not lecture beyond the flag; the record does the work.
3. Verify the trade price is plausible against the day's range (`get_prices`) and tag it.
4. Dispatch **scribe** to write `journal/YYYY-MM-DD-TICKER-action.md` (full template:
   thesis in 4 sentences, expected value range, pre-committed falsifiers with dates,
   what would prove us wrong, emotional state, process-compliance flags) and to update
   `portfolio.md` and `watchlist.md` accordingly.
5. For SELLS: also ask which sell-discipline rule (1–4) justified it, record the answer
   verbatim, and schedule a post-mortem: dispatch **scribe** to draft it now if the
   position is fully closed.

## Output

Confirm the journal entry path and show the entry. If any process flags were raised,
repeat them once, neutrally. No praise, no judgment — the journal is a mirror.
