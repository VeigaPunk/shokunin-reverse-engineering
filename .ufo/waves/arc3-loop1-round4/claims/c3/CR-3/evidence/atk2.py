#!/usr/bin/env python3
"""CR-3 battery D — symlinked-parent / relative trickery aimed at real custody
paths (sandbox HOME), and guard-coverage probes. Scratch only.

usage: atk2.py <tool.py>
"""
import hashlib, os, shutil, subprocess, sys
from pathlib import Path

TOOL = Path(sys.argv[1]).resolve()
ROOT = Path("/dev/shm/cr3-r4/atk-D")


def sha(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
    except OSError as e:
        return "ERR(%s)" % e.__class__.__name__


shutil.rmtree(ROOT, ignore_errors=True)
ROOT.mkdir(parents=True)
h = ROOT / "home"
(h / ".config/devin").mkdir(parents=True)
(h / ".omp/agent").mkdir(parents=True)
(h / ".kimi-code").mkdir(parents=True)
for rel, txt in ((".config/devin/mcp_config.json", '{"devin"}\n'), (".omp/agent/mcp.json", '{"omp"}\n'),
                 (".kimi-code/config.toml", "# kimi\n"), (".bashrc", "# bashrc\n"), (".profile", "# profile\n")):
    (h / rel).write_text(txt)
v = ROOT / "victim.conf"; v.write_text("victim\n")
print("tool: %s sha256=%s" % (TOOL, sha(TOOL)))
print("sandbox HOME: %s" % h)


def run(args, cwd=None, timeout=20):
    env = dict(os.environ); env["HOME"] = str(h); env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        p = subprocess.run([sys.executable, str(TOOL)] + [str(a) for a in args],
                           capture_output=True, text=True, env=env, cwd=str(cwd) if cwd else None,
                           timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return "HANG", "", ""


def case(tag, args, targets, cwd=None, extra=""):
    before = {t: sha(t) for t in targets}
    rc, o, e = run(args, cwd)
    changed = [str(t) for t in targets if sha(t) != before[t]]
    print("\n-- %s\n   cmd: capture %s" % (tag, " ".join(str(a) for a in args)))
    print("   exit=%s  changed=%s  traceback=%s" % (rc, changed or "none", "Traceback" in e))
    if e.strip():
        print("   stderr| %s" % e.strip().splitlines()[-1][:160])
    if extra:
        print("   %s" % extra)


CUST = [h / ".config/devin/mcp_config.json", h / ".omp/agent/mcp.json",
        h / ".kimi-code/config.toml", h / ".bashrc", h / ".profile"]

# D1 symlinked dir + ".." + custody leaf
ld = ROOT / "ld"; os.symlink(h / ".kimi-code", ld)
case("D1 --out LINK/../.kimi-code/config.toml  (symlinked parent + .. to custody leaf)",
     ["capture", "--out", ld / ".." / ".kimi-code" / "config.toml", "--paths", v, "--label", "D1"],
     [h / ".kimi-code/config.toml"])

# D2 symlinked dir + ".." + custody leaf (2 levels)
ld2 = ROOT / "ld2"; os.symlink(h, ld2)
case("D2 --out LINK2/.kimi-code/config.toml  (symlinked parent straight to HOME)",
     ["capture", "--out", ld2 / ".kimi-code" / "config.toml", "--paths", v, "--label", "D2"],
     [h / ".kimi-code/config.toml"])

# D3 symlink chain: two hops to a custody path
a = ROOT / "hop-a"; b = ROOT / "hop-b"
os.symlink(b, a); os.symlink(h / ".profile", b)
case("D3 --out HOP-A (2-hop symlink chain to ~/.profile)",
     ["capture", "--out", a, "--paths", v, "--label", "D3"], [h / ".profile"])

# D4 measured path is itself a symlink to a custody path; --out = that symlink's target
sc = ROOT / "sym-measured"; os.symlink(h / ".bashrc", sc)
case("D4 --out ~/.bashrc while --paths SYMLINK->~/.bashrc (inode arm)",
     ["capture", "--out", h / ".bashrc", "--paths", sc, "--label", "D4"], [h / ".bashrc"])

# D5 out whose parent is a symlink to a custody dir; leaf is a custody FILE name
ld3 = ROOT / "ld3"; os.symlink(h / ".config" / "devin", ld3)
case("D5 --out LINK3/mcp_config.json (leaf is a custody file)",
     ["capture", "--out", ld3 / "mcp_config.json", "--paths", v, "--label", "D5"],
     [h / ".config/devin/mcp_config.json"])

# D6 ".." trickery on a path that does not exist yet, aiming at custody leaf via symlinked dir
case("D6 --out LINK2/../home/.bashrc (.. through a symlink to HOME)",
     ["capture", "--out", ld2 / ".." / "home" / ".bashrc", "--paths", v, "--label", "D6"],
     [h / ".bashrc"])

# D7 relative ".." climb from a deep cwd
deep = ROOT / "a/b/c"; deep.mkdir(parents=True)
case("D7 cwd=ROOT/a/b/c --out ../../../home/.bashrc",
     ["capture", "--out", "../../../home/.bashrc", "--paths", v, "--label", "D7"],
     [h / ".bashrc"], cwd=deep)

# D8 control: out is a fresh file inside a NON-custody dir
fresh_dir = ROOT / "fresh"; fresh_dir.mkdir()
case("D8 control --out FRESH/ok.txt", ["capture", "--out", fresh_dir / "ok.txt", "--paths", v, "--label", "D8"], [])
print("   receipt exists: %s" % (fresh_dir / "ok.txt").exists())
print("   sidecar exists: %s" % (fresh_dir / "ok.txt.sha256").exists())
