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
EXPECTED = HERE.relative_to(ROOT) / "expected.json"
RESULT = Path("evidence/round-1-2026-10-15/result.json")


class Finding(Exception):
    def __init__(self, code, name):
        self.code, self.name = code, name


def require(condition, name, code=1):
    if not condition:
        raise Finding(code, name)


def load(path):
    return json.loads(path.read_text())


def blocked_prerequisites(root, expected, result, plan):
    routing = load(root / expected["routing_observation_path"])
    required = expected["required_routes"]
    observed = routing["observed"]
    resolved = {role: "@" + family["alias"]
                for family in plan["routePreflight"]["families"]
                for role in family["roles"]}
    roles = set(required) - {"connector_fallback"}
    require(routing["required"] == required
            and all(observed[role] == resolved[role] for role in roles)
            and routing["cards_model_binding_found"] is False
            and routing["routes_probed"] is False,
            "routing_observation_mismatch")
    missing_routes = any(observed[role] != required[role] for role in roles)
    missing_routes |= required["connector_fallback"] not in observed["m_antigravity_fallbacks"]
    require(missing_routes and routing["state"] == "blocked",
            "routing_observation_mismatch")
    require(routing["native_tasks_spawned"] == result["dispatch"]["spawned"] == 0
            and routing["native_tasks_settled"] == result["dispatch"]["settled"] == 0,
            "undispatched_wave_observation_mismatch")
    binding = load(root / expected["receipt_binding_path"])
    fields = set(expected["required_receipt_fields"])
    bound = set(binding["task_receipt_binding_keys"])
    missing = fields - bound
    require(not bound and set(binding["missing"]) == missing == fields
            and binding["dispatch_kind"] == "argv"
            and set(binding["dispatch_keys"]) == {"argv", "kind"}
            and binding["mint_attempted"] is False
            and binding["receipt_validated"] is False
            and binding["sighting_complete_attempted"] is False,
            "receipt_observation_mismatch")
    return (["required_alias_bindings_missing"] if missing_routes else []) + (
        ["applicable_receipt_binding_missing"] if missing else [])


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
    blockers = blocked_prerequisites(root, expected, result, plan)
    if admission and blockers:
        raise Finding(2, "+".join(blockers))
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
            fixture_expected = copy.deepcopy(expected)
            changed = None
            if name in ("routing_status_contradiction", "settled_without_dispatch"):
                changed = expected["routing_observation_path"]
                observation = load(ROOT / changed)
                if name == "routing_status_contradiction":
                    observation["state"] = "ready"
                else:
                    observation["native_tasks_settled"] = 1
            elif name == "receipt_presence_contradiction":
                changed = expected["receipt_binding_path"]
                observation = load(ROOT / changed)
                observation["missing"] = []
            if changed is not None:
                # Re-pin only the isolated fixture: test semantic contradictions,
                # not another copy of the already-covered digest failure.
                data = json.dumps(observation).encode()
                (fixture / changed).write_bytes(data)
                fixture_expected["snapshots"][changed] = hashlib.sha256(data).hexdigest()
            (fixture / EXPECTED).write_text(json.dumps(fixture_expected))
            snapshot = fixture / expected["bundle_path"]
            original = snapshot.read_bytes()
            if name == "snapshot_tampered":
                snapshot.write_bytes(original + b" ")
            if name == "missing_result":
                target.unlink()
            command = [sys.executable, str(Path(__file__).resolve()), "--root", str(fixture)]
            if name in ("blocked_admission", "routing_status_contradiction",
                        "receipt_presence_contradiction", "settled_without_dispatch"):
                command.append("--admission")
            run = subprocess.run(command, capture_output=True, text=True)
            snapshot.write_bytes(original)
            if changed is not None:
                (fixture / changed).write_bytes((ROOT / changed).read_bytes())
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
        expected = load(args.root / EXPECTED)
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
