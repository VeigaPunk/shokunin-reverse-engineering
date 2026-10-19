#!/usr/bin/env python3
"""RV-6 attack battery: declared-class reachability + regression arms.

Usage: battery.py <tool.py> <scratch-base> <outdir>
Every arm is fixture-level or scratch-copy-level; no custody path is written.
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
rows = []


def run(args, cwd=None, env_extra=None):
    env = dict(os.environ)
    env["CUSTODY_PAIR_SCRATCH"] = str(BASE)
    if env_extra:
        env.update(env_extra)
    return subprocess.run([PY, str(TOOL)] + args, capture_output=True, text=True,
                          env=env, cwd=str(cwd) if cwd else None)


def arm(name, cls, p, extra=""):
    got = p.returncode
    ok = (got == cls)
    rows.append({"arm": name, "want_exit": cls, "got_exit": got, "hold": ok,
                 "detail": extra})
    print("\n### %-46s want=%s got=%s %s" % (name, cls, got, "HOLD" if ok else "FAIL"))
    if extra:
        print(extra)


root = Path(tempfile.mkdtemp(prefix="rv6-battery-", dir=str(BASE)))
sha = subprocess.run(["sha256sum", str(TOOL)], capture_output=True, text=True).stdout.split()[0]
print("tool  : %s\nsha256: %s\nroot  : %s" % (TOOL, sha, root))

def fixture(name, data=b"fixture\n", mode=None, mtime=(1000000000, 1000000000)):
    f = root / name
    f.write_bytes(data)
    os.utime(f, mtime)
    if mode is not None:
        os.chmod(f, mode)
    return f

# ---------------------------------------------------------------- class 0
f0 = fixture("c0.conf")
rec0 = root / "c0-pre.txt"
arm("class-0-MATCH", 0, run(["capture", "--paths", str(f0), "--out", str(rec0)]),
    "capture + verify clean")
arm("class-0-verify-MATCH", 0, run(["verify", str(rec0), "--live"]))

# ---------------------------------------------------------------- class 10
f10 = fixture("c10.conf")
rec10 = root / "c10-pre.txt"
run(["capture", "--paths", str(f10), "--out", str(rec10)])
f10.write_bytes(b"tampered bytes\n")
arm("class-10-CONTENT-DRIFT", 10, run(["verify", str(rec10), "--live"]))

# ---------------------------------------------------------------- class 11
f11 = fixture("c11.conf")
rec11 = root / "c11-pre.txt"
run(["capture", "--paths", str(f11), "--out", str(rec11)])
f11.write_bytes(b"fixture\n")            # same content, in place
os.utime(f11, (1000000000, 1000000000))  # mtime restored
arm("class-11-REWRITE-DRIFT", 11, run(["verify", str(rec11), "--live"]))

# ---------------------------------------------------------------- class 12
f12 = fixture("c12.conf")
rec12 = root / "c12-pre.txt"
run(["capture", "--paths", str(f12), "--out", str(rec12)])
os.chmod(f12, 0o600)
arm("class-12-METADATA-DRIFT", 12, run(["verify", str(rec12), "--live"]))

# ---------------------------------------------------------------- class 13
f13 = fixture("c13.conf")
rec13 = root / "c13-pre.txt"
run(["capture", "--paths", str(f13), "--out", str(rec13)])
f13.unlink()
arm("class-13-ABSENT", 13, run(["verify", str(rec13), "--live"]))

# ---------------------------------------------------------------- class 14
f14 = fixture("c14.conf", b"unreadable\n", mode=0)
rec14 = root / "c14-pre.txt"
p14 = run(["capture", "--paths", str(f14), "--out", str(rec14)])
os.chmod(f14, 0o644)
arm("class-14-capture-UNEVALUABLE", 14, p14,
    "READ-ERROR in receipt: %s" % ("READ-ERROR:" in rec14.read_text() if rec14.exists() else "(no receipt)"))
os.chmod(f14, 0)
arm("class-14-verify-UNEVALUABLE", 14, run(["verify", str(rec14), "--live"]))
os.chmod(f14, 0o644)

# ---------------------------------------------------------------- class 2 (USAGE)
arm("class-2-USAGE-unparsable", 2, run(["verify", str(f0), "--live"]),
    "a non-receipt file as the reference")
arm("class-2-USAGE-missing-receipt", 2, run(["verify", str(root / "nope.txt"), "--live"]))
arm("class-2-USAGE-missing-scratch", 2, run(["selftest", "--scratch", str(root / "no-such-dir")]))
arm("class-2-USAGE-tmp-scratch", 2, run(["selftest", "--scratch", "/tmp/rv6-must-not-run"]))
arm("class-2-USAGE-custody-overwrite", 2,
    run(["capture", "--out", str(Path("~/.bashrc").expanduser()), "--paths", "~/.bashrc"]),
    "refuse to write a receipt over a custody path")

# ---------------------------------------------------------------- class 3 (SELFTEST-FAIL)
# Reachability of exit 3 shown on a scratch copy with one case sabotaged.
sab = OUT / "sabotaged-selftest-fail.py"
src = TOOL.read_text()
needle = 'run_case(cases, "content-drift-detected", case_content)'
alt = 'run_case(cases, "content-drift-detected", lambda: (_ for _ in ()).throw(AssertionError("rv6 sabotage")))'
if needle in src:
    sab.write_text(src.replace(needle, alt), encoding="utf-8")
    p3 = subprocess.run([PY, str(sab), "selftest", "--scratch", str(BASE)],
                        capture_output=True, text=True, env={**os.environ, "CUSTODY_PAIR_SCRATCH": str(BASE)})
    arm("class-3-SELFTEST-FAIL (sabotaged scratch copy)", 3, p3,
        [l for l in p3.stdout.splitlines() if l.startswith("CUSTODY_PAIR_SELFTEST")])
else:
    print("\n### class-3 arm: needle not found in this revision (case text changed)")

# ---------------------------------------------------------------- closure (a)
a = root / "a"; a.mkdir()
vic = a / "vic.sha256"; vic.write_text("victim-bytes\n", encoding="utf-8")
v_sha0 = subprocess.run(["sha256sum", str(vic)], capture_output=True, text=True).stdout.split()[0]
pa = run(["capture", "--paths", str(vic), "--out", str(a / "vic")])
v_sha1 = subprocess.run(["sha256sum", str(vic)], capture_output=True, text=True).stdout.split()[0]
arm("closure-a-sidecar-scope-refused", 2, pa,
    "victim sha %s -> %s (unchanged=%s)\nstderr: %s" % (v_sha0[:16], v_sha1[:16], v_sha0 == v_sha1,
                                                        pa.stderr.strip()))
# a2: the sidecar of a fresh --out must not be able to land on a scoped path either
a2 = root / "a2"; a2.mkdir()
vic2 = a2 / "vic2.sha256"; vic2.write_text("victim2\n", encoding="utf-8")
v2_sha0 = subprocess.run(["sha256sum", str(vic2)], capture_output=True, text=True).stdout.split()[0]
pa2 = run(["capture", "--paths", str(vic2), "--out", str(a2 / "vic2")])
v2_sha1 = subprocess.run(["sha256sum", str(vic2)], capture_output=True, text=True).stdout.split()[0]
arm("closure-a2-sidecar-target-is-scoped-path", 2, pa2,
    "victim2 unchanged=%s  stderr: %s" % (v2_sha0 == v2_sha1, pa2.stderr.strip()))
# a3: the ordinary case must still work (fresh out, sidecar written)
a3 = root / "a3"; a3.mkdir()
ok_file = fixture("a3/ordinary.conf")
pa3 = run(["capture", "--paths", str(ok_file), "--out", str(a3 / "rec.txt")])
side3 = (a3 / "rec.txt.sha256").exists()
arm("closure-a3-ordinary-sidecar-still-written", 0, pa3,
    "sidecar exists=%s" % side3)

# ---------------------------------------------------------------- closure (b)
b = root / "b"; b.mkdir()
pfile = b / "pfile.txt"; pfile.write_text("regular file\n", encoding="utf-8")
pb = run(["capture", "--out", str(pfile / "sub" / "r.txt"), "--paths", str(pfile)])
arm("closure-b-mkdir-not-a-directory", 2, pb,
    "traceback=%s\nstderr: %s" % ("Traceback" in pb.stderr, pb.stderr.strip()[:400]))
# b2: --out '' (the CR-4 T17 self-refutation vector)
pb2 = run(["capture", "--out", "", "--paths", str(pfile)])
arm("closure-b2-empty-out", 2, pb2, "traceback=%s stderr: %s" % ("Traceback" in pb2.stderr,
                                                                  pb2.stderr.strip()[:300]))
# b3: read-only parent dir -> USAGE, not traceback
b3 = root / "b3"; b3.mkdir(); os.chmod(b3, 0o500)
pb3 = run(["capture", "--out", str(b3 / "sub" / "r.txt"), "--paths", str(pfile)])
os.chmod(b3, 0o755)
arm("closure-b3-readonly-parent", 2, pb3,
    "traceback=%s stderr: %s" % ("Traceback" in pb3.stderr, pb3.stderr.strip()[:300]))
# b4: a legal nested --out must still be created and written
b4 = run(["capture", "--out", str(root / "b4" / "deep" / "rec.txt"), "--paths", str(pfile)])
arm("closure-b4-legal-nested-out-still-works", 0, b4,
    "receipt exists=%s" % (root / "b4" / "deep" / "rec.txt").exists())

# ---------------------------------------------------------------- closure (c)
c = root / "c"; c.mkdir()
one = c / "one.conf"; one.write_bytes(b"coverage fixture\n"); os.utime(one, (1000000000, 1000000000))
dupe = c / "dupe5.txt"
pc = run(["capture", "--paths"] + [str(one)] * 5 + ["--out", str(dupe)])
stanzas = sum(1 for l in dupe.read_text().splitlines() if l.startswith("PATH:")) if dupe.exists() else -1
pcg = run(["verify", str(dupe), "--live", "--require-paths", "5"])
cov = [l for l in pcg.stdout.splitlines() if "REFERENCE-COVERAGE" in l]
arm("closure-c1-dupe-stanzas-gated", 2, pcg,
    "stanzas in reference=%d\ncoverage line: %s\nstderr: %s" % (stanzas, cov or "(none)", pcg.stderr.strip()))
# c2: 5 distinct non-canonical paths (count-gate semantics: still passes; declared?)
others = []
for i in range(4):
    others.append(fixture("c/other%d.conf" % i, b"other %d\n" % i))
five = c / "five.txt"
run(["capture", "--paths", str(one)] + [str(x) for x in others] + ["--out", str(five)])
pcg2 = run(["verify", str(five), "--live", "--require-paths", "5"])
cov2 = [l for l in pcg2.stdout.splitlines() if "REFERENCE-COVERAGE" in l]
rows.append({"arm": "closure-c2-five-distinct-noncanonical", "want_exit": "n/a",
             "got_exit": pcg2.returncode, "hold": None,
             "detail": "exit=%d coverage=%s" % (pcg2.returncode, cov2 or "(none)")})
print("\n### %-46s exit=%s  %s" % ("closure-c2-five-distinct-noncanonical", pcg2.returncode,
                                    cov2 or "(no coverage line)"))
# c3: the real 5 custody paths must still pass the gate (no false positive)
five_cust = c / "custody-five.txt"
p_cust = run(["capture", "--out", str(five_cust), "--label", "rv6-custody-five"])
pcg3 = run(["verify", str(five_cust), "--live", "--require-paths", "5"])
arm("closure-c3-canonical-five-passes-gate", 0, pcg3,
    "capture exit=%d\ncoverage line: %s" % (p_cust.returncode,
                                            [l for l in pcg3.stdout.splitlines() if "REFERENCE-COVERAGE" in l]))
# c4: a 1-of-5 reference must still gate (regression of the r3 D3 close)
one5 = c / "one-of-five.txt"
run(["capture", "--paths", str(one), "--out", str(one5)])
pcg4 = run(["verify", str(one5), "--live", "--require-paths", "5"])
arm("closure-c4-one-of-five-still-gates", 2, pcg4,
    "coverage line: %s" % [l for l in pcg4.stdout.splitlines() if "REFERENCE-COVERAGE" in l])
# c5: without the flag, the declared default must be unchanged (no gate)
pcg5 = run(["verify", str(one5), "--live"])
arm("closure-c5-no-flag-default-unchanged", 0, pcg5)

# ---------------------------------------------------------------- regressions
# the round-2/3 guard arms must still refuse
g = root / "g"; g.mkdir()
gs = g / "scoped.conf"; gs.write_bytes(b"scoped\n")
pg = run(["capture", "--out", str(gs), "--paths", str(gs)])
arm("regress-guard-scoped-path-refused", 2, pg,
    "scoped bytes intact=%s" % (gs.read_bytes() == b"scoped\n"))
gl = g / "alias.conf"; os.link(gs, gl)
pgl = run(["capture", "--out", str(gl), "--paths", str(gs)])
arm("regress-guard-hardlink-refused", 2, pgl,
    "scoped bytes intact=%s" % (gs.read_bytes() == b"scoped\n"))
arm("regress-guard-canonical-refused", 2,
    run(["capture", "--out", str(Path("~/.profile").expanduser()), "--paths", "~/.bashrc"]))

# ---------------------------------------------------------------- live pair + sidecars
lp = OUT / "live-pre.txt"; lq = OUT / "live-post.txt"
p1 = run(["capture", "--out", str(lp), "--label", "rv6-live-pre"])
p2 = run(["capture", "--out", str(lq), "--label", "rv6-live-post"])
pv = run(["verify", str(lp), str(lq), "--require-paths", "5"])
arm("live-pair-MATCH-5of5", 0, pv,
    "capture exits %d/%d\n%s" % (p1.returncode, p2.returncode,
                                  [l for l in pv.stdout.splitlines() if l.startswith("CUSTODY_PAIR_VERIFY")]))
sc = subprocess.run(["sha256sum", "-c", str(lp) + ".sha256"], capture_output=True, text=True,
                    cwd=str(lp.parent))
sc2 = subprocess.run(["sha256sum", "-c", str(lq) + ".sha256"], capture_output=True, text=True,
                     cwd=str(lq.parent))
rows.append({"arm": "live-pair-sidecars", "want_exit": 0, "got_exit": sc.returncode + sc2.returncode,
             "hold": sc.returncode == 0 and sc2.returncode == 0,
             "detail": "pre: %s post: %s" % (sc.stdout.strip(), sc2.stdout.strip())})
print("\n### live-pair-sidecars  pre=%r post=%r" % (sc.stdout.strip(), sc2.stdout.strip()))
# self-pin
pin = [l for l in lp.read_text().splitlines() if l.startswith("# tool:")]
rows.append({"arm": "receipt-self-pin", "want_exit": sha, "got_exit": pin[0] if pin else "",
             "hold": bool(pin) and sha in pin[0], "detail": pin[0] if pin else "(none)"})
print("\n### receipt-self-pin  %s" % (pin[0] if pin else "(none)"))
print("    tool sha256       %s" % sha)

# ---------------------------------------------------------------- selftest
ps = run(["selftest"])
last = [l for l in ps.stdout.splitlines() if l.startswith("CUSTODY_PAIR_SELFTEST")]
fails = [l for l in ps.stdout.splitlines() if " FAIL" in l]
cases = [l.split()[1] for l in ps.stdout.splitlines() if l.startswith("case ")]
rows.append({"arm": "selftest", "want_exit": 0, "got_exit": ps.returncode, "hold": ps.returncode == 0,
             "detail": (last[0] if last else "(none)")})
print("\n### selftest  %s" % (last[0] if last else "(none)"))
print("    failing: %s" % (fails or "(none)"))
print("    cases (%d): %s" % (len(cases), ", ".join(cases)))

(OUT / "battery.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
holds = sum(1 for r in rows if r["hold"] is True)
fails_n = sum(1 for r in rows if r["hold"] is False)
print("\n=== BATTERY: arms=%d hold=%d fail=%d (n/a=%d) ===" % (len(rows), holds, fails_n,
                                                                sum(1 for r in rows if r["hold"] is None)))
for r in rows:
    if r["hold"] is False:
        print("  FAIL %s want=%s got=%s" % (r["arm"], r["want_exit"], r["got_exit"]))
print("wrote %s" % (OUT / "battery.json"))
