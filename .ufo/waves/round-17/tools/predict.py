#!/usr/bin/env python3
"""predict.py -- predict Ghidra's Go RTTI snapshot decisions for one carrier.

Usage:
  python3 -I predict.py --go-version STR [--goos linux --goarch amd64] \
      --golang-root DIR
  python3 -I predict.py --selftest

--go-version is the raw `go_version` string REA `inspect-go-binary` reports
(build_info.go_version), e.g. "go1.27.2-X:nodwarf5", "go1.23.12", "".

Normalization replicates exactly what Ghidra does on that raw string:
  1. "go" prefix strip -- GoBuildInfo.java:488-489 (member
     ghidra/app/util/bin/format/golang/GoBuildInfo.java inside
     Ghidra/Features/Base/lib/Base-src.zip):
         if (versionString.startsWith("go"))
             versionString = versionString.substring(2);
  2. GoVer.parse(s, 0) -- GoVer.java:62-81 (member
     ghidra/app/util/bin/format/golang/GoVer.java): the regex
     "[^.0-9].*$" deletes the first non-digit/non-dot char and the rest of
     the line (line 64-65), the remainder is split on '.', at least two
     components are required (line 66), the third defaults to 0 via
     GoVer.parse (line 46-48, missingPatchValue=0; GoBuildInfo.getGoVer
     calls GoVer.parse at GoBuildInfo.java:237-238), and components must
     parse as Java ints (lines 69-80, NumberFormatException -> INVALID).
     "devel go1.24-abcdef" therefore normalizes to INVALID: it does not
     start with "go", and the 'd' at index 0 truncates the string to "".

Predictions made from the normalized GoVer:
  in_declared_range : GoRttiMapper.SUPPORTED_VERSIONS is
      GoVerRange.parse("1.15-1.25") (GoRttiMapper.java:79). Both endpoints
      are parsed with parseWildcardPatch (GoVerRange.java:47,52) giving
      patch -1; contains() (GoVerRange.java:83-87) uses GoVer.compareTo
      (GoVer.java:143-152) where a -1 patch wildcard compares equal, so
      the declared range is effectively 1.15.x .. 1.25.x.
  expected.untested_version : normalized string when outside the range,
      else null (GoRttiMapper.java:170-171 logs "Untested Go version [%s]").
  expected.snapshot_label   : the normalized requested version when a base
      snapshot file exists, else null. GoApiSnapshot.get passes the
      requested goVer into read() (GoApiSnapshot.java:111), so
      apiSnapshot.getVer() logged by GoRttiMapper.java:178-180 is the
      requested version even when a lower patch diff is selected.
  expected.missing_bootstrap: true iff r16 selection status is
      "missing_base" (GoApiSnapshot.get returns EMPTY when no patch-0
      base file exists, GoApiSnapshot.java:122-126,115).

The selection preview itself comes from r16 selection.py
(.ufo/waves/round-16/selection.py::select_snapshot), imported by file
path; that module models GoApiSnapshot.getApiSnapshotJsonFile/
getPatchVerDiffFile/read over the golang typeinfo directory.

Empty or unparseable --go-version exits 2 with a reason on stderr; the
tool never guesses. JSON on stdout (sort_keys=True, indent=2). Exit 0
emitted, 2 could-not-evaluate (bad/empty version, unreadable root,
selection failure). Python 3 stdlib only. Writes nothing outside the
tempfiles created by --selftest.
"""

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_SELECTION_PATH = Path(
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/"
    "round-16/selection.py"
)

# GoVerRange.parse("1.15-1.25") endpoints, GoRttiMapper.java:79 +
# GoVerRange.java:42-57: both sides get wildcard patch -1.
SUPPORTED_RANGE_TEXT = "1.15-1.25"
SUPPORTED_RANGE = ((1, 15, -1), (1, 25, -1))

_JAVA_INT_MAX = 2147483647

# GoVer.java:64-65 -- Objects.requireNonNullElse(s, "")
#   .replaceAll("[^.0-9].*$", "")
# Java replaceAll here is non-multiline: '.' does not match '\n' and '$'
# binds at end of input or before a final line terminator, exactly like
# Python's re.sub with this pattern.
_TRAILING_JUNK_RE = re.compile(r"[^.0-9].*$")


def _load_selection_module():
    """Import r16 selection.py by file path (sibling lane artifact)."""
    spec = importlib.util.spec_from_file_location(
        "r16_selection", str(_SELECTION_PATH))
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load %s" % (_SELECTION_PATH,))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _strip_go_prefix(s):
    """GoBuildInfo.parseBuildInfo, GoBuildInfo.java:488-489."""
    return s[2:] if s.startswith("go") else s


