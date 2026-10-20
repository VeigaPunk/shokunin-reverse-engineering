# CompareAttack — round 17 wave 2 (FALSIFY, compare.py)

Axes: **calibration** (does the verdict remain truthful under adversarial input)
and **depth** (do the new route fields discriminate, and can bad input be told
apart from a real mismatch).

Target: `.ufo/waves/round-17/tools/compare.py` at lane revision
`da64646adcb19c1ede7537b799b8c7d283fe43da` (Python 3.14.8). Driver:
`.ufo/waves/round-17/w2/compare-attack.py` — 31 cases, each run as
`python3 -I -B compare.py --prediction P --observation O` via subprocess, with
fixtures under `tempfile.mkdtemp()` (removed after). Command run:

```
python3 -I -B .ufo/waves/round-17/w2/compare-attack.py   # exit 1: findings
```

## Result

31 cases: 12 OK (all controls + both genuine route mismatches exit 1 as
required), **4 crashes, 9 false-matches (exit 0 on bad/missing evidence),
6 masked-invalid (bad input reported as exit-1 verdict), 1 false-mismatch**
— 19 findings. Every attack lands on one root cause: `load_inputs`
(compare.py:73-112) validates only the three r16 fields; `snapshot_route`,
`fallback_to`, `snapshot_fallbacks`, and JSON-`null` bodies bypass shape
checks, then `compare()` (compare.py:134-148) synthesizes absent keys as
`None`/`[]`.

Controls that passed (the route discrimination itself works on real shapes):
`route_mismatch` info-vs-fallback → 1; `fallback_to_mismatch` → 1;
`predicted_no_fb_observed_fb` (pred null vs observed `[{to}]`) → 1;
both genuine-retained-shape matches → 0; invalid JSON / missing obs key → 2.

## Defects

### D1 — crashes on valid-JSON malformed input (4 cases) [HIGH]

Uncaught `TypeError`, shell exit 1 indistinguishable from a true mismatch —
a consumer sees `exit 1` + stderr traceback, not contract exit 2.

- `snapshot_fallbacks` non-iterable — compare.py:140-142 iterates
  `observation.get("snapshot_fallbacks")` unvalidated:
  `"snapshot_fallbacks": 7` → `TypeError: 'int' object is not iterable`;
  `true` → `'bool' object is not iterable`. (Any falsy scalar like `0`
  hits `or []` instead and becomes FALSE-MATCH — see D3.)
- Top-level `null` body — compare.py:86/101 guard on `pred is not None`,
  so `"expected" required` / "top-level object" errors are never appended
  for a file containing literally `null`; compare.py:123
  (`prediction["expected"]`) and :125 (`observation["untested_versions"]`)
  then raise `TypeError: 'NoneType' object is not subscriptable`. Both
  directions crash; `false`, `[]`, `123` correctly give exit 2.

### D2 — absent/unobservable route data silently equals "no route" [HIGH]

compare.py:140-142 builds the observed fallback list as
`[f.get("to") for f in (observation.get("snapshot_fallbacks") or []) ...]`
and :139 reads `observation.get("snapshot_route")` → `None` when absent.

- Observation lacking `snapshot_fallbacks` entirely → exit **0** when pred
  `fallback_to` is null: an absent key is reported as `observed: []`
  ("no fallbacks observed") — `obs_lacks_fallbacks_key_only`.
- `"snapshot_fallbacks": null` → same `or []` collapse → exit **0**
  (`obs_fallbacks_explicit_null`). Compare the r16 fields: `null` there is
  exit 2 via `_is_string_list` (compare.py:105-108) — an internal
  convention inconsistency.
- Pred `snapshot_route: null` + `fallback_to: null` vs observation with
  **no route keys at all** → exit **0** (`obs_lacks_all_route_keys_pred_null`):
  a prediction that asserts nothing about the route accepts an observation
  that observed nothing about it. Calibration hole: an un-instrumented /
  pre-integration observation can satisfy a route claim by silence.
- Pred `snapshot_route: "info"` vs route-less observation → exit 1
  (`MASKED-INVALID`): bad input is masked as a prediction failure.

