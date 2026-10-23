#!/usr/bin/env python3
"""CtlNoReader control reader: plausible-but-synthetic no-reader replay.

Same no-reader threat model: argv[1] is the opaque carrier path and is never
opened.  Unlike control-reader-constant-e01.py this record is NOT copied from
any frozen manifest row; it is a hand-written, syntactically canonical and
semantically plausible GLIBC requirement record (libc.so.6 requiring
GLIBC_2.2.5 and GLIBC_2.34, with the SysV ELF string hashes those names really
have).  It measures whether canonicality plus plausibility alone can satisfy
the frozen predicate.

Control, not a candidate implementation.
"""
import json
import sys

CONSTANT = {
    "schema": 1,
    "needed": [
        {
            "file": "libc.so.6",
            "versions": [
                {"name": "GLIBC_2.2.5", "flags": 0, "other": 2, "hash": 157882997},
                {"name": "GLIBC_2.34", "flags": 0, "other": 4, "hash": 110530996},
            ],
        }
    ],
}


def main():
    # argv[1] is intentionally ignored: this reader never opens the input.
    sys.stdout.write(json.dumps(CONSTANT, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
