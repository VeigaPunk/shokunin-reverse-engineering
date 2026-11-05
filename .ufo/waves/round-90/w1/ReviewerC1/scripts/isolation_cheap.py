#!/usr/bin/env python3
"""Reviewer probe: does a repair that writes a sibling file next to `out`
get caught by the counter's isolation arm?  We run the genuine repair but
pre-place a hidden extra file in the box — the counter lists the whole box
after the child exits, so any extra entry (ours or a cheat's) makes
box_after not in ([ 'in'], ['in','out']) and fails isolation."""
import os, subprocess, sys, tempfile, stat

S = "/fast/scratch/hyaku/kaidoku-r90/ReviewerC1"
repair = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-90/upx-break-repair.py"

def run(cmd, box, extra):
    src, dst = os.path.join(box, "in"), os.path.join(box, "out")
    with open(src, "wb") as fh:
        fh.write(open("/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/work/run/t-jq--7", "rb").read())
    if extra:
        with open(os.path.join(box, "sibling"), "wb") as fh:
            fh.write(b"decoy\n")
    argv = [sys.executable, "-I", "-B", cmd, "--in", src, "--out", dst]
    env = {"HOME": os.path.join(S, "work/home"), "TMPDIR": os.path.join(S, "work/tmp"),
           "LANG": "C", "PATH": "/usr/bin"}
    r = subprocess.run(argv, capture_output=True, env=env)
    return {"rc": r.returncode, "box_after": sorted(os.listdir(box))}

box = tempfile.mkdtemp(prefix="isobox-")
r1 = run(repair, box, False)
print("repair-only box_after:", r1["box_after"], "rc:", r1["rc"])
box2 = tempfile.mkdtemp(prefix="isobox2-")
r2 = run(repair, box2, True)
print("with-pre-seeded-sibling box_after:", r2["box_after"], "rc:", r2["rc"])
# verdict: does the counter's `sorted(after) in (['in'], ['in','out'])` arm catch it?
print("catches_extra:", sorted(os.listdir(box2)) not in (["in"], ["in", "out"]))
