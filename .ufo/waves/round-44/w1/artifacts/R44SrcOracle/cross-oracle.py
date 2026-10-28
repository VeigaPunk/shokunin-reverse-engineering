#!/usr/bin/env python3
"""Cross-oracle check: unsquashfs 4.7.5 extraction digests == unblob __output__ tree digests.

Reads the frozen carrier table (tools/round-44/carriers.json) so the checked set is exactly
the frozen set: every carrier's `path` is extracted with /usr/bin/unsquashfs into a scratch
dir and compared path-for-path (sha256 + size, no extra/missing member) against that carrier's
`output_tree` under corpus/evidence/round-44/oracle/ (S138 bytes).

Read-only; exit 0 iff every carrier matches.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
CARRIERS = f"{LANE}/tools/round-44/carriers.json"


def tree(root):
    out = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            p = os.path.join(dirpath, name)
            with open(p, "rb") as f:
                b = f.read()
            out[os.path.relpath(p, root)] = (hashlib.sha256(b).hexdigest(), len(b))
    return out


def main():
    cfg = json.load(open(CARRIERS))
    ver = subprocess.run(["/usr/bin/unsquashfs", "--version"], capture_output=True, text=True)
    print("oracle:", (ver.stdout or ver.stderr).splitlines()[0], f"(exit {ver.returncode})")
    print(f"carriers: {len(cfg['carriers'])} from {os.path.relpath(CARRIERS, LANE)}")
    bad = 0
    scratch = tempfile.mkdtemp(prefix="probe-R44SrcOracle-x-")
    try:
        for c in cfg["carriers"]:
            src = os.path.join(LANE, c["path"])
            want_root = os.path.join(LANE, c["output_tree"])
            dst = os.path.join(scratch, c["id"])
            r = subprocess.run(
                ["/usr/bin/unsquashfs", "-no-progress", "-n", "-d", dst, src],
                capture_output=True, text=True,
            )
            got = tree(dst) if os.path.isdir(dst) else {}
            want = tree(want_root)
            same = got == want
            ok = same and r.returncode == 0 and len(got) == c.get("expected_regular", len(want))
            bad += 0 if ok else 1
            print(f"{'MATCH' if ok else 'FAIL '} {c['id']} {c['handler']}/{c['endian']} "
                  f"rc={r.returncode} members={len(got)} expected_regular={c.get('expected_regular')}")
            for k in sorted(set(got) | set(want)):
                if got.get(k) != want.get(k):
                    print(f"   MISMATCH {k}: unsquashfs={got.get(k)} expected={want.get(k)}")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    print(f"cross_oracle_failed_carriers={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
