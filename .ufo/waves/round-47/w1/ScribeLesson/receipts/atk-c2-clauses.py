#!/usr/bin/env python3
"""R47-C2 attacks, in-process against the frozen record.py evaluate_text()/derive().

F1  an `axes` correction line is not parsed at all: `CORR`'s alternation is
    (seats|window|path|rev), so claims clause 3's "an axes correction must state
    <resolved>/<total>" is unreachable and the `axes` branch of corrects() is dead code.
F2  a `window` correction is rejected unless its stated pair equals an EXISTING atom's
    pair; the round-46 window atom is a placeholder (pair None), so the append-only
    repair route can never exempt it.
F3  feasibility: the only route to mismatches == [] is to rewrite the round-46 sentence in
    place and edit the axes rows (no correction line can do either).
F4  the seats class derives from dispatch SPECS: a wave spec the round itself calls
    "left undispatched" counts as seats, so R46-V1's falsified claim verifies.
F5  a false base revision written in uppercase is never collected (REV_TOKEN is [0-9a-f]).
"""
import json
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "3186f69b49798f2cc05727bbfd1604505fcee03b"
sys.path.insert(0, os.path.join(LANE, "tools/round-47"))
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
import record  # noqa: E402
import gate  # noqa: E402

CARD = gate.show(LANE, REV, "SCORECARD.md")
files = lambda p: gate.show(LANE, REV, p)  # noqa: E731
out = {}


def ev(card, name):
    code, rec = record.evaluate_text(card, files, LANE, REV, battery=None)
    return {"case": name, "exit": code,
            "failing": rec.get("failing"),
            "mismatches": [(m["class"], m["key"]) for m in rec.get("mismatches", [])],
            "corrections": rec.get("corrections"),
            "corrections_bad": [c["detail"] for c in rec.get("corrections_bad", [])],
            "exempted": [e["class"] for e in rec.get("exempted", [])]}


out["base"] = ev(CARD, "base-at-rev")

# F1: axes correction line — parsed?
axes_card = CARD + ("\n## Record corrections — round 47\n\n"
                    "- corrects axes coverage: 138/138\n"
                    "- corrects axes depth: 23/23\n")
out["F1_corrections_parsed"] = record.corrections(axes_card)
out["F1"] = ev(axes_card, "axes-corrections-only")

# F2: a truthful empty window stated as a correction, with the placeholder atom in scope
win_card = CARD + ("\n## Record corrections — round 47\n\n"
                   "- corrects seats round-45: 2 waves, 76 seats total\n"
                   "- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46\n")
out["F2"] = ev(win_card, "window-correction-vs-placeholder")

# F3: rename the placeholder window in place + fix the two axes rows, keep two corrections
fixed = CARD.replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md",
                     "332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md")
fixed = re.sub(r"(?m)^(\| coverage \|[^|]*\|[^|]*\| )133/133", r"\g<1>138/138", fixed)
fixed = re.sub(r"(?m)^(\| depth \|[^|]*\|[^|]*\| )20/20", r"\g<1>23/23", fixed)
out["F3_edits_applied"] = {
    "window_pair_rewritten": "332f4884..58eb04b6 -- tools/round-46" in fixed,
    "coverage_row": re.search(r"(?m)^\| coverage \|.{0,80}", fixed).group(0)[:60],
    "depth_row": re.search(r"(?m)^\| depth \|.{0,80}", fixed).group(0)[:60]}
out["F3_inplace_only"] = ev(fixed, "in-place-fix-no-corrections")
out["F3_reachable"] = ev(fixed + ("\n## Record corrections — round 47\n\n"
                                  "- corrects seats round-45: 2 waves, 76 seats total\n"
                                  "- corrects window round-46: empty in 332f4884..58eb04b6 "
                                  "-- tools/round-46\n"), "in-place-fix-plus-corrections")

# F4: the round-46 seat atom, derived by the counter's own derive()
sec46 = dict(record.sections(CARD))["46"]
atoms = [a for a in record.collect(sec46, "46", files, LANE, REV) if a["class"] == "seats"]
cache = {"46": record.dispatch_counts(files, "46"), "45": record.dispatch_counts(files, "45")}
out["F4"] = {
    "atoms": [a["atom"] for a in atoms],
    "derive": [record.derive(a, files, LANE, REV, lambda r: cache[str(r)]) for a in atoms],
    "round46_w2_files_at_rev": gate.git(LANE, "ls-tree", "-r", "--name-only", REV,
                                        "--", ".ufo/waves/round-46/w2/").stdout.split(),
    "round46_results_json_at_rev": len([l for l in gate.git(
        LANE, "ls-tree", "-r", "--name-only", REV, "--", ".ufo/waves/round-46").stdout.splitlines()
        if l.endswith("results.json")]),
    "dispatch_commit": gate.git(LANE, "log", "--format=%h %s", "--diff-filter=A", "--",
                                ".ufo/waves/round-46/w2-dispatch.json").stdout.strip(),
}
out["F4_battery_on_f3_card"] = record.run_battery(
    fixed + ("\n## Record corrections — round 47\n\n"
             "- corrects seats round-45: 2 waves, 76 seats total\n"
             "- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46\n"),
    files, LANE, REV)

# F5: a wrong base revision in uppercase is never collected
upper = CARD.replace("Base `149133d47aa7e90796f96047afe6d251a3e65b2c`",
                     "Base `ABC1234`").replace("Base `5382acc85f9d8617fe242fc116819b8055dfc4c7`",
                                               "Base `DEF5678`")
out["F5_collected_uppercase"] = [a["atom"] for a in record.collect(
    dict(record.sections(upper))["46"], "46", files, LANE, REV) if "ABC1234" in a["atom"]
    or "DEF5678" in a["atom"]]
out["F5"] = ev(upper, "uppercase-false-base")

print(json.dumps(out, indent=1))
