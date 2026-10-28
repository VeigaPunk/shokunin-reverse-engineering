#!/usr/bin/env python3
"""Ablation driver v2: one check at a time, replaced by a no-op, then
(a) the module's own --selftest and (b) the real counter at HEAD are re-run.
A cut whose removal leaves both green is a check with no failing case.
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

CUTS = [
    ("c1-marker-count",
     '        if occurrences != 1:\n            failing.append(f"marker_occurrences {occurrences} != 1")',
     "        pass"),
    ("c1-block-last",
     '    if hard and not receipt["block_is_last"]:\n        failing.append("marker block is not the last craft block")',
     "    pass"),
    ("c1-title-numbered",
     "    if hard and not block.startswith(\"24. \"):\n        failing.append(\"marker block title does not start with '24. '\")",
     "    pass"),
    ("c2-header-exact",
     "    if hard:\n        header_ok = header == HEADER\n    else:",
     "    if hard:\n        header_ok = True\n    else:"),
    ("c3-rows-four",
     '        if len(rows) != 4:\n            failing.append(f"rows {len(rows)} != 4")\n        if any(len(r) != 4 for r in rows):\n            failing.append("a row does not have exactly 4 cells")',
     "        pass"),
    ("c3-exit-cells", "    if bad_exit:\n        failing.append", "    if False:\n        failing.append"),
    ("c4-v3-cardinality",
     '        multi = [n for n, ids in enumerate(per_row) if len(ids) != 1]\n        if multi:\n            failing.append(f"rows naming != 1 routed id: {multi}")\n        if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:\n            failing.append(f"routed cardinality {counts} != each of {ROUTED} exactly once")',
     "        pass"),
    ("c4-v2-any-row",
     "        missing = [i for i in ROUTED if i not in counts]\n        if missing:\n            failing.append(f\"routed ids not named by any row: {missing}\")",
     "        pass"),
    ("c5-v3-arm-exact",
     "        if any(a not in VOCAB for a in arm):\n            failing.append(f\"arm cells not exact vocabulary tokens: {arm}\")",
     "        pass"),
    ("c5-v2-arm-substring",
     "        if any(not any(t in a.lower() for t in VOCAB) for a in arm):\n            failing.append(\"arm cells outside the vocabulary\")",
     "        pass"),
    ("c6-digest-equality",
     "        if not m or m.group(1) != MUT_DIGEST:\n            failing.append(\"mutations_sha256 does not match the counter's own mutation list\")",
     "        pass"),
    ("c6-mutation-names",
     "        unnamed = [n for n in names if n not in block]\n        if unnamed:\n            failing.append(f\"mutation names not stated in the block: {unnamed}\")",
     "        pass"),
    ("c7-flag-order",
     "            if n_ok != 1 or n_bad != 0:\n                failing.append(f\"gate.py flag order: {n_ok} correct, {n_bad} reversed\")",
     "            pass"),
    ("c8-refs-count",
     '    if receipt["refs"] < 3:\n        failing.append(f"refs {receipt[\'refs\']} < 3")',
     "    pass"),
    ("c8-self-exemption",
     "        if name == SELF:\n            continue  # identified by its own sha256 pin, not by a line selector",
     "        pass"),
    ("c8-must-cite",
     "    if hard and MUST_CITE not in cited:\n        failing.append(f\"does not cite {MUST_CITE}\")",
     "    pass"),
    ("c8-range-in-bounds",
     "        if not (1 <= start <= end <= count):\n            bad.append(f\"{name}:{start}-{end} outside 1..{count}\")",
     "        pass"),
    ("c8-selector-required",
     "        if hard and not first:\n            bad.append(f\"{name}: no line selector\")\n            continue",
     "        pass"),
    ("c8-allowlist",
     "        if not name.startswith(ALLOW):\n            bad.append(f\"{name}: outside the validated path set\")\n            continue",
     "        pass"),
    ("c8-interpreter-pin",
     '        if want is None:\n            failing.append("interpreter absent at rev")\n        elif not m or m.group(1) != want:\n            failing.append("interpreter sha256 pin does not match the bytes at rev")',
     "        pass"),
    ("c8-dangling-ref",
     "        if count is None:\n            bad.append(f\"{name}: absent at rev\")\n            continue",
     "        pass"),
    ("battery-clause9",
     '        for key, want in (("forgeries_total", 4), ("v2_green", 4), ("v3_green", 0),\n                          ("genuine_green", 1), ("crash", 0)):\n            if battery.get(key) != want:\n                failing.append(f"battery {key} {battery.get(key)} != {want}")',
     "        pass"),
    ("receipt-block-fields",
     '    receipt.update({"block_is_last": blocks[-1] is block,\n                    "block_title": block.split("**", 1)[0][:24],\n                    "header": header, "rows": len(rows)})',
     "    receipt.update({})"),
    ("mutation-substring-is-noop",
     'def _m_substring_arm(block, spec):\n    rows = [r[:2] + ["order-ish"] + r[3:] for r in _rows(block)]\n    return rewrite_rows(block, rows), {}',
     'def _m_substring_arm(block, spec):\n    return block, {}'),
    ("all-mutations-noop",
     'MUTATIONS = [("substring-arm", _m_substring_arm),\n             ("duplicate-routed-id", _m_duplicate_id),\n             ("stale-mutations-digest", _m_stale_digest),\n             ("flag-order-drift", _m_flag_order)]',
     'MUTATIONS = [("substring-arm", lambda b, s: (b, {})),\n             ("duplicate-routed-id", lambda b, s: (b, {})),\n             ("stale-mutations-digest", lambda b, s: (b, {})),\n             ("flag-order-drift", lambda b, s: (b, {}))]'),
]


def run(mod_path, args):
    p = subprocess.run([sys.executable, "-I", "-B", mod_path, *args],
                       capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    return p.returncode, p.stdout + p.stderr


def probe(name, src):
    d = os.path.join(S, "abl2", name, "tools")
    os.makedirs(os.path.join(d, "round-47"), exist_ok=True)
    os.makedirs(os.path.join(d, "round-46"), exist_ok=True)
    mod = os.path.join(d, "round-47", "exact.py")
    open(mod, "w").write(src)
    shutil.copy(GATE, os.path.join(d, "round-46", "gate.py"))
    st = run(mod, ["--root", LANE, "--freeze", FREEZE, "--rev", "09a9f912f4a639b91bce7dcd3711d8f391969d4f", "--selftest"])
    cn = run(mod, ["--root", LANE, "--freeze", FREEZE, "--rev", "09a9f912f4a639b91bce7dcd3711d8f391969d4f"])
    rec = {"selftest_exit": st[0], "selftest_line": st[1].strip().splitlines()[0][:60]
           if st[1].strip() else "", "counter_exit": cn[0]}
    try:
        got = json.loads(cn[1])
        bat = got.get("battery") or {}
        rec.update({"met": got.get("met_target"), "failing": got.get("failing"),
                    "v2_green": bat.get("v2_green"), "v3_green": bat.get("v3_green"),
                    "forgeries": bat.get("forgeries_total"),
                    "genuine_green": bat.get("genuine_green"),
                    "noop_fixtures": [f["name"] for f in bat.get("fixtures", [])
                                      if f.get("error")]})
    except Exception:
        rec["raw"] = cn[1][:200]
    try:
        sel = json.loads(st[1].split("\n", 1)[1])
        rec["selftest_failed_cases"] = [c["case"] for c in sel["cases"] if not c["ok"]]
    except Exception:
        pass
    return rec


def main():
    src0 = open(BASE).read()
    out = {"baseline": probe("baseline", src0)}
    for name, old, new in CUTS:
        if old not in src0:
            out[name] = {"error": "anchor not found"}
            continue
        out[name] = probe(name, src0.replace(old, new, 1))
    print(json.dumps(out, indent=1))


main()
