#!/usr/bin/env python3
"""Scores the draft `## Owned axes` cells without writing the lane tree.

Reads SCORECARD.md at --rev, replaces only the two `coverage`/`depth` rows with
`receipts/cell_lines.txt`, and runs the frozen counter's `evaluate_text` on the
edited card (battery off: the card's corrections section is unchanged).

Usage: python3 -I -B validate_draft.py --root <lane> --rev <REV>
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    sys.path.insert(0, os.path.join(root, "tools", "round-47"))
    sys.path.insert(0, os.path.join(root, "tools", "round-46"))
    import gate  # noqa: PLC0415
    import record  # noqa: PLC0415

    rev = gate.resolve(root, args.rev)
    card = gate.show(root, rev, "SCORECARD.md")
    new = open(os.path.join(HERE, "cell_lines.txt"), encoding="utf-8").read().splitlines()
    lines = card.splitlines()
    if len(new) != 2 or lines[22].split("|", 2)[1].strip() != "coverage" \
            or lines[23].split("|", 2)[1].strip() != "depth":
        print(json.dumps({"reason": "card rows are not at lines 23-24 as expected"}))
        return 2
    lines[22], lines[23] = new[0], new[1]
    edited = "\n".join(lines) + ("\n" if card.endswith("\n") else "")
    files = lambda p: gate.show(root, rev, p)  # noqa: E731
    code, receipt = record.evaluate_text(edited, files, root, rev, battery=None)
    out = {"utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "rev": rev, "exit": code, "mismatches": receipt.get("mismatches"),
           "corrections": receipt.get("corrections"),
           "corrections_bad": receipt.get("corrections_bad"),
           "exempted": [a.get("atom") for a in receipt.get("exempted", [])],
           "verified": receipt.get("verified"), "atoms": receipt.get("atoms"),
           "failing": receipt.get("failing"), "met_target": receipt.get("met_target"),
           "substitution": "SCORECARD.md lines 23-24 replaced in memory by receipts/cell_lines.txt"}
    print(json.dumps(out, indent=1, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
