#!/usr/bin/env python3
"""log-extract-attack.py -- adversarial ghidra.log fixtures fed to round-17
tools/log-extract.py (imported by path; sys.dont_write_bytecode set before
import). Author-side falsification seat (KaidokuR17.LogExtractFuzz).

Ground truth for expected emission, from installed Base-src.zip
(ghidra_12.1.4_PUBLIC):
  - GoApiSnapshot.java:158-164 emits exactly one of
    WARN  "Falling back from <goVer> to <patchVer> for Go API snapshot"
    INFO  "Using Go API snapshot for <goVer>"        (requested ver)
    and only when a base snapshot JSON exists (:122-126 gate in
    getApiSnapshotJsonFile).
  - GoRttiMapper.java:106  INFO "Reading Go binary info: <progname>"
    :115  WARN  <BootstrapInfoException text>     (relayed verbatim)
    :121  ERROR "Failed to read Go info"          (+ stack trace)
    :168  WARN  "Invalid Go version string [<raw buildinfo version>]"
    :171  ERROR "Untested Go version [<goVer>]"
    :179-180 INFO "Using Go API snapshot for version <snapshot.getVer()>"
    :359  (via :115) "Missing Go bootstrap type info, unable to extract
          Go RTTI info."
  - GolangSymbolAnalyzer.java:139 INFO "Go version <goVer>"
  - GoVer.toString() = "M.m.p" (patch -1 -> "M.m"); the raw build-info
    version string appears verbatim only inside "Invalid Go version
    string [...]".

Each case writes bytes to a fresh dir under /tmp, calls parse_log
directly, and reports observed fields plus a verdict. Verdicts:
  CLEAN    observed == documented expectation (control cases)
  DEFECT   output contradicts what the source-grounded log content means
  WEAK     brittle/absorptive behavior: plausible inputs silently dropped
           or attacker/shape-controlled bytes can forge extracted fields
Cases also run the tool CLI once for the exit-2/exit-0 contract where noted.
Python 3 stdlib only; fixtures only under /tmp; tool file never modified.
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True  # assigned import contract: no bytecode

TOOL = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/log-extract.py"
PILOT_SHFMT_LOG = (
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/"
    "pilot/shfmt-log/ghidra.log"
)

spec = importlib.util.spec_from_file_location("log_extract_target", TOOL)
le = importlib.util.module_from_spec(spec)
spec.loader.exec_module(le)

TS = "2026-10-20 10:47:46"
BASE = [
    f"{TS} INFO  (ProgramLoader) Using Language/Compiler: x86:LE:64:default:golang  ",
    f"{TS} INFO  (GoRttiMapper) Reading Go binary info: target-bab29b2ca7a9.bin  ",
    f"{TS} INFO  (GoApiSnapshot) Using Go API snapshot for 1.23.12  ",
    f"{TS} INFO  (GoRttiMapper) Using Go API snapshot for version 1.23.12  ",
    f"{TS} INFO  (GolangSymbolAnalyzer) Go version 1.23.12  ",
]
BASE_BYTES = ("\n".join(BASE) + "\n").encode()

RESULTS = []


def field_digest(r):
    return {
        "classification": r["classification"],
        "snapshot_route": r["snapshot_route"],
        "snapshot_labels": r["snapshot_labels"],
        "api_snapshot_info_labels": r["api_snapshot_info_labels"],
        "snapshot_fallbacks": r["snapshot_fallbacks"],
        "untested_versions": r["untested_versions"],
        "invalid_version_strings": r["invalid_version_strings"],
        "go_version_logged": r["go_version_logged"],
        "missing_bootstrap": r["missing_bootstrap"],
        "analyzer_errors": r["analyzer_errors"],
        "mapper_errors": r["mapper_errors"],
        "bootstrap_attempts": r["bootstrap_attempts"],
        "go_line_components": [g["component"] for g in r["go_lines"]],
        "language_compiler": r["language_compiler"],
        "log_file_line": r["log_file_line"],
        "import_target": r["import_target"],
    }


def run_case(tmp, name, content_bytes, expect, verdict, note,
             check_cli=False):
    path = os.path.join(tmp, name + ".log")
    with open(path, "wb") as f:
        f.write(content_bytes)
    out = {"case": name, "verdict": verdict, "note": note,
           "log_bytes": len(content_bytes)}
    try:
        r = le.parse_log(path)
    except Exception as e:  # ExtractError or crash: both reportable
        out["parse_exception"] = f"{type(e).__name__}: {e}"
        RESULTS.append(out)
        return out
    obs = field_digest(r)
    out["observed"] = obs
    diffs = {}
    for k, v in expect.items():
        if obs.get(k) != v:
            diffs[k] = {"expected": v, "observed": obs.get(k)}
    out["diffs"] = diffs
    # Cross-field coherence flags (tool-internal invariants per its own
    # :76-80 comment: only GoApiSnapshot discriminates route).
    flags = []
    if obs["classification"] == "snapshot_loaded" and obs["snapshot_route"] == "none":
        flags.append("snapshot_loaded_with_route_none")
    if obs["snapshot_route"] == "fallback" and not obs["snapshot_labels"]:
        flags.append("fallback_without_labels")
    if obs["snapshot_labels"] and obs["snapshot_route"] == "none":
        flags.append("labels_without_route")
    out["coherence_flags"] = flags
    if check_cli:
        p = subprocess.run(
            [sys.executable, "-B", "-I", TOOL, "--log", path],
            capture_output=True, text=True)
        out["cli_exit"] = p.returncode
        out["cli_stderr_tail"] = p.stderr.strip()[-200:]
    RESULTS.append(out)
    return out


def main():
    tmp = tempfile.mkdtemp(prefix="log-extract-attack-", dir="/tmp")
    try:
        base_expect = {
            "classification": "snapshot_loaded",
            "snapshot_route": "info",
            "snapshot_labels": ["1.23.12"],
            "api_snapshot_info_labels": ["1.23.12"],
            "go_version_logged": ["1.23.12"],
            "language_compiler": "x86:LE:64:default:golang",
            "bootstrap_attempts": 1,
        }

        # ---- controls ----------------------------------------------------
        run_case(tmp, "ctrl_baseline", BASE_BYTES, base_expect, "CLEAN",
                 "unmodified real-shaped snapshot_loaded log")

        run_case(tmp, "ctrl_crlf",
                 BASE_BYTES.replace(b"\n", b"\r\n"),
                 base_expect, "CLEAN",
                 "CRLF endings; splitlines handles them; go_lines raw keeps \\r?")

        run_case(tmp, "ctrl_stacktrace",
                 ("\n".join(BASE + [
                     f"{TS} ERROR (GoRttiMapper) Failed to read Go info  ",
                     "java.io.IOException: boom",
                     "\tat ghidra.app.util.bin.format.golang.rtti."
                     "GoApiSnapshot.get(GoApiSnapshot.java:104)",
                     "\tat ghidra.app.util.bin.format.golang.rtti."
                     "GoRttiMapper.getGoBinary(GoRttiMapper.java:175)",
                     "Caused by: java.io.IOException: Missing Go bootstrap "
                     "type info",
                 ]) + "\n").encode(),
                 dict(base_expect, missing_bootstrap=False,
                      mapper_errors=["Failed to read Go info"]),
                 "CLEAN",
                 "continuation/stack frames dropped even when one line "
                 "carries the bootstrap text: 'Caused by: ... Missing Go "
                 "bootstrap type info' does NOT set missing_bootstrap "
                 "(detection is record-line-only, tool :190)")

        # ---- silent-drop brittleness (WEAK) ------------------------------
        run_case(tmp, "tabs_after_level",
                 (f"{TS} INFO\t(GoApiSnapshot) Using Go API snapshot for "
                  "1.23.12\n" + "\n".join(BASE[1:2]) + "\n").encode(),
                 {"classification": "other",
                  "go_line_components": ["GoRttiMapper"],
                  "snapshot_route": "none", "snapshot_labels": []},
                 "WEAK",
                 "tab between LEVEL and (Component): LINE_RE :69 requires "
                 "literal spaces; the real INFO record is silently dropped "
                 "while the surviving Reading-record masks it as 'other'")

        run_case(tmp, "tabs_after_component",
                 (f"{TS} INFO  (GoApiSnapshot)\tUsing Go API snapshot for "
                  "1.23.12\n").encode(),
                 {"classification": "no_go_analysis",
                  "snapshot_route": "none", "snapshot_labels": []},
                 "WEAK",
                 "tab between (Component) and message: whole record dropped; "
                 "custom log4j layouts using \\t lose every line")

        run_case(tmp, "ms_timestamp",
                 ("\n".join(
                     l.replace("10:47:46 ", "10:47:46.123 ") for l in BASE)
                     + "\n").encode(),
                 {"classification": "no_go_analysis",
                  "language_compiler": None, "go_line_components": []},
                 "WEAK",
                 "millisecond timestamp '10:47:46.123' fails LINE_RE :69 "
                 "(\\d{2}:\\d{2}:\\d{2} then space): every record dropped; "
                 "a full Go run reports no_go_analysis")

        run_case(tmp, "bom",
                 b"\xef\xbb\xbf" + BASE_BYTES,
                 dict(base_expect, language_compiler=None),
                 "WEAK",
                 "UTF-8 BOM fuses to the first record: LINE_RE ^-anchor "
                 "fails, the ProgramLoader line carrying "
                 "language_compiler is dropped -> reported null on an "
                 "otherwise complete golang log")


        run_case(tmp, "paren_component",
                 (f"{TS} INFO  (GoRttiMapper (x86)) Reading Go binary info: "
                  "t.bin\n").encode(),
                 {"go_line_components": [], "classification": "no_go_analysis",
                  "bootstrap_attempts": 0},
                 "WEAK",
                 "component containing ')' breaks [^)]* at :69 -> dropped")

        # ---- record injection (DEFECT-class for evidence integrity) ------
        run_case(tmp, "non_utf8",
                 (f"{TS} ERROR (GoRttiMapper) Untested Go version "
                  "[1.27").encode() + b"\xff" +
                 (".0]  \n" +
                  f"{TS} WARN  (GoRttiMapper) note: caf").encode() +
                 b"\xe9\x80" + b" bytes  \n",
                 {"untested_versions": ["1.27�.0"],
                  "classification": "other"},
                 "WEAK",
                 "raw 0xff/0xe9 invalid bytes: errors='replace' at :127 "
                 "silently substitutes U+FFFD; corrupted version bytes "
                 "enter untested_versions with no flag -- compare.py "
                 "could mismatch/match on mangled data invisibly")

        run_case(tmp, "level_spoof",
                 ("\n".join([
                     f"{TS} WARN  (GoApiSnapshot) Using Go API snapshot "
                     "for 1.23.12  ",
                     f"{TS} INFO  (GoApiSnapshot) Falling back from "
                     "1.25.8 to 1.25.0 for Go API snapshot  ",
                 ]) + "\n").encode(),
                 {"snapshot_route": "conflict",
                  "api_snapshot_info_labels": ["1.23.12"],
                  "snapshot_fallbacks": [{"from": "1.25.8", "to": "1.25.0"}],
                  "snapshot_labels": ["1.23.12"]},
                 "WEAK",
                 "level never checked by FALLBACK_RE/API_INFO_RE "
                 ":196-202: a WARN INFO-shaped line lands in "
                 "api_snapshot_info_labels and an INFO WARN-shaped line "
                 "in snapshot_fallbacks -> 'conflict' on messages whose "
                 "levels contradict their shape")

        forged = (
            f"{TS} INFO  (GoRttiMapper) Reading Go binary info: "
            "target "          # real U+2028, embedded inside the name
            f"{TS} ERROR (GoRttiMapper) Untested Go version [9.9.9]  "
            "\n"
        ).encode()
        run_case(tmp, "u2028_injection", forged,
                 {"untested_versions": ["9.9.9"],
                  "classification": "other",
                  "go_line_components": ["GoRttiMapper", "GoRttiMapper"]},
                 "DEFECT",
                 "U+2028 inside program name: text.splitlines() :144 treats "
                 "it as a line break, so ONE physical log line yields TWO "
                 "records; the second is attacker-forged (a Go binary name "
                 "controls 'Reading Go binary info: <name>' and the raw "
                 "build-info version string controls 'Invalid Go version "
                 "string [<...>]'). Fields fabricated into the receipt: "
                 "untested_versions=['9.9.9'] -> compare.py would report "
                 "match:true for a predicted untested version the analyzer "
                 "never emitted")

        forged2 = (
            f"{TS} INFO  (GoRttiMapper) Reading Go binary info: x"
            f"{TS} WARN  (GoRttiMapper) Missing Go bootstrap type info, "
            "unable to extract Go RTTI info.\n"
        ).encode()
        run_case(tmp, "vtab_injection", forged2,
                 {"missing_bootstrap": True,
                  "classification": "bootstrap_missing"},
                 "DEFECT",
                 "\\x0b vertical tab in a message splits the same way; a "
                 "log with zero bootstrap failures extracts "
                 "missing_bootstrap=true -> classification bootstrap_missing")

        # ---- component lookalikes (DEFECT) -------------------------------
        run_case(tmp, "component_lookalikes",
                 ("\n".join([
                     f"{TS} INFO  (GoApiSnapshotX) Using Go API snapshot "
                     "for 9.9.9  ",
                     f"{TS} WARN  (NotGoApiSnapshot) Falling back from "
                     "1.1.1 to 1.1.0 for Go API snapshot  ",
                     f"{TS} INFO  (GovernorOfGo) Using Go API snapshot "
                     "for 7.7.7  ",
                     f"{TS} INFO  (GoatAnalyzer) nothing Go here  ",
                 ]) + "\n").encode(),
                 {"snapshot_labels": ["9.9.9", "7.7.7"],
                  "snapshot_route": "none",
                  "classification": "snapshot_loaded"},
                 "DEFECT",
                 "_is_go_component :97-103 accepts ANY startswith('Go'); "
                 "SNAPSHOT_RE :182-184 runs on every go_line while route "
                 ":196 gates on exact 'GoApiSnapshot'. Fake components "
                 "populate snapshot_labels and flip classification to "
                 "snapshot_loaded while snapshot_route stays 'none' -- the "
                 "tool's own :76-80 comment says only GoApiSnapshot can "
                 "discriminate, yet labels/classification ignore that. "
                 "NotGoApiSnapshot correctly excluded (control). "
                 "compare.py 'observed contains predicted' matches forged "
                 "labels.")

        run_case(tmp, "untested_injection",
                 (f"{TS} WARN  (GoatAnalyzer) Untested Go version [0.0.0]  "
                  "\n").encode(),
                 {"untested_versions": ["0.0.0"], "classification": "other"},
                 "DEFECT",
                 "UNTESTED_RE :178 is applied to every go_line, not just "
                 "GoRttiMapper (sole real emitter, GoRttiMapper.java:171); "
                 "any 'Go*' component forges untested_versions")

        # ---- INFO+WARN conflict / anchoring asymmetry --------------------
        run_case(tmp, "info_warn_conflict",
                 ("\n".join(BASE + [
                     f"{TS} WARN  (GoApiSnapshot) Falling back from "
                     "1.25.8 to 1.25.0 for Go API snapshot  ",
                 ]) + "\n").encode(),
                 dict(base_expect,
                      snapshot_route="conflict",
                      snapshot_fallbacks=[{"from": "1.25.8",
                                           "to": "1.25.0"}]),
                 "WEAK",
                 "real possible shape: one retained ghidra.log covering two "
                 "analysis sessions (different programs/versions) emits a "
                 "truthful INFO for program A and a truthful WARN for "
                 "program B; :222-229 collapses both to 'conflict' -- the "
                 "tool has no per-attempt scoping, so 'conflict' also "
                 "means 'two legitimate events'. Note the fallback's "
                 "requested '1.25.8' contributes no snapshot_label either "
                 "(WARN text never matches SNAPSHOT_RE).")

        run_case(tmp, "warn_extra_text",
                 ("\n".join([
                     f"{TS} WARN  (GoApiSnapshot) Falling back from "
                     "1.25.8 to 1.25.0 for Go API snapshot (attempt 2)  ",
                     f"{TS} INFO  (GoApiSnapshot) Using Go API snapshot "
                     "for 1.23.12 (patched)  ",
                 ]) + "\n").encode(),
                 {"snapshot_route": "fallback",
                  "snapshot_fallbacks": [{"from": "1.25.8", "to": "1.25.0"}],
                  "api_snapshot_info_labels": [],
                  "snapshot_labels": ["1.23.12"]},
                 "WEAK",
                 "anchoring asymmetry: FALLBACK_RE :81 has no trailing "
                 "anchor (extra text silently accepted into route) while "
                 "API_INFO_RE :82 requires \\s*$ (same suffix silently "
                 "drops the INFO from route but SNAPSHOT_RE still labels "
                 "it). Neither path flags the malformed line.")

        run_case(tmp, "api_info_version_phrasing",
                 (f"{TS} INFO  (GoApiSnapshot) Using Go API snapshot for "
                  "version 1.23.12  \n").encode(),
                 {"api_snapshot_info_labels": [],
                  "snapshot_labels": ["1.23.12"],
                  "snapshot_route": "none",
                  "classification": "snapshot_loaded"},
                 "DEFECT",
                 "API_INFO_RE :82 lacks the (?:version )? guard that "
                 "SNAPSHOT_RE :73 has AND demands \\s*$: the phrased INFO "
                 "fails entirely -> route 'none', while SNAPSHOT_RE still "
                 "labels '1.23.12' -> classification 'snapshot_loaded' "
                 "with route 'none' -- labels and route disagree about "
                 "the same line")

        run_case(tmp, "fallback_only_truncated",
                 ("\n".join(BASE[:2] + [
                     f"{TS} WARN  (GoApiSnapshot) Falling back from "
                     "1.25.8 to 1.25.0 for Go API snapshot  ",
                 ]) + "\n").encode(),
                 {"snapshot_route": "fallback",
                  "snapshot_labels": [],
                  "classification": "other"},
                 "DEFECT",
                 "log truncated between GoApiSnapshot.java:160 and the "
                 "GoRttiMapper.java:180 echo (poll-race window admitted by "
                 "carrier-run log_capture_limit, or CancelledException at "
                 ":183-185): a snapshot WAS loaded via fallback yet "
                 "classification='other' (not snapshot_loaded) and "
                 "snapshot_labels is EMPTY -- neither the requested "
                 "'1.25.8' nor the authoritative 'to' 1.25.0 enters any "
                 "label field, so compare.py reports mismatch against the "
                 "predicted requested label on a truthful retained log")


        run_case(tmp, "fallback_warn_only_noecho",
                 (f"{TS} WARN  (GoApiSnapshot) Falling back from 1.25.8 to "
                  "1.25.0 for Go API snapshot  \n").encode(),
                 {"snapshot_route": "fallback",
                  "snapshot_labels": [],
                  "classification": "other"},
                 "DEFECT",
                 "fallback WARN alone: classification 'other' though a "
                 "snapshot provably loaded; snapshot_labels empty so "
                 "compare.py reports mismatch against predicted requested "
                 "label on a truthful log")

        # ---- version string shapes ---------------------------------------
        run_case(tmp, "version_suffixes",
                 ("\n".join([
                     f"{TS} ERROR (GoRttiMapper) Untested Go version "
                     "[1.27.0-X:nodwarf5]  ",
                     f"{TS} WARN  (GoRttiMapper) Invalid Go version string "
                     "[devel go1.26-abc +dirty]  ",
                     f"{TS} INFO  (GolangSymbolAnalyzer) Go version "
                     "1.25rc1  ",
                     f"{TS} INFO  (GoApiSnapshot) Using Go API snapshot "
                     "for 1.25.0-beta.1  ",
                 ]) + "\n").encode(),
                 {"untested_versions": ["1.27.0-X:nodwarf5"],
                  "invalid_version_strings": ["devel go1.26-abc +dirty"],
                  "go_version_logged": ["1.25rc1"],
                  "snapshot_labels": ["1.25.0-beta.1"],
                  "snapshot_route": "info"},
                 "CLEAN",
                 "suffixed versions pass through verbatim; note "
                 "go_version_logged '1.25rc1' is verbatim raw, while "
                 "Untested/Invalid can never carry these shapes from real "
                 "emitters (GoVer.toString is M.m.p) -- pass-through "
                 "accepted uncritically")

        # ---- size / encoding ----------------------------------------------
        big = (f"{TS} WARN  (GoTypeManager) Failed to get subtype '" +
               "A" * (1024 * 1024 + 7) + "'  \n").encode()
        run_case(tmp, "line_gt_1mb", BASE_BYTES + big,
                 dict(base_expect,
                      go_line_components=None),  # components differ; skip
                 "CLEAN",
                 "1MB+ single message line: parsed, no truncation flag in "
                 "output (log_bytes records size but no per-line cap "
                 "exists -- a memory/latency observation, not a defect)",
                 )
        # fix expectation: just confirm parse survived & base fields held
        RESULTS[-1]["observed"].pop("go_line_components", None)
        RESULTS[-1]["diffs"].pop("go_line_components", None)

        # ---- vacuity / precedence -----------------------------------------
        run_case(tmp, "empty_file", b"",
                 {"classification": "no_go_analysis", "go_line_components": [],
                  "language_compiler": None, "log_file_line": None},
                 "DEFECT",
                 "empty log -> 'no_go_analysis': identical to a genuine "
                 "gcc-binary log. Poll-race or a zero-byte retained copy is "
                 "reported as 'Go analysis never ran' with no "
                 "truncation/emptiness signal")

        with open(PILOT_SHFMT_LOG, "rb") as f:
            pilot_lines = f.read().split(b"\n")
        header_only = b"\n".join(pilot_lines[:81]) + b"\n"  # before line 82
        run_case(tmp, "pilot_truncated_pre_go", header_only,
                 {"classification": "no_go_analysis",
                  "language_compiler": "x86:LE:64:default:golang"},
                 "DEFECT",
                 "REAL retained pilot log truncated at line 81 (one line "
                 "before the first GoRttiMapper record at :82): a go1.27 "
                 "bootstrap-failure run reports no_go_analysis. "
                 "carrier-run.py's own log_capture_limit admits 'lines "
                 "written after the final poll ... can be missing', so "
                 "this misclassification is reachable in-lane, and "
                 "language_compiler=golang makes it a false 'no Go' "
                 "verdict rather than 'truncated'.")

        run_case(tmp, "bootstrap_plus_snapshot",
                 ("\n".join(BASE + [
                     f"{TS} WARN  (GoRttiMapper) Missing Go bootstrap type "
                     "info, unable to extract Go RTTI info.  ",
                 ]) + "\n").encode(),
                 dict(base_expect, missing_bootstrap=True,
                      classification="bootstrap_missing"),
                 "WEAK",
                 "precedence :212-219: any bootstrap text anywhere "
                 "reclassifies the whole log to bootstrap_missing even "
                 "when snapshot evidence is present (two programs: one "
                 "mapped, one failed); route stays 'info' so evidence "
                 "survives but the headline field hides it")

        run_case(tmp, "bootstrap_substring",
                 (f"{TS} INFO  (GoRttiMapper) Retried after earlier "
                  "Missing Go bootstrap type info warning  \n").encode(),
                 {"missing_bootstrap": True,
                  "classification": "bootstrap_missing"},
                 "WEAK",
                 "unanchored substring at :190: ANY Go-prefixed component "
                 "message containing the phrase flips classification; "
                 "level and emitter unchecked (real emitter is a WARN of "
                 "the exception text via :115/:359)")

        run_case(tmp, "log_file_injection",
                 ("\n".join([
                     f"{TS} ERROR (Whatever) cleanup failed, see Using "
                     "log file: /tmp/attacker.log for details  ",
                     f"{TS} INFO  (Whatever) IMPORTING: file:///etc/passwd "
                     "extra words  ",
                 ]) + "\n").encode(),
                 {"log_file_line": "/tmp/attacker.log",
                  "import_target": "/etc/passwd",
                  "classification": "no_go_analysis"},
                 "DEFECT",
                 "LOG_FILE_RE/IMPORT_RE :156-163 are .search over EVERY "
                 "record's message (no emitter component gate, no anchor): "
                 "any component mentioning the phrase hijacks "
                 "log_file_line/import_target -- these feed provenance "
                 "fields in the receipt")

        run_case(tmp, "language_compiler_first_wins",
                 ("\n".join([
                     f"{TS} INFO  (ProgramLoader) Using Language/Compiler: "
                     "x86:LE:64:default:gcc  ",
                     f"{TS} INFO  (ProgramLoader) Using Language/Compiler: "
                     "x86:LE:64:default:golang  ",
                 ]) + BASE[1:] + "\n").encode()
                 if False else
                 ("\n".join([
                     f"{TS} INFO  (ProgramLoader) Using Language/Compiler: "
                     "x86:LE:64:default:gcc  ",
                     f"{TS} INFO  (ProgramLoader) Using Language/Compiler: "
                     "x86:LE:64:default:golang  ",
                 ] + BASE[1:]) + "\n").encode(),
                 dict(base_expect,
                      language_compiler="x86:LE:64:default:gcc"),
                 "WEAK",
                 "first-match-wins :152-155 with no component gate: a "
                 "multi-program session's earlier non-Go spec is reported "
                 "even though Go lines exist")

        # CLI spot-check: exit code contract on one DEFECT case
        run_case(tmp, "cli_exit_check", BASE_BYTES, base_expect, "CLEAN",
                 "CLI exit must be 0 with JSON on stdout", check_cli=True)

        print(json.dumps({"tool": TOOL, "tool_sha256": hashlib.sha256(
            open(TOOL, "rb").read()).hexdigest(),
            "cases": RESULTS}, indent=2, sort_keys=True))
    finally:
        # fixtures are evidence-bearing for the report; keep dir path in output
        print(f"FIXTURES_KEPT_AT {tmp}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main() or 0)
