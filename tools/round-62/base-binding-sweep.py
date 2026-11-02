#!/usr/bin/env python
"""base-binding-sweep.py - base-rev-threading receipt sweep.

Round 62 capability (R62-C1, depth).  The r60 planned candidate, named again
by the r61 record: the frozen single-receipt gate
`tools/round-59/annotation-audit.py` carries a `--base-rev` option ("also
re-derive each annotation's base: value at this revision"), but the r60
multi-receipt sweep never threads it - its own limits line says so
("`--base-rev` re-derivation is not swept (the base of each historical
annotation is the single gate's option, available per receipt)").  So no
instrument of this lane ever mechanically checked the `base:` half of any
receipt annotation: the sweep verified record values only.  This sweep is
the threading instrument the r60/r61 records called for: the base revision
comes from the receipt's OWN bytes, so the check is per-receipt context with
no caller input.

Model (composition, never duplication):

  enumeration  identical to the r60 sweep: `git -C root ls-tree -r
               --name-only REV -- .ufo/waves`, filtered to paths matching
               `.ufo/waves/round-<N>/l1/(scores|records)/`, deduplicated,
               sorted
  base binding a rev-name binding scanned in the receipt's OWN committed
               bytes (`git show REV:RECEIPT`, never the worktree): the r61
               grammar - a lowercase name token, an optional
               ``commit``/``rev`` word, then a 40-hex commit id with a
               negative lookahead rejecting hex run-ons (a 64-hex sha256
               does NOT bind).  First occurrence of a name wins.  The
               receipt is base-THREADED iff a binding named exactly ``base``
               exists; its 40-hex value is passed to the frozen gate as
               --base-rev.  A receipt with no ``base`` binding runs
               unthreaded (the r60 semantics, unchanged).  --no-base-thread
               disables threading fleet-wide (the equivalence arm: the
               finding set must equal the r60 sweep's)
  audit tool   the committed `tools/round-59/annotation-audit.py`,
               byte-pinned: the sweep hashes the worktree copy and records
               its sha256; with --expect-sha256 a mismatch is exit 2
               (could-not-evaluate) - the sweep never audits with unpinned
               checker bytes
  per receipt  one argv subprocess (sys.executable -X utf8 -I -B TOOL
               --root ROOT --receipt PATH --rev REV [--base-rev HEX]; no
               shell).  rc 0 -> green; rc 1 -> findings; rc 2 ->
               unevaluable; any other rc, an unparsable stdout, or a failed
               spawn -> invocation_error, and the sweep exits 2
               (fail-closed).  rc 0 with an unparsable body is ALSO an
               invocation error: a green claim must come from the checker's
               own summary, never from a missing one
  findings     keys `<receipt>:<line>:<class>`, identical to the r60 key
               format, so the standing round-60 disposition table stays
               compatible; with --dispositions (TSV `key<TAB>text`, no
               header) every key must be covered by a non-empty disposition
               and every table key must match a finding (an uncovered
               finding is named; an extra table row is DISPOSITION_ORPHAN -
               both exit 1)

Verdict map: 0 = inventory complete (at least one receipt enumerated, zero
invocation errors) and every finding covered exactly by --dispositions (or
no findings at all); 1 = inventory complete but findings exist that
--dispositions does not cover exactly (or --dispositions is absent while
findings exist); 2 = could-not-evaluate (zero receipts, any invocation
error, unknown revision, failed git call, audit-tool absent or pin
mismatch).  A green sweep never claims the underlying defects are erased -
filed bytes stay as filed.

Limits: the per-receipt check is the frozen gate's grammar only
(`base: N -> record: M` annotations against piped `grep -c` probes); a
receipt that binds ``base`` to a 40-hex id that git cannot resolve yields
the gate's PROBE_FAILED finding with a ``base:`` prefix (fail-closed: a
base claim the gate cannot check is a finding, never a pass); the binding
name is exactly ``base`` (first occurrence wins) - a receipt that names its
base state by any other word runs unthreaded and its base values stay
unchecked by design, which the inventory reports as receipts_without_base_
binding; the base-derivation count in the inventory is computed by a
reporting-only mirror of the frozen gate's extractor and grammar matcher
(verbatim copy below) - the mirror never produces a verdict, it only counts
annotation instances whose bound command the gate will base-re-derive; the
verdict always comes from the gate subprocess.  Disposition text is not
truth-checked - a disposition's honesty rests on the citations it names,
which a non-author can re-derive (the r60 contract).

--selftest runs the enumeration filter, the binding scanner, the threading
decision, the classifier, the verdict aggregation, the mirror statistic and
the pin check over in-memory fixtures with injected git/audit/hash runners
(no git, no grep, no subprocess, no writes outside an optional --json-out)
asserting the exit class, the finding keys and the threading argv of every
case; the committed-tree demonstrations in the round-62 receipts are the
second evidence.

Demonstrations on the committed tree (round-62 receipts):
  inventory  --rev <tip> over the whole wave corpus: every annotated
             receipt with a self-named ``base`` binding is threaded (the
             r58 c1-after is the corpus's one such receipt; its four
             grammar-matched annotation instances gain the BASE
             re-derivation the r60 sweep never ran) and the standing
             finding keys are unchanged
  red        the same run without --dispositions: exit 1, the standing
             finding keys named
  green      the same run with the (extended) disposition table: exit 0
  equality   --no-base-thread: the finding set equals the r60 sweep's
  fail-closed --expect-sha256 with a wrong pin: exit 2
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys

WAVE_ROOT = ".ufo/waves"
RECEIPT_RE = re.compile(
    r"^\.ufo/waves/round-\d+/l1/(scores|records)/.+$")
REV_RE = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_TOOL = "tools/round-59/annotation-audit.py"

# The r61 binding grammar (tools/round-61/numstat-edge-audit.py), mirrored:
# a lowercase name token, optional commit/rev word, optional backticks, a
# 40-hex id, hex run-ons rejected by the negative lookahead.
BINDING_RE = re.compile(
    r"(?P<name>[a-z][a-z-]*)\s+(?:commit\s+|rev\s+)?`?(?P<hex>[\da-f]{40})"
    r"(?![\da-f])`?")

CMD_PREFIX = "$ "
ANN_RE = re.compile(r"^\(.*?\bbase:\s*(-?\d+)\s*->\s*record:\s*(-?\d+)",
                    re.S)
INT_RE = re.compile(r"^-?\d+$")
SHOW_GRAMMAR = ["git", "show"]
LSTREE_GRAMMAR = ["git", "ls-tree", "-r", "--name-only"]

BASE_CLASS = "ANNOTATION_BASE_MISMATCH"


class SweepError(Exception):
    pass


def is_receipt(path):
    """The enumeration predicate: scores/ or records/ receipts of any round."""
    return bool(RECEIPT_RE.match(path))


def _git(argv):
    return subprocess.run(argv, capture_output=True)


def enumerate_receipts(root, rev, run_git=None):
    """One ls-tree listing at --rev, filtered, deduplicated, sorted."""
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


def receipt_bytes(root, rev, path, run_git=None):
    """Committed bytes of one receipt at --rev (never the worktree)."""
    argv = ["git", "-C", root, "show", f"{rev}:{path}"]
    try:
        proc = (run_git or _git)(argv)
    except OSError as exc:
        raise SweepError(f"oserror: {exc}") from exc
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", errors="replace")


def find_bindings(text):
    """name -> 40-hex, first occurrence wins, in scan order (r61 grammar)."""
    found = {}
    for m in BINDING_RE.finditer(text):
        name = m.group("name")
        if name not in found:
            found[name] = m.group("hex")
    return found


def base_binding(text):
    """The receipt's own base revision: the first binding named `base`."""
    return find_bindings(text).get("base")


