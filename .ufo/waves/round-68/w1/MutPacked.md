# MutPacked — mutation probe on the R68-C2 route (round-68, w1, attempt 1)

Seat: mutation-tester (`MutPacked`), one of 13 seats in the single v1 build+attack wave, one of 4 attack seats.
Scope: `tools/round-68/packed-elf.py` only, scratch copies only. No lane file edited, no index touched, no commit.

- Frozen target sha256 (read-only): `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e` — re-verified unchanged after the probe.
- Base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`; operative freeze `1eaf596e5f241762349fbd102c9e09ec1df18e3f`.
- Detail, per-mutant patches and the fire matrix: `./.ufo/waves/round-68/w1/MutPacked/mutants.md`.
- Receipts: `./.ufo/waves/round-68/w1/MutPacked/receipts/` (harness, mutant copies, all JSON receipts, selftest transcripts, `MANIFEST.sha256`).

## Mandate

Five mutants, each cutting one behaviour-bearing point of the R68-C2 route, each scored by the tool's own detectors; report which detector fires, with which case name; if none fires, state what the green run would then claim and which case would bind it.

M1 `identity_ok` returns True without comparing (line 257). M2 `recovery_ok` compares the unpacked counts to themselves (line 261). M3 `detected` uses only `upx -l` rc, dropping the section-count clause (line 249). M4 `before_ok` compares the packed count to itself instead of the carrier floor (line 254). M5 the control arm is dropped from `fold` (line 289).

## Method (observation)

Four independent detectors were run on the pristine copy first, then on each mutant, then re-checked on the pristine bytes:

1. **D1 `--selftest`** — 13 registered cases.
2. **D2 `--skip-run`** — the no-claim short circuit (pins real: REA `package.json` sha `a5003023…`, version 6.5.0).
3. **D3 the real route** — actual `/usr/bin/upx` 5.2.0, GNU readelf 2.47, REA 6.5.0, the two pinned carriers `/usr/bin/jq` and `/usr/bin/xxd`, in scratch work roots. Pristine: rc 0, `met_target true`, `carriers_matched 2 of 2`, `control_ok true`, `before_procedures [3, 3]`, `section_count 0` on both, `orig_counts` 167/30/190 (jq) and 99/29/103 (xxd), floors 50/25, jq refusal `packed_rc 1` (`invalid_request`) / `unpacked_rc 0` with `FUN_00103fa0` present in 4841 bytes. This confirms the green configuration and that the frozen route is green on this host.
4. **D4/D5 fixture-root `score()` call** — the tool's real `score()`, `section_count`, `counts_from`, `carrier_arms`, `fold` and exit logic, over a modelled environment (fake `upx`/`readelf`/REA) with two fixture carriers carrying real sha256 pins. `S0_green` satisfies every arm; `S1`…`S5` each break exactly one arm's precondition. Pristine S0: rc 0, `met_target true`, `failing []`. Pristine S1–S4: rc 1 with the broken arm named in `failing`; pristine S5: rc 1, `control_ok false`, `failing []`. Deterministic (repeat run byte-identical).

A baseline failure would have been inconclusive; the pristine baseline passed on all five detectors, so silence by a mutant is a survival.

## Findings (observation)

| mutant | selftest | `--skip-run` | real green route | modelled green | firing detector / case |
|---|---|---|---|---|---|
| M1 identity_ok≡True | 13/13 pass | rc 1, payload identical but for `instrument.sha256` | rc 0 green, scoring fields identical | identical | only `S1_identity_broken`; `failing [fa:identity_ok, fb:identity_ok]` → `[]`, rc 1→0 |
| M2 recovery_ok self-compare | 13/13 pass | identical | green, identical | identical | only `S2_recovery_broken`; `failing [fa:recovery_ok, fb:recovery_ok]` → `[]`, rc 1→0 |
| M3 detected = `upx -l` rc | 13/13 pass | identical | green, identical | identical | only `S3_sections_present`; `failing [fa:detected, fb:detected]` → `[]`, rc 1→0 |
| M4 before_ok self-compare | 13/13 pass | identical | green, identical | identical | only `S4_before_above_floor`; `failing [fa:before_ok, fb:before_ok]` → `[]`, rc 1→0 |
| M5 control dropped from fold | 13/13 pass | identical | green, identical | identical | only `S5_control_hot`; `control_ok false` → `true`, `failing []` both, rc 1→0 |

Exhaustive over 5 mutants × 6 scenarios: each mutant differs from pristine in exactly one scenario and never elsewhere (`receipts/matrix.json`).

## Survivors named, and the false green each would license

All five survive every detector the lane actually runs — selftest, `--skip-run`, the real green route, and the modelled green route. The survivor set under the green configuration R68-C2 is scored in is exactly **{M1, M2, M3, M4, M5}**.

- **M1** → `identity_ok true` would no longer mean `upx -d` restored the pinned bytes; "unpack with sha identity" would be unevidenced while `carriers_matched 2 of 2` still stood. Binding case: `S1_identity_broken`.
- **M2** → `recovery_ok` would mean only "REA returned three integers"; "recovers the original's REA inventory" would be unfalsifiable. Binding case: `S2_recovery_broken`.
- **M3** → `detected` would rest solely on the packer's own verdict, dropping the independent structural clause; on the pinned carriers `section_count` is 0 either way, so the clause is never negatively exercised. Binding case: `S3_sections_present`.
- **M4** → the "stub, not the program" floor would never be compared; any packed inventory would pass. Binding case: `S4_before_above_floor`.
- **M5** → `control_ok true` would be vacuous and `met_target` would stop depending on the negative arm on the same bytes. Binding case: `S5_control_hot`.

## Coverage finding (report-only; contract untouched)

`selftest()`'s 13 cases never evaluate any of the five arm expressions: lines 313–314 (`identity-equal`, `identity-mismatch`) compare string literals `"ab"*32` / `"cd"*32` without invoking `score()`, and the remaining cases exercise `section_count`, `counts_from`, `carrier_arms`, `fold` and a literal dict. A defect in `score()`'s arm wiring is therefore invisible to `--selftest` at all five sites. The lane's registry claim of 13 cases is accurate but non-discriminating for these sites. This is a coverage finding, not permission to change the contract: no arm, threshold, carrier pin or predicate was altered, and R68-C2 stands as declared.

## Restoration evidence

- Frozen file was never written; sha256 before and after the probe identical (`48ef4c68…`) and `git status --porcelain -- tools/round-68` shows no modified tracked file (only an unrelated untracked `registry-conformance.receipt.json` from another seat).
- Each D3 receipt carries `instrument.sha256` of the copy actually executed, so every mutant receipt is self-identifying: M1 `85d34a25…`, M2 `855dbb26…`, M3 `eb769153…`, M4 `541311a1…`, M5 `0c501fa8…`; pristine `48ef4c68…`.
- Scratch `/fast/scratch/hyaku/kaidoku-r68/MutPacked/` deleted after receipts were copied here.

## Tools / channels

None installed or upgraded (no pacman transaction run; nothing needed). Used: `python3` 3.14, `/usr/bin/upx` 5.2.0 (sha256 recorded in every D3 receipt), GNU readelf 2.47, `node` v24.21.0, REA 6.5.0 invoked as `node <REA root>/scripts/rea.mjs` (never `npx -y`).

## Unknowns

- Whether a *hand-crafted* ELF can make `upx -l` return 0 while a section-header table survives — i.e. whether M3 is behaviour-equivalent on all admissible inputs, not just on the two pinned carriers. Not probed: out of seat scope.
- Whether REA analyze is bit-deterministic across hosts for these carriers (identical `evidence_id`s were observed here). Not probed.
