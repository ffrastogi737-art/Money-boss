#!/usr/bin/env python3
"""Deterministic watchdog. Reads SURVIVAL_LEDGER.md + docs/assets/config.js, smoke-tests URLs, writes ONLY STATUS.txt."""
import re, sys, datetime as dt, urllib.request

LEDGER, CONFIG, OUT = "SURVIVAL_LEDGER.md", "docs/assets/config.js", "STATUS.txt"
now = dt.datetime.now(dt.timezone.utc)


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""


def iso(key, text):
    m = re.search(rf"^{key}:\s*(\S+)", text, re.M)
    try:
        return dt.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except Exception:
        return None


def money(key, text):
    m = re.search(rf"^{key}:\s*\$([\d,]+(?:\.\d+)?)", text, re.M)
    return float(m.group(1).replace(",", "")) if m else None


def smoke(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "money-boss-audit"}), timeout=15) as r:
            return r.status
    except Exception as e:
        return getattr(e, "code", None) or type(e).__name__


def main():
    L, C = read(LEDGER), read(CONFIG)
    lines = [f"STATUS generated {now:%Y-%m-%dT%H:%M:%SZ}"]
    start, r14, r30 = iso("START_DATE", L), iso("14_DAY_REVIEW_DATE", L), iso("30_DAY_SCALE_DATE", L)
    lines.append(f"Day {(now - start).days if start else '?'} since start" + ("" if start else " (START_DATE unparsable)"))
    for name, d in (("72h", start and start + dt.timedelta(hours=72)), ("14d", r14), ("30d", r30)):
        lines.append(f"Checkpoint {name}: " + ("unknown" if not d else ("DUE" if now >= d else f"in {(d - now).days}d")))
    gross, net, pay = (money(k, L) for k in ("TOTAL_GROSS_REVENUE", "TOTAL_NET_REVENUE", "TOTAL_VERIFIED_PAYOUT"))
    lines.append(f"Ledger (self-reported, owner-verify): gross={gross} net={net} verified_payout={pay}")

    wired = bool(re.search(r'goatcounter:\s*"[^"]+"', C))
    protected = bool(re.search(r"VERIFIED_SALE|PAYOUT_PENDING", re.sub(r"PROSPECTS -> .*", "", L)))
    lines.append("Analytics: " + ("WIRED (visit counts live in GoatCounter dashboard; audit cannot read them -> sample unverified)" if wired else "TRACTION_UNKNOWN (config.js goatcounter empty)"))
    if protected:
        lines.append("Protected: sale/payout state present -> NO archiving allowed")

    for url, note in re.findall(r"^- URL:\s*(\S+)\s*\|\s*(.*)$", L, re.M):
        code = smoke(url)
        lines.append(f"URL {url} -> {code} " + ("[VERIFIED live]" if code == 200 else "[NOT LIVE: Pages disabled/building?]"))

    if not wired:
        verdict = "TRACTION_UNKNOWN"
    elif (net or 0) > 0:
        verdict = "VERIFIED_SALE_CHECK_OWNER"
    else:
        verdict = "INSUFFICIENT_SAMPLE"
    if start and r14 and now >= r14 and wired and not protected and (net or 0) == 0:
        verdict = "REVIEW_REQUIRED (14d passed, no sale; confirm traffic >=100 in GoatCounter before archiving)"
    lines.append(f"VERDICT: {verdict}")
    return lines


if __name__ == "__main__":
    try:
        out = main()
    except Exception as e:  # never crash the workflow
        out = [f"STATUS generated {now:%Y-%m-%dT%H:%M:%SZ}", f"AUDIT_ERROR: {type(e).__name__}: {e}"]
    open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))
    sys.exit(0)
