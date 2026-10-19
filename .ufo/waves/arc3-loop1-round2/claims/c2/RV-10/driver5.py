#!/usr/bin/env python3
"""RV-10 pass 5: conformance against the CURRENT census revision (per-file floor)."""
import json, os, sys

sys.path.insert(0, "/var/tmp/rv10")
import driver as D
import driver2 as D2
import driver3 as D3

SHA = sys.argv[1] if len(sys.argv) > 1 else "09e270c2"
CUR = "/var/tmp/rv10/tool/census-%s.py" % SHA
D.CENSUS["cur"] = CUR


def neutral(src, name):
    def rep(t, old, new):
        assert old in t, old[:50]
        return t.replace(old, new, 1)
    blind = rep(rep(rep(src, r'PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)', r'PIN = re.compile(r"rea-agents@(ZZZ\d+)", re.I)'),
                   r'VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")', r'VER = re.compile(r"(?<![\d.])9\.\d+\.\d+")'),
                   r'PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")', r'PTR = re.compile(r"((?:~|/)ZZZ\.(?:json|toml|ya?ml)):(\d+)")')
    open("/var/tmp/rv10/tool/census-%s-blind.py" % name, "w").write(blind)
    ver = rep(src, r'VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")', r'VER = re.compile(r"(?<![\d.])9\.\d+\.\d+")')
    open("/var/tmp/rv10/tool/census-%s-blindver.py" % name, "w").write(ver)
    pin = rep(src, r'PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)', r'PIN = re.compile(r"rea-agents@(ZZZ\d+)", re.I)')
    open("/var/tmp/rv10/tool/census-%s-blindpin.py" % name, "w").write(pin)


def m_blank_skill(case):      # line count preserved, zero loci in SKILL.md
    p = case + "/SKILL.md"
    n = len(open(p, encoding="utf-8").read().splitlines())
    open(p, "w", encoding="utf-8").write("\n".join("placeholder line %d" % i for i in range(n)) + "\n")


def m_strip_skill(case):      # needles neutralised in place, line count preserved
    p = case + "/SKILL.md"
    t = open(p, encoding="utf-8").read()
    t = t.replace("rea-agents@6.5.0", "rea-agents@n/a").replace("rea-agents@6.7.0", "rea-agents@n/a")
    open(p, "w", encoding="utf-8").write(t)


def main():
    src = open(CUR, encoding="utf-8").read()
    neutral(src, SHA)
    D.CENSUS["curblind"] = "/var/tmp/rv10/tool/census-%s-blind.py" % SHA
    D.CENSUS["curver"] = "/var/tmp/rv10/tool/census-%s-blindver.py" % SHA
    D.CENSUS["curpin"] = "/var/tmp/rv10/tool/census-%s-blindpin.py" % SHA
    print("== pass 5: current %s (sha256 %s) ==" % (SHA, D.sha256(CUR)[:16]))
    D.rows = []
    # parity with the declared PASS/FAIL/anchor map
    D.census_run("M0-repo", "cur", "M0", "PASS", 0, None, root=D.REPO, extra=("--json",))
    D.census_run("M0b-copy-quiet", "cur", "M0b", "PASS", 0)
    D.census_run("M1-false-pin", "cur", "M1", "STALE->FAIL", 1, D.m_pin)
    D.census_run("M2-undeclared", "cur", "M2", "UNDECLARED->FAIL", 1, D.m_append)
    D.census_run("M3-marker-strip", "cur", "M3", "SCOPE-ERROR->FAIL", 1, D.m_marker)
    D.census_run("M4b-ptr-beyond", "cur", "M4b", "UNRESOLVED->FAIL", 1, D2.m_prov44_ptr_beyond)
    D.census_run("M5-shelter", "cur", "M5", "named residual PASS", 0, D.m_shelter)
    D.census_run("M6-anchor", "cur", "M6", "ANCHOR-FAIL", 2, None, home=D.FAKEHOME)
    D.census_run("M7-anchor-json", "cur", "M7", "ANCHOR-FAIL", 2, None, home=D.FAKEHOME, extra=("--json",))
    # H1 class
    D.census_run("M8-skill-absent", "cur", "M8", "UNREADABLE->FAIL", 1, D.m_absent_skill)
    D.census_run("M9-sc-absent", "cur", "M9", "UNREADABLE->FAIL", 1, D.m_absent_sc)
    D.census_run("M10-prov-absent", "cur", "M10", "UNREADABLE->FAIL", 1, D.m_absent_prov)
    D.census_run("M11-root-absent", "cur", "M11", "UNREADABLE->FAIL", 1, None, root=D.RV + "/nope")
    D.census_run("M12-skill-dir", "cur", "M12", "UNREADABLE->FAIL", 1, D.m_skill_dir)
    D.census_run("M13-skill-chmod0", "cur", "M13", "UNREADABLE->FAIL", 1, D.m_skill_chmod0)
    D.census_run("M14-skill-empty", "cur", "M14", "UNREADABLE->FAIL", 1, D.m_skill_empty)
    D.census_run("M15-sc-empty", "cur", "M15", "UNREADABLE->FAIL", 1, D.m_sc_empty)
    D.census_run("M16-skill-trunc15", "cur", "M16", "UNREADABLE->FAIL", 1, D3.m_trunc_skill)
    D.census_run("M17-skill-fifo", "cur", "M17", "not in map", None, D.m_skill_fifo, timeout=5)
    # H3 class incl. the new per-file floor
    D.census_run("M18-blind-all", "curblind", "M18", "BLIND->FAIL", 1)
    D.census_run("M19-partial-ver", "curver", "M19", "declared residual", None)
    D.census_run("M20-partial-pin", "curpin", "M20", "declared residual", None)
    D.census_run("M21-blank-skill", "cur", "M21", "per-file floor->FAIL", 1, m_blank_skill)
    D.census_run("M22-strip-skill", "cur", "M22", "per-file floor->FAIL", 1, m_strip_skill)
    D.census_run("M23-blank-skill-json", "cur", "M23", "per-file floor->FAIL", 1, m_blank_skill, extra=("--json",))
    D.census_run("M24-badflag", "cur", "M24", "not in map (argparse)", None, None, extra=("--bogus",))
    print("\nWROTE %d rows" % len(D.rows))
    with open(D.RV + "/logs/matrix5-%s.tsv" % SHA, "w") as fh:
        fh.write("\n".join(D.rows) + "\n")


if __name__ == "__main__":
    main()
