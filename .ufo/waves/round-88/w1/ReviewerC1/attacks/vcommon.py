"""ReviewerC1 cheap-rule variants for R88-C1 (scratch only, not part of the lane).

Each rule is composed with the frozen round-87 anchor repair exactly like the
claimed repair composes it: try rep.repair(d) first; if it refuses, derive the
zeroed first-block sz_cpr by the rule, patch those 4 bytes, then rep.repair
again.  Only rules R1-R6 differ in the derivation; R7 is the upx-in-the-loop
oracle.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import struct
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R87 = os.path.join(LANE, "tools", "round-87", "upx-magic-repair.py")


def load_r87():
    spec = importlib.util.spec_from_file_location("r87repair", R87)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Refused(Exception):
    pass


def l_info_candidates(d: bytes, ph_off: int, ph: dict) -> list[int]:
    """Claimed repair's own candidate locator (version/format match only)."""
    want = struct.pack("<I", ph["u_file_size"])
    found, p = [], d.find(want, 12)
    while p != -1 and p < ph_off:
        m = p - 12
        if m >= 4 and m + 32 <= ph_off and d[m + 6] == ph["version"] \
                and d[m + 7] == ph["format"]:
            found.append(m)
        p = d.find(want, p + 1)
    return found


def seg_total(d: bytes, start: int, end: int, m0: int, alt: int | None):
    q, n, total = start, 0, 0
    while q + 12 <= end:
        sz_unc, sz_cpr = struct.unpack_from("<II", d, q)
        if (sz_unc == 0 or sz_cpr == 0 or sz_cpr > sz_unc
                or q + 12 + sz_cpr > end or d[q + 8] not in (m0, alt)):
            break
        q += 12 + sz_cpr
        n += 1
        total += sz_unc
    return q, n, total


def derive(rule: str, d: bytes, rep):
    ph_off, ph = rep.find_packheader(d)
    m0list = l_info_candidates(d, ph_off, ph)
    if rule == "R4-pblocksize":
        for m in m0list:
            b0 = m + 20
            sz_unc0, sz_cpr0 = struct.unpack_from("<II", d, b0)
            if sz_cpr0 != 0 or sz_unc0 == 0:
                continue
            val = struct.unpack_from("<I", d, m + 16)[0]  # p_info.p_blocksize
            dd = bytearray(d)
            struct.pack_into("<I", dd, b0 + 4, val)
            return bytes(dd), {"rule": rule, "derived_sz_cpr": val,
                               "p_blocksize": val, "l_info": m}
        raise Refused("no repairable first block")
    if rule == "R5-clen-12n":
        for m in m0list:
            b0 = m + 20
            sz_unc0, sz_cpr0 = struct.unpack_from("<II", d, b0)
            if sz_cpr0 != 0 or sz_unc0 == 0:
                continue
            m0 = d[b0 + 8]
            _q, n2, _t = seg_total(d, b0 + 12, ph_off, m0, ph["method"])
            blocks = 1 + n2
            val = ph["c_len"] - 12 * blocks
            dd = bytearray(d)
            struct.pack_into("<I", dd, b0 + 4, val & 0xFFFFFFFF)
            return bytes(dd), {"rule": rule, "derived_sz_cpr": val,
                               "c_len": ph["c_len"], "blocks": blocks}
        raise Refused("no repairable first block")
    if rule == "R7-oracle":
        for m in m0list:
            b0 = m + 20
            sz_unc0, sz_cpr0 = struct.unpack_from("<II", d, b0)
            if sz_cpr0 != 0 or sz_unc0 == 0:
                continue
            m0 = d[b0 + 8]
            tried = 0
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
                tried += 1
                with tempfile.NamedTemporaryFile(suffix=".elf", delete=False) as tf:
                    tf.write(bytes(dd))
                    probe_path = tf.name
                try:
                    r = subprocess.run(["upx", "-t", "-q", probe_path],
                                       capture_output=True, timeout=60)
                    if r.returncode == 0:
                        return bytes(dd), {"rule": rule, "derived_sz_cpr": derived,
                                           "oracle_trials": tried}
                finally:
                    os.unlink(probe_path)
            raise Refused(f"oracle: no candidate passes upx -t ({tried} tried)")
        raise Refused("no repairable first block")
    # R1/R2/R3/R6 share the structural candidate scan
    if rule == "R6-global-scanfill":
        lo, hi = None, None  # whole-file bounds, no method constraint applied later
    best = None
    for m in m0list:
        b0 = m + 20
        sz_unc0, sz_cpr0 = struct.unpack_from("<II", d, b0)
        if sz_cpr0 != 0 or sz_unc0 == 0:
            continue
        m0 = d[b0 + 8]
        s_lo = b0 + 13
        s_hi = (len(d) - 12) if rule == "R6-global-scanfill" else (ph_off - 12)
        for s1 in range(s_lo, s_hi):
            su, sc = struct.unpack_from("<II", d, s1)
            if not (0 < sc <= su) or s1 + 12 + sc > (len(d) - 12 if rule == "R6-global-scanfill" else ph_off):
                continue
            if rule != "R6-global-scanfill" and d[s1 + 8] not in (m0, ph["method"]):
                continue
            derived = s1 - (b0 + 12)
            if not (0 < derived <= sz_unc0):
                continue
            if rule == "R1-first-plausible":
                return _fill(d, b0, derived, rule)
            if rule == "R2-ulen-no-sentinel":
                dd = bytearray(d)
                struct.pack_into("<I", dd, b0 + 4, derived)
                stop, n, total = seg_total(bytes(dd), b0, ph_off, m0, ph["method"])
                fits = total <= ph["u_len"]
                key = (fits, total, -derived)
                if best is None or key > best[0]:
                    best = (key, bytes(dd), {"rule": rule, "derived_sz_cpr": derived,
                                             "uncompressed_accounted": total,
                                             "fits_u_len": fits})
                break  # claimed scans all l_infos; one is enough for the probe here
            if rule == "R3-sentinel-only-smallest":
                dd = bytearray(d)
                struct.pack_into("<I", dd, b0 + 4, derived)
                try:
                    rep.find_sentinel(bytes(dd), b0, ph_off, ph["method"])
                except rep.Refused:
                    continue
                return _fill(d, b0, derived, rule)
            if rule == "R6-global-scanfill":
                return _fill(d, b0, derived, rule)
    if best is not None:
        return best[1], best[2]
    raise Refused(f"{rule}: no candidate")


def _fill(d, b0, derived, rule):
    dd = bytearray(d)
    struct.pack_into("<I", dd, b0 + 4, derived)
    return bytes(dd), {"rule": rule, "derived_sz_cpr": derived}


def repair(rule: str, d: bytes):
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise Refused("not a little-endian ELF")
    rep = load_r87()
    try:
        out, info = rep.repair(d)
        info["class"] = "anchor" if not info.get("intact") else "intact"
        return out, info
    except rep.Refused as anchor_refusal:
        try:
            g_out, g_info = derive(rule, d, rep)
        except rep.Refused as geo_refusal:
            raise Refused(f"{anchor_refusal}; {geo_refusal}")
        out, info = rep.repair(g_out)
        info["class"] = f"cheap-{rule}"
        info["geometry"] = g_info
        return out, info


def main(rule: str, argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.inp, "rb") as fh:
        d = fh.read()
    try:
        out, info = repair(rule, d)
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    with open(a.out, "wb") as fh:
        fh.write(out)
    if a.json:
        print(json.dumps(info, indent=1, sort_keys=True))
    return 0
