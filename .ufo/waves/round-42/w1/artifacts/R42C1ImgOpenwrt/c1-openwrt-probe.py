#!/usr/bin/env python3
"""R42-C1 candidate recon probe: OpenWrt Kamikaze 8.09.x SquashFS v3 images.

Chain: fetch (+published md5sums check) -> container walk -> SquashFS v3
superblock -> unblob 26.6.4 handler pattern match (bytes only, no unblob run)
-> carve [offset, offset+bytes_used) -> non-sasquatch readers
   (`unsquashfs -s/-lls/-d`, `7z l -slt` / `7z x`) -> per-type inventory and
regular-file set agreement.

This seat may NOT run REA/unblob/sasquatch on a candidate or on anything carved
from it; it may only read candidates with unsquashfs, 7z and pure readers.
So this tool never invokes those three.

Usage:
  c1-openwrt-probe.py --work DIR [--only ID[,ID...]] [--no-fetch]
Writes under --work only: dl/ carve/ readers/ out/.
Honours TMPDIR.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

BASE = "https://archive.openwrt.org/kamikaze"

# id, release, target-dir, filename
CANDIDATES = [
    ("OW-8.09.1-ppc40x", "8.09.1", "ppc40x", "openwrt-ppc40x-squashfs.img"),
    ("OW-8.09.2-ppc44x", "8.09.2", "ppc44x", "openwrt-ppc44x-squashfs.img"),
    ("OW-8.09-brcm24", "8.09", "brcm-2.4", "openwrt-brcm-2.4-squashfs.trx"),
    ("OW-8.09.2-brcm47xx", "8.09.2", "brcm47xx", "openwrt-brcm47xx-squashfs.trx"),
    ("OW-8.09.1-wrt54g", "8.09.1", "brcm47xx", "openwrt-wrt54g-squashfs.bin"),
    ("OW-8.09.2-atheros", "8.09.2", "atheros", "openwrt-atheros-root.squashfs"),
    ("OW-8.09-ar71xx", "8.09", "ar71xx", "openwrt-ar71xx-root.squashfs"),
    ("OW-8.09.2-x86-img", "8.09.2", "x86", "openwrt-x86-squashfs.image"),
    ("OW-8.09-x86-fs", "8.09", "x86", "openwrt-x86-squashfs.fs"),
    ("OW-8.09.2-adm5120-be", "8.09.2", "adm5120/router_be",
     "openwrt-adm5120-p-334wt-squashfs.trx"),
]

# unblob 26.6.4 unblob/handlers/filesystem/squashfs.py, transcribed from the
# HexString blocks: 4 raw magic bytes + a u16 version at offset 28, read in the
# endianness the magic implies.
HANDLER_PATTERNS = [
    ("squashfs_v1", b"sqsh", "BE", 1), ("squashfs_v1", b"hsqs", "LE", 1),
    ("squashfs_v2", b"sqsh", "BE", 2), ("squashfs_v2", b"hsqs", "LE", 2),
    ("squashfs_v2_nonstandard", b"sqlz", "BE", 2), ("squashfs_v2_nonstandard", b"zlqs", "LE", 2),
    ("squashfs_v3", b"sqsh", "BE", 3), ("squashfs_v3", b"hsqs", "LE", 3),
    ("squashfs_v3_ddwrt", b"tqsh", "BE", 3), ("squashfs_v3_ddwrt", b"hsqt", "LE", 3),
    ("squashfs_v3_broadcom", b"qshs", "BE", 3), ("squashfs_v3_broadcom", b"shsq", "LE", 3),
    ("squashfs_v3_nonstandard", b"sqlz", "BE", 3), ("squashfs_v3_nonstandard", b"zlqs", "LE", 3),
    ("squashfs_v4_le", b"hsqs", "LE", 4),
    ("squashfs_v4_be", b"sqsh", "BE", 4),
    ("squashfs_v4_broadcom", b"qshs", "BE", 4), ("squashfs_v4_broadcom", b"shsq", "LE", 4),
]
MAGICS = sorted({p[1] for p in HANDLER_PATTERNS})
TYPEMAP = {"-": "file", "d": "dir", "l": "symlink", "c": "char",
           "b": "block", "p": "fifo", "s": "socket"}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def md5_file(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def get(url: str, timeout=120) -> tuple[int, dict, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "c1-probe/1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, dict(r.headers), r.read()


def fetch(url: str, dest: str, no_fetch: bool) -> dict:
    rec = {"url": url, "path": os.path.relpath(dest)}
    if no_fetch and os.path.exists(dest):
        rec.update(status="cached", access_time_utc=None, last_modified=None)
    else:
        t = datetime.now(timezone.utc)
        status, hdr, data = get(url)
        rec.update(status=status,
                   access_time_utc=t.strftime("%Y-%m-%dT%H:%M:%SZ"),
                   last_modified=hdr.get("Last-Modified"),
                   content_length=hdr.get("Content-Length"))
        with open(dest, "wb") as fh:
            fh.write(data)
    rec["bytes"] = os.path.getsize(dest)
    rec["sha256"] = sha256_file(dest)
    rec["md5"] = md5_file(dest)
    return rec


def published_md5(release: str, target: str, fname: str) -> dict:
    url = f"{BASE}/{release}/{target}/md5sums"
    try:
        status, _, body = get(url, timeout=60)
    except Exception as exc:
        return {"url": url, "status": f"error: {exc}"}
    rec = {"url": url, "status": status, "published_md5": None, "line": None}
    for line in body.decode("utf-8", "replace").splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].lstrip("./") == fname:
            rec["published_md5"] = parts[0]
            rec["line"] = line
    return rec


def parse_v3(data: bytes, off: int, endian: str) -> dict:
    e = ">" if endian == "BE" else "<"

    def u(fmt, pos):
        return struct.unpack_from(e + fmt, data, off + pos)[0]

    sb = {
        "offset": off,
        "magic_hex": data[off:off + 4].hex(),
        "magic_ascii": data[off:off + 4].decode("latin-1"),
        "endianness": endian,
        "s_major": u("H", 28), "s_minor": u("H", 30),
        "inodes": u("I", 4),
        "block_size": u("I", 51),
        "block_size_1": u("H", 32), "block_log": u("H", 34),
        "fragments": u("I", 55),
        "flags": data[off + 36], "no_uids": data[off + 37], "no_guids": data[off + 38],
        "mkfs_time": u("I", 39),
        "root_inode": u("Q", 43),
        "bytes_used": u("Q", 63),
        "uid_start": u("Q", 71), "guid_start": u("Q", 79),
        "inode_table_start": u("Q", 87),
        "directory_table_start": u("Q", 95),
        "fragment_table_start": u("Q", 103),
        "lookup_table_start": u("Q", 111),
    }
    ts = datetime.fromtimestamp(sb["mkfs_time"], timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sb["mkfs_time_utc"] = ts
    sb["compression"] = None  # v3 has no compression id field
    return sb


def handler_matches(data: bytes, off: int) -> list:
    hits = []
    if off < 0 or off + 30 > len(data):
        return hits
    for name, magic, pat_endian, ver in HANDLER_PATTERNS:
        if data[off:off + 4] != magic:
            continue
        e = ">" if pat_endian == "BE" else "<"
        if struct.unpack_from(e + "H", data, off + 28)[0] == ver:
            hits.append({"handler": name,
                         "pattern": f"{magic.hex()} [24] "
                                    + (f"{ver:04x}" if pat_endian == "BE" else f"{ver:04x}"),
                         "pattern_endian": pat_endian,
                         "extractor": "sasquatch-v4be" if (ver == 4 and pat_endian == "BE")
                                      else "sasquatch",
                         "extractor_arg": "-be" if pat_endian == "BE" else "-le"})
    return hits


def scan_magics(data: bytes) -> list:
    found = []
    for m in MAGICS:
        start = 0
        while True:
            i = data.find(m, start)
            if i < 0:
                break
            found.append((i, m.decode("latin-1")))
            start = i + 1
    return sorted(found)


def container_chain(data: bytes, sb_off: int) -> list:
    chain = []
    pos = 0
    if data[0:4] == b"HDR0":
        # OpenWrt trx.c: magic, len, crc32, flag_version{flags u16, version u16},
        # offsets[3], and for version >= 2 lengths[3].
        flags = struct.unpack_from("<H", data, 12)[0]
        version = struct.unpack_from("<H", data, 14)[0]
        rec = {
            "layer": "trx", "magic": "HDR0", "header_bytes": 28 if version < 2 else 40,
            "trx_len": struct.unpack_from("<I", data, 4)[0],
            "crc32": "%08x" % struct.unpack_from("<I", data, 8)[0],
            "flags": flags, "version": version,
            "offsets": list(struct.unpack_from("<3I", data, 16)),
            "note": "OpenWrt TRX: header, loader at offsets[0], rootfs at offsets[1]",
        }
        if version >= 2:
            rec["lengths"] = list(struct.unpack_from("<3I", data, 28))
        chain.append(rec)
        pos = rec["header_bytes"]
    elif data[0:4] == b"W54G":
        chain.append({
            "layer": "w54g", "magic": "W54G", "header_bytes": 32,
            "note": "Linksys/Broadcom device header before the squashfs on "
                    "openwrt-brcm47xx *-squashfs.bin images",
            "head_hex": data[:32].hex(),
        })
        pos = 32
    elif data[0:4] == b"\x27\x05\x19\x56":
        hcrc, = struct.unpack_from(">I", data, 4)
        ts, size = struct.unpack_from(">II", data, 8)
        load, ep = struct.unpack_from(">II", data, 16)
        dcrc, osid, arch, typ, comp = struct.unpack_from(">IBBBB", data, 24)
        chain.append({
            "layer": "uimage", "magic": "0x27051956", "header_bytes": 64,
            "header_crc": "%08x" % hcrc,
            "timestamp_utc": datetime.fromtimestamp(ts, timezone.utc)
                             .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "data_size": size, "load": hex(load), "entry": hex(ep),
            "data_crc": "%08x" % dcrc, "os": osid, "arch": arch, "type": typ,
            "compression": comp,
            "name": data[32:64].split(b"\x00")[0].decode("latin-1"),
            "note": "PowerPC uImage header (64 B); kernel payload precedes the 2 MiB rootfs",
        })
        pos = 64
    else:
        chain.append({"layer": "plain", "header_bytes": 0,
                      "note": "file starts with the SquashFS superblock",
                      "head_hex": data[:16].hex()})
    chain.append({"layer": "squashfs", "offset": sb_off, "gap_from_previous": sb_off - pos})
    return chain


def run(argv, cwd=None, timeout=1800) -> dict:
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return {"argv": argv, "exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def sevenzip_listing(out: str) -> list:
    entries, cur, started = [], None, False
    for line in out.splitlines():
        if line.startswith("----------"):
            started = True
            continue
        if not started:
            continue
        if line.startswith("Path = "):
            if cur:
                entries.append(cur)
            cur = {"path": line[7:], "mode": None, "folder": False, "size": None}
        elif cur is None:
            continue
        elif line.startswith("Folder = "):
            cur["folder"] = line[9:].strip() == "+"
        elif line.startswith("Size = "):
            v = line[7:].strip()
            cur["size"] = int(v) if v else None
        elif line.startswith("Mode = "):
            cur["mode"] = line[7:].strip()
    if cur:
        entries.append(cur)
    for e in entries:
        e["type"] = TYPEMAP.get((e["mode"] or "?")[0], "unknown")
    return entries


def walk_tree(root: str) -> list:
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                rows.append({"path": rel, "type": "symlink", "target": os.readlink(full)})
            else:
                rows.append({"path": rel, "type": "file",
                             "size": os.path.getsize(full), "sha256": sha256_file(full)})
    return rows


def lzma_probe(data: bytes, sb: dict) -> dict:
    """Can a stdlib reader decode the blocks?  v3 OpenWrt images are raw LZMA1
    (no per-block header): metadata blocks carry a 2-byte size header, data
    blocks are framed only by the inode block list."""
    import lzma
    rec = {"codec": "LZMA1 raw", "lc": 3, "lp": 0, "pb": 2,
           "metadata_block_expected": 8192}
    e = ">" if sb["endianness"] == "BE" else "<"
    f = [{"id": lzma.FILTER_LZMA1, "dict_size": 1 << 16, "lc": 3, "lp": 0, "pb": 2}]
    out = {}
    for label, pos in (("inode_table", sb["inode_table_start"]),
                       ("directory_table", sb["directory_table_start"])):
        if pos + 2 > len(data):
            out[label] = {"error": "offset beyond file"}
            continue
        hdr = struct.unpack_from(e + "H", data, pos)[0]
        size = hdr & 0x7FFF
        blob = data[pos + 2:pos + 2 + size]
        dec = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=f)
        try:
            body = dec.decompress(blob)
        except Exception as exc:
            out[label] = {"header": "%04x" % hdr, "compressed_size": size,
                          "error": f"{type(exc).__name__}: {exc}"}
            continue
        out[label] = {"header": "%04x" % hdr, "uncompressed_flag": bool(hdr & 0x8000),
                      "compressed_size": size, "decoded_bytes": len(body),
                      "eof": dec.eof, "head_hex": body[:12].hex()}
    # data block 0 sits directly after the 119-byte v3 superblock
    dec = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=f)
    try:
        body = dec.decompress(data[119:119 + 400000])
    except Exception as exc:
        out["data_block_0"] = {"offset": 119, "error": f"{type(exc).__name__}: {exc}"}
    else:
        elf = None
        if body[:4] == b"\x7fELF":
            cls, dt = body[4], body[5]
            machine = struct.unpack_from(">H" if dt == 2 else "<H", body, 18)[0]
            elf = {"class": cls, "data": dt, "machine": machine,
                   "machine_name": {2: "SPARC", 3: "i386", 8: "MIPS", 20: "PowerPC",
                                    40: "ARM", 62: "x86-64"}.get(machine, str(machine))}
        out["data_block_0"] = {"offset": 119, "decoded_bytes": len(body),
                               "eof": dec.eof, "head_hex": body[:8].hex(), "elf": elf}
    rec["blocks"] = out
    rec["stdlib_reader_feasible"] = (
        out.get("inode_table", {}).get("decoded_bytes") == 8192
        and out.get("data_block_0", {}).get("decoded_bytes") == sb["block_size"])
    return rec


def probe_one(work: str, cid: str, release: str, target: str, fname: str,
              no_fetch: bool) -> dict:
    url = f"{BASE}/{release}/{target}/{fname}"
    dest = os.path.join(work, "dl", f"{cid}.bin")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    rec = {"id": cid, "release": release, "target": target, "filename": fname,
           "fetch": fetch(url, dest, no_fetch)}
    rec["published_md5"] = published_md5(release, target, fname)
    if rec["published_md5"].get("published_md5"):
        rec["published_md5"]["matches"] = (
            rec["published_md5"]["published_md5"] == rec["fetch"]["md5"])
    with open(dest, "rb") as fh:
        data = fh.read()
    rec["magic_scan"] = scan_magics(data)
    sb_off = sb_endian = None
    for off, _ in rec["magic_scan"]:
        hits = handler_matches(data, off)
        if hits:
            sb_off, sb_endian = off, hits[0]["pattern_endian"]
            break
    if sb_off is None:
        rec["error"] = "no squashfs handler pattern matched"
        return rec
    sb = parse_v3(data, sb_off, sb_endian)
    rec["superblock"] = sb
    rec["handler_matches"] = handler_matches(data, sb_off)
    rec["handler_match_offsets"] = [
        {"offset": off, "handlers": [h["handler"] for h in handler_matches(data, off)]}
        for off, _ in rec["magic_scan"] if handler_matches(data, off)]
    rec["container_chain"] = container_chain(data, sb_off)
    end = sb_off + sb["bytes_used"]
    rec["carve"] = {
        "start": sb_off, "end": end, "size": end - sb_off,
        "rule": "[offset, offset+bytes_used)",
        "tail_bytes_after_chunk": len(data) - end,
        "bytes_after_chunk_hex": data[end:end + 24].hex(),
        "bytes_before_chunk_hex": data[max(0, sb_off - 16):sb_off].hex(),
    }
    pad = {}
    for ps in (4096, 1024):
        size = (sb["bytes_used"] + ps - 1) // ps * ps
        seg = data[sb_off + sb["bytes_used"]:sb_off + size]
        pad[str(ps)] = {"rounded_size": size, "pad_len": size - sb["bytes_used"],
                        "all_zero": seg == b"\x00" * (size - sb["bytes_used"]),
                        "hex": seg[:16].hex()}
    rec["unblob_chunk_end_padding"] = pad
    carve_path = os.path.join(work, "carve", f"{cid}.sqfs")
    os.makedirs(os.path.dirname(carve_path), exist_ok=True)
    carve_data = data[sb_off:end]
    with open(carve_path, "wb") as fh:
        fh.write(carve_data)
    rec["carve"].update(path=os.path.relpath(carve_path), sha256=sha256_file(carve_path))

    rd = os.path.join(work, "readers", cid)
    os.makedirs(rd, exist_ok=True)
    r_lls = run(["unsquashfs", "-lls", "-no-progress", carve_path], cwd=rd)
    ux = os.path.join(rd, "u-extract")
    r_ud = run(["unsquashfs", "-no-progress", "-d", ux, carve_path], cwd=rd)
    r_zs = run(["unsquashfs", "-s", carve_path], cwd=rd)
    r_zl = run(["7z", "l", "-slt", carve_path], cwd=rd)
    zx = os.path.join(rd, "z-extract")
    r_zx = run(["7z", "x", "-y", "-o" + zx, carve_path], cwd=rd)

    zentries = sevenzip_listing(r_zl["stdout"])
    zby = {}
    for e in zentries:
        if e["path"] == carve_path:
            continue
        zby.setdefault(e["path"], e)
    ztype = {p: e["type"] for p, e in zby.items()}
    z_files = {p: e for p, e in zby.items() if e["type"] == "file"}
    z_links = {p: e for p, e in zby.items() if e["type"] == "symlink"}
    z_devs = {p: e for p, e in zby.items() if e["type"] in ("char", "block", "fifo", "socket")}
    z_dirs = {p: e for p, e in zby.items() if e["type"] == "dir"}
    method = None
    for line in r_zl["stdout"].splitlines():
        if line.startswith("Method = "):
            method = line[9:].strip()
    fsver = None
    for line in r_zl["stdout"].splitlines():
        if line.startswith("File System = "):
            fsver = line[14:].strip()

    zx_rows = walk_tree(zx) if os.path.isdir(zx) else []
    zx_files = {x["path"]: x for x in zx_rows if x["type"] == "file"}
    zx_links = {x["path"]: x for x in zx_rows if x["type"] == "symlink"}
    # 7-Zip materialises every refused "dangerous" symlink as a 0-byte regular
    # file, so the extraction tree is NOT usable as an oracle by itself: type
    # the inventory from `7z l -slt` Mode and take content from the extraction.
    missing = sorted(set(z_files) - set(zx_files))
    phantom = sorted(set(zx_files) & set(z_links))
    extra = sorted(set(zx_files) - set(z_files) - set(z_links))
    size_mismatch = sorted(p for p in set(z_files) & set(zx_files)
                           if z_files[p]["size"] != zx_files[p]["size"])
    oracle_rows = {p: {"size": z_files[p]["size"], "sha256": zx_files[p]["sha256"]}
                   for p in z_files
                   if p in zx_files and z_files[p]["size"] == zx_files[p]["size"]}
    link_target_cmp = {
        "listing_n": len(z_links), "extracted_n": len(zx_links),
        "refused_by_7z": sorted(set(z_links) - set(zx_links))[:30],
        "n_refused": len(set(z_links) - set(zx_links)),
        "phantom_zero_byte_files": len(phantom),
        "phantom_missing_entirely": sorted(set(z_links) - set(zx_links) - set(zx_files))[:10],
    }
    ux_rows = walk_tree(ux) if os.path.isdir(ux) else []
    rec["readers"] = {
        "unsquashfs": {
            "version": (run(["unsquashfs", "-version"])["stdout"].splitlines() or [""])[0],
            "s": {"exit": r_zs["exit"], "stdout": r_zs["stdout"], "stderr": r_zs["stderr"]},
            "lls": {"exit": r_lls["exit"], "n_lines": len(r_lls["stdout"].splitlines()),
                    "stdout_head": r_lls["stdout"][:400],
                    "stderr": r_lls["stderr"][-600:]},
            "d": {"exit": r_ud["exit"], "stdout": r_ud["stdout"][-400:],
                  "stderr": r_ud["stderr"][-600:]},
            "extracted": {"n": len(ux_rows),
                          "files": sum(1 for x in ux_rows if x["type"] == "file")},
            "reads_v3_lzma": r_lls["exit"] == 0,
            "usable_as_oracle": r_lls["exit"] == 0 and r_ud["exit"] == 0,
        },
        "sevenzip": {
            "version": [l.strip() for l in run(["7z"])["stdout"].splitlines()
                        if l.startswith("7-Zip")][0],
            "l": {"exit": r_zl["exit"], "file_system": fsver, "method": method,
                  "n_entries": len(zby)},
            "x": {"exit": r_zx["exit"], "stdout_tail": r_zx["stdout"][-300:],
                  "stderr_tail": r_zx["stderr"][-400:]},
            "counts": {"file": len(z_files), "dir": len(z_dirs), "symlink": len(z_links),
                       "device_like": len(z_devs),
                       "device_paths": sorted(z_devs)[:20]},
            "usable_as_oracle": r_zl["exit"] == 0 and not missing and not size_mismatch,
        },
        "agreement": {
            "regular_files_in_listing": len(z_files),
            "regular_files_extracted": len(zx_files),
            "oracle_rows": len(oracle_rows),
            "missing_after_extract": missing[:20], "n_missing": len(missing),
            "phantom_at_symlink_paths": phantom[:10], "n_phantom": len(phantom),
            "extra_after_extract": extra[:20], "n_extra": len(extra),
            "size_mismatch": size_mismatch[:20], "n_size_mismatch": len(size_mismatch),
            "listing_vs_extract_identical": not missing and not extra and not size_mismatch,
            "symlinks": link_target_cmp,
            "cross_reader_possible": r_lls["exit"] == 0,
            "second_reader": ("unsquashfs" if r_lls["exit"] == 0
                              else "lane stdlib v3-LZMA reader (required)"),
        },
        "lzma": lzma_probe(carve_data, sb),
    }
    outdir = os.path.join(work, "out")
    os.makedirs(outdir, exist_ok=True)
    for suffix, payload in (
            (".lls.txt", r_lls["stdout"] + "\n# STDERR\n" + r_lls["stderr"]),
            (".unsquashfs-d.log", r_ud["stdout"] + "\n# STDERR\n" + r_ud["stderr"]),
            (".7z-slt.txt", r_zl["stdout"]),
            (".7z-x.log", r_zx["stdout"] + "\n# STDERR\n" + r_zx["stderr"])):
        with open(os.path.join(outdir, cid + suffix), "w") as fh:
            fh.write(payload)
    with open(os.path.join(outdir, cid + ".oracle-7z.tsv"), "w") as fh:
        fh.write("path\tsize\tsha256\n")
        for p in sorted(oracle_rows):
            fh.write(f"{p}\t{oracle_rows[p]['size']}\t{oracle_rows[p]['sha256']}\n")
    with open(os.path.join(outdir, cid + ".nonregular.tsv"), "w") as fh:
        fh.write("path\ttype\tdetail\n")
        for p in sorted(z_links):
            tgt = zx_links[p]["target"] if p in zx_links else ""
            fh.write(f"{p}\tsymlink\t{tgt}\n")
        for p in sorted(z_devs):
            fh.write(f"{p}\t{z_devs[p]['type']}\t{z_devs[p].get('mode')}\n")
        for p in sorted(z_dirs):
            fh.write(f"{p}\tdir\t\n")
    rec["nonregular"] = {
        "n_symlinks": len(z_links), "n_devices": len(z_devs), "n_dirs": len(z_dirs),
        "symlinks_sample": [{"path": p, "target": z_links[p].get("size")}
                            for p in sorted(z_links)[:15]],
    }
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    os.makedirs(work, exist_ok=True)
    only = {s for s in a.only.split(",") if s}
    out = []
    for cid, rel, tgt, fn in CANDIDATES:
        if only and cid not in only:
            continue
        try:
            rec = probe_one(work, cid, rel, tgt, fn, a.no_fetch)
        except Exception as exc:
            rec = {"id": cid, "release": rel, "target": tgt, "filename": fn,
                   "error": f"{type(exc).__name__}: {exc}"}
        out.append(rec)
        print(cid, rec.get("error", ""), flush=True)
    with open(os.path.join(work, "out", "candidates.json"), "w") as fh:
        json.dump({"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "tool": "c1-openwrt-probe.py",
                   "candidates": out}, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