def gover_parse(s, missing_patch_value=0):
    """Replicates GoVer.parse(s, missingPatchValue), GoVer.java:62-81.

    Returns (major, minor, patch) or None for GoVer.INVALID. Java's
    String.split discards every trailing empty field, so "1.2." -> ["1",
    "2"]; "" itself splits to [""] (length 1) -> INVALID via line 66.
    Components are ASCII digits or "" only (the regex guarantees it);
    "" or a value outside int range is NumberFormatException -> INVALID.
    """
    cleaned = _TRAILING_JUNK_RE.sub("", s)  # GoVer.java:64-65
    parts = cleaned.split(".")
    while parts and parts[-1] == "":
        parts.pop()  # Java split() drops ALL trailing empty strings
    if len(parts) < 2:
        return None  # GoVer.java:66-68
    comps = []
    for piece in parts[:3]:  # parts[3:] are never read: GoVer.java:72-74
        if piece == "" or len(piece) > 10 or int(piece) > _JAVA_INT_MAX:
            return None  # NumberFormatException, GoVer.java:77-80
        comps.append(int(piece))
    patch = comps[2] if len(parts) > 2 else missing_patch_value
    return (comps[0], comps[1], patch)  # GoVer.java:75


def gover_is_invalid(ver):
    """GoVer.isInvalid, GoVer.java:105-107: major==0 && minor==0."""
    return ver[0] == 0 and ver[1] == 0


def gover_to_string(ver):
    """GoVer.toString, GoVer.java:154-159. predict never sees patch -1
    (GoVer.parse uses missingPatchValue=0), but handle it anyway."""
    if ver[2] != -1:
        return "%d.%d.%d" % ver
    return "%d.%d" % ver[:2]


def _gover_compare(a, b):
    """GoVer.compareTo, GoVer.java:143-152. A -1 patch on either side is
    a wildcard and compares equal (line 149)."""
    if a[0] != b[0]:
        return -1 if a[0] < b[0] else 1
    if a[1] != b[1]:
        return -1 if a[1] < b[1] else 1
    if a[2] == -1 or b[2] == -1:
        return 0
    if a[2] != b[2]:
        return -1 if a[2] < b[2] else 1
    return 0


def supported_versions_contains(ver):
    """GoVerRange.contains, GoVerRange.java:83-87, over the fixed
    SUPPORTED_VERSIONS range (GoRttiMapper.java:79). Neither endpoint is
    invalid or GoVer.ANY here, so the test reduces to start<=v and
    end>=v."""
    start, end = SUPPORTED_RANGE
    return _gover_compare(start, ver) <= 0 and _gover_compare(end, ver) >= 0


BASIS = [
    "Base-src.zip:ghidra/app/util/bin/format/golang/GoBuildInfo.java:488-489 "
    "(strip leading \"go\")",
    "Base-src.zip:ghidra/app/util/bin/format/golang/GoBuildInfo.java:237-238 "
    "(getGoVer = GoVer.parse(version))",
    "Base-src.zip:ghidra/app/util/bin/format/golang/GoVer.java:62-81 "
    "(parse: [^.0-9].*$ truncation, split, int components, patch default 0)",
    "Base-src.zip:ghidra/app/util/bin/format/golang/GoVer.java:105-107 "
    "(isInvalid: 0.0.x)",
    "Base-src.zip:ghidra/app/util/bin/format/golang/GoVer.java:143-159 "
    "(compareTo wildcard patch / toString)",
    "Base-src.zip:ghidra/app/util/bin/format/golang/GoVerRange.java:42-57,83-87 "
    "(parse \"1.15-1.25\" wildcard endpoints, contains)",
    "Base-src.zip:ghidra/app/util/bin/format/golang/rtti/"
    "GoRttiMapper.java:79,170-171 "
    "(SUPPORTED_VERSIONS \"1.15-1.25\", \"Untested Go version\" log)",
    "Base-src.zip:ghidra/app/util/bin/format/golang/rtti/"
    "GoRttiMapper.java:174-181 "
    "(snapshot get + \"Using Go API snapshot for version %s\")",
    "Base-src.zip:ghidra/app/util/bin/format/golang/rtti/"
    "GoApiSnapshot.java:111,122-126,148-166 "
    "(getVer is requested goVer; patch-0 base; EMPTY when no base)",
    "kaidoku-shokunin/.ufo/waves/round-16/selection.py "
    "(select_snapshot source-law preview)",
]


