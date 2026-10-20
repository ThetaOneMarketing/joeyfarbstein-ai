#!/usr/bin/env python3
"""
build_opportunities.py — turn the interview's profile.json into the opportunities page.

Usage:
  python3 build_opportunities.py --out ai-standing-out
      reads  ai-standing-out/profile.json (and findings.json / interview.md if they're there)
      writes ai-standing-out/opportunities.html
  python3 build_opportunities.py --profile some/profile.json --write page.html

Checks the data before it writes anything: every opportunity needs a name, a one-line description,
hours back a week, an effort level, and a confidence level. No prices allowed; the page shows a
price placeholder that Joey fills in on the call.
"""
import argparse, json, re, sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "opportunities.html"
EFFORTS = {"tonight", "afternoon", "hookup"}
CONF = {"high", "medium", "low"}
PRICE_RE = re.compile(r"\$\s?\d|\b\d+\s?(dollars|bucks)\b|/mo\b|per month", re.I)


def check(p):
    errs = []
    ops = p.get("opportunities")
    if not isinstance(ops, list) or not ops:
        return ["profile.json has no opportunities list"]
    if not 3 <= len(ops) <= 8:
        errs.append(f"aim for 3 to 8 opportunities (found {len(ops)})")
    for i, o in enumerate(ops, 1):
        tag = f"opportunity {i} ({o.get('name', '?')})"
        for k in ("name", "description", "why"):
            if not str(o.get(k, "")).strip():
                errs.append(f"{tag}: missing {k}")
        try:
            lo = float(o.get("hours_low")); hi = float(o.get("hours_high", lo))
            if lo < 0 or hi < lo or hi > 40:
                errs.append(f"{tag}: hours_low/hours_high look wrong ({lo}, {hi})")
        except (TypeError, ValueError):
            errs.append(f"{tag}: hours_low must be a number")
        if o.get("effort") not in EFFORTS:
            errs.append(f"{tag}: effort must be one of {sorted(EFFORTS)}")
        if str(o.get("confidence", "")).lower() not in CONF:
            errs.append(f"{tag}: confidence must be high, medium, or low")
        if "price" in o and o["price"] not in (None, ""):
            errs.append(f"{tag}: remove the price. Joey sets prices on the call.")
        for k, v in o.items():
            if isinstance(v, str) and PRICE_RE.search(v):
                errs.append(f"{tag}: {k} mentions money ({v[:60]!r}). No prices or dollar figures on this page.")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="ai-standing-out", help="folder with profile.json; the page is written here")
    ap.add_argument("--profile", help="path to profile.json (default: <out>/profile.json)")
    ap.add_argument("--write", help="where to write the page (default: <out>/opportunities.html)")
    a = ap.parse_args()
    out = Path(a.out)
    prof_path = Path(a.profile) if a.profile else out / "profile.json"
    if not prof_path.exists():
        sys.exit(f"No profile.json at {prof_path}. The interview writes it first.")
    p = json.loads(prof_path.read_text())

    # pull the audit link and notes in if they're next to the profile
    findings = prof_path.parent / "findings.json"
    if findings.exists() and not p.get("bundle_id"):
        f = json.loads(findings.read_text())
        m = re.search(r"/audits/([a-z0-9]{12})/?$", f.get("bundle_url") or "")
        if m: p["bundle_id"] = m.group(1)
        p.setdefault("from_audit", True)
    notes = prof_path.parent / "interview.md"
    if notes.exists() and not p.get("interview_md"):
        p["interview_md"] = notes.read_text()[:60000]

    errs = check(p)
    if errs:
        print("Fix these in profile.json, then run this again:")
        for e in errs: print("  - " + e)
        sys.exit(1)

    # rank: most hours back first, then the easiest
    order = {"tonight": 0, "afternoon": 1, "hookup": 2}
    p["opportunities"].sort(key=lambda o: (-(float(o["hours_low"]) + float(o.get("hours_high", o["hours_low"]))) / 2,
                                           order[o["effort"]]))
    for i, o in enumerate(p["opportunities"], 1):
        o["rank"] = i

    blob = json.dumps(p, indent=2, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\u0021--")
    html = TEMPLATE.read_text().replace("{{OPPORTUNITIES_JSON}}", blob, 1)
    dest = Path(a.write) if a.write else out / "opportunities.html"
    dest.write_text(html)
    lo = sum(float(o["hours_low"]) for o in p["opportunities"])
    hi = sum(float(o.get("hours_high", o["hours_low"])) for o in p["opportunities"])
    print(f"Wrote {dest}: {len(p['opportunities'])} opportunities, about {lo:g} to {hi:g} hours a week.")


if __name__ == "__main__":
    main()
