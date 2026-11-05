#!/usr/bin/env python3
"""pe-upx-trunc-battery.py - round-99 frozen counter for R99-C2 (coverage).

Frontier -> core move: "truncated payloads" of UPX-packed PE (corpus/README.md
Round-98 frontier note: "Mach-O, PE DLLs, other offsets, UPX2 sections and
truncated payloads stay Frontier").  The round-98 repair answers `ok intact`,
exit 0, on a pack truncated inside its sections, where `upx -t` fails with
`OverlayException: invalid overlay size` (UPX 5.2.0 `Packer::checkOverlay`,
S326; overlay computed in `PeFile::unpack0`, S324).  A candidate must refuse
those inputs while still repairing every round-98 tamper, on a population that
the round-98 forgeries cannot pass (non-992 PackHeader offset, DLLs, `UPX2`
third sections, runtime-random overlays, a checksum-invalid decoy).

Candidate bytes are read with `git show <rev>:<repair path>` when --rev is a
commit (never from the working tree), so a dirty tree cannot be scored.

Carriers (10, sha256-pinned): the six round-98 carriers plus four DLLs.
Every carrier is packed in --work with `upx --best -q -f`.  The packer is the
oracle; the candidate is never trusted.

Arms (per carrier unless stated):
  recovered  T1 magic / T2 names / T3 both tampers (as round 98): candidate
             rc 0, `upx -t` of its output rc 0, sha256(`upx -d`) equal to the
             untampered pack's (30 cells).
  decoy      T1 plus a checksum-invalid PackHeader look-alike (version and
             format bytes copied to the gate window start, see decoy()):
             recovered as above.  Applies to the 9 carriers whose two decoy
             bytes are zero in the pack (all but sevenzip64dll, whose window
             start lies in its section table) (9).
  intact     the untampered pack: rc 0 and unpack equivalence (10).
  overlay    the untampered pack, and its T3 tamper, with a runtime-random
             overlay (os.urandom length 1..4096, random bytes) appended:
             rc 0 and sha256(`upx -d` of output) equal to sha256(`upx -d` of the
             untampered pack + the same overlay) (20).
  truncated  untampered and T3, each cut at (a) ALIGN_UP(last section
             rawdataptr + SizeOfRawData, FileAlignment) - 1 and (b) UPX1
             rawdataptr + SizeOfRawData/2 (40): `upx -t` of the cut input
             rc != 0 (effective) and the candidate rc 2, no --out file, and
             `truncated` in its stderr.
  refused    the unpacked carriers t64 and winhello (not UPX): rc 2, no --out
             (2).
  cli        (1) --in names a missing file, (2) --out in a missing directory,
             (3) --out is an existing directory: rc 2, no `Traceback` in the
             output, nothing created (3).
  static     candidate source text contains none of the FORBIDDEN tokens
             (process spawning, dynamic import, exec/eval) (1).  The packer must
             not be the candidate's own oracle.  A text screen, not a sandbox.
  effective  `upx -t` of every tampered, decoy and truncated input is non-zero
             (30 + 9 + 40 = 79).

Label: `recovered R of 30; decoy D of 9; intact I of 10; overlay O of 20;
truncated T of 40; refused F of 2; cli C of 3; static S of 1; effective E of 79`.
Frozen predicate (R99-C2): label equals TARGET and exit 0.  Exit 1 otherwise;
2 usage/preflight (pin mismatch, wrong upx, pack failure, unreadable rev).
--work and --json-out are mandatory; nothing is written under /tmp unless
--work points there.
"""
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys

