#!/usr/bin/env python3
"""R40-C1 rerun-binding semantic projection (pre-freeze draft tool).

Hypothesis this tool measures:
  two REA 6.5.0 `extract-firmware` runs of the same carrier, into *different*
  scratch output directories, yield an identical semantic projection.

The projection is exactly the field list named in the R40-C1 draft predicate, so
that the freeze can adopt it unchanged or extend it with a measured reason:

  subject_sha256       subject.digest.sha256
  files                sorted [suffix, sha256, size]            (normalized_result.files)
  chunks               sorted [handler, start, end, extraction_failed]
  extraction_gaps      sorted [kind, suffix, sorted(suffix(dep) ...)]
  unpublished_entries  sorted [kind, suffix]
  diagnostics          sorted multiset of diagnostics[*].report.__typename__

`suffix` is the path after the first path component that ends in `_extract`
(the chunk extract directory), with a leading `$output/` removed.  A v4 SquashFS
member is therefore `firmware.bin_extract/x/y` -> `x/y`, independent of the
scratch root the run happened to use.  Nothing else is compared: `evidence_id`,
`parameters.output_directory`, `files[].path`, `chunks[].provider_id`,
`derivations[].provider_blob_id`, `extraction_gaps[].continuation_id`,
`raw_result.report[].task.path` and every timestamp are run-identity, and the
hypothesis is that they are the *only* fields that vary (see field-variance.py).

`--profile` exists because the six-field projection may be oracle-closed (a
fabricator that reads carrier pin + oracle.tsv + symlinks.tsv can produce all six
fields without running anything).  The extended profiles are measurements for the
freeze decision, never the default:
  core            the six draft fields (default; what the predicate would freeze)
  plus-mime       core + files[].mime_type (libmagic: not in the oracle)
  plus-content    plus-mime + files[].md5 and files[].sha1 taken from the run's
                  raw_result HashReport (content fingerprints the frozen oracle,
                  which publishes sha256 only, cannot produce without the bytes)
  plus-extractor  plus-mime + ordered derivations edges + engine name/version +
                  published_bytes + coverage (all extractor-determined)

Usage
  projection.py project FILE [--profile core|plus-mime|plus-extractor] [--json]
  projection.py compare A B [--profile ...] [--json]
  projection.py --selftest
Exit: 0 equal / project ok; 3 projections differ; 2 bad input; 1 selftest failure.
Pure stdlib.
"""

import argparse
import hashlib
import json
import sys
from collections import Counter

SCHEMA = "kaidoku-r40-rerun-projection-v0-draft"
PROFILES = ("core", "plus-mime", "plus-content", "plus-extractor")
EXTRACT_MARK = "_extract"
OUTPUT_MARK = "$output/"


# --------------------------------------------------------------------------- io
def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


# ------------------------------------------------------------------- path rule
def rel_suffix(relpath):
    """Path after the first `<something>_extract` chunk extract directory.

    A missing path is legitimate in an extraction that never produced entries
    (e.g. `missing-extractor-dependency` gaps carry relative_path: null), so
    None is preserved rather than raised on; anything else non-string is an
    input error.
    """
    if relpath is None:
        return None
    if not isinstance(relpath, str):
        raise ValueError("path is not a string: %r" % (relpath,))
    path = relpath
    while path.startswith(OUTPUT_MARK):
        path = path[len(OUTPUT_MARK):]
    parts = [p for p in path.split("/") if p not in ("", ".")]
    for i, part in enumerate(parts):
        if part.endswith(EXTRACT_MARK) and i + 1 < len(parts):
            return "/".join(parts[i + 1:])
    return "/".join(parts)


# ------------------------------------------------------------------ projection
def _normalized(receipt):
    nr = receipt.get("normalized_result")
    if not isinstance(nr, dict):
        raise ValueError("receipt has no normalized_result object")
    return nr


