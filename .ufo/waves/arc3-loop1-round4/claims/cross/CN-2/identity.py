#!/usr/bin/env python3
"""CN-2 identity re-derivation (rule #14) — arc3-loop1-round4.

Prints sha256 + line/byte counts for every artifact in this seat's tree, plus
the fold sources it consumed. The receipt file itself is excluded from its own
list by construction (it records identities; it never records its own).
"""
import hashlib, pathlib, sys

BASE = pathlib.Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
CN2 = BASE / ".ufo/waves/arc3-loop1-round4/claims/cross/CN-2"
OUTLINE = BASE / ".ufo/waves/arc3-loop1-round4/claims/cross/records-outline.md"
SOURCES = [
    BASE / ".ufo/waves/arc3-loop1-round4/claims/c1/records-drafts/records-drafts.md",
    BASE / ".ufo/waves/arc3-loop1-round4/claims/c2/records-drafts/scorecard-section-draft.md",
    BASE / ".ufo/waves/arc3-loop1-round4/claims/c2/records-drafts/LOG-entry-draft.md",
    BASE / ".ufo/waves/arc3-loop1-round4/claims/c3/records-drafts/scorecard-section-draft.md",
    BASE / ".ufo/waves/arc3-loop1-round4/claims/c3/records-drafts/LOG-entry-draft.md",
]

files = [OUTLINE] + sorted(p for p in CN2.rglob("*") if p.is_file() and p.name != "identity.txt")
print("== CN-2 artifact identities (rule #14) ==")
for p in files:
    data = p.read_bytes()
    print("sha256=%s  lines=%d  bytes=%d  %s" % (
        hashlib.sha256(data).hexdigest(), data.count(b"\n"), len(data),
        p.relative_to(BASE)))
print("\n== fold sources consumed (a later revision voids the fold) ==")
for p in SOURCES:
    if not p.is_file():
        print("ABSENT  %s" % p.relative_to(BASE)); continue
    data = p.read_bytes()
    print("sha256=%s  lines=%d  %s" % (
        hashlib.sha256(data).hexdigest(), data.count(b"\n"), p.relative_to(BASE)))
