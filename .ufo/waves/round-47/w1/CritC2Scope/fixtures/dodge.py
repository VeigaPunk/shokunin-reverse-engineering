#!/usr/bin/env python3
"""CritC2Scope: does the `sections == 2` boundary let a round dodge a false atom?"""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import record  # noqa: E402

REV = sys.argv[1] if len(sys.argv) > 1 else "2e4ae434"


def files(path):
    r = subprocess.run(["git", "-C", LANE, "show", f"{REV}:{path}"],
                       capture_output=True, text=True)
    return None if r.returncode != 0 else r.stdout


CARD = files("SCORECARD.md")
out = {}

secs = record.sections(CARD)
r45 = dict((r, t) for r, t in secs)["45"]
r46 = dict((r, t) for r, t in secs)["46"]
out["sections_at_rev"] = [r for r, _ in secs]


def run(name, card, battery=False):
    code, rec = record.evaluate_text(card, files, LANE, REV,
                                     battery=record.run_battery(card, files, LANE, REV)
                                     if battery else None)
    out[name] = {"exit": code,
                 "sections": rec.get("sections"),
                 "atoms": rec.get("atoms"),
                 "mismatches": [m["atom"][:90] for m in rec.get("mismatches", [])],
                 "exempted": [e["atom"][:90] for e in rec.get("exempted", [])],
                 "failing": rec.get("failing") or rec.get("reason"),
                 "corrections": rec.get("corrections")}
    return code, rec


run("E0_base", CARD)

# E1: corrupt one in-scope rev atom in the round-46 section (to a non-resolving hex).
bad46 = r46.replace("`5382acc8", "`deadbee1", 1)
assert bad46 != r46
card1 = CARD.replace(r46, bad46)
run("E1_corrupt_round46_rev", card1)

# E2: same corruption, then append two truthful duplicate headings using the
# existing round numbers 45 and 46. `sections()` takes the last two matches by
# position, so the originals fall out of scope; no clause requires the two
# in-scope headings to be distinct rounds or the newest rounds.
card2 = card1 + "\n" + r45 + "\n" + r46 + "\n"
run("E2_corrupt46_plus_duplicate_headings", card2)

# E3: corrupt a round-45 rev atom instead (in scope, currently exempted? no: pick one
# that is not the corrected seat atom), then append the same two duplicates.
bad45 = r45.replace("`149133d4", "`deadbee2", 1)
assert bad45 != r45
card3 = CARD.replace(r45, bad45)
run("E3_corrupt_round45_rev", card3)
card4 = card3 + "\n" + r45 + "\n" + r46 + "\n"
run("E4_corrupt45_plus_duplicate_headings", card4)

# E5: the round's own landing: a single `## Round 47` heading (no atoms yet) is
# enough for round-45 to leave the window. Rows: sections become [46, 47].
card5 = CARD + "\n## Round 47 — landing\n\nno atoms yet\n"
run("E5_single_new_round_heading", card5)

# E6: corrupt round-45, plus a single truthful `## Round 47` section that supplies
# the four section-borne classes from real dispatch files (round-45's own), so the
# class-coverage clause is met while round-45's original section is out of scope.
minimal = (
    "\n## Round 47 — landing\n\n"
    "Waves: 40 + 36 = 76 seats\n\n"
    "`git log 2e4ae434..2e4ae434 -- tools/round-47/` is empty\n\n"
    ".ufo/waves/round-45/w1-dispatch.json\n\n"
    "measured at `2e4ae434`\n"
)
card6 = card3 + minimal
run("E6_corrupt45_plus_one_new_section", card6)

# E7: empty-frame dodge: replace every `## Round N` heading body with one line, keep
# two headings, see what stops it.
card7 = CARD + "\n## Round 48 — empty\n\nnothing\n" + "\n## Round 49 — empty\n\nnothing\n"
run("E7_two_empty_new_sections", card7)

# E8: duplicate heading with no body at all - does a *bare* duplicate heading that
# repeats an existing heading push the original out while contributing zero atoms?
card8 = CARD + "\n## Round 46 — duplicate heading\n\nnothing\n"
run("E8_bare_duplicate_46", card8)

print(json.dumps(out, indent=1))