def project(receipt, profile="core"):
    """Return the semantic projection dict (JSON-serialisable, order-free)."""
    if profile not in PROFILES:
        raise ValueError("unknown profile %r" % (profile,))
    nr = _normalized(receipt)
    subject = ((receipt.get("subject") or {}).get("digest") or {}).get("sha256")

    hashes = {}
    if profile in ("plus-content", "plus-extractor"):
        for task in (receipt.get("raw_result") or {}).get("report") or []:
            # the HashReport carries no path of its own; the task does
            key = rel_suffix((task.get("task") or {}).get("path"))
            if key is None:
                continue
            for report in task.get("reports") or []:
                if report.get("__typename__") != "HashReport":
                    continue
                hashes[key] = {"md5": report.get("md5"), "sha1": report.get("sha1")}
    want_mime = profile != "core"
    want_content = profile in ("plus-content", "plus-extractor")
    files = []
    for entry in nr.get("files") or []:
        row = [rel_suffix(entry.get("relative_path")),
               entry.get("sha256"),
               entry.get("size")]
        if want_mime:
            row.append(entry.get("mime_type"))
        if want_content:
            content = hashes.get(rel_suffix(entry.get("relative_path")) or "", {})
            row.append(content.get("md5"))
            row.append(content.get("sha1"))
        files.append(row)
    files.sort(key=lambda r: (r[0] if r[0] is not None else "", canonical(r[1:])))
    keep = 3 + (1 if want_mime else 0) + (2 if want_content else 0)
    files = [r[:keep] for r in files]

    chunks = []
    for chunk in nr.get("chunks") or []:
        rng = chunk.get("range") or {}
        start = rng.get("offset")
        end = None
        if isinstance(start, int) and isinstance(rng.get("length"), int):
            end = start + rng["length"]
        chunks.append([chunk.get("handler"), start, end,
                       bool(chunk.get("extraction_failed"))])
    chunks.sort(key=canonical)

    gaps = []
    for gap in nr.get("extraction_gaps") or []:
        deps = sorted(rel_suffix(d) for d in (gap.get("dependencies") or []))
        gaps.append([gap.get("kind"), rel_suffix(gap.get("relative_path")), deps])
    gaps.sort(key=canonical)

    unpublished = []
    for entry in nr.get("unpublished_entries") or []:
        unpublished.append([entry.get("kind"), rel_suffix(entry.get("relative_path"))])
    unpublished.sort(key=canonical)

    diagnostics = sorted(
        ((diag.get("report") or {}).get("__typename__") or "<none>")
        for diag in nr.get("diagnostics") or []
    )

    out = {
        "schema": SCHEMA,
        "profile": profile,
        "subject_sha256": subject,
        "files": files,
        "chunks": chunks,
        "extraction_gaps": gaps,
        "unpublished_entries": unpublished,
        "diagnostics": diagnostics,
    }

    if profile == "plus-extractor":
        edges = []
        for deriv in nr.get("derivations") or []:
            edges.append([rel_suffix(deriv.get("parent_path")),
                          rel_suffix(deriv.get("child_path")),
                          deriv.get("handler")])
        edges.sort(key=canonical)
        out["derivations"] = edges
        engine = nr.get("engine") or {}
        out["engine"] = {"name": engine.get("name"), "version": engine.get("version")}
        out["published_bytes"] = nr.get("published_bytes")
        out["coverage"] = nr.get("coverage")

    out["projection_sha256"] = digest({k: v for k, v in out.items()
                                       if k != "projection_sha256"})
    return out


# -------------------------------------------------------------------- compare
def _index(rows, key_len, key_positions):
    """Map a tuple of selected positions -> list of rows (collision-safe)."""
    index = {}
    for row in rows:
        key = tuple(row[p] for p in key_positions)
        index.setdefault(key, []).append(row)
    return index


def _set_diff(left, right):
    lcount = Counter(canonical(r) for r in left)
    rcount = Counter(canonical(r) for r in right)
    missing = sorted((lcount - rcount).elements())
    extra = sorted((rcount - lcount).elements())
    return [json.loads(x) for x in missing], [json.loads(x) for x in extra]


def _files_detail(left, right):
    lmap = {row[0]: row for row in left}
    rmap = {row[0]: row for row in right}
    missing = [lmap[k] for k in sorted(set(lmap) - set(rmap))]
    extra = [rmap[k] for k in sorted(set(rmap) - set(lmap))]
    changed = [{"suffix": k, "left": lmap[k], "right": rmap[k]}
               for k in sorted(set(lmap) & set(rmap)) if lmap[k] != rmap[k]]
    return {"missing_in_right": missing, "extra_in_right": extra, "changed": changed}


