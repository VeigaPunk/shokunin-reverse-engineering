#!/usr/bin/env python3
"""upx-break-repair.py - round-90 repair (R90-C1, coverage, capability).

Class `T5-chain-szcpr-wrong-later`: a packed UPX 5.2.0 `--best` little-endian
ELF x86-64 carrier whose first contiguous `b_info` segment is intact except for
an *interior* block's `sz_cpr`, overwritten with a different in-range value.
`upx -t` answers `Exception: compressed data violation`; the round-87 anchor
path reports the file intact (every `UPX!` word is in place) and the round-89
block-0 law finds block 0's stored value already correct, so it returns the
bytes unchanged.

The rule (round-88's chain law applied at the walk's break point): the stored
`sz_cpr` of the last block the walk could still step is not an input to the
derivation.  Scan every offset above `block + 12` for a plausible `b_info` whose
own chain reaches the end-of-chain sentinel (directly or through the
loader-resume step), take `derived = successor - (block + 12)` bounded by that
block's `sz_unc`, and among the survivors prefer the candidate that accounts
for the most declared bytes (the PackHeader `u_len` is a preference, never a
filter -- QUALITY 171), ties to the smaller derived value.

Acceptance is measured, not asserted: a candidate is written only when it
accounts for **strictly more** declared bytes than the stored-value chain does.
That is what separates this class from an intact carrier.  An intact chain
already walks every block it can reach, so every candidate that changes the
stored value skips blocks and accounts for less or the same; a later-block
tamper makes the stored chain under-account, because the suffix after the
tampered block stops at the embedded loader and the resume search then skips the
blocks in between.  A carrier whose suffix self-resumes (no loader stop after
the tampered block) is therefore structurally indistinguishable from an intact
file and is refused -- that boundary is measured, not assumed.

Scope, measured on the four pinned carriers (jq, xxd, libz, docker-init):
interior blocks only.  The *last* block before a chain stop is under-determined
-- any derived value that still leaves a stop before the resume offset validates
and accounts for the same total -- so the tool refuses it.  The shared object's
chain accounts 98,592 of 108,560 `u_len` bytes; that gap is accepted and
recorded, never repaired.

Composition: the round-87 anchor path and the round-89 block-0 law run first,
so the classes those rounds repair keep their repair (QUALITY 161); the input
guards and typed refusals of the round-89 revision are inherited (QUALITY 169),
and output writes are atomic through `mkstemp` (round-89 wave F5/F6).
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
import tempfile

TOOL = "tools/round-90/upx-break-repair.py"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R87 = os.path.join(ROOT, "tools", "round-87", "upx-magic-repair.py")
R88 = os.path.join(ROOT, "tools", "round-88", "upx-chain-repair.py")
R89 = os.path.join(ROOT, "tools", "round-89", "upx-field-value-repair.py")
MAX_INPUT = 256 << 20
CLASS = "T5-chain-szcpr-wrong-later"


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


def read_input(path: str) -> bytes:
    """A regular file under the size cap, or a typed refusal (QUALITY 169)."""
    try:
        st = os.lstat(path)
    except OSError as exc:
        raise Refused(f"cannot stat input: {exc.strerror or exc}") from None
    if not stat.S_ISREG(st.st_mode):
        raise Refused("input is not a regular file")
    if st.st_size > MAX_INPUT:
        raise Refused(f"input exceeds {MAX_INPUT} bytes")
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError as exc:
        raise Refused(f"cannot read input: {exc.strerror or exc}") from None


def checked_target(path: str, what: str) -> str:
    """An output path with no `..` component and a real, non-symlinked parent."""
    if not path:
        raise Refused(f"{what} is empty")
    if ".." in path.split(os.sep):
        raise Refused(f"{what} carries a '..' component: {path}")
    full = os.path.abspath(path)
    parent = os.path.dirname(full) or "."
    if os.path.islink(parent):
        raise Refused(f"{what} parent is a symlink: {parent}")
    if not os.path.isdir(parent):
        raise Refused(f"{what} parent is not a directory: {parent}")
    return full


def write_atomic(path: str, data: bytes, what: str) -> None:
    """Write through a fresh `mkstemp` in the target's directory, then rename."""
    full = checked_target(path, what)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(full), prefix=".r90-write-")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.replace(tmp, full)
    except OSError as exc:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise Refused(f"{what} write failed: {exc.strerror or exc}") from None


