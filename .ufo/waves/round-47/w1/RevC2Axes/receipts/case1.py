import json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC2Axes")
from driver import *  # noqa

green = green_card()

# 0 baseline: does the repaired card actually go green?
fx = Fixture("baseline")
fx.commit({"SCORECARD.md": green}, "r47 axes: baseline green card")
record("baseline-green", fx, "green", 0)

# 1 the depth row deleted outright: does the counter still go green?
fx = Fixture("drop-depth")
c = drop_axis_row(green, "depth")
assert not re.search(r"(?m)^\|\s*depth\s*\|", c.split("## Owned axes",1)[1].split("\n## ",1)[0])
fx.commit({"SCORECARD.md": c}, "r47 axes: depth row deleted")
record("depth-row-deleted", fx, "dropdepth", 0)

# 2 the depth row renamed so the axis cell no longer matches exactly
fx = Fixture("rename-depth")
c = set_axis_row(green, "depth", axis_row(green, "depth").group(0).replace(
    "| depth |", "| depth (craft) |", 1))
fx.commit({"SCORECARD.md": c}, "r47 axes: depth row renamed")
record("depth-row-renamed", fx, "renamedepth", 0)

# 3 the depth row reflowed so its fraction lands on a continuation line
fx = Fixture("reflow-depth")
row = axis_row(green, "depth").group(0)
head, tail = row.split("|", 3)[2], None
c = green.replace(row, "| depth | 10 → 10 |\n" + row.split("|", 2)[2].lstrip(), 1)
fx.commit({"SCORECARD.md": c}, "r47 axes: depth row reflowed")
record("depth-row-reflowed", fx, "reflow", 0)

# 4 the false claim survives when a truthful fraction precedes it in the same row
fx = Fixture("preceded-truth")
row = axis_row(green, "depth").group(0)
m = re.search(r"\| depth \| 10 → 10 \|", row)
assert m
false_row = row.replace("| depth | 10 → 10 |", "| depth | 10 → 10 (23/23) |", 1)
false_row = re.sub(r"\b23/23\b", "20/20", false_row, count=1) if False else false_row
# make the observable cell claim a stale 20/20 while the parenthetical carries 23/23
false_row = false_row.replace("| depth | 10 → 10 (23/23) |", "| depth | 10 → 10 (23/23) |", 1)
idx = false_row.index("| depth | 10 → 10 (23/23) |") + len("| depth | 10 → 10 (23/23) |")
false_row = false_row[:idx] + " 20/20 queue-drain" + false_row[idx:]
c = set_axis_row(green, "depth", false_row)
fx.commit({"SCORECARD.md": c}, "r47 axes: truthful fraction ahead of a false headline")
record("false-headline-after-truthful-fraction", fx, "prectruth", 0)

# 5 the honest reflow-style card that states history in the score cell
fx = Fixture("honest-history")
row = axis_row(green, "coverage").group(0)
honest = row.replace("| coverage | 9.72 → 10.0 |",
                     "| coverage | 9.72 → 10.0 (133/133 → 138/138) |", 1)
assert honest != row
c = set_axis_row(green, "coverage", honest)
fx.commit({"SCORECARD.md": c}, "r47 axes: history stated in the score cell")
record("honest-history-in-score-cell", fx, "honesthist", 1)

json.dump(RESULTS, open(os.path.join(S, "cases1.json"), "w"), indent=1)
