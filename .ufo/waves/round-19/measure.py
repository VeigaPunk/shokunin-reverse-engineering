#!/usr/bin/env python3
"""Measure the three round-19 claims from immutable lane Git objects.

Usage  python3 -I -B .ufo/waves/round-19/measure.py <revision>
       python3 -I -B .ufo/waves/round-19/measure.py --selftest
       python3 -I -B .ufo/waves/round-19/measure.py --root DIR <revision>

C1  open routed round-18 defects, from
    `.ufo/waves/round-19/tools/routed-r18.py --root LANE --rev REV --strict`
    (its JSON `open_count`; `defects[]` with `open: true` gives the ids).
C2  stated-vs-live client pin mismatches, from
    `.ufo/waves/round-19/tools/province-pins.py --root LANE --rev REV`
    (its JSON `mismatch_count`), plus the `.ufo/gates/c1-census-v10.py`
    verdict/exit at `--root LANE` (its `verdict` field or `VERDICT:` line).
C3  `.ufo/waves/round-19/predictions/<label>.prediction.json` labels carrying
    a frozen 64-hex `carrier.sha256` (`labels_frozen`),
    `.ufo/waves/round-19/runs/<label>/compare.json` artifacts
    (`compare_jsons`, `matched` = its own recorded `all_match: true`), and
    `.ufo/waves/round-19/runs/<label>/compare.exit` files reading `0`
    (`compare_exit0`).

Only committed bytes at <revision> are read: the tree from `git ls-tree -r`,
blobs from `git show REV:path`. Every `*.py` in the revision's tools directory
is materialized to a tempfile.mkdtemp() copy (so a sibling such as `revpin.py`
resolves) and loaded with `importlib.util.spec_from_file_location`; the C1/C2
tools are invoked in-process with `--root <lane> --rev <resolved commit>`
(C1 additionally `--strict`), stdout/stderr captured. The census gate at
<revision> is materialized to the same temp root and run as a child process
with `--root <lane> --json`, because it is a whole instrument with its own
exit contract.

Anything absent or unusable at <revision> prints `null` plus a named reason
(`tool_absent_at_rev`, `gate_absent_at_rev`, `tool_output_not_json_object`,
`tool_rev_mismatch`, `compare_json_unparseable`, ...); the run never crashes on
it. A count of 0 is a measured zero, not an error.

Exit 0 after the report is emitted: per-claim `status` and the top-level
`could_not_evaluate` flag carry the outcome, because a measured zero and an
unevaluable claim must both print a report. Exit 2 when the revision cannot be
resolved or its tree cannot be listed. --selftest exits 0 on
`SELFTEST: CLEAN cases=N`, 1 on `SELFTEST: FAILED ... cases=N failures=[...]`.

Every number is a census, never a verdict: measure.py re-runs no defect check,
no pin comparison, no gate assertion and no Go analysis. No carrier binary is
executed and no semantic pass is claimed.
"""
import argparse
import contextlib
import importlib.util
import inspect
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

try:
    LANE = Path(__file__).resolve().parents[3]
except IndexError:  # not at LANE/.ufo/waves/round-19/measure.py
    LANE = None
ROUND = ".ufo/waves/round-19"
TOOLS_DIR = f"{ROUND}/tools"
TOOL_PATHS = {
    "C1": f"{TOOLS_DIR}/routed-r18.py",
    "C2": f"{TOOLS_DIR}/province-pins.py",
}
GATE_PATH = ".ufo/gates/c1-census-v10.py"
PRED_RE = re.compile(r"^" + re.escape(ROUND) + r"/predictions/([^/]+)\.prediction\.json$")
SUMS_PATH = f"{ROUND}/predictions/SHA256SUMS"
RUNS_RE = re.compile(r"^" + re.escape(ROUND) + r"/runs/([^/]+)/compare\.json$")
EXIT_RE = re.compile(r"^" + re.escape(ROUND) + r"/runs/([^/]+)/compare\.exit$")
SHA256_RE = re.compile(r"[0-9a-fA-F]{64}")
VERDICT_RE = re.compile(r"^VERDICT:\s*(PASS|FAIL)\b", re.MULTILINE)
CENSUS_TIMEOUT = 300

LIMITS = [
    "C1/C2 copy the tools' own contract JSON at the measured revision; measure.py "
    "re-runs no defect check and no pin comparison.",
    "C2's census facet is the `.ufo/gates/c1-census-v10.py` blob at REV run with "
    "`--root LANE`. The instrument reads the LANE working tree and the live host "
    "client configs, not REV's blobs, so its verdict is a live reading made by "
    "that revision's code, not a revision-scoped snapshot of text.",
    "C1/C2 require the tool's echoed `rev` to equal the resolved commit when it "
    "is present; a mismatch is could-not-evaluate because the count would not be "
    "at REV.",
    "C3 `labels_frozen` counts committed `predictions/<label>.prediction.json` "
    "blobs whose `carrier.sha256` is a 64-hex string. Freeze order (prediction "
    "commit before any carrier run commit) is not verified here; that is the "
    "decision rule's receipt-validate binding gate.",
    "C3 `matched` is the value each compare.json records for `all_match`, copied, "
    "not re-derived; measure.py re-reads no run log and re-compares no field.",
    "C3 `compare_exit0` reads `runs/<label>/compare.exit` verbatim as an integer; "
    "a missing or non-integer exit is named, never guessed.",
    "A count of 0 is a measured zero (no matching artifact at that revision), not "
    "an error.",
    "Tools are imported from a temporary copy of the revision's bytes and run "
    "in-process against the resolved commit; the worktree is never read and no "
    "carrier binary is executed.",
    "Import-time and call-time Python stdout/stderr are captured; a tool that "
    "writes straight to the process file descriptors (an uncaptured child) is "
    "outside that capture.",
]


def fail(reason, message):
    """Abort the measurement itself (exit 2), naming the reason on stderr."""
    print(f"measure.py: {reason}: {message}", file=sys.stderr)
    raise SystemExit(2)


