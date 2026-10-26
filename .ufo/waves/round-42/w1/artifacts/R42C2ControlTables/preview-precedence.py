#!/usr/bin/env python3
"""preview-precedence.py -- R42-C2 precedence preview (round 42 wave 1, DEV, not frozen).

Derived from `tools/round-41/indep-eval-v3.py` (base c4a38ea) with ONE substantive
change: the numbered list in the `## R42-C2` section of
kaidoku-shokunin/plans/round-42-claims.md (13 steps) replaces the round-41 list of 12,
so steps 2 (F = no squashfs handler, not "no v4 handler"), 6 (legacy-body-failure) and
7..13 are renumbered per the draft.  The envelope field map, BE/SR/P extraction,
`ACTION_BY_LABEL`, the wrapping rules and the CLI are the round-41 evaluator's.

Baseline check: on the 52 committed round-41 dev envelopes this file reproduces the
round-41 evaluator's (label, action) 52/52, because every one of those carriers uses a
`squashfs_v4_*` handler where the two precedence texts agree.  That equality is the
calibration anchor (section 4 of ../R42C2ControlTables.md); the round-41 evaluator
itself is kept in this directory as `ref-indep-eval-v3.py` for the comparison.

It is NOT the claim's frozen evaluator: R42C2Eval's `tools/round-42/indep-eval-v4.py`
is, and every control number in ../R42C2ControlTables.md must be re-derived from it at
the freeze.  Its only output is (label, action); it never reads SKILL.md, a triage
table, the interpreter or a generator.

Inputs kept verbatim from the round-41 evaluator:
  1. the `**Label precedence**` numbered list in
     kaidoku-shokunin/plans/round-41-claims.md (the twelve steps, now superseded);
  2. REA 6.5.0 envelope structure, observed in committed envelopes under
     corpus/evidence/round-40/c2/heldout/*/envelope.json and
     corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json, and in
     rea-agents/dist/firmware/{FirmwarePublication,FirmwareReports,FirmwareFiles}.js;
  3. nothing else.

The only output is (label, action); `action` comes from ACTION_BY_LABEL, a
fixed map transcribed from the precedence's own label list, so the evaluator
carries no table-derived knowledge of what an outcome is "supposed" to mean.

CLI
  indep-eval-v3.py --envelopes DIR [--out FILE] [--full]
      DIR holds either one JSON envelope per file, or one sub-directory per
      envelope containing envelope.json / rea-full.json / *.json.  With
      --full, rea-full.json (the `{ok,data,meta}` CLI envelope) is preferred
      over the bare data object.  Prints JSON: one (label, action, step,
      features, extraction provenance) record per envelope id.
  indep-eval-v3.py --selftest
      38 synthetic feature tuples: at least one per precedence step plus the
      boundaries this file documents as ambiguous.

Envelope field map (each feature names the field it was read from):

  OP  operation                       top-level `operation`
  PR  provider                        `provider.id`
  H   handler set                     `normalized_result.chunks[].handler`
                                      + `normalized_result.extraction_gaps[].handler`
                                      (fallback: raw_result `ChunkReport.handler_name`)
  HF  failing-chunk handler set       `normalized_result.extraction_gaps[].handler`
                                      where `.kind == "extractor-failure"` (step 5 only)
  G   gap-kind set                    `normalized_result.extraction_gaps[].kind`
  D   dependency-name set             `normalized_result.extraction_gaps[].dependencies[]`
                                      + `normalized_result.diagnostics[].missing_dependencies[]`
                                      + `normalized_result.diagnostics[].report.dependencies[]`
  BE  `-be` in a recorded child argv  argv text from `normalized_result.diagnostics[].report.command`
                                      (list form: `.report.argv` / `.argv`); exact argv token,
                                      not substring
  SR  symlink removed                 `normalized_result.diagnostics[].report.__typename__`
                                      == "MaliciousSymlinkRemoved" (fallback: the same
                                      token in `raw_result.execution.stdout.text`)
  P   published regular files         len(`normalized_result.files`)

Stdlib only; no network, no writes outside --out.
"""

import argparse
import json
import os
import re
import shlex
import sys

# --------------------------------------------------------------------------
# The thirteen precedence steps of the round-42 draft, transcribed from
# plans/round-42-claims.md `## R42-C2`.  Kept as text so the report can quote
# what each code branch implements.
# --------------------------------------------------------------------------
PRECEDENCE = [
    "1. OP != extract_firmware or PR != unblob -> (unclassified, none).",
    "2. F = empty and depth-limited in G -> container-depth-limited.",
    "3. F = empty -> no-squashfs-chunk.",
    "4. missing-extractor-dependency in G -> dep-missing-be if D holds sasquatch-v4be, "
    "else dep-missing-le if D holds sasquatch, else continue.",
    "5. extractor-failure in G and P > 0 -> partial-body-failure.",
    "6. extractor-failure in G, P = 0, BE = no, squashfs_v4_be in HF -> "
    "avm-marker-be-dropped.",
    "7. extractor-failure in G, P = 0, HF intersects L -> legacy-body-failure.",
    "8. extractor-failure in G, P = 0 -> body-extractor-failure.",
    "9. unknown-chunk-handler in G -> unknown-residue.",
    "10. depth-limited in G -> depth-limited.",
    "11. SR = yes and unpublished-entry in G -> mixed-symlinks.",
    "12. SR = yes and G = empty -> escaping-symlink-removed.",
    "13. G = {unpublished-entry} -> in-tree-symlink-metadata.",
    "14. G = empty, P > 0 -> clean; G = empty, P = 0 -> clean-empty.",
    "15. anything else -> (unclassified, none).",
]

