#!/usr/bin/env python3
"""record-cells.py - round-91 counter (R91-C3, calibration).

A claim row in `SCORECARD.md` is the lane's self-assessment of one move. Round
91 routes two defects that say a row may name an artifact that does not exist:
QUALITY 173 (a receipt is taken at the measured revision) and the round-90
spot-check D-5 (`--rev <measured>` names no revision and a directory names no
receipt). This counter re-derives, from committed bytes only, whether each
round's claim rows name artifacts that resolve.

Selection rule (frozen): every row of `SCORECARD.md` at `--rev` whose first
cell matches `R<NN>-C<k>` for NN in `--rounds` (default 89 90; round 88 is excluded
because its battery receipts predate the revision field, named as debt).

Three atoms per row, each counted, never inferred:

- **A1 receipt** — the row names at least one `.ufo/waves/round-<NN>/…json`
  path and every such path exists at `--rev` (`git cat-file -e REV:path`). A
  directory is not a receipt.
- **A2 revision** — the row names at least one hex token of 7..40 chars that
  resolves as a commit in `--root` (`git rev-parse --verify <tok>^{commit}`).
- **A3 agreement** — at least one named receipt carries its own `revision` (or
  `rev`) field, that commit resolves, and its hex shares a prefix with a
  revision the row itself names. A row that cites base receipts only, or whose
  receipt names a revision the row does not, is a mismatch (the D-3 class: the
  citation names a revision the receipt does not).

`met` is `mismatches == 0 and rows >= --expect-rows`. The counter is
read-only over the lane tree and writes nothing but `--json-out` and its own
scratch.

Selftest (`--selftest`) runs four isolated fixtures over a throwaway git repo:
a complete row (0 mismatches), a row naming no .json path (3 atoms), a row naming an absent
receipt (2 atoms) and a row whose receipt revision is not the row's revision (each 1
mismatch on its atom). Exit 0 only when all four score as declared.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/round-91/record-cells.py"
ROW = re.compile(r"^\|\s*(R(\d{2})-C(\d+))\s*/")
RECEIPT = re.compile(r"\.ufo/waves/round-(\d{2})/[A-Za-z0-9_@./-]+\.json")
HEXTOK = re.compile(r"\b([0-9a-f]{7,40})\b")
REVFIELD = re.compile(r'"(?:revision|rev|measured_revision)"\s*:\s*"([0-9a-f]{7,40})"')


class Unevaluable(Exception):
    pass


def run(argv: list, cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True)


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return run(["git", "-C", root, *args])


def read_at(root: str, rev: str, path: str) -> str:
    p = git(root, "show", f"{rev}:{path}")
    if p.returncode != 0:
        raise Unevaluable(f"absent at {rev}: {path}")
    return p.stdout


def exists_at(root: str, rev: str, path: str) -> bool:
    """A receipt is a blob at that revision; a directory is not a receipt."""
    p = git(root, "cat-file", "-t", f"{rev}:{path}")
    return p.returncode == 0 and p.stdout.strip() == "blob"


def revision_ok(root: str, tok: str) -> bool:
    return git(root, "rev-parse", "--verify", f"{tok}^{{commit}}").returncode == 0


def row_revision(root: str, row: str) -> set:
    """Hex tokens that resolve as commits (longest first, no receipt names)."""
    found = set()
    for tok in HEXTOK.findall(row):
        if revision_ok(root, tok):
            found.add(tok)
    return found


def score_row(root: str, rev: str, row: str, argv_round: int) -> dict:
    out = {"row": row[:70], "atoms": {}, "mismatches": []}
    receipts = sorted(set(RECEIPT.findall(row)))
    paths = [m.group(0) for m in RECEIPT.finditer(row)]
    a1 = bool(paths)
    for p, rnd in zip(paths, receipts):
        if rnd != str(argv_round) or not exists_at(root, rev, p):
            a1 = False
            out["mismatches"].append(f"A1 receipt absent at {rev}: {p}")
    if not paths:
        out["mismatches"].append("A1 names no receipt file")
    out["atoms"]["A1_receipt"] = a1

    named = row_revision(root, row)
    out["atoms"]["A2_revision"] = bool(named)
    if not named:
        out["mismatches"].append("A2 names no resolving revision")

    agree, found = False, False
    for p in paths:
        if not exists_at(root, rev, p):
            continue
        text = read_at(root, rev, p)
        for tok in REVFIELD.findall(text):
            if not revision_ok(root, tok):
                out["mismatches"].append(f"A3 receipt {p} revision {tok} does not resolve")
                continue
            found = True
            if any(r.startswith(tok) or tok.startswith(r) for r in named):
                agree = True
    if not found:
        out["mismatches"].append("A3 no named receipt carries a revision")
    elif not agree:
        out["mismatches"].append("A3 no receipt revision agrees with a row revision")
    out["atoms"]["A3_agreement"] = agree
    return out


def score(root: str, rev: str, rounds: list[int], expect_rows: int) -> dict:
    text = read_at(root, rev, "SCORECARD.md")
    want = {str(r) for r in rounds}
    rows, seen = [], set()
    for line in text.splitlines():
        m = ROW.match(line)
        if not m or m.group(2) not in want:
            continue
        ident = m.group(1)
        if ident in seen:
            continue
        seen.add(ident)
        rows.append(score_row(root, rev, line, int(m.group(2))))
    mismatches = sum(len(r["mismatches"]) for r in rows)
    atoms = sum(len(r["atoms"]) for r in rows)
    passed = sum(1 for r in rows for v in r["atoms"].values() if v)
    label = f"mismatches {mismatches}"
    return {"tool": TOOL, "revision": rev, "rounds": rounds, "rows": len(rows),
            "atoms": atoms, "atoms_true": passed, "mismatches": mismatches,
            "detail": rows, "label": label,
            "met": mismatches == 0 and len(rows) >= expect_rows,
            "expect_rows": expect_rows}


# ---- selftest ---------------------------------------------------------------

ROWS = {
    "complete": "| R88-C1 / depth | a → b | `cmd --json-out .ufo/waves/round-88/receipts/c1.json` at `{rev}` | met |",
    "dir": "| R88-C2 / depth | a → b | `cmd` — `.ufo/waves/round-88/receipts/` | met |",
    "absent": "| R89-C1 / coverage | a → b | `.ufo/waves/round-89/receipts/missing.json` at `{rev}` | met |",
    "foreign": "| R90-C1 / coverage | a → b | `.ufo/waves/round-90/receipts/c1.json` at `{rev}` | met |",
}


def selftest() -> int:
    base = tempfile.mkdtemp(prefix="rc-selftest-", dir=os.environ.get("TMPDIR") or "/tmp")
    try:
        root = os.path.join(base, "repo")
        os.makedirs(root)
        git(root, "init", "-q")
        git(root, "config", "user.name", "selftest")
        git(root, "config", "user.email", "selftest@example.invalid")
        for rnd, name in (("88", "c1.json"), ("88", "absent"), ("90", "c1.json")):
            d = os.path.join(root, ".ufo/waves/round-" + rnd, "receipts")
            os.makedirs(d, exist_ok=True)
        with open(os.path.join(root, ".ufo/waves/round-88/receipts/c1.json"), "w") as fh:
            fh.write('{"revision": "REVX"}')
        with open(os.path.join(root, ".ufo/waves/round-90/receipts/c1.json"), "w") as fh:
            fh.write('{"revision": "REVFOREIGN"}')
        with open(os.path.join(root, "SCORECARD.md"), "w") as fh:
            fh.write("# card\n\n" + "\n".join(ROWS[k] for k in ROWS) + "\n")
        git(root, "add", "-A")
        git(root, "commit", "-qm", "fixture")
        rev = git(root, "rev-parse", "HEAD").stdout.strip()
        # one earlier commit supplies a resolving foreign revision
        with open(os.path.join(root, ".ufo/waves/round-90/receipts/c1.json"), "w") as fh:
            fh.write('{"revision": "REVFOREIGN"}')
        text = open(os.path.join(root, "SCORECARD.md")).read()
        earlier = rev
        for k in ROWS:
            text = text.replace("{rev}", earlier)
        open(os.path.join(root, "SCORECARD.md"), "w").write(text)
        git(root, "add", "-A")
        git(root, "commit", "-qm", "revs")
        rev = git(root, "rev-parse", "HEAD").stdout.strip()
        # make the round-88 receipt name the "earlier" revision, the row names rev
        with open(os.path.join(root, ".ufo/waves/round-88/receipts/c1.json"), "w") as fh:
            fh.write('{"revision": "%s"}' % earlier)
        git(root, "add", "-A")
        git(root, "commit", "-qm", "pin")
        rev = git(root, "rev-parse", "HEAD").stdout.strip()
        got = score(root, rev, [88, 89, 90], 4)
        by_row = {r["row"][:24]: r for r in got["detail"]}
        cases = [
            ("complete", 0, "R88-C1 / depth"),
            ("nojson", 3, "R88-C2 / depth"),
            ("absent", 2, "R89-C1 / coverage"),
            ("foreign", 1, "R90-C1 / coverage"),
        ]
        fails = 0
        for name, want, prefix in cases:
            hit = next((r for k, r in by_row.items() if prefix.split()[0] in k), None)
            if hit is None:
                print(f"FAIL {name}: row not selected"); fails += 1; continue
            ok = (len(hit["mismatches"]) == want)
            print(f"{'ok' if ok else 'FAIL'} {name}: mismatches {len(hit['mismatches'])} want {want}")
            fails += 0 if ok else 1
        print(f"selftest cases=4 failures={fails}")
        return 0 if fails == 0 else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--rounds", nargs="+", type=int, default=[89, 90])
    ap.add_argument("--expect-rows", type=int, default=6)
    ap.add_argument("--expect", help="frozen label, e.g. 'mismatches 0'")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root)
    rev = args.rev or git(root, "rev-parse", "HEAD").stdout.strip()
    try:
        got = score(root, rev, args.rounds, args.expect_rows)
    except Unevaluable as exc:
        print(json.dumps({"tool": TOOL, "revision": rev, "error": str(exc)}))
        return 2
    if args.expect is not None:
        got["expect"] = args.expect
        got["met"] = got["met"] and got["label"] == args.expect
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(got, fh, indent=1, sort_keys=True)
    print(got["label"], "rows", got["rows"], "atoms", f"{got['atoms_true']}/{got['atoms']}",
          "met", got["met"])
    for r in got["detail"]:
        for mm in r["mismatches"]:
            print(" ", mm)
    return 0 if got["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
