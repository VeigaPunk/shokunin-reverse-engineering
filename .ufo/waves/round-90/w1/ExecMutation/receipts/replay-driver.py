#!/usr/bin/env python3
"""Replay driver for the round-90 ExecMutation seat (mutation table over the
round-90 instruments). Rebuilds the mirror under a scratch dir, applies the 17
single-edit mutants from receipts/mutants.json, and runs --selftest on each.

  python3 -I -B replay-driver.py <scratch-dir> <seat-receipts-dir>

Requires the lane repo checkout at /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
"""
import json, os, shutil, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FR = "upx-break-repair.py"
FB = "upx-later-block-battery.py"

S, RECP = sys.argv[1], sys.argv[2]
shutil.rmtree(S, ignore_errors=True)
os.makedirs(S, exist_ok=True)
repo = os.path.join(S, "repo"); os.makedirs(os.path.join(repo, "tools"))
for r in ("round-87", "round-88", "round-89", "round-90"):
    shutil.copytree(os.path.join(LANE, "tools", r), os.path.join(repo, "tools", r))
PR = os.path.join(S, "pristine"); os.makedirs(PR)
for f in (FR, FB):
    shutil.copy2(os.path.join(repo, "tools", "round-90", f), os.path.join(PR, f))
    p = subprocess.run(["python3", "-I", "-B", os.path.join(repo, "tools", "round-90", f), "--selftest"],
                       capture_output=True, text=True)
    assert p.returncode == 0, (f, p.returncode, p.stdout, p.stderr)

rows = json.load(open(os.path.join(RECP, "mutants.json")))
for m in rows:
    mid = m["id"]
    d = os.path.join(S, "mut", mid, "tools")
    for r in ("round-87", "round-88", "round-89"):
        os.symlink(os.path.join(repo, "tools", r), os.path.join(d, r))
    os.makedirs(os.path.join(d, "round-90"))
    if m["file"] == FR:
        shutil.copy2(os.path.join(PR, FR), os.path.join(d, "round-90", FR))
        os.symlink(os.path.join(PR, FB), os.path.join(d, "round-90", FB))
    else:
        os.symlink(os.path.join(PR, FR), os.path.join(d, "round-90", FR))
        shutil.copy2(os.path.join(PR, FB), os.path.join(d, "round-90", FB))
    path = os.path.join(d, "round-90", m["file"])
    src = open(path).read()
    old, new = m["old"], m["new"]
    assert src.count(old) == 1, (mid, "old_string count", src.count(old))
    open(path, "w").write(src.replace(old, new, 1))
    p = subprocess.run(["python3", "-I", "-B", path, "--selftest"], capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip()
    status = "KILLED" if p.returncode != 0 else "SURVIVED"
    print(f"{mid} rc={p.returncode} {status} :: {out.splitlines()[0][:120] if out else '(no output)'}")
    with open(os.path.join(RECP, "mut-selftest", f"{mid}.txt"), "w") as fh:
        fh.write(f"cmd: python3 -I -B {path} --selftest\nexit: {p.returncode}\n--- stdout ---\n{p.stdout}\n--- stderr ---\n{p.stderr}")
print("replay complete")
