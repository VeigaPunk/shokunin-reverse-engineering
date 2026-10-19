#!/usr/bin/env python3
"""EX-23 after-state attacks — refutation attempts against the landed sidecar guard.

Every probe runs on a scratch COPY of the tool; the real target is read-only.
usage: python3 after-attacks.py <tool.py> <scratch-root> <label>
"""

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

TOOL = Path(sys.argv[1]).resolve()
ROOT = Path(sys.argv[2]).resolve()
LABEL = sys.argv[3] if len(sys.argv) > 3 else "attacks"


def sha256(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return "ABSENT"


def run(argv, cwd, tool=None):
    p = subprocess.run([sys.executable, str(tool or TOOL)] + argv, cwd=str(cwd),
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def box(name):
    d = ROOT / LABEL / name
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    return d


def report(name, rc, so, se, facts, verdict):
    print("=" * 78)
    print("ATTACK %s  label=%s tool=%s" % (name, LABEL, sha256(TOOL)))
    print("  exit=%d" % rc)
    for line in (se.strip() or so.strip()).splitlines()[:4]:
        print("  | %s" % line)
    for k, v in facts.items():
        print("  %-34s %s" % (k + ":", v))
    print("  VERDICT: %s" % verdict)


# F — symlink sidecar vector: the derived sidecar path is a SYMLINK to the
# measured file.  Path resolution must catch it (resolve() follows symlinks).
d = box("F-symlink-sidecar")
(d / "vic.conf").write_bytes(b"measured through a symlink sidecar\n")
before = sha256(d / "vic.conf")
os.symlink("vic.conf", d / "out.txt.sha256")     # sidecar path -> symlink -> measured
rc, so, se = run(["capture", "--out", "out.txt", "--paths", "vic.conf"], d)
after = sha256(d / "vic.conf")
report("F-symlink-sidecar-to-measured", rc, so, se,
       {"measured before": before[:16], "measured after": after[:16],
        "receipt written": (d / "out.txt").exists()},
       "REFUTED-IF-CLOBBERED" if after != before else
       ("REFUSED-AS-DECLARED" if rc == 2 else "OPEN-EXIT%d" % rc))

# G — relative spelling: `cd` into the fixture dir, use `./x.sha256` vs `x`.
d = box("G-relative-spelling")
(d / "vic").write_bytes(b"measured file, relative spelling\n")
before = sha256(d / "vic")
rc, so, se = run(["capture", "--out", "./vic.sha256", "--paths", "./vic"], d)
after = sha256(d / "vic")
report("G-relative-spelling", rc, so, se,
       {"measured before": before[:16], "measured after": after[:16]},
       "REFUTED-IF-CLOBBERED" if after != before else
       ("REFUSED-AS-DECLARED" if rc == 2 else "OPEN-EXIT%d" % rc))

# H — over-refusal control: a receipt legitimately NAMED <x>.sha256 whose stem is
# NOT a measured path must still be written (the guard must not blanket-ban the
# name pattern).
d = box("H-overrefusal-control")
(d / "p.conf").write_bytes(b"measured p\n")
(d / "q.sha256").write_bytes(b"unrelated bystander\n")
rc, so, se = run(["capture", "--out", "q.sha256", "--paths", "p.conf"], d)
ok = rc == 0 and (d / "q.sha256").read_bytes().startswith(b"# custody-pair receipt")
report("H-overrefusal-control", rc, so, se,
       {"q.sha256 is a receipt": (d / "q.sha256").read_bytes().startswith(b"# custody-pair receipt"),
        "q.sha256.sha256 sidecar": (d / "q.sha256.sha256").exists()},
       "PASS (no over-refusal)" if ok else "OVER-REFUSAL-DETECTED exit=%d" % rc)

# I — --out with no usable name: sidecar derivation must be a declared USAGE.
for spelling in ("", "."):
    d = box("I-emptyname" + ("-dot" if spelling else "-empty"))
    (d / "p.conf").write_bytes(b"measured p\n")
    rc, so, se = run(["capture", "--out", spelling, "--paths", "p.conf"], d)
    traceback = "Traceback" in se
    report("I-out=%r" % spelling, rc, so, se,
           {"traceback": traceback},
           "REFUTED-IF-TRACEBACK" if traceback else
           ("DECLARED-USAGE" if rc == 2 else "exit=%d" % rc))

# J — sabotage: is the neighbour arm load-bearing?  Delete the `cand_res in
# neighbours` term from a copy; arm B (measured file's sidecar-shaped neighbour)
# must go RED while A and E stay closed.
src = TOOL.read_text()
sab = src.replace("if (cand_res in guarded_names or cand_res in neighbours\n",
                  "if (cand_res in guarded_names\n")
assert sab != src, "sabotage anchor not found"
sab_path = ROOT / LABEL / "sabotaged-no-neighbours.py"
sab_path.write_bytes(sab.encode())
print("=" * 78)
print("SABOTAGE J  removed the `cand_res in neighbours` term")
print("  sabotaged-copy sha256=%s" % sha256(sab_path))
for arm, out, paths, fixtures in (
        ("A", "vic", "vic.sha256", {"vic.sha256": b"measured X.sha256\n"}),
        ("B", "vic.sha256", "vic", {"vic": b"measured X\n",
                                    "vic.sha256": b"existing neighbour\n"})):
    d = box("J-%s" % arm)
    for rel, blob in fixtures.items():
        (d / rel).write_bytes(blob)
    key = paths if arm == "A" else "vic"
    before = sha256(d / key)
    rc, so, se = run(["capture", "--out", out, "--paths", paths], d, tool=sab_path)
    after = sha256(d / key)
    print("  arm %s: exit=%d measured-before=%s measured-after=%s %s"
          % (arm, rc, before[:16], after[:16],
             "CLOBBERED(red, as expected)" if before != after else
             ("closed" if rc == 2 else "exit=%d" % rc)))
    if arm == "B":
        for line in (se.strip() or so.strip()).splitlines()[:2]:
            print("    | %s" % line)
print("  VERDICT: sabotage arm B must be RED and arm A must stay closed for the")
print("           neighbour term to be load-bearing (non-vacuity of the after-state).")
