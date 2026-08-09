#!/usr/bin/env python3
"""
WJ Capital — finance-data MCP server.

Free, reliable primary-source financial data for a value-investing research team.

Sources & precedence:
  - SEC EDGAR official APIs (US filings, XBRL fundamentals, 13F holdings) — authoritative for US names
  - yfinance (optional dependency) — global prices, profiles, and statements (unofficial; best-effort)
  - Stooq CSV — price fallback, no key
  - Frankfurter API — FX rates, no key

Etiquette: EDGAR requires a User-Agent identifying you (set SEC_EDGAR_USER_AGENT env var)
and max 10 req/s. This server rate-limits and caches to disk to stay well under limits.

All tools return JSON strings with a `source` field so analysts can cite provenance.
"""

import json
import os
import re
import time
import html as html_lib
from datetime import date
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

try:
    import yfinance as yf
    HAS_YF = True
except Exception:
    HAS_YF = False

mcp = FastMCP("wj-finance")

# ----------------------------------------------------------------------------- config
def _resolve_sec_ua() -> str:
    """SEC requires a User-Agent naming a real person and a reachable email, and it
    rate-limits and blocks per *identity*, not per IP. Shipping a default here would
    mean every installation worldwide scrapes EDGAR as the same person — one abuser
    gets everyone blocked, and the traffic is attributed to whoever's address it is.
    So there is deliberately no fallback: refuse to start instead."""
    ua = (os.environ.get("SEC_EDGAR_USER_AGENT") or "").strip()
    # An unexpanded "${SEC_EDGAR_USER_AGENT}" means the var was never set in the
    # environment Claude Code launched us from; treat it as absent, not as a value.
    if ua.startswith("${"):
        ua = ""
    if "@" not in ua:
        raise SystemExit(
            "wj-finance: set SEC_EDGAR_USER_AGENT before starting this server.\n"
            "  SEC EDGAR requires you to identify yourself, e.g.\n"
            '    export SEC_EDGAR_USER_AGENT="Jane Doe jane@example.com"\n'
            "  Use your own name and email — EDGAR blocks by identity, so a shared\n"
            "  or fake value gets every user of this plugin throttled together."
        )
    return ua


SEC_UA = _resolve_sec_ua()
HEADERS_SEC = {"User-Agent": SEC_UA, "Accept-Encoding": "gzip, deflate"}
CACHE_DIR = Path(os.environ.get("WJ_CACHE_DIR", str(Path.home() / ".cache" / "wj-capital")))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

_last_sec_call = [0.0]


def _sec_throttle():
    """Keep EDGAR traffic ≤ ~5 req/s (half the official 10/s ceiling)."""
    now = time.time()
    wait = 0.2 - (now - _last_sec_call[0])
    if wait > 0:
        time.sleep(wait)
    _last_sec_call[0] = time.time()


def _cache_get(key: str, max_age_s: int):
    p = CACHE_DIR / (re.sub(r"[^A-Za-z0-9_.-]", "_", key) + ".json")
    if p.exists() and (time.time() - p.stat().st_mtime) < max_age_s:
        try:
            return json.loads(p.read_text())
        except Exception:
            return None
    return None


def _cache_put(key: str, obj):
    p = CACHE_DIR / (re.sub(r"[^A-Za-z0-9_.-]", "_", key) + ".json")
    try:
        p.write_text(json.dumps(obj))
    except Exception:
        pass


def _get(url: str, headers=None, timeout=30):
    _sec_throttle() if "sec.gov" in url else None
    with httpx.Client(follow_redirects=True, timeout=timeout) as c:
        r = c.get(url, headers=headers or {})
        r.raise_for_status()
        return r


def _sec_json(url: str, cache_key: str, max_age_s: int = 6 * 3600):
    cached = _cache_get(cache_key, max_age_s)
    if cached is not None:
        return cached
    data = _get(url, headers=HEADERS_SEC).json()
    _cache_put(cache_key, data)
    return data


def _err(msg: str, **extra):
    return json.dumps({"error": msg, **extra})


# ----------------------------------------------------------------------------- ticker/CIK mapping
def _norm_ticker(t: str) -> str:
    """Share classes are written three ways for the same security — BRK.B, BRK-B, BRKB.
    SEC's file uses the hyphen; users and other data vendors use the dot or nothing.
    Both the map keys and the lookups must be normalized the SAME way, or every
    hyphenated ticker becomes unreachable."""
    return t.upper().replace("-", "").replace(".", "")


