#!/usr/bin/env python3
"""CU-1 (arc3-loop1-round3): cross-wave custody continuity table.

Extracts per-path sha256 (short) + inode where the receipt carries it, from the
v1/v2 receipt shapes in-tree, and prints one row per capture. Read-only.
"""
import os
import re
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PATHS = [
    "/home/vgpnk/.config/devin/mcp_config.json",
    "/home/vgpnk/.omp/agent/mcp.json",
    "/home/vgpnk/.kimi-code/config.toml",
    "/home/vgpnk/.bashrc",
    "/home/vgpnk/.profile",
]
SHORT = [os.path.basename(p) for p in PATHS]

SOURCES = [
    ("r1 CU-1 stanza-v1 (09:57:18Z)", ".ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt"),
    ("r1 CU-1 pipe-v1 (09:57:48Z)", ".ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair-metadata.txt"),
    ("r1 EX-02 pre-install (09:57Z)", ".ufo/waves/arc3-loop1-round1/claims/c1/EX-02/custody-pre-pair.txt"),
    ("r1 EX-02 post-install (09:59Z)", ".ufo/waves/arc3-loop1-round1/claims/c1/EX-02/custody-post-pair.txt"),
    ("r1 EX-26 sums-v1 (10:00:43Z)", ".ufo/waves/arc3-loop1-round1/claims/c3/EX-26/custody-sha256.txt"),
    ("r2 EX-31 v2 pre (12:04Z)", ".ufo/waves/arc3-loop1-round2/claims/c3/receipts/config-pre-pair-v2.txt"),
    ("r2 CU-1 v2 post (12:31:44Z)", ".ufo/waves/arc3-loop1-round2/claims/cross/CU-1/config-post-pair-v2.txt"),
    ("r3 EX-29 v2 pre (13:06:57Z)", ".ufo/waves/arc3-loop1-round3/claims/c2/receipts/config-pre-pair-v2r3.txt"),
    ("r3 CU-1 v2 mid (13:10Z)", ".ufo/waves/arc3-loop1-round3/claims/cross/CU-1/cu1-mid1-capture.txt"),
]


def extract(text):
    """Return {path: (sha_short, inode_or_None)} across the v1/v2 shapes."""
    out = {}
    # v2 stanzas: PATH: ... then SHA256: / INODE:
    cur = None
    for line in text.splitlines():
        if line.startswith("PATH: "):
            cur = line[6:].strip()
            out.setdefault(cur, [None, None])
        elif cur and line.startswith("SHA256: "):
            out[cur][0] = line[8:].strip()[:12]
        elif cur and line.startswith("INODE: "):
            out[cur][1] = line[7:].strip()
    # sums-v1: "<sha256>  <path>"
    for m in re.finditer(r"^([0-9a-f]{64})\s+(\S+)$", text, re.M):
        p = m.group(2)
        cur_pair = out.setdefault(p, [None, None])
        cur_pair[0] = cur_pair[0] or m.group(1)[:12]
    # pipe-v1: "path | inode | ctime | mtime | size | blocks | sha256"
    for line in text.splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 7 and re.fullmatch(r"[0-9a-f]{64}", parts[6]):
            pair = out.setdefault(parts[0], [None, None])
            pair[0] = pair[0] or parts[6][:12]
            pair[1] = pair[1] or parts[1]
    return out


def main():
    print("capture | " + " | ".join(SHORT))
    rows = []
    for label, rel in SOURCES:
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            print("%s | MISSING-FILE" % label)
            continue
        with open(p, "r", encoding="utf-8", errors="replace") as fh:
            got = extract(fh.read())
        cells = []
        for full in PATHS:
            sha, ino = got.get(full, [None, None])
            if sha is None:
                cells.append("?")
            else:
                cells.append("%s%s" % (sha, "/i%s" % ino if ino else ""))
        print("%s | %s" % (label, " | ".join(cells)))
        rows.append(cells)
    # digest-change report per path
    print()
    for i, name in enumerate(SHORT):
        col = [r[i] for r in rows]
        uniq = []
        for c in col:
            base = c.split("/")[0]
            if base not in uniq:
                uniq.append(base)
        print("%-22s distinct digests across captures: %d %s" % (name, len(uniq), uniq))
    return 0


if __name__ == "__main__":
    sys.exit(main())