#!/usr/bin/env python
"""numstat-edge-audit.py - edge-labeled numstat claim gate.

Round 61 capability (R61-C2, depth).  The r60 non-author closure's routed
defect D60-1 (corpus/lessons/round-60-verifier-spotcheck.md, note 1): the
after-receipt `.ufo/waves/round-60/l1/scores/c1-after.txt` says "SKILL delta
landing->record exactly `1 0` by numstat", but the `1 0` numstat is the
freeze->landing edge (the landing commit bbdb03ab added the registry row);
the landing->record edge re-derives to 0 0.  The same mislabel sits in two
sibling sites of the round: the LOG round-60 close entry ("the SKILL delta
landing->record exactly `1 0`") and the SCORECARD round-60 atom T7 ("the
SKILL delta landing->tip exactly `1 0`"; landing->tip re-derives 0 0,
base->tip is 1 0).  The class: an edge-labeled delta claim whose named edge
differs from the edge the numbers were actually taken over.  This gate is
that class as an instrument (the M57-1 / D58-1 lineage).

Model: a receipt's committed bytes (`git show REV:RECEIPT` - never the
worktree) are scanned for two shapes:

  binding    a rev-name binding: a lowercase name token, an optional
             ``commit``/``rev`` word, then a 40-hex commit id - e.g. "the
             record commit 29083b0c...", "operative freeze 8e583663...",
             "and the landing bbdb03ab...".  First occurrence of a name
             wins.  A 64-hex sha256 does NOT bind (a negative lookahead
             rejects hex run-ons).  Callers may supply additional context
             with --name NAME=HEX (recorded in the JSON output as
             caller-supplied - the receipt bytes do not carry them).
  edge claim a line matching
             (SKILL|LOG|SCORECARD|PROVINCE) delta <a>-><b> exactly `<x> <y>`
             where <a>,<b> are rev names and the arrow is U+2192.  The
             subject word maps to the repo file: SKILL->SKILL.md,
             LOG->LOG.md, SCORECARD->SCORECARD.md, PROVINCE->PROVINCE.md.
             The ASCII ``->`` form and the ``A..B`` dot form are outside
             this grammar (out of scope, not findings, like the r59 gate's
             unannotated commands).

Every edge claim is re-derived:

  $ git -C root diff --numstat --no-numstat... --no-color --no-renames X Y -- path

  absent row  -> measured (0, 0)
  "-" counts  -> NUMSTAT_BINARY (fail-closed: git-diff docs, the --numstat
              definition - binary files output two "-" instead of saying
              0 0, so a binary edge is not a count this gate can compare)
  claimed (x, y) != measured (add, del)
              -> NUMSTAT_EDGE_MISMATCH (the D60-1 defect itself fires here)
  a claim name with no binding and no override
              -> NUMSTAT_NAME_UNRESOLVED (fail-closed: a claim this gate
              cannot check is a finding, never a pass)

Verdict map: 0 = clean (at least one edge claim, every one re-derives);
1 = defect (any finding, each named); 2 = could-not-evaluate (zero edge
claims in the grammar, receipt absent at REV, unknown revision, failed git
call).  A receipt claiming nothing in this grammar is unevaluable, never
vacuously clean (the QUALITY #66 boundary).

Limits: one receipt per run; the arrow grammar above only (a receipt that
phrases its deltas differently is unevaluable, not clean); internal
bindings require the full 40-hex form (abbreviated hashes + ellipsis, as
SCORECARD sections print them, do not resolve - supply --name overrides);
a correction appended AFTER a defective claim does not clear it - filed
bytes stay as filed, so a receipt whose historical claim contradicts its
own edge keeps firing forever (that persistent state is receipted, not
repaired away).

--selftest runs the extractor, the resolver and the audit over in-memory
fixtures with an injected git runner (no git, no writes outside an optional
--json-out) asserting the exit class, the finding ids and the values of
every case; the committed-tree demonstrations in the round-61 receipts are
the second evidence.

Demonstrations on the committed tree (round-61 receipts):
  red    --receipt .ufo/waves/round-60/l1/scores/c1-after.txt --rev 2d976fba...
             (the D60-1 defect as filed: exit 1, NUMSTAT_EDGE_MISMATCH -
             claims 1 0, re-derives 0 0; internal bindings from the header)
  red    --receipt SCORECARD.md --rev <r61 base> --name landing=... --name tip=...
             (the T7 sibling: exit 1, NUMSTAT_EDGE_MISMATCH; the r59 T8
             freeze->fixup `1 0` claim on the same run re-derives green)
  red    --receipt LOG.md --rev <r60 close> --name landing=... --name record=...
             (the LOG close-entry sibling: exit 1; the r59 entry's
             freeze->fixup `1 0` claim re-derives green)
  green  --receipt .ufo/waves/round-61/l1/scores/d601-correction.txt --rev <landing>
             (the round-61 correction receipt: every edge claim re-derives,
             exit 0)
  red-2  --receipt SCORECARD.md --rev <r61 base>  (no overrides: the T7/T8
             names do not resolve from the section's abbreviated hashes ->
             NUMSTAT_NAME_UNRESOLVED, the fail-closed arm)
  exit-2 --receipt .ufo/waves/round-59/l1/scores/d581-correction.txt --rev ...
             (a receipt with zero claims in this grammar: unevaluable)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

TOOL = "tools/round-61/numstat-edge-audit.py"

SUBJECT_PATH = {
    "SKILL": "SKILL.md",
    "LOG": "LOG.md",
    "SCORECARD": "SCORECARD.md",
    "PROVINCE": "PROVINCE.md",
}

BINDING_RE = re.compile(
    r"(?P<name>[a-z][a-z-]*)\s+(?:commit\s+|rev\s+)?`?(?P<hex>[\da-f]{40})(?![\da-f])`?"
)
CLAIM_RE = re.compile(
    r"(?P<subject>SKILL|LOG|SCORECARD|PROVINCE)\s+delta\s+"
    r"(?P<a>[a-z][a-z-]*)\s*\u2192\s*(?P<b>[a-z][a-z-]*)\s+"
    r"exactly\s+`(?P<x>\d+)\s+(?P<y>\d+)`"
)

FINDING_EDGE = "NUMSTAT_EDGE_MISMATCH"
FINDING_NAME = "NUMSTAT_NAME_UNRESOLVED"
FINDING_BINARY = "NUMSTAT_BINARY"


def extract_bindings(text):
    """name -> 40-hex, first occurrence wins, in scan order."""
    found = {}
    for m in BINDING_RE.finditer(text):
        name = m.group("name")
        if name not in found:
            found[name] = m.group("hex")
    return found


def extract_claims(text):
    """Edge claims as dicts with receipt line numbers (1-based)."""
    claims = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in CLAIM_RE.finditer(line):
            claims.append(
                {
                    "line": lineno,
                    "subject": m.group("subject"),
                    "path": SUBJECT_PATH[m.group("subject")],
                    "a": m.group("a"),
                    "b": m.group("b"),
                    "claimed": [int(m.group("x")), int(m.group("y"))],
                }
            )
    return claims


def parse_numstat(stdout, path):
    """Return ('counts', (add, del)) | ('binary', None) | ('absent', (0, 0))."""
    for line in stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        add, dele, fpath = parts[0], parts[1], "\t".join(parts[2:])
        if fpath != path:
            continue
        if add == "-" or dele == "-":
            return ("binary", None)
        return ("counts", (int(add), int(dele)))
    return ("absent", (0, 0))


def audit(root, receipt_path, rev, overrides=None, runner=None):
    """Audit one receipt's edge claims at one revision."""
    overrides = overrides or {}
    findings = []
    if runner is None:
        runner = default_runner
    rc, out, err = runner(["git", "-C", root, "show", f"{rev}:{receipt_path}"])
    if rc != 0:
        return {
            "receipt": receipt_path,
            "rev": rev,
            "claims_found": 0,
            "findings": [],
            "exit": 2,
            "exit_reason": f"receipt absent at REV or unreadable: {err.strip()[:120]}",
            "bindings_used": {},
            "caller_supplied_names": sorted(overrides),
        }
    text = out.decode("utf-8", errors="replace")
    claims = extract_claims(text)
    if not claims:
        return {
            "receipt": receipt_path,
            "rev": rev,
            "claims_found": 0,
            "findings": [],
            "exit": 2,
            "exit_reason": "no edge claim in the gate grammar (unevaluable, never clean)",
            "bindings_used": {},
            "caller_supplied_names": sorted(overrides),
        }
    internal = extract_bindings(text)
    bindings = dict(internal)
    for name, hexv in overrides.items():
        bindings[name] = hexv
    for claim in claims:
        missing = [n for n in (claim["a"], claim["b"]) if n not in bindings]
        if missing:
            findings.append(
                {
                    "class": FINDING_NAME,
                    "line": claim["line"],
                    "detail": (
                        f"{claim['subject']} delta {claim['a']}\u2192{claim['b']}: "
                        f"name(s) {', '.join(missing)} unresolvable from the receipt's "
                        f"bindings or caller overrides"
                    ),
                }
            )
            continue
        xa, xb = bindings[claim["a"]], bindings[claim["b"]]
        grc, gout, gerr = runner(
            [
                "git", "-C", root, "diff", "--numstat", "--no-color", "--no-renames",
                xa, xb, "--", claim["path"],
            ]
        )
        if grc != 0:
            findings.append(
                {
                    "class": FINDING_NAME,
                    "line": claim["line"],
                    "detail": (
                        f"git diff failed for {claim['path']} "
                        f"{xa[:12]}..{xb[:12]}: {gerr.strip()[:120]}"
                    ),
                }
            )
            continue
        kind, measured = parse_numstat(gout.decode("utf-8", errors="replace"), claim["path"])
        if kind == "binary":
            findings.append(
                {
                    "class": FINDING_BINARY,
                    "line": claim["line"],
                    "detail": (
                        f"{claim['subject']} delta {claim['a']}\u2192{claim['b']} "
                        f"claimed {claim['claimed'][0]} {claim['claimed'][1]} but the edge "
                        f"is binary (numstat prints - -), not a count"
                    ),
                }
            )
            continue
        if measured != tuple(claim["claimed"]):
            findings.append(
                {
                    "class": FINDING_EDGE,
                    "line": claim["line"],
                    "detail": (
                        f"{claim['subject']} delta {claim['a']}\u2192{claim['b']} "
                        f"({claim['path']}) claims {claim['claimed'][0]} {claim['claimed'][1]} "
                        f"but the edge re-derives to {measured[0]} {measured[1]} "
                        f"at {xa[:12]}..{xb[:12]}"
                    ),
                }
            )
    used = {
        n: bindings.get(n, "<unresolved>")
        for n in sorted({c["a"] for c in claims} | {c["b"] for c in claims})
    }
    if findings:
        exit_code, reason = 1, f"{len(findings)} finding(s) named"
    else:
        exit_code, reason = 0, "every edge claim re-derives"
    return {
        "receipt": receipt_path,
        "rev": rev,
        "claims_found": len(claims),
        "findings": findings,
        "exit": exit_code,
        "exit_reason": reason,
        "bindings_used": used,
        "caller_supplied_names": sorted(overrides),
    }