# Fixed map written from the precedence's labels.  No label outside this map is
# ever produced; a label outside this map is a bug, not a new outcome.
ACTION_BY_LABEL = {
    "no-squashfs-chunk": "inspect-input",
    "dep-missing-be": "install-extractor-be",
    "dep-missing-le": "install-extractor-le",
    "partial-body-failure": "salvage-partial",
    "avm-marker-be-dropped": "wrap-extractor-be",
    "body-extractor-failure": "preserve-failure",
    "legacy-body-failure": "cross-read-legacy",
    "container-depth-limited": "raise-depth",
    "unknown-residue": "isolate-residue",
    "depth-limited": "raise-depth",
    "mixed-symlinks": "audit-symlinks",
    "escaping-symlink-removed": "expect-link-absent",
    "in-tree-symlink-metadata": "count-gap",
    "clean": "none",
    "clean-empty": "confirm-empty",
    "unclassified": "none",
}

SQUASHFS_HANDLER_PREFIX = "squashfs_"
LEGACY_HANDLER_RE = r"^squashfs_v[123]"
BE_DEPENDENCY = "sasquatch-v4be"
LE_DEPENDENCY = "sasquatch"
AVM_HANDLER = "squashfs_v4_be"
REMOVED_SYMLINK_TYPENAME = "MaliciousSymlinkRemoved"
TYPENAME_KEYS = ("__typename__", "type", "kind", "name")


# --------------------------------------------------------------------------
# envelope access
# --------------------------------------------------------------------------
def unwrap(doc):
    """Accept a bare data object or a full CLI envelope `{ok,data,meta}`.

    The CLI envelope is recognised by `data` being an object that looks like an
    analysis envelope (has `operation` or `normalized_result`); anything else is
    treated as the data object itself.  Returns (data_object, wrapped?).
    """
    if isinstance(doc, dict):
        data = doc.get("data")
        if isinstance(data, dict) and (
            "operation" in data or "normalized_result" in data or "provider" in data
        ):
            return data, True
    return doc, False


def _iter_dicts(value):
    """Yield every dict reachable from `value` (bounded, non-recursive-safe)."""
    stack = [value]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def _argv_strings(nr):
    """Every recorded child argv string/text under `normalized_result.diagnostics`.

    REA keeps the producer's failure report verbatim; the child argv is
    `diagnostics[].report.command` (a string) in unblob 26.6.4 envelopes.
    """
    out = []
    for diag in nr.get("diagnostics") or []:
        if not isinstance(diag, dict):
            continue
        for holder in (diag, diag.get("report") if isinstance(diag.get("report"), dict) else None):
            if not isinstance(holder, dict):
                continue
            for key in ("command", "argv", "args"):
                val = holder.get(key)
                if isinstance(val, str) and val.strip():
                    out.append(val)
                elif isinstance(val, list) and val and all(isinstance(x, str) for x in val):
                    out.append(" ".join(val))
    return out


def _argvs_be_state(nr):
    """BE as the precedence's `-be in a recorded child argv (yes/no/n/a)`.

    'yes' -- some recorded argv carries `-be` as its own token.
    'no'  -- at least one argv was recorded and none carries `-be`.
    'n/a' -- no child argv was recorded at all (the extractor never ran).

    A substring test is wrong on purpose-built evidence: `sasquatch-v4be` and
    `-no-exit-code` both contain the letters b,e; only token equality is
    honest.  Returns (state, note).
    """
    argvs = _argv_strings(nr)
    if not argvs:
        return "n/a", "no diagnostics[].report.command recorded"
    tokens = []
    for argv in argvs:
        try:
            tokens.extend(shlex.split(argv))
        except ValueError:
            tokens.extend(argv.split())
    has = "-be" in tokens
    return ("yes" if has else "no"), ("argv: " + " | ".join(argvs))[:400]


def _removed_symlink(nr, doc):
    """SR: a symlink was removed during extraction (yes/no) + where it was seen.

    REA publishes only regular files and records an in-tree symlink as an
    `unpublished-entry`; an escaping/empty-target symlink is deleted by the
    producer's sandbox and leaves NO `extraction_gaps` row (that silence is
    R40-CL6/L6).  The observable trace is the producer's own report, kept
    verbatim in `normalized_result.diagnostics[].report`: typename
    "MaliciousSymlinkRemoved" with `link`/`target`.  As a defence against a
    trimmed `normalized_result`, the same token is also looked for in
    `raw_result.execution.stdout.text` (unblob's summary line).
    """
    for diag in nr.get("diagnostics") or []:
        for holder in (diag, diag.get("report") if isinstance(diag.get("report"), dict) else None):
            if not isinstance(holder, dict):
                continue
            for key in TYPENAME_KEYS:
                if holder.get(key) == REMOVED_SYMLINK_TYPENAME:
                    return True, "normalized_result.diagnostics[].report.%s" % key
    stdout = (
        (((doc.get("raw_result") or {}).get("execution") or {}).get("stdout") or {}).get("text")
        or ""
    )
    if REMOVED_SYMLINK_TYPENAME in stdout:
        return True, "raw_result.execution.stdout.text"
    return False, "absent"


