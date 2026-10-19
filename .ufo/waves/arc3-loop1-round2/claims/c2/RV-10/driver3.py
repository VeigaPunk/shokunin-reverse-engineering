#!/usr/bin/env python3
"""RV-10 pass 3: exit-code conformance against EX-16's LANDED v11."""
import json, os, sys

sys.path.insert(0, "/var/tmp/rv10")
import driver as D
import driver2 as D2

D.CENSUS["landed"] = "/var/tmp/rv10/tool/census-landed.py"
L = "landed"


def m_trunc_skill(case):
    p = case + "/SKILL.md"
    L_ = open(p, encoding="utf-8").read().splitlines()
    open(p, "w", encoding="utf-8").write("\n".join(L_[:15]) + "\n")


def m_trunc_prov(case):
    p = case + "/PROVINCE.md"
    L_ = open(p, encoding="utf-8").read().splitlines()
    open(p, "w", encoding="utf-8").write("\n".join(L_[:100]) + "\n")


def main():
    print("== pass 3: landed %s ==" % D.sha256(D.CENSUS[L])[:16])
    D.rows = []
    D.census_run("L0-baseline-repo", L, "L0", "PASS", 0, None, root=D.REPO)
    D.census_run("L0b-baseline-copy", L, "L0b", "PASS", 0)
    D.census_run("L1-false-current-pin", L, "L1", "STALE->FAIL", 1, D.m_pin)
    D.census_run("L2-undeclared-append", L, "L2", "UNDECLARED->FAIL", 1, D.m_append)
    D.census_run("L3-marker-strip", L, "L3", "SCOPE-ERROR->FAIL", 1, D.m_marker)
    D.census_run("L4b-ptr-beyond-EOF", L, "L4b", "UNRESOLVED->FAIL", 1, D2.m_prov44_ptr_beyond)
    D.census_run("L5-dated-shelter", L, "L5", "DATED fail-open (named residual)", 0, D.m_shelter)
    D.census_run("L6-anchor-fail", L, "L6", "ANCHOR-FAIL", 2, None, home=D.FAKEHOME)
    D.census_run("L7-anchor-fail-json", L, "L7", "ANCHOR-FAIL", 2, None, home=D.FAKEHOME, extra=("--json",))
    print("\n-- H1 class on landed --")
    D.rows.append("-- H1 class on landed --")
    D.census_run("L8-skill-absent", L, "L8", "UNREADABLE->FAIL", 1, D.m_absent_skill)
    D.census_run("L9-scorecard-absent", L, "L9", "UNREADABLE->FAIL", 1, D.m_absent_sc)
    D.census_run("L10-province-absent", L, "L10", "UNREADABLE->FAIL", 1, D.m_absent_prov)
    D.census_run("L11-root-absent", L, "L11", "UNREADABLE->FAIL", 1, None, root=D.RV + "/nope")
    D.census_run("L12-skill-is-dir", L, "L12", "UNREADABLE->FAIL", 1, D.m_skill_dir)
    D.census_run("L13-skill-chmod000", L, "L13", "UNREADABLE->FAIL", 1, D.m_skill_chmod0)
    D.census_run("L14-skill-empty", L, "L14", "UNREADABLE->FAIL", 1, D.m_skill_empty)
    D.census_run("L15-scorecard-empty", L, "L15", "UNREADABLE->FAIL", 1, D.m_sc_empty)
    D.census_run("L16-skill-truncated-15", L, "L16", "UNREADABLE->FAIL", 1, m_trunc_skill)
    D.census_run("L17-province-truncated-100", L, "L17", "UNREADABLE->FAIL", 1, m_trunc_prov)
    D.census_run("L18-skill-fifo", L, "L18", "not in map", None, D.m_skill_fifo, timeout=5)
    print("\n-- H3 class on landed --")
    D.rows.append("-- H3 class on landed --")
    D.census_run("L19-blind-all", "blind", "L19", "BLIND->FAIL", 1)
    D.census_run("L20-partial-blind-ver", "blindver", "L20", "declared residual (tree floor)", None)
    print("\n-- modes / invocation --")
    D.rows.append("-- modes / invocation --")
    D.census_run("L21-json-unreadable", L, "L21", "UNREADABLE->FAIL", 1, D.m_skill_empty, extra=("--json",))
    D.census_run("L22-json-clean", L, "L22", "PASS", 0, None, extra=("--json",))
    D.census_run("L23-badflag", L, "L23", "not in map (argparse)", None, None, extra=("--bogus",))
    D.census_run("L24-help", L, "L24", "not in map (argparse)", 0, None, extra=("-h",))
    print("\nWROTE %d rows" % len(D.rows))
    with open(D.RV + "/logs/matrix3.tsv", "w") as fh:
        fh.write("\n".join(D.rows) + "\n")


if __name__ == "__main__":
    main()
