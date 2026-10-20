# MutateCompareRoute — round 17 wave 2

Author-side advisory mutation probe. Axes: **calibration** (what CLEAN actually detects) and **depth** (route/destination discrimination).

## Result

**Observation:** 10 independent one-line mutants, five per target, all **SURVIVED the requested `--selftest` detector**: killed 0, survived 10, inconclusive 0. Each mutant also changed its intended behavior under a separate bounded witness. Every witness passed its specified oracle on pristine/restored bytes and detected its mutant; these supplemental witnesses are **not** existing selftest coverage.

This is a concrete **selftest coverage finding**, not evidence that the pristine route implementation is wrong. No pristine behavioral defect was observed in these ten witnesses. No contract changes or production fixes were made.

Scope: `.ufo/waves/round-17/tools/{compare,predict}.py` at `da64646adcb19c1ede7537b799b8c7d283fe43da`. `git ls-tree` and `git hash-object` matched these working-file blob IDs before copying:

- compare: `ae4cc19935e6417568afaafb05392c2869e832ea`
- predict: `db5559bdcb60f05b1b6031e350f6b9c3a5a504f1`

## Detector and exact commands

Isolated root `D=/tmp/r17-MutateCompareRoute-zOmIWt`; each ID below owns `D/ID/compare.py` or `D/ID/predict.py`. A stage runs the ten independent copies concurrently, with a 30-second timeout per selftest/witness child. Exact stage commands, all exit 0 and empty stderr:

```sh
/usr/bin/python3 -B -I /tmp/r17-MutateCompareRoute-zOmIWt/run_stage.py baseline
/usr/bin/python3 -B -I /tmp/r17-MutateCompareRoute-zOmIWt/run_stage.py mutated
/usr/bin/python3 -B -I /tmp/r17-MutateCompareRoute-zOmIWt/run_stage.py restored
```

For each ID and each stage the selftest argv is `/usr/bin/python3 -B -I D/launch.py D/ID/TOOL.py --selftest`, with the displayed D/ID/TOOL substitutions. Actual example:

```sh
/usr/bin/python3 -B -I /tmp/r17-MutateCompareRoute-zOmIWt/launch.py /tmp/r17-MutateCompareRoute-zOmIWt/P1/predict.py --selftest
```

Actual stdout and exits for **every** respective copy in **all three stages**:

```text
C1–C5: exit 0; stdout: SELFTEST: CLEAN cases=10
P1–P5: exit 0; stdout: SELFTEST: CLEAN cases=17
stderr: empty in all 30 invocations
```

The unchanged targets' selftests launch their own subprocesses without `-B`. To obey the no-bytecode requirement without altering target code, `launch.py` contains:

```python
import pathlib
import runpy
import sys

sys.executable = str(pathlib.Path(__file__).with_name("python-B"))
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
```

`D/python-B` is executable and contains `#!/bin/sh` followed by `exec /usr/bin/python3 -B "$@"`. Thus target CLI children also run with `-B`. No REA/Ghidra/carrier execution, dispatch, installs or updates.

## Mutants and behavioral outputs

All anchors below are relative to the lane and name the unmodified revision. Every listed mutation changed only that line in its own `/tmp` copy. **Verdict for every row: SURVIVED `--selftest`.**

### Comparison

| ID | Original point and injected defect | Witness output: pristine → mutated → restored |
|---|---|---|
| C1 | `.ufo/waves/round-17/tools/compare.py:135`: `if "snapshot_route" in exp:` → `if False:` (drop route activation) | exit `1 → 0 → 1`; `all_match=false → true → false`; mutant `route_fields=[]` |
| C2 | `compare.py:146`: prepend `field == "snapshot_route" or` to equality (always accept route) | exit `1 → 0 → 1`; mutant route `{predicted:"info", observed:"fallback", match:true}` |
| C3 | `compare.py:148`: prepend `field == "fallback_to" or` to membership (always accept destination) | exit `1 → 0 → 1`; mutant destination `{predicted:"1.99.2", observed:["1.99.1"], match:true}` |
| C4 | `compare.py:140`: `f.get("to")` → `f.get("from")` | exit `0 → 1 → 0`; mutant destination `{predicted:"1.99.2", observed:["1.99.5"], match:false}` |
| C5 | `compare.py:146`: use `predicted[field] != observed[field]` only for `snapshot_route`, retaining equality for the boolean | exit `0 → 1 → 0`; mutant route `{predicted:"info", observed:"info", match:false}` |

For C2/C3, mutant `all_match=true`; for C4/C5, mutant `all_match=false`. Pristine/restored route-field projections matched exactly. Witness argv for each C ID:

```text
/usr/bin/python3 -B -I D/launch.py D/ID/compare.py --prediction D/fixtures/ID.prediction.json --observation D/fixtures/ID.observation.json
```

Synthetic unit fixtures, not retained carrier observations: every prediction has `expected.untested_version=null`, `snapshot_label="1.99.5"`, `missing_bootstrap=false`; every observation has `untested_versions=[]`, `snapshot_labels=["1.99.5"]`, `missing_bootstrap=false`. Route additions:

| IDs | Predicted route / fallback_to | Observed route / snapshot_fallbacks |
|---|---|---|
| C1,C2 | `"info" / null` | `"fallback" / []` (deliberately isolate route equality) |
| C3 | `"fallback" / "1.99.2"` | `"fallback" / [{"from":"1.99.5","to":"1.99.1"}]` |
| C4 | `"fallback" / "1.99.2"` | `"fallback" / [{"from":"1.99.5","to":"1.99.2"}]` |
| C5 | `"info" / null` | `"info" / []` |

Negative C1–C3 pristine exits 1 are the **expected mismatch**, not baseline failures.

