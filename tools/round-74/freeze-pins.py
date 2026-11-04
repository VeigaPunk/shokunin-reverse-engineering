#!/usr/bin/env python3
"""freeze-pins.py - round-74 instrument (R74-C2 calibration, planned item d).

The round-29 freeze gate reads a claim freeze's producer pins from the freeze
commit.  Round 73's freeze pinned two producer blobs that were not the blobs at
that commit (QUALITY row 130), so the gate reports `INSTRUMENT_PIN_MISMATCH`
permanently for that freeze.  The repair is procedural and must be mechanical
before the freeze commit exists: compute every pin from the bytes the freeze
will name, not from a plan paragraph or an earlier copy.

This checker reads a `claims.json` (from the worktree before the freeze commit,
or from `--rev` after it) and compares every pin in `instruments` and
`loaded_by_counter` with the sha256 of that path's bytes in the same world.

Exit: 0 every pin equals its blob; 1 mismatches, each named; 2 could-not-
evaluate (unreadable container, a pinned path absent from the world).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

BLOCKS = ("instruments", "loaded_by_counter")


class Unevaluable(Exception):
    """Exit-2 class: the checker cannot score this container."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_at(root: str, rev: str | None, path: str) -> bytes | None:
    full = os.path.join(root, path)
    if rev is None:
        try:
            with open(full, "rb") as fh:
                return fh.read()
        except OSError:
            return None
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def check(root: str, claims_path: str, rev: str | None) -> dict:
    if rev is None:
        try:
            with open(os.path.join(root, claims_path), encoding="utf-8") as fh:
                claims = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            raise Unevaluable(f"claims container unreadable: {exc}")
    else:
        proc = subprocess.run(["git", "-C", root, "show",
                               f"{rev}:{claims_path}"], capture_output=True)
        if proc.returncode != 0:
            raise Unevaluable(f"claims container absent at {rev}")
        try:
            claims = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise Unevaluable(f"claims container is not JSON: {exc}")
    rows = []
    missing = []
    for block in BLOCKS:
        pins = claims.get(block)
        if not isinstance(pins, dict):
            missing.append(f"{block}: block absent")
            continue
        for path, digest in pins.items():
            blob = blob_at(root, rev, path)
            if blob is None:
                missing.append(f"{block}:{path}: path absent from the world")
                continue
            rows.append({"block": block, "path": path, "pinned": digest,
                         "blob": sha256_bytes(blob),
                         "matched": sha256_bytes(blob) == digest})
    mismatches = [row for row in rows if not row["matched"]]
    ok = bool(rows) and not mismatches and not missing
    return {"schema": "kaidoku-r74-freeze-pins-v1",
            "claims": claims_path, "rev": rev, "world":
            ("rev" if rev else "worktree"),
            "rows": rows, "row_count": len(rows),
            "mismatches": [f"{r['block']}:{r['path']}" for r in mismatches],
            "missing": missing, "ok": ok}


def selftest() -> int:
    cases = {}
    cases["sha-stable"] = sha256_bytes(b"x") == sha256_bytes(b"x")
    cases["sha-changes"] = sha256_bytes(b"x") != sha256_bytes(b"y")
    root = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    blob = blob_at(root, None, "tools/round-74/freeze-pins.py")
    cases["blob-at-worktree"] = blob is not None and len(blob) > 0
    cases["blob-absent"] = blob_at(root, None, "no/such/path") is None
    print(json.dumps({"selftest": "tools/round-74/freeze-pins.py",
                      "cases": len(cases),
                      "failures": [k for k, v in cases.items() if not v]},
                     indent=1, sort_keys=True))
    return 0 if all(cases.values()) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--claims", default=".ufo/waves/round-74/claims.json")
    ap.add_argument("--rev")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        receipt = check(args.root, args.claims, args.rev)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r74-freeze-pins-v1",
                          "unevaluable": str(exc)}), file=sys.stderr)
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
