# MutationRecord — round 81 / C2

Axes: calibration and depth; no domain coverage or promotion claim. Frozen claim read at lane HEAD abdcfd3c28d98288a3dc6b4e98c88d115ed42b53; base control uses 5b59ae615a2ab68e3b421820d1c72751e1185385.

## Attack and observations

Single defect: frozen AST omission of the sole git-commit call in `make_fixture_repo()`. Expected detector: exactly one declared `record-fixture-committed-clean` row becomes false, mutant exits 1 with SELFTEST summary; pristine remains green. Counter and predicates unchanged.

| Target/control | Pristine exit / summary | Omission exit / summary | Frozen result | Interpretation |
|---|---|---|---|---|
| Round-80 base | 0 / 9,0 | 0 / 9,0 | killed 0, survivors 1 | Survives: fake battery reads worktree rather than HEAD |
| ExecRecord final candidate | 0 / 11,0 | 1 / 11,2 | killed 1, survivors 0; counter exit 0 | Killed by committed-record boundary |
| Mock-only impostor | 0 / 11,0 | 0 / 11,0 | killed 0, survivors 1; counter exit 1 | Named always-green canned receipt cannot kill |
| Crash-only impostor | 1 / no summary | 1 / no summary | killed 0, survivors 1; counter exit 1 | Inconclusive baseline, correctly not credited as kill |

Candidate mutant emits exactly one clean detector row, `pass: false`, `got: {"unevaluable": "PROVINCE.md absent at HEAD"}`. Duplicate integration row also fails for that same boundary. Both runs have empty stderr; all original nine cases remain green. Thus this is not an unrelated exception or missing-summary kill. Candidate uses real binder battery; only live `read_lines` and fixture GHIDRA path are redirected. Fixture worktree is deliberately corrupted after creation, so pristine success depends on committed bytes.

Primary receipt: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/MutationRecord/kill-run.json`. Base/control/restoration receipts are beside it: `base-control.json`, `mock-control.json`, `crash-control.json`, `controls-summary.json`, `restoration.json`, and each `*-restored.json`. Candidate snapshot, binder, base and intentionally invalid impostor sources retained there. `probe.py` and `restore.py` retain exact bounded control/restoration operations; both require explicit `--work` and `--out`. They expect retained inputs staged in that scratch. No integrated verification was run.

## Hashes and restoration

Candidate before/after SHA256: `6bffdbc1c2f027c7b70cadfb70aabdf5ec6a9e3a6067484886d3560fad3efe3c`.
Omission bytes: `d6aa5152894d8dc397e2ec0a91227ee87dfdf03f15f13ab7158dc7570ce4d472`.
Restored detector: exit 0, SELFTEST 11/0.

Binder SHA256: `a5755ba1884f0c8d695d16289edbf5dff420e72d7552d424c2cc2df7bb94a438`, matched base committed binder bytes.
Frozen counter SHA256: `52c829c604a5aac9306458cc6291b8cc648d3999ccf2eec0348666e582d524d6`.
Base before/after: `f2aa8422f4d5ac93d1e3ed2823eb72869694b46682e90d8e1e908c0555da2a0a`; restored exit 0, 9/0. Mock before/after: `a6e3e9d9bd03342b2128126b5930dbd305da91c05330944f8f3616c1e10bc60c`; restored 11/0. Crash before/after: `88bb15b2d94bd7e97c5411c036f0a9f258deeec3724968060219ad76da5a2d4b`; restored reproduces exit 1/no summary. Full mutant hashes in restoration receipts.

All fixture git writes stayed inside `/fast/scratch/hyaku/kaidoku-r81/MutationRecord/`; every fixture root was checked with `git -C <absolute-root> rev-parse --show-toplevel` before first commit. Lane production and git state untouched by this seat. TMPDIR and counter --work explicitly scoped to that scratch. No tools installed, no client configs read, no build/test sweeps.

## Opened source decisions

Opened and admitted as command-semantics evidence: https://git-scm.com/docs/git-show — DESCRIPTION: “For plain blobs, it shows the plain contents.” Supports the binder's committed-object read, not general detector correctness. Reuse existing S255 by URL (as identified in ExecRecord evidence); no new SOURCE row created.

Opened but rejected as the primary anchor: https://git-scm.com/docs/git-cat-file — `-e`: “Exit with zero status if <object> exists and is a valid object.” The binder actually invokes git show, so cat-file is not the matching operation. Flip: binder switches its object-read boundary to cat-file. Reuse existing S256 by URL; no duplicate SOURCE row.

Assimilation: none. These are bounded empirical findings, not admission votes. L1 owns integrated frozen-command verification.

Self-evaluation: accuracy 4 (raw receipts ground findings; no integrated commit claim); completeness 4 (all assigned controls covered, not broader counter spoof resistance); clarity 4 (table distinguishes crash baseline from valid survivor); actionability 4 (receipts and exact bytes retained; rerun requires scratch staging); conciseness 4 (hash detail retained for audit). Average 4.0. Improvement priority: L1 should use final integrated revision, not scratch fixture revision, for the frozen acceptance command. Would user agree: likely, within this seat's bounds.

Report: .ufo/waves/round-81/w1/MutationRecord/MutationRecord.md

Cleanup observed: scratch deletion command completed successfully with `scratch removed; receipts retained`.
