#!/usr/bin/env python3
"""Measure round-20 claims from immutable lane Git objects.

Usage: python3 -I -B .ufo/waves/round-20/measure.py REV --freeze COMMIT
       python3 -I -B .ufo/waves/round-20/measure.py --selftest

C1 and C2 execute their tool sources from REV's Git blobs and preserve each
JSON summary. C3 counts prediction blobs unchanged since --freeze, receipts
accepted by REV's receipt validator with --require-mid-maps, and JSON compare
records under runs/<label>/compare.json. No current worktree file is used to
discover the measured inputs.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

try:
    LANE = Path(__file__).resolve().parents[3]
except IndexError:
    LANE = None

ROUND = ".ufo/waves/round-20"
TOOLS_DIR = f"{ROUND}/tools"
C1_PATH = f"{TOOLS_DIR}/routed-r19.py"
C2_PATH = f"{TOOLS_DIR}/verb-coverage.py"
VALIDATOR_PATH = ".ufo/waves/round-17/tools/receipt-validate.py"
PINS_PATH = ".ufo/waves/round-17/tools/pins.py"
PRED_RE = re.compile(r"^" + re.escape(ROUND) + r"/predictions/([^/]+)\.prediction\.json$")
RECEIPT_RE = re.compile(r"^" + re.escape(ROUND) + r"/runs/([^/]+)/receipt\.json$")
COMPARE_RE = re.compile(r"^" + re.escape(ROUND) + r"/runs/([^/]+)/compare\.json$")
EXIT_RE = re.compile(r"^" + re.escape(ROUND) + r"/runs/([^/]+)/compare\.exit$")
# Round-20 lesson Mistakes 6: the in-run compare received the wrong prediction file and exited 2
# for every label; the post-run re-run with the frozen comparator on the frozen emulator outputs is
# retained under evidence/compare-rerun/ and, when present, supersedes runs/<label>/compare.json.
RERUN_RE = re.compile(r"^" + re.escape(ROUND) + r"/evidence/compare-rerun/(t[0-9]+-[^/]+)\.json$")

LIMITS = [
    "C1 and C2 summaries come from the corresponding Python tool blobs at REV; "
    "their exit status, summary and stderr are reported without reimplementing their checks.",
    "C3 prediction freeze identity compares Git blob object IDs at REV and --freeze; "
    "it does not infer prediction chronology from commit timestamps.",
    "C3 receipt validation executes the validator and pins.py blobs at REV with "
    "--require-mid-maps. The validator reads file paths recorded inside receipts; "
    "those referenced external bytes can change independently of Git history.",
    "C3 comparison records are parsed from runs/<label>/compare.json at REV; "
    "matched counts only bound labels whose record reports a match or whose "
    "recorded compare exit is zero. No run log is re-extracted or compared here.",
    "Raw counts describe committed files at REV. A measured zero is not an error; "
    "missing or unusable instruments are named separately.",
]


def fail(reason, message):
    print(f"measure.py: {reason}: {message}", file=sys.stderr)
    raise SystemExit(2)


def _git(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), "--no-optional-locks", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _resolve(root, revision):
    proc = _git(root, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{revision}^{{commit}}")
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("ascii", "replace").strip() or None


def _tree(root, revision):
    proc = _git(root, "ls-tree", "-r", "-z", "--name-only", revision)
    if proc.returncode != 0:
        return None
    return {os.fsdecode(item) for item in proc.stdout.split(b"\0") if item}


def _read_blob(root, revision, rel):
    proc = _git(root, "show", f"{revision}:{rel}")
    if proc.returncode != 0:
        return None
    return proc.stdout


def _blob_oid(root, revision, rel):
    proc = _git(root, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{revision}:{rel}")
    if proc.returncode != 0:
        return None
    oid = proc.stdout.decode("ascii", "replace").strip()
    if not oid:
        return None
    kind = _git(root, "cat-file", "-t", oid)
    if kind.returncode != 0 or kind.stdout.strip() != b"blob":
        return None
    return oid


def _parse_json(data):
    if not data:
        return None
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        pass
    for line in reversed(data.decode("utf-8", "replace").splitlines()):
        if not line.strip():
            continue
        try:
            return json.loads(line)
        except ValueError:
            continue
    return None


def _tail(data, limit=800):
    text = (data or b"").decode("utf-8", "replace").strip()
    return text[-limit:] if text else None


def _safe_dest(base, rel):
    path = PurePosixPath(rel)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError("unsafe_revision_path")
    return base.joinpath(*path.parts)


def _materialize_tools(root, revision, paths, destination):
    failures = {}
    for rel in sorted(path for path in paths if path.startswith(TOOLS_DIR + "/") and path.endswith(".py")):
        try:
            target = _safe_dest(destination, rel)
        except ValueError as exc:
            failures[rel] = str(exc)
            continue
        data = _read_blob(root, revision, rel)
        if data is None:
            failures[rel] = "tool_blob_unreadable"
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return failures


def _materialize_validator(root, revision, paths, destination):
    for rel in (VALIDATOR_PATH, PINS_PATH):
        if rel not in paths:
            return f"{rel.rsplit('/', 1)[-1]}_absent_at_rev"
        try:
            target = _safe_dest(destination, rel)
        except ValueError as exc:
            return str(exc)
        data = _read_blob(root, revision, rel)
        if data is None:
            return f"{rel.rsplit('/', 1)[-1]}_blob_unreadable"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return None


def _reported_revision(payload):
    for name in ("rev", "revision"):
        value = payload.get(name)
        if isinstance(value, str):
            return value
    return None


def _claim_tool(root, revision, paths, failures, materialized_root, rel, name, extra=()):
    claim = {
        "tool_path": rel,
        "status": "could-not-evaluate",
        "reason": None,
        "tool_exit": None,
        "tool_rev": None,
        "stderr": None,
        "summary": None,
    }
    if rel not in paths:
        claim["reason"] = "tool_absent_at_rev"
        return claim
    if rel in failures:
        claim["reason"] = failures[rel]
        return claim
    try:
        tool = _safe_dest(materialized_root, rel)
    except ValueError as exc:
        claim["reason"] = str(exc)
        return claim
    if not tool.is_file():
        claim["reason"] = "tool_blob_unreadable"
        return claim
    argv = [sys.executable, "-I", "-B", str(tool), "--root", str(root), "--rev", revision, *extra]
    try:
        run = subprocess.run(
            argv,
            cwd=str(root),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=300,
        )
    except subprocess.TimeoutExpired as exc:
        claim["reason"] = "tool_timeout"
        claim["stderr"] = _tail(exc.stderr)
        return claim
    except OSError as exc:
        claim["reason"] = f"tool_spawn_error:{type(exc).__name__}"
        return claim
    claim["tool_exit"] = run.returncode
    claim["stderr"] = _tail(run.stderr)
    payload = _parse_json(run.stdout)
    if not isinstance(payload, dict):
        claim["reason"] = "tool_output_not_json_object"
        claim["raw_output"] = _tail(run.stdout)
        return claim
    claim["summary"] = payload
    claim["tool_rev"] = _reported_revision(payload)
    if run.returncode not in (0, 1):
        claim["reason"] = f"tool_exit_{run.returncode}"
        return claim
    if claim["tool_rev"] is not None and claim["tool_rev"] != revision:
        claim["reason"] = "tool_rev_mismatch"
        return claim
    claim["status"] = "evaluated"
    return claim


def _read_label_blobs(root, revision, freeze, paths):
    predictions = {}
    receipts = {}
    comparisons = {}
    exits = {}
    for rel in sorted(paths):
        match = PRED_RE.fullmatch(rel)
        if match:
            label = match.group(1)
            rev_oid = _blob_oid(root, revision, rel)
            frozen_oid = _blob_oid(root, freeze, rel)
            predictions[label] = {
                "path": rel,
                "blob": rev_oid,
                "freeze_blob": frozen_oid,
                "equals_freeze": rev_oid is not None and rev_oid == frozen_oid,
                "reason": None if frozen_oid is not None else "prediction_absent_at_freeze",
            }
            continue
        match = RECEIPT_RE.fullmatch(rel)
        if match:
            receipts[match.group(1)] = rel
            continue
        match = COMPARE_RE.fullmatch(rel)
        if match:
            comparisons[match.group(1)] = rel
            continue
        match = EXIT_RE.fullmatch(rel)
        if match:
            exits[match.group(1)] = rel
    for rel in sorted(paths):
        match = RERUN_RE.fullmatch(rel)
        if match and match.group(1) in comparisons:
            comparisons[match.group(1)] = rel
            exits.pop(match.group(1), None)
    return predictions, receipts, comparisons, exits


def _receipt_result(root, revision, receipt_rel, temp_root, paths, validator_error):
    if receipt_rel is None:
        return {"valid": False, "reason": "receipt_absent_at_rev"}
    if validator_error is not None:
        return {"valid": False, "reason": validator_error}
    receipt_data = _read_blob(root, revision, receipt_rel)
    if receipt_data is None:
        return {"valid": False, "reason": "receipt_blob_unreadable"}
    nonce = str(len(list((temp_root / "receipts").glob("*.json"))))
    receipt_path = temp_root / "receipts" / f"receipt-{nonce}.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_bytes(receipt_data)
    validator = _safe_dest(temp_root, VALIDATOR_PATH)
    try:
        run = subprocess.run(
            [sys.executable, "-I", "-B", str(validator), "--require-mid-maps", str(receipt_path)],
            cwd=str(temp_root),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=300,
        )
    except subprocess.TimeoutExpired as exc:
        return {"valid": False, "reason": "receipt_validator_timeout", "stderr": _tail(exc.stderr)}
    except OSError as exc:
        return {"valid": False, "reason": f"receipt_validator_spawn_error:{type(exc).__name__}"}
    payload = _parse_json(run.stdout)
    result = {
        "valid": False,
        "exit": run.returncode,
        "require_mid_maps": payload.get("require_mid_maps") if isinstance(payload, dict) else None,
        "counts": payload.get("counts") if isinstance(payload, dict) else None,
        "findings": None,
        "stderr": _tail(run.stderr),
    }
    entries = payload.get("receipts") if isinstance(payload, dict) else None
    if isinstance(entries, list) and len(entries) == 1 and isinstance(entries[0], dict):
        result["findings"] = entries[0].get("findings")
    counts = result["counts"]
    entry_valid = (
        isinstance(entries, list)
        and len(entries) == 1
        and isinstance(entries[0], dict)
        and entries[0].get("valid") is True
    )
    count_valid = isinstance(counts, dict) and counts.get("valid") == 1 and counts.get("invalid") == 0 and counts.get("unreadable") == 0
    if not isinstance(payload, dict):
        result["reason"] = "receipt_validator_output_not_json_object"
    elif payload.get("require_mid_maps") is not True:
        result["reason"] = "receipt_validator_did_not_require_mid_maps"
    elif run.returncode != 0 or not entry_valid or not count_valid:
        result["reason"] = "receipt_invalid"
    else:
        result["valid"] = True
        result["reason"] = None
    return result


def _compare_details(root, revision, rel, exit_rel):
    if rel is None:
        return {"present": False, "valid_record": False, "matched": None, "reason": "compare_record_absent_at_rev"}
    data = _read_blob(root, revision, rel)
    payload = _parse_json(data) if data is not None else None
    if not isinstance(payload, dict):
        return {"present": True, "path": rel, "valid_record": False, "matched": None, "reason": "compare_record_unparseable"}
    exit_value = None
    exit_data = _read_blob(root, revision, exit_rel) if exit_rel is not None else None
    if exit_data is not None:
        try:
            exit_value = int(exit_data.decode("utf-8").strip())
        except (UnicodeDecodeError, ValueError):
            exit_value = None
    match_value = None
    match_source = None
    for key in ("match", "matched"):
        if isinstance(payload.get(key), bool):
            match_value = payload[key]
            match_source = key
            break
    if match_value is None:
        for key in ("status", "result", "verdict"):
            value = payload.get(key)
            if isinstance(value, str) and value.lower() in ("match", "matched", "mismatch", "no_match", "unmatched"):
                match_value = value.lower() in ("match", "matched")
                match_source = key
                break
    if match_value is None and exit_value in (0, 1):
        match_value = exit_value == 0
        match_source = "compare.exit"
    return {
        "present": True,
        "path": rel,
        "valid_record": True,
        "record": payload,
        "exit_path": exit_rel,
        "exit": exit_value,
        "matched": match_value,
        "match_source": match_source,
        "reason": None if match_value is not None else "compare_match_not_reported",
    }


def _claim_c3(root, revision, freeze, paths, temp_root):
    validator_error = _materialize_validator(root, revision, paths, temp_root)
    predictions, receipt_paths, compare_paths, exit_paths = _read_label_blobs(root, revision, freeze, paths)
    labels = sorted(set(predictions) | set(receipt_paths) | set(compare_paths) | set(exit_paths))
    receipt_results = {}
    compare_results = {}
    for label in labels:
        receipt_results[label] = _receipt_result(
            root, revision, receipt_paths.get(label), temp_root, paths, validator_error
        )
        compare_results[label] = _compare_details(
            root, revision, compare_paths.get(label), exit_paths.get(label)
        )
    bound = sorted(
        label
        for label in labels
        if predictions.get(label, {}).get("equals_freeze") is True
        and receipt_results[label].get("valid") is True
        and compare_results[label].get("valid_record") is True
    )
    matched = sorted(
        label for label in bound if compare_results[label].get("matched") is True
    )
    compare_unparseable = sorted(
        label for label in labels if compare_results[label].get("reason") == "compare_record_unparseable"
    )
    status = "evaluated"
    reason = None
    if validator_error is not None and receipt_paths:
        status = "could-not-evaluate"
        reason = validator_error
    elif compare_unparseable:
        status = "could-not-evaluate"
        reason = "compare_record_unparseable"
    raw_counts = {
        "prediction_files": len(predictions),
        "freeze_equal_predictions": sum(entry["equals_freeze"] for entry in predictions.values()),
        "receipt_files": len(receipt_paths),
        "receipt_valid": sum(entry["valid"] for entry in receipt_results.values()),
        "receipt_invalid_or_unusable": sum(not entry["valid"] for entry in receipt_results.values()),
        "compare_files": len(compare_paths),
        "compare_records": sum(entry["valid_record"] for entry in compare_results.values()),
        "compare_matched_records": sum(entry["matched"] is True for entry in compare_results.values()),
        "compare_exit_files": len(exit_paths),
        "first_failure_bound": len(bound),
        "matched": len(matched),
    }
    return {
        "status": status,
        "reason": reason,
        "freeze_revision": freeze,
        "first_failure_bound": len(bound),
        "first_failure_bound_ids": bound,
        "matched": len(matched),
        "matched_ids": matched,
        "raw_counts": raw_counts,
        "labels": {
            label: {
                "prediction": predictions.get(label),
                "receipt": receipt_results.get(label),
                "compare_first_failure": compare_results.get(label),
                "first_failure_bound": label in bound,
                "matched": compare_results[label].get("matched"),
            }
            for label in labels
        },
    }


def measure(root, revision_requested, freeze_requested):
    root = Path(root).resolve()
    revision = _resolve(root, revision_requested)
    if revision is None:
        fail("revision_unresolvable", revision_requested)
    freeze = _resolve(root, freeze_requested)
    if freeze is None:
        fail("freeze_unresolvable", freeze_requested)
    paths = _tree(root, revision)
    if paths is None:
        fail("revision_tree_unreadable", revision)
    with tempfile.TemporaryDirectory(prefix="measure-r20-") as scratch:
        temp_root = Path(scratch)
        tool_root = temp_root / "revision-tools"
        tool_root.mkdir(parents=True, exist_ok=True)
        failures = _materialize_tools(root, revision, paths, tool_root)
        c1 = _claim_tool(root, revision, paths, failures, tool_root, C1_PATH, "c1", extra=("--strict",))
        c2 = _claim_tool(root, revision, paths, failures, tool_root, C2_PATH, "c2")
        c3 = _claim_c3(root, revision, freeze, paths, temp_root)
    return {
        "argv": list(sys.argv),
        "lane": str(root),
        "round": ROUND,
        "revision": revision,
        "revision_requested": revision_requested,
        "freeze_revision": freeze,
        "freeze_requested": freeze_requested,
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "raw_counts": c3["raw_counts"],
        "could_not_evaluate": any(
            claim["status"] != "evaluated" for claim in (c1, c2, c3)
        ),
        "limits": LIMITS,
    }


# Fixture tools deliberately test the measurement contract, not the correctness
# of the separately owned routed, coverage, or receipt-validation instruments.
STUB_ROUTED = '''#!/usr/bin/env python3
import argparse, json
p = argparse.ArgumentParser()
p.add_argument("--root", required=True)
p.add_argument("--rev", required=True)
p.add_argument("--strict", action="store_true")
a = p.parse_args()
print(json.dumps({"rev": a.rev, "open_count": 2, "strict_seen": a.strict}))
'''
STUB_COVERAGE = '''#!/usr/bin/env python3
import argparse, json
p = argparse.ArgumentParser()
p.add_argument("--root", required=True)
p.add_argument("--rev", required=True)
a = p.parse_args()
print(json.dumps({"rev": a.rev, "target_count": 5, "exercised_count": 3}))
'''
STUB_VALIDATOR = '''#!/usr/bin/env python3
import argparse, json, pathlib, sys
p = argparse.ArgumentParser()
p.add_argument("--require-mid-maps", action="store_true")
p.add_argument("receipts", nargs="+")
a = p.parse_args()
receipt = json.loads(pathlib.Path(a.receipts[0]).read_text(encoding="utf-8"))
valid = a.require_mid_maps and receipt.get("valid") is True
finding = [] if valid else [{"code": "fixture_invalid"}]
print(json.dumps({"require_mid_maps": a.require_mid_maps, "receipts": [{"valid": valid, "findings": finding}], "counts": {"receipts": 1, "valid": int(valid), "invalid": int(not valid), "unreadable": 0}}))
sys.exit(0 if valid else 1)
'''


def _fixture_git(root):
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "measure-r20-selftest",
        "GIT_AUTHOR_EMAIL": "selftest@invalid",
        "GIT_COMMITTER_NAME": "measure-r20-selftest",
        "GIT_COMMITTER_EMAIL": "selftest@invalid",
    })

    def run(*args):
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env=env,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"fixture_git_{args[0]}_exit_{proc.returncode}")
        return proc.stdout.decode("utf-8", "replace")

    return run


def _fixture_commit(run, root, files, message):
    for rel, content in files.items():
        target = _safe_dest(root, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode("utf-8") if isinstance(content, str) else content
        target.write_bytes(data)
    run("add", "-A")
    run("-c", "commit.gpgsign=false", "commit", "-q", "-m", message)
    return run("rev-parse", "HEAD").strip()


def _fixture_base():
    return {
        C1_PATH: STUB_ROUTED,
        C2_PATH: STUB_COVERAGE,
        VALIDATOR_PATH: STUB_VALIDATOR,
        PINS_PATH: "# fixture sibling required by the validator tool layout\n",
        f"{ROUND}/predictions/alpha.prediction.json": '{"first_failure":{"h1":{"kind":"eof","index":1}}}\n',
        f"{ROUND}/predictions/beta.prediction.json": '{"first_failure":{"h1":{"kind":"eof","index":2}}}\n',
        f"{ROUND}/predictions/gamma.prediction.json": '{"first_failure":{"h1":null}}\n',
        f"{ROUND}/predictions/delta.prediction.json": '{"first_failure":{"h1":null}}\n',
    }


def selftest():
    cases = []
    failures = []

    def check(case_id, condition):
        cases.append(case_id)
        if not condition:
            failures.append(case_id)

    temp = Path(tempfile.mkdtemp(prefix="measure-r20-selftest-"))
    try:
        root = temp / "fixture-repo"
        root.mkdir()
        run = _fixture_git(root)
        run("init", "-q")
        freeze = _fixture_commit(run, root, _fixture_base(), "freeze predictions")
        revision_files = {
            f"{ROUND}/predictions/beta.prediction.json": '{"first_failure":{"h1":{"kind":"eof","index":3}}}\n',
            f"{ROUND}/runs/alpha/receipt.json": '{"valid":true}\n',
            f"{ROUND}/runs/alpha/compare.json": '{"match":true,"expected":{"kind":"eof"},"observed":{"kind":"eof"}}\n',
            f"{ROUND}/runs/alpha/compare.exit": "0\n",
            f"{ROUND}/runs/beta/receipt.json": '{"valid":true}\n',
            f"{ROUND}/runs/beta/compare.json": '{"match":false,"expected":{"kind":"eof"},"observed":{"kind":"invalid_index"}}\n',
            f"{ROUND}/runs/beta/compare.exit": "1\n",
            f"{ROUND}/runs/gamma/receipt.json": '{"valid":false}\n',
            f"{ROUND}/runs/gamma/compare.json": '{"match":true}\n',
            f"{ROUND}/runs/gamma/compare.exit": "0\n",
            f"{ROUND}/runs/delta/receipt.json": '{"valid":true}\n',
        }
        revision = _fixture_commit(run, root, revision_files, "record run evidence")
        out = measure(root, revision, freeze)
        check("complete_revision_resolved", out["revision"] == revision)
        check("freeze_resolved", out["freeze_revision"] == freeze)
        check("c1_summary", out["c1"]["summary"] == {"rev": revision, "open_count": 2, "strict_seen": True})
        check("c1_strict_exit", out["c1"]["tool_exit"] == 0)
        check("c2_summary", out["c2"]["summary"] == {"rev": revision, "target_count": 5, "exercised_count": 3})
        check("prediction_blob_freeze", out["c3"]["raw_counts"]["freeze_equal_predictions"] == 3)
        check("receipt_validator_mid_maps", out["c3"]["labels"]["alpha"]["receipt"]["require_mid_maps"] is True)
        check("receipt_invalid_excluded", out["c3"]["labels"]["gamma"]["first_failure_bound"] is False)
        check("changed_prediction_excluded", out["c3"]["labels"]["beta"]["first_failure_bound"] is False)
        check("compare_required", out["c3"]["labels"]["delta"]["first_failure_bound"] is False)
        check("bound_count", out["c3"]["first_failure_bound"] == 1)
        check("bound_ids", out["c3"]["first_failure_bound_ids"] == ["alpha"])
        check("matched_count", out["c3"]["matched"] == 1)
        check("raw_prediction_count", out["raw_counts"]["prediction_files"] == 4)
        check("raw_receipt_count", out["raw_counts"]["receipt_files"] == 4)
        check("raw_compare_count", out["raw_counts"]["compare_files"] == 3)
        (root / f"{ROUND}/predictions/zeta.prediction.json").parent.mkdir(parents=True, exist_ok=True)
        (root / f"{ROUND}/predictions/zeta.prediction.json").write_text("{}\n", encoding="utf-8")
        after_worktree_change = measure(root, revision, freeze)
        check("working_tree_excluded", after_worktree_change["raw_counts"]["prediction_files"] == 4)
        historical = measure(root, freeze, freeze)
        check("historical_runs_absent", historical["raw_counts"]["receipt_files"] == 0)
        check("historical_count_zero", historical["c3"]["first_failure_bound"] == 0)

        broken = temp / "broken-repo"
        broken.mkdir()
        broken_run = _fixture_git(broken)
        broken_run("init", "-q")
        base = _fixture_commit(broken_run, broken, {"corpus/README.md": "fixture\n"}, "empty")
        absent = measure(broken, base, base)
        check("absent_c1_named", absent["c1"]["reason"] == "tool_absent_at_rev")
        check("absent_c2_named", absent["c2"]["reason"] == "tool_absent_at_rev")
        check("absent_c3_zero", absent["c3"]["first_failure_bound"] == 0)
        check("absent_not_crash", absent["could_not_evaluate"] is True)

        caught = None
        try:
            measure(broken, "0" * 40, base)
        except SystemExit as exc:
            caught = exc.code
        check("bad_revision_refused", caught == 2)
        caught = None
        try:
            measure(broken, base, "0" * 40)
        except SystemExit as exc:
            caught = exc.code
        check("bad_freeze_refused", caught == 2)
    except (Exception, SystemExit) as exc:
        failures.append(f"selftest_raised_{type(exc).__name__}")
    finally:
        shutil.rmtree(temp, ignore_errors=True)
    if failures:
        print(f"SELFTEST: FAILED cases={len(cases)} fails={len(failures)} ids={failures}")
        raise SystemExit(1)
    print(f"SELFTEST: CLEAN cases={len(cases)}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Measure round-20 claims from Git objects at one revision.")
    parser.add_argument("revision", nargs="?", help="commit sha or ref to measure")
    parser.add_argument("--freeze", help="commit containing the frozen predictions")
    parser.add_argument("--root", default=None, help="lane Git worktree; defaults to three parents above this file")
    parser.add_argument("--selftest", action="store_true", help="run mkdtemp fixture repositories")
    args = parser.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    if not args.revision:
        fail("usage", "measure.py REV --freeze COMMIT | --selftest")
    if not args.freeze:
        fail("freeze_required", "pass --freeze COMMIT")
    if args.root is not None:
        root = Path(args.root)
    elif LANE is not None:
        root = LANE
    else:
        fail("lane_unresolvable", "pass --root DIR or run from LANE/.ufo/waves/round-20/")
    print(json.dumps(measure(root, args.revision, args.freeze), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
