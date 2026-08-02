---
name: red-team
description: >
  This skill should be used when the user wants a thesis ATTACKED — "red team this",
  "attack my thesis on X", "why am I wrong about X", "steelman the bear case", "kill this
  idea". Runs the firm's adversarial review standalone (outside a full deep dive),
  including on existing portfolio positions.
metadata:
  version: "0.1.0"
---

# Red Team — standalone adversarial review

Load the firm-doctrine skill (ai-guardrails is the critical file here).

## Procedure

1. **Assemble the evidence packet WITHOUT the founder's conclusion.** If the user stated
   their thesis, extract only its FACTUAL claims into neutral form ("the company claims X
   market position; margins have been Y"). Strip advocacy. If an existing memo exists in
   `wj-records/memos/`, use its evidence sections, not its conclusions.
2. If evidence is thin, first gather minimally: `get_financial_history`,
   `get_company_profile`, latest 10-K risk factors via `get_filing_text` — enough for the
   attack to be evidence-based rather than speculative.
3. Dispatch **devils-advocate** with the neutral packet. For portfolio positions, also
   pass the pre-committed falsifiers from the original memo/journal and ask specifically:
   have any fired?
4. On return, do NOT soften the verdict. Present it verdict-first.

## Output (to the user)

- The red-team VERDICT, verbatim severity level
- Falsifiers ranked, each with: the attack, the evidence, what would settle it
- Which falsifiers you (the orchestrator) can answer from existing evidence — answer
  them; which require new work — list as follow-ups
- If this is a portfolio position and a pre-committed falsifier has FIRED: state in bold
  that sell-discipline rule 2 is triggered and the doctrine says facts kill theses —
  then leave the decision to the founder, without urgency language.

This skill is also the right response when the founder seems in love with an idea:
being argued with is a service he explicitly requested in ground rule 12.
