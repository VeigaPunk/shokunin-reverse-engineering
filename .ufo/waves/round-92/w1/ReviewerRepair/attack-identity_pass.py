#!/usr/bin/env python3
"""identity_pass.py - ReviewerRepair attack tool for R92-C1 (ATTACK q4).

Always exits 0 and writes the input bytes unchanged. Per the frozen counter:
near cells become `silent`, far cells become `silent` (never refused), intact
cells pass by definition. Run to check whether the unchanged-output pass can
satisfy any frozen arm.
"""
import json
import sys
import os


def main():
    argv = sys.argv[1:]
    src = argv[argv.index("--in") + 1]
    dst = argv[argv.index("--out") + 1]
    with open(src, "rb") as fh:
        data = fh.read()
    with open(dst, "wb") as fh:
        fh.write(data)
    print(json.dumps({"tool": "identity_pass", "class": "intact"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
