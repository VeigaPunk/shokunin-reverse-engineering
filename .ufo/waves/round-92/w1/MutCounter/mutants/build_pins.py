#!/usr/bin/env python3
"""Build the pinned carrier table for the MutCounter mutants (scratch only).

Packs each frozen carrier with the same pinned packer and the same layout
functions the frozen counters use, then writes:
  .ufo/mut/pinned/<cid>.bin     pristine packed image (upx --best)
  .ufo/mut/pinned/table.json    {cid: {packed_sha256, window, pristine, length}}
`window` is the file offset of the last block's sz_cpr (the 4-byte field the
frozen counters tamper with); `pristine` is its stored value.
Imports the frozen v2 instrument from the clone (ROOT derived from this path).
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v2 = _load(os.path.join(ROOT, "tools/round-92/stop-boundary-battery-v2.py"), "v2")
work = sys.argv[1]
os.makedirs(work, exist_ok=True)
env = v2.env_for(work)
rep = _load(os.path.join(ROOT, v2.R87), "r87")
r88 = _load(os.path.join(ROOT, v2.R88), "r88")
os.makedirs(os.path.join(HERE, "pinned"), exist_ok=True)
table = {}
for cid, src, pin in v2.CARRIERS:
    assert v2.sha256_file(src) == pin, cid
    packed = v2.pack(src, work, env)
    _b0, blocks = v2.layout(packed, rep, r88)
    last = blocks[-1]
    with open(os.path.join(HERE, "pinned", cid + ".bin"), "wb") as fh:
        fh.write(packed)
    table[cid] = {"packed_sha256": v2.sha256_bytes(packed),
                  "window": last["block"] + 4, "pristine": last["sz_cpr"],
                  "length": len(packed), "blocks": len(blocks)}
with open(os.path.join(HERE, "pinned", "table.json"), "w", encoding="utf-8") as fh:
    json.dump(table, fh, indent=1, sort_keys=True)
print(json.dumps(table, indent=1, sort_keys=True))
