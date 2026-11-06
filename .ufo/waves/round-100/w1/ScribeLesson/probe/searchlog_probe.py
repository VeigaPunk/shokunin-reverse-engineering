#!/usr/bin/env python3
"""D10-shaped probe for a round-N search-log note (the round-74 atom shape).
usage: searchlog_probe.py <SOURCES.md> <round label e.g. 'round 99'>
exit 0 = the note is present; 1 = absent; 2 = input missing."""
import sys, os
path, rnd = sys.argv[1], sys.argv[2]
if not os.path.exists(path):
    print("no such file: %s" % path, file=sys.stderr); raise SystemExit(2)
text = open(path, encoding="utf-8").read()
body = text.split("## Search log", 1)[1] if "## Search log" in text else ""
has = (rnd in body) and ("Identified" in body)
print(("present" if has else "absent") + ": %s note in %s" % (rnd, path))
raise SystemExit(0 if has else 1)
