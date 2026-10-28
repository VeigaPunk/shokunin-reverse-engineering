#!/usr/bin/env python3
"""ScribeCorrections: verify the two drafted `## Record corrections — round 48`
lines against the frozen instruments' own derivation paths.

Line grammar under test (record2.py CORR + record.py corrects + record2._quote_correction):
  - corrects seats round-47: <statement matching CORR_SEATS, deriving (waves, total)>
  - corrects quote round-47: <statement whose first '(atoms|exempted|corrections|mismatches) N'
    token states the receipt value that corrects a wrong quote>

Checks:
  A. before-state: score() on the card AT HEAD as committed -> correction clauses absent/red
  B. candidate card (HEAD bytes + our two lines) -> corrections parsed, each re-derives,
     quote_fixes applied, clause-4 quote_bad empty for exempted 2, floor seats_ok for 47
  C. forged quote value (exempted 2) -> _quote_correction rejects (not backed)
  D. forged seats value (2 waves / wrong total) -> corrects() rejects
  E. post-landing simulation: card + fake `## Round 48` section (in-scope sections become
     47+48) + corrections -> both corrections still re-derive; seats floor still ok
All lane reads are read-only (`git show`, `rev-parse`, `merge-base`, `log`).
"""
import hashlib
import json
import os
import re
import sys
import time

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(ROOT, "tools/round-48"))
sys.path.insert(0, os.path.join(ROOT, "tools/round-46"))
import gate  # noqa: E402
import record2  # noqa: E402

REV = "HEAD"
SEATS_LINE = ("- corrects seats round-47: 1 wave, 75 seats total — "
              ".ufo/waves/round-47/w1-dispatch.json reports counts.spawn 75 "
              "and is the only dispatch file for the round; the section names "
              "no seat total.")
QUOTE_LINE = ("- corrects quote round-47: exempted 1 — the cited receipt "
              ".ufo/waves/round-47/l1/scores/c2-at-A7.json exempts one atom "
              "(a list of one element), where the section quotes \"exempted 2\".")
CORR_BLOCK = ("\n## Record corrections — round 48\n\n"
              "Append-only repair of atoms `tools/round-48/record2.py` re-derives; "
              "each `corrects` line is itself re-derived by the counter at the "
              "measured revision.\n\n" + SEATS_LINE + "\n" + QUOTE_LINE + "\n")

results = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "rev_cmd": "rev := HEAD (f3a7afc…)", "checks": {}}


def files_at(rev):
    return lambda p: gate.show(ROOT, rev, p)


card = gate.show(ROOT, REV, "SCORECARD.md")
mod = record2.oracle(ROOT, REV)
files = files_at(REV)
spawns = record2.spawns_cache(mod, files)

# --- A: before-state --------------------------------------------------------
codeA, rA = record2.score(card, files, ROOT, REV, "v3", battery=None)
results["checks"]["A_before_score"] = {
    "exit": codeA,
    "failing": rA.get("failing"),
    "quotes_bad": rA.get("quotes_bad"),
    "floor_47": [r for r in rA.get("floor", []) if r["round"] == "round-47"],
}

# --- B: candidate card ------------------------------------------------------
cand = card.rstrip() + "\n" + CORR_BLOCK
corrs = record2.corrections_section(cand)
results["checks"]["B_parsed_lines"] = corrs

cand_files_map = {record2.CARD: cand}


def cand_files(p):
    if p in cand_files_map:
        return cand_files_map[p]
    return gate.show(ROOT, REV, p)


codeB, rB = record2.score(cand, cand_files, ROOT, REV, "v3", battery=None)
results["checks"]["B_candidate_score"] = {
    "exit": codeB,
    "corrections": rB.get("corrections"),
    "corrections_bad": rB.get("corrections_bad"),
    "quotes_bad": rB.get("quotes_bad"),
    "quotes_corrected": rB.get("quotes_corrected"),
    "quotes_checked": rB.get("quotes_checked"),
    "floor": rB.get("floor"),
    "failing": rB.get("failing"),
}

# --- C: forged quote value --------------------------------------------------
forged = dict(corrs[1])
forged["statement"] = "exempted 2 — a forged correction restating the wrong quote"
secs = record2.section_bodies(cand)
okC, detC = record2._quote_correction(forged, secs, cand_files)
results["checks"]["C_forged_quote"] = {"ok": okC, "detail": detC}

# --- D: forged seats values -------------------------------------------------
forgD = []
for bad in ("2 waves, 75 seats total", "1 wave, 74 seats total",
            "1 wave, 76 seats total", "75 seats"):
    e = dict(corrs[0])
    e["statement"] = bad
    okD, detD = mod["corrects"](e, cand_files, ROOT, REV, record2.spawns_cache(mod, cand_files))
    forgD.append({"statement": bad, "ok": okD, "detail": detD})
okD0, detD0 = mod["corrects"](corrs[0], cand_files, ROOT, REV,
                              record2.spawns_cache(mod, cand_files))
results["checks"]["D_seats"] = {"genuine": {"ok": okD0, "detail": detD0},
                               "forged": forgD}
# A minimal oracle-clean `## Round 48` section: seat atom bound to the w1
# dispatch (overlaid from the worktree, which is what the landing commits), a
# window that is empty by git log, path atoms the landing will carry (the
# committed round-47 receipt) plus the uncommitted round-48 control (overlaid),
# two rev atoms, both claim ids. files() serves CARD=candidate bytes and
# overlays the not-yet-committed round-48 files.
disk_dispatch = None
dp = os.path.join(ROOT, ".ufo/waves/round-48/w1-dispatch.json")
if os.path.exists(dp):
    disk_dispatch = open(dp).read()
disk_ctl = None
cp = os.path.join(ROOT, ".ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json")
if os.path.exists(cp):
    disk_ctl = open(cp).read()

OVERLAY = {".ufo/waves/round-48/w1-dispatch.json": disk_dispatch,
           ".ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json": disk_ctl}

ROUND48 = ("\n## Round 48 — draft sections for correction grammar verification\n\n"
           "Waves: 75 + 0 = 75 seats. The dispatch file "
           "`.ufo/waves/round-48/w1-dispatch.json` carries counts.spawn 75. "
           "The do-nothing control is `.ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json`. "
           "`git log --name-status --format= 61b87d74..f3a7afc4 -- tools/round-45/` "
           "is empty. Claims R48-C1 and R48-C2 measured at `f3a7afc4` over base "
           "`61b87d74`; the cited receipt is `.ufo/waves/round-47/l1/scores/c2-at-A7.json`.\n")


def sim_files(p):
    if p == record2.CARD:
        return sim_card
    if p in OVERLAY and OVERLAY[p] is not None:
        return OVERLAY[p]
    return gate.show(ROOT, REV, p)


sim_card = card.rstrip() + "\n" + ROUND48 + CORR_BLOCK
codeE, rE = record2.score(sim_card, sim_files, ROOT, REV, "v3", battery=None)
results["checks"]["E_post_landing"] = {
    "exit": codeE,
    "sections": rE.get("sections"),
    "corrections": rE.get("corrections"),
    "corrections_bad": rE.get("corrections_bad"),
    "floor": rE.get("floor"),
    "quotes_bad": rE.get("quotes_bad"),
    "quotes_corrected": rE.get("quotes_corrected"),
    "oracle_failing": rE.get("oracle", {}).get("mismatches"),
    "failing": rE.get("failing"),
}

body = json.dumps(results, indent=1, default=str)
print(body)
print("sha256:", hashlib.sha256(body.encode()).hexdigest())