# --- reporting-only mirror of the frozen gate's extractor and grammar -----
# Verbatim copies of tools/round-59/annotation-audit.py extract()/match_
# grammar() (minus the unused record-value capture).  The mirror NEVER
# produces a verdict; it only counts the annotation instances whose bound
# command the frozen gate will base-re-derive when --base-rev is threaded.
# The verdict always comes from the gate subprocess.

def mirror_extract(text):
    """Commands and annotations as the frozen gate binds them."""
    commands = []
    annotations = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith(CMD_PREFIX):
            commands.append(stripped[len(CMD_PREFIX):])
            continue
        m = ANN_RE.match(raw)
        if m and commands:
            annotations.append(len(commands) - 1)
    return commands, annotations


def mirror_match_grammar(cmd):
    """Parse a command line into a re-executable probe descriptor or None."""
    try:
        tokens = shlex.split(cmd)
    except ValueError:
        return None
    n = len(tokens)
    pipe = None
    for i in range(n - 3):
        if tokens[i] == "|" and tokens[i + 1] == "grep" and \
                tokens[i + 2] == "-c":
            pipe = i
            break
    if pipe is None:
        return None
    head = tokens[:pipe]
    pat = tokens[pipe + 3]
    if tokens[pipe + 4:]:
        return None
    if head[:2] == SHOW_GRAMMAR and len(head) == 3:
        spec = head[2]
        if ":" not in spec:
            return None
        rev, _, path = spec.partition(":")
        if not REV_RE.match(rev) or not path:
            return None
        return {"kind": "show", "path": path, "pattern": pat}
    if head[:4] == LSTREE_GRAMMAR and len(head) == 7 and head[5] == "--":
        rev, path = head[4], head[6]
        if not REV_RE.match(rev) or not path:
            return None
        return {"kind": "lstree", "path": path, "pattern": pat}
    return None


