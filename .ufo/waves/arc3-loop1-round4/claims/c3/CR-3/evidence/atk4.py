#!/usr/bin/env python3
"""CR-3 battery F — spelling-dependence of the NEW neighbour guard.

The guard derives the neighbour as `Path(str(g) + ".sha256")`. For a measured
path spelled `X/.` that yields the bogus name `X/..sha256`, NOT `X.sha256` —
so the real neighbour may be unprotected. Scratch only.

usage: atk4.py <tool.py>
"""
import hashlib, os, shutil, subprocess, sys
from pathlib import Path

TOOL = Path(sys.argv[1]).resolve()
ROOT = Path("/dev/shm/cr3-r4/atk-F")


def sha(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
    except OSError as e:
        return "ERR(%s)" % e.__class__.__name__


shutil.rmtree(ROOT, ignore_errors=True)
ROOT.mkdir(parents=True)
h = ROOT / "home"; h.mkdir()
print("tool: %s sha256=%s" % (TOOL, sha(TOOL)))


def run(args, cwd=None, timeout=12):
    env = dict(os.environ); env["HOME"] = str(h); env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        p = subprocess.run([sys.executable, str(TOOL)] + [str(a) for a in args],
                           capture_output=True, text=True, env=env, cwd=str(cwd) if cwd else None,
                           timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return "HANG", "", ""


def case(tag, paths_spelling, out_name, cwd=None):
    d = ROOT / tag.split()[0]
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    x = d / "X"; x.write_text("measured payload\n")
    xs = d / "X.sha256"; xs.write_text("ORIGINAL NEIGHBOUR — must survive\n")
    b = sha(xs)
    rc, o, e = run(["capture", "--out", out_name, "--paths", paths_spelling, "--label", tag.split()[0]],
                   cwd=cwd or d)
    clob = sha(xs) != b
    print("\n-- %s" % tag)
    print("   --paths %r  --out %r  (cwd=%s)" % (paths_spelling, out_name, cwd or d))
    print("   exit=%s  NEIGHBOUR-CLOBBERED=%s" % (rc, clob))
    if e.strip():
        print("   stderr| %s" % e.strip().splitlines()[-1][:140])
    if clob:
        print("   X.sha256 now: %r" % xs.read_text()[:70])


case("F1 measured path spelled X/.", "X/.", "X.sha256")
case("F2 measured path spelled X/ (trailing slash)", "X/", "X.sha256")
case("F3 measured path spelled ./X", "./X", "X.sha256")
case("F4 measured path spelled X/../X", "X/../X", "X.sha256")
case("F5 CONTROL measured path spelled X (expect refusal)", "X", "X.sha256")
case("F6 measured path spelled X/. and --out X.sha256.sha256", "X/.", "X.sha256.sha256")
case("F7 measured path spelled . (cwd=d, X measured via absolute)", ".", "X.sha256")
