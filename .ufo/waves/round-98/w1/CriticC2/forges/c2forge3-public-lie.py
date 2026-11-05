#!/usr/bin/env python3
"""c2forge3-public-lie.py - FORGE C2-3 (critic, round-98 falsification seat).

A counter that never scores anything: its public command exits 0 and prints
`selfverify ok=True reasons=0` without running the battery and without writing
any receipt.  count_problems is v8's honest fourteen-key schema check.
The predicate should certify this only if its public leg is an honor system.
"""
import argparse
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V8 = os.path.join(HERE, "stop-boundary-repair-battery-v8.py")
V3 = os.path.join(HERE, "..", "round-93", "stop-boundary-repair-battery-v3.py")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v8 = _load(V8, "c2forge3_v8")
v3 = _load(V3, "c2forge3_v3")
count_problems = v8.count_problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--work")
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--expect")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    ap.parse_args(argv)
    # FORGE C2-3 (critic): the lie - no battery, no receipt, claimed green.
    print("selfverify ok=True reasons=0")
    print("%s met True exit 0" % v3.FROZEN_LABEL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
