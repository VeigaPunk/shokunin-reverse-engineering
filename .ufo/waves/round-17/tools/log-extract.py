#!/usr/bin/env python3
"""log-extract.py -- extract Go-analyzer diagnostics from a retained Ghidra
analyzeHeadless ghidra.log (round-17 contract, contract.md section
"W/tools/log-extract.py").

Usage:
    python3 -I log-extract.py --log GHIDRA_LOG
    python3 -I log-extract.py --selftest

Emits JSON (sort_keys=True, indent=2) on stdout:
    {log_path, log_sha256, language_compiler,
     go_lines: [{line, level, component, message, raw}],
     untested_versions, snapshot_labels, go_version_logged,
     missing_bootstrap, analyzer_errors, classification}

go_lines keeps every log record whose component is in the contract's named set
or starts with "Go"/"Golang". `line` is the 1-based line number; `raw` is the
verbatim line text (trailing whitespace preserved) so callers can re-anchor
citations without re-reading the log. The deduplicated list fields
(untested_versions, snapshot_labels, go_version_logged, analyzer_errors)
preserve first-occurrence order; per-event duplicates remain in go_lines.

Log line format observed (pilot ghidra.log files):
    YYYY-MM-DD HH:MM:SS LEVEL  (Component) message<trailing spaces>
Level is space-padded to 5 chars (INFO␣, WARN␣, DEBUG, ERROR). Continuation
lines (e.g. the AutoAnalysisManager timing table) carry no timestamp/level and
are not records.

Grounded in Base-src.zip (Ghidra 12.1.4):
  ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java
    :115  Msg.warn(GoRttiMapper.class, <BootstrapInfoException message>)
    :171  Msg.error(GoRttiMapper.class, "Untested Go version [%s]")
    :179-180 Msg.info(GoRttiMapper.class, "Using Go API snapshot for version %s")
    :358-360 "Missing Go bootstrap type info, unable to extract Go RTTI info."
  ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java
    :163  Msg.info(GoApiSnapshot.class, "Using Go API snapshot for %s")
  ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java
    :135  Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper")
    :139  Msg.info(this, "Go version %s")
  ghidra/app/plugin/core/analysis/GolangStringAnalyzer.java
    :105  Msg.error(this, "Go string analyzer error: unable to get GoRttiMapper")

Exit: 0 emitted, 2 could-not-evaluate (unreadable/bad input).
Python 3 stdlib only. No network. Read-only against the log file.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# Contract: component in this set, or component starting with "Go"/"Golang".
GO_COMPONENTS = {
    "GoRttiMapper",
    "GoApiSnapshot",
    "GolangSymbolAnalyzer",
    "GolangStringAnalyzer",
    "GoTypeManager",
    "GoFunctionFixup",
    "GoFunctionMultiReturn",
}

LINE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) ([A-Z]+) +\(([^)]*)\) (.*)$"
)
LANGUAGE_COMPILER_RE = re.compile(r"^Using Language/Compiler: (.*\S)\s*$")
UNTESTED_RE = re.compile(r"Untested Go version \[([^\]]+)\]")
SNAPSHOT_RE = re.compile(r"^Using Go API snapshot for (?:version )?(\S+)")
GO_VERSION_RE = re.compile(r"^Go version (\d\S*)")
MISSING_BOOTSTRAP_TEXT = "Missing Go bootstrap type info"
# Round-17 L1 integration (w1 ScoutGoApiSnapshotLog/ConnRequestedLabel/CriticC2Novelty):
# GoApiSnapshot.java:158-164 emits exactly one of WARN "Falling back from A to B for Go API
# snapshot" or INFO "Using Go API snapshot for A" once a base JSON exists; neither when the
# base is missing (:122-126). GoRttiMapper.java:179-180 echoes the REQUESTED version, so
# only the GoApiSnapshot component discriminates the selection route.
FALLBACK_RE = re.compile(r"^Falling back from (\S+) to (\S+) for Go API snapshot")
API_INFO_RE = re.compile(r"^Using Go API snapshot for (\S+)\s*$")
INVALID_VERSION_RE = re.compile(r"Invalid Go version string \[([^\]]*)\]")
READING_RE = re.compile(r"^Reading Go binary info: (\S+)")
LOG_FILE_RE = re.compile(r"Using log file: (\S+)")
IMPORT_RE = re.compile(r"IMPORTING: file://(\S+)")


class ExtractError(Exception):
    pass


def _is_go_component(component):
    # Round-17 integration: also keep Go fixup background commands
    # (PropagateRttiBackgroundCommand, FixClosureFuncArgsBackgroundCommand), which
    # the contract allowlist dropped (w1 CriticCapabilityPreclaim F7, ReviewPilotLogs P3).
    return (
        component in GO_COMPONENTS
        or component.startswith("Go")
        or component.startswith("Golang")
        or (component.endswith("BackgroundCommand")
            and ("Rtti" in component or "Closure" in component))
    )


def _dedupe(items):
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def parse_log(log_path):
    """Parse one ghidra.log and return the extraction dict.

    Raises ExtractError on unreadable input.
    """
    try:
        with open(log_path, "rb") as f:
            data = f.read()
    except OSError as e:
        raise ExtractError(f"cannot read log: {e}")

    text = data.decode("utf-8", errors="replace")

    language_compiler = None
    go_lines = []
    untested_versions = []
    snapshot_labels = []
    go_version_logged = []
    missing_bootstrap = False
    analyzer_errors = []
    api_info_labels = []
    fallbacks = []
    invalid_versions = []
    reading_count = 0
    mapper_errors = []
    log_file = None
    import_target = None

    for lineno, raw in enumerate(text.splitlines(), start=1):
        m = LINE_RE.match(raw)
        if not m:
            continue  # continuation line / non-record
        level = m.group(3)
        component = m.group(4)
        message = m.group(5).rstrip()

        if language_compiler is None:
            lm = LANGUAGE_COMPILER_RE.match(message)
            if lm:
                language_compiler = lm.group(1)
        if log_file is None:
            fm = LOG_FILE_RE.search(message)
            if fm:
                log_file = fm.group(1)
        if import_target is None:
            im = IMPORT_RE.search(message)
            if im:
                import_target = im.group(1)

        if not _is_go_component(component):
            continue

        go_lines.append(
            {
                "line": lineno,
                "level": level,
                "component": component,
                "message": message,
                "raw": raw,
            }
        )

        um = UNTESTED_RE.search(message)
        if um:
            untested_versions.append(um.group(1))

        sm = SNAPSHOT_RE.match(message)
        if sm:
            snapshot_labels.append(sm.group(1))

        gm = GO_VERSION_RE.match(message)
        if gm:
            go_version_logged.append(gm.group(1))

        if MISSING_BOOTSTRAP_TEXT in message:
            missing_bootstrap = True

        if level == "ERROR" and component.startswith("Golang"):
            analyzer_errors.append(message)

        if component == "GoApiSnapshot":
            fb = FALLBACK_RE.match(message)
            if fb:
                fallbacks.append({"from": fb.group(1), "to": fb.group(2)})
            ai = API_INFO_RE.match(message)
            if ai:
                api_info_labels.append(ai.group(1))
        iv = INVALID_VERSION_RE.search(message)
        if iv:
            invalid_versions.append(iv.group(1))
        if component == "GoRttiMapper":
            if READING_RE.match(message):
                reading_count += 1
            if level == "ERROR" and not UNTESTED_RE.search(message):
                mapper_errors.append(message)

    if missing_bootstrap:
        classification = "bootstrap_missing"
    elif snapshot_labels:
        classification = "snapshot_loaded"
    elif not go_lines:
        classification = "no_go_analysis"
    else:
        classification = "other"

    # Selection route observed from the GoApiSnapshot component only.
    if fallbacks and api_info_labels:
        snapshot_route = "conflict"
    elif fallbacks:
        snapshot_route = "fallback"
    elif api_info_labels:
        snapshot_route = "info"
    else:
        snapshot_route = "none"

    return {
        "log_path": os.path.abspath(log_path),
        "log_sha256": hashlib.sha256(data).hexdigest(),
        "log_bytes": len(data),
        "language_compiler": language_compiler,
        "log_file_line": log_file,
        "import_target": import_target,
        "go_lines": go_lines,
        "untested_versions": _dedupe(untested_versions),
        "snapshot_labels": _dedupe(snapshot_labels),
        "api_snapshot_info_labels": _dedupe(api_info_labels),
        "snapshot_fallbacks": [dict(t) for t in
                               _dedupe(tuple(sorted(f.items())) for f in fallbacks)],
        "snapshot_route": snapshot_route,
        "invalid_version_strings": _dedupe(invalid_versions),
        "bootstrap_attempts": reading_count,
        "mapper_errors": _dedupe(mapper_errors),
        "go_version_logged": _dedupe(go_version_logged),
        "missing_bootstrap": missing_bootstrap,
        "analyzer_errors": _dedupe(analyzer_errors),
        "classification": classification,
    }


def _selftest():
    """Build synthetic ghidra.log fixtures, assert extraction fields.

    Returns (True, case_count) on clean, (False, detail) on failure.
    """
    tmp = tempfile.mkdtemp(prefix="log-extract-selftest-")
    cases = 0
    try:

        def run_case(name, lines, checks):
            nonlocal cases
            cases += 1
            path = os.path.join(tmp, name + ".log")
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            try:
                result = parse_log(path)
            except ExtractError as e:
                return f"case {name}: parse failed: {e}"
            for field, expected in checks.items():
                if result.get(field) != expected:
                    return (
                        f"case {name}: {field}={result.get(field)!r} "
                        f"expected {expected!r}"
                    )
            return None

        shfmt_like = [
            "2026-10-20 10:17:29 INFO  (ProgramLoader) Using Language/Compiler: "
            "x86:LE:64:default:golang  ",
            "2026-10-20 10:17:30 INFO  (GoRttiMapper) Reading Go binary info: "
            "target-58f765638eed.bin  ",
            "2026-10-20 10:17:30 ERROR (GoRttiMapper) Untested Go version "
            "[1.27.0]  ",
            "2026-10-20 10:17:30 WARN  (GoRttiMapper) Missing Go bootstrap type "
            "info, unable to extract Go RTTI info.  ",
            "2026-10-20 10:17:30 ERROR (GolangSymbolAnalyzer) Go symbol analyzer "
            "error: unable to get GoRttiMapper  ",
            "2026-10-20 10:17:40 ERROR (GolangStringAnalyzer) Go string analyzer "
            "error: unable to get GoRttiMapper  ",
        ]
        err = run_case(
            "bootstrap_missing",
            shfmt_like,
            {
                "classification": "bootstrap_missing",
                "language_compiler": "x86:LE:64:default:golang",
                "untested_versions": ["1.27.0"],
                "snapshot_labels": [],
                "go_version_logged": [],
                "missing_bootstrap": True,
                "analyzer_errors": [
                    "Go symbol analyzer error: unable to get GoRttiMapper",
                    "Go string analyzer error: unable to get GoRttiMapper",
                ],
            },
        )
        if err:
            return False, err

        esb_like = [
            "2026-10-20 10:18:20 INFO  (GoRttiMapper) Reading Go binary info: "
            "target-bab29b2ca7a9.bin  ",
            "2026-10-20 10:18:20 INFO  (GoApiSnapshot) Using Go API snapshot for "
            "1.23.12  ",
            "2026-10-20 10:18:21 INFO  (GoRttiMapper) Using Go API snapshot for "
            "version 1.23.12  ",
            "2026-10-20 10:18:21 INFO  (GolangSymbolAnalyzer) Go version "
            "1.23.12  ",
            "2026-10-20 10:18:21 INFO  (GoTypeManager) Found 4881 Go types  ",
        ]
        err = run_case(
            "snapshot_loaded",
            esb_like,
            {
                "classification": "snapshot_loaded",
                "snapshot_labels": ["1.23.12"],
                "go_version_logged": ["1.23.12"],
                "untested_versions": [],
                "missing_bootstrap": False,
                "analyzer_errors": [],
            },
        )
        if err:
            return False, err

        err = run_case(
            "no_go_analysis",
            [
                "2026-10-20 10:00:00 INFO  (HeadlessAnalyzer) HEADLESS: "
                "execution starts  ",
                "2026-10-20 10:00:01 INFO  (ProgramLoader) Using "
                "Language/Compiler: x86:LE:64:default:gcc  ",
            ],
            {
                "classification": "no_go_analysis",
                "language_compiler": "x86:LE:64:default:gcc",
                "go_lines": [],
                "missing_bootstrap": False,
            },
        )
        if err:
            return False, err

        err = run_case(
            "other",
            [
                "2026-10-20 10:00:00 INFO  (GoRttiMapper) Reading Go binary "
                "info: t.bin  ",
                "2026-10-20 10:00:01 INFO  (GoTypeManager) Found 5 Go types  ",
            ],
            {
                "classification": "other",
                "missing_bootstrap": False,
                "snapshot_labels": [],
            },
        )
        if err:
            return False, err

        # Boundary: non-Go components stay out of go_lines; Golang* and Go fixup
        # background commands are in; GoRttiMapper ERROR is not an analyzer_error
        # (contract: Golang* only) but is a mapper_error.
        err = run_case(
            "component_boundary",
            [
                "2026-10-20 10:00:00 INFO  (PropagateRttiBackgroundCommand) Go "
                "RTTI callsite fixup info (total/updated/skipped): 9/9/0  ",
                "2026-10-20 10:00:01 INFO  (GolangDWARFFunctionFixup) fixed 1  ",
                "2026-10-20 10:00:02 ERROR (GoRttiMapper) Failed to read Go "
                "info  ",
                "    continuation line without timestamp  ",
                "2026-10-20 10:00:03 INFO  (AutoAnalysisManager) Go unrelated  ",
            ],
            {
                "classification": "other",
                "analyzer_errors": [],
                "mapper_errors": ["Failed to read Go info"],
                "snapshot_route": "none",
            },
        )
        if err:
            return False, err
        # verify boundary go_lines membership explicitly
        boundary = parse_log(os.path.join(tmp, "component_boundary.log"))
        comps = [g["component"] for g in boundary["go_lines"]]
        if comps != ["PropagateRttiBackgroundCommand", "GolangDWARFFunctionFixup",
                     "GoRttiMapper"]:
            return False, f"component_boundary go_lines components {comps!r}"
        if boundary["go_lines"][0]["line"] != 1:
            return False, "component_boundary line numbering wrong"

        # Route discrimination: fallback WARN vs exact INFO vs requested-label echo.
        err = run_case(
            "fallback_route",
            [
                "2026-10-20 10:00:00 INFO  (GoRttiMapper) Reading Go binary info: t.bin  ",
                "2026-10-20 10:00:00 WARN  (GoApiSnapshot) Falling back from 1.25.8 to "
                "1.25.0 for Go API snapshot  ",
                "2026-10-20 10:00:01 INFO  (GoRttiMapper) Using Go API snapshot for "
                "version 1.25.8  ",
            ],
            {
                "snapshot_route": "fallback",
                "snapshot_fallbacks": [{"from": "1.25.8", "to": "1.25.0"}],
                "api_snapshot_info_labels": [],
                "snapshot_labels": ["1.25.8"],
                "bootstrap_attempts": 1,
            },
        )
        if err:
            return False, err
        err = run_case(
            "invalid_version",
            [
                "2026-10-20 10:00:00 INFO  (GoRttiMapper) Reading Go binary info: t.bin  ",
                "2026-10-20 10:00:00 WARN  (GoRttiMapper) Invalid Go version string [devel]  ",
            ],
            {"invalid_version_strings": ["devel"], "snapshot_route": "none",
             "classification": "other"},
        )
        if err:
            return False, err

        # Exit-2 path: unreadable log via subprocess.
        cases += 1
        proc = subprocess.run(
            [
                sys.executable,
                "-I",
                os.path.abspath(__file__),
                "--log",
                os.path.join(tmp, "does-not-exist.log"),
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 2:
            return False, f"missing-file exit={proc.returncode} expected 2"

        return True, cases
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=(
            "Extract Go-analyzer diagnostics from a retained Ghidra "
            "ghidra.log. Emits JSON on stdout; exit 0 emitted, "
            "2 could-not-evaluate."
        )
    )
    ap.add_argument("--log", help="path to ghidra.log")
    ap.add_argument(
        "--selftest",
        action="store_true",
        help="run synthetic-fixture selftest and exit",
    )
    args = ap.parse_args(argv)

    if args.selftest:
        ok, info = _selftest()
        if ok:
            print(f"SELFTEST: CLEAN cases={info}")
            return 0
        print(f"SELFTEST: FAILED {info}")
        return 1

    if not args.log:
        print("error: --log is required (or --selftest)", file=sys.stderr)
        return 2

    try:
        result = parse_log(args.log)
    except ExtractError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
