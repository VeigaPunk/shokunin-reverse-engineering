#!/usr/bin/env python3
"""fresh-source2-check.py - the held-out arm's second fresh source, measured (S321).

Round 93 carried the limit "the fresh-pack arm has one source (/usr/bin/env)". This check
measures a SECOND packable little-endian x86-64 ELF (`--source`, default /usr/bin/printf,
sha-pinned) through the same chain the round-92/93 battery uses, by importing the round-92
battery-v2 helpers (pack, layout, invoke, env_for) - the frozen v3 verdict code and its
FRESH_SOURCES pin are untouched:

  1. pack the source twice with `upx --best`; both packed images must be byte-identical
     (determinism) and must not collide with any public carrier's packed bytes;
  2. intact control: the repair on the pristine packed image returns it byte-identical;
  3. near cells: the last block's `sz_cpr` moved by the round-92 deltas is repaired
     (output == pristine packed bytes);
  4. far cells: the same block moved by the round-92 far deltas is refused.

This is a supplementary measurement: it is NOT part of the R96-C1 frozen label and proves
source diversity of the held-out arm, not a new repair capability. Exit 0 iff every class
above holds on this source.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/round-96/fresh-source2-check.py"
V2 = os.path.join(HERE, "..", "round-92", "stop-boundary-battery-v2.py")
DEFAULT_SOURCE = "/usr/bin/printf"
DEFAULT_SOURCE_SHA = "b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7"
DEFAULT_REPAIR = "tools/round-92/upx-stop-boundary-search-repair.py"
FAR_DELTAS = (-40, 40)


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v2 = _load(V2, "fresh_source2_v2")
battery92 = _load(os.path.join(HERE, "..", "round-92", "stop-boundary-repair-battery.py"),
                  "fresh_source2_b92")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    ap.add_argument("--source-sha", default=DEFAULT_SOURCE_SHA)
    ap.add_argument("--repair-cmd", default=DEFAULT_REPAIR)
    ap.add_argument("--work", required=True)
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--json-out")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    os.makedirs(os.path.abspath(args.work), exist_ok=True)
    rec = {"tool": TOOL, "source": args.source, "source_sha256": args.source_sha,
           "revision": args.rev}
    if v2.sha256_file(args.source) != args.source_sha:
        rec["unevaluable"] = "fresh source sha256 drift"
        rec["exit"] = 2
        rendered = json.dumps(rec, indent=1, sort_keys=True)
        print(rendered)
        return 2
    env = v2.env_for(args.work)
    repair = os.path.join(root, args.repair_cmd)
    rep = _load(os.path.join(root, v2.R87), "fs2_r87")
    r88 = _load(os.path.join(root, v2.R88), "fs2_r88")

    src_path = os.path.join(args.work, "fresh-src2.bin")
    with open(args.source, "rb") as fh:
        data = fh.read()
    with open(src_path, "wb") as fh:
        fh.write(data)
    packed1 = v2.pack(src_path, args.work, env)
    packed2 = v2.pack(src_path, args.work, env)
    packed1, packed2 = bytes(packed1), bytes(packed2)
    rec["packed_sha256"] = v2.sha256_bytes(packed1)
    rec["deterministic"] = packed1 == packed2
    public_shas = {v2.sha256_bytes(v2.pack(src, args.work, env))
                   for _, src, _ in v2.CARRIERS}
    rec["collides_public_packed"] = rec["packed_sha256"] in public_shas

    rec0, blocks = v2.layout(packed1, rep, r88)
    rec["blocks"] = len(blocks)
    last = blocks[-1] if blocks else None

    intact = v2.invoke(repair, packed1, env, args.work)
    rec["intact_identity"] = intact.get("rc") == 0 and intact.get("output") == packed1

    cells = []
    for kind, deltas in (("near", v2.DIRECTIONS), ("far", FAR_DELTAS)):
        for delta in deltas:
            value = last["sz_cpr"] + delta
            if not (0 < value <= last["sz_unc"]):
                cells.append({"kind": kind, "delta": delta, "class": "out-of-range"})
                continue
            t = bytearray(packed1)
            struct.pack_into("<I", t, last["block"] + 4, value)
            row = battery92.score_cell(repair, bytes(t), last, packed1, env,
                                       args.work)
            row.update({"kind": kind, "delta": delta})
            cells.append(row)
    rec["cells"] = cells
    near = [c for c in cells if c["kind"] == "near" and c.get("class") != "out-of-range"]
    far = [c for c in cells if c["kind"] == "far" and c.get("class") != "out-of-range"]
    repaired = sum(1 for c in near if c["class"] == "repaired")
    far_refused = sum(1 for c in far if c["class"] == "refused")
    ok = (rec["deterministic"] and not rec["collides_public_packed"]
          and rec["intact_identity"] and len(near) == len(v2.DIRECTIONS)
          and repaired == len(near) and len(far) == len(FAR_DELTAS)
          and far_refused == len(far))
    rec["counts"] = {"near": len(near), "repaired": repaired,
                     "far": len(far), "far_refused": far_refused}
    rec["label"] = ("fresh-source2 repaired %d of %d; far-refused %d of %d; "
                    "intact %s"
                    % (repaired, len(near), far_refused, len(far),
                       "1 of 1" if rec["intact_identity"] else "0 of 1"))
    rec["met_target"] = ok
    rec["exit"] = 0 if ok else 1
    rendered = json.dumps(rec, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(rendered + "\n")
    print(rendered)
    print(rec["label"], "met", ok, "exit", rec["exit"])
    return rec["exit"]


if __name__ == "__main__":
    raise SystemExit(main())
