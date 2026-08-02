# WJ Capital

An AI value-investing firm you install into [Claude Code](https://claude.com/claude-code):
eight specialist research agents, seven disciplined workflows, a written doctrine, and a
finance-data server wired straight to primary sources.

**You are the fund manager and the only decision-maker.** The AI team reads filings,
verifies every number against the source, argues against itself, and keeps the written
record. It never decides, never predicts prices, and never places a trade.

---

## Install

```sh
# 1. Identify yourself to SEC EDGAR — required, no default is shipped
export SEC_EDGAR_USER_AGENT="Your Name you@example.com"

# 2. Add the marketplace and install
claude plugin marketplace add <your-github-user>/wj-capital
claude plugin install wj-capital@wj-capital-marketplace

# 3. Create the finance server's virtualenv
cd "$(claude plugin details wj-capital --path)" \
  && python3 -m venv mcp/.venv \
  && mcp/.venv/bin/pip install -r mcp/requirements.txt
```

Restart Claude Code. Full setup notes, including why each step is the way it is, are in
[`wj-capital/README.md`](wj-capital/README.md).

## Use

| Command | What it does |
|---|---|
| `/triage TICKER` | Fast first look — DEEP-DIVE / WATCHLIST / TOO HARD / PASS |
| `/deep-dive TICKER` | The full production line: 3 parallel specialists → adversarial review → checklist gate → sizing → memo |
| `/red-team TICKER` | Standalone attack on a thesis, including ones you already own |
| `/clone` | Superinvestor 13F sweep |
| `/portfolio-review` | Thesis health, sizing drift, correlations, cash |
| `/record-decision` | Same-day decision journal for every trade |
| `/quarterly-letter` | The accountability letter to your future self |

## Why it is built this way

Three structural choices do most of the work:

- **Context firewalls.** Specialists read thousands of pages inside their own context and
  return ≤1,500 words. The firm reads everything without drowning your session.
- **Adversarial separation.** Analysts form views before hearing your thesis, and the
  devil's advocate is never told your conclusion is the right one. Anti-sycophancy by
  structure rather than by willpower.
- **Tool-grounded numbers.** No financial figure ever comes from model memory. Every one
  carries a source tag; anything unverifiable is marked **UNVERIFIED**.

The reasoning behind all of it — the research it is built on, each agent's mandate, the
workflows, the data layer — is in the
[**Operating Manual**](docs/operating-manual.md).

## Your records stay yours

The firm's memos, decision journal, letters and portfolio live in `wj-records/` in
*your* working folder, created on first use. Nothing in this repository contains or
collects holdings, and `wj-records/` is gitignored so a clone of this repo can never
turn your positions into a pull request. Keep that folder somewhere permanent and back
it up — it is the firm's institutional memory.

## Disclaimer

**This is research tooling, not investment advice.** Nothing it produces is a
recommendation to buy or sell any security, and its authors are not licensed investment
advisers. Data comes from third-party sources that may be incomplete, delayed or wrong —
verify every load-bearing figure against primary filings before acting. Your decisions
and their outcomes are yours alone.

MIT licensed. See [LICENSE](LICENSE).
