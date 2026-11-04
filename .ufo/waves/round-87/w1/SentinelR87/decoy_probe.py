#!/usr/bin/env python3
"""SentinelR87 decoy-sentinel probe (round 87).  Read-only on the repo.

Usage: python3 -I -B decoy_probe.py <scratch-dir>
Packs jq and docker-init with /usr/bin/upx --best into <scratch-dir>, applies T1
(every UPX! -> 00000000), plants a 25-byte decoy (one plausible b_info of the
chain's method + a 12-byte zero sentinel) 64 bytes after the first chain walk's
stop offset (inside the loader stub), and reports where the repair writes.
"""
import importlib.util, os, shutil, struct, subprocess, sys

TOOL = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-87/upx-magic-repair.py"
spec = importlib.util.spec_from_file_location("rep", TOOL)
rep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rep)
R = sys.argv[1]
os.makedirs(R, exist_ok=True)
for cid, src in (("jq", "/usr/bin/jq"), ("dinit", "/usr/bin/docker-init")):
    shutil.copy(src, f"{R}/{cid}.orig")
    subprocess.run(["/usr/bin/upx", "-q", "--best", "-f", "-o", f"{R}/{cid}.packed", f"{R}/{cid}.orig"],
                   capture_output=True, check=True)
    p = open(f"{R}/{cid}.packed", "rb").read()
    t = p.replace(b"UPX!", b"\0" * 4)
    ph_off, ph = rep.find_packheader(t)
    lm, s, info = rep.find_linfo(t, ph_off, ph)
    stop, _, meth = rep.walk_chain(t, lm + 20, ph_off, None)
    at = stop + 64
    decoy = struct.pack("<IIBBBB", 2, 1, meth, 0, 0, 0) + b"\x01" + b"\0" * 12
    for label, base in (("tampered+decoy", t), ("intact+decoy", p)):
        d = bytearray(base); d[at:at + len(decoy)] = decoy; d = bytes(d)
        f = f"{R}/{cid}.{label}"
        open(f, "wb").write(d)
        out, inf = rep.repair(d)
        open(f + ".rep", "wb").write(out)
        tin = subprocess.run(["/usr/bin/upx", "-t", "-q", f], capture_output=True).returncode
        tout = subprocess.run(["/usr/bin/upx", "-t", "-q", f + ".rep"], capture_output=True).returncode
        print(f"{cid} {label}: real_sentinel={s} decoy_at={at} tool_b_info_end={inf['anchors']['b_info_end']} "
              f"restored={[r['anchor'] for r in inf['restored']]} real_end_after={out[s + 4:s + 8].hex()} "
              f"upx_t(input)={tin} upx_t(repaired)={tout}")
