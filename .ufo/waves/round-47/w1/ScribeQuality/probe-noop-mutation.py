#!/usr/bin/env python3
"""ScribeQuality probe — is a no-op mutation counted as a scored v2 forgery?

Reads tools/round-47/exact.py (frozen, unmodified on disk) at a given --rev, imports it,
and calls run_battery twice: once with the frozen MUTATIONS list, once with entry 0
(`substring-arm`) replaced in memory by an identity mutation that changes nothing and
records no override. Nothing on the lane tree is written; the fixtures are one-commit git
repos under $TMPDIR that run_battery creates and deletes itself.

Prints a JSON receipt: the frozen battery, the no-op battery, and the score() verdict on
the no-op battery (the frozen clause 9 tuple is what score() compares).
"""
import argparse
import json
import os
import sys
import tempfile
from hashlib import sha256

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
TOOLS = os.path.join(LANE, "tools", "round-47")
sys.path.insert(0, TOOLS)
import exact  # noqa: E402
import gate  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", required=True)
    ap.add_argument("--json-out")
    a = ap.parse_args()
    rev = a.rev
    scratch = tempfile.mkdtemp(dir=os.environ.get("TMPDIR") or None, prefix="sq-noop-")

    skill = gate.show(LANE, rev, "SKILL.md")
    files = lambda p: gate.show(LANE, rev, p)  # noqa: E731
    out = {"rev": rev, "exact_sha256": sha256(open(exact.__file__, "rb").read()).hexdigest(),
           "mutations_sha256": exact.MUT_DIGEST}

    frozen = exact.run_battery(LANE, rev, scratch)
    out["frozen_battery"] = {k: frozen.get(k) for k in
                             ("forgeries_total", "v2_green", "v3_green",
                              "genuine_green", "crash")}
    out["frozen_fixtures"] = [{"name": f.get("name"), "v2_exit": f.get("v2_exit"),
                               "v3_exit": f.get("v3_exit"), "error": f.get("error")}
                              for f in frozen.get("fixtures", [])]
    c0, r0 = exact.score(skill, files, "v3", rev, battery=frozen)
    out["frozen_score"] = {"exit": c0, "met_target": r0.get("met_target"),
                           "failing": r0.get("failing")}

    # the defect under test: one mutation that constructs nothing and changes nothing
    def identity(block, spec):
        return block, {}

    patched = [("substring-arm", identity)] + list(exact.MUTATIONS[1:])
    saved = exact.MUTATIONS
    exact.MUTATIONS = patched
    try:
        noop = exact.run_battery(LANE, rev, scratch)
    finally:
        exact.MUTATIONS = saved
    out["noop_battery"] = {k: noop.get(k) for k in
                           ("forgeries_total", "v2_green", "v3_green",
                            "genuine_green", "crash")}
    out["noop_fixtures"] = [{"name": f.get("name"), "v2_exit": f.get("v2_exit"),
                             "v3_exit": f.get("v3_exit"), "error": f.get("error")}
                            for f in noop.get("fixtures", [])]
    exact.MUTATIONS = patched
    try:
        c1, r1 = exact.score(skill, files, "v3", rev, battery=noop)
    finally:
        exact.MUTATIONS = saved
    out["noop_score"] = {"exit": c1, "met_target": r1.get("met_target"),
                         "failing": r1.get("failing")}
    print(json.dumps(out, indent=1))
    if a.json_out:
        with open(a.json_out, "w") as fh:
            json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
