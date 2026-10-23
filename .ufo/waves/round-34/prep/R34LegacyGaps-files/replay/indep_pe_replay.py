#!/usr/bin/env python3
"""Isolated replay shim for the archived round-32 independent-pe comparator.

Imports `.ufo/waves/round-32/independent-pe/compare.py` unchanged (read-only)
and rebinds only its two path globals - TSV and BASE - to a fixture directory,
because the archived file hardcodes both and ignores argv. Exit code is the
archived comparator's own `main()` return.
"""
import importlib.util
import sys


def main():
    if len(sys.argv) != 4:
        print("usage: indep_pe_replay.py <archived-compare.py> <fixture-BASE> <fixture-carriers.tsv>")
        return 2
    src, base, tsv = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = importlib.util.spec_from_file_location("r32_independent_pe_compare", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.TSV = tsv
    mod.BASE = base
    return mod.main()


if __name__ == "__main__":
    sys.exit(main())
