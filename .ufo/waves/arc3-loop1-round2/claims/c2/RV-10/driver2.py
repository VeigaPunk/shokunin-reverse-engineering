#!/usr/bin/env python3
"""RV-10 pass 2: corrected probe fixtures + in-range UNRESOLVED/STALE classes."""
import json, os, shutil, subprocess, sys

sys.path.insert(0, "/var/tmp/rv10")
import driver as D

RV, REPO = D.RV, D.REPO
P = RV + "/probe"
PTABLE, PEXPECT = D.PTABLE, D.PEXPECT
sha = D.sha256


def m_prov44_ptr_beyond(case):  # in-place mutation of PROVINCE.md:44 (CURRENT single-line row)
    p = case + "/PROVINCE.md"
    L = open(p, encoding="utf-8").read().splitlines()
    assert len(L) >= 44
    L[43] = ("| REA MCP server | See `~/.kimi-code/config.toml:99999` for the pointer-class check "
             "| broken pointer | 2026-10-13 receipt |")
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")


def m_prov44_ptr_nopin(case):  # pointer resolves to a real line that holds no pin -> STALE
    p = case + "/PROVINCE.md"
    L = open(p, encoding="utf-8").read().splitlines()
    L[43] = ("| REA MCP server | See `~/.kimi-code/config.toml:5` for the pointer-class check "
             "| nopin pointer | 2026-10-13 receipt |")
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")


def main():
    print("== pass 2 ==")
    D.rows = []
    # --- census: exact FAIL classes re-derived in range ---
    D.census_run("C4b-ptr-beyond-EOF", "before", "C4b", "UNRESOLVED->FAIL", 1, m_prov44_ptr_beyond)
    D.census_run("C4c-ptr-line-nopin", "before", "C4c", "STALE->FAIL", 1, m_prov44_ptr_nopin)
    D.census_run("C3j-marker-strip-json", "before", "C3j", "SCOPE-ERROR->FAIL", 1, D.m_marker, extra=("--json",))
    D.census_run("C4b7-ptr-beyond-h1h3", "h1h3", "C4b7", "UNRESOLVED->FAIL", 1, m_prov44_ptr_beyond)
    D.census_run("A14b-empty-skill-json", "h1h3", "A14b", "silent PASS? (attack)", None, D.m_skill_empty,
                 extra=("--json",))

    # --- probe: re-pinned dead table (digest matches) ---
    d = json.loads(json.dumps(json.load(open(PTABLE))))
    d["entries"][0]["must_match"] = "NEEDLE-THAT-CANNOT-MATCH-ANYTHING"
    json.dump(d, open(P + "/t-dead2.json", "w"))
    pex = json.load(open(PEXPECT))
    e = dict(pex); e["pointer_table"] = {"sha256": sha(P + "/t-dead2.json")}
    json.dump(e, open(P + "/e-dead2-repin.json", "w"))
    D.probe_run("P2-dead-default-repinned",
                ["--root", REPO, "--rev", "HEAD", "--table", P + "/t-dead2.json",
                 "--expected", P + "/e-dead2-repin.json"],
                "failed->1 per :42; default mode?", None)
    D.probe_run("P2s-dead-strict-repinned",
                ["--root", REPO, "--rev", "HEAD", "--table", P + "/t-dead2.json",
                 "--expected", P + "/e-dead2-repin.json", "--strict"],
                "failed->1 (strict)", 1)

    # --- probe: directory in place of the table ---
    os.makedirs(P + "/t-dir.json", exist_ok=True)
    D.probe_run("P9-table-is-dir",
                ["--root", REPO, "--rev", "HEAD", "--table", P + "/t-dir.json",
                 "--expected", P + "/e-pristine.json"],
                "could-not-evaluate->2", 2)

    # --- probe: pre-guard probe (e845c2b) against the landed expected -> selftest fail class ---
    old = subprocess.run(["git", "-C", REPO, "show",
                          "e845c2b:.ufo/gates/citation-drift/citation-drift-probe.py"],
                         capture_output=True, text=True)
    assert old.returncode == 0, old.stderr
    open(P + "/probe-pre-guard.py", "w").write(old.stdout)
    print("  pre-guard probe sha256 %s" % sha(P + "/probe-pre-guard.py")[:16])
    rc, out, err = D.run([sys.executable, P + "/probe-pre-guard.py", "--selftest", "--expected", PEXPECT])
    D.record("P10-oldprobe-newexpected-selftest", "probe-e845c2b", "selftest failed->1", 1, rc, out, err)
    with open(RV + "/logs/P10-oldprobe-newexpected-selftest.out", "w") as fh:
        fh.write(out + err)

    D.rows.append("-- pass 2 rows end --")
    print("\nWROTE %d rows" % len(D.rows))
    with open(RV + "/logs/matrix2.tsv", "w") as fh:
        fh.write("\n".join(D.rows) + "\n")


if __name__ == "__main__":
    main()
