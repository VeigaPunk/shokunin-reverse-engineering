import json, os, re, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC2Axes")
from driver import *  # noqa

green = green_card()
README = show(FREEZE, "corpus/README.md")
A = "2026-10-26-binwalk-v3-unit-of-work"          # existing knowledge stem (deleted)
B = "2026-10-27-r47-forged-new-entry"             # new stem (added, map row added)
assert "corpus/knowledge/" + A + ".md" in show(FREEZE, "corpus/knowledge/" + A + ".md") or True

# 6 stale coverage map: same file count, a dangling entry, and the row still green
fx = Fixture("stale-map")
readme = README.replace("| section | entries | state |",
                        "| section | entries | state |", 1)
row = "| REA CLI & self-docs | `2026-10-13-rea-cli-surface`, `%s` | forged row |\n" % B
readme = readme.replace("## Coverage map\n\n", "## Coverage map\n\n" + row, 1)
assert readme != README
card = green  # coverage row already says 138/138
fx.commit({"SCORECARD.md": card,
           "corpus/README.md": readme,
           "corpus/knowledge/" + B + ".md": "# forged entry\n"},
          "r47 axes: rename one knowledge file, map still lists the old stem",
          remove=["corpus/knowledge/" + A + ".md"])
ra = fx.recipe_a()
record("coverage-stale-map-same-file-count", fx, "stalemap", 0,
       extra={"recipe_a": {k: ra.get(k) for k in ("mapped", "knowledge_files",
                                                  "missing", "dangling")}})

# 6b control: a knowledge file with no map token at all must red the fraction
fx = Fixture("unmapped")
fx.commit({"SCORECARD.md": green,
           "corpus/knowledge/" + B + ".md": "# unmapped entry\n"},
          "r47 axes: add a knowledge file with no map token")
record("coverage-unmapped-file-control", fx, "unmapped", 1)

# 7 an `axes` correction cannot be written: the grammar drops the class
fx = Fixture("axes-correction")
stale = card_at()
stale = set_frac(stale, "depth", "23/23")            # depth repaired in place
stale += corrections(
    "- corrects seats round-45: 2 waves, 76 seats total",
    "- corrects window 46: empty in %s..%s -- corpus/lessons/round-46.md" % (BASE, FREEZE),
    "- corrects axes coverage: 138/138",
)
fx.commit({"SCORECARD.md": stale}, "r47 axes: an axes correction line in the grammar")
record("axes-correction-unparseable", fx, "axescorr", 1)

# 8 a zero-length window correction exempts the unverifiable window atom
fx = Fixture("zero-window")
c = green.replace("empty in %s..%s -- corpus/lessons/round-46.md" % (BASE, FREEZE),
                  "empty in %s..%s -- SKILL.md" % (FREEZE, FREEZE), 1)
assert c != green
fx.commit({"SCORECARD.md": c}, "r47 axes: zero-length window correction")
record("zero-length-window-correction", fx, "zerowin", 0)

# 8b a window correction naming a path that never existed
fx = Fixture("ghost-path-window")
c = green.replace("empty in %s..%s -- corpus/lessons/round-46.md" % (BASE, FREEZE),
                  "empty in %s..%s -- .ufo/waves/round-999/" % (BASE, FREEZE), 1)
fx.commit({"SCORECARD.md": c}, "r47 axes: window correction over a path that never existed")
record("window-correction-ghost-path", fx, "ghostwin", 0)

# 9 record.py's depth derivation is not command A's: a block citing no knowledge entry
BLOCK24 = (
    "- **24. A block that cites only a lesson and a tool.** <!-- exactness-table v3 -->"
    "\n\nCites `corpus/lessons/round-46.md:27-31` and `tools/round-47/exact.py`. No"
    " `corpus/knowledge/` entry.\n\n")
fx = Fixture("depth-divergence")
skill = show(FREEZE, "SKILL.md")
head, tail = skill.split("## Queue-drain craft ", 1)
craft, rest = tail.split("\n## ", 1)
skill2 = head + "## Queue-drain craft " + craft.rstrip("\n") + "\n\n" + BLOCK24 + "\n## " + rest
card24 = green
card24 = set_frac(card24, "depth", "24/24")
fx.commit({"SCORECARD.md": card24, "SKILL.md": skill2},
          "r47 axes: a 24th craft block citing no knowledge entry")
ra = fx.recipe_a()
record("depth-derivation-diverges-from-command-A", fx, "depthdiv", 0,
       extra={"recipe_a": {k: ra.get(k) for k in ("citation_resolved_rules",
                                                  "rule_blocks", "depth_score")}})

# 9b control: the same card with the row telling command A's number
fx = Fixture("depth-command-a")
card23 = set_frac(green, "depth", "23/24")
fx.commit({"SCORECARD.md": card23, "SKILL.md": skill2},
          "r47 axes: 24th block, row states command A's 23/24")
ra = fx.recipe_a()
record("depth-row-states-command-A-number", fx, "depthca", 1,
       extra={"recipe_a": {k: ra.get(k) for k in ("citation_resolved_rules",
                                                  "rule_blocks", "depth_score")}})

json.dump(RESULTS, open(os.path.join(S, "cases2.json"), "w"), indent=1)
