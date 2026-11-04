#!/usr/bin/env python3
"""Assemble the round-88 mutation table from measured artifacts.

Inputs (all measured by this seat, none typed):
  mutants.json        - 13 declared mutants + 3 control-green probes, with the
                        exact anchor/replacement, anchor-match count, diff and
                        the --selftest rc / case count / failure names
  base-receipt.json   - the base counter run with REA enabled (claim predicate)
  receipt-<id>.json   - one full counter run per repair mutant (--no-rea)
  geometry-probe.json - derived sz_cpr for base/R03/R04 on three carriers
Output: table.json (seat dir).
"""

import hashlib
import json
import os
import shutil

S = "/fast/scratch/hyaku/kaidoku-r88/ExecMutation"
SEAT = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
        "/.ufo/waves/round-88/w1/ExecMutation")
REC = os.path.join(SEAT, "receipts")
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

ARMS = ("repair_rc0", "field_only", "test_ok", "identity")


def keep(path):
    """Copy a measured artifact into the seat dir; return its lane-relative path."""
    os.makedirs(REC, exist_ok=True)
    dst = os.path.join(REC, os.path.basename(path))
    shutil.copy2(path, dst)
    return os.path.relpath(dst, LANE)


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    mut = json.load(open(os.path.join(S, "mutants.json")))
    base = json.load(open(os.path.join(S, "base-receipt.json")))
    geo = json.load(open(os.path.join(S, "geometry-probe.json")))

    rows = []
    for r in mut["rows"]:
        row = {k: r[k] for k in (
            "id", "file", "anchor", "replacement", "declared_case", "rationale",
            "anchor_count", "mutant_sha256", "source_sha256", "selftest_rc",
            "selftest_cases", "selftest_failures", "declared_case_present",
            "declared_case_failed", "verdict", "diff")}
        rp = os.path.join(S, f"receipt-{r['id']}.json")
        if os.path.isfile(rp):
            d = json.load(open(rp))
            per = {c["carrier"]: {k: c["arms"][k] for k in ARMS} for c in d["cases"]}
            false_arms = {c["carrier"]: {k: v for k, v in c.get("false_arms", {}).items()
                                         if k != "rea_recover"} for c in d["cases"]}
            killed = any(not all(a.values()) for a in per.values())
            row["counter_probe"] = {
                "receipt": keep(rp),
                "receipt_sha256": sha(rp),
                "command": "python3 tools/round-88/upx-chain-battery.py --root <lane> "
                           f"--repair-cmd <mutant {r['id']}> --upx /usr/bin/upx "
                           "--pkg <rea-agents> --work <scratch>/work-"
                           f"{r['id']} --json-out <scratch>/receipt-{r['id']}.json --no-rea",
                "rea_enabled": False,
                "note": "rea_recover is false by --no-rea in every case; only the four "
                        "byte-level arms are read here",
                "controls_ok": d["controls_ok"],
                "per_carrier_arms": per,
                "false_arms": false_arms,
                "counter_kill": killed,
            }
        rows.append(row)

    probes = []
    for p in mut["control_probes"]:
        rp = os.path.join(S, f"receipt-{p['id']}.json")
        d = json.load(open(rp))
        probes.append({
            "id": p["id"], "file": p["file"], "anchor": p["anchor"],
            "replacement": p["replacement"], "rationale": p["rationale"],
            "repair_cmd": p["repair_cmd"], "anchor_count": p["anchor_count"],
            "mutant_sha256": p["mutant_sha256"],
            "receipt": keep(rp), "receipt_sha256": sha(rp),
            "command": "python3 <mutant battery> --root <lane> --repair-cmd "
                       f"{p['repair_cmd']} --upx /usr/bin/upx --pkg <rea-agents> "
                       f"--work <scratch>/work-{p['id']} --json-out <scratch>/"
                       f"receipt-{p['id']}.json --no-rea",
            "measured": {"label": d.get("label"), "recovered": d.get("recovered"),
                         "controls_ok": d.get("controls_ok"),
                         "regression_met": d.get("regression", {}).get("met"),
                         "met_target": d.get("met_target"), "exit": d.get("exit")},
            "control_turned_green": bool(d.get("controls_ok")
                                         and all(d["controls_ok"].values())),
        })

    out = {
        "schema": "kaidoku-r88-mutation-table-v1",
        "seat": "ExecMutation",
        "round": 88,
        "lane": LANE,
        "instruments": {
            "tools/round-88/upx-chain-repair.py": sha(os.path.join(LANE, "tools/round-88/upx-chain-repair.py")),
            "tools/round-88/upx-chain-battery.py": sha(os.path.join(LANE, "tools/round-88/upx-chain-battery.py")),
        },
        "method": {
            "kill": "a mutant is killed only when its declared case is present in the "
                    "instrument's --selftest and appears in the failure list",
            "gap-absent-case": "the declared case does not exist in the instrument; "
                               "recorded as a coverage gap, never a kill",
            "counter_probe": "each repair mutant was additionally run through the real "
                             "counter with --no-rea; rea_recover is false by construction, "
                             "so only repair_rc0/field_only/test_ok/identity are read",
        },
        "base": {
            "repair_selftest": mut["base"]["repair"],
            "battery_selftest": mut["base"]["battery"],
            "battery_run_with_rea": {
                "command": "python3 tools/round-88/upx-chain-battery.py --root "
                           "/home/vgpnk/Projects/shokunin/kaidoku-shokunin --repair-cmd "
                           "tools/round-88/upx-chain-repair.py --upx /usr/bin/upx --pkg "
                           "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents "
                           "--work /fast/scratch/hyaku/kaidoku-r88/ExecMutation/base-work "
                           "--json-out /fast/scratch/hyaku/kaidoku-r88/ExecMutation/"
                           "base-receipt.json --evidence-dir /fast/scratch/hyaku/"
                           "kaidoku-r88/ExecMutation/base-rea",
                "receipt": keep(os.path.join(S, "base-receipt.json")),
                "receipt_sha256": sha(os.path.join(S, "base-receipt.json")),
                "label": base["label"], "recovered": base["recovered"],
                "target": base["target"], "controls_ok": base["controls_ok"],
                "regression": {k: base["regression"][k] for k in
                               ("recovered", "target", "controls_ok", "met", "rc")},
                "met_target": base["met_target"], "exit": base["exit"],
                "wall_seconds": 182.95,
                "rea_counts": {c["carrier"]: (c.get("rea") or {}).get("counts")
                               for c in base["cases"]},
                "unpacked_sha256": {c["carrier"]: c["unpacked_sha256"] for c in base["cases"]},
                "packed_sha256": {c["carrier"]: c["packed_sha256"] for c in base["cases"]},
            },
        },
        "mutants": rows,
        "control_green_probes": probes,
        "geometry_probe": geo,
        "candidate_census": json.load(open(os.path.join(S, "candidate-census.json"))),
        "candidate_census_artifact": keep(os.path.join(S, "candidate-census.json")),
        "geometry_probe_artifact": keep(os.path.join(S, "geometry-probe.json")),
        "mutant_manifest": keep(os.path.join(S, "mutants.json")),
        "summary": {
            "mutants": len(rows),
            "killed_by_selftest": [r["id"] for r in rows if r["verdict"] == "killed"],
            "survivors_selftest": [r["id"] for r in rows if r["verdict"] == "survivor"],
            "absent_case_gaps": [r["id"] for r in rows if r["verdict"] == "gap-absent-case"],
            "survivors_also_killed_by_counter": [
                r["id"] for r in rows if r["verdict"] == "survivor"
                and r.get("counter_probe", {}).get("counter_kill")],
            "survivors_not_killed_anywhere": [
                r["id"] for r in rows if r["verdict"] == "survivor"
                and not r.get("counter_probe", {}).get("counter_kill")],
            "control_green_probes_green": [p["id"] for p in probes
                                           if p["control_turned_green"]],
            "control_green_probes_met_target": [p["id"] for p in probes
                                                if p["measured"]["met_target"]],
        },
    }
    os.makedirs(SEAT, exist_ok=True)
    path = os.path.join(SEAT, "table.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(out["summary"], indent=1))
    print("wrote", path, sha(path))


if __name__ == "__main__":
    main()
