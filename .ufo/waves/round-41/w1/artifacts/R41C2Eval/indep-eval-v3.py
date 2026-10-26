#!/usr/bin/env python3
"""indep-eval-v3.py -- R41-C2 INDEPENDENT evaluator (round 41 wave 1).

Written by seat R41C2Eval from exactly three inputs:
  1. the `**Label precedence**` numbered list in
     kaidoku-shokunin/plans/round-41-claims.md (the twelve steps, verbatim in
     PRECEDENCE below);
  2. REA 6.5.0 envelope structure, observed in committed envelopes under
     corpus/evidence/round-40/c2/heldout/*/envelope.json and
     corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json, and in
     rea-agents/dist/firmware/{FirmwarePublication,FirmwareReports,FirmwareFiles}.js;
  3. nothing else.  It never reads SKILL.md (or its triage-table blocks), any
     tools/round-3*/ interpreter or generator, the round-40 evaluator, or any
     other seat's artifacts.

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
import shlex
import sys

# --------------------------------------------------------------------------
# The twelve precedence steps, transcribed verbatim from the draft claims file.
# Kept as text so the report can quote what each code branch implements.
# --------------------------------------------------------------------------
PRECEDENCE = [
    "1. OP != extract_firmware or PR != unblob -> (unclassified, none).",
    "2. no squashfs_v4_* handler in H -> no-squashfs-chunk.",
    "3. missing-extractor-dependency in G -> dep-missing-be if D names sasquatch-v4be, "
    "dep-missing-le if D names sasquatch.",
    "4. extractor-failure in G and P > 0 -> partial-body-failure, whatever other gaps "
    "or removed links accompany it (combined sets).",
    "5. extractor-failure in G, P = 0, BE = no, handler squashfs_v4_be -> avm-marker-be-dropped.",
    "6. extractor-failure in G, P = 0 -> body-extractor-failure.",
    "7. depth-limited in G -> depth-limited-nested (new), whatever symlink gaps accompany it.",
    "8. SR = yes and unpublished-entry in G -> mixed-symlinks.",
    "9. SR = yes and G = empty -> escaping-symlink-removed.",
    "10. G = {unpublished-entry} -> in-tree-symlink-metadata.",
    "11. G = empty, P > 0 -> clean; G = empty, P = 0 -> clean-empty.",
    "12. anything else -> (unclassified, none).",
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
    "depth-limited-nested": "raise-depth",
    "mixed-symlinks": "audit-symlinks",
    "escaping-symlink-removed": "expect-link-absent",
    "in-tree-symlink-metadata": "count-gap",
    "clean": "none",
    "clean-empty": "confirm-empty",
    "unclassified": "none",
}

SQUASHFS_HANDLER_PREFIX = "squashfs_v4_"
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
    """Return (label, action, step) for a feature tuple, applying steps 1..12."""
    op = feats.get("OP")
    pr = feats.get("PR")
    h = set(feats.get("H") or [])
    g = set(feats.get("G") or [])
    d = set(feats.get("D") or [])
    be = feats.get("BE")
    sr = (feats.get("SR") == "yes") or feats.get("SR") is True
    p = feats.get("P") or 0

    squashfs = {name for name in h if name.startswith(SQUASHFS_HANDLER_PREFIX)}

    # 1
    if op != "extract_firmware" or pr != "unblob":
        return _done("unclassified", 1)
    # 2
    if not squashfs:
        return _done("no-squashfs-chunk", 2)
    # 3  D "names" a dependency: exact membership, never substring --
    #    "sasquatch" is a substring of "sasquatch-v4be", so substring matching
    #    would relabel every BE dependency as LE.  be is tested first because
    #    the precedence names it first.
    if "missing-extractor-dependency" in g:
        if BE_DEPENDENCY in d:
            return _done("dep-missing-be", 3)
        if LE_DEPENDENCY in d:
            return _done("dep-missing-le", 3)
        # neither name present: step 3 states no outcome; fall through.
    # 4
    if "extractor-failure" in g and p > 0:
        return _done("partial-body-failure", 4)
    # 5  the handler named here is the failing extraction's handler: use the
    #    extractor-failure gap's own handler when the envelope records one, and
    #    the run-wide handler set H otherwise.
    step5_handlers = set(feats.get("HF") or []) or h
    if "extractor-failure" in g and p == 0 and be == "no" and AVM_HANDLER in step5_handlers:
        return _done("avm-marker-be-dropped", 5)
    # 6
    if "extractor-failure" in g and p == 0:
        return _done("body-extractor-failure", 6)
    # 7
    if "depth-limited" in g:
        return _done("depth-limited-nested", 7)
    # 8
    if sr and "unpublished-entry" in g:
        return _done("mixed-symlinks", 8)
    # 9
    if sr and not g:
        return _done("escaping-symlink-removed", 9)
    # 10
    if g == {"unpublished-entry"}:
        return _done("in-tree-symlink-metadata", 10)
    # 11
    if not g:
        return _done("clean" if p > 0 else "clean-empty", 11)
    # 12
    return _done("unclassified", 12)


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
    ("s2-no-handler", _env(handlers=(), p=0), "no-squashfs-chunk", 2),
    ("s2-handler-elsewhere", _env(handlers=("gzip",), p=0), "no-squashfs-chunk", 2),
    ("s2-le-handler-is-a-squashfs-handler", _env(handlers=("squashfs_v4_le",), p=2), "clean", 11),
    # step 3
    ("s3-dep-be", _env(handlers=("squashfs_v4_be",), gaps=("missing-extractor-dependency",),
                       deps=("sasquatch-v4be",), p=0), "dep-missing-be", 3),
    ("s3-dep-le", _env(handlers=("squashfs_v4_le",), gaps=("missing-extractor-dependency",),
                       deps=("sasquatch",), p=0), "dep-missing-le", 3),
    ("s3-dep-both-be-first", _env(gaps=("missing-extractor-dependency",),
                                  deps=("sasquatch", "sasquatch-v4be"), p=0), "dep-missing-be", 3),
    ("s3-dep-other-name-falls-through", _env(gaps=("missing-extractor-dependency",),
                                             deps=("unsquashfs",), p=0), "unclassified", 12),
    ("s3-LE-substring-must-not-match-be", _env(gaps=("missing-extractor-dependency",),
                                               deps=("sasquatch-v4be-x",), p=0), "unclassified", 12),
    ("s3-be-substring-must-not-match-le", _env(gaps=("missing-extractor-dependency",),
                                               deps=("xsasquatch",), p=0), "unclassified", 12),
    ("s3-dep-in-gap-only-handler", _env(handlers=(), gaps=("missing-extractor-dependency",),
                                        deps=("sasquatch-v4be",), p=0),
     "no-squashfs-chunk", 2),
    # step 4 (combined sets included)
    ("s4-partial", _env(gaps=("extractor-failure",), argv="sasquatch-v4be -be -f -d out in",
                        p=5), "partial-body-failure", 4),
    ("s4-partial-p1", _env(gaps=("extractor-failure",), argv="sasquatch-v4be -be -f -d out in",
                           p=1), "partial-body-failure", 4),
    ("s4-partial-plus-in-tree", _env(gaps=("extractor-failure", "unpublished-entry"),
                                     argv="sasquatch-v4be -be -f -d out in", p=3),
     "partial-body-failure", 4),
    ("s4-partial-plus-mixed", _env(gaps=("extractor-failure", "unpublished-entry"), sr=True,
                                   argv="sasquatch-v4be -be -f -d out in", p=2),
     "partial-body-failure", 4),
    ("s4-partial-without-argv", _env(gaps=("extractor-failure",), p=4), "partial-body-failure", 4),
    # step 5 / 6
    ("s5-avm-marker-be-dropped", _env(gaps=("extractor-failure",),
                                      argv="sasquatch-v4be -no-exit-code -f -d out in",
                                      p=0), "avm-marker-be-dropped", 5),
    ("s5-boundary-be-yes", _env(gaps=("extractor-failure",),
                                argv="sasquatch-v4be -be -no-exit-code -f -d out in", p=0),
     "body-extractor-failure", 6),
    ("s5-boundary-no-argv", _env(gaps=("extractor-failure",), p=0), "body-extractor-failure", 6),
    ("s5-boundary-le-handler-with-no-be", _env(handlers=("squashfs_v4_le",),
                                               gaps=("extractor-failure",),
                                               argv="sasquatch -no-exit-code -f -d out in",
                                               p=0), "body-extractor-failure", 6),
    ("s6-body-failure", _env(handlers=("squashfs_v4_be",), gaps=("extractor-failure",),
                             argv="sasquatch-v4be -be -f -d out in", p=0),
     "body-extractor-failure", 6),
    # step 7 (combined sets included)
    ("s7-depth-alone", _env(gaps=("depth-limited",), p=3), "depth-limited-nested", 7),
    ("s7-depth-plus-in-tree", _env(gaps=("depth-limited", "unpublished-entry"), p=8),
     "depth-limited-nested", 7),
    ("s7-depth-plus-mixed", _env(gaps=("depth-limited", "unpublished-entry"), sr=True, p=5),
     "depth-limited-nested", 7),
    ("s7-partial-precedes-depth", _env(gaps=("extractor-failure", "depth-limited"),
                                    argv="sasquatch-v4be -be -f", p=2),
     "partial-body-failure", 4),
    # step 8
    ("s8-mixed", _env(gaps=("unpublished-entry",), sr=True, p=4), "mixed-symlinks", 8),
    ("s8-mixed-p0", _env(gaps=("unpublished-entry",), sr=True, p=0), "mixed-symlinks", 8),
    # step 9
    ("s9-escaping", _env(sr=True, p=3), "escaping-symlink-removed", 9),
    ("s9-boundary-escaping-p0", _env(sr=True, p=0), "escaping-symlink-removed", 9),
    ("s9-boundary-sr-with-unrelated-gap", _env(gaps=("encrypted-chunk",), sr=True, p=2),
     "unclassified", 12),
    # step 10
    ("s10-in-tree", _env(gaps=("unpublished-entry",), p=8), "in-tree-symlink-metadata", 10),
    ("s10-in-tree-p0", _env(gaps=("unpublished-entry",), p=0), "in-tree-symlink-metadata", 10),
    ("s10-boundary-singleton-not-met", _env(gaps=("unpublished-entry", "unknown-chunk-handler"),
                                            p=8), "unclassified", 12),
    # step 11
    ("s11-clean", _env(p=5), "clean", 11),
    ("s11-clean-empty", _env(p=0), "clean-empty", 11),
    ("s11-clean-empty-sr-no", _env(p=0, sr=False), "clean-empty", 11),
    # step 12
    ("s12-unknown-kinds-only", _env(gaps=("encrypted-chunk",), p=5), "unclassified", 12),
    ("s12-unknown-plus-unpublished", _env(gaps=("unpublished-entry", "encrypted-chunk"),
                                          p=5), "unclassified", 12),
    # structure boundaries
    ("b-wrapped-cli-envelope", _env(p=2, wrapped=True), "clean", 11),
    ("b-be-token-substring-trap", _env(gaps=("extractor-failure",),
                                       argv="sasquatch-v4be -no-exit-code -f -d out in", p=0),
     "avm-marker-be-dropped", 5),
    ("b-be-as-separate-argv-token", _env(gaps=("extractor-failure",),
                                         argv="sasquatch-v4be -be -d out in", p=0),
     "body-extractor-failure", 6),
    # multi-chunk boundary: the failing chunk is the LE one, so step 5's
    # "handler squashfs_v4_be" must be read from the failing gap, not from H.
    ("b-step5-uses-failing-chunk-handler",
     _env(handlers=("squashfs_v4_be", "squashfs_v4_le"), gaps=("extractor-failure",),
          gap_handlers={"extractor-failure": "squashfs_v4_le"},
          argv="sasquatch -no-exit-code -f -d out in", p=0),
     "body-extractor-failure", 6),
    ("b-step5-failing-chunk-is-be",
     _env(handlers=("squashfs_v4_be", "squashfs_v4_le"), gaps=("extractor-failure",),
          gap_handlers={"extractor-failure": "squashfs_v4_be"},
          argv="sasquatch-v4be -no-exit-code -f -d out in", p=0),
     "avm-marker-be-dropped", 5),
    # A17: a receipt with no `files` array at all is read as P = 0, the only value
    # the text allows; documented so a trimmed receipt cannot pass as "confirmed empty".
    ("b-files-absent-reads-as-p-zero", _env(p=0, files_absent=True), "clean-empty", 11),
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
    for step in range(1, 13):
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
