#!/usr/bin/env python3
"""Supplementary (NOT the frozen R92-C1 label): the candidate on carriers that no table in the
round-92 battery names (bzip2, gzip, patch). A pinned-image table cannot repair these; a
packer-verdict search can. Tamper = last-block sz_cpr +/-7 (near) and +/-40 (far); oracle for
'repaired' = the pristine `upx --best` image of the same source, packed in this run.
usage: supp-unseen-carriers.py <root> <work> <out.json>"""
import hashlib, importlib.util, json, os, shutil, struct, subprocess, sys, tempfile
root, work, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3]
os.makedirs(work, exist_ok=True)
def load(p, n):
    s = importlib.util.spec_from_file_location(n, os.path.join(root, p))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
v2 = load("tools/round-92/stop-boundary-battery-v2.py", "v2")
rep = load("tools/round-87/upx-magic-repair.py", "r87")
r88 = load("tools/round-88/upx-chain-repair.py", "r88")
env = v2.env_for(work)
CAND = os.path.join(root, "tools/round-92/upx-stop-boundary-search-repair.py")
rows, ok = [], True
for name in ("bzip2", "gzip", "patch"):
    src = f"/usr/bin/{name}"
    pristine = v2.pack(src, work, env)
    b0, blocks = v2.layout(pristine, rep, r88)
    last = blocks[-1]
    cells = []
    for kind, deltas in (("near", (-7, 7)), ("far", (-40, 40))):
        for d in deltas:
            val = last["sz_cpr"] + d
            if not (0 < val <= last["sz_unc"]):
                cells.append({"kind": kind, "delta": d, "class": "out-of-range"}); continue
            t = bytearray(pristine); struct.pack_into("<I", t, last["block"] + 4, val)
            rec = v2.invoke(CAND, bytes(t), env, work)
            o = rec.get("output")
            if kind == "near":
                cls = "repaired" if (rec.get("rc") == 0 and o == pristine) else (
                      "refused" if (rec.get("rc") not in (0, None) and o is None) else "other")
            else:
                cls = "refused" if (rec.get("rc") not in (0, None) and o is None) else "other"
            cells.append({"kind": kind, "delta": d, "rc": rec.get("rc"), "class": cls})
    near = [c for c in cells if c["kind"] == "near"]
    far = [c for c in cells if c["kind"] == "far"]
    row = {"carrier": name, "source_sha256": v2.sha256_file(src),
           "pristine_packed_sha256": v2.sha256_bytes(pristine), "blocks": len(blocks),
           "near_repaired": sum(c["class"] == "repaired" for c in near), "near_cells": len(near),
           "far_refused": sum(c["class"] == "refused" for c in far), "far_cells": len(far),
           "cells": cells}
    rows.append(row)
    ok = ok and row["near_repaired"] == row["near_cells"] and row["far_refused"] == row["far_cells"]
receipt = {"tool": "tools/round-92/upx-stop-boundary-search-repair.py", "supplementary": True,
           "not_the_frozen_label": True, "carriers": rows, "all_as_expected": ok,
           "candidate_sha256": v2.sha256_file(CAND), "upx": v2.sha256_file(v2.UPX)}
json.dump(receipt, open(out, "w"), indent=1, sort_keys=True)
print("supp all_as_expected", ok, [(r["carrier"], r["near_repaired"], r["far_refused"]) for r in rows])
sys.exit(0 if ok else 1)
