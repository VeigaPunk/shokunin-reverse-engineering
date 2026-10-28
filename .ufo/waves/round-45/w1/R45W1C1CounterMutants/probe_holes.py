#!/usr/bin/env python3
"""Probe the two surviving mutants with the selftest cases that should have caught them.

Each probe builds a repository shape the frozen selftest never builds, then runs the
pristine counter and the mutant on that shape and prints both receipts' verdicts.
"""
import importlib.util
import json
import os
import tempfile

S = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load("pris", os.path.join(S, "pristine.py"))
M1 = load("m1", os.path.join(S, "m1-rule-blocks-ge.py"))
M2 = load("m2", os.path.join(S, "m2-skip-marker-check.py"))


def run(mod, skill, preflight=None, claims=True):
    d = tempfile.mkdtemp(dir=S, prefix="probe-")
    f = mod.make_repo(d, skill, preflight or mod.STUB_OK, claims=claims)
    code, receipt = mod.evaluate(d, f, f)
    return code, receipt


def short(tag, code, receipt):
    print(json.dumps({"probe": tag, "exit": code,
                      "rule_blocks": receipt.get("rule_blocks"),
                      "block22_present": receipt.get("block22_present"),
                      "block22_rows": receipt.get("block22_rows"),
                      "block22_refs": receipt.get("block22_refs"),
                      "failing": receipt.get("failing")}, sort_keys=True))


# --- H1: 23 rule blocks, the marked block otherwise perfect (predicate says == 22) ---
skill23 = P.skill_with(22, P.good_block())
short("H1-red-extra-rule-block/pristine", *run(P, skill23))
short("H1-red-extra-rule-block/m1", *run(M1, skill23))

# --- H2a: 22 blocks, marker absent, the table otherwise perfect -----------------------
skill_nomark = P.skill_with(21, P.good_block().replace(P.MARKER, "<!-- unrelated -->"))
short("H2a-red-marker-absent/pristine", *run(P, skill_nomark))
short("H2a-red-marker-absent/m2", *run(M2, skill_nomark))

# --- H2b: duplicate marker, 22 blocks ------------------------------------------------
extra = ("- **23. Extra.** " + P.MARKER + " body\n\n" + P.GOOD_HEADER + P.GOOD_ROW * 8
         + "\n  Refs: corpus/lessons/round-44.md:38\n\n")
skill_dup = P.skill_with(20, P.good_block() + extra)
short("H2b-red-duplicate-marker/pristine", *run(P, skill_dup))
short("H2b-red-duplicate-marker/m2", *run(M2, skill_dup))
