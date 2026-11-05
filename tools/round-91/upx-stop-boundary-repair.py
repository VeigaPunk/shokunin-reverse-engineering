#!/usr/bin/env python3
"""upx-stop-boundary-repair.py - round-91 repair (R91-C1, coverage, capability).

Class `T7-chain-stop-boundary`: a packed UPX 5.2.0 `--best` little-endian ELF
x86-64 carrier whose **last** block before the chain stop carries a different
in-range `sz_cpr` (`0 < stored +/- 7 <= sz_unc`, i.e. a value the packer's own
bounds accept). `upx -t` answers `Exception: compressed data violation`. The
round-90 repair cannot decide the cell -- every derived value that still leaves
a stop before the resume offset validates and accounts for the same total -- and
its fall-through hands the bytes to the round-89 block-0 law, which answers
**rc 0** for a file it did not repair: byte-identical on four cells, and on two
it writes the four-byte `UPX!` sentinel **outside** the tampered window
(QUALITY 176). A caller cannot tell that rc 0 from a repair.

The rule, which is the round-90 module's own docstring sentence implemented
instead of asserted (QUALITY 162): *a broken chain whose walkable prefix is at
least two blocks long is this lane's later-block class and is either repaired
here or refused -- never handed to the block-0 law*. So this tool composes the
round-90 derivation unchanged, and where that derivation has no unique successor
it raises a typed refusal (`stop-boundary`) instead of falling through. The
output file is then never created: the refusal writes nothing, so the caller
gets rc 2 and the input bytes are untouched.

Scope: the refusal is the capability. This tool does not claim to repair a
last-block tamper (the geometry does not decide it) and does not decompress
what it refuses. Composition: round-87 anchors, round-88 geometry and the
round-90 break-point law keep their classes (QUALITY 161); input guards are the
round-90 read/write contract, and the whole body -- parser, derivation and
writes -- is wrapped, so no path ends in an uncaught traceback (QUALITY 177).

Exit: 0 = the bytes change (a class this lane repairs); 2 = typed refusal, no
output written; 1 = an internal error, reported with its exception class.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

TOOL = "tools/round-91/upx-stop-boundary-repair.py"
R87 = "tools/round-87/upx-magic-repair.py"
R88 = "tools/round-88/upx-chain-repair.py"
R89 = "tools/round-89/upx-field-value-repair.py"
R90 = "tools/round-90/upx-break-repair.py"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAX_INPUT = 256 << 20
CLASS = "T7-chain-stop-boundary"


class Refused(Exception):
    pass


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_input(path: str) -> bytes:
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


def checked_target(path: str) -> str:
    if not path:
        raise Refused("--out is empty")
    if ".." in path.split(os.sep):
        raise Refused(f"--out carries a '..' component: {path}")
    full = os.path.abspath(path)
    parent = os.path.dirname(full) or "."
    if os.path.islink(parent):
        raise Refused(f"--out parent is a symlink: {parent}")
    if not os.path.isdir(parent):
        raise Refused(f"--out parent is not a directory: {parent}")
    if os.path.exists(full) and os.path.isdir(full):
        raise Refused(f"--out is a directory: {full}")
    return full


def write_atomic(path: str, data: bytes) -> None:
    full = checked_target(path)
    fd = tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(full), prefix=".r91-write-")
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        fd = None
        os.replace(tmp, full)
        tmp = None
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass
        if tmp is not None:
            try:
                os.unlink(tmp)
            except OSError:
                pass


def classify(d: bytes, r90, rep, r88) -> tuple:
    """(blocks, b0, ph, stored_ok, stored_total, method) for the walkable prefix."""
    found = r90.longest_prefix(d, rep, r88)
    if found is None:
        return None
    _m, b0, ph, blocks, method = found
    ph_off, _ph = rep.find_packheader(d)
    stored_ok, sinfo = r90.chain_ok(d, rep, b0, ph_off, ph)
    stored_total = (r90.accounted(d, r88, b0, ph_off, method, ph, sinfo)
                    if stored_ok else None)
    return blocks, b0, ph, stored_ok, stored_total, method


def upx_test(d: bytes) -> bool:
    """The packer's own verdict on the INPUT: `upx -t` rc 0 means intact.

    Used only to separate an intact carrier from a stop-boundary tamper whose
    chain geometry is unchanged (a `+7` value keeps the walked total equal to
    `u_len`, so the geometry cannot tell the two apart; measured in
    `.ufo/waves/round-91/pre/probes/`).  It never produces output bytes.
    """
    fd, path = tempfile.mkstemp(prefix=".r91-test-", dir=tempfile.gettempdir())
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(d)
        p = subprocess.run(["/usr/bin/upx", "-t", "-q", path], capture_output=True,
                           text=True, timeout=600, env=_clean_env())
        return p.returncode == 0
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _clean_env() -> dict:
    return {"PATH": os.environ.get("PATH") or "/usr/bin", "LANG": "C",
            "HOME": tempfile.gettempdir()}


def repair(d: bytes) -> tuple[bytes, dict]:
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise Refused("not a little-endian ELF")
    rep = load_module(os.path.join(ROOT, R87), "r87repair")
    r88 = load_module(os.path.join(ROOT, R88), "r88repair")
    r89 = load_module(os.path.join(ROOT, R89), "r89repair")
    r90 = load_module(os.path.join(ROOT, R90), "r90repair")
    with open(os.path.join(ROOT, R90), "rb") as fh:
        pins = {"r90_sha256": hashlib.sha256(fh.read()).hexdigest()}
    try:
        cls = classify(d, r90, rep, r88)
        if cls is None or len(cls[0]) < 2:
            out, info = r90._block0(d, rep, r89, pins)
            info.update(pins)
            return out, info
        blocks, b0, ph, stored_ok, stored_total, method = cls
        min_total = stored_total if stored_ok else None
        patched, rec = r90.derive_break(d, rep, r88, min_total, ph["u_len"])
        if patched is not None:
            return r90._patched(patched, rec, rep, pins)
        # No successor decides the walk.  Either the input is intact, or the
        # tampered block is the last before the stop.  Only the packer's verdict
        # on the input separates them; the output of this branch is the input
        # byte-identical, or a typed refusal with no output file.
        if upx_test(d):
            return d, {"class": "intact", "break_index": None, "pins": pins,
                       **pins}
        raise Refused(
            "stop-boundary: the walk's last storable block has no successor that "
            f"accounts for the declared u_len ({ph['u_len']}) and `upx -t` refuses "
            f"the input (prefix {len(blocks)} blocks, stored_total {stored_total}); "
            "this class is refused, not repaired")
    except (rep.Refused, r90.Refused) as exc:
        # Qualifying the composed module's own refusal class is the R91 wave-1
        # MED-1 repair: an inner `Refused` used to escape to main()'s `except
        # Exception` and answer rc 1 ("error") where this tool's contract says
        # rc 2 ("typed refusal").
        raise Refused(f"upstream refusal: {exc}") from None


def _pack_copy(src: str, work: str) -> bytes:
    """Pack a private copy of `src` with the pinned packer, in `work` (scratch)."""
    box = tempfile.mkdtemp(prefix="r91-st-", dir=work)
    inp, outp = os.path.join(box, "in"), os.path.join(box, "packed")
    shutil.copyfile(src, inp)
    os.chmod(inp, 0o755)
    p = subprocess.run(["/usr/bin/upx", "--best", "-q", "-o", outp, inp],
                       capture_output=True, text=True, timeout=600, env=_clean_env())
    if p.returncode != 0:
        raise RuntimeError(f"upx pack failed rc={p.returncode}")
    with open(outp, "rb") as fh:
        return fh.read()


def selftest() -> int:
    """Real packed carrier: intact -> identity; last-block +/-7 -> typed refusal."""
    import struct
    fails, ncases = [], 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    work = os.environ.get("TMPDIR") or tempfile.gettempdir()
    rep = load_module(os.path.join(ROOT, R87), "r87_st")
    r88 = load_module(os.path.join(ROOT, R88), "r88_st")
    packed = _pack_copy("/usr/bin/xxd", work)
    try:
        out, info = repair(packed)
        check("intact-identity", out == packed and info.get("class") == "intact")
    except Refused as exc:
        check("intact-identity", False)
        print("  intact refusal:", exc)
    cls = classify(packed, load_module(os.path.join(ROOT, R90), "r90_st"), rep, r88)
    last = cls[1]  # b0
    blocks = cls[0]
    lb = blocks[-1]
    for delta in (-7, 7):
        v = lb["sz_cpr"] + delta
        if not (0 < v <= lb["sz_unc"]):
            check(f"last-{delta}-in-range", False)
            continue
        t = bytearray(packed)
        struct.pack_into("<I", t, lb["block"] + 4, v)
        try:
            repair(bytes(t))
            check(f"last-{delta}-refused", False)
        except Refused as exc:
            check(f"last-{delta}-refused", str(exc).startswith("stop-boundary"))
    try:
        repair(b"not an elf at all" * 8)
        check("non-elf-refused", False)
    except Refused:
        check("non-elf-refused", True)
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
        # Both targets are validated before the first write, so a refused
        # `--info` cannot leave an `--out` on disk behind an rc 2 (wave-1
        # SentinelWrite MED-2: the contract is "2 = typed refusal, no output").
        checked_target(args.dst)
        if args.info:
            checked_target(args.info)
        write_atomic(args.dst, out)
        if args.info:
            write_atomic(args.info, json.dumps(
                {"tool": TOOL, "class": info.get("class"),
                 **{k: info.get(k) for k in ("break_index", "stored_sz_cpr",
                                             "derived_sz_cpr", "delta",
                                             "uncompressed_accounted")}},
                indent=1, sort_keys=True).encode())
        print(json.dumps({k: info.get(k) for k in
                          ("class", "break_index", "stored_sz_cpr",
                           "derived_sz_cpr", "delta")}, sort_keys=True))
        return 0
    except Refused as exc:
        print(json.dumps({"tool": TOOL, "class": CLASS, "refused": str(exc)}))
        return 2
    except Exception as exc:  # every path is wrapped: no uncaught traceback
        print(json.dumps({"tool": TOOL, "class": CLASS, "error":
                          f"{exc.__class__.__name__}: {exc}"}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
