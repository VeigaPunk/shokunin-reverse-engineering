#!/usr/bin/env python3
"""Locate each quote in its committed source copy within the stated line range.

Whitespace-normalised substring test over the joined lines [start, end] (1-based,
inclusive). Exit 0 = every quote located; 1 = at least one quote not located;
2 = could not evaluate (missing file or bad input).
"""
import sys, pathlib, re, json

BASE = pathlib.Path(__file__).resolve().parent.parent.parent / "sources"
CASES = [
    # (file, start, end, word_count_claimed, quote)
    ("AVM-BE-format.txt", 1, 2, "a non-standard SquashFS format (called AVM-BE below) used by AVM since Fritz!OS Labor 6.35", None),
    ("AVM-BE-format.txt", 4, 7, "it uses the big-endian layout for most of the data stored in the SquashFS image", None),
    ("AVM-BE-format.txt", 8, 9, "the only data field stored in the little-endian format is the block length value at the beginning of each block", None),
    ("AVM-BE-format.txt", 10, 10, "compression method is hardcoded to be XZ", None),
    ("AVM-BE-format.txt", 13, 14, "super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value as the super-block field 'bytes_used'", None),
    ("101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch", 7, 8, "+#define AVM_LE 2", None),
    ("101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch", 17, 18, "+#if   defined(TARGET_FORMAT) && (TARGET_FORMAT == SQUASHFS4_LE || TARGET_FORMAT == AVM_LE)", None),
    ("550-mkfs_time__AVM_BE_AVM_LE.patch", 7, 9, "+#if (TARGET_FORMAT == AVM_BE || TARGET_FORMAT == AVM_LE)", None),
    ("550-mkfs_time__AVM_BE_AVM_LE.patch", 25, 27, "if (sBlk.s.s_major == 4 && sBlk.s.mkfs_time == (int)sBlk.s.bytes_used) {", None),
    ("550-mkfs_time__AVM_BE_AVM_LE.patch", 27, 28, "mkfs_str = \"is not available because of modified AVM-format (mkfs_time == bytes_used)\\n\";", None),
    ("squashfs4-host-be.mk", 33, 33, "EXTRA_CFLAGS=\"-DTARGET_FORMAT=AVM_BE\"", None),
    ("350-unsquashfs__AVM_BE.patch", 33, 35, "block length in AVM-BE format is stored in LE order", None),
]

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def main():
    results = []
    try:
        for fname, a, b, quote, _ in CASES:
            lines = (BASE / fname).read_text(encoding="utf-8").splitlines()
            window = norm(" ".join(lines[a - 1:b]))
            ok = norm(quote) in window
            results.append({"file": fname, "lines": [a, b], "quote": quote, "located": ok})
    except (OSError, IndexError) as e:
        print(f"QUOTE_CHECK could-not-evaluate: {e}", file=sys.stderr)
        return 2
    print(json.dumps(results, indent=1, ensure_ascii=False))
    bad = [r for r in results if not r["located"]]
    print(f"QUOTE_CHECK located={len(results)-len(bad)} missing={len(bad)}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
