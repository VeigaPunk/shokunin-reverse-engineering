#!/usr/bin/env python3
"""freeze-pins.py - round-75 instrument (R75-C2 calibration, routed defect 6).

The round-74 SentinelScope SS74-1 finding: claim pin keys were joined to the
worktree root and opened directly, so an absolute key, a `..` segment or a
symlink could read outside it.  Every container path (including the claims
container itself) is now lexically checked and, in the worktree world,
resolved and required to stay inside the root before any open.

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


def lexical_ok(path: str) -> None:
    """SS74-1: a claims row may not name an absolute or traversing path."""
    if not isinstance(path, str) or not path:
        raise Unevaluable("a pin names an empty path")
    if os.path.isabs(path):
        raise Unevaluable(f"pin path is absolute: {path}")
    if any(part in ("..", ".") for part in path.replace("\\", "/").split("/")):
        raise Unevaluable(f"pin path contains a traversal segment: {path}")


def contained(root: str, path: str) -> str:
    """The resolved path must remain inside the worktree root (SS74-1).

    The worktree world opens files, so a symlink that resolves outside the
    root is refused before the open.  A Git-object expression is not a
    filesystem read, but the same lexical rule applies to it.
    """
    lexical_ok(path)
    root_abs = os.path.realpath(root)
    full = os.path.realpath(os.path.join(root_abs, path))
    try:
        inside = os.path.commonpath([root_abs, full]) == root_abs
    except ValueError:
        inside = False
    if not inside:
        raise Unevaluable(f"pin path resolves outside the worktree root: {path}")
    return full


def blob_at(root: str, rev: str | None, path: str) -> bytes | None:
    lexical_ok(path)
    if rev is None:
        full = contained(root, path)
        try:
            with open(full, "rb") as fh:
                return fh.read()
        except OSError:
            return None
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def check(root: str, claims_path: str, rev: str | None) -> dict:
    lexical_ok(claims_path)
    if rev is None:
        try:
            with open(contained(root, claims_path), encoding="utf-8") as fh:
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
    return {"schema": "kaidoku-r75-freeze-pins-v1",
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
    blob = blob_at(root, None, "tools/round-75/freeze-pins.py")
    cases["blob-at-worktree"] = blob is not None and len(blob) > 0
    cases["blob-absent"] = blob_at(root, None, "no/such/path") is None
    for name, path in (("containment-absolute-refused", "/etc/passwd"),
                       ("containment-traversal-refused",
                        "tools/../../etc/passwd")):
        try:
            blob_at(root, None, path)
            cases[name] = False
        except Unevaluable:
            cases[name] = True
    cases["containment-descendant-ok"] = contained(
        root, "tools/round-75/freeze-pins.py").startswith(
            os.path.realpath(root) + os.sep)
    print(json.dumps({"selftest": "tools/round-75/freeze-pins.py",
                      "cases": len(cases), "case_names": sorted(cases),
                      "failures": [k for k, v in cases.items() if not v]},
                     indent=1, sort_keys=True))
    return 0 if all(cases.values()) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--claims", default=".ufo/waves/round-75/claims.json")
    ap.add_argument("--rev")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        receipt = check(args.root, args.claims, args.rev)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r75-freeze-pins-v1",
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
