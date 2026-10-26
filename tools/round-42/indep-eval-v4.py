#!/usr/bin/env python3
"""R42-C2 independent evaluator (v4).

Written ONLY from the draft label precedence of `plans/round-42-claims.md`
(## R42-C2, numbered steps 1-13) plus the REA 6.5.0 envelope structure.  It never
reads the SKILL table, the v4 interpreter, the generator or its class map; the
expected (label, action) pairs of a held-out set come from this file alone.

Feature extraction (one REA envelope).  Every feature names the field it is read
from; nothing is inferred from the label classes:

  OP  `operation`                                    (top level of the envelope)
  PR  `provider.id`                                  (top level; exact, case-sensitive)
  H   ordered unique handler names, `normalized_result.chunks[].handler` followed by
      `normalized_result.extraction_gaps[].handler`, null/empty dropped
  F   {h in H : h startswith "squashfs_"}            (the SquashFS handler set)
  G   set of `normalized_result.extraction_gaps[].kind`
  D   union of `normalized_result.extraction_gaps[].dependencies` (exact names)
  BE  "yes" if any recorded child argv in `normalized_result.diagnostics[].report.command`
      carries the shell token `-be`; "no" if argvs are recorded and none does;
      "n/a" if no argv is recorded at all (BE="n/a" never satisfies step 5)
  SR  "yes" iff a producer report with `__typename__ == "MaliciousSymlinkRemoved"`
      appears in `normalized_result.diagnostics[].report` (a removal is not a gap kind)
  P   len(`normalized_result.files`); an absent list reads 0

Derived helper (not a feature): the failing handler set HF = ordered unique
`extraction_gaps[].handler` of the gaps whose kind is `extractor-failure`; when no
such gap names a handler, HF falls back to F (amendment A1).  L = the v1-v3 names:
a handler matching `squashfs_v1*`, `squashfs_v2*` or `squashfs_v3*` (unblob 26.6.4:
squashfs_v1, squashfs_v2, squashfs_v2_nonstandard, squashfs_v3, squashfs_v3_ddwrt,
squashfs_v3_broadcom, squashfs_v3_nonstandard).

AMENDMENT A1 (L1 KaidokuR42, 2026-10-26, from the amended precedence text only —
`plans/round-42-claims.md` ## R42-C2, steps 1-15; the seat's 13-step body above was
renumbered and two steps added; the table, interpreter and generator were not read):

  1. OP != extract_firmware or PR != unblob                  -> unclassified / none
  2. F = {} and depth-limited in G                           -> container-depth-limited / raise-depth
  3. F = {}                                                  -> no-squashfs-chunk / inspect-input
  4. missing-extractor-dependency in G:
       D holds sasquatch-v4be                                -> dep-missing-be / install-extractor-be
       else D holds sasquatch                                -> dep-missing-le / install-extractor-le
       else continue
  5. extractor-failure in G and P > 0                        -> partial-body-failure / salvage-partial
  6. extractor-failure in G, P = 0, BE = no, squashfs_v4_be in HF
                                                             -> avm-marker-be-dropped / wrap-extractor-be
  7. extractor-failure in G, P = 0, HF meets L               -> legacy-body-failure / cross-read-legacy
  8. extractor-failure in G, P = 0                           -> body-extractor-failure / preserve-failure
  9. unknown-chunk-handler in G                              -> unknown-residue / isolate-residue
 10. depth-limited in G                                      -> depth-limited / raise-depth
 11. SR = yes and unpublished-entry in G                     -> mixed-symlinks / audit-symlinks
 12. SR = yes and G = {}                                     -> escaping-symlink-removed / expect-link-absent
 13. G = {unpublished-entry}                                 -> in-tree-symlink-metadata / count-gap
 14. G = {}: P > 0 -> clean / none ; P = 0 -> clean-empty / confirm-empty
 15. anything else                                           -> unclassified / none

CLI (same shape as round 41's evaluator: `--envelopes DIR --out FILE`, `--full`,
`--selftest`; plus an optional single-envelope positional):

  indep-eval-v4.py ENVELOPE.json            one envelope -> one record on stdout
  indep-eval-v4.py --envelopes DIR [--out F] [--full]
                                            one record per subdirectory holding
                                            envelope.json (or rea-full.json with --full)
  indep-eval-v4.py --selftest               hand-written envelopes for every step

An input may be a CLI envelope ({"ok":..,"data":{..},"meta":..}) or a bare data
object (the committed envelope form).  Exit codes: 0 ok, 1 selftest failure,
2 usage/IO error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
from typing import Any, Iterable

EVALUATOR = "indep-eval-v4.py"

# Label/action vocabulary of the draft precedence, in the order the draft prints
# the pairs.  Emitted in the batch output so a counter can check the alphabet.
VOCABULARY = [
    ("unclassified", "none"),
    ("no-squashfs-chunk", "inspect-input"),
    ("dep-missing-be", "install-extractor-be"),
    ("dep-missing-le", "install-extractor-le"),
    ("partial-body-failure", "salvage-partial"),
    ("avm-marker-be-dropped", "wrap-extractor-be"),
    ("legacy-body-failure", "cross-read-legacy"),
    ("body-extractor-failure", "preserve-failure"),
    ("container-depth-limited", "raise-depth"),
    ("unknown-residue", "isolate-residue"),
    ("depth-limited", "raise-depth"),
    ("mixed-symlinks", "audit-symlinks"),
    ("escaping-symlink-removed", "expect-link-absent"),
    ("in-tree-symlink-metadata", "count-gap"),
    ("clean", "none"),
    ("clean-empty", "confirm-empty"),
]

LEGACY_HANDLER = re.compile(r"squashfs_v[123]($|_)")
SQUASHFS_PREFIX = "squashfs_"
V4_BE = "squashfs_v4_be"
KIND_DEP = "missing-extractor-dependency"
KIND_EXTRACT = "extractor-failure"
KIND_DEPTH = "depth-limited"
KIND_UNPUBLISHED = "unpublished-entry"
KIND_UNKNOWN = "unknown-chunk-handler"
DEP_BE = "sasquatch-v4be"
DEP_LE = "sasquatch"


# --------------------------------------------------------------------------- io


def unwrap(doc: Any) -> dict:
    """Accept a CLI envelope ({"ok","data","meta"}) or a bare data object.

    REA 6.5.0 `--format json --full-output` prints {"ok": bool, "data": <envelope>,
    "meta": {...}}; the committed evidence form is the <envelope> object itself
    (evidence_id, operation, provider, normalized_result, ...).
    """
    if not isinstance(doc, dict):
        raise ValueError("envelope is not a JSON object")
    data = doc.get("data")
    if isinstance(data, dict) and "normalized_result" in data:
        return data
    if "data" in doc and "normalized_result" not in doc and isinstance(data, dict):
        return data
    return doc


def _norm(env: dict) -> dict:
    nr = env.get("normalized_result")
    return nr if isinstance(nr, dict) else {}


def _dicts(value: Any) -> Iterable[dict]:
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                yield item


def _ordered_unique(names: Iterable[Any]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for name in names:
        if isinstance(name, str) and name and name not in seen:
            seen.add(name)
            out.append(name)
    return out


# --------------------------------------------------------------------- features


def extract_features(env: dict) -> dict:
    """Return OP, PR, H, F, G, D, BE, SR, P and the derived FH."""
    nr = _norm(env)

    op = env.get("operation")
    provider = env.get("provider")
    pr = provider.get("id") if isinstance(provider, dict) else None

    chunks = list(_dicts(nr.get("chunks")))
    gaps = list(_dicts(nr.get("extraction_gaps")))
    diagnostics = list(_dicts(nr.get("diagnostics")))

    handlers = _ordered_unique(
        [c.get("handler") for c in chunks] + [g.get("handler") for g in gaps]
    )
    f = sorted(h for h in handlers if h.startswith(SQUASHFS_PREFIX))

    g_kinds = sorted({g.get("kind") for g in gaps if isinstance(g.get("kind"), str)})

    deps: set[str] = set()
    for gap in gaps:
        for dep in gap.get("dependencies") or []:
            if isinstance(dep, str):
                deps.add(dep)

    argvs: list[str] = []
    sr = False
    for diag in diagnostics:
        report = diag.get("report")
        if not isinstance(report, dict):
            continue
        cmd = report.get("command")
        if isinstance(cmd, str) and cmd.strip():
            argvs.append(cmd)
        elif isinstance(cmd, list) and cmd:
            argvs.append(" ".join(str(part) for part in cmd))
        typename = report.get("__typename__") or report.get("type")
        if typename == "MaliciousSymlinkRemoved":
            sr = True

    be = "n/a"
    for argv in argvs:
        try:
            tokens = shlex.split(argv)
        except ValueError:
            tokens = argv.split()
        if "-be" in tokens:
            be = "yes"
            break
    if argvs and be == "n/a":
        be = "no"

    files = nr.get("files")
    p = len(files) if isinstance(files, list) else 0

    failing = _ordered_unique(
        gap.get("handler") for gap in gaps if gap.get("kind") == KIND_EXTRACT
    )
    fh = failing or f  # A1: HF falls back to F

    return {
        "OP": op,
        "PR": pr,
        "H": handlers,
        "F": f,
        "G": g_kinds,
        "D": sorted(deps),
        "BE": be,
        "SR": "yes" if sr else "no",
        "P": p,
        "FH": fh,
    }


# ------------------------------------------------------------------------ steps


def classify(features: dict) -> tuple[str, str, int]:
    """Apply amended (A1) steps 1-15, first match wins.  Returns (label, action, step)."""
    op = features["OP"]
    pr = features["PR"]
    f = features["F"]
    g = set(features["G"])
    d = set(features["D"])
    be = features["BE"]
    sr = features["SR"] == "yes"
    p = features["P"]
    fh = features["FH"]

    if op != "extract_firmware" or pr != "unblob":
        return "unclassified", "none", 1
    if not f and KIND_DEPTH in g:
        return "container-depth-limited", "raise-depth", 2
    if not f:
        return "no-squashfs-chunk", "inspect-input", 3
    if KIND_DEP in g:
        if DEP_BE in d:
            return "dep-missing-be", "install-extractor-be", 4
        if DEP_LE in d:
            return "dep-missing-le", "install-extractor-le", 4
    if KIND_EXTRACT in g and p > 0:
        return "partial-body-failure", "salvage-partial", 5
    if KIND_EXTRACT in g and p == 0 and be == "no" and V4_BE in fh:
        return "avm-marker-be-dropped", "wrap-extractor-be", 6
    if KIND_EXTRACT in g and p == 0 and any(LEGACY_HANDLER.match(h) for h in fh):
        return "legacy-body-failure", "cross-read-legacy", 7
    if KIND_EXTRACT in g and p == 0:
        return "body-extractor-failure", "preserve-failure", 8
    if KIND_UNKNOWN in g:
        return "unknown-residue", "isolate-residue", 9
    if KIND_DEPTH in g:
        return "depth-limited", "raise-depth", 10
    if sr and KIND_UNPUBLISHED in g:
        return "mixed-symlinks", "audit-symlinks", 11
    if sr and not g:
        return "escaping-symlink-removed", "expect-link-absent", 12
    if g == {KIND_UNPUBLISHED}:
        return "in-tree-symlink-metadata", "count-gap", 13
    if not g:
        if p > 0:
            return "clean", "none", 14
        return "clean-empty", "confirm-empty", 14
    return "unclassified", "none", 15


def evaluate(env: dict) -> dict:
    features = extract_features(env)
    label, action, step = classify(features)
    return {"label": label, "action": action, "step": step, "features": features}


# ------------------------------------------------------------------------ batch


def envelope_path(directory: str, full: bool) -> str | None:
    if full:
        candidate = os.path.join(directory, "rea-full.json")
        if os.path.isfile(candidate):
            return candidate
    candidate = os.path.join(directory, "envelope.json")
    if os.path.isfile(candidate):
        return candidate
    if full:
        candidate = os.path.join(directory, "after.json")
        if os.path.isfile(candidate):
            return candidate
    return None


def _record(id_: str, path: str, env: dict) -> dict:
    result = evaluate(env)
    return {
        "id": id_,
        "envelope": path,
        "label": result["label"],
        "action": result["action"],
        "step": result["step"],
        "features": result["features"],
    }


def _looks_like_envelope(doc: Any) -> bool:
    """A manifest/counter JSON in the same directory is skipped, not scored."""
    if not isinstance(doc, dict):
        return False
    if doc.get("predicate_type") == "rea.analysis":
        return True
    if "normalized_result" in doc or "operation" in doc:
        return True
    data = doc.get("data")
    return isinstance(data, dict) and (
        "normalized_result" in data or "operation" in data
    )


def run_batch(directory: str, full: bool) -> dict:
    if not os.path.isdir(directory):
        raise OSError(f"not a directory: {directory}")
    records: list[dict] = []
    skipped: list[str] = []
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if os.path.isfile(path) and name.endswith(".json"):
            with open(path, encoding="utf-8") as handle:
                doc = json.load(handle)
            if not _looks_like_envelope(doc):
                skipped.append(name)
                continue
            records.append(_record(name, path, unwrap(doc)))
            continue
        if not os.path.isdir(path):
            continue
        target = envelope_path(path, full)
        if target is None:
            skipped.append(name)
            continue
        with open(target, encoding="utf-8") as handle:
            doc = json.load(handle)
        if not _looks_like_envelope(doc):
            skipped.append(name)
            continue
        records.append(_record(name, target, unwrap(doc)))

    counts: dict[str, int] = {}
    for record in records:
        counts[record["label"]] = counts.get(record["label"], 0) + 1
    return {
        "evaluator": EVALUATOR,
        "mode": "full" if full else "envelope",
        "directory": os.path.abspath(directory),
        "n": len(records),
        "skipped": skipped,
        "labels": dict(sorted(counts.items())),
        "vocabulary": [{"label": l, "action": a} for l, a in VOCABULARY],
        "results": records,
    }


# --------------------------------------------------------------------- selftest


def _env(
    op: str = "extract_firmware",
    pr: str = "unblob",
    chunk_handlers: Iterable[Any] = (),
    gaps: Iterable[dict] = (),
    commands: Iterable[str] = (),
    files: int = 0,
    symlink_removed: bool = False,
    wrap: bool = False,
) -> dict:
    """Hand-written envelope: only the fields the precedence reads."""
    chunks = []
    for index, handler in enumerate(chunk_handlers):
        chunks.append(
            {
                "input_path": "$input",
                "provider_id": f"1:{index}",
                "range": {"offset": 0, "length": 1},
                "handler": handler,
                "encrypted": False,
                "root_file_range": {"offset": 0, "length": 1},
                "extraction_failed": False,
            }
        )
    gaps = list(gaps)
    diagnostics = []
    for command in commands:
        diagnostics.append(
            {
                "input_path": "$input",
                "stage": "squashfs",
                "report": {
                    "severity": "WARNING",
                    "command": command,
                    "stdout": "",
                    "stderr": "",
                    "exit_code": 1,
                    "__typename__": "ExtractCommandFailedReport",
                },
            }
        )
    if symlink_removed:
        diagnostics.append(
            {
                "input_path": "$input",
                "report": {
                    "severity": "WARNING",
                    "link": "$output/firmware.bin_extract/a",
                    "target": "$output/elsewhere",
                    "__typename__": "MaliciousSymlinkRemoved",
                },
            }
        )
    env = {
        "evidence_id": "ev_selftest",
        "subject": {"name": "carrier.sqsh", "digest": {"sha256": "0" * 64}, "format": "file"},
        "provider": {"id": pr, "name": pr, "version": "26.6.4"},
        "predicate_type": "rea.analysis",
        "operation": op,
        "parameters": {"max_depth": 1},
        "raw_result": {"report": []},
        "normalized_result": {
            "engine": {"name": "unblob"},
            "coverage": "partial",
            "files": [
                {"relative_path": f"f{i}", "size": 1, "sha256": "0" * 64}
                for i in range(files)
            ],
            "unpublished_entries": [],
            "chunks": chunks,
            "derivations": [],
            "depth_limited_paths": [],
            "diagnostics": diagnostics,
            "extraction_gaps": gaps,
            "extraction_continuations": [],
        },
        "confidence": "observed",
        "authority": "shipped-artifact",
        "environment": None,
        "limitations": [],
    }
    if wrap:
        return {"ok": True, "data": env, "meta": {"command": "extract-firmware"}}
    return env


def _gap(kind: str, handler: Any = None, deps: Iterable[str] = ()) -> dict:
    return {
        "kind": kind,
        "input_path": "$input",
        "relative_path": None,
        "handler": handler,
        "provider_id": "1:1",
        "range": {"offset": 0, "length": 1},
        "root_file_range": {"offset": 0, "length": 1},
        "dependencies": list(deps),
        "continuation_id": "0" * 64,
    }


def _cases() -> list[tuple[str, dict, str, str, int]]:
    le_argv = "sasquatch -le -no-exit-code -f -d /o/firmware.bin_extract /o/firmware.bin"
    be_argv = "sasquatch -be -no-exit-code -f -d /o/firmware.bin_extract /o/firmware.bin"
    v4be_avm = "sasquatch-v4be -no-exit-code -f -d /o/firmware.bin_extract /o/firmware.bin"
    v4be_be = "sasquatch-v4be -be -no-exit-code -f -d /o/firmware.bin_extract /o/firmware.bin"
    cases = [
        # --- step 1
        ("s1 operation not extract_firmware",
         _env(op="extract_filesystem", chunk_handlers=["squashfs_v4_le"]),
         "unclassified", "none", 1),
        ("s1 provider not unblob",
         _env(pr="binwalk", chunk_handlers=["squashfs_v4_le"]),
         "unclassified", "none", 1),
        ("s1 provider case matters",
         _env(pr="Unblob", chunk_handlers=["squashfs_v4_le"]),
         "unclassified", "none", 1),
        # --- step 2
        ("s2 no squashfs handler at all",
         _env(chunk_handlers=["gzip"]),
         "no-squashfs-chunk", "inspect-input", 2),
        ("s2 null handler only",
         _env(chunk_handlers=[None]),
         "no-squashfs-chunk", "inspect-input", 2),
        ("s2 wins over a dependency gap",
         _env(chunk_handlers=["cpio"], gaps=[_gap("missing-extractor-dependency", "cpio", [DEP_LE])]),
         "no-squashfs-chunk", "inspect-input", 2),
        # --- step 3
        ("s3 v4 BE missing sasquatch-v4be",
         _env(chunk_handlers=[V4_BE],
              gaps=[_gap("missing-extractor-dependency", V4_BE, [DEP_BE])]),
         "dep-missing-be", "install-extractor-be", 3),
        ("s3 legacy chunk missing sasquatch",
         _env(chunk_handlers=["squashfs_v3"],
              gaps=[_gap("missing-extractor-dependency", "squashfs_v3", [DEP_LE])]),
         "dep-missing-le", "install-extractor-le", 3),
        ("s3 both names present answers BE first",
         _env(chunk_handlers=["squashfs_v3"],
              gaps=[_gap("missing-extractor-dependency", "squashfs_v3", [DEP_LE, DEP_BE])]),
         "dep-missing-be", "install-extractor-be", 3),
        ("s3 dependency gap beats published files + extractor failure",
         _env(chunk_handlers=["squashfs_v4_le"],
              gaps=[_gap("missing-extractor-dependency", "squashfs_v4_le", [DEP_LE]),
                    _gap(KIND_EXTRACT, "squashfs_v4_le")],
              files=3),
         "dep-missing-le", "install-extractor-le", 3),
        ("s3 dependency naming neither continues past step 3 (falls to 13)",
         _env(chunk_handlers=["squashfs_v3"],
              gaps=[_gap("missing-extractor-dependency", "squashfs_v3", ["7z"])],
              files=2),
         "unclassified", "none", 13),
        # --- step 4
        ("s4 extractor failure with files published",
         _env(chunk_handlers=["squashfs_v4_be"],
              gaps=[_gap(KIND_EXTRACT, "squashfs_v4_be"), _gap("unpublished-entry", None)],
              commands=[v4be_avm], files=7),
         "partial-body-failure", "salvage-partial", 4),
        ("s4 legacy failure with files published",
         _env(chunk_handlers=["squashfs_v3"], gaps=[_gap(KIND_EXTRACT, "squashfs_v3")],
              commands=[le_argv], files=2),
         "partial-body-failure", "salvage-partial", 4),
        # --- step 5
        ("s5 AVM v4 BE failure without -be",
         _env(chunk_handlers=[V4_BE], gaps=[_gap(KIND_EXTRACT, V4_BE)], commands=[v4be_avm]),
         "avm-marker-be-dropped", "wrap-extractor-be", 5),
        ("s5 requires BE=no: -be argv falls to step 7",
         _env(chunk_handlers=[V4_BE], gaps=[_gap(KIND_EXTRACT, V4_BE)], commands=[v4be_be]),
         "body-extractor-failure", "preserve-failure", 7),
        ("s5 requires BE recorded at all (n/a falls to step 7)",
         _env(chunk_handlers=[V4_BE], gaps=[_gap(KIND_EXTRACT, V4_BE)]),
         "body-extractor-failure", "preserve-failure", 7),
        # --- step 6
        ("s6 legacy v3 LE failure",
         _env(chunk_handlers=["squashfs_v3"], gaps=[_gap(KIND_EXTRACT, "squashfs_v3")],
              commands=[le_argv]),
         "legacy-body-failure", "cross-read-legacy", 6),
        ("s6 legacy v3 BE failure (BE ignored for v1-v3)",
         _env(chunk_handlers=["squashfs_v3"], gaps=[_gap(KIND_EXTRACT, "squashfs_v3")],
              commands=[be_argv]),
         "legacy-body-failure", "cross-read-legacy", 6),
        ("s6 legacy v1 failure with no argv recorded",
         _env(chunk_handlers=["squashfs_v1"], gaps=[_gap(KIND_EXTRACT, "squashfs_v1")]),
         "legacy-body-failure", "cross-read-legacy", 6),
        ("s6 legacy v2_nonstandard failure",
         _env(chunk_handlers=["squashfs_v2_nonstandard"],
              gaps=[_gap(KIND_EXTRACT, "squashfs_v2_nonstandard")], commands=[le_argv]),
         "legacy-body-failure", "cross-read-legacy", 6),
        ("s6 legacy v3_ddwrt failure",
         _env(chunk_handlers=["squashfs_v3_ddwrt"],
              gaps=[_gap(KIND_EXTRACT, "squashfs_v3_ddwrt")], commands=[le_argv]),
         "legacy-body-failure", "cross-read-legacy", 6),
        ("s6 legacy v3_broadcom failure",
         _env(chunk_handlers=["squashfs_v3_broadcom"],
              gaps=[_gap(KIND_EXTRACT, "squashfs_v3_broadcom")], commands=[be_argv]),
         "legacy-body-failure", "cross-read-legacy", 6),
        ("s6 legacy handler reaches FH through the gap handler",
         _env(chunk_handlers=[None], gaps=[_gap(KIND_EXTRACT, "squashfs_v3")],
              commands=[le_argv]),
         "legacy-body-failure", "cross-read-legacy", 6),
        # --- step 7
        ("s7 v4 LE failure",
         _env(chunk_handlers=["squashfs_v4_le"], gaps=[_gap(KIND_EXTRACT, "squashfs_v4_le")],
              commands=[le_argv]),
         "body-extractor-failure", "preserve-failure", 7),
        ("s7 v4 broadcom failure is not the AVM row",
         _env(chunk_handlers=["squashfs_v4_broadcom"],
              gaps=[_gap(KIND_EXTRACT, "squashfs_v4_broadcom")], commands=[v4be_avm]),
         "body-extractor-failure", "preserve-failure", 7),
        # --- step 8
        ("s8 depth-limited beats symlink rows",
         _env(chunk_handlers=["squashfs_v3"],
              gaps=[_gap(KIND_DEPTH, None), _gap("unpublished-entry", None)],
              symlink_removed=True, files=2),
         "depth-limited", "raise-depth", 8),
        # --- step 9
        ("s9 removal beside an unpublished entry",
         _env(chunk_handlers=["squashfs_v4_le"],
              gaps=[_gap("unpublished-entry", None)], symlink_removed=True, files=2),
         "mixed-symlinks", "audit-symlinks", 9),
        # --- step 10
        ("s10 removal with no gaps",
         _env(chunk_handlers=["squashfs_v4_le"], symlink_removed=True, files=4),
         "escaping-symlink-removed", "expect-link-absent", 10),
        ("s10 removal with zero files still escaping-symlink-removed",
         _env(chunk_handlers=["squashfs_v4_le"], symlink_removed=True, files=0),
         "escaping-symlink-removed", "expect-link-absent", 10),
        # --- step 11
        ("s11 unpublished-entry exactly",
         _env(chunk_handlers=["squashfs_v3"], gaps=[_gap("unpublished-entry", None)], files=5),
         "in-tree-symlink-metadata", "count-gap", 11),
        # --- step 12
        ("s12 no gaps and files",
         _env(chunk_handlers=["squashfs_v3"], files=5),
         "clean", "none", 12),
        ("s12 no gaps and no files",
         _env(chunk_handlers=["squashfs_v3"], files=0),
         "clean-empty", "confirm-empty", 12),
        ("s12 no gaps and absent files list reads 0",
         _env(chunk_handlers=["squashfs_v3"], files=0),
         "clean-empty", "confirm-empty", 12),
        # --- step 13
        ("s13 encrypted chunk",
         _env(chunk_handlers=["squashfs_v4_le"],
              gaps=[_gap("encrypted-chunk", "squashfs_v4_le")], files=2),
         "unclassified", "none", 13),
        ("A1 s9 unknown-chunk-handler beside a clean squashfs chunk",
         _env(chunk_handlers=["squashfs_v3", None],
              gaps=[_gap("unknown-chunk-handler", None)], files=2),
         "unknown-residue", "isolate-residue", 109),
        ("s13 removal beside an unrelated gap",
         _env(chunk_handlers=["squashfs_v4_le"],
              gaps=[_gap("encrypted-chunk", "squashfs_v4_le")],
              symlink_removed=True, files=2),
         "unclassified", "none", 13),
        # --- envelope wrapper
        ("cli envelope wrapper is unwrapped",
         _env(chunk_handlers=["squashfs_v3"], wrap=True, files=1),
         "clean", "none", 12),
    ]
    old_to_a1 = {1: 1, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 10, 9: 11, 10: 12, 11: 13, 12: 14, 13: 15}
    cases = [(n, e, l, a, (st - 100 if st > 100 else old_to_a1[st])) for n, e, l, a, st in cases]
    cases += [
        ("A1 s2 container at depth limit (tar, no squashfs handler)",
         _env(chunk_handlers=["tar"], gaps=[_gap(KIND_DEPTH, None)], files=1),
         "container-depth-limited", "raise-depth", 2),
        ("A1 s2 null handler with depth-limited",
         _env(chunk_handlers=[None], gaps=[_gap(KIND_DEPTH, None)]),
         "container-depth-limited", "raise-depth", 2),
        ("A1 s3 container without depth limit is no-squashfs-chunk",
         _env(chunk_handlers=["tar"], files=3),
         "no-squashfs-chunk", "inspect-input", 3),
        ("A1 s9 residue beats depth-limited",
         _env(chunk_handlers=["squashfs_v3", None],
              gaps=[_gap(KIND_UNKNOWN, None), _gap(KIND_DEPTH, None), _gap(KIND_UNPUBLISHED, None)],
              files=3),
         "unknown-residue", "isolate-residue", 9),
        ("A1 s5 partial failure beats residue",
         _env(chunk_handlers=["squashfs_v4_le", None],
              gaps=[_gap(KIND_EXTRACT, "squashfs_v4_le"), _gap(KIND_UNKNOWN, None)], files=2),
         "partial-body-failure", "salvage-partial", 5),
        ("A1 s7 HF names the failing legacy chunk beside a clean v4 BE chunk",
         _env(chunk_handlers=["squashfs_v3", V4_BE], gaps=[_gap(KIND_EXTRACT, "squashfs_v3")],
              commands=[le_argv]),
         "legacy-body-failure", "cross-read-legacy", 7),
        ("A1 s8 failing v4 LE chunk beside a clean legacy chunk",
         _env(chunk_handlers=["squashfs_v3", "squashfs_v4_le"],
              gaps=[_gap(KIND_EXTRACT, "squashfs_v4_le")], commands=[le_argv]),
         "body-extractor-failure", "preserve-failure", 8),
        ("A1 HF falls back to F, not H (handlerless failure gap, non-squashfs sibling)",
         _env(chunk_handlers=["squashfs_v3", "gzip"], gaps=[_gap(KIND_EXTRACT, None)],
              commands=[le_argv]),
         "legacy-body-failure", "cross-read-legacy", 7),
    ]
    return cases


def selftest() -> int:
    failures = 0
    cases = _cases()
    for name, raw, want_label, want_action, want_step in cases:
        env = unwrap(raw)
        result = evaluate(env)
        got = (result["label"], result["action"], result["step"])
        want = (want_label, want_action, want_step)
        if got == want:
            print(f"PASS {name}")
        else:
            failures += 1
            print(f"FAIL {name}: got {got} want {want}")
    # Every step 1-15 must be reachable, and every vocabulary pair must appear.
    seen_steps = {
        evaluate(unwrap(raw))["step"] for _, raw, *_ in cases
    }
    pairs = {(evaluate(unwrap(raw))["label"], evaluate(unwrap(raw))["action"]) for _, raw, *_ in cases}
    missing_steps = sorted(set(range(1, 16)) - seen_steps)
    missing_pairs = sorted(set(VOCABULARY) - pairs)
    if missing_steps:
        failures += 1
        print(f"FAIL unreachable steps: {missing_steps}")
    else:
        print("PASS every step 1-15 is exercised")
    if missing_pairs:
        failures += 1
        print(f"FAIL vocabulary never produced: {missing_pairs}")
    else:
        print("PASS every (label, action) pair is exercised")
    print(f"{len(cases) - failures if failures <= len(cases) else 0}/{len(cases)} cases; "
          f"{failures} failure(s)")
    return 1 if failures else 0


# ------------------------------------------------------------------------- main


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="R42-C2 independent evaluator")
    parser.add_argument("envelope", nargs="?", help="one envelope JSON (bare or CLI form)")
    parser.add_argument("--envelopes", metavar="DIR", help="directory of envelopes")
    parser.add_argument("--out", metavar="FILE", help="write JSON here instead of stdout")
    parser.add_argument(
        "--full", action="store_true", help="prefer rea-full.json (the CLI envelope)"
    )
    parser.add_argument("--selftest", action="store_true", help="run hand-written envelopes")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    if args.envelopes:
        try:
            payload = run_batch(args.envelopes, args.full)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"{EVALUATOR}: {exc}", file=sys.stderr)
            return 2
        text = json.dumps(payload, indent=1, sort_keys=False) + "\n"
        if args.out:
            with open(args.out, "w", encoding="utf-8") as handle:
                handle.write(text)
        else:
            sys.stdout.write(text)
        return 0

    if args.envelope:
        try:
            with open(args.envelope, encoding="utf-8") as handle:
                env = unwrap(json.load(handle))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"{EVALUATOR}: {exc}", file=sys.stderr)
            return 2
        payload = _record(os.path.basename(args.envelope), os.path.abspath(args.envelope), env)
        text = json.dumps(payload, indent=1) + "\n"
        if args.out:
            with open(args.out, "w", encoding="utf-8") as handle:
                handle.write(text)
        else:
            sys.stdout.write(text)
        return 0

    parser.print_usage(sys.stderr)
    print(f"{EVALUATOR}: give an envelope, --envelopes DIR or --selftest", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
