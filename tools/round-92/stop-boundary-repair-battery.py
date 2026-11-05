#!/usr/bin/env python3
"""stop-boundary-repair-battery.py - round-92 counter (R92-C1, coverage).

Scores a REPAIR command on the round-91 class `T7-chain-stop-boundary` (packed
UPX 5.2.0 `--best` little-endian ELF; the last block before the chain stop has
`sz_cpr` moved by -7 or +7) over the five carriers of
`tools/round-92/stop-boundary-battery-v2.py` (jq, xxd, libz, docker-init and the
unseen `/usr/bin/xz`): 10 tampered cells plus 5 intact controls.

A tampered cell is **repaired** only when the command exits 0 and its output is
byte-identical to the carrier's pristine packed bytes (the bytes `upx --best`
produced before the tamper). The classes are:

- **repaired** - rc 0 and output == the pristine packed bytes;
- **wrong**    - rc 0, output of the input's length, changed only inside the
                 4-byte window, but not equal to the pristine bytes (a silent
                 rewrite; harm, not a repair);
- **unsafe**   - rc 0 and an output that differs OUTSIDE the tampered window
                 (harm; QUALITY 176);
- **silent**   - rc 0 and output byte-identical to the input (QUALITY 167);
- **refused**  - rc != 0 and no output file (no repair, no harm);
- **other**    - anything else.

Far cells (the window's negative control): the same last block moved by -40 or
+40 (both in range) on each carrier, 10 cells. Each far cell must be **refused**
(rc != 0, no output); a far cell that is repaired, rewritten or silently passed
is not counted as far-refused.

Intact control: rc 0 with output byte-identical to the input on each carrier.

Frozen label: `repaired P of C; wrong W; unsafe U; intact I of 5; far-refused F of G`.
`met_target` requires the label to equal `--expect` exactly (`repaired 10 of 10;
wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`), C == 10, P == 10, W == 0,
U == 0, I == 5, G == 10 and F == 10, exit 0.
The receipt pins the command, this counter and the imported v2 instrument by
sha256, and every carrier's pinned and packed sha256. Scratch is `--work`.
"""

from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/round-92/stop-boundary-repair-battery.py"
V2 = os.path.join(HERE, "stop-boundary-battery-v2.py")
DEFAULT_REPAIR = "tools/round-92/upx-stop-boundary-search-repair.py"
FAR_DELTAS = (-40, 40)


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v2 = _load(V2, "stop_boundary_battery_v2")


def score_cell(repair: str, tampered: bytes, block: dict, packed: bytes, env: dict,
               work: str) -> dict:
    rec = v2.invoke(repair, tampered, env, work)
    out = rec.get("output")
    rc = rec.get("rc")
    row = {"tampered_block": block["block"], "stored_sz_cpr": block["sz_cpr"],
           "rc": rc, "box_after": rec.get("box_after"), "tail": rec.get("tail")}
    if rc == 0 and out is not None:
        lo, hi = block["block"] + 4, block["block"] + 8
        if out == packed:
            row["class"] = "repaired"
        elif len(out) != len(tampered):
            row["class"] = "unsafe"
            row["detail"] = f"length {len(out)} != {len(tampered)}"
        elif out == tampered:
            row["class"] = "silent"
        else:
            outside = [i for i, (a, b) in enumerate(zip(tampered, out))
                       if a != b and not (lo <= i < hi)]
            row["class"] = "unsafe" if outside else "wrong"
            if outside:
                row["outside_window"] = outside[:8]
    elif rc not in (0, None) and out is None:
        row["class"] = "refused"
    else:
        row["class"] = "other"
    return row


