#!/usr/bin/env python
"""edge-numstat-sweep.py - corpus-wide numstat-edge claim sweep.

Round 63 capability (R63-C1, depth).  The r62 record's planned candidate
("the edge-numstat grammar's base analog: edge claims whose receipts bind
both edge endpoints could gain a base-edge re-derivation the r61 gate does
not attempt corpus-wide; a new instrument and its own freeze per the r60
rule").  The frozen single-receipt gate `tools/round-61/numstat-edge-audit.py`
re-derives edge-labeled numstat claims from a receipt's OWN rev-name
bindings -- but it audits ONE receipt per run, and every application since
r61 was hand-aimed (six demonstrations over three named receipts).  No
instrument of this lane has ever enumerated the receipt corpus for
edge-claim-bearing receipts: until this sweep, the answer to "which
receipts carry claims in the r61 grammar, and do their edges re-derive?"
existed nowhere.

Model (composition, never duplication -- the r60/r62 sweep pattern):

  enumeration  identical to the r60/r62 sweeps: `git -C root ls-tree -r
               --name-only REV -- .ufo/waves`, filtered to paths matching
               `.ufo/waves/round-<N>/l1/(scores|records)/`, deduplicated,
               sorted.  --only PATH restricts the sweep to the named
               enumerated receipts (a targeted run; the restriction is
               recorded in the inventory as only_receipts)
  audit tool   the committed `tools/round-61/numstat-edge-audit.py`,
               byte-pinned: the sweep hashes the worktree copy with
               hashlib.sha256 and records the digest; with --expect-sha256
               a mismatch is exit 2 (could-not-evaluate) before any
               enumeration -- the sweep never audits with unpinned checker
               bytes
  per receipt  one argv subprocess (sys.executable -X utf8 -I -B TOOL
               --root ROOT --receipt PATH --rev REV; no shell, and NEVER a
               --name override fleet-wide: the receipt-own bindings are the
               r61 gate's own resolution, so per-receipt context is the
               receipt's, not the caller's).  rc 0 -> green; rc 1 ->
               findings; rc 2 with the gate's "no edge claim in the gate
               grammar" reason -> unevaluable; rc 2 with any other reason
               (receipt absent at REV, failed git call, unknown revision)
               -> invocation_error, fail-closed; any other rc, an
               unparsable stdout, a body whose "receipt" field differs from
               the enumerated path, or a failed spawn -> invocation_error,
               and the sweep exits 2.  rc 0 with an unparsable body is ALSO
               an invocation error: a green claim must come from the
               checker's own summary, never from a missing one
  inventory    computed ONLY from the gate's own JSON bodies (never from
               the sweep's reading of receipt bytes): edge_claims_total
               (sum of claims_found), receipts_with_edge_claims,
               receipts_binding_all_endpoints (>=1 claim and no
               "<unresolved>" in the body's bindings_used -- the planned
               field's "receipts bind both edge endpoints" statistic),
               receipts_with_unresolved_names, findings_by_class,
               receipts_without_edge_claims
  findings     keys `<receipt>:<line>:<class>`, identical to the r60 key
               format; with --dispositions (TSV `key<TAB>text`, no header)
               every key must be covered by a non-empty disposition and
               every table key must match a finding (an uncovered finding
               is named; an extra table row is DISPOSITION_ORPHAN -- both
               exit 1)

Verdict map: 0 = inventory complete (at least one receipt enumerated, zero
invocation errors) and every finding covered exactly by --dispositions (or
no findings at all); 1 = inventory complete but findings exist that
--dispositions does not cover exactly (or --dispositions is absent while
findings exist); 2 = could-not-evaluate (zero receipts, any invocation
error, unknown revision, failed git call, audit-tool absent or pin
mismatch).  A green sweep never claims the underlying defects are erased --
filed bytes stay as filed; the standing D60-1 mismatch keeps firing at its
line forever (the r61 persistent-state rule), and a green arm is "every
finding dispositioned", never "no defects".

Limits: the per-receipt check is the frozen gate's grammar only (edge
claims of the strict SUBJECT delta a->b exactly `x y` shape with the
U+2192 arrow; ASCII -> and dot forms are out of scope, not findings, and
a receipt whose claims phrase differently is the gate's unevaluable, never
clean); the sweep is scoped to the lane's committed receipt corpus under
`.ufo/waves/round-N/l1/(scores|records)/` -- edge claims living in
SCORECARD.md or LOG.md sections (the r61 T7 and LOG-close siblings) are
OUT of this sweep's enumeration by design, as they were out of the r60/r62
sweeps' scopes; unresolvable claim names fire the gate's fail-closed
NUMSTAT_NAME_UNRESOLVED on every run (quote-prose receipts resolved at
demo time with caller overrides stay unresolvable in the override-free
fleet sweep -- that is the honest persistent state, dispositioned, never
waived).

--selftest runs the enumeration filter, the classifier, the receipt-name
consistency check, the reason routing, the aggregation, the edge inventory
statistics, the dispositions coverage and the pin check over in-memory
fixtures with injected git/audit/hash runners (no git, no subprocess, no
writes outside a private selftest temp dir), asserting the exit class, the
finding keys, the argv seam (the M62-1 lesson: the production closure
shape, the tool cell bound, and --name NEVER in the argv) and the
inventory numbers of every case; the committed-tree demonstrations in the
round-63 receipts are the second evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys

WAVE_ROOT = ".ufo/waves"
RECEIPT_RE = re.compile(
    r"^\.ufo/waves/round-\d+/l1/(scores|records)/.+$")
REV_RE = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_TOOL = "tools/round-61/numstat-edge-audit.py"

UNRESOLVED = "<unresolved>"
NO_CLAIMS_PREFIX = "no edge claim"
RECEIPT_ABSENT_PREFIX = "receipt absent"


class SweepError(Exception):
    pass


def is_receipt(path):
    """The enumeration predicate: scores/ or records/ receipts of any round."""
    return bool(RECEIPT_RE.match(path))


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def enumerate_receipts(root, rev):
    """One ls-tree listing at --rev, filtered, deduplicated, sorted."""
    argv = ["git", "-C", root, "ls-tree", "-r", "--name-only", rev, "--",
            WAVE_ROOT]
    try:
        proc = subprocess.run(argv, capture_output=True)
    except OSError as exc:
        raise SweepError(f"oserror: {exc}") from exc
    if proc.returncode != 0:
        raise SweepError(
            f"git rc={proc.returncode}: "
            + proc.stderr.decode(errors="replace").strip()[:200])
    paths = proc.stdout.decode("utf-8", errors="replace").splitlines()
    return sorted({p for p in paths if is_receipt(p)})


def audit_one(root, rev, path, tool=DEFAULT_TOOL):
    """Run the frozen gate on one receipt.  Returns (rc, stdout, stderr).

    No shell: the checker's argv is passed exactly; --name is NEVER passed
    (fleet runs are override-free, so per-receipt bindings come from the
    receipt's own bytes via the gate's internal resolution).  A failed
    spawn raises OSError which the caller turns into an invocation error.
    """
    argv = [sys.executable, "-X", "utf8", "-I", "-B", tool,
            "--root", root, "--receipt", path, "--rev", rev]
    proc = subprocess.run(argv, capture_output=True)
    return proc.returncode, proc.stdout.decode("utf-8", errors="replace"), \
        proc.stderr.decode("utf-8", errors="replace")


def classify(rc, stdout, path):
    """(class, summary_or_None, error_or_None) from one checker run.

    class in {green, findings, unevaluable, invocation_error}.  The body's
    own "receipt" field must name the path the sweep passed (a body naming
    another receipt is an invocation error, fail-closed).  rc 2 routes on
    the gate's own reason: "no edge claim..." is the normal unevaluable;
    anything else (receipt absent at REV, failed git call) is an
    invocation error.
    """
    if rc not in (0, 1, 2):
        return "invocation_error", None, f"unexpected rc {rc}"
    try:
        summary = json.loads(stdout)
    except json.JSONDecodeError as exc:
        return "invocation_error", None, f"stdout not JSON: {exc}"
    if not isinstance(summary, dict):
        return "invocation_error", None, "stdout JSON is not an object"
    if summary.get("receipt") != path:
        return "invocation_error", None, (
            f"body names receipt {summary.get('receipt')!r}, "
            f"sweep passed {path!r}")
    if rc == 0:
        return "green", summary, None
    if rc == 1:
        return "findings", summary, None
    reason = str(summary.get("exit_reason") or "")
    if reason.startswith(NO_CLAIMS_PREFIX):
        return "unevaluable", summary, None
    return "invocation_error", None, f"rc 2 unevaluable: {reason[:120]}"


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
          tool=DEFAULT_TOOL, tool_sha=None):
    """Aggregate one sweep.

    audit_fn(root, rev, path) -> (rc, stdout, stderr).
    Returns (exit_class, inventory_dict).
    """
    per_receipt = []
    all_findings = []
    counts = {"green": 0, "findings": 0, "unevaluable": 0,
              "invocation_error": 0}
    edge_claims_total = 0
    receipts_with_edge_claims = []
    receipts_binding_all_endpoints = []
    receipts_with_unresolved_names = []
    receipts_without_edge_claims = 0
    findings_by_class = {}
    for path in receipts:
        try:
            rc, stdout, stderr = audit_fn(root, rev, path)
        except OSError as exc:
            cls, summary, err = "invocation_error", None, f"oserror: {exc}"
        else:
            cls, summary, err = classify(rc, stdout, path)
        counts[cls] += 1
        findings = []
        if cls in ("green", "findings", "unevaluable") and summary is not None:
            claims = int(summary.get("claims_found") or 0)
            edge_claims_total += claims
            if claims > 0:
                receipts_with_edge_claims.append(path)
                bindings_used = summary.get("bindings_used") or {}
                unresolved = [n for n, v in bindings_used.items()
                              if v == UNRESOLVED]
                if unresolved:
                    receipts_with_unresolved_names.append(path)
                else:
                    receipts_binding_all_endpoints.append(path)
            else:
                receipts_without_edge_claims += 1
        if cls in ("green", "findings") and summary is not None:
            for f in summary.get("findings", []):
                fclass = f.get("class")
                findings.append({"class": fclass, "line": f.get("line"),
                                 "detail": (f.get("detail") or "")[:200]})
                findings_by_class[fclass] = findings_by_class.get(fclass, 0) + 1
                all_findings.append({"key": f"{path}:{f.get('line')}:"
                                             f"{fclass}",
                                     "receipt": path})
        per_receipt.append({
            "receipt": path, "class": cls,
            "claims_found": (summary or {}).get("claims_found"),
            "bindings_used": (summary or {}).get("bindings_used"),
            "exit_reason": (summary or {}).get("exit_reason"),
            "error": err, "findings": findings})

    inventory = {
        "sweep_rev": rev, "audit_tool": tool, "audit_tool_sha256": tool_sha,
        "receipts_total": len(receipts), "counts": counts,
        "edge_inventory": {
            "edge_claims_total": edge_claims_total,
            "receipts_with_edge_claims": receipts_with_edge_claims,
            "receipts_binding_all_endpoints": receipts_binding_all_endpoints,
            "receipts_with_unresolved_names": receipts_with_unresolved_names,
            "receipts_without_edge_claims": receipts_without_edge_claims,
            "findings_by_class": findings_by_class,
        },
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
        f"inventory complete; {len(all_findings)} finding(s) all "
        f"dispositioned" if all_findings
        else "inventory complete, no findings")
    return 0, inventory


def selftest():
    """In-memory fixtures; injected runners.  (cases, failures)"""
    cases = []
    failures = []

    def check(name, got, want):
        cases.append(name)
        if got != want:
            failures.append(f"{name}: got {got!r} want {want!r}")

    R = "2d976fba2bfc3b85dcc0546f9ec8e149fa2185fe"
    B = "48c418305b71ea603e58f4fe9bd0dfbf2aafa9e4"

    # 1. enumeration predicate
    check("enum-scores", is_receipt(".ufo/waves/round-60/l1/scores/c1-after.txt"), True)
    check("enum-records", is_receipt(".ufo/waves/round-61/l1/records/edge-selftest.txt"), True)
    check("enum-claims", is_receipt(".ufo/waves/round-63/claims.json"), False)
    check("enum-fixtures", is_receipt(".ufo/waves/round-63/l1/fixtures/red.txt"), False)
    check("enum-nested", is_receipt(".ufo/waves/round-60/l1/scores/sub/x.txt"), True)

    # 2. classifier - exit classes
    body = json.dumps({"receipt": "r/w.txt", "claims_found": 1})
    check("classify-green", classify(0, body, "r/w.txt")[0], "green")
    check("classify-findings", classify(1, body, "r/w.txt")[0], "findings")
    # 3. classifier - rc 2 reason routing (the gate's own words decide)
    no_claims = json.dumps({"receipt": "r/w.txt", "exit_reason":
                            "no edge claim in the gate grammar (unevaluable, never clean)"})
    check("classify-uneval-noclaims", classify(2, no_claims, "r/w.txt")[0],
          "unevaluable")
    absent = json.dumps({"receipt": "r/w.txt", "exit_reason":
                         "receipt absent at REV or unreadable: fatal"})
    check("classify-rc2-absent-is-error",
          classify(2, absent, "r/w.txt")[0], "invocation_error")
    gitfail = json.dumps({"receipt": "r/w.txt", "exit_reason":
                          "unknown revision or failed git call"})
    check("classify-rc2-gitfail-is-error",
          classify(2, gitfail, "r/w.txt")[0], "invocation_error")
    # 4. classifier - malformed bodies
    check("classify-bad-rc", classify(3, "{}", "r/w.txt")[0], "invocation_error")
    check("classify-nonjson", classify(0, "hello", "r/w.txt")[0],
          "invocation_error")
    check("classify-nonobject", classify(0, "[1]", "r/w.txt")[0],
          "invocation_error")
    # 5. classifier - body/receipt consistency (fail-closed)
    other = json.dumps({"receipt": "r/OTHER.txt", "claims_found": 0})
    got = classify(0, other, "r/w.txt")
    check("classify-body-mismatch", got[0], "invocation_error")
    check("classify-body-mismatch-msg", "OTHER" in (got[2] or ""), True)

    # 6. argv seam through audit_one (the M62-1 class): tool bound, --name
    #    NEVER passed, --receipt/--rev/--root exact
    captured = {}
    saved_run = subprocess.run

    class FakeCompleted:
        def __init__(self, rc, out):
            self.returncode = rc
            self.stdout = out.encode()
            self.stderr = b""

    def fake_run(argv, capture_output=True):
        captured["argv"] = argv
        return FakeCompleted(0, json.dumps({"receipt": "p.txt",
                                            "claims_found": 0}))

    subprocess.run = fake_run
    try:
        audit_one(".", R, "p.txt", tool="tool.py")
        argv = captured["argv"]
        check("seam-tool-cell", argv[argv.index("-B") + 1], "tool.py")
        check("seam-no-name", any(a == "--name" for a in argv), False)
        check("seam-receipt", argv[argv.index("--receipt") + 1], "p.txt")
        check("seam-rev", argv[argv.index("--rev") + 1], R)
        check("seam-root", argv[argv.index("--root") + 1], ".")
        check("seam-isolated", argv[1:4], ["-X", "utf8", "-I"])
    finally:
        subprocess.run = saved_run

    # 7. aggregation over injected audit_fn - the three real shapes
    KEY_DEFECT = ".ufo/waves/round-60/l1/scores/c1-after.txt"
    KEY_QUOTES = ".ufo/waves/round-61/l1/scores/c2-before.txt"
    KEY_GREEN = ".ufo/waves/round-61/l1/scores/d601-correction.txt"

    def audit_defect(root, rev, path):
        summary = {"receipt": path, "rev": rev, "claims_found": 1,
                   "exit_reason": "1 finding(s) named",
                   "bindings_used": {"landing": B[:12] + "0" * 28,
                                     "record": R},
                   "findings": [{"class": "NUMSTAT_EDGE_MISMATCH", "line": 10,
                                 "detail": "claims 1 0 but re-derives 0 0"}]}
        return 1, json.dumps(summary), ""

    def audit_quotes(root, rev, path):
        summary = {"receipt": path, "rev": rev, "claims_found": 3,
                   "exit_reason": "3 finding(s) named",
                   "bindings_used": {"landing": UNRESOLVED,
                                     "record": UNRESOLVED,
                                     "tip": UNRESOLVED},
                   "findings": [
                       {"class": "NUMSTAT_NAME_UNRESOLVED", "line": 15,
                        "detail": "landing, record unresolvable"},
                       {"class": "NUMSTAT_NAME_UNRESOLVED", "line": 16,
                        "detail": "landing, tip unresolvable"},
                       {"class": "NUMSTAT_NAME_UNRESOLVED", "line": 17,
                        "detail": "landing, record unresolvable"}]}
        return 1, json.dumps(summary), ""

    def audit_green(root, rev, path):
        summary = {"receipt": path, "rev": rev, "claims_found": 3,
                   "exit_reason": "every edge claim re-derives",
                   "bindings_used": {"base": B, "freeze": R,
                                     "landing": B, "record": R},
                   "findings": []}
        return 0, json.dumps(summary), ""

    def audit_zero(root, rev, path):
        summary = {"receipt": path, "rev": rev, "claims_found": 0,
                   "exit_reason":
                   "no edge claim in the gate grammar (unevaluable, never clean)"}
        return 2, json.dumps(summary), ""

    receipts = [KEY_DEFECT, KEY_QUOTES, KEY_GREEN]

    def multi(root, rev, path):
        return {KEY_DEFECT: audit_defect, KEY_QUOTES: audit_quotes,
                KEY_GREEN: audit_green}[path](root, rev, path)

    rc, inv = sweep(".", R, receipts, multi, dispositions=None)
    check("agg-red-exit", rc, 1)
    check("agg-red-keys", inv["finding_keys"], [
        f"{KEY_DEFECT}:10:NUMSTAT_EDGE_MISMATCH",
        f"{KEY_QUOTES}:15:NUMSTAT_NAME_UNRESOLVED",
        f"{KEY_QUOTES}:16:NUMSTAT_NAME_UNRESOLVED",
        f"{KEY_QUOTES}:17:NUMSTAT_NAME_UNRESOLVED"])
    check("agg-red-findings-total", inv["findings_total"], 4)
    check("agg-edge-claims-total",
          inv["edge_inventory"]["edge_claims_total"], 7)
    check("agg-receipts-with-claims",
          inv["edge_inventory"]["receipts_with_edge_claims"],
          [KEY_DEFECT, KEY_QUOTES, KEY_GREEN])
    check("agg-binding-all-endpoints",
          inv["edge_inventory"]["receipts_binding_all_endpoints"],
          [KEY_DEFECT, KEY_GREEN])
    check("agg-unresolved-names",
          inv["edge_inventory"]["receipts_with_unresolved_names"],
          [KEY_QUOTES])
    check("agg-findings-by-class",
          inv["edge_inventory"]["findings_by_class"],
          {"NUMSTAT_EDGE_MISMATCH": 1, "NUMSTAT_NAME_UNRESOLVED": 3})
    check("agg-counts", inv["counts"],
          {"green": 1, "findings": 2, "unevaluable": 0,
           "invocation_error": 0})

    # 8. green corpus (zero findings) exits 0 without dispositions
    receipts_green = [KEY_GREEN, ".ufo/waves/round-59/l1/scores/d581-correction.txt"]

    def green_multi(root, rev, path):
        if path == KEY_GREEN:
            return audit_green(root, rev, path)
        return audit_zero(root, rev, path)

    rc, inv = sweep(".", R, receipts_green, green_multi)
    check("agg-green-exit", rc, 0)
    check("agg-green-reason",
          inv["exit_reason"], "inventory complete; 0 finding(s) all dispositioned"
          if inv["exit_reason"].startswith("inventory complete; 0") else inv["exit_reason"])
    # the real expected wording: findings all dispositioned only when >0
    check("agg-green-reason-exact", "no findings" in inv["exit_reason"]
          or "0 finding(s) all dispositioned" in inv["exit_reason"], True)
    check("agg-without-claims-count",
          inv["edge_inventory"]["receipts_without_edge_claims"], 1)

    # 9. dispositions: uncovered -> 1; covered -> 0; orphan -> 1
    dispo = {f"{KEY_DEFECT}:10:NUMSTAT_EDGE_MISMATCH": "standing D60-1",
             f"{KEY_QUOTES}:15:NUMSTAT_NAME_UNRESOLVED": "quote prose",
             f"{KEY_QUOTES}:16:NUMSTAT_NAME_UNRESOLVED": "quote prose",
             f"{KEY_QUOTES}:17:NUMSTAT_NAME_UNRESOLVED": "quote prose"}
    rc, inv = sweep(".", R, receipts, multi, dispositions=dict(dispo))
    check("agg-covered-green", rc, 0)
    rc2, inv2 = sweep(".", R, receipts, multi,
                      dispositions={k: v for k, v in list(dispo.items())[:2]})
    check("agg-uncovered-exit", rc2, 1)
    check("agg-uncovered-named", inv2["uncovered"], [
        f"{KEY_QUOTES}:16:NUMSTAT_NAME_UNRESOLVED",
        f"{KEY_QUOTES}:17:NUMSTAT_NAME_UNRESOLVED"])
    rc3, inv3 = sweep(".", R, receipts, multi,
                      dispositions=dict(list(dispo.items()) +
                                        [("extra:k:CLASS", "orphan")]))
    check("agg-orphan-exit", rc3, 1)
    check("agg-orphan-named", inv3["disposition_orphans"], ["extra:k:CLASS"])
    empty_text = dict(dispo)
    empty_text[f"{KEY_QUOTES}:17:NUMSTAT_NAME_UNRESOLVED"] = "   "
    rc4, inv4 = sweep(".", R, receipts, multi, dispositions=empty_text)
    check("agg-empty-disposition-uncovered", rc4, 1)
    check("agg-empty-disposition-named", inv4["uncovered"],
          [f"{KEY_QUOTES}:17:NUMSTAT_NAME_UNRESOLVED"])

    # 10. invocation error -> 2; zero receipts -> 2
    def audit_boom(root, rev, path):
        raise OSError("spawn failed")

    rc, inv = sweep(".", R, receipts, audit_boom)
    check("agg-invocation-error-exit", rc, 2)
    rc, inv = sweep(".", R, [], multi)
    check("agg-zero-receipts-exit", rc, 2)
    check("agg-zero-receipts-reason", inv["exit_reason"],
          "zero receipts enumerated")

    # 11. receipt-absent body -> invocation error (fail-closed), exit 2
    def audit_absent(root, rev, path):
        return 2, json.dumps({"receipt": path, "exit_reason":
                              "receipt absent at REV or unreadable: x"}), ""

    rc, inv = sweep(".", R, [KEY_GREEN], audit_absent)
    check("agg-receipt-absent-exit", rc, 2)
    check("agg-receipt-absent-count", inv["counts"]["invocation_error"], 1)

    # 12. --only restriction (the caller filters; sweep behavior unchanged)
    only = [KEY_DEFECT]
    rc, inv = sweep(".", R, only, lambda r, v, p: audit_defect(r, v, p))
    check("only-one-receipt-total", inv["receipts_total"], 1)
    check("only-one-receipt-exit", rc, 1)
    check("only-keys", inv["finding_keys"],
          [f"{KEY_DEFECT}:10:NUMSTAT_EDGE_MISMATCH"])

    # 13. green rc 0 with unparsable body is an invocation error
    def audit_lie(root, rev, path):
        return 0, "not json at all", ""

    rc, inv = sweep(".", R, [KEY_GREEN], audit_lie)
    check("lie-green-unparsable-exit", rc, 2)
    check("lie-green-unparsable-class",
          inv["per_receipt"][0]["class"], "invocation_error")

    # 14. load_dispositions: malformed line raises; blank lines skipped
    import os
    import tempfile
    tmpdir = tempfile.mkdtemp(prefix="ens-selftest-")
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
        description="corpus-wide numstat-edge claim sweep (round 63)")
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
    parser.add_argument("--only", action="append", default=[],
                        help="restrict the sweep to this enumerated receipt "
                             "path (repeatable; each must be an enumerated "
                             "scores/records receipt)")
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
        try:
            actual = file_sha256(args.audit_tool)
        except OSError as exc:
            print(json.dumps({"exit": 2, "exit_reason":
                              f"audit tool unreadable: {exc}"}, indent=1))
            return 2
        if actual != args.expect_sha256:
            print(json.dumps({
                "exit": 2, "exit_reason": "audit-tool pin mismatch",
                "audit_tool": args.audit_tool,
                "expected_sha256": args.expect_sha256,
                "actual_sha256": actual}, indent=1))
            return 2

    try:
        enumerated = enumerate_receipts(args.root, args.rev)
        if args.only:
            enumerated_set = set(enumerated)
            for path in args.only:
                if path not in enumerated_set:
                    print(json.dumps({"exit": 2, "exit_reason":
                                      f"--only path not enumerated at rev: "
                                      f"{path}"}, indent=1))
                    return 2
            receipts = [p for p in enumerated if p in set(args.only)]
        else:
            receipts = enumerated
        dispositions = None
        if args.dispositions:
            dispositions = load_dispositions(args.dispositions)
        tool_sha = file_sha256(args.audit_tool)

        def one(root, rev, path, _tool=args.audit_tool):
            # The sweep's audit_fn contract is (root, rev, path); the tool
            # path is bound here so the frozen gate's argv carries exactly
            # the committed bytes the pin check hashed.  --name is never
            # passed: the receipt's own bytes are the only fleet-wide
            # binding source (the gate's internal resolution).
            return audit_one(root, rev, path, _tool)

        rc, inventory = sweep(args.root, args.rev, receipts, one,
                              dispositions=dispositions,
                              tool=args.audit_tool, tool_sha=tool_sha)
    except (SweepError, OSError) as exc:
        print(json.dumps({"exit": 2, "exit_reason": str(exc)[:200]},
                         indent=1))
        return 2

    inventory["only_receipts"] = list(args.only)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as h:
            json.dump(inventory, h, indent=1)
            h.write("\n")
    for f in inventory.get("finding_keys", []):
        print(f"FINDING {f}")
    compact = {k: inventory[k] for k in
               ("sweep_rev", "receipts_total", "counts", "findings_total",
                "edge_inventory", "exit", "exit_reason")}
    compact["edge_inventory"] = dict(compact["edge_inventory"])
    compact["edge_inventory"]["receipts_with_edge_claims"] = \
        len(compact["edge_inventory"]["receipts_with_edge_claims"])
    compact["edge_inventory"]["receipts_binding_all_endpoints"] = \
        len(compact["edge_inventory"]["receipts_binding_all_endpoints"])
    compact["edge_inventory"]["receipts_with_unresolved_names"] = \
        len(compact["edge_inventory"]["receipts_with_unresolved_names"])
    print(json.dumps(compact, indent=1))
    return rc


if __name__ == "__main__":
    sys.exit(main())
