#!/usr/bin/env python3
"""EX-05 (c1, round 2): instrument-native token/locus scan of a text block.

Imports a census v10 revision as a module and asks ITS OWN classify() whether
the text can ever form a locus: classify() returns a record only when a unit
matches REA_GATE and holds >= 1 needle (pin / bare version / rooted pointer /
cache hash). Zero records therefore means the text is locus-free under that
instrument, position-independently for the needle test.

Usage: python3 payload-token-scan.py <census.py> <block-file>
"""
import importlib.util
import sys


def load(path):
    spec = importlib.util.spec_from_file_location("census", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(census_path, block_path):
    mod = load(census_path)
    text = open(block_path, encoding="utf-8").read().rstrip("\n")
    lines = text.splitlines()
    needles = {"pin": [m.group(0) for m in mod.PIN.finditer(text)],
               "bare": [m.group(0) for m in mod.VER.finditer(text)],
               "ptr": [m.group(0) for m in mod.PTR.finditer(text)],
               "cache": [m.group(0) for m in mod.CACHE.finditer(text)],
               "gate": [m.group(0) for m in mod.REA_GATE.finditer(text)]}
    out = {}
    recs = mod.classify("SKILL.md", lines, mod.live_pins(), out)
    print("needles=%r" % {k: v for k, v in needles.items() if v})
    print("needle_total=%d loci_records=%d record_classes=%r"
          % (sum(len(v) for v in needles.values()), len(recs), sorted(out)))
    return 1 if (recs or any(needles.values())) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