def _ticker_map():
    data = _sec_json("https://www.sec.gov/files/company_tickers.json", "company_tickers", 24 * 3600)
    out = {}
    for _, v in data.items():
        t = v["ticker"].upper()
        entry = {"cik": int(v["cik_str"]), "name": v["title"], "ticker": t}
        out[t] = entry
        # Also index under the punctuation-stripped form so BRK.B and BRKB both land.
        # setdefault so a real ticker is never shadowed by another's normalized form.
        out.setdefault(_norm_ticker(t), entry)
    return out


def _lookup_cik(ticker: str):
    tm = _ticker_map()
    return tm.get(ticker.upper()) or tm.get(_norm_ticker(ticker))


# Well-known superinvestor 13F filers (CIK numbers are stable public identifiers).
SUPERINVESTORS = {
    "berkshire": (1067983, "Berkshire Hathaway (Buffett)"),
    "himalaya": (1709323, "Himalaya Capital (Li Lu)"),
    "baupost": (1061768, "Baupost Group (Klarman)"),
    "pabrai": (1173334, "Dalal Street / Pabrai Funds (Pabrai)"),
    "oaktree": (949509, "Oaktree Capital (Marks)"),
    "aquamarine": (1426749, "Aquamarine Capital (Guy Spier)"),
    "greenlein": (1079114, "Sequoia / Ruane Cunniff"),
    "markel": (1096343, "Markel Gayner"),
    "tweedy": (732905, "Tweedy Browne"),
    "fairfax": (915191, "Fairfax Financial (Watsa)"),
}


@mcp.tool()
def resolve_company(query: str) -> str:
    """Resolve a company name or ticker to its identifiers.

    For US-listed companies returns ticker, SEC CIK number and registered name
    (needed by the EDGAR tools). For international tickers, pass the exchange-suffixed
    symbol (e.g. 0700.HK, RMS.PA, 005930.KS) straight to the price/profile tools instead.

    Args:
        query: Company name fragment or ticker symbol, e.g. "Alphabet" or "GOOGL".
    """
    q = query.strip().upper()
    tm = _ticker_map()
    hits = []
    if q in tm:
        hits.append(tm[q])
    for t, v in tm.items():
        if len(hits) >= 8:
            break
        if q in v["name"].upper() and v not in hits:
            hits.append(v)
    if not hits:
        return _err(f"No US-listed match for '{query}'. If it is a non-US listing, use the "
                    f"exchange-suffixed ticker directly (e.g. 0700.HK) with get_company_profile/get_prices.")
    return json.dumps({"source": "SEC company_tickers.json", "matches": hits[:8]})


# ----------------------------------------------------------------------------- fundamentals (EDGAR XBRL)
# Concept map: friendly name -> list of us-gaap tags to try in order.
CONCEPTS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax"],
    "net_income": ["NetIncomeLoss"],
    "operating_income": ["OperatingIncomeLoss"],
    "gross_profit": ["GrossProfit"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment"],
    "total_assets": ["Assets"],
    "total_liabilities": ["Liabilities"],
    "stockholders_equity": ["StockholdersEquity",
                            "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "long_term_debt": ["LongTermDebtNoncurrent", "LongTermDebt"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "shares_outstanding": ["CommonStockSharesOutstanding", "WeightedAverageNumberOfDilutedSharesOutstanding",
                           "EntityCommonStockSharesOutstanding"],
    "eps_diluted": ["EarningsPerShareDiluted"],
    "dividends_paid": ["PaymentsOfDividendsCommonStock", "PaymentsOfDividends"],
    "rnd_expense": ["ResearchAndDevelopmentExpense"],
    "interest_expense": ["InterestExpense"],
}