def features(doc):
    """Extract OP, PR, H, G, D, BE, SR, P and the field each came from."""
    data, wrapped = unwrap(doc)
    if not isinstance(data, dict):
        return {
            "OP": None, "PR": None, "H": [], "HF": [], "G": [], "D": [],
            "BE": "n/a", "SR": "no", "P": 0,
            "_prov": {"error": "envelope is not a JSON object"},
            "_id": None, "_wrapped": False,
        }
    nr = data.get("normalized_result")
    nr = nr if isinstance(nr, dict) else {}

    op = data.get("operation")
    provider = data.get("provider")
    pr = provider.get("id") if isinstance(provider, dict) else None

    handlers = set()
    prov_h = []
    for chunk in nr.get("chunks") or []:
        if isinstance(chunk, dict) and isinstance(chunk.get("handler"), str) and chunk["handler"]:
            handlers.add(chunk["handler"])
            prov_h.append("chunks[].handler")
    for gap in nr.get("extraction_gaps") or []:
        if isinstance(gap, dict) and isinstance(gap.get("handler"), str) and gap["handler"]:
            handlers.add(gap["handler"])
            prov_h.append("extraction_gaps[].handler")
    if not prov_h:
        # Only when normalized_result carries no chunk/gap handler: fall back to
        # the producer's raw ChunkReport, which names the same handler.
        for rec in ((data.get("raw_result") or {}).get("report") or []):
            if not isinstance(rec, dict):
                continue
            for report in rec.get("reports") or []:
                if isinstance(report, dict) and report.get("__typename__") == "ChunkReport":
                    name = report.get("handler_name")
                    if isinstance(name, str) and name:
                        handlers.add(name)
                        prov_h.append("raw_result.report[].reports[].handler_name")

    gaps = set()
    prov_g = "absent"
    for gap in nr.get("extraction_gaps") or []:
        if isinstance(gap, dict) and isinstance(gap.get("kind"), str):
            gaps.add(gap["kind"])
            prov_g = "extraction_gaps[].kind"

    # HF: handler(s) carried by the extractor-failure gap itself.  Steps 4-6 are
    # about one failing extraction, and REA reports which handler failed on that
    # gap; H is the run-wide handler set and can hold several chunks.  Step 5's
    # "handler squashfs_v4_be" is read against HF when the envelope distinguishes
    # them, and against H otherwise.
    failing_handlers = set()
    for gap in nr.get("extraction_gaps") or []:
        if (isinstance(gap, dict) and gap.get("kind") == "extractor-failure"
                and isinstance(gap.get("handler"), str) and gap["handler"]):
            failing_handlers.add(gap["handler"])

    deps = set()
    prov_d = []
    for gap in nr.get("extraction_gaps") or []:
        for dep in (gap.get("dependencies") or []) if isinstance(gap, dict) else []:
            if isinstance(dep, str):
                deps.add(dep)
                prov_d.append("extraction_gaps[].dependencies[]")
    for diag in nr.get("diagnostics") or []:
        if not isinstance(diag, dict):
            continue
        for holder in (diag, diag.get("report") if isinstance(diag.get("report"), dict) else None):
            if not isinstance(holder, dict):
                continue
            for key in ("missing_dependencies", "dependencies"):
                for dep in holder.get(key) or []:
                    if isinstance(dep, str):
                        deps.add(dep)
                        prov_d.append("diagnostics[]." + key + "[]")

    be, be_note = _argvs_be_state(nr)
    sr, sr_note = _removed_symlink(nr, data)

    files = nr.get("files")
    p = len(files) if isinstance(files, list) else 0
    p_note = "len(normalized_result.files)" if isinstance(files, list) else "normalized_result.files absent -> 0"

    evidence_id = None
    if isinstance(data.get("evidence_id"), str):
        evidence_id = data["evidence_id"]
    elif isinstance(doc.get("data"), dict) and isinstance(doc["data"].get("evidence_id"), str):
        evidence_id = doc["data"]["evidence_id"]

    return {
        "OP": op,
        "PR": pr,
        "H": sorted(handlers),
        "HF": sorted(failing_handlers),
        "G": sorted(gaps),
        "D": sorted(deps),
        "BE": be,
        "SR": sr,
        "P": p,
        "_prov": {
            "OP": "operation",
            "PR": "provider.id",
            "H": sorted(set(prov_h)) or "absent",
            "HF": "extraction_gaps[].handler where kind == extractor-failure" if failing_handlers
                  else "absent (no extractor-failure gap handler; step 5 falls back to H)",
            "G": prov_g,
            "D": sorted(set(prov_d)) or "absent",
            "BE": be_note,
            "SR": sr_note,
            "P": p_note,
            "wrapped_cli_envelope": wrapped,
            "normalized_result_present": bool(nr),
        },
        "_id": evidence_id,
    }


