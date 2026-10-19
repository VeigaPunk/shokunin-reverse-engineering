#!/usr/bin/env python3
"""RV-10 exit-code conformance driver (arc3-loop1-round2, chain c2).

Fixture matrix over the two instruments of the c2 chain. Every run is a scratch
copy; the repo gate files are read-only inputs. Records per fixture:
exit code, verdict line, traceback presence.

Declared maps under test
  census .ufo/gates/c1-census-v10.py:122   "Exit 0 PASS, 1 FAIL, 2 anchor failure"
  probe  .ufo/gates/citation-drift/citation-drift-probe.py:42
         "exit 0 clean, 1 failed, 2 could-not-evaluate" (+ --strict split)
"""
import json, os, shutil, subprocess, sys

RV = "/var/tmp/rv10"
REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = RV + "/trees/base"
CASES = RV + "/cases"
LOGD = RV + "/logs"
HOME_REAL = os.environ.get("HOME", "/home/vgpnk")
FAKEHOME = RV + "/fakehome"
PROBE = REPO + "/.ufo/gates/citation-drift/citation-drift-probe.py"
PTABLE = REPO + "/.ufo/gates/citation-drift/pointer-table.json"
PEXPECT = REPO + "/.ufo/gates/citation-drift/expected.json"

CENSUS = {
    "before": RV + "/tool/census-before.py",
    "h1h3": RV + "/tool/census-h1h3.py",      # projection of the round-1 H1+H3 patch texts
    "blind": RV + "/tool/census-blind.py",    # rebuilt H3 injection on the current revision
    "blind-h1h3": RV + "/tool/census-blind-h1h3.py",
    "blindver": RV + "/tool/census-blindver.py",          # VER needle only (partial blindness)
    "blindver-h1h3": RV + "/tool/census-blindver-h1h3.py",
}

rows = []


def sha256(path):
    import hashlib
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(cmd, env=None, timeout=20):
    e = dict(os.environ)
    if env:
        e.update(env)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as exc:
        return "TIMEOUT", (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or ""), ""


def last_line(out, prefixes):
    tail = [l for l in out.splitlines() if l.startswith(prefixes)]
    return " | ".join(tail[-2:]) if tail else (out.strip().splitlines() or ["<no output>"])[-1]


def record(fixture, tool, declared, expected, rc, out, err):
    tb = "TRACEBACK" if "Traceback" in err else ""
    verdict = last_line(out, ("VERDICT", "ANCHOR-FAIL", "SCOPE-ERRORS", "G2 ", "CITATION_DRIFT_VERDICT", "CITATION_DRIFT_SELFTEST"))
    ok = "OK" if rc == expected else ("N/A" if expected is None else "MISMATCH")
    line = "%-28s %-12s %-6s %-8s %-6s %s %s" % (fixture, tool, declared, rc, ok, tb, verdict[:110])
    print(line)
    rows.append(line)


def fresh(case):
    d = os.path.join(CASES, case)
    if os.path.exists(d):
        shutil.rmtree(d)
    shutil.copytree(BASE, d)
    return d


def edit(path, old, new):
    txt = open(path, encoding="utf-8").read()
    assert old in txt, "needle %r absent from %s" % (old[:50], path)
    open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))


# ---- mutations ------------------------------------------------------------
def m_pin(case):    edit(case + "/SKILL.md", "rea-agents@6.5.0", "rea-agents@6.3.0")
def m_append(case):
    open(case + "/SCORECARD.md", "a").write("\nThe kimi client remains pinned to rea-agents@6.3.0 for the current round.\n")
def m_marker(case): edit(case + "/PROVINCE.md", "verified on this host 2026-10-13", "verified on this host [marker removed]")
def m_shelter(case):
    p = case + "/SCORECARD.md"
    L = open(p, encoding="utf-8").read().splitlines()
    L.insert(800, "Current status: kimi runs rea-agents@6.3.0 as of this round.")
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
def m_ptr(case):
    open(case + "/SCORECARD.md", "a").write("\nSee ~/.kimi-code/config.toml:9999 for the pointer class check.\n")
