#!/usr/bin/env python3
"""Summarize per-seat status files beneath a wave directory."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

VALID = {"settled", "failed", "blocked"}


def summarize(root: Path) -> dict[str, Any]:
    names = sorted(p.name for p in root.iterdir() if p.is_dir()) if root.is_dir() else []
    counts = {state: 0 for state in VALID}
    by_role: dict[str, int] = {}
    missing: list[str] = []
    parse_errors: list[str] = []
    unknown = 0
    for name in names:
        path = root / name / "status.json"
        if not path.is_file():
            missing.append(name)
            unknown += 1
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(record, dict) or record.get("seat") != name or record.get("status") not in VALID:
                raise ValueError("expected object with matching seat and valid status")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            parse_errors.append(f"{name}: {exc}")
            unknown += 1
            continue
        state = record["status"]
        counts[state] += 1
        role = record.get("role")
        if isinstance(role, str) and role:
            by_role[role] = by_role.get(role, 0) + 1
    return {"seats_total": len(names), **counts, "unknown": unknown,
            "by_role": dict(sorted(by_role.items())), "missing": missing,
            "parse_errors": parse_errors}


def expected_names(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return [line.strip() for line in text.splitlines() if line.strip()]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError("expected file must contain a JSON string array or newline-separated names")


def selftest(work: Path) -> int:
    root = work / "wave-accounting-fixture"
    root.mkdir(parents=True, exist_ok=True)
    fixtures = {
        "settled-seat": '{"seat":"settled-seat","role":"executor","status":"settled"}',
        "failed-seat": '{"seat":"failed-seat","role":"scribe","status":"failed"}',
        "malformed-seat": '{not json',
    }
    for name, text in fixtures.items():
        seat_dir = root / name
        seat_dir.mkdir(exist_ok=True)
        (seat_dir / "status.json").write_text(text, encoding="utf-8")
    (root / "missing-seat").mkdir(exist_ok=True)
    result = summarize(root)
    passed = (result["seats_total"] == 4 and result["settled"] == 1 and
              result["failed"] == 1 and result["blocked"] == 0 and
              result["unknown"] == 2 and result["missing"] == ["missing-seat"] and
              len(result["parse_errors"]) == 1 and
              result["by_role"] == {"executor": 1, "scribe": 1})
    print(json.dumps({"selftest": "passed" if passed else "failed", "result": result}, sort_keys=True))
    return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wave_root", nargs="?", type=Path)
    parser.add_argument("expected_file", nargs="?", type=Path)
    parser.add_argument("--expected", dest="expected_option", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--work", type=Path, help="scratch directory for selftest fixtures")
    args = parser.parse_args()
    if args.selftest:
        work = args.work or Path(os.environ.get("TMPDIR", tempfile.gettempdir()))
        work.mkdir(parents=True, exist_ok=True)
        return selftest(work)
    if args.wave_root is None:
        parser.error("wave_root is required unless --selftest is used")
    result = summarize(args.wave_root)
    print(json.dumps(result, sort_keys=True))
    if not args.check:
        return 0
    expected_path = args.expected_option or args.expected_file
    if expected_path is None:
        parser.error("--check requires an expected seat names file (positional or --expected)")
    try:
        expected = expected_names(expected_path)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"cannot read expected seats: {exc}", file=sys.stderr)
        return 2
    good = True
    for name in expected:
        path = args.wave_root / name / "status.json"
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(record, dict) or record.get("seat") != name or record.get("status") not in VALID:
                good = False
        except (OSError, UnicodeError, json.JSONDecodeError):
            good = False
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
