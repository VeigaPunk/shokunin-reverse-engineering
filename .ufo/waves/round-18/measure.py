#!/usr/bin/env python3
"""Measure the three round-18 claims from immutable lane Git objects.

Usage  python3 -I -B .ufo/waves/round-18/measure.py <revision>
       python3 -I -B .ufo/waves/round-18/measure.py --selftest
       python3 -I -B .ufo/waves/round-18/measure.py --root DIR <revision>

C1  open routed r17 defects, from `.ufo/waves/round-18/tools/routed-defects.py`
    (its JSON `open_count`).
C2  live HEAD-as-revision sites, from
    `.ufo/waves/round-18/tools/head-rev-lint.py` (its JSON `live_count`).
C3  `.ufo/waves/round-18/runs/*/compare.json` artifacts whose `fields[]` carry
    an `extra.eof_reads` or `extra.analyzer_errors_empty` entry, plus each
    run's own recorded `all_match`.

Only committed bytes at <revision> are read: the tree from `git ls-tree -r`,
blobs from `git show REV:path`. The two C1/C2 tools are materialized to a
tempfile.mkdtemp() copy (together with every other `*.py` in that tools
directory, so a sibling such as `revpin.py` resolves) and loaded with
`importlib.util.spec_from_file_location` only when present at <revision>;
when absent, that claim reports `could-not-evaluate` with reason
`tool_absent_at_rev` rather than guessing. The tools run in-process with
`--root <lane> --rev <resolved commit>`, stdout/stderr captured.

Exit 0 after a complete report is emitted: per-claim `status` and the
top-level `could_not_evaluate` flag carry the outcome, because a measured
`open_count: 0` and an unevaluable claim must both print a report. Exit 2 when
the revision cannot be resolved or its tree cannot be listed. --selftest
exits 0 on `SELFTEST: CLEAN cases=N`, 1 on `SELFTEST: FAILED ...`.

Every number is a census, never a verdict. C1 counts the tool's own open
defects, C2 the lint's own live sites, C3 a field name in a retained
artifact. No carrier binary is executed and no semantic pass is claimed.
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
except IndexError:  # not at LANE/.ufo/waves/round-18/measure.py
    LANE = None
ROUND = ".ufo/waves/round-18"
TOOLS_DIR = f"{ROUND}/tools"
TOOL_PATHS = {
    "C1": f"{TOOLS_DIR}/routed-defects.py",
    "C2": f"{TOOLS_DIR}/head-rev-lint.py",
}
RUNS_RE = re.compile(r"^" + re.escape(ROUND) + r"/runs/([^/]+)/compare\.json$")
EXTRA_FIELDS = ("extra.eof_reads", "extra.analyzer_errors_empty")

LIMITS = [
    "C1/C2 copy the tools' own contract JSON at the measured revision; measure.py "
    "re-runs no defect check and no lint rule.",
    "C3 counts compare.json `fields[]` entries whose `field` is exactly one of the "
    "two names; it re-derives no all_match and re-reads no run log.",
    "C3 all_match is the value the artifact itself records, copied, not verified.",
    "C1/C2 require the tool's echoed `rev` to equal the resolved commit when it is "
    "present; a mismatch is could-not-evaluate because the count would not be at REV.",
    "A count of 0 is a measured zero (no matching artifact at that revision), not an error.",
    "Tools are imported from a temporary copy of the revision's bytes and run in-process "
    "against the resolved commit; the worktree is never read and no carrier binary is executed.",
    "Import-time and call-time Python stdout/stderr are captured; a tool that writes "
    "straight to the process file descriptors (an uncaptured child) is outside that capture.",
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
    temp_root = Path(tempfile.mkdtemp(prefix="measure18-tools-"))
    dest = temp_root / ROUND / "tools"
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


def _run_tool(rel, module_name, root, revision, tools_dir):
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
    invocation = _invoke(module, ["--root", str(root), "--rev", revision])
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
        rel, "measure18_routed_defects", root, revision, tools_dir
    )
    claim["tool_exit"] = code
    claim["tool_stderr"] = stderr_tail
    if detail is None and code not in (0, 1):
        detail = _exit_detail(code)
    if detail is not None:
        claim["reason"] = detail
        claim["tool_output"] = payload
        return claim
    tool_rev = payload.get("rev")
    claim["tool_rev"] = tool_rev if isinstance(tool_rev, str) else None
    if isinstance(tool_rev, str) and tool_rev != revision:
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


def _claim_c2(root, revision, paths, tools_dir, failures):
    rel = TOOL_PATHS["C2"]
    claim = {
        "tool_path": rel,
        "status": "could-not-evaluate",
        "reason": None,
        "tool_exit": None,
        "tool_rev": None,
        "tool_stderr": None,
        "live_count": None,
        "files_scanned": None,
        "fixture_count": None,
    }
    if rel not in paths:
        claim["reason"] = "tool_absent_at_rev"
        return claim
    if rel in failures:
        claim["reason"] = failures[rel]
        return claim
    payload, code, detail, stderr_tail = _run_tool(
        rel, "measure18_head_rev_lint", root, revision, tools_dir
    )
    claim["tool_exit"] = code
    claim["tool_stderr"] = stderr_tail
    if detail is None and code not in (0, 1):
        detail = _exit_detail(code)
    if detail is not None:
        claim["reason"] = detail
        claim["tool_output"] = payload
        return claim
    tool_rev = payload.get("rev")
    claim["tool_rev"] = tool_rev if isinstance(tool_rev, str) else None
    if isinstance(tool_rev, str) and tool_rev != revision:
        claim["reason"] = "tool_rev_mismatch"
        claim["tool_output"] = payload
        return claim
    live_count = payload.get("live_count")
    if isinstance(live_count, bool) or not isinstance(live_count, int):
        claim["reason"] = "tool_output_missing_live_count"
        claim["tool_output"] = payload
        return claim
    claim["status"] = "evaluated"
    claim["live_count"] = live_count
    for field in ("files_scanned", "fixture_count"):
        value = payload.get(field)
        claim[field] = value if isinstance(value, int) and not isinstance(value, bool) else None
    return claim


def _extra_fields(payload):
    """Names among EXTRA_FIELDS that this compare.json compares.

    Only compare.py's field list counts: an entry in `fields` whose `field`
    is exactly one of EXTRA_FIELDS. A different shape is left uncounted
    rather than inferred, so a producer mismatch surfaces as a low count.
    """
    found = set()
    fields = payload.get("fields")
    if isinstance(fields, list):
        for item in fields:
            if isinstance(item, dict) and item.get("field") in EXTRA_FIELDS:
                found.add(item["field"])
    return sorted(found)


def _claim_c3(root, revision, paths):
    labels = {}
    unparseable = []
    compare_jsons = 0
    with_extra = 0
    field_counts = {name: 0 for name in EXTRA_FIELDS}
    for rel in sorted(path for path in paths if RUNS_RE.match(path)):
        label = RUNS_RE.match(rel).group(1)
        compare_jsons += 1
        proc = _git(root, "show", f"{revision}:{rel}")
        payload = None
        if proc.returncode == 0:
            try:
                payload = json.loads(proc.stdout)
            except ValueError:
                payload = None
        if not isinstance(payload, dict):
            unparseable.append(
                {
                    "path": rel,
                    "reason": "compare_json_unparseable"
                    if proc.returncode == 0
                    else "compare_json_unreadable",
                }
            )
            labels[label] = {
                "path": rel,
                "all_match": None,
                "carries_extra": False,
                "extra_fields": [],
            }
            continue
        names = _extra_fields(payload)
        if names:
            with_extra += 1
            for name in names:
                field_counts[name] += 1
        all_match = payload.get("all_match")
        labels[label] = {
            "path": rel,
            "all_match": all_match if isinstance(all_match, bool) else None,
            "carries_extra": bool(names),
            "extra_fields": names,
        }
    status = "evaluated"
    reason = None
    if unparseable:
        status = "could-not-evaluate"
        reason = unparseable[0]["reason"]
    return {
        "status": status,
        "reason": reason,
        "compare_jsons": compare_jsons,
        "compare_jsons_with_extra": with_extra,
        "extra_field_counts": field_counts,
        "labels": labels,
        "unparseable": unparseable,
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
            c2 = _claim_c2(root, revision, paths, tools_dir, failures)
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
        "c2_live_count": c2["live_count"],
        "c3_compare_jsons": c3["compare_jsons"],
        "c3_compare_jsons_with_extra": c3["compare_jsons_with_extra"],
        "c3_all_match_by_label": {
            label: entry["all_match"] for label, entry in c3["labels"].items()
        },
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
            {"id": "R17-A", "open": True, "checks": []},
            {"id": "R17-B", "open": True, "checks": []},
            {"id": "R17-C", "open": False, "checks": []},
        ],
        "open_count": 2,
    }
    print(json.dumps(payload))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
'''

STUB_ROUTED_NOT_JSON = '''#!/usr/bin/env python3
import argparse
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
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
    parser.parse_args(argv)
    print(json.dumps({"rev": "f" * 40, "defects": [], "open_count": 0}))
    return 0
'''

STUB_ROUTED_IMPORT_EXIT = '''#!/usr/bin/env python3
import argparse, sys
parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
parser.add_argument("--rev", required=True)
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
    args = parser.parse_args(argv)
    print(json.dumps({"rev": args.rev, "defects": [], "open_count": 0}))
    return 0
'''

STUB_ROUTED_NO_MAIN = '''#!/usr/bin/env python3
def unrelated():
    return 0
'''

STUB_HEAD_OK = '''#!/usr/bin/env python3
import argparse, json, subprocess
import revpin
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    listing = subprocess.check_output(
        ["git", "-C", args.root, "ls-tree", "-r", "--name-only", args.rev],
        text=True,
    )
    payload = {
        "rev": args.rev,
        "files_scanned": len(listing.splitlines()),
        "sites": [],
        "live_count": revpin.LIVE_COUNT,
        "fixture_count": 2,
    }
    print(json.dumps(payload))
    return 0
'''

STUB_REVPIN = "LIVE_COUNT = 3\n"

CMP_EXTRA = (
    json.dumps(
        {
            "all_match": True,
            "fields": [
                {"field": "snapshot_label", "predicted": "a", "observed": "a", "match": True},
                {
                    "field": "extra.eof_reads",
                    "predicted": [[17645861, 111938854]],
                    "observed": [[17645861, 111938854]],
                    "match": True,
                },
            ],
            "observation": "o",
            "prediction": "p",
        },
        indent=1,
        sort_keys=True,
    )
    + "\n"
)
CMP_PLAIN = (
    json.dumps(
        {"all_match": False, "fields": [{"field": "snapshot_label", "match": False}]},
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
    tmp = Path(tempfile.mkdtemp(prefix=f"measure-r18-selftest-{name}-"))
    try:
        revision = _git_fixture(tmp, files)
        body(tmp, revision)
    except (Exception, SystemExit) as exc:  # noqa: BLE001 - a crashed case is a failed case
        cases.append(1)
        failures.append(f"{name}_raised_{type(exc).__name__}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def selftest():
    cases = []
    failures = []

    def check(name, condition):
        cases.append(1)
        if not condition:
            failures.append(name)

    base = {"corpus/README.md": "# fixture\n"}

    # A: nothing of round-18 committed -> both tools absent, C3 a measured zero.
    def case_a(root, revision):
        out = measure(root, revision)
        check("a_c1_status", out["c1"]["status"] == "could-not-evaluate")
        check("a_c1_reason", out["c1"]["reason"] == "tool_absent_at_rev")
        check("a_c1_count", out["c1_open_count"] is None)
        check("a_c2_reason", out["c2"]["reason"] == "tool_absent_at_rev")
        check("a_c2_count", out["c2_live_count"] is None)
        check("a_c3_status", out["c3"]["status"] == "evaluated")
        check("a_c3_zero", out["c3_compare_jsons"] == 0)
        check("a_c3_extra_zero", out["c3_compare_jsons_with_extra"] == 0)
        check("a_flag", out["could_not_evaluate"] is True)
        check("a_revision", out["revision"] == revision)

    _with_fixture("a", base, case_a, cases, failures)

    # B: both tools plus revpin and two runs -> counts, sibling import, labels.
    def case_b(root, revision):
        out = measure(root, revision)
        check("b_c1_status", out["c1"]["status"] == "evaluated")
        check("b_c1_count", out["c1_open_count"] == 2)
        check("b_c1_open_ids", out["c1"]["open_ids"] == ["R17-A", "R17-B"])
        check("b_c1_defects", len(out["c1"]["defects"] or []) == 3)
        check("b_c1_exit", out["c1"]["tool_exit"] == 0)
        check("b_c1_rev", out["c1"]["tool_rev"] == revision)
        check("b_c2_status", out["c2"]["status"] == "evaluated")
        check("b_c2_rev", out["c2"]["tool_rev"] == revision)
        check("b_c2_sibling_import", out["c2_live_count"] == 3)
        check("b_c2_files", out["c2"]["files_scanned"] >= 6)
        check("b_c2_fixtures", out["c2"]["fixture_count"] == 2)
        check("b_c3_count", out["c3_compare_jsons"] == 2)
        check("b_c3_extra", out["c3_compare_jsons_with_extra"] == 1)
        swiss = out["c3"]["labels"]["s1246-swiss-methods"]
        plain = out["c3"]["labels"]["pro-notesmd-cli"]
        check("b_label_extra", swiss["carries_extra"] is True)
        check("b_label_extra_name", swiss["extra_fields"] == ["extra.eof_reads"])
        check("b_label_all_match", swiss["all_match"] is True)
        check("b_label_plain", plain["carries_extra"] is False)
        check("b_label_plain_match", plain["all_match"] is False)
        check("b_flat_map", out["c3_all_match_by_label"] == {
            "pro-notesmd-cli": False,
            "s1246-swiss-methods": True,
        })
        check("b_field_counts", out["c3"]["extra_field_counts"] == {
            "extra.eof_reads": 1,
            "extra.analyzer_errors_empty": 0,
        })
        check("b_flag", out["could_not_evaluate"] is False)
        check("b_no_revpin_leak", "revpin" not in sys.modules)
        check(
            "b_no_tool_leak",
            not any(name.startswith("measure18_") for name in sys.modules),
        )

    b_files = dict(base)
    b_files[f"{TOOLS_DIR}/routed-defects.py"] = STUB_ROUTED_OK
    b_files[f"{TOOLS_DIR}/head-rev-lint.py"] = STUB_HEAD_OK
    b_files[f"{TOOLS_DIR}/revpin.py"] = STUB_REVPIN
    b_files[f"{ROUND}/runs/s1246-swiss-methods/compare.json"] = CMP_EXTRA
    b_files[f"{ROUND}/runs/pro-notesmd-cli/compare.json"] = CMP_PLAIN
    _with_fixture("b", b_files, case_b, cases, failures)

    # C (red): tool present but prints no JSON -> named could-not-evaluate.
    def case_c(root, revision):
        out = measure(root, revision)
        check("c_c1_status", out["c1"]["status"] == "could-not-evaluate")
        check("c_c1_reason", out["c1"]["reason"] == "tool_output_not_json_object")
        check("c_c1_exit", out["c1"]["tool_exit"] == 0)
        check("c_c2_ok", out["c2"]["status"] == "evaluated")
        check("c_flag", out["could_not_evaluate"] is True)

    c_files = dict(base)
    c_files[f"{TOOLS_DIR}/routed-defects.py"] = STUB_ROUTED_NOT_JSON
    c_files[f"{TOOLS_DIR}/head-rev-lint.py"] = STUB_HEAD_OK
    c_files[f"{TOOLS_DIR}/revpin.py"] = STUB_REVPIN
    _with_fixture("c", c_files, case_c, cases, failures)

    # D (red): tool emits its JSON then exits 2 -> not evaluated, payload kept.
    def case_d(root, revision):
        out = measure(root, revision)
        check("d_c1_status", out["c1"]["status"] == "could-not-evaluate")
        check("d_c1_reason", out["c1"]["reason"] == "tool_exit_2")
        check("d_c1_exit", out["c1"]["tool_exit"] == 2)
        check("d_c1_count_none", out["c1_open_count"] is None)
        check("d_c1_payload", (out["c1"].get("tool_output") or {}).get("open_count") == 2)

    d_files = dict(base)
    d_files[f"{TOOLS_DIR}/routed-defects.py"] = STUB_ROUTED_EXIT2
    _with_fixture("d", d_files, case_d, cases, failures)

    # E (red): tool present but exposes no main/run callable.
    def case_e(root, revision):
        out = measure(root, revision)
        check("e_c1_reason", out["c1"]["reason"] == "tool_has_no_callable_main")
        check("e_c1_status", out["c1"]["status"] == "could-not-evaluate")

    e_files = dict(base)
    e_files[f"{TOOLS_DIR}/routed-defects.py"] = STUB_ROUTED_NO_MAIN
    _with_fixture("e", e_files, case_e, cases, failures)

    # F (red): one run's compare.json is not JSON -> C3 cannot be counted whole.
    def case_f(root, revision):
        out = measure(root, revision)
        check("f_c3_status", out["c3"]["status"] == "could-not-evaluate")
        check("f_c3_reason", out["c3"]["reason"] == "compare_json_unparseable")
        check("f_c3_count", out["c3"]["compare_jsons"] == 1)
        check("f_c3_unparseable", len(out["c3"]["unparseable"]) == 1)
        check("f_flag", out["could_not_evaluate"] is True)

    f_files = dict(base)
    f_files[f"{ROUND}/runs/broken/compare.json"] = CMP_BROKEN
    _with_fixture("f", f_files, case_f, cases, failures)

    # G (red): an unresolvable revision aborts with exit 2 and a named reason.
    def case_g(root, _revision):
        err, code = io.StringIO(), None
        try:
            with redirect_stderr(err):
                main(["0" * 40, "--root", str(root)])
        except SystemExit as exc:
            code = exc.code
        check("g_exit", code == 2)
        check("g_reason", "revision_unresolvable" in err.getvalue())

    _with_fixture("g", base, case_g, cases, failures)

    # H: a tool committed later must not leak into an earlier revision.
    def case_h(root, revision):
        first = measure(root, revision)
        check("h_first_absent", first["c1"]["reason"] == "tool_absent_at_rev")
        run = _fixture_git(root)
        later = _commit(
            run, root, {f"{TOOLS_DIR}/routed-defects.py": STUB_ROUTED_OK}, "add tool"
        )
        second = measure(root, later)
        check("h_second_evaluated", second["c1"]["status"] == "evaluated")
        check("h_second_count", second["c1_open_count"] == 2)
        again = measure(root, revision)
        check("h_first_stable", again["c1"]["reason"] == "tool_absent_at_rev")

    _with_fixture("h", base, case_h, cases, failures)

    # I (red): tool echoes another revision -> its count is not at REV.
    def case_i(root, revision):
        out = measure(root, revision)
        check("i_c1_status", out["c1"]["status"] == "could-not-evaluate")
        check("i_c1_reason", out["c1"]["reason"] == "tool_rev_mismatch")
        check("i_c1_tool_rev", out["c1"]["tool_rev"] == "f" * 40)
        check("i_c1_count_none", out["c1_open_count"] is None)
        check("i_flag", out["could_not_evaluate"] is True)

    i_files = dict(base)
    i_files[f"{TOOLS_DIR}/routed-defects.py"] = STUB_ROUTED_OTHER_REV
    _with_fixture("i", i_files, case_i, cases, failures)

    # J (red): tool runs at import time (no __main__ guard) -> named finding,
    # and the measurement still completes rather than dying with its exit.
    def case_j(root, revision):
        out = measure(root, revision)
        check(
            "j_c1_reason",
            out["c1"]["reason"].startswith("tool_import_error: SystemExit"),
        )
        check("j_c1_status", out["c1"]["status"] == "could-not-evaluate")
        check("j_c2_absent", out["c2"]["reason"] == "tool_absent_at_rev")
        check("j_flag", out["could_not_evaluate"] is True)

    j_files = dict(base)
    j_files[f"{TOOLS_DIR}/routed-defects.py"] = STUB_ROUTED_IMPORT_EXIT
    _with_fixture("j", j_files, case_j, cases, failures)

    # K: a tool that prints at import must not reach measure's own stdout.
    def case_k(root, revision):
        captured = io.StringIO()
        with redirect_stdout(captured):
            out = measure(root, revision)
        check("k_c1_evaluated", out["c1"]["status"] == "evaluated")
        check("k_c1_zero", out["c1_open_count"] == 0)
        check("k_stdout_clean", captured.getvalue() == "")

    k_files = dict(base)
    k_files[f"{TOOLS_DIR}/routed-defects.py"] = STUB_ROUTED_IMPORT_NOISE
    _with_fixture("k", k_files, case_k, cases, failures)

    if failures:
        print(f"SELFTEST: FAILED cases={len(cases)} failures={failures}")
        raise SystemExit(1)
    print(f"SELFTEST: CLEAN cases={len(cases)}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Measure round-18 claims from Git objects at one revision."
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
        fail("lane_unresolvable", "pass --root DIR or run from LANE/.ufo/waves/round-18/")
    print(json.dumps(measure(root, args.revision), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
