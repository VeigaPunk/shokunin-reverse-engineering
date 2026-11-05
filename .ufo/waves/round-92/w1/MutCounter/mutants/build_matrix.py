#!/usr/bin/env python3
"""Build kill-matrix.json from the MutCounter receipts (scratch). Reads only receipts and
the lane's pre receipts (read-only). Verdict rule: met_target False -> KILLED; True -> SURVIVED.
Gate failures are the label fields that differ from the frozen --expect values."""
import json
import os
import re
import sys

S = "/fast/scratch/hyaku/kaidoku-r92/MutCounter"
L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REC = os.path.join(S, "rec")
REV = "11f8606178dfd9e72001b31daf412c5463106a63"
V2 = "tools/round-92/stop-boundary-battery-v2.py"
C1 = "tools/round-92/stop-boundary-repair-battery.py"
V2_EXPECT = "refused 10 of 10; typed 10; unsafe 0; intact 5 of 5"
C1_EXPECT = "repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10"

# Mutant design intent (what each mutant is supposed to demonstrate), per the assignment.
ROWS = [
    ("M1", V2, V2_EXPECT, "counterfeit of CHEAT-A carrier-read; xz ADDED to carrier list",
     "carrier-read oracle that knows the unseen carrier"),
    ("M2", V2, V2_EXPECT, "counterfeit of CHEAT-B hash table; sha256 of five fresh packed carriers",
     "hash-table oracle over the five pinned carriers"),
    ("M3", V2, V2_EXPECT, "rc 2 with plain-text last stdout line", "typed-refusal check"),
    ("M4", V2, V2_EXPECT, "rc 2 that also writes the output file", "no-output-on-refusal check"),
    ("M5", V2, V2_EXPECT, "rc 2 with JSON that has no `refused` key", "typed-refusal key check"),
    ("M6", V2, V2_EXPECT, "exit 1 on all refusals (CHEAT-C variant)", "rc-2 typed-refusal check"),
    ("CA", V2, V2_EXPECT, "harness cross-check: CHEAT-A (four carriers), clone copy",
     "must reproduce lane pre label"),
    ("CB", V2, V2_EXPECT, "harness cross-check: CHEAT-B (four hashes), clone copy",
     "must reproduce lane pre label"),
    ("CC", V2, V2_EXPECT, "harness cross-check: CHEAT-C (exit 1), clone copy",
     "must reproduce lane pre label"),
    ("X1", V2, V2_EXPECT, "EXTRA (beyond the six assigned): tampered -> input + sentinel, rc 0",
     "v2 unsafe gate (no assigned mutant reaches it)"),
    ("N1", C1, C1_EXPECT, "carrier-table repair; pinned packed image for tampered cells; refuses others",
     "table repair, literal (intact refused)"),
    ("N1i", C1, C1_EXPECT, "carrier-table repair with intact identity passthrough",
     "table repair that passes every gate it can"),
    ("N2", C1, C1_EXPECT, "tampered input + sentinel word outside window (rc 0)", "unsafe gate"),
    ("N3", C1, C1_EXPECT, "window rewritten to value != pristine (XOR 1), rc 0", "wrong gate"),
    ("N4", C1, C1_EXPECT, "repairs far cells to pristine; refuses others (intact refused)",
     "far-refused gate and intact gate"),
    ("N4i", C1, C1_EXPECT, "repairs far cells to pristine; intact identity passthrough",
     "far-refused gate alone"),
    ("N5", C1, C1_EXPECT, "tampered -> pristine; far refused; intact with one byte changed",
     "intact-identity gate alone"),
]
BASE = [
    ("B0", V2, V2_EXPECT, "positive control: round-91 refusal tool under v2 (must be met)", "control"),
    ("B1", C1, C1_EXPECT, "do-nothing control: round-91 repair under C1 battery (must not be met)",
     "control"),
]
EXPECT_FIELDS = {
    "v2": {"refused": 10, "typed": 10, "unsafe": 0, "intact": 5},
    "c1": {"repaired": 10, "wrong": 0, "unsafe": 0, "intact": 5, "far-refused": 10},
}


def parse_label(label):
    out = {}
    for part in label.split(";"):
        part = part.strip()
        m = re.match(r"^(refused|repaired|wrong|unsafe|typed|intact|far-refused)\s+(\d+)", part)
        if m:
            out[m.group(1)] = int(m.group(2))
    return out


def gate_failures(label, kind):
    got = parse_label(label)
    want = EXPECT_FIELDS[kind]
    return {k: {"want": v, "got": got.get(k)} for k, v in want.items() if got.get(k) != v}


