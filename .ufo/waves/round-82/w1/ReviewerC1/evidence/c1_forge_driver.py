#!/usr/bin/env python3
"""ReviewerC1 r82: predicate-level forged-state battery against pinned gate bytes.

Loads the gate module from a scratch copy verified byte-identical to the lane
instrument, builds counterexample states by minimally mutating the genuine
landing receipt (fetched from lane git at the measured rev), and scores each
with the gate's own conjunction()/frozen_killed().
"""
import hashlib
import importlib.util
import json
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r82/ReviewerC1"
REV = "eb227c4694e16cb8fae74df0eea2f07643b46124"
GATE = LANE + "/tools/round-82/conjunction-gate.py"
GATE_COPY = SCRATCH + "/work/conjunction-gate.copy.py"
LANDING = ".ufo/waves/round-81/l1/scores/c2-at-landing.json"
GATE_SHA = "6155a1ffa7564acffc755caeafbe450f5b080d00526edf4bef247444ad04e1af"

ORIG = [
    "green-strict-refuses-every-red",
    "green-strict-refuses-no-green",
    "red-loose-accepts-reds",
    "red-refuse-all-fails-greens",
    "red-duplicate-without-signal",
    "red-duplicate-signal-with-collapsed-count",
    "green-validate-consistent",
    "red-validate-tampered-false-greens",
    "red-validate-control-not-reproducing",
]


def landing():
    b = subprocess.check_output(["git", "-C", LANE, "show", f"HEAD:{LANDING}"])
    import copy
    return copy.deepcopy(json.loads(b.decode("utf-8")))


def load_gate():
    data = open(GATE, "rb").read()
    assert hashlib.sha256(data).hexdigest() == GATE_SHA, "gate digest drift"
    open(GATE_COPY, "wb").write(data)
    spec = importlib.util.spec_from_file_location("conj_gate", GATE_COPY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def idx(cases, name):
    return next(i for i, r in enumerate(cases)
                if isinstance(r, dict) and r.get("case") == name)


def main():
    g = load_gate()
    results = []

    def score(name, expect, receipt):
        ok, defects = g.conjunction(receipt)
        frozen = g.frozen_killed(receipt)
        results.append({"state": name, "expected": expect,
                        "conjunction_ok": ok, "defects": defects,
                        "frozen_killed": frozen,
                        "recorded_killed": receipt.get("killed"),
                        "recorded_ok": receipt.get("ok"),
                        "recorded_survivors": receipt.get("survivors"),
                        "recorded_mutants": receipt.get("mutants")})

    base = landing()

    # ---- counterexamples -------------------------------------------------
    ce1 = landing()
    ce1["pristine"]["exit"] = False
    ce1["pristine"]["summary"] = [11, False]
    ce1["survivors"] = False
    ce1["mutants"] = True
    score("CE1-bool-for-int", "accepted (defects [])", ce1)

    ce2a = landing()
    ce2a["pristine"]["summary"] = [1, 0]
    score("CE2a-summary-cases-1-of-11-emitted", "accepted (defects [])", ce2a)

    ce2b = landing()
    ce2b["pristine"]["summary"] = [0, 0]
    score("CE2b-summary-cases-0-of-11-emitted", "accepted (defects [])", ce2b)

    ce3 = landing()
    pc = ce3["pristine"]["cases"]
    pc[idx(pc, "record-fixture-committed-duplicate")] = dict(
        pc[idx(pc, "green-validate-consistent")])
    score("CE3-duplicate-original-row-10-distinct", "accepted (defects [])", ce3)

    ce4 = landing()
    pc = ce4["pristine"]["cases"]
    ce4["pristine"]["cases"] = [r for r in pc
                                if r.get("case") != "record-fixture-committed-duplicate"]
    ce4["pristine"]["cases"].append({"pass": True})
    score("CE4-floor-padded-by-caseless-dict", "accepted (defects [])", ce4)

    ce5 = landing()
    ce5["killed"] = 0
    ce5["ok"] = False
    score("CE5-recorded-killed-0-contradicts-rederived", "accepted (defects [])", ce5)

    ce5b = landing()
    ce5b["mutant"]["exit"] = 0
    ce5b["killed"] = 1
    ce5b["ok"] = True
    score("CE5b-recorded-killed-1-with-mutant-exit-0",
          "refused only via frozen_rule_not_killed; recorded-field contradiction unflagged",
          ce5b)

    # ---- negative controls (gate must refuse) ---------------------------
    nc1 = landing()
    nc1["pristine"]["cases"] = [
        r for r in nc1["pristine"]["cases"]
        if r.get("case") != "green-strict-refuses-no-green"]
    score("NC1-missing-original", "refused original_cases_absent", nc1)

    nc2 = landing()
    nc2["mutant"]["cases"] = nc2["mutant"]["cases"] + [
        {"case": "record-fixture-committed-clean", "pass": False}]
    score("NC2-duplicate-detector", "refused detector_absent_or_passing", nc2)

    nc3 = landing()
    nc3["pristine"]["summary"] = [11, 1]
    score("NC3-summary-failure-1", "refused pristine_failures_nonzero", nc3)

    nc4 = landing()
    nc4["pristine"]["cases"] = nc4["pristine"]["cases"][:10]
    score("NC4-ten-real-cases", "refused pristine_cases_below_floor", nc4)

    out = {"gate_sha256": GATE_SHA, "landing_rev_field": base.get("rev"),
           "measured_rev": REV, "results": results}
    path = SCRATCH + "/evidence/c1-forged-states.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
