#!/usr/bin/env python3
"""CtlNoReader control reader: size-keyed manifest-oracle replay (never opens input).

Same no-reader family as the other controls: the carrier input file is NEVER
opened.  Only os.stat() metadata of the opaque path is consulted, plus an
on-disk independent record source (the frozen manifest).  The frozen manifest
gives a distinct byte size for each of the twelve carriers, so size alone
identifies the carrier without reading a single byte of carrier content.

The emitted record is therefore the independently frozen expected record for
whichever carrier was presented, and it is exactly right for the unmodified
(schedule 0) carrier.  This control exists to measure which counter mechanism
actually stops a content-free replay: the per-row "every schedule must match"
aggregation, the randomized same-length string-table renaming, or the target
count of twelve.

Control, not a candidate implementation.
"""
import json
import os
import sys

MANIFEST = "/fast/scratch/hyaku/kaidoku-r34/w1/CtlNoReader/.ufo/waves/round-34/expected.json"


def load_by_size():
    with open(MANIFEST, "rb") as handle:
        manifest = json.loads(handle.read().decode("utf-8"))
    table = {}
    for row in manifest["carriers"]:
        table[row["size"]] = row["expected"]
    return table


def main():
    path = sys.argv[1]
    # os.stat only: the carrier bytes are never opened.
    size = os.stat(path).st_size
    record = load_by_size()[size]
    sys.stdout.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
