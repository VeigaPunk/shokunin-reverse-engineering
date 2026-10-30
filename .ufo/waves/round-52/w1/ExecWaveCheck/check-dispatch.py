#!/usr/bin/env python3
"""Check wave dispatch specs for unresolved uppercase placeholders and unused brace fields."""
import argparse
import json
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\{[A-Z_0-9]{2,}\}")
UNUSED_PATH_BRACES = re.compile(r"\{[^{}]*/home/vgpnk/Projects/shokunin/kaidoku-shokunin[^{}]*\}")


def findings(text):
    out = []
    for pattern in (PLACEHOLDER, UNUSED_PATH_BRACES):
        out.extend(match.group(0) for match in pattern.finditer(text))
    return out


def check_payload(data):
    issues = []
    context = data.get("context", "")
    if isinstance(context, str):
        issues.extend(("<context>", value) for value in findings(context))
    for item in data.get("items", []):
        name = str(item.get("name", "<unnamed>"))
        prompt = item.get("prompt", "")
        if isinstance(prompt, str):
            issues.extend((name, value) for value in findings(prompt))
    return issues


def selftest():
    fixtures = [
        ({"context": "clean context", "items": [{"name": "clean", "prompt": "nothing unresolved"}]}, False),
        ({"context": "{UNRESOLVED_TOKEN}", "items": []}, True),
        ({"context": "clean", "items": [{"name": "item-x", "prompt": "path {prefix /home/vgpnk/Projects/shokunin/kaidoku-shokunin/x}"}]}, True),
    ]
    for fixture, expected in fixtures:
        actual = bool(check_payload(fixture))
        if actual != expected:
            print(f"selftest failed: expected violations={expected}, got={actual}", file=sys.stderr)
            return 1
    print("selftest: 3 fixtures passed (clean, uppercase marker, literal lane-path braces)")
    return 0


def load_json(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", nargs="?", help="wave spec JSON")
    parser.add_argument("rendered", nargs="?", help="optional rendered dispatch JSON")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        result = selftest()
        if result:
            return result
        if not args.spec:
            return 0
    if not args.spec:
        parser.error("spec is required unless --selftest is used")
    issues = []
    for source in (args.spec, args.rendered):
        if source:
            data = load_json(source)
            issues.extend((source, *issue) for issue in check_payload(data))
    if issues:
        for source, name, snippet in issues:
            print(f"{source}: {name}: {snippet}")
        return 1
    print("dispatch placeholder check: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
