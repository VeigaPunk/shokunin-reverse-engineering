#!/usr/bin/env python3
"""CtlNoReader control reader: degenerate no-reader replay (empty requirement set).

Same no-reader threat model as control-reader-constant-e01.py: argv[1] is the
opaque carrier path and is never opened.  The emitted record is the canonical
empty requirement set, which is also the independently frozen expected record
for carrier e12 (the carrier with no GNU version requirements).

Used to measure the counter's floor: e12 has no string_table, so both scoring
schedules present the unmodified carrier.  This control therefore probes whether
the per-row "all schedules must match" rule and the target==12 rule together
reject a reader that never reads anything.
"""
import json
import sys

CONSTANT = {"schema": 1, "needed": []}


def main():
    # argv[1] is intentionally ignored: this reader never opens the input.
    sys.stdout.write(json.dumps(CONSTANT, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