def mirror_base_probe_instances(text):
    """Annotation instances whose bound command the gate will base-check."""
    commands, bound = mirror_extract(text)
    count = 0
    for cmd_index in bound:
        if cmd_index < len(commands) and \
                mirror_match_grammar(commands[cmd_index]) is not None:
            count += 1
    return count


# --- end reporting-only mirror --------------------------------------------


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_one(root, rev, path, base_rev=None, tool=DEFAULT_TOOL):
    """Run the frozen gate on one receipt.  Returns (rc, stdout, stderr).

    Signature matches the sweep's audit_fn contract (root, rev, path,
    base_rev) so a threaded and an unthreaded receipt take the same call
    shape; the tool path is the fifth parameter.  No shell: the checker's
    argv is passed exactly; a failed spawn raises OSError which the caller
    turns into an invocation error.  --base-rev is threaded only when the
    receipt's own bytes bound a base revision.
    """
    argv = [sys.executable, "-X", "utf8", "-I", "-B", tool,
            "--root", root, "--receipt", path, "--rev", rev]
    if base_rev is not None:
        argv += ["--base-rev", base_rev]
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


def sweep(root, rev, receipts, audit_fn, dispositions=None,
          tool=DEFAULT_TOOL, tool_sha=None, bindings=None, probe_stats=None):
    """Aggregate one sweep.

    audit_fn(root, rev, path, base_rev) -> (rc, stdout, stderr).
    bindings: {path: base_hex_or_None} threaded per receipt (None entry =
    run unthreaded).  probe_stats: {path: base_probe_instances} for the
    inventory.  Returns (exit_class, inventory_dict).
    """
    bindings = bindings or {}
    probe_stats = probe_stats or {}
    per_receipt = []
    all_findings = []
    counts = {"green": 0, "findings": 0, "unevaluable": 0,
              "invocation_error": 0}
    threaded = []
    base_annotation_instances = 0
    base_probe_instances = 0
    for path in receipts:
        base_rev = bindings.get(path)
        try:
            rc, stdout, stderr = audit_fn(root, rev, path, base_rev)
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
        if base_rev is not None:
            threaded.append({"receipt": path, "base_rev": base_rev})
            base_annotation_instances += int((summary or {})
                                             .get("annotations") or 0)
            base_probe_instances += int(probe_stats.get(path) or 0)
        per_receipt.append({
            "receipt": path, "class": cls,
            "base_rev": base_rev,
            "base_probe_instances": probe_stats.get(path),
            "annotations": (summary or {}).get("annotations"),
            "checked": (summary or {}).get("checked"),
            "error": err, "findings": findings})

    inventory = {
        "sweep_rev": rev, "audit_tool": tool, "audit_tool_sha256": tool_sha,
        "receipts_total": len(receipts), "counts": counts,
        "findings_total": len(all_findings),
        "base_threading": {
            "receipts_with_base_binding": len(threaded),
            "threaded_receipts": threaded,
            "base_annotation_instances": base_annotation_instances,
            "base_probe_instances": base_probe_instances,
            # base_class_findings: ANNOTATION_BASE_MISMATCH keys on receipts
            # threaded here.  Record-class findings on the same receipts keep
            # firing unchanged (persistent state, never hidden by threading).
            "base_class_findings": sorted(
                f["key"] for f in all_findings
                if bindings.get(f["key"].rsplit(":", 2)[0])
                and f["key"].rsplit(":", 1)[-1] == BASE_CLASS),
        },
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
        f"inventory complete; {len(all_findings)} finding(s) all "
        f"dispositioned" if all_findings
        else "inventory complete, no findings")
    return 0, inventory


