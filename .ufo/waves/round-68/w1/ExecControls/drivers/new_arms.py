#!/usr/bin/env python3
"""new_arms.py - round-68 extra controls (A registry pollution, B packed-count
shortcut, C all-false) scored against the committed instruments' own functions.

Arm A plants defects in a scratch clone of the real base-revision inputs and
asks the imported census which of its mismatch classes fire.
Arm B builds synthetic carriers whose packed inventory equals the original's
(the "detection from a packed count" shortcut) and asks carrier_arms/fold.
Arm C is the degenerate all-false carrier.

Every arm records the value it would score if the counter were wrong
(`false_green_value`) and the exact committed expression that blocks it.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
RC = os.path.join(LANE, "tools", "round-68", "registry-conformance.py")
PE = os.path.join(LANE, "tools", "round-68", "packed-elf.py")
BASE = "fcbe200f6739c38939e0dabf3f251de2cc6bd727"
PRE = os.path.join(LANE, ".ufo", "waves", "round-68", "l1", "pre")
SCRATCH = os.environ.get("R68_SCRATCH",
                         "/fast/scratch/hyaku/kaidoku-r68/ExecControls")
FIXTURE = os.path.join(SCRATCH, "registry-fixture")
OUT = os.path.join(LANE, ".ufo", "waves", "round-68", "w1", "ExecControls",
                   "new-arms.json")
FULL = "0=met; 1=not met; 2=could-not-evaluate"


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def row(path: str, verdict: str = FULL) -> str:
    return f"| `{path}` | g | {verdict} | s | p | w | o |"


def inject(skill_text: str, rows: list[str], close: str) -> str:
    idx = skill_text.index(close)
    head, tail = skill_text[:idx], skill_text[idx:]
    if not head.endswith("\n"):
        head += "\n"
    return head + "\n".join(rows) + "\n" + tail


def materialise(name: str, skill_text: str, plans: dict[str, str],
                existing: set[str]) -> dict:
    """Write the fixture tree and read it back: the census gets disk bytes."""
    root = os.path.join(FIXTURE, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "plans"), exist_ok=True)
    with open(os.path.join(root, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(skill_text)
    for rel, text in plans.items():
        dst = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(text)
    with open(os.path.join(root, "existing.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sorted(existing)) + "\n")
    skill_disk = open(os.path.join(root, "SKILL.md"), encoding="utf-8").read()
    plans_disk = {}
    for dirpath, _, files in os.walk(os.path.join(root, "plans")):
        for fname in sorted(files):
            full = os.path.join(dirpath, fname)
            plans_disk[os.path.relpath(full, root)] = open(full, encoding="utf-8").read()
    existing_disk = set(open(os.path.join(root, "existing.txt"),
                             encoding="utf-8").read().split())
    return {"root": root, "skill": skill_disk, "plans": plans_disk,
            "existing": existing_disk}


def self_plans_from_rows(rc_mod, rows: list[dict]) -> dict[str, str]:
    """Reproduce the committed c1-shortcut-self scope: plans built from rows."""
    self_plans: dict[str, set[str]] = {}
    for r in rows:
        m = rc_mod.re.match(r"tools/round-(\d+)/", r["path"])
        if not m:
            continue
        self_plans.setdefault(
            f"plans/round-{int(m.group(1))}-claims.md", set()).add(r["path"])
    return {k: "\n".join(sorted(v)) for k, v in self_plans.items()}


def arm_a(rc_mod, plans: dict[str, str], skill: str, existing: set[str]) -> dict:
    missing = [p for p in ("tools/round-67/avm-le-counter.py",
                           "tools/round-67/mutation-battery.py") if p in existing]
    baseline_rows = [row(p) for p in missing]
    baseline_skill = inject(skill, baseline_rows, rc_mod.MARK_CLOSE)
    base = rc_mod.census(plans, baseline_skill, existing)

    planted = ["tools/round-68/never-built.py"]
    thin_path = "tools/round-40/c1-counter.py"
    junk_skill = inject(baseline_skill, [row(planted[0]), row(thin_path, "0=met")],
                        rc_mod.MARK_CLOSE)
    junk = rc_mod.census(plans, junk_skill, existing)

    # the census reads the planted table from disk, in a scratch tree
    fixture = materialise("junk", junk_skill, plans, existing)
    junk_disk = rc_mod.census(fixture["plans"], fixture["skill"], fixture["existing"])

    # decomposition: a counter that summed only `unregistered` reports 0 here
    wrong_sum = len(junk["unregistered"]) + len(junk["duplicate_rows"])
    self_census = rc_mod.census(self_plans_from_rows(rc_mod, rc_mod.registry_rows(junk_skill)),
                                junk_skill, existing)

    # a full-verdict row for an existing but out-of-plan-scope tool
    oos_path = "tools/round-40/sqfs-list.py"
    oos_skill = inject(baseline_skill, [row(oos_path)], rc_mod.MARK_CLOSE)
    oos = rc_mod.census(plans, oos_skill, existing)

    observed = {
        "baseline": {"mismatches": base["mismatches"], "scope_size": base["scope_size"],
                     "registry_rows": base["registry_rows"]},
        "junk": {"mismatches": junk["mismatches"],
                 "row_absent": junk["row_absent"], "thin": junk["thin"],
                 "unregistered": junk["unregistered"],
                 "duplicate_rows": junk["duplicate_rows"],
                 "registry_rows": junk["registry_rows"]},
        "junk_from_disk": {"mismatches": junk_disk["mismatches"],
                           "row_absent": junk_disk["row_absent"],
                           "thin": junk_disk["thin"],
                           "fixture_root": fixture["root"]},
        "wrong_sum_registry_classes": wrong_sum,
        "self_scope_census": {"mismatches": self_census["mismatches"],
                              "scope_size": self_census["scope_size"]},
        "out_of_scope_full_verdict": {"path": oos_path,
                                      "mismatches": oos["mismatches"]},
    }
    ok = (base["mismatches"] == 0 and base["scope_size"] > 0
          and junk["mismatches"] == 2
          and junk["row_absent"] == planted
          and junk["thin"] == [thin_path]
          and junk["unregistered"] == [] and junk["duplicate_rows"] == []
          and junk_disk["mismatches"] == 2
          and junk_disk["row_absent"] == planted and junk_disk["thin"] == [thin_path]
          and wrong_sum == 0 and self_census["mismatches"] == 2
          and oos["mismatches"] == 0)
    return {
        "id": "A-registry-junk-fixture",
        "class": "shortcut control (table pollution)",
        "expected": {"baseline_mismatches": 0, "junk_mismatches": 2,
                     "row_absent": planted, "thin": [thin_path]},
        "observed": observed,
        "ok": ok,
        "false_green_value": {
            "wrong_sum_unregistered_plus_duplicate_only": wrong_sum,
            "self_scope_census_mismatches": self_census["mismatches"],
            "note": ("a census that summed only unregistered/duplicate reports 0 on a "
                     "table carrying one fabricated row and one thin cell — that is "
                     "the false-green value. The table-with-itself shortcut reports 2 "
                     "here because both planted defects are row-visible; its false "
                     "green is confined to omission (measured at base by "
                     "c1-shortcut-self: 0 while the truth is 2 unregistered paths)."),
        },
        "why_committed_cannot": (
            "mismatches is the sum of four independently computed lists: "
            "len(unregistered) + len(duplicate_rows) + len(row_absent) + len(thin); "
            "row_absent compares every row path against the git ls-tree blob set and "
            "thin runs VERDICT_RE's three bullets over the row's verdict cell, so a "
            "fabricated row and a 0-only verdict cell each add 1 even though no plan "
            "mentions them."),
    }


def arm_b(pe_mod, packed: dict) -> dict:
    carriers = packed["carriers"]
    results = {}

    def synth(packed_counts: dict) -> list[dict]:
        out = []
        for c in carriers:
            pc = packed_counts if packed_counts else {}
            before_ok = (pc.get("procedure_count") is not None
                         and pc["procedure_count"] < c["before_floor"])
            has_refusal = c.get("refusal") is not None
            arms = pe_mod.carrier_arms(True, before_ok, True, True,
                                       True if has_refusal else None)
            out.append({"id": c["id"], "packed_counts": pc,
                        "orig_counts": c["orig_counts"],
                        "before_floor": c["before_floor"],
                        "arms": arms, "ok": all(arms.values())})
        return out

    for name, pc in (("b1_packed_equals_original", None),
                     ("b2_packed_inventory_absent", {})):
        if pc is None:
            syn = synth({})  # placeholder, replaced per carrier below
            for item, c in zip(syn, carriers):
                item["packed_counts"] = dict(c["orig_counts"])
                item["arms"] = pe_mod.carrier_arms(
                    True, (c["orig_counts"]["procedure_count"] < c["before_floor"]),
                    True, True, True if c.get("refusal") else None)
                item["ok"] = all(item["arms"].values())
        else:
            syn = synth(pc)
        verdict = pe_mod.fold(syn, packed["control_ok"], packed["target"])
        results[name] = {"carriers": syn, "fold": verdict,
                         "false_green_fold": pe_mod.fold(
                             [{"ok": True} for _ in syn], True, packed["target"])}
    ok = all(not v["fold"]["met_target"] for v in results.values())
    return {
        "id": "B-packed-inventory-equals-original",
        "class": "shortcut control (detection from a packed count)",
        "expected": {"met_target": False},
        "observed": results,
        "ok": ok,
        "false_green_value": {
            "met_target": True,
            "carriers_matched": packed["target"],
            "note": ("scoring before_ok as 'a packed inventory exists' and reusing the "
                     "original's sha/counts gives all-true arms and a green fold; "
                     "that is the value a packed-count-only counter would report"),
        },
        "why_committed_cannot": (
            "before_ok = packed procedure_count is not None and < min_orig_procedures//2 "
            "(50 for jq, 25 for xxd); a packed count equal to the original's is 167/99, "
            "so before_ok is false. identity_ok requires sha256(unpacked) == the carrier "
            "pin, and upx -d refuses a non-packed original (measured control rc 2/2), so "
            "no unpacked file exists to hash. recovery_ok requires a fresh REA analyze of "
            "that file to equal orig_counts. control_ok additionally requires upx -l and "
            "-d to fail on the original, which the committed receipt records as 2/2."),
    }


def arm_c(pe_mod, packed: dict) -> dict:
    all_false = pe_mod.carrier_arms(False, False, False, False, False)
    c1 = pe_mod.fold([{"ok": all(all_false.values())},
                      {"ok": all(all_false.values())}], True, packed["target"])
    c2 = pe_mod.fold([{"ok": True}, {"ok": True}], False, packed["target"])
    c3 = pe_mod.fold([{"ok": True}, {"ok": False}], True, packed["target"])
    observed = {
        "c1_every_arm_false": {"arms": all_false, "carrier_ok": all(all_false.values()),
                               "fold": c1},
        "c2_control_false": c2,
        "c3_one_carrier_short": c3,
    }
    ok = (c1["met_target"] is False and c2["met_target"] is False
          and c3["met_target"] is False)
    return {
        "id": "C-all-false",
        "class": "degenerate control",
        "expected": {"met_target": False},
        "observed": observed,
        "ok": ok,
        "false_green_value": {
            "c1_every_arm_false": {"met_target": True, "carriers_matched": 2},
            "c2_control_false": {"met_target": True},
            "note": ("a fold that counted carriers instead of all(arms.values()) would "
                     "green both; a fold that dropped control_ok would green the second"),
        },
        "why_committed_cannot": (
            "each carrier's ok = all(arms.values()); fold counts only c['ok'], and "
            "met_target = matched == target and bool(control_ok). A carrier with any "
            "false arm is never counted, and control_ok is folded from the packer's "
            "refusal on every original."),
    }


def main() -> int:
    rc_mod = load(RC, "r68_registry")
    pe_mod = load(PE, "r68_packed")
    plans, skill, existing = rc_mod.read_revision(LANE, BASE)
    with open(os.path.join(PRE, "c2-dryrun-at-base.json"), encoding="utf-8") as fh:
        packed = json.load(fh)
    a = arm_a(rc_mod, plans, skill, existing)
    b = arm_b(pe_mod, packed)
    c = arm_c(pe_mod, packed)
    payload = {
        "schema": "kaidoku-r68-new-arms-v1",
        "base": BASE,
        "revision_note": ("census inputs read at the base revision through read-only "
                          "git; packed arms reuse the committed base dry-run receipt"),
        "arm_count": 3,
        "shortcut_control_count": 2,
        "arms": [a, b, c],
        "ok": a["ok"] and b["ok"] and c["ok"],
    }
    text = json.dumps(payload, indent=1, sort_keys=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
