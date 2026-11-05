#!/usr/bin/env python3
"""szcpr_law.py - independent derivation of the round-90 law for an interior
first-segment b_info.sz_cpr (class T5-chain-szcpr-wrong-later).

Seat ExecDeriveIndep, wave r90-w1, round 90 (kaidoku).  Written from scratch
for this seat; it imports neither tools/round-87 nor tools/round-88 nor
tools/round-90.  It re-uses only the file-layout conventions those tools
document, re-implemented here:

  m+0   l_info.l_magic  "UPX!"
  m+6   l_info.l_version, l_info.l_format      (match the PackHeader)
  m+12  p_info (p_progid, p_filesize, p_blocksize); p_filesize == the
        PackHeader's u_file_size, and that equality is the locator anchor
  m+20  first b_info of the chain

Each b_info is 12 bytes: sz_unc u32, sz_cpr u32, b_method u8, b_ftid u8,
b_cto8 u8, b_unused u8.  A block's successor starts at pos + 12 + sz_cpr.
The chain is interrupted by an embedded loader (the first-segment stop) and
resumes at a later offset whose own walk ends in an end-of-chain sentinel
(sz_unc == 0, b_method..b_unused == 0) before the PackHeader.  The PackHeader
(32 bytes, validated by sum(buf[4:31]) % 251 == buf[31], near EOF) declares
u_len, the uncompressed length the chain must account.

THE LAW (derived here, tested in ExecDeriveIndep.md): a block at pos whose
stored sz_cpr breaks the chain is justified by exactly one value,

    sz_cpr = s - (pos + 12),

where s is the successor block's position.  A candidate successor s is
accepted only when, with that value written, the whole chain (first segment
plus loader resume) ends in the end-of-chain sentinel, the uncompressed bytes
it accounts equal the declared u_len EXACTLY, and they strictly exceed what
the stored chain accounts.  The filter is a filter, not a rank key: it must
leave exactly one candidate.  Zero candidates (a chain that can never cover
u_len) or more than one (the last block before a stop, where every in-range
value leaves the same accounting) leave the bytes unchanged - never a guess.

CLI:
  szcpr_law.py dump        --in F [--json]
  szcpr_law.py repair      --in F --out G [--json]
  szcpr_law.py derivations --in F --block-offset N [--derived V,V,...] [--json]

Exit: 0 a verdict was produced (G written; byte-identical when unchanged);
2 refused (not a little-endian ELF, no validated PackHeader, no anchored
l_info whose chain reaches a sentinel).  The tool reads only --in; it never
runs the packer.
"""

from __future__ import annotations

import argparse
import bisect
import json
import struct
import sys
import time

MAGIC = b"UPX!"
PH_SIZE = 32
TAIL_WINDOW = 512           # PackHeader search window from the end of file
MAX_BLOCKS = 1 << 16
MAX_INPUT = 256 << 20


class Refused(Exception):
    pass


# ---------------------------------------------------------------- location

def ph_checksum(buf: bytes) -> int:
    return sum(buf[4:PH_SIZE - 1]) % 251


def find_packheader(d: bytes) -> tuple[int, dict]:
    """Last offset in the tail window whose 32 bytes validate as a PackHeader."""
    n = len(d)
    lo = max(0, n - TAIL_WINDOW)
    for o in range(n - PH_SIZE, lo - 1, -1):
        h = d[o:o + PH_SIZE]
        version, fmt = h[4], h[5]
        if version < 10 or fmt >= 128 or fmt in (1, 2, 3, 4):
            continue
        if h[PH_SIZE - 1] != ph_checksum(h):
            continue
        u_len, c_len, u_file_size = struct.unpack_from("<III", h, 16)
        if not (0 < c_len <= n and 0 < u_len and 0 < u_file_size):
            continue
        return o, {"version": version, "format": fmt, "method": h[6],
                   "level": h[7], "u_len": u_len, "c_len": c_len,
                   "u_file_size": u_file_size}
    raise Refused("no validated PackHeader in the tail window")


