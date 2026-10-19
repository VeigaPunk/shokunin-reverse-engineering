#!/usr/bin/env python3
"""Pointer-truth assertion for SHONEN.md's queue-drain craft-section claim.

SEAT EX-04 (c1, arc3-loop1-round2). Independent of the citation-drift probe:
its `shonen-skill-range` entry grades range *content* (a needle somewhere inside
the stated span), so an end-point overshoot or a stale rule count passes it
silently (measured by E16, arc2-loop1-round10 §2.3-2.4; re-measured this round
in the insert simulation). This tool grades the pointer itself:

  A1  stated range start == the `## Queue-drain craft` heading line
  A2  stated range end lies in the craft section: last rule line <= end < the
      next `## ` heading line (the trailing blank run is tolerated; anything
      past the heading is an overshoot, anything before the last rule line
      drops the newest rule out of the stated range)
  A3  stated N/N count == the number of `- **` rule blocks in the section
  A4  the newest rule block's opening phrase lies inside the stated range

Usage: python3 craft-pointer-truth.py [ROOT] [--json]
Exit 0 = all assertions pass; 1 = at least one mismatch; 2 = unparsable.
"""
import json
import re
import sys
from pathlib import Path

CLAIM = re.compile(r"`SKILL\.md:(\d+)-(\d+)`")
COUNT = re.compile(r"(\d+)/(\d+) rule blocks")


def measure(root):
    root = Path(root)
    skill = (root / "SKILL.md").read_text(encoding="utf-8").splitlines()
    shonen = (root / "SHONEN.md").read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(skill, 1)
                 if l.startswith("## Queue-drain craft"))
    nxt = next(i for i, l in enumerate(skill, 1)
               if i > start and l.startswith("## "))
    end_true = max(i for i in range(start, nxt) if skill[i - 1].strip())
    blocks = [i for i in range(start, end_true + 1)
              if skill[i - 1].startswith("- **")]
    line6 = shonen[5]
    m = CLAIM.search(line6)
    c = COUNT.search(line6)
    if not m or not c:
        return None, line6
    stated_lo, stated_hi = int(m.group(1)), int(m.group(2))
    stated_n, stated_d = int(c.group(1)), int(c.group(2))
    newest = skill[blocks[-1] - 1][: 60]
    checks = [
        ("A1-start", stated_lo == start, "stated=%d true=%d" % (stated_lo, start)),
        ("A2-end", end_true <= stated_hi < nxt,
         "stated=%d last_rule=%d next_heading=%d" % (stated_hi, end_true, nxt)),
        ("A3-count", stated_n == stated_d == len(blocks),
         "stated=%d/%d counted=%d" % (stated_n, stated_d, len(blocks))),
        ("A4-newest-in-range",
         stated_lo <= blocks[-1] <= stated_hi,
         "newest_rule_line=%d phrase=%r" % (blocks[-1], newest[:40])),
    ]
    return checks, line6


def main(argv):
    root = ""
    as_json = "--json" in argv
    pos = [a for a in argv[1:] if not a.startswith("--")]
    if pos:
        root = pos[0]
    elif not Path("SHONEN.md").exists():
        root = "."
    checks, line6 = measure(root or ".")
    if checks is None:
        print("POINTER_TRUTH_UNPARSABLE: SHONEN.md:6 = %r" % line6)
        return 2
    failed = [n for n, ok, _ in checks if not ok]
    if as_json:
        print(json.dumps({"root": str(Path(root or ".").resolve()),
                          "shonen_line6": line6,
                          "checks": [{"id": n, "ok": ok, "detail": d}
                                     for n, ok, d in checks],
                          "verdict": "fail" if failed else "pass"},
                         sort_keys=True))
        return 1 if failed else 0
    for n, ok, d in checks:
        print("POINTER_TRUTH %-20s %-4s %s" % (n, "PASS" if ok else "FAIL", d))
    print("POINTER_TRUTH_VERDICT: %s (failed=%s)"
          % ("FAIL" if failed else "PASS", ",".join(failed) or "none"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
