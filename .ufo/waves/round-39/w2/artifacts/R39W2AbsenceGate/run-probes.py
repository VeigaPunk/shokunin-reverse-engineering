#!/usr/bin/env python3
"""Behavioral probes for the surviving mutants, on scratch fixtures.

Every probe runs the pristine script and the mutant side by side on the same
fixture and prints both exit codes and the discriminating output line.
"""
import os
import shutil
import subprocess

S = os.path.dirname(os.path.abspath(__file__))
os.chdir(S)
os.makedirs("out", exist_ok=True)
env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH="/fast/scratch/hyaku")
R7 = "lanes/kaidoku/round7/work/r7-local-measurements.tsv"


def run(script, args, timeout=30):
    p = subprocess.run(["timeout", str(timeout), "python3", "-I", "-B", script] + args,
                       capture_output=True, text=True, env=env, timeout=timeout + 20)
    return p.returncode, (p.stdout + p.stderr).strip()


def mk(root, rel, data=b"x"):
    path = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    return path


def last(lines, prefix):
    for l in reversed(lines):
        if l.startswith(prefix):
            return l
    return "(none)"


shutil.rmtree("fx", ignore_errors=True)
os.makedirs("fx")
print("uid=%d (EACCES probes require non-root)" % os.getuid())
print()

# --- m04: directory symlinks (contract: directory symlinks are not followed) ---
ds = os.path.abspath("fx/ds")
mk(ds, "outside/lanes/kaidoku/round7/work/r7-local-measurements.tsv")
os.makedirs(ds + "/root")
os.symlink("../outside", ds + "/root/link")
for name, script in [("pristine", "pristine.py"),
                     ("m04-follow-dir-symlinks", "mut/m04-follow-dir-symlinks.py")]:
    rc, out = run(script, ["--claim", R7, "--root", ds + "/root"])
    ls = out.splitlines()
    print("[m04 dir-symlink] %-24s rc=%s %s" % (name, rc, last(ls, "VERDICT")))
    for l in ls:
        if l.startswith("HIT"):
            print("      %s" % l)

cy = os.path.abspath("fx/cy")
os.makedirs(cy + "/root")
os.symlink(cy + "/root", cy + "/root/self")
for name, script in [("pristine", "pristine.py"),
                     ("m04-follow-dir-symlinks", "mut/m04-follow-dir-symlinks.py")]:
    rc, out = run(script, ["--claim", R7, "--root", cy + "/root"], timeout=15)
    ls = out.splitlines()
    print("[m04 self-cycle]  %-24s rc=%s %s" % (name, rc, last(ls, "VERDICT")))
print()

# --- m07: unreadable root (probe dropped vs kept) ---
ur = os.path.abspath("fx/ur")
mk(ur, "root/keep/x.txt")
os.chmod(ur + "/root", 0o000)
try:
    for name, script in [("pristine", "pristine.py"),
                         ("m07-root-probe-dropped", "mut/m07-root-probe-dropped.py")]:
        rc, out = run(script, ["--claim", R7, "--root", ur + "/root"])
        ls = out.splitlines()
        print("[m07 unread-root] %-24s rc=%s %s" % (name, rc, " | ".join(ls[:2])))
finally:
    os.chmod(ur + "/root", 0o755)
print()

# --- m10: EXIT_ERROR constant drift (documented contract: usage/unreadable -> 2) ---
nope = os.path.abspath("fx/nope")
for name, script in [("pristine", "pristine.py"),
                     ("m10-error-code-three", "mut/m10-error-code-three.py")]:
    rc, out = run(script, ["--claim", R7, "--root", nope])
    ls = out.splitlines()
    print("[m10 missing-root] %-23s rc=%s %s" % (name, rc, ls[0] if ls else "(none)"))
print()

# --- m16: PRESENT constant drift (documented contract: PRESENT -> 1) ---
pr = os.path.abspath("fx/pr")
mk(pr, "root/" + R7)
for name, script in [("pristine", "pristine.py"),
                     ("m16-present-constant-five", "mut/m16-present-constant-five.py")]:
    rc, out = run(script, ["--claim", R7, "--root", pr + "/root"])
    ls = out.splitlines()
    print("[m16 present-rc]  %-24s rc=%s %s" % (name, rc, last(ls, "VERDICT")))
print()

# --- m03: case-variant file (contract: literal component match) ---
ci = os.path.abspath("fx/ci")
mk(ci, "root/lanes/kaidoku/round7/work/R7-LOCAL-MEASUREMENTS.TSV")
for name, script in [("pristine", "pristine.py"),
                     ("m03-case-insensitive", "mut/m03-case-insensitive.py")]:
    rc, out = run(script, ["--claim", R7, "--root", ci + "/root"])
    ls = out.splitlines()
    print("[m03 case-variant] %-24s rc=%s %s" % (name, rc, last(ls, "VERDICT")))
print()

# --- m13: root order dependence (nested roots, inner listed first) ---
ni = os.path.abspath("fx/ni")
mk(ni, "outer/" + R7)
outer, inner = ni + "/outer", ni + "/outer/lanes"
for order, roots in [("outer-first", [outer, inner]), ("inner-first", [inner, outer])]:
    for name, script in [("pristine", "pristine.py"),
                         ("m13-no-length-sort", "mut/m13-no-length-sort.py")]:
        rc, out = run(script, ["--claim", R7, "--root", roots[0], "--root", roots[1]])
        ls = out.splitlines()
        print("[m13 %-12s] %-24s rc=%s %s" % (order, name, rc, last(ls, "VERDICT")))
print()

# --- m17: duplicate roots via symlinked path (dedup is by realpath) ---
sr = os.path.abspath("fx/sr")
mk(sr, "a/" + R7)
os.symlink(sr + "/a", sr + "/b")
a, b = sr + "/a", sr + "/b"
for name, script in [("pristine", "pristine.py"),
                     ("m17-dedup-no-realpath", "mut/m17-dedup-no-realpath.py")]:
    rc, out = run(script, ["--claim", R7, "--root", a, "--root", b])
    ls = out.splitlines()
    print("[m17 symlink-roots] %-23s rc=%s %s" % (name, rc, last(ls, "VERDICT")))
    for l in ls:
        if l.startswith("HIT"):
            print("      %s" % l)