def l_info_candidates(d: bytes, ph_off: int, ph: dict) -> list[int]:
    """Offsets of an l_info magic word whose version/format match the
    PackHeader and whose p_info carries the PackHeader's u_file_size."""
    want = struct.pack("<I", ph["u_file_size"])
    found, p = [], d.find(want, 12)
    while p != -1 and p < ph_off:
        m = p - 12
        if m >= 4 and m + 32 <= ph_off and d[m + 6] == ph["version"] \
                and d[m + 7] == ph["format"]:
            found.append(m)
        p = d.find(want, p + 1)
    return found


# --------------------------------------------------------------- chain walk

def walk_first(d: bytes, start: int, end: int,
               alt: int | None) -> tuple[int, list, int | None]:
    """Walk contiguous b_info blocks from `start`, capturing the first block's
    method; later blocks must match it or `alt`.  Returns (stop, blocks,
    method); blocks are (off, sz_unc, sz_cpr)."""
    q, blocks, method = start, [], None
    for _ in range(MAX_BLOCKS):
        if q < 0 or q + 12 > end:
            break
        sz_unc, sz_cpr = struct.unpack_from("<II", d, q)
        meth = d[q + 8]
        if sz_unc == 0 or sz_cpr == 0 or sz_cpr > sz_unc \
                or q + 12 + sz_cpr > end:
            break
        if method is None:
            method = meth
        elif meth != method and meth != alt:
            break
        blocks.append((q, sz_unc, sz_cpr))
        q += 12 + sz_cpr
    return q, blocks, method


def walk_with(d: bytes, start: int, end: int, methods: set) -> tuple[int, list]:
    q, blocks = start, []
    for _ in range(MAX_BLOCKS):
        if q < 0 or q + 12 > end:
            break
        sz_unc, sz_cpr = struct.unpack_from("<II", d, q)
        if (sz_unc == 0 or sz_cpr == 0 or sz_cpr > sz_unc
                or q + 12 + sz_cpr > end or d[q + 8] not in methods):
            break
        blocks.append((q, sz_unc, sz_cpr))
        q += 12 + sz_cpr
    return q, blocks


def is_sentinel(d: bytes, s: int, ph_off: int) -> bool:
    if s < 0 or s + 12 > ph_off:
        return False
    return d[s:s + 4] == b"\0\0\0\0" and d[s + 8:s + 12] == b"\0\0\0\0"


