# ExecArm — round-74 runtime seam comparison

Axes: runtime verdict preservation, receipt provenance, environment-value safety, lane isolation.

## Result

The assigned invocation completed in 30.94 seconds, exit 1, with **11/12 arms passing**, not the requested 12/12. **A12_kernel_witness is true**: genuine_ok, forged_detected, lie_clean and verdict.ok are all true. No host carrier refusal prevented scoring; no arm is unknown.

Raw probe output, with only four environment `values` dictionaries removed for the round-72 security guard, is retained at `.ufo/waves/round-74/w1/ExecArm/probe-at-freeze.json`. Every arm observation, key inventory, canary-presence boolean and verdict is otherwise retained. This is not an unredacted byte-for-byte receipt.

## Row-by-row comparison

Baseline: `.ufo/waves/round-73/l1/scores/c1-at-landing.json`.

| Arm id | Round-73 landing ok | Round-74 freeze ok | Pattern |
|---|---|---|---|
| A1_hash_before_exec | true | true | same |
| A2_threaded_path | true | false | divergence |
| A3_child_env_allowlist | true | true | same |
| A4_broken_node_typed | true | true | same |
| A5_packer_exec_format | true | true | same |
| A6_home_no_tmp | true | true | same |
| A7_per_run_work | true | true | same |
| A8_child_env_observed | true | true | same |
| A9_concurrent_collision | true | true | same |
| A10_run_binding | true | true | same |
| A11_checker_env | true | true | same |
| A12_kernel_witness | true | true | same |

Arm IDs and order are identical. Baseline arms_passed=12, target=12, ok=true; measured arms_passed=11, target=12, ok=false, failed=["A2_threaded_path"].

## Exact divergent rows

Baseline A2 row:

```json
{"id":"A2_threaded_path","observed":{"argv0s":["/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73"],"defects":[],"expect_upx":"/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","missing":[],"module_default":"/usr/bin/upx"},"ok":true}
```

Measured A2 row:

```json
{"id":"A2_threaded_path","observed":{"argv0s":["/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73","/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73"],"defects":[],"expect_upx":"/fast/scratch/hyaku/kaidoku-r74/ExecArm/upx","missing":[],"module_default":"/usr/bin/upx"},"ok":false}
```

This is a defect against the assigned full-pattern acceptance, not a fabricated 12/12 result. The observed divergence is explained by the historical receipt's eight producer argv paths differing from the required seat-owned scratch packer path. The A2 predicate at `tools/round-74/seam-probe.py:868-869` explicitly requires every historical argv[0] to equal the new `--expect-upx` path. Producer-binding defects and missing argv lists are empty. [INFERENCE] This demonstrates an invocation/receipt-path incompatibility, not evidence that the A12 injectable-reader/wiring refactor regressed. No implementation changes or receipt-path substitutions were made.

## Invocation and provenance

Executed from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` with TMPDIR and --work both `/fast/scratch/hyaku/kaidoku-r74/ExecArm`:

```text
python3 -I -B tools/round-74/seam-probe.py --root . --rev 021914c0e638454e507087accfe41af1ab69f185 --tool tools/round-73/packed-elf.py --battery tools/round-73/mutation-check.py --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work /fast/scratch/hyaku/kaidoku-r74/ExecArm --receipt .ufo/waves/round-73/pre/route-at-declaration.json --receipt-rev d36c6ee00122e9c991d7c8efc2e179dc0a10d9ed --expect-upx /fast/scratch/hyaku/kaidoku-r74/ExecArm/upx --nonce-commitment <read from the assigned commitment file> --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ExecArm/probe-at-freeze.json
```

`--receipt-rev` was parsed from the route receipt's own top-level `rev`. The scratch UPX copy hash was `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`, matching the pinned bytes. Measured instrument hash `ed3e26fab2ace12e94956704bab68940443fe093bd10aa2c70c75aa9c3284c1b` and battery hash `9b25ed2d47780e780f1433f40b6f5dc5bbb55a9c2d825b7ba84e7e24114df3cc` match the baseline receipt.

Scratch was removed in `finally` after receipt production; cleanup reported `scratch_removed True`. No tools installed, no git mutations, no source changes, no extra test/build/lint/format runs. LSP was not exposed in this seat; no symbol refactor was attempted.

## Risks and self-evaluation

Full 12/12 preservation is not established: A2 differs and is reported above. Security-required omission of four shim environment-value dictionaries means the retained receipt is semantically intact for arm scoring but not byte-identical to stdout. No raw environment dump is retained.

Self-evaluation (1–5): accuracy 4 (A2 mechanism observed, causality limited); completeness 4 (all 12 rows and divergence retained, raw receipt necessarily value-redacted); clarity 4 (exact rows make report longer); actionability 4 (predicate and mismatch localized, no unauthorized remediation); conciseness 4 (full rows retained to meet acceptance). Overall 4.0. The parent should resolve the A2 historical-path/new-copy contract before interpreting this run as full-pattern preservation; do not alter this measured result to green it.
