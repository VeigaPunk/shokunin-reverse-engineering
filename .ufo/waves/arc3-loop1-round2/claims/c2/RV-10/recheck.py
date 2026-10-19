#!/usr/bin/env python3
"""RV-10 quick conformance re-check, parameterized by revision sha (first 8)."""
import json, os, sys

sys.path.insert(0, "/var/tmp/rv10")
import driver as D
import driver2 as D2
import driver3 as D3
import driver5 as D5

SHA = sys.argv[1]
REPO = D.REPO
cur_src = REPO + "/.ufo/gates/c1-census-v10.py"
CUR = "/var/tmp/rv10/tool/census-%s.py" % SHA
if not os.path.exists(CUR):
    D.shutil.copy(cur_src, CUR)
have = D.sha256(CUR)[:8]
assert have == SHA, "snapshot sha %s != requested %s (file moved)" % (have, SHA)
D.CENSUS["cur"] = CUR
D.CENSUS["curblind"] = "/var/tmp/rv10/tool/census-%s-blind.py" % SHA
D.CENSUS["curver"] = "/var/tmp/rv10/tool/census-%s-blindver.py" % SHA
D.CENSUS["curpin"] = "/var/tmp/rv10/tool/census-%s-blindpin.py" % SHA
if not os.path.exists(D.CENSUS["curblind"]):
    D5.neutral(open(CUR, encoding="utf-8").read(), SHA)

print("== re-check %s (sha256 %s, %d lines) ==" % (SHA, D.sha256(CUR)[:16],
      len(open(CUR, encoding="utf-8").read().splitlines())))
D.rows = []
D.census_run("Q0-repo-clean", "cur", "Q0", "PASS->0 (ordinary at HEAD)", 0, None, root=REPO)
D.census_run("Q1-blank-skill", "cur", "Q1", "per-file floor->1", 1, D5.m_blank_skill)
D.census_run("Q2-strip-skill", "cur", "Q2", "per-file floor->1", 1, D5.m_strip_skill)
D.census_run("Q3-blind-all", "curblind", "Q3", "BLIND->1", 1)
D.census_run("Q4-partial-ver", "curver", "Q4", "declared residual", None)
D.census_run("Q5-partial-pin", "curpin", "Q5", "declared residual", None)
D.census_run("Q6-skill-absent", "cur", "Q6", "UNREADABLE->1", 1, D.m_absent_skill)
D.census_run("Q7-skill-empty", "cur", "Q7", "UNREADABLE->1", 1, D.m_skill_empty)
D.census_run("Q8-false-pin", "cur", "Q8", "STALE->1", 1, D.m_pin)
D.census_run("Q9-anchor", "cur", "Q9", "ANCHOR->2", 2, None, home=D.FAKEHOME)
D.census_run("Q10-shelter", "cur", "Q10", "named residual", None, D.m_shelter)
D.census_run("Q11-fifo", "cur", "Q11", "not in map", None, D.m_skill_fifo, timeout=5)
D.census_run("Q12-badflag", "cur", "Q12", "not in map", None, None, extra=("--bogus",))
with open(D.RV + "/logs/recheck-%s.tsv" % SHA, "w") as fh:
    fh.write("\n".join(D.rows) + "\n")
