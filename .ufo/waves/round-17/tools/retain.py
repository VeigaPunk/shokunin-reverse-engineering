#!/usr/bin/env python3
"""retain.py -- generic retained execution: run one argv, keep the receipt.

    retain.py --out RECEIPT.json [--pin PATH]... [--cwd DIR] [--timeout S] -- ARGV...

Takes pre-pins, runs ARGV (no shell), captures the child's stdout/stderr to
RECEIPT.stdout / RECEIPT.stderr next to the receipt, takes post-pins, and
writes a receipt JSON {argv, cwd, started_at_utc, ended_at_utc, exit,
stdout_path, stdout_sha256, stderr_path, stderr_sha256, python, orig_argv,
pins_pre, pins_post, pins_compare}.

Exit: 0 if the child ran (any child exit is recorded, not propagated) and the
pins compare equal; 1 if pins differ; 2 if the child could not start or timed
out, or on bad input (missing pins.py, unreadable --out dir, missing ARGV).

Pins prove only "same bytes at two instants" (pre vs post), never "unchanged
throughout the run"; see pins.py --help for the same caveat.

Selftest: `retain.py --selftest` builds its own fixtures under
tempfile.mkdtemp(), exercises clean / pins-differ / timeout cases using only
`python3 -c` children, removes the fixtures, prints
`SELFTEST: CLEAN cases=N` or `SELFTEST: FAILED ...`, exits 0/1.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

PINS_PATH = Path(__file__).resolve().parent / "pins.py"


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_pins():
    """Import the sibling pins.py by absolute path (contract section retain.py)."""
    if not PINS_PATH.is_file():
        return None
    spec = importlib.util.spec_from_file_location("pins", PINS_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json_atomic(path, payload):
    tmp = path.parent / (path.name + ".tmp")
    tmp.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(tmp, path)


def emit(payload):
    print(json.dumps(payload, sort_keys=True, indent=2))


def run(argv_list, cwd, timeout, out_path, pin_paths):
    """Execute one retained run; return (receipt, tool_exit_code)."""
    receipt_path = out_path.resolve()
    stdout_path = Path(str(receipt_path) + ".stdout")
    stderr_path = Path(str(receipt_path) + ".stderr")

    pins = load_pins()
    if pins is None:
        emit({
            "error": f"pins.py not found at {PINS_PATH}",
            "receipt_path": str(receipt_path),
        })
        return None, 2

    try:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_handle = open(stdout_path, "wb")
        stderr_handle = open(stderr_path, "wb")
    except OSError as error:
        emit({"error": f"cannot open capture files: {error}",
              "receipt_path": str(receipt_path)})
        return None, 2

    child_cwd = str(Path(cwd).resolve()) if cwd else os.getcwd()
    timed_out = False
    spawn_error = None
    child_exit = None

    with stdout_handle, stderr_handle:
        pins_pre = pins.snapshot(pin_paths)
        started_at = utcnow()
        try:
            child = subprocess.Popen(
                argv_list,
                cwd=child_cwd,
                stdout=stdout_handle,
                stderr=stderr_handle,
                shell=False,
            )
        except OSError as error:
            spawn_error = str(error)
        else:
            try:
                child.wait(timeout=timeout)
                child_exit = child.returncode
            except subprocess.TimeoutExpired:
                timed_out = True
                child.kill()
                child.wait()
                child_exit = child.returncode
        ended_at = utcnow()
        pins_post = pins.snapshot(pin_paths)

    pins_compare = pins.compare(pins_pre, pins_post)
    receipt = {
        "argv": argv_list,
        "cwd": child_cwd,
        "started_at_utc": started_at,
        "ended_at_utc": ended_at,
        "exit": child_exit,
        "stdout_path": str(stdout_path),
        "stdout_sha256": sha256_file(stdout_path),
        "stderr_path": str(stderr_path),
        "stderr_sha256": sha256_file(stderr_path),
        "python": sys.version,
        "orig_argv": getattr(sys, "orig_argv", sys.argv),
        "pins_pre": pins_pre,
        "pins_post": pins_post,
        "pins_compare": pins_compare,
    }
    if timed_out:
        receipt["timed_out"] = True
    if spawn_error is not None:
        receipt["spawn_error"] = spawn_error
    write_json_atomic(receipt_path, receipt)

    if spawn_error is not None or timed_out:
        code = 2
    elif not pins_compare.get("equal", False):
        code = 1
    else:
        code = 0
    emit({
        "receipt_path": str(receipt_path),
        "child_exit": child_exit,
        "timed_out": timed_out,
        "spawn_error": spawn_error,
        "pins_equal": pins_compare.get("equal", False),
        "exit": code,
    })
    return receipt, code


def parse_args(raw):
    """Split CLI on the first `--`; contract forbids argparse.REMAINDER quirks."""
    if "--selftest" in raw:
        return "selftest", None
    try:
        sep = raw.index("--")
    except ValueError:
        emit({"error": "missing `-- ARGV...` separator"})
        raise SystemExit(2)
    head, child_argv = raw[:sep], raw[sep + 1:]
    parser = argparse.ArgumentParser(
        prog="retain.py",
        description="Run one argv with pre/post pins and a retained receipt.",
    )
    parser.add_argument("--out", required=True, help="receipt JSON path")
    parser.add_argument("--pin", action="append", default=[],
                        help="path to pin pre/post; repeatable")
    parser.add_argument("--cwd", default=None, help="child working directory")
    parser.add_argument("--timeout", type=float, default=None,
                        help="child timeout in seconds")
    args = parser.parse_args(head)
    if not child_argv:
        emit({"error": "empty child argv after `--`"})
        raise SystemExit(2)
    return "run", (args, child_argv)


def selftest():
    """Exercise clean / pins-differ / timeout cases via `python3 -c` children."""
    tmp = Path(tempfile.mkdtemp(prefix="retain-selftest-"))
    cases = 0
    failures = []
    py = sys.executable  # python3; children are `<python3> -c <code>` only

    def check(name, args_list, child_argv, want_exit, verify=None):
        nonlocal cases
        cases += 1
        receipt, code = run(child_argv, args_list.cwd, args_list.timeout,
                            Path(args_list.out), args_list.pin)
        if code != want_exit:
            failures.append(f"{name}: exit {code} != {want_exit}")
            return
        if verify is not None and not verify(receipt):
            failures.append(f"{name}: receipt verification failed")

    ns = argparse.Namespace

    # Case 1 (clean): child exits 3, pinned file untouched -> tool exit 0.
    pinned = tmp / "pinned.bin"
    pinned.write_bytes(b"stable-bytes")
    check(
        "clean",
        ns(out=str(tmp / "clean.json"), pin=[str(pinned)], cwd=str(tmp),
           timeout=30.0),
        [py, "-c", "import sys; print('ok'); sys.exit(3)"],
        0,
        lambda r: r is not None and r["exit"] == 3
        and r["pins_compare"]["equal"] is True
        and r["argv"][1] == "-c"
        and Path(r["stdout_path"]).read_bytes() == b"ok\n",
    )

    # Case 2 (red): child mutates the pinned file -> tool exit 1.
    check(
        "pins-differ",
        ns(out=str(tmp / "red.json"), pin=[str(pinned)], cwd=str(tmp),
           timeout=30.0),
        [py, "-c", f"open({str(pinned)!r}, 'wb').write(b'mutated')"],
        1,
        lambda r: r is not None and r["exit"] == 0
        and r["pins_compare"]["equal"] is False
        and str(pinned) in r["pins_compare"]["changed"],
    )

    # Case 3 (timeout): child sleeps past --timeout -> tool exit 2, timed_out.
    check(
        "timeout",
        ns(out=str(tmp / "timeout.json"), pin=[], cwd=str(tmp), timeout=1.0),
        [py, "-c", "import time; time.sleep(30)"],
        2,
        lambda r: r is not None and r.get("timed_out") is True,
    )

    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    if failures:
        print("SELFTEST: FAILED " + "; ".join(failures))
        return 1
    print(f"SELFTEST: CLEAN cases={cases}")
    return 0


def main():
    mode, payload = parse_args(sys.argv[1:])
    if mode == "selftest":
        raise SystemExit(selftest())
    args, child_argv = payload
    _receipt, code = run(child_argv, args.cwd, args.timeout,
                         Path(args.out), args.pin)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
