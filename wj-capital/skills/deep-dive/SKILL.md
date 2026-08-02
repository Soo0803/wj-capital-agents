---
name: deep-dive
description: >
  This skill should be used when the user wants the FULL research workup on a company —
  "deep dive on X", "full research on TICKER", "run the process on X", "work this one up".
  It orchestrates the whole firm: parallel specialist research, adversarial review,
  checklist gate, sizing, and the investment memo. Expect a long-running, multi-agent job.
metadata:
  version: "0.1.0"
---

# Deep Dive — the full research process

This is WJ Capital's core production line. The main session acts as Chief of Staff:
it orchestrates, synthesizes, and keeps context clean; specialists do the heavy reading
in their own context windows and return distilled findings (context-firewall design).

Load the firm-doctrine skill first. Confirm with the user only if the target is ambiguous;
otherwise proceed.

## Phase 1 — Parallel evidence gathering (single message, three agents at once)

Dispatch simultaneously, each with this delegation template filled in:
*objective / output format / tools & sources to use / boundaries (what NOT to do) /
max length of returned summary*:

1. **business-analyst** — the business-quality dossier. Boundary: no valuation, no
   buy/pass language. BLIND: do not tell it the founder's opinion of the stock.
2. **forensic-accountant** — accounting quality + survival stress test. Boundary:
   numbers quality only.
3. **valuation-analyst** — conservative intrinsic-value range + embedded expectations.
   BLIND: do not pass it any target price or the founder's lean.

Effort scaling: mega-cap with clean history → standard effort; complex/multi-segment/
non-US → tell agents to go deeper on specific sections and name them.

## Phase 2 — Synthesis (you, inline)

Merge the three reports into a coherent evidence packet (~2 pages). Resolve
contradictions explicitly — where two agents disagree on a number, the filing wins;
where they disagree on judgment, present both views. List open questions. Show the
packet to the user BRIEFLY (verdict-level summary) before the adversarial phase.

## Phase 3 — Adversarial review (mandatory)

Dispatch **devils-advocate** with the evidence packet. Do NOT include the founder's
opinion or your Phase-2 lean — evidence only. Its falsifiers must each get a written
answer: answer them yourself from the packet where possible; dispatch a targeted
follow-up to the relevant specialist where not; leave honestly OPEN what cannot be
resolved and say so.

## Phase 4 — Checklist gate (mandatory)

Dispatch **checklist-auditor** with everything (packet + red-team verdict + answers).
If the gate FAILS: report the failure prominently; the process stops at WATCHLIST or
PASS unless the founder explicitly writes the "why we proceed anyway" justification.

## Phase 5 — Sizing and memo

1. Dispatch **risk-officer** for the sizing recommendation and portfolio-fit analysis
   (only if the gate passed or the founder overrode in writing).
2. Dispatch **scribe** to assemble the full memo per template, filing it in
   `wj-records/memos/`, preserving all source tags, UNVERIFIED flags, and the
   unsoftened red-team verdict.

## Phase 6 — Present to the fund manager

Present: verdict-level summary (5–10 lines), the memo file, the checklist result, the
red-team verdict, and the sizing analysis. Then STOP. Recommend nothing with urgency.
The decision belongs to the fund manager; remind them of ground rule 8 (no memo, no trade;
one night between decision and order) and rule 87.

Throughout: every figure source-tagged; subagent returns ≤ ~1,500 words each; keep raw
filings out of the main context.
