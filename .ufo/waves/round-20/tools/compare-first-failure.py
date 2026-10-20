#!/usr/bin/env python3
"""Compare a frozen H1 first-failure forecast with one extracted log failure."""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile


def validate_failure(value, where):
    """Validate the C3 failure shape while retaining all supplied fields."""
    if value is None:
        return
    if not isinstance(value, dict):
        raise ValueError(f"{where}: expected object or null")
    if not isinstance(value.get("kind"), str) or not value["kind"]:
        raise ValueError(f"{where}: kind must be a non-empty string")
    for field in ("index", "va"):
        item = value.get(field)
        if item is not None and (not isinstance(item, int) or isinstance(item, bool)):
            raise ValueError(f"{where}: {field} must be an integer or null")
    if not isinstance(value.get("phase"), str):
        raise ValueError(f"{where}: phase must be a string")


def same_failure(predicted, observed):
    """C3 equality: both silent, or matching kind and index; va/phase are ignored."""
    validate_failure(predicted, "prediction.first_failure.h1")
    validate_failure(observed, "extractor result")
    if predicted is None or observed is None:
        return predicted is None and observed is None
    return predicted["kind"] == observed["kind"] and predicted["index"] == observed["index"]


def read_prediction(path):
    with open(path, "r", encoding="utf-8") as source:
        payload = json.load(source)
    if not isinstance(payload, dict):
        raise ValueError("prediction: expected JSON object")
    first_failure = payload.get("first_failure")
    if not isinstance(first_failure, dict) or "h1" not in first_failure:
        raise ValueError("prediction: missing first_failure.h1")
    predicted = first_failure["h1"]
    validate_failure(predicted, "prediction.first_failure.h1")
    return predicted


def run_extractor(extractor, log_path):
    if not os.path.isfile(extractor):
        raise ValueError(f"extractor_not_found: {extractor}")
    if not os.path.isfile(log_path):
        raise ValueError(f"log_not_found: {log_path}")
    try:
        process = subprocess.run(
            [sys.executable, "-I", "-B", extractor, log_path],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ValueError(f"extractor_execution_failed: {error}") from error
    if process.returncode != 0:
        detail = process.stderr.strip()
        raise ValueError(f"extractor_exit_{process.returncode}: {detail or 'no stderr'}")
    try:
        observed = json.loads(process.stdout)
    except json.JSONDecodeError as error:
        raise ValueError(f"extractor_output_not_json: {error}") from error
    # first-failure-extract.py prints an envelope {log_path, last_line,
    # first_failure, other_errors, ...}; the comparison object is its
    # `first_failure` member (null = no Go-analysis failure up to last_line).
    if isinstance(observed, dict) and "first_failure" in observed and "last_line" in observed:
        observed = observed["first_failure"]
    validate_failure(observed, "extractor result")
    return observed


def evaluate_paths(prediction_path, log_path, extractor_path):
    predicted = None
    observed = None
    try:
        predicted = read_prediction(prediction_path)
        observed = run_extractor(extractor_path, log_path)
        matched = same_failure(predicted, observed)
    except (OSError, ValueError) as error:
        return {
            "match": None,
            "predicted": predicted,
            "observed": observed,
            "error": str(error),
        }, 2
    return {
        "match": matched,
        "predicted": predicted,
        "observed": observed,
    }, 0 if matched else 1


def selftest():
    cases = []
    failures = []

    def check(case_id, condition):
        cases.append(case_id)
        if not condition:
            failures.append(case_id)

    check("both_silent", same_failure(None, None))
    check("kind_index_only", same_failure(
        {"kind": "invalid_index", "index": 9, "va": 1, "phase": "predicted"},
        {"kind": "invalid_index", "index": 9, "va": 2, "phase": "observed"},
    ))
    check("index_mismatch", not same_failure(
        {"kind": "invalid_index", "index": 9, "va": None, "phase": "map"},
        {"kind": "invalid_index", "index": 10, "va": None, "phase": "map"},
    ))
    try:
        same_failure({"kind": "invalid_index", "index": True, "va": None, "phase": "map"}, None)
    except ValueError:
        check("reject_boolean_index", True)
    else:
        check("reject_boolean_index", False)

    scratch = tempfile.mkdtemp(prefix="compare-first-failure-selftest-")
    try:
        prediction_path = os.path.join(scratch, "prediction.json")
        log_path = os.path.join(scratch, "log.json")
        extractor_path = os.path.join(scratch, "extractor.py")
        expected = {"kind": "eof", "index": 42, "va": 4096, "phase": "type"}
        with open(prediction_path, "w", encoding="utf-8") as output:
            json.dump({"first_failure": {"h1": expected}}, output)
        with open(log_path, "w", encoding="utf-8") as output:
            json.dump(expected, output)
        with open(extractor_path, "w", encoding="utf-8") as output:
            output.write(
                "import json, sys\n"
                "with open(sys.argv[1], encoding='utf-8') as source:\n"
                "    print(json.dumps(json.load(source)))\n"
            )
        result, exit_code = evaluate_paths(prediction_path, log_path, extractor_path)
        check("extractor_path_executes", exit_code == 0 and result["match"] is True)
        check("records_both_objects", result["predicted"] == expected and result["observed"] == expected)
    except (OSError, ValueError) as error:
        check("extractor_path_executes", False)
        check("records_both_objects", False)
        failures.append(f"selftest_setup:{error}")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    if failures:
        print(f"SELFTEST: FAILED cases={len(cases)} fails={','.join(failures)}")
        return 1
    print(f"SELFTEST: CLEAN cases={len(cases)}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prediction")
    parser.add_argument("--log")
    parser.add_argument("--extractor", help="first-failure-extract.py executable script")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    missing = [name for name in ("prediction", "log", "extractor") if not getattr(args, name)]
    if missing:
        parser.error("required outside --selftest: " + ", ".join("--" + item for item in missing))
    result, exit_code = evaluate_paths(args.prediction, args.log, args.extractor)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
