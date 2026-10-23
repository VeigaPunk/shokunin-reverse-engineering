#!/usr/bin/env python3
"""Same bounded text-only behavioral detector for all three counter states."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
COUNTER = ROOT / "tools/round-34/version-needs-counter.py"
FREEZE = "54a87a51a865ab931fd355e767303337b05cccf4"
phase = sys.argv[1]
assert phase in {"pristine", "mutated", "restored"}
setup = json.loads((BASE / "setup.json").read_text())
spec = json.loads((BASE / "spec.json").read_text())
fixture_row = spec["manifest"]["carriers"][0]
original = (BASE / "fixture.txt").read_bytes()
alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def store(name, data):
    if isinstance(data, str):
        data = data.encode("ascii")
    assert len(data) <= 524288
    path = BASE / name
    assert not path.exists(), "evidence_already_exists"
    path.write_bytes(data)
    return {"path": name, "size": len(data), "sha256": digest(data)}


def audits(result, label):
    row = result["rows"][0]
    attempts = row["attempts"]
    assert len(attempts) == 2
    assert attempts[0]["input_sha256"] == digest(original)
    assert attempts[0]["string_translation"] is None
    translation = bytes.fromhex(attempts[1]["string_translation"])
    assert len(translation) == 256
    table = fixture_row["string_table"]
    start, end = table["offset"], table["offset"] + table["size"]
    candidate = original[:start] + original[start:end].translate(translation) + original[end:]
    candidate_receipt = store(phase + "." + label + ".schedule1.txt", candidate)
    prediction = json.loads(json.dumps(fixture_row["expected"]))
    renamed_files_in_original_order = []
    renamed_versions_in_original_order = []
    for record in prediction["needed"]:
        record["file"] = record["file"].encode("ascii").translate(translation).decode("ascii")
        renamed_files_in_original_order.append(record["file"])
        for version in record["versions"]:
            version["name"] = version["name"].encode("ascii").translate(translation).decode("ascii")
            renamed_versions_in_original_order.append((version["name"], version["other"]))
        record["versions"].sort(key=lambda version: (version["name"], version["other"]))
    prediction["needed"].sort(key=lambda record: record["file"])
    expected_hashes = sorted((version["other"], version["hash"], version["flags"]) for record in fixture_row["expected"]["needed"] for version in record["versions"])
    observed = attempts[1]["observed"]
    observed_hashes = sorted((version["other"], version["hash"], version["flags"]) for record in observed["needed"] for version in record["versions"])
    suffix_aliases = all(candidate[start + index * 3 + 1:start + index * 3 + 3] == bytes([translation[letter], 0]) for index, letter in enumerate(sorted(alphabet)))
    return {
        "all_alphabet_bytes_changed": all(translation[byte] != byte for byte in alphabet),
        "alphabet_bijection": set(translation[byte] for byte in alphabet) == set(alphabet),
        "all_other_bytes_identity": all(translation[byte] == byte for byte in range(256) if byte not in alphabet),
        "same_length": len(candidate) == len(original),
        "outside_table_unchanged": candidate[:start] == original[:start] and candidate[end:] == original[end:],
        "input_hash_matches_retained_text": attempts[1]["input_sha256"] == digest(candidate),
        "original_hash_replay_key_changed": digest(candidate) != digest(original),
        "suffix_aliases_preserved": suffix_aliases,
        "file_sort_reversal_present": renamed_files_in_original_order != sorted(renamed_files_in_original_order),
        "version_sort_reversal_present": renamed_versions_in_original_order != sorted(renamed_versions_in_original_order),
        "observed_matches_independent_translation": observed == prediction,
        "recorded_hash_flags_other_preserved": observed_hashes == expected_hashes,
        "candidate": candidate_receipt,
    }


runs = []
for label, reader in (("byte", "byte_reader.py"), ("replay", "original_hash_replay.py")):
    argv = [
        "timeout", "--signal=TERM", "--kill-after=2s", "25s",
        "prlimit", "--as=536870912", "--nproc=4096", "--cpu=20",
        sys.executable, "-I", "-B", str(COUNTER),
        "--root", str(ROOT), "--rev", FREEZE, "--freeze", FREEZE,
        "--fixture-spec", str(BASE / "spec.json"),
        "--fixture-reader", str(BASE / reader),
    ]
    started = datetime.now(timezone.utc).isoformat()
    run = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, cwd=ROOT)
    finished = datetime.now(timezone.utc).isoformat()
    stdout = store(phase + "." + label + ".stdout.json", run.stdout)
    stderr = store(phase + "." + label + ".stderr.txt", run.stderr)
    result = json.loads(run.stdout)
    runs.append({
        "label": label,
        "observed_utc": started,
        "finished_utc": finished,
        "argv": argv,
        "exit": run.returncode,
        "stdout": run.stdout.decode("ascii"),
        "stderr": run.stderr.decode("ascii"),
        "stdout_receipt": stdout,
        "stderr_receipt": stderr,
        "summary": {"matched": result["matched"], "target": result["target"], "met_target": result["met_target"], "finding": result["finding"], "schedules": [{"schedule": attempt["schedule"], "exit": attempt["exit"], "matched": attempt["matched"], "input_sha256": attempt["input_sha256"]} for attempt in result["rows"][0]["attempts"]]},
        "audits": audits(result, label),
    })
byte, replay = runs
behavior_checks = {
    "byte_reader_succeeds_both_schedules": byte["exit"] == 0 and byte["summary"]["met_target"] and all(attempt["matched"] for attempt in byte["summary"]["schedules"]),
    "byte_independent_translation_and_hash_checks": all(value for key, value in byte["audits"].items() if key != "candidate"),
    "replay_rejected_only_after_translation": replay["exit"] == 1 and not replay["summary"]["met_target"] and [attempt["matched"] for attempt in replay["summary"]["schedules"]] == [True, False],
    "replay_translation_is_nonidentity": replay["audits"]["original_hash_replay_key_changed"],
}
passed = all(behavior_checks.values())
code_bytes = COUNTER.read_bytes()
code_receipt = store("counter." + phase + ".snapshot.py", code_bytes)
result = {
    "kind": "isolated_text_mutation_detector_not_production_score",
    "phase": phase,
    "detector_argv": sys.orig_argv,
    "observed_utc": datetime.now(timezone.utc).isoformat(),
    "measured_revision": setup["measured_revision"],
    "freeze_revision": FREEZE,
    "code": code_receipt,
    "fixture_sha256": digest(original),
    "behavior_checks": behavior_checks,
    "detector_passed": passed,
    "detector_exit": 0 if passed else 1,
    "runs": runs,
}
store(phase + ".json", json.dumps(result, sort_keys=True, indent=2) + "\n")
print(json.dumps({key: value for key, value in result.items() if key != "runs"}, sort_keys=True))
for item in runs:
    print(json.dumps({"label": item["label"], "exit": item["exit"], **item["summary"], "audits": item["audits"]}, sort_keys=True))
raise SystemExit(0 if passed else 1)
