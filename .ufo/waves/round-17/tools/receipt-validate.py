#!/usr/bin/env python3
"""receipt-validate.py -- re-verify a recorded receipt against live bytes.

Usage: python3 -I receipt-validate.py RECEIPT.json...
       python3 -I receipt-validate.py --selftest

For every receipt argument the tool:

  1. Classifies the shape: `retain` (retain.py fields), `carrier`
     (carrier-run.py fields: label/carrier/steps), or `unknown`.
  2. Checks the required-field set for that shape (contract: receipt
     `{argv, cwd, started_at_utc, ended_at_utc, exit, stdout_path,
     stdout_sha256, stderr_path, stderr_sha256, python, orig_argv,
     pins_pre, pins_post, pins_compare}` for retain.py; `label, carrier,
     steps, retained_logs, pins_pre, pins_post, pins_compare, python,
     orig_argv, log_capture_limit` for carrier-run.py).
  3. Recomputes the sha256 (and recorded size/bytes where present) of
     every file the receipt commits to, preferring the newest recorded
     digest (sha256_post over sha256 over sha256_pre; pins_post entries
     over pins_pre entries for the same path). A file legitimately
     changed between pins_pre and pins_post is therefore NOT flagged.
  4. Re-runs pins.compare on the recorded pins_pre/pins_post snapshots
     and checks equality of {equal, changed, missing} against the
     recorded pins_compare. Timestamps are ignored.

pins.py is imported by absolute path via importlib from the resolved
sibling `tools/pins.py`, mirroring retain.py's loader. When pins.py is
absent the tool cannot evaluate and exits 2.

Exit codes: 0 every receipt valid, 1 any receipt invalid (findings
listed), 2 any receipt unreadable/invalid JSON or pins.py unavailable.
No network, no subprocesses, nothing is executed but this script.

Limitation (recorded, not hardened): validation proves only that the
recorded digests match the bytes present NOW. Bytes could have been
modified and restored between the run and validation; the receipt's
own pins section is trusted as the record of the run-window state.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import re
import os
import shutil
import sys

sys.dont_write_bytecode = True  # never write __pycache__ next to imported pins.py
import tempfile
from pathlib import Path

PINS_PATH = Path(__file__).resolve().parent / "pins.py"

RETAIN_REQUIRED = [
    "argv", "cwd", "started_at_utc", "ended_at_utc", "exit",
    "stdout_path", "stdout_sha256", "stderr_path", "stderr_sha256",
    "python", "orig_argv", "pins_pre", "pins_post", "pins_compare",
]
CARRIER_REQUIRED = [
    "label", "carrier", "steps", "retained_logs",
    "pins_pre", "pins_post", "pins_compare",
    "python", "orig_argv", "log_capture_limit",
]
CARRIER_STEP_REQUIRED = [
    "argv", "cwd", "exit",
    "stdout_path", "stdout_sha256", "stderr_path", "stderr_sha256",
]
# Newest-first preference among digest keys recorded for one path.
SHA_KEYS = ["sha256_post", "sha256", "sha256_pre"]
# Snapshot subtrees handled by dedicated logic, never by the generic walk.
PIN_KEYS = ("pins_pre", "pins_post")


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_pins():
    """Import the sibling pins.py by absolute path (contract section
    pins.py + retain.py loader idiom)."""
    if not PINS_PATH.is_file():
        return None
    spec = importlib.util.spec_from_file_location("pins", PINS_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def classify(receipt):
    # Round-17 L1 integration (w2: all eight producer receipts failed
    # `unrecognized_shape`): carrier-run.py writes `steps` as an object keyed by
    # step name; the original selftest fixture used a list. Accept both.
    if not isinstance(receipt, dict):
        return "unknown"
    if isinstance(receipt.get("steps"), (list, dict)) and isinstance(
        receipt.get("carrier"), dict
    ):
        return "carrier"
    if "argv" in receipt and "pins_compare" in receipt:
        return "retain"
    return "unknown"


def _iter_steps(steps):
    if isinstance(steps, dict):
        return [(f"$.steps.{name}", step) for name, step in steps.items()]
    return [(f"$.steps[{i}]", step) for i, step in enumerate(steps or [])]


def check_binding(receipt, findings):
    """Re-derive the log-to-run binding from the retained log bytes (w2
    ReceiptForge/RunProcontainerdshim F4): every bound session's ghidra.log must
    name its own path and the imported target-<carrier sha256[:12]>.bin; no step
    may carry a mid-run pin drift record; recorded mid-run checks must be equal."""
    checks = 0
    if "bound_sessions" not in receipt:
        # Absence must not be safer than emptiness (w2 ReceiptForge F2).
        findings.append({"code": "missing_field", "where": "$.bound_sessions"})
        return checks + 1
    carrier = receipt.get("carrier") or {}
    _k, sha = newest_sha(carrier) if isinstance(carrier, dict) else (None, None)
    # The carrier must be one of the pinned paths with the same digest (w2 ReceiptForge F4).
    checks += 1
    pin_ent = ((receipt.get("pins_pre") or {}).get("entries") or {}).get(
        carrier.get("path") if isinstance(carrier, dict) else None) or {}
    if not sha or pin_ent.get("sha256") != sha:
        findings.append({"code": "carrier_not_pinned", "where": "$.carrier"})
    bound = receipt.get("bound_sessions") or []
    checks += 1
    if len(bound) < 1:
        findings.append({"code": "no_bound_session", "where": "$.bound_sessions"})
    by_dir = {e.get("session_dir"): e for e in receipt.get("retained_logs") or []
              if isinstance(e, dict)}
    carrier_md5 = None
    cpath = carrier.get("path") if isinstance(carrier, dict) else None
    if sha and cpath and os.path.isfile(cpath) and sha256_file(cpath) == sha:
        h = hashlib.md5()
        with open(cpath, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        carrier_md5 = h.hexdigest()
    for d in bound:
        checks += 1
        ent = by_dir.get(d) or {}
        path = ((ent.get("files") or {}).get("ghidra.log") or {}).get("path")
        try:
            if not path or os.path.islink(path):
                raise OSError("missing or symlinked log")
            text = open(path, "rb").read().decode("utf-8", "replace")
        except OSError:
            text = ""
        lines = [ln.rstrip("\r").rstrip() for ln in text.split("\n")]
        # Line-anchored records (w2 BindingFuzz b05-b07: substrings inside stack
        # traces or suffixed names bound falsely).
        logfile_ok = any(re.fullmatch(
            r"\S+ \S+ INFO +\(LoggingInitialization\) Using log file: "
            + re.escape(f"{d}/ghidra.log"), ln) for ln in lines)
        target_ok = bool(sha) and any(re.fullmatch(
            r"\S+ \S+ INFO +\(HeadlessAnalyzer\) IMPORTING: "
            + re.escape(f"file://{d}/target-{sha[:12]}.bin"), ln) for ln in lines)
        # Full-digest binding when the pinned carrier is still on disk (w2
        # BindingFuzz b04: 12-hex prefixes can collide): Ghidra's loader line
        # carries the target's full MD5.
        md5_ok = None
        if carrier_md5 and sha:
            md5_ok = any(ln.startswith(f"Loading file://{d}/target-{sha[:12]}.bin?MD5={carrier_md5}")
                         for ln in lines)
        if not (logfile_ok and target_ok and md5_ok is not False):
            findings.append({"code": "binding_mismatch", "where": "$.bound_sessions",
                             "path": path or d, "logfile_ok": logfile_ok,
                             "target_ok": target_ok, "md5_ok": md5_ok})
    for where, step in _iter_steps(receipt.get("steps")):
        if not isinstance(step, dict):
            continue
        checks += 1
        if step.get("pins_changed_during_run"):
            findings.append({"code": "mid_run_pin_drift", "where": where})
        for i, chk in enumerate(step.get("pin_checks") or []):
            checks += 1
            if not (isinstance(chk, dict) and chk.get("equal") is True):
                findings.append({"code": "mid_run_pin_drift",
                                 "where": f"{where}.pin_checks[{i}]"})
    return checks


def newest_sha(dct):
    """Return (key, value) for the newest digest key present, else (None, None)."""
    for key in SHA_KEYS:
        value = dct.get(key)
        if isinstance(value, str) and len(value) == 64:
            return key, value
    return None, None


def verify_file(path, expected_sha, findings, where, expected_size=None):
    """Recompute digest/size of `path`; append findings on mismatch."""
    if not os.path.isfile(path):
        findings.append({
            "code": "missing_file",
            "where": where,
            "path": path,
            "expected_sha256": expected_sha,
        })
        return 0
    try:
        actual = sha256_file(path)
    except OSError as error:
        findings.append({
            "code": "unreadable_file",
            "where": where,
            "path": path,
            "error": str(error),
        })
        return 0
    checks = 1
    if expected_sha is not None and actual != expected_sha:
        findings.append({
            "code": "sha256_mismatch",
            "where": where,
            "path": path,
            "expected_sha256": expected_sha,
            "actual_sha256": actual,
        })
    if expected_size is not None:
        checks += 1
        try:
            actual_size = os.path.getsize(path)
            if actual_size != expected_size:
                findings.append({
                    "code": "size_mismatch",
                    "where": where,
                    "path": path,
                    "expected_bytes": expected_size,
                    "actual_bytes": actual_size,
                })
        except OSError:
            pass
    return checks


def verify_pin_entries(snapshot, other_snapshot, which, findings):
    """Verify pin-entry digests. Entries also pinned in `other_snapshot`
    are skipped when `which` is pins_pre (post is authoritative)."""
    checks = 0
    entries = snapshot.get("entries")
    if not isinstance(entries, dict):
        findings.append({
            "code": "pins_shape",
            "where": which,
            "detail": "missing entries mapping",
        })
        return checks
    other_entries = {}
    if isinstance(other_snapshot, dict):
        candidate = other_snapshot.get("entries")
        if isinstance(candidate, dict):
            other_entries = candidate
    for path, entry in sorted(entries.items()):
        if which == "pins_pre" and path in other_entries:
            continue
        where = f"{which}.entries.{path}"
        if not isinstance(entry, dict):
            findings.append({
                "code": "pins_shape", "where": where,
                "detail": "entry is not an object"})
            continue
        if "error" in entry:
            # Recorded snapshot error: nothing recorded to recompute.
            continue
        checks += verify_file(
            path, entry.get("sha256"), findings, where,
            expected_size=entry.get("size"))
    return checks


def walk_pairs(node, findings, where, seen):
    """Recursively verify every recorded (path, sha256[, size/bytes])
    commitment outside the pins subtrees. Returns check count."""
    checks = 0
    if isinstance(node, dict):
        obj_id = id(node)
        if obj_id in seen:
            return checks
        seen.add(obj_id)
        path = node.get("path")
        if isinstance(path, str):
            _key, sha = newest_sha(node)
            if sha is not None:
                size = node.get("bytes")
                if not isinstance(size, int):
                    size = node.get("size")
                checks += verify_file(
                    path, sha, findings, where,
                    expected_size=size if isinstance(size, int) else None)
        else:
            # `<stem>_path` + `<stem>_sha256` sibling convention.
            for key, value in sorted(node.items()):
                if not (isinstance(key, str) and key.endswith("_path")):
                    continue
                stem = key[:-5]
                sha = node.get(stem + "_sha256")
                if isinstance(value, str) and isinstance(sha, str):
                    checks += verify_file(
                        value, sha, findings,
                        f"{where}.{stem}")
        for key, value in node.items():
            if key in PIN_KEYS:
                continue
            if isinstance(value, (dict, list)):
                checks += walk_pairs(value, findings, f"{where}.{key}", seen)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            if isinstance(value, (dict, list)):
                checks += walk_pairs(
                    value, findings, f"{where}[{index}]", seen)
    return checks


def check_required(receipt, kind, findings):
    checks = 0
    if kind == "retain":
        required = RETAIN_REQUIRED
    elif kind == "carrier":
        required = CARRIER_REQUIRED
    else:
        findings.append({
            "code": "unrecognized_shape",
            "where": "$",
            "detail": "receipt matches neither retain nor carrier shape",
        })
        required = []
    for key in required:
        checks += 1
        if key not in receipt:
            findings.append({
                "code": "missing_field", "where": f"$.{key}"})
    if kind == "retain" or (kind == "unknown" and "argv" in receipt):
        argv = receipt.get("argv")
        if "argv" in receipt and not isinstance(argv, list):
            findings.append({
                "code": "field_type", "where": "$.argv",
                "detail": "argv is not a list"})
        compare = receipt.get("pins_compare")
        if isinstance(compare, dict) and not isinstance(
            compare.get("equal"), bool
        ):
            findings.append({
                "code": "field_type", "where": "$.pins_compare.equal",
                "detail": "equal is not a bool"})
    if kind == "carrier":
        carrier = receipt.get("carrier")
        if isinstance(carrier, dict):
            checks += 1
            if "path" not in carrier:
                findings.append({
                    "code": "missing_field", "where": "$.carrier.path"})
            _key, sha = newest_sha(carrier)
            checks += 1
            if sha is None:
                findings.append({
                    "code": "missing_field", "where": "$.carrier",
                    "detail": "no sha256/sha256_pre/sha256_post digest"})
        for where, step in _iter_steps(receipt.get("steps")):
            if not isinstance(step, dict):
                findings.append({
                    "code": "field_type", "where": where,
                    "detail": "step is not an object"})
                continue
            for key in CARRIER_STEP_REQUIRED:
                checks += 1
                if key not in step:
                    findings.append({
                        "code": "missing_field",
                        "where": f"{where}.{key}"})
            checks += 1
            if not any(k.startswith("started") for k in step):
                findings.append({
                    "code": "missing_field",
                    "where": f"{where}.started_at_utc"})
            checks += 1
            if not any(k.startswith("ended") for k in step):
                findings.append({
                    "code": "missing_field",
                    "where": f"{where}.ended_at_utc"})
    return checks


def rerun_pins_compare(receipt, pins, findings):
    """Re-run pins.compare on recorded pre/post; verify recorded result."""
    pre = receipt.get("pins_pre")
    post = receipt.get("pins_post")
    recorded = receipt.get("pins_compare")
    if not isinstance(pre, dict) or not isinstance(post, dict):
        findings.append({
            "code": "missing_field",
            "where": "$.pins_pre/pins_post",
            "detail": "snapshots absent or not objects"})
        return 0
    try:
        recomputed = pins.compare(pre, post)
    except Exception as error:  # pins API or snapshot-shape failure
        findings.append({
            "code": "pins_compare_error",
            "where": "$.pins_compare",
            "error": f"{type(error).__name__}: {error}",
        })
        return 0
    checks = 1
    if not isinstance(recorded, dict):
        findings.append({
            "code": "missing_field", "where": "$.pins_compare"})
        return checks
    # pins.compare returns {equal, changed, missing, errors, *_taken_at_utc};
    # timestamps are instants, not recomputable — verify the four set fields.
    for field in ("equal", "changed", "missing", "errors"):
        exp = recomputed.get(field)
        got = recorded.get(field)
        if field in ("changed", "missing", "errors") and isinstance(exp, list):
            match = isinstance(got, list) and sorted(got) == sorted(exp)
        else:
            match = got == exp
        if not match:
            findings.append({
                "code": "pins_compare_mismatch",
                "where": f"$.pins_compare.{field}",
                "recorded": got,
                "recomputed": exp,
            })
    return checks


def validate_receipt(receipt, pins):
    """Validate one already-parsed receipt dict."""
    findings = []
    checks = 0
    kind = classify(receipt)
    checks += check_required(receipt, kind, findings)
    if kind == "carrier":
        checks += check_binding(receipt, findings)
    if pins is not None:
        checks += rerun_pins_compare(receipt, pins, findings)
    pre = receipt.get("pins_pre") if isinstance(receipt, dict) else None
    post = receipt.get("pins_post") if isinstance(receipt, dict) else None
    if isinstance(pre, dict):
        checks += verify_pin_entries(pre, post, "pins_pre", findings)
    if isinstance(post, dict):
        checks += verify_pin_entries(post, None, "pins_post", findings)
    if isinstance(receipt, dict):
        checks += walk_pairs(receipt, findings, "$", set())
    return {
        "kind": kind,
        "valid": not findings,
        "findings": findings,
        "checks_performed": checks,
    }


def validate_paths(paths, pins):
    """Validate every receipt path; returns (result_dict, exit_code)."""
    reports = []
    unreadable = 0
    invalid = 0
    for raw in paths:
        entry = {"receipt": raw}
        try:
            with open(raw, "r", encoding="utf-8") as handle:
                receipt = json.load(handle)
        except OSError as error:
            entry["status"] = "unreadable"
            entry["error"] = str(error)
            reports.append(entry)
            unreadable += 1
            continue
        except json.JSONDecodeError as error:
            entry["status"] = "unreadable"
            entry["error"] = f"invalid JSON: {error}"
            reports.append(entry)
            unreadable += 1
            continue
        result = validate_receipt(receipt, pins)
        result["status"] = "valid" if result["valid"] else "invalid"
        result.update(entry)
        reports.append(result)
        if not result["valid"]:
            invalid += 1
    if unreadable:
        code = 2
    elif invalid:
        code = 1
    else:
        code = 0
    return {
        "tool": "receipt-validate.py",
        "pins_available": pins is not None,
        "pins_path": str(PINS_PATH),
        "receipts": reports,
        "counts": {
            "receipts": len(paths),
            "valid": len(paths) - invalid - unreadable,
            "invalid": invalid,
            "unreadable": unreadable,
        },
        "exit": code,
    }, code


def emit(payload):
    print(json.dumps(payload, sort_keys=True, indent=2))


def _pins_triplet(pins, pin_path):
    """Snapshot `pin_path` twice (unchanged) and return the trio."""
    pre = pins.snapshot([str(pin_path)])
    post = pins.snapshot([str(pin_path)])
    return pre, post, pins.compare(pre, post)


def _retain_receipt(tmpdir, pins, pin_file, stdout_file, stderr_file):
    """Build a contract-shaped retain.py receipt over real files."""
    pre, post, compare = _pins_triplet(pins, pin_file)
    return {
        "argv": ["python3", "-c", "print(1)"],
        "cwd": str(tmpdir),
        "started_at_utc": utcnow(),
        "ended_at_utc": utcnow(),
        "exit": 0,
        "stdout_path": str(stdout_file),
        "stdout_sha256": sha256_file(stdout_file),
        "stderr_path": str(stderr_file),
        "stderr_sha256": sha256_file(stderr_file),
        "python": sys.version,
        "orig_argv": getattr(sys, "orig_argv", sys.argv),
        "pins_pre": pre,
        "pins_post": post,
        "pins_compare": compare,
    }


def _carrier_receipt(tmpdir, pins, carrier_file, log_file):
    """Build a minimal contract-shaped carrier-run.py receipt."""
    pre, post, compare = _pins_triplet(pins, carrier_file)
    log_sha = sha256_file(log_file)
    return {
        "label": "selftest-carrier",
        "carrier": {
            "path": str(carrier_file),
            "sha256_pre": sha256_file(carrier_file),
            "sha256_post": sha256_file(carrier_file),
        },
        "steps": {"inspect-go-binary": {
            "argv": ["npx", "-y", "rea-agents@6.5.0",
                     "inspect-go-binary", str(carrier_file),
                     "--format", "json"],
            "cwd": str(tmpdir),
            "started_at_utc": utcnow(),
            "ended_at_utc": utcnow(),
            "exit": 0,
            "stdout_path": str(log_file),
            "stdout_sha256": log_sha,
            "stderr_path": str(log_file),
            "stderr_sha256": log_sha,
        }},
        "bound_sessions": ["/tmp/rea-ghidra-selftest"],
        "retained_logs": [{
            "session_dir": "/tmp/rea-ghidra-selftest",
            "files": {"ghidra.log": {
                "path": str(log_file),
                "sha256": log_sha,
                "bytes": os.path.getsize(log_file),
            }},
            "polls": 3,
            "last_copy_utc": utcnow(),
        }],
        "pins_pre": pre,
        "pins_post": post,
        "pins_compare": compare,
        "python": sys.version,
        "orig_argv": getattr(sys, "orig_argv", sys.argv),
        "log_capture_limit": "polling copy",
    }


def selftest(pins):
    """Green retain receipt, green carrier receipt, tampered-file red,
    tampered pins_compare red, unreadable receipt. Exits 0/1."""
    cases = []

    def record(name, code, want, detail=""):
        cases.append({
            "case": name, "exit": code, "expected_exit": want,
            "ok": code == want, "detail": detail})

    if pins is None:
        print(f"SELFTEST: FAILED pins.py unavailable at {PINS_PATH}")
        return 1

    tmpdir = Path(tempfile.mkdtemp(prefix="receipt-validate-selftest-"))
    try:
        pin_file = tmpdir / "pinned.txt"
        pin_file.write_text("pinned bytes\n", encoding="utf-8")
        stdout_file = tmpdir / "capture.stdout"
        stdout_file.write_text("child stdout\n", encoding="utf-8")
        stderr_file = tmpdir / "capture.stderr"
        stderr_file.write_text("child stderr\n", encoding="utf-8")
        log_file = tmpdir / "ghidra.log"
        log_file.write_text("log line\n", encoding="utf-8")

        # Case 1: intact retain-shaped receipt -> exit 0.
        receipt1 = tmpdir / "r1.json"
        receipt1.write_text(json.dumps(
            _retain_receipt(tmpdir, pins, pin_file,
                            stdout_file, stderr_file)),
            encoding="utf-8")
        _out, code = validate_paths([str(receipt1)], pins)
        record("retain_green", code, 0)

        # Case 2: tampered pinned + captured file -> exit 1 naming path.
        pin_file.write_text("tampered bytes\n", encoding="utf-8")
        _out2, code = validate_paths([str(receipt1)], pins)
        detail = ""
        if _out2["receipts"]:
            detail = json.dumps(_out2["receipts"][0].get("findings", []))
        record("tampered_file_red", code, 1, detail)
        pin_file.write_text("pinned bytes\n", encoding="utf-8")

        # Case 3: tampered recorded pins_compare -> exit 1.
        receipt3 = tmpdir / "r3.json"
        data = _retain_receipt(tmpdir, pins, pin_file,
                               stdout_file, stderr_file)
        data["pins_compare"] = dict(data["pins_compare"])
        data["pins_compare"]["changed"] = ["/nonexistent/forged"]
        receipt3.write_text(json.dumps(data), encoding="utf-8")
        _out3, code = validate_paths([str(receipt3)], pins)
        record("pins_compare_forged_red", code, 1)

        # Case 4: intact producer-shaped (steps object) carrier receipt whose
        # bound log names its own session path and target prefix -> exit 0.
        sess = "/tmp/rea-ghidra-selftest"
        sha12 = sha256_file(pin_file)[:12]
        md5 = hashlib.md5(pin_file.read_bytes()).hexdigest()

        def good_log(prefix=sha12, md5v=md5, extra=""):
            return (f"2026-10-20 10:00:00 INFO  (LoggingInitialization) Using log file: {sess}/ghidra.log\n"
                    f"2026-10-20 10:00:01 INFO  (HeadlessAnalyzer) IMPORTING: file://{sess}/target-{prefix}.bin\n"
                    f"Loading file://{sess}/target-{prefix}.bin?MD5={md5v}...\n" + extra)
        log_file.write_text(good_log(), encoding="utf-8")
        receipt4 = tmpdir / "r4.json"
        receipt4.write_text(json.dumps(
            _carrier_receipt(tmpdir, pins, pin_file, log_file)),
            encoding="utf-8")
        _out4, code = validate_paths([str(receipt4)], pins)
        record("carrier_green", code, 0,
               json.dumps(_out4["receipts"][0].get("findings", [])
                          if _out4["receipts"] else []))

        # Case 4b: foreign log (other target prefix) with consistent digests -> 1.
        log_file.write_text(good_log(prefix="000000000000"), encoding="utf-8")
        receipt4b = tmpdir / "r4b.json"
        receipt4b.write_text(json.dumps(
            _carrier_receipt(tmpdir, pins, pin_file, log_file)),
            encoding="utf-8")
        _out4b, code = validate_paths([str(receipt4b)], pins)
        record("carrier_foreign_log_red", code, 1)

        # Case 4b2: right prefix, wrong full MD5 (prefix collision) -> 1;
        # binding needles only inside a stack trace -> 1.
        log_file.write_text(good_log(md5v="0" * 32), encoding="utf-8")
        receipt4d = tmpdir / "r4d.json"
        receipt4d.write_text(json.dumps(
            _carrier_receipt(tmpdir, pins, pin_file, log_file)), encoding="utf-8")
        _o, code = validate_paths([str(receipt4d)], pins)
        record("carrier_md5_collision_red", code, 1)
        log_file.write_text(
            f"\tat x(Using log file: {sess}/ghidra.log)\n"
            f"\tat y(IMPORTING: file://{sess}/target-{sha12}.bin)\n"
            f"Loading file://{sess}/target-{sha12}.bin?MD5={md5}...\n", encoding="utf-8")
        receipt4e = tmpdir / "r4e.json"
        receipt4e.write_text(json.dumps(
            _carrier_receipt(tmpdir, pins, pin_file, log_file)), encoding="utf-8")
        _o, code = validate_paths([str(receipt4e)], pins)
        record("carrier_stacktrace_needles_red", code, 1)

        # Case 4c: recorded mid-run pin drift -> 1.
        data = json.loads(receipt4.read_text(encoding="utf-8"))
        log_file.write_text(good_log(), encoding="utf-8")
        data = _carrier_receipt(tmpdir, pins, pin_file, log_file)
        data["steps"]["inspect-go-binary"]["pin_checks"] = [
            {"taken_at_utc": utcnow(), "equal": False}]
        receipt4c = tmpdir / "r4c.json"
        receipt4c.write_text(json.dumps(data), encoding="utf-8")
        _out4c, code = validate_paths([str(receipt4c)], pins)
        record("carrier_mid_run_drift_red", code, 1)

        # Case 5: unreadable receipt path -> exit 2.
        _out5, code = validate_paths(
            [str(tmpdir / "does-not-exist.json")], pins)
        record("unreadable_receipt", code, 2)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    failures = [c for c in cases if not c["ok"]]
    if failures:
        print("SELFTEST: FAILED " + json.dumps(cases, sort_keys=True))
        return 1
    print(f"SELFTEST: CLEAN cases={len(cases)}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Re-verify recorded receipt digests and pins "
        "compare against live files.")
    parser.add_argument("--selftest", action="store_true",
                        help="run built-in fixtures and exit")
    parser.add_argument("receipts", nargs="*", metavar="RECEIPT.json")
    args = parser.parse_args()

    pins = load_pins()
    if args.selftest:
        raise SystemExit(selftest(pins))
    if not args.receipts:
        parser.print_help(sys.stderr)
        raise SystemExit(2)
    if pins is None:
        emit({"tool": "receipt-validate.py",
              "error": f"pins.py unavailable at {PINS_PATH}",
              "exit": 2})
        raise SystemExit(2)
    out, code = validate_paths(args.receipts, pins)
    emit(out)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
