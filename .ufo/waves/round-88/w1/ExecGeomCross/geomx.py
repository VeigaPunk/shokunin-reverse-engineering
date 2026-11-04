#!/usr/bin/env python3
"""geomx.py - ExecGeomCross: independent re-derivation of the R88-C1
chain-geometry rule for a zeroed first b_info `sz_cpr` in a UPX 5.2.0
little-endian ELF.

Written from scratch for this seat: no import of tools/round-88 or
tools/round-87, no reuse of their locator or walk code.  The only shared
inputs are the UPX on-disk structure definitions (PackHeader / l_info /
p_info / b_info) and the geometry rule under test:

  the next block starts exactly 12 + sz_cpr bytes after this one, so
  sz_cpr = candidate - (block0 + 12) for the next plausible b_info whose
  own chain reaches the end-of-chain sentinel, with 0 < sz_cpr <= sz_unc;
  among candidates the one accounting for the most of the PackHeader's
  declared u_len wins (fits_u_len first, then largest accounted total,
  then smallest derived value).

Modes:
  inspect <packed>                 dump PackHeader / l_info / chain / sentinel
  derive  <carrier> <workdir>      pack, tamper, derive, validate, cross-check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys

MAGIC = b"UPX!"
PH_SIZE = 32          # magic version format method level u_adler c_adler u_len
                      # c_len u_file_size filter filter_cto n_mru checksum
PH_WINDOW = 512       # PackHeader lives in the file tail
MAX_BLOCKS = 1 << 16
UPX = "/usr/bin/upx"


class Refuse(Exception):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ph_checksum(h: bytes) -> int:
    """UPX PackHeader checksum: sum of bytes 4..30 mod 251 (excludes magic)."""
    return sum(h[4:31]) % 251


# --------------------------------------------------------------------------
# anchors
# --------------------------------------------------------------------------
def find_packheader(d: bytes) -> tuple[int, dict]:
    """Last offset in the tail window whose 32 bytes validate as a PackHeader."""
    n = len(d)
    lo = max(0, n - PH_WINDOW)
    for o in range(n - PH_SIZE, lo - 1, -1):
        h = d[o:o + PH_SIZE]
        if len(h) != PH_SIZE:
            continue
        version, fmt = h[4], h[5]
        if not 10 <= version <= 20:
            continue
        if fmt >= 128 or fmt in (1, 2, 3, 4):     # LE, non-DOS
            continue
        if h[31] != ph_checksum(h):
            continue
        u_len, c_len, u_file_size = struct.unpack_from("<III", h, 16)
        if not (0 < u_len and 0 < c_len <= n and 0 < u_file_size):
            continue
        return o, {"offset": o, "magic": h[0:4].hex(), "version": version,
                   "format": fmt, "method": h[6], "level": h[7],
                   "u_len": u_len, "c_len": c_len, "u_file_size": u_file_size,
                   "filter": h[28], "filter_cto": h[29], "n_mru": h[30],
                   "checksum_ok": True}
    raise Refuse("no validated PackHeader in the tail window")


def find_linfo_by_magic(d: bytes, ph_off: int, ph: dict) -> list[dict]:
    """Locate l_info from its own `UPX!` word (independent of the u_file_size
    redundancy): l_info = {l_checksum, l_magic, l_lsize, l_version, l_format}
    then p_info = {p_progid, p_filesize, p_blocksize}; b_info starts at
    l_magic + 20."""
    out, p = [], d.find(MAGIC, 8)
    while p != -1 and p < ph_off:
        if p + 20 <= ph_off:
            l_lsize = struct.unpack_from("<H", d, p + 4)[0]
            l_version, l_format = d[p + 6], d[p + 7]
            # p_info begins at l_magic + 8 (l_info is 12 bytes from l_checksum)
            p_progid, p_filesize, p_blocksize = struct.unpack_from("<III", d, p + 8)
            if (l_version == ph["version"] and l_format == ph["format"]
                    and l_lsize > 0 and p_filesize == ph["u_file_size"]
                    and 0 < p_blocksize <= p_filesize):
                out.append({"l_magic": p, "l_info": p - 4, "b0": p + 20,
                            "l_lsize": l_lsize, "l_version": l_version,
                            "l_format": l_format, "p_progid": p_progid,
                            "p_filesize": p_filesize, "p_blocksize": p_blocksize})
        p = d.find(MAGIC, p + 1)
    return out


def find_linfo_by_pfsize(d: bytes, ph_off: int, ph: dict) -> list[dict]:
    """Locate l_info from the u_file_size redundancy instead (p_filesize sits
    12 bytes after l_magic), as an independent cross-check of the magic
    locator."""
    want = struct.pack("<I", ph["u_file_size"])
    out, p = [], d.find(want, 12)
    while p != -1 and p < ph_off:
        m = p - 12
        if m >= 4 and m + 20 <= ph_off and d[m + 6] == ph["version"] \
                and d[m + 7] == ph["format"]:
            out.append({"l_magic": m, "l_info": m - 4, "b0": m + 20,
                        "l_lsize": struct.unpack_from("<H", d, m + 4)[0],
                        "p_progid": struct.unpack_from("<I", d, m + 8)[0],
                        "p_filesize": struct.unpack_from("<I", d, m + 12)[0],
                        "p_blocksize": struct.unpack_from("<I", d, m + 16)[0]})
        p = d.find(want, p + 1)
    return out


# --------------------------------------------------------------------------
# b_info chain
# --------------------------------------------------------------------------
def block_at(d: bytes, q: int, end: int, methods: set[int]) -> dict | None:
    if q < 0 or q + 12 > end:
        return None
    sz_unc, sz_cpr = struct.unpack_from("<II", d, q)
    if sz_unc == 0 or sz_cpr == 0 or sz_cpr > sz_unc:
        return None
    if q + 12 + sz_cpr > end:
        return None
    if d[q + 8] not in methods:
        return None
    return {"off": q, "sz_unc": sz_unc, "sz_cpr": sz_cpr, "method": d[q + 8],
            "ftid": d[q + 9], "cto8": d[q + 10], "unused": d[q + 11],
            "advance": 12 + sz_cpr}


def walk(d: bytes, start: int, end: int, methods: set[int]) -> tuple[int, list[dict]]:
    """Walk one contiguous b_info run; returns (stop offset, blocks)."""
    q, blocks = start, []
    for _ in range(MAX_BLOCKS):
        b = block_at(d, q, end, methods)
        if b is None:
            break
        blocks.append(b)
        q += b["advance"]
    return q, blocks


def is_sentinel(d: bytes, s: int, ph_off: int) -> bool:
    """End-of-chain b_info: sz_unc == 0, method/ftid/cto8/unused all zero,
    wholly before the PackHeader."""
    return (0 <= s and s + 12 <= ph_off
            and d[s:s + 4] == b"\0\0\0\0" and d[s + 8:s + 12] == b"\0\0\0\0")


def reach(d: bytes, start: int, ph_off: int, methods: set[int]) -> dict:
    """Walk from `start`; where the run stops short of a sentinel (embedded
    loader), resume at the best later offset whose own run ends at one
    (sentinel reading UPX! preferred, then nearest the PackHeader)."""
    stop, blocks = walk(d, start, ph_off, methods)
    if is_sentinel(d, stop, ph_off):
        return {"end": stop, "blocks": blocks, "resume": None, "resumed": []}
    best = None
    for s in range(stop + 1, ph_off - 12):
        b = block_at(d, s, ph_off, methods)
        if b is None:
            continue
        e2, b2 = walk(d, s, ph_off, methods)
        if b2 and is_sentinel(d, e2, ph_off):
            key = (d[e2 + 4:e2 + 8] == MAGIC, e2)
            if best is None or key > best[0]:
                best = (key, e2, s, b2)
    if best is None:
        return {"end": stop, "blocks": blocks, "resume": None, "resumed": [],
                "reached": False}
    return {"end": best[1], "blocks": blocks, "resume": best[2], "resumed": best[3],
            "reached": True}


# --------------------------------------------------------------------------
# the geometry rule under test
# --------------------------------------------------------------------------
def derive(d: bytes, ph_off: int, ph: dict, lin: dict) -> dict:
    b0 = lin["b0"]
    sz_unc0, sz_cpr0 = struct.unpack_from("<II", d, b0)
    m0 = d[b0 + 8]
    methods = {m0, ph["method"]}
    scanned = 0
    structural = []
    for s1 in range(b0 + 13, ph_off - 12):
        scanned += 1
        b = block_at(d, s1, ph_off, methods)
        if b is None:
            continue
        derived = s1 - (b0 + 12)
        if not 0 < derived <= sz_unc0:
            continue
        structural.append({"next_block": s1, "derived": derived,
                           "next_sz_unc": b["sz_unc"], "next_sz_cpr": b["sz_cpr"],
                           "next_method": b["method"]})
    cands = []
    for c in structural:
        dd = bytearray(d)
        struct.pack_into("<I", dd, b0 + 4, c["derived"])
        r = reach(bytes(dd), b0, ph_off, methods)
        if not is_sentinel(dd, r["end"], ph_off):
            c["chain_from_b0_reaches_sentinel"] = False
            continue
        e2, b2 = walk(dd, c["next_block"], ph_off, methods)
        total = (sum(x["sz_unc"] for x in r["blocks"])
                 + sum(x["sz_unc"] for x in r["resumed"]))
        rec = dict(c)
        rec.update({
            "chain_from_b0_reaches_sentinel": True,
            "chain_from_candidate_alone_reaches_sentinel": is_sentinel(dd, e2, ph_off),
            "sentinel": r["end"],
            "sentinel_sz_cpr_is_magic": dd[r["end"] + 4:r["end"] + 8] == MAGIC,
            "blocks_from_b0": len(r["blocks"]),
            "resume": r["resume"],
            "blocks_resumed": len(r["resumed"]),
            "uncompressed_accounted": total,
            "fits_u_len": total <= ph["u_len"],
            "key": (total <= ph["u_len"], total, -c["derived"]),
        })
        cands.append(rec)
    cands.sort(key=lambda r: r["key"], reverse=True)
    return {"b0": b0, "block0_sz_unc": sz_unc0, "block0_sz_cpr_observed": sz_cpr0,
            "block0_method": m0, "packheader_method": ph["method"],
            "u_len": ph["u_len"], "offsets_scanned": scanned,
            "structural_candidates": len(structural),
            "sentinel_reaching_candidates": len(cands),
            "candidates": cands,
            "chosen": cands[0] if cands else None}


# --------------------------------------------------------------------------
# process helpers
# --------------------------------------------------------------------------
def run(cmd: list[str], cwd: str | None = None) -> dict:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True)
    return {"cmd": cmd, "exit": p.returncode,
            "stdout": p.stdout.decode("utf-8", "replace").strip(),
            "stderr": p.stderr.decode("utf-8", "replace").strip()}


def inspect(path: str) -> dict:
    with open(path, "rb") as fh:
        d = fh.read()
    ph_off, ph = find_packheader(d)
    magic_l = find_linfo_by_magic(d, ph_off, ph)
    pfsize_l = find_linfo_by_pfsize(d, ph_off, ph)
    rec = {"file": path, "size": len(d), "sha256": sha256(d),
           "packheader": ph, "linfo_by_magic": magic_l,
           "linfo_by_p_filesize": pfsize_l,
           "locators_agree": ([x["l_magic"] for x in magic_l]
                              == [x["l_magic"] for x in pfsize_l]),
           "linfo_count_magic": len(magic_l), "linfo_count_pfsize": len(pfsize_l)}
    if magic_l:
        lin = magic_l[0]
        b0 = lin["b0"]
        sz_unc0, sz_cpr0 = struct.unpack_from("<II", d, b0)
        methods = {d[b0 + 8], ph["method"]}
        r = reach(d, b0, ph_off, methods)
        rec.update({"b0": b0, "block0_sz_unc": sz_unc0, "block0_sz_cpr": sz_cpr0,
                    "block0_method": d[b0 + 8],
                    "chain_blocks": len(r["blocks"]), "chain_end": r["end"],
                    "resume": r["resume"], "blocks_resumed": len(r["resumed"]),
                    "sentinel_ok": is_sentinel(d, r["end"], ph_off),
                    "chain_sz_unc_sum": sum(x["sz_unc"] for x in r["blocks"])
                    + sum(x["sz_unc"] for x in r["resumed"]),
                    "blocks": [{"off": x["off"], "sz_unc": x["sz_unc"],
                                "sz_cpr": x["sz_cpr"], "method": x["method"]}
                               for x in (r["blocks"] + r["resumed"])]})
    return rec


# --------------------------------------------------------------------------
# full pipeline for one carrier
# --------------------------------------------------------------------------
def derive_carrier(carrier: str, workdir: str, repair_tool: str) -> dict:
    os.makedirs(workdir, exist_ok=True)
    name = os.path.basename(carrier)
    orig = os.path.join(workdir, name + ".orig")
    packed = os.path.join(workdir, name + ".packed")
    if not os.path.exists(orig):
        shutil.copyfile(carrier, orig)
        os.chmod(orig, 0o755)
    orig_sha = sha256(open(orig, "rb").read())
    if not os.path.exists(packed):
        r = run([UPX, "--best", "-o", packed, orig])
        if r["exit"] != 0:
            raise Refuse(f"upx --best failed: {r['stderr']}")
    d = open(packed, "rb").read()
    ph_off, ph = find_packheader(d)
    magic_l = find_linfo_by_magic(d, ph_off, ph)
    pfsize_l = find_linfo_by_pfsize(d, ph_off, ph)
    if not magic_l:
        raise Refuse("no l_info validated from its own magic word")
    lin = magic_l[0]
    b0 = lin["b0"]
    sz_unc0, sz_cpr0 = struct.unpack_from("<II", d, b0)

    # 1. tamper: zero block0's sz_cpr only
    tampered = bytearray(d)
    struct.pack_into("<I", tampered, b0 + 4, 0)
    tampered = bytes(tampered)
    tp = os.path.join(workdir, name + ".tampered")
    with open(tp, "wb") as fh:
        fh.write(tampered)

    # 2. UPX's own verdict on the tampered file
    t_tampered = run([UPX, "-t", tp])

    # 3. independent derivation
    geo = derive(tampered, ph_off, ph, lin)

    # 4. ambiguity: does any *other* sentinel-reaching candidate also pass
    #    upx -t / upx -d ?
    amb = []
    if geo["chosen"] is not None:
        for i, c in enumerate(geo["candidates"]):
            dd = bytearray(tampered)
            struct.pack_into("<I", dd, b0 + 4, c["derived"])
            cp = os.path.join(workdir, f"{name}.cand{i}.s{c['derived']}")
            with open(cp, "wb") as fh:
                fh.write(bytes(dd))
            t = run([UPX, "-t", cp])
            entry = {"derived": c["derived"], "next_block": c["next_block"],
                     "chosen": i == 0, "upx_t_exit": t["exit"],
                     "upx_t_stderr": t["stderr"].splitlines()[-1:] if t["stderr"] else []}
            if t["exit"] == 0:
                dp = os.path.join(workdir, f"{name}.cand{i}.d")
                shutil.copyfile(cp, dp)
                u = run([UPX, "-d", "-o", dp + ".out", dp])
                entry["upx_d_exit"] = u["exit"]
                if u["exit"] == 0:
                    entry["restored_sha256"] = sha256(open(dp + ".out", "rb").read())
                    entry["restored_matches_orig"] = entry["restored_sha256"] == orig_sha
            amb.append(entry)

    # 5. winner validation
    win = None
    if geo["chosen"] is not None:
        wd = bytearray(tampered)
        struct.pack_into("<I", wd, b0 + 4, geo["chosen"]["derived"])
        wpath = os.path.join(workdir, name + ".derived")
        with open(wpath, "wb") as fh:
            fh.write(bytes(wd))
        t = run([UPX, "-t", wpath])
        wrec = {"derived": geo["chosen"]["derived"], "upx_t_exit": t["exit"],
                "upx_t_stderr": t["stderr"].splitlines()[-1:] if t["stderr"] else [],
                "byte_identical_to_packed": bytes(wd) == d,
                "only_szcpr_window_differs": bytes(wd) == d}
        if t["exit"] == 0:
            dw = os.path.join(workdir, name + ".derived.d")
            shutil.copyfile(wpath, dw)
            u = run([UPX, "-d", "-o", dw + ".out", dw])
            wrec["upx_d_exit"] = u["exit"]
            if u["exit"] == 0:
                rs = sha256(open(dw + ".out", "rb").read())
                wrec["restored_sha256"] = rs
                wrec["restored_matches_orig"] = rs == orig_sha
        win = wrec

    # 6. committed repair on the same tampered file
    committed = {"ran": False}
    if os.path.exists(repair_tool):
        out = os.path.join(workdir, name + ".committed")
        r = run([sys.executable, "-I", "-B", repair_tool, "--in", tp, "--out", out, "--json"])
        committed = {"ran": True, "exit": r["exit"], "stderr": r["stderr"]}
        if r["exit"] == 0:
            try:
                info = json.loads(r["stdout"])
                committed["class"] = info.get("class")
                committed["derived_sz_cpr"] = (info.get("geometry") or {}).get("derived_sz_cpr")
                committed["geometry"] = {k: v for k, v in (info.get("geometry") or {}).items()
                                         if k != "walk"}
            except json.JSONDecodeError:
                committed["parse_error"] = True
            committed["output_sha256"] = sha256(open(out, "rb").read())
            committed["output_byte_identical_to_packed"] = open(out, "rb").read() == d
    mine = geo["chosen"]["derived"] if geo["chosen"] else None
    return {"carrier": carrier, "name": name, "orig_sha256": orig_sha,
            "packed_sha256": sha256(d), "packed_size": len(d),
            "packheader": ph, "l_info": lin,
            "locator_agreement": ([x["l_magic"] for x in magic_l]
                                  == [x["l_magic"] for x in pfsize_l]),
            "linfo_count_magic": len(magic_l), "linfo_count_pfsize": len(pfsize_l),
            "block0": {"off": b0, "sz_unc": sz_unc0, "sz_cpr_intact": sz_cpr0},
            "tampered_sha256": sha256(tampered),
            "tampered_upx_t": {"exit": t_tampered["exit"],
                               "stderr": t_tampered["stderr"].splitlines()[-2:]},
            "geometry": {k: v for k, v in geo.items() if k != "candidates"},
            "candidates": geo["candidates"], "ambiguity": amb,
            "winner": win, "committed": committed,
            "agreement": (mine is not None and committed.get("derived_sz_cpr") == mine)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["inspect", "derive"])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--repair-tool", default="")
    a = ap.parse_args(argv)
    if a.mode == "inspect":
        print(json.dumps([inspect(p) for p in a.paths], indent=1, sort_keys=True))
        return 0
    if len(a.paths) != 2:
        print("derive needs <carrier> <workdir>", file=sys.stderr)
        return 2
    try:
        rec = derive_carrier(a.paths[0], a.paths[1], a.repair_tool)
    except Refuse as exc:
        print(json.dumps({"carrier": a.paths[0], "refused": str(exc)}))
        return 2
    print(json.dumps(rec, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
