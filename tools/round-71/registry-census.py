#!/usr/bin/env python3
"""registry-census.py - round-71 instrument (R71-C3 operability).

Supersedes `tools/round-51/census3.py` (which stays byte-identical at its own
round) for one surface: the SKILL.md instrument-registry v2 block's own row
grammar.  The round-51 parser required exactly seven `|`-split cells and died
with `registry row must have seven cells` on the lane's own registry as soon as
rounds 69/70 appended rows: four round-69 rows carry a bare `|` inside the
pinned-value cell (eight cells) and six round-70 rows omit the owner cell (six
cells), so the standing drift census was unevaluable (exit 2) from
`616a5f2f` until this instrument (round-70 M70-7).

Grammar v2, declared here and recorded in the round-71 addendum:

  * a registry row is a GFM table line (`|` ... `|`); cells split on
    *unescaped* pipes, and `\\|` inside a cell is one literal pipe (GFM 4.10);
  * the first four cells are tool · purpose · verdict map · self-test command;
  * the last cell is the owner; the second-to-last is the write scope; every
    cell between the self-test command and those two is the pinned-value path,
    re-joined with `|` (this is how the four round-69 rows were authored:
    their pinned cell contains a literal pipe);
  * a row is CONFORMANT when it has at least six cells, its tool cell is a
    backtick-delimited normalized repository path that exists at the measured
    revision, and its re-joined pinned-value cell is non-empty.

Filed round-69 rows are never rewritten: the grammar reads them as authored.
The six round-70 rows are repaired in the same round this instrument lands
(owner cell appended, disclosed in LOG.md and the lesson), because an omitted
column is a defect, not a grammar variant.

Exit 0: markers, row grammar and inventory all clean (paths derived, every row
conformant, no duplicate); 1: findings named (nonconformant rows, duplicates);
2: malformed or unavailable input (markers, unreadable SKILL.md, bad argv).
`--selftest` runs isolated CLI fixtures and asserts exit codes plus finding
codes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

TOOL = "tools/round-71/registry-census.py"
OPEN = "<!-- instrument-registry v2 -->"
CLOSE = "<!-- /instrument-registry -->"
GRAMMAR = ("v2: split on unescaped '|', unescape '\\|'; tool/purpose/verdict/"
           "selftest = cells 0-3; owner = last; write_scope = second-last; "
           "pinned = join(cells[4:-2], '|'); conformant iff >=6 cells, a "
           "backtick path that exists at --rev, and a non-empty pinned cell")
HEADER = ("| tool | gate or probe - purpose | verdict map (exit codes) | self-test "
          "command | pinned-value path | write scope | owner |")


class CensusError(ValueError):
    """Exit-2 class: the registry cannot be measured, so nothing is claimed."""


def safe_path(path: str) -> bool:
    return (isinstance(path, str) and bool(path)
            and re.fullmatch(r"[A-Za-z0-9._/-]+", path) is not None
            and not path.startswith("/") and ".." not in path.split("/")
            and os.path.normpath(path).replace(os.sep, "/") == path)


def read_at(root: str, rev: str, path: str) -> str | None:
    if not safe_path(path):
        raise CensusError(f"non-normalized repository path: {path!r}")
    if rev == "WORKTREE":
        try:
            with open(os.path.join(root, path), encoding="utf-8") as stream:
                return stream.read()
        except FileNotFoundError:
            return None
    result = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                            capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def exists_at(root: str, rev: str, path: str) -> bool:
    if rev == "WORKTREE":
        return os.path.isfile(os.path.join(root, path))
    result = subprocess.run(["git", "-C", root, "cat-file", "-e", f"{rev}:{path}"],
                            capture_output=True)
    return result.returncode == 0


def split_cells(text: str) -> list[str]:
    """Split a table line on unescaped pipes, unescaping `\\|` (GFM 4.10)."""
    cells, buf, i = [], [], 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and i + 1 < len(text) and text[i + 1] == "|":
            buf.append("|")
            i += 2
            continue
        if ch == "|":
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    return cells


def parse(skill: str, exists) -> dict:
    """Parse the registry block under grammar v2; returns rows, paths, findings."""
    if skill.count(OPEN) != 1 or skill.count(CLOSE) != 1:
        raise CensusError("missing or duplicate registry markers")
    if skill.index(OPEN) >= skill.index(CLOSE):
        raise CensusError("reversed registry markers")
    block = skill.split(OPEN, 1)[1].split(CLOSE, 1)[0]
    rows = []
    for lineno, line in enumerate(block.splitlines(), 1):
        text = line.strip()
        if not text.startswith("|"):
            continue
        if not text.endswith("|"):
            raise CensusError("unterminated registry row")
        cells = split_cells(text[1:-1])
        if cells and cells[0] == "tool":
            continue
        if cells and all(re.fullmatch(r"[-:]+", c) for c in cells if c):
            continue
        if not cells or not cells[0]:
            raise CensusError("registry row with an empty tool cell")
        token = cells[0]
        defects = []
        if not (token.startswith("`") and token.endswith("`")):
            defects.append("tool-not-backticked")
            path = None
        else:
            path = token[1:-1]
            if not safe_path(path):
                defects.append("path-invalid")
                path = None
        if len(cells) < 6:
            defects.append("cells<6")
        pinned = "|".join(cells[4:-2]).strip() if len(cells) >= 6 else ""
        if not pinned or pinned == "—":
            defects.append("pinned-empty")
        if path is not None and not exists(path):
            defects.append("path-absent")
        rows.append({"line": lineno, "tool": token, "path": path,
                     "cells": len(cells), "pinned": pinned,
                     "write_scope": cells[-2] if len(cells) >= 2 else "",
                     "owner": cells[-1] if cells else "",
                     "defects": defects})
    if not rows:
        raise CensusError("empty registry")
    paths = [r["path"] for r in rows if r["path"]]
    seen, duplicates = set(), []
    for p in paths:
        if p in seen and p not in duplicates:
            duplicates.append(p)
        seen.add(p)
    nonconformant = [{"tool": r["tool"], "line": r["line"],
                      "defects": r["defects"]} for r in rows if r["defects"]]
    joined = [{"tool": r["tool"], "line": r["line"], "cells": r["cells"]}
              for r in rows if r["cells"] > 7]
    return {"grammar": GRAMMAR, "rows": len(rows), "row_list": rows,
            "paths": sorted(paths),
            "duplicates": duplicates, "nonconformant": nonconformant,
            "multicell_rows": joined,
            "legacy_rows": [{"tool": r["tool"], "cells": r["cells"]}
                            for r in rows if r["cells"] != 7]}


def derive(root: str, rev: str) -> dict:
    skill = read_at(root, rev, "SKILL.md")
    if skill is None:
        raise CensusError("SKILL.md unavailable at revision")
    doc = parse(skill, lambda p: exists_at(root, rev, p))
    doc.update({"rev": rev, "rule": "registry row grammar v2",
                "provenance": {"source": "SKILL.md registry markers"}})
    return doc


def verdict(doc: dict) -> tuple[dict, int]:
    findings = []
    if doc["duplicates"]:
        findings.append({"code": "DUPLICATE", "paths": doc["duplicates"]})
    if doc["nonconformant"]:
        findings.append({"code": "NONCONFORMANT", "rows": doc["nonconformant"]})
    out = {"grammar": doc["grammar"], "rows": doc["rows"],
           "paths": len(doc["paths"]), "multicell_rows": len(doc["multicell_rows"]),
           "legacy_rows": doc["legacy_rows"], "duplicates": doc["duplicates"],
           "nonconformant": doc["nonconformant"], "findings": findings,
           "rev": doc["rev"], "ok": not findings}
    return out, (0 if not findings else 1)


def selftest() -> int:
    cases = {}

    def row(*cells: str) -> str:
        return "| " + " | ".join(cells) + " |\n"

    good = row("`tools/a.py`", "gate - a", "0/1/2", "--selftest", "pin", "none",
               "kaidoku")
    r69 = row("`tools/b.py`", "gate - b", "0/1/2", "--selftest", "pin one",
              "pin two", "write", "kaidoku")
    six = row("`tools/c.py`", "gate - c", "0/1/2", "--selftest", "pin",
              "write")
    escaped = row("`tools/d.py`", "gate - d", "0/1/2", "--selftest",
                  "a \\| b", "write", "kaidoku")
    table = lambda *rows: (OPEN + "\n" + HEADER + "\n"
                           + "|---|---|---|---|---|---|---|\n" + "".join(rows) + CLOSE)

    paths = {"tools/a.py", "tools/b.py", "tools/c.py", "tools/d.py", "tools/e.py"}
    parsed = parse(table(good, r69, escaped), lambda p: p in paths)
    cases["clean-7-cell"] = (parsed["rows"] == 3 and not parsed["nonconformant"]
                             and parsed["duplicates"] == [])
    cases["r69-8-cell-joined"] = (
        parsed["legacy_rows"] == [{"tool": "`tools/b.py`", "cells": 8}]
        and parsed["rows"] == 3)
    b_row = parse(table(r69), lambda p: p in paths)["row_list"][0]
    cases["pinned-rejoined"] = b_row["pinned"] == "pin one|pin two"
    cases["pinned-write-owner"] = (b_row["write_scope"] == "write"
                                   and b_row["owner"] == "kaidoku")
    d_row = parse(table(escaped), lambda p: p in paths)["row_list"][0]
    cases["escaped-pipe-one-cell"] = (d_row["cells"] == 7
                                      and d_row["pinned"] == "a | b")
    six_parsed = parse(table(good, six), lambda p: p in paths)
    cases["six-cell-nonconformant"] = (
        [r["defects"] for r in six_parsed["nonconformant"]]
        == [["pinned-empty"]])
    five = row("`tools/e.py`", "gate", "0/1", "--selftest")
    five_parsed = parse(table(good, five), lambda p: p in paths)
    cases["five-cell-nonconformant"] = (
        five_parsed["nonconformant"][0]["defects"] == ["cells<6", "pinned-empty"])
    absent = parse(table(row("`tools/z.py`", "g", "0", "s", "p", "w", "kaidoku")),
                   lambda p: p in paths)
    cases["absent-path-named"] = (
        absent["nonconformant"][0]["defects"] == ["path-absent"])
    dup = parse(table(good, good), lambda p: p in paths)
    cases["duplicate-named"] = dup["duplicates"] == ["tools/a.py"]
    # CLI fixtures: the outer CLI, isolated roots, exit codes and finding codes.
    scratch = os.environ.get("TMPDIR") or os.path.join(
        os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"),
        "kaidoku-r71", "registry-census-selftest")
    os.makedirs(scratch, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="registry.", dir=scratch) as root:
        os.makedirs(os.path.join(root, "tools"))
        for name in ("a.py", "b.py"):
            with open(os.path.join(root, "tools", name), "w") as fh:
                fh.write("# fixture; never executed\n")
        clean_table = table(good, row("`tools/b.py`", "gate - b", "0/1/2",
                                      "--selftest", "pin", "none", "kaidoku"))
        scenarios = (
            ("cli-clean", clean_table, 0, []),
            ("cli-six-cell", table(good, six), 1, ["NONCONFORMANT"]),
            ("cli-duplicate", table(good, good), 1, ["DUPLICATE"]),
            ("cli-absent", table(row("`tools/z.py`", "g", "0", "s", "p", "w",
                                     "kaidoku")), 1, ["NONCONFORMANT"]),
            ("cli-marker", clean_table.replace(CLOSE, ""), 2, []),
        )
        for name, skill, code, codes in scenarios:
            with open(os.path.join(root, "SKILL.md"), "w") as fh:
                fh.write(skill)
            proc = subprocess.run(
                [sys.executable, "-I", "-B", os.path.abspath(__file__),
                 "--root", root, "--rev", "WORKTREE"],
                capture_output=True, text=True)
            cases[name] = proc.returncode == code
            if code in (0, 1):
                payload = json.loads(proc.stdout)
                found = {f["code"] for f in payload.get("findings", [])}
                cases[name] = cases[name] and found == set(codes)
    print(json.dumps({"selftest": cases, "cases": len(cases),
                      "failures": [k for k, v in cases.items() if not v]},
                     indent=1, sort_keys=True))
    return 0 if all(cases.values()) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--generate", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.root and args.rev):
        print("registry-census: --root and --rev are required", file=sys.stderr)
        return 2
    try:
        doc = derive(args.root, args.rev)
    except CensusError as exc:
        print(json.dumps({"tool": TOOL, "unevaluable": str(exc), "exit": 2}),
              file=sys.stderr)
        return 2
    out, code = verdict(doc)
    if args.generate and not args.out:
        print("registry-census: --generate requires --out", file=sys.stderr)
        return 2
    text = json.dumps(out, indent=1, sort_keys=True)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