def m_absent_skill(case): os.remove(case + "/SKILL.md")
def m_absent_sc(case): os.remove(case + "/SCORECARD.md")
def m_absent_prov(case): os.remove(case + "/PROVINCE.md")
def m_skill_dir(case): os.remove(case + "/SKILL.md"); os.mkdir(case + "/SKILL.md")
def m_skill_fifo(case): os.remove(case + "/SKILL.md"); os.mkfifo(case + "/SKILL.md")
def m_skill_empty(case): open(case + "/SKILL.md", "w").close()
def m_sc_empty(case): open(case + "/SCORECARD.md", "w").close()
def m_skill_chmod0(case):
    os.chmod(case + "/SKILL.md", 0)


def census_run(name, toolkey, case, declared, expected, mutate=None, root=None, home=None,
               extra=(), timeout=20):
    c = fresh(case)
    if mutate:
        mutate(c)
    env = {"HOME": home} if home else None
    rc, out, err = run([sys.executable, CENSUS[toolkey], "--root", root or c] + list(extra),
                       env=env, timeout=timeout)
    if mutate is m_skill_chmod0:
        os.chmod(c + "/SKILL.md", 0o644)
    record(case + "[" + toolkey + "]", os.path.basename(CENSUS[toolkey]), declared, expected, rc, out, err)
    with open(os.path.join(LOGD, "%s.%s.out" % (case, toolkey)), "w") as fh:
        fh.write("$ %s %s --root %s\nEXIT=%s\n--stderr--\n%s--stdout--\n%s"
                 % (sys.executable, CENSUS[toolkey], root or c, rc, err, out))
    return rc


def probe_run(name, args, declared, expected, table=None, expected_path=None):
    cmd = [sys.executable, PROBE] + args
    rc, out, err = run(cmd)
    record(name, "probe", declared, expected, rc, out, err)
    with open(os.path.join(LOGD, name + ".out"), "w") as fh:
        fh.write("$ %s\nEXIT=%s\n--stderr--\n%s--stdout--\n%s" % (" ".join(cmd), rc, err, out))
    return rc


