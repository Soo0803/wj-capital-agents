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
# 1. Identify yourself to SEC EDGAR, then reload your shell.
#    Required — no default is shipped, and the server refuses to start without it.
echo 'export SEC_EDGAR_USER_AGENT="Your Name you@example.com"' >> ~/.zshrc && exec zsh

# 2. Install
claude plugin marketplace add Soo0803/wj-capital-agents
claude plugin install wj-capital@wj-capital-agents

# 3. Build the finance server's virtualenv
cd "$(claude plugin details wj-capital --path)" && ./install.sh
```

Restart Claude Code, then try `/wj-capital:triage AAPL`.

`install.sh` is safe to re-run — it repairs a half-built environment and tells you exactly
what is wrong if the server won't start. Setup notes with the reasoning behind each step
are in [`wj-capital/README.md`](wj-capital/README.md).

### See what you get first

[**docs/example-memo.md**](docs/example-memo.md) is a complete `/deep-dive` output on a
fictional company — source tags, UNVERIFIED flags, the checklist scorecard, and a red-team
verdict that talks the fund manager *out* of the trade. Read it before installing; it is a
more honest description of this tool than anything on this page.

### A note on cost

`/deep-dive` dispatches six or more agents, several of which read entire filings. A full
workup costs meaningfully more than a chat — the published figure for multi-agent research
is around 15× a single conversation. That is the deal: you pay tokens to have three
specialists and an adversary read what you would not have read. Use `/triage` first; it is
cheap by design, and most ideas should die there.

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

## Standing on their shoulders

Nothing in this firm's doctrine is original. It is an attempt to encode, faithfully and in
executable form, what six investors spent their careers explaining in public for free —
in letters, lectures, books and annual meetings, to anyone who cared to read them. Their
generosity in teaching is the reason a solo investor can run a disciplined process at all.

**Warren Buffett** — the punch card with twenty lifetime slots, which is why this firm is
built to say no; the circle of competence, honestly drawn; owner earnings over reported
earnings; and rule number one, don't lose money. The annual letters are the model for
`/quarterly-letter`.

**Charlie Munger** — inversion: ask what would destroy this, not what would prove it. The
`devils-advocate` agent exists because Munger insisted every idea deserves an "abominable
no-man," and it is graded on the strength of its refutations because agreement is worthless.
The firm's rejection of decision-by-committee is his too.

**Mohnish Pabrai** — cloning without ego, which is what `/clone` does with 13F filings; and
the checklist built from other investors' documented mistakes rather than from theory,
which is what `checklist-auditor` runs. "Heads I win, tails I don't lose much" is the
asymmetry every memo is tested against.

**Li Lu** — research as investigative journalism: read as though a long-lost uncle left you
the whole business and there is no one to ask. His twin tests gate concentration here —
ten-year visibility at ~90% confidence, and the willingness to buy more after a 50% fall.
His three lessons against shorting are why this firm never shorts.

**Howard Marks** — second-level thinking, which turns "is this a good company?" into "what
is already in the price, and why is the consensus wrong?" Risk as permanent loss rather
than volatility. And the discipline behind every refusal to forecast here: you can't
predict, you can prepare.

**Seth Klarman** — margin of safety as the first principle rather than a nicety; cash held
without apology as the residual of the opportunity set; and the insight that mispricings
have *mechanisms* — forced sellers, spinoffs, index deletions, neglect — which is what
`idea-scout` hunts rather than screening on multiples alone.

Any errors in the translation from their ideas to this code are ours, not theirs. Read the
originals; this is a scaffold for applying them, never a substitute for understanding them.

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
