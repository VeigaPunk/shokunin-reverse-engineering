#!/usr/bin/env python3
"""Pre-seen overlap check for a frozen test set (QUALITY row 44, mistake M28-4).

Usage: python3 -I -B tools/round-28/preseen-overlap.py --root <LANE>

Counts how many R28-C2 test selectors (corpus/evidence/round-28/c2/selectors.tsv) already had an
openchain response in the lane before the R28-C2 freeze (86fa8526, 2026-10-22T17:21:55Z): the
round-25 openchain responses, and R28-C1 openchain lookups whose manifest utc is earlier than the
freeze. Exit 0 when the overlap is 0, 1 otherwise.
"""
import argparse
import glob
import json
import os
import sys

FREEZE_UTC = "2026-10-22T17:21:55Z"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    os.chdir(a.root)
    man = json.load(open("corpus/evidence/round-28/c1/db/manifest.json"))
    pre_c1 = {e["file"][len("openchain-"):-len(".json")] for e in man
              if e["file"].startswith("openchain-") and e["utc"] < FREEZE_UTC}
    r25 = {os.path.basename(p)[len("openchain-"):-len(".json")].replace("0x", "")
           for p in glob.glob("corpus/evidence/round-25/**/openchain-*.json", recursive=True)}
    sels = [l.split("\t")[0] for l in open("corpus/evidence/round-28/c2/selectors.tsv").read().splitlines()[1:]]
    seen = [s for s in sels if s in pre_c1 or s in r25]
    print("test_selectors=%d seen_before_freeze=%d (round-25 responses %d, R28-C1 lookups before %s %d)"
          % (len(sels), len(seen), len([s for s in sels if s in r25]), FREEZE_UTC,
             len([s for s in sels if s in pre_c1])))
    return 1 if seen else 0


if __name__ == "__main__":
    sys.exit(main())