def compare(left, right, profile="core"):
    """Compare two receipts (or two projections). Returns a JSON-able dict."""
    lp = left if isinstance(left, dict) and left.get("schema") == SCHEMA else project(left, profile)
    rp = right if isinstance(right, dict) and right.get("schema") == SCHEMA else project(right, profile)
    fields = [k for k in lp if k not in ("schema", "profile", "projection_sha256")]
    diff = {}
    for field in fields:
        if field not in rp:
            diff[field] = {"left": lp[field], "right": None, "detail": "absent"}
            continue
        if canonical(lp[field]) == canonical(rp[field]):
            continue
        detail = None
        if field == "files":
            detail = _files_detail(lp[field], rp[field])
        elif isinstance(lp[field], list):
            missing, extra = _set_diff(lp[field], rp[field])
            detail = {"missing_in_right": missing, "extra_in_right": extra}
        diff[field] = {"left": lp[field], "right": rp[field], "detail": detail}
    return {
        "schema": SCHEMA,
        "profile": profile,
        "equal": not diff,
        "differing_fields": sorted(diff),
        "diff": diff,
        "left_sha256": lp.get("projection_sha256"),
        "right_sha256": rp.get("projection_sha256"),
    }


# -------------------------------------------------------------------- selftest
def _receipt(files, chunks, gaps, unpublished, diagnostics, subject="pin",
             outdir="/scratch/a/extract", evidence_id="ev_a", prefix="firmware.bin_extract"):
    def rel(inner):
        return "%s/%s" % (prefix, inner)

    nr = {
        "engine": {"name": "unblob", "version": "26.6.4",
                   "executable_path": "/host/unblob",
                   "executable_sha256": "0" * 64,
                   "source_revision": None, "worker_count": 1},
        "selection": {"offset": 0, "length": 10, "sha256": subject},
        "output_directory": outdir,
        "coverage": "partial" if gaps else "complete",
        "files": [
            {"relative_path": rel(inner), "path": "%s/%s" % (outdir, rel(inner)),
             "size": size, "sha256": sha, "reported_sha256": sha,
             "mime_type": mime, "analysis_depth": 1,
             "runtime_address": None, "original_file_range": None}
            for inner, sha, size, mime in files
        ],
        "unpublished_entries": [
            {"relative_path": rel(inner), "kind": kind, "link_target": target}
            for inner, kind, target in unpublished
        ],
        "chunks": [
            {"input_path": "$input", "provider_id": "1:1",
             "range": {"offset": offset, "length": length}, "handler": handler,
             "encrypted": False, "root_file_range": {"offset": offset, "length": length},
             "extraction_failed": failed}
            for handler, offset, length, failed in chunks
        ],
        "derivations": [
            {"parent_path": "$output/" + prefix, "child_path": rel(inner),
             "provider_blob_id": "1:1", "handler": None, "parent_file_range": None}
            for inner, _sha, _size, _mime in files
        ],
        "depth_limited_paths": [],
        "diagnostics": [
            {"input_path": "$input",
             "report": {"__typename__": typename, "severity": "WARNING",
                        "link": "%s/%s" % (outdir, rel(inner)),
                        "target": "/host/extracted/etc/x"}}
            for inner, typename in diagnostics
        ],
        "extraction_gaps": [
            {"kind": kind, "input_path": "$output/" + rel(inner),
             "relative_path": rel(inner), "handler": None, "provider_id": None,
             "range": None, "root_file_range": None, "dependencies": deps,
             "continuation_id": "c" * 64}
            for kind, inner, deps in gaps
        ],
        "extraction_continuations": [],
        "published_bytes": sum(size for _i, _s, size, _m in files),
    }
    return {
        "evidence_id": evidence_id,
        "subject": {"name": "carrier.sqsh", "digest": {"sha256": subject},
                    "local_path": "/lane/carrier.sqsh", "format": "file",
                    "architecture": None},
        "provider": {"id": "unblob", "name": "Unblob", "version": "26.6.4"},
        "analysis_profile": None,
        "predicate_type": "rea.analysis",
        "operation": "extract_firmware",
        "parameters": {"path": "/lane/carrier.sqsh", "output_directory": outdir,
                       "max_depth": 3, "max_output_bytes": 1, "max_output_files": 1},
        "raw_result": {"report": [], "execution": {"stdout": {"text": outdir}},
                       "version_execution": {}},
        "normalized_result": nr,
        "confidence": "observed",
        "authority": "shipped-artifact",
        "environment": None,
        "limitations": None,
        "relationship_coverage": None,
        "locations": [{"kind": "file-offset-range", "start": 0, "end": 10}],
        "evidence_links": [],
    }


