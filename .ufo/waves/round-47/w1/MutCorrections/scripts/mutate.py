#!/usr/bin/env python3
"""Apply one named mutation to SCORECARD.md in the fixture clone."""
import re
import sys

name, CARD = sys.argv[1], sys.argv[2]
text = open(CARD).read()

SEATS45 = "- corrects seats round-45: 2 waves, 76 seats total"
WIN46 = ("- corrects window round-46: empty in 332f4884..58eb04b6"
         " -- tools/round-46 plans/round-46-claims.md")
AXES_BLOCK = (
    "- corrects axes coverage: 138/138 — `git ls-tree -r --name-only <rev> corpus/knowledge"
    " | grep -c\n  '\\.md$'` → 138 and command A → `mapped 138`, so the row's head now"
    " reads 138/138.\n"
    "- corrects axes depth: 24/24 — command A at the round-47 landing → `rule_blocks 24`,\n"
    "  `citation_resolved_rules 24`, so the row's head now reads 24/24.\n")

SUB = {  # single-anchor substitutions: name -> (old, new)
    "wrong-round-in-window": (SEATS45, SEATS45.replace("round-45", "round-46")),
    "wrong-round-historical-true": (SEATS45,
                                    "- corrects seats round-43: 2 waves, 64 seats total"),
    "cross-round-total": (SEATS45, "- corrects seats round-45: 2 waves, 80 seats total"),
    "ghost-path-window-pathspec": (WIN46,
                                   "- corrects window round-46: empty in 332f4884..58eb04b6"
                                   " -- does/not/exist/"),
    "window-pair-out-of-scope": (WIN46,
                                 "- corrects window round-46: empty in 332f4884..332f4884"
                                 " -- tools/round-46 plans/round-46-claims.md"),
    "window-pair-real-other-commits": (
        WIN46, "- corrects window round-46: empty in 1e2c310295..07d2894eab"
               " -- tools/round-47/exact.py"),
    "window-pair-atom-range": (
        WIN46, "- corrects window round-46: empty in 0425224..58eb04b6"
               " -- tools/round-46 plans/round-46-claims.md"),
    "duplicate-correction": (SEATS45, SEATS45 + "\n" + SEATS45),
    "duplicate-replaces-repair": (WIN46, SEATS45),
    "false-axes-correction": ("- corrects axes coverage: 138/138",
                              "- corrects axes coverage: 1/2"),
    "false-axes-bogus-axis": ("- corrects axes coverage: 138/138",
                              "- corrects axes bogus: 1/2"),
    "axes-corrections-deleted": (AXES_BLOCK, ""),
}

if name in ("ghost-path-exemption", "ghost-path-non-atom"):
    anchor = AXES_BLOCK
    if text.count(anchor) != 1:
        sys.exit("anchor not unique")
    ghost = ("corpus/does/not/exist.md" if name == "ghost-path-exemption"
             else "corpus/README.md")
    out = text.replace(anchor, anchor + "- corrects path %s: landed\n" % ghost, 1)
elif name in SUB:
    old, new = SUB[name]
    if text.count(old) != 1:
        sys.exit("anchor not unique/found: %r count=%d" % (old[:60], text.count(old)))
    out = text.replace(old, new, 1)
else:
    sys.exit("unknown mutation " + name)

if out == text:
    sys.exit("no-op mutation")
open(CARD, "w").write(out)