def _git(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def _resolve(root, revision):
    proc = _git(root, "rev-parse", "--verify", "--quiet", f"{revision}^{{commit}}")
    if proc.returncode != 0:
        fail(
            "revision_unresolvable",
            f"cannot resolve {revision!r} in {root}: {proc.stderr.strip()[:200]}",
        )
    return proc.stdout.strip()


def _tree(root, revision):
    proc = _git(root, "ls-tree", "-r", "--name-only", revision)
    if proc.returncode != 0:
        fail(
            "revision_unreadable",
            f"cannot list the tree of {revision} in {root}: {proc.stderr.strip()[:200]}",
        )
    return {line for line in proc.stdout.splitlines() if line}


def _materialize(root, revision, paths):
    """Copy every tools/*.py blob at `revision` into a mkdtemp mirror.

    Returns (temp_root, tools_dir, failures). A blob that cannot be read is
    recorded in `failures` instead of aborting the other claim.
    """
    temp_root = Path(tempfile.mkdtemp(prefix="measure19-tools-"))
    dest = temp_root / TOOLS_DIR
    dest.mkdir(parents=True, exist_ok=True)
    failures = {}
    for rel in sorted(paths):
        if not rel.endswith(".py") or str(Path(rel).parent) != TOOLS_DIR:
            continue
        proc = _git(root, "show", f"{revision}:{rel}")
        if proc.returncode != 0:
            failures[rel] = "tool_blob_unreadable"
            continue
        (dest / Path(rel).name).write_text(proc.stdout, encoding="utf-8")
    return temp_root, dest, failures


@contextlib.contextmanager
def _import_scope(tools_dir):
    """Expose the temp tools dir for sibling imports, then purge what we loaded."""
    before_modules = set(sys.modules)
    before_path = list(sys.path)
    sys.path.insert(0, str(tools_dir))
    try:
        yield
    finally:
        sys.path[:] = before_path
        for name in set(sys.modules) - before_modules:
            module = sys.modules.get(name)
            filename = getattr(module, "__file__", None)
            if filename and str(Path(filename).resolve()).startswith(
                str(tools_dir.resolve())
            ):
                del sys.modules[name]


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"spec_from_file_location returned no loader for {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _tail(text, limit=400):
    stripped = (text or "").strip()
    return stripped[:limit] if stripped else None


def _parse_json(text):
    """Parse a tool's stdout: whole buffer first, then its last non-empty line."""
    stripped = (text or "").strip()
    if not stripped:
        return None
    lines = stripped.splitlines()
    for candidate in (stripped, lines[-1]):
        try:
            return json.loads(candidate)
        except (TypeError, ValueError):
            continue
    return None


def _invoke(module, argv):
    """Call the module's main/run callable, capturing stdout, stderr, and exit."""
    callable_ = None
    for name in ("main", "run"):
        candidate = getattr(module, name, None)
        if callable(candidate):
            callable_ = candidate
            break
    if callable_ is None:
        return {"exit": None, "stdout": "", "stderr": "", "error": "tool_has_no_callable_main"}

    try:
        accepts_argv = any(
            parameter.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.VAR_POSITIONAL,
            )
            for parameter in inspect.signature(callable_).parameters.values()
        )
    except (TypeError, ValueError):
        accepts_argv = True

    out, err = io.StringIO(), io.StringIO()
    saved_argv = list(sys.argv)
    try:
        with redirect_stdout(out), redirect_stderr(err):
            sys.argv = [getattr(module, "__name__", "tool")] + list(argv)
            try:
                code = callable_(list(argv)) if accepts_argv else callable_()
            except SystemExit as exc:
                code = exc.code
            except Exception as exc:  # noqa: BLE001 - reported, never swallowed
                return {
                    "exit": None,
                    "stdout": out.getvalue(),
                    "stderr": err.getvalue(),
                    "error": f"tool_raised: {type(exc).__name__}: {exc}"[:300],
                }
    finally:
        sys.argv = saved_argv

    if code is None:
        code = 0
    if not isinstance(code, int):
        code = 2
    return {
        "exit": code,
        "stdout": out.getvalue(),
        "stderr": err.getvalue(),
        "error": None,
    }


def _run_tool(rel, module_name, root, revision, tools_dir, extra=()):
    """Import one revision-bound tool and run its CLI.

    Returns (payload, exit_code, detail, stderr_tail); detail names the first
    structural failure (import, call, or JSON) and is None on a parsed dict.
    """
    out, err = io.StringIO(), io.StringIO()
    try:
        with redirect_stdout(out), redirect_stderr(err):
            module = _load_module(tools_dir / Path(rel).name, module_name)
    except (Exception, SystemExit) as exc:  # noqa: BLE001 - becomes a named finding
        return None, None, f"tool_import_error: {type(exc).__name__}: {exc}"[:300], _tail(
            err.getvalue()
        )
    invocation = _invoke(
        module, ["--root", str(root), "--rev", revision, *extra]
    )
    stderr_tail = _tail(invocation["stderr"])
    if invocation["error"]:
        return None, invocation["exit"], invocation["error"], stderr_tail
    payload = _parse_json(invocation["stdout"])
    if not isinstance(payload, dict):
        return None, invocation["exit"], "tool_output_not_json_object", stderr_tail
    return payload, invocation["exit"], None, stderr_tail


def _exit_detail(code):
    if code == 2:
        return "tool_exit_2"
    if isinstance(code, int):
        return f"tool_exit_{code}"
    return "tool_exit_unknown"


def _tool_rev(payload):
    value = payload.get("rev")
    return value if isinstance(value, str) else None


