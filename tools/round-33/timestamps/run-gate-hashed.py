#!/usr/bin/env python3
"""Hash-bound allowance wrapper for evidence-timestamps.py.

Every allowance entry pins the SHA256 of the entire source line at the gated
revision (Git object bytes, LF delimiter excluded). The wrapper verifies all
pinned lines before forwarding any --allow. Any mismatch, missing path, or
missing line exits 1 with the stable code ``allowance_line_changed`` and runs
no gate, so an edited line cannot inherit an allowance. This keeps a frozen
stdout echo allowable while refusing an execution instant inserted into that
same line.

Usage:
  run-gate-hashed.py --root REPO --rev REV --path SCOPE --spec SPEC.json --out DIR
  run-gate-hashed.py --selftest
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
from datetime import datetime, timezone
from pathlib import PurePosixPath

HERE = os.path.dirname(os.path.realpath(__file__))
TOOL = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py"
SCRATCH_ROOT = "/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair"
SELFTEST_ASSETS = (
    "run-gate-hashed.py",
    "allowances-hashed.json",
    "build-hashed-fixture.sh",
    "run-hashed-selftest.sh",
)
SELFTEST_TIMEOUT = "600"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SCHEMA = "r33-hashed-allow-gate-v1"
DROP_ENV = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cleaned_env():
    return {key: value for key, value in os.environ.items() if key not in DROP_ENV}


def git(root, *args):
    return subprocess.run(
        ["git", "-C", root, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=cleaned_env(),
        check=False,
    )


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def write_bytes(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as stream:
        stream.write(data)


def dump_json(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def fail(code, out, message, extra=None, exit_code=2):
    error = {"code": code, "message": message}
    if extra:
        error.update(extra)
    payload = {"schema": SCHEMA, "tool_run": False, "error": error}
    if out:
        os.makedirs(out, exist_ok=True)
        write_bytes(os.path.join(out, "stdout.json"), (dump_json(payload) + "\n").encode("ascii"))
        write_bytes(os.path.join(out, "stderr.txt"), b"")
        write_bytes(os.path.join(out, "receipt.txt"),
                    f"utc_start={utc_now()}\nexit={exit_code}\ntool_run=false\n".encode("ascii"))
    sys.stdout.write(dump_json(payload) + "\n")
    return exit_code


def validate_scope(raw):
    if not raw:
        raise ValueError("--path must name a repository-relative path")
    if raw.startswith("/"):
        raise ValueError("--path must be repository-relative")
    path = PurePosixPath(raw)
    if ".." in path.parts:
        raise ValueError("--path may not contain '..'")
    return str(path) or "."


def validate_entry(entry, index):
    if not isinstance(entry, dict):
        raise ValueError(f"allow[{index}] must be an object")
    name = entry.get("file")
    line = entry.get("line")
    digest = entry.get("line_sha256")
    if not isinstance(name, str) or not name:
        raise ValueError(f"allow[{index}].file must be a non-empty string")
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or str(path) in ("", "."):
        raise ValueError(f"allow[{index}].file must be repository-relative")
    if not isinstance(line, int) or isinstance(line, bool) or line < 1:
        raise ValueError(f"allow[{index}].line must be a positive integer")
    if not isinstance(digest, str) or not HEX64.fullmatch(digest):
        raise ValueError(f"allow[{index}].line_sha256 must be 64 lowercase hex characters")
    return str(path), line, digest


def run_selftest():
    """Run the clone selftest from a unique scratch copy; never write beside this script."""
    missing = [name for name in SELFTEST_ASSETS if not os.path.isfile(os.path.join(HERE, name))]
    if missing:
        sys.stdout.write(dump_json({"schema": SCHEMA, "tool_run": False,
                                    "error": {"code": "selftest_assets_missing",
                                              "message": "missing: " + ", ".join(missing)}}) + "\n")
        return 2
    try:
        os.makedirs(SCRATCH_ROOT, exist_ok=True)
        tempdir = tempfile.mkdtemp(prefix="selftest-", dir=SCRATCH_ROOT)
    except OSError as exc:
        return fail("selftest_scratch_unavailable", None, str(exc))
    try:
        for name in SELFTEST_ASSETS:
            shutil.copy2(os.path.join(HERE, name), os.path.join(tempdir, name))
        result = subprocess.run(
            ["timeout", SELFTEST_TIMEOUT, "bash", os.path.join(tempdir, "run-hashed-selftest.sh")],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=cleaned_env(), check=False)
        sys.stdout.buffer.write(result.stdout)
        sys.stdout.buffer.flush()
        if result.stderr:
            sys.stderr.buffer.write(result.stderr)
            sys.stderr.buffer.flush()
        if result.returncode == 124:
            sys.stderr.write("selftest exceeded 600s; temporary fixture removed\n")
        return result.returncode
    finally:
        shutil.rmtree(tempdir, ignore_errors=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true",
                        help="run the bounded clone selftest (green echo, same-line red, unlisted red)")
    parser.add_argument("--root", help="repository root")
    parser.add_argument("--rev", help="commit revision to gate")
    parser.add_argument("--path", help="repository-relative evidence scope")
    parser.add_argument("--spec", help="hash-bound allowance JSON")
    parser.add_argument("--out", help="directory for stdout/stderr/receipt")
    args = parser.parse_args(argv)

    if args.selftest:
        return run_selftest()

    missing = [flag for flag, value in (("--root", args.root), ("--rev", args.rev),
                                        ("--path", args.path), ("--spec", args.spec),
                                        ("--out", args.out)) if not value]
    if missing:
        sys.stdout.write(dump_json({"schema": SCHEMA, "tool_run": False,
                                    "error": {"code": "arguments_missing",
                                              "message": "required arguments: " + ", ".join(missing)}}) + "\n")
        return 2

    try:
        scope = validate_scope(args.path)
    except ValueError as exc:
        return fail("spec_invalid", args.out, str(exc))

    root = os.path.realpath(os.path.abspath(args.root))
    if not os.path.isdir(root):
        return fail("root_unavailable", args.out, f"--root is not a directory: {root}")

    try:
        with open(args.spec, "rb") as stream:
            spec = json.loads(stream.read().decode("utf-8"))
    except (OSError, ValueError) as exc:
        return fail("spec_unreadable", args.out, str(exc))

    if not isinstance(spec, dict) or spec.get("schema") != SCHEMA:
        return fail("spec_invalid", args.out, f"spec schema must be {SCHEMA}")
    if spec.get("scope") != scope:
        return fail("spec_scope_mismatch", args.out,
                    f"spec scope {spec.get('scope')!r} != --path {scope!r}")
    entries = spec.get("allow")
    if not isinstance(entries, list):
        return fail("spec_invalid", args.out, "spec allow must be a list")

    checked = []
    try:
        for index, entry in enumerate(entries):
            name, line, digest = validate_entry(entry, index)
            checked.append((index, name, line, digest, entry.get("tokens")))
    except ValueError as exc:
        return fail("spec_invalid", args.out, str(exc))

    resolved_proc = git(root, "rev-parse", "--verify", "--quiet", "--end-of-options",
                        args.rev + "^{commit}")
    resolved = resolved_proc.stdout.decode("ascii", "replace").strip()
    if resolved_proc.returncode or not re.fullmatch(r"[0-9a-f]{40,64}", resolved):
        return fail("revision_invalid", args.out, "Git did not resolve --rev to a commit")

    verified = []
    for index, name, line, digest, tokens in checked:
        tree_path = name if scope == "." else f"{scope}/{name}"
        blob_proc = git(root, "cat-file", "blob", f"{resolved}:{tree_path}")
        if blob_proc.returncode:
            return fail("allowance_line_changed", args.out,
                        f"{name}:{line} does not resolve to a blob at {resolved}",
                        {"file": name, "line": line, "expected_sha256": digest,
                         "actual_sha256": None, "detail": "path_missing",
                         "verified_before_failure": [item["file"] + ":" + str(item["line"]) for item in verified]},
                        exit_code=1)
        lines = blob_proc.stdout.split(b"\n")
        if line > len(lines):
            return fail("allowance_line_changed", args.out,
                        f"{name}:{line} is past the end of the blob at {resolved}",
                        {"file": name, "line": line, "expected_sha256": digest,
                         "actual_sha256": None, "detail": "line_missing",
                         "verified_before_failure": [item["file"] + ":" + str(item["line"]) for item in verified]},
                        exit_code=1)
        actual = sha256_bytes(lines[line - 1])
        if actual != digest:
            return fail("allowance_line_changed", args.out,
                        f"{name}:{line} changed at {resolved}; no allowance forwarded",
                        {"file": name, "line": line, "expected_sha256": digest,
                         "actual_sha256": actual, "detail": "line_hash_mismatch",
                         "verified_before_failure": [item["file"] + ":" + str(item["line"]) for item in verified]},
                        exit_code=1)
        verified.append({"file": name, "line": line, "line_sha256": actual, "tokens": tokens})

    tool_argv = ["env", "-u", "GIT_DIR", "-u", "GIT_WORK_TREE", "-u", "GIT_INDEX_FILE",
                 "python3", "-I", "-B", TOOL, "--root", root, "--rev", resolved,
                 "--path", scope, "--strict"]
    for item in verified:
        tool_argv.extend(["--allow", f'{item["file"]}:{item["line"]}'])

    env = cleaned_env()
    os.makedirs(args.out, exist_ok=True)
    started = utc_now()
    result = subprocess.run(tool_argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env=env, check=False)
    ended = utc_now()

    write_bytes(os.path.join(args.out, "stdout.json"), result.stdout)
    write_bytes(os.path.join(args.out, "stderr.txt"), result.stderr)
    tool_sha = sha256_bytes(open(TOOL, "rb").read())
    spec_sha = sha256_bytes(open(args.spec, "rb").read())
    receipt = [
        f"utc_start={started}",
        "argv=" + dump_json(tool_argv),
        f"exit={result.returncode}",
        f"utc_end={ended}",
        f"tool={TOOL}",
        f"tool_sha256={tool_sha}",
        f"spec={os.path.abspath(args.spec)}",
        f"spec_sha256={spec_sha}",
        f"root={root}",
        f"resolved_rev={resolved}",
        "verified_lines=" + dump_json(verified),
        "allow_forwarded=" + dump_json([f'{item["file"]}:{item["line"]}' for item in verified]),
        f"stdout_bytes={len(result.stdout)} stderr_bytes={len(result.stderr)}",
    ]
    write_bytes(os.path.join(args.out, "receipt.txt"),
                ("\n".join(receipt) + "\n").encode("utf-8"))

    sys.stdout.buffer.write(result.stdout)
    sys.stdout.buffer.flush()
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