def default_runner(argv):
    proc = subprocess.run(argv, capture_output=True)
    return proc.returncode, proc.stdout, proc.stderr


def parse_overrides(pairs):
    overrides = {}
    for item in pairs or []:
        if "=" not in item:
            raise SystemExit(f"numstat-edge-audit: --name expects NAME=HEX, got {item!r}")
        name, hexv = item.split("=", 1)
        if not re.fullmatch(r"[a-z][a-z-]*", name) or not re.fullmatch(r"[\da-f]{40}", hexv):
            raise SystemExit(
                f"numstat-edge-audit: --name expects NAME=lowercase and a 40-hex commit id, "
                f"got {item!r}"
            )
        overrides[name] = hexv
    return overrides


def selftest():
    """In-memory cases; an injected runner replaces git entirely."""
    FULL_A = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    FULL_B = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    FULL_C = "cccccccccccccccccccccccccccccccccccccccc"

    class Fixture:
        def __init__(self):
            self.blobs = {}
            self.diffs = {}

    def runner_for(fx):
        def run(argv):
            if argv[:4] == ["git", "-C", "root", "show"]:
                rev, path = argv[4].split(":", 1)
                blob = fx.blobs.get((rev, path))
                if blob is None:
                    return (128, b"", b"fatal: not in rev")
                return (0, blob.encode("utf-8"), b"")
            if argv[:4] == ["git", "-C", "root", "diff"]:
                xa, xb = argv[-4], argv[-3]
                path = argv[-1]
                return (0, fx.diffs.get((xa, xb, path), b"").encode("utf-8"), b"")
            return (2, b"", b"unexpected argv")

        return run

    cases = []

    def check(name, got, want):
        cases.append({"case": name, "ok": got == want, "got": got, "want": want})

    # --- extraction ---
    text = (
        "measured at the record commit %s, a descendant of the operative freeze %s "
        "and the landing %s\nthe SKILL delta landing\u2192record exactly `1 0` by numstat\n"
        % (FULL_B, FULL_A, FULL_C)
    )
    b = extract_bindings(text)
    check("binding record-commit-word", b.get("record"), FULL_B)
    check("binding freeze-no-commit-word", b.get("freeze"), FULL_A)
    check("binding landing-bare", b.get("landing"), FULL_C)

    b2 = extract_bindings("the sha passed to sha256 `%s` re-hashed\n" % ("1234567890" * 6 + "abcd"))
    check("non-binding sha256-64hex", b2, {})

    b3 = extract_bindings("rev=%s check=x\n" % FULL_A)
    check("non-binding rev-equals", b3, {})

    b4 = extract_bindings(
        "the record commit %s noted; later the record commit %s again\n" % (FULL_A, FULL_B)
    )
    check("binding first-occurrence-wins", b4.get("record"), FULL_A)

    c1 = extract_claims("the SKILL delta landing\u2192record exactly `1 0` by numstat\n")
    check(
        "claim-extract arrow",
        (c1[0]["subject"], c1[0]["a"], c1[0]["b"], c1[0]["claimed"], c1[0]["path"]),
        ("SKILL", "landing", "record", [1, 0], "SKILL.md"),
    )

    c2 = extract_claims("LOG base\u2192record exactly 38 0; owned-axes rows byte-equal\n")
    check("out-of-scope no-backticks", c2, [])

    c3 = extract_claims("the SKILL delta freeze..landing exactly `1 0`\n")
    check("out-of-scope dot-form", c3, [])

    c4 = extract_claims("byte-identical freeze->record - the landing edited nothing filed\n")
    check("out-of-scope ascii-arrow", c4, [])

    c5 = extract_claims("the SCORECARD delta of this record commit reads 625/1\n")
    check("out-of-scope reads-form", c5, [])

    c6 = extract_claims("PROVINCE diff empty base\u2192record\n")
    check("out-of-scope no-delta-word", c6, [])

    # --- audit outcomes (injected runner) ---
    fx = Fixture()
    receipt = "r/w.txt"
    fx.blobs[(FULL_B, receipt)] = (
        "header: the freeze %s and the landing %s and the record commit %s\n"
        "the SKILL delta landing\u2192record exactly `1 0` by numstat\n"
        % (FULL_A, FULL_C, FULL_B)
    )
    fx.diffs[(FULL_C, FULL_B, "SKILL.md")] = ""  # landing->record: no change
    got = audit("root", receipt, FULL_B, runner=runner_for(fx))
    check(
        "audit-red-d601",
        (got["exit"], got["findings"][0]["class"], "claims 1 0" in got["findings"][0]["detail"]),
        (1, FINDING_EDGE, True),
    )

    fx2 = Fixture()
    fx2.blobs[(FULL_B, receipt)] = (
        "the freeze %s and the landing %s\n"
        "the SKILL delta freeze\u2192landing exactly `0 0` (corrected)\n" % (FULL_A, FULL_C)
    )
    fx2.diffs[(FULL_A, FULL_C, "SKILL.md")] = ""
    got2 = audit("root", receipt, FULL_B, runner=runner_for(fx2))
    check("audit-green-corrected", (got2["exit"], got2["findings"]), (0, []))

    fx3 = Fixture()
    fx3.blobs[(FULL_B, receipt)] = "the SKILL delta landing\u2192record exactly `1 0`\n"
    got3 = audit("root", receipt, FULL_B, runner=runner_for(fx3))
    check(
        "audit-name-unresolved-failclosed",
        (got3["exit"], got3["findings"][0]["class"]),
        (1, FINDING_NAME),
    )

    fx4 = Fixture()
    fx4.blobs[(FULL_B, receipt)] = (
        "the freeze %s and the landing %s\nthe SKILL delta freeze\u2192landing exactly `5 3`\n"
        % (FULL_A, FULL_C)
    )
    fx4.diffs[(FULL_A, FULL_C, "SKILL.md")] = "-\t-\tSKILL.md\n"
    got4 = audit("root", receipt, FULL_B, runner=runner_for(fx4))
    check(
        "audit-binary-failclosed",
        (got4["exit"], got4["findings"][0]["class"]),
        (1, FINDING_BINARY),
    )

    fx5 = Fixture()
    fx5.blobs[(FULL_B, receipt)] = (
        "the freeze %s and the landing %s\nthe SKILL delta freeze\u2192landing exactly `1 0`\n"
        % (FULL_A, FULL_C)
    )
    fx5.diffs[(FULL_A, FULL_C, "SKILL.md")] = "1\t0\tSKILL.md\n"
    got5 = audit("root", receipt, FULL_B, runner=runner_for(fx5))
    check("audit-green-exact-match", (got5["exit"], got5["findings"]), (0, []))

    fx6 = Fixture()
    fx6.blobs[(FULL_B, receipt)] = (
        "the freeze %s and the landing %s\nthe SKILL delta freeze\u2192landing exactly `0 0`\n"
        % (FULL_A, FULL_C)
    )
    fx6.diffs[(FULL_A, FULL_C, "SKILL.md")] = ""
    got6 = audit("root", receipt, FULL_B, runner=runner_for(fx6))
    check("audit-green-absent-row-is-zero", (got6["exit"], got6["findings"]), (0, []))

    fx7 = Fixture()
    fx7.blobs[(FULL_B, receipt)] = "no claims here at all\n"
    got7 = audit("root", receipt, FULL_B, runner=runner_for(fx7))
    check("audit-zero-claims-exit2", got7["exit"], 2)

    got8 = audit("root", "absent.txt", FULL_B, runner=runner_for(Fixture()))
    check("audit-receipt-absent-exit2", got8["exit"], 2)

    fx9 = Fixture()
    fx9.blobs[(FULL_B, receipt)] = (
        "the freeze %s\n" % FULL_A
        + "the SKILL delta freeze\u2192landing exactly `0 0`\n"
        + "the LOG delta freeze\u2192landing exactly `38 0`\n"
    )
    fx9.diffs[(FULL_A, FULL_C, "SKILL.md")] = ""
    fx9.diffs[(FULL_A, FULL_C, "LOG.md")] = "38\t0\tLOG.md\n"
    got9 = audit("root", receipt, FULL_B, overrides={"landing": FULL_C}, runner=runner_for(fx9))
    check(
        "audit-multi-claim-green-with-override",
        (got9["exit"], got9["claims_found"], got9["caller_supplied_names"]),
        (0, 2, ["landing"]),
    )

    fx10 = Fixture()
    fx10.blobs[(FULL_B, receipt)] = (
        "the freeze %s\nthe SKILL delta freeze\u2192landing exactly `1 0`\n"
        "the LOG delta freeze\u2192landing exactly `1 0`\n" % FULL_A
    )
    fx10.diffs[(FULL_A, FULL_C, "SKILL.md")] = "1\t0\tSKILL.md\n"
    fx10.diffs[(FULL_A, FULL_C, "LOG.md")] = "7\t0\tLOG.md\n"
    got10 = audit("root", receipt, FULL_B, overrides={"landing": FULL_C}, runner=runner_for(fx10))
    check(
        "audit-mixed-one-finding",
        (got10["exit"], len(got10["findings"]), got10["findings"][0]["class"]),
        (1, 1, FINDING_EDGE),
    )

    # numstat parser units
    check("parse-counts", parse_numstat("12\t3\tSKILL.md\n", "SKILL.md"), ("counts", (12, 3)))
    check("parse-binary", parse_numstat("-\t-\tSKILL.md\n", "SKILL.md"), ("binary", None))
    check("parse-absent", parse_numstat("1\t0\tOTHER.md\n", "SKILL.md"), ("absent", (0, 0)))

    failures = [c for c in cases if not c["ok"]]
    result = {
        "tool": TOOL,
        "selftest": True,
        "cases": len(cases),
        "failures": [c["case"] for c in failures],
        "exit": 1 if failures else 0,
    }
    print(json.dumps(result, indent=1))
    return 1 if failures else 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="numstat-edge-audit.py")
    ap.add_argument("--root", default=".")
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--rev", default=None)
    ap.add_argument("--name", action="append", default=[],
                    help="caller-supplied binding NAME=40hex (repeatable)")
    ap.add_argument("--json-out", default=None,
                    help="write the JSON receipt here (the only write)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        rc = selftest()
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"tool": TOOL, "selftest": True, "exit": rc}) + "\n")
        return rc

    if not args.receipt or not args.rev:
        ap.error("--receipt and --rev are required (or --selftest)")
    if not re.fullmatch(r"[\da-f]{40}", args.rev):
        print("numstat-edge-audit: --rev must be a 40-hex commit id", file=sys.stderr)
        return 2
    try:
        overrides = parse_overrides(args.name)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 2
    result = audit(args.root, args.receipt, args.rev, overrides=overrides)
    result["tool"] = TOOL
    print(json.dumps(result, indent=1))
    for f in result["findings"]:
        print(f"{args.receipt}:{f['line']}:{f['class']}: {f['detail']}", file=sys.stderr)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(result, indent=1) + "\n")
    return result["exit"]


if __name__ == "__main__":
    sys.exit(main())
