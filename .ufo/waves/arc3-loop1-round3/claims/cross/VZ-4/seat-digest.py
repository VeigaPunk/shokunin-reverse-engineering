#!/usr/bin/env python3
"""VZ-4 seat-report digest — pulls the load-bearing lines out of every delivered
seat report so the wave summary quotes seats rather than paraphrasing them.
Prints, per seat: first heading, any VERDICT/STATUS/ATTACK/BLOCKER line, and the
report's sha256 + byte size.
"""
import hashlib, pathlib, re, sys

WAVE = pathlib.Path(__file__).resolve().parents[3]
seats = sorted((WAVE / 'seats').glob('*.md'))
pat = re.compile(r'(?i)(verdict|status|blocker|attack|refut|honest stop|not verified|FAIL|CLEAN|undelivered)')
for p in seats:
    b = p.read_bytes()
    text = b.decode('utf-8', 'replace')
    lines = text.splitlines()
    head = next((l for l in lines if l.strip().startswith('#')), '(no heading)')
    hits = [l.strip() for l in lines if pat.search(l)][:4]
    print(f"== {p.stem} | {len(b)}B | {hashlib.sha256(b).hexdigest()[:16]} | {head.strip()[:90]}")
    for h in hits:
        print(f"   {h[:170]}")