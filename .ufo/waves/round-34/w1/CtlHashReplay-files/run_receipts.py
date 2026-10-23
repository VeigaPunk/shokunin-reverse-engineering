#!/usr/bin/env python3
"""Run every CtlHashReplay probe and record an exact receipt.

For each probe: exact argv, observed UTC start/end, exit code, stdout and
stderr bytes (SHA256 + captured to files), and the SHA256 of every artifact
touched. Nothing here runs the production reader
(tools/round-34/elf-version-needs.py) and nothing authors a binary fixture.

The production-reader prohibition is enforced mechanically here: the argv of
every probe is checked against a deny list before it runs.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "controls" / "round-34" / "receipts"
FREEZE = "54a87a51a865ab931fd355e767303337b05cccf4"
COUNTER = "tools/round-34/version-needs-counter.py"
READER = "controls/round-34/ctl-hash-replay.py"
DENY = ("elf-version-needs.py",)


def utc():
    return subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], stdout=subprocess.PIPE,
                          check=True).stdout.decode().strip()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(name, argv, timeout=180):
    for token in DENY:
        if any(token in part for part in argv):
            raise SystemExit("denied_probe:" + token)
    OUT.mkdir(parents=True, exist_ok=True)
    started = utc()
    try:
        done = subprocess.run(argv, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        code, out, err = done.returncode, done.stdout, done.stderr
        timed_out = False
    except subprocess.TimeoutExpired:
        code, out, err, timed_out = None, b"", b"", True
    ended = utc()
    (OUT / (name + ".stdout")).write_bytes(out)
    (OUT / (name + ".stderr")).write_bytes(err)
    return {
        "name": name,
        "argv": argv,
        "cwd": str(ROOT),
        "utc_start": started,
        "utc_end": ended,
        "exit": code,
        "timed_out": timed_out,
        "stdout_bytes": len(out),
        "stdout_sha256": sha(out),
        "stderr_bytes": len(err),
        "stderr_sha256": sha(err),
        "stdout_path": str((OUT / (name + ".stdout")).relative_to(ROOT)),
        "stderr_path": str((OUT / (name + ".stderr")).relative_to(ROOT)),
    }


def main():
    counter = ["python3", "-I", "-B", COUNTER]
    root_flag = ["--root", str(ROOT)]
    rev_freeze = ["--rev", FREEZE, "--freeze", FREEZE]
    probes = [
        ("ctl-hash-replay-run1", counter + root_flag + rev_freeze + ["--control-reader", READER]),
        ("ctl-hash-replay-run2", counter + root_flag + rev_freeze + ["--control-reader", READER]),
        ("ctl-hash-replay-run3", counter + root_flag + rev_freeze + ["--control-reader", READER]),
        ("counter-selftest", counter + ["--selftest"]),
        ("table-fidelity", ["python3", "-I", "-B", "controls/round-34/check_table_fidelity.py"]),
        ("reader-access-audit-e01", ["python3", "-I", "-B", "controls/round-34/audit_reader_access.py", READER,
                                     "corpus/evidence/round-34/elf/e01.bin"]),
        ("reader-access-audit-e12", ["python3", "-I", "-B", "controls/round-34/audit_reader_access.py", READER,
                                     "corpus/evidence/round-34/elf/e12.bin"]),
        ("degenerate-empty-baseline", counter + root_flag + rev_freeze +
         ["--control-reader", "controls/round-34/ctl-degenerate-empty.py"]),
        ("author-schedule-miss", ["python3", "-I", "-B", "controls/round-34/check_author_schedule_miss.py"]),
    ]
    records = [run(name, argv) for name, argv in probes]
    for record in records:
        out = (ROOT / record["stdout_path"]).read_bytes()
        try:
            parsed = json.loads(out)
            record["result_summary"] = {k: parsed[k] for k in
                                         ("matched", "target", "met_target", "finding", "mode", "documents_ok",
                                          "passed", "total", "all_miss", "mutants", "table_size",
                                          "every_carrier_present", "every_table_value_equals_frozen_expected",
                                          "every_probe_digest_misses", "table_keys_equal_manifest_digests",
                                          "elf_interpretation_tokens_in_source")
                                         if k in parsed}
            if "rows" in parsed and all("matched" in row and "attempts" in row for row in parsed["rows"]):
                record["result_summary"]["per_row"] = [
                    {"id": row["id"],
                     "matched": row["matched"],
                     "schedules": [{"schedule": a["schedule"], "exit": a["exit"], "matched": a["matched"],
                                    "input_sha256": a.get("input_sha256"),
                                    "string_translation_present": a.get("string_translation") is not None}
                                   for a in row["attempts"]]}
                    for row in parsed["rows"]]
        except ValueError:
            record["result_summary"] = {"non_json_stdout": True}
    artifacts = {}
    for path in sorted((ROOT / "controls" / "round-34").rglob("*")):
        if path.is_file():
            artifacts[str(path.relative_to(ROOT))] = {"sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}
    report = {
        "kind": "ctl_hash_replay_receipts",
        "seat": "CtlHashReplay",
        "freeze": FREEZE,
        "sandbox_root": str(ROOT),
        "production_reader_run": False,
        "binary_fixture_authored": False,
        "deny_list": list(DENY),
        "probes": records,
        "artifacts": artifacts,
    }
    (OUT / "receipts.json").write_text(json.dumps(report, sort_keys=True, indent=1))
    print(json.dumps(report, sort_keys=True, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