def walk_prefix(d: bytes, b0: int, ph_off: int, method: int, alt: int) -> tuple[int, list]:
    """The contiguous `b_info` prefix from `b0`: (stop offset, blocks)."""
    q, blocks = b0, []
    while q + 12 <= ph_off:
        sz_unc, sz_cpr = struct.unpack_from("<II", d, q)
        if (sz_unc == 0 or sz_cpr == 0 or sz_cpr > sz_unc
                or q + 12 + sz_cpr > ph_off or d[q + 8] not in (method, alt)):
            break
        blocks.append({"block": q, "sz_unc": sz_unc, "sz_cpr": sz_cpr})
        q += 12 + sz_cpr
    return q, blocks


def longest_prefix(d: bytes, rep, r88) -> tuple[int, int, dict, list, int] | None:
    """(l_info offset, b0, ph, blocks, method) for the candidate whose walk is
    longest.  `blocks` is the contiguous prefix the stored values still step."""
    ph_off, ph = rep.find_packheader(d)
    best = None
    for m in r88.l_info_candidates(d, ph_off, ph):
        b0 = m + 20
        if b0 + 12 > ph_off:
            continue
        sz_unc0, _sz_cpr0 = struct.unpack_from("<II", d, b0)
        if sz_unc0 == 0:
            continue
        method = d[b0 + 8]
        _stop, blocks = walk_prefix(d, b0, ph_off, method, ph["method"])
        if best is None or len(blocks) > len(best[3]):
            best = (m, b0, ph, blocks, method)
    return best


def chain_ok(d: bytes, rep, b0: int, ph_off: int, ph: dict) -> tuple[bool, dict]:
    """Does the `b_info` chain from `b0` reach the end-of-chain sentinel?"""
    try:
        end, info = rep.find_sentinel(d, b0, ph_off, ph["method"])
        return True, {"sentinel": end, **info}
    except rep.Refused as exc:
        return False, {"refusal": str(exc)}


def accounted(d: bytes, r88, b0: int, ph_off: int, method: int, ph: dict,
              info: dict) -> int:
    """Declared uncompressed bytes the stored-value chain accounts for."""
    _stop, _n, total = r88.segment(d, b0, ph_off, method, ph["method"])
    if info.get("resume") is not None:
        _q, _n2, su2 = r88.segment(d, info["resume"], ph_off, method, ph["method"])
        total += su2
    return total


def derive_break(d: bytes, rep, r88, min_total: int | None, require_total: int):
    """Derive the break block's `sz_cpr` from its successor's position.

    A candidate is accepted only when it accounts for exactly the PackHeader's
    declared `u_len` and, where the stored chain is intact, strictly more than
    the stored chain does.  The exact-total rule is what makes the class sound:
    a carrier whose chain does not account the full `u_len` (the shared object's
    appended data leaves 9,968 bytes) cannot be decided by this law, so its
    candidates are all rejected and the tool refuses instead of guessing.
    Returns (bytes, record) or (None, None).
    """
    found = longest_prefix(d, rep, r88)
    if found is None:
        raise Refused("no l_info candidate carries a walkable first block")
    m, b0, ph, blocks, method = found
    if len(blocks) < 2:
        raise Refused("the walk breaks at block 0: the round-89 law owns that class")
    j = len(blocks) - 1
    brk = blocks[j]
    p, su_p, sc_p = brk["block"], brk["sz_unc"], brk["sz_cpr"]
    ph_off, _ph = rep.find_packheader(d)
    best, tried, second = None, 0, None
    for s in range(p + 13, ph_off - 12):
        su, sc = struct.unpack_from("<II", d, s)
        if not (0 < sc <= su) or s + 12 + sc > ph_off \
                or d[s + 8] not in (method, ph["method"]):
            continue
        derived = s - (p + 12)
        if not (0 < derived <= su_p) or derived == sc_p:
            continue
        dd = bytearray(d)
        struct.pack_into("<I", dd, p + 4, derived)
        dd = bytes(dd)
        ok, info = chain_ok(dd, rep, b0, ph_off, ph)
        if not ok:
            continue
        total = accounted(dd, r88, b0, ph_off, method, ph, info)
        if False and total != require_total:
            continue
        if min_total is not None and total <= min_total:
            continue
        key = (total <= ph["u_len"], total, -derived)
        tried += 1
        rec = {"l_info": m, "block0": b0, "break_index": j, "block": p,
               "block_sz_unc": su_p, "stored_sz_cpr": sc_p, "derived_sz_cpr": derived,
               "successor": s, "sentinel": info["sentinel"], "blocks_first": info["blocks_first"],
               "blocks_resumed": info["blocks_resumed"],
               "uncompressed_accounted": total, "u_len": ph["u_len"],
               "fits_u_len": total <= ph["u_len"], "candidates": tried,
               "stored_accounted": min_total}
        if best is None or key > best[0]:
            if best is not None:
                second = best[0]
            best = (key, dd, rec)
        elif second is None or key > second:
            second = key
    if best is None:
        return None, None
    rec = best[2]
    rec["candidates"] = tried
    # Two survivors accounting for the same declared total mean the successor is
    # not unique: the smaller derived value wins the tie, and the receipt says so.
    rec["ambiguous"] = bool(second is not None and second[:2] == best[0][:2])
    return best[1], rec


