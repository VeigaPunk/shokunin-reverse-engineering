#!/usr/bin/env python3
"""EX-29 simulation suite for the census SCOPE retirement/laundering analysis.

Runs seven measured cases against fixtures built from the repo root at run time.
Writes nothing outside .sim-work/ (created and removed by this script).
Usage: python3 sim-suite.py            (from the repo root)
"""
import os, shutil, subprocess, sys

REPO = os.getcwd()
SEAT = os.path.join(REPO, ".ufo/waves/arc3-loop1-round1/claims/c3/EX-29")
WORK = os.path.join(SEAT, ".sim-work")
CENSUS = os.path.join(REPO, ".ufo/gates/c1-census-v10.py")
FILES = ("PROVINCE.md", "SKILL.md", "SCORECARD.md")

ROW_PROV_40 = '    ("PROVINCE.md", 40, 43, "DATED", 40, r"verified on this host 2026-10-13"),\n'
ROW_SC_12 = '    ("SCORECARD.md", 417, 466, "DATED", 417, r"2026-10-16"),\n'
ROW_SC_13 = '    ("SCORECARD.md", 467, 502, "DATED", 467, r"2026-10-16"),\n'
ROW_SC_20 = '    ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3")'
ROW_SC_11 = '    ("SCORECARD.md", 273, 326, "DATED", 273, r"2026-10-16")'

PLANT_B = ("The live Kimi pin remains `rea-agents@6.4.0` at "
           "`~/.kimi-code/config.toml:3298` this round.")
PLANT_C = ("The live Kimi pin remains `rea-agents@6.4.0` at "
           "`~/.kimi-code/config.toml:3298` this round.")


def build_fixture(name, plant_line, plant_text):
    d = os.path.join(WORK, name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for f in FILES:
        shutil.copyfile(os.path.join(REPO, f), os.path.join(d, f))
    if plant_line:
        p = os.path.join(d, "SCORECARD.md")
        lines = open(p, encoding="utf-8").read().splitlines()
        assert not lines[plant_line - 1].strip(), "plant site not blank"
        lines[plant_line - 1] = plant_text
        open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return d


def build_variant(tag, subs):
    s = open(CENSUS, encoding="utf-8").read()
    for a, b in subs:
        assert a in s, "substitution anchor missing: %r" % a
        s = s.replace(a, b, 1)
    p = os.path.join(WORK, "census-%s.py" % tag)
    open(p, "w", encoding="utf-8").write(s)
    return p


def run(tag, script, root, note):
    r = subprocess.run([sys.executable, script, "--root", root],
                       capture_output=True, text=True)
    print("### %s" % tag)
    print("    note : %s" % note)
    print("    cmd  : python3 %s --root %s" % (os.path.relpath(script, REPO),
                                                os.path.relpath(root, REPO)))
    keys = ("live anchors", "SCOPE-ERRORS", "G2 positive", "VERDICT",
            "ANCHOR-FAIL")
    for line in r.stdout.splitlines():
        if line.startswith(keys):
            print("    %s" % line)
    for line in r.stdout.splitlines():
        if "-> historical" in line or "-> STALE" in line or "-> UNDECLARED" in line \
           or "-> AMBIGUOUS" in line:
            print("    locus %s" % line.strip())
    print("    exit : %d" % r.returncode)
    print()


def main():
    if os.path.isdir(WORK):
        shutil.rmtree(WORK)
    os.makedirs(WORK)

    pristine = build_fixture("fixture-pristine", None, None)

    # ---- SIM-A: retirement neutrality (real HEAD content, unplanted) ------
    a1 = build_variant("retire-3-20", [(ROW_PROV_40, ""), (ROW_SC_20 + ",\n", "")])
    run("SIM-A1 retire rows 3+20 (recommended set)", a1, pristine,
        "real HEAD content; expect PASS 0/0/0/0, SCOPE-ERRORS []")
    a2 = build_variant("retire-all4", [(ROW_PROV_40, ""), (ROW_SC_12, ""),
                                       (ROW_SC_13, ""), (ROW_SC_20 + ",\n", "")])
    run("SIM-A2 retire rows 3+12+13+20 (widest retire set)", a2, pristine,
        "real HEAD content; expect PASS 0/0/0/0 (retirement is verdict-neutral)")
    run("SIM-A0 control: unmodified v10", CENSUS, pristine,
        "real HEAD content under the landed table; expect PASS 0/0/0/0")

    # ---- SIM-B: overshoot / shelter (planted stale claim at :856) ---------
    fx_b = build_fixture("fixture-launder", 856, PLANT_B)
    run("SIM-B1 planted stale claim at :856, landed table", CENSUS, fx_b,
        "expect FAIL: the planted locus is outside every declared row")
    b2 = build_variant("widen-856", [(ROW_SC_20, '    ("SCORECARD.md", 769, 856, "DATED", 769, r"arc2-loop1-round3")')])
    run("SIM-B2 same plant, row 20 widened 855->856 (minimal widen to pass)",
        b2, fx_b, "expect PASS: the stale claim is absorbed as historical")
    b3 = build_variant("widen-eof", [(ROW_SC_20, '    ("SCORECARD.md", 769, 1336, "DATED", 769, r"arc2-loop1-round3")')])
    run("SIM-B3 same plant, row 20 widened to EOF 855->1336", b3, fx_b,
        "expect PASS: same shelter, larger")

    # ---- SIM-C: slide absorption (planted stale claim at :272) -----------
    fx_c = build_fixture("fixture-slide", 272, PLANT_C)
    run("SIM-C1 planted stale claim at :272, landed table", CENSUS, fx_c,
        "expect FAIL: :272 sits in the luna-round-1 tail, undeclared")
    c2 = build_variant("slide-11", [(ROW_SC_11, '    ("SCORECARD.md", 268, 321, "DATED", 273, r"2026-10-16")')])
    run("SIM-C2 same plant, row 11 as the content-equivalent of an un-re-keyed "
        "+5 slide (273,326 -> 268,321)", c2, fx_c,
        "expect PASS: the stale claim is absorbed into the DATED range")
    c3 = build_variant("anchored-11", [(ROW_SC_11, '    ("SCORECARD.md", 278, 331, "DATED", 273, r"2026-10-16")')])
    run("SIM-C3 control: content-anchored re-key after +5 growth (278,331)",
        c3, fx_c, "expect FAIL: the anchored bound does not reach :272")

    shutil.rmtree(WORK)
    print("sim work dir removed: %s" % WORK)


if __name__ == "__main__":
    main()