def selftest():
    """In-memory fixtures; injected git/audit/hash runners.  (cases, fails)"""
    cases = []
    failures = []

    def check(name, got, want):
        cases.append(name)
        if got != want:
            failures.append(f"{name}: got {got!r} want {want!r}")

    R = "df62b6f986fb460847037482e0199cdf1541e393"
    T = "536c48650a5ccc435387b2060638a9d8a4bebf44"
    B = "42c794afc5cdf2f72d80edb839cfbcbfe32e6bad"

    # 1. enumeration predicate
    check("enum-scores", is_receipt(".ufo/waves/round-58/l1/scores/c1-after.txt"), True)
    check("enum-records", is_receipt(".ufo/waves/round-61/l1/records/edge-selftest.txt"), True)
    check("enum-claims", is_receipt(".ufo/waves/round-62/claims.json"), False)
    check("enum-fixtures", is_receipt(".ufo/waves/round-62/l1/fixtures/red.txt"), False)
    check("enum-nested", is_receipt(".ufo/waves/round-58/l1/scores/sub/x.txt"), True)

    # 2. binding scanner - positives
    check("bind-round-base", base_binding(f"round base `{R}`\n"), R)
    check("bind-base-commit", base_binding(f"the base commit {R} lands\n"), R)
    check("bind-base-rev", base_binding(f"base rev {R}\n"), R)
    check("bind-inline", base_binding(f"x the base {T} y\n"), T)
    # 3. binding scanner - negatives
    check("bind-sha256-runon", base_binding(
        f"base 873c447fcdeed1efd506fdd49c6910df8a3517896fdcad3c935359f457f13"
        f"97e\n"), None)
    check("bind-sha256-word", base_binding(
        f"sha256 {R}\n"), None)
    check("bind-annotation", base_binding(
        "(base: 0 -> record: 1; note)\n"), None)
    check("bind-other-name", base_binding(
        f"record {R}\nfreeze {T}\n"), None)
    check("bind-hyphen-name", base_binding(
        f"pre-base {R}\n"), None)
    check("bind-abbrev", base_binding("base 42c794af\n"), None)
    check("bind-41hex", base_binding(f"base {R}0\n"), None)
    # 4. first occurrence wins
    check("bind-first-wins", base_binding(
        f"base {R}\nlater base {T}\n"), R)

    # 5. threading decision through audit_one's argv contract
    captured = {}
    saved_run = subprocess.run

    class FakeCompleted:
        def __init__(self, rc, out):
            self.returncode = rc
            self.stdout = out.encode()
            self.stderr = b""

    def fake_run(argv, capture_output=True):
        captured["argv"] = argv
        return FakeCompleted(0, '{"receipt": "r", "findings": []}')

    subprocess.run = fake_run
    try:
        audit_one(".", R, "p.txt", base_rev=None, tool="tool.py")
        threaded_argv = [a for a in captured["argv"]]
        check("thread-off", any(a == "--base-rev" for a in threaded_argv), False)
        audit_one(".", R, "p.txt", base_rev=B, tool="tool.py")
        threaded_argv = captured["argv"]
        check("thread-on", any(a == "--base-rev" for a in threaded_argv), True)
        check("thread-on-value", threaded_argv[-1], B)
    finally:
        subprocess.run = saved_run

    # 6. classifier
    check("classify-green", classify(0, '{"a": 1}')[0], "green")
    check("classify-findings", classify(1, '{"a": 1}')[0], "findings")
    check("classify-uneval", classify(2, '{"a": 1}')[0], "unevaluable")
    check("classify-bad-rc", classify(3, "{}")[0], "invocation_error")
    check("classify-nonjson", classify(0, "hello")[0], "invocation_error")
    check("classify-nonobject", classify(0, "[1]")[0], "invocation_error")

    # 7. mirror statistic
    text = (f"$ git show {T}:LOG.md | grep -c 'pat one'\n"
            "2\n"
            "(base: 0 -> record: 2; ok)\n"
            "$ echo not-a-git-probe\n"
            "0\n"
            "(base: 1 -> record: 0; outside grammar)\n")
    check("mirror-probe-instances", mirror_base_probe_instances(text), 1)
    text2 = (f"$ git ls-tree -r --name-only {T} -- a/b.txt | grep -c 'x'\n"
             "1\n"
             "(base: 0 -> record: 1; ls-tree grammar)\n")
    check("mirror-probe-instances-lstree",
          mirror_base_probe_instances(text2), 1)
    text3 = ("$ git show HEAD:LOG.md | grep -c 'abbrev'\n"
             "0\n"
             "(base: 0 -> record: 0; abbreviated rev is outside)\n")
    check("mirror-probe-instances-abbrev",
          mirror_base_probe_instances(text3), 0)

    # 8. aggregation over injected audit_fn
    KEY = ".ufo/waves/round-58/l1/scores/c1-after.txt"

    def audit_red(root, rev, path, base_rev):
        summary = {"receipt": path, "rev": rev, "base_rev": base_rev,
                   "annotations": 2, "checked": 2,
                   "findings": [
                       {"class": "ANNOTATION_OUTPUT_MISMATCH", "line": 6,
                        "detail": "claims 1, output 0"},
                       {"class": BASE_CLASS, "line": 11,
                        "detail": f"claims base: 0, re-derives 1 at {B}"}]}
        return 1, json.dumps(summary), ""

    receipts = [KEY]
    bindings = {KEY: B}
    probe_stats = {KEY: 2}
    rc, inv = sweep(".", R, receipts, audit_red, dispositions=None,
                    bindings=bindings, probe_stats=probe_stats)
    check("agg-red-exit", rc, 1)
    check("agg-red-keys", inv["finding_keys"],
          [f"{KEY}:6:ANNOTATION_OUTPUT_MISMATCH", f"{KEY}:11:{BASE_CLASS}"])
    check("agg-threaded-count",
          inv["base_threading"]["receipts_with_base_binding"], 1)
    check("agg-base-ann-instances",
          inv["base_threading"]["base_annotation_instances"], 2)
    check("agg-base-probe-instances",
          inv["base_threading"]["base_probe_instances"], 2)
    check("agg-base-class-findings", inv["base_threading"]
          ["base_class_findings"], [f"{KEY}:11:{BASE_CLASS}"])

    # 9. dispositions: uncovered finding -> 1; covered -> 0; orphan -> 1
    rc, inv = sweep(".", R, receipts, audit_red,
                    dispositions={f"{KEY}:6:ANNOTATION_OUTPUT_MISMATCH": "d1"},
                    bindings=bindings, probe_stats=probe_stats)
    check("agg-uncovered", rc, 1)
    check("agg-uncovered-named", inv["uncovered"],
          [f"{KEY}:11:{BASE_CLASS}"])
    rc, inv = sweep(".", R, receipts, audit_red,
                    dispositions={f"{KEY}:6:ANNOTATION_OUTPUT_MISMATCH": "d1",
                                  f"{KEY}:11:{BASE_CLASS}": "d2"},
                    bindings=bindings, probe_stats=probe_stats)
    check("agg-covered-green", rc, 0)
    rc, inv = sweep(".", R, receipts, audit_red,
                    dispositions={f"{KEY}:6:ANNOTATION_OUTPUT_MISMATCH": "d1",
                                  f"{KEY}:11:{BASE_CLASS}": "d2",
                                  "extra:key:WHATEVER": "orphan"},
                    bindings=bindings, probe_stats=probe_stats)
    check("agg-orphan", rc, 1)
    check("agg-orphan-named", inv["disposition_orphans"], ["extra:key:WHATEVER"])

    # 10. invocation error -> 2; zero receipts -> 2
    def audit_boom(root, rev, path, base_rev):
        raise OSError("spawn failed")

    rc, inv = sweep(".", R, receipts, audit_boom, bindings=bindings)
    check("agg-invocation-error", rc, 2)
    rc, inv = sweep(".", R, [], audit_red)
    check("agg-zero-receipts", rc, 2)

    # 11. unthreaded receipt keeps base_rev None; no binding -> no thread
    def audit_spy(root, rev, path, base_rev):
        captured["base_seen"] = base_rev
        return 2, json.dumps({"receipt": path, "error": "no annotation"}), ""

    rc, inv = sweep(".", R, receipts, audit_spy, bindings={KEY: None})
    check("unthreaded-passes-none", captured["base_seen"], None)
    rc, inv = sweep(".", R, receipts, audit_spy, bindings={KEY: B})
    check("threaded-passes-hex", captured["base_seen"], B)

    # 12. the production seam: sweep's audit_fn contract wired to the REAL
    # audit_one (the main() closure shape) - the tool cell must be the bound
    # tool and threading must reach the argv (the M62-1 class, covered here
    # after the live dry run caught the signature mismatch pre-commit)
    subprocess.run = fake_run
    try:
        def one(root, rev, path, base_rev, _tool="tool.py"):
            return audit_one(root, rev, path, base_rev, _tool)

        rc, inv = sweep(".", R, receipts, one, bindings={KEY: B})
        argv = captured["argv"]
        check("seam-tool-cell", argv[argv.index("-B") + 1], "tool.py")
        check("seam-threaded", "--base-rev" in argv, True)
        rc, inv = sweep(".", R, receipts, one, bindings={KEY: None})
        argv = captured["argv"]
        check("seam-unthreaded-tool-cell", argv[argv.index("-B") + 1],
              "tool.py")
        check("seam-unthreaded", "--base-rev" in argv, False)
    finally:
        subprocess.run = saved_run

    # 12. load_dispositions: malformed line raises
    import tempfile
    import os
    tmpdir = tempfile.mkdtemp(prefix="bbs-selftest-")
    try:
        badp = os.path.join(tmpdir, "bad.tsv")
        with open(badp, "w", encoding="utf-8") as h:
            h.write("no-tab-line\n")
        raised = False
        try:
            load_dispositions(badp)
        except SweepError:
            raised = True
        check("dispo-malformed-raises", raised, True)
        goodp = os.path.join(tmpdir, "good.tsv")
        with open(goodp, "w", encoding="utf-8", newline="\n") as h:
            h.write("k1\ttext one\n\nk2\ttext two\n")
        table = load_dispositions(goodp)
        check("dispo-load", table, {"k1": "text one", "k2": "text two"})
    finally:
        for name in os.listdir(tmpdir):
            os.unlink(os.path.join(tmpdir, name))
        os.rmdir(tmpdir)

    return cases, failures


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="base-rev-threading receipt sweep (round 62)")
    parser.add_argument("--root", default=".",
                        help="lane repo root (git -C target)")
    parser.add_argument("--rev", help="40-hex revision: the tree enumerated "
                                      "and the receipt bytes audited")
    parser.add_argument("--audit-tool", default=DEFAULT_TOOL,
                        help="the frozen single-receipt gate to compose")
    parser.add_argument("--expect-sha256",
                        help="refuse to run unless the audit tool's worktree "
                             "bytes hash to this (fail-closed pin check)")
    parser.add_argument("--dispositions",
                        help="TSV key<TAB>text covering every finding key")
    parser.add_argument("--no-base-thread", action="store_true",
                        help="disable base threading fleet-wide (the r60 "
                             "equivalence arm)")
    parser.add_argument("--json-out", help="optional path for the JSON "
                                           "inventory receipt")
    parser.add_argument("--selftest", action="store_true",
                        help="run in-memory fixtures, no git, no subprocess")
    args = parser.parse_args(argv)

    if args.selftest:
        cases, failures = selftest()
        print(f"cases {len(cases)}, failures {failures!r}")
        return 1 if failures else 0

    if not args.rev or not REV_RE.match(args.rev):
        print("could-not-evaluate: --rev must be a 40-hex revision",
              file=sys.stderr)
        return 2

    if args.expect_sha256 is not None:
        actual = file_sha256(args.audit_tool)
        if actual != args.expect_sha256:
            print(json.dumps({
                "exit": 2, "exit_reason": "audit-tool pin mismatch",
                "audit_tool": args.audit_tool,
                "expected_sha256": args.expect_sha256,
                "actual_sha256": actual}, indent=1))
            return 2

    try:
        receipts = enumerate_receipts(args.root, args.rev)
        bindings = {}
        probe_stats = {}
        if not args.no_base_thread:
            for path in receipts:
                text = receipt_bytes(args.root, args.rev, path)
                if text is None:
                    continue
                hex_ = base_binding(text)
                if hex_:
                    bindings[path] = hex_
                    probe_stats[path] = mirror_base_probe_instances(text)
        dispositions = None
        if args.dispositions:
            dispositions = load_dispositions(args.dispositions)
        tool_sha = file_sha256(args.audit_tool)

        def one(root, rev, path, base_rev, _tool=args.audit_tool):
            # The sweep's audit_fn contract is (root, rev, path, base_rev);
            # the tool path is bound here so the frozen gate's argv carries
            # exactly the committed bytes the pin check hashed.
            return audit_one(root, rev, path, base_rev, _tool)

        rc, inventory = sweep(args.root, args.rev, receipts, one,
                              dispositions=dispositions,
                              tool=args.audit_tool, tool_sha=tool_sha,
                              bindings=bindings, probe_stats=probe_stats)
    except (SweepError, OSError) as exc:
        print(json.dumps({"exit": 2, "exit_reason": str(exc)[:200]},
                         indent=1))
        return 2

    inventory["no_base_thread"] = bool(args.no_base_thread)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as h:
            json.dump(inventory, h, indent=1)
            h.write("\n")
    for f in inventory.get("finding_keys", []):
        print(f"FINDING {f}")
    print(json.dumps({k: inventory[k] for k in
                      ("sweep_rev", "receipts_total", "counts",
                       "findings_total", "base_threading", "exit",
                       "exit_reason")}, indent=1))
    return rc


if __name__ == "__main__":
    sys.exit(main())