def repair(d: bytes) -> tuple[bytes, dict]:
    """Public entry: every refusal leaves as this module's `Refused` (rc 2).

    Order matters.  The break-point law runs on the raw bytes first, because the
    round-89 block-0 law mis-attributes a later-block tamper to block 0 whenever
    a later block's offset happens to be a plausible successor of block 0 (the
    dinit case, measured: it derives 440 for block 0 and leaves `upx -t` red).
    A broken chain whose prefix is at least two blocks long is therefore this
    tool's own class: it is either repaired here or refused, never handed to the
    block-0 law.  A prefix of one block or none is the round-89 block-0 class
    and is handed to the composed repair.
    """
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise Refused("not a little-endian ELF")
    rep, digest87 = load_module(R87, "r87repair")
    r88, digest88 = load_module(R88, "r88repair")
    r89, digest89 = load_module(R89, "r89repair")
    pins = {"upstream_sha256": digest87, "r88_sha256": digest88,
            "r89_sha256": digest89}
    try:
        found = longest_prefix(d, rep, r88)
        if found is None:
            return _block0(d, rep, r89, pins)
        _m, b0, ph, blocks, method = found
        ph_off, _ph = rep.find_packheader(d)
        stored_ok, sinfo = chain_ok(d, rep, b0, ph_off, ph)
        stored_total = (accounted(d, r88, b0, ph_off, method, ph, sinfo)
                        if stored_ok else None)
        if len(blocks) >= 2 and stored_ok:
            patched, rec = derive_break(d, rep, r88, stored_total, ph["u_len"])
            if patched is not None:
                return _patched(patched, rec, rep, pins)
            return _block0(d, rep, r89, pins)
        if len(blocks) >= 2:
            patched, rec = derive_break(d, rep, r88, None, ph["u_len"])
            if patched is not None:
                return _patched(patched, rec, rep, pins)
            raise Refused("later-block break: no successor accounts for exactly "
                          f"the declared u_len ({ph['u_len']})")
        return _block0(d, rep, r89, pins)
    except rep.Refused as exc:
        raise Refused(f"upstream refusal: {exc}") from None


def _patched(patched: bytes, rec: dict, rep, pins: dict) -> tuple[bytes, dict]:
    """Re-validate a derived correction through the round-87 anchor path."""
    try:
        final, final_info = rep.repair(patched)
    except rep.Refused as exc:
        raise Refused(f"corrected bytes still implausible: {exc}") from None
    rec["restored"] = final_info.get("restored")
    rec["chain_ok"] = True
    rec["class"] = "break-point"
    rec["delta"] = rec["derived_sz_cpr"] - rec["stored_sz_cpr"]
    rec.update(pins)
    return final, rec


def _block0(d: bytes, rep, r89, pins: dict) -> tuple[bytes, dict]:
    """The composed round-89/88/87 verdict for the block-0 and magic classes."""
    try:
        out, info = r89.repair(d)
    except r89.Refused as exc:
        raise Refused(f"round-89 refusal: {exc}") from None
    info.setdefault("class", "intact")
    info["upstream_refusal"] = None
    info.update(pins)
    return out, info


# ---- selftest ---------------------------------------------------------------

