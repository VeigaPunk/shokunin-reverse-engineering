#!/usr/bin/env python3
"""RevC2Exempt — panels against the CURRENT instrument (A5 = a631bba0) and landing card."""
import hashlib
import importlib.util
import json
import os

S = "/fast/scratch/hyaku/kaidoku-r47/RevC2Exempt"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
INST = os.path.join(S, "inst-a631bba0", "round-47", "record.py")
REV = "07d2894e"

spec = importlib.util.spec_from_file_location("recA5", INST)
rec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rec)
FILES = lambda p: rec.gate.show(LANE, REV, p)  # noqa: E731
CARD = rec.gate.show(LANE, REV, "SCORECARD.md")
CORR_HEAD = "## Record corrections — round 47"
C45 = "- corrects seats round-45: 2 waves, 76 seats total"
C46 = "- corrects seats round-46: 2 waves, 80 seats total"
CW = ("- corrects window round-46: empty in 332f4884..58eb04b6 -- "
      "tools/round-46 plans/round-46-claims.md")


def with_corr(card, lines):
    at = card.find(CORR_HEAD)
    return (card[:at] if at >= 0 else card) + CORR_HEAD + "\n\n" + "\n".join(lines) + "\n"


def run(name, card, expect, note, battery=False):
    code, receipt = rec.evaluate_text(card, FILES, LANE, REV, battery=None)
    clause = {"exit": code, "failing": receipt.get("failing")}
    if battery and code in (0, 1):
        b = rec.run_battery(card, FILES, LANE, REV)
        code, receipt = rec.evaluate_text(card, FILES, LANE, REV, battery=b)
    out = {"panel": name, "mode": "cli" if battery else "clauses",
           "clause_exit": clause["exit"], "clause_failing": clause["failing"],
           "exit": code, "expect_exit": expect, "ok": code == expect, "note": note,
           "failing": receipt.get("failing"),
           "mismatches": [{"class": m["class"], "key": m["key"], "atom": m["atom"][:120]}
                          for m in receipt.get("mismatches", [])],
           "exempted": [{"class": a["class"], "key": a["key"], "atom": a["atom"][:100]}
                        for a in receipt.get("exempted", [])],
           "corrections": receipt.get("corrections"),
           "corrections_bad": [b["detail"] if isinstance(b, dict) else b
                               for b in (receipt.get("corrections_bad") or [])],
           "battery": receipt.get("battery"),
           "card_sha256": hashlib.sha256(card.encode()).hexdigest()}
    print(json.dumps({k: out[k] for k in ("panel", "mode", "clause_exit", "exit",
                                          "expect_exit", "ok", "failing", "exempted",
                                          "corrections", "corrections_bad")}, indent=1))
    return out


panels = []

# R0 — the L1's own claim, reproduced.
panels.append(run("R0-landed-card", CARD, 0, "landing card, A5 instrument", battery=True))

# R1 — a correction for a round the card never contains is accepted as historical.
phantom = CARD.replace(CW, CW + "\n- corrects window round-3: empty in "
                                  "13a9e9e1..13a9e9e1 -- corpus/")
panels.append(run("R1-phantom-historical-window-correction-clauses", phantom, 0,
                  "round-3 appears nowhere in the card; A3 accepts the line as historical"))

# R1b — one real historical line + one phantom line satisfies corrections >= 2 with the
# exemption granted by the phantom line, through the full CLI (battery included).
r1b = with_corr(CARD, [C45, "- corrects window round-3: empty in 13a9e9e1..13a9e9e1 -- corpus/"])
panels.append(run("R1b-phantom-line-full-cli", r1b, 0,
                  "corrections 2, one of them names a round that does not exist, "
                  "the placeholder atom is exempted by that phantom line", battery=True))

# R2 — the correction's window/pathspec need not be the atom's: any empty window over any
# real path exempts a placeholder atom. `corpus/lessons/` over the round-46 window.
r2 = with_corr(CARD, [C45, C46,
                      "- corrects window round-46: empty in 332f4884..58eb04b6 -- "
                      "corpus/lessons/"])
panels.append(run("R2-window-correction-over-unrelated-pathspec", r2, 0,
                  "the atom's own pathspec (tools/round-46 plans/round-46-claims.md) is "
                  "never compared with the correction's", battery=True))

# R3 — content blindness: two contradictory seat atoms in one round, one correction.
two_seat = CARD.replace("Waves: 40 + 40 = 80 seats",
                        "Waves: 40 + 40 = 80 seats. Waves: 40 + 45 = 85 seats")
panels.append(run("R3-one-line-exempts-contradictory-seat-atoms",
                  with_corr(two_seat, [C45, C46, CW]), 0,
                  "both seat atoms share key '46'; one statement exempts both, so the card "
                  "keeps a claim the correction does not identify", battery=True))

# R4 — the cap: three false seat atoms + one placeholder window = 4 atoms > 3.
three_seat = CARD.replace("Waves: 40 + 40 = 80 seats",
                          "Waves: 40 + 40 = 80 seats. Waves: 40 + 45 = 85 seats. "
                          "Wave 1: 39 seats; wave 2: 36 seats")
panels.append(run("R4-four-exemptible-atoms", with_corr(three_seat, [C45, C46, CW]), 1,
                  "cap holds: exempted 4 > 3", battery=False))
three_only = CARD.replace("Waves: 40 + 40 = 80 seats",
                          "Waves: 40 + 40 = 80 seats. Waves: 40 + 45 = 85 seats")
panels.append(run("R4b-three-exemptible-atoms", with_corr(three_only, [C45, C46, CW]), 0,
                  "three false atoms, three exemptions, exit 0", battery=False))

with open(os.path.join(S, "out", "attack-panels3.json"), "w") as fh:
    json.dump({"rev": REV, "instrument_sha256":
               hashlib.sha256(open(INST, "rb").read()).hexdigest(),
               "panels": panels}, fh, indent=1, sort_keys=True)
print(json.dumps({"unexpected": [p["panel"] for p in panels if not p["ok"]]}))
