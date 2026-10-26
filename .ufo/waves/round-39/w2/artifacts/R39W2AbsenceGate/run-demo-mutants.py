#!/usr/bin/env python3
"""Run the bounded round-38 demonstration (r7 fleet-root / r7 both-roots) with
every mutant and compare exit code + normalized output against a fresh pristine
run of the same tree state.

m04-follow-dir-symlinks is SKIPPED on the real trees: following directory
symlinks can traverse out of the two permitted roots via absolute symlinks and
can blow up traversal size on symlink farms. It is probed on scratch fixtures
instead (run-probes.py).
"""
import os
import re
import subprocess

S = os.path.dirname(os.path.abspath(__file__))
os.chdir(S)
os.makedirs("out", exist_ok=True)
env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH="/fast/scratch/hyaku")

FLEET = "/home/vgpnk/Projects/shokunin"
KNOW = "/home/vgpnk/Projects/shokuknow"
R7 = "lanes/kaidoku/round7/work/r7-local-measurements.tsv"
SKIP_REAL_TREE = {"m04-follow-dir-symlinks"}

ARMS = {
    "r7-fleet": ["--claim", R7, "--root", FLEET],
    "r7-both": ["--claim", R7, "--root", FLEET, "--root", KNOW],
}


def norm(text):
    # The fleet tree is live (sibling waves write into it), so traversal counters
    # drift between runs; compare rc, verdict, hits, hit paths, notes only.
    text = re.sub(r"elapsed=[0-9.]+s", "elapsed=X", text)
    text = re.sub(r"dirs_walked=[0-9]+", "dirs_walked=X", text)
    text = re.sub(r"entries_seen=[0-9]+", "entries_seen=X", text)
    return text


def run(script, args, timeout=120):
    p = subprocess.run(["timeout", str(timeout), "python3", "-I", "-B", script] + args,
                       capture_output=True, text=True, env=env, timeout=timeout + 30)
    return p.returncode, p.stdout + p.stderr


base = {}
for tag, args in ARMS.items():
    rc, out = run("pristine.py", args)
    base[tag] = (rc, norm(out))
    with open(os.path.join("out", "demo-base-%s.txt" % tag), "w") as fh:
        fh.write(out)
    print("pristine %-9s rc=%s" % (tag, rc))

print()
for fn in sorted(os.listdir("mut")):
    if not fn.endswith(".py"):
        continue
    name = fn[:-3]
    if name in SKIP_REAL_TREE:
        print("%-32s skipped-on-real-trees (symlink-follow hazard; see scratch probes)" % name)
        continue
    diffs = []
    for tag, args in ARMS.items():
        rc, out = run(os.path.join("mut", fn), args)
        with open(os.path.join("out", "demo-%s-%s.txt" % (name, tag)), "w") as fh:
            fh.write(out)
        brc, bout = base[tag]
        if rc == brc and norm(out) == bout:
            diffs.append("%s=SAME(rc=%s)" % (tag, rc))
        else:
            diffs.append("%s=DIFF(mut_rc=%s base_rc=%s)" % (tag, rc, brc))
    print("%-32s %s" % (name, "  ".join(diffs)))