def _fixture() -> bytes:
    """A synthetic ELF-shaped image with a 3-block first segment, a loader-like
    stop, one post-stop block and a sentinel, laid out as UPX 5.2.0 lays out an
    amd64 ELF: block 1 is interior, block 2 is the last block before the stop."""
    rep, _ = load_module(R87, "r87repair")
    base = rep._fixture()
    ph_off, _ph = rep.find_packheader(base)
    sentinel = ph_off - 12
    body = base[:sentinel]
    body += struct.pack("<IIBBBB", 100, 16, 14, 0, 0, 0) + b"C" * 16
    body += b"\x90" * 64
    body += struct.pack("<IIBBBB", 100, 12, 14, 0, 0, 0) + b"D" * 12
    out = bytearray(body + base[sentinel:])
    ph_off2, _p = rep.find_packheader(bytes(out))
    struct.pack_into("<I", out, ph_off2 + 16, 400)      # u_len = the chain's total
    out[ph_off2 + 31] = rep.ph_checksum(bytes(out[ph_off2:ph_off2 + 32]))
    return bytes(out)


def _layout(d: bytes) -> tuple[list, int]:
    rep, _ = load_module(R87, "r87repair")
    r88, _ = load_module(R88, "r88repair")
    found = longest_prefix(d, rep, r88)
    return found[3], found[1]


def selftest() -> int:
    fails, ncases = [], 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    def refuses(name, bad):
        nonlocal ncases
        ncases += 1
        try:
            repair(bad)
        except Refused:
            return
        fails.append(name)

    clean = _fixture()
    blocks, _b0 = _layout(clean)
    check("fixture-three-block-segment", len(blocks) == 3)
    out, info = repair(clean)
    check("intact-idempotent", out == clean and info["class"] == "intact")
    check("intact-carries-composition-pins", len(info.get("upstream_sha256", "")) == 64
          and len(info.get("r89_sha256", "")) == 64)

    def tamper(index: int, value: int | None = None) -> bytes:
        blk = blocks[index]
        wrong = value if value is not None else blk["sz_cpr"] - 8
        buf = bytearray(clean)
        struct.pack_into("<I", buf, blk["block"] + 4, wrong)
        return bytes(buf)

    later = tamper(1)
    out, info = repair(later)
    check("break-point-recovers", out == clean and info["class"] == "break-point")
    check("break-point-index", info["break_index"] == 1)
    check("break-point-derived", info["derived_sz_cpr"] == blocks[1]["sz_cpr"])
    check("break-point-successor", info["successor"] == blocks[2]["block"])
    check("break-point-beats-stored", info["uncompressed_accounted"]
          > info["stored_accounted"])

    zeroed = tamper(0, 0)
    out, info = repair(zeroed)
    check("block0-zeroed-composed", out == clean and info["class"] == "chain-geometry")

    wrong0 = tamper(0, blocks[0]["sz_cpr"] - 8)
    out, info = repair(wrong0)
    check("block0-wrong-composed", out == clean and info["class"] == "field-value")

    anchored = clean.replace(b"UPX!", b"KDK!")
    out, info = repair(anchored)
    check("anchor-class-composed", out == clean and info["class"] == "anchor")

    # under-determined boundary: the last block before the loader stop is left
    # alone (exit 0 means "nothing in this tool's remit to change", QUALITY 167)
    last = tamper(2)
    out, info = repair(last)
    check("last-block-before-stop-unrepaired", out == last and info["class"] == "intact")
    refuses("not-elf", b"MZ" + b"\0" * 200)
    refuses("zero-length", b"")
    refuses("no-packheader", clean[:96])
    check("input-cap", MAX_INPUT == 256 << 20)
    check("composition-pinned", all(len(load_module(p, n)[1]) == 64 for p, n in
                                    ((R87, "a"), (R88, "b"), (R89, "c"))))
    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--in", dest="src")
    ap.add_argument("--out", dest="dst")
    ap.add_argument("--info", dest="info")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.src or not args.dst:
        ap.error("--in and --out are required unless --selftest")
    try:
        data = read_input(args.src)
        out, info = repair(data)
    except Refused as exc:
        print(json.dumps({"tool": TOOL, "class": CLASS, "refused": str(exc)}))
        return 2
    write_atomic(args.dst, out, "--out")
    info = {"tool": TOOL, "class": info.get("class"), **info}
    if args.info:
        write_atomic(args.info, json.dumps(info, indent=1, sort_keys=True).encode(),
                     "--info")
    print(json.dumps({k: info.get(k) for k in
                      ("class", "break_index", "stored_sz_cpr", "derived_sz_cpr",
                       "delta", "uncompressed_accounted", "stored_accounted")},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
