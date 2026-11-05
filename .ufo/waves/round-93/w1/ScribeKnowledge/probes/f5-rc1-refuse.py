#!/usr/bin/env python3
"""PROBE (unscored): refuses every input with rc 1 and no output file.
A typed refusal is rc 2 + JSON `refused`; this is neither. If v3's
far_refused / fresh_far_refused counts it, the strict typing is recorded
but never asserted in the verdict."""
import sys, json
d=open(sys.argv[sys.argv.index("--in")+1],"rb").read()
print(json.dumps({"tool":"f5-rc1-refuse","refused":"untyped rc 1"}))
sys.exit(1)
