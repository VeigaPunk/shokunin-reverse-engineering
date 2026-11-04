#!/usr/bin/env python3
"""Pure-seam probe: exercise helpers of each mutant with inputs the selftest omits."""
from __future__ import annotations

import importlib.util
import json
import os
import sys

SCRATCH = "/fast/scratch/hyaku/kaidoku-r69/MutBattery"
FROZEN = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-69/packed-elf.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location("m_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def safe(fn, *args, **kwargs):
    try:
        return {"ok": True, "value": fn(*args, **kwargs)}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "exception": f"{exc.__class__.__name__}: {exc}"}


def model(**over):
    base = {
        "upx_list_rc": 0, "section_count": 0,
        "packed_procedures": 3, "before_max_procedures": 10,
        "unpack_rc": 0, "unpacked_sha256": "aa" * 32, "pin": "aa" * 32,
        "recovered_counts": {"procedure_count": 167, "segment_count": 30, "string_count": 190},
        "orig_counts": {"procedure_count": 167, "segment_count": 30, "string_count": 190},
        "control_list_rc": 2, "control_decompress_rc": 2, "address": None,
    }
    base.update(over)
    return base


PARTIAL_HEADER = ("  Class:                             ELF64\n"
                  "  Data:                              2's complement, little endian\n"
                  "  Machine:                           Advanced Micro Devices X86-64\n")
FULL_HEADER = PARTIAL_HEADER + "  Type:                              DYN (Shared object file)\n"
SENTINEL_ONLY = "There are no sections in this file.\n"
SENTINEL_AND_ROWS = ("There are no sections in this file.\n"
                     "  [ 1] .interp PROGBITS 0000000000000318 000318 00001c 00 A 0 0 1\n")

CASES = [
    ("MB01_control_default", lambda m: m.carrier_arms(True, True, True, True, None),
     "carrier_arms(...) without control_ok"),
    ("MB02_fold_empty_control", lambda m: m.fold([], 0),
     "fold([], 0)"),
    ("MB03_fold_missing_control_arm",
     lambda m: m.fold([{"ok": True, "arms": {}}], 1),
     "fold(one carrier with no control arm)"),
    ("MB04_fold_matched_ge",
     lambda m: m.fold([{"ok": True, "arms": {"control_ok": True}}] * 4, 3),
     "fold(4 ok carriers, target 3)"),
    ("MB07_elf_format_len", lambda m: m.elf_format(PARTIAL_HEADER),
     "elf_format(3-of-4 header)"),
    ("MB07_elf_format_len", lambda m: m.elf_format(FULL_HEADER),
     "elf_format(4-of-4 header)"),
    ("MB10_section_branch_sentinel", lambda m: m.section_count(SENTINEL_ONLY),
     "section_count(sentinel only)"),
    ("MB10_section_branch_sentinel", lambda m: m.section_count(SENTINEL_AND_ROWS),
     "section_count(sentinel + section rows)"),
    ("MB12_refusal_code_floor",
     lambda m: m.evaluate_carrier(model(address="0x1000", refusal_packed_rc=1,
                                        refusal_unpacked_rc=0,
                                        refusal_symbol_present=True,
                                        refusal_code_bytes=50))["arms"]["refusal_ok"],
     "refusal_ok with 50-byte decompilation"),
    ("MB13_refusal_unpacked_rc",
     lambda m: m.evaluate_carrier(model(address="0x1000", refusal_packed_rc=1,
                                        refusal_unpacked_rc=7,
                                        refusal_symbol_present=True,
                                        refusal_code_bytes=400))["arms"]["refusal_ok"],
     "refusal_ok with unpacked decompile rc=7"),
]


def main():
    rows = []
    for mid in sorted({c[0] for c in CASES}):
        pristine = load("pristine", FROZEN)
        mutant = load(mid, os.path.join(SCRATCH, mid + "-packed-elf.py"))
        for case_id, fn, desc in CASES:
            if case_id != mid:
                continue
            rows.append({"mutant": mid, "probe": desc,
                         "pristine": safe(fn, pristine),
                         "mutant_value": safe(fn, mutant)})
    out = {"probes": rows}
    print(json.dumps(out, indent=1, sort_keys=True))
    with open(os.path.join(SCRATCH, "pure-probe.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
