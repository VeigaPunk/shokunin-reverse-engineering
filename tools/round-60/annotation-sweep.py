#!/usr/bin/env python
"""annotation-sweep.py - multi-receipt annotation-consistency sweep.

Round 60 capability (R60-C1, depth).  The r59 planned candidate: the frozen
single-receipt gate `tools/round-59/annotation-audit.py` runs per receipt, so
the lane had no complete inventory of the annotation-contradiction class (the
M57-1 / D58-1 class) across its receipt corpus.  This sweep is the driver the
r59 record called for: it enumerates every committed receipt under the lane's
wave scores/ and records/ directories at ONE revision, runs the FROZEN
round-59 gate on each, and accounts for every finding the gate names.

Model (composition, never duplication):

  enumeration  `git -C root ls-tree -r --name-only REV -- .ufo/waves` (one
               listing, git objects at --rev, never the worktree), filtered
               to paths matching `.ufo/waves/round-<N>/l1/scores/` or
               `.../l1/records/`, deduplicated, sorted (deterministic order)
  audit tool   the committed `tools/round-59/annotation-audit.py`, byte-pinned:
               the sweep hashes the worktree copy and records its sha256; with
               --expect-sha256 a mismatch is exit 2 (could-not-evaluate) -
               the sweep never audits with unpinned checker bytes
  per receipt  one argv subprocess (sys.executable -X utf8 -I -B TOOL --root
               ROOT --receipt PATH --rev REV; no shell, no worktree reads by
               the checker beyond its own `git -C` object reads).  rc 0 ->
               green; rc 1 -> findings; rc 2 -> unevaluable; any other rc, an
               unparsable stdout, or a failed spawn -> invocation_error, and
               the sweep exits 2 (fail-closed; it never guesses a verdict it
               could not obtain).  rc 0 with an unparsable body is ALSO an
               invocation error: a green claim must come from the checker's
               own summary, never from a missing one
  findings     each finding becomes the key `<receipt>:<line>:<class>`; with
               --dispositions (a TSV: `key<TAB>disposition text`, no header)
               every key must be covered by a non-empty disposition, and
               every table key must match a finding (an uncovered finding is
               named; an extra table row is DISPOSITION_ORPHAN - both exit 1)

Verdict map: 0 = inventory complete (at least one receipt enumerated, zero
invocation errors) and every finding covered exactly by --dispositions (or no
findings at all); 1 = inventory complete but findings exist that --dispositions
does not cover exactly (or --dispositions is absent while findings exist); 2 =
could-not-evaluate (zero receipts, any invocation error, unknown revision,
failed git call, audit-tool absent or pin mismatch).  A green sweep never
claims the underlying defects are erased - filed bytes stay as filed; it
claims every named finding is accounted for in an on-record disposition (the
r59 disposition pattern).

Limits: the per-receipt check is the frozen gate's grammar only (`base: N ->
record: M` annotations against piped `grep -c` probes); receipts without that
shape are unevaluable, named as such, never clean; `--base-rev` re-derivation
is not swept (the base of each historical annotation is the single gate's
option, available per receipt); disposition text is not truth-checked - a
disposition's honesty rests on the citations it names, which a non-author can
re-derive.

--selftest runs the enumeration filter, the key derivation, the disposition
matching and the verdict aggregation over in-memory fixtures with an injected
audit runner (no git, no subprocess, no writes outside an optional
--json-out); the committed-tree demonstrations in the round-60 receipts are
the second evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

WAVE_ROOT = ".ufo/waves"
RECEIPT_RE = re.compile(
    r"^\.ufo/waves/round-\d+/l1/(scores|records)/.+$")
REV_RE = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_TOOL = "tools/round-59/annotation-audit.py"


class SweepError(Exception):
    pass


def is_receipt(path):
    """The enumeration predicate: scores/ or records/ receipts of any round."""
    return bool(RECEIPT_RE.match(path))


def enumerate_receipts(root, rev, run_git=None):
    """One ls-tree listing at --rev, filtered, deduplicated, sorted.

    run_git injection point for --selftest.  Raises SweepError on git failure.
    """
    argv = ["git", "-C", root, "ls-tree", "-r", "--name-only", rev, "--",
            WAVE_ROOT]
    try:
        proc = (run_git or _git)(argv)
    except OSError as exc:
        raise SweepError(f"oserror: {exc}") from exc
    if proc.returncode != 0:
        raise SweepError(
            f"git rc={proc.returncode}: "
            + proc.stderr.decode(errors="replace").strip()[:200])
    paths = proc.stdout.decode("utf-8", errors="replace").splitlines()
    return sorted({p for p in paths if is_receipt(p)})


def _git(argv):
    return subprocess.run(argv, capture_output=True)


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_one(root, rev, path, tool):
    """Run the frozen gate on one receipt.  Returns (rc, stdout, stderr).

    No shell: the checker's argv is passed exactly; a failed spawn raises
    OSError which the caller turns into an invocation error.
    """
    argv = [sys.executable, "-X", "utf8", "-I", "-B", tool,
            "--root", root, "--receipt", path, "--rev", rev]
    proc = subprocess.run(argv, capture_output=True)
    return proc.returncode, proc.stdout.decode("utf-8", errors="replace"), \
        proc.stderr.decode("utf-8", errors="replace")


def classify(rc, stdout):
    """(class, summary_or_None, error_or_None) from one checker run.

    class in {green, findings, unevaluable, invocation_error}.
    """
    if rc not in (0, 1, 2):
        return "invocation_error", None, f"unexpected rc {rc}"
    try:
        summary = json.loads(stdout)
    except json.JSONDecodeError as exc:
        return "invocation_error", None, f"stdout not JSON: {exc}"
    if not isinstance(summary, dict):
        return "invocation_error", None, "stdout JSON is not an object"
    if rc == 0:
        return "green", summary, None
    if rc == 1:
        return "findings", summary, None
    return "unevaluable", summary, None


def load_dispositions(path):
    """Read the TSV: `key<TAB>text`, no header.  Malformed line -> exit 2."""
    table = {}
    with open(path, "r", encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, start=1):
            line = raw.rstrip("\n").rstrip("\r")
            if not line.strip():
                continue
            if "\t" not in line:
                raise SweepError(
                    f"dispositions malformed at line {lineno}: no TAB")
            key, _, text = line.partition("\t")
            table[key] = text.strip()
    return table


def sweep(root, rev, receipts, audit_fn, dispositions=None, tool=DEFAULT_TOOL,
          tool_sha=None):
    """Aggregate one sweep.  audit_fn(root, rev, path) -> (rc, stdout, stderr).

    Returns (exit_class, inventory_dict).
    """
    per_receipt = []
    all_findings = []
    counts = {"green": 0, "findings": 0, "unevaluable": 0,
              "invocation_error": 0}
    for path in receipts:
        try:
            rc, stdout, stderr = audit_fn(root, rev, path)
        except OSError as exc:
            cls, summary, err = "invocation_error", None, f"oserror: {exc}"
        else:
            cls, summary, err = classify(rc, stdout)
        counts[cls] += 1
        findings = []
        if cls in ("green", "findings") and summary is not None:
            for f in summary.get("findings", []):
                findings.append({"class": f.get("class"), "line": f.get("line"),
                                 "detail": (f.get("detail") or "")[:200]})
                all_findings.append({"key": f"{path}:{f.get('line')}:"
                                              f"{f.get('class')}",
                                     "receipt": path})
        elif cls == "findings" and summary is None:
            findings.append({"class": "SUMMARY_MISSING", "line": None,
                             "detail": err or ""})
            all_findings.append({"key": f"{path}:-:SUMMARY_MISSING",
                                 "receipt": path})
        per_receipt.append({
            "receipt": path, "class": cls,
            "annotations": (summary or {}).get("annotations"),
            "checked": (summary or {}).get("checked"),
            "error": err, "findings": findings})

    inventory = {
        "sweep_rev": rev, "audit_tool": tool, "audit_tool_sha256": tool_sha,
        "receipts_total": len(receipts), "counts": counts,
        "findings_total": len(all_findings),
        "per_receipt": per_receipt,
        "finding_keys": [f["key"] for f in all_findings],
    }

    if len(receipts) == 0 or counts["invocation_error"] > 0:
        inventory["exit"] = 2
        inventory["exit_reason"] = (
            "zero receipts enumerated" if len(receipts) == 0
            else f"{counts['invocation_error']} invocation error(s)")
        return 2, inventory

    if dispositions is None:
        if all_findings:
            inventory["exit"] = 1
            inventory["exit_reason"] = (
                f"{len(all_findings)} finding(s) named, no --dispositions "
                f"given")
        else:
            inventory["exit"] = 0
            inventory["exit_reason"] = "inventory complete, no findings"
        return inventory["exit"], inventory

    uncovered = [f["key"] for f in all_findings
                 if not (dispositions.get(f["key"]) or "").strip()]
    finding_key_set = {f["key"] for f in all_findings}
    orphans = [k for k in sorted(dispositions) if k not in finding_key_set]
    inventory["uncovered"] = uncovered
    inventory["disposition_orphans"] = orphans
    if uncovered or orphans:
        inventory["exit"] = 1
        inventory["exit_reason"] = (
            f"{len(uncovered)} uncovered finding(s), "
            f"{len(orphans)} disposition orphan(s)")
        return 1, inventory
    inventory["exit"] = 0
    inventory["exit_reason"] = (
        f"inventory complete; {len(all_findings)} finding(s) all dispositioned")
    return 0, inventory


def selftest():
    """In-memory fixtures; no git, no subprocess.  Returns (cases, failures)."""
    cases = []
    failures = []

    def check(name, got, want):
        cases.append(name)
        if got != want:
            failures.append(f"{name}: got {got!r} want {want!r}")

    # 1-6. the enumeration predicate
    check("filter-scores", is_receipt(".ufo/waves/round-59/l1/scores/c1.txt"),
          True)
    check("filter-records",
          is_receipt(".ufo/waves/round-59/l1/records/a/b.json"), True)
    check("filter-other-scope",
          is_receipt(".ufo/waves/round-59/l1/s259/grep.html"), False)
    check("filter-non-l1", is_receipt(".ufo/waves/round-30/w1/x.md"), False)
    check("filter-container",
          is_receipt(".ufo/waves/round-59/claims.json"), False)
    check("filter-freeze", is_receipt(".ufo/waves/round-59/l1/FREEZE"), False)

    # 7. enumeration: filter + dedupe + sorted order
    listed = [".ufo/waves/round-30/w1/x.md",
              ".ufo/waves/round-59/l1/records/z.txt",
              ".ufo/waves/round-48/l1/scores/a.json",
              ".ufo/waves/round-59/l1/records/z.txt"]
    got = sorted({p for p in listed if is_receipt(p)})
    check("enumerate-sorted-dedup", got,
          [".ufo/waves/round-48/l1/scores/a.json",
           ".ufo/waves/round-59/l1/records/z.txt"])

    # 8-12. classification of one checker run
    check("classify-green", classify(0, '{"findings": [], "exit": 0}')[0],
          "green")
    check("classify-findings",
          classify(1, '{"findings": [{"class": "C", "line": 6}]}')[0],
          "findings")
    check("classify-unevaluable", classify(2, '{"error": "x"}')[0],
          "unevaluable")
    check("classify-bad-rc", classify(3, "")[0], "invocation_error")
    check("classify-green-no-json", classify(0, "not json")[0],
          "invocation_error")

    # 13-15. green-with-findings, findings-without-summary, empty sweep
    def runner(table):
        def run(root, rev, path):
            return table[path]
        return run

    R = "a" * 40
    ok = '{"annotations": 1, "checked": 1, "findings": [], "exit": 0}'
    bad = ('{"annotations": 1, "checked": 1, "exit": 1, "findings": '
           '[{"class": "ANNOTATION_OUTPUT_MISMATCH", "line": 6, '
           '"detail": "d"}]}')
    uneval = '{"error": "no annotation found", "exit": 2}'
    table = {".ufo/waves/round-48/l1/scores/a.json": (0, ok, ""),
             ".ufo/waves/round-58/l1/scores/b.txt": (1, bad, "printed"),
             ".ufo/waves/round-59/l1/records/c.json": (2, uneval, "")}
    rc, inv = sweep("root", R, sorted(table), runner(table))
    check("sweep-exit-undispositioned", rc, 1)
    check("sweep-counts", inv["counts"],
          {"green": 1, "findings": 1, "unevaluable": 1, "invocation_error": 0})
    check("sweep-keys", inv["finding_keys"],
          [".ufo/waves/round-58/l1/scores/b.txt:6:"
           "ANNOTATION_OUTPUT_MISMATCH"])

    rc, inv = sweep("root", R, sorted(table), runner(table),
                    dispositions={".ufo/waves/round-58/l1/scores/b.txt:6:"
                                  "ANNOTATION_OUTPUT_MISMATCH":
                                  "disclosed at records/x.txt"})
    check("sweep-exit-covered", rc, 0)
    check("sweep-reason", "all dispositioned" in inv["exit_reason"], True)

    # 16. missing key -> 1, named
    rc, inv = sweep("root", R, sorted(table), runner(table),
                    dispositions={})
    check("sweep-exit-empty-table", rc, 1)
    check("sweep-uncovered-named", len(inv["uncovered"]), 1)

    # 17. orphan disposition -> 1
    rc, inv = sweep("root", R, sorted(table), runner(table),
                    dispositions={".ufo/waves/round-58/l1/scores/b.txt:6:"
                                  "ANNOTATION_OUTPUT_MISMATCH": "ok",
                                  ".ufo/waves/round-48/l1/scores/a.json:9:C":
                                  "extra"})
    check("sweep-exit-orphan", rc, 1)
    check("sweep-orphan-named", inv["disposition_orphans"],
          [".ufo/waves/round-48/l1/scores/a.json:9:C"])

    # 18. empty disposition text counts as uncovered (fail-closed)
    rc, inv = sweep("root", R, sorted(table), runner(table),
                    dispositions={".ufo/waves/round-58/l1/scores/b.txt:6:"
                                  "ANNOTATION_OUTPUT_MISMATCH": "  "})
    check("sweep-empty-text-uncovered", rc, 1)

    # 19. invocation error -> 2, never a verdict guess
    broken = dict(table)
    broken[".ufo/waves/round-59/l1/scores/d.txt"] = (0, "garbage", "")
    rc, inv = sweep("root", R, sorted(broken), runner(broken))
    check("sweep-invocation-error", rc, 2)
    check("sweep-error-reason", "invocation error" in inv["exit_reason"], True)

    # 20. zero receipts -> 2, never vacuously clean (the QUALITY #66 boundary)
    rc, inv = sweep("root", R, [], runner({}))
    check("sweep-empty-corpus", rc, 2)
    check("sweep-empty-corpus-reason", inv["exit_reason"],
          "zero receipts enumerated")

    # 21. findings-class receipt with unparsable stdout -> invocation error
    broken2 = dict(table)
    broken2[".ufo/waves/round-58/l1/scores/b.txt"] = (1, "no json", "err")
    rc, inv = sweep("root", R, sorted(broken2), runner(broken2))
    check("sweep-findings-unparsable", rc, 2)

    # 22. TSV loader: malformed line raises (exit 2 upstream)
    try:
        load_dispositions_error = False
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False,
                                         encoding="utf-8",
                                         newline="\n") as fh:
            fh.write("k1\ttext\nbad-line-without-tab\n")
            tmp = fh.name
        try:
            load_dispositions(tmp)
        except SweepError:
            load_dispositions_error = True
        finally:
            os.unlink(tmp)
    except OSError:
        load_dispositions_error = False
    check("tsv-malformed-raises", load_dispositions_error, True)

    return cases, failures


def main():
    ap = argparse.ArgumentParser(
        description="multi-receipt annotation-consistency sweep (round 60)")
    ap.add_argument("--root", default=".", help="lane repo root (git -C)")
    ap.add_argument("--rev", help="40-hex revision: the tree enumerated and "
                                  "the receipt bytes audited")
    ap.add_argument("--audit-tool", default=DEFAULT_TOOL,
                    help="the frozen single-receipt gate to compose")
    ap.add_argument("--expect-sha256", default=None,
                    help="refuse to run unless the audit tool's worktree "
                         "bytes hash to this (fail-closed pin check)")
    ap.add_argument("--dispositions", default=None,
                    help="TSV key<TAB>text covering every finding key")
    ap.add_argument("--json-out", default=None,
                    help="optional path for the JSON inventory receipt")
    ap.add_argument("--selftest", action="store_true",
                    help="run in-memory fixtures, no git, no subprocess")
    args = ap.parse_args()

    if args.selftest:
        cases, failures = selftest()
        summary = {"tool": "tools/round-60/annotation-sweep.py",
                   "selftest": True, "cases": len(cases),
                   "failures": failures, "exit": 1 if failures else 0}
        out = json.dumps(summary, indent=1)
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8",
                      newline="\n") as fh:
                fh.write(out + "\n")
        print(out)
        return 1 if failures else 0

    if not args.rev or not REV_RE.match(args.rev):
        print("annotation-sweep: --rev must be a 40-hex commit id "
              "(or --selftest)", file=sys.stderr)
        return 2
    if not os.path.isfile(args.audit_tool):
        print(f"annotation-sweep: audit tool absent: {args.audit_tool}",
              file=sys.stderr)
        return 2
    try:
        tool_sha = file_sha256(args.audit_tool)
    except OSError as exc:
        print(f"annotation-sweep: cannot hash audit tool: {exc}",
              file=sys.stderr)
        return 2
    if args.expect_sha256 and tool_sha != args.expect_sha256:
        print(f"annotation-sweep: audit tool pin mismatch: worktree "
              f"{tool_sha} != expected {args.expect_sha256}", file=sys.stderr)
        return 2

    try:
        receipts = enumerate_receipts(args.root, args.rev)
        table = load_dispositions(args.dispositions) \
            if args.dispositions else None
    except (SweepError, OSError) as exc:
        print(f"annotation-sweep: {exc}", file=sys.stderr)
        return 2

    exit_class, inventory = sweep(
        args.root, args.rev, receipts,
        lambda root, rev, path: audit_one(root, rev, path, args.audit_tool),
        dispositions=table, tool=args.audit_tool, tool_sha=tool_sha)

    findings_printed = 0
    for entry in inventory["per_receipt"]:
        for f in entry["findings"]:
            print(f"{entry['receipt']}:{f['line']}:{f['class']}: "
                  f"{f['detail']}", file=sys.stderr)
            findings_printed += 1
    if inventory.get("uncovered"):
        print(f"uncovered: {inventory['uncovered']}", file=sys.stderr)
    if inventory.get("disposition_orphans"):
        print(f"disposition_orphans: {inventory['disposition_orphans']}",
              file=sys.stderr)
    out = json.dumps(inventory, indent=1)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(out + "\n")
    print(json.dumps({k: inventory[k] for k in
                      ("sweep_rev", "receipts_total", "counts",
                       "findings_total", "exit", "exit_reason")}))
    return exit_class


if __name__ == "__main__":
    sys.exit(main())
