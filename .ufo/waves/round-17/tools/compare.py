#!/usr/bin/env python3
"""compare.py -- compare one predict.py output with one log-extract.py output.

Usage:
  python3 -I compare.py --prediction P.json --observation O.json
  python3 -I compare.py --selftest

Prediction file: predict.py output; the fields compared live under "expected"
({"untested_version": str|null, "snapshot_label": str|null,
  "missing_bootstrap": bool}).
Observation file: log-extract.py output; fields compared are top-level
({"untested_versions": [str], "snapshot_labels": [str],
  "missing_bootstrap": bool}).

Per-field verdicts:
  untested_version : match iff predicted value is contained in observed
                     untested_versions, or both sides are empty (predicted
                     null/"" and observed list empty).
  snapshot_label   : same contains-or-both-empty rule over observed
                     snapshot_labels (a list, because one version can produce
                     both "for X" and "for version X" log lines).
  missing_bootstrap: match iff predicted and observed booleans are equal.

Output: JSON on stdout (sort_keys=True, indent=2) with a per-field
{field, predicted, observed, match} list and all_match. Exit 0 when every
field matches, 1 on any mismatch, 2 on invalid/unreadable input (not a
verdict: bad JSON, wrong types, missing required keys, unreadable files).
Python 3 stdlib only. Writes nothing outside tempfiles created by --selftest.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

FIELDS = ("untested_version", "snapshot_label", "missing_bootstrap")
# Round-17 L1 integration: selection-route fields, compared only when the prediction
# carries them (predict.py >= integration). snapshot_label echoes the request
# (GoRttiMapper.java:179-180) and cannot discriminate the route; these can.
ROUTE_FIELDS = ("snapshot_route", "fallback_to")

RULES = {
    "untested_version": "contains-or-both-empty",
    "snapshot_label": "contains-or-both-empty (non-discriminating: request echo)",
    "missing_bootstrap": "equality",
    "snapshot_route": "equality (observed from GoApiSnapshot component only)",
    "fallback_to": "contains-or-both-empty over observed snapshot_fallbacks[].to",
}

PRED_REQUIRED = {
    "expected.untested_version": "str|null",
    "expected.snapshot_label": "str|null",
    "expected.missing_bootstrap": "bool",
}
OBS_REQUIRED = {
    "untested_versions": "list[str]",
    "snapshot_labels": "list[str]",
    "missing_bootstrap": "bool",
}


def _is_string_list(value):
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _is_str_or_none(value):
    return value is None or isinstance(value, str)


def load_inputs(prediction_path, observation_path):
    """Read and shape-validate both files; return (prediction, observation, errors)."""
    errors = []
    data = {}
    for tag, path in (("prediction", prediction_path), ("observation", observation_path)):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data[tag] = json.load(fh)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            data[tag] = None
            errors.append("{0}: cannot read/parse {1!r}: {2}".format(tag, path, exc))

    pred = data["prediction"]
    if pred is not None:
        if not isinstance(pred, dict) or not isinstance(pred.get("expected"), dict):
            errors.append(
                "prediction: top-level object with object key 'expected' required"
            )
        else:
            exp = pred["expected"]
            if not _is_str_or_none(exp.get("untested_version", False)):
                errors.append("prediction.expected.untested_version must be str|null")
            if not _is_str_or_none(exp.get("snapshot_label", False)):
                errors.append("prediction.expected.snapshot_label must be str|null")
            if not isinstance(exp.get("missing_bootstrap"), bool):
                errors.append("prediction.expected.missing_bootstrap must be bool")

    obs = data["observation"]
    if obs is not None:
        if not isinstance(obs, dict):
            errors.append("observation: top-level object required")
        else:
            if not _is_string_list(obs.get("untested_versions")):
                errors.append("observation.untested_versions must be list[str]")
            if not _is_string_list(obs.get("snapshot_labels")):
                errors.append("observation.snapshot_labels must be list[str]")
            if not isinstance(obs.get("missing_bootstrap"), bool):
                errors.append("observation.missing_bootstrap must be bool")

    return pred, obs, errors


def _contains_or_both_empty(predicted, observed_list):
    if predicted in (None, ""):
        return len(observed_list) == 0
    return predicted in observed_list


def compare(prediction, observation):
    """Build the per-field verdict structure from validated inputs."""
    exp = prediction["expected"]
    observed = {
        "untested_version": observation["untested_versions"],
        "snapshot_label": observation["snapshot_labels"],
        "missing_bootstrap": observation["missing_bootstrap"],
    }
    predicted = {
        "untested_version": exp["untested_version"],
        "snapshot_label": exp["snapshot_label"],
        "missing_bootstrap": exp["missing_bootstrap"],
    }
    active = list(FIELDS)
    if "snapshot_route" in exp:
        active += list(ROUTE_FIELDS)
        predicted["snapshot_route"] = exp.get("snapshot_route")
        predicted["fallback_to"] = exp.get("fallback_to")
        observed["snapshot_route"] = observation.get("snapshot_route")
        observed["fallback_to"] = [f.get("to") for f in
                                   (observation.get("snapshot_fallbacks") or [])
                                   if isinstance(f, dict)]
    fields = []
    for field in active:
        if field in ("missing_bootstrap", "snapshot_route"):
            match = predicted[field] == observed[field]
        else:
            match = _contains_or_both_empty(predicted[field], observed[field])
        fields.append(
            {
                "field": field,
                "predicted": predicted[field],
                "observed": observed[field],
                "match": match,
            }
        )
    return {
        "fields": fields,
        "all_match": all(item["match"] for item in fields),
        "rules": RULES,
    }


def _dump(obj):
    print(json.dumps(obj, sort_keys=True, indent=2))


def run(prediction_path, observation_path):
    """Returns process exit code after emitting the result JSON."""
    pred, obs, errors = load_inputs(prediction_path, observation_path)
    if errors:
        _dump(
            {
                "error": "invalid input",
                "observation": observation_path,
                "prediction": prediction_path,
                "problems": errors,
            }
        )
        return 2
    result = compare(pred, obs)
    result["observation"] = observation_path
    result["prediction"] = prediction_path
    _dump(result)
    return 0 if result["all_match"] else 1


# ---------------------------------------------------------------------------
# --selftest: builds fixtures under tempfile.mkdtemp(), exercises the real CLI
# (this script via sys.executable), then removes them.
# ---------------------------------------------------------------------------

_PRED_MATCH = {
    "input": "go1.27.0-X:nodwarf5",
    "normalized": "1.27.0",
    "in_declared_range": False,
    "selection": {"status": "missing_base"},
    "expected": {
        "untested_version": "1.27.0",
        "snapshot_label": "1.27.0",
        "missing_bootstrap": True,
    },
    "basis": ["contract placeholder"],
}

_OBS_MATCH = {
    "log_path": "ghidra.log",
    "log_sha256": "0" * 64,
    "language_compiler": "Go:LE:64:default",
    "go_lines": [],
    "untested_versions": ["1.27.0"],
    "snapshot_labels": ["1.27.0"],
    "go_version_logged": [],
    "missing_bootstrap": True,
    "analyzer_errors": [],
    "classification": "bootstrap_missing",
}

_PRED_EMPTY = {
    "input": "go1.23.12",
    "normalized": "1.23.12",
    "in_declared_range": True,
    "selection": {"status": "exact"},
    "expected": {
        "untested_version": None,
        "snapshot_label": "1.23.12",
        "missing_bootstrap": False,
    },
    "basis": ["contract placeholder"],
}

_OBS_EMPTY = {
    "log_path": "ghidra.log",
    "log_sha256": "0" * 64,
    "language_compiler": "Go:LE:64:default",
    "go_lines": [],
    "untested_versions": [],
    "snapshot_labels": ["1.23.12", "version 1.23.12"],
    "go_version_logged": ["1.23.12"],
    "missing_bootstrap": False,
    "analyzer_errors": [],
    "classification": "snapshot_loaded",
}


def _mutate(obj, path, value):
    """Deep-copy obj, set a dotted key path (list index ok) to value."""
    import copy

    out = copy.deepcopy(obj)
    node = out
    parts = path.split(".")
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    node[parts[-1]] = value
    return out


def _pop(obj, path):
    """Deep-copy obj, remove a dotted key path."""
    import copy

    out = copy.deepcopy(obj)
    node = out
    parts = path.split(".")
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    del node[parts[-1]]
    return out


def _selftest():
    cases = [
        # (name, prediction object-or-raw, observation object-or-raw,
        #  expected exit, expected all_match or None)
        ("full_match", _PRED_MATCH, _OBS_MATCH, 0, True),
        ("both_empty_match", _PRED_EMPTY, _OBS_EMPTY, 0, True),
        (
            "untested_version_mismatch",
            _mutate(_PRED_MATCH, "expected.untested_version", "9.9.9"),
            _OBS_MATCH,
            1,
            False,
        ),
        (
            "snapshot_label_mismatch",
            _mutate(_PRED_MATCH, "expected.snapshot_label", "1.26.0"),
            _OBS_MATCH,
            1,
            False,
        ),
        (
            "missing_bootstrap_mismatch",
            _mutate(_PRED_MATCH, "expected.missing_bootstrap", False),
            _OBS_MATCH,
            1,
            False,
        ),
        (
            "predicted_present_observed_empty",
            _PRED_MATCH,
            _mutate(_OBS_EMPTY, "snapshot_labels", []),
            1,
            False,
        ),
        ("prediction_not_json", "{not json", _OBS_MATCH, 2, None),
        (
            "prediction_missing_expected_key",
            _pop(_PRED_MATCH, "expected.untested_version"),
            _OBS_MATCH,
            2,
            None,
        ),
        (
            "observation_wrong_type",
            _PRED_MATCH,
            _mutate(_OBS_MATCH, "untested_versions", "1.27.0"),
            2,
            None,
        ),
        ("observation_not_object", _PRED_MATCH, [1, 2, 3], 2, None),
    ]

    tmp = tempfile.mkdtemp(prefix="compare-selftest-")
    script = os.path.abspath(__file__)
    failures = []
    try:
        pred_path = os.path.join(tmp, "prediction.json")
        obs_path = os.path.join(tmp, "observation.json")
        for name, pred_obj, obs_obj, want_exit, want_all_match in cases:
            for path, obj in ((pred_path, pred_obj), (obs_path, obs_obj)):
                if isinstance(obj, str):
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(obj)
                else:
                    with open(path, "w", encoding="utf-8") as fh:
                        json.dump(obj, fh)
            proc = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    script,
                    "--prediction",
                    pred_path,
                    "--observation",
                    obs_path,
                ],
                capture_output=True,
                text=True,
            )
            if proc.returncode != want_exit:
                failures.append(
                    "{0}: exit {1} != {2} (stderr: {3})".format(
                        name, proc.returncode, want_exit, proc.stderr.strip()[:200]
                    )
                )
                continue
            if want_all_match is not None:
                try:
                    payload = json.loads(proc.stdout)
                except json.JSONDecodeError as exc:
                    failures.append("{0}: stdout not JSON: {1}".format(name, exc))
                    continue
                if payload.get("all_match") is not want_all_match:
                    failures.append(
                        "{0}: all_match {1!r} != {2!r}".format(
                            name, payload.get("all_match"), want_all_match
                        )
                    )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("SELFTEST: FAILED " + "; ".join(failures))
        return 1
    print("SELFTEST: CLEAN cases={0}".format(len(cases)))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Compare predict.py --output JSON against log-extract.py --output "
            "JSON field by field; exit 0 all match, 1 any mismatch, "
            "2 invalid input."
        )
    )
    parser.add_argument("--selftest", action="store_true", help="run self tests")
    parser.add_argument("--prediction", metavar="P.json", help="predict.py output")
    parser.add_argument("--observation", metavar="O.json", help="log-extract.py output")
    args = parser.parse_args(argv)

    if args.selftest:
        if args.prediction or args.observation:
            parser.error("--selftest takes no file arguments")
        return _selftest()
    if not args.prediction or not args.observation:
        parser.error("--prediction and --observation are required (or --selftest)")
    return run(args.prediction, args.observation)


if __name__ == "__main__":
    sys.exit(main())