@mcp.tool()
def get_financial_history(ticker: str, years: int = 10, concepts: str = "") -> str:
    """Multi-year fundamental history from primary sources.

    US-listed companies: exact as-filed annual figures from SEC XBRL company facts
    (authoritative — cite as '10-K via SEC XBRL'). International tickers (with exchange
    suffix like 0700.HK): falls back to yfinance statements (~4 years, verify against
    the company's own IR reports before relying on them).

    Args:
        ticker: US ticker (AAPL) or suffixed international ticker (0700.HK).
        years: How many fiscal years back (default 10, US only; yfinance gives ~4).
        concepts: Optional comma-separated subset to fetch. Available: revenue, net_income,
            operating_income, gross_profit, operating_cash_flow, capex, total_assets,
            total_liabilities, stockholders_equity, long_term_debt, cash, shares_outstanding,
            eps_diluted, dividends_paid, rnd_expense, interest_expense. Default: all.
    """
    wanted = [c.strip() for c in concepts.split(",") if c.strip()] or list(CONCEPTS)
    info = _lookup_cik(ticker)
    if info:
        cik10 = f"{info['cik']:010d}"
        try:
            facts = _sec_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json",
                              f"facts_{cik10}", 12 * 3600)
        except Exception as e:
            return _err(f"EDGAR companyfacts failed: {e}")
        gaap = facts.get("facts", {}).get("us-gaap", {})
        dei = facts.get("facts", {}).get("dei", {})
        out = {}
        for name in wanted:
            tags = CONCEPTS.get(name)
            if not tags:
                continue
            series = {}
            for tag in tags:
                node = gaap.get(tag) or dei.get(tag)
                if not node:
                    continue
                for unit, vals in node.get("units", {}).items():
                    for v in vals:
                        # annual figures: 10-K frames, full-year duration or instant
                        if v.get("form") not in ("10-K", "10-K/A", "20-F", "20-F/A"):
                            continue
                        fy, fp = v.get("fy"), v.get("fp")
                        end = v.get("end", "")
                        if fp != "FY" or not fy:
                            continue
                        key = str(end[:4] if end else fy)
                        # prefer the latest-filed value for each year
                        series[key] = v.get("val")
                if series:
                    break
            if series:
                yrs = sorted(series)[-years:]
                out[name] = {y: series[y] for y in yrs}
        if not out:
            return _err("No XBRL annual data found (foreign private issuers under IFRS may "
                        "not populate us-gaap tags; try yfinance via an exchange-suffixed ticker or read the filing).")
        return json.dumps({
            "source": f"SEC XBRL companyfacts (as filed, 10-K/20-F), CIK {info['cik']}",
            "company": info["name"], "ticker": info["ticker"], "annual": out,
            "note": "Values in USD (or filing currency) as filed. Cite as filed figures.",
        })
    # ----- international / non-EDGAR fallback
    if not HAS_YF:
        return _err("Not a US-listed ticker and yfinance is not installed. "
                    "pip install yfinance, or supply figures from the company's IR reports.")
    try:
        t = yf.Ticker(ticker)
        blocks = {}
        for label, df in (("income_statement", t.income_stmt),
                          ("balance_sheet", t.balance_sheet),
                          ("cash_flow", t.cashflow)):
            if df is None or df.empty:
                continue
            blocks[label] = {
                str(col.date() if hasattr(col, "date") else col):
                    {str(idx): (None if v != v else float(v)) for idx, v in df[col].items()
                     if v == v}
                for col in df.columns
            }
        if not blocks:
            return _err(f"yfinance returned no statements for {ticker}.")
        return json.dumps({
            "source": "yfinance (unofficial Yahoo Finance; VERIFY against company IR filings before use)",
            "ticker": ticker, "statements": blocks,
        })
    except Exception as e:
        return _err(f"yfinance failed for {ticker}: {e}")


# ----------------------------------------------------------------------------- filings
@mcp.tool()
def get_filings(ticker: str, form: str = "10-K", limit: int = 8) -> str:
    """List a US company's recent SEC filings of a given form, with document URLs.

    Args:
        ticker: US-listed ticker.
        form: Form type, e.g. 10-K, 10-Q, 8-K, DEF 14A, 13F-HR, 20-F, S-1. Empty = all forms.
        limit: Max filings to return (default 8).
    """
    info = _lookup_cik(ticker)
    if not info:
        return _err(f"'{ticker}' is not in the SEC ticker map (US listings only).")
    cik10 = f"{info['cik']:010d}"
    subs = _sec_json(f"https://data.sec.gov/submissions/CIK{cik10}.json", f"subs_{cik10}", 3600)
    rec = subs.get("filings", {}).get("recent", {})
    rows = []
    for i in range(len(rec.get("accessionNumber", []))):
        f = rec["form"][i]
        if form and f.upper() != form.upper():
            continue
        acc = rec["accessionNumber"][i]
        acc_nodash = acc.replace("-", "")
        primary = rec["primaryDocument"][i]
        rows.append({
            "form": f,
            "filed": rec["filingDate"][i],
            "period": rec.get("reportDate", [""] * 9999)[i] if i < len(rec.get("reportDate", [])) else "",
            "accession": acc,
            "primary_doc_url": f"https://www.sec.gov/Archives/edgar/data/{info['cik']}/{acc_nodash}/{primary}",
        })
        if len(rows) >= limit:
            break
    return json.dumps({"source": "SEC EDGAR submissions API", "company": info["name"],
                       "cik": info["cik"], "filings": rows})


TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)
HTML_RE = re.compile(r"<[^>]+>")


def _html_to_text(raw: str) -> str:
    txt = TAG_RE.sub(" ", raw)
    txt = HTML_RE.sub(" ", txt)
    txt = html_lib.unescape(txt)
    txt = re.sub(r"[ \t\xa0]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n\n", txt)
    return txt.strip()


@mcp.tool()
def get_filing_text(url: str, offset: int = 0, max_chars: int = 40000, find: str = "") -> str:
    """Fetch an SEC filing document (or any IR page/document URL) as plain text, in chunks.

    A full 10-K can exceed 500k characters — read it in slices, or use `find` to jump to
    a phrase (e.g. 'Risk Factors', "Management's Discussion"). Returns text plus next_offset.

    Args:
        url: Document URL (from get_filings / search_filings), or a company IR page URL.
        offset: Character offset to start from (default 0).
        max_chars: Max characters to return (default 40000).
        find: Optional phrase — start the slice at its first occurrence at/after `offset`.
    """
    try:
        headers = HEADERS_SEC if "sec.gov" in url else {"User-Agent": SEC_UA}
        raw = _get(url, headers=headers, timeout=60).text
    except Exception as e:
        return _err(f"fetch failed: {e}")
    text = _html_to_text(raw) if "<" in raw[:1000] else raw
    n = len(text)
    start = min(offset, n)
    if find:
        pos = text.upper().find(find.upper(), start)
        if pos >= 0:
            start = max(pos - 200, 0)
        else:
            return _err(f"phrase '{find}' not found at/after offset {offset}", total_chars=n)
    end = min(start + max_chars, n)
    return json.dumps({
        "source": url, "total_chars": n, "start": start,
        "next_offset": end if end < n else None,
        "text": text[start:end],
    })


@mcp.tool()
def search_filings(query: str, forms: str = "", start_date: str = "", end_date: str = "", size: int = 10) -> str:
    """Full-text search across all SEC filings since 2001 (EDGAR full-text search).

    Great for screening: customer/supplier mentions, 'going concern', 'material weakness',
    product names, competitor mentions across companies.

    Args:
        query: Search terms. Use double quotes inside for exact phrases, e.g. '"net operating loss"'.
        forms: Optional comma-separated forms filter, e.g. "10-K,8-K".
        start_date: Optional YYYY-MM-DD.
        end_date: Optional YYYY-MM-DD.
        size: Max hits (default 10, max 50).
    """
    params = {"q": query, "size": str(min(size, 50))}
    if forms:
        params["forms"] = forms
    if start_date and end_date:
        params.update({"dateRange": "custom", "startdt": start_date, "enddt": end_date})
    from urllib.parse import urlencode
    url = f"https://efts.sec.gov/LATEST/search-index?{urlencode(params)}"
    try:
        data = _get(url, headers=HEADERS_SEC).json()
    except Exception as e:
        return _err(f"EDGAR full-text search failed: {e}")
    hits = []
    for h in data.get("hits", {}).get("hits", [])[:size]:
        src = h.get("_source", {})
        acc_file = h.get("_id", ":").split(":")
        acc, fname = (acc_file + [""])[:2]
        ciks = src.get("ciks", [])
        cik = int(ciks[0]) if ciks else None
        hits.append({
            "company": (src.get("display_names") or [""])[0],
            "form": src.get("root_forms") or src.get("file_type"),
            "filed": src.get("file_date"),
            "doc_url": (f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/{fname}"
                        if cik else None),
        })
    return json.dumps({"source": "SEC EDGAR full-text search (efts.sec.gov)",
                       "total": data.get("hits", {}).get("total", {}).get("value"), "hits": hits})


