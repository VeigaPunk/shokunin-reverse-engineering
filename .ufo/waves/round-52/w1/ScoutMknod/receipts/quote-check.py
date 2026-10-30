#!/usr/bin/env python3
"""Re-check the seat's located quotes against the fetched man-page bodies.

Usage:  python3 quote-check.py [bodies-dir]   (default: ./bodies relative to this file)
Exit 0 = every quote is present verbatim; exit 1 = at least one quote is not.
The quote table itself is quote-check.json.
"""
import json, html, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
bodies = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "bodies")
PAGES = {"mknod": "mknod.2.html", "caps": "capabilities.7.html"}

def detag(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    t = re.sub(r"(?s)<(script|style).*?</\1>", "", t)
    t = re.sub(r"(?s)<[^>]+>", "", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()

table = json.load(open(os.path.join(here, "quote-check.json")))
bad = 0
for key, fname in PAGES.items():
    text = detag(os.path.join(bodies, fname))
    for q in table[key]:
        ok = re.sub(r"\s+", " ", q["quote"]).strip() in text
        if not ok:
            bad += 1
        print(f"{key:6s} {q['id']:4s} words={q['words']:2d} verbatim={ok}  [{q['location']}]")
print(f"quotes={sum(len(v) for v in table.values())} missing={bad}")
sys.exit(1 if bad else 0)
