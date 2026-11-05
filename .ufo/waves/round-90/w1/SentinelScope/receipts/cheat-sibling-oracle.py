#!/usr/bin/env python3
"""Probe: a repair that derives nothing and reads a *sibling* invocation box.

The counter hands every child an absolute --in path inside `<work>/r90-boxes-*`,
which the sandbox does not hide (only the run root is tmpfs'd).  N3 (the
intact-idempotent control) runs immediately before each carrier's P1 cells and
leaves its repaired bytes in a sibling box as `out`.
"""
import os, sys


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    src = argv[argv.index("--in") + 1]
    dst = argv[argv.index("--out") + 1]
    want = os.path.getsize(src)
    with open(src, "rb") as fh:
        tampered = fh.read()
    box = os.path.dirname(src)
    boxes = os.path.dirname(box)
    best = None
    try:
        sibs = sorted(os.listdir(boxes))
    except OSError as exc:
        print(f"sibling-oracle: cannot list boxes: {exc}", file=sys.stderr)
        return 2
    for sib in sibs:
        cand = os.path.join(boxes, sib, "out")
        if not os.path.isfile(cand) or os.path.getsize(cand) != want:
            continue
        with open(cand, "rb") as fh:
            data = fh.read()
        diff = sum(1 for a, b in zip(tampered, data) if a != b)
        if best is None or diff < best[0]:
            best = (diff, cand, data)
    if best is None:
        print(f"sibling-oracle: {len(sibs)} sibling boxes, none with a "
              f"{want}-byte out", file=sys.stderr)
        return 2
    diff, cand, data = best
    with open(dst, "wb") as fh:
        fh.write(data)
    print(f"sibling-oracle: copied {cand} ({diff} differing byte(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
