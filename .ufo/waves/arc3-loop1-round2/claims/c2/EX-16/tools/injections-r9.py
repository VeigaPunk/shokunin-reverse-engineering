#!/usr/bin/env python3
"""EX-16 r9 injection battery — census H1/H3 fail-closure falsifiability harness.

Usage: python3 injections-r9.py <instrument.py> <label> <outdir>

Cases (roots are fresh copies of /dev/shm/ex16/root-before):
  standard : t0-baseline t1-false-current-pin t2-undeclared-append
             t3-marker-strip t4-anchor-fail t5-dated-shelter t6-ptr-out-of-range
  H1 class : h1-{skill,province,scorecard}-absent, h1-skill-zero-byte,
             h1-skill-truncated, h1-skill-isdir, h1-skill-eacces
  H3 class : h3-blind-all, h3-blind-pin, h3-blind-gate (instrument copies)
  H4 demo  : w1-scope-widen-tail (instrument copy with widened DATED end)
  quiet    : q0-quiet-baseline
Every case writes <outdir>/<name>.out (stdout+stderr+EXIT) and a line of
<outdir>/SUMMARY.txt.  Instrument-copy cases also leave <outdir>/instr-<case>.py.
"""
import os, re, shutil, subprocess, sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "/dev/shm/ex16"
ROOT_BEFORE = os.path.join(BASE, "root-before")
FILES = ("PROVINCE.md", "SKILL.md", "SCORECARD.md")
NEVER = 're.compile(r"(?!x)x")'


def build_root():
    os.makedirs(ROOT_BEFORE, exist_ok=True)
    for f in FILES:
        shutil.copy2(os.path.join(REPO, f), os.path.join(ROOT_BEFORE, f))


def edit(path, old, new):
    txt = open(path, encoding="utf-8").read()
    assert old in txt, "needle not found in %s: %r" % (path, old[:60])
    open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))


def mutate_instrument(instrument, outdir, case, subs):
    dst = os.path.join(outdir, "instr-%s.py" % case)
    txt = open(instrument, encoding="utf-8").read()
    for old, new in subs:
        assert old in txt, "instrument needle not found for %s: %r" % (case, old[:60])
        txt = txt.replace(old, new, 1)
    open(dst, "w", encoding="utf-8").write(txt)
    return dst


# ---- case mutators, one per attack -----------------------------------------
def t1(case):   # false current pin in SKILL.md CURRENT range
    edit(os.path.join(case, "SKILL.md"), "rea-agents@6.5.0", "rea-agents@6.3.0")


def t2(case):   # undeclared stale locus appended past the last declared line
    with open(os.path.join(case, "SCORECARD.md"), "a") as fh:
        fh.write("\nThe kimi client remains pinned to rea-agents@6.3.0 for the current round.\n")


def t3(case):   # strip a DATED marker (PROVINCE.md:40)
    edit(os.path.join(case, "PROVINCE.md"), "verified on this host 2026-10-13",
         "verified on this host [marker removed]")


