#!/usr/bin/env python3
"""CR-3 — generate floor-variant copies of census v10 and run them on roots.

Variants (all textual edits of the pristine gate, sha 6f1d19ff…):
  none    pristine control copy
  blind   needles neutered (round-1 CR-5 method)
  row     floor: every declared SCOPE row in-bounds must hold >=1 assert
  rowany  floor: as 'row', plus rows whose file is absent/unreadable
  class   floor: every CURRENT row must hold >=1 assert
  file    floor: every scoped file with lines>0 must hold >=1 locus
  global  floor: corpus total loci > 0
Blind combos: blind_row, blind_class, blind_global, blind_file.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

GATE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py"
REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCR = "/var/tmp/cr3/scratch"
REC = "/var/tmp/cr3/receipts"
SRC = open(GATE, encoding="utf-8").read()

assert hashlib.sha256(SRC.encode()).hexdigest() == \
    "6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b", "gate drift"

A1 = '''        loci.append(rec)
        out.setdefault(disp, []).append(rec)
'''
A1N = A1 + '        out.setdefault("__all__", []).append(rec)\n'

A2 = '''    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\
         and (not g11) and g2_ok
'''
FLOOR = '''    FLOOR_MODE = "MODEHERE"
    all_loci = out.get("__all__", [])
    def _row_counts():
        rc = {}
        for (rf, rs, re_, rcls, rml, rmr) in SCOPE:
            n = 0
            for rec0 in all_loci:
                if rec0["file"] != rf:
                    continue
                for d0 in rec0["asserts"]:
                    if rs <= d0["line"] <= re_:
                        n += 1
            rc["%s:%d-%d" % (rf, rs, re_)] = (n, rcls, filelines.get(rf))
        return rc
    floor_violations = []
    if FLOOR_MODE == "row":
        floor_violations = [k for k, (n, _c, _fl) in _row_counts().items() if n == 0]
    elif FLOOR_MODE == "rowany":
        floor_violations = [k for k, (n, _c, fl) in _row_counts().items() if n == 0 or not fl]
    elif FLOOR_MODE == "class":
        floor_violations = [k for k, (n, c_, _fl) in _row_counts().items()
                            if n == 0 and c_ == "CURRENT"]
    elif FLOOR_MODE == "file":
        floor_violations = [f for f, c in counts.items() if c["lines"] > 0 and c["loci"] == 0]
    elif FLOOR_MODE == "global":
        floor_violations = [] if sum(c["loci"] for c in counts.values()) > 0 else ["<corpus>"]
    floor_ok = not floor_violations
    print("FLOOR(%s) violations: %r" % (FLOOR_MODE, floor_violations), file=sys.stderr)
''' + A2.replace("and g2_ok\n", "and g2_ok and floor_ok\n")

NEUTER = [
    ('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
     'PIN = re.compile(r"rea-agents@(ZZZ\\d+)", re.I)'),
    ('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
     'VER = re.compile(r"(?<![\\d.])9\\.\\d+\\.\\d+")'),
    ('PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")',
     'PTR = re.compile(r"((?:~|/)ZZZ\\.(?:json|toml|ya?ml)):(\\d+)")'),
]


def variant(name, mode, blind):
    t = SRC
    t2 = t.replace(A1, A1N, 1)
    assert t2 != t, name + ": anchor1"
    t = t2.replace(A2, FLOOR.replace("MODEHERE", mode), 1)
    assert t != t2, name + ": anchor2"
    if blind:
        for old, new in NEUTER:
            t2 = t.replace(old, new, 1)
            assert t2 != t, name + ": neuter " + old[:30]
            t = t2
    p = os.path.join(SCR, "census-%s.py" % name)
    open(p, "w", encoding="utf-8").write(t)
    return p


def run(tool, root, tag):
    r = subprocess.run([sys.executable, tool, "--root", root, "--json"],
                       capture_output=True, text=True, timeout=120)
    out = "\n".join(l for l in r.stdout.splitlines() if not l.startswith("FLOOR("))
    floor = [l for l in r.stderr.splitlines() if l.startswith("FLOOR(")]
    try:
        import json
        d = json.loads(out)
        v = d["verdict"]
        counts = d["counts"]
    except Exception:
        v, counts = "PARSE-FAIL", out[:200]
    path = os.path.join(REC, tag + ".out")
    open(path, "w", encoding="utf-8").write(
        "cmd: python3 %s --root %s --json\nexit: %d\n" % (tool, root, r.returncode)
        + r.stdout + ("\n--stderr--\n" + r.stderr if r.stderr else ""))
    print("%-22s exit=%d verdict=%s counts=%s" % (tag, r.returncode, v, counts))
    for line in floor:
        print("      " + line)
    return r.returncode, v


if __name__ == "__main__":
    os.makedirs(SCR, exist_ok=True)
    os.makedirs(REC, exist_ok=True)

    # injection root: plant needles in one zero-locus DATED row + one CURRENT row
    INJ = os.path.join(SCR, "root-inj")
    os.makedirs(INJ, exist_ok=True)
    for f in ("PROVINCE.md", "SKILL.md", "SCORECARD.md"):
        shutil.copyfile(os.path.join(REPO, f), os.path.join(INJ, f))
    sc = open(os.path.join(INJ, "SCORECARD.md"), encoding="utf-8").read().splitlines()
    sc[779:779] = ["  - planted probe pin rea-agents@6.3.0 in a zero-locus DATED row."]
    open(os.path.join(INJ, "SCORECARD.md"), "w", encoding="utf-8").write("\n".join(sc) + "\n")
    sk = open(os.path.join(INJ, "SKILL.md"), encoding="utf-8").read().splitlines()
    sk[14:14] = ["  - devin pin rea-agents@6.3.0 planted in a CURRENT row."]
    open(os.path.join(INJ, "SKILL.md"), "w", encoding="utf-8").write("\n".join(sk) + "\n")

    # H1 root: SKILL.md absent (round-1 H1 case: CURRENT-only file)
    H1 = os.path.join(SCR, "root-noskill")
    os.makedirs(H1, exist_ok=True)
    for f in ("PROVINCE.md", "SCORECARD.md"):
        shutil.copyfile(os.path.join(REPO, f), os.path.join(H1, f))

    v_none = variant("none", "none", False)
    v_blind = variant("blind", "none", True)
    v_row = variant("row", "row", False)
    v_rowany = variant("rowany", "rowany", False)
    v_class = variant("class", "class", False)
    v_file = variant("file", "file", False)
    v_global = variant("global", "global", False)
    v_brow = variant("blind-row", "row", True)
    v_bclass = variant("blind-class", "class", True)
    v_bglobal = variant("blind-global", "global", True)
    v_bfile = variant("blind-file", "file", True)

    print("--- control + before-state (H3 reproduction) at HEAD ---")
    run(v_none, REPO, "v-none-head")
    run(v_blind, REPO, "v-blind-head")
    print("--- floor variants at HEAD ---")
    run(v_row, REPO, "v-row-head")
    run(v_rowany, REPO, "v-rowany-head")
    run(v_class, REPO, "v-class-head")
    run(v_file, REPO, "v-file-head")
    run(v_global, REPO, "v-global-head")
    print("--- blind + floor (after-state must FAIL) at HEAD ---")
    run(v_brow, REPO, "v-blind-row-head")
    run(v_bclass, REPO, "v-blind-class-head")
    run(v_bglobal, REPO, "v-blind-global-head")
    run(v_bfile, REPO, "v-blind-file-head")
    print("--- needle injections (row functionality) ---")
    run(v_none, INJ, "v-none-inj")
    run(v_row, INJ, "v-row-inj")
    print("--- H1 interaction: SKILL.md absent ---")
    run(v_none, H1, "v-none-noskill")
    run(v_row, H1, "v-row-noskill")
    run(v_rowany, H1, "v-rowany-noskill")
    run(v_class, H1, "v-class-noskill")
    run(v_file, H1, "v-file-noskill")
