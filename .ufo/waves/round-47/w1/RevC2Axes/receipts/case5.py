import json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC2Axes")
from driver import *  # noqa
green = green_card()
fx = Fixture("h-baseline"); fx.commit({"SCORECARD.md": green}, "head-bytes baseline"); record("h-baseline-green", fx, "hb", 0)
fx = Fixture("h-dropdepth"); fx.commit({"SCORECARD.md": drop_axis_row(green, "depth")}, "head-bytes depth dropped"); record("h-depth-row-deleted", fx, "hd", 0)
row = axis_row(green, "depth").group(0)
fr = row.replace("| depth | 10 → 10 |", "| depth | 10 → 10 (23/23) |", 1)
i = fr.index("| depth | 10 → 10 (23/23) |") + len("| depth | 10 → 10 (23/23) |")
fr = fr[:i] + " 20/20 queue-drain" + fr[i:]
fx = Fixture("h-falsetruth"); fx.commit({"SCORECARD.md": set_axis_row(green, "depth", fr)}, "head-bytes false headline"); record("h-false-headline", fx, "hf", 0)
README = show(FREEZE, "corpus/README.md"); A="2026-10-26-binwalk-v3-unit-of-work"; B="2026-10-27-r47-forged-new-entry"
row = "| REA CLI & self-docs | `2026-10-13-rea-cli-surface`, `%s` | forged row |\n" % B
readme = README.replace("## Coverage map\n\n", "## Coverage map\n\n" + row, 1)
fx = Fixture("h-stalemap"); fx.commit({"SCORECARD.md": green, "corpus/README.md": readme, "corpus/knowledge/%s.md"%B:"#x\n"}, "head-bytes stale map", remove=["corpus/knowledge/%s.md"%A]); record("h-coverage-stale-map", fx, "hs", 0)
json.dump(RESULTS, open(os.path.join(S,"cases5.json"),"w"), indent=1)
