#!/usr/bin/env python3
"""CritC2Axes: falsify the `axes` atom class of tools/round-47/record.py (read-only)."""
import json
import os
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
TOOLS = os.path.join(ROOT, "tools/round-47")
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.path.join(ROOT, "tools/round-46"))
import gate  # noqa: E402
import record  # noqa: E402

REV = sys.argv[1]
tip = gate.resolve(ROOT, REV)
card0 = gate.show(ROOT, tip, "SCORECARD.md")
readme0 = gate.show(ROOT, tip, "corpus/README.md")
assert card0 and readme0, "card/readme absent"
emit = lambda p: gate.show(ROOT, tip, p)

results = []


def run(name, card=None, overrides=None):
    card = card0 if card is None else card
    over = overrides or {}

    def files(p):
        return over[p] if p in over else emit(p)

    code, rec = record.evaluate_text(card, files, ROOT, tip, battery=None)
    axes = {}
    for a in rec.get("mismatches", []):
        axes[a["key"]] = a["derived"]
    results.append({
        "name": name, "exit": code, "failing": rec.get("failing"),
        "corrections": rec.get("corrections"),
        "corrections_bad": len(rec.get("corrections_bad") or []),
        "axes_mismatch": axes.get("coverage"), "axes_mismatch_depth": axes.get("depth"),
    })
    print(json.dumps(results[-1]))


# E1 — control: the card as committed must stay green.
run("E1-control-unchanged")

# E2 — forge ONLY the score cell of the coverage row (baseline and current).
assert "| coverage | 9.72 → 10.0 |" in card0
run("E2-score-cell-forged", card0.replace("| coverage | 9.72 → 10.0 |",
                                          "| coverage | 3.14 → 4.20 |", 1))

# E3 — forge ONLY the depth row's score cell.
assert "| depth | 10 → 10 |" in card0
run("E3-depth-score-forged", card0.replace("| depth | 10 → 10 |",
                                           "| depth | 0.00 → 1.00 |", 1))

# E4 — an out-of-range score (above the 0-10 scale) is still green.
run("E4-score-out-of-range", card0.replace("| coverage | 9.72 → 10.0 |",
                                           "| coverage | 42.0 → 99.9 |", 1))

# E5 — control: forging the FRACTION is caught (the atom binds only this).
run("E5-fraction-forged", card0.replace("138/138 knowledge files mapped",
                                        "137/138 knowledge files mapped", 1))

# E6 — move the fraction into the score column and falsify the observable cell:
#      the atom is the first fraction anywhere in the row, not the observable column.
row_forged = card0.replace(
    "| coverage | 9.72 → 10.0 | 138/138 knowledge files mapped",
    "| coverage | 138/138 | 0/138 knowledge files mapped", 1)
assert row_forged != card0
run("E6-fraction-in-score-column", row_forged)

# E7 — a false `axes` correction line is silently not parsed (CORR excludes axes).
bad_axes = card0 + ("\n- corrects axes coverage: 7/9\n- corrects axes depth: 1/24\n"
                    "- corrects axes calibration: 0/0\n")
run("E7-false-axes-corrections", bad_axes)

# E8 — deleting the two landed `axes` correction lines changes nothing.
stripped = "\n".join(l for l in card0.splitlines()
                    if not l.startswith("- corrects axes "))
run("E8-axes-corrections-deleted", stripped)

# E9 — forged corpus/README.md: a coverage-map token naming no knowledge file.
#      `dangling []` is asserted in the observable cell but never derived.
marker = "## Coverage map\n"
assert marker in readme0
ghost = readme0.replace(marker, marker + "\n- `2026-10-27-r47-ghost-entry` ghost entry for a file that does not exist\n", 1)
run("E9-dangling-map-token", None, {"corpus/README.md": ghost})

print(json.dumps({"derived": {"coverage": record.coverage_pair(ROOT, tip, emit),
                              "depth": record.depth_pair(emit)}}))
print(json.dumps({"card_axes_atoms": record.collect_axes(card0)}))
