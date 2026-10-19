#!/usr/bin/env python3
"""EX-21 apply recipe — SKILL.md custody-pair registry-row update (anchored, line-neutral).

Usage:  python3 apply-registry-row.py <repo-root>/SKILL.md && diff -u <orig> ... 

Base: SKILL.md sha256 c134afcb2e648aa3f8ff96f11d03aee2be6715811cb7edb3b7be6ac40aa0aa90
      (390 lines; the custody-pair row is line 390, 1-based — the ONLY line changed).
Every anchor must occur exactly once in the row; the file stays line-neutral.
The resulting patched file: 5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f
The resulting patched row:  cf5111a795a7bfee0c49534bd28307d95a8c69e64ce1bf473303e1cf9ddde14b
"""
import hashlib
import sys
from pathlib import Path

REPLACEMENTS = [
    ("the receipt self-pins the instrument's sha256 and receipt-version 2) + a `.sha256` sidecar;",
     "the receipt self-pins the instrument's sha256 and receipt-version 2) + a `.sha256` sidecar; "
     "a path that exists but cannot be evaluated is recorded with `READ-ERROR`/`STAT-ERROR`, never silently as absent;"),
    ("`verify <receipt_a> <receipt_b>` or `verify <receipt_a> --live` — ",
     "`verify <receipt_a> <receipt_b>` or `verify <receipt_a> --live` [`--require-paths <N>`] — "),
    ("13 ABSENT; 2 USAGE (bad args, unreadable or unparsable receipt, refused write)",
     "13 ABSENT, 14 UNEVALUABLE (a path exists but could not be evaluated — EACCES on open or a stat error "
     "other than ENOENT; classified before the both-absent branch, so it can never read as a fail-open MATCH); "
     "2 USAGE (bad args, unreadable or unparsable receipt, a reference below `--require-paths N` — printing "
     "`REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: <canonical paths absent from the reference>` "
     "— refused write, unusable selftest scratch base)"),
    ("precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH",
     "precedence CONTENT-DRIFT > UNEVALUABLE > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH"),
    ("capture is 0 at 5/5, else 13 with the receipt still written, and it refuses to write a receipt over a custody path;",
     "capture is 0 at 5/5, 14 when \u22651 path is present-but-unevaluable, else 13 with the receipt still written, "
     "and it refuses to write a receipt over any path it measures or a custody path (by resolved path or inode);"),
    ("with its sha256 contract intact (5/5)**",
     "with its sha256 contract intact (5/5); `--require-paths N` applies to v1 references too**"),
    ("same command with `selftest`; 15 fixture cases —",
     "same command with `selftest`; 22 fixture cases —"),
    ("unparsable → 2, refuse-to-write-over-custody-path → 2;",
     "unparsable → 2, refuse-to-write-over-custody-path → 2, unreadable-path → 14 (and a parsed unreadable receipt "
     "is never a fail-open MATCH), reference below `--require-paths` → 2, missing/unusable/`/tmp` `--scratch` → 2, "
     "`--paths X --out X` and a hardlink alias → 2;"),
    ("**normal entry writes nothing under the custody paths — files opened for reading only, never renamed, mtime never touched;",
     "**normal entry writes nothing under the custody paths — files opened for reading only, never renamed, mtime never touched; "
     "the write guard covers `set(--paths) \u222a CUSTODY_PATHS` by resolved path and inode (a self-harm guard, not a security boundary);"),
]


def main(path: str) -> int:
    skill = Path(path)
    orig = skill.read_text(encoding="utf-8")
    lines = orig.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("| custody-pair |")]
    if len(idx) != 1:
        print("REFUSE: custody-pair row not unique: %s" % idx, file=sys.stderr)
        return 1
    row = lines[idx[0]]
    for old, new in REPLACEMENTS:
        if row.count(old) != 1:
            print("REFUSE: anchor occurrence %d != 1: %r" % (row.count(old), old[:70]), file=sys.stderr)
            return 1
        row = row.replace(old, new)
    lines[idx[0]] = row
    patched = "\n".join(lines)
    if len(patched.split("\n")) != len(orig.split("\n")):
        print("REFUSE: not line-neutral", file=sys.stderr)
        return 1
    skill.write_text(patched, encoding="utf-8")
    print("patched line %d; file sha256 %s" % (idx[0] + 1, hashlib.sha256(patched.encode()).hexdigest()))
    print("row sha256 %s" % hashlib.sha256(row.encode()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "SKILL.md"))