def main():
    os.makedirs(CASES, exist_ok=True)
    os.makedirs(LOGD, exist_ok=True)
    for p in (FAKEHOME + "/.config/devin", FAKEHOME + "/.omp/agent", FAKEHOME + "/.kimi-code"):
        os.makedirs(p, exist_ok=True)
    open(FAKEHOME + "/.config/devin/mcp_config.json", "w").write('{"mcpServers": {}}\n')
    open(FAKEHOME + "/.omp/agent/mcp.json", "w").write('{"mcpServers": {}}\n')
    open(FAKEHOME + "/.kimi-code/config.toml", "w").write('# no rea-agents pin\n')

    print("== instruments ==")
    for k, v in CENSUS.items():
        print("  %-12s %s  %s" % (k, sha256(v)[:16], v))
    print("  probe        %s  %s" % (sha256(PROBE)[:16], PROBE))
    print()
    hdr = "%-28s %-12s %-6s %-8s %-6s %-10s %s" % ("fixture", "tool", "class", "exit", "match", "stderr", "verdict")
    print(hdr)
    rows.append(hdr)

    # ---- census: declared PASS / FAIL classes -----------------------------
    print("\n-- census: clean / FAIL classes (declared 0 vs 1) --")
    rows.append("-- census: clean / FAIL classes --")
    census_run("C0-baseline", "before", "C0", "PASS", 0)
    census_run("C1-false-current-pin", "before", "C1", "STALE->FAIL", 1, m_pin)
    census_run("C2-undeclared-append", "before", "C2", "UNDECLARED->FAIL", 1, m_append)
    census_run("C3-marker-strip", "before", "C3", "SCOPE-ERROR->FAIL", 1, m_marker)
    census_run("C4-ptr-out-of-range", "before", "C4", "UNRESOLVED->FAIL", 1, m_ptr)
    census_run("C5-dated-shelter", "before", "C5", "DATED-in-range (fail-open, refused)", 0, m_shelter)

    print("\n-- census: anchor class (declared 2) --")
    rows.append("-- census: anchor class --")
    census_run("C6-anchor-fail", "before", "C6", "ANCHOR-FAIL", 2, None, home=FAKEHOME)
    census_run("C7-anchor-fail-json", "before", "C7", "ANCHOR-FAIL", 2, None, home=FAKEHOME, extra=("--json",))

    print("\n-- census: H1 absent/unreadable fixtures (declared could-not-evaluate) --")
    rows.append("-- census: H1 absent/unreadable fixtures --")
    census_run("C8-skill-absent", "before", "C8", "declared non-zero (H1)", None, m_absent_skill)
    census_run("C9-scorecard-absent", "before", "C9", "declared non-zero (H1)", None, m_absent_sc)
    census_run("C10-province-absent", "before", "C10", "declared non-zero (H1)", None, m_absent_prov)
    census_run("C11-root-absent", "before", "C11", "declared non-zero (H1)", None, None,
               root=RV + "/does-not-exist")
    census_run("C12-skill-is-dir", "before", "C12", "declared non-zero (H1)", None, m_skill_dir)
    census_run("C13-skill-chmod000", "before", "C13", "declared non-zero (H1)", None, m_skill_chmod0)
    census_run("C14-skill-empty-file", "before", "C14", "declared non-zero (H1)", None, m_skill_empty)
    census_run("C15-scorecard-empty-file", "before", "C15", "declared non-zero (H1)", None, m_sc_empty)
    census_run("C16-skill-fifo", "before", "C16", "declared non-zero (H1)", None, m_skill_fifo, timeout=5)

    print("\n-- census: H3 blind-instrument fixtures (declared could-not-evaluate) --")
    rows.append("-- census: H3 blind-instrument fixtures --")
    census_run("C17-blind-needles", "blind", "C17", "declared non-zero (H3)", None)
    census_run("C18-partial-blind-ver", "blindver", "C18", "declared non-zero (H3)", None)

    print("\n-- census: invocation class (out of the declared map) --")
    rows.append("-- census: invocation class --")
    census_run("C19-badflag", "before", "C19", "not in map (argparse)", None, None, extra=("--bogus",))
    census_run("C20-help", "before", "C20", "not in map (argparse)", 0, None, extra=("-h",))

    print("\n-- census: mode parity (--json vs text) --")
    rows.append("-- census: mode parity --")
    census_run("C21-json-stale", "before", "C21", "STALE->FAIL", 1, m_pin, extra=("--json",))
    census_run("C22-json-clean", "before", "C22", "PASS", 0, None, extra=("--json",))

    # ---- census: after-state projection (H1+H3 patch texts applied) -------
    print("\n-- census: after-projection (H1+H3 patch texts applied to scratch copy) --")
    rows.append("-- census: after-projection --")
    census_run("A0-baseline", "h1h3", "A0", "PASS", 0)
    census_run("A8-skill-absent", "h1h3", "A8", "declared non-zero (H1)", 1, m_absent_skill)
    census_run("A13-skill-chmod000", "h1h3", "A13", "declared non-zero (H1)", 1, m_skill_chmod0)
    census_run("A14-skill-empty-file", "h1h3", "A14", "declared non-zero (H1)?", None, m_skill_empty)
    census_run("A12-skill-is-dir", "h1h3", "A12", "declared non-zero (H1)", 1, m_skill_dir)
    census_run("A17-blind-needles", "blind-h1h3", "A17", "declared non-zero (H3)", 1)
    census_run("A18-partial-blind-ver", "blindver-h1h3", "A18", "declared non-zero (H3)?", None)
    census_run("A6-anchor-fail", "h1h3", "A6", "ANCHOR-FAIL", 2, None, home=FAKEHOME)
    census_run("A1-false-current-pin", "h1h3", "A1", "STALE->FAIL", 1, m_pin)

    # ---- probe: declared 0/1/2 classes ------------------------------------
    print("\n-- probe: declared 0/1/2 classes --")
    rows.append("-- probe: 0/1/2 classes --")
    P = RV + "/probe"
    j = lambda p, o: json.dump(o, open(p, "w"))
    pt = json.load(open(PTABLE))
    pex = json.load(open(PEXPECT))
    # pristine copies
    shutil.copy(PTABLE, P + "/t-pristine.json")
    shutil.copy(PEXPECT, P + "/e-pristine.json")
    # dead-citation table
    d = json.loads(json.dumps(pt)); d["entries"][0]["must_match"] = "NEEDLE-THAT-CANNOT-MATCH-ANYTHING"
    j(P + "/t-dead.json", d)
    exp_clean = dict(pex)
    j(P + "/e-pinned-pristine.json", exp_clean)
    exp_dead = dict(pex)  # same pinned digest -> tampered
    j(P + "/e-pinned-dead-table.json", exp_dead)
    # unpinned baseline (no pointer_table key)
    e_unpin = dict(pex); e_unpin.pop("pointer_table", None)
    j(P + "/e-unpinned.json", e_unpin)
    # empty table, digest re-pinned to it
    empty = {"entries": []}
    j(P + "/t-empty.json", empty)
    e_empty = dict(pex); e_empty["pointer_table"] = {"sha256": sha256(P + "/t-empty.json")}
    j(P + "/e-empty-pinned.json", e_empty)

    probe_run("P0-selftest", ["--selftest", "--expected", PEXPECT], "13/13 declared cases", 0)
    probe_run("P1-clean-default", ["--root", REPO, "--rev", "HEAD"], "clean->0 (reported)", 0)
    probe_run("P1s-clean-strict", ["--root", REPO, "--rev", "HEAD", "--strict"], "clean->0", 0)
    probe_run("P2-dead-default", ["--root", REPO, "--rev", "HEAD", "--table", P + "/t-dead.json",
                                  "--expected", P + "/e-pinned-dead-table.json"],
              "failed->1 per :42; default mode?", None)
    probe_run("P2s-dead-strict", ["--root", REPO, "--rev", "HEAD", "--table", P + "/t-dead.json",
                                  "--expected", P + "/e-pinned-dead-table.json", "--strict"],
              "failed->1", 1)
    probe_run("P3-table-tampered", ["--root", REPO, "--rev", "HEAD", "--table", P + "/t-dead.json",
                                    "--expected", P + "/e-pinned-pristine.json"],
              "could-not-evaluate->2", 2)
    probe_run("P4-table-absent", ["--root", REPO, "--rev", "HEAD", "--table", P + "/nope.json",
                                  "--expected", P + "/e-pristine.json"], "could-not-evaluate->2", 2)
    probe_run("P5-table-unpinned", ["--root", REPO, "--rev", "HEAD", "--table", P + "/t-pristine.json",
                                    "--expected", P + "/e-unpinned.json"], "could-not-evaluate->2", 2)
    probe_run("P6-rev-unresolvable", ["--root", REPO, "--rev",
                                      "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"],
              "could-not-evaluate->2", 2)
    probe_run("P7-table-empty-repinned", ["--root", REPO, "--rev", "HEAD", "--table", P + "/t-empty.json",
                                          "--expected", P + "/e-empty-pinned.json"], "clean->0", 0)
    probe_run("P8-badflag", ["--bogus"], "not in map (argparse)", None)

    print("\nWROTE %d rows" % len(rows))
    with open(LOGD + "/matrix.tsv", "w") as fh:
        fh.write("\n".join(rows) + "\n")


if __name__ == "__main__":
    main()