# ----------------------------------------------------------------------------- 13F cloning
@mcp.tool()
def get_13f_holdings(manager: str, top_n: int = 25) -> str:
    """Latest 13F-HR holdings of an institutional manager — for superinvestor idea sourcing.

    Known shortcuts: berkshire, himalaya, baupost, pabrai, oaktree, aquamarine, tweedy,
    fairfax, markel. Otherwise pass a manager's CIK number.
    Remember: 13Fs lag ~45 days, show US-listed longs only, and understate global books
    (e.g. Himalaya's non-US holdings are invisible).

    Args:
        manager: Shortcut name (see above) or a numeric CIK.
        top_n: Number of largest positions to return (default 25).
    """
    key = manager.strip().lower()
    if key in SUPERINVESTORS:
        cik, label = SUPERINVESTORS[key]
    elif key.isdigit():
        cik, label = int(key), f"CIK {key}"
    else:
        return _err(f"Unknown manager '{manager}'. Use one of {sorted(SUPERINVESTORS)} or a CIK number.")
    cik10 = f"{cik:010d}"
    subs = _sec_json(f"https://data.sec.gov/submissions/CIK{cik10}.json", f"subs_{cik10}", 3600)
    rec = subs.get("filings", {}).get("recent", {})
    acc = None
    filed = None
    for i in range(len(rec.get("form", []))):
        if rec["form"][i].startswith("13F-HR"):
            acc, filed = rec["accessionNumber"][i], rec["filingDate"][i]
            break
    if not acc:
        return _err(f"No 13F-HR found for {label}.")
    folder = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}"
    try:
        idx = _get(f"{folder}/index.json", headers=HEADERS_SEC).json()
    except Exception as e:
        return _err(f"Could not list 13F documents: {e}")
    info_doc = None
    for item in idx.get("directory", {}).get("item", []):
        name = item.get("name", "")
        if name.lower().endswith(".xml") and "primary_doc" not in name.lower():
            info_doc = name
    if not info_doc:
        return _err("No information-table XML found in the 13F folder.")
    xml = _get(f"{folder}/{info_doc}", headers=HEADERS_SEC).text
    rows = []
    for m in re.finditer(r"<(?:\w+:)?infoTable>(.*?)</(?:\w+:)?infoTable>", xml, re.S):
        blk = m.group(1)

        def g(tag):
            mm = re.search(rf"<(?:\w+:)?{tag}>(.*?)</(?:\w+:)?{tag}>", blk, re.S)
            return html_lib.unescape(mm.group(1).strip()) if mm else ""
        try:
            val = int(float(g("value") or 0))
        except ValueError:
            val = 0
        rows.append({"issuer": g("nameOfIssuer"), "class": g("titleOfClass"),
                     "cusip": g("cusip"), "value_usd": val,
                     "shares": g("sshPrnamt"), "put_call": g("putCall")})
    # aggregate multiple lines per issuer
    agg = {}
    for r in rows:
        k = r["issuer"]
        a = agg.setdefault(k, {"issuer": k, "value_usd": 0, "cusip": r["cusip"]})
        a["value_usd"] += r["value_usd"]
    total = sum(a["value_usd"] for a in agg.values()) or 1
    top = sorted(agg.values(), key=lambda x: -x["value_usd"])[:top_n]
    for t in top:
        t["pct_of_13f"] = round(100 * t["value_usd"] / total, 2)
    return json.dumps({
        "source": f"SEC EDGAR 13F-HR information table, accession {acc}",
        "manager": label, "filed": filed, "positions_reported": len(agg),
        "total_13f_value_usd": total, "top_holdings": top,
        "caveat": "45-day lag; US-listed longs only; values as filed.",
    })


# ----------------------------------------------------------------------------- prices & profile
@mcp.tool()
def get_company_profile(ticker: str) -> str:
    """Quick company snapshot: price, market cap, valuation ratios, sector, 52-week range.

    Works for US and international tickers (0700.HK, RMS.PA, 005930.KS...). Data from
    yfinance (unofficial) — treat ratios as screening-grade, verify before deciding.

    Args:
        ticker: Ticker symbol, exchange-suffixed for non-US listings.
    """
    if not HAS_YF:
        return _err("yfinance not installed (pip install yfinance). For US names use "
                    "get_financial_history + get_prices fallback instead.")
    try:
        t = yf.Ticker(ticker)
        inf = t.info or {}
        keep = ["longName", "exchange", "currency", "sector", "industry", "country",
                "marketCap", "currentPrice", "trailingPE", "forwardPE", "priceToBook",
                "enterpriseValue", "enterpriseToEbitda", "dividendYield", "payoutRatio",
                "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "sharesOutstanding", "bookValue",
                "returnOnEquity", "operatingMargins", "profitMargins", "totalDebt",
                "totalCash", "freeCashflow", "longBusinessSummary"]
        out = {k: inf.get(k) for k in keep if inf.get(k) is not None}
        if "longBusinessSummary" in out:
            out["longBusinessSummary"] = out["longBusinessSummary"][:800]
        if not out:
            return _err(f"yfinance returned nothing for {ticker} (delisted? wrong suffix?)")
        return json.dumps({"source": "yfinance (unofficial; screening-grade)", "ticker": ticker, **out})
    except Exception as e:
        return _err(f"yfinance failed: {e}")


