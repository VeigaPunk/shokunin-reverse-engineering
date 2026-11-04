# MutProbe — frozen counter mutation battery

Axes: mutation sensitivity; observation completeness; exact restoration; write-scope isolation.

Frozen source: `4737a542ae3b1b910d8fe43efbd572bc578b07c6`, extracted using read-only git show. Real-input runs used declaration revision `8b82516182a269482f3a7dc96b50cd2ac349f3a6`, base `5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d`, base probe `5ee94c56ce7490938ee38c2e5c10930a1fd1330a`, the round-69 landing receipt and round-70 declaration receipt specified in the assignment. Every command, rc, full stdout and stderr is preserved in adjacent JSON records. No tools installed or updated.

## Mutation table

The bounded behavioral detector is the counter's actual CLI run on identical inputs before, during and after its mutation. Each mutation affected scratch bytes only.

| Counter | Single mutated expression | Pristine → mutant → restored rc | Actual observation | Verdict |
|---|---|---|---|---|
| forged-receipts | line 218: expected landing rc becomes 0 for F1_wrong-rev only, instead of 1 | 0 → 1 → 0 | Mutant names only F1_wrong-rev as failing; reader actually returned 1 and named rev clause | Killed |
| seam-probe | line 192: A1 expected rc 2 → 0 | 1 → 1 → 1 | 6/7 → 5/7 → 6/7; failed arms A7 → A1,A7 → A7 | Inconclusive globally: pristine already fails; A1 sensitivity independently visible, not counted as killed |
| controls | line 128: base-forged acceptance expected rc 0 → 1 | 0 → 1 → 0 | Mutant names `c1: base reader did not accept the wrong-rev shape`; actual base rc remains 0/met true | Killed |
| mutation-check | line 141: target-pin mismatch `!=` → `==` | 0 → 1 → 0 | Matching genuine pin becomes `matched:false`, named target pin mismatch; all five route mutants still killed | Killed by matching-pin detector |

Additional paired input for the SAME target-pin mutant: intentionally wrong pin `deaddeaddeaddeaddeaddeaddeaddead` gives rc **1 → 0 → 1**. Mutant wrongly reports `target_pin.matched:true`, `ok:true`, no defect. This is a real false-green *mutated counter* under the wrong-pin input; the matching-pin positive control kills it. Do not misreport this as a surviving mutant across the combined detector or as a defect in the unmodified target-pin check.

## Frozen seam defect: A7 cannot invoke its battery

The pristine frozen seam-probe returns 6/7, not 7/7. `A7_per_run_work` records rc_a=rc_b=2, work_dir_a=work_dir_b=null, distinct=false. Its shared `invoke()` adapter (lines 133–135) unconditionally passes `--pkg`; frozen mutation-check does not accept that argument. Reproducing the exact A7 argv directly yields:

```
mutation-check.py: error: unrecognized arguments: --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
```

Evidence: `seam-probe-pristine.json`, `seam-probe-restored.json`, `mutation-check-seam-a7-exact-argv.json`. Both pristine and restored runs show the same failure; it is not caused by the A1 mutation. This defeats the claimed frozen 7/7 seam at the tested declaration revision. No repair applied.

## Honest observations and structural-honesty negatives

Actual generated receipts are preserved as `*-honest-receipt.json`. Forged-receipts carries ten shape rows with base/landing rc, rejection clauses, and identity-probe observations, plus genuine and battery arms. Controls carries seven `observed` dictionaries. Mutation-check carries pristine selftest data, target/floor observations and five mutant rows. Seam-probe carries seven `observed` dictionaries, including its honest A7 failure. Thus none of these actual runs merely prints ok=true without observations; seam's run is honestly red.

The separate `--validate` entry points are weaker than the actual producers. All four accept their original receipts (validation denotes structure, not successful behavior). Removing evidence produces:

| Validator | Evidence removed | rc | Finding |
|---|---|---|---|
| forged-receipts | Per-shape observed details except shape/clause/base_rc/landing_rc; genuine reduced to `{ok:true}`; battery_arms omitted | 0 | Accepts declarative constants without genuine/battery observations or clause_found/probe evidence |
| controls | All seven `observed` dictionaries | 0 | Accepts all-green arm labels with no per-arm observations |
| mutation-check | pristine result, target_pin, pristine_floor, per-mutant cases/expect_case/stderr | 0 | Accepts receipt lacking pin/floor/pristine observations; still retains rc/failed/verdict rows |
| seam-probe | All seven `observed` dictionaries | 1 | Correctly names seven missing-observation defects |

These are observed structural-honesty coverage holes, not proof that a full actual-run counter accepted a flipped arm. Inputs and raw validator outputs are adjacent `*-redacted-receipt.json` / `*-validate-redacted.json`. Validators' intentionally structural scope does not establish behavioral success.

## Restoration and scope evidence

`hashes.json` records full SHA-256 before/mutated/restored for all four counter copies. Restored hashes were computed from restored file bytes and equal frozen before hashes:

- forged-receipts: `b64e5e5ad52751d8c69448028418f37585c84ee0725239a3570c93b702be2c8c`
- seam-probe: `ffb2a1685d4b9ddedfd4ebdec57131cbc110bab889c1dcd9eb6189ff5ad357a6`
- controls: `fb9443d4a89ee1836af3232777873dd91f38b714f4c268df08a7e34248b33d8b`
- mutation-check: `d2d9a49f509e9ec2aad3f38ec9c3b7e520a816dc3dc9d73810fc4c62510934a9`

All restored counters reran the identical bounded detector; output rc sequences are above. Ten actual forged fixture files were copied into `forged-shapes/` before scratch cleanup. Only own findings and scratch were written. No git/jj mutation, sibling source modification, system installation, or alternate runtime invocation. This report stays in the explicitly authorized seat directory rather than the conflicting sibling-level Report trailer path.

VERDICT: not-met — frozen seam A7 fails on unsupported --pkg; three arm mutants killed, seam mutant inconclusive, and three validators accept evidence-stripped receipts.
