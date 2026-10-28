#!/usr/bin/env python3
"""SimplC2 scratch harness: card-level questions about tools/round-47/record.py.

Imports a counter copy as a module and drives evaluate_text against the real lane repo
at a fixed revision. Read-only on the lane; all receipts land in $S/receipts.
"""
import hashlib
import importlib.util
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.path.dirname(os.path.abspath(__file__))
REV_FREEZE = "07d2894eabe88c326e9036262f20ad02662c860d"  # declared freeze (A5)
REV_BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
OUT = os.path.join(S, "receipts")
os.makedirs(OUT, exist_ok=True)


def load(modname, path):
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    spec.loader.exec_module(mod)
    return mod


def card_at(rev):
    import subprocess
    r = subprocess.run(["git", "-C", LANE, "show", f"{rev}:SCORECARD.md"],
                       capture_output=True, text=True, check=True)
    return r.stdout


def files_at(rev):
    import subprocess

    def show(path):
        r = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"],
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    return show


def run_case(name, mod, card, rev, extra=None):
    code, rec = mod.evaluate_text(card, files_at(rev), LANE, rev, battery=None)
    row = {"case": name, "module": os.path.basename(os.path.dirname(mod.__file__)),
           "rev": rev, "exit": code,
           "card_sha256": hashlib.sha256(card.encode()).hexdigest(),
           "corrections": rec.get("corrections"),
           "exempted": [e["class"] + ":" + str(e["key"]) for e in rec.get("exempted", [])],
           "mismatches": [m["class"] + ":" + str(m["key"]) for m in rec.get("mismatches", [])],
           "corrections_bad": len(rec.get("corrections_bad", [])),
           "atoms_by_class": rec.get("atoms_by_class"),
           "failing": rec.get("failing")}
    if extra:
        row.update(extra)
    return row


def patch_head(card, old, new):
    assert card.count(old) == 1, (old, card.count(old))
    return card.replace(old, new, 1)


def patch_axes_head(card, old, new):
    """Replace a fraction only inside the CURRENT `## Owned axes` section."""
    i = card.index("## Owned axes")
    j = card.find("\n## ", i + 1)
    head, body, tail = card[:i], card[i:j], card[j:]
    assert body.count(old) == 1, (old, body.count(old))
    return head + body.replace(old, new, 1) + tail


def main():
    real = load("rec_real", os.path.join(S, "mut/base/record.py"))
    card = card_at(REV_FREEZE)
    rows = []

    # --- T1: baseline at the declared freeze / base -------------------------------
    rows.append(run_case("freeze-baseline", real, card, REV_FREEZE))
    rows.append(run_case("base-baseline", real, card_at(REV_BASE), REV_BASE))

    # --- T2: is the axes derivation the only guard on the Owned-axes head? --------
    forged = patch_axes_head(card, "138/138", "199/199")
    rows.append(run_case("axes-head-forged-199", real, forged, REV_FREEZE))
    forged2 = patch_axes_head(card, "24/24", "3/3")
    rows.append(run_case("axes-head-forged-depth-3", real, forged2, REV_FREEZE))
    # a counter that keeps the class but trusts the claim: shows the guard is the derive()
    # branch, and that clause 2 alone would not have caught this card
    bypass = load("rec_bypass", os.path.join(S, "mut/bypass/record.py"))
    rows.append(run_case("axes-head-forged-199-bypass", bypass, forged, REV_FREEZE))
    rows.append(run_case("freeze-baseline-bypass", bypass, card, REV_FREEZE))
    # and a counter with the class cut: clause 2 fires even on the pristine card
    cut = load("rec_cut", os.path.join(S, "mut/cut/record.py"))
    rows.append(run_case("freeze-baseline-cut", cut, card, REV_FREEZE))
    rows.append(run_case("axes-head-forged-199-cut", cut, forged, REV_FREEZE))

    # --- T3: CORR_MIN=2, real floor or formality? ---------------------------------
    # (a) the landing card minus the historical seats correction
    lines = card.splitlines(keepends=True)
    drop = [l for l in lines if l.startswith("- corrects seats round-45")]
    assert len(drop) == 1
    one = card.replace(drop[0], "", 1)
    rows.append(run_case("corrections-1-landing-minus-seats", real, one, REV_FREEZE))
    min1 = load("rec_min1", os.path.join(S, "mut/min1/record.py"))
    rows.append(run_case("corrections-1-minus-seats-CORR_MIN-1", min1, one, REV_FREEZE))

    # (b) replace the historical seats correction with a *decorative but true* one for
    #     round 44 (dispatch: w1 37 + w2 42 = 79) that exempts nothing
    deco = one.replace("## Round 47", "- corrects seats round-44: 2 waves, 79 seats total\n\n"
                       "## Round 47", 1)
    rows.append(run_case("corrections-2-decorative-round44", real, deco, REV_FREEZE))

    # (c) zero real repairs: fix the round-46 window sentence in place with a concrete
    #     pair that reproduces as empty, then two decorative historical corrections
    wpath, wpair = "332f4884", "58eb04b6"
    old_win = "0425224..<tip>"
    fixed = patch_head(card, old_win, f"{wpair}..{wpair}")
    fixed = fixed.replace("- corrects seats round-45", "- no-op seats round-45", 1)
    fixed = fixed.replace("- corrects window round-46", "- no-op window round-46", 1)
    fixed = fixed.replace("## Round 47",
                          "- corrects seats round-43: 2 waves, 64 seats total\n"
                          "- corrects seats round-44: 2 waves, 79 seats total\n\n"
                          "## Round 47", 1)
    rows.append(run_case("zero-repair-two-decorative", real, fixed, REV_FREEZE))

    # --- T4: the `- corrects axes` line is not parsed at all ----------------------
    ghost = card.replace(
        "## Round 47", "- corrects axes coverage: 999/999\n\n## Round 47", 1)
    rows.append(run_case("axes-correction-false-999", real, ghost, REV_FREEZE,
                         {"note": "parsed-correction count must not move"}))
    # an axes atom can therefore never be exempted: false claim + correction stays red
    axes_bad = patch_axes_head(card, "138/138", "133/133")
    axes_bad = axes_bad.replace(
        "## Round 47", "- corrects axes coverage: 133/133\n\n## Round 47", 1)
    rows.append(run_case("axes-atom-false-plus-axes-correction", real, axes_bad, REV_FREEZE))

    with open(os.path.join(OUT, "card-matrix.json"), "w") as fh:
        json.dump(rows, fh, indent=1)
    for r in rows:
        print(f"{r['case']:44s} exit={r['exit']} corr={r['corrections']} "
              f"exempt={','.join(r['exempted']) or '-'} fail={r['failing']}")


if __name__ == "__main__":
    main()
