#!/usr/bin/env python3
"""compare-attack.py -- adversarial-input probe for round-17 tools/compare.py.

Exercises the real CLI (`python3 -I -B compare.py --prediction P --observation O`)
with inputs the shipped --selftest never builds:

  * route mismatch / fallback_to mismatch (contract exit-1 controls),
  * prediction carrying snapshot_route while the observation lacks
    snapshot_route / snapshot_fallbacks (pre-integration log-extract shape),
  * malformed snapshot_fallbacks entries (non-dict items, non-list values),
  * null vs empty-list conventions,
  * top-level JSON null bodies,
  * extra / route-typed fields that bypass load_inputs validation.

Per contract.md the only legal verdict exits are 0 (all match) and 1 (any
mismatch); bad/unreadable input MUST be exit 2. An uncaught traceback is a
crash even when the shell-visible exit code is 1.

Fixtures are written under tempfile.mkdtemp() on the default temp dir and
removed afterwards. Read-only with respect to the lane: invokes compare.py
exactly as a user would. Run:

  python3 -I -B compare-attack.py            # table + JSON detail on stdout
"""

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

COMPARE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/compare.py"

# --- fixtures shaped like real retained artifacts --------------------------
# predictions/*.json shape: route fields live under expected (verified at
# predictions/calib-shfmt.prediction.json:15-21, pro-aether:15-21).
PRED_NONE = {  # calib-shfmt shape: out-of-range, missing base
    "expected": {
        "untested_version": "1.27.0",
        "snapshot_label": None,
        "missing_bootstrap": True,
        "snapshot_route": "none",
        "fallback_to": None,
    },
}
PRED_INFO = {  # calib-esbuild-0.25.12 shape: in-range, exact base
    "expected": {
        "untested_version": None,
        "snapshot_label": "1.23.12",
        "missing_bootstrap": False,
        "snapshot_route": "info",
        "fallback_to": None,
    },
}
PRED_FB = {  # pro-aether shape: fallback route
    "expected": {
        "untested_version": None,
        "snapshot_label": "1.25.14",
        "missing_bootstrap": False,
        "snapshot_route": "fallback",
        "fallback_to": "1.25.0",
    },
}
OBS_NONE = {  # runs/calib-shfmt/observation.json:76-81 shape
    "untested_versions": ["1.27.0"],
    "snapshot_labels": [],
    "missing_bootstrap": True,
    "snapshot_route": "none",
    "snapshot_fallbacks": [],
}
OBS_INFO = {  # runs/calib-esbuild-0.25.12/observation.json:161-167 shape
    "untested_versions": [],
    "snapshot_labels": ["1.23.12"],
    "missing_bootstrap": False,
    "snapshot_route": "info",
    "snapshot_fallbacks": [],
}
OBS_FB = {  # runs/pro-notesmd-cli/observation.json shape (fallback route)
    "untested_versions": [],
    "snapshot_labels": ["1.25.14"],  # request echo = fallback "from"
    "missing_bootstrap": False,
    "snapshot_route": "fallback",
    "snapshot_fallbacks": [{"from": "1.25.14", "to": "1.25.0"}],
}


def _mutate(obj, path, value):
    """Deep-copy obj, set a dotted key path (list index ok) to value."""
    out = copy.deepcopy(obj)
    node = out
    parts = path.split(".")
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    node[parts[-1]] = value
    return out


def _pop(obj, path):
    """Deep-copy obj, remove a dotted key path."""
    out = copy.deepcopy(obj)
    node = out
    parts = path.split(".")
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    del node[parts[-1]]
    return out


