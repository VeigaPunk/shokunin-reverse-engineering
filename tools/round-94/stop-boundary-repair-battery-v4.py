#!/usr/bin/env python3
"""stop-boundary-repair-battery-v4.py - round-94 counter (R94-C1, calibration).

The VERDICT code is the round-93 counter `tools/round-93/stop-boundary-repair-battery-v3.py`,
imported by path and pinned by sha256 in `.ufo/waves/round-94/claims.json`. v4 changes
exactly one thing: the RECEIPT WRITER.

Round-93 M93-e: v3 stores the repaired fresh-cell output bytes in
`fresh_cells[*].output`, so `json.dump` raised `TypeError` on the honest case and the
frozen `--json-out` command exited 1 with a truncated receipt (D-93-D). v4 answers
each bytes value with `{"bytes": <len>, "sha256": <hex>}` (the JSON encodable version the
`json` documentation's `default` hook asks for) and raises `TypeError` for any other
unknown type. The receipt is written to `<json-out>.tmp` and renamed into place only after
`json.dump` returns, so a receipt is complete JSON or absent.

Usage is identical to v3: `--root --repair-cmd --work --rev --expect --json-out`.
Exit 0 iff the frozen label is met (the verdict code's exit). `--selftest` exercises the
writer's helper cases; the claim's evidence is the public CLI run with `--json-out`, not
the selftest.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/round-94/stop-boundary-repair-battery-v4.py"
V3_TOOL = "tools/round-93/stop-boundary-repair-battery-v3.py"
V3 = os.path.join(HERE, "..", "round-93", "stop-boundary-repair-battery-v3.py")


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v3 = _load(V3, "r93_v3_verdict")


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _default(obj):
    """JSON encodable version of bytes; any other unknown type is an error, never a str()."""
    if isinstance(obj, (bytes, bytearray)):
        return {"bytes": len(obj), "sha256": hashlib.sha256(bytes(obj)).hexdigest()}
    raise TypeError(f"Cannot serialize object of {type(obj)}")


def write_receipt(path: str, receipt: dict) -> None:
    """Complete JSON or absent: serialize to `<path>.tmp`, rename only on success."""
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True, default=_default)
            fh.write("\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def _selftest(work: str) -> int:
    os.makedirs(work, exist_ok=True)
    results = []

    def case(name: str, ok: bool) -> None:
        results.append((name, ok))
        print(f"selftest {name}: {'ok' if ok else 'FAIL'}")

    blob = b"\x7fELF-fixture"
    enc = _default(blob)
    case("bytes-encoded", enc == {"bytes": len(blob),
                                  "sha256": hashlib.sha256(blob).hexdigest()})
    p = os.path.join(work, "receipt-bytes.json")
    write_receipt(p, {"label": "x", "fresh_cells": [{"output": blob, "rc": 0}]})
    with open(p, encoding="utf-8") as fh:
        back = json.load(fh)
    case("bytes-receipt-reparses",
         back["fresh_cells"][0]["output"]["bytes"] == len(blob)
         and not os.path.exists(p + ".tmp"))
    q = os.path.join(work, "receipt-unknown.json")
    try:
        write_receipt(q, {"x": object()})
        raised = False
    except TypeError:
        raised = True
    case("unknown-type-raises", raised and not os.path.exists(q)
         and not os.path.exists(q + ".tmp"))
    print(f"SELFTEST cases={len(results)} failures={sum(1 for _, ok in results if not ok)}")
    return 0 if all(ok for _, ok in results) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--repair-cmd", default=v3.DEFAULT_REPAIR)
    ap.add_argument("--work")
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--expect", help="frozen label: %r" % v3.FROZEN_LABEL)
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest(args.work or os.path.join(
            os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kaidoku-r94", "selftest-c1"))
    if not args.work or args.expect is None:
        print("usage: --work <dir> --expect <label> [--json-out <path>]", file=sys.stderr)
        return 2
    code, receipt = v3.score(args)
    root = os.path.abspath(args.root)
    receipt["tool"] = TOOL
    receipt["verdict_counter"] = V3_TOOL
    receipt["verdict_sha256"] = _sha256_file(os.path.join(root, V3_TOOL))
    receipt["counter_sha256"] = _sha256_file(os.path.join(root, TOOL))
    receipt["exit"] = code
    if args.json_out:
        write_receipt(args.json_out, receipt)
    print(receipt.get("label", receipt.get("unevaluable")), "met",
          receipt.get("met_target"), "exit", code)
    return code


if __name__ == "__main__":
    sys.exit(main())