# --------------------------------------------------------------------------
# the classification: one branch per precedence step, in order
# --------------------------------------------------------------------------
def classify(feats):
    """Return (label, action, step) for a feature tuple, applying A1 steps 1..15."""
    op = feats.get("OP")
    pr = feats.get("PR")
    h = set(feats.get("H") or [])
    g = set(feats.get("G") or [])
    d = set(feats.get("D") or [])
    be = feats.get("BE")
    sr = (feats.get("SR") == "yes") or feats.get("SR") is True
    p = feats.get("P") or 0

    # F: the SquashFS handler names in H; L: the v1-v3 family inside F
    squashfs = {name for name in h if name.startswith(SQUASHFS_HANDLER_PREFIX)}
    legacy = {name for name in squashfs if re.match(LEGACY_HANDLER_RE, name)}
    # HF: the handlers of the extractor-failure gaps; if none carries one, HF = F
    hf = {name for name in (feats.get("HF") or []) if name} or squashfs

    # 1
    if op != "extract_firmware" or pr != "unblob":
        return _done("unclassified", 1)
    # 2  no squashfs handler at this depth but the run was depth-capped: the image may
    #    sit inside a container below the budget (round-42 A1)
    if not squashfs and "depth-limited" in g:
        return _done("container-depth-limited", 2)
    # 3  F empty and not depth-capped: nothing SquashFS was carved (round-41 defect R41-CL4)
    if not squashfs:
        return _done("no-squashfs-chunk", 3)
    # 4  D "holds" a dependency: exact membership, never substring --
    #    "sasquatch" is a substring of "sasquatch-v4be", so substring matching
    #    would relabel every BE dependency as LE.  be is tested first because
    #    the precedence names it first.  A dependency gap naming neither
    #    continues at step 5.
    if "missing-extractor-dependency" in g:
        if BE_DEPENDENCY in d:
            return _done("dep-missing-be", 4)
        if LE_DEPENDENCY in d:
            return _done("dep-missing-le", 4)
    # 5
    if "extractor-failure" in g and p > 0:
        return _done("partial-body-failure", 5)
    # 6
    if ("extractor-failure" in g and p == 0 and be == "no"
            and AVM_HANDLER in hf):
        return _done("avm-marker-be-dropped", 6)
    # 7  a failing v1-v3 extraction: no byte-order handshake or AVM pre-check applies
    if "extractor-failure" in g and p == 0 and (hf & legacy):
        return _done("legacy-body-failure", 7)
    # 8
    if "extractor-failure" in g and p == 0:
        return _done("body-extractor-failure", 8)
    # 9  unclaimed bytes beside the chunk (A1: placed before the depth row)
    if "unknown-chunk-handler" in g:
        return _done("unknown-residue", 9)
    # 10
    if "depth-limited" in g:
        return _done("depth-limited", 10)
    # 11
    if sr and "unpublished-entry" in g:
        return _done("mixed-symlinks", 11)
    # 12
    if sr and not g:
        return _done("escaping-symlink-removed", 12)
    # 13
    if g == {"unpublished-entry"}:
        return _done("in-tree-symlink-metadata", 13)
    # 14
    if not g:
        return _done("clean" if p > 0 else "clean-empty", 14)
    # 15
    return _done("unclassified", 15)


def _done(label, step):
    return label, ACTION_BY_LABEL[label], step


# --------------------------------------------------------------------------
# synthetic tuples for --selftest
# --------------------------------------------------------------------------
def _env(op="extract_firmware", pr="unblob", handlers=("squashfs_v4_be",), gaps=(),
         deps=(), argv=None, sr=False, p=1, wrapped=False, gap_handlers=None,
         files_absent=False):
    """Build a minimal envelope carrying only the fields the evaluator reads.

    `gap_handlers` maps a gap kind to the handler REA records on that gap row
    (the failing extraction's handler); the default leaves it null, as the
    depth-limited and unpublished-entry rows always are.
    """
    gap_handlers = gap_handlers or {}
    diagnostics = []
    if argv is not None:
        diagnostics.append({"input_path": "$input", "stage": "squashfs_v4_be",
                            "report": {"severity": "ERROR", "command": argv, "exit_code": 1,
                                       "__typename__": "ExtractCommandFailedReport"}})
    if sr:
        diagnostics.append({"input_path": "$input", "report": {
            "severity": "WARNING", "link": "$output/a", "target": "../b",
            "__typename__": "MaliciousSymlinkRemoved"}})
    nr = {
        "chunks": [{"handler": name, "extraction_failed": "extractor-failure" in gaps}
                   for name in handlers],
        "extraction_gaps": [{"kind": kind, "handler": gap_handlers.get(kind),
                             "dependencies": list(deps) if kind == "missing-extractor-dependency" else []}
                            for kind in gaps],
        "diagnostics": diagnostics,
        "files": [{"relative_path": "f%02d" % i, "sha256": "%064x" % i} for i in range(p)],
        "unpublished_entries": ([{"kind": "symlink", "relative_path": "s", "link_target": "../t"}]
                                if "unpublished-entry" in gaps else []),
    }
    if files_absent:
        del nr["files"]
    data = {"evidence_id": "ev_synthetic", "operation": op, "provider": {"id": pr},
            "normalized_result": nr}
    if wrapped:
        return {"ok": True, "data": data, "meta": {}}
    return data


