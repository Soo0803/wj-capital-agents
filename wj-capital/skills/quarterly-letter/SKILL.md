---
name: quarterly-letter
description: >
  This skill should be used when the user asks for the quarterly (or annual) letter —
  "write the quarterly letter", "quarter-end review", "annual letter". It produces the
  Buffett-partnership-style letter to the founder's future self: results vs benchmark,
  decisions and reasoning, mistakes admitted, doctrine adherence audit.
metadata:
  version: "0.1.0"
---

# Quarterly Letter — the accountability document

Load the firm-doctrine skill (ground-rules; the letters are the thinking, the record,
and the accountability).

## Procedure

1. Gather the quarter's record: `wj-records/journal/` entries this quarter,
   `portfolio.md`, `watchlist.md`, memos written, post-mortems filed.
2. Dispatch **risk-officer** for the quarter-end portfolio numbers: return vs benchmark
   (MSCI ACWI total return default; note USD and home currency) over the quarter and
   trailing 1/3/5 years where history exists — all tool-fetched with source tags. If the
   user's actual account returns are not recorded, ask for them once, or compute an
   approximation from the portfolio file and label it APPROXIMATION prominently.
3. Dispatch **scribe** to draft the letter with this structure:
   - Results table first, no commentary spin — then the reminder from ground rule 2
     (judge over 3–5 years)
   - What we did this quarter and why (buys, sells, passes, sizing changes) — reasoning
     restated from the journal, not reconstructed after the fact
   - **Mistakes and process violations, named plainly, in their own section** — the most
     important section; if the honest answer is "none identified", say what we might be
     missing instead
   - Thesis updates: falsifiers fired or approached, re-underwrites completed
   - Doctrine adherence audit: each ground rule tested this quarter and how we behaved
   - What we are studying (circle-of-competence expansion work)
   - No forecasts, no targets, no promises — per doctrine
4. File as `letters/YYYY-QN.md`. Present the draft; the founder edits and finalizes —
   it is HIS letter to his future self.

Tone: Buffett-plain. Short sentences. Numbers with sources. Candor over comfort.