# (name, prediction obj-or-raw-str, observation obj-or-raw-str,
#  contract-intended exit, note)
CASES = [
    # -- controls: must stay green ----------------------------------------
    ("ctl_full_match_none", PRED_NONE, OBS_NONE, 0,
     "retained calib-shfmt shape"),
    ("ctl_full_match_fallback", PRED_FB, OBS_FB, 0,
     "retained pro-aether shape"),
    ("ctl_pred_not_json", "{oops", OBS_NONE, 2, "unparseable prediction"),
    ("ctl_obs_missing_field", PRED_NONE,
     _pop(OBS_NONE, "untested_versions"), 2, "required obs key absent"),

    # -- genuine mismatches: contract exit 1 --------------------------------
    ("route_mismatch", PRED_INFO, OBS_FB, 1,
     "info vs fallback: route must fail"),
    ("fallback_to_mismatch", _mutate(PRED_FB, "expected.fallback_to", "1.24.0"),
     OBS_FB, 1, "predicted base not among observed fallback targets"),
    ("predicted_no_fb_observed_fb",
     _mutate(PRED_FB, "expected.fallback_to", None), OBS_FB, 1,
     "pred null vs observed fallback list"),
    ("route_and_fallback_mismatch",
     _mutate(PRED_FB, "expected.fallback_to", "9.9.9"), OBS_INFO, 1,
     "both route fields wrong at once"),

    # -- prediction carries route, observation lacks route keys --------------
    ("obs_lacks_all_route_keys_pred_route", PRED_INFO,
     _pop(_pop(OBS_INFO, "snapshot_route"), "snapshot_fallbacks"), 2,
     "pre-integration obs shape: no route data to compare against"),
    ("obs_lacks_all_route_keys_pred_null",
     _mutate(_mutate(PRED_INFO, "expected.snapshot_route", None),
             "expected.fallback_to", None),
     _pop(_pop(OBS_INFO, "snapshot_route"), "snapshot_fallbacks"), 2,
     "pred route null should not silently equal an absent key"),
    ("obs_lacks_fallbacks_key_only", PRED_NONE,
     _pop(OBS_NONE, "snapshot_fallbacks"), 2,
     "absent key is not evidence of an empty observed list"),
    ("obs_fallbacks_explicit_null", PRED_NONE,
     _mutate(OBS_NONE, "snapshot_fallbacks", None), 2,
     "null must not be conflated with observed [] (cf. untested_versions null -> 2)"),

    # -- malformed snapshot_fallbacks ----------------------------------------
    ("fallbacks_scalar_int", PRED_NONE,
     _mutate(OBS_NONE, "snapshot_fallbacks", 7), 2,
     "non-iterable container"),
    ("fallbacks_scalar_bool", PRED_NONE,
     _mutate(OBS_NONE, "snapshot_fallbacks", True), 2,
     "non-iterable container"),
    ("fallbacks_scalar_string", PRED_NONE,
     _mutate(OBS_NONE, "snapshot_fallbacks", "1.25.0"), 2,
     "string iterates as chars -> silently empty"),
    ("fallbacks_dict_not_list", PRED_FB,
     _mutate(OBS_FB, "snapshot_fallbacks", {"to": "1.25.0"}), 2,
     "dict iterates as keys -> silently empty"),
    ("fallback_entry_string", PRED_FB,
     _mutate(OBS_FB, "snapshot_fallbacks", ["oops"]), 2,
     "non-dict entry dropped"),
    ("fallback_entry_list", PRED_FB,
     _mutate(OBS_FB, "snapshot_fallbacks", [["from", "x"]]), 2,
     "non-dict entry dropped"),
    ("fallback_mixed_valid_and_junk", PRED_FB,
     _mutate(OBS_FB, "snapshot_fallbacks",
             [{"to": "1.25.0"}, 42, "junk"]), 2,
     "malformed members tolerated if one dict has matching to"),
    ("fallback_to_nonstring_double_malformed",
     _mutate(PRED_FB, "expected.fallback_to", 5),
     _mutate(OBS_FB, "snapshot_fallbacks", [{"to": 5}]), 2,
     "both sides type-invalid; equality makes them match"),

    # -- null vs empty / type-confusion on route fields ----------------------
    ("pred_route_null_obs_none",
     _mutate(PRED_NONE, "expected.snapshot_route", None), OBS_NONE, 2,
     "pred null vs observed 'none': null is unvalidated"),
    ("pred_fallback_without_route_key_matching_rest",
     _pop(_mutate(PRED_INFO, "expected.fallback_to", "9.9.9"),
          "expected.snapshot_route"), OBS_INFO, 2,
     "bogus fallback_to silently never compared: activation keys off snapshot_route"),
    ("pred_route_int_obs_int",
     _mutate(PRED_NONE, "expected.snapshot_route", 1),
     _mutate(OBS_NONE, "snapshot_route", 1), 2,
     "type-invalid route equal on both sides"),
    ("pred_route_dict_obs_dict",
     _mutate(PRED_NONE, "expected.snapshot_route", {"a": 1}),
     _mutate(OBS_NONE, "snapshot_route", {"a": 1}), 2,
     "JSON-object route compared by =="),
    ("pred_route_list_obs_str",
     _mutate(PRED_INFO, "expected.snapshot_route", ["info"]), OBS_INFO, 2,
     "malformed pred route yields 1, masking invalid input as verdict"),
    ("pred_fallback_without_route_key",
     _pop(_mutate(PRED_INFO, "expected.fallback_to", "1.25.0"),
          "expected.snapshot_route"), OBS_FB, 1,
     "fallback_to present but snapshot_route absent: route fields un-checked"),
    ("pred_untested_empty_str_obs_contains_it",
     _mutate(PRED_INFO, "expected.untested_version", ""),
     _mutate(OBS_INFO, "untested_versions", [""]), 0,
     "legal str '' treated as null by _contains_or_both_empty"),
    ("obs_route_absent_pred_route_none_str",
     PRED_NONE, _pop(OBS_NONE, "snapshot_route"), 1,
     "'none' vs absent (null): mismatch, but masked reason"),

    # -- top-level JSON null bodies -------------------------------------------
    ("pred_file_json_null", "null", OBS_NONE, 2,
     "parses as None -> no 'expected' error appended -> crash downstream"),
    ("obs_file_json_null", PRED_NONE, "null", 2,
     "parses as None -> skipped validation -> crash downstream"),

    # -- extra fields ----------------------------------------------------------
    ("extra_fields_tolerated",
     _mutate(_mutate(PRED_NONE, "expected.surprise", {"x": 1}),
             "top_junk", [1, 2]),
     _mutate(OBS_NONE, "obs_extra", "yes"), 0,
     "extra keys must not disturb the verdict"),
]


