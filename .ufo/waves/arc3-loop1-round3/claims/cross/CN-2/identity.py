#!/usr/bin/env python3
"""CN-2 identity re-derivation (rule #14) — prints sha256 + line counts for
every artifact in this seat's tree. The receipt is EXCLUDED from its own list by
construction (it records identities; it never records its own)."""
import hashlib, pathlib

BASE = pathlib.Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
OUTLINE = BASE / ".ufo/waves/arc3-loop1-round3/claims/cross/records-outline.md"
CN2 = BASE / ".ufo/waves/arc3-loop1-round3/claims/cross/CN-2"

files = [OUTLINE] + sorted(p for p in CN2.rglob("*") if p.is_file() and p.name != "identity.txt")
for p in files:
    data = p.read_bytes()
    print("sha256=%s  lines=%d  bytes=%d  %s" % (
        hashlib.sha256(data).hexdigest(), data.count(b"\n"), len(data),
        p.relative_to(BASE)))