@mcp.tool()
def get_prices(ticker: str, period: str = "5y", interval: str = "1mo") -> str:
    """Historical prices (close, adjusted) for charting, drawdown and multiple history.

    Uses yfinance; falls back to Stooq daily CSV (US/major markets) if unavailable.

    Args:
        ticker: Ticker (suffixed for non-US, e.g. 0700.HK).
        period: 1y, 5y, 10y, max (yfinance syntax).
        interval: 1d, 1wk, 1mo.
    """
    if HAS_YF:
        try:
            h = yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=True)
            if h is not None and not h.empty:
                closes = {str(ix.date()): round(float(v), 4) for ix, v in h["Close"].items()}
                return json.dumps({"source": "yfinance (adjusted close)", "ticker": ticker,
                                   "period": period, "interval": interval, "close": closes})
        except Exception:
            pass
    # Stooq fallback (daily only)
    sym = ticker.lower()
    if "." not in sym:
        sym += ".us"
    try:
        csv = _get(f"https://stooq.com/q/d/l/?s={sym}&i=d", timeout=30).text
        lines = csv.strip().splitlines()
        if len(lines) < 2:
            return _err(f"No price data for {ticker} from yfinance or Stooq.")
        closes = {}
        for ln in lines[1:]:
            parts = ln.split(",")
            if len(parts) >= 5:
                closes[parts[0]] = float(parts[4])
        # thin to monthly if long
        if len(closes) > 400:
            closes = {d: v for d, v in closes.items() if d[8:10] <= "07" and d[5:7] in
                      ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")}
        return json.dumps({"source": "Stooq daily CSV (fallback, unadjusted)", "ticker": ticker,
                           "close": closes})
    except Exception as e:
        return _err(f"Price fetch failed for {ticker}: {e}")


@mcp.tool()
def get_fx_rate(base: str = "USD", quotes: str = "EUR,HKD,MYR", on_date: str = "") -> str:
    """FX rates for multi-currency valuation (Frankfurter API — central-bank data, no key).

    Args:
        base: Base currency code (default USD).
        quotes: Comma-separated quote currencies (default EUR,HKD,MYR).
        on_date: Optional YYYY-MM-DD for a historical date (default latest).
    """
    d = on_date or "latest"
    url = f"https://api.frankfurter.app/{d}?from={base.upper()}&to={quotes.upper()}"
    try:
        data = _get(url, timeout=20).json()
        return json.dumps({"source": "Frankfurter (ECB & central banks)", **data})
    except Exception as e:
        return _err(f"FX fetch failed: {e}")


@mcp.tool()
def screen_by_metric(concept: str = "Revenues", unit: str = "USD", year: int = 0, quarter: str = "") -> str:
    """Cross-sectional XBRL 'frame': one us-gaap concept for ALL US filers in one period.

    Useful for building screens (e.g. every filer's revenue, equity, or net income for a
    year) that you then filter locally. Returns up to 200 largest values.

    Args:
        concept: A us-gaap tag, e.g. Revenues, NetIncomeLoss, StockholdersEquity, Assets.
        unit: Unit, normally USD.
        year: Calendar year, e.g. 2025. 0 = latest full year (current year - 1).
        quarter: Optional Q1-Q4 for a quarterly duration frame; empty for annual (CY####).
    """
    y = year or (date.today().year - 1)
    frame = f"CY{y}{quarter.upper()}" if quarter else f"CY{y}"
    url = f"https://data.sec.gov/api/xbrl/frames/us-gaap/{concept}/{unit}/{frame}.json"
    try:
        data = _sec_json(url, f"frame_{concept}_{frame}", 24 * 3600)
    except Exception as e:
        return _err(f"frames API failed for {concept} {frame}: {e}")
    rows = sorted(data.get("data", []), key=lambda r: -abs(r.get("val", 0)))[:200]
    return json.dumps({
        "source": f"SEC XBRL frames {frame}", "concept": concept,
        "count_total": len(data.get("data", [])),
        "top200": [{"entity": r.get("entityName"), "cik": r.get("cik"), "val": r.get("val")} for r in rows],
    })


if __name__ == "__main__":
    mcp.run()
