#!/usr/bin/env python3
"""upx-stop-boundary-search-repair.py - round-92 repair candidate (R92-C1, coverage).

Class `T7-chain-stop-boundary`: a packed UPX 5.2.0 `--best` little-endian ELF
x86-64 carrier whose **last** block before the chain stop carries a different
in-range `sz_cpr`.  Round 91 (tools/round-91/upx-stop-boundary-repair.py) ends
this class in a typed refusal, because the chain geometry cannot decide the
stored value: every derived successor that validates accounts for the same
total.  This candidate adds the declared +/-16 window on top of the unchanged
round-91 path: the last block's `sz_cpr` is searched over
`[stored-16, stored+16]` (clamped to `0 < v <= sz_unc`), each candidate value is
decided by the packer's own verdict (`upx -t` rc 0 on a private copy under
TMPDIR), and the repair is written only when EXACTLY ONE value in the window is
green and the result differs from the input only inside the four-byte field.
Zero or two-plus green values, or any other check failure, is a typed refusal
(rc 2, no output file).  An intact input takes the round-91 path unchanged
(`upx -t` green, no successor decision): rc 0, output byte-identical.

The last block is located on the tampered bytes in up to two readings of the
same geometry (measured on the counter carriers: the pristine b_info chain ends
thousands of bytes before the PackHeader, so the walk's PackHeader bound
absorbs small `+delta` lies):

- the last block the walk still stepped through (`blocks[-1]`, the lie in its
  own field) -- always probed;
- an unappended `b_info` header at the walk stop, for a carrier without that
  slack: a plausible header whose declared span overshoots the PackHeader.

Both readings are probed and the packer verdict decides; uniqueness is required
across ALL probes, so an ambiguous window refuses instead of guessing.

Exit: 0 = the bytes change (intact identity or the unique window repair);
2 = typed refusal, no output written; 1 = an internal error, reported with its
exception class.  Standard library only.
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

TOOL = "tools/round-92/upx-stop-boundary-search-repair.py"
R91 = "tools/round-91/upx-stop-boundary-repair.py"
R87 = "tools/round-87/upx-magic-repair.py"
R88 = "tools/round-88/upx-chain-repair.py"
R90 = "tools/round-90/upx-break-repair.py"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(HERE, "stop-boundary-battery-v2.py")
MAX_INPUT = 256 << 20
CLASS = "T7-chain-stop-boundary"
WINDOW = 16
UPX = "/usr/bin/upx"

_rep91 = None
_helpers = None


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rep91():
    """The round-91 tool's module: its contract helpers are reused verbatim."""
    global _rep91
    if _rep91 is None:
        _rep91 = load_module(os.path.join(ROOT, R91), "cand_r91repair")
    return _rep91


def helpers():
    """(rep=r87, r88, r90) loaded from the same ROOT as the round-91 tool."""
    global _helpers
    if _helpers is None:
        rep = load_module(os.path.join(ROOT, R87), "cand_r87repair")
        r88 = load_module(os.path.join(ROOT, R88), "cand_r88repair")
        r90 = load_module(os.path.join(ROOT, R90), "cand_r90repair")
        _helpers = (rep, r88, r90)
    return _helpers


def _clean_env() -> dict:
    return {"PATH": os.environ.get("PATH") or "/usr/bin", "LANG": "C",
            "HOME": tempfile.gettempdir()}


def upx_green(data: bytes) -> bool:
    """The packer's own verdict on arbitrary bytes: `upx -t` rc 0 means green.

    The bytes are written to a private file under the caller's TMPDIR (never
    /tmp) and the probe never produces output bytes.
    """
    fd, path = tempfile.mkstemp(prefix=".r92-probe-", dir=tempfile.gettempdir())
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        p = subprocess.run([UPX, "-t", "-q", path], capture_output=True,
                           text=True, timeout=600, env=_clean_env())
        return p.returncode == 0
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def last_block_spots(d: bytes, blocks: list, q_stop: int, ph_off: int,
                     method: int, ph: dict) -> list:
    """Plausible (offset, sz_unc, field_value) spots for the tampered last block.

    Measured geometry (round-92 wave probe): the pristine b_info chain ends
    well before the PackHeader on every counter carrier (jq 10097 < 14000, xxd
    15630 < 19524, libz 60127 < 65544, docker-init 352674 < 357748, xz 42590 <
    46532), so the walk's `q + 12 + sc <= ph_off` bound absorbs small `+delta`
    lies: the LIED span still fits and the walk steps THROUGH the tampered
    block, which is then `blocks[-1]` with the lie in its own field.  That last
    walked block is therefore always probed.  For a carrier without that slack,
    a `+delta` lie overshoots the bound and is left unappended: a plausible
    header at the walk stop whose declared span overshoots the PackHeader is
    probed as the second reading.
    """
    spots = []
    if blocks:
        lb = blocks[-1]
        spots.append((lb["block"], lb["sz_unc"], lb["sz_cpr"]))
    if q_stop + 12 <= ph_off:
        su, sc = struct.unpack_from("<II", d, q_stop)
        if su > 0 and sc > 0 and q_stop + 12 + sc > ph_off \
                and d[q_stop + 8] in (method, ph["method"]):
            if not any(p == q_stop for p, _su, _v in spots):
                spots.append((q_stop, su, sc))
    return spots


