#!/usr/bin/env python3
"""upx-field-value-repair.py - round-89 repair (R89-C1, coverage, capability).

Class `T4-chain-szcpr-wrong`: block 0's `b_info.sz_cpr` holds an in-range but
WRONG value.  Every bound the packer applies to that field (`0 < sz_cpr <=
sz_unc`, `sz_cpr` inside the tail window) passes, so the packer's arithmetic
gate stays silent and the refusal surfaces only at the payload stage
(`compressed data violation`).  The round-88 repair cannot see the class: it
enters the geometry walk only when the stored value is zero, and its round-87
anchor path treats an intact magic as `intact` and returns the input unchanged.

The derivation is the round-88 chain-geometry law, stored-value blind: the first
block's `sz_cpr` is the distance from block 0's payload start to the next
`b_info` candidate, bounded by `sz_unc0`, and among the survivors the candidate
that accounts for the most declared `u_len` wins (`(fits_u_len, total,
-derived)`, S309).  A stored value equal to the derived one is `intact` and the
input is returned byte-identical; any other stored value is corrected.

Refusals: not a little-endian ELF; no validated PackHeader; no l_info candidate
whose first block has a derivable geometry (a corrupted payload breaks the walk,
which is the guard the class relies on).

Composition: the packer's locator law and the chain walk come from
`tools/round-87/upx-magic-repair.py` and `tools/round-88/upx-chain-repair.py`,
both loaded by path and pinned by sha256 in the receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import struct
import sys

TOOL = "tools/round-89/upx-field-value-repair.py"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R87 = os.path.join(ROOT, "tools", "round-87", "upx-magic-repair.py")
R88 = os.path.join(ROOT, "tools", "round-88", "upx-chain-repair.py")
MAX_INPUT = 256 << 20
CLASS = "T4-chain-szcpr-wrong"


class Refused(Exception):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with open(path, "rb") as fh:
        digest = sha256_bytes(fh.read())
    return mod, digest


def derive(d: bytes, rep, r88) -> tuple[int, dict]:
    """The round-88 accounting law with the stored value taken out of the gate."""
    ph_off, ph = rep.find_packheader(d)
    best, last = None, "no l_info candidate carries a derivable first block"
    for m in r88.l_info_candidates(d, ph_off, ph):
        b0 = m + 20
        if b0 + 12 > ph_off:
            continue
        sz_unc0, stored = struct.unpack_from("<II", d, b0)
        if sz_unc0 == 0:
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
            _stop, n, total = r88.segment(dd, b0, ph_off, m0, ph["method"])
            resumed = 0
            if info["resume"] is not None:
                _q, n2, su2 = r88.segment(dd, info["resume"], ph_off, m0, ph["method"])
                total += su2
                resumed = n2
            key = (total <= ph["u_len"], total, -derived)
            rec = {"l_info": m, "block0": b0, "block0_sz_unc": sz_unc0,
                   "stored_sz_cpr": stored, "derived_sz_cpr": derived,
                   "next_block": s1, "sentinel": end, "blocks_first": n,
                   "blocks_resumed": resumed, "uncompressed_accounted": total,
                   "u_len": ph["u_len"], "fits_u_len": total <= ph["u_len"],
                   "walk": info}
            if best is None or key > best[0]:
                best = (key, derived, rec)
    if best is None:
        raise Refused(last)
    return best[1], best[2]


def repair(d: bytes) -> tuple[bytes, dict]:
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise Refused("not a little-endian ELF")
    rep, digest87 = load_module(R87, "r87repair")
    r88, digest88 = load_module(R88, "r88repair")
    # The round-87 anchor path first (magic restore / intact passthrough), so the
    # round-87 class keeps its repair.  A broken first block makes that walk
    # refuse; the field derivation then runs on the original bytes.
    anchor_refusal = None
    try:
        anchor_out, anchor_info = rep.repair(d)
        anchor_class = "intact" if anchor_info.get("intact") else "anchor"
    except rep.Refused as exc:
        anchor_out, anchor_info, anchor_class = d, {"refusal": str(exc)}, None
        anchor_refusal = str(exc)
    derived, info = derive(anchor_out, rep, r88)
    info["upstream_sha256"] = digest87
    info["r88_sha256"] = digest88
    info["anchor_class"] = anchor_class
    info["anchor_refusal"] = anchor_refusal
    if info["stored_sz_cpr"] == derived:
        info["class"] = anchor_class or "intact"
        info["delta"] = 0
        return anchor_out, info
    out = bytearray(anchor_out)
    struct.pack_into("<I", out, info["block0"] + 4, derived)
    info["class"] = "chain-geometry" if info["stored_sz_cpr"] == 0 else "field-value"
    info["delta"] = derived - info["stored_sz_cpr"]
    # Re-validate the corrected bytes through the round-87 anchor path: a
    # correction that does not restore a plausible chain is refused, not written.
    try:
        final, final_info = rep.repair(bytes(out))
    except rep.Refused as exc:
        raise Refused(f"corrected bytes still implausible: {exc}")
    info["restored"] = final_info.get("restored")
    return final, info


def _packed_fixture(stored: int | None = None) -> bytes:
    """The round-87 synthetic image with block 0's `sz_cpr` set to `stored`."""
    rep, _ = load_module(R87, "r87repair")
    clean = rep._fixture()
    if stored is None:
        return clean
    ph_off, ph = rep.find_packheader(clean)
    m, _s, _w = rep.find_linfo(clean, ph_off, ph)
    out = bytearray(clean)
    struct.pack_into("<I", out, m + 20 + 4, stored)
    return bytes(out)