TOOL = "tools/round-99/pe-upx-trunc-battery.py"
UPX_VERSION = "upx 5.2.0"
DL = "/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib"
OGL = "/usr/lib/python3.14/site-packages/OpenGL/DLLS"
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
    ("freeglut32dll", OGL + "/freeglut32.vc14.dll",
     "c9c00a4ea9b9fecdcae81f6facaf27e349714d56fe7640ce9c37ed38841a0b87"),
    ("gle64dll", OGL + "/gle64.vc9.dll",
     "b427510af633a6298481e738942f3268daedf44d6c01af74620579034bede9ce"),
    ("llio32dll", "/opt/ghidra/GPL/DMG/data/os/win_x86_32/llio_i386.dll",
     "e855478acf0d36f846befb48bfd239b7ef46e568e2408091591adec274ed0879"),
    ("sevenzip64dll", "/opt/ghidra/Ghidra/Features/FileFormats/data/sevenzipnativelibs/"
     "Windows-amd64/lib7-Zip-JBinding.dll",
     "c769642c8a489e8fc078b8387fb9865ac5c5482ce22301a40d00145fa1304b27"),
]
REFUSE = ("t64", "winhello")
TAMPERS = ("magic", "names", "both")
NEW_NAMES = (b".text", b".data", b".rdata")
FORBIDDEN = ("subprocess", "os.system", "os.exec", "os.spawn", "os.popen", "posix_spawn",
             "os.fork", "from os import", "import pty", "ctypes", "importlib", "__import__",
             "exec(", "eval(", "runpy")
TARGET = ("recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; "
          "truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79")


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(path):
    with open(path, "rb") as fh:
        return sha_bytes(fh.read())


def run(argv, timeout=600):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return -9, "timeout"


