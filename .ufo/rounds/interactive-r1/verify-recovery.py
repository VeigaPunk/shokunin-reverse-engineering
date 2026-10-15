#!/usr/bin/env python3
"""Validate this round's pinned evidence package, not semantic truth or admission."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = Path("evidence/round-1-2026-10-15/result.json")


class Finding(Exception):
    def __init__(self, code, name):
        self.code, self.name = code, name


def require(condition, name, code=1):
    if not condition:
        raise Finding(code, name)


def load(path):
    return json.loads(path.read_text())


def check(root, expected, admission=False):
    for path, digest in expected["snapshots"].items():
        file = root / path
        require(file.is_file(), "snapshot_missing", 2)
        require(hashlib.sha256(file.read_bytes()).hexdigest() == digest,
                "snapshot_tampered", 2)
    require((root / RESULT).is_file(), "missing_result", 2)
    result = load(root / RESULT)
    require(result["baseline_revision"] == expected["baseline_revision"]
            and result["measured_revision"] == expected["measured_revision"],
            "revision_mismatch")
    obligations = result["obligations"]
    ids = [row["id"] for row in obligations]
    require(sorted(ids) == expected["obligation_ids"], "obligation_set_mismatch")
    require(all(row["status"] == "aligned" and row["reviewer"] == "L1-author"
                and row["source_review"] for row in obligations), "review_incomplete")
    require(result["admitted"] is False and result["verified_round_increment"] == 0
            and result["outside_spot_check"] is False, "unearned_admission")
    require(result["smoke"]["subject_sha256"] == expected["smoke"]["subject_sha256"],
            "subject_mismatch")
    bundle = load(root / expected["bundle_path"])
    records = [r for r in bundle["records"]
               if r["evidence_id"] == expected["smoke"]["evidence_id"]]
    require(len(records) == 1, "smoke_record_mismatch")
    record = records[0]
    require(record["subject"]["digest"]["sha256"] == result["smoke"]["subject_sha256"]
            and record["subject"]["local_path"] == expected["smoke"]["path"],
            "subject_mismatch")
    require(record["operation"] == "inspect_native_instruction"
            and record["parameters"]["address"] == "0x117070"
            and record["confidence"] == "observed"
            and record["authority"] == "shipped-artifact", "smoke_authority_mismatch")
    instruction = record["normalized_result"]
    require(instruction["status"] == "decoded" and instruction["bytes"] == "f30f1efa"
            and instruction["length"] == 4 and instruction["mnemonic"] == "ENDBR64",
            "smoke_instruction_mismatch")
    measurements = load(root / expected["measurements_path"])
    for stage in ("baseline", "after"):
        require(measurements[stage] == expected["controls"][stage], "control_mismatch")
    wave = load(root / expected["wave_validation_path"])
    require(wave["exit_code"] == 0 and wave["dispatched"] is False,
            "wave_state_mismatch")
    plan = json.loads(wave["stdout"])
    require(plan["counts"] == {"spawn": 32, "resume": 0, "total": 32},
            "wave_count_mismatch")
    require(len({t["name"] for t in plan["tasks"]}) == 32,
            "wave_count_mismatch")
    if admission:
        # This recovery has no dispatched wave or applicable task-receipt binding.
        # A later sound round needs new evidence, never a flipped acceptance flag.
        raise Finding(2, "required_alias_bindings_missing+applicable_receipt_binding_missing")
    return "RECOVERY_EVIDENCE: CLEAN finding=pinned_package_consistent author_review=9/9 coverage=70/72 citation_rules=9/9 admitted=false verified_round_increment=0"


def selftest(expected):
    result = load(ROOT / RESULT)
    cases = expected["selftest"]
    with tempfile.TemporaryDirectory(prefix="gate-selftest-", dir=HERE) as directory:
        fixture = Path(directory)
        for relative in expected["snapshots"]:
            target = fixture / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        target = fixture / RESULT
        target.parent.mkdir(parents=True, exist_ok=True)
        for case in cases:
            candidate = copy.deepcopy(result)
            name = case["case"]
            if name == "wrong_revision":
                candidate["measured_revision"] = "0" * 40
            elif name == "omitted_obligation":
                candidate["obligations"].pop()
            elif name == "duplicate_obligation":
                candidate["obligations"][-1] = candidate["obligations"][0]
            elif name == "wrong_subject":
                candidate["smoke"]["subject_sha256"] = "0" * 64
            elif name == "unearned_admission":
                candidate["admitted"] = True
            target.write_text(json.dumps(candidate))
            snapshot = fixture / expected["bundle_path"]
            original = snapshot.read_bytes()
            if name == "snapshot_tampered":
                snapshot.write_bytes(original + b" ")
            if name == "missing_result":
                target.unlink()
            command = [sys.executable, str(Path(__file__).resolve()), "--root", str(fixture)]
            if name == "blocked_admission":
                command.append("--admission")
            run = subprocess.run(command, capture_output=True, text=True)
            snapshot.write_bytes(original)
            passed = run.returncode == case["exit_code"] and case["finding"] in run.stdout
            print(f"SELFTEST_CASE: {'CLEAN' if passed else 'FAILED'} case={name} exit={run.returncode} expected={case['exit_code']} finding={case['finding']}")
            require(passed, "selftest_case_failed")
    return f"RECOVERY_SELFTEST: CLEAN cases={len(cases)} exit=0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--admission", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    label = "ROUND_ADMISSION" if args.admission else "RECOVERY_EVIDENCE"
    try:
        expected = load(HERE / "expected.json")
        print(selftest(expected) if args.selftest else check(args.root, expected, args.admission))
        return 0
    except Finding as error:
        state = "COULD_NOT_EVALUATE" if error.code == 2 else "FAILED"
        print(f"{label}: {state} finding={error.name} exit={error.code}")
        return error.code
    except (OSError, ValueError, KeyError, TypeError):
        print(f"{label}: COULD_NOT_EVALUATE finding=unreadable_or_invalid_input exit=2")
        return 2


if __name__ == "__main__":
    sys.exit(main())