def _claim_c1(root, revision, paths, tools_dir, failures):
    rel = TOOL_PATHS["C1"]
    claim = {
        "tool_path": rel,
        "status": "could-not-evaluate",
        "reason": None,
        "tool_exit": None,
        "tool_rev": None,
        "tool_stderr": None,
        "open_count": None,
        "defects": None,
        "open_ids": None,
    }
    if rel not in paths:
        claim["reason"] = "tool_absent_at_rev"
        return claim
    if rel in failures:
        claim["reason"] = failures[rel]
        return claim
    payload, code, detail, stderr_tail = _run_tool(
        rel, "measure19_routed_r18", root, revision, tools_dir, extra=("--strict",)
    )
    claim["tool_exit"] = code
    claim["tool_stderr"] = stderr_tail
    if detail is None and code not in (0, 1):
        detail = _exit_detail(code)
    if detail is not None:
        claim["reason"] = detail
        claim["tool_output"] = payload
        return claim
    tool_rev = _tool_rev(payload)
    claim["tool_rev"] = tool_rev
    if tool_rev is not None and tool_rev != revision:
        claim["reason"] = "tool_rev_mismatch"
        claim["tool_output"] = payload
        return claim
    open_count = payload.get("open_count")
    if isinstance(open_count, bool) or not isinstance(open_count, int):
        claim["reason"] = "tool_output_missing_open_count"
        claim["tool_output"] = payload
        return claim
    defects = payload.get("defects")
    claim["status"] = "evaluated"
    claim["open_count"] = open_count
    claim["defects"] = defects if isinstance(defects, list) else None
    if isinstance(defects, list):
        claim["open_ids"] = sorted(
            item["id"]
            for item in defects
            if isinstance(item, dict)
            and item.get("open") is True
            and isinstance(item.get("id"), str)
        )
    return claim


