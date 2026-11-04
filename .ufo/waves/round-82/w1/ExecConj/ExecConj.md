# ExecConj — round 82 C1 independent reproduction

## Scope and axes

Axes: frozen-byte fidelity, complete predicate comparison, bounded execution, containment. Advisory candidates only; no admission/promotion decision or production edits.

Measured revision: `2d63e1a7d04d4dcff45c3908bb51be787a2f22e1`; declaration: `42c78912733357dabe8fcaf513a09c4a3c4ba2aa`; base: `9cc8fbbc893d4f76ced1ac8cf66a6239cde91770`.

## Observed results

The independent frozen C1 battery exited **0**. Receipt: `c1-battery.json`. It reports forged_total=3, refused=3, genuine_ok=true, frozen_rule_accepts_forged=3, both pin-match flags=true, ok=true, validate.defects=[]. Reasons are sorted in the receipt: binder_digest_mismatch, pristine_cases_below_floor, pristine_failures_nonzero. Each forged arm's first reason matches its declaration and every arm has met=true.

The frozen counter independently exited **0 on both retained fixture scripts**, reproducing its false greens:

| Fixture | Pristine summary | Parsed pristine cases | Frozen ok | New conjunction defects, in order |
|---|---|---:|---|---|
| fixture-undersized-pristine.py | [1,0] | 1 | true | pristine_cases_below_floor; original_cases_absent |
| fixture-dirty-pristine-summary.py | [11,3] | 1 | true | pristine_failures_nonzero; pristine_cases_below_floor; original_cases_absent |

`undersized.json` and `dirty.json` differ from the corresponding retained round-82 pre receipts **only in rev** (freeze versus base). Comparison includes complete nested stdout/stderr, cases, summaries, target and instrument hashes, binder pin and verdict fields—not merely ok. Fixture, counter, binder and landing bytes had identical hashes at base and freeze.

The genuine landing receipt has summary [11,0], 11 parsed pristine cases, no missing original names and a matching binder digest. Its conjunction returns true with no defects. The nine original names are retained verbatim in `predicate-comparison.json`. Replacing one original name while retaining 11 cases is refused with original_cases_absent.

## Candidate counterexample: summary population is not enforced

Direct, bounded calls to the **frozen** conjunction using a copy of the genuine landing receipt observed:

- Change only pristine.summary to **[1,0]**, keeping 11 case rows: accepted=true, defects=[].
- Change only pristine.summary to **[12,0]**, keeping 11 case rows: accepted=true, defects=[].

The implementation checks the summary's two-integer shape and failure component, but population uses len(pristine.cases), never summary[0]. Thus the retained undersized fixture is refused because its case list is short; the battery does not isolate refusal of a below-floor summary population when the list remains populated. This is a candidate full-conjunction gap if the declared population floor includes the reported summary population; under a case-list-only interpretation it remains an observed consistency blind spot, not an admission decision. The original fixture battery itself passes unchanged.

Evidence: `predicate-comparison.json`; retained read-only reproduction driver `predicate-probes.py`. No production fix proposed or applied.

## Revision and execution binding

Frozen gate SHA-256: `6155a1ffa7564acffc755caeafbe450f5b080d00526edf4bef247444ad04e1af`.

Counter: `52c829c604a5aac9306458cc6291b8cc648d3999ccf2eec0348666e582d524d6`.

Binder: `a5755ba1884f0c8d695d16289edbf5dff420e72d7552d424c2cc2df7bb94a438`.

Exact argv, cwd, explicit TMPDIR and return codes: `commands.json`. Executed scripts were byte-exact copies extracted with git show at the frozen revision; equality with working-tree scripts was asserted before execution. Root reads and receipt loads used the explicit revision. This was not a printed-command/C2 execution assessment.

All runs used `/fast/scratch/hyaku/kaidoku-r82/ExecConj/`, explicit TMPDIR, and counter --work beneath it. Scratch was removed after evidence retention: `cleanup.json`. The two fixture scripts perform no git mutations; no fixture commits were necessary. Python 3.14.8 was already available; no installs/updates or pacman transactions occurred. No LSP tool is mounted; this read-only execution slice required no symbol refactor. No build/lint/test sweep, delegation, external-state remediation or production write occurred.

## Retained files and limits

All files are under `.ufo/waves/round-82/w1/ExecConj/`: this report, `commands.json`, `c1-battery.json`, `undersized.json`, `dirty.json`, each run's `.stdout.txt` and `.stderr.txt`, `predicate-comparison.json`, `predicate-probes.py`, `cleanup.json`.

The battery's third false green is a re-derived frozen-rule control over the binder-swapped landing record; it is not a third live counter execution. Only the two assigned fixture scripts were independently run through the frozen counter. No C2 verdict or broader domain capability claim is made. No blockers.
