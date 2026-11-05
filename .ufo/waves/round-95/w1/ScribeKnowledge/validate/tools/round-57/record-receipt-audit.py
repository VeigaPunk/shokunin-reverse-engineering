#!/usr/bin/env python
"""record-receipt-audit.py - the M56-4 rule extended: every file a record section names must resolve.

Round 57 capability (R57-C2, depth).  M56-4 (corpus/lessons/round-56.md) and the
round-56 non-author closure's routed defect D4: a record section's receipts list
may name files that were never passed to the commit helper, so they exist only in
the worktree; the round-56 post-close correction landed the two receipts its own
audit caught but missed a third named receipt
(``.ufo/waves/round-56/l1/records/receipt-audit-green-r56.txt``) because the audit
diffed the tree against the two receipts named by the M56-4 lesson row instead of
against EVERY file the record section names.  D4's fix clause: "extend M56-4's
rule to diff ``git ls-tree`` against EVERY file the record names, not the two it
caught."  This instrument is that extension.

Model: the record section's committed bytes (``git show REV:RECORD`` - never the
worktree) are sliced to one ``##``-heading section, every backtick-quoted path
starting ``.ufo/waves/round-N/`` is extracted (duplicates collapsed), and each is
resolved by exact match against ``git ls-tree -r --name-only REV`` - one listing,
one revision, git objects only, nothing written.

Verdict map: 0 = clean (at least one path named, every one resolves at REV);
1 = missing (at least one NAMED_PATH_ABSENT finding, each named);
2 = could-not-evaluate (record or section absent at REV, zero paths extracted,
unknown revision, or a failed git call).  A section naming nothing is
unevaluable, never vacuously clean (the QUALITY #66 boundary).

Limits: backtick-quoted full ``.ufo/waves/round-N/...`` paths only - a receipt
named without backticks, under another directory, or via the records tables'
``.../scores/<name>`` shorthand cells is not seen; exact-path match at a single
revision; paths are checked for existence in the tree, never for content.

--selftest runs the extractor, the section slicer and the audit over in-memory
fixtures (no git, no writes outside an optional --json-out) asserting the exit
class, the finding id and the extracted set of every case; the committed-tree
demonstrations in the round-57 receipts are the second evidence.

Demonstrations on the committed tree (round 57 receipts):
  red    --record SCORECARD.md --heading "Round 56" --rev <r57 base 63413677>
             (the D4 defect itself: the r56 record section names 13 receipts but
             receipt-audit-green-r56.txt resolves to nothing in the tree -> exit 1)
  green  the same section at the round-57 carry-in landing, after the receipt
             lands -> exit 0, every named path resolves
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

NAMED_PATH = re.compile(r"`(\.ufo/waves/round-[0-9]+/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+)`")


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def slice_section(text: str, heading: str):
    """Return the lines from the first '## ' heading containing `heading`
    to the next '## ' heading, or None when no heading matches."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and heading in line:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def extract_paths(text: str) -> list:
    """Sorted, duplicate-collapsed backtick-quoted .ufo/waves/round-N/ file paths."""
    return sorted(set(NAMED_PATH.findall(text)))


def audit(paths: list, listing: list) -> dict:
    """listing: the full `git ls-tree -r --name-only REV` output lines.
    Zero named paths is unevaluable, never vacuously clean (QUALITY #66)."""
    present = set(listing)
    if not paths:
        return {"verdict": "unevaluable", "exit": 2, "named": 0,
                "missing": 0, "findings": []}
    findings = [{"finding": "NAMED_PATH_ABSENT", "name": path}
                for path in paths if path not in present]
    verdict = "missing" if findings else "clean"
    return {"verdict": verdict,
            "exit": 1 if findings else 0,
            "named": len(paths),
            "missing": len(findings),
            "findings": findings}


CASES = [
    ("all-present", [".ufo/waves/round-56/l1/a.txt",
                     ".ufo/waves/round-56/l1/b.json"],
     [".ufo/waves/round-56/l1/a.txt", ".ufo/waves/round-56/l1/b.json"],
     0, None, 2),
    ("one-missing-named",
     [".ufo/waves/round-56/l1/a.txt", ".ufo/waves/round-56/l1/gone.txt"],
     [".ufo/waves/round-56/l1/a.txt"],
     1, "NAMED_PATH_ABSENT", 2),
    ("duplicate-collapsed",
     [".ufo/waves/round-56/l1/a.txt"],
     [".ufo/waves/round-56/l1/a.txt"],
     0, None, 1),
    ("zero-named-unevaluable", [], ["anything"], 2, None, 0),
]