SELFTEST_CASES = [
    # (name, envelope, expected label, expected step)
    # step 1
    ("s1-op-inspect", _env(op="inspect_firmware_regions"), "unclassified", 1),
    ("s1-pr-binwalk", _env(pr="binwalk"), "unclassified", 1),
    ("s1-op-spelling-extract-firmware", _env(op="extract-firmware"), "unclassified", 1),
    # step 2
    ("s2-no-handler", _env(handlers=(), p=0), "no-squashfs-chunk", 3),
    ("s2-handler-elsewhere", _env(handlers=("gzip",), p=0), "no-squashfs-chunk", 3),
    ("s2-le-handler-is-a-squashfs-handler", _env(handlers=("squashfs_v4_le",), p=2), "clean", 14),
    # step 3
    ("s3-dep-be", _env(handlers=("squashfs_v4_be",), gaps=("missing-extractor-dependency",),
                       deps=("sasquatch-v4be",), p=0), "dep-missing-be", 4),
    ("s3-dep-le", _env(handlers=("squashfs_v4_le",), gaps=("missing-extractor-dependency",),
                       deps=("sasquatch",), p=0), "dep-missing-le", 4),
    ("s3-dep-both-be-first", _env(gaps=("missing-extractor-dependency",),
                                  deps=("sasquatch", "sasquatch-v4be"), p=0), "dep-missing-be", 4),
    ("s3-dep-other-name-falls-through", _env(gaps=("missing-extractor-dependency",),
                                             deps=("unsquashfs",), p=0), "unclassified", 15),
    ("s3-LE-substring-must-not-match-be", _env(gaps=("missing-extractor-dependency",),
                                               deps=("sasquatch-v4be-x",), p=0), "unclassified", 15),
    ("s3-be-substring-must-not-match-le", _env(gaps=("missing-extractor-dependency",),
                                               deps=("xsasquatch",), p=0), "unclassified", 15),
    ("s3-dep-in-gap-only-handler", _env(handlers=(), gaps=("missing-extractor-dependency",),
                                        deps=("sasquatch-v4be",), p=0),
     "no-squashfs-chunk", 3),
    # step 4 (combined sets included)
    ("s4-partial", _env(gaps=("extractor-failure",), argv="sasquatch-v4be -be -f -d out in",
                        p=5), "partial-body-failure", 5),
    ("s4-partial-p1", _env(gaps=("extractor-failure",), argv="sasquatch-v4be -be -f -d out in",
                           p=1), "partial-body-failure", 5),
    ("s4-partial-plus-in-tree", _env(gaps=("extractor-failure", "unpublished-entry"),
                                     argv="sasquatch-v4be -be -f -d out in", p=3),
     "partial-body-failure", 5),
    ("s4-partial-plus-mixed", _env(gaps=("extractor-failure", "unpublished-entry"), sr=True,
                                   argv="sasquatch-v4be -be -f -d out in", p=2),
     "partial-body-failure", 5),
    ("s4-partial-without-argv", _env(gaps=("extractor-failure",), p=4), "partial-body-failure", 5),
    # step 5 / 6
    ("s5-avm-marker-be-dropped", _env(gaps=("extractor-failure",),
                                      argv="sasquatch-v4be -no-exit-code -f -d out in",
                                      p=0), "avm-marker-be-dropped", 6),
    ("s5-boundary-be-yes", _env(gaps=("extractor-failure",),
                                argv="sasquatch-v4be -be -no-exit-code -f -d out in", p=0),
     "body-extractor-failure", 8),
    ("s5-boundary-no-argv", _env(gaps=("extractor-failure",), p=0), "body-extractor-failure", 8),
    ("s5-boundary-le-handler-with-no-be", _env(handlers=("squashfs_v4_le",),
                                               gaps=("extractor-failure",),
                                               argv="sasquatch -no-exit-code -f -d out in",
                                               p=0), "body-extractor-failure", 8),
    ("s6-body-failure", _env(handlers=("squashfs_v4_be",), gaps=("extractor-failure",),
                             argv="sasquatch-v4be -be -f -d out in", p=0),
     "body-extractor-failure", 8),
    # step 7 (combined sets included)
    ("s7-depth-alone", _env(gaps=("depth-limited",), p=3), "depth-limited", 10),
    ("s7-depth-plus-in-tree", _env(gaps=("depth-limited", "unpublished-entry"), p=8),
     "depth-limited", 10),
    ("s7-depth-plus-mixed", _env(gaps=("depth-limited", "unpublished-entry"), sr=True, p=5),
     "depth-limited", 10),
    ("s7-partial-precedes-depth", _env(gaps=("extractor-failure", "depth-limited"),
                                    argv="sasquatch-v4be -be -f", p=2),
     "partial-body-failure", 5),
    # step 8
    ("s8-mixed", _env(gaps=("unpublished-entry",), sr=True, p=4), "mixed-symlinks", 11),
    ("s8-mixed-p0", _env(gaps=("unpublished-entry",), sr=True, p=0), "mixed-symlinks", 11),
    # step 9
    ("s9-escaping", _env(sr=True, p=3), "escaping-symlink-removed", 12),
    ("s9-boundary-escaping-p0", _env(sr=True, p=0), "escaping-symlink-removed", 12),
    ("s9-boundary-sr-with-unrelated-gap", _env(gaps=("encrypted-chunk",), sr=True, p=2),
     "unclassified", 15),
    # step 10
    ("s10-in-tree", _env(gaps=("unpublished-entry",), p=8), "in-tree-symlink-metadata", 13),
    ("s10-in-tree-p0", _env(gaps=("unpublished-entry",), p=0), "in-tree-symlink-metadata", 13),
    ("s10-boundary-singleton-not-met", _env(gaps=("unpublished-entry", "encrypted-chunk"),
                                            p=8), "unclassified", 15),
    # step 11
    ("s11-clean", _env(p=5), "clean", 14),
    ("s11-clean-empty", _env(p=0), "clean-empty", 14),
    ("s11-clean-empty-sr-no", _env(p=0, sr=False), "clean-empty", 14),
    # step 12
    ("s12-unknown-kinds-only", _env(gaps=("encrypted-chunk",), p=5), "unclassified", 15),
    ("s12-unknown-plus-unpublished", _env(gaps=("unpublished-entry", "encrypted-chunk"),
                                          p=5), "unclassified", 15),
    # structure boundaries
    ("b-wrapped-cli-envelope", _env(p=2, wrapped=True), "clean", 14),
    ("b-be-token-substring-trap", _env(gaps=("extractor-failure",),
                                       argv="sasquatch-v4be -no-exit-code -f -d out in", p=0),
     "avm-marker-be-dropped", 6),
    ("b-be-as-separate-argv-token", _env(gaps=("extractor-failure",),
                                         argv="sasquatch-v4be -be -d out in", p=0),
     "body-extractor-failure", 8),
    # multi-chunk boundary: the failing chunk is the LE one, so step 5's
    # "handler squashfs_v4_be" must be read from the failing gap, not from H.
    ("b-step5-uses-failing-chunk-handler",
     _env(handlers=("squashfs_v4_be", "squashfs_v4_le"), gaps=("extractor-failure",),
          gap_handlers={"extractor-failure": "squashfs_v4_le"},
          argv="sasquatch -no-exit-code -f -d out in", p=0),
     "body-extractor-failure", 8),
    ("b-step5-failing-chunk-is-be",
     _env(handlers=("squashfs_v4_be", "squashfs_v4_le"), gaps=("extractor-failure",),
          gap_handlers={"extractor-failure": "squashfs_v4_be"},
          argv="sasquatch-v4be -no-exit-code -f -d out in", p=0),
     "avm-marker-be-dropped", 6),
    # A17: a receipt with no `files` array at all is read as P = 0, the only value
    # the text allows; documented so a trimmed receipt cannot pass as "confirmed empty".
    ("b-files-absent-reads-as-p-zero", _env(p=0, files_absent=True), "clean-empty", 14),
    # ---- round-42 additions: the v1-v3 handler family (steps 2, 3, 6, 12) ------
    # step 2 boundary: a legacy handler IS a squashfs handler, so it must not be
    # labelled no-squashfs-chunk (round-41 routed defect R41-CL4).
    ("r42-legacy-clean-v3-le", _env(handlers=("squashfs_v3_le",), p=4), "clean", 14),
    ("r42-legacy-clean-v3-be", _env(handlers=("squashfs_v3_be",), p=4), "clean", 14),
    ("r42-legacy-clean-v1", _env(handlers=("squashfs_v1_le",), p=2), "clean", 14),
    ("r42-legacy-clean-v2-nonstandard", _env(handlers=("squashfs_v2_nonstandard_le",),
                                             p=2), "clean", 14),
    ("r42-legacy-clean-v3-ddwrt", _env(handlers=("squashfs_v3_ddwrt_le",), p=6), "clean", 14),
    ("r42-legacy-clean-v3-broadcom", _env(handlers=("squashfs_v3_broadcom_be",), p=6),
     "clean", 14),
    ("r42-legacy-clean-empty", _env(handlers=("squashfs_v3_le",), p=0), "clean-empty", 14),
    # step 3 on a legacy handler: only the named binary decides, not the handler name
    ("r42-legacy-dep-missing-le", _env(handlers=("squashfs_v3_le",),
                                       gaps=("missing-extractor-dependency",),
                                       deps=("sasquatch",), p=0), "dep-missing-le", 4),
    ("r42-legacy-dep-missing-be-name", _env(handlers=("squashfs_v3_be",),
                                            gaps=("missing-extractor-dependency",),
                                            deps=("sasquatch-v4be",), p=0),
     "dep-missing-be", 4),
    ("r42-legacy-dep-unnamed-falls-through", _env(handlers=("squashfs_v3_le",),
                                                  gaps=("missing-extractor-dependency",),
                                                  deps=(), p=0), "unclassified", 15),
    # step 4 with a legacy handler: files published, so partial regardless of family
    ("r42-legacy-partial", _env(handlers=("squashfs_v3_be",), gaps=("extractor-failure",),
                                argv="sasquatch -be -no-exit-code -f -d out in", p=3),
     "partial-body-failure", 5),
    # step 6: zero files, a v1-v3 handler.  BE = no on an LE-service chunk and
    # BE = yes on a -be argv both reach the same row; step 5 cannot fire because
    # the failing handler is not squashfs_v4_be.
    ("r42-legacy-body-failure-le", _env(handlers=("squashfs_v3_le",),
                                        gaps=("extractor-failure",),
                                        argv="sasquatch -no-exit-code -f -d out in", p=0),
     "legacy-body-failure", 7),
    ("r42-legacy-body-failure-be", _env(handlers=("squashfs_v3_be",),
                                        gaps=("extractor-failure",),
                                        argv="sasquatch -be -no-exit-code -f -d out in", p=0),
     "legacy-body-failure", 7),
    ("r42-legacy-body-failure-no-argv", _env(handlers=("squashfs_v1_le",),
                                             gaps=("extractor-failure",), p=0),
     "legacy-body-failure", 7),
    ("r42-legacy-body-failure-v3-ddwrt", _env(handlers=("squashfs_v3_ddwrt_be",),
                                              gaps=("extractor-failure",),
                                              argv="sasquatch -be -f", p=0),
     "legacy-body-failure", 7),
    # step 6 reads the FAILING handler (HF), not the run-wide set: a clean v4 chunk
    # beside a failing v3 chunk is legacy, and vice versa is step 5.
    ("r42-mixed-failing-v3-beside-clean-v4", _env(
        handlers=("squashfs_v3_le", "squashfs_v4_be"), gaps=("extractor-failure",),
        gap_handlers={"extractor-failure": "squashfs_v3_le"},
        argv="sasquatch -no-exit-code -f -d out in", p=0), "legacy-body-failure", 7),
    ("r42-mixed-failing-v4be-beside-clean-v3", _env(
        handlers=("squashfs_v3_le", "squashfs_v4_be"), gaps=("extractor-failure",),
        gap_handlers={"extractor-failure": "squashfs_v4_be"},
        argv="sasquatch-v4be -no-exit-code -f -d out in", p=0), "avm-marker-be-dropped", 6),
    # step 8 and 12 on a legacy chunk
    ("r42-legacy-depth-limited", _env(handlers=("squashfs_v3_le",), gaps=("depth-limited",),
                                      p=5), "depth-limited", 10),
    ("r42-mixed-clean-v3-and-v4", _env(handlers=("squashfs_v3_le", "squashfs_v4_le"), p=9),
     "clean", 14),
    ("r42-nonstandard-v2-magic-is-legacy", _env(handlers=("squashfs_v2_nonstandard_be",),
                                                gaps=("extractor-failure",), p=0),
     "legacy-body-failure", 7),
    # ---- A1 additions: container, residue, HF-based steps 6/7 ----------------
    # step 2: no squashfs handler at this depth, but the run was depth-capped
    ("a1-container-depth-limited", _env(handlers=("trx_v1",), gaps=("depth-limited",), p=0),
     "container-depth-limited", 2),
    ("a1-container-depth-limited-tar", _env(handlers=("tar",), gaps=("depth-limited",), p=2),
     "container-depth-limited", 2),
    # step 3 boundary: a container-shaped non-squashfs handler WITHOUT a depth cap
    ("a1-container-no-depth-is-no-chunk", _env(handlers=("trx_v1",), p=0),
     "no-squashfs-chunk", 3),
    # step 9: unclaimed bytes beside a clean chunk
    ("a1-unknown-residue", _env(handlers=("squashfs_v3",), gaps=("unknown-chunk-handler",),
                                p=3), "unknown-residue", 9),
    ("a1-unknown-residue-plus-depth", _env(handlers=("squashfs_v3_le",),
                                           gaps=("unknown-chunk-handler", "depth-limited"),
                                           p=3), "unknown-residue", 9),
    ("a1-unknown-residue-plus-in-tree", _env(handlers=("squashfs_v3",),
                                             gaps=("unknown-chunk-handler",
                                                   "unpublished-entry"), p=3),
     "unknown-residue", 9),
    # steps 5-8 still precede step 9: a failure with zero files is the body row
    ("a1-residue-beside-zero-file-failure", _env(handlers=("squashfs_v3",),
                                                 gaps=("extractor-failure",
                                                       "unknown-chunk-handler"), p=0),
     "legacy-body-failure", 7),
    # step 6/7 read HF, not the run-wide handler set (A1)
    ("a1-hf-v3-beside-clean-v4be-is-legacy", _env(
        handlers=("squashfs_v3", "squashfs_v4_be"), gaps=("extractor-failure",),
        gap_handlers={"extractor-failure": "squashfs_v3"},
        argv="sasquatch -le -no-exit-code -f -d out in", p=0),
     "legacy-body-failure", 7),
    ("a1-hf-v4be-is-avm", _env(
        handlers=("squashfs_v3", "squashfs_v4_be"), gaps=("extractor-failure",),
        gap_handlers={"extractor-failure": "squashfs_v4_be"},
        argv="sasquatch-v4be -no-exit-code -f -d out in", p=0),
     "avm-marker-be-dropped", 6),
    # HF falls back to F when the failure gap carries no handler
    ("a1-hf-defaults-to-f", _env(handlers=("squashfs_v2",), gaps=("extractor-failure",), p=0),
     "legacy-body-failure", 7),
    ("a1-hf-defaults-to-f-v4be-no-be", _env(handlers=("squashfs_v4_be",),
                                            gaps=("extractor-failure",),
                                            argv="sasquatch-v4be -no-exit-code -f", p=0),
     "avm-marker-be-dropped", 6),
    # a dependency gap plus a failure resolves at step 4, not steps 5-8
    ("a1-dep-plus-failure-with-files", _env(
        handlers=("squashfs_v3", "squashfs_v4_be"),
        gaps=("extractor-failure", "missing-extractor-dependency"),
        deps=("sasquatch-v4be",), gap_handlers={"extractor-failure": "squashfs_v3"},
        argv="sasquatch -le -no-exit-code -f", p=2), "dep-missing-be", 4),
]


