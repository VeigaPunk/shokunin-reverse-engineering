import json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC2Axes")
from driver import *  # noqa
green = green_card()
fx = Fixture("drop-coverage")
c = drop_axis_row(green, "coverage")
fx.commit({"SCORECARD.md": c}, "r47 axes: coverage row deleted")
record("coverage-row-deleted", fx, "dropcov", 0)
json.dump(RESULTS, open(os.path.join(S, "cases4.json"), "w"), indent=1)