BASE_FILES = [("README.txt", "a" * 64, 10, "text/plain"),
              ("cfg/app.json", "b" * 64, 20, "application/json")]
BASE_CHUNKS = [("squashfs_v4_be", 0, 100, False)]
BASE_GAPS = [("unpublished-entry", "usr/link-in", [])]
BASE_UNPUB = [("usr/link-in", "symlink", "notes.txt")]
BASE_DIAG = [("usr/escape", "MaliciousSymlinkRemoved")]


def _base(**kw):
    args = {"files": BASE_FILES, "chunks": BASE_CHUNKS, "gaps": BASE_GAPS,
            "unpublished": BASE_UNPUB, "diagnostics": BASE_DIAG}
    args.update(kw)
    return _receipt(**args)


def selftest():
    cases = []

    def case(name, left, right, expect_equal, expect_fields=(), profile="core"):
        cases.append((name, left, right, expect_equal, tuple(expect_fields), profile))

    # --- invariance: only run identity changes -------------------------------
    run2 = _base(outdir="/other/root/e2/extract", evidence_id="ev_b")
    run2["normalized_result"]["chunks"][0]["provider_id"] = "999:1"
    run2["normalized_result"]["derivations"][0]["provider_blob_id"] = "999:1"
    for f in run2["normalized_result"]["files"]:
        f["path"] = f["path"].replace("/scratch/a/extract", "/other/root/e2/extract")
    run2["raw_result"]["report"] = [{"task": {"path": "/other/root/e2/tmp/x", "blob_id": "999:1"}}]
    run2["parameters"]["output_directory"] = "/other/root/e2/extract"
    case("run-identity-only", _base(), run2, True)

    reordered = _base()
    reordered["normalized_result"]["files"].reverse()
    reordered["normalized_result"]["unpublished_entries"].reverse()
    case("order-insensitive", _base(), reordered, True)

    bracket = _base()
    for f in bracket["normalized_result"]["files"]:
        f["relative_path"] = "$output/" + f["relative_path"]
    for g in bracket["normalized_result"]["extraction_gaps"]:
        g["relative_path"] = "$output/" + g["relative_path"]
    for u in bracket["normalized_result"]["unpublished_entries"]:
        u["relative_path"] = "$output/" + u["relative_path"]
    case("output-token-prefix", _base(), bracket, True)

    nested = _base(prefix="firmware.bin_extract/inner.sqfs_extract")
    case("nested-extract-visible", _base(), nested, False,
         ("files", "extraction_gaps", "unpublished_entries"))  # suffix keeps inner dir

    # --- the six draft fields must discriminate ------------------------------
    case("subject-pin", _base(), _base(subject="other"), False, ("subject_sha256",))

    f = list(BASE_FILES)
    f[0] = ("README.txt", "c" * 64, 10, "text/plain")
    case("file-sha", _base(), _base(files=f), False, ("files",))

    f = list(BASE_FILES)
    f[0] = ("README.txt", "a" * 64, 11, "text/plain")
    case("file-size", _base(), _base(files=f), False, ("files",))

    case("file-missing", _base(), _base(files=BASE_FILES[:1]), False, ("files",))

    case("chunk-handler", _base(), _base(chunks=[("squashfs_v4_le", 0, 100, False)]),
         False, ("chunks",))
    case("chunk-failed", _base(), _base(chunks=[("squashfs_v4_be", 0, 100, True)]),
         False, ("chunks",))
    case("chunk-range", _base(), _base(chunks=[("squashfs_v4_be", 0, 99, False)]),
         False, ("chunks",))

    case("gap-kind", _base(), _base(gaps=[("missing-extractor-dependency", "usr/link-in", [])]),
         False, ("extraction_gaps",))
    case("gap-missing", _base(), _base(gaps=[]), False, ("extraction_gaps",))
    case("gap-dependencies", _base(), _base(gaps=[("unpublished-entry", "usr/link-in",
                                                   ["firmware.bin_extract/x"])]),
         False, ("extraction_gaps",))
    case("unpublished-link", _base(), _base(unpublished=[]), False,
         ("unpublished_entries",))

    case("diagnostics-multiset", _base(), _base(diagnostics=[]), False, ("diagnostics",))
    case("diagnostics-count", _base(), _base(diagnostics=BASE_DIAG * 2), False,
         ("diagnostics",))

    # --- profiles: mime is invisible to core, visible to plus-mime -----------
    f = list(BASE_FILES)
    f[1] = ("cfg/app.json", "b" * 64, 20, "text/plain")
    case("mime-only-core-blind", _base(), _base(files=f), True)
    case("mime-only-plus-mime", _base(), _base(files=f), False, ("files",),
         profile="plus-mime")

    with_hash = _base()
    with_hash["raw_result"]["report"] = [
        {"task": {"path": "/x/extracted/firmware.bin_extract/README.txt"},
         "reports": [{"__typename__": "HashReport", "md5": "1" * 32, "sha1": "2" * 40,
                      "sha256": "a" * 64, "path": "/x/extracted/firmware.bin_extract/README.txt"}]},
        {"task": {"path": "/x/extracted/firmware.bin_extract/cfg/app.json"},
         "reports": [{"__typename__": "HashReport", "md5": "3" * 32, "sha1": "4" * 40,
                      "sha256": "b" * 64, "path": "/x/extracted/firmware.bin_extract/cfg/app.json"}]},
    ]
    without_hash = _base()
    case("content-core-blind", with_hash, without_hash, True)
    case("content-plus-content", with_hash, without_hash, False, ("files",),
         profile="plus-content")

    # --- failure shapes are total -------------------------------------------
    def failed(path_in_gap):
        r = _base(files=[], gaps=[("missing-extractor-dependency", path_in_gap, [])],
                  unpublished=[], diagnostics=[])
        if path_in_gap is None:
            for g in r["normalized_result"]["extraction_gaps"]:
                g["relative_path"] = None
                g["input_path"] = "$input"
        r["normalized_result"]["chunks"][0]["extraction_failed"] = True
        return r

    case("null-gap-path-total", failed(None), failed(None), True)
    case("failed-chunk-visible", _base(), failed("x"), False,
         ("files", "chunks", "extraction_gaps", "unpublished_entries", "diagnostics"))

    # --- both projections carry a stable digest -----------------------------
    p1 = project(_base())
    p2 = project(run2)
    cases.append(("digest-stable", p1, p2, True, (), "core"))

    failures = []
    for name, left, right, expect_equal, expect_fields, profile in cases:
        if isinstance(left, dict) and left.get("schema") == SCHEMA:
            result = compare(left, right, profile)
        else:
            result = compare(left, right, profile)
        ok = result["equal"] is expect_equal
        if ok and not expect_equal:
            ok = set(result["differing_fields"]) == set(expect_fields)
        status = "PASS" if ok else "FAIL"
        print("%s %-26s equal=%-5s fields=%s" %
              (status, name, result["equal"], ",".join(result["differing_fields"]) or "-"))
        if not ok:
            failures.append((name, result))
    total = len(cases)
    print("\nselftest: %d cases, %d pass, %d fail" % (total, total - len(failures), len(failures)))
    for name, result in failures:
        print("  failed: %s\n%s" % (name, json.dumps(result["diff"], indent=1)[:2000]))
    return 1 if failures else 0


