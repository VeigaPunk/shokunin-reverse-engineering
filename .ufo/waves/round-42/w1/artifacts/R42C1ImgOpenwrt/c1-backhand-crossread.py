#!/usr/bin/env python3
"""R42-C1 third-reader cross-read: backhand-cli 0.25.5 vs the 7-Zip oracle.

For each carved candidate this tool
  1. reads the superblock with `unsquashfs-backhand -k <kind> -s`   (independent superblock parse)
  2. extracts with `-k <kind> -d DIR`                              (symlinks extract as symlinks)
  3. types the 7-Zip side from `7z l -slt` Mode and takes content from `7z x`
  4. compares regular files (path + size + sha256) and symlink sets, both ways.

It is a pure reader: no REA, no unblob, no sasquatch.

Usage:
  c1-backhand-crossread.py --work DIR [--carves CARVEDIR]
Writes DIR/out/backhand-crossread.json and DIR/out/backhand-<id>.sv.
Honours TMPDIR.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

BACKHAND = "/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand"
TYPEMAP = {"-": "file", "d": "dir", "l": "symlink", "c": "char",
           "b": "block", "p": "fifo", "s": "socket"}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def run(argv, timeout=1800) -> dict:
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    return {"argv": argv, "exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def walk(root: str) -> tuple[dict, dict]:
    """Type by lstat.  Symlinks to directories must be counted as symlinks, so
    directory entries are inspected too (os.walk files them under dirnames)."""
    reg, lnk = {}, {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames) + sorted(dirnames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                lnk[rel] = os.readlink(full)
            elif name in filenames:
                reg[rel] = {"size": os.path.getsize(full), "sha256": sha256_file(full)}
    return reg, lnk


def sevenzip_typed(carve: str) -> tuple[dict, dict, dict]:
    out = run(["7z", "l", "-slt", carve])["stdout"]
    cur, typed = None, {}
    method = fsver = None
    for line in out.splitlines():
        if line.startswith("Path = ") and not line.startswith("Path = /"):
            cur = line[7:]
        elif line.startswith("Mode = ") and cur:
            typed[cur] = line[7:].strip()
        elif line.startswith("Method = "):
            method = line[9:].strip()
        elif line.startswith("File System = "):
            fsver = line[14:].strip()
    files = {p for p, m in typed.items() if m[:1] == "-"}
    links = {p for p, m in typed.items() if m[:1] == "l"}
    return files, links, {"method": method, "file_system": fsver, "n_typed": len(typed)}


def backhand_sb(kind: str, carve: str) -> dict:
    r = run([BACKHAND, "-k", kind, "-s", carve])
    sb = {"exit": r["exit"], "raw_head": r["stdout"][:40]}
    for key, pat in (("version_major", r"version_major:\s*0x([0-9a-fA-F]+)"),
                     ("version_minor", r"version_minor:\s*0x([0-9a-fA-F]+)"),
                     ("block_size", r"\bblock_size:\s*0x([0-9a-fA-F]+)"),
                     ("fragments", r"fragments:\s*0x([0-9a-fA-F]+)"),
                     ("inode_count", r"inode_count:\s*0x([0-9a-fA-F]+)"),
                     ("flags", r"flags:\s*0x([0-9a-fA-F]+)"),
                     ("mkfs_time", r"mkfs_time:\s*0x([0-9a-fA-F]+)")):
        m = re.search(pat, r["stdout"])
        sb[key] = int(m.group(1), 16) if m else None
    m = re.search(r"bytes_used:\s*0x([0-9a-fA-F]+)", r["stdout"])
    sb["bytes_used"] = int(m.group(1), 16) if m else None
    if sb.get("mkfs_time"):
        sb["mkfs_time_utc"] = datetime.fromtimestamp(sb["mkfs_time"], timezone.utc) \
            .strftime("%Y-%m-%dT%H:%M:%SZ")
    sb["stderr"] = r["stderr"][-300:]
    return sb


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--carves", required=True)
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    outdir = os.path.join(work, "out")
    os.makedirs(outdir, exist_ok=True)
    results = []
    for name in sorted(os.listdir(a.carves)):
        if not name.endswith(".sqfs"):
            continue
        cid = name[:-5]
        carve = os.path.join(a.carves, name)
        with open(carve, "rb") as fh:
            head = fh.read(4)
        kind = "be_v3_0_lzma" if head == b"sqsh" else "le_v3_0_lzma"
        sb = backhand_sb(kind, carve)
        dest = os.path.join(work, "bh", cid)
        r = run([BACKHAND, "-k", kind, "-d", dest, "-f", "--quiet", carve])
        breg, blnk = walk(dest) if os.path.isdir(dest) else ({}, {})
        zfiles, zlinks, zmeta = sevenzip_typed(carve)
        zx = os.path.join(work, "zx", cid)
        if not os.path.isdir(zx):
            run(["7z", "x", "-y", "-o" + zx, carve])
        zreg, zlnk = walk(zx) if os.path.isdir(zx) else ({}, {})
        only_b = sorted(set(breg) - zfiles)
        only_z = sorted(zfiles - set(breg))
        mism = sorted(p for p in set(breg) & zfiles
                      if breg[p] != zreg.get(p))
        rec = {
            "id": cid,
            "kind": kind,
            "backhand_version": run([BACKHAND, "--version"])["stdout"].strip(),
            "backhand_superblock": sb,
            "backhand_extract": {"exit": r["exit"], "stderr_tail": r["stderr"][-400:],
                                 "regular": len(breg), "symlinks": len(blnk),
                                 "dirs": sum(1 for _ in os.walk(dest))
                                 if os.path.isdir(dest) else 0},
            "sevenzip": {"typed_regular": len(zfiles), "typed_symlinks": len(zlinks),
                         **zmeta},
            "agreement": {
                "path_set_identical": set(breg) == zfiles,
                "regular_files_backhand": len(breg),
                "regular_files_7z_typed": len(zfiles),
                "only_backhand": only_b[:10], "n_only_backhand": len(only_b),
                "only_7z": only_z[:10], "n_only_7z": len(only_z),
                "content_mismatch": mism[:10], "n_content_mismatch": len(mism),
                "all_regular_agree": (set(breg) == zfiles and not mism),
                "symlinks_backhand": len(blnk), "symlinks_7z_typed": len(zlinks),
                "symlink_path_set_identical": set(blnk) == zlinks,
                "symlinks_7z_not_in_backhand": sorted(zlinks - set(blnk))[:10],
                "symlink_target_mismatch": [p for p in sorted(set(blnk) & set(zlnk))
                                            if blnk[p] != zlnk[p]][:10],
            },
        }
        # per-file side files for the lane
        with open(os.path.join(outdir, f"backhand-{cid}.sv.tsv"), "w") as fh:
            fh.write("path\tsize\tsha256\tkind\n")
            for p in sorted(breg):
                fh.write(f"{p}\t{breg[p]['size']}\t{breg[p]['sha256']}\tfile\n")
            for p in sorted(blnk):
                fh.write(f"{p}\t0\t-\tsymlink->{blnk[p]}\n")
        results.append(rec)
        print(cid, "agree" if rec["agreement"]["all_regular_agree"] else "DISAGREE",
              rec["agreement"]["regular_files_backhand"], rec["agreement"]["regular_files_7z_typed"],
              flush=True)
    with open(os.path.join(outdir, "backhand-crossread.json"), "w") as fh:
        json.dump({"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "tool": "c1-backhand-crossread.py", "results": results}, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
