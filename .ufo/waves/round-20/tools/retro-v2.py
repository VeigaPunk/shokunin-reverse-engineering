#!/usr/bin/env python3
"""Compare v2 H1 first-failure JSONs with retained round-19 pass2 logs."""
import argparse
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

COMPARE = Path(__file__).resolve().with_name("compare-first-failure.py")


def json_cell(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def read_h1_for_display(path):
    try:
        with open(path, "r", encoding="utf-8") as source:
            payload = json.load(source)
    except (OSError, json.JSONDecodeError) as error:
        return None, f"prediction_unreadable: {error}"
    if not isinstance(payload, dict):
        return None, "prediction_not_object"
    first_failure = payload.get("first_failure")
    if not isinstance(first_failure, dict) or "h1" not in first_failure:
        return None, "prediction_missing_first_failure.h1"
    return first_failure["h1"], None


def logs_for_label(pass2_root, label):
    carrier_dir = Path(pass2_root) / label
    if not carrier_dir.is_dir():
        return []
    return sorted(path for path in carrier_dir.rglob("ghidra.log") if path.is_file())


def compare_one(prediction_path, log_path, extractor_path):
    if not COMPARE.is_file():
        return None, "compare_tool_not_found"
    try:
        process = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                str(COMPARE),
                "--prediction",
                str(prediction_path),
                "--log",
                str(log_path),
                "--extractor",
                str(extractor_path),
            ],
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, f"compare_execution_failed: {error}"
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError as error:
        return None, f"compare_output_not_json: {error}"
    if not isinstance(result, dict) or process.returncode not in (0, 1, 2):
        return None, f"compare_unusable_exit_{process.returncode}"
    if process.returncode == 2 or result.get("match") not in (True, False):
        return result, result.get("error", "comparison_unevaluable")
    return result, None


def make_rows(v2_dir, pass2_root, extractor_path):
    rows = []
    issues = []
    mismatches = 0
    unevaluable = 0
    predictions = sorted(Path(v2_dir).glob("*.json"))
    for prediction_path in predictions:
        label = prediction_path.stem
        predicted, prediction_error = read_h1_for_display(prediction_path)
        logs = logs_for_label(pass2_root, label)
        result = None
        error = prediction_error
        if prediction_error is None and len(logs) == 1:
            result, compare_error = compare_one(prediction_path, logs[0], extractor_path)
            if compare_error:
                error = compare_error
        elif prediction_error is None and not logs:
            error = "bound_pass2_log_missing"
        elif prediction_error is None:
            error = f"ambiguous_pass2_logs: {len(logs)}"

        if result is not None:
            predicted = result.get("predicted", predicted)
            observed = result.get("observed")
            matched = result.get("match")
        else:
            observed = None
            matched = None
        if error is not None or matched not in (True, False):
            match_text = "unevaluable"
            unevaluable += 1
            issues.append(f"{label}: {error or 'comparison_unevaluable'}")
        elif matched:
            match_text = "yes"
        else:
            match_text = "no"
            mismatches += 1
        rows.append({
            "label": label,
            "predicted": predicted,
            "observed": observed,
            "match": match_text,
        })
    return rows, issues, mismatches, unevaluable


def render_table(rows):
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(("label", "predicted", "observed", "match"))
    for row in rows:
        writer.writerow((
            row["label"],
            json_cell(row["predicted"]),
            json_cell(row["observed"]),
            row["match"],
        ))
    return buffer.getvalue()


def write_table(text, output_path):
    if output_path == "-":
        sys.stdout.write(text)
        return
    with open(output_path, "w", encoding="utf-8", newline="") as target:
        target.write(text)