def main():
    tmp = tempfile.mkdtemp(prefix="compare-attack-")
    pred_path = os.path.join(tmp, "prediction.json")
    obs_path = os.path.join(tmp, "observation.json")
    results = []
    try:
        for name, pred_obj, obs_obj, want_exit, note in CASES:
            for path, obj in ((pred_path, pred_obj), (obs_path, obs_obj)):
                if isinstance(obj, str):
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(obj)
                else:
                    with open(path, "w", encoding="utf-8") as fh:
                        json.dump(obj, fh)
            proc = subprocess.run(
                ["python3", "-I", "-B", COMPARE,
                 "--prediction", pred_path, "--observation", obs_path],
                capture_output=True, text=True, timeout=60,
            )
            crashed = ("Traceback" in proc.stderr) or proc.returncode < 0
            all_match = None
            try:
                all_match = json.loads(proc.stdout).get("all_match")
            except json.JSONDecodeError:
                pass
            if crashed:
                verdict = "CRASH"
            elif proc.returncode != want_exit:
                if want_exit == 2 and proc.returncode == 0:
                    verdict = "FALSE-MATCH"
                elif want_exit == 2 and proc.returncode == 1:
                    verdict = "MASKED-INVALID"  # bad input reported as verdict
                elif want_exit == 0 and proc.returncode == 1:
                    verdict = "FALSE-MISMATCH"
                else:
                    verdict = "WRONG-EXIT"
            else:
                verdict = "OK"
            results.append({
                "case": name, "want_exit": want_exit,
                "got_exit": proc.returncode, "all_match": all_match,
                "crash": crashed, "verdict": verdict, "note": note,
                "stderr_tail": proc.stderr.strip().splitlines()[-1]
                               if proc.stderr.strip() else "",
            })
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    for r in results:
        print("{verdict:14} {case:44} want={want_exit} got={got_exit} "
              "all_match={all_match} {note}".format(**r))
    bad = [r for r in results if r["verdict"] != "OK"]
    print("\n=== compare-attack summary ===")
    print(json.dumps({
        "compare": COMPARE,
        "cases": len(results),
        "ok": len(results) - len(bad),
        "findings": len(bad),
        "crashes": [r["case"] for r in results if r["verdict"] == "CRASH"],
        "false_matches": [r["case"] for r in results
                          if r["verdict"] == "FALSE-MATCH"],
        "masked_invalid": [r["case"] for r in results
                           if r["verdict"] == "MASKED-INVALID"],
        "false_mismatches": [r["case"] for r in results
                             if r["verdict"] == "FALSE-MISMATCH"],
        "wrong_exit": [r["case"] for r in results
                       if r["verdict"] == "WRONG-EXIT"],
        "detail": [r for r in results if r["verdict"] != "OK"],
    }, indent=2, sort_keys=True))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