def predict(go_version_raw, goos, goarch, golang_root):
    """Build the full prediction dict for one raw go_version string."""
    stripped = _strip_go_prefix(go_version_raw)
    ver = gover_parse(stripped, 0)
    if ver is None or gover_is_invalid(ver):
        raise ValueError(
            "unparseable Go version %r (post-strip %r): GoVer.INVALID"
            % (go_version_raw, stripped))
    normalized = gover_to_string(ver)

    selection = _load_selection_module().select_snapshot(
        Path(golang_root), normalized, goos, goarch)

    in_range = supported_versions_contains(ver)
    has_base = selection["status"] != "missing_base"
    # Round-17 L1 integration: GoApiSnapshot.getPatchVerDiffFile (GoApiSnapshot.java:148-166)
    # logs WARN "Falling back from <req> to <selected> for Go API snapshot" when the selected
    # patch differs from the requested patch, else INFO "Using Go API snapshot for <req>";
    # nothing when the base JSON is missing (:122-126 return null before the diff search).
    if not has_base:
        route, fallback_to = "none", None
    else:
        sel_patch = selection.get("selected_patch")
        sel_patch = 0 if sel_patch is None else int(sel_patch)
        if sel_patch == ver[2]:
            route, fallback_to = "info", None
        else:
            route, fallback_to = "fallback", "%d.%d.%d" % (ver[0], ver[1], sel_patch)
    return {
        "input": go_version_raw,
        "normalized": normalized,
        "in_declared_range": in_range,
        "selection": selection,
        "expected": {
            # GoRttiMapper.java:170-171: logs the GoVer (toString form).
            "untested_version": None if in_range else normalized,
            # Contract: normalized requested label when a base exists,
            # matching apiSnapshot.getVer() at GoApiSnapshot.java:111.
            # NON-DISCRIMINATING for selection: it echoes the request.
            "snapshot_label": normalized if has_base else None,
            # Contract: true iff selection status is missing_base
            # (GoApiSnapshot.EMPTY, GoApiSnapshot.java:115,122-126). Source law is
            # stronger-conditioned (EMPTY and registerStructures IOException,
            # GoRttiMapper.java:351-361); missing_base is the practical proxy.
            "missing_bootstrap": not has_base,
            "snapshot_route": route,
            "fallback_to": fallback_to,
        },
        "basis": BASIS + ["GoApiSnapshot.java:148-166 (route: INFO exact/patch-0 vs WARN fallback)"],
    }


def _dump(obj):
    print(json.dumps(obj, sort_keys=True, indent=2))


def run(go_version_raw, goos, goarch, golang_root):
    """Emit the prediction JSON; return the process exit code."""
    try:
        result = predict(go_version_raw, goos, goarch, golang_root)
    except ValueError as e:
        # Bad/empty/unparseable version: exit 2, never a guess.
        print(json.dumps(
            {"error": str(e), "input": go_version_raw},
            sort_keys=True), file=sys.stderr)
        return 2
    except Exception as e:  # unreadable root / selection load failure
        print(json.dumps(
            {"error": "%s: %s" % (type(e).__name__, e),
             "input": go_version_raw},
            sort_keys=True), file=sys.stderr)
        return 2
    _dump(result)
    return 0


# ---------------------------------------------------------------------------
# --selftest: builds a fixture golang root under tempfile.mkdtemp(),
# exercises the real CLI (this script via sys.executable), then removes it.
# ---------------------------------------------------------------------------