### Prediction

| ID | Original point and injected defect | Input; actual `(snapshot_route, fallback_to)` pristine → mutated → restored |
|---|---|---|
| P1 | `.ufo/waves/round-17/tools/predict.py:216`: `if sel_patch == ver[2]:` → `if sel_patch == 0 or sel_patch == ver[2]:` | `go1.98.4`: `("fallback","1.98.0") → ("info",null) → ("fallback","1.98.0")` |
| P2 | `predict.py:212`: missing-base route `"none"` → `"info"` | `go1.97.1`: `("none",null) → ("info",null) → ("none",null)` |
| P3 | `predict.py:219`: destination formatting uses requested `ver[2]` instead of `sel_patch` | `go1.99.5`: `("fallback","1.99.2") → ("fallback","1.99.5") → ("fallback","1.99.2")` |
| P4 | `predict.py:217`: exact-route `"info"` → `"fallback"` | `go1.99.2`: `("info",null) → ("fallback",null) → ("info",null)` |
| P5 | `predict.py:219`: replace formatted fallback destination with `None` | `go1.99.5`: `("fallback","1.99.2") → ("fallback",null) → ("fallback","1.99.2")` |

All 15 prediction witness CLI runs exit 0. Witness argv, substituting ID/input from the table:

```text
/usr/bin/python3 -B -I D/launch.py D/ID/predict.py --go-version INPUT --golang-root D/fixtures/golang
```

The fixture has bases `go1.21.0.json`, `go1.98.0.json`, `go1.99.0.json`, each `{"all":{"Types":{}},"linux":null}`, and only `patchverdiffs/go1.99.2.json.diff` with `{"sections":[]}`. In every stage, selection status/selected_patch remained P1 `base_only/0`, P2 `missing_base/null`, P3/P5 `fallback_diff/2`, P4 `exact_diff/2`. Therefore the witnessed changes are route/destination corruption, not selector changes.

## Missing cases / causal explanation

**Observation:** comparison fixtures at `.ufo/waves/round-17/tools/compare.py:193-243` have no `expected.snapshot_route`. The ten cases at `compare.py:273-322` consequently never enter the route block at `compare.py:135-142`. Missing cases are route match/mismatch, destination match/mismatch, from-vs-to discrimination, and presence of both additional verdict fields.

**Observation:** prediction's CLI cases at `.ufo/waves/round-17/tools/predict.py:303-331` include exact diff, fallback diff and missing base, but the assertion projection at `predict.py:344-360` contains neither `snapshot_route` nor `fallback_to`. Its `1.98` base-only/no-diff fixture is never requested with a nonzero patch. Missing assertions are `none/null` for absent base, `info/null` for exact diff and patch zero, and `fallback/selected-version` for lower-diff and nonzero-request/base-only routes. The actual P1 witness supplies the missing latter case.

**Source basis, not a runtime observation:** installed `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:122-126` returns before diff lookup if the base is absent; `:148-166` warns whenever the selected patch differs from the request, including reaching zero, and otherwise logs INFO. This supports the witness oracles without invoking Ghidra. Unexercised additional combinations above are proposed coverage, not claimed tested cases.

**Inference:** CLEAN provides no regression protection for these integrated route/destination semantics. This does not negate the retained comparisons or establish a pristine production error.

## Hashes and restoration

SHA-256 before **and** after restoration (all five corresponding copies):

- C1–C5: `82a18846e4ad92806882d469931cfe2b8fce7b07d80fe082f7dac1f8d9939e16`
- P1–P5: `79780c99bb0d293e1c1f6a8487db9b5befa3ad17d7350fc2e8441bce8312449b`
- Read-only r16 selector dependency: `6917da09fe61644a0e091e4e1763eda89c32db9de02aa29dad9d275cd50ef430` (initial pin only).

| ID | SHA-256 while mutated |
|---|---|
| C1 | `30f70eb88c9ff74bcf2415a4afe9ef8b1afdbd99bc6d5d6cb69c831301353481` |
| C2 | `fb3eb575c9b403776e0811088cc097f8af5bf7e974514a686f8050d35930b7c1` |
| C3 | `9f9de4a298471a28e33c8720448d0a720530c8b34c75f2494b0108ddba3e6ba2` |
| C4 | `dbf6726f50706c1da920ba79e3cfd3e0e1d0cce75dc0a6ca24f4809ada08e291` |
| C5 | `44cef890ba1770df6bfa69554b66c876037a1c80768858763841efed517906a7` |
| P1 | `e54213d536dd73fefbf56bcade0f647fa86b84a4daa59fd306ac6c8c83df5be8` |
| P2 | `52f814b87d1e148d841d5dd773c21cd05f0dd154000eb43e1f06c4db9e22783e` |
| P3 | `0677ebd3c5dac1f231f66ab04946f18a81aa59d4dd4827695dab03094106d5c7` |
| P4 | `5f0e7f991061fcd7174e94a7aafb24f399ed2bd052aac6963af8f1abd1ed526e` |
| P5 | `8d4da5764cc669aaa586d598a6368a45430cbcccd00422441c17930d9e94db74` |

Restoration executed in `finally`, using `cp D/pristine/TOOL.py D/ID/TOOL.py`; all ten copies returned 0. The restored detector recorded the original hashes above and the original outputs. Every stage also hashed each target before/after its detector: `detector_preserved_bytes=true` in all 30 records.

Full argv/stdout/stderr and hashes remain temporarily at `D/{baseline,mutated,restored}.json`; `D/run_stage.py` is the bounded witness runner. This report embeds the substantive evidence so it does not rely on `/tmp` durability. Lane tools/corpus/other files were never written; the only lane output is this report. No commits or pushes.
