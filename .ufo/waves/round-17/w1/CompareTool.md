# CompareTool — compare.py report

## Deliverable
- New file: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/compare.py` (only file written besides this report).
- Implements contract.md:75-78 (`## W/tools/compare.py`): `--prediction P.json --observation O.json`, per-field `{field, predicted, observed, match}` for `untested_version`, `snapshot_label`, `missing_bootstrap`; exit 0 all match, 1 any mismatch, 2 invalid input. Stdlib only, `python3 -I` runnable, JSON `sort_keys=True, indent=2`.

## Field-rule interpretation (observation vs inference)
- **Observation (contract:77):** `untested_version` rule is explicit — "observed list contains predicted, or both empty". Implemented as `contains-or-both-empty` over `observation.untested_versions` (list) vs `prediction.expected.untested_version` (scalar, null/"" = empty). compare.py lines 118-124, 133-145.
- **Inference:** `snapshot_label` gets the same `contains-or-both-empty` rule over `observation.snapshot_labels`, because log-extract (contract:53-54) produces a *list* of labels and the pilot log shows one version emitting two label lines (`Using Go API snapshot for 1.23.12` and `Using Go API snapshot for version 1.23.12`, pilot/esbuild-0.25.12-log/ghidra.log:63-64). A single observed line can't pair 1:1 with the predicted scalar; membership is the honest rule. Flagged for L1 in case equality-of-sets was intended instead.
- **Inference:** `missing_bootstrap` is plain boolean equality (contract lists no other rule).
- **Inference:** predicted values are read from `prediction.expected.*` per contract:70-71's predict.py output shape; observed values from top-level `observation.untested_versions|snapshot_labels|missing_bootstrap` per contract:52-59's log-extract shape.
- **Inference (empty side):** predicted `null` *or* `""` counts as "empty" (predict.py may emit `str|null` per contract:70); observed side empty iff the list is empty.
- Output adds `all_match`, `rules`, and both input paths alongside the contract-mandated `fields` list — extra keys, no contract field renamed.

## Validation (exit 2 conditions)
Non-object/missing `expected`, non-str-or-null `untested_version`/`snapshot_label`, non-bool `missing_bootstrap`, non-list-of-str `untested_versions`/`snapshot_labels`, non-bool observed `missing_bootstrap`, unparseable/unreadable JSON, missing CLI args → exit 2 with a `problems` list (compare.py lines 71-115). Missing file, unreadable dir, and argparse errors all map to 2.

## Verification exercised
- `python3 -I .../tools/compare.py --selftest` → `SELFTEST: CLEAN cases=10`, exit 0 (run once, per contract:9).
  - 10 subprocess cases through the real CLI: 2 green (populated match; both-empty match), 4 red (each field mismatch + predicted-present/observed-empty) → exit 1 verified, 4 invalid (bad JSON, missing required key, wrong type, non-object observation) → exit 2 verified. `all_match` parsed back from stdout and checked.
- One manual smoke run of the real CLI on a matching pair → exit 0, output shape as shown above (fields/rules/all_match present).
- Temp fixtures created under `tempfile.mkdtemp()` and removed via `shutil.rmtree` in `finally` (lines 241-293); tool writes nothing else.

## Risks / limits
- `snapshot_label` membership rule is an inference (see above); if L1 wants set-equality or first-element matching, it is a one-line change.
- Comparison is by exact string; any normalization drift between predict.py's normalized label and log-extract's captured label surfaces as a real mismatch (by design — mismatches must not be hidden, claims.json:22).
- Selftest cases are synthetic fixtures, not pilot-derived logs; field-name fidelity rests on the contract text, not on a real log-extract run (tool not yet written at assignment time).
- No installs, no REA/Ghidra invocation, no carrier execution, no files outside `tools/compare.py` and this report.

Report: .ufo/waves/round-17/w1/CompareTool.md