def _selftest():
    tmp = tempfile.mkdtemp(prefix="predict-selftest-")
    script = Path(__file__).resolve()
    failures = []
    try:
        root = Path(tmp) / "golang"
        (root / "patchverdiffs").mkdir(parents=True)
        # Bases: 1.21 (in-range, no diffs), 1.98 (no diffs), 1.99 (diffs).
        for name in ("go1.21.0.json", "go1.98.0.json", "go1.99.0.json"):
            (root / name).write_text(
                json.dumps({"all": {"Types": {}}, "linux": None}),
                encoding="utf-8")
        (root / "patchverdiffs" / "go1.99.2.json.diff").write_text(
            json.dumps({"sections": []}), encoding="utf-8")

        def invoke(*argv):
            proc = subprocess.run(
                [sys.executable, "-I", str(script), *argv],
                capture_output=True, text=True)
            out = None
            if proc.stdout.strip():
                try:
                    out = json.loads(proc.stdout)
                except json.JSONDecodeError:
                    out = "<non-json stdout>"
            return proc.returncode, out, proc.stderr.strip()

        base_argv = ["--goos", "linux", "--goarch", "amd64",
                     "--golang-root", str(root)]
        # (name, extra argv, want_exit, dict of expected JSON fields or None)
        cases = [
            ("experiment_suffix",
             ["--go-version", "go1.99.2-X:nodwarf5"] + base_argv, 0,
             {"normalized": "1.99.2", "in_declared_range": False,
              "status": "exact_diff", "selected_patch": 2,
              "untested_version": "1.99.2", "snapshot_label": "1.99.2",
              "missing_bootstrap": False}),
            ("in_range_rc",
             ["--go-version", "go1.21rc2"] + base_argv, 0,
             {"normalized": "1.21.0", "in_declared_range": True,
              "status": "base_only", "selected_patch": 0,
              "untested_version": None, "snapshot_label": "1.21.0",
              "missing_bootstrap": False}),
            ("missing_base",
             ["--go-version", "go1.97.1"] + base_argv, 0,
             {"normalized": "1.97.1", "in_declared_range": False,
              "status": "missing_base",
              "untested_version": "1.97.1", "snapshot_label": None,
              "missing_bootstrap": True}),
            ("fallback_diff",
             ["--go-version", "go1.99.5"] + base_argv, 0,
             {"normalized": "1.99.5", "status": "fallback_diff",
              "selected_patch": 2, "snapshot_label": "1.99.5",
              "missing_bootstrap": False}),
            ("devel_string_invalid",
             ["--go-version", "devel go1.24-abcdef"] + base_argv, 2, None),
            ("empty_string_invalid",
             ["--go-version", ""] + base_argv, 2, None),
        ]
        for name, argv, want_exit, want in cases:
            code, out, err = invoke(*argv)
            if code != want_exit:
                failures.append(
                    "%s: exit %d != %d (stderr: %s)"
                    % (name, code, want_exit, err[:200]))
                continue
            if want is None:
                continue
            if not isinstance(out, dict):
                failures.append("%s: stdout not a JSON object" % name)
                continue
            got = {
                "normalized": out.get("normalized"),
                "in_declared_range": out.get("in_declared_range"),
                "status": (out.get("selection") or {}).get("status"),
                "selected_patch":
                    (out.get("selection") or {}).get("selected_patch"),
                "untested_version":
                    (out.get("expected") or {}).get("untested_version"),
                "snapshot_label":
                    (out.get("expected") or {}).get("snapshot_label"),
                "missing_bootstrap":
                    (out.get("expected") or {}).get("missing_bootstrap"),
            }
            for key, val in want.items():
                if got.get(key) != val:
                    failures.append(
                        "%s: %s %r != %r" % (name, key, got.get(key), val))

        # Pure-normalization cases (no fixture files needed).
        norm_cases = [
            ("go1.27.2-X:nodwarf5", "1.27.2"),
            ("go1.23.12", "1.23.12"),
            ("go1.21rc2", "1.21.0"),
            ("1.23.12", "1.23.12"),
            ("go1.16.05", "1.16.5"),       # Java parseInt accepts "05"
            ("go1.2", "1.2.0"),            # missing patch defaults to 0
            ("go1.2.3.9", "1.2.3"),        # parts[3:] unread
            ("devel go1.24-abcdef", None),
            ("", None),
            ("go0.0.7", None),             # INVALID sentinel 0.0.x
            ("go99999999999.1.0", None),   # component > Java int
        ]
        for raw, want in norm_cases:
            ver = gover_parse(_strip_go_prefix(raw), 0)
            got = None
            if ver is not None and not gover_is_invalid(ver):
                got = gover_to_string(ver)
            if got != want:
                failures.append(
                    "normalize(%r): %r != %r" % (raw, got, want))
        total = len(cases) + len(norm_cases)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("SELFTEST: FAILED " + "; ".join(failures))
        return 1
    print("SELFTEST: CLEAN cases=%d" % total)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Predict Ghidra Go RTTI snapshot selection, untested-"
                    "version and missing-bootstrap outcomes for one raw "
                    "go_version string, using the r16 selection preview. "
                    "Pure prediction: never runs Ghidra or the carrier.")
    parser.add_argument("--go-version",
                        help='raw REA build_info.go_version, e.g. '
                             '"go1.27.2-X:nodwarf5"')
    parser.add_argument("--goos", default="linux")
    parser.add_argument("--goarch", default="amd64")
    parser.add_argument("--golang-root",
                        help="directory containing go<M.m.p>.json base "
                             "snapshots and patchverdiffs/")
    parser.add_argument("--selftest", action="store_true",
                        help="run fixture-based self-test and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return _selftest()
    if args.go_version is None:
        parser.error("--go-version is required")
    if args.golang_root is None:
        parser.error("--golang-root is required")
    return run(args.go_version, args.goos, args.goarch, args.golang_root)


if __name__ == "__main__":
    sys.exit(main())
