# Example output — an investment memo

> ### ⚠️ Fictional company. Every number below is invented.
>
> **Calder Fastening Systems** does not exist. This memo shows the *shape* of what
> `/deep-dive` produces — the section structure, the source tags, the UNVERIFIED
> flags, the unsoftened red-team verdict. It is not analysis, not a recommendation,
> and not about any real business. A real memo's figures all come from filings
> fetched at runtime.

---

## Calder Fastening Systems (NYSE: CFSY) — WATCHLIST — 2026-03-14

**One-line thesis:** A boring, profitable maker of aerospace fasteners was spun out of a
conglomerate, is too small for its former holders to keep, and is being sold by people who
have never valued it on its own — but the mispricing is only ~20%, not enough yet.

### 1. The business (what we would own)

Calder makes threaded fasteners and precision locking components for commercial aircraft
engines. Roughly 70% of revenue is aftermarket [10-K FY2025 p.7 via SEC EDGAR], which is
the part that matters: a fastener certified into an engine programme cannot be swapped for
a competitor's without re-qualification costing more than a decade of fastener spend.

Unit economics are ordinary at the gross line (38.2% GM, FY2025 [XBRL `GrossProfit`
/ `Revenues`]) and unusual below it — maintenance capex runs 1.9% of sales because the
plants are old, paid for, and adequate.

The moat is qualification lock-in, and its trajectory is flat to slowly improving: content
per engine has grown 3.1% annually over ten years [10-K FY2016–FY2025, `RevenuePerUnit`
disclosures], while ROIC has held between 14% and 19% through a pandemic that halved
flight hours. That is moat evidence rather than moat narrative.

### 2. Why the opportunity exists (the mispricing mechanism)

Spun off from Halloran Industrial in November 2025 at a $840M market cap. Halloran holders
received one CFSY share per twelve. **The mechanism is forced selling:** Halloran was an
S&P 500 constituent, CFSY is not, so index funds holding ~31% of the parent [DEF 14A 2025
ownership table] had to sell irrespective of price. Sell-side coverage is one analyst.

Consensus, to the extent it exists, treats CFSY as a cyclical industrial trading on peak
aftermarket earnings. We believe the aftermarket revenue is closer to an annuity than a
cycle, because it tracks the installed fleet's flight hours rather than new aircraft
orders — and the installed fleet keeps flying longer as new deliveries slip.

### 3. The numbers (all tool-fetched)

| FY | Revenue $M | Op income $M | FCF $M | ROIC | Shares M | Net debt $M |
|---|---|---|---|---|---|---|
| 2021 | 412 | 51 | 44 | 11.2% | 61.0 | 210 |
| 2022 | 468 | 71 | 58 | 14.1% | 60.8 | 188 |
| 2023 | 524 | 89 | 77 | 16.8% | 60.5 | 151 |
| 2024 | 571 | 101 | 88 | 18.0% | 60.2 | 122 |
| 2025 | 598 | 104 | 91 | 18.6% | 60.1 | 104 |

*All rows: SEC XBRL company facts, accession 0000320193-26-000012. ROIC computed in code
from `OperatingIncomeLoss` ÷ (total assets − current liabilities).*

**Normalized earnings power:** $86M owner earnings, derived by averaging FY2021–FY2025 FCF
and deducting a $5M annual charge for the maintenance capex the segment under-spent while
inside Halloran. **UNVERIFIED:** the under-spend figure comes from management's spin-off
roadshow, not from a filing. It is load-bearing and must be confirmed against the first
standalone 10-K.

**Balance-sheet survival:** revenue −30% for 18 months leaves $41M FCF against $19M
interest and no maturities before 2031 [10-K FY2025 Note 9]. Survives without external
capital. Computed, not asserted.

### 4. Valuation

**Method 1 — earnings power vs history and hurdle.** $86M normalized owner earnings on
60.1M shares = $1.43/share. At a 10% hurdle with no growth: **$14.30 LOW.** Granting the
3% content growth the ten-year record supports: **$19.10 BASE.**

**Method 2 — private-market comparables.** Three aerospace fastener transactions since 2019
cleared at 11–14× EBIT [transaction values UNVERIFIED — press reports, not filings]. At
11× FY2025 EBIT less net debt: **$17.30.** Independent of Method 1 and lands close, which
is mild corroboration rather than proof.

**Intrinsic value range: LOW $14.30 / BASE $19.10.** No high case — we don't buy the high case.

**Current price $15.40. Margin of safety vs BASE: 19.4%.**

**Reverse-engineered expectations:** at $15.40 the market is pricing roughly 0.5% perpetual
real growth. That is pessimistic against a ten-year record of 3.1%, but it is not absurd —
the market is not obviously wrong here, it is mildly wrong.

