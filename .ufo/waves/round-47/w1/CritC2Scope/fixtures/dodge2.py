#!/usr/bin/env python3
"""CritC2Scope probe 3: cheapest dodge (one bare heading), landing-shaped card, receipt identity."""
import hashlib
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
secs = dict((r, t) for r, t in record.sections(CARD))
r45, r46 = secs["45"], secs["46"]


def snap(rec):
    keep = {k: rec.get(k) for k in ("sections", "atoms", "atoms_by_class", "mismatches",
                                    "exempted", "corrections", "sections_bad")}
    return keep


def run(name, card, battery=False):
    code, rec = record.evaluate_text(card, files, LANE, REV,
                                     battery=record.run_battery(card, files, LANE, REV)
                                     if battery else None)
    s = snap(rec)
    s["exit"] = code
    s["failing"] = rec.get("failing") or rec.get("reason")
    s["receipt_sha256"] = hashlib.sha256(json.dumps(s, sort_keys=True).encode()).hexdigest()[:16]
    out[name] = s
    return code, rec


# E0 baseline
run("E0_base", CARD)

# E8': the cheapest dodge — ONE appended heading line with an empty body, no new
# round number, no atoms, plus one corrupted round-45 rev atom.
bad45 = r45.replace("`149133d4", "`deadbee2", 1)
assert bad45 != r45
card_bad45 = CARD.replace(r45, bad45)
run("E8a_corrupt45_only", card_bad45)
card_e8 = card_bad45 + "\n## Round 46 — duplicate heading\n"
run("E8b_corrupt45_plus_one_bare_heading", card_e8)

# sanity: the same bare heading on a clean card
run("E8c_clean_plus_one_bare_heading", CARD + "\n## Round 46 — duplicate heading\n")

# E9: landing-shaped card — append the round's own `## Round 47` section carrying the
# true dispatch count (75 seats in one wave), then the SAME corrections section is
# already in the card. Round-45 leaves the window.
landing = CARD + (
    "\n## Round 47 — the two frozen counters\n\n"
    "Base `13a9e9e1`; freeze `5017e1f7`. Wave 1: 75 seats.\n\n"
    "| claim | before | after |\n|---|---|---|\n| R47-C2 | red | green |\n\n"
    "Measured at `2e4ae434`, receipt `.ufo/waves/round-47/l1/scores/`.\n")
run("E9_landing_with_round47_section", landing)

# E10: does the landing-shaped card still report the round-45 corrections as exempting
# anything? And how many atoms survive?
code, rec = run("E10_landing_full_atoms", landing)
out["E10_exempted_keys"] = [e["class"] + ":" + str(e["key"]) for e in rec.get("exempted", [])]
out["E10_atoms_by_class"] = rec.get("atoms_by_class")

# E11: with the landing section, delete the round-45 seats correction -> is it still needed?
card_no45corr = landing.replace(
    "- corrects seats round-45: 2 waves, 76 seats total — `w1-dispatch.json` reports `counts.spawn 40`\n"
    "  and `w2-dispatch.json` reports `counts.spawn 36`, so the round-45 cell's \"wave 2: 32 seats\"\n"
    "  understates the dispatched wave by four.\n", "")
assert card_no45corr != landing, "correction text did not match"
run("E11_landing_minus_round45_correction", card_no45corr)

print(json.dumps(out, indent=1))