def selftest():
    failures = []
    steps_seen = set()
    for name, env, want_label, want_step in SELFTEST_CASES:
        got = classify(features(env))
        if got[0] != want_label or got[2] != want_step:
            failures.append("%s: want (%s, step %d) got (%s, step %d)"
                            % (name, want_label, want_step, got[0], got[2]))
        steps_seen.add(want_step)
    # every precedence step must be exercised, and every label must be reachable
    labels_seen = {want for _, _, want, _ in SELFTEST_CASES}
    for step in range(1, 16):
        if step not in steps_seen:
            failures.append("step %d has no selftest case" % step)
    for label in ACTION_BY_LABEL:
        if label not in labels_seen:
            failures.append("label %s has no selftest case" % label)
    # action map must be total and fixed
    for label, action in ACTION_BY_LABEL.items():
        if not action:
            failures.append("empty action for %s" % label)
    result = {
        "cases": len(SELFTEST_CASES),
        "steps_covered": sorted(steps_seen),
        "labels_covered": sorted(labels_seen),
        "failures": failures,
        "ok": not failures,
    }
    print(json.dumps(result, indent=1, sort_keys=True))
    return 0 if not failures else 1


# --------------------------------------------------------------------------
# envelope collection
# --------------------------------------------------------------------------
def collect(dirpath, prefer_full=False):
    """Yield (id, path) for every envelope under `dirpath`."""
    names = sorted(os.listdir(dirpath))
    subdirs = [n for n in names if os.path.isdir(os.path.join(dirpath, n))]
    if subdirs:
        for name in subdirs:
            cands = ["rea-full.json", "envelope.json"] if prefer_full else ["envelope.json", "rea-full.json"]
            for cand in cands:
                path = os.path.join(dirpath, name, cand)
                if os.path.isfile(path):
                    yield name, path
                    break
            else:
                jsons = sorted(n for n in os.listdir(os.path.join(dirpath, name))
                               if n.endswith(".json"))
                if jsons:
                    yield name, os.path.join(dirpath, name, jsons[0])
    for name in names:
        path = os.path.join(dirpath, name)
        if os.path.isfile(path) and name.endswith(".json"):
            yield os.path.splitext(name)[0], path


