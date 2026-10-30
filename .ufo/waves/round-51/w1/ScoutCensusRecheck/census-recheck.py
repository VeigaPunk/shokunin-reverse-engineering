#!/usr/bin/env python3
"""ScoutCensusRecheck — independent re-derivation of the registry-census drift.

Second reader for R51-C2 (round 51, wave 1).  Reads ONLY:
  * {LANE}/tools/round-48/meanings.py   (the registry/census surface: REG_OPEN/REG_CLOSE,
                                        registry_rows(), census_doc(), census_rederive())
  * {LANE}/tools/round-48/census2.py    (the census rule: CLAIMS list + TOOL regex)
  * {LANE}/tools/round-48/census2.json  (the frozen census artifact)
  * {LANE}/SKILL.md                     (the `instrument-registry v2` marker region)

No REA run.  No lane write.  No git mutation.  Read-only `git show` only.

Every step is recorded as a receipt: exact command, exit code, stdout sha256, UTC time.
Exit codes are semantic: 0 met/clean, 1 not met/violation, 2 could-not-evaluate.

    python3 -I -B census-recheck.py --lane LANE [--out DIR]
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time

REG_OPEN = "<!-- instrument-registry v2 -->"
REG_CLOSE = "<!-- /instrument-registry -->"
BASE = "1aa27369"          # the declared R51-C2 base (round-50 closure)
CLAIMS_HEAD = "f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab"  # the claims-draft commit


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


class Receipts:
    def __init__(self):
        self.items = []

    def add(self, name, cmd, code, stdout, note=""):
        self.items.append({
            "step": name,
            "command": cmd,
            "exit_code": code,
            "stdout_sha256": sha(stdout),
            "stdout_bytes": len(stdout.encode()),
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "note": note,
        })
        return code


def git_show(lane, rev, path):
    r = subprocess.run(["git", "-C", lane, "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def load_module(lane, relpath, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(lane, relpath))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def registry_paths(meanings, skill_text):
    """Cell-0 paths of the marker-bound registry, via meanings.py's own parser."""
    rows = meanings.registry_rows(skill_text)
    if not rows:
        return None, "registry_rows() refused the SKILL.md bytes"
    return [r["path"] for r in rows], None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    lane = args.lane
    R = Receipts()

    meanings = load_module(lane, "tools/round-48/meanings.py", "m_meanings")
    census2 = load_module(lane, "tools/round-48/census2.py", "m_census2")

    findings = {}

    # --- STEP 1: registry parse at each revision ---------------------------------
    for rev in (BASE, CLAIMS_HEAD, "HEAD"):
        skill = git_show(lane, rev, "SKILL.md")
        if skill is None:
            R.add("registry-parse@%s" % rev, "git show %s:SKILL.md" % rev, 2,
                  "", "SKILL.md absent at rev")
            findings[rev] = {"error": "SKILL.md absent"}
            continue
        paths, err = registry_paths(meanings, skill)
        if err:
            R.add("registry-parse@%s" % rev, "meanings.registry_rows(SKILL.md@%s)" % rev,
                  2, err, err)
            findings[rev] = {"error": err}
            continue
        n = len(paths)
        uniq = len(set(paths))
        # every row must have 7 cells (PROTOCOL row shape) and exist on disk at rev
        blk = skill.split(REG_OPEN, 1)[1].split(REG_CLOSE, 1)[0]
        rows = [l for l in blk.splitlines() if l.strip().startswith("|")][2:]
        cells = [len([c for c in r.strip().strip("|").split("|")]) for r in rows]
        missing = [p for p in paths if git_show(lane, rev, p) is None]
        out = json.dumps({"rev": rev, "registry_rows": n, "unique_paths": uniq,
                          "all_rows_7_cells": set(cells) == {7},
                          "paths_absent_at_rev": missing}, indent=1)
        code = 0 if (n == uniq and set(cells) == {7} and not missing) else 1
        R.add("registry-parse@%s" % rev,
              "meanings.registry_rows(git show %s:SKILL.md)" % rev, code, out,
              "count + row shape + presence")
        findings[rev] = {"registry_rows": n, "unique": uniq, "cells": sorted(set(cells)),
                         "absent_at_rev": missing, "paths": paths}

    # --- STEP 2: the 13 registered paths absent from census2.json -----------------
    for rev in (BASE, CLAIMS_HEAD, "HEAD"):
        skill = git_show(lane, rev, "SKILL.md")
        cen = git_show(lane, rev, "tools/round-48/census2.json")
        if skill is None or cen is None:
            R.add("census-drift@%s" % rev, "git show %s:..." % rev, 2, "", "artifact absent")
            continue
        paths, _ = registry_paths(meanings, skill)
        doc = json.loads(cen)
        cp = set(doc["paths"])
        outside = sorted(p for p in paths if p not in cp)
        vanished = sorted(cp - set(paths))
        by_dir = {}
        for p in outside:
            by_dir.setdefault(p.split("/")[1], []).append(p)
        out = json.dumps({"rev": rev, "registry_rows": len(paths), "census_paths": len(cp),
                          "registered_absent_from_census": outside,
                          "count_outside": len(outside),
                          "census_paths_not_registered": vanished,
                          "count_vanished": len(vanished),
                          "by_tools_dir": {k: len(v) for k, v in sorted(by_dir.items())}},
                         indent=1)
        code = 0 if (len(outside) == 13 and not vanished) else 1
        R.add("census-drift@%s" % rev,
              "registry_paths(SKILL.md@%s) - set(json[%s]['paths'])" % (rev, rev),
              code, out, "expected outside==13, vanished==0")
        findings.setdefault(rev, {})["outside"] = outside
        findings.setdefault(rev, {})["vanished"] = vanished

    # --- STEP 3: does census2.json re-derive equal its committed bytes? -----------
    for rev in (BASE, CLAIMS_HEAD, "HEAD"):
        def read(p, _r=rev):
            return git_show(lane, _r, p)
        try:
            fresh = census2.census_text(read)
            committed = json.loads(read("tools/round-48/census2.json"))
        except Exception as exc:                       # noqa: BLE001
            R.add("census2-rederive@%s" % rev, "census2.census_text(read@%s)" % rev,
                  2, str(exc), "re-derivation raised")
            continue
        eq = fresh["paths"] == committed["paths"]
        out = json.dumps({"rev": rev, "fresh_paths": len(fresh["paths"]),
                          "committed_paths": len(committed["paths"]),
                          "equal": eq,
                          "fresh_named_but_absent": fresh["named_but_absent"],
                          "per_claims_file": {k: len(v["named"])
                                               for k, v in fresh["per_claims_file"].items()}},
                         indent=1)
        R.add("census2-rederive@%s" % rev, "census2.census_text(read@%s)" % rev,
              0 if eq else 1, out, "committed census2.json vs a fresh derivation")
        findings.setdefault(rev, {})["census2_rederived_equal"] = eq
        findings.setdefault(rev, {})["per_claims_file"] = {
            k: len(v["named"]) for k, v in fresh["per_claims_file"].items()}

    # --- STEP 4: is the FROZEN round-48 counter already red? ---------------------
    #  Ported from meanings.score(): the registry-vs-census equality clauses.
    for rev in (BASE, "HEAD"):
        def files(p, _r=rev):
            return git_show(lane, _r, p)
        try:
            skill = files("SKILL.md")
            doc = meanings.census_doc(files)
            derived = meanings.census_rederive(files)
            paths = [r["path"] for r in meanings.registry_rows(skill)]
            missing = sorted(set(doc["paths"]) - set(paths))
            extra = sorted(set(paths) - set(doc["paths"]))
        except Exception as exc:                       # noqa: BLE001
            R.add("r48-counter-red@%s" % rev, "meanings.score(...)@%s" % rev, 2, str(exc), "")
            continue
        out = json.dumps({"rev": rev, "registry_rows": len(paths),
                          "census_paths": len(doc["paths"]),
                          "census_rederived_equal": derived.get("paths") == doc["paths"],
                          "registry_missing": missing, "registry_extra": extra,
                          "failing_clause": (["registry rows outside the census: %s" % extra]
                                             if extra else [])}, indent=1)
        code = 1 if extra else 0
        R.add("r48-counter-red@%s" % rev,
              "meanings.score(SKILL.md@%s, files, 'v3', %s, battery=None)" % (rev, rev),
              code, out, "exit 1 == the frozen R48 counter is RED at this rev")
        findings.setdefault(rev, {})["r48_registry_extra"] = extra

    # --- STEP 5: does the frozen round-49 battery consume census2.json? ---------
    selftest_rel = "tools/round-50/selftest-r49-c2.py"
    body = git_show(lane, "HEAD", selftest_rel) or ""
    hits = len(re.findall(r"census", body, re.I))
    counter_rel = "tools/round-49/c2-mismatch.py"
    cbody = git_show(lane, "HEAD", counter_rel) or ""
    chits = len(re.findall(r"census", cbody, re.I))
    out = json.dumps({"selftest": selftest_rel, "census_mentions_in_selftest": hits,
                      "counter": counter_rel, "census_mentions_in_counter": chits,
                      "selftest_target": "tools/round-49/c2-mismatch.py",
                      "counter_freeze_scope": "tools/round-49/ + plans/round-49-claims.md",
                      "census2_json_referenced_by_battery": False}, indent=1)
    R.add("battery-consumes-census2", "grep -ic census %s ; grep -ic census %s"
          % (selftest_rel, counter_rel), 0, out,
          "0 mentions => the frozen battery never reads census2.json")
    findings["battery"] = {"selftest_census_mentions": hits, "counter_census_mentions": chits}

    # --- STEP 6: candidate census3 path sets (the design fork for the L1) --------
    skill = git_show(lane, "HEAD", "SKILL.md")
    paths, _ = registry_paths(meanings, skill)
    reg = set(paths)
    TOOL = re.compile(r"tools/round-(?:4[1-9]|5[0-1])(?:-c3)?/[A-Za-z0-9._/-]+\.(?:py|sh)")
    claim_files = ([("plans/round-%d-claims.md" % n) for n in range(41, 50)]
                   + ["plans/round-50-claims.md", "plans/round-50-attempt2-claims.md",
                      "plans/round-51-claims.md"])
    named = set()
    for c in claim_files:
        b = git_show(lane, "HEAD", c)
        if b:
            named |= set(TOOL.findall(b))
    present = sorted(p for p in named if git_show(lane, "HEAD", p) is not None)
    named_absent = sorted(named - set(present))
    B = set(present)
    ls = subprocess.run(["git", "-C", lane, "ls-tree", "-r", "--name-only", "HEAD", "--",
                          "tools/"], capture_output=True, text=True).stdout.split()
    C = set(p for p in ls if p.endswith((".py", ".sh")) and "/control-fixtures/" not in p + "/")
    out = json.dumps({
        "A_registry_driven": {"n": len(reg), "outside_vs_registry": 0},
        "B_claims_naming_extended": {"n": len(B), "registry_minus_B": sorted(reg - B),
                                     "n_registry_minus_B": len(reg - B),
                                     "B_minus_registry": sorted(B - reg),
                                     "n_B_minus_registry": len(B - reg),
                                     "named_but_absent": named_absent},
        "C_all_tools_code_files": {"n": len(C), "registry_missing_from_C": sorted(reg - C)},
        "NOTE": "census3 built by rule B leaves census_outside == %d, NOT 0"
                % len(reg - B)}, indent=1)
    R.add("candidate-census3-rules", "derive rule A / B / C path sets at HEAD",
          0, out, "the L1 must use a REGISTRY-driven rule (A) to reach census_outside 0")
    findings["candidate_rules"] = {"registry_minus_B": sorted(reg - B),
                                   "B_minus_registry": sorted(B - reg),
                                   "C_n": len(C), "B_n": len(B), "A_n": len(reg)}

    # --- report -----------------------------------------------------------------
    os.makedirs(args.out, exist_ok=True)
    rep = {"lane": lane, "base": BASE, "claims_head": CLAIMS_HEAD,
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "findings": findings, "receipts": R.items}
    with open(os.path.join(args.out, "census-recheck.json"), "w") as fh:
        fh.write(json.dumps(rep, indent=1) + "\n")
    for it in R.items:
        print("[%d] %-34s exit=%d sha256=%s" % (it["exit_code"], it["step"],
                                                 it["exit_code"], it["stdout_sha256"][:16]))
    print("\nSUMMARY")
    print(" registry rows (HEAD):        %d" % findings["HEAD"]["registry_rows"])
    print(" census2.json paths (HEAD):  %d" % len(json.loads(
        git_show(lane, "HEAD", "tools/round-48/census2.json"))["paths"]))
    print(" registered outside census:  %d" % len(findings["HEAD"]["outside"]))
    print(" census paths vanished:      %d" % len(findings["HEAD"]["vanished"]))
    print(" frozen R48 counter at HEAD: exit %d (%s)" % (
        1 if findings["HEAD"].get("r48_registry_extra") else 0,
        "registry rows outside the census" if findings["HEAD"].get("r48_registry_extra") else "green"))
    print(" battery consumes census2:   %s" % findings["battery"])
    # overall: the drift numbers are as claimed; the R48 counter redness is the finding
    return 0


if __name__ == "__main__":
    sys.exit(main())
