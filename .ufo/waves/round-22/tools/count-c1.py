#!/usr/bin/env python3
"""R22-C1 counter: frozen T1 catalog verbs exercised by retained, bound Evidence.

A T1 verb counts only when a knowledge entry at REV names the verb, cites a
retained file under EVIDENCE_PREFIX by full lane path, and that file holds a
non-refused JSON record whose evidence_id (cited in the same entry) and
operation match the verb (r21 `bind`). Mentions alone never count.
Not cryptographic authentication; local record binding only.

Exit 0 when every T1 verb is exercised, 1 when any is not, 2 unevaluable.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

T1 = ("identify-flutter-build", "inspect-dart-aot", "debug-with-gdb",
      "debug-with-rizin", "inspect-signal-decoders", "decode-signal-recording")
EVIDENCE_PREFIX = ".ufo/waves/round-22/evidence/c1/"


def load(root, rel, name):
    spec = importlib.util.spec_from_file_location(name, Path(root) / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure(root, rev):
    r21 = load(root, ".ufo/waves/round-21/tools/verb-coverage.py", "kaidoku_r21_bind")
    r20 = r21.legacy_helpers(root)
    r20.DEFAULT_TARGETS = T1
    r20.EVIDENCE_PREFIX = EVIDENCE_PREFIX
    r20.CITED = re.compile(re.escape(EVIDENCE_PREFIX) + r"[A-Za-z0-9._/-]*", re.ASCII)
    try:
        result = r21._measure(r20, root, rev)
    except r20.Refusal as error:
        raise ValueError(str(error)) from error
    exercised = [verb for verb in T1 if result["targets"][verb]["exercised"]]
    return {
        "rev": result["rev"],
        "claim": "R22-C1",
        "t1": list(T1),
        "t1_exercised": exercised,
        "t1_exercised_count": len(exercised),
        "t1_total": len(T1),
        "targets": result["targets"],
        "catalog_zero": result["zero"],
        "catalog_zero_count": len(result["zero"]),
        "catalog_mentioned_count": len(result["mentioned"]),
        "catalog_total": len(result["cli_commands"]),
        "limit": result["limit"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    args = parser.parse_args()
    try:
        out = measure(args.root, args.rev)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        print(json.dumps({"finding": "unevaluable", "error": str(error)}))
        return 2
    print(json.dumps(out, sort_keys=True))
    return 0 if out["t1_exercised_count"] == out["t1_total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