def pe_layout(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    if b[pe:pe + 4] != b"PE\0\0":
        raise ValueError("not PE")
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    falign = struct.unpack_from("<I", b, pe + 24 + 36)[0]
    st = pe + 24 + opt
    secs = [struct.unpack_from("<II", b, st + 40 * k + 16) for k in range(n)]  # (rsize, rptr)
    return st, n, falign, secs


def align_up(v, a):
    return (v + a - 1) // a * a


def tamper(packed, kind):
    b = bytearray(packed)
    if kind in ("magic", "both"):
        i = b.find(b"UPX!")
        if i < 0:
            raise ValueError("no UPX! word")
        b[i:i + 4] = b"\0\0\0\0"
    if kind in ("names", "both"):
        st, n, _, _ = pe_layout(b)
        for k in range(min(n, len(NEW_NAMES))):
            off = st + 40 * k
            if bytes(b[off:off + 3]) == b"UPX":
                b[off:off + 8] = NEW_NAMES[k].ljust(8, b"\0")
    return bytes(b)


def decoy(packed):
    """T1 plus a look-alike at the gate window start j = UPX1 rawdataptr - 64:
    only bytes j+4 (version) and j+5 (format) are written, copied from the real
    PackHeader, so its checksum byte (j+31) does not validate.  Applicable only
    when those two bytes are zero in the pack; None otherwise."""
    i = packed.find(b"UPX!")
    _, _, _, secs = pe_layout(packed)
    j = secs[1][1] - 64
    if j < 0 or j + 32 > i or packed[j + 4:j + 6] != b"\0\0":
        return None
    b = bytearray(tamper(packed, "magic"))
    b[j + 4] = packed[i + 4]
    b[j + 5] = packed[i + 5]
    return bytes(b)


def cuts(packed):
    _, _, falign, secs = pe_layout(packed)
    rsize_l, rptr_l = secs[-1]
    end = align_up(rptr_l + rsize_l, falign)
    rsize1, rptr1 = secs[1]
    return {"end-1": end - 1, "upx1-mid": rptr1 + rsize1 // 2}


def unpack_sha(upx, src, work, tag):
    out = os.path.join(work, tag + ".unp")
    if os.path.exists(out):
        os.unlink(out)
    rc, _ = run([upx, "-d", "-q", "-o", out, src])
    return sha(out) if rc == 0 and os.path.exists(out) else None


def write(path, data):
    with open(path, "wb") as fh:
        fh.write(data)


def candidate(cmd, inp, out):
    if out and os.path.isfile(out):
        os.unlink(out)
    return run([sys.executable, "-I", "-B", cmd, "--in", inp, "--out", out])


def load_candidate(root, rev, rel, work):
    dst = os.path.join(work, "candidate.py")
    if rev == "worktree":
        shutil.copyfile(os.path.join(root, rel), dst)
    else:
        p = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, rel)], capture_output=True)
        if p.returncode != 0:
            raise ValueError("cannot read %s at %s" % (rel, rev))
        write(dst, p.stdout)
    return dst


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="lane repo root")
    ap.add_argument("--repair", required=True, help="repo-relative path of the candidate repair")
    ap.add_argument("--rev", required=True, help="commit to read the candidate from, or 'worktree'")
    ap.add_argument("--upx", default="/usr/bin/upx")
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out", required=True)
    a = ap.parse_args(argv)
    p = subprocess.run([a.upx, "--version"], capture_output=True, text=True)
    ver = p.stdout
    if p.returncode != 0 or not ver.startswith(UPX_VERSION):
        print("preflight: upx version %r" % ver[:40], file=sys.stderr)
        return 2
    work = os.path.abspath(a.work)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    rev = a.rev
    if rev != "worktree":
        q = subprocess.run(["git", "-C", a.root, "rev-parse", "--verify", rev + "^{commit}"],
                           capture_output=True, text=True)
        if q.returncode != 0:
            print("preflight: unreadable rev %s" % rev, file=sys.stderr)
            return 2
        rev = q.stdout.strip()
    try:
        cmd = load_candidate(a.root, rev, a.repair, work)
    except ValueError as e:
        print("preflight: %s" % e, file=sys.stderr)
        return 2
    with open(cmd, "rb") as fh:
        src_text = fh.read().decode("utf-8", "replace")
    cells = []
    n = {"recovered": 0, "decoy": 0, "decoy_cells": 0, "intact": 0, "overlay": 0, "truncated": 0,
         "refused": 0, "cli": 0, "static": 0, "effective": 0}

    def tampered_cell(arm, name, tag, data, ref):
        tp = os.path.join(work, "%s.%s.in" % (name, tag))
        write(tp, data)
        trc, _ = run([a.upx, "-t", "-q", tp])
        eff = trc != 0
        out = os.path.join(work, "%s.%s.out" % (name, tag))
        rrc, msg = candidate(cmd, tp, out)
        got = test_rc = None
        if rrc == 0 and os.path.exists(out):
            test_rc, _ = run([a.upx, "-t", "-q", out])
            if test_rc == 0:
                got = unpack_sha(a.upx, out, work, "%s.%s" % (name, tag))
        ok = got is not None and got == ref
        cells.append({"arm": arm, "carrier": name, "case": tag, "effective": eff,
                      "candidate_rc": rrc, "test_rc": test_rc, "unpack_sha256": got,
                      "ref_sha256": ref, "ok": ok, "msg": msg[-300:]})
        return ok, eff

    for name, srcp, pin in CARRIERS:
        if not os.path.exists(srcp) or sha(srcp) != pin:
            print("preflight: pin mismatch %s" % name, file=sys.stderr)
            return 2
        orig = os.path.join(work, name + ".orig")
        shutil.copyfile(srcp, orig)
        packed = os.path.join(work, name + ".upx")
        rc, msg = run([a.upx, "--best", "-q", "-f", "-o", packed, orig])
        if rc != 0:
            print("preflight: pack failed %s %s" % (name, msg[-200:]), file=sys.stderr)
            return 2
        ref = unpack_sha(a.upx, packed, work, name + ".ref")
        if ref is None:
            print("preflight: reference unpack failed %s" % name, file=sys.stderr)
            return 2
        with open(packed, "rb") as fh:
            pb = fh.read()
        # intact
        out = os.path.join(work, name + ".intact.out")
        rrc, msg = candidate(cmd, packed, out)
        ok = rrc == 0 and os.path.exists(out) and unpack_sha(a.upx, out, work, name + ".intact") == ref
        n["intact"] += ok
        cells.append({"arm": "intact", "carrier": name, "candidate_rc": rrc, "ok": ok, "msg": msg[-300:]})
        for kind in TAMPERS:
            ok, eff = tampered_cell("recovered", name, kind, tamper(pb, kind), ref)
            n["recovered"] += ok
            n["effective"] += eff
        dec = decoy(pb)
        if dec is not None:
            n["decoy_cells"] += 1
            ok, eff = tampered_cell("decoy", name, "decoy", dec, ref)
            n["decoy"] += ok
            n["effective"] += eff
        # overlay (runtime random)
        ov = os.urandom(1 + int.from_bytes(os.urandom(2), "little") % 4096)
        ovp = os.path.join(work, name + ".ovref.in")
        write(ovp, pb + ov)
        ref_ov = unpack_sha(a.upx, ovp, work, name + ".ovref")
        for tag, data in (("ov-intact", pb + ov), ("ov-both", tamper(pb, "both") + ov)):
            tp = os.path.join(work, "%s.%s.in" % (name, tag))
            write(tp, data)
            out = os.path.join(work, "%s.%s.out" % (name, tag))
            rrc, msg = candidate(cmd, tp, out)
            got = None
            if rrc == 0 and os.path.exists(out):
                got = unpack_sha(a.upx, out, work, "%s.%s" % (name, tag))
            ok = ref_ov is not None and got == ref_ov
            n["overlay"] += ok
            cells.append({"arm": "overlay", "carrier": name, "case": tag, "overlay_len": len(ov),
                          "candidate_rc": rrc, "unpack_sha256": got, "ref_sha256": ref_ov,
                          "ok": ok, "msg": msg[-300:]})
        # truncated
        for base_tag, base in (("intact", pb), ("both", tamper(pb, "both"))):
            for cut_tag, at in sorted(cuts(pb).items()):
                tag = "trunc-%s-%s" % (base_tag, cut_tag)
                tp = os.path.join(work, "%s.%s.in" % (name, tag))
                write(tp, base[:at])
                trc, _ = run([a.upx, "-t", "-q", tp])
                eff = trc != 0
                n["effective"] += eff
                out = os.path.join(work, "%s.%s.out" % (name, tag))
                rrc, msg = candidate(cmd, tp, out)
                ok = rrc == 2 and not os.path.exists(out) and "truncated" in msg
                n["truncated"] += ok
                cells.append({"arm": "truncated", "carrier": name, "case": tag, "cut": at,
                              "size": len(pb), "effective": eff, "candidate_rc": rrc,
                              "ok": ok, "msg": msg[-300:]})
        if name in REFUSE:
            out = os.path.join(work, name + ".refuse.out")
            rrc, msg = candidate(cmd, orig, out)
            ok = rrc == 2 and not os.path.exists(out)
            n["refused"] += ok
            cells.append({"arm": "refused", "carrier": name, "candidate_rc": rrc, "ok": ok,
                          "msg": msg[-300:]})
    # cli envelope
    some_packed = os.path.join(work, "t32.upx")
    cli_dir = os.path.join(work, "cli")
    os.makedirs(cli_dir)
    existing_dir = os.path.join(cli_dir, "is-a-dir")
    os.makedirs(existing_dir)
    cases = [("missing-in", os.path.join(cli_dir, "no-such-input"), os.path.join(cli_dir, "o1")),
             ("missing-out-dir", some_packed, os.path.join(cli_dir, "no-such-dir", "o2")),
             ("out-is-dir", some_packed, existing_dir)]
    for tag, inp, out in cases:
        before = sorted(os.listdir(cli_dir))
        rc, msg = run([sys.executable, "-I", "-B", cmd, "--in", inp, "--out", out])
        after = sorted(os.listdir(cli_dir))
        ok = (rc == 2 and "Traceback" not in msg and before == after
              and os.listdir(existing_dir) == [])
        n["cli"] += ok
        cells.append({"arm": "cli", "case": tag, "candidate_rc": rc, "ok": ok, "msg": msg[-300:]})
    hits = [t for t in FORBIDDEN if t in src_text]
    n["static"] = int(not hits)
    cells.append({"arm": "static", "forbidden_hits": hits, "ok": not hits})
    label = ("recovered %(recovered)d of 30; decoy %(decoy)d of %(decoy_cells)d; intact %(intact)d of 10; "
             "overlay %(overlay)d of 20; truncated %(truncated)d of 40; refused %(refused)d of 2; "
             "cli %(cli)d of 3; static %(static)d of 1; effective %(effective)d of 79") % n
    met = label == TARGET
    receipt = {"tool": TOOL, "rev": rev, "repair": a.repair, "repair_sha256": sha(cmd),
               "counter_sha256": sha(os.path.abspath(__file__)), "upx": ver.splitlines()[0],
               "label": label, "target": TARGET, "met": met, "exit": 0 if met else 1,
               "counts": n, "cells": cells}
    tmp = a.json_out + ".partial"
    with open(tmp, "w") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, a.json_out)
    print(label, "met", met)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
