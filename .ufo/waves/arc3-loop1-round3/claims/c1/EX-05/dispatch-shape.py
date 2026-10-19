#!/usr/bin/env python3
"""dispatch-shape.py — classify an EVM runtime's selector-dispatch shape.

Seat EX-05 (chain c1, round 3). Cross-round comparison helper: the r1 knowledge
entry records dispatcher prologue classes `5f3560e01c` / `60003560e01c`; this
script reports, per runtime hex, the prologue bytes and how the selector
comparisons are shaped, so optimizer-enabled shapes can be compared against the
r1 recorded classes with a repeatable reading rather than an eyeball.

Readings (hex-string pattern counts over the whole blob, plus the head window):
  prologue          : first 24 bytes
  lowcalldata_guard : `60043610` (PUSH1 4; CALLDATASIZE; LT) — calldatasize<4 guard
  shift_idiom       : `5f3560e01c` (PUSH0; CALLDATALOAD; PUSH1 0xe0; SHR)
  legacy_idiom      : `60003560e01c` (PUSH1 0; CALLDATALOAD; PUSH1 0xe0; SHR)
  eq_dispatch       : `63<sel>1461<dest>57` — DUP1 PUSH4 sel EQ PUSH2 dest JUMPI
  gt_dispatch       : `63<sel>1161<dest>57` — DUP1 PUSH4 sel GT PUSH2 dest JUMPI (binary search)
  lt_dispatch       : `63<sel>1061<dest>57` — DUP1 PUSH4 sel LT PUSH2 dest JUMPI (binary search)

usage: python3 dispatch-shape.py <runtime.hex> [...more.hex] [--json]
"""
import json
import re
import sys

EQ = re.compile(r"63([0-9a-f]{8})14(60[0-9a-f]{2}|61[0-9a-f]{4})57")
GT = re.compile(r"63([0-9a-f]{8})11(60[0-9a-f]{2}|61[0-9a-f]{4})57")
LT = re.compile(r"63([0-9a-f]{8})10(60[0-9a-f]{2}|61[0-9a-f]{4})57")


def classify(path: str):
    h = open(path).read().strip().replace("0x", "").lower()
    out = {
        "file": path,
        "bytes": len(h) // 2,
        "prologue_hex": h[:48],
        "lowcalldata_guard": h.count("60043610"),
        "shift_idiom_5f3560e01c": h.count("5f3560e01c"),
        "legacy_idiom_60003560e01c": h.count("60003560e01c"),
        "eq_dispatch": [(m.group(1), int(m.group(2), 16)) for m in EQ.finditer(h)],
        "gt_dispatch": [(m.group(1), int(m.group(2), 16)) for m in GT.finditer(h)],
        "lt_dispatch": [(m.group(1), int(m.group(2), 16)) for m in LT.finditer(h)],
        "dest_widths": sorted({len(m.group(2)) for m in EQ.finditer(h)} | {len(m.group(2)) for m in GT.finditer(h)}),
        "push4_distinct": sorted({m.group(1) for m in re.finditer(r"63([0-9a-f]{8})", h)}),
    }
    out["shape"] = (
        "linear-eq" if len(out["eq_dispatch"]) >= 2 and not out["gt_dispatch"] and not out["lt_dispatch"]
        else "binary-search-gt" if out["gt_dispatch"] and not out["eq_dispatch"] and not out["lt_dispatch"]
        else "mixed" if out["eq_dispatch"] or out["gt_dispatch"] or out["lt_dispatch"]
        else "none-detected"
    )
    return out


if __name__ == "__main__":
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    res = [classify(p) for p in paths]
    if "--json" in sys.argv:
        print(json.dumps(res, indent=2))
    else:
        for r in res:
            print(f"{r['file']}\n  bytes={r['bytes']} shape={r['shape']} prologue={r['prologue_hex'][:40]}")
            print(f"  lowcalldata_guard={r['lowcalldata_guard']} 5f3560e01c={r['shift_idiom_5f3560e01c']} 60003560e01c={r['legacy_idiom_60003560e01c']}")
            print(f"  eq={len(r['eq_dispatch'])} gt={len(r['gt_dispatch'])} lt={len(r['lt_dispatch'])} push4_distinct={len(r['push4_distinct'])}")