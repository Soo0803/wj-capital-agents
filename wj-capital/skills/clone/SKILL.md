---
name: clone
description: >
  This skill should be used when the user wants to source ideas from superinvestor
  filings — "run the clone screen", "what are the superinvestors buying", "check the
  13Fs", "any new positions at Berkshire/Himalaya/Baupost/Pabrai". Pabrai-style shameless
  cloning as an IDEA SOURCE (never as a conclusion).
metadata:
  version: "0.1.0"
---

# Clone — superinvestor 13F sweep

Load the firm-doctrine skill (philosophy: cloning sources ideas, never conclusions).

## Procedure

1. Dispatch **idea-scout** with the objective: sweep `get_13f_holdings` for the standard
   roster (berkshire, himalaya, baupost, pabrai, oaktree, aquamarine, tweedy, fairfax) —
   plus any manager the user names (by CIK if not in the roster).
2. Instruct it to focus on: NEW positions, large adds (>25% share increase), and
   concentrated high-conviction weights (>5% of a manager's 13F) — and to note for each:
   manager, weight, estimated cost context (price range during the quarter via
   `get_prices`), and whether the current price is above or below that range.
3. Require the caveats in the output: 45-day lag; US-listed longs only; a position may
   already be sold; Himalaya's non-US book is invisible; we don't know their reasons.
4. On return, apply the firm filter inline: circle of competence, plausible cheapness
   TODAY (not at their cost), analyzability. Route each survivor: TRIAGE candidate /
   ignore.

## Output

- Table of noteworthy 13F moves with source tags (accession numbers)
- Which 2–3 names deserve triage and the one-line reason each
- The reminder, verbatim: "A cloned idea still goes through the full process — triage,
  deep dive, red team, checklist. We copy homework sources, not homework answers."
