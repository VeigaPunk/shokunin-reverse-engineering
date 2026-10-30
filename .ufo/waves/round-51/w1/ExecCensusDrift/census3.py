#!/usr/bin/env python3
"""Registry-driven census for the marker-bounded instrument-registry v2."""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

OPEN = "<!-- instrument-registry v2 -->"
CLOSE = "<!-- /instrument-registry -->"
SUPERSEDES = "tools/round-48/census2.json for registry inventory only"
RULE = "unique registered tool paths in SKILL.md's instrument-registry v2 block at --rev"
PATH_RE = re.compile(r"^[A-Za-z0-9._/-]+$")


class CensusError(ValueError):
    pass


def read_at(root, rev, path):
    if rev == "WORKTREE":
        full = os.path.join(root, path)
        try:
            with open(full, encoding="utf-8") as stream:
                return stream.read()
        except FileNotFoundError:
            return None
    result = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                            capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def registry_paths(skill, file_reader):
    if skill.count(OPEN) != 1 or skill.count(CLOSE) != 1:
        raise CensusError("missing or duplicate instrument-registry markers")
    block = skill.split(OPEN, 1)[1].split(CLOSE, 1)[0]
    paths = []
    for lineno, line in enumerate(block.splitlines(), 1):
        text = line.strip()
        if not text.startswith("|"):
            continue
        cells = [cell.strip() for cell in text.strip("|").split("|")]
        if len(cells) < 2:
            raise CensusError(f"malformed registry row at block line {lineno}")
        raw = cells[0].strip("`")
        if raw == "tool" or set(raw) <= set("-:"):
            continue
        if not PATH_RE.fullmatch(raw) or raw.startswith("/") or ".." in raw.split("/"):
            raise CensusError(f"malformed registered path at block line {lineno}: {raw!r}")
        normalized = os.path.normpath(raw).replace(os.sep, "/")
        if normalized != raw:
            raise CensusError(f"non-normalized registered path at block line {lineno}: {raw!r}")
        if file_reader(raw) is None:
            raise CensusError(f"registered path missing at revision: {raw}")
        paths.append(raw)
    if not paths:
        raise CensusError("registry contains no tool paths")
    duplicates = sorted(path for path in set(paths) if paths.count(path) > 1)
    if duplicates:
        raise CensusError("duplicate registered paths: " + ", ".join(duplicates))
    return sorted(paths)


def derive(root, rev):
    skill = read_at(root, rev, "SKILL.md")
    if skill is None:
        raise CensusError("SKILL.md unreadable at revision")
    paths = registry_paths(skill, lambda path: read_at(root, rev, path))
    return {"rule": RULE, "paths": paths,
            "provenance": {"rev": rev, "source": "SKILL.md instrument-registry v2 markers"},
            "supersedes": SUPERSEDES}


def compare(root, rev, census_path):
    expected = derive(root, rev)
    artifact = read_at(root, rev, census_path)
    if artifact is None:
        raise CensusError(f"census artifact unreadable at revision: {census_path}")
    try:
        actual = json.loads(artifact)
        paths = actual["paths"]
        if not isinstance(paths, list) or any(not isinstance(p, str) for p in paths):
            raise TypeError("paths must be a string list")
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise CensusError(f"malformed census artifact: {exc}") from exc
    registry_only = sorted(set(expected["paths"]) - set(paths))
    census_only = sorted(set(paths) - set(expected["paths"]))
    duplicate_list = sorted(p for p in set(paths) if paths.count(p) > 1)
    return {"rev": rev, "registry_paths": len(expected["paths"]),
            "census_paths": len(paths), "census_outside": registry_only,
            "census_unregistered": census_only, "duplicates": duplicate_list,
            "exit": 0 if not registry_only and not census_only and not duplicate_list else 1}


def selftest():
    good = ["tools/a.py", "tools/b.sh"]
    def altered(paths):
        outside = sorted(set(good) - set(paths))
        unregistered = sorted(set(paths) - set(good))
        duplicates = sorted(p for p in set(paths) if paths.count(p) > 1)
        return bool(outside or unregistered or duplicates)
    cases = {"clean": not altered(good), "extra": altered(good + ["tools/x.py"]),
             "missing": altered(good[:1]), "duplicate": altered(good + [good[0]]),
             "unknown": altered(["tools/a.py", "tools/z.py"])}
    print(json.dumps({"selftest": cases}, sort_keys=True))
    return 0 if all(cases.values()) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--census")
    parser.add_argument("--historical", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        if args.historical:
            census = json.loads(read_at(args.root, args.rev, "tools/round-48/census2.json"))
            current = derive(args.root, args.rev)["paths"]
            outside = sorted(set(current) - set(census["paths"]))
            unregistered = sorted(set(census["paths"]) - set(current))
            print(json.dumps({"registry_paths": len(current), "census_paths": len(census["paths"]),
                              "census_outside": outside, "census_unregistered": unregistered,
                              "exit": 1 if outside or unregistered else 0}, indent=2))
            return 1 if outside or unregistered else 0
        if args.generate:
            if not args.out:
                raise CensusError("--generate requires --out")
            doc = derive(args.root, args.rev)
            doc["provenance"].update({"command": " ".join(sys.argv),
                                      "utc": datetime.datetime.now(datetime.timezone.utc).isoformat()})
            with open(args.out, "w", encoding="utf-8") as stream:
                json.dump(doc, stream, indent=2)
                stream.write("\n")
            print(json.dumps({"generated": args.out, "paths": len(doc["paths"])}))
            return 0
        if args.check:
            if not args.census:
                raise CensusError("--check requires --census")
            result = compare(args.root, args.rev, args.census)
            print(json.dumps(result, indent=2))
            return result["exit"]
        raise CensusError("choose --generate, --check, --historical, or --selftest")
    except (CensusError, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
