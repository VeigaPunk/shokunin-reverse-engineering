#!/usr/bin/env python3
"""selfcheck.py — developer fixture runner for selection.py.

Round-16 wave w1 deliverable. This is a *developer test runner only*: it is not
registered as any gate, produces no score, and proves nothing about the real
Ghidra runtime. It exercises the source-law *model* in selection.py against
hand-authored fixture trees built under an isolated temporary directory.

Usage (isolated invocation, matching the project's exercised recheck
convention):
    python3 -I selfcheck.py [--fixtures PATH ...]

Default fixture file: selection-fixtures.json next to this script. The option
is repeatable, so negative-fixtures.json (or any other schema-conforming file)
can be added:

    python3 -I selfcheck.py --fixtures selection-fixtures.json \
        --fixtures negative-fixtures.json

Fixture schema (shared contract):
    Top level: {"cases": [case, ...]} or a bare list of cases.
    case:
      id        unique string label (required)
      request   "M.m.p" string passed to select_snapshot (required)
      goos      GOOS string, default "linux"
      goarch    GOARCH string, default "amd64"
      files     mapping of relative filename -> content, materialized under a
                fresh temporary root:
                  * JSON object {}  -> written as a JSON document
                  * string          -> written verbatim (raw bytes/text, e.g.
                                       intentionally unreadable JSON)
                  * {"raw": str}    -> written verbatim (explicit form)
                  * {"raw_b64": s}  -> base64-decoded bytes written verbatim
      expected  mapping whose entries must appear identically in the result
                dict returned by select_snapshot (subset match). Required for
                positive cases with at least one non-forced key — a mapping
                that is empty or names only patch_applied/evidence_class
                (which carry no source-selection content) is a harness error,
                not a vacuous pass.
      expect_error  optional; when present the case passes iff
                select_snapshot raises instead of returning:
                  * true            -> any Exception
                  * string          -> substring of the exception type name
                                       or message
                  * {"type": T, "contains": S} -> type-name substring T and
                                       message substring S (either field may
                                       be omitted)

Expectation semantics:
  * A key absent from the result always mismatches ("key missing") — an
    expected null never passes on absence; null means the key is present
    with value None.
  * "base" and "selected_diff": a string expectation containing '/'
    (e.g. "patchverdiffs/go1.24.5.json.diff") is compared against the actual
    file's path relative to the case temp root, preserving the subdirectory;
    a string without '/' is compared against the basename only (fixture roots
    are temporary, so absolute paths are never asserted). A mapping expectation
    is matched recursively, with a "path" member normalized the same way.
  * "patch_applied" is forced to boolean False and "evidence_class" to
    "source_model" on every non-error result — the preview never applies
    JsonPatch and its evidence is source-model only. If a case also authors an
    expectation for either key it is still compared against the actual value,
    so a conflicting authored value fails loudly instead of being discarded.
  * Integer expectations are exact-int: an actual bool (False/True == 0/1)
    never satisfies an int expectation.

Exit status: 0 when every case passes, 1 when any case mismatches, 2 on
harness-level failures (unreadable/invalid fixtures file, missing or
non-importable selection.py, malformed case schema — per-case FixtureError is
printed as ERROR and drives exit 2, not exit 1). Per-case results and the
exact differing keys are printed to stdout.
"""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SELECTION_PATH = HERE / "selection.py"
DEFAULT_FIXTURES = HERE / "selection-fixtures.json"

# Result keys whose expectations are filenames, matched against the basename
# of the reported path rather than a rooted absolute path.
PATH_KEYS = ("base", "selected_diff")

# Forced invariants of the selection preview: no diff is ever applied, and the
# result is a source-model observation, not a provider or runtime result.
FORCED = (("patch_applied", False), ("evidence_class", "source_model"))
FORCED_KEYS = frozenset(k for k, _ in FORCED)


class FixtureError(Exception):
    """The fixture file or a case violates the shared schema."""


