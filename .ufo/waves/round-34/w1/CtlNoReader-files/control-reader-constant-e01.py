#!/usr/bin/env python3
"""CtlNoReader control reader: a no-reader replay of one frozen expected record.

Threat model exercised: an adversary that satisfies the frozen
P34-version-needs counter WITHOUT ever opening the carrier input.

The reader receives the opaque carrier path as argv[1] and deliberately never
touches it.  It emits one plausible canonical GNU version-needs record that was
authored independently of the reader (the frozen manifest entry for carrier
e01 in .ufo/waves/round-34/expected.json, produced by author_expected.py).

No ELF parsing, no file access, no environment probe: argv[1] is not even
referenced.  This is a control, not a candidate implementation.
"""
import json
import sys

# Independently frozen expected record for carrier e01, verbatim.
# {"schema": 1, "needed": [{"file": "libc.so.6", "versions": [...]}]}
CONSTANT = {
    "schema": 1,
    "needed": [
        {
            "file": "libc.so.6",
            "versions": [
                {"name": "GLIBC_2.14", "flags": 0, "other": 7, "hash": 110530964},
                {"name": "GLIBC_2.16", "flags": 0, "other": 6, "hash": 110530966},
                {"name": "GLIBC_2.2.5", "flags": 0, "other": 2, "hash": 157882997},
                {"name": "GLIBC_2.3", "flags": 0, "other": 8, "hash": 225011987},
                {"name": "GLIBC_2.3.4", "flags": 0, "other": 3, "hash": 157882740},
                {"name": "GLIBC_2.34", "flags": 0, "other": 4, "hash": 110530996},
                {"name": "GLIBC_2.4", "flags": 0, "other": 5, "hash": 225011988},
                {"name": "GLIBC_ABI_DT_RELR", "flags": 0, "other": 9, "hash": 16584258},
            ],
        }
    ],
}


def main():
    # argv[1] (the opaque carrier path) is intentionally ignored: this reader
    # never opens the input.
    sys.stdout.write(json.dumps(CONSTANT, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
