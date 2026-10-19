#!/usr/bin/env python3
"""EX-16 interplay battery (wave arc3-loop1-round4, chain c2).

Re-runnable: clones the repo into /var/tmp, mutates ONE thing per case, commits
in the clone, and grades both instruments (citation-drift probe + c1 census) on
the clone. The repo under work is only ever read. Scratch never under /tmp.

Usage: python3 interplay-battery.py [--out DIR]
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PROBE = os.path.join(REPO, ".ufo/gates/citation-drift/citation-drift-probe.py")
TABLE = os.path.join(REPO, ".ufo/gates/citation-drift/pointer-table.json")
EXPECTED = os.path.join(REPO, ".ufo/gates/citation-drift/expected.json")
CENSUS = os.path.join(REPO, ".ufo/gates/c1-census-v10.py")
EX14 = os.path.join(REPO, ".ufo/waves/arc3-loop1-round4/claims/c2/EX-14/evidence/"
                          "demo-frontier-repair.patch.md")
EX26 = os.path.join(REPO, ".ufo/waves/arc3-loop1-round4/claims/c3/EX-26/evidence/"
                          "ruling-block.txt")
RV4_APPLIER = os.path.join(REPO, ".ufo/waves/arc3-loop1-round4/claims/c2/RV-4/"
                                 "prose-apply.py")
WORK = "/var/tmp/ex16/interplay-battery"


def sh(cmd, cwd=None, check=True, **kw):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kw)
    if check and p.returncode != 0:
        raise RuntimeError("%s -> %d\n%s%s" % (cmd, p.returncode, p.stdout, p.stderr))
    return p


def clone(name):
    d = os.path.join(WORK, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(WORK, exist_ok=True)
    sh(["git", "clone", "-q", "--no-hardlinks", REPO, d])
    return d


def commit(d, msg):
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "-c", "user.email=e@x", "-c", "user.name=e",
        "commit", "-q", "--allow-empty", "-m", msg])


def probe(d):
    p = sh([sys.executable, PROBE, "--root", d, "--rev", "HEAD",
            "--table", TABLE, "--expected", EXPECTED, "--strict"], check=False)
    ids = sorted(set(re.findall(r"CITATION_DRIFT: (\S+) entry=(\S+)", p.stdout)))
    v = re.search(r"CITATION_DRIFT_VERDICT: (\S+) findings=(\d+) exit=(\d+)", p.stdout)
    return v.group(1), int(v.group(2)), int(v.group(3)), ids


def census(d):
    """The census grades a scoped root carrying the three scoped files."""
    r = os.path.join(WORK, "croot-" + os.path.basename(d))
    shutil.rmtree(r, ignore_errors=True)
    os.makedirs(r)
    for f in ("PROVINCE.md", "SKILL.md", "SCORECARD.md"):
        shutil.copy(os.path.join(d, f), r)
    p = sh([sys.executable, CENSUS, "--root", r], check=False)
    se = next((l for l in p.stdout.splitlines() if l.startswith("SCOPE-ERRORS")), "")
    v = next((l for l in p.stdout.splitlines() if l.startswith("VERDICT")), "")
    return p.returncode, v.strip(), se.strip()


def edit_province(d, fn):
    p = os.path.join(d, "PROVINCE.md")
    ls = open(p, encoding="utf-8").read().split("\n")
    open(p, "w", encoding="utf-8").write("\n".join(fn(ls)))


def ins_below_frontier(n):
    def fn(ls):
        i = next(k for k, l in enumerate(ls) if "bare hashes (no signature DB" in l)
        ls[i + 1:i + 1] = ["  filler %d" % k for k in range(n)]
        return ls
    return fn


def ins_above_line18(ls):
    ls.insert(13, "an inserted line above the drift-prone paragraph")
    return ls


def ins_above_line119(ls):
    i = next(k for k, l in enumerate(ls) if "bare hashes (no signature DB" in l)
    ls[i + 1:i + 1] = ["  filler"]
    return ls


def ins_at_eof(ls):
    ls.insert(len(ls) - 1, "a trailing appendix line below the declared max end")
    return ls


def surface_sameline(ls):
    i = next(k for k, l in enumerate(ls) if l.startswith("Surface summary:"))
    ls[i] = ("Surface summary (re-censused 2026-10-19): the `rea` MCP/CLI surfaces"
             " resolve per client: Devin and OMP")
    return ls


def surface_plus1(ls):
    i = next(k for k, l in enumerate(ls) if l.startswith("Surface summary:"))
    ls[i + 1:i + 1] = ["an inserted continuation line inside the surface-summary paragraph"]
    return ls


def frontier_sameline(ls):
    i = next(k for k, l in enumerate(ls) if "real solc/vyper-compiled bytecode untested" in l)
    ls[i] = ("  (Core, r3-07) and real solc-0.8.37 carriers (Core, arc3-r1); vyper"
             " untested;")
    return ls


def readme_mut(repl_from, repl_to):
    def fn(d):
        p = os.path.join(d, ".ufo/gates/custody-pair/README.md")
        t = open(p, encoding="utf-8").read()
        assert repl_from in t, "needle absent before mutation: %r" % repl_from
        open(p, "w", encoding="utf-8").write(t.replace(repl_from, repl_to))
    return fn


CASES = [
    ("base", None, None),
    ("prov-plus2-below-frontier", edit_province, ins_below_frontier(2)),
    ("prov-plus3-below-frontier", edit_province, ins_below_frontier(3)),
    ("prov-insert-above-line18", edit_province, ins_above_line18),
    ("prov-insert-above-line119", edit_province, ins_above_line119),
    ("prov-insert-at-eof", edit_province, ins_at_eof),
    ("prov-surface-sameline", edit_province, surface_sameline),
    ("prov-surface-plus1", edit_province, surface_plus1),
    ("prov-frontier-sameline", edit_province, frontier_sameline),
    ("readme-drop-never-tmp", readme_mut("**never `/tmp`**", "**never the quota-exhausted scratch**"), None),
    ("readme-drop-precedence", readme_mut("Severity precedence for the verdict of a `verify` run",
                                          "The worst finding decides the verdict of a `verify` run"), None),
    ("readme-drop-fieldset", readme_mut("MTIME_UTC_RENDER", "MTIME_UTC"), None),
    ("readme-drop-rewrite-id", readme_mut("Rewrite identity is `INODE` + `CTIME`",
                                          "Rewrite identity is the digest pair"), None),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO,
                    ".ufo/waves/arc3-loop1-round4/claims/c2/EX-16/evidence"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    lines = []
    lines.append("== EX-16 interplay battery ==")
    lines.append("repo: %s" % REPO)
    lines.append("HEAD: %s" % sh(["git", "-C", REPO, "rev-parse", "HEAD"]).stdout.strip())
    lines.append("scratch: %s (never /tmp)" % WORK)
    lines.append("")
    for name, fn, arg in CASES:
        d = clone(name)
        if fn is edit_province:
            edit_province(d, arg)
        elif fn is not None:
            fn(d)
        commit(d, name)
        n = len(open(os.path.join(d, "PROVINCE.md"), encoding="utf-8").read().split("\n"))
        lines.append("CASE %-30s PROVINCE_lines=%3d probe=%s" % (name, n, probe(d)))
        lines.append("%-35s census=%s" % ("", census(d)))

    # -- applied patch texts -------------------------------------------------
    lines.append("")
    lines.append("== applied patch texts ==")
    d = clone("ex14-demo")
    p = sh([sys.executable, RV4_APPLIER, EX14, d], check=False)
    lines.append("EX-14 demo patch (RV-4 prose applier): rc=%d %s"
                 % (p.returncode, p.stdout.strip().replace("\n", " | ")))
    commit(d, "ex14")
    lines.append("  PROVINCE lines=%d sha=%s"
                 % (len(open(os.path.join(d, "PROVINCE.md"), encoding="utf-8").read().split("\n")),
                    sh(["sha256sum", "PROVINCE.md"], cwd=d).stdout.split()[0]))
    lines.append("  probe=%s" % (probe(d),))
    lines.append("  census=%s" % (census(d),))

    d = clone("ex26-ruling")
    rp = os.path.join(d, ".ufo/gates/custody-pair/README.md")
    t = open(rp, encoding="utf-8").read()
    block = open(EX26, encoding="utf-8").read()
    anchor = "## Exit codes (declared)"
    assert t.count(anchor) == 1
    open(rp, "w", encoding="utf-8").write(t.replace(anchor, block + anchor, 1))
    commit(d, "ex26")
    lines.append("C3 EX-26 ruling block inserted before `%s`:" % anchor)
    lines.append("  README lines=%d sha=%s"
                 % (len(open(rp, encoding="utf-8").read().split("\n")),
                    sh(["sha256sum", ".ufo/gates/custody-pair/README.md"], cwd=d).stdout.split()[0]))
    lines.append("  probe=%s" % (probe(d),))

    out = "\n".join(lines) + "\n"
    print(out)
    with open(os.path.join(args.out, "interplay-battery.txt"), "w") as fh:
        fh.write(out)
    print("written: %s" % os.path.join(args.out, "interplay-battery.txt"))


if __name__ == "__main__":
    main()