def t5(case):   # false current-claim planted inside a DATED range (shelter demo)
    lines = open(os.path.join(case, "SCORECARD.md"), encoding="utf-8").read().splitlines()
    lines.insert(800, "Current status: kimi runs rea-agents@6.3.0 as of this round.")
    open(os.path.join(case, "SCORECARD.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


def t6(case):   # pointer needle outside declared range
    with open(os.path.join(case, "SCORECARD.md"), "a") as fh:
        fh.write("\nSee ~/.kimi-code/config.toml:9999 for the pointer class check.\n")


def h1_absent(f):
    def m(case):
        os.remove(os.path.join(case, f))
    return m


def h1_zero(case):
    open(os.path.join(case, "SKILL.md"), "w").close()


def h1_trunc(case):  # keep only the first 12 lines (rows 18-20 now lie past EOF)
    p = os.path.join(case, "SKILL.md")
    lines = open(p, encoding="utf-8").read().splitlines()
    open(p, "w", encoding="utf-8").write("\n".join(lines[:12]) + "\n")


def h1_isdir(case):
    p = os.path.join(case, "SKILL.md")
    os.remove(p)
    os.mkdir(p)


def h1_eacces(case):
    os.chmod(os.path.join(case, "SKILL.md"), 0)


def h3_nullskill(case):  # EX-14's nullskill: needles stripped from SKILL.md:10-20
    p = os.path.join(case, "SKILL.md")
    lines = open(p, encoding="utf-8").read().splitlines()
    for i in range(9, min(20, len(lines))):
        lines[i] = re.sub(r"rea-agents@\d+\.\d+\.\d+", "rea-agents@X", lines[i])
        lines[i] = re.sub(r"(?<![\d.])6\.\d+\.\d+", "Y", lines[i])
    open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def h5_skill_padded(case):  # EX-12 F5: content erased, length preserved
    p = os.path.join(case, "SKILL.md")
    n = len(open(p, encoding="utf-8").read().splitlines())
    open(p, "w", encoding="utf-8").write("\n" * n)


CASES = [
    ("t0-baseline", None, {}),
    ("t1-false-current-pin", t1, {}),
    ("t2-undeclared-append", t2, {}),
    ("t3-marker-strip", t3, {}),
    ("t4-anchor-fail", None, {"env_home": os.path.join(BASE, "fakehome")}),
    ("t5-dated-shelter", t5, {}),
    ("t6-ptr-out-of-range", t6, {}),
    ("h1-skill-absent", h1_absent("SKILL.md"), {}),
    ("h1-province-absent", h1_absent("PROVINCE.md"), {}),
    ("h1-scorecard-absent", h1_absent("SCORECARD.md"), {}),
    ("h1-skill-zero-byte", h1_zero, {}),
    ("h1-skill-truncated", h1_trunc, {}),
    ("h1-skill-isdir", h1_isdir, {}),
    ("h1-skill-eacces", h1_eacces, {}),
    ("h3-nullskill", h3_nullskill, {}),
    ("h5-skill-padded", h5_skill_padded, {}),
    ("q0-quiet-baseline", None, {"quiet": True}),
]

BLIND_SUBS = {
    "h3-blind-all": [('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)', "PIN = " + NEVER),
                     ('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")', "VER = " + NEVER),
                     ('PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")', "PTR = " + NEVER)],
    "h3-blind-pin": [('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)', "PIN = " + NEVER)],
    "h3-blind-gate": [('REA_GATE = re.compile(r"rea-agents|\\brea\\b|config\\.toml|mcp_config\\.json|mcp\\.json|mcp_servers|devin|\\bomp\\b|kimi|npx", re.I)',
                       "REA_GATE = " + NEVER)],
    "w1-scope-widen-tail": [('("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3")',
                             '("SCORECARD.md", 769, 1419, "DATED", 769, r"arc2-loop1-round3")')],
    "w2-scope-widen-overshoot": [('("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3")',
                                  '("SCORECARD.md", 769, 1450, "DATED", 769, r"arc2-loop1-round3")')],
}


def run_case(instrument, case_root, name, outdir, env_home=None, quiet=False, root_override=None):
    env = dict(os.environ)
    if env_home:
        env["HOME"] = env_home
    cmd = [sys.executable, instrument, "--root", root_override or case_root]
    if quiet:
        cmd.append("--quiet")
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    out = p.stdout + p.stderr
    with open(os.path.join(outdir, name + ".out"), "w") as fh:
        fh.write(out + "\nEXIT=%d\n" % p.returncode)
    tail = [l for l in out.splitlines()
            if l.startswith(("VERDICT", "SCOPE-ERRORS", "ANCHOR-FAIL", "UNREADABLE",
                             "DECLARED", "G2"))]
    return p.returncode, tail


def main():
    instrument, label, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    build_root()
    sha = subprocess.run(["sha256sum", instrument], capture_output=True, text=True).stdout.split()[0]
    lines = []
    lines.append("== instrument %s  sha256 %s  label %s" % (instrument, sha, label))
    print(lines[-1])
    for name, mut, kw in CASES:
        case = os.path.join(BASE, "cases-%s" % label, name)
        if os.path.exists(case):
            shutil.rmtree(case)
        shutil.copytree(ROOT_BEFORE, case)
        if mut:
            mut(case)
        rc, tail = run_case(instrument, case, name, outdir, **kw)
        row = "[%s] %-24s exit=%d  %s" % (label, name, rc, " | ".join(tail))
        lines.append(row)
        print(row)
    for name, subs in BLIND_SUBS.items():
        inst = mutate_instrument(instrument, outdir, name, subs)
        case = os.path.join(BASE, "cases-%s" % label, name)
        if os.path.exists(case):
            shutil.rmtree(case)
        shutil.copytree(ROOT_BEFORE, case)
        if name.startswith("w"):
            t2(case)  # laundered tail pin: a widened DATED row swallows it
        rc, tail = run_case(inst, case, name, outdir)
        row = "[%s] %-24s exit=%d  %s" % (label, name, rc, " | ".join(tail))
        lines.append(row)
        print(row)
    with open(os.path.join(outdir, "SUMMARY-%s.txt" % label), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
