#!/usr/bin/env python3
"""Record one existing CLI selftest; never import or author fixture recipes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
if len(sys.argv) != 3 or sys.argv[1] not in ("count", "metadata", "tag") or sys.argv[2] not in ("pristine", "mutated", "restored"):
    raise SystemExit("usage: run_probe.py {count|metadata|tag} {pristine|mutated|restored}")
kind, phase = sys.argv[1:]
work = ROOT / kind
parser = work / "chpe_profile.py"
sibling = work / "selftest_pegen.py"
pristine = (ROOT / "chpe_profile.py.pristine").read_bytes()
pristine_sibling = (ROOT / "selftest_pegen.py.pristine").read_bytes()
expected = json.loads((ROOT / "inputs.json").read_text())["source"]
assert hashlib.sha256(pristine).hexdigest() == expected["chpe_profile.py"]["sha256"]
assert hashlib.sha256(pristine_sibling).hexdigest() == expected["selftest_pegen.py"]["sha256"]

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def hashes():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (parser, sibling)}

argv = ["/usr/bin/timeout", "--signal=TERM", "--kill-after=2s", "30s",
        "/usr/bin/prlimit", "--as=268435456", "--cpu=20", "--fsize=1048575",
        "--nproc=8192", "--nofile=128", "--core=0", "--",
        "/usr/bin/python3", "-I", "-B", str(parser), "--selftest"]
env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
env.update(TMPDIR=str(work / "tmp"), LC_ALL="C.UTF-8")
receipt = {"kind": kind, "phase": phase, "argv": argv, "cwd": str(work),
           "environment_overrides": {k: env[k] for k in ("TMPDIR", "LC_ALL")},
           "start_utc": utc(), "source_before": hashes(), "python": sys.version,
           "wall_limit_seconds": 30, "kill_grace_seconds": 2,
           "supervisor_limit_seconds": 35, "source_derived_cli_launch_max": 107,
           "detector_cli_concurrency_max": 1, "nproc_is_per_uid_not_tree_quota": True}
start = time.monotonic()
proc = None
try:
    assert sibling.read_bytes() == pristine_sibling
    if phase != "mutated":
        assert parser.read_bytes() == pristine
    (work / "tmp").mkdir(exist_ok=True)
    with (work / (phase + ".stdout")).open("wb") as stdout, (work / (phase + ".stderr")).open("wb") as stderr:
        proc = subprocess.Popen(argv, cwd=work, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        receipt["process_group"] = proc.pid
        try:
            receipt["exit"] = proc.wait(timeout=35)
        except subprocess.TimeoutExpired:
            receipt["supervisor_timeout"] = True
            os.killpg(proc.pid, signal.SIGKILL)
            receipt["exit"] = proc.wait(timeout=3)
except Exception as exc:
    receipt["recorder_error"] = repr(exc)
finally:
    if proc is not None:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
            receipt["cleanup_signal"] = "SIGKILL sent to owned process group"
        except ProcessLookupError:
            receipt["cleanup_signal"] = "ESRCH: owned group already absent"
        if proc.poll() is None:
            proc.wait(timeout=3)
        try:
            os.killpg(proc.pid, 0)
            receipt["owned_group_absent_after_cleanup"] = False
        except ProcessLookupError:
            receipt["owned_group_absent_after_cleanup"] = True
    receipt["source_after_detector"] = hashes()
    if phase == "mutated":
        parser.write_bytes(pristine)
        receipt["restored_in_finally_utc"] = utc()
    receipt["source_final"] = hashes()
    receipt["parser_exact_pristine_final"] = parser.read_bytes() == pristine
    receipt["sibling_exact_pristine_final"] = sibling.read_bytes() == pristine_sibling
    receipt["end_utc"] = utc()
    receipt["elapsed_seconds"] = time.monotonic() - start

for stream in ("stdout", "stderr"):
    path = work / (phase + "." + stream)
    data = path.read_bytes() if path.exists() else b""
    receipt[stream] = {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    if stream == "stdout" and data:
        try:
            summary = json.loads(data)
            receipt["selftest_summary"] = {k: v for k, v in summary.items() if k != "results"}
        except json.JSONDecodeError as exc:
            receipt["stdout_json_error"] = str(exc)
receipt_path = work / (phase + ".receipt.json")
receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, sort_keys=True))
raise SystemExit(0 if "recorder_error" not in receipt and receipt.get("owned_group_absent_after_cleanup", False) else 2)
