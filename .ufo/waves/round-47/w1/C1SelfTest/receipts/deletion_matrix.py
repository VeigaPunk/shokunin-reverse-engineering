#!/usr/bin/env python3
"""R47 C1SelfTest — clause-deletion matrix over the frozen exact.py selftest.

For each clause: copy tools/round-47/exact.py into a mirrored scratch tree
(<S>/<slug>/tools/round-47/exact.py + <S>/<slug>/tools/round-46/gate.py), delete exactly
that clause, run the copy's own --selftest, and record the banner, the exit code, the
stdout sha256 and the UTC time.  A clause whose deletion leaves `failures=0` has no case
that notices it.

The frozen bytes are never modified.  Mirrored trees are left in place so
liveness_probes.py can load them.

Usage: HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/C1SelfTest \
       python3 -B deletion_matrix.py <lane-root> <scratch> <out.json>
"""
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

LANE, S, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
SRC = open(os.path.join(LANE, "tools/round-47/exact.py")).read()
GATE = open(os.path.join(LANE, "tools/round-46/gate.py")).read()

# (slug, clause, old, new).  `new` is "" only where the surrounding block stays non-empty;
# otherwise it is `pass` — a bare deletion there is an IndentationError, not a verdict.
D = [
 ("C1-marker-occurrences", "marker_occurrences != 1",
  '        if occurrences != 1:\n            failing.append(f"marker_occurrences {occurrences} != 1")\n', ''),
 ("C1-block-is-last", "marked block is the last craft block",
  '    if hard and not receipt["block_is_last"]:\n        failing.append("marker block is not the last craft block")\n', ''),
 ("C1-title-24", "block title starts with '24. '",
  '    if hard and not block.startswith("24. "):\n        failing.append("marker block title does not start with \'24. \'")\n', ''),
 ("C2-header-exact", "header == HEADER (v3 equality)",
  '        header_ok = header == HEADER\n', '        header_ok = True\n'),
 ("C3-rows-four", "rows != 4",
  '        if len(rows) != 4:\n            failing.append(f"rows {len(rows)} != 4")\n', ''),
 ("C3-four-cells", "every row has exactly four cells",
  '        if any(len(r) != 4 for r in rows):\n            failing.append("a row does not have exactly 4 cells")\n', ''),
 ("C3-exit-set", "exit cell in {0,1,2}",
  '    if bad_exit:\n        failing.append(f"exit cells outside {{0,1,2}}: {len(bad_exit)}")\n', ''),
 ("C4-one-id-per-row", "each row names exactly one routed id",
  '        multi = [n for n, ids in enumerate(per_row) if len(ids) != 1]\n        if multi:\n            failing.append(f"rows naming != 1 routed id: {multi}")\n', ''),
 ("C4-cardinality", "routed id multiset is exactly once each",
  '        if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:\n            failing.append(f"routed cardinality {counts} != each of {ROUTED} exactly once")\n', ''),
 ("C5-arm-exact", "arm cell is an exact vocabulary token",
  '        if any(a not in VOCAB for a in arm):\n            failing.append(f"arm cells not exact vocabulary tokens: {arm}")\n', '        pass\n'),
 ("C6-mutations-digest", "mutations_sha256 == MUT_DIGEST",
  '        if not m or m.group(1) != MUT_DIGEST:\n            failing.append("mutations_sha256 does not match the counter\'s own mutation list")\n', ''),
 ("C6-mutation-names", "block states all four mutation names",
  '        if unnamed:\n            failing.append(f"mutation names not stated in the block: {unnamed}")\n', ''),
 ("C7-flag-order", "gate.py flag-order clause",
  '            if n_ok != 1 or n_bad != 0:\n                failing.append(f"gate.py flag order: {n_ok} correct, {n_bad} reversed")\n', ''),
 ("C8-refs-floor", "refs >= 3",
  '    if receipt["refs"] < 3:\n        failing.append(f"refs {receipt[\'refs\']} < 3")\n', ''),
 ("C8-bad-refs", "unresolved/unvalidated citations fail",
  '    if bad_refs:\n        failing.append(f"unresolved or unvalidated citations: {len(bad_refs)}")\n', ''),
 ("C8-must-cite", "corpus/lessons/round-46.md is cited",
  '    if hard and MUST_CITE not in cited:\n        failing.append(f"does not cite {MUST_CITE}")\n', ''),
 ("C8-interpreter-pin", "interpreter_sha256 == bytes at rev",
  '        elif not m or m.group(1) != want:\n            failing.append("interpreter sha256 pin does not match the bytes at rev")\n', ''),
 ("C8-line-selector", "every non-self reference carries a line selector",
  '        if hard and not first:\n            bad.append(f"{name}: no line selector")\n            continue\n', ''),
 ("C8-allowlist", "reference path inside ALLOW",
  '        if not name.startswith(ALLOW):\n            bad.append(f"{name}: outside the validated path set")\n            continue\n', ''),
 ("C9-battery-counts", "battery.forgeries_total==4, v2_green==4, v3_green==0, genuine_green==1, crash==0",
  '        for key, want in (("forgeries_total", 4), ("v2_green", 4), ("v3_green", 0),\n                          ("genuine_green", 1), ("crash", 0)):\n            if battery.get(key) != want:\n                failing.append(f"battery {key} {battery.get(key)} != {want}")\n', ''),
 ("Z-malformed-branch", "craft heading without its trailing space is named",
  '        if MALFORMED in skill:\n            raise Malformed("craft heading lacks its trailing space")\n', '        pass\n'),
]