# ------------------------------------------------------------------------ main
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()

    ap = argparse.ArgumentParser(description="R40-C1 rerun-binding semantic projection")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_project = sub.add_parser("project", help="print the projection of one receipt")
    p_project.add_argument("file")
    p_project.add_argument("--profile", choices=PROFILES, default="core")
    p_project.add_argument("--json", action="store_true")
    p_compare = sub.add_parser("compare", help="compare two receipts (or projections)")
    p_compare.add_argument("left")
    p_compare.add_argument("right")
    p_compare.add_argument("--profile", choices=PROFILES, default="core")
    p_compare.add_argument("--json", action="store_true")
    opts = ap.parse_args(argv)

    try:
        if opts.cmd == "project":
            out = project(load_json(opts.file), opts.profile)
            print(json.dumps(out, indent=2, ensure_ascii=False) if opts.json
                  else out["projection_sha256"])
            return 0
        result = compare(load_json(opts.left), load_json(opts.right), opts.profile)
        if opts.json:
            print(json.dumps(result, indent=1, ensure_ascii=False))
        else:
            print("equal=%s fields=%s" %
                  (result["equal"], ",".join(result["differing_fields"]) or "-"))
        return 0 if result["equal"] else 3
    except (OSError, ValueError) as exc:
        print("projection: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
