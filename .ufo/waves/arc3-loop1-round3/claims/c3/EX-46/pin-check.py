#!/usr/bin/env python3
"""EX-46 pin-check: re-derive the pointer-table digest and compare against the
pin in expected.json. Rule #14 discipline: identity is re-derived, never cited
from memory. Read-only; run after every revision of the artifact pair.

Usage: python3 pin-check.py [--table PATH] [--expected PATH]
Exit 0 iff sha256(table bytes) == expected.json pointer_table.sha256.
"""
import argparse, hashlib, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--table", default=".ufo/gates/citation-drift/pointer-table.json")
ap.add_argument("--expected", default=".ufo/gates/citation-drift/expected.json")
a = ap.parse_args()

tbytes = open(a.table, "rb").read()
derived = hashlib.sha256(tbytes).hexdigest()
try:
    e = json.load(open(a.expected))
    pin = e.get("pointer_table")
    pin = pin.get("sha256") if isinstance(pin, dict) else None
except Exception as ex:  # unreadable expected -> could-not-evaluate
    print("PIN_CHECK: could-not-evaluate expected unreadable: %r" % (ex,))
    sys.exit(2)
print("PIN_CHECK: table=%s bytes=%d sha256=%s" % (a.table, len(tbytes), derived))
print("PIN_CHECK: expected=%s pin=%s" % (a.expected, pin))
if pin is None:
    print("PIN_CHECK: VERDICT none (expected pins no pointer-table digest)")
    sys.exit(2)
if derived == pin:
    print("PIN_CHECK: VERDICT MATCH")
    sys.exit(0)
print("PIN_CHECK: VERDICT MISMATCH (derived != pin)")
sys.exit(1)