def selftest():
    case_ids = []
    failures = []

    def check(case_id, condition):
        case_ids.append(case_id)
        if not condition:
            failures.append(case_id)

    scratch = tempfile.mkdtemp(prefix="retro-v2-selftest-")
    try:
        root = Path(scratch)
        v2_dir = root / "v2"
        pass2_root = root / "pass2"
        v2_dir.mkdir()
        extractor_path = root / "extractor.py"
        extractor_path.write_text(
            "import json, sys\n"
            "with open(sys.argv[1], encoding='utf-8') as source:\n"
            "    print(json.dumps(json.load(source)))\n",
            encoding="utf-8",
        )
        fixtures = {
            "alpha": (
                {"kind": "invalid_index", "index": 7, "va": 100, "phase": "predicted"},
                {"kind": "invalid_index", "index": 7, "va": 200, "phase": "observed"},
                "yes",
            ),
            "beta": (
                {"kind": "invalid_index", "index": 8, "va": None, "phase": "predicted"},
                {"kind": "invalid_index", "index": 7, "va": None, "phase": "observed"},
                "no",
            ),
        }
        for label, (predicted, observed, _) in fixtures.items():
            with open(v2_dir / f"{label}.json", "w", encoding="utf-8") as output:
                json.dump({"first_failure": {"h1": predicted}}, output)
            log_dir = pass2_root / label / "logs" / "fixture"
            log_dir.mkdir(parents=True)
            with open(log_dir / "ghidra.log", "w", encoding="utf-8") as output:
                json.dump(observed, output)
        with open(v2_dir / "gamma.json", "w", encoding="utf-8") as output:
            json.dump({"first_failure": {"h1": None}}, output)

        rows, issues, mismatches, unevaluable = make_rows(
            v2_dir, pass2_root, extractor_path
        )
        by_label = {row["label"]: row for row in rows}
        check("match_row", by_label.get("alpha", {}).get("match") == "yes")
        check("mismatch_row", by_label.get("beta", {}).get("match") == "no")
        check("missing_log_unevaluable", by_label.get("gamma", {}).get("match") == "unevaluable")
        check("csv_columns_and_order", render_table(rows).splitlines()[0]
              == "label,predicted,observed,match")
        check("counts_follow_rows", mismatches == 1 and unevaluable == 1 and len(issues) == 1)
    except (OSError, ValueError) as error:
        failures.append(f"selftest_setup:{error}")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    if failures:
        print(f"SELFTEST: FAILED cases={len(case_ids)} fails={','.join(failures)}")
        return 1
    print(f"SELFTEST: CLEAN cases={len(case_ids)}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v2-dir", help="directory of <label>.json v2 outputs")
    parser.add_argument("--pass2-dir", help="round-19 runs/pass2 directory")
    parser.add_argument("--extractor", help="first-failure-extract.py executable script")
    parser.add_argument("--output", default="-", help="CSV path (default: stdout; - means stdout)")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    missing = [name for name in ("v2_dir", "pass2_dir", "extractor") if not getattr(args, name)]
    if missing:
        parser.error("required outside --selftest: " + ", ".join("--" + item.replace("_", "-") for item in missing))
    if not os.path.isdir(args.v2_dir):
        print(f"retro-v2.py: v2_dir_not_found: {args.v2_dir}", file=sys.stderr)
        return 2
    if not os.path.isdir(args.pass2_dir):
        print(f"retro-v2.py: pass2_dir_not_found: {args.pass2_dir}", file=sys.stderr)
        return 2
    if not os.path.isfile(args.extractor):
        print(f"retro-v2.py: extractor_not_found: {args.extractor}", file=sys.stderr)
        return 2
    if not COMPARE.is_file():
        print(f"retro-v2.py: compare_tool_not_found: {COMPARE}", file=sys.stderr)
        return 2

    rows, issues, mismatches, unevaluable = make_rows(
        args.v2_dir, args.pass2_dir, args.extractor
    )
    if not rows:
        print("retro-v2.py: no_v2_json_files", file=sys.stderr)
        return 2
    try:
        write_table(render_table(rows), args.output)
    except OSError as error:
        print(f"retro-v2.py: output_write_failed: {error}", file=sys.stderr)
        return 2
    for issue in issues:
        print(f"retro-v2.py: unevaluable: {issue}", file=sys.stderr)
    if unevaluable:
        return 2
    if mismatches:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