### 5. The bear case (strongest honest form)

**1. The aftermarket annuity is a post-COVID catch-up bulge, not a baseline.**
Shops deferred maintenance through 2020–21 and are working through backlog now. FY2024–25
growth would then be pull-forward, and normalized earnings are overstated by perhaps 15%.
*Our answer:* partial admission. Aftermarket revenue grew 4.2% annually in FY2016–19,
before any pandemic distortion [10-K FY2019 segment note], so the annuity predates COVID —
but we cannot rule out that the 2024–25 rate is inflated. This is why we use a five-year
average rather than the trailing year.

**2. Single-programme concentration.** 34% of aftermarket revenue comes from one engine
family [10-K FY2025 p.19]. A successor design that re-qualifies fasteners removes it.
*Our answer:* we cannot refute this. The programme's replacement is not expected before
2034 [**UNVERIFIED** — trade press], and re-qualification historically takes 3–5 years,
but a decade of visibility on a third of the aftermarket is the thesis's weakest joint.

**3. Post-spin managements dress the first year.** Working capital was released into the
spin, flattering FCF.
*Our answer:* refuted on the numbers. Receivable days moved 47→49 and inventory days 88→91
[XBRL, FY2024 vs FY2025] — working capital was a modest *use* of cash, not a source.

### 6. Falsifiers & re-underwriting triggers (pre-committed)

- Aftermarket revenue growth below 1% for two consecutive quarters → the annuity claim is wrong.
- The first standalone 10-K shows maintenance capex above 3.5% of sales → normalized
  earnings power is overstated and the valuation must be rebuilt.
- Any announced re-qualification on the concentrated engine programme → thesis void, exit
  regardless of price.
- Net debt rising above $150M without an acquisition → capital discipline claim is wrong.

**Scheduled re-underwrite:** first standalone 10-K, expected February 2027.

### 7. Risk of permanent loss

Realistic downside: aftermarket normalizes 15% lower *and* multiple compresses to 9× EBIT
→ roughly $11.20, a 27% loss from here. Permanent-loss risk is genuinely low — the balance
sheet survives, the product is certified in, and the plants are written down. This is a
**high-uncertainty, low-risk** situation in Buffett's sense, which is the kind we want.

### 8. Checklist result

**PASS 71 · FLAG 4 · FAIL 0 · N/A 15** — gate passed with flags.

| # | Item | Result | Response |
|---|---|---|---|
| 23 | Revenue concentration < 25% | **FLAG** | 34% single-programme, disclosed in §5 |
| 41 | Three years standalone audited financials | **FLAG** | Spun off Nov 2025; carve-out accounts only |
| 44 | Maintenance capex verifiable from filings | **FLAG** | Management estimate; falsifier set |
| 78 | Margin of safety ≥ 30% | **FLAG** | 19.4% — below the firm's bar |

### 9. Devil's-advocate verdict

**Survives with flags — but the price does not.**

The adversarial review could not break the moat evidence or the survival arithmetic, and
it refuted the working-capital objection outright. It did not accept the normalized
earnings figure: the maintenance-capex adjustment rests on a roadshow deck, and a 15%
error there moves BASE from $19.10 to about $16.60, which erases most of the margin of
safety at today's price.

Its closing observation, quoted unsoftened: *"You have found a real business at a fair
price and called it a bargain. The mechanism is genuine and the selling is genuine, but
19% is not a margin of safety on a company with one year of standalone accounts and one
customer programme worth a third of profits. Wait for the 10-K or wait for $13."*

### 10. Proposed action

**WATCHLIST — no purchase.** Checklist item 78 fails the firm's own bar and the red team
independently reached the same conclusion by a different route.

- **Buy-below price:** $13.40 (30% margin of safety vs BASE $19.10)
- **Size if triggered:** Standard tier, 4–6%. Not core — Li Lu's first test fails, because
  ten-year visibility on the concentrated programme is well below 90% confidence.
- **Re-underwrite on:** the February 2027 standalone 10-K, or a fall through $13.40, or
  any falsifier firing — whichever comes first.

### Sources

1. CFSY Form 10-K FY2025 — SEC EDGAR accession 0000320193-26-000012
2. CFSY Form 10-K FY2019, FY2016 — segment disclosures, via EDGAR
3. Halloran Industrial DEF 14A 2025 — beneficial ownership table
4. SEC XBRL company facts API — revenue, operating income, FCF, share count, debt
5. Comparable transaction multiples — trade press, **UNVERIFIED**, not used in the primary method

---
*Decision rights: the fund manager. This is research, not advice. Verify all load-bearing
numbers against primary filings before acting.*
