#!/usr/bin/env python3
"""anchor-coverage — which of the 18 rows' anchor-cell digest slots are
reproduced as bytes in the landing pack?

Seat R43C2Land, round 43 wave 1.  Stdlib only, TMPDIR-honouring.

The gate reads only the URL cell, and none of the 18 rows pins a digest there
(the sibling seat's finding B1, independently reproduced here).  The digests
that do exist sit in the anchor cell: 41 slots over 12 rows.  The claim's
useful question is not "does the gate pass" (it passes on a stub) but "does the
landing actually carry the bytes the rows pin".

This tool answers that mechanically: it hashes every member of every archive
copy, every byte copy, and every gzip payload, and checks each anchor-cell
digest against that set.  A slot is covered iff some in-lane copy contains
bytes with that digest.

Usage: anchor-coverage.py --pack <dir> --sources <lane>/corpus/SOURCES.md --out <tsv>
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import sys
import tarfile

HEX64 = re.compile(r"(?<![0-9a-fA-F])([0-9a-fA-F]{64})(?![0-9a-fA-F])")
TARGET_ROWS = ["S001", "S002", "S003", "S006", "S007", "S023", "S035", "S040",
               "S048", "S056", "S066", "S070", "S079", "S081", "S082", "S083",
               "S090", "S092"]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_set(pack: str) -> dict[str, list[str]]:
    """digest -> [copy member descriptions] for every byte the pack carries."""
    out: dict[str, list[str]] = {}
    tree = os.path.join(pack, "corpus", "evidence", "round-42", "local-sources")
    for dirpath, _dirnames, filenames in os.walk(tree):
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, pack)
            with open(path, "rb") as fh:
                raw = fh.read()
            if raw[:2] == b"\x1f\x8b":
                try:
                    out.setdefault(sha256_bytes(gzip.decompress(raw)), []).append(
                        rel + " (decoded)")
                except OSError:
                    pass
            if tarfile.is_tarfile(path):
                with tarfile.open(path, "r:") as tar:
                    for m in tar.getmembers():
                        if not m.isreg():
                            continue
                        fh = tar.extractfile(m)
                        if fh is None:
                            continue
                        out.setdefault(sha256_bytes(fh.read()), []).append(
                            "%s:%s" % (rel, m.name))
            out.setdefault(sha256_bytes(raw), []).append(rel)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--sources", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    with open(args.sources, "r", encoding="utf-8") as fh:
        text = fh.read()

    slots = {}
    for line in text.splitlines():
        if not line.startswith("| S"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) < 11 or cells[0] not in TARGET_ROWS:
            continue
        slots[cells[0]] = [d.lower() for d in HEX64.findall(cells[5] + " " + cells[6])]

    have = digest_set(os.path.abspath(args.pack))

    rows = ["row\tslots\tcovered\tuncovered\tslot_digest\twhere"]
    total = covered_n = 0
    for sid in TARGET_ROWS:
        digs = slots.get(sid, [])
        covered = [d for d in digs if d in have]
        missing = [d for d in digs if d not in have]
        total += len(digs)
        covered_n += len(covered)
        rows.append("%s\t%d\t%d\t%d" % (sid, len(digs), len(covered), len(missing)))
        for d in missing:
            rows.append("%s\t\t\t\t%s\tNOT-IN-PACK" % ("", d))
        for d in covered:
            rows.append("%s\t\t\t\t%s\t%s" % ("", d, "; ".join(have[d][:2])))
    rows.append("TOTAL\t%d\t%d\t%d" % (total, covered_n, total - covered_n))

    out = "\n".join(rows) + "\n"
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(out)
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
