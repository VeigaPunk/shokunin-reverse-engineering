#!/usr/bin/env python3
"""m5 sub-probe: under the mutant, `red-interpreter-fails` still exits 1, but for the
wrong reason (selftest never ran). Show the receipt field that distinguishes it."""
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
M5 = load("m5", os.path.join(S, "m5-skip-selftest.py"))

for tag, mod in (("pristine", P), ("m5", M5)):
    d = tempfile.mkdtemp(dir=S, prefix="probe5-")
    f = mod.make_repo(d, mod.skill_with(21, mod.good_block()), mod.STUB_RED)
    code, receipt = mod.evaluate(d, f, f)
    print(json.dumps({"probe": "red-interpreter-fails/" + tag, "exit": code,
                      "preflight_selftest": receipt.get("preflight_selftest"),
                      "failing": receipt.get("failing")}, sort_keys=True))
