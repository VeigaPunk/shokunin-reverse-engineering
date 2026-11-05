#!/usr/bin/env python3
"""derive-szcpr.py - ExecGeomIndep (round 89, kaidoku) independent derivation.

Re-derives block 0's `b_info.sz_cpr` from chain geometry, implemented from
scratch against the law stated in plans/round-89-claims.md and
corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md:

  block 0's `sz_cpr` is the distance from block 0's payload start
  (`b0 + 12`) to the next plausible `b_info` candidate whose chain reaches
  the end-of-chain sentinel, bounded by `sz_unc0`; among survivors the
  candidate accounting for the most of the PackHeader's declared `u_len`
  wins (key `(fits_u_len, total, -derived)`).

STORED-VALUE BLIND by construction: the stored 32-bit word at `b0 + 4` is
read exactly once, for the report only, and is never used in any gate, scan
bound, or walk.  The candidate walk runs on a copy with the derived value
written in, so no input variant (intact / 0 / true-8 / 0xFFFFFFF0) can
influence the result.

Imports nothing from tools/round-87, round-88 or round-89; the PackHeader
locator is this file's own (tail-window `UPX!` scan + header checksum
`sum(bytes) % 251` + version/format/length sanity).  tools/round-87/
upx-magic-repair.py is used only by oracle-packheader.py, as an oracle.

CLI: --in FILE [--out FILE] [--json OUT] | --locate FILE
Exit: 0 derived; 2 refused (typed, stderr).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys

MAGIC = b"UPX!"
PH_SIZE = 32
TAIL_WINDOW = 512
MAX_INPUT = 256 << 20


class Refused(Exception):
    pass


def u32(buf: bytes, off: int) -> int:
    return struct.unpack_from("<I", buf, off)[0]


def ph_checksum(head: bytes) -> int:
    """UPX PackHeader header checksum: sum of bytes 4..30 modulo 251."""
    return sum(head[4:PH_SIZE - 1]) % 251


def find_packheader(d: bytes) -> tuple[int, dict]:
    """Own locator: every `UPX!` word in the tail window whose 32 bytes
    validate (version >= 10, non-DOS format, checksum, positive lengths);
    the word nearest the end of file wins."""
    n = len(d)
    lo = max(0, n - TAIL_WINDOW)
    valid = []
    o = d.rfind(MAGIC, lo, n - PH_SIZE + 1)
    while o != -1:
        head = d[o:o + PH_SIZE]
        if (len(head) == PH_SIZE and head[4] >= 10
                and head[5] not in (1, 2, 3, 4) and head[5] < 128
                and head[PH_SIZE - 1] == ph_checksum(head)):
            u_len, c_len, u_file_size = struct.unpack_from("<III", head, 16)
            if 0 < c_len <= n and 0 < u_len and 0 < u_file_size:
                valid.append((o, {"version": head[4], "format": head[5],
                                  "method": head[6], "level": head[7],
                                  "u_len": u_len, "c_len": c_len,
                                  "u_file_size": u_file_size}))
        o = d.rfind(MAGIC, lo, o)
    if not valid:
        raise Refused("no PackHeader validated in the tail window")
    off, ph = valid[0]
    return off, ph


def lmagic_candidates(d: bytes, ph_off: int, ph: dict) -> list[int]:
    """Own locator: every `p_filesize == PackHeader.u_file_size` occurrence
    whose l_info anchor validates.  Layout from l_magic: magic 0-3, l_lsize
    4-5, l_version 6, l_format 7, p_progid 8-11, p_filesize 12-15, block0 at 20.
    The returned offset is the l_magic offset (block 0 = offset + 20)."""
    want = struct.pack("<I", ph["u_file_size"])
    out, p = [], d.find(want, 12)
    while p != -1 and p < ph_off:
        lm = p - 12  # p_filesize sits 12 bytes after l_magic
        if (lm >= 4 and lm + 20 <= ph_off and d[lm:lm + 4] == MAGIC
                and d[lm + 6] == ph["version"] and d[lm + 7] == ph["format"]):
            out.append(lm)
        p = d.find(want, p + 1)
    return out


def is_sentinel(d: bytes, s: int, ph_off: int) -> bool:
    """End-of-chain b_info: sz_unc == 0 and method/ftid/cto8/unused == 0."""
    return (0 <= s and s + 12 <= ph_off
            and d[s:s + 4] == b"\0\0\0\0" and d[s + 8:s + 12] == b"\0\0\0\0")


def walk_segment(d: bytes, start: int, end: int, methods: frozenset,
                 stats: dict) -> tuple[int, int, int]:
    """One contiguous b_info segment: (stop, blocks, sum of sz_unc)."""
    q, n, total = start, 0, 0
    while q + 12 <= end:
        stats["walk_steps"] += 1
        sz_unc, sz_cpr = u32(d, q), u32(d, q + 4)
        if (sz_unc == 0 or sz_cpr == 0 or sz_cpr > sz_unc
                or q + 12 + sz_cpr > end or d[q + 8] not in methods):
            break
        q += 12 + sz_cpr
        n += 1
        total += sz_unc
    return q, n, total


def reach_sentinel(d: bytes, start: int, ph_off: int, methods: frozenset,
                   stats: dict) -> dict | None:
    """Reach the end-of-chain sentinel from `start`: contiguous walk first;
    where the chain stops at the embedded loader, resume at a later plausible
    b_info whose own chain reaches a sentinel.  A sentinel whose sz_cpr word
    already reads `UPX!` wins, else the sentinel nearest the PackHeader."""
    stop, n1, _t = walk_segment(d, start, ph_off, methods, stats)
    if n1 == 0:
        return None
    if is_sentinel(d, stop, ph_off):
        return {"end": stop, "resume": None, "blocks_first": n1,
                "blocks_resumed": 0}
    memo: dict[int, tuple[int, int]] = {}

    def walk_memo(s: int) -> tuple[int, int]:
        path, q = [], s
        while q not in memo:
            if q + 12 > ph_off:
                break
            sz_unc, sz_cpr = u32(d, q), u32(d, q + 4)
            if (sz_unc == 0 or sz_cpr == 0 or sz_cpr > sz_unc
                    or q + 12 + sz_cpr > ph_off or d[q + 8] not in methods):
                break
            stats["walk_steps"] += 1
            path.append(q)
            q += 12 + sz_cpr
        end, n = memo.get(q, (q, 0))
        for k, p in enumerate(reversed(path), 1):
            memo[p] = (end, n + k)
        return memo.get(s, (s, 0))

    best = None
    for s in range(stop + 1, ph_off - 12):
        stats["resume_candidates"] += 1
        sz_unc, sz_cpr = u32(d, s), u32(d, s + 4)
        if (not (0 < sz_cpr < sz_unc) or d[s + 8] not in methods
                or d[s + 9] or d[s + 10]):
            continue
        end, n2 = walk_memo(s)
        if n2 and is_sentinel(d, end, ph_off):
            key = (d[end + 4:end + 8] == MAGIC, end)
            if best is None or key > best[0]:
                best = (key, end, s, n2)
    if best is None:
        return None
    _key, end, s, n2 = best
    return {"end": end, "resume": s, "blocks_first": n1, "blocks_resumed": n2}


def derive(d: bytes) -> tuple[dict, dict, tuple[int, dict]]:
    """Derive block 0's sz_cpr.  Returns (record, stats, (ph_off, ph))."""
    stats = {"lmagic_candidates": 0, "scan_offsets": 0, "plausible_next": 0,
             "sentinel_survivors": 0, "walk_steps": 0, "resume_candidates": 0}
    ph_off, ph = find_packheader(d)
    survivors = []
    best_key, best = None, None
    last = "no l_info candidate carries a derivable first block"
    for lm in lmagic_candidates(d, ph_off, ph):
        stats["lmagic_candidates"] += 1
        b0 = lm + 20
        if b0 + 12 > ph_off:
            continue
        sz_unc0, stored = u32(d, b0), u32(d, b0 + 4)
        if sz_unc0 == 0:
            continue
        m0 = d[b0 + 8]
        methods = frozenset((m0, ph["method"]))
        for s1 in range(b0 + 13, ph_off - 12):
            stats["scan_offsets"] += 1
            su, sc = u32(d, s1), u32(d, s1 + 4)
            if (not (0 < sc <= su) or s1 + 12 + sc > ph_off
                    or d[s1 + 8] not in methods):
                continue
            stats["plausible_next"] += 1
            derived = s1 - (b0 + 12)
            if not (0 < derived <= sz_unc0):
                continue
            dd = bytearray(d)
            pass  # MUTANT: stored value left in place (walk reads it)
            walk = reach_sentinel(bytes(dd), b0, ph_off, methods, stats)
            if walk is None:
                continue
            stats["sentinel_survivors"] += 1
            _stop, n, total = walk_segment(dd, b0, ph_off, methods, stats)
            resumed = 0
            if walk["resume"] is not None:
                _q, n2, su2 = walk_segment(dd, walk["resume"], ph_off,
                                           methods, stats)
                total += su2
                resumed = n2
            fits = total <= ph["u_len"]
            rec = {"l_magic": lm, "block0": b0, "block0_sz_unc": sz_unc0,
                   "stored_sz_cpr": stored, "derived_sz_cpr": derived,
                   "next_block": s1, "sentinel": walk["end"],
                   "blocks_first": walk["blocks_first"],
                   "blocks_resumed": resumed,
                   "uncompressed_accounted": total, "u_len": ph["u_len"],
                   "fits_u_len": fits}
            survivors.append(rec)
            key = (fits, total, -derived)
            if best_key is None or key > best_key:
                best_key, best = key, rec
    if best is None:
        raise Refused(last)
    return best, survivors, stats, (ph_off, ph)


