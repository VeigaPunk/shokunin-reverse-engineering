#!/usr/bin/env python3
"""ExecReproC1 hand-derived R98-C1 oracle cells.

Own tamper implementation (derived from the claim text, not imported from the
battery): T1 zero the first PackHeader `UPX!` word; T2 rename the first three
section headers whose name starts with `UPX`, positionally, to
.text/.data/.rdata; T3 = T1 then T2.  Oracle: sha256(upx -d repaired) ==
sha256(upx -d untampered pack).  Usage:
  hand_cell.py <repair-script-abs> <receipts-dir>
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

UPX = "/usr/bin/upx"
PINNED = {
    "t32": ("/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib/t32.exe",
            "6b4195e640a85ac32eb6f9628822a622057df1e459df7c17a12f97aeabc9415b", "magic"),
    "w64": ("/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib/w64.exe",
            "7a319ffaba23a017d7b1e18ba726ba6c54c53d6446db55f92af53c279894f8ad", "names"),
    "winhello": ("/opt/ghidra/docs/GhidraClass/ExerciseFiles/WinhelloCPP/WinHelloCPP.exe",
                 "7a98a934de5f578c3a547af873221b221d037bafa87ceee71dd4f089dd228202", "both"),
}
NEW_NAMES = (b".text", b".data", b".rdata")


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1] if (p.stdout + p.stderr).strip() else ""


def sec_table(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    assert b[pe:pe + 4] == b"PE\0\0", "not PE"
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    return pe + 24 + opt, n


def my_tamper(data, kind):
    b = bytearray(data)
    if kind in ("magic", "both"):
        i = b.find(b"UPX!")
        assert i >= 0, "no UPX! word"
        b[i:i + 4] = b"\x00\x00\x00\x00"
    if kind in ("names", "both"):
        st, n = sec_table(b)
        for k in range(min(n, 3)):
            off = st + 40 * k
            if bytes(b[off:off + 3]) == b"UPX":
                b[off:off + 8] = NEW_NAMES[k].ljust(8, b"\x00")
    return bytes(b)


def cell(name, work):
    src, pin, kind = PINNED[name]
    rec = {"cell": name, "carrier": os.path.basename(src), "pin": pin, "tamper": kind}
    rec["carrier_sha256"] = sha(src)
    rec["pin_ok"] = rec["carrier_sha256"] == pin
    orig = os.path.join(work, name + ".exe")
    with open(src, "rb") as fh:
        data = fh.read()
    with open(orig, "wb") as fh:
        fh.write(data)
    packed = os.path.join(work, name + ".upx")
    rec["pack_rc"], rec["pack_msg"] = run([UPX, "--best", "-q", "-o", packed, orig])
    ref = os.path.join(work, name + ".ref")
    rec["refunpack_rc"], _ = run([UPX, "-d", "-q", "-o", ref, packed])
    rec["ref_sha256"] = sha(ref) if rec["refunpack_rc"] == 0 else None
    rec["ref_equals_carrier"] = rec["ref_sha256"] == rec["carrier_sha256"]
    tampered = os.path.join(work, name + ".t.upx")
    with open(packed, "rb") as fh:
        tb = my_tamper(fh.read(), kind)
    with open(tampered, "wb") as fh:
        fh.write(tb)
    rec["tampered_t_rc"], rec["tampered_t_msg"] = run([UPX, "-t", tampered])
    rec["effective"] = rec["tampered_t_rc"] != 0
    repaired = os.path.join(work, name + ".rep")
    rrc, rms = run([sys.executable, "-I", "-B", sys.argv[1], "--in", tampered, "--out", repaired])
    rec["repair_rc"], rec["repair_msg"] = rrc, rms
    rec["repair_wrote_out"] = os.path.exists(repaired)
    if rec["repair_wrote_out"]:
        rec["repaired_t_rc"], _ = run([UPX, "-t", repaired])
        unp = os.path.join(work, name + ".rep.unp")
        rec["repaired_d_rc"], _ = run([UPX, "-d", "-q", "-o", unp, repaired])
        rec["unpacked_sha256"] = sha(unp) if rec["repaired_d_rc"] == 0 else None
        rec["recovered"] = rec["unpacked_sha256"] == rec["ref_sha256"]
    else:
        rec["repaired_t_rc"] = rec["repaired_d_rc"] = None
        rec["unpacked_sha256"] = None
        rec["recovered"] = False
    rec["ok"] = bool(rec["pin_ok"] and rec["effective"] and rec["recovered"]
                     and rec["repair_rc"] == 0 and rec["repaired_t_rc"] == 0)
    return rec


def main():
    work = os.path.abspath(sys.argv[2])
    os.makedirs(work, exist_ok=True)
    recs = [cell(n, work) for n in ("t32", "w64", "winhello")]
    with open(os.path.join(work, "hand-cells.json"), "w") as fh:
        json.dump({"cells": recs, "upx": subprocess.run([UPX, "--version"], capture_output=True, text=True).stdout.splitlines()[0]}, fh, indent=1)
    for r in recs:
        print("HAND %s/%s: pin_ok=%s effective=%s repair_rc=%s recovered=%s ok=%s"
              % (r["cell"], r["tamper"], r["pin_ok"], r["effective"], r["repair_rc"], r["recovered"], r["ok"]))
    print("HAND_ALL_OK=%s" % all(r["ok"] for r in recs))


if __name__ == "__main__":
    main()