def _run_census(root, revision, temp_root, paths):
    """Run the revision's c1-census-v10 instrument against the lane.

    The blob comes from <revision>; the instrument reads the lane worktree and
    the live host configs (its declared scope), which the report states.
    """
    claim = {
        "path": GATE_PATH,
        "verdict": None,
        "exit": None,
        "reason": None,
        "stderr": None,
        "source": None,
        "counts": None,
    }
    if GATE_PATH not in paths:
        claim["reason"] = "gate_absent_at_rev"
        return claim
    proc = _git(root, "show", f"{revision}:{GATE_PATH}")
    if proc.returncode != 0:
        claim["reason"] = "gate_blob_unreadable"
        return claim
    dest = temp_root / GATE_PATH
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(proc.stdout, encoding="utf-8")
    try:
        run = subprocess.run(
            [sys.executable, "-I", "-B", str(dest), "--root", str(root), "--json"],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            timeout=CENSUS_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        claim["reason"] = "c1_census_timeout"
        return claim
    except OSError as exc:  # noqa: BLE001 - becomes a named finding
        claim["reason"] = f"c1_census_spawn_error: {type(exc).__name__}"[:80]
        return claim
    claim["exit"] = run.returncode
    claim["stderr"] = _tail(run.stderr)
    payload = _parse_json(run.stdout)
    if isinstance(payload, dict) and payload.get("verdict") in ("PASS", "FAIL"):
        claim["verdict"] = payload["verdict"]
        claim["source"] = "json"
        counts = {}
        for name in ("stale", "ambiguous", "undeclared", "unresolved", "scope_errors"):
            value = payload.get(name)
            counts[name] = len(value) if isinstance(value, list) else None
        claim["counts"] = counts
    else:
        matches = VERDICT_RE.findall(run.stdout or "")
        if matches:
            claim["verdict"] = matches[-1]
            claim["source"] = "text"
        else:
            claim["reason"] = "c1_census_verdict_missing"
            return claim
    if run.returncode not in (0, 1):
        claim["reason"] = f"c1_census_exit_{run.returncode}"
    return claim


def _claim_c2(root, revision, paths, tools_dir, failures, temp_root):
    rel = TOOL_PATHS["C2"]
    claim = {
        "tool_path": rel,
        "status": "could-not-evaluate",
        "reason": None,
        "tool_exit": None,
        "tool_rev": None,
        "tool_stderr": None,
        "mismatch_count": None,
        "c1_census_path": GATE_PATH,
        "c1_census_verdict": None,
        "c1_census_exit": None,
        "c1_census_reason": None,
        "c1_census_stderr": None,
        "c1_census_source": None,
        "c1_census_counts": None,
    }
    census = _run_census(root, revision, temp_root, paths)
    claim["c1_census_verdict"] = census["verdict"]
    claim["c1_census_exit"] = census["exit"]
    claim["c1_census_reason"] = census["reason"]
    claim["c1_census_stderr"] = census["stderr"]
    claim["c1_census_source"] = census["source"]
    claim["c1_census_counts"] = census["counts"]

    if rel not in paths:
        claim["reason"] = "tool_absent_at_rev"
        return claim
    if rel in failures:
        claim["reason"] = failures[rel]
        return claim
    payload, code, detail, stderr_tail = _run_tool(
        rel, "measure19_province_pins", root, revision, tools_dir
    )
    claim["tool_exit"] = code
    claim["tool_stderr"] = stderr_tail
    if detail is None and code not in (0, 1):
        detail = _exit_detail(code)
    if detail is not None:
        claim["reason"] = detail
        claim["tool_output"] = payload
        return claim
    tool_rev = _tool_rev(payload)
    claim["tool_rev"] = tool_rev
    if tool_rev is not None and tool_rev != revision:
        claim["reason"] = "tool_rev_mismatch"
        claim["tool_output"] = payload
        return claim
    mismatch_count = payload.get("mismatch_count")
    if isinstance(mismatch_count, bool) or not isinstance(mismatch_count, int):
        claim["reason"] = "tool_output_missing_mismatch_count"
        claim["tool_output"] = payload
        return claim
    claim["mismatch_count"] = mismatch_count
    if census["reason"] is not None:
        claim["reason"] = census["reason"]
        return claim
    claim["status"] = "evaluated"
    return claim


def _read_blob(root, revision, rel):
    proc = _git(root, "show", f"{revision}:{rel}")
    if proc.returncode != 0:
        return None, "blob_unreadable"
    return proc.stdout, None


def _prediction_entries(root, revision, paths):
    entries = {}
    unparseable = []
    for rel in sorted(path for path in paths if PRED_RE.match(path)):
        label = PRED_RE.match(rel).group(1)
        text, error = _read_blob(root, revision, rel)
        payload = None
        if text is not None:
            try:
                payload = json.loads(text)
            except ValueError:
                payload = None
        if not isinstance(payload, dict):
            reason = "prediction_json_unparseable" if error is None else error
            unparseable.append({"path": rel, "reason": reason})
            entries[label] = {
                "path": rel,
                "frozen": False,
                "carrier_sha256": None,
                "reason": reason,
            }
            continue
        carrier = payload.get("carrier")
        sha = carrier.get("sha256") if isinstance(carrier, dict) else None
        frozen = isinstance(sha, str) and bool(SHA256_RE.fullmatch(sha))
        entries[label] = {
            "path": rel,
            "frozen": frozen,
            "carrier_sha256": sha if isinstance(sha, str) else None,
            "reason": None if frozen else "carrier_sha256_absent_or_not_64_hex",
        }
    return entries, unparseable


def _sums_labels(root, revision, paths):
    """Labels covered by predictions/SHA256SUMS, plus whether it exists."""
    if SUMS_PATH not in paths:
        return {"path": SUMS_PATH, "present": False, "labels": [], "unreadable": None}
    text, error = _read_blob(root, revision, SUMS_PATH)
    if text is None:
        return {"path": SUMS_PATH, "present": True, "labels": [], "unreadable": error}
    labels = set()
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        name = Path(parts[-1]).name
        match = PRED_RE.match(f"{ROUND}/predictions/{name}")
        if match:
            labels.add(match.group(1))
    return {
        "path": SUMS_PATH,
        "present": True,
        "labels": sorted(labels),
        "unreadable": None,
    }


def _exit_entries(root, revision, paths):
    entries = {}
    for rel in sorted(path for path in paths if EXIT_RE.match(path)):
        label = EXIT_RE.match(rel).group(1)
        text, error = _read_blob(root, revision, rel)
        value = None
        reason = error
        if text is not None:
            stripped = text.strip()
            try:
                value = int(stripped)
                reason = None
            except ValueError:
                reason = "compare_exit_not_integer"
        entries[label] = {"path": rel, "value": value, "reason": reason}
    return entries


def _keep_bool(payload, name):
    value = payload.get(name)
    return value if isinstance(value, bool) else None


def _claim_c3(root, revision, paths):
    predictions, prediction_unparseable = _prediction_entries(root, revision, paths)
    sums = _sums_labels(root, revision, paths)
    exits = _exit_entries(root, revision, paths)
    compare_unparseable = []
    runs = {}
    for rel in sorted(path for path in paths if RUNS_RE.match(path)):
        label = RUNS_RE.match(rel).group(1)
        text, error = _read_blob(root, revision, rel)
        payload = None
        if text is not None:
            try:
                payload = json.loads(text)
            except ValueError:
                payload = None
        if not isinstance(payload, dict):
            reason = "compare_json_unparseable" if error is None else "compare_json_unreadable"
            compare_unparseable.append({"path": rel, "reason": reason})
            runs[label] = {
                "path": rel,
                "all_match": None,
                "reason": reason,
            }
            continue
        runs[label] = {
            "path": rel,
            "all_match": _keep_bool(payload, "all_match"),
            "reason": None,
        }

    labels_frozen = sorted(label for label, entry in predictions.items() if entry["frozen"])
    unfrozen = sorted(
        label for label, entry in predictions.items() if not entry["frozen"]
    )
    compare_jsons = len(runs)
    compare_exit0 = sorted(
        label for label, entry in exits.items() if entry["value"] == 0
    )
    exit_missing = sorted(
        {label for label, entry in exits.items() if entry["value"] is None}
        | {label for label in runs if label not in exits}
    )
    matched = sorted(
        label for label, entry in runs.items() if entry["all_match"] is True
    )
    status = "evaluated"
    reason = None
    if prediction_unparseable:
        status = "could-not-evaluate"
        reason = prediction_unparseable[0]["reason"]
    elif compare_unparseable:
        status = "could-not-evaluate"
        reason = compare_unparseable[0]["reason"]
    return {
        "status": status,
        "reason": reason,
        "prediction_files": len(predictions),
        "labels_frozen": len(labels_frozen),
        "labels_frozen_ids": labels_frozen,
        "unfrozen_labels": unfrozen,
        "prediction_unparseable": prediction_unparseable,
        "sums": sums,
        "compare_jsons": compare_jsons,
        "compare_exit_files": len(exits),
        "compare_exit0": len(compare_exit0),
        "compare_exit0_ids": compare_exit0,
        "compare_exit_missing": exit_missing,
        "matched": len(matched),
        "matched_ids": matched,
        "labels": {
            label: {
                "prediction": predictions.get(label),
                "compare": runs.get(label),
                "compare_exit": exits.get(label),
            }
            for label in sorted(set(predictions) | set(runs) | set(exits))
        },
        "compare_unparseable": compare_unparseable,
    }


def measure(root, revision_requested):
    """Census the three claims over committed objects at `revision_requested`."""
    root = Path(root).resolve()
    revision = _resolve(root, revision_requested)
    paths = _tree(root, revision)
    temp_root, tools_dir, failures = _materialize(root, revision, paths)
    try:
        with _import_scope(tools_dir):
            c1 = _claim_c1(root, revision, paths, tools_dir, failures)
            c2 = _claim_c2(root, revision, paths, tools_dir, failures, temp_root)
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
    c3 = _claim_c3(root, revision, paths)

    return {
        "argv": list(sys.argv),
        "lane": str(root),
        "round": ROUND,
        "revision": revision,
        "revision_requested": revision_requested,
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "c1_open_count": c1["open_count"],
        "c2_mismatch_count": c2["mismatch_count"],
        "c2_c1_census_verdict": c2["c1_census_verdict"],
        "c2_c1_census_exit": c2["c1_census_exit"],
        "c3_labels_frozen": c3["labels_frozen"],
        "c3_compare_jsons": c3["compare_jsons"],
        "c3_compare_exit0": c3["compare_exit0"],
        "c3_matched": c3["matched"],
        "could_not_evaluate": any(
            claim["status"] != "evaluated" for claim in (c1, c2, c3)
        ),
        "limits": LIMITS,
    }


# --------------------------------------------------------------------------
# Selftest: fixture repositories under tempfile.mkdtemp(), removed afterwards.
# --------------------------------------------------------------------------

STUB_ROUTED_OK = '''#!/usr/bin/env python3
import argparse, json
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    payload = {
        "rev": args.rev,
        "defects": [
            {"id": "R18-A", "open": True, "checks": []},
            {"id": "R18-B", "open": True, "checks": []},
            {"id": "R18-C", "open": False, "checks": []},
        ],
        "open_count": 2,
        "strict": bool(args.strict),
    }
    print(json.dumps(payload))
    return 1 if args.strict and payload["open_count"] else 0
if __name__ == "__main__":
    raise SystemExit(main())
'''

STUB_ROUTED_NOT_JSON = '''#!/usr/bin/env python3
import argparse
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--strict", action="store_true")
    parser.parse_args(argv)
    print("SELFTEST not json")
    return 0
'''

STUB_ROUTED_EXIT2 = '''#!/usr/bin/env python3
import argparse, json
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    print(json.dumps({"rev": args.rev, "defects": [], "open_count": 2}))
    raise SystemExit(2)
'''

STUB_ROUTED_OTHER_REV = '''#!/usr/bin/env python3
import argparse, json
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--strict", action="store_true")
    parser.parse_args(argv)
    print(json.dumps({"rev": "f" * 40, "defects": [], "open_count": 0}))
    return 0
'''

STUB_ROUTED_IMPORT_EXIT = '''#!/usr/bin/env python3
import argparse, sys
parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
parser.add_argument("--rev", required=True)
parser.add_argument("--strict", action="store_true")
parser.parse_args()
print("{}")
sys.exit(2)
'''

STUB_ROUTED_IMPORT_NOISE = '''#!/usr/bin/env python3
import argparse, json, sys
print("IMPORT NOISE to stdout")
sys.stderr.write("IMPORT NOISE to stderr\\n")
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    print(json.dumps({"rev": args.rev, "defects": [], "open_count": 0}))
    return 0
'''

STUB_ROUTED_NO_MAIN = '''#!/usr/bin/env python3
def unrelated():
    return 0
'''

STUB_PROVINCE_OK = '''#!/usr/bin/env python3
import argparse, json
import revpin
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    args = parser.parse_args(argv)
    print(json.dumps({
        "rev": args.rev,
        "mismatch_count": revpin.MISMATCH_COUNT,
        "mismatches": [{"client": "devin"}, {"client": "omp"}],
    }))
    return 0
'''

STUB_PROVINCE_NOT_JSON = '''#!/usr/bin/env python3
import argparse
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    parser.parse_args(argv)
    print("province pins: 2 mismatches")
    return 0
'''

STUB_REVPIN = "MISMATCH_COUNT = 2\n"

STUB_GATE_JSON_FAIL = '''#!/usr/bin/env python3
import argparse, json
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    payload = {
        "live": {"devin": "6.7.0"},
        "verdict": "FAIL",
        "stale": [{"file": "PROVINCE.md"}],
        "ambiguous": [],
        "undeclared": [{"file": "SKILL.md"}],
        "unresolved": [],
        "scope_errors": [],
    }
    if args.json:
        print(json.dumps(payload))
    else:
        print("VERDICT: FAIL  (stale=1 ambiguous=0 undeclared=1 unresolved=0)")
    return 1
if __name__ == "__main__":
    raise SystemExit(main())
'''

STUB_GATE_JSON_PASS = '''#!/usr/bin/env python3
import argparse, json
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = {"verdict": "PASS", "stale": [], "ambiguous": [], "undeclared": [],
               "unresolved": [], "scope_errors": []}
    if args.json:
        print(json.dumps(payload))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
'''

STUB_GATE_TEXT_PASS = '''#!/usr/bin/env python3
import argparse
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--json", action="store_true")
    parser.parse_args(argv)
    print("live anchors (re-derived): {'devin': '6.7.0'}")
    print("VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
'''

STUB_GATE_EXIT2 = '''#!/usr/bin/env python3
import argparse
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--json", action="store_true")
    parser.parse_args(argv)
    print("ANCHOR-FAIL: {'devin': None}")
    return 2
if __name__ == "__main__":
    raise SystemExit(main())
'''

SHA = "a" * 64


def _pred(sha=SHA):
    carrier = {"path": "/fixture/carrier"}
    if sha is not None:
        carrier["sha256"] = sha
    return (
        json.dumps(
            {
                "carrier": carrier,
                "c3": {"h1_kind": "invalid_index", "emulator": "tools/swiss-misread.py"},
                "expected": {"snapshot_label": "1.25.0"},
            },
            indent=1,
            sort_keys=True,
        )
        + "\n"
    )


PRED_OK = _pred()
PRED_NO_SHA = _pred(sha=None)
PRED_SHORT_SHA = _pred(sha="deadbeef")
PRED_BROKEN = "{not json\n"

CMP_MATCH = (
    json.dumps(
        {
            "all_match": True,
            "fields": [
                {"field": "snapshot_label", "predicted": "1.25.0", "observed": "1.25.0", "match": True},
                {"field": "extra.invalid_index_reads", "predicted": [], "observed": [], "match": True},
            ],
            "observation": "o",
            "prediction": "p",
        },
        indent=1,
        sort_keys=True,
    )
    + "\n"
)
CMP_NOMATCH = (
    json.dumps(
        {"all_match": False, "fields": [{"field": "snapshot_route", "match": False}]},
        sort_keys=True,
    )
    + "\n"
)
CMP_BROKEN = "{not json\n"


def _fixture_git(root):
    env = dict(os.environ)
    env.update(
        {
            "GIT_AUTHOR_NAME": "measure-selftest",
            "GIT_AUTHOR_EMAIL": "selftest@invalid",
            "GIT_COMMITTER_NAME": "measure-selftest",
            "GIT_COMMITTER_EMAIL": "selftest@invalid",
        }
    )

    def run(*args):
        return subprocess.check_output(
            ["git", "-C", str(root), *args], text=True, encoding="utf-8", env=env
        )

    return run


def _commit(run, root, files, message):
    for rel, text in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    run("add", "-A")
    run("-c", "commit.gpgsign=false", "commit", "-q", "-m", message)
    return run("rev-parse", "HEAD").strip()


def _git_fixture(root, files):
    run = _fixture_git(root)
    run("init", "-q")
    return _commit(run, root, files, "fixture")


def _with_fixture(name, files, body, cases, failures):
    tmp = Path(tempfile.mkdtemp(prefix=f"measure-r19-selftest-{name}-"))
    try:
        revision = _git_fixture(tmp, files)
        body(tmp, revision)
    except (Exception, SystemExit) as exc:  # noqa: BLE001 - a crashed case is a failed case
        cases.append(1)
        failures.append(f"{name}_raised_{type(exc).__name__}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _base_tools():
    return {
        f"{TOOLS_DIR}/routed-r18.py": STUB_ROUTED_OK,
        f"{TOOLS_DIR}/province-pins.py": STUB_PROVINCE_OK,
        f"{TOOLS_DIR}/revpin.py": STUB_REVPIN,
        GATE_PATH: STUB_GATE_JSON_FAIL,
    }


def selftest():
    cases = []
    failures = []

    def check(name, condition):
        cases.append(1)
        if not condition:
            failures.append(name)

    base = {"corpus/README.md": "# fixture\n"}

    # A: nothing of round-19 committed -> named nulls, C3 a measured zero.
    def case_a(root, revision):
        out = measure(root, revision)
        check("a_c1_status", out["c1"]["status"] == "could-not-evaluate")
        check("a_c1_reason", out["c1"]["reason"] == "tool_absent_at_rev")
        check("a_c1_count", out["c1_open_count"] is None)
        check("a_c2_status", out["c2"]["status"] == "could-not-evaluate")
        check("a_c2_reason", out["c2"]["reason"] == "tool_absent_at_rev")
        check("a_c2_count", out["c2_mismatch_count"] is None)
        check("a_c2_gate_absent", out["c2"]["c1_census_reason"] == "gate_absent_at_rev")
        check("a_c2_verdict", out["c2_c1_census_verdict"] is None)
        check("a_c2_exit", out["c2_c1_census_exit"] is None)
        check("a_c3_status", out["c3"]["status"] == "evaluated")
        check("a_c3_predictions", out["c3"]["prediction_files"] == 0)
        check("a_c3_frozen", out["c3_labels_frozen"] == 0)
        check("a_c3_jsons", out["c3_compare_jsons"] == 0)
        check("a_c3_exit0", out["c3_compare_exit0"] == 0)
        check("a_c3_matched", out["c3_matched"] == 0)
        check("a_c3_sums_absent", out["c3"]["sums"]["present"] is False)
        check("a_flag", out["could_not_evaluate"] is True)
        check("a_revision", out["revision"] == revision)

    _with_fixture("a", base, case_a, cases, failures)

    # B: everything present -> counts, sibling import, frozen labels, gate red.
    def case_b(root, revision):
        out = measure(root, revision)
        check("b_c1_status", out["c1"]["status"] == "evaluated")
        check("b_c1_count", out["c1_open_count"] == 2)
        check("b_c1_open_ids", out["c1"]["open_ids"] == ["R18-A", "R18-B"])
        check("b_c1_defects", len(out["c1"]["defects"] or []) == 3)
        check("b_c1_exit", out["c1"]["tool_exit"] == 1)
        check("b_c1_rev", out["c1"]["tool_rev"] == revision)
        check("b_c2_status", out["c2"]["status"] == "evaluated")
        check("b_c2_count", out["c2_mismatch_count"] == 2)
        check("b_c2_rev", out["c2"]["tool_rev"] == revision)
        check("b_c2_sibling_import", out["c2"]["tool_stderr"] is None)
        check("b_census_verdict", out["c2_c1_census_verdict"] == "FAIL")
        check("b_census_exit", out["c2_c1_census_exit"] == 1)
        check("b_census_source", out["c2"]["c1_census_source"] == "json")
        check(
            "b_census_counts",
            out["c2"]["c1_census_counts"] == {
                "stale": 1,
                "ambiguous": 0,
                "undeclared": 1,
                "unresolved": 0,
                "scope_errors": 0,
            },
        )
        check("b_c3_status", out["c3"]["status"] == "evaluated")
        check("b_c3_predictions", out["c3"]["prediction_files"] == 2)
        check("b_c3_frozen", out["c3_labels_frozen"] == 2)
        check("b_c3_frozen_ids", out["c3"]["labels_frozen_ids"] == ["alpha", "beta"])
        check("b_c3_nested_excluded", "alpha-misread" not in out["c3"]["labels"])
        check("b_c3_jsons", out["c3_compare_jsons"] == 2)
        check("b_c3_exit_files", out["c3"]["compare_exit_files"] == 2)
        check("b_c3_exit0", out["c3_compare_exit0"] == 1)
        check("b_c3_exit0_ids", out["c3"]["compare_exit0_ids"] == ["alpha"])
        check("b_c3_matched", out["c3_matched"] == 1)
        check("b_c3_matched_ids", out["c3"]["matched_ids"] == ["alpha"])
        check("b_c3_sums", out["c3"]["sums"]["labels"] == ["alpha", "beta"])
        check("b_c3_label_match", out["c3"]["labels"]["alpha"]["compare"]["all_match"] is True)
        check("b_c3_label_nomatch", out["c3"]["labels"]["beta"]["compare"]["all_match"] is False)
        check("b_flag", out["could_not_evaluate"] is False)
        check("b_no_revpin_leak", "revpin" not in sys.modules)
        check(
            "b_no_tool_leak",
            not any(name.startswith("measure19_") for name in sys.modules),
        )

    b_files = dict(base)
    b_files.update(_base_tools())
    b_files[f"{ROUND}/predictions/alpha.prediction.json"] = PRED_OK
    b_files[f"{ROUND}/predictions/beta.prediction.json"] = PRED_OK
    b_files[f"{ROUND}/predictions/swiss-misread/alpha-misread.json"] = PRED_BROKEN
    b_files[SUMS_PATH] = (
        f"{SHA}  {ROUND}/predictions/alpha.prediction.json\n"
        f"{SHA}  {ROUND}/predictions/beta.prediction.json\n"
    )
    b_files[f"{ROUND}/runs/alpha/compare.json"] = CMP_MATCH
    b_files[f"{ROUND}/runs/alpha/compare.exit"] = "0\n"
    b_files[f"{ROUND}/runs/beta/compare.json"] = CMP_NOMATCH
    b_files[f"{ROUND}/runs/beta/compare.exit"] = "1\n"
    _with_fixture("b", b_files, case_b, cases, failures)

    # C: gate reads PASS, exit 0 -> census fields agree.
    def case_c(root, revision):
        out = measure(root, revision)
        check("c_census_verdict", out["c2_c1_census_verdict"] == "PASS")
        check("c_census_exit", out["c2_c1_census_exit"] == 0)
        check("c_c2_status", out["c2"]["status"] == "evaluated")

    c_files = dict(base)
    c_files.update(_base_tools())
    c_files[GATE_PATH] = STUB_GATE_JSON_PASS
    _with_fixture("c", c_files, case_c, cases, failures)

    # D: gate emits no verdict and exits 2 -> named, C2 unevaluable.
    def case_d(root, revision):
        out = measure(root, revision)
        check("d_census_verdict", out["c2_c1_census_verdict"] is None)
        check("d_census_exit", out["c2_c1_census_exit"] == 2)
        check("d_census_reason", out["c2"]["c1_census_reason"] == "c1_census_verdict_missing")
        check("d_c2_reason", out["c2"]["reason"] == "c1_census_verdict_missing")
        check("d_c2_status", out["c2"]["status"] == "could-not-evaluate")
        check("d_c2_count", out["c2_mismatch_count"] == 2)
        check("d_flag", out["could_not_evaluate"] is True)

    d_files = dict(base)
    d_files.update(_base_tools())
    d_files[GATE_PATH] = STUB_GATE_EXIT2
    _with_fixture("d", d_files, case_d, cases, failures)

    # E: gate without a JSON field but with a VERDICT line -> text fallback.
    def case_e(root, revision):
        out = measure(root, revision)
        check("e_census_verdict", out["c2_c1_census_verdict"] == "PASS")
        check("e_census_source", out["c2"]["c1_census_source"] == "text")
        check("e_census_exit", out["c2_c1_census_exit"] == 0)
        check("e_c2_status", out["c2"]["status"] == "evaluated")

    e_files = dict(base)
    e_files.update(_base_tools())
    e_files[GATE_PATH] = STUB_GATE_TEXT_PASS
    _with_fixture("e", e_files, case_e, cases, failures)

    # F (red): C1 tool prints no JSON -> named could-not-evaluate, C2 still runs.
    def case_f(root, revision):
        out = measure(root, revision)
        check("f_c1_status", out["c1"]["status"] == "could-not-evaluate")
        check("f_c1_reason", out["c1"]["reason"] == "tool_output_not_json_object")
        check("f_c1_count", out["c1_open_count"] is None)
        check("f_c2_ok", out["c2"]["status"] == "evaluated")
        check("f_flag", out["could_not_evaluate"] is True)

    f_files = dict(base)
    f_files.update(_base_tools())
    f_files[f"{TOOLS_DIR}/routed-r18.py"] = STUB_ROUTED_NOT_JSON
    _with_fixture("f", f_files, case_f, cases, failures)

    # G (red): C1 tool emits its JSON then exits 2 -> not evaluated, payload kept.
    def case_g(root, revision):
        out = measure(root, revision)
        check("g_c1_status", out["c1"]["status"] == "could-not-evaluate")
        check("g_c1_reason", out["c1"]["reason"] == "tool_exit_2")
        check("g_c1_exit", out["c1"]["tool_exit"] == 2)
        check("g_c1_count_none", out["c1_open_count"] is None)
        check("g_c1_payload", (out["c1"].get("tool_output") or {}).get("open_count") == 2)

    g_files = dict(base)
    g_files.update(_base_tools())
    g_files[f"{TOOLS_DIR}/routed-r18.py"] = STUB_ROUTED_EXIT2
    _with_fixture("g", g_files, case_g, cases, failures)

    # H (red): tool echoes another revision -> its count is not at REV.
    def case_h(root, revision):
        out = measure(root, revision)
        check("h_c1_status", out["c1"]["status"] == "could-not-evaluate")
        check("h_c1_reason", out["c1"]["reason"] == "tool_rev_mismatch")
        check("h_c1_tool_rev", out["c1"]["tool_rev"] == "f" * 40)
        check("h_c1_count_none", out["c1_open_count"] is None)
        check("h_flag", out["could_not_evaluate"] is True)

    h_files = dict(base)
    h_files.update(_base_tools())
    h_files[f"{TOOLS_DIR}/routed-r18.py"] = STUB_ROUTED_OTHER_REV
    _with_fixture("h", h_files, case_h, cases, failures)

    # I (red): one run's compare.json is not JSON -> C3 cannot be counted whole.
    def case_i(root, revision):
        out = measure(root, revision)
        check("i_c3_status", out["c3"]["status"] == "could-not-evaluate")
        check("i_c3_reason", out["c3"]["reason"] == "compare_json_unparseable")
        check("i_c3_jsons", out["c3"]["compare_jsons"] == 1)
        check("i_c3_unparseable", len(out["c3"]["compare_unparseable"]) == 1)
        check("i_c3_exit_independent", out["c3_compare_exit0"] == 1)
        check("i_flag", out["could_not_evaluate"] is True)

    i_files = dict(base)
    i_files[f"{ROUND}/runs/broken/compare.json"] = CMP_BROKEN
    i_files[f"{ROUND}/runs/broken/compare.exit"] = "0\n"
    _with_fixture("i", i_files, case_i, cases, failures)

    # J (red): an unresolvable revision aborts with exit 2 and a named reason.
    def case_j(root, _revision):
        err, code = io.StringIO(), None
        try:
            with redirect_stderr(err):
                main(["0" * 40, "--root", str(root)])
        except SystemExit as exc:
            code = exc.code
        check("j_exit", code == 2)
        check("j_reason", "revision_unresolvable" in err.getvalue())

    _with_fixture("j", base, case_j, cases, failures)

    # K: tools and gate committed later must not leak into an earlier revision.
    def case_k(root, revision):
        first = measure(root, revision)
        check("k_first_absent", first["c1"]["reason"] == "tool_absent_at_rev")
        check("k_first_gate_absent", first["c2"]["c1_census_reason"] == "gate_absent_at_rev")
        run = _fixture_git(root)
        later = _commit(run, root, _base_tools(), "add tools and gate")
        second = measure(root, later)
        check("k_second_evaluated", second["c1"]["status"] == "evaluated")
        check("k_second_count", second["c1_open_count"] == 2)
        check("k_second_gate", second["c2_c1_census_verdict"] == "FAIL")
        again = measure(root, revision)
        check("k_first_stable", again["c1"]["reason"] == "tool_absent_at_rev")
        check("k_first_gate_stable", again["c2"]["c1_census_reason"] == "gate_absent_at_rev")

    _with_fixture("k", base, case_k, cases, failures)

    # L: tool prints at import -> captured, never reaches measure's stdout,
    # and an import-time SystemExit is a named finding, not a crash.
    def case_l(root, revision):
        captured = io.StringIO()
        with redirect_stdout(captured):
            out = measure(root, revision)
        check("l_c1_evaluated", out["c1"]["status"] == "evaluated")
        check("l_c1_zero", out["c1_open_count"] == 0)
        check("l_stdout_clean", captured.getvalue() == "")
        run = _fixture_git(root)
        later = _commit(
            run,
            root,
            {f"{TOOLS_DIR}/routed-r18.py": STUB_ROUTED_IMPORT_EXIT},
            "import-time exit",
        )
        crashed = measure(root, later)
        check(
            "l_import_exit_reason",
            (crashed["c1"]["reason"] or "").startswith("tool_import_error: SystemExit"),
        )
        check("l_import_exit_status", crashed["c1"]["status"] == "could-not-evaluate")
        check("l_import_exit_c2", crashed["c2"]["status"] == "evaluated")

    l_files = dict(base)
    l_files.update(_base_tools())
    l_files[f"{TOOLS_DIR}/routed-r18.py"] = STUB_ROUTED_IMPORT_NOISE
    _with_fixture("l", l_files, case_l, cases, failures)

    # M: unfrozen/short-sha predictions and a missing compare.exit are named.
    def case_m(root, revision):
        out = measure(root, revision)
        check("m_frozen_count", out["c3"]["labels_frozen"] == 0)
        check("m_unfrozen", out["c3"]["unfrozen_labels"] == ["alpha", "beta"])
        check("m_prediction_files", out["c3"]["prediction_files"] == 2)
        check(
            "m_frozen_reason",
            out["c3"]["labels"]["alpha"]["prediction"]["reason"]
            == "carrier_sha256_absent_or_not_64_hex",
        )
        check("m_exit0", out["c3_compare_exit0"] == 1)
        check("m_exit_missing", out["c3"]["compare_exit_missing"] == ["beta"])
        check("m_status", out["c3"]["status"] == "evaluated")

    m_files = dict(base)
    m_files[f"{ROUND}/predictions/alpha.prediction.json"] = PRED_NO_SHA
    m_files[f"{ROUND}/predictions/beta.prediction.json"] = PRED_SHORT_SHA
    m_files[f"{ROUND}/runs/alpha/compare.json"] = CMP_MATCH
    m_files[f"{ROUND}/runs/alpha/compare.exit"] = "0\n"
    m_files[f"{ROUND}/runs/beta/compare.json"] = CMP_MATCH
    _with_fixture("m", m_files, case_m, cases, failures)

    # N (red): an unparseable frozen prediction is a named C3 finding.
    def case_n(root, revision):
        out = measure(root, revision)
        check("n_status", out["c3"]["status"] == "could-not-evaluate")
        check("n_reason", out["c3"]["reason"] == "prediction_json_unparseable")
        check("n_frozen", out["c3"]["labels_frozen"] == 1)
        check("n_unparseable", len(out["c3"]["prediction_unparseable"]) == 1)
        check("n_flag", out["could_not_evaluate"] is True)

    n_files = dict(base)
    n_files[f"{ROUND}/predictions/alpha.prediction.json"] = PRED_OK
    n_files[f"{ROUND}/predictions/beta.prediction.json"] = PRED_BROKEN
    _with_fixture("n", n_files, case_n, cases, failures)

    # O (red): C2 tool prints no JSON -> C2 unevaluable, census still reported.
    def case_o(root, revision):
        out = measure(root, revision)
        check("o_c2_status", out["c2"]["status"] == "could-not-evaluate")
        check("o_c2_reason", out["c2"]["reason"] == "tool_output_not_json_object")
        check("o_c2_count", out["c2_mismatch_count"] is None)
        check("o_census_verdict", out["c2_c1_census_verdict"] == "FAIL")
        check("o_census_exit", out["c2_c1_census_exit"] == 1)

    o_files = dict(base)
    o_files.update(_base_tools())
    o_files[f"{TOOLS_DIR}/province-pins.py"] = STUB_PROVINCE_NOT_JSON
    _with_fixture("o", o_files, case_o, cases, failures)

    # P: tool present but exposes no main/run callable.
    def case_p(root, revision):
        out = measure(root, revision)
        check("p_c1_reason", out["c1"]["reason"] == "tool_has_no_callable_main")
        check("p_c1_status", out["c1"]["status"] == "could-not-evaluate")

    p_files = dict(base)
    p_files[f"{TOOLS_DIR}/routed-r18.py"] = STUB_ROUTED_NO_MAIN
    _with_fixture("p", p_files, case_p, cases, failures)

    if failures:
        print(f"SELFTEST: FAILED cases={len(cases)} failures={failures}")
        raise SystemExit(1)
    print(f"SELFTEST: CLEAN cases={len(cases)}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Measure round-19 claims from Git objects at one revision."
    )
    parser.add_argument("revision", nargs="?", help="commit sha or ref to measure")
    parser.add_argument(
        "--root",
        default=None,
        help="lane work tree (default: three parents above this file)",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="build fixture repos under mkdtemp and check the census",
    )
    args = parser.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    if not args.revision:
        fail("usage", "measure.py <revision> | --selftest")
    if args.root is not None:
        root = Path(args.root)
    elif LANE is not None:
        root = LANE
    else:
        fail("lane_unresolvable", "pass --root DIR or run from LANE/.ufo/waves/round-19/")
    print(json.dumps(measure(root, args.revision), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