def locate(d: bytes) -> dict:
    """Locator-only view (used to build tamper variants)."""
    rec, _surv, stats, (ph_off, ph) = derive(d)
    return {"packheader_off": ph_off, "packheader": ph, **rec, "stats": stats}


def classify(stored: int, derived: int) -> str:
    if stored == derived:
        return "intact"
    if stored == 0:
        return "chain-geometry"
    if stored == 0xFFFFFFF0:
        return "field-value-outofrange"
    return "field-value"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst")
    ap.add_argument("--json", dest="jsn")
    ap.add_argument("--locate", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.src, "rb") as fh:
            d = fh.read()
    except OSError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    if len(d) > MAX_INPUT:
        print(f"refused: input larger than {MAX_INPUT} bytes", file=sys.stderr)
        return 2
    if a.locate:
        print(json.dumps(locate(d), indent=1, sort_keys=True))
        return 0
    try:
        rec, survivors, stats, (ph_off, ph) = derive(d)
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    out = d
    if rec["stored_sz_cpr"] != rec["derived_sz_cpr"]:
        out = bytearray(d)
        struct.pack_into("<I", out, rec["block0"] + 4, rec["derived_sz_cpr"])
        out = bytes(out)
    if a.dst:
        with open(a.dst, "wb") as fh:
            fh.write(out)
    summary = {"input_sha256": hashlib.sha256(d).hexdigest(),
               "output_sha256": hashlib.sha256(out).hexdigest(),
               "class": classify(rec["stored_sz_cpr"], rec["derived_sz_cpr"]),
               "stored_sz_cpr": rec["stored_sz_cpr"],
               "derived_sz_cpr": rec["derived_sz_cpr"],
               "changed": out != d, **rec, "stats": stats,
               "survivors": survivors}
    if a.jsn:
        with open(a.jsn, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=1, sort_keys=True)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
