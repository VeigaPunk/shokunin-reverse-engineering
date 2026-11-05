#!/usr/bin/env python3
"""SentinelTools probe (scratch-only, not a lane change).

Loads the clone's round-93 v3 counter in-process, runs score() (no json.dump in
the probe), and replaces every bytes value in the receipt with {sha256, len} so the
receipt serialises. Demonstrates that the TypeError in main()'s json.dump is the
only defect on the honest-repair path: the label and met_target are unchanged.

Usage (scratch paths; TMPDIR must be set so child scratch stays under --work):
  TMPDIR=$WORK/probe-tmp python3 -I -B probe_sanitize_fresh_output.py \
      <clone> <work> <rev> <expect>
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys


def sanitize(o):
    if isinstance(o, bytes):
        return {"sha256": hashlib.sha256(o).hexdigest(), "len": len(o)}
    if isinstance(o, dict):
        return {k: sanitize(v) for k, v in o.items()}
    if isinstance(o, list):
        return [sanitize(v) for v in o]
    return o


def main(clone, work, rev, expect):
    spec = importlib.util.spec_from_file_location(
        "v3probe", os.path.join(clone, "tools/round-93/stop-boundary-repair-battery-v3.py"))
    v3 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v3)
    for name, repair in (("pos", "tools/round-92/upx-stop-boundary-search-repair.py"),
                         ("F3", ".ufo/waves/round-93/controls/identity_noop.py")):
        w = os.path.join(work, "probe-" + name)
        os.makedirs(w, exist_ok=True)
        ns = argparse.Namespace(root=clone, repair_cmd=repair, work=w, rev=rev,
                                expect=expect, json_out=None)
        code, rec = v3.score(ns)
        print(name, "code", code, rec.get("label"), "met", rec.get("met_target"))
        with open(os.path.join(work, f"probe-sanitized-{name}.json"), "w") as fh:
            fh.write(json.dumps(sanitize(rec), indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:5]))