### D3 — malformed `snapshot_fallbacks` silently coerced empty (3 cases)

- `"snapshot_fallbacks": "1.25.0"` — a string is iterable; chars aren't
  dicts → `[]` → exit **0** with pred null fallback. A scalar string that
  *contains the answer* is dropped.
- `"snapshot_fallbacks": {"to": "1.25.0"}` (dict, not list) → iterates
  keys → `[]` → exit 1 masked as verdict.
- Entries that aren't dicts (`"oops"`, `[["from","x"]]`, mixed
  `[{"to":"1.25.0"},42,"junk"]`) are silently dropped by the
  `isinstance(f, dict)` filter; the mixed case exits **0** — malformed
  members ride along unreported.

### D4 — route fields never type-validated; `==` on garbage matches (4 cases)

Activation at compare.py:135 requires only `"snapshot_route" in exp`; no
type check exists for either route field.

- `pred_fallback_without_route_key_matching_rest`: prediction carrying
  `fallback_to: "9.9.9"` but **no** `snapshot_route` → route fields
  silently never compared → exit **0** against a matching observation.
  Activation keys off only one of the two fields.
- `pred_route_int_obs_int` (`1` vs `1`) and `pred_route_dict_obs_dict`
  (`{"a":1}` vs `{"a":1}`) → `==` true → exit **0**.
- `fallback_to_nonstring_double_malformed` (pred `5`, observed
  `[{"to": 5}]`) → `5 in [5]` → exit **0**.
- `pred_route_list_obs_str` (`["info"]` vs `"info"`) → exit 1 masked as
  verdict instead of exit 2.
- `pred_route_null_obs_none` (null vs `"none"`) → exit 1 masked — null is
  not a legal `snapshot_route` yet is compared as if it were.

### D5 — `""` conflated with null in `_contains_or_both_empty` [LOW]

compare.py:116 `if predicted in (None, "")` — `untested_version: ""` is a
legal str (passes `_is_str_or_none`, :69-70/93) but is treated as "no
prediction": predicted `""` vs observed `[""]` → `len([""]) != 0` →
**mismatch** for an exact value match. Prediction containing the empty
string can never match an observation that actually reported it.

## Observation vs inference

- Observed: all exits/stderr above from the 31 subprocess runs (driver
  stdout reproduces the full table + JSON detail).
- Observed: genuine-mismatch controls exit 1; route discrimination on
  real retained shapes is intact — these are input-validation defects,
  not verdict-logic defects on well-formed data.
- [INFERENCE] `want=2` annotations encode the contract (contract.md:6:
  "2 could-not-evaluate (bad input ...)"); one could argue absent
  route keys deserve exit 1 rather than 2 — D2's exit-**0** cases are
  indefensible under either convention.
- [INFERENCE] Severity is bounded in practice because every observation
  this lane feeds compare.py is produced by this lane's log-extract.py,
  which always emits `snapshot_route`/`snapshot_fallbacks`
  (log-extract.py:242-244) — the crashes/false-matches require foreign
  or hand-mutated observations. Still a calibration defect: the tool's
  own JSON output contract promises exit 2 for bad input.

## Suggested fix (advisory, not applied)

Extend `load_inputs`: require `observation.snapshot_route` str and
`snapshot_fallbacks` list[dict-with-str-`to`] whenever the prediction
carries route fields; require `expected.snapshot_route`/`fallback_to`
str|null; treat top-level `null` bodies as parse-but-invalid (append the
existing "required" errors even when `data[tag] is None` after a
successful parse); make `_contains_or_both_empty` key on `is None` only.

## Retained evidence

- Driver: `.ufo/waves/round-17/w2/compare-attack.py` (exit 1, 19 findings).
- Full run table + JSON detail captured at execution (reproduced by the
  command above); 4 crash stderr tails shown in D1.
- Anchors: compare.py:86,101,105-108,116,123,125,135,139-142,145-146;
  contract.md:6,76-78; log-extract.py:242-244;
  predictions/pro-notesmd-cli.prediction.json:15-21 (real route shape);
  runs/pro-notesmd-cli/observation.json tail (snapshot_fallbacks/route).

Tooling: none installed; stdlib only, Python 3.14.8.