def search(d: bytes, spots: list) -> list:
    """Every green (offset, value, candidate) with v in [stored-16, stored+16],
    0 < v <= sz_unc, skipping the input's own value (the input is already red).
    """
    greens = []
    for p, su, stored in spots:
        lo = max(1, stored - WINDOW)
        hi = min(su, stored + WINDOW)
        for v in range(lo, hi + 1):
            if v == stored:
                continue
            cand = bytearray(d)
            struct.pack_into("<I", cand, p + 4, v)
            cand = bytes(cand)
            if upx_green(cand):
                greens.append((p, v, cand))
    return greens


def repair(d: bytes) -> tuple:
    """The round-91 path first; on its stop-boundary refusal, the window search."""
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise rep91().Refused("not a little-endian ELF")
    try:
        # The round-91 tool's own body: intact identity, the block-0 law, the
        # break law, and the typed stop-boundary refusal this candidate extends.
        return rep91().repair(d)
    except rep91().Refused as exc:
        if not str(exc).startswith("stop-boundary"):
            raise
    rep, r88, r90 = helpers()
    ph_off, ph = rep.find_packheader(d)
    found = r90.longest_prefix(d, rep, r88)
    if found is None:
        raise rep91().Refused(
            "stop-boundary: the packer refuses the input and no l_info candidate "
            "carries a walkable chain to locate the last block")
    _m, b0, ph2, blocks, method = found
    q_stop = (blocks[-1]["block"] + 12 + blocks[-1]["sz_cpr"]) if blocks else b0
    spots = last_block_spots(d, blocks, q_stop, ph_off, method, ph)
    if not spots:
        raise rep91().Refused(
            f"stop-boundary: the packer refuses the input but no plausible "
            f"last-block window exists (prefix {len(blocks)} blocks, walk stop "
            f"{q_stop}, packheader {ph_off})")
    greens = search(d, spots)
    if not greens:
        raise rep91().Refused(
            f"stop-boundary: no green value in the +/-{WINDOW} window "
            f"(spots {[(p, v) for p, _su, v in spots]}, the packer refuses the "
            f"input and every in-window candidate)")
    if len(greens) > 1:
        raise rep91().Refused(
            f"stop-boundary: {len(greens)} green values "
            f"{[(p, v) for p, v, _c in greens]} in the +/-{WINDOW} window -- "
            "the packer verdict does not decide the stored value")
    p, v, cand = greens[0]
    stored = struct.unpack_from("<I", d, p + 4)[0]
    if len(cand) != len(d):
        raise rep91().Refused("stop-boundary: candidate changed the file length")
    if any(a != b and not (p + 4 <= i < p + 8)
           for i, (a, b) in enumerate(zip(d, cand))):
        raise rep91().Refused("stop-boundary: candidate changed bytes outside "
                              "the four-byte window")
    if not upx_green(cand):
        raise rep91().Refused("stop-boundary: the final verdict is not green")
    return cand, {"class": "repaired", "block": p, "blocks": len(blocks),
                  "stored_sz_cpr": stored, "derived_sz_cpr": v,
                  "delta": v - stored}


def _battery_walk(packed: bytes):
    """The frozen counter's own layout() for the selftest fixtures, when the
    imported v2 instrument sits next to this tool; else the round-90 walk."""
    try:
        v2 = load_module(V2, "cand_r92v2")
        rep, r88, _r90 = helpers()
        b0, blocks = v2.layout(packed, rep, r88)
        return "v2.layout", (b0, blocks)
    except OSError:
        rep, r88, r90 = helpers()
        found = r90.longest_prefix(packed, rep, r88)
        _m, b0, _ph, blocks, _method = found
        return "r90.longest_prefix", (b0, blocks)


def _pack_copy(src: str, work: str) -> bytes:
    """Pack a private copy of `src` with the pinned packer, in `work`."""
    import shutil
    box = tempfile.mkdtemp(prefix="r92-st-", dir=work)
    inp, outp = os.path.join(box, "in"), os.path.join(box, "packed")
    shutil.copyfile(src, inp)
    os.chmod(inp, 0o755)
    p = subprocess.run([UPX, "--best", "-q", "-o", outp, inp],
                       capture_output=True, text=True, timeout=600,
                       env=_clean_env())
    if p.returncode != 0:
        raise RuntimeError(f"upx pack failed rc={p.returncode}")
    with open(outp, "rb") as fh:
        return fh.read()


