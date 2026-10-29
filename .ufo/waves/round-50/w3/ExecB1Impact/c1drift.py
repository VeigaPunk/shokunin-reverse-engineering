#!/usr/bin/env python3
"""ExecB1Impact: report the C1 counter's freeze-drift set for a REV (no REA run).

Imports the FROZEN counter `tools/round-50/c1-counter.py` from the fixture clone and calls
its own `frozen_drift()` — the exact function the counter uses — with the carriers spec
read at the freeze.  No REA, no network, no lane writes.
"""
import json
import subprocess
import sys


def main():
    clone, freeze, rev = sys.argv[1], sys.argv[2], sys.argv[3]
    sys.path.insert(0, clone + '/tools/round-50')
    import importlib.util
    spec_ = importlib.util.spec_from_file_location('c1counter', clone + '/tools/round-50/c1-counter.py')
    mod = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(mod)
    raw = mod.show(clone, freeze, mod.CARRIERS)
    spec = json.loads(raw)
    drift = mod.frozen_drift(clone, freeze, rev, spec)
    print(json.dumps({'freeze': freeze, 'rev': rev, 'drift': drift,
                      'drift_nonempty': bool(drift)}, indent=1))


if __name__ == '__main__':
    main()
