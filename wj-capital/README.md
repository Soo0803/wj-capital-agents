# WJ Capital — an AI value-investing firm

A complete AI research team for a one-decision-maker value-investing operation, modeled
on the practices of Buffett, Munger, Li Lu, Pabrai, Marks and Klarman, and built on
Anthropic's multi-agent design guidance. **The human fund manager is the
only decision-maker. The AI team researches, verifies, argues and drafts — it never
decides and never predicts prices.**

## The team (8 agents)

| Agent | Role | Modeled on |
|---|---|---|
| `idea-scout` | Sources ideas: 13F cloning, forced sellers, screens, watchlist patrol | Pabrai's cloning; Klarman's mispricing mechanics |
| `business-analyst` | Business quality, moat, industry, management — from primary filings | Li Lu's investigative-journalist research |
| `forensic-accountant` | Accounting red flags, footnotes, survival stress test | Pabrai's checklist origins; Klarman's risk-first |
| `valuation-analyst` | Conservative intrinsic-value range, two independent methods, embedded expectations | Buffett/Munger "value should scream"; Marks's second-level thinking |
| `devils-advocate` | Attacks every thesis; scored on refutation strength | Munger, "the abominable no-man" |
| `checklist-auditor` | Runs the ~90-point pre-investment checklist as the final gate | Pabrai/Gawande |
| `risk-officer` | Position sizing, correlations, liquidity, cash policy, drawdown prep | Marks's risk control; Klarman's cash discipline |
| `scribe` | Memos, decision journal, quarterly letters, post-mortems, records | Buffett's letters; Marks's memos |

## The workflows (skills)

- `/triage TICKER` — fast filter: DEEP-DIVE / WATCHLIST / TOO HARD / PASS
- `/deep-dive TICKER` — the full production line: 3 parallel specialists → adversarial
  review → checklist gate → sizing → memo
- `/red-team TICKER` — standalone thesis attack (works on portfolio positions too)
- `/clone` — superinvestor 13F sweep (Berkshire, Himalaya, Baupost, Pabrai, Oaktree…)
- `/portfolio-review` — thesis health, sizing drift, correlations, cash, watchlist readiness
- `/record-decision` — same-day decision journal for every trade
- `/quarterly-letter` — the accountability letter to your future self
- `firm-doctrine` — the firm's constitution (philosophy, ground rules, checklist, memo
  template, sizing/sell rules, AI guardrails), loaded automatically during investment work

## The data layer (MCP server `wj-finance`)

Primary-source financial data, free endpoints, with provenance on every figure:

| Tool | Source |
|---|---|
| `resolve_company` | SEC ticker/CIK map |
| `get_financial_history` | SEC XBRL company facts (as-filed, 10y); yfinance fallback for international |
| `get_filings`, `get_filing_text`, `search_filings` | SEC EDGAR submissions, archives, full-text search |
| `get_13f_holdings` | SEC 13F-HR information tables (superinvestor cloning) |
| `get_company_profile`, `get_prices` | yfinance (screening-grade), Stooq fallback |
| `get_fx_rate` | Frankfurter (ECB/central banks) |
| `screen_by_metric` | SEC XBRL frames (cross-sectional screens) |

## Setup

1. **Set `SEC_EDGAR_USER_AGENT` to your own name and email.** Required — the server
   refuses to start without it, deliberately.

   ```sh
   export SEC_EDGAR_USER_AGENT="Jane Doe jane@example.com"
   ```

   SEC EDGAR requires requests to identify a real person, and it throttles and blocks
   by *identity*, not by IP. If this plugin shipped a shared default, one heavy user
   would get everyone else blocked. Put the export in your shell profile so it is set
   before Claude Code launches.

2. **Create the server's virtualenv.** Python 3.10+:

   ```sh
   python3 -m venv mcp/.venv
   mcp/.venv/bin/pip install -r mcp/requirements.txt
   ```

   A venv rather than a bare `pip install` because most modern Pythons (Homebrew,
   Debian) refuse to install into the system interpreter — PEP 668. `.mcp.json` points
   at `mcp/.venv/bin/python` explicitly, so this path is not optional.

3. Install the plugin; the `wj-finance` MCP server starts automatically.
4. The firm's records live in `wj-records/` in your working folder (memos, journal,
   letters, post-mortems, watchlist, portfolio) — created on first use. Keep this folder
   in one permanent place (and back it up): it is the firm's institutional memory.

## Design principles (from the research)

- **Context firewalls**: specialists read thousands of pages in their own context and
  return ≤1,500-word distilled findings.
- **Blind analysis & adversarial separation**: analysts form views before hearing your
  thesis; the devil's advocate never sees your conclusion framed as correct (anti-
  sycophancy, by structure not willpower).
- **Tool-grounded numbers**: no financial figure from model memory, ever; every figure
  carries a source tag; EDGAR beats aggregators; UNVERIFIED items are flagged.
- **No price prediction, no urgency, no autonomous trading.** The gate sequence
  (memo → red team → checklist → one night's sleep) is doctrine.

## Disclaimers

**This is research tooling, not investment advice.** Nothing this team produces is a
recommendation to buy or sell any security, and no agent here is a licensed adviser.
You are the fund manager: every decision, and every consequence, is yours.

Verify all load-bearing numbers against primary filings before acting. The agents mark
figures they could not verify as **UNVERIFIED** — take that literally. yfinance data is
unofficial, undocumented and screening-grade only; 13F data lags ~45 days and covers
long US equity positions only, so it is an idea source, never a conclusion.

Provided under the MIT licence, without warranty of any kind.