class TailIndex:
    """The loader-resume scan, precomputed once per file.

    A resume candidate is a position s whose b_info is plausible with
    0 < sz_cpr < sz_unc (strict), b_ftid == 0 and b_cto8 == 0, whose own walk
    (blocks matching the segment method or the PackHeader method) advances at
    least one block and ends in an end-of-chain sentinel.  Scanning ascending
    and keeping a candidate only on a strictly greater key
    (sentinel sz_cpr field == "UPX!", sentinel offset) selects, among the
    candidates after any stop, the smallest position achieving the maximal
    key - here reduced to a suffix maximum, so a probe is O(log n)."""

    def __init__(self, d: bytes, first_pos: int, ph_off: int, methods: set):
        self.d, self.ph_off = d, ph_off
        memo: dict[int, tuple[int, int]] = {}

        def walk_from(s: int) -> tuple[int, int]:
            path, q = [], s
            while q not in memo:
                if q + 12 > ph_off:
                    break
                su, sc = struct.unpack_from("<II", d, q)
                if (su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off
                        or d[q + 8] not in methods):
                    break
                path.append(q)
                q += 12 + sc
            end, n = memo.get(q, (q, 0))
            for k, p in enumerate(reversed(path), 1):
                memo[p] = (end, n + k)
            return memo.get(s, (s, 0))

        pos, ends, keys, sums, nblocks = [], [], [], [], []
        for s in range(first_pos + 1, ph_off - 12):
            su, sc = struct.unpack_from("<II", d, s)
            if not (0 < sc < su) or s + 12 + sc > ph_off \
                    or d[s + 8] not in methods or d[s + 9] or d[s + 10]:
                continue
            end, n2 = walk_from(s)
            if not n2 or not is_sentinel(d, end, ph_off):
                continue
            stop2, blocks = walk_with(d, s, ph_off, methods)
            if not blocks or stop2 != end:
                continue
            pos.append(s)
            ends.append(end)
            keys.append((d[end + 4:end + 8] == MAGIC, end))
            sums.append(sum(b[1] for b in blocks))
            nblocks.append(len(blocks))
        n = len(pos)
        self.pos, self.ends, self.keys = pos, ends, keys
        self.sums, self.nblocks = sums, nblocks
        self.sufkey = [None] * (n + 1)
        self.firstof = [n] * (n + 1)
        for i in range(n - 1, -1, -1):
            if self.sufkey[i + 1] is None or keys[i] > self.sufkey[i + 1]:
                self.sufkey[i], self.firstof[i] = keys[i], i
            elif keys[i] == self.sufkey[i + 1]:
                self.sufkey[i], self.firstof[i] = keys[i], i
            else:
                self.sufkey[i], self.firstof[i] = self.sufkey[i + 1], self.firstof[i + 1]

    def probe(self, stop: int):
        """Best resume candidate strictly after `stop`:
        (resume_pos, sentinel, resumed_sum, resumed_block_count) or None."""
        i = bisect.bisect_right(self.pos, stop)
        if i >= len(self.pos) or self.sufkey[i] is None:
            return None
        j = self.firstof[i]
        return self.pos[j], self.ends[j], self.sums[j], self.nblocks[j]


# ------------------------------------------------------------------ analysis

def analyze(d: bytes) -> dict:
    """Locate the packed image and probe the stored chain."""
    ph_off, ph = find_packheader(d)
    last = "no anchored l_info carries a walkable chain"
    for m in l_info_candidates(d, ph_off, ph):
        b0 = m + 20
        stop, blocks, method = walk_first(d, b0, ph_off, ph["method"])
        if not blocks or method is None:
            last = f"l_info@{m}: p_info is not followed by a plausible b_info"
            continue
        tail = TailIndex(d, b0, ph_off, (method, ph["method"]))
        total = sum(b[1] for b in blocks)
        if is_sentinel(d, stop, ph_off):
            stored = {"resume": None, "sentinel": stop, "total": total,
                      "blocks_first": len(blocks), "blocks_resumed": 0}
        else:
            r = tail.probe(stop)
            if r is None:
                last = f"l_info@{m}: b_info chain does not reach a sentinel"
                continue
            resume, end, res_sum, n_res = r
            stored = {"resume": resume, "sentinel": end,
                      "total": total + res_sum, "blocks_first": len(blocks),
                      "blocks_resumed": n_res, "res_sum": res_sum}
        return {"ph_off": ph_off, "ph": ph, "l_info": m, "b0": b0,
                "stop": stop, "blocks": blocks, "method": method,
                "tail": tail, "stored": stored}
    raise Refused(last)


def _patched_probe(info: dict, d: bytes, t_off: int, derived: int):
    """Probe the file with block t_off's sz_cpr forced to `derived`:
    (walk_stop, first_blocks, total or None)."""
    ph_off, ph, b0 = info["ph_off"], info["ph"], info["b0"]
    dd = bytearray(d)
    struct.pack_into("<I", dd, t_off + 4, derived)
    stop2, blocks2, _ = walk_first(bytes(dd), b0, ph_off, ph["method"])
    total2 = sum(b[1] for b in blocks2)
    r2 = info["tail"].probe(stop2)
    if r2 is None:
        return stop2, blocks2, None
    _res, _end, res_sum2, _n2 = r2
    return stop2, blocks2, total2 + res_sum2