def score(args) -> tuple:
    root = os.path.abspath(args.root)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    env = v2.env_for(work)
    repair = os.path.join(root, args.repair_cmd)
    if not os.path.isfile(repair):
        return 2, {"tool": TOOL, "unevaluable": f"no repair command at {args.repair_cmd}"}
    if v2.sha256_file(v2.UPX) != v2.UPX_SHA256:
        return 2, {"tool": TOOL, "unevaluable": "packer sha256 drift"}
    rep = _load(os.path.join(root, v2.R87), "r87")
    r88 = _load(os.path.join(root, v2.R88), "r88")
    cells, intact, carriers = [], [], {}
    for cid, src, pin in v2.CARRIERS:
        if v2.sha256_file(src) != pin:
            return 2, {"tool": TOOL, "unevaluable": f"carrier pin drift: {cid}"}
        packed = v2.pack(src, work, env)
        b0, blocks = v2.layout(packed, rep, r88)
        carriers[cid] = {"source_sha256": pin, "packed_sha256": v2.sha256_bytes(packed),
                         "blocks": len(blocks)}
        if not blocks:
            return 2, {"tool": TOOL, "unevaluable": f"no walkable chain: {cid}"}
        rec = v2.invoke(repair, packed, env, work)
        same = rec.get("rc") == 0 and rec.get("output") == packed
        intact.append({"carrier": cid, "rc": rec.get("rc"), "identity": same,
                       "box_after": rec.get("box_after")})
        last = blocks[-1]
        for kind, deltas in (("near", v2.DIRECTIONS), ("far", FAR_DELTAS)):
            for delta in deltas:
                value = last["sz_cpr"] + delta
                if not (0 < value <= last["sz_unc"]):
                    cells.append({"carrier": cid, "kind": kind, "delta": delta,
                                  "class": "out-of-range"})
                    continue
                t = bytearray(packed)
                struct.pack_into("<I", t, last["block"] + 4, value)
                row = score_cell(repair, bytes(t), last, packed, env, work)
                row.update({"carrier": cid, "kind": kind, "delta": delta,
                            "stored": last["sz_cpr"], "value": value,
                            "block_index": len(blocks) - 1})
                cells.append(row)
    all_cells = [c for c in cells if c.get("class") != "out-of-range"]
    far = [c for c in all_cells if c["kind"] == "far"]
    far_refused = sum(1 for c in far if c["class"] == "refused")
    scored = [c for c in all_cells if c["kind"] == "near"]
    repaired = sum(1 for c in scored if c["class"] == "repaired")
    wrong = sum(1 for c in scored if c["class"] == "wrong")
    unsafe = sum(1 for c in scored if c["class"] == "unsafe")
    refused = sum(1 for c in scored if c["class"] == "refused")
    silent = sum(1 for c in scored if c["class"] == "silent")
    intact_ok = sum(1 for i in intact if i["identity"])
    label = (f"repaired {repaired} of {len(scored)}; wrong {wrong}; unsafe {unsafe}; "
             f"intact {intact_ok} of {len(intact)}; far-refused {far_refused} of {len(far)}")
    met = (label == args.expect and len(scored) == 10 and repaired == 10 and wrong == 0
           and unsafe == 0 and intact_ok == 5 and len(far) == 10 and far_refused == 10)
    return (0 if met else 1), {
        "tool": TOOL, "class": "T7-chain-stop-boundary", "repair": args.repair_cmd,
        "repair_sha256": v2.sha256_file(repair),
        "counter_sha256": v2.sha256_file(os.path.join(root, TOOL)),
        "instrument_v2_sha256": v2.sha256_file(V2),
        "revision": args.rev, "cells": cells, "intact": intact, "carriers": carriers,
        "counts": {"scored": len(scored), "repaired": repaired, "wrong": wrong,
                   "unsafe": unsafe, "refused": refused, "silent": silent,
                   "intact": intact_ok, "far": len(far), "far_refused": far_refused},
        "expect": args.expect, "label": label, "met_target": met,
        "exit": 0 if met else 1,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--repair-cmd", default=DEFAULT_REPAIR)
    ap.add_argument("--work", required=True)
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--expect", required=True,
                    help="frozen label: 'repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10'")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    code, receipt = score(args)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(receipt.get("label", receipt.get("unevaluable")), "met", receipt.get("met_target"),
          "exit", code)
    return code


if __name__ == "__main__":
    sys.exit(main())