def _is_envelope(doc):
    """True if `doc` carries an analysis envelope rather than side metadata.

    A lane directory may also hold a manifest or a receipt; those have no
    `operation`/`normalized_result`/`provider` and must not be labelled.
    """
    data, _ = unwrap(doc)
    return isinstance(data, dict) and any(
        key in data for key in ("operation", "normalized_result", "provider")
    )


def evaluate_dir(dirpath, prefer_full=False):
    labels = {}
    errors = {}
    skipped = []
    for env_id, path in collect(dirpath, prefer_full):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                doc = json.load(fh)
        except (OSError, ValueError) as exc:
            errors[env_id] = "%s: %s" % (path, exc)
            continue
        if not _is_envelope(doc):
            skipped.append({"id": env_id, "path": os.path.basename(path),
                            "reason": "no operation/normalized_result/provider"})
            continue
        feats = features(doc)
        label, action, step = classify(feats)
        if label not in ACTION_BY_LABEL:
            errors[env_id] = "label %r is not in the fixed action map" % (label,)
            continue
        labels[env_id] = {
            "label": label,
            "action": action,
            "step": step,
            "evidence_id": feats.get("_id"),
            "features": {k: feats[k] for k in ("OP", "PR", "H", "HF", "G", "D", "BE", "SR", "P")},
            "extraction": feats["_prov"],
            "source": os.path.basename(path),
        }
    counts = {}
    for rec in labels.values():
        counts[rec["label"]] = counts.get(rec["label"], 0) + 1
    out = {
        "evaluator": "indep-eval-v3.py",
        "precedence_source": "plans/round-41-claims.md **Label precedence** (draft)",
        "directory": dirpath,
        "envelope_count": len(labels),
        "label_counts": dict(sorted(counts.items())),
        "labels": dict(sorted(labels.items())),
    }
    if errors:
        out["errors"] = errors
    if skipped:
        out["skipped"] = skipped
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="R41-C2 independent evaluator")
    ap.add_argument("--envelopes", metavar="DIR", help="directory of envelopes")
    ap.add_argument("--out", metavar="FILE", help="write JSON here instead of stdout")
    ap.add_argument("--full", action="store_true",
                    help="prefer rea-full.json (the CLI envelope) over envelope.json")
    ap.add_argument("--selftest", action="store_true", help="run synthetic tuples")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.envelopes:
        ap.error("one of --envelopes or --selftest is required")
    if not os.path.isdir(args.envelopes):
        ap.error("--envelopes %r is not a directory" % args.envelopes)
    result = evaluate_dir(args.envelopes, prefer_full=args.full)
    text = json.dumps(result, indent=1, sort_keys=True)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print("wrote %s (%d envelopes)" % (args.out, result["envelope_count"]))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
