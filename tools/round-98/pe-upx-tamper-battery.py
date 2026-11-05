#!/usr/bin/env python3
"""pe-upx-tamper-battery.py - round-98 frozen counter for R98-C1 (coverage).

Frontier -> core move: "packed PE inputs" (corpus/README.md round-92
frontier note, `Still Frontier: ... PE and Mach-O packed inputs`).  The
lane's held repair (tools/round-87/upx-magic-repair.py) is ELF-only.  This
battery scores a candidate repair command on UPX 5.2.0 `--best` packed PE
carriers (three win32/pe, three win64/pe; sha256-pinned below) under three
anti-unpack tampers:

  T1 magic   the PackHeader `UPX!` word (first occurrence in the packed file)
             overwritten with four zero bytes.
  T2 names   every section header whose name starts with `UPX` renamed, by
             position, to `.text`, `.data`, `.rdata` (others left as found).
  T3 both    T1 then T2.

Cells (6 carriers x 3 tampers = 18):
  effective  `upx -t <tampered>` exits non-zero (the tamper is real).
  recovered  `python3 -I -B <repair> --in <tampered> --out <repaired>` exits
             0, `upx -t <repaired>` exits 0, and the sha256 of
             `upx -d -o <u> <repaired>` equals the sha256 of `upx -d` of the
             untampered packed file (unpack equivalence; the oracle is the
             packer itself, never the candidate).
Arms:
  intact     the untampered packed file through the candidate: exit 0 and
             the same unpack-equivalence test (6 cells).
  refused    the original UNPACKED carriers t64.exe and WinHelloCPP.exe
             (not UPX) through the candidate: exit 2 and no --out file (2).

Label: `recovered R of 18; intact I of 6; refused F of 2; effective E of 18`.
Frozen predicate (R98-C1): label ==
  `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18`
and exit 0.  Exit 1 otherwise; 2 usage/preflight (pin mismatch, wrong upx).
--work is mandatory (scratch, never /tmp by default); --json-out mandatory.
"""
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys

UPX_VERSION = "upx 5.2.0"
DL = "/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib"
CARRIERS = [
    ("t32", DL + "/t32.exe", "6b4195e640a85ac32eb6f9628822a622057df1e459df7c17a12f97aeabc9415b"),
    ("t64", DL + "/t64.exe", "81a618f21cb87db9076134e70388b6e9cb7c2106739011b6a51772d22cae06b7"),
    ("w32", DL + "/w32.exe", "47872cc77f8e18cf642f868f23340a468e537e64521d9a3a416c8b84384d064b"),
    ("w64", DL + "/w64.exe", "7a319ffaba23a017d7b1e18ba726ba6c54c53d6446db55f92af53c279894f8ad"),
    ("winhello", "/opt/ghidra/docs/GhidraClass/ExerciseFiles/WinhelloCPP/WinHelloCPP.exe",
     "7a98a934de5f578c3a547af873221b221d037bafa87ceee71dd4f089dd228202"),
    ("fastlist64", "/home/vgpnk/.local/share/fnm/node-versions/v22.20.0/installation/lib/"
     "node_modules/pnpm/dist/vendor/fastlist-0.3.0-x64.exe",
     "d1a71f9ac1728082c1b276392725c3e010b98714888579b99152e401abedbf11"),
]
REFUSE = ("t64", "winhello")
TAMPERS = ("magic", "names", "both")
NEW_NAMES = (b".text", b".data", b".rdata")
TARGET = "recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18"


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(argv, timeout=600):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr)[-400:]
    except subprocess.TimeoutExpired:
        return -9, "timeout"


