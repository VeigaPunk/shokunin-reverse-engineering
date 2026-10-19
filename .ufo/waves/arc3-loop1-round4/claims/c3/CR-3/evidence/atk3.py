#!/usr/bin/env python3
"""CR-3 battery E — attacks on the ROUND-4 landed guard (revision 29bb45ae…).

E1-E4: the neighbour set (`<measured> + ".sha256"`) is checked by resolved path
       only, never by inode — a hardlink alias of the neighbour should slip past.
E5-E7: sidecar-shaped neighbour via the derived-sidecar candidate.
E8-E10: FIFO / ELOOP / non-regular --out classes.

usage: atk3.py <tool.py>
"""
import hashlib, os, shutil, subprocess, sys
from pathlib import Path

TOOL = Path(sys.argv[1]).resolve()
ROOT = Path("/dev/shm/cr3-r4/atk-E")


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
print("tool: %s sha256=%s" % (TOOL, sha(TOOL)))
print("sandbox HOME: %s" % h)


def run(args, cwd=None, timeout=12):
    env = dict(os.environ); env["HOME"] = str(h); env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        p = subprocess.run([sys.executable, str(TOOL)] + [str(a) for a in args],
                           capture_output=True, text=True, env=env, cwd=str(cwd) if cwd else None,
                           timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return "HANG", "", ""


def case(tag, args, watch, note=""):
    before = {w: sha(w) for w in watch}
    rc, o, e = run(args)
    changed = [str(w) for w in watch if sha(w) != before[w]]
    print("\n-- %s" % tag)
    print("   exit=%s  traceback=%s  CHANGED=%s" % (rc, "Traceback" in e, changed or "none"))
    if e.strip():
        print("   stderr| %s" % e.strip().splitlines()[-1][:150])
    if note:
        print("   %s" % note)


# E1: measured path X with a REAL sidecar-shaped neighbour X.sha256;
#     --out is a hardlink alias of X.sha256 under another name.
d = ROOT / "e1"; d.mkdir()
x = d / "victim.conf"; x.write_text("victim payload\n")
xs = d / "victim.conf.sha256"; xs.write_text("ORIGINAL SIDECAR — must survive\n")
alias = d / "alias.out"
os.link(xs, alias)                     # alias.out is the SAME inode as victim.conf.sha256
case("E1 --out HARDLINK-ALIAS-OF-NEIGHBOUR  (--paths X, out ~ X.sha256 by inode)",
     ["capture", "--out", alias, "--paths", x, "--label", "E1"], [xs, x],
     "alias inode == X.sha256 inode: %s" % (os.stat(alias).st_ino == os.stat(xs).st_ino))

# E2: same, but the alias is created with a .sha256-looking name in another dir
d2 = ROOT / "e2"; d2.mkdir()
x2 = d2 / "conf"; x2.write_text("payload two\n")
xs2 = d2 / "conf.sha256"; xs2.write_text("ORIGINAL SIDECAR TWO — must survive\n")
alias2 = d2 / "other.txt"; os.link(xs2, alias2)
case("E2 --out OTHER-NAME hardlink -> measured path's .sha256 neighbour",
     ["capture", "--out", alias2, "--paths", x2, "--label", "E2"], [xs2, x2])

# E3: derived sidecar is a hardlink to the measured path's neighbour
d3 = ROOT / "e3"; d3.mkdir()
x3 = d3 / "c3.conf"; x3.write_text("payload three\n")
xs3 = d3 / "c3.conf.sha256"; xs3.write_text("ORIGINAL SIDECAR THREE — must survive\n")
o3 = d3 / "out3.txt"; o3.write_text("placeholder\n")
os.remove(d3 / "out3.txt.sha256") if (d3 / "out3.txt.sha256").exists() else None
os.link(xs3, d3 / "out3.txt.sha256")   # derived sidecar name is a hardlink to X.sha256
case("E3 derived sidecar (out.txt.sha256) is a hardlink to the measured path's neighbour",
     ["capture", "--out", o3, "--paths", x3, "--label", "E3"], [xs3, x3])

# E4: direct spelling control — should be REFUSED (exit 2)
case("E4 CONTROL --out X.sha256 directly (expect exit 2, refused)",
     ["capture", "--out", xs, "--paths", x, "--label", "E4"], [xs])

# E5: FIFO as --out (already known hang; re-confirm on this revision)
f5 = ROOT / "fifo-out"; os.mkfifo(f5)
case("E5 --out FIFO (no reader)", ["capture", "--out", f5, "--paths", x, "--label", "E5"], [],
     "HANG = open() blocks forever, no timeout inside the tool")

# E6: --out is a symlink loop
l6 = ROOT / "loop"; os.symlink(l6, l6)
case("E6 --out SYMLINK-LOOP", ["capture", "--out", l6, "--paths", x, "--label", "E6"], [])

# E7: parent is a symlink loop
d7 = ROOT / "e7"; d7.mkdir()
lp = d7 / "ploop"; os.symlink(lp, lp)
case("E7 --out parent-is-SYMLINK-LOOP/child.txt", ["capture", "--out", lp / "child.txt", "--paths", x, "--label", "E7"], [])

# E8: --out is a symlink to a measured path (control, expect refuse)
d8 = ROOT / "e8"; d8.mkdir()
x8 = d8 / "meas.conf"; x8.write_text("measurable\n")
s8 = d8 / "sym-to-meas"; os.symlink(x8, s8)
case("E8 CONTROL --out SYMLINK->measured path (expect exit 2)", ["capture", "--out", s8, "--paths", x8, "--label", "E8"], [x8])

# E9: --out inside a custody DIRECTORY via symlinked parent (unchanged scope question)
ld9 = ROOT / "ld9"; os.symlink(h / ".config/devin", ld9)
case("E9 --out symlinked-parent -> custody DIR /planted.txt", ["capture", "--out", ld9 / "planted.txt", "--paths", x, "--label", "E9"],
     [h / ".config/devin/planted.txt"], "planted exists: %s" % (h / ".config/devin/planted.txt").exists())

# E10: sidecar of the receipt lands on a custody path's NEIGHBOUR name? (custody ~/.bashrc.sha256)
d10 = ROOT / "e10"; d10.mkdir()
o10 = d10 / "o.txt"; o10.write_text("x\n")
# make the derived sidecar a hardlink to a freshly planted ~/.bashrc.sha256
hb = h / ".bashrc.sha256"; hb.write_text("CUSTODY NEIGHBOUR FILE\n")
os.remove(d10 / "o.txt.sha256") if (d10 / "o.txt.sha256").exists() else None
os.link(hb, d10 / "o.txt.sha256")
case("E10 derived sidecar hardlinked to ~/.bashrc.sha256 (a custody neighbour)",
     ["capture", "--out", o10, "--paths", x, "--label", "E10"], [hb])
