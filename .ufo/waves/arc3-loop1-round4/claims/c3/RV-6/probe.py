#!/usr/bin/env python3
"""RV-6 probe: reproduce the three C3-r4 injections (a/b/c) + selftest count.

Usage: probe.py <tool.py> <scratch-base> <outdir>
Runs against any revision; every arm is fixture-level (no custody path touched).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
PY = sys.executable

results = []


def run(args, cwd=None):
    env = dict(os.environ)
    env["CUSTODY_PAIR_SCRATCH"] = str(BASE)
    p = subprocess.run([PY, str(TOOL)] + args, capture_output=True, text=True,
                       env=env, cwd=str(cwd) if cwd else None)
    return p


def rec(name, verdict, detail):
    results.append({"probe": name, "verdict": verdict, "detail": detail})
    print("\n### %s -> %s" % (name, verdict))
    print(detail)


root = Path(tempfile.mkdtemp(prefix="rv6-probe-", dir=str(BASE)))
print("tool  : %s" % TOOL)
print("sha256: %s" % subprocess.run(["sha256sum", str(TOOL)], capture_output=True,
                                     text=True).stdout.split()[0])
print("root  : %s" % root)

# ------------------------------------------------------------------ probe A
# (a) sidecar path not scope-checked: --paths X.sha256 --out X aims the derived
#     sidecar at the measured file's own name.
a = root / "a"
a.mkdir()
vic = a / "vic.sha256"
vic.write_text("victim-bytes\n", encoding="utf-8")
before_bytes = vic.read_bytes()
before_sha = subprocess.run(["sha256sum", str(vic)], capture_output=True, text=True).stdout.split()[0]
p = run(["capture", "--paths", str(vic), "--out", str(a / "vic"), "--label", "rv6-a"])
after_sha = subprocess.run(["sha256sum", str(vic)], capture_output=True, text=True).stdout.split()[0]
clobbered = (before_bytes != vic.read_bytes())
rec("A-sidecar-scope", "CLOBBERED" if clobbered else "REFUSED/INTACT",
    "exit=%d\nvictim sha256 before=%s after=%s\nvictim bytes changed=%s\n"
    "stdout:\n%s\nstderr:\n%s" % (p.returncode, before_sha, after_sha, clobbered,
                                   p.stdout.strip(), p.stderr.strip()))

# ------------------------------------------------------------------ probe B
# (b) out.parent.mkdir outside the guarded try: --out <regular-file>/sub/r.txt
b = root / "b"
b.mkdir()
pfile = b / "pfile.txt"
pfile.write_text("i am a regular file\n", encoding="utf-8")
p = run(["capture", "--out", str(pfile / "sub" / "r.txt"), "--paths", str(pfile), "--label", "rv6-b"])
tb = "Traceback" in p.stderr
rec("B-mkdir-traceback", "TRACEBACK exit=%d" % p.returncode if tb else "DECLARED exit=%d" % p.returncode,
    "exit=%d  traceback=%s\nstderr:\n%s\nstdout:\n%s" % (p.returncode, tb, p.stderr.strip()[:1500],
                                                          p.stdout.strip()[:600]))

# ------------------------------------------------------------------ probe C
# (c) coverage gate counts stanzas, not distinct paths.
c = root / "c"
c.mkdir()
one = c / "one.conf"
one.write_bytes(b"coverage fixture\n")
os.utime(one, (1000000000, 1000000000))

# C1: 5x duplicate stanza for ONE path (built by the tool itself)
dupe = c / "dupe5.txt"
p_cap = run(["capture", "--paths", str(one), str(one), str(one), str(one), str(one),
             "--out", str(dupe), "--label", "rv6-c-dupe5"])
stanzas = sum(1 for l in dupe.read_text().splitlines() if l.startswith("PATH:")) if dupe.exists() else -1
p_gate = run(["verify", str(dupe), "--live", "--require-paths", "5"])
cov_lines = [l for l in p_gate.stdout.splitlines() if "REFERENCE-COVERAGE" in l]
rec("C1-dupe-stanza-gate", "PASS exit=%d" % p_gate.returncode if p_gate.returncode == 0 else
    "GATED exit=%d" % p_gate.returncode,
    "capture exit=%d stanzas=%d\nverify --require-paths 5 exit=%d\n"
    "REFERENCE-COVERAGE lines: %s\nverdict line: %s\nstderr: %s"
    % (p_cap.returncode, stanzas, p_gate.returncode, cov_lines or "(none)",
       [l for l in p_gate.stdout.splitlines() if l.startswith("VERDICT")],
       p_gate.stderr.strip()))

# C2: 5 distinct NON-canonical scratch paths (also satisfies a stanza count)
others = []
for i in range(4):
    f = c / ("other%d.conf" % i)
    f.write_bytes(b"other fixture %d\n" % i)
    os.utime(f, (1000000000, 1000000000))
    others.append(f)
five = c / "five.txt"
p_cap2 = run(["capture", "--paths", str(one), *[str(x) for x in others],
              "--out", str(five), "--label", "rv6-c-five"])
p_gate2 = run(["verify", str(five), "--live", "--require-paths", "5"])
cov2 = [l for l in p_gate2.stdout.splitlines() if "REFERENCE-COVERAGE" in l]
rec("C2-noncanonical-five-gate", "PASS exit=%d" % p_gate2.returncode if p_gate2.returncode == 0 else
    "GATED exit=%d" % p_gate2.returncode,
    "verify --require-paths 5 exit=%d\nREFERENCE-COVERAGE lines: %s\nverdict: %s\nstderr: %s"
    % (p_gate2.returncode, cov2 or "(none)",
       [l for l in p_gate2.stdout.splitlines() if l.startswith("VERDICT")],
       p_gate2.stderr.strip()))

# ------------------------------------------------------------------ selftest
p_self = run(["selftest"])
last = [l for l in p_self.stdout.splitlines() if l.startswith("CUSTODY_PAIR_SELFTEST")]
fails = [l for l in p_self.stdout.splitlines() if " FAIL" in l]
rec("D-selftest", "CLEAN" if p_self.returncode == 0 else "DIRTY exit=%d" % p_self.returncode,
    "%s\nfailing cases: %s\nexit=%d" % (last or "(no summary line)", fails or "(none)", p_self.returncode))

# ------------------------------------------------------------------ live pair
# The round's live pair must verify MATCH 5/5 with the landed tool.
live_pre = OUT / "live-pre.txt"
live_post = OUT / "live-post.txt"
p1 = run(["capture", "--out", str(live_pre), "--label", "rv6-live-pre"])
p2 = run(["capture", "--out", str(live_post), "--label", "rv6-live-post"])
p_v = run(["verify", str(live_pre), str(live_post), "--require-paths", "5"])
rec("E-live-pair", "MATCH exit=%d" % p_v.returncode if p_v.returncode == 0 else "exit=%d" % p_v.returncode,
    "capture pre exit=%d post exit=%d\nverify exit=%d\nverdict: %s\n%s"
    % (p1.returncode, p2.returncode, p_v.returncode,
       [l for l in p_v.stdout.splitlines() if l.startswith("VERDICT")],
       [l for l in p_v.stdout.splitlines() if l.startswith("CUSTODY_PAIR_VERIFY")]))

(OUT / "probe.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print("\nwrote %s" % (OUT / "probe.json"))
print("scratch root: %s" % root)
