# ExecRegress88 — round 89 no-harm regression under the round-89 repair

Seat: ExecRegress88 (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `0ec2bb4016655f605657d6e0e700ec2e6893ac27`.
Scope: four runs requested by the L1 (two batteries, four selftests, one `--no-rea` ablation). No edits to tracked files. No installs. No git mutation.

## Pins re-hashed before the runs (`sha256sum`, exit 0)

| file | sha256 | matches pin |
|---|---|---|
| tools/round-89/upx-field-value-repair.py | 332917f2b620da7a659b78db5bf498c8af2eba6ae529d872c2518b62ad6b1070 | yes (claims.json instruments) |
| tools/round-89/upx-field-battery.py | f6f5ed61f47e055b7cfa6b58c2e29064d8e4eb31859ff1963a8e80393cd0b720 | yes |
| tools/round-89/depth-blocks-v2.py | 359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f | yes (not run by this seat) |
| tools/round-88/upx-chain-battery.py | a01ed6227878db2a64c7274d6ad2f37aa7c2e3462629cbb1f8619094bc037160 | yes |
| tools/round-88/upx-chain-repair.py | 59ee51b0e63d3e089c23cee066b637841133412cee50748d84d717d61f8a0b46 | yes |
| tools/round-87/upx-magic-repair.py | 96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24 | yes |
| tools/round-87/upx-tamper-battery.py | 0f2d2bd80108ded5282dbb8cbf79044357538458143c97ee591cc78e8e5384b0 | not pinned in claims.json; recorded as observed |
| /usr/bin/upx | cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969 (`upx 5.2.0`) | yes |
| rea-agents package.json | a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c | yes |

## Run table

Host note: the host was shared with ~50 live peers during these runs. Wall times are measured on a loaded machine and are not a clean benchmark.

| # | label | tool (repair) | arms / controls | exit | wall time | receipt |
|---|---|---|---|---|---|---|
| R1 | round-88 class regression, zeroed/wrong `sz_cpr`, with REA | `tools/round-88/upx-chain-battery.py` (repair = `tools/round-89/upx-field-value-repair.py`) | `recovered 4 of 4`; N1-refuse-plain true, N2-corrupt-payload true, N3-intact-idempotent true; nested r87 regression `recovered 8 of 8`, met true | 0 | 204.91 s (3m24.9s real) | `r88-chain-regression.json` |
| R2 | round-87 magic class, 8 cases, with REA | `tools/round-87/upx-tamper-battery.py` (repair = `tools/round-87/upx-magic-repair.py`) | `recovered 8 of 8`; N1, N2, N3 true; met true | 0 | 135.18 s (2m15.0s real) | `r87-magic-regression.json` |
| S1 | selftest `tools/round-87/upx-magic-repair.py --selftest` | — | `SELFTEST cases=33 failures=0` | 0 | not timed (see note) | `selftest-1.log` |
| S2 | selftest `tools/round-88/upx-chain-repair.py --selftest` | — | `SELFTEST cases=11 failures=0` | 0 | not timed | `selftest-2.log` |
| S3 | selftest `tools/round-88/upx-chain-battery.py --selftest` | — | `SELFTEST cases=6 failures=0` | 0 | not timed | `selftest-3.log` |
| S4 | selftest `tools/round-89/upx-field-value-repair.py --selftest` | — | `SELFTEST cases=16 failures=0` | 0 | not timed | `selftest-4.log` |
| A1 | ablation of R1 with `--no-rea` | `tools/round-88/upx-chain-battery.py --no-rea` (repair = round-89) | `recovered 0 of 4`; N1, N2, N3 true; nested r87 regression `recovered 8 of 8`, met true | **1** | 123.37 s (2m3.4s real) | `r88-chain-regression-norea.json` |

Notes on the table:

- **R1 first attempt, not counted.** The first invocation of R1 exited 2 with `work_unusable: /fast/scratch/hyaku/kaidoku-r89/ExecRegress88/r88-chain controls_ok=None met=False exit=2`. Cause: the `--work` directory did not exist, and the battery refuses a missing work dir (`upx-chain-battery.py:257-258`). I created the directory and re-ran it. The reported R1 is the second, successful run. The first failure is not evidence of any regression.
- **Selftest wall times not recorded.** The timing wrapper failed with `error: command not found: bc`. I did not install `bc`. Each selftest returned exit 0 and printed its `SELFTEST` line; the timing is missing, not zero.
- **R2 does not exercise the round-89 repair.** R2 is wired to the round-87 repair (`upx-magic-repair.py`) by design. The round-89 repair touches the round-87 class only through the nested regression, which R1 runs (see below). R2 is recorded as the round-87 baseline the L1 asked for.

## Controls, per run

R1 (`r88-chain-regression.json`, `label` `recovered 4 of 4`, `rea_enabled` true, `repair_sha256` `332917f2…070`, `tool_sha256` `a01ed622…160`): each of the four cases (`jq`, `xxd`, `libz`, `dinit`) has `recovered: true`, `false_arms: {}`, and all five arms (`repair_rc0`, `field_only`, `test_ok`, `identity`, `rea_recover`) true.

R2 (`r87-magic-regression.json`, `label` `recovered 8 of 8`, `rea_enabled` true, `repair_sha256` `96da7d8e…c24`): eight cases, all `recovered: true`, `false_arms: {}`. Carriers and tampers: `jq`, `xxd`, `libz`, `dinit` each under `T1-zero` and `T2-foreign`.

A1 (`r88-chain-regression-norea.json`, `label` `recovered 0 of 4`, `rea_enabled` false): all four cases have `arms = {field_only: true, identity: true, rea_recover: false, repair_rc0: true, test_ok: true}` and `false_arms = {rea_recover: "REA disabled (--no-rea)"}`.

## Ablation: which arm carries the difference (R1 vs A1)

Only `rea_recover` differs. Every other arm is identical between R1 and A1 in all four cases. The `--no-rea` ablation drops the score from `4 of 4` to `0 of 4` and exits 1 because `met_target` requires all four cases recovered, and `rea_recover` is the only arm that REA gates.

The controls N1, N2, N3 and the nested regression (`recovered 8 of 8`) are unchanged by `--no-rea`. The nested round-87 counter is launched without `--no-rea` (`upx-chain-battery.py:370-374`), so REA stays on for the nested arm in both R1 and A1.

Timing: R1 204.91 s vs A1 123.37 s, a difference of 81.5 s. This is the only quantified time delta. The two runs share the nested round-87 counter, which runs REA in both. The time delta therefore fits the parent's `rea_recover` analyses, but this seat did not separately time the parent's REA calls, and the host load is uncontrolled. I do not claim a per-arm cost beyond that difference.

## Findings

1. **Round-88 class holds under the round-89 repair.** R1 scores `recovered 4 of 4` with all controls and the nested regression true, exit 0. This matches the R89-C1 regression arm.
2. **Round-87 class holds under its own repair.** R2 scores `recovered 8 of 8`, exit 0. The round-89 repair does not touch it: R2 is wired to the round-87 repair.
3. **Round-89 repair on the round-87 class, through the nested arm.** R1's nested round-87 counter, which runs the round-89 repair on the eight round-87 cases, scores `recovered 8 of 8` with the three controls true. This is the only place the round-89 repair meets the round-87 population. It holds in both R1 and A1.
4. **`--no-rea` removes only the scorer's REA credit.** A1 fails all four cases on `rea_recover` (the counter cannot credit REA-verified recovery when REA is disabled); the other arms are unchanged. This shows which arm the counter gates on REA. It does not show that the repair depends on REA, and it is not a regression of the repair.
5. **Selftests all green.** 33, 11, 6 and 16 cases, zero failures.

## Verdict

No-harm regression: **pass** for the round-88 class (R1, 4 of 4, with controls and nested regression true, exit 0), the round-87 class (R2, 8 of 8, exit 0), and all four selftests (exit 0). The ablation A1 is red as expected from the REA-dependent arm, and the `rea_recover` arm is the only one that differs.

## Tooling
No tools installed or upgraded; no install was needed for these runs. `bc` was missing and not installed. No pacman transaction attempted.

## Cleanup

Scratch `/fast/scratch/hyaku/kaidoku-r89/ExecRegress88/` (r87-magic, r88-chain, r88-chain-norea) was emptied by the batteries' own run-root cleanup and is removed before yield. Receipts in this seat directory are kept and listed below.

## Receipts (this directory)

- `r88-chain-regression.json` (R1)
- `r88-chain-regression-norea.json` (A1)
- `r87-magic-regression.json` (R2)
- `selftest-1.log`, `selftest-2.log`, `selftest-3.log`, `selftest-4.log` (S1–S4)
- `instrument-hashes.txt` (sha256 of the four tools the selftests exercise)
- `report.md` (this file)
