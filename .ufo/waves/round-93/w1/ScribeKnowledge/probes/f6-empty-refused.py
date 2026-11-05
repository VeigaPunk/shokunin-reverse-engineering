#!/usr/bin/env python3
"""PROBE (unscored): typed rc 2, but the `refused` value is the empty string.
strict_typed() must call it untyped. If far_refused still counts it, the
strict typing is computed but never asserted in the verdict."""
import sys, json
print(json.dumps({"tool":"f6-empty-refused","refused":""}))
sys.exit(2)
