# WJ Capital — Operating Manual

*How the firm is organized, what every agent does, how the workflows run, and how to
operate and grow your AI value-investing team.*

Version 0.1.0

> **Doctrine lives in the plugin, not here.** This manual is the guided tour. The rules
> the agents actually load at runtime are in
> [`wj-capital/skills/firm-doctrine/references/`](../wj-capital/skills/firm-doctrine/references/) —
> `philosophy.md`, `ground-rules.md`, `checklist.md`, `memo-template.md`,
> `sizing-and-selling.md`, `ai-guardrails.md`. Where this manual and those files
> disagree, **those files win**: they are what runs.

> **Not investment advice.** See the [disclaimer](../wj-capital/README.md#disclaimers).

## Contents
Executive Summary
Part I — Research Foundations
Part II — The Firm (organization and the eight team members in detail)
Part III — The Workflows (standard operating procedures)
Part IV — The Data Layer
Part V — The Doctrine
Part VI — Installation, Operations, and Growth
Key Sources

## Executive Summary
This manual documents WJ Capital — your AI value-investing firm, delivered as an installable Claude plugin. The firm consists of eight specialist AI agents, seven disciplined workflows, a written doctrine (investment philosophy, ground rules, a 90-point pre-investment checklist, memo template, sizing and sell rules, and mandatory AI guardrails), and a custom finance-data server that gives every agent direct access to primary sources: SEC filings, as-filed XBRL financials, superinvestor 13F holdings, global prices and FX rates.
The design principle, drawn from both the great value investors and from published research on AI agent teams: you are the fund manager and the only decision-maker; the AI team does the research legwork, verifies every number against primary sources, argues both sides adversarially, and keeps the firm’s written record — but it never decides, never predicts prices, and never pushes you to trade.
Day one, after installing: say "/clone" to sweep the superinvestors’ latest filings, "/triage TICKER" for a fast first look at any idea, "/deep-dive TICKER" to run the full production line, and "I bought…" to have the decision journaled. Everything else in this manual is detail.

## Part I — Research Foundations

### 1.1 How strong AI agent teams are built (Anthropic’s guidance)
The firm’s architecture follows Anthropic’s published engineering guidance on agents, distilled to six rules:
- Start simple; add agents only where they pay. Multi-agent systems cost roughly 15× the tokens of a chat conversation. They are worth it for heavily parallelizable, breadth-first research — exactly what a deep dive is — and wasteful for simple lookups. WJ Capital therefore runs cheap tasks inline (triage) and reserves the multi-agent pipeline for full workups.
- Orchestrator–workers is the backbone pattern. A lead session decomposes the task and dispatches specialists that work in parallel; Anthropic’s own research system, built this way, beat a single-agent baseline by 90% on breadth-first research. In WJ Capital, your main session is the orchestrator ("Chief of Staff") and the eight agents are the workers.
- Context is the scarcest capital. Long contexts degrade recall ("context rot"). Specialists therefore do their heavy reading — thousands of pages of filings — inside their own context windows and return distilled summaries of at most ~1,500 words. This "context firewall" is why the firm can read everything without drowning the conversation you actually work in.
- Delegations must be explicit. Vague instructions cause duplicated and missing work. Every workflow in this plugin dispatches agents with a fixed template: objective, output format, tools and sources to use, boundaries (what NOT to do), and a maximum summary length.
- Verification is structural, not optional. The best agent systems use fresh-context reviewers who cannot be anchored by the reasoning that produced the work. WJ Capital institutionalizes this as the devil’s advocate (adversarial review with a mandate to refute) plus the checklist auditor (mechanical gate).
- Tools should be few, workflow-shaped, and token-efficient. The finance server exposes ten consolidated tools that return meaningful, source-tagged data rather than raw API plumbing.

### 1.2 What the evidence says about AI in investment research
The published record is clear about where AI helps and where it hurts:
- Reliably good: reading and summarizing filings at scale; cross-document synthesis (this year’s 10-K vs prior years, competitors’ filings); surfacing red flags in footnotes as candidates for human review; applying explicit checklists; devil’s advocacy on command; drafting memos from verified data. These are precisely the jobs assigned to the team.
- Unreliable: precise arithmetic without tools; stock-price forecasting (the longest-running AI-picked ETF underperformed the market; published "prediction" results have been withdrawn or decayed); recalling company facts from memory (documented hallucination of financial figures); and — most dangerous for you — sycophancy: models drift toward validating the user’s stated thesis.
- The mitigations are structural, and all are built in: every number must be tool-fetched from a primary source and carry a source tag; all arithmetic runs in code; analysts form views blind, before hearing your thesis; the devil’s advocate is never told your conclusion is correct; no agent predicts prices or urges action; and you verify load-bearing numbers before committing capital.
- Practitioner consensus (Bridgewater, Balyasny, Man Group, and Anthropic’s own financial-services design): AI as junior analysts doing breadth under human supervision — the human does depth, judgment, sizing and the final decision. That is exactly this firm’s constitution.

### 1.3 The multi-agent pattern borrowed from the literature
The most relevant published blueprint (the "TradingAgents" framework and its descendants) organizes agents as: specialist analysts → a structured bull-vs-bear debate → a risk-lens review → a single accountable decision node. WJ Capital uses the same organization with one deliberate change: the decision node is you, a human — never an agent. The persona-checklist pattern (each agent applying a codified philosophy) is implemented through the firm doctrine that every agent must load before working.

## Part II — The Firm

### 2.1 Organization and decision rights
WJ Capital is organized like the firms in your research report — one accountable mind, many informing minds, and structure that prevents forced errors:

| Seat | Who | Decides |
|---|---|---|
| Fund manager | You (human) | Everything: what to research further, buy, sell, size, override — always in writing, per the ground rules |
| Chief of staff / orchestrator | Main Claude session | How to decompose work, which agents to dispatch, synthesis of findings — never investment decisions |
| Specialists (8 agents) | AI subagents | Nothing. They research, verify, attack, audit, and draft |

This mirrors the unanimous view of the great investors on committees (Munger: "It’s hard to think of great success by committees in the investment world") while capturing the one thing committees do provide — structured challenge — through dedicated adversarial roles instead of votes.

### 2.2 The team, member by member

#### Idea Scout (sourcing)
Duty: find candidates and route them; never conclude. Hunting grounds: superinvestor 13F filings (Berkshire, Himalaya, Baupost, Pabrai, Oaktree, Aquamarine, Tweedy Browne, Fairfax — via the 13F tool with accession-number citations); mechanically produced mispricings (spinoffs, index deletions, post-bankruptcy equities, forced sellers, 52-week-low quality); statistical screens over SEC XBRL cross-sections; and watchlist patrol — comparing live prices against your written buy-below levels so panics convert into prepared purchases. Output: a ranked shortlist of 3–7 names, each with the mispricing mechanism named in one sentence, circle-of-competence plausibility, the biggest obvious risk, and a routing verdict (deep-dive / watchlist / too hard / pass).

#### Business Analyst (quality)
Duty: the deep qualitative study, done the way Li Lu teaches — as if a long-lost uncle left you the whole company. Works primary sources in strict order: three years of 10-Ks (business, risk factors, MD&A, and management’s old promises vs what happened), the proxy statement (incentives, related parties), transcripts and shareholder letters, competitors’ filings (the industry described without your company’s PR), and the 10-year financial record to test every qualitative claim ("a moat that never shows up in ROIC is a story"). Output: the Business Dossier — what the company does and who pays it, unit economics, moat with evidence and 10-year trajectory, industry structure, management capital-allocation record, the 10-year question, and a quality grade (A–D) with confidence level and unverified items listed. Works blind: never told your opinion first.

#### Forensic Accountant (truth of the numbers)
Duty: professional skepticism — treat the income statement as marketing until footnotes, cash flow and the balance sheet corroborate it. Builds the 10-year reconciliation (net income vs operating cash flow vs free cash flow; accruals gaps; receivables and inventory vs revenue; share count; debt), reads the accounting-policy, revenue, debt, lease, contingency and related-party notes plus the auditor’s report, audits non-GAAP adjustments across years, and runs the survival stress test: if revenue fell 30% for 18 months, does the company need external capital? — computed, not asserted. Output: accounting-quality grade (clean / minor flags / serious flags / uninvestable), survival verdict with the computation, numbered findings with source tags, and the three disclosures you should read with your own eyes.

#### Valuation Analyst (price vs value)
Duty: conservative approximation, never precision — "if the value doesn’t scream at you, it’s too close." Derives normalized mid-cycle earnings power from 5–10 year records with honest maintenance capex; values by two independent methods (earnings-power value against history, peers and a 10% hurdle; plus asset value, sum-of-parts or liquidation — a DCF only ever as a sanity check, labeled illustration); reverse-engineers what growth and margins the current price implies; and states the realistic downside case. All arithmetic runs in code on tool-fetched inputs, with the three most load-bearing numbers cross-checked against the actual filing. Output: LOW and BASE intrinsic value (no high case — the firm doesn’t buy high cases), margin of safety at the current price, the embedded-expectations verdict, and the one assumption the valuation is hostage to.

#### Devil’s Advocate (the structural Munger)
Duty: kill theses. Evaluated on the strength and evidential grounding of its attacks — agreement is failure, and so is lazy boilerplate contrarianism. Receives the evidence packet with your conclusion stripped out, and works seven axes: the mispricing claim (if you can’t name why the bargain exists, you’re the patsy); three specific thesis-killer scenarios with base rates; an audit that tries to break the packet’s load-bearing numbers against the filings; an active hunt for disconfirming evidence the packet doesn’t mention (short reports, litigation, insider selling, going-concern language); a behavioral audit of YOUR process (anchoring, social proof, boredom-buying, urgency); the strongest case the business is structurally worse in ten years; and a pre-mortem written from three years in the future. Output: a verdict (thesis broken / serious unresolved objections / survives with flags / survives cleanly) plus numbered falsifiers, each with what evidence would settle it. Doctrine: no memo is finalized until every falsifier has a written answer.

#### Checklist Auditor (the final gate)
Duty: mechanical rigor. Runs the firm’s ~90-point checklist — built, Pabrai-style, from the documented mistakes of great investors — item by item against the evidence packet, verifying independently with the data tools where the packet is silent, never assuming an answer. Sections: circle of competence, business quality, accounting red flags, balance-sheet survival, management incentives, industry, valuation, behavioral biases, portfolio fit, and the final gate (memo written? night slept on it?). Output: gate result (passed / passed with flags / failed), the full scored table with citations, every FAIL and FLAG expanded, and unanswered items as required follow-ups. Doctrine: any FAIL, or three-plus FLAGS, means the memo must explain why you proceed anyway — or you pass.

#### Risk Officer (portfolio survival)
Duty: portfolio-level thinking, where risk means permanent loss, never volatility. For new positions: verifies the process prerequisites exist, applies the sizing-tier framework (punch-card 15–25% only when both Li Lu tests pass; core 8–12%; standard 4–6%; starter 1–2%; special situation 2–5%), and computes portfolio fit — concentration, hidden correlations (same customer, same macro exposure, same currency), liquidity in days-to-exit, and the two survival numbers: portfolio impact if this position went to zero, and if the top three positions halved simultaneously. For reviews: thesis health per holding (have pre-committed falsifiers fired?), drift from doctrine norms, cash reported neutrally as the residual, and drawdown preparedness — is the watchlist stocked so a 30% market decline converts cash into positions per ground rule 5? Output: verdict-first, numbers-tabled, with any ground-rule violation flagged in bold at the top.

#### Scribe (the firm’s written memory)
Duty: the record — because at Buffett’s partnership, Oaktree and Baupost alike, the letters ARE the thinking, the record and the accountability. Maintains the records folder (wj-records/): investment memos assembled strictly from the research packet using the firm template (never adding facts, never softening the red-team verdict, preserving every source tag and UNVERIFIED flag); same-day decision-journal entries for every trade (thesis in four sentences, expected value range, pre-committed falsifiers, what would prove us wrong, and your stated emotional state — tomorrow’s post-mortem data); quarterly letters to your future self (results vs benchmark over 1/3/5 years, mistakes named plainly in their own section, a doctrine-adherence audit, no forecasts); post-mortems for every exit that name whether the cause was bad luck or bad process and propose the specific checklist amendment — this is how the firm compounds institutional knowledge; and the living watchlist and portfolio files.

## Part III — The Workflows (Standard Operating Procedures)
Each workflow is a skill you invoke by slash command or plain language. They encode the firm’s process so quality does not depend on remembering it.

| Workflow | When to use | What happens |
|---|---|---|
| /triage TICKER | Any new idea, first look | Fast, cheap, inline: snapshot, cheapness sniff, mispricing mechanism named, circle check, one killer-look at the filings. Verdict: DEEP-DIVE / WATCHLIST (with buy-below price) / TOO HARD / PASS |
| /deep-dive TICKER | An idea worth real work | The production line: business-analyst + forensic-accountant + valuation-analyst in parallel (blind) → synthesis → devil’s advocate attack → checklist gate → risk-officer sizing → scribe writes the memo → presented to you. Stops at every gate that fails |
| /red-team TICKER | You have a thesis or a position and want it attacked | Your conclusion is stripped; the devil’s advocate attacks the neutral evidence; for portfolio names it also checks whether your pre-committed falsifiers have fired |
| /clone | Weekly / quarterly idea sourcing | Idea-scout sweeps the superinvestor 13Fs for new positions and big adds, prices them vs the managers’ cost quarters, filters by your circle, routes 2–3 to triage. Caveats always attached: 45-day lag, US-longs only, ideas not conclusions |
| /portfolio-review | Monthly/quarterly, or after big market moves | Risk-officer reviews weights, price-vs-intrinsic-range, thesis health, correlations, liquidity, cash and watchlist readiness; sell-discipline triggers quoted in bold; scribe updates the records |
| /record-decision | Same day as ANY trade or pass decision | One question round, process-compliance cross-check (memo? checklist? red team?), plausibility check of your fill price, journal entry written, records updated. Process violations flagged neutrally — the record does the work |
| /quarterly-letter | Quarter end | The accountability letter to your future self: results vs benchmark (1/3/5yr), decisions restated from the journal (not reconstructed), mistakes in their own section, doctrine-adherence audit, what we’re studying. No forecasts |

### 3.1 The deep-dive pipeline in detail
- Phase 1 — parallel evidence (three agents, one dispatch). Each receives the same delegation template: objective, required output format, tools and sources, boundaries, and a ≤1,500-word summary cap. The business and valuation analysts are explicitly blind to your opinion.
- Phase 2 — synthesis. The orchestrator merges the three reports into a ~2-page evidence packet, resolves numeric contradictions by going back to the filing (the filing always wins), and lists open questions.
- Phase 3 — adversarial review. The devil’s advocate gets evidence only. Every falsifier it raises must be answered in writing — from the packet, by a targeted follow-up dispatch, or by an honest "OPEN".
- Phase 4 — the checklist gate. Mechanical, cited, complete. A failed gate stops the process at watchlist/pass unless you write the override justification yourself.
- Phase 5 — sizing and memo. Risk-officer proposes the evidence-supported tier; the scribe assembles the memo with nothing softened.
- Phase 6 — your decision. The firm presents and stops. Ground rule 8: no memo, no trade — and one night between decision and order.

### 3.2 The operating rhythm

| Cadence | Ritual |
|---|---|
| Weekly (~30 min) | Watchlist patrol (idea-scout); anything near buy-below prices; one /triage if something interesting surfaced |
| Quarterly | /clone after 13F season (mid-Feb, mid-May, mid-Aug, mid-Nov); /portfolio-review; /quarterly-letter; re-underwrites that came due |
| Per idea | triage → (if warranted) deep-dive → sleep on it → decide → /record-decision |
| Annually | Read the year’s letters and journal; post-mortem review; amend the checklist with what the year taught; re-state your circle of competence in writing |

## Part IV — The Data Layer
The wj-finance MCP server gives every agent primary-source data with provenance. Design rules: few workflow-shaped tools; token-efficient responses; a source tag on every figure; EDGAR beats aggregators; caching and rate-limiting keep the firm a polite citizen of free public infrastructure.

| Tool | What it returns | Source & notes |
|---|---|---|
| resolve_company | Ticker ↔ SEC CIK ↔ registered name | SEC company_tickers.json |
| get_financial_history | 10-year as-filed annual fundamentals (revenue, income, cash flow, capex, debt, equity, shares, EPS…) | SEC XBRL company facts — authoritative for US names; yfinance fallback for international (marked "verify against IR filings") |
| get_filings | Recent filings of any form with document URLs | SEC submissions API |
| get_filing_text | Any filing or IR page as clean text, in chunks, with phrase-jump (find="Risk Factors") | SEC Archives / direct fetch |
| search_filings | Full-text search across all filings since 2001 | EDGAR full-text search — screening for "material weakness", "going concern", customer names, competitor mentions |
| get_13f_holdings | A manager’s latest 13F positions, aggregated and weighted, with accession citation | SEC 13F-HR information tables; superinvestor shortcuts built in |
| get_company_profile | Price, market cap, ratios, sector, 52-week range, business summary | yfinance — screening-grade, works internationally (0700.HK, RMS.PA, 005930.KS…) |
| get_prices | Historical closes for drawdowns/ranges | yfinance, Stooq fallback |
| get_fx_rate | Spot/historical FX for multi-currency work | Frankfurter (ECB/central banks), no key |
| screen_by_metric | One accounting concept across ALL US filers for a period | SEC XBRL frames — raw material for cross-sectional screens |

Honest limits. yfinance is an unofficial source: fine for screening, never for deciding — the doctrine requires load-bearing numbers to be verified against filings. 13Fs lag 45 days and show only US-listed longs. International filings (HKEX, European registers) have no good free APIs; the firm reads them via get_filing_text on IR/exchange URLs, and the agents are instructed to say so when data confidence is lower. Earnings-call transcripts have no reliable free API; use company IR pages or paste transcripts into the conversation for analysis.

## Part V — The Doctrine (why each rule exists)
The full doctrine travels inside the plugin and loads automatically during investment work. Summary of what governs the firm and where each rule comes from:
- Investment philosophy — nine beliefs (ownership, Mr. Market, margin of safety, risk-control primacy, punch-card selectivity, second-level thinking, named mispricing mechanisms, cash as residual, no macro forecasting) and six nevers (no leverage, no shorting, no committees, no style drift, no urgency, no buying outside the written circle). Sources: Buffett/Munger, Li Lu, Pabrai, Marks, Klarman — as documented in your Phase-1 research report.
- Ground rules — twelve rules you set with yourself, Buffett-partnership style: judged over 3–5 years against a named benchmark; drawdowns are for deploying the watchlist, not selling; no memo, no trade; same-day journal; quarterly letters; the AI team is obligated to disagree in writing (rule 12).
- The 90-point checklist — ten sections built from documented investor mistakes; the final gate. Its most important property is Pabrai’s finding: the causes of most losses were visible before purchase.
- Sizing and selling — conviction tiers bounded by survival; the two Li Lu tests as the concentration bar; four legitimate sell reasons (intrinsic value reached, falsifier fired, decisively better use, discovered error) and the explicit list of illegitimate ones (price fell, position feels big, guru sold, macro headlines).
- AI guardrails — the seventeen mandatory rules that counter documented AI failure modes: tool-fetched numbers only, source tags, code-only arithmetic, no price prediction, no urgency, blind analysis, adversarial separation, fact/estimate/opinion labeling, "too hard" respected, and the decision-rights line on every memo.

## Part VI — Installation, Operations, and Growth

### 6.1 Installation
- **Set `SEC_EDGAR_USER_AGENT` to your own name and email first.** This is required, not optional: the server refuses to start without it, by design. SEC EDGAR throttles and blocks by *identity* rather than by IP, so a shipped default would mean every installation worldwide scraping as the same person — one heavy user getting everyone else blocked, with the traffic attributed to whoever's address it was. Put `export SEC_EDGAR_USER_AGENT="Your Name you@example.com"` in your shell profile so it is set before Claude Code launches.
- Install the plugin: `claude plugin marketplace add <owner>/wj-capital-agents` then `claude plugin install wj-capital@wj-capital-agents`.
- Build the finance server's virtualenv: `cd "$(claude plugin details wj-capital --path)" && ./install.sh`. A venv rather than a bare `pip install` because modern Pythons (Homebrew, Debian) refuse to install into the system interpreter — PEP 668 — and `.mcp.json` invokes `mcp/.venv/bin/python` by path. The script is safe to re-run; it repairs a half-built environment and tells you exactly what is wrong if the server will not start.
- Work from one permanent folder. The firm’s memory lives in wj-records/ (memos, journal, letters, post-mortems, watchlist, portfolio) — back it up; it is the compounding asset.

### 6.2 First week
- Day 1: read the doctrine files; edit the philosophy and ground rules until they are truly YOURS (rename the benchmark, currency, anything) — the firm enforces what is written, so write what you mean.
- Day 2: write your circle of competence into the philosophy file — industries you honestly understand, and the explicit too-hard list.
- Day 3: /clone, pick one name, /triage it.
- Day 4–5: /deep-dive the best candidate end-to-end to see every gate fire. Note where the process felt slow or noisy — then tune the skill files (they are plain text).
- Weekend: if you hold positions already, give the risk-officer your holdings and let the scribe build portfolio.md, then /portfolio-review.

### 6.3 Improving the firm (the firm is also a portfolio)
- Evaluate like Anthropic does: keep ~20 representative test prompts (a triage, a deep dive on a company you know well, a red-team of a thesis you KNOW is flawed) and re-run them after any prompt change; judge outcomes, not paths.
- Post-mortems amend the checklist. Every loss and every process violation should end as a one-line addition or sharpening of a checklist item — the same loop Pabrai used to build it.
- Let Claude improve Claude: when an agent underperforms, show the transcript to your main session and ask it to diagnose and propose edits to that agent’s file. Test against your eval set before adopting.
- Extend deliberately: natural additions are a transcript-analysis agent (paste transcripts in), an HKEX/Bursa retrieval skill for your region, a special-situations analyst (spinoffs/arbitrage per Greenblatt), and paid data (a transcript API, Tiingo) wired into the same MCP server. Add one at a time; every new agent is context and cost.

### 6.4 Boundaries (read once, remember always)
- Nothing this team produces is investment advice; it is research tooling for your private use.
- The AI never trades, never holds credentials to any brokerage, and must never be given them.
- Verify every load-bearing number against the primary filing with your own eyes before committing capital — the guardrails minimize hallucination risk; they cannot make it zero.
- The firm’s edge is your temperament amplified by structure. The tools read faster than any human alive; only you can supply the patience, the honesty in drawdowns, and the willingness to look wrong for years. That part was never automatable.

## Key Sources

### Agent-team design
- Anthropic — Building Effective Agents; How We Built Our Multi-Agent Research System; Effective Context Engineering for AI Agents; Writing Effective Tools for AI Agents (anthropic.com/engineering)
- Claude Code documentation — Subagents, Skills, Plugins, Memory, MCP (code.claude.com/docs); Claude Agent SDK (platform.claude.com/docs)
- IBM — What Is a Context Window? (ibm.com/think/topics/context-window)
- MAST: Why Do Multi-Agent LLM Systems Fail? (arXiv:2503.13657)

### AI in investment research
- TradingAgents: Multi-Agents LLM Financial Trading Framework (arXiv:2412.20138); FinRobot (arXiv:2405.14767); FinMem (arXiv:2311.13743)
- Kim, Muhn & Nikolaev — Financial Statement Analysis with LLMs (arXiv:2407.17866; withdrawn Feb 2025 — cited here as a caution)
- Lopez-Lira & Tang — Can ChatGPT Forecast Stock Price Movements? (arXiv:2304.07619)
- Anthropic — Towards Understanding Sycophancy in Language Models (arXiv:2310.13548); hallucination in financial LLMs (arXiv:2311.15548)
- CFA Institute — AI in Investment Management: From Exuberance to Realism (2025); Unstructured Data and AI (2024)
- Anthropic — Claude for Financial Services; press coverage of Bridgewater AIA Labs, Balyasny, Man Group, Two Sigma (Bloomberg, Fortune, P&I)

### Data infrastructure
- SEC EDGAR APIs and access rules (sec.gov/search-filings/edgar-application-programming-interfaces; data.sec.gov); Form 13F data sets (sec.gov)
- yfinance (unofficial), Stooq, Frankfurter/ECB; open-source reference servers: stefanoamorelli/sec-edgar-mcp, OpenBB Platform

### Investment doctrine
- The firm’s Phase-1 research report: "How the Great Value Investors Built Their Firms" (this session, July 2026) and all primary sources cited therein — Buffett Partnership letters, Berkshire Owner’s Manual, Li Lu’s lectures, Pabrai’s talks and books, Oaktree memos and philosophy, Klarman’s Margin of Safety.
