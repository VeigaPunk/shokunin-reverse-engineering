#!/usr/bin/env python3
"""Ablation driver v3: (a) v2 made strict, (b) the duplicate-id forgery made
single-defect, (c) the no-op forgery accounting. Each run reports the selftest,
the counter verdict and the per-fixture battery detail.
"""
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/SimplC1"
FREEZE = "f54b3b6d"
BASE = os.path.join(S, "base", "tools", "round-47", "exact.py")
GATE = os.path.join(S, "base", "tools", "round-46", "gate.py")

V2_ROWS = "    elif len(rows) < 4:\n        failing.append(f\"rows {len(rows)} < 4\")"
V2_ARM = ('        if any(not any(t in a.lower() for t in VOCAB) for a in arm):\n'
          '            failing.append("arm cells outside the vocabulary")')
V2_HEADER = ('        header_ok = all(any(t in h.lower() for h in header) for t in\n'
             '                        (x.lower() for x in HEADER))')
DUP = ('    rows.insert(2, ["R46-CL2", "a duplicate trigger cell", "order", "1"])')
C4 = ('        multi = [n for n, ids in enumerate(per_row) if len(ids) != 1]\n'
      '        if multi:\n            failing.append(f"rows naming != 1 routed id: {multi}")\n'
      '        if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:\n'
      '            failing.append(f"routed cardinality {counts} != each of {ROUTED} exactly once")')
NOOP = ('            out["fixtures"].append({"name": name, "error": "mutation was a no-op"})\n'
        '            out["forgeries_total"] += 1\n            out["v2_green"] += 1')
ALLNOOP = ('MUTATIONS = [("substring-arm", _m_substring_arm),\n'
           '             ("duplicate-routed-id", _m_duplicate_id),\n'
           '             ("stale-mutations-digest", _m_stale_digest),\n'
           '             ("flag-order-drift", _m_flag_order)]')

CASES = [
    ("v2-rows-strict", [(V2_ROWS, "    elif len(rows) != 4:\n        failing.append(f\"rows {len(rows)} != 4\")")]),
    ("v2-arm-strict", [(V2_ARM, V2_ARM.replace("not any(t in a.lower() for t in VOCAB)", "a not in VOCAB"))]),
    ("v2-header-strict", [(V2_HEADER, "        header_ok = header == HEADER")]),
    ("dup-forgery-4row", [(DUP, '    rows[1] = ["R46-CL2", "a duplicate trigger cell", "order", "1"]')]),
    ("dup-forgery-4row+no-clause4", [(DUP, '    rows[1] = ["R46-CL2", "a duplicate trigger cell", "order", "1"]'),
                                     (C4, "        pass")]),
    ("noop-counts-as-crash", [(NOOP, NOOP.replace('out["v2_green"] += 1', 'out["crash"] += 1'))]),
    ("noop-counts-as-crash+allnoop", [(NOOP, NOOP.replace('out["v2_green"] += 1', 'out["crash"] += 1')),
                                      (ALLNOOP, 'MUTATIONS = [("substring-arm", lambda b, s: (b, {})),\n'
                                                '             ("duplicate-routed-id", lambda b, s: (b, {})),\n'
                                                '             ("stale-mutations-digest", lambda b, s: (b, {})),\n'
                                                '             ("flag-order-drift", lambda b, s: (b, {}))]')]),
]


def run(mod, args):
    p = subprocess.run([sys.executable, "-I", "-B", mod, *args], capture_output=True,
                       text=True, env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    return p.returncode, p.stdout + p.stderr


def probe(name, src):
    d = os.path.join(S, "abl3", name, "tools")
    os.makedirs(os.path.join(d, "round-47"), exist_ok=True)
    os.makedirs(os.path.join(d, "round-46"), exist_ok=True)
    mod = os.path.join(d, "round-47", "exact.py")
    open(mod, "w").write(src)
    shutil.copy(GATE, os.path.join(d, "round-46", "gate.py"))
    st = run(mod, ["--root", LANE, "--freeze", FREEZE, "--rev", "09a9f912f4a639b91bce7dcd3711d8f391969d4f", "--selftest"])
    cn = run(mod, ["--root", LANE, "--freeze", FREEZE, "--rev", "09a9f912f4a639b91bce7dcd3711d8f391969d4f"])
    rec = {"selftest_exit": st[0], "counter_exit": cn[0]}
    try:
        sel = json.loads(st[1].split("\n", 1)[1])
        rec["selftest_failed"] = [c["case"] for c in sel["cases"] if not c["ok"]]
    except Exception:
        rec["selftest_raw"] = st[1][:160]
    try:
        got = json.loads(cn[1])
        bat = got.get("battery") or {}
        rec.update({"met": got.get("met_target"), "failing": got.get("failing"),
                    "v2_green": bat.get("v2_green"), "v3_green": bat.get("v3_green"),
                    "forgeries": bat.get("forgeries_total"), "crash": bat.get("crash"),
                    "fixtures": [(f["name"], f.get("v2_exit"), f.get("v3_exit"),
                                  f.get("error") or (f.get("v3_failing") or [None])[0])
                                 for f in bat.get("fixtures", [])]})
    except Exception:
        rec["raw"] = cn[1][:200]
    return rec


def main():
    src0 = open(BASE).read()
    out = {"baseline": probe("baseline", src0)}
    for name, patches in CASES:
        s = src0
        bad = [o for o, _ in patches if o not in s]
        if bad:
            out[name] = {"error": "anchor not found", "anchors": bad}
            continue
        for old, new in patches:
            s = s.replace(old, new, 1)
        out[name] = probe(name, s)
    print(json.dumps(out, indent=1))


main()