def _load_selection_module(path: Path):
    """Import selection.py by path via importlib (no sys.path mutation).

    sys.dont_writebytecode is raised around exec_module so the import cannot
    leave a __pycache__ under the live wave directory; the runner promises
    writes confined to per-case temp trees. The previous flag is restored in
    the finally block, so the documented 'python3 -I' argv is unchanged.
    """
    spec = importlib.util.spec_from_file_location("kaidoku_r16_selection", path)
    if spec is None or spec.loader is None:
        raise FixtureError(f"cannot build import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def _load_cases(path: Path) -> list:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise FixtureError(f"cannot read fixtures {path}: {exc}") from exc
    except UnicodeError as exc:
        raise FixtureError(f"fixtures {path} is not valid UTF-8: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise FixtureError(f"invalid JSON in fixtures {path}: {exc}") from exc
    if isinstance(doc, dict):
        doc = doc.get("cases", doc)
    if not isinstance(doc, list):
        raise FixtureError(f"{path}: expected a case list or {{'cases': [...]}}")
    return doc


def _materialize(root: Path, files) -> None:
    """Write the case's file mapping under the temporary root."""
    if files is None:
        return
    if not isinstance(files, dict):
        raise FixtureError(f"'files' must be an object, got {type(files).__name__}")
    for relname, content in files.items():
        if not isinstance(relname, str) or not relname:
            raise FixtureError(f"invalid fixture filename {relname!r}")
        rel = Path(relname)
        if rel.is_absolute() or ".." in rel.parts:
            raise FixtureError(f"fixture filename escapes the temp root: {relname!r}")
        target = root / rel
        if isinstance(content, dict) and "raw_b64" in content:
            data = base64.b64decode(content["raw_b64"])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            continue
        if isinstance(content, dict) and "raw" in content:
            text = content["raw"]
            if not isinstance(text, str):
                raise FixtureError(f"'raw' for {relname} must be a string")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            continue
        if isinstance(content, str):
            # Raw verbatim text: lets fixtures carry intentionally malformed
            # JSON without inventing an out-of-schema marker.
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            continue
        if isinstance(content, (dict, list)):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(content, indent=2) + "\n", encoding="utf-8")
            continue
        raise FixtureError(
            f"unsupported file content for {relname}: {type(content).__name__}")


def _entry_path(entry):
    """Extract the raw path string from a base/selected_diff entry, or None."""
    if isinstance(entry, dict):
        return entry.get("path")
    if isinstance(entry, str):
        return entry
    return None


def _basename_of(entry):
    """Return the basename of a base/selected_diff entry's path, or None."""
    raw = _entry_path(entry)
    return None if raw is None else Path(str(raw)).name


def _path_cmp(entry, root, exp: str):
    """Normalize an actual path for comparison against a string expectation.

    An expectation containing '/' (e.g. "patchverdiffs/go1.24.5.json.diff") is
    compared against the path relative to the case's temp root, preserving the
    subdirectory; an expectation without '/' compares basenames only. A path
    outside the root falls back to its absolute spelling, which mismatches the
    relative expectation explicitly rather than silently degrading.
    """
    raw = _entry_path(entry)
    if raw is None:
        return None
    if "/" not in exp:
        return Path(str(raw)).name
    try:
        return Path(str(raw)).relative_to(root).as_posix()
    except (ValueError, OSError):
        return str(raw)


def _match(actual, expected, key_path, diffs) -> None:
    """Recursive subset comparison; diffs collects dotted key-path mismatches."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            diffs.append(f"{key_path}: expected object {expected!r}, got {actual!r}")
            return
        for k, v in expected.items():
            child = f"{key_path}.{k}" if key_path else k
            if k not in actual:
                diffs.append(f"{child}: expected {v!r}, key missing")
            else:
                _match(actual[k], v, child, diffs)
        return
    if isinstance(expected, bool):
        # Boolean compare by identity: 0/1 must not satisfy true/false.
        if actual is not expected:
            diffs.append(f"{key_path}: expected {expected!r}, got {actual!r}")
        return
    if isinstance(expected, int):
        # Exact int: a bool actual (False/True == 0/1) must not satisfy it.
        if type(actual) is not int or actual != expected:
            diffs.append(f"{key_path}: expected {expected!r}, got {actual!r}")
        return
    if actual != expected:
        diffs.append(f"{key_path}: expected {expected!r}, got {actual!r}")


def _compare(result, expected, root: Path) -> list:
    """Return the list of mismatch descriptions for one case result."""
    diffs = []
    if not isinstance(result, dict):
        diffs.append(f"result: expected dict, got {type(result).__name__}")
        return diffs
    # Forced invariants first: patch_applied must be literally False and
    # evidence_class literally "source_model" on every non-error result.
    for key, want in FORCED:
        got = result.get(key, "<missing>")
        if key == "patch_applied":
            if got is not False:
                diffs.append(f"{key}: expected False, got {got!r}")
        elif got != want:
            diffs.append(f"{key}: expected {want!r}, got {got!r}")
    for key, exp in expected.items():
        # Forced keys still compare an authored expectation against the actual
        # value (below) so a conflicting fixture value fails loudly instead of
        # being silently discarded by the forced pass above.
        if key not in result:
            # Presence check precedes every comparison shape: without it a
            # missing key reads as None and an expected null would pass.
            diffs.append(f"{key}: expected {exp!r}, key missing")
            continue
        if key in PATH_KEYS:
            actual_entry = result[key]
            if isinstance(exp, str):
                got = _path_cmp(actual_entry, root, exp)
                if got != exp:
                    diffs.append(f"{key}: expected path {exp!r}, got {got!r}")
            elif isinstance(exp, dict):
                if not isinstance(actual_entry, dict):
                    diffs.append(f"{key}: expected object {exp!r}, got {actual_entry!r}")
                    continue
                for k, v in exp.items():
                    child = f"{key}.{k}"
                    if k not in actual_entry:
                        diffs.append(f"{child}: expected {v!r}, key missing")
                    elif k == "path" and isinstance(v, str):
                        got = _path_cmp(actual_entry, root, v)
                        if got != v:
                            diffs.append(f"{child}: expected path {v!r}, got {got!r}")
                    else:
                        _match(actual_entry[k], v, child, diffs)
            elif exp is None:
                if actual_entry is not None:
                    diffs.append(f"{key}: expected None, got {actual_entry!r}")
            else:
                diffs.append(f"{key}: unsupported expectation type "
                             f"{type(exp).__name__} for a path key")
            continue
        _match(result[key], exp, key, diffs)
    return diffs


def _error_ok(exc: BaseException, spec) -> bool:
    if spec is True:
        return isinstance(exc, Exception)
    name = type(exc).__name__
    msg = str(exc)
    if isinstance(spec, str):
        return spec in name or spec in msg
    if isinstance(spec, dict):
        t = spec.get("type")
        c = spec.get("contains")
        if t is not None and t not in name:
            return False
        if c is not None and c not in msg:
            return False
        return t is not None or c is not None
    return False


def run_case(module, case) -> tuple:
    """Run one fixture case. Returns (ok, detail_lines)."""
    if not isinstance(case, dict):
        raise FixtureError(f"case is not an object: {case!r}")
    cid = case.get("id")
    if not isinstance(cid, str) or not cid:
        raise FixtureError(f"case missing string 'id': {case!r}")
    request = case.get("request")
    if not isinstance(request, str):
        raise FixtureError(f"case {cid}: missing string 'request'")
    goos = case.get("goos", "linux")
    goarch = case.get("goarch", "amd64")
    expected = case.get("expected", {})
    if expected is None:
        expected = {}
    if not isinstance(expected, dict):
        raise FixtureError(f"case {cid}: 'expected' must be an object")
    expect_error = case.get("expect_error")
    if expect_error is None and not any(
            k not in FORCED_KEYS for k in expected):
        raise FixtureError(
            f"case {cid}: 'expected' has no non-forced key; a positive case "
            f"must assert at least one source-selection result key beyond "
            f"patch_applied/evidence_class (use 'expect_error' for error cases)")

    detail = []
    with tempfile.TemporaryDirectory(prefix="selcheck-") as td:
        root = Path(td)
        try:
            _materialize(root, case.get("files"))
        except (ValueError, TypeError, OSError) as exc:
            # Input/materialization failures (bad raw_b64, unwritable target,
            # invalid path parts) are harness errors, not model outcomes.
            raise FixtureError(
                f"case {cid}: materialization failed: {exc}") from exc
        try:
            result = module.select_snapshot(root, request, goos, goarch)
        except Exception as exc:  # noqa: BLE001 - expectations may demand errors
            if expect_error is not None and _error_ok(exc, expect_error):
                return True, [f"raised expected {type(exc).__name__}: {exc}"]
            detail.append(f"unexpected exception {type(exc).__name__}: {exc}")
            return False, detail
    if expect_error is not None:
        status = result.get("status") if isinstance(result, dict) else type(result).__name__
        detail.append(
            f"expected error {expect_error!r} but select_snapshot returned "
            f"status={status!r}")
        return False, detail
    diffs = _compare(result, expected, root)
    if diffs:
        detail.extend(diffs)
        detail.append("actual result: " + json.dumps(result, sort_keys=True))
        return False, detail
    status = result.get("status", "<none>")
    base = _basename_of(result.get("base"))
    diff = _basename_of(result.get("selected_diff"))
    detail.append(
        f"status={status} base={base} selected_diff={diff} "
        f"selected_patch={result.get('selected_patch')}")
    return True, detail


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Developer fixture self-check for selection.py "
                    "(not a gate; source-model preview only).")
    ap.add_argument("--fixtures", action="append", default=None,
                    help="fixture JSON path; repeatable "
                         f"(default: {DEFAULT_FIXTURES})")
    ap.add_argument("--selection", default=str(SELECTION_PATH),
                    help="selection.py to import (default: sibling file)")
    args = ap.parse_args(argv)

    sel_path = Path(args.selection)
    if not sel_path.is_file():
        print(f"selfcheck: selection module not found: {sel_path}", file=sys.stderr)
        return 2
    try:
        module = _load_selection_module(sel_path)
    except FixtureError as exc:
        print(f"selfcheck: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - import failures are harness errors
        print(f"selfcheck: cannot import {sel_path}: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if not callable(getattr(module, "select_snapshot", None)):
        print(f"selfcheck: {sel_path} has no select_snapshot()", file=sys.stderr)
        return 2

    fixture_paths = ([Path(p) for p in args.fixtures]
                     if args.fixtures else [DEFAULT_FIXTURES])
    try:
        cases = []
        for fp in fixture_paths:
            cases.extend(_load_cases(fp))
    except FixtureError as exc:
        print(f"selfcheck: {exc}", file=sys.stderr)
        return 2
    if not cases:
        print("selfcheck: no fixture cases loaded", file=sys.stderr)
        return 2

    print(f"selfcheck: {sel_path.name} against "
          + ", ".join(str(p) for p in fixture_paths))
    npass = 0
    nfail = 0
    harness_failed = False
    for i, case in enumerate(cases):
        cid = case.get("id", f"<case-{i}>") if isinstance(case, dict) else f"<case-{i}>"
        try:
            ok, detail = run_case(module, case)
        except FixtureError as exc:
            # Schema violation is a harness failure (exit 2), not a case
            # mismatch (exit 1).
            harness_failed = True
            print(f"ERROR {cid}: fixture error: {exc}")
            continue
        tag = "PASS" if ok else "FAIL"
        first = detail[0] if detail else ""
        print(f"{tag} {cid}: {first}")
        for line in detail[1:]:
            print(f"     {line}")
        if ok:
            npass += 1
        else:
            nfail += 1
    print(f"selfcheck: {len(cases)} case(s), {npass} pass, {nfail} fail"
          + (", harness errors" if harness_failed else ""))
    if harness_failed:
        return 2
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
