#!/usr/bin/env python3
"""EX-25 extra fixture builder — the vectors added after the first matrix.

Built ONCE and pinned (the attack battery consumes them read-only, so the bytes
are identical across phases).  Uses the BEFORE revision's renderer for the
tool-produced parts.

  hardlink5-pre.txt         5 hardlink names for ONE inode (boundary of
                            "distinct path" counting)
  dupe5-bad-second-pre.txt  5 stanzas of one path, the 2nd carrying READ-ERROR
  dupe5-bad-last-pre.txt    the same, the bad stanza last
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import shutil
import sys
import time
from pathlib import Path

ROOT = Path("/var/tmp/ex25-r4")
TOOL = ROOT / "tools" / "before" / "custody-pair.py"
FIX = ROOT / "fixtures"


def load_tool(path: Path):
    spec = importlib.util.spec_from_file_location("cp_ex25b", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    cp = load_tool(TOOL)
    now = time.time()

    # ---- hardlink: 5 names, one inode ------------------------------------
    hl = FIX / "scratch" / "hl"
    if hl.exists():
        shutil.rmtree(hl)
    hl.mkdir(parents=True)
    base = hl / "hl-0"
    base.write_text("ex25 hardlink payload\n", encoding="utf-8")
    for i in range(1, 5):
        os.link(base, hl / ("hl-%d" % i))
    secs = [cp.capture_path(hl / ("hl-%d" % i)) for i in range(5)]
    text = cp.render_receipt(secs, "EX-25 hardlink-5-names (one inode)", now)
    (FIX / "hardlink5-pre.txt").write_text(text, encoding="utf-8")

    # ---- duplicate stanzas with an unevaluable copy ----------------------
    one = (FIX / "one-pre.txt").read_text(encoding="utf-8")
    hdr = one.split("PATH: ", 1)[0]
    blk = ("PATH: " + one.split("PATH: ", 1)[1]).rstrip("\n")
    bad = blk.replace("SHA256:", "READ-ERROR: [Errno 13] Permission denied\nSHA256:")
    (FIX / "dupe5-bad-second-pre.txt").write_text(
        hdr + blk + "\n\n" + bad + "\n\n" + blk + "\n\n" + blk + "\n\n" + blk + "\n",
        encoding="utf-8")
    (FIX / "dupe5-bad-last-pre.txt").write_text(
        hdr + blk + "\n\n" + blk + "\n\n" + blk + "\n\n" + blk + "\n\n" + bad + "\n",
        encoding="utf-8")

    for name in ("hardlink5-pre.txt", "dupe5-bad-second-pre.txt", "dupe5-bad-last-pre.txt"):
        p = FIX / name
        print("FIXTURE %-30s %6d B  sha256=%s" % (name, len(p.read_bytes()), sha256_file(p)))
    print("# hardlink inode set: %s" % sorted({s["inode"] for s in secs}))
    print("# hardlink distinct resolved: %d" % len({str((hl / ('hl-%d' % i)).resolve()) for i in range(5)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