def section_table(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    if b[pe:pe + 4] != b"PE\0\0":
        raise ValueError("not PE")
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    return pe + 24 + opt, n


def tamper(packed, kind):
    b = bytearray(packed)
    if kind in ("magic", "both"):
        i = b.find(b"UPX!")
        if i < 0:
            raise ValueError("no UPX! word")
        b[i:i + 4] = b"\0\0\0\0"
    if kind in ("names", "both"):
        st, n = section_table(b)
        for k in range(min(n, len(NEW_NAMES))):
            off = st + 40 * k
            if bytes(b[off:off + 3]) == b"UPX":
                b[off:off + 8] = NEW_NAMES[k].ljust(8, b"\0")
    return bytes(b)


def unpack_sha(upx, src, work, tag):
    out = os.path.join(work, tag + ".unp")
    if os.path.exists(out):
        os.unlink(out)
    rc, _ = run([upx, "-d", "-q", "-o", out, src])
    return sha(out) if rc == 0 and os.path.exists(out) else None


def repair(cmd, src, dst):
    if os.path.exists(dst):
        os.unlink(dst)
    return run([sys.executable, "-I", "-B", cmd, "--in", src, "--out", dst])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repair-cmd", required=True, help="path to a python repair script")
    ap.add_argument("--upx", default="/usr/bin/upx")
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--rev", default="worktree")
    a = ap.parse_args(argv)
    p = subprocess.run([a.upx, "--version"], capture_output=True, text=True)
    rc, ver = p.returncode, p.stdout
    if rc != 0 or not ver.startswith(UPX_VERSION):
        print("preflight: upx version %r" % ver[:40], file=sys.stderr)
        return 2
    work = os.path.abspath(a.work)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    cells, arms = [], []
    R = I = F = E = 0
    for name, src, pin in CARRIERS:
        if not os.path.exists(src) or sha(src) != pin:
            print("preflight: pin mismatch %s" % name, file=sys.stderr)
            return 2
        orig = os.path.join(work, name + ".exe")
        shutil.copyfile(src, orig)
        packed = os.path.join(work, name + ".upx")
        rc, msg = run([a.upx, "--best", "-q", "-o", packed, orig])
        if rc != 0:
            print("preflight: pack failed %s %s" % (name, msg), file=sys.stderr)
            return 2
        ref = unpack_sha(a.upx, packed, work, name + ".ref")
        if ref is None:
            print("preflight: reference unpack failed %s" % name, file=sys.stderr)
            return 2
        with open(packed, "rb") as fh:
            pb = fh.read()
        # intact arm
        out = os.path.join(work, name + ".intact.rep")
        rrc, rmsg = repair(a.repair_cmd, packed, out)
        ok = rrc == 0 and os.path.exists(out) and unpack_sha(a.upx, out, work, name + ".intact") == ref
        I += ok
        arms.append({"arm": "intact", "carrier": name, "repair_rc": rrc, "ok": ok, "msg": rmsg})
        for kind in TAMPERS:
            tp = os.path.join(work, "%s.%s.tam" % (name, kind))
            with open(tp, "wb") as fh:
                fh.write(tamper(pb, kind))
            trc, _ = run([a.upx, "-t", "-q", tp])
            eff = trc != 0
            E += eff
            out = os.path.join(work, "%s.%s.rep" % (name, kind))
            rrc, rmsg = repair(a.repair_cmd, tp, out)
            got = None
            test_rc = None
            if rrc == 0 and os.path.exists(out):
                test_rc, _ = run([a.upx, "-t", "-q", out])
                if test_rc == 0:
                    got = unpack_sha(a.upx, out, work, "%s.%s" % (name, kind))
            rec = got is not None and got == ref
            R += rec
            cells.append({"carrier": name, "tamper": kind, "effective": eff,
                          "repair_rc": rrc, "test_rc": test_rc, "unpack_sha256": got,
                          "ref_sha256": ref, "recovered": rec, "msg": rmsg})
        if name in REFUSE:
            out = os.path.join(work, name + ".refuse.rep")
            rrc, rmsg = repair(a.repair_cmd, orig, out)
            ok = rrc == 2 and not os.path.exists(out)
            F += ok
            arms.append({"arm": "refused", "carrier": name, "repair_rc": rrc, "ok": ok, "msg": rmsg})
    label = "recovered %d of 18; intact %d of 6; refused %d of 2; effective %d of 18" % (R, I, F, E)
    met = label == TARGET
    receipt = {"tool": "tools/round-98/pe-upx-tamper-battery.py", "rev": a.rev,
               "repair_cmd": a.repair_cmd,
               "repair_sha256": sha(a.repair_cmd) if os.path.exists(a.repair_cmd) else None,
               "counter_sha256": sha(os.path.abspath(__file__)), "upx": ver.splitlines()[0],
               "label": label, "met": met, "exit": 0 if met else 1,
               "cells": cells, "arms": arms}
    with open(a.json_out, "w") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(label, "met", met)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