# ---------------------------------------------------------------- the law

def repair_law(d: bytes) -> tuple[bytes, dict]:
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise Refused("not a little-endian ELF")
    if len(d) > MAX_INPUT:
        raise Refused("input cap")
    t0 = time.perf_counter()
    info = analyze(d)
    ph_off, ph = info["ph_off"], info["ph"]
    u_len = ph["u_len"]
    stored = info["stored"]
    base = {"u_len": u_len, "stored_total": stored["total"],
            "l_info": info["l_info"], "first_block": info["b0"],
            "blocks_first": stored["blocks_first"],
            "first_stop": info["stop"], "resume": stored["resume"],
            "sentinel": stored["sentinel"],
            "covers_u_len_stored": stored["total"] == u_len}
    if stored["total"] == u_len:
        return d, {"verdict": "unchanged-intact",
                   "reason": "stored chain reaches the sentinel and accounts exactly u_len",
                   **base, "elapsed_s": round(time.perf_counter() - t0, 3)}
    accepted, tried = [], 0
    cum = 0
    for t_off, t_unc, t_cpr in info["blocks"]:
        cum += t_unc
        lo = t_off + 13
        hi = min(ph_off - 12, t_off + 12 + t_unc) + 1
        for s in range(lo, hi):
            su, sc = struct.unpack_from("<II", d, s)
            if not (0 < sc <= su) or s + 12 + sc > ph_off \
                    or d[s + 8] not in (info["method"], ph["method"]):
                continue
            derived = s - (t_off + 12)
            if not (0 < derived <= t_unc):
                continue
            tried += 1
            stop2, blocks2, total2 = _patched_probe(info, d, t_off, derived)
            if total2 is None or not any(b[0] == t_off for b in blocks2):
                continue
            if total2 == u_len and total2 > stored["total"]:
                accepted.append({"block": t_off, "block_index":
                                 [b[0] for b in info["blocks"]].index(t_off),
                                 "derived": derived, "successor": s,
                                 "total": total2})
    out = d
    if len(accepted) == 1:
        a = accepted[0]
        buf = bytearray(d)
        struct.pack_into("<I", buf, a["block"] + 4, a["derived"])
        out = bytes(buf)
        verdict = {"verdict": "recovered", "patch": a, "candidates_tried": tried,
                   "accepted": 1, **base}
    elif accepted:
        verdict = {"verdict": "unchanged-ambiguous",
                   "reason": "more than one candidate accounts exactly u_len; "
                             "the last-block-before-a-stop under-determination",
                   "candidates": accepted[:16], "accepted": len(accepted),
                   "candidates_tried": tried, **base}
    elif stored["resume"] is not None:
        verdict = {"verdict": "unchanged-out-of-class",
                   "reason": "even a perfect chain accounts %d of %d u_len; the "
                             "exact-total rule cannot decide here" %
                             (stored["total"], u_len),
                   "candidates_tried": tried, "accepted": 0, **base}
    else:
        verdict = {"verdict": "unchanged-no-candidate",
                   "reason": "no candidate successor yields a sentinel-reaching "
                             "chain accounting exactly u_len",
                   "candidates_tried": tried, "accepted": 0, **base}
    verdict["elapsed_s"] = round(time.perf_counter() - t0, 3)
    return out, verdict


# ------------------------------------------------------------------ dump

