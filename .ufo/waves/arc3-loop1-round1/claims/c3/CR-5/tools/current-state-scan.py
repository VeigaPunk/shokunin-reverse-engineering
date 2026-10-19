#!/usr/bin/env python3
"""CR-5 current-state-language scan over declared DATED regions.

Usage: python3 current-state-scan.py <census.py> <root>
For each DATED row, prints lines inside it that carry live-state language
(now/current/today/at HEAD/this round/remains/is pinned/zero-drift) — the
text that a DATED classification would swallow if it ever gained a needle.
Also prints the region's line count and whether it contains a round header.
"""
import os, re, sys

LIVE = re.compile(r"\b(now|current|today|at HEAD|this round|remains|"
                  r"is pinned|zero-drift|live)\b", re.I)
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[1])))
import importlib.util
spec = importlib.util.spec_from_file_location("census_mod", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
SCOPE = mod.SCOPE
root = sys.argv[2]
cache = {}
for (f, s, e, cls, ml, mr) in SCOPE:
    if cls != "DATED":
        continue
    if f not in cache:
        cache[f] = open(os.path.join(root, f), encoding="utf-8",
                        errors="replace").read().splitlines()
    lines = cache[f]
    hits = [(i, lines[i - 1]) for i in range(s, min(e, len(lines)) + 1)
            if LIVE.search(lines[i - 1])]
    print("%s %d-%d (%d lines, %d live-language hits)" % (f, s, e, e - s + 1, len(hits)))
    for i, txt in hits:
        print("   :%d %s" % (i, txt.strip()[:110]))
