#!/usr/bin/env python3
"""upx-chain-repair.py - round-88 repair (R88-C1, coverage, capability).

The round-87 repair restores the three `UPX!` anchors of a magic-tampered UPX
5.2.0 little-endian ELF.  It cannot repair a *metadata* corruption: when the
first `b_info` block's `sz_cpr` (compressed length) is zeroed, its chain walk
cannot take a first step, and it refuses with
`p_info is not followed by a plausible b_info` while `upx -t` answers
`CantUnpackException: b_info corrupted`.

Recovery is chain geometry, not a magic word.  `b_info` blocks of a chain are
contiguous, so the next block starts exactly `12 + sz_cpr` bytes after this
one.  The repair searches, from the smallest offset above `block0 + 12`, for
bytes that form a plausible `b_info` under block0's method (or the
PackHeader's) whose own chain reaches the end-of-chain sentinel, derives
`sz_cpr = candidate - (block0 + 12)` and requires `0 < sz_cpr <= sz_unc`.
Candidates whose `l_info` carries `p_filesize == PackHeader.u_file_size` are
preferred (the field redundancy UPX itself writes for executables and shared
objects).  The restored file then goes through the round-87 anchor repair,
composed unchanged, so both classes are served by one command.

Composition is explicit and pinned: the round-87 module is imported by path
from this repo and its sha256 is recorded in every `--json` record.  This tool
never executes the input, never reads a carrier's source path, and only writes
the four bytes it derived.

Exit: 0 repaired or intact; 2 refused (typed, stderr); 1 unexpected.

--selftest runs the pure helpers on an in-memory fixture (no upx, no REA).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import stat
import struct
import sys

TOOL = "tools/round-88/upx-chain-repair.py"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPSTREAM = os.path.join(ROOT, "tools", "round-87", "upx-magic-repair.py")
MAX_INPUT = 256 << 20
MAGIC = b"UPX!"


class Refused(Exception):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_upstream(path: str = UPSTREAM):
    spec = importlib.util.spec_from_file_location("r87repair", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with open(path, "rb") as fh:
        digest = sha256_bytes(fh.read())
    return mod, digest


def l_info_candidates(d: bytes, ph_off: int, ph: dict) -> list[int]:
    """Every offset whose `u_file_size` bytes are followed by an l_info whose
    version/format bytes match the PackHeader (round-87's own locator law)."""
    want = struct.pack("<I", ph["u_file_size"])
    found, p = [], d.find(want, 12)
    while p != -1 and p < ph_off:
        m = p - 12
        if m >= 4 and m + 32 <= ph_off and d[m + 6] == ph["version"] \
                and d[m + 7] == ph["format"]:
            found.append(m)
        p = d.find(want, p + 1)
    return found


def segment(d: bytes, start: int, end: int, method: int, alt: int | None) -> tuple[int, int, int]:
    """Walk one contiguous b_info segment: (stop, blocks, sum of sz_unc)."""
    q, n, total = start, 0, 0
    while q + 12 <= end:
        sz_unc, sz_cpr = struct.unpack_from("<II", d, q)
        if (sz_unc == 0 or sz_cpr == 0 or sz_cpr > sz_unc
                or q + 12 + sz_cpr > end or d[q + 8] not in (method, alt)):
            break
        q += 12 + sz_cpr
        n += 1
        total += sz_unc
    return q, n, total


def geometry(d: bytes, rep) -> tuple[bytes, dict]:
    """Derive a zeroed first-block `sz_cpr` from chain geometry.

    The recovered geometry must account for the PackHeader's declared
    uncompressed length: no candidate may claim more than `u_len`, and among
    the survivors the one that accounts for the most declared bytes wins.  A
    shared object whose b_info chain does not cover the whole `u_len` (its
    appended data is not chain data) still yields its single structural
    candidate."""
    ph_off, ph = rep.find_packheader(d)
    best, last = None, "no l_info candidate carries a repairable first block"
    for m in l_info_candidates(d, ph_off, ph):
        b0 = m + 20
        sz_unc0, sz_cpr0 = struct.unpack_from("<II", d, b0)
        if sz_cpr0 != 0 or sz_unc0 == 0:
            continue
        m0 = d[b0 + 8]
        for s1 in range(b0 + 13, ph_off - 12):
            su, sc = struct.unpack_from("<II", d, s1)
            if not (0 < sc <= su) or s1 + 12 + sc > ph_off \
                    or d[s1 + 8] not in (m0, ph["method"]):
                continue
            derived = s1 - (b0 + 12)
            if not (0 < derived <= sz_unc0):
                continue
            dd = bytearray(d)
            struct.pack_into("<I", dd, b0 + 4, derived)
            try:
                end, info = rep.find_sentinel(bytes(dd), b0, ph_off, ph["method"])
            except rep.Refused:
                continue
            stop, n, total = segment(dd, b0, ph_off, m0, ph["method"])
            resumed = 0
            if info["resume"] is not None:
                _q, n2, su2 = segment(dd, info["resume"], ph_off, m0, ph["method"])
                total += su2
                resumed = n2
            if total > ph["u_len"]:
                fits = False
            else:
                fits = True
            key = (fits, total, -derived)
            rec = {"l_info": m, "block0": b0, "block0_sz_unc": sz_unc0,
                   "derived_sz_cpr": derived, "next_block": s1, "sentinel": end,
                   "blocks_first": n, "blocks_resumed": resumed,
                   "uncompressed_accounted": total, "u_len": ph["u_len"],
                   "fits_u_len": fits,
                   "walk": info}
            if best is None or key > best[0]:
                best = (key, bytes(dd), rec)
    if best is None:
        raise Refused(last)
    return best[1], best[2]


def repair(d: bytes) -> tuple[bytes, dict]:
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise Refused("not a little-endian ELF")
    rep, digest = load_upstream()
    try:
        out, info = rep.repair(d)
        info["class"] = "anchor" if not info.get("intact") else "intact"
        info["upstream_sha256"] = digest
        return out, info
    except rep.Refused as anchor_refusal:
        try:
            g_out, g_info = geometry(d, rep)
        except rep.Refused as geo_refusal:
            raise Refused(f"{anchor_refusal}; {geo_refusal}")
        out, info = rep.repair(g_out)
        info["class"] = "chain-geometry"
        info["upstream_sha256"] = digest
        info["geometry"] = g_info
        info["anchor_refusal"] = str(anchor_refusal)
        return out, info


def _fixture(sz_cpr0: int | None = None) -> bytes:
    """The round-87 synthetic image (l_info, p_info, a 2-block chain, a
    sentinel, a PackHeader) with block0's sz_cpr optionally zeroed."""
    rep, _ = load_upstream()
    clean = rep._fixture()
    if sz_cpr0 is None:
        return clean
    ph_off, ph = rep.find_packheader(clean)
    m, _s, _w = rep.find_linfo(clean, ph_off, ph)
    b0 = m + 20
    out = bytearray(clean)
    struct.pack_into("<I", out, b0 + 4, sz_cpr0)
    return bytes(out)


def selftest() -> int:
    rep, _ = load_upstream()
    fails, ncases = [], 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    def refuses(name, data):
        nonlocal ncases
        ncases += 1
        try:
            repair(data)
        except Refused:
            return
        fails.append(name)

    clean = _fixture()
    out, info = repair(clean)
    check("intact-idempotent", out == clean and info["class"] == "intact")

    zeroed = _fixture(0)
    out, info = repair(zeroed)
    check("chain-geometry-recovers", out == clean and info["class"] == "chain-geometry")
    check("derived-value", info["geometry"]["derived_sz_cpr"] == 40)
    check("geometry-records-u_len", info["geometry"]["uncompressed_accounted"] == 200
          and info["geometry"]["u_len"] == 64)

    # anchor class still served by the composed repair
    anchored = clean.replace(MAGIC, b"KDK!")
    out, info = repair(anchored)
    check("anchor-class-composed", out == clean and info["class"] == "anchor"
          and len(info["restored"]) == 3)

    # out of population: no PackHeader, no ELF, empty
    refuses("no-packheader", clean[:96])
    refuses("not-elf", b"MZ" + b"\0" * 200)
    refuses("zero-length", b"")
    # disclosed limit: a non-zero but wrong sz_cpr is *not* derived - the
    # composed repair leaves the bytes alone (the counter's `upx -t` arm, not
    # this tool, refuses such a file)
    wrong = _fixture(7)
    out, info = repair(wrong)
    check("szcpr-nonzero-not-derived", out == wrong and "geometry" not in info)
    check("input-cap", MAX_INPUT == 256 << 20)
    check("upstream-pinned", len(load_upstream()[1]) == 64)
    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.inp or not a.out:
        print("refused: --in and --out are required", file=sys.stderr)
        return 2
    try:
        st = os.stat(a.inp)
        if not stat.S_ISREG(st.st_mode):
            raise Refused(f"--in is not a regular file: {a.inp}")
        if st.st_size > MAX_INPUT:
            raise Refused(f"--in exceeds {MAX_INPUT} bytes")
        with open(a.inp, "rb") as fh:
            data = fh.read(MAX_INPUT + 1)
        out, info = repair(data)
        with open(a.out, "wb") as fh:
            fh.write(out)
    except (Refused, OSError) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(info, sort_keys=True))
    else:
        print(f"{info['class']}: restored {len(info.get('restored', []))} anchor(s)"
              f"{' derived sz_cpr ' + str(info['geometry']['derived_sz_cpr']) if info.get('geometry') else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
