#!/usr/bin/env python3
"""PL-2 fixture matrix: landed v11 vs v10 baseline (arc3-loop1-round2, chain c2).

Scratch under /dev/shm only. Writes full per-run receipts to <work>/outs/.
Usage: python3 matrix.py [--work /dev/shm/pl2/matrix]
"""
import argparse, hashlib, os, re, shutil, subprocess, sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
V10_SRC = REPO + "/.ufo/waves/arc3-loop1-round2/claims/c2/RV-6/before/c1-census-v10.py"
LIVE = REPO + "/.ufo/gates/c1-census-v10.py"
FILES = ["PROVINCE.md", "SKILL.md", "SCORECARD.md"]
TREES = ["b21c0da", "679af5d", "158a966", "1692acb", "265e1aa", "6bc4c29", "fd30b9c"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(instr, root, json_mode=False):
    cmd = [sys.executable, instr, "--root", root] + (["--json"] if json_mode else ["--quiet"])
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def classlines(out):
    keep = ("VERDICT:", "UNREADABLE", "DECLARED FAIL", "G2 ", "SCOPE-ERRORS", "ANCHOR-FAIL")
    return " | ".join(l.strip() for l in out.splitlines() if l.strip().startswith(keep))


def variant(src, dst, subs, tag):
    txt = open(src, encoding="utf-8").read()
    for old, new in subs:
        assert txt.count(old) == 1, "%s anchor missing/ambiguous: %r" % (tag, old[:50])
        txt = txt.replace(old, new)
    open(dst, "w", encoding="utf-8").write(txt)
    return dst


NEUTER = [('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
           'PIN = re.compile(r"never-match-A")'),
          ('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
           'VER = re.compile(r"never-match-B")'),
          ('PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")',
           'PTR = re.compile(r"never-match-C")')]
NARROW_GATE = [('REA_GATE = re.compile(r"rea-agents|\\brea\\b|config\\.toml|mcp_config\\.json|mcp\\.json|mcp_servers|devin|\\bomp\\b|kimi|npx", re.I)',
                'REA_GATE = re.compile(r"zzz-never-match")')]
WEAK_PIN = [('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
             'PIN = re.compile(r"rea-agents@(6\\.5\\.\\d+)", re.I)')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/dev/shm/pl2/matrix")
    args = ap.parse_args()
    W = args.work
    for d in ("outs", "instruments", "cases"):
        os.makedirs(os.path.join(W, d), exist_ok=True)

    v10 = os.path.join(W, "instruments", "v10-ref.py")
    shutil.copy2(V10_SRC, v10)
    landed_snap = os.path.join(W, "instruments", "landed-%s.py" % sha(LIVE)[:8])
    shutil.copy2(LIVE, landed_snap)
    print("v10-ref      sha256 %s" % sha(v10))
    print("landed       sha256 %s  (live path %s)" % (sha(landed_snap), sha(LIVE)))
    if sha(landed_snap) != sha(LIVE):
        print("WARNING: live target moved while snapshotting")

    base = os.path.join(W, "cases", "base", "root")
    shutil.rmtree(os.path.join(W, "cases"), ignore_errors=True)
    os.makedirs(base)
    for f in FILES:
        shutil.copy2(os.path.join(REPO, f), os.path.join(base, f))

    def case(name, mutate=None):
        cdir = os.path.join(W, "cases", name)
        root = os.path.join(cdir, "root")
        sub = os.path.join(cdir, "sub")
        shutil.copytree(base, root)
        if mutate:
            mutate(root)
        row = []
        for tag, instr in (("v10", v10), ("v11", landed_snap)):
            rc, out = run(instr, root)
            open(os.path.join(W, "outs", "%s.%s.out" % (name, tag)), "w",
                 encoding="utf-8").write(out + "\nEXIT=%d\n" % rc)
            row.append("%s exit=%d %s" % (tag, rc, classlines(out)))
        print("[%-22s] %s" % (name, "  ||  ".join(row)))

    print("\n== fixture matrix ==")
    case("c0-baseline")
    case("cA-absent-skill", lambda r: os.remove(os.path.join(r, "SKILL.md")))
    case("cA2-empty-skill", lambda r: open(os.path.join(r, "SKILL.md"), "w").close())
    def trunc(r):
        keep = open(os.path.join(r, "SKILL.md"), encoding="utf-8").read().splitlines()[:5]
        open(os.path.join(r, "SKILL.md"), "w", encoding="utf-8").write("\n".join(keep) + "\n")
    case("cA3-trunc-skill", trunc)
    case("cB-absent-province", lambda r: os.remove(os.path.join(r, "PROVINCE.md")))
    case("cB2-absent-scorecard", lambda r: os.remove(os.path.join(r, "SCORECARD.md")))
    case("cF-eacces-skill", lambda r: os.chmod(os.path.join(r, "SKILL.md"), 0))
    case("cG-dir-skill", lambda r: (os.remove(os.path.join(r, "SKILL.md")),
                                    os.mkdir(os.path.join(r, "SKILL.md"))))
    case("cE-empty-root2", lambda r: [os.remove(os.path.join(r, f)) for f in FILES])

    print("\n== instrument variants (same root as c0) ==")
    neut10 = variant(v10, os.path.join(W, "instruments", "v10-neutered.py"), NEUTER, "n10")
    neut11 = variant(landed_snap, os.path.join(W, "instruments", "v11-neutered.py"), NEUTER, "n11")
    gate10 = variant(v10, os.path.join(W, "instruments", "v10-gate.py"), NARROW_GATE, "g10")
    gate11 = variant(landed_snap, os.path.join(W, "instruments", "v11-gate.py"), NARROW_GATE, "g11")
    weak10 = variant(v10, os.path.join(W, "instruments", "v10-weakpin.py"), WEAK_PIN, "w10")
    weak11 = variant(landed_snap, os.path.join(W, "instruments", "v11-weakpin.py"), WEAK_PIN, "w11")
    for name, i10, i11 in (("cC-neutered", neut10, neut11),
                           ("cC2-gate-narrowed", gate10, gate11),
                           ("cD1b-weak-pin", weak10, weak11)):
        row = []
        for tag, instr in (("v10", i10), ("v11", i11)):
            rc, out = run(instr, base)
            open(os.path.join(W, "outs", "%s.%s.out" % (name, tag)), "w",
                 encoding="utf-8").write(out + "\nEXIT=%d\n" % rc)
            row.append("%s exit=%d %s" % (tag, rc, classlines(out)))
        print("[%-22s] %s" % (name, "  ||  ".join(row)))

    print("\n== historical trees (attribution only; old tree vs new scope table) ==")
    for t in TREES:
        root = os.path.join(REPO, ".ufo/waves/arc3-loop1-round1/claims/c3/RV-11/scratch", "tree-" + t)
        if not os.path.isdir(root):
            print("[tree-%s] MISSING" % t)
            continue
        row = []
        for tag, instr in (("v10", v10), ("v11", landed_snap)):
            rc, out = run(instr, root)
            open(os.path.join(W, "outs", "tree-%s.%s.out" % (t, tag)), "w",
                 encoding="utf-8").write(out + "\nEXIT=%d\n" % rc)
            v = [l for l in out.splitlines() if l.startswith("VERDICT")]
            row.append("%s exit=%d %s" % (tag, rc, v[0] if v else "?"))
        print("[tree-%-10s] %s" % (t, "  ||  ".join(row)))

    print("\n== HEAD json key delta ==")
    rc10, o10 = run(v10, REPO, json_mode=True)
    rc11, o11 = run(landed_snap, REPO, json_mode=True)
    import json as _json
    j10, j11 = _json.loads(o10), _json.loads(o11)
    print("v10 keys: %s" % sorted(j10))
    print("v11 keys added: %s" % sorted(set(j11) - set(j10)))
    print("v11 keys removed: %s" % sorted(set(j10) - set(j11)))
    same = [k for k in j10 if k in j11 and j10[k] == j11[k]]
    diff = [k for k in j10 if k in j11 and j10[k] != j11[k]]
    print("shared keys equal: %d  differing: %r" % (len(same), diff))
    open(os.path.join(W, "outs", "head-v10.json"), "w").write(o10)
    open(os.path.join(W, "outs", "head-v11.json"), "w").write(o11)


if __name__ == "__main__":
    sys.exit(main())
