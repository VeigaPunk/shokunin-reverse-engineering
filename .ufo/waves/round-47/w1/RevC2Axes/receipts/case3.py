import json, os, re, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC2Axes")
from driver import *  # noqa

green = green_card()
skill = show(FREEZE, "SKILL.md")
head, tail = skill.split("## Queue-drain craft ", 1)
craft, rest = tail.split("\n## ", 1)
rules = list(re.finditer(r"(?m)^- \*\*", craft))
assert len(rules) == 23, len(rules)

# 10 shrink the depth denominator: drop the last craft block and claim 22/22
last = rules[-1].start()
craft22 = craft[:last].rstrip("\n") + "\n\n"
skill22 = head + "## Queue-drain craft " + craft22 + "\n## " + rest
fx = Fixture("shrink-depth")
card = set_frac(green, "depth", "22/22")
fx.commit({"SCORECARD.md": card, "SKILL.md": skill22},
          "r47 axes: drop the last craft block, claim 22/22")
ra = fx.recipe_a()
record("depth-denominator-shrunk", fx, "shrink", 0,
       extra={"recipe_a": {k: ra.get(k) for k in ("rule_blocks", "citation_resolved_rules")}})

# 10b the same card with the row still saying 23/23 (the honest denominator)
fx = Fixture("shrink-honest")
fx.commit({"SCORECARD.md": green, "SKILL.md": skill22},
          "r47 axes: block dropped, row keeps 23/23")
record("depth-block-dropped-row-keeps-23", fx, "shrinkhonest", 1)

# 11 coverage denominator shrunk with the map: delete a knowledge file and its token
readme = show(FREEZE, "corpus/README.md")
A = "2026-10-26-binwalk-v3-unit-of-work"
assert A in readme
readme2 = readme.replace("`%s`" % A, "`removed-entry`", 1)
assert readme2 != readme
fx = Fixture("shrink-coverage")
card = set_frac(green, "coverage", "137/137")
fx.commit({"SCORECARD.md": card, "corpus/README.md": readme2},
          "r47 axes: delete a knowledge file and its map token, claim 137/137",
          remove=["corpus/knowledge/%s.md" % A])
ra = fx.recipe_a()
record("coverage-denominator-shrunk", fx, "shrinkcov", 0,
       extra={"recipe_a": {k: ra.get(k) for k in ("mapped", "knowledge_files", "missing", "dangling")}})
json.dump(RESULTS, open(os.path.join(S, "cases3.json"), "w"), indent=1)