def selftest() -> int:
    """Fixtures in the scratch tree: intact identity, last-block +/-7 repairs to
    the pristine bytes, +/-40 far refusal, not-an-ELF refusal, and an attempted
    two-green forged fixture (skipped, loudly, when none is constructible)."""
    import struct
    fails, ncases, notes = [], 0, []

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    work = os.path.join(tempfile.gettempdir(), "r92-selftest-work")
    os.makedirs(work, exist_ok=True)
    packed = _pack_copy("/usr/bin/xxd", work)
    _how, (b0, blocks) = _battery_walk(packed)
    if not blocks:
        print("SELFTEST unevaluable: no walkable chain")
        return 1
    notes.append(f"walk={_how} blocks={len(blocks)} "
                 f"last=(off={blocks[-1]['block']}, cpr={blocks[-1]['sz_cpr']}, "
                 f"unc={blocks[-1]['sz_unc']})")
    last = blocks[-1]
    try:
        out, info = repair(packed)
        check("intact-identity", out == packed and info.get("class") == "intact")
    except rep91().Refused as exc:
        check("intact-identity", False)
        notes.append(f"intact refused: {exc}")
    for delta in (-7, 7):
        v = last["sz_cpr"] + delta
        if not (0 < v <= last["sz_unc"]):
            check(f"last-{delta}-in-range", False)
            continue
        t = bytearray(packed)
        struct.pack_into("<I", t, last["block"] + 4, v)
        try:
            out, info = repair(bytes(t))
            check(f"last-{delta}-repaired-to-pristine",
                  out == packed and info.get("class") == "repaired")
        except rep91().Refused as exc:
            check(f"last-{delta}-repaired-to-pristine", False)
            notes.append(f"last-{delta} refused: {exc}")
    for delta in (-40, 40):
        v = last["sz_cpr"] + delta
        if not (0 < v <= last["sz_unc"]):
            check(f"far-{delta}-in-range", False)
            continue
        t = bytearray(packed)
        struct.pack_into("<I", t, last["block"] + 4, v)
        try:
            repair(bytes(t))
            check(f"far-{delta}-refused", False)
        except rep91().Refused as exc:
            check(f"far-{delta}-refused", str(exc).startswith("stop-boundary"))
    try:
        repair(b"not an elf at all" * 8)
        check("non-elf-refused", False)
    except rep91().Refused:
        check("non-elf-refused", True)
    # Two-green forge attempt: sweep a wide window around the pristine value on
    # the last block; a cell whose sweep holds two greens gives a field value
    # whose +/-16 window contains both.
    true_v = last["sz_cpr"]
    lo, hi = max(1, true_v - 64), min(last["sz_unc"], true_v + 64)
    greens = []
    for v in range(lo, hi + 1):
        if v == true_v:
            continue
        c = bytearray(packed)
        struct.pack_into("<I", c, last["block"] + 4, v)
        if upx_green(bytes(c)):
            greens.append(v)
    notes.append(f"two-green sweep +-{64} around pristine: greens={greens}")
    if len(greens) >= 2 and greens[1] - greens[0] <= 2 * WINDOW:
        forged = bytearray(packed)
        struct.pack_into("<I", forged, last["block"] + 4,
                         (greens[0] + greens[1]) // 2)
        try:
            repair(bytes(forged))
            check("two-green-forged-refused", False)
        except rep91().Refused as exc:
            check("two-green-forged-refused", str(exc).startswith("stop-boundary"))
    else:
        notes.append("two-green fixture NOT constructible in the swept window "
                     f"({len(greens)} greens, spread "
                     f"{(greens[-1] - greens[0]) if len(greens) > 1 else 0})")
    print(f"SELFTEST cases={ncases} failures={len(fails)} "
          f"{' '.join(fails)} | {'; '.join(notes)}".rstrip())
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
        r = rep91()
    except Exception as exc:
        print(json.dumps({"tool": TOOL, "class": CLASS,
                          "error": f"{exc.__class__.__name__}: {exc}"}))
        return 1
    try:
        data = r.read_input(args.src)
        out, info = repair(data)
        # Both targets are validated before the first write, so a refused
        # `--info` cannot leave an `--out` on disk behind an rc 2.
        r.checked_target(args.dst)
        if args.info:
            r.checked_target(args.info)
        r.write_atomic(args.dst, out)
        if args.info:
            r.write_atomic(args.info, json.dumps(
                {"tool": TOOL, "class": info.get("class"),
                 **{k: info.get(k) for k in ("block", "blocks", "stored_sz_cpr",
                                             "derived_sz_cpr", "delta",
                                             "break_index")}},
                indent=1, sort_keys=True).encode())
        print(json.dumps({k: info.get(k) for k in
                          ("class", "block", "blocks", "stored_sz_cpr",
                           "derived_sz_cpr", "delta")}, sort_keys=True))
        return 0
    except r.Refused as exc:
        print(json.dumps({"tool": TOOL, "class": CLASS, "refused": str(exc)}))
        return 2
    except Exception as exc:  # every path is wrapped: no uncaught traceback
        print(json.dumps({"tool": TOOL, "class": CLASS,
                          "error": f"{exc.__class__.__name__}: {exc}"}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
