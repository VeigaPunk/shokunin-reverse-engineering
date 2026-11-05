#!/usr/bin/env python
"""receipt-audit.py - freeze-receipt completeness gate.

Round 56 capability (R56-C2, depth).  M55-4 (corpus/lessons/round-55.md) and the
round-55 non-author closure's carry-in item 2: the frozen claims-container atom
T2 named ``freeze-gate-tip-90f3a9b9.json`` among the "freeze receipts committed",
but the freeze commit ``1f9be6eb`` silently dropped it (the pathspec named the
wrong round directory, and ``treecommit.py`` treats a path missing on disk as a
removal no-op).  M55-4's fix rule: "after every helper commit, re-derive the
landed path count against the intended list, and ``git cat-file -e`` every
receipt the container text claims was committed".  This gate is that rule as an
instrument.

Model: every receipt path a claims container's strings claim is checked against
the tree at --rev, read from git objects (``git cat-file -e REV:path``;
``git ls-tree -r --name-only REV -- .ufo/waves/round-N/``), never from a mutable
worktree - the same revision-pinned read discipline S255 grounds and S256
anchors.  Two extraction grammars over the container's JSON strings:

  full wave path  ``.ufo/waves/round-N/...`` ending .txt/.json/.tsv
                  -> must exist at --rev (repo-wide ``cat-file -e``)
  bare name       ``<name>.(txt|json|tsv)`` with no directory part
                  -> must resolve to exactly one path under the container's
                     OWN round scope ``.ufo/waves/round-N/**`` at --rev

``claims*.json`` files themselves are containers, not receipts, and are never
checked.  A bare name matching more than one path in scope fails closed
(RECEIPT_AMBIGUOUS) - the protocol's bare-name fail-closed rule; repo-wide bare
resolution is not offered because the wave tree carries dozen-plus same-named
receipts across rounds (``census-start.txt`` alone resolves to 12+ paths at the
round-56 base), which is exactly the ambiguity the round-scoped default avoids.

Verdict map: 0 = clean (every claimed receipt resolves at --rev, unambiguously
within its scope); 1 = failed (at least one RECEIPT_ABSENT or RECEIPT_AMBIGUOUS
finding, each named); 2 = could-not-evaluate (missing --claims/--rev, unknown
revision, unreadable claims JSON, or a failed git call).

--selftest runs the extractor and the scoped resolver over in-memory fixtures
(no git, no writes outside an optional --json-out) asserting both the exit class
and the finding id of every case; the committed-tree demonstrations in the
round-56 receipts are the second evidence.

Demonstrations on the committed tree (round 56 receipts):
  red    --claims .ufo/waves/round-55/claims.json --rev 1f9be6eb
             (the M55-4 event itself: T2's bare name freeze-gate-tip-90f3a9b9.json
             resolves to zero paths under round-55 at the freeze -> exit 1,
             RECEIPT_ABSENT)
  green  --claims .ufo/waves/round-56/claims.json --rev <round-56 freeze>
             (this round's own freeze: every claimed receipt present -> exit 0)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

FULL_PATH = re.compile(
    r"(?<![A-Za-z0-9_./-])(\.ufo/waves/round-[0-9]+/[A-Za-z0-9_./-]+\.(?:txt|json|tsv))"
    r"(?![A-Za-z0-9_-])")
BARE_NAME = re.compile(
    r"(?<![A-Za-z0-9_./-])([A-Za-z0-9_][A-Za-z0-9_.-]*\.(?:txt|json|tsv))(?![A-Za-z0-9_/-])")
CLAIMS_FILE = re.compile(r"^claims[A-Za-z0-9_.-]*\.json$")
ROUND_OF_CLAIMS = re.compile(r"^\.ufo/waves/(round-[0-9]+)/claims[A-Za-z0-9_.-]*\.json$")


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def strings(node) -> "iterator[str]":
    if isinstance(node, str):
        yield node
    elif isinstance(node, list):
        for item in node:
            yield from strings(item)
    elif isinstance(node, dict):
        for item in node.values():
            yield from strings(item)


def extract_receipts(texts) -> dict:
    """Return {"full": sorted set of wave paths, "bare": sorted set of names}."""
    full, bare = set(), set()
    for text in texts:
        for path in FULL_PATH.findall(text):
            if not CLAIMS_FILE.match(path.rsplit("/", 1)[-1]):
                full.add(path)
        for name in BARE_NAME.findall(text):
            if not CLAIMS_FILE.match(name):
                bare.add(name)
    return {"full": sorted(full), "bare": sorted(bare)}


def audit(receipts: dict, round_scope: str, path_exists, round_listing) -> dict:
    """path_exists(path) -> bool; round_listing() -> list of paths in scope."""
    findings = []
    checked = 0
    for path in receipts["full"]:
        checked += 1
        if not path_exists(path):
            findings.append({"finding": "RECEIPT_ABSENT", "name": path,
                             "scope": "repo"})
    scope_prefix = ".ufo/waves/%s/" % round_scope
    for name in receipts["bare"]:
        checked += 1
        matches = [p for p in round_listing()
                   if p.startswith(scope_prefix) and p.rsplit("/", 1)[-1] == name]
        if not matches:
            findings.append({"finding": "RECEIPT_ABSENT", "name": name,
                             "scope": round_scope})
        elif len(matches) > 1:
            findings.append({"finding": "RECEIPT_AMBIGUOUS", "name": name,
                             "scope": round_scope, "matches": sorted(matches)})
    findings.sort(key=lambda f: (f["finding"], f["name"]))
    verdict = "failed" if findings else "clean"
    return {"verdict": verdict,
            "exit": 1 if findings else 0,
            "round_scope": round_scope,
            "receipts_checked": checked,
            "findings": findings}


CASES = [
    ("green-unique-bare",
     {"full": [], "bare": ["receipt.txt"]}, "round-56",
     {"listing": [".ufo/waves/round-56/l1/receipt.txt"], "exists": {}},
     0, None),
    ("absent-bare",
     {"full": [], "bare": ["missing.txt"]}, "round-56",
     {"listing": [".ufo/waves/round-56/l1/other.txt"], "exists": {}},
     1, "RECEIPT_ABSENT"),
    ("ambiguous-bare",
     {"full": [], "bare": ["dup.txt"]}, "round-56",
     {"listing": [".ufo/waves/round-56/a/dup.txt", ".ufo/waves/round-56/b/dup.txt"],
      "exists": {}},
     1, "RECEIPT_AMBIGUOUS"),
    ("full-path-present",
     {"full": [".ufo/waves/round-56/l1/receipt.txt"], "bare": []}, "round-56",
     {"listing": [], "exists": {".ufo/waves/round-56/l1/receipt.txt": True}},
     0, None),
    ("full-path-absent",
     {"full": [".ufo/waves/round-99/l1/gone.txt"], "bare": []}, "round-56",
     {"listing": [], "exists": {}},
     1, "RECEIPT_ABSENT"),
    ("scope-isolates-rounds",
     {"full": [], "bare": ["receipt.txt"]}, "round-56",
     {"listing": [".ufo/waves/round-55/l1/receipt.txt",
                  ".ufo/waves/round-56/l1/receipt.txt",
                  ".ufo/waves/round-57/l1/receipt.txt"]},
     0, None),
    ("mixed-present-absent",
     {"full": [".ufo/waves/round-56/l1/here.txt"], "bare": ["gone.txt"]}, "round-56",
     {"listing": [".ufo/waves/round-56/l1/here.txt"],
      "exists": {".ufo/waves/round-56/l1/here.txt": True}},
     1, "RECEIPT_ABSENT"),
]


def selftest() -> int:
    failures = []
    extraction_cases = [
        ("claims-files-excluded",
         ["freeze receipts: claims.json claims-v2.json and census-start.txt; "
          "see corpus/x.tsv, plans/y.md, tools/z.py, .ufo/waves/round-9/claims.json"],
         {"full": [], "bare": ["census-start.txt"]}),
        ("full-path-and-dedupe",
         [".ufo/waves/round-56/l1/a.txt named again; bare a.txt; b.txt b.txt"],
         {"full": [".ufo/waves/round-56/l1/a.txt"], "bare": ["a.txt", "b.txt"]}),
    ]
    for name, texts, want in extraction_cases:
        got = extract_receipts(texts)
        if got != want:
            failures.append("%s: extracted %s != %s" % (name, got, want))
    for name, receipts, scope, fx, want_exit, want_finding in CASES:
        listing = fx["listing"]
        result = audit(receipts, scope,
                       path_exists=lambda p, fx=fx: fx["exists"].get(p, False),
                       round_listing=lambda listing=listing: listing)
        if result["exit"] != want_exit:
            failures.append("%s: exit %d != %d" % (name, result["exit"], want_exit))
            continue
        if want_finding is not None:
            got = {f["finding"] for f in result["findings"]}
            if want_finding not in got:
                failures.append("%s: findings %s lack %s"
                                % (name, sorted(got), want_finding))
        if result["verdict"] not in ("clean", "failed"):
            failures.append("%s: bad verdict %r" % (name, result["verdict"]))
    print("receipt-audit selftest: extraction %d + audit %d cases, failures %d%s"
          % (len(extraction_cases), len(CASES), len(failures),
             "" if not failures else "; failed: " + "; ".join(failures)))
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--claims")
    ap.add_argument("--rev")
    ap.add_argument("--round")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.claims or not args.rev:
        print("2 could-not-evaluate: --claims and --rev are required (or --selftest)",
              file=sys.stderr)
        return 2
    m = ROUND_OF_CLAIMS.match(args.claims)
    if not m and not args.round:
        print("2 could-not-evaluate: --claims path must match "
              ".ufo/waves/round-N/claims*.json (or pass --round)", file=sys.stderr)
        return 2
    round_scope = args.round or m.group(1)
    probe = git(args.root, "rev-parse", "--verify", "--end-of-options",
                args.rev + "^{commit}")
    if probe.returncode != 0:
        print("2 could-not-evaluate: unknown revision %s" % args.rev, file=sys.stderr)
        return 2
    rev = probe.stdout.decode().strip()
    raw = git(args.root, "cat-file", "blob", "%s:%s" % (rev, args.claims))
    if raw.returncode != 0:
        print("2 could-not-evaluate: claims file %s absent at %s"
              % (args.claims, rev), file=sys.stderr)
        return 2
    try:
        container = json.loads(raw.stdout.decode("utf-8"))
    except (UnicodeError, ValueError) as error:
        print("2 could-not-evaluate: unreadable claims JSON: %s" % error,
              file=sys.stderr)
        return 2

    def path_exists(path: str) -> bool:
        return git(args.root, "cat-file", "-e", "%s:%s" % (rev, path)).returncode == 0

    listing_cache = {}

    def round_listing() -> list:
        if "listing" not in listing_cache:
            out = git(args.root, "ls-tree", "-r", "--name-only", rev, "--",
                      ".ufo/waves/%s/" % round_scope)
            if out.returncode != 0:
                raise SystemExit("2 could-not-evaluate: git ls-tree failed for %s"
                                 % round_scope)
            listing_cache["listing"] = out.stdout.decode("utf-8", "replace").splitlines()
        return listing_cache["listing"]

    receipts = extract_receipts(list(strings(container)))
    result = audit(receipts, round_scope, path_exists, round_listing)
    result["claims"] = args.claims
    result["rev"] = rev
    rendered = json.dumps(result, indent=1, sort_keys=True)
    print(rendered)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(rendered + "\n")
    return result["exit"]


if __name__ == "__main__":
    sys.exit(main())
