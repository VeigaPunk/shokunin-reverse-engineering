#!/usr/bin/env python3
"""fixture-repair.py -- the smallest repair for the S126 defect, applied to a THROWAWAY clone.

Brings the three own-work bodies the S126 row pins into the lane at
`corpus/evidence/round-11/avm-be/` and repoints the row and the knowledge lineage at them.
Byte-exactness is asserted against the digests the row already carries, so the repair cannot
"succeed" by substituting a stub.

usage: fixture-repair.py --lane <clone> --source <dir holding the three bodies>
exit: 0 repaired and all three digests agree with the row pins; 1 digest disagreement; 2 usage/IO.
"""

import argparse
import hashlib
import os
import re
import shutil
import sys

BODIES = [
    ("lead1-avm-image.tsv", "f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0"),
    ("avm-be.squashfs", "c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32"),
    ("unblob.log", "352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7"),
]
DEST_REL = "corpus/evidence/round-11/avm-be"

OLD_PATHS = [
    "/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv",
    "/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs",
]
KNOWLEDGE = "corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--source", required=True)
    a = ap.parse_args()

    dest_dir = os.path.join(a.lane, DEST_REL)
    os.makedirs(dest_dir, exist_ok=True)
    bad = 0
    for name, want in BODIES:
        src = os.path.join(a.source, name)
        if not os.path.isfile(src):
            print("repair: missing body %s" % src, file=sys.stderr)
            return 2
        got = sha256(src)
        if got != want:
            print("repair: %s digest %s != pin %s" % (name, got, want), file=sys.stderr)
            bad += 1
        shutil.copyfile(src, os.path.join(dest_dir, name))
    if bad:
        return 1

    src_md = os.path.join(a.lane, "corpus", "SOURCES.md")
    with open(src_md, "r", encoding="utf-8") as fh:
        text = fh.read()
    if not all(p in text for p in OLD_PATHS):
        print("repair: expected host-local pointers absent (already repaired?)", file=sys.stderr)
        return 1
    for p in OLD_PATHS:
        text = text.replace(p, "%s/%s" % (DEST_REL, os.path.basename(p)))
    text = text.replace("run log `unblob.log`", "run log `%s/unblob.log`" % DEST_REL)
    with open(src_md, "w", encoding="utf-8") as fh:
        fh.write(text)

    kp = os.path.join(a.lane, KNOWLEDGE)
    with open(kp, "r", encoding="utf-8") as fh:
        ktext = fh.read()
    for p in OLD_PATHS:
        ktext = ktext.replace(p, "%s/%s" % (DEST_REL, os.path.basename(p)))
    with open(kp, "w", encoding="utf-8") as fh:
        fh.write(ktext)

    rows = re.findall(r"^\|\s*S126\s*\|.*$", text, re.M)
    print("repair: bodies copied to %s; S126 rows rewritten=%d" % (DEST_REL, len(rows)))
    for name, want in BODIES:
        print("repair: %-20s %s" % (name, sha256(os.path.join(dest_dir, name))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
