#!/usr/bin/env python3
"""Oracle-agreement check on a magic-normalised copy of a DD-WRT v3 carrier.

Producers: backhand 0.25.5 `unsquashfs-backhand` (kinds le_v3_0_lzma / be_v3_0_lzma) and 7-Zip 26.04.
Both are run on a copy whose first four bytes are the standard v3 magic for the byte order
(hsqt -> hsqs, tqsh -> sqsh); the carrier pin is always the published, unpatched bytes.

Reports: path-set agreement, per-type counts, and (with --full) sha256 agreement over regular files.

Usage: oracle-agreement.py --work DIR [--full] image:offset [image:offset ...]
"""
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess

BACKHAND = "/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand"
STD = {b"hsqt": (b"hsqs", "le_v3_0_lzma"), b"tqsh": (b"sqsh", "be_v3_0_lzma"),
       b"hsqs": (b"hsqs", "le_v3_0_lzma"), b"sqsh": (b"sqsh", "be_v3_0_lzma")}
V3_FMT = "6I4H3B I Q I I I Q Q Q Q Q Q Q"


def bytes_used(buf, off):
    magic = buf[off:off + 4]
    be = magic in (b"sqsh", b"tqsh", b"qshs", b"sqlz")
    vals = struct.unpack((">" if be else "<") + V3_FMT, buf[off + 4:off + 119])
    return magic, vals[18]


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def sevenzip_rows(out):
    rows, cur = {}, None
    for line in out.splitlines():
        if line.startswith("Path = "):
            cur = line[7:].strip()
            rows[cur] = {}
        elif cur and line.startswith("Mode = "):
            rows[cur]["mode"] = line[7:].strip()
        elif cur and line.startswith("Size = "):
            rows[cur]["size"] = line[7:].strip()
    return rows


def walk(root):
    files, links, dirs = {}, {}, set()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in list(dirnames) + list(filenames):
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, root)
            if os.path.islink(p):
                links[rel] = os.readlink(p)
            elif name in dirnames:
                dirs.add(rel)
            else:
                files[rel] = (os.path.getsize(p), hashlib.sha256(open(p, "rb").read()).hexdigest())
    return files, links, dirs


def probe(image, off, workdir, full):
    buf = open(image, "rb").read()
    magic, used = bytes_used(buf, off)
    std, kind = STD[magic]
    rec = {"image": image, "offset": off, "bytes_used": used, "magic": magic.decode(),
           "backhand_kind": kind, "normalised_magic": std.decode()}
    if magic not in STD:
        rec["error"] = "no standard-magic mapping"
        return rec
    norm = os.path.join(workdir, os.path.basename(image) + f".{off}.norm.sqfs")
    blob = bytearray(buf[off:off + used])
    blob[0:4] = std
    open(norm, "wb").write(blob)
    rec["normalised_sha256"] = hashlib.sha256(blob).hexdigest()
    rc_l, so_l, se_l = run([BACKHAND, "-l", "-k", kind, norm])
    bh_paths = {ln.strip().lstrip("/") for ln in so_l.splitlines() if ln.strip() and ln.strip() != "/"}
    rc_7, so_7, se_7 = run(["7z", "l", "-ba", "-slt", norm])
    z = sevenzip_rows(so_7)
    z_paths = {p for p in z if p}
    rec["backhand"] = {"rc": rc_l, "paths": len(bh_paths), "stderr": se_l.strip()[:200]}
    rec["sevenzip"] = {"rc": rc_7, "paths": len(z_paths),
                       "files": sum(1 for v in z.values() if v.get("mode", "").startswith("-")),
                       "dirs": sum(1 for v in z.values() if v.get("mode", "").startswith("d")),
                       "symlinks": sum(1 for v in z.values() if v.get("mode", "").startswith("l"))}
    rec["path_sets_equal"] = bh_paths == z_paths
    rec["only_backhand"] = sorted(bh_paths - z_paths)[:5]
    rec["only_7z"] = sorted(z_paths - bh_paths)[:5]
    if full:
        d_bh = os.path.join(workdir, os.path.basename(image) + ".bh")
        d_7 = os.path.join(workdir, os.path.basename(image) + ".7z")
        shutil.rmtree(d_bh, ignore_errors=True)
        shutil.rmtree(d_7, ignore_errors=True)
        rc_x, _, se_x = run([BACKHAND, "-d", d_bh, "-k", kind, norm])
        rc_7x, _, _ = run(["7z", "x", "-y", "-o" + d_7, norm])
        f_bh, l_bh, dir_bh = walk(d_bh)
        f_7, l_7, dir_7 = walk(d_7)
        common = set(f_bh) & set(f_7)
        agree = sum(1 for p in common if f_bh[p] == f_7[p])
        rec["extract"] = {"backhand_rc": rc_x, "backhand_files": len(f_bh), "backhand_links": len(l_bh),
                          "sevenzip_rc": rc_7x, "sevenzip_files": len(f_7), "sevenzip_links": len(l_7),
                          "common_regular": len(common), "sha256_agree": agree,
                          "only_backhand_regular": sorted(set(f_bh) - set(f_7))[:5],
                          "only_7z_regular": sorted(set(f_7) - set(f_bh))[:5]}
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("targets", nargs="+")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    out = []
    for t in a.targets:
        img, off = t.rsplit(":", 1)
        out.append(probe(img, int(off, 0), a.work, a.full))
    print(json.dumps(out, indent=1))