def selftest() -> int:
    failures = []
    extraction_cases = [
        ("list-and-table-cells-dedupe-nonwave-ignored",
         "- `.ufo/waves/round-56/l1/scores/c1-after.txt` rev=x\n"
         "- `.ufo/waves/round-56/l1/scores/c1-after.txt` again\n"
         "| r | see `.ufo/waves/round-56/l1/scores/c2-after.txt` |\n"
         "the `tools/round-56/receipt-audit.py` and `corpus/lessons/round-56.md` "
         "are not wave paths; `.../scores/shorthand.txt` is not extracted\n",
         [".ufo/waves/round-56/l1/scores/c1-after.txt",
          ".ufo/waves/round-56/l1/scores/c2-after.txt"]),
        ("claims-json-and-html-count-as-named-files",
         "the freeze adds `.ufo/waves/round-56/claims.json` and the snapshot "
         "`.ufo/waves/round-56/l1/s256/git-cat-file.html`\n",
         [".ufo/waves/round-56/claims.json",
          ".ufo/waves/round-56/l1/s256/git-cat-file.html"]),
        ("trailing-punct-and-nested-rounds-ok",
         "(`.ufo/waves/round-55/claims.json`; receipt `.ufo/waves/round-57/l1/x.txt`.)\n",
         [".ufo/waves/round-55/claims.json", ".ufo/waves/round-57/l1/x.txt"]),
    ]
    for name, text, want in extraction_cases:
        got = extract_paths(text)
        if got != want:
            failures.append("%s: extracted %s != %s" % (name, got, want))
    section_cases = [
        ("sliced-to-next-heading",
         "## Round 55\nold `.ufo/waves/round-55/l1/old.txt`\n"
         "## Round 56 (the one wanted)\nnew `.ufo/waves/round-56/l1/new.txt`\n"
         "## Round 57\nlater `.ufo/waves/round-57/l1/later.txt`\n",
         "Round 56",
         [".ufo/waves/round-56/l1/new.txt"]),
        ("heading-absent",
         "## Round 55\nbody\n", "Round 99", None),
    ]
    for name, text, heading, want in section_cases:
        got = slice_section(text, heading)
        if want is None:
            if got is not None:
                failures.append("%s: expected None, got %r" % (name, got))
        else:
            if got is None:
                failures.append("%s: expected a section, got None" % name)
            else:
                got_paths = extract_paths(got)
                if got_paths != want:
                    failures.append("%s: section extracted %s != %s"
                                    % (name, got_paths, want))
    for name, paths, listing, want_exit, want_finding, want_named in CASES:
        result = audit(paths, listing)
        if result["exit"] != want_exit:
            failures.append("%s: exit %d != %d" % (name, result["exit"], want_exit))
            continue
        if result["named"] != want_named:
            failures.append("%s: named %d != %d" % (name, result["named"], want_named))
        if want_finding is not None:
            got = {f["finding"] for f in result["findings"]}
            if want_finding not in got:
                failures.append("%s: findings %s lack %s"
                                % (name, sorted(got), want_finding))
        if result["verdict"] not in ("clean", "missing", "unevaluable"):
            failures.append("%s: bad verdict %r" % (name, result["verdict"]))
    print("record-receipt-audit selftest: extraction %d + section %d + audit %d "
          "cases, failures %d%s"
          % (len(extraction_cases), len(section_cases), len(CASES), len(failures),
             "" if not failures else "; failed: " + "; ".join(failures)))
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--record")
    ap.add_argument("--heading")
    ap.add_argument("--rev")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.record or not args.heading or not args.rev:
        print("2 could-not-evaluate: --record, --heading and --rev are required "
              "(or --selftest)", file=sys.stderr)
        return 2
    probe = git(args.root, "rev-parse", "--verify", "--end-of-options",
                args.rev + "^{commit}")
    if probe.returncode != 0:
        print("2 could-not-evaluate: unknown revision %s" % args.rev, file=sys.stderr)
        return 2
    rev = probe.stdout.decode().strip()
    raw = git(args.root, "cat-file", "blob", "%s:%s" % (rev, args.record))
    if raw.returncode != 0:
        print("2 could-not-evaluate: record %s absent at %s" % (args.record, rev),
              file=sys.stderr)
        return 2
    section = slice_section(raw.stdout.decode("utf-8", "replace"), args.heading)
    if section is None:
        print("2 could-not-evaluate: no '## ' heading matching %r in %s at %s"
              % (args.heading, args.record, rev), file=sys.stderr)
        return 2
    listing_out = git(args.root, "ls-tree", "-r", "--name-only", rev)
    if listing_out.returncode != 0:
        print("2 could-not-evaluate: git ls-tree failed for %s" % rev, file=sys.stderr)
        return 2
    listing = listing_out.stdout.decode("utf-8", "replace").splitlines()
    paths = extract_paths(section)
    result = audit(paths, listing)
    result["record"] = args.record
    result["heading"] = args.heading
    result["rev"] = rev
    rendered = json.dumps(result, indent=1, sort_keys=True)
    print(rendered)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(rendered + "\n")
    return result["exit"]


if __name__ == "__main__":
    sys.exit(main())
