---
name: triage
description: >
  This skill should be used when the user wants a QUICK first look at an investment idea —
  "triage TICKER", "quick look at X", "is X worth researching?", "first pass on this
  company". It is the firm's cheap fast filter: kill or route in ~15 minutes of work,
  NOT a full deep dive.
metadata:
  version: "0.1.0"
---

# Triage — the fast filter

Purpose: most ideas should die quickly and cheaply. Triage decides: DEEP-DIVE /
WATCHLIST / TOO HARD / PASS. It never concludes "buy".

Load the firm-doctrine skill first (philosophy + ai-guardrails minimum).

## Procedure (do this inline — no subagents for triage; keep it cheap)

1. **Identify**: `resolve_company` (US) or use the suffixed ticker directly.
   `get_company_profile` for the snapshot (price, mcap, ratios) — tag as screening-grade.
2. **Cheapness sniff**: `get_financial_history` (10y if US). Compute (in code, not
   in-head): earnings yield on normalized-ish average earnings, revenue/income trend,
   ROE range, share count trend, net debt. Is there PLAUSIBLE cheapness vs quality?
3. **Mispricing mechanism**: can it be NAMED in one sentence (forced seller, spinoff,
   panic, neglect, complexity)? If no candidate mechanism → likely fairly priced → PASS.
4. **Circle check**: is this analyzable by the founder (business model comprehensible,
   accounting readable, jurisdiction trustworthy)? Genuine doubt → TOO HARD (a success,
   not a failure).
5. **One killer look**: skim the latest 10-K risk factors / auditor's report via
   `get_filing_text` with `find` targeting: "going concern", "material weakness",
   "related party". Any hit → note it prominently.

## Output (to the user, compact)

- Verdict first: **DEEP-DIVE / WATCHLIST (with a suggested buy-below price and the
  reasoning) / TOO HARD / PASS** — one-paragraph justification
- The snapshot table with source tags
- The named mispricing mechanism (or its absence)
- The 3 questions a deep dive must answer
- Anything UNVERIFIED flagged

End with: "Triage only — no position without the full process (deep-dive → red-team →
checklist → memo). Decision rights: the fund manager."