def cell_summary(rec):
    cells = rec.get("cells", [])
    by = {}
    for c in cells:
        key = (c.get("kind", "near"), c.get("class"))
        by[f"{key[0]}:{key[1]}"] = by.get(f"{key[0]}:{key[1]}", 0) + 1
    intact = [i.get("identity") for i in rec.get("intact", [])]
    return {"cell_classes": by, "intact_identity": intact}


def load_matrix():
    rows = {}
    with open(os.path.join(REC, "matrix.log"), encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            rows[parts[0]] = {"counter": parts[1], "cmd": parts[2],
                              "exit": int(parts[3].split("=")[1]), "stdout_last": parts[4]}
    return rows


def main():
    logs = load_matrix()
    counters = {V2: None, C1: None}
    out_rows = []
    for rid, counter, expect, desc, intent in ROWS + [(b[0], b[1], b[2], b[3], b[4]) for b in BASE]:
        rec_path = os.path.join(REC, f"{rid}.json")
        if rid in ("B0", "B1"):
            rec_path = os.path.join(REC, {"B0": "B0-positive-v2-round91.json",
                                          "B1": "B1-do-nothing-c1-round91.json"}[rid])
        with open(rec_path, encoding="utf-8") as fh:
            rec = json.load(fh)
        kind = "v2" if counter == V2 else "c1"
        label = rec.get("label", rec.get("unevaluable"))
        met = bool(rec.get("met_target"))
        if counter == V2:
            counters[V2] = rec.get("counter_sha256")
        else:
            counters[C1] = rec.get("counter_sha256")
        if rid in logs:
            exit_code = logs[rid]["exit"]
            cmd = (f"TMPDIR=$S/tmp python3 -I -B {counter} --root $C --repair-cmd "
                   f"{logs[rid]['cmd']} --work $S/work/{rid} --rev {REV} --expect \"{expect}\" "
                   f"--json-out $R/{rid}.json")
        else:
            exit_code = 0 if met else 1
            cmd = (f"TMPDIR=$S/tmp python3 -I -B {counter} --root $C --repair-cmd "
                   f"{rec.get('repair')} --work $S/work/{rid} --rev {REV} --expect \"{expect}\" "
                   f"--json-out $R/{rid}.json (baseline run, from the B-series)")
        row = {
            "id": rid,
            "intent": desc,
            "design_check": intent,
            "counter": counter,
            "counter_sha256": rec.get("counter_sha256"),
            "repair_cmd": logs.get(rid, {}).get("cmd", rec.get("repair")),
            "repair_sha256": rec.get("repair_sha256"),
            "command": cmd,
            "exit": exit_code,
            "label": label,
            "met_target": met,
            "verdict": ("SURVIVED" if met else "KILLED") if rid not in ("B0", "B1")
                       else ("CONTROL-MET" if met else "CONTROL-NOT-MET"),
            "gate_failures": gate_failures(label, kind) if isinstance(label, str) and "unevaluable" not in rec else None,
            "counts": rec.get("counts"),
            "summary": cell_summary(rec),
            "receipt": f"receipts/{os.path.basename(rec_path)}",
        }
        out_rows.append(row)

    # harness cross-check: clone counterfeits vs the lane's pre receipts for the same counterfeit
    pre_dir = os.path.join(L, ".ufo/waves/round-92/pre")
    xcheck = {}
    for rid, pre in (("CA", "c2-counterfeit-A-v2.json"), ("CB", "c2-counterfeit-B-v2.json"),
                     ("CC", "c2-counterfeit-C-v2.json")):
        with open(os.path.join(pre_dir, pre), encoding="utf-8") as fh:
            pre_label = json.load(fh).get("label")
        mine = next(r["label"] for r in out_rows if r["id"] == rid)
        xcheck[rid] = {"lane_pre_label": pre_label, "mutmatrix_label": mine,
                       "reproduces": pre_label == mine}

    survivors = [r["id"] for r in out_rows if r["verdict"] == "SURVIVED"]
    killed = [r["id"] for r in out_rows if r["verdict"] == "KILLED"]
    doc = {
        "seat": "MutCounter",
        "lane": "kaidoku",
        "round": 92,
        "revision": REV,
        "frozen_counter_sha256": counters,
        "expected_counter_sha256": {V2: "f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874",
                                    C1: "63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc"},
        "rows": out_rows,
        "killed": killed,
        "survived": survivors,
        "harness_crosscheck": xcheck,
        "rule": "met_target False -> KILLED (mutant detected); met_target True -> SURVIVED (named limit)",
    }
    out = os.path.join(S, "kill-matrix.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    for r in out_rows:
        print(f"{r['id']:<4} {r['verdict']:<13} exit={r['exit']} met={r['met_target']!s:<5} "
              f"{r['label']}")
    print("survived:", survivors)
    print("killed:", killed)
    print("crosscheck:", json.dumps(xcheck, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
