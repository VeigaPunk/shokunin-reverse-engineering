#!/usr/bin/env python3
"""Over-tightening probe for tools/round-78/attack-gate.py scan_record.

Arms:
 P    minimal correct cell + authenticated receipt -> expect zero findings.
 S1   grammar-legal clauses judge_group certifies green (pristine 0,
      validate defect-free) under the genuine rule set.
 S2   the actual round-78 capability row text as drafted in the worktree
      SCORECARD.md (its parenthesised group ends in "validate defect-free").
 N1   authenticated receipt minus the instrument pin -> expect receipt_auth.
 N2   wrong claimed value -> expect value_mismatch.
"""
import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

S = pathlib.Path(sys.argv[1])
GATE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-78/attack-gate.py"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "ffcb47d13f0340f88397af6c8d2707a9554abab3"
GENUINE = {"receipt_auth", "qualified_atom", "near_miss_field",
           "negated_verdict", "unbound_verdict"}

spec = importlib.util.spec_from_file_location("gate", GATE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

ENV = {"PATH": "/usr/bin:/bin", "HOME": str(S),
       "GIT_AUTHOR_NAME": "probe", "GIT_AUTHOR_EMAIL": "probe@localhost",
       "GIT_COMMITTER_NAME": "probe", "GIT_COMMITTER_EMAIL": "probe@localhost"}


def git(*args):
    return subprocess.run(["git", "-C", str(S), *args], capture_output=True,
                          text=True, env=ENV)


INSTRUMENT = b"#!/usr/bin/env python3\n# probe instrument v1\nprint('probe')\n"
SCORECARD = """# probe record

## Capabilities

| id | owner | note | round | verdict |
|----|-------|------|-------|---------|
| R78-probe | ReviewerC1 | `.ufo/waves/round-78/l1/scores/probe.json` records ({group}) | 78 | ok |
"""


def build(group, receipt, receipt_bytes=None,
          receipt_path=".ufo/waves/round-78/l1/scores/probe.json",
          fetch_rev=None):
    if S.exists():
        shutil.rmtree(S)
    (S / "tools/probe").mkdir(parents=True)
    (S / "tools/probe/instrument.py").write_bytes(INSTRUMENT)
    target = S / receipt_path
    target.parent.mkdir(parents=True, exist_ok=True)
    (S / "SCORECARD.md").write_text(SCORECARD.format(group=group))
    target.write_bytes(receipt_bytes if receipt_bytes is not None
                       else json.dumps(receipt, indent=1).encode())
    subprocess.run(["git", "init", "--quiet", str(S)], env=ENV)
    top = git("rev-parse", "--show-toplevel").stdout.strip()
    assert pathlib.Path(top).resolve() == S.resolve(), f"toplevel {top} != {S}"
    git("add", "-A")
    git("commit", "--quiet", "-m", "probe: tree")
    c1 = git("rev-parse", "HEAD").stdout.strip()
    sha = hashlib.sha256(INSTRUMENT).hexdigest()
    if receipt is not None and isinstance(receipt.get("rev"), str):
        receipt["rev"] = c1
        if isinstance(receipt.get("instrument"), dict):
            receipt["instrument"]["sha256"] = sha
        target.write_text(json.dumps(receipt, indent=1))
        git("add", "-A")
        git("commit", "--quiet", "-m", "probe: receipt bound")
    if fetch_rev:
        proc = git("fetch", "--quiet", LANE, fetch_rev)
        assert proc.returncode == 0, proc.stderr
    head = git("rev-parse", "HEAD").stdout.strip()
    return c1, sha, head


def run_case(name, group, receipt, rules, receipt_bytes=None,
             receipt_path=".ufo/waves/round-78/l1/scores/probe.json",
             fetch_rev=None):
    c1, sha, head = build(group, receipt, receipt_bytes, receipt_path,
                          fetch_rev)
    res = gate.scan_record(str(S), head, set(rules))
    slim = {"case": name, "head": head,
            "in_scope_cells": res["in_scope_cells"],
            "groups": res["groups"], "bound_clauses": res["bound_clauses"],
            "mismatch_count": res["mismatch_count"],
            "findings": [{"rule": f.get("rule"), "clause": f.get("clause"),
                          "group": f.get("group"), "reason": f.get("reason")}
                         for f in res["findings"]]}
    print(json.dumps(slim, indent=1))
    return res


base_receipt = {"schema": "probe-receipt-v1", "rev": "@C1@",
                "instrument": {"path": "tools/probe/instrument.py",
                               "sha256": "@SHA@"}}

# P: minimal correct cell; clauses digit-first / atom / count forms only.
p_receipt = dict(base_receipt, mismatch_count=0,
                 atoms=[{"id": "D24_capability_rows", "ok": True}])
p = run_case("P positive minimal correct cell",
             "0 mismatches, D24 true", p_receipt, GENUINE)

# S1: clauses the selftest certifies green (green-pristine/green-validate)
#     under the genuine rule set that includes near_miss_field.
s1_receipt = dict(base_receipt, cases=0, validate={"defects": []})
s1 = run_case("S1 pristine+validate clauses, genuine rules",
              "pristine 0, validate defect-free", s1_receipt, GENUINE)

# S2: the worktree's drafted round-78 capability row 660 cell verbatim,
#     receipt bytes verbatim at the path the cell names, lane rev fetched
#     so receipt_auth can re-derive the pinned instrument blob.
row660 = ("`.ufo/waves/round-78/pre/c1-at-base.json` (fixtures_total 10, "
          "base_accepted 10, refused 10, validate defect-free)")
frozen_receipt_bytes = subprocess.run(
    ["git", "-C", LANE, "show", f"{FREEZE}:.ufo/waves/round-78/pre/c1-at-base.json"],
    capture_output=True).stdout
s2 = run_case("S2 drafted round-78 row cell verbatim", row660, None, GENUINE,
              receipt_bytes=frozen_receipt_bytes,
              receipt_path=".ufo/waves/round-78/pre/c1-at-base.json",
              fetch_rev="3e6b1efcad3a743913baa09f46427e5f8877a62b")

# N1: authenticated receipt shape but the instrument pin removed.
n1 = run_case("N1 instrument pin removed",
              "0 mismatches, D24 true",
              {"schema": "probe-receipt-v1", "rev": "@C1@", "mismatch_count": 0,
               "atoms": [{"id": "D24_capability_rows", "ok": True}]}, GENUINE)

# N2: every guard satisfied but the claimed value is wrong.
n2_receipt = dict(base_receipt, mismatch_count=0,
                  atoms=[{"id": "D24_capability_rows", "ok": True}])
n2 = run_case("N2 wrong claimed value", "1 mismatches, D24 true",
              n2_receipt, {"value_mismatch"})

ok = (p["findings"] == [] and p["mismatch_count"] == 0
      and p["groups"] == 1 and p["bound_clauses"] == 2
      and s1["findings"] == [] and s1["mismatch_count"] == 0
      and s2["findings"] == [] and s2["mismatch_count"] == 0
      and s2["groups"] == 1 and s2["bound_clauses"] == 4
      and n1["findings"] and n1["findings"][0]["rule"] == "receipt_auth"
      and n2["findings"] and n2["findings"][0]["rule"] == "value_mismatch")
print("PROBE-OK" if ok else "PROBE-FAIL")
sys.exit(0 if ok else 1)