env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
rows = []
for slug, clause, old, new in D:
    n = SRC.count(old)
    if n != 1:
        rows.append({"slug": slug, "clause": clause, "status": f"OLD_STRING_COUNT={n}"})
        continue
    root = os.path.join(S, slug)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "tools/round-47"))
    os.makedirs(os.path.join(root, "tools/round-46"))
    open(os.path.join(root, "tools/round-47/exact.py"), "w").write(SRC.replace(old, new, 1))
    open(os.path.join(root, "tools/round-46/gate.py"), "w").write(GATE)
    t0 = time.time()
    p = subprocess.run([sys.executable, "-I", "-B", os.path.join(root, "tools/round-47/exact.py"),
                        "--selftest", "--root", LANE, "--freeze", FREEZE, "--rev", FREEZE],
                       capture_output=True, text=True, env=env, cwd=S)
    out = p.stdout
    j = out.find("{")
    try:
        payload = json.loads(out[j:]) if j >= 0 else {"cases": []}
    except ValueError:
        payload = {"cases": []}
    flipped = [c["case"] for c in payload.get("cases", []) if not c["ok"]]
    rows.append({"slug": slug, "clause": clause, "exit": p.returncode,
                 "banner": (out.splitlines() or [None])[0],
                 "flipped_cases": flipped, "registered": len(payload.get("cases", [])),
                 "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
                 "stderr_tail": (p.stderr.strip().splitlines() or [None])[-1],
                 "utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "elapsed_s": round(time.time() - t0, 1)})
    print(f"{slug:22s} exit={p.returncode} {(rows[-1]['banner'] or ''):42s} flipped={flipped or 'NONE'}")

json.dump({"driver": os.path.abspath(__file__),
           "driver_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
           "frozen_exact_sha256": hashlib.sha256(SRC.encode()).hexdigest(),
           "frozen_gate_sha256": hashlib.sha256(GATE.encode()).hexdigest(),
           "clauses_tested": len(D), "rows": rows}, open(OUT, "w"), indent=1)
unnoticed = [r["slug"] for r in rows if r.get("flipped_cases") == [] and r.get("exit") == 0]
print("deletion-unnoticed clauses: %d/%d %s" % (len(unnoticed), len(D), unnoticed))