def selftest() -> int:
    rep, _ = load_module(R87, "r87repair")
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

    clean = _packed_fixture()
    ph_off, ph = rep.find_packheader(clean)
    m, _s, _w = rep.find_linfo(clean, ph_off, ph)
    b0 = m + 20
    true_cpr = struct.unpack_from("<I", clean, b0 + 4)[0]

    out, info = repair(clean)
    check("intact-is-byte-identical", out == clean)
    check("intact-class", info["class"] == "intact")
    check("intact-derives-true-value", info["derived_sz_cpr"] == true_cpr)

    zeroed = _packed_fixture(0)
    out, info = repair(zeroed)
    check("zeroed-recovered", struct.unpack_from("<I", out, b0 + 4)[0] == true_cpr)
    check("zeroed-class", info["class"] == "chain-geometry")

    wrong = true_cpr - 8 if true_cpr > 8 else true_cpr + 8
    tampered = _packed_fixture(wrong)
    out, info = repair(tampered)
    check("wrong-nonzero-recovered", struct.unpack_from("<I", out, b0 + 4)[0] == true_cpr)
    check("wrong-nonzero-class", info["class"] == "field-value")
    check("wrong-nonzero-delta", info["delta"] == true_cpr - wrong)
    check("wrong-nonzero-equals-intact", out == clean)

    refuses("refuse-not-elf", b"not an elf at all" * 8)
    refuses("refuse-empty", b"")
    # The round-87 class still repairs through this tool (composition, no-harm).
    magic_tampered = rep._fixture(tamper=b"UPX?")
    out, info = repair(magic_tampered)
    check("magic-class-composed", out == clean and info["class"] == "anchor")
    # An out-of-range stored value is the same class: the derivation never reads
    # it, so the packer's arithmetic gate firing early changes nothing here.
    huge = bytearray(tampered)
    huge[b0 + 4:b0 + 8] = struct.pack("<I", 0xFFFFFFF0)
    out, info = repair(bytes(huge))
    check("wrong-out-of-range-recovered", struct.unpack_from("<I", out, b0 + 4)[0] == true_cpr)
    check("wrong-out-of-range-class", info["class"] == "field-value")
    # A payload corruption is not a structural defect: the walk steps by field
    # values, so the repair cannot see it and the counter's `test_ok`/`identity`
    # arms are the guard (disclosed limit, round-89 entry).
    corrupt = bytearray(tampered)
    corrupt[len(corrupt) // 2] ^= 0xFF
    out, info = repair(bytes(corrupt))
    check("corrupt-payload-not-structural", info["class"] == "field-value")
    check("corrupt-payload-output-carries-the-flip", out[len(out) // 2] == corrupt[len(corrupt) // 2])

    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--in", dest="src")
    ap.add_argument("--out", dest="dst")
    ap.add_argument("--info", dest="info")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.src or not a.dst:
        print("usage: --in FILE --out FILE [--info FILE] | --selftest", file=sys.stderr)
        return 2
    try:
        if os.path.getsize(a.src) > MAX_INPUT:
            raise Refused(f"input larger than {MAX_INPUT} bytes")
        with open(a.src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    try:
        out, info = repair(data)
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    tmp = a.dst + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(out)
    os.replace(tmp, a.dst)
    rec = {"tool": TOOL, "tool_sha256": sha256_bytes(open(__file__, "rb").read()),
           "input_sha256": sha256_bytes(data), "output_sha256": sha256_bytes(out),
           "info": info}
    if a.info:
        with open(a.info, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
    print(f"{info['class']}: stored {info['stored_sz_cpr']} -> derived "
          f"{info['derived_sz_cpr']} at block0 {info['block0']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
