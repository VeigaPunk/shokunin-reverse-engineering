# MutProbe — frozen seam selftest mutation probe

Frozen source: `34fe7aa70b627d92e2d27dbce308d9f5bebda63d`. All edits were isolated scratch copies; lane instruments were untouched.

Axes: detector sensitivity, exact restoration, historical comparability.

Detector: `python3 -I -B <absolute scratch-copy> --selftest`, 30-second timeout; pristine, mutated, and restored bytes use the same detector. Round-72 baseline/restored: rc 0, 10 cases, failures `[]`. Round-71 baseline/restored: rc 0, 9 cases, failures `[]`.

| Round-72 mutant | rc | failed cases | verdict | case that should bind it |
|---|---:|---|---|---|
| a-children | 0 | `[]` | survived | A11 must reject checker_child_env missing git or readelf while all other witnesses are clean. |
| b-keys-exact | 0 | `[]` | survived | A11 must reject shim environment with an extra non-canary key while checker summary is clean. |
| c-canary | 0 | `[]` | survived | A11 must reject checker summary canary_present=true with independently clean shim environments. |
| d-return-code | 0 | `[]` | survived | A11 must reject nonzero checker rc despite otherwise clean summary and shims. |
| e-present-guard | 0 | `[]` | survived | A10 malformed/missing clauses must remain fail-closed; this conjunct is redundant after clauses normalization. |
| f-non-none | 1 | `['a10-binding-from-checker']` | killed | a10-binding-from-checker must reject run_binding=false; also test zero and string values. |
| c-shim-canary | 0 | `[]` | survived | A11 must reject leaked shim canary; keys_exact independently rejects its extra key, so isolated deletion may be redundant. |

## Findings

The requested six mutations yield five survivors and one kill. The additional shim-canary deletion also survives. A11 has no direct selftest case: children, keys_exact, checker-summary canary and rc deletions are undetected. This is a coverage finding, not evidence that the full runtime seam accepts a bad checker.

`e-present-guard` deletes both `and present` verdict conjuncts, not normalization or the returned present field. Its survival is an equivalent-mutant limitation: after non-dict clauses normalize to `{}`, `is True` already rejects them. No valid ordinary-JSON counterexample distinguishes this deletion; do not count it as proof of broken fail-closed behavior. Likewise shim-canary deletion is independently guarded by exact keys.

`f-non-none` is killed by `a10-binding-from-checker`: a false checker binding is no longer accepted as a true verdict.

## Round-71 before state

The exact six requested mutations cannot be applied: round-71 has no A11 or binding_verdict. All six anchor-match counts are zero; unchanged selftests are green and explicitly marked not_applicable in results.json, never mislabeled survivors. A native historical calibration control (`binding_ok = True` in the receipt-derived A10 verdict) survives: rc 0, 9 cases, failures `[]`; patch and pristine/mutated/restored evidence are retained. No A11 backport was fabricated.

## Restoration and provenance

- Round-72 original/restored SHA-256: `7f46e3efb3c4768d16f9c5a7c01a3448b4f6dc15ae731f46f3150dc2f6e10622`.
- Round-71 original/restored SHA-256: `22b840e1427b24618ac33075169d29780887d2cffb5b7b989af8cc4bb6ee0ce2`.
- Each mutated hash, full stdout/stderr, rc, failed cases, baseline and restored result is in results.json.
- Restoration re-read each committed source blob using read-only git show; all byte comparisons match.
- Seven round-72 unified patches plus the native round-71 control patch are retained beside this report.
- No tool installation/update; no package, packer, git writes or sibling/lane-source edits.

## Scope and risks

Exact six-way before-state scores are unavailable because the requested behaviors did not exist in round-71; reporting green unchanged runs as kills/survivors would be misleading. No contract changes or integrations are proposed.

## Self-evaluation

Accuracy 4: exact historical comparison is structurally unavailable and is explicitly N/A. Completeness 4: all new mutants plus both canary interpretations exercised; historical forced-true control substitutes only as a labeled control. Clarity 4: redundant deletions separated from genuine detection gaps. Actionability 5: patches and complete detector transcripts retained. Conciseness 4: provenance is verbose to preserve reproducibility. Overall 4.2; improvement: add direct A11 negative cases in a separate authorized change.
