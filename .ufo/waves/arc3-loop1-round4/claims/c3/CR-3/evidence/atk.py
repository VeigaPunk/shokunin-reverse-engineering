#!/usr/bin/env python3
"""CR-3 (round 4) attack battery — sidecar guard, mkdir guard, symlinked parent,
relative trickery. Scratch only. Never writes a real custody path.

usage: atk.py <tool.py> <mode>   modes: A B C
"""
import os, shutil, stat, subprocess, sys, hashlib
from pathlib import Path

TOOL = Path(sys.argv[1]).resolve()
MODE = sys.argv[2]
ROOT = Path("/dev/shm/cr3-r4/atk-%s" % MODE)


def sha(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
    except OSError as e:
        return "ERR(%s)" % e.__class__.__name__


def fresh():
    shutil.rmtree(ROOT, ignore_errors=True)
    ROOT.mkdir(parents=True)
    h = ROOT / "home"
    h.mkdir()
    # sandbox custody tree: HOME is redirected, so CUSTODY_PATHS expand here
    (h / ".config/devin").mkdir(parents=True)
    (h / ".omp/agent").mkdir(parents=True)
    (h / ".kimi-code").mkdir(parents=True)
    (h / ".config/devin/mcp_config.json").write_text('{"sandbox":"devin"}\n')
    (h / ".omp/agent/mcp.json").write_text('{"sandbox":"omp"}\n')
    (h / ".kimi-code/config.toml").write_text('# sandbox kimi\n')
    (h / ".bashrc").write_text("# sandbox bashrc\n")
    (h / ".profile").write_text("# sandbox profile\n")
    return h


def run(args, home, cwd=None, timeout=25):
    env = dict(os.environ)
    env["HOME"] = str(home)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run([sys.executable, str(TOOL)] + [str(a) for a in args],
                       capture_output=True, text=True, env=env,
                       cwd=str(cwd) if cwd else None, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def hdr(t):
    print("\n" + "=" * 78)
    print("## " + t)
    print("=" * 78)


def report(tag, rc, out, err, extra=""):
    print("-- %s" % tag)
    print("   exit=%d" % rc)
    if out.strip():
        for l in out.strip().splitlines()[:6]:
            print("   stdout| %s" % l)
    if err.strip():
        for l in err.strip().splitlines()[:6]:
            print("   stderr| %s" % l)
    if extra:
        print("   %s" % extra)


# --------------------------------------------------------------------------- #
if MODE == "A":
    h = fresh()
    print("tool: %s sha256=%s" % (TOOL, sha(TOOL)))
    print("sandbox HOME: %s" % h)

    hdr("A1  --paths X.sha256 --out X   (sidecar lands ON a measured path)")
    x = ROOT / "victim.conf"
    x.write_text("victim payload\n")
    xs = ROOT / "victim.conf.sha256"
    xs.write_text("ORIGINAL SIDECAR CONTENT — must survive\n")
    b_xs, b_x = sha(xs), sha(x)
    rc, out, err = run(["capture", "--out", x, "--paths", xs, "--label", "A1"], h)
    report("A1", rc, out, err,
           "victim.conf.sha256 before=%s after=%s  CLOBBERED=%s" % (b_xs, sha(xs), sha(xs) != b_xs))
    print("   measured path bytes: %r" % (xs.read_text()[:60] if xs.exists() else "<gone>"))
    print("   receipt at victim.conf: %s (sha before=%s after=%s)" % (sha(x) != b_x, b_x, sha(x)))

    hdr("A2  --out X.sha256 --paths X   (frozen-claim phrasing: sidecar at measured file's neighbour)")
    y = ROOT / "neigh.conf"
    y.write_text("neighbour payload\n")
    ys = ROOT / "neigh.conf.sha256"
    ys.write_text("ORIGINAL NEIGHBOUR — must survive\n")
    b_ys = sha(ys)
    rc, out, err = run(["capture", "--out", ys, "--paths", y, "--label", "A2"], h)
    report("A2", rc, out, err,
           "neigh.conf.sha256 before=%s after=%s CLOBBERED=%s" % (b_ys, sha(ys), sha(ys) != b_ys))

    hdr("A3  sidecar is a SYMLINK to a custody path (sandbox ~/.bashrc)")
    d = ROOT / "d"; d.mkdir()
    safe = d / "safe.txt"; safe.write_text("safe target\n")
    link = d / "link.txt"
    os.symlink(safe, link)                      # out resolves to a NON-guarded file -> allowed
    os.symlink(h / ".bashrc", d / "link.txt.sha256")   # derived sidecar -> custody path
    b_bash = sha(h / ".bashrc")
    rc, out, err = run(["capture", "--out", link, "--paths", ROOT / "victim.conf", "--label", "A3"], h)
    report("A3", rc, out, err,
           "sandbox ~/.bashrc before=%s after=%s CLOBBERED=%s" % (b_bash, sha(h / ".bashrc"),
                                                                  sha(h / ".bashrc") != b_bash))
    if b_bash != sha(h / ".bashrc"):
        print("   ~/.bashrc head: %r" % (h / ".bashrc").read_text()[:60])

    hdr("A4  sidecar is a HARDLINK alias of a custody path (sandbox ~/.profile)")
    d2 = ROOT / "d2"; d2.mkdir()
    o2 = d2 / "out.txt"; o2.write_text("placeholder\n")
    os.link(h / ".profile", d2 / "out.txt.sha256")
    b_prof = sha(h / ".profile")
    rc, out, err = run(["capture", "--out", o2, "--paths", ROOT / "victim.conf", "--label", "A4"], h)
    report("A4", rc, out, err,
           "sandbox ~/.profile before=%s after=%s CLOBBERED=%s" % (b_prof, sha(h / ".profile"),
                                                                   sha(h / ".profile") != b_prof))
    print("   inode of out.txt.sha256 == ~/.profile inode: %s"
          % (os.stat(d2 / "out.txt.sha256").st_ino == os.stat(h / ".profile").st_ino))

    hdr("A5  relative spelling: --paths ./r.sha256 --out r  (cwd=scratch)")
    r = ROOT / "r.conf"; r.write_text("relative payload\n")
    rs = ROOT / "r.conf.sha256"; rs.write_text("ORIGINAL REL SIDECAR — must survive\n")
    b_rs = sha(rs)
    rc, out, err = run(["capture", "--out", "r.conf", "--paths", "./r.conf.sha256", "--label", "A5"], h, cwd=ROOT)
    report("A5", rc, out, err,
           "r.conf.sha256 before=%s after=%s CLOBBERED=%s" % (b_rs, sha(rs), sha(rs) != b_rs))

    hdr("A6  control: sidecar aimed at a custody path while out is also guarded (both refused?)")
    rc, out, err = run(["capture", "--out", h / ".bashrc", "--paths", ROOT / "victim.conf", "--label", "A6"], h)
    report("A6", rc, out, err, "sandbox ~/.bashrc sha=%s (expect unchanged 16-hex)" % sha(h / ".bashrc"))

elif MODE == "B":
    h = fresh()
    print("tool: %s sha256=%s" % (TOOL, sha(TOOL)))
    print("sandbox HOME: %s" % h)

    def b_case(tag, make_parent, outname):
        hdr(tag)
        parent = ROOT / ("parent-" + tag.split()[0])
        make_parent(parent)
        out = parent / outname
        rc, o, e = run(["capture", "--out", out, "--paths", ROOT / "victim.conf", "--label", tag.split()[0]], h)
        tb = "Traceback" in e
        report(tag, rc, o, e, "RAW-TRACEBACK=%s" % tb)
        if e.strip():
            print("   last stderr line: %r" % e.strip().splitlines()[-1])

    def mk_file(p): p.write_text("i am a regular file\n")
    def mk_dangling(p): os.symlink(ROOT / "no-such-target", p)
    def mk_fifo(p): os.mkfifo(p)
    def mk_noperm(p):
        p.mkdir(); os.chmod(p, 0o500)
    def mk_symlink_to_file(p):
        t = ROOT / "symfile-target"; t.write_text("target\n"); os.symlink(t, p)

    b_case("B1 parent is a regular file  --out FILE/child.txt", mk_file, "child.txt")
    b_case("B2 parent is a dangling symlink --out LINK/child.txt", mk_dangling, "child.txt")
    b_case("B3 parent is a FIFO --out FIFO/child.txt", mk_fifo, "child.txt")
    b_case("B4 parent mode 0500 (unwritable) --out DIR/child.txt", mk_noperm, "child.txt")
    b_case("B5 parent is a symlink to a file --out LINK/child.txt", mk_symlink_to_file, "child.txt")
    b_case("B6 grandparent is a file --out FILE/sub/child.txt", mk_file, "sub/child.txt")

    hdr("B7 control: writable parent -> clean receipt (no traceback)")
    p = ROOT / "ok-parent"; p.mkdir()
    rc, o, e = run(["capture", "--out", p / "child.txt", "--paths", ROOT / "victim.conf", "--label", "B7"], h)
    report("B7", rc, o, e, "RAW-TRACEBACK=%s" % ("Traceback" in e))

    hdr("B8 FIFO as --out itself (not a parent)")
    f = ROOT / "outfifo"; os.mkfifo(f)
    try:
        rc, o, e = run(["capture", "--out", f, "--paths", ROOT / "victim.conf", "--label", "B8"], h, timeout=6)
        report("B8", rc, o, e, "RAW-TRACEBACK=%s" % ("Traceback" in e))
    except subprocess.TimeoutExpired:
        print("-- B8  exit=HANG(>6s)  open(FIFO,'w') blocked with no reader — capture never returns")

elif MODE == "C":
    h = fresh()
    print("tool: %s sha256=%s" % (TOOL, sha(TOOL)))
    print("sandbox HOME: %s" % h)
    v = ROOT / "victim.conf"; v.write_text("victim payload\n")

    hdr("C1 symlinked parent -> custody DIRECTORY: --out LINK/x.txt (LINK -> ~/.config/devin)")
    linkdir = ROOT / "linkdir"
    os.symlink(h / ".config/devin", linkdir)
    rc, o, e = run(["capture", "--out", linkdir / "planted.txt", "--paths", v, "--label", "C1"], h)
    planted = h / ".config/devin/planted.txt"
    report("C1", rc, o, e, "file created INSIDE custody dir: %s exists=%s" % (planted, planted.exists()))

    hdr("C2 symlinked parent -> custody dir, leaf = a custody file name (guard must hold)")
    b = sha(h / ".bashrc")
    rc, o, e = run(["capture", "--out", linkdir / ".." / ".bashrc", "--paths", v, "--label", "C2"], h)
    report("C2", rc, o, e, "~/.bashrc before=%s after=%s changed=%s" % (b, sha(h / ".bashrc"), b != sha(h / ".bashrc")))

    hdr("C3 relative escape via .. : cwd=sub, --out ../home/.bashrc")
    sub = ROOT / "sub"; sub.mkdir()
    b = sha(h / ".bashrc")
    rc, o, e = run(["capture", "--out", "../home/.bashrc", "--paths", v, "--label", "C3"], h, cwd=sub)
    report("C3", rc, o, e, "~/.bashrc changed=%s" % (b != sha(h / ".bashrc")))

    hdr("C4 hardlink alias of a custody path as --out")
    b = sha(h / ".bashrc")
    alias = ROOT / "hl-alias"; os.link(h / ".bashrc", alias)
    rc, o, e = run(["capture", "--out", alias, "--paths", v, "--label", "C4"], h)
    report("C4", rc, o, e, "~/.bashrc changed=%s" % (b != sha(h / ".bashrc")))

    hdr("C5 symlink to a custody path as --out (absolute target)")
    b = sha(h / ".bashrc")
    s1 = ROOT / "sym-abs"; os.symlink(h / ".bashrc", s1)
    rc, o, e = run(["capture", "--out", s1, "--paths", v, "--label", "C5"], h)
    report("C5", rc, o, e, "~/.bashrc changed=%s" % (b != sha(h / ".bashrc")))

    hdr("C6 symlink to a custody path as --out (RELATIVE target)")
    b = sha(h / ".bashrc")
    s2 = ROOT / "sym-rel"; os.symlink("../home/.bashrc", s2)
    rc, o, e = run(["capture", "--out", s2, "--paths", v, "--label", "C6"], h)
    report("C6", rc, o, e, "~/.bashrc changed=%s" % (b != sha(h / ".bashrc")))

    hdr("C7 symlinked GRANDparent -> home, --out LINK/.kimi-code/config.toml")
    gp = ROOT / "gp"; os.symlink(h, gp)
    b = sha(h / ".kimi-code/config.toml")
    rc, o, e = run(["capture", "--out", gp / ".kimi-code" / "config.toml", "--paths", v, "--label", "C7"], h)
    report("C7", rc, o, e, "config.toml changed=%s" % (b != sha(h / ".kimi-code/config.toml")))

    hdr("C8 --out '.' (a directory) and --out '' ")
    for arg in (".", ""):
        rc, o, e = run(["capture", "--out", arg, "--paths", v, "--label", "C8"], h, cwd=ROOT)
        report("C8 --out %r" % arg, rc, o, e, "RAW-TRACEBACK=%s" % ("Traceback" in e))

    hdr("C9 unguarded out whose sidecar is a custody path via symlinked parent")
    d = ROOT / "d9"; d.mkdir()
    o9 = d / "o.txt"; o9.write_text("x\n")
    os.symlink(h / ".profile", d / "o.txt.sha256")
    b = sha(h / ".profile")
    rc, o, e = run(["capture", "--out", o9, "--paths", v, "--label", "C9"], h)
    report("C9", rc, o, e, "~/.profile changed=%s" % (b != sha(h / ".profile")))
else:
    raise SystemExit("unknown mode %r" % MODE)
