#!/usr/bin/env python3
"""EX-13 (c2) re-check on R4 (EX-16's per-readable-file floor) + variant C prototype.

Reads the pinned R4 instrument copy in tools/ (never the live target), builds:
  * root-scorecard-current-silenced (F4): ONLY SCORECARD.md's declared CURRENT row
    56-60 blanked; PROVINCE.md / SKILL.md byte-intact, all DATED rows intact
  * census-r4-variantC.py: R4 + "every readable file with declared CURRENT rows must
    contribute >= 1 current-ok assertion whose own scope is CURRENT" (prototype only)
Writes receipts into ../receipts-r4/ and never touches any repo target.

Usage: python3 r4-recheck.py [--work DIR] [--repo DIR]
"""
import argparse, hashlib, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
R4_SHA = "df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43"
REPO_DEFAULT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

H3K_OLD = '    h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None)\n    g2_ok = h3_ok'
H3K_NEW = '''    # variant C (EX-13, prototype): every readable file that declares CURRENT rows
    # must contribute >= 1 current-ok assertion whose own scope is CURRENT.
    files_with_current = {s[0] for s in SCOPE if s[3] == "CURRENT"}
    cur_floor = {f: 0 for f in files}
    for recs in out.values():
        if not isinstance(recs, list):
            continue
        for rec in recs:
            if not isinstance(rec, dict):
                continue
            for d in rec["asserts"]:
                if d["disp"] == "current-ok" and d["scope"] == "CURRENT":
                    cur_floor[rec["file"]] += 1
    h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None) and \\
        all(cur_floor[f] > 0 for f in files_with_current if filelines[f] is not None)
    g2_ok = h3_ok'''
PRINT_OLD = '''    print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
          % ("ok" if g2_ok else "SUSPECT",
             ", ".join("%s=%d" % (f, floor[f]) for f in files), n_loci))'''
PRINT_NEW = '''    print("G2 positive-assertion guard: %s (current-ok per file: %s; CURRENT-class per file: %s; total loci=%d; floor=1/file+CURRENT)"
          % ("ok" if g2_ok else "SUSPECT",
             ", ".join("%s=%d" % (f, floor[f]) for f in files),
             ", ".join("%s=%d" % (f, cur_floor[f]) for f in files), n_loci))'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/var/tmp/ex13-r2")
    ap.add_argument("--repo", default=REPO_DEFAULT)
    a = ap.parse_args()
    W, R = a.work, a.repo
    OUT = os.path.join(HERE, os.pardir, "receipts-r4")
    os.makedirs(W, exist_ok=True); os.makedirs(OUT, exist_ok=True)

    pinned = os.path.join(HERE, "census-landed-r4.py")
    r4 = open(pinned, encoding="utf-8").read()
    assert hashlib.sha256(r4.encode()).hexdigest() == R4_SHA, "pinned R4 drift"
    open(os.path.join(W, "census-r4.py"), "w").write(r4)
    assert r4.count(H3K_OLD) == 1 and r4.count(PRINT_OLD) == 1, "R4 anchors"
    open(os.path.join(W, "census-r4-variantC.py"), "w").write(
        r4.replace(H3K_OLD, H3K_NEW).replace(PRINT_OLD, PRINT_NEW))

    # F4 fixture
    fx = os.path.join(W, "root-scorecard-current-silenced"); os.makedirs(fx, exist_ok=True)
    for f in ("PROVINCE.md", "SKILL.md"):
        shutil.copy(os.path.join(R, f), os.path.join(fx, f))
    lines = open(os.path.join(R, "SCORECARD.md"), encoding="utf-8").read().splitlines()
    for i in range(55, 60):
        lines[i] = "neutral filler line"
    open(os.path.join(fx, "SCORECARD.md"), "w").write("\n".join(lines) + "\n")

    V = {"r4": os.path.join(W, "census-r4.py"), "r4C": os.path.join(W, "census-r4-variantC.py")}
    ROOTS = {"live": R, "silenced": "%s/root-current-silenced" % W,
             "allsilent2": "%s/root-all-silent2" % W, "f4": fx,
             "skillGone": "%s/root-skill-absent" % W, "empty": "%s/root-empty" % W}
    lines_out = []
    for v in ("r4", "r4C"):
        for r in ("live", "silenced", "allsilent2", "f4", "skillGone", "empty"):
            p = subprocess.run([sys.executable, V[v], "--root", ROOTS[r]], capture_output=True, text=True)
            tag = "%s-%s" % (v, r)
            open(os.path.join(OUT, tag + ".out"), "w").write(p.stdout + p.stderr)
            g2 = next((l.strip() for l in p.stdout.splitlines() if "G2 positive" in l), "?")
            vd = next((l.strip() for l in p.stdout.splitlines() if l.startswith("VERDICT")), "?")
            cls = next((l.strip() for l in p.stdout.splitlines() if l.startswith("DECLARED FAIL")), "")
            row = "%-11s exit=%d %-40s | %s | %s" % (tag, p.returncode, vd, g2[:110], cls)
            lines_out.append(row); print(row)
    lines_out.append("pinned R4 sha256: " + R4_SHA)
    open(os.path.join(OUT, "summary.txt"), "w").write("\n".join(lines_out) + "\n")


if __name__ == "__main__":
    sys.exit(main())