def dump(d: bytes) -> dict:
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise Refused("not a little-endian ELF")
    ph_off, ph = find_packheader(d)
    last = "no anchored l_info carries a walkable chain"
    for m in l_info_candidates(d, ph_off, ph):
        b0 = m + 20
        stop, blocks, method = walk_first(d, b0, ph_off, ph["method"])
        if not blocks or method is None:
            last = f"l_info@{m}: no plausible first block"
            continue
        tail = TailIndex(d, b0, ph_off, (method, ph["method"]))
        total = sum(b[1] for b in blocks)
        if is_sentinel(d, stop, ph_off):
            resume, sentinel, res_sum, n_res = None, stop, 0, 0
        else:
            r = tail.probe(stop)
            if r is None:
                last = f"l_info@{m}: chain does not reach a sentinel"
                continue
            resume, sentinel, res_sum, n_res = r
        full = total + res_sum
        return {
            "ph": {"offset": ph_off, **ph},
            "l_info_magic": m, "p_info": m + 12, "first_block": b0,
            "first_segment": [{"index": i, "offset": off, "sz_unc": su,
                               "sz_cpr": sc}
                              for i, (off, su, sc) in enumerate(blocks)],
            "first_stop": stop,
            "blocks_first": len(blocks),
            "first_sum": total,
            "resume": resume, "blocks_resumed": n_res, "resumed_sum": res_sum,
            "sentinel": sentinel,
            "accounted_total": full, "u_len": ph["u_len"],
            "covers_full_u_len": full == ph["u_len"],
            "last_first_block": (lambda b: {"index": len(blocks) - 1,
                                            "offset": b[0], "sz_unc": b[1],
                                            "sz_cpr": b[2]})(blocks[-1]),
        }
    raise Refused(last)


def derivations(d: bytes, block_offset: int, values: list[int]) -> dict:
    """Accounting table: for each candidate sz_cpr value, what the chain
    accounts.  The decidability evidence: an interior block has exactly one
    value reaching u_len; the last block before a stop has many; an
    under-covering chain has none."""
    info = analyze(d)
    ph = info["ph"]
    u_len = ph["u_len"]
    hit = [b for b in info["blocks"] if b[0] == block_offset]
    if not hit:
        raise Refused("block_offset is not a block entered by the stored walk")
    t_off, t_unc, t_cpr = hit[0]
    lo, hi = 1, t_unc
    if values:
        vals = [v for v in values if lo <= v <= hi]
    else:
        vals = sorted({1, 2, max(1, t_cpr // 2), t_cpr - 7, t_cpr, t_cpr + 7,
                       t_unc - 1, t_unc} & set(range(lo, hi + 1)))
    rows = []
    for v in vals:
        stop2, blocks2, total2 = _patched_probe(info, d, t_off, v)
        rows.append({"derived": v, "is_stored": v == t_cpr,
                     "walk_stop": stop2, "total": total2,
                     "equals_u_len": total2 == u_len})
    n_deciding = sum(1 for r in rows if r["equals_u_len"])
    return {"block_offset": t_off, "block_index":
            [b[0] for b in info["blocks"]].index(t_off),
            "sz_unc": t_unc, "stored_sz_cpr": t_cpr, "u_len": u_len,
            "values_derived_reaching_u_len": n_deciding,
            "decidable": n_deciding == 1, "rows": rows}


# -------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("dump", "repair", "derivations"):
        sp = sub.add_parser(name)
        sp.add_argument("--in", dest="inp", required=True)
    sub.choices["repair"].add_argument("--out", required=True)
    sub.choices["derivations"].add_argument("--block-offset", type=int)
    sub.choices["derivations"].add_argument("--derived")
    for sp in sub.choices.values():
        sp.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.inp, "rb") as fh:
            d = fh.read()
        if a.cmd == "dump":
            out, info = None, dump(d)
        elif a.cmd == "derivations":
            vals = [int(x) for x in a.derived.split(",")] if a.derived else None
            out, info = None, derivations(d, a.block_offset, vals or [])
        else:
            out, info = repair_law(d)
            if a.out:
                with open(a.out, "wb") as fh:
                    fh.write(out)
    except Refused as exc:
        print(json.dumps({"refused": str(exc), "in": a.inp}))
        return 2
    print(json.dumps(info, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
