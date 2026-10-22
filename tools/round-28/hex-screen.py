#!/usr/bin/env python3
"""Pre-freeze screen for EVM hex carriers (QUALITY row 43, mistake M28-1).

Usage: python3 -I -B tools/round-28/hex-screen.py --root <LANE> <carriers.tsv>

Reads a carrier list whose second column is a lane-relative runtime hex path, and applies
the input rule REA 6.5.0 states when it refuses a carrier ("Hex carrier requires complete
hexadecimal byte pairs, an optional 0x prefix and outer ASCII whitespace"). Prints one line
per failing carrier and a summary. Exit 0 when every carrier passes, 1 otherwise.
"""
import argparse
import os
import re
import sys

HEX = re.compile(r"\A(?:0[xX])?(?:[0-9a-fA-F]{2})*\Z")
PLACEHOLDER = re.compile(r"__\$[0-9a-fA-F]{34}\$__")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("carriers")
    a = ap.parse_args()
    lines = open(a.carriers, encoding="utf-8").read().splitlines()
    bad = total = 0
    for line in lines[1:]:
        cols = line.split("\t")
        if len(cols) < 2:
            continue
        total += 1
        body = open(os.path.join(a.root, cols[1]), encoding="ascii", errors="replace").read()
        body = body.strip(" \t\r\n\f\v")
        if not HEX.match(body):
            bad += 1
            ph = PLACEHOLDER.findall(body)
            print("FAIL %s %s placeholders=%d %s" % (cols[0], cols[1], len(ph), " ".join(ph)))
    print("carriers=%d fail=%d" % (total, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
