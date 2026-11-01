#!/usr/bin/env python
"""v6-block-digest.py - reproducible digest of the SKILL.md triage-table v6 block.

Round 55 repair for routed defect "v6-table digest not reproducible from the
receipt" (corpus/lessons/round-54-verifier-spotcheck.md section 5 item 3): the
round-54 receipt printed the 16-hex prefix ``b340ed2b48facca7`` without naming
its extraction command; this probe defines THE extraction so the value is
re-derivable by anyone.

Extraction (deterministic, bytes only):
  1. read SKILL.md at --rev from git objects (``git show REV:SKILL.md``);
  2. split on b"\\n" (the blob has no carriage returns; the splitter is the
     definition, not an assumption about the file);
  3. find the single line containing the literal marker
     ``<!-- sqfs-triage-table v6 -->`` (first match; two matches refuse);
  4. from the next line, find the first line whose lstrip() starts with b"|"
     (the table header); the actions comment line above it is included;
  5. extend through every consecutive line whose lstrip() starts with b"|"
     (header, separator, data rows; the first non-| line ends the block);
  6. the block is marker line .. last ``|`` line inclusive, joined with
     b"\\n" plus one trailing b"\\n".

Verdict: 0 = digest printed (stdout JSON and --json-out when given);
2 = could-not-evaluate (marker absent or ambiguous, SKILL.md absent at the
revision, unknown revision, bad arguments).  Exit 1 is reserved for --selftest
failures.  This probe never writes inside the lane tree; --json-out only.

Pinned reference values (2026-11-01, round 55): the digest at the round-53
base 45c6878634c16caa8e3e63472b30e439581b3a0d, the round-54 landing
c753b24f96db335eeeca0003d2906457d6e71849, the round-54 close
90f3a9b9d3970ae87173787521a821132c10c66c and the round-55 base
79421b757f36b2ddb776631ecfd57d42dc2f33e2 is
946e535947ba6d17da9f4b1ca7993af285e66103547a5c2107b253e5dd204bcc
(23 lines, 8961 bytes).  The round-54 receipt's ``b340ed2b48facca7`` was NOT
reproduced by this extraction (disclosure in the round-55 receipt
.ufo/waves/round-55/l1/records/v6-digest-repro.txt); byte-identity across the
revisions - the claim the receipt supported - holds under this command and
held independently under the round-54 closure's three extraction boundaries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys

MARKER = b"<!-- sqfs-triage-table v6 -->"
SELFTEST_MARK = "v6-block-digest selftest"


def git_show(root: str, rev: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", root, "show", rev + ":" + path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise SystemExit("2 could-not-evaluate: git show failed for %s:%s: %s"
                         % (rev, path, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def extract_block(blob: bytes) -> bytes:
    lines = blob.split(b"\n")
    marker_at = [i for i, ln in enumerate(lines) if MARKER in ln]
    if not marker_at:
        raise SystemExit("2 could-not-evaluate: marker %r absent" % MARKER.decode())
    if len(marker_at) > 1:
        raise SystemExit("2 could-not-evaluate: marker appears %d times" % len(marker_at))
    mi = marker_at[0]
    ts = None
    for i in range(mi + 1, len(lines)):
        if lines[i].lstrip().startswith(b"|"):
            ts = i
            break
    if ts is None:
        raise SystemExit("2 could-not-evaluate: no markdown table row after the marker")
    end = ts
    while end + 1 < len(lines) and lines[end + 1].lstrip().startswith(b"|"):
        end += 1
    return b"\n".join(lines[mi:end + 1]) + b"\n"


def digest_at(root: str, rev: str, path: str) -> dict:
    blob = git_show(root, rev, path)
    block = extract_block(blob)
    return {
        "rev": rev,
        "path": path,
        "sha256": hashlib.sha256(block).hexdigest(),
        "lines": block.count(b"\n"),
        "bytes": len(block),
        "marker": MARKER.decode(),
        "extraction": "marker line through the last consecutive '|'-leading line, "
                      "LF-joined with one trailing LF (see module docstring)",
    }


def selftest() -> int:
    good = (
        b"prose before\n"
        b"  " + MARKER + b"\n"
        b"  <!-- sqfs-triage-actions: a b c -->\n"
        b"  | h1 | h2 |\n"
        b"  | --- | --- |\n"
        b"  | r1 | x |\n"
        b"  | r2 | y |\n"
        b"\n"
        b"- **28. next block.**\n"
    )
    block = extract_block(good)
    want = b"\n".join(good.split(b"\n")[1:7]) + b"\n"
    checks = [("block bytes", block == want)]
    checks.append(("digest stable", hashlib.sha256(block).hexdigest()
                   == hashlib.sha256(want).hexdigest()))
    trailing = good.replace(b"  | r2 | y |\n", b"  | r2 | y |   \n")
    checks.append(("trailing-space row included, digest changes",
                   extract_block(trailing) != block))
    try:
        extract_block(b"no marker here\n")
        checks.append(("marker absent refuses", False))
    except SystemExit as exc:
        checks.append(("marker absent refuses", str(exc).startswith("2")))
    two = b"  " + MARKER + b"\n\n  " + MARKER + b"\n"
    try:
        extract_block(two)
        checks.append(("ambiguous marker refuses", False))
    except SystemExit as exc:
        checks.append(("ambiguous marker refuses", str(exc).startswith("2")))
    failed = [name for name, ok in checks if not ok]
    print("%s: cases %d, failures %d%s" % (
        SELFTEST_MARK, len(checks), len(failed),
        "" if not failed else "; failed: " + ", ".join(failed)))
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--path", default="SKILL.md")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.rev:
        print("2 could-not-evaluate: --rev is required (or use --selftest)",
              file=sys.stderr)
        return 2
    result = digest_at(args.root, args.rev, args.path)
    rendered = json.dumps(result, indent=1, sort_keys=True)
    print(rendered)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(rendered + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
