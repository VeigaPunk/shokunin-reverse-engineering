# R40W2C2CounterMutants — mutation test of `tools/round-40/c2-counter.py`

**Verdict: DEFECTS FOUND** — 5 of 19 single-logic mutants survived both detectors (coverage gaps in the counter's test battery and in the real-run detector at the measured revision). The R40-C2 MET verdict at 42c10a58 is not overturned by any mutant: no mutant turned tampered claim data into a false MET. Survivors are coverage findings, not contract changes.

**Attacked:** the claim that the frozen C2 counter (`tools/round-40/c2-counter.py`, seed bytes == freeze 7fce3086 blob, sha256 `9bd792494ca042d840371e525ed6ea6a1f841f68415e4c405c41c13057183dd1`) actually detects what P40-C2 says it detects: seed==freeze, regeneration comparison, v2 table identity, manifest-after-freeze ordering, digest checks, pair match, the L1-added NOMATCH_PAIR row handling, `arms_valid` incl. `ood`, and the `met_target` formula.

## Method

- Detectors per mutant, both run on every mutant:
  - **D-selftest**: `python3 -I -B <mutant> --selftest`. Pristine: exit 0, `{"cases": 42, "green": 11, "red": 31, "pass": 42, "fail": 0}`. Kill = exit != 0 or the selftest JSON differs.
  - **D-real**: `python3 -I -B <mutant> --root <LANE> --rev 42c10a58cb2cae3a4a0122af35a0cf95ac718043 --freeze 7fce308631a8b457d6b7c5a4b39a923c4e9a49de --json-out <scratch>`. Pristine: exit 0, `matched 26/26, bindings_false [], distinct_decisions 12, met_target true` — reproduces `.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`. Kill = exit != 0 or stdout summary differs.
- Mutants are one-string replacements of a scratch copy (`HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r40/R40W2C2CounterMutants/mut/`); the lane was **never** written (no sandbox clone needed — the counter reads the lane via read-only git only). Restoration evidence: lane file sha256 before and after the whole battery is `9bd79249…83dd1`; `git status --porcelain -- tools/round-40/` = 0 entries.
- Driver and raw outputs: `.ufo/waves/round-40/w2/artifacts/R40W2C2CounterMutants/` (`mutdrive.py`, `mutants-summary.json`, `baseline-selftest.out`, `baseline-real.json`, per-mutant sources in `mutants/`, receipts for all survivors and real-run kills).
- Tooling installed: none (python3 stdlib + read-only git; no pacman touched).

## Results — 19 mutants: 14 killed, 5 survived, 0 inconclusive

| Mutant | Locus (single logic change) | Verdict | Killed by | Evidence |
|---|---|---|---|---|
| M01 | `seed_matches_freeze` := True | killed | selftest | `seed != freeze: binding seed_matches_freeze not false (got True)` |
| M02 | `regenerated_seed_matches_freeze` := True | **SURVIVED** | — | both detectors green |
| M03 | regen compare: regenerated sha256 no longer vs manifest pin | **SURVIVED** | — | both detectors green |
| M04 | regen compare: regenerated arm no longer vs manifest arm | **SURVIVED** | — | both detectors green |
| M05 | `v2_table_identical` drops `v2_rev == v2_fz` | killed | selftest | `v2 table edited after freeze: binding v2_table_identical not false (got True)` |
| M06 | `V2_COLUMNS` drops `action` | killed | selftest | `v2 header lacks action: binding v2_table_columns not false (got True)` |
| M07 | `manifest_after_freeze` drops `ma != freeze` + `is_ancestor` | killed | selftest | `manifest added before freeze: binding manifest_after_freeze not false (got True)` |
| M08 | `manifest_before_envelopes` := True | killed | selftest | `envelope before manifest: binding manifest_before_envelopes not false (got True)` |
| M09 | envelope `digest_ok` := `ebytes is not None` | killed | selftest | `subject digest mismatch: binding envelopes_valid not false (got True)` |
| M10 | `commit_ok` drops sha equality | killed | selftest | `carrier not committed as pinned: binding carriers_committed not false (got True)` |
| M11 | `pair_match` compares label only | **SURVIVED** | — | both detectors green |
| M12 | `pair_match` := True | killed | selftest | `best table plus a * default row…: want exit 1 got 0` |
| M13 | L1 NOMATCH: drop `or label == 'unclassified'` row exemption in `reported` | killed | **real** | exit 1, `bindings_false=['decisions_reported','row_decisions_consistent']`, matched still 26 |
| M14 | L1 NOMATCH: drop `or k == NOMATCH_PAIR` in `consistent` | killed | **real** | exit 1, `bindings_false=['row_decisions_consistent']` |
| M15 | `arms_valid` drops `'ood'` | killed | **real** | exit 1, `bindings_false=['arms_valid']` |
| M16 | `met` drops `bindings_ok` (single site) | killed | selftest | red cases want exit 1, get 2 — the `met_target_consistent` guard fires (`unevaluable met_target_inconsistent`) |
| M17 | frozen-path scan narrowed to `COUNTER` only | killed | selftest | `interpreter edited after freeze: want exit 2 got 0` |
| M18 | `generator_sha_matches_freeze` := True | killed | selftest | `generator object with wrong sha: binding generator_sha_matches_freeze not false (got True)` |
| M19 | `writer_matches_manifest` := True | **SURVIVED** | — | both detectors green |

Detector split: 11 selftest-only kills, 3 real-run-only kills (M13, M14, M15 — exactly the L1-added NOMATCH exemptions and the `ood` arm; the real manifest at 42c10a58 has arms `{after: 20, before: 4, ood: 2}` and the `unclassified/none` pair maps to rows `[null]`, carriers H25/H26). The 42-case battery never builds a row-less expected pair or an `ood` arm, so those loci are pinned only by the real data; the complement is also true (all 11 selftest-only kills pass the real run because the frozen data genuinely satisfies those equalities).

## Survivors and the test each needs

1. **M02 — regenerated-seed binding.** The counter always invokes the generator with `--seed FREEZE`, so the regenerated manifest's seed can only disagree if the generator ignores its seed argument; no selftest fixture builds such a generator. *Needed test:* red selftest case whose stub generator writes a foreign seed (e.g. `'0'*64`) into its manifest → pristine must exit 1 on `regenerated_seed_matches_freeze`.
2. **M03 — regenerated-digest comparison.** Every fixture's manifest pin is derived from the body the stub generator itself wrote, so regenerated bytes can never disagree with the pin. *Needed test:* fixture that tampers the committed manifest `sha256` of one carrier (pin ≠ regenerated bytes) while keeping the committed bytes equal to the pin → pristine must exit 1 on `carriers_regenerated`; with M03 it would not.
3. **M04 — regenerated arm/class cross-check.** No fixture lets the committed manifest's `arm`/`class` disagree with the regeneration (e.g. `before` vs `after`). `arms_valid` only checks membership, not equality. *Needed test:* manifest entry with `arm` flipped relative to the regenerated manifest → pristine must exit 1 on `carriers_regenerated`.
4. **M11 — pair_match ignoring action.** The battery's `label right, action wrong` case corrupts one carrier of a class; the resulting bogus expected pair then shares its row with another pair, so `row_decisions_consistent` fires anyway and masks the pair_match regression. The real data at 42c10a58 is fully consistent, so D-real cannot see it either. *Needed test:* wrong `expected_action` applied to **both** carriers of one class (same wrong value, label still right, no other pair moves) → pristine must exit 1 on the pair mismatch alone; with M11 it exits 0.
5. **M19 — declared writer digest.** No selftest fixture declares a `generator.writer.sha256` at all (declared `None` → binding vacuously true), and the real manifest declares the true freeze sha (`f535e60e…41188`, verified against the freeze blob). *Needed test:* `gen_obj`-style fixture with `writer.sha256 = 'f'*64` → pristine must exit 1 on `writer_matches_manifest`.

Pattern: every survivor vacuates a **cross-check binding whose two sides cannot disagree in any existing fixture and do not disagree in the frozen data** — redundant on green data, unpinned against a targeted fabrication. Suggested hardening is the five red fixtures above, not a contract change.

## Other observations

- M16 shows the `met_target_consistent` guard plus the red cases wanting exit 1 pin the `met_target` formula against single-site tampering (mutant → exit 2, `met_target_inconsistent`); at the real revision the mutant is indistinguishable (all bindings true), so the pin comes entirely from the battery.
- M13's kill keeps `matched == 26`: the NOMATCH row shape (`decisions_reported`) is what separates the L1 fix from a counter that silently accepts unrowed decisions — worth keeping as a binding.
- Limits: single-logic textual mutants only, no compound mutants; D-real exercised at the one measured revision (42c10a58); mutant selection covers every locus named in the assignment plus freeze-integrity (M17) and generator/writer digest loci (M18/M19).

## Integrity

- Pristine lane counter sha256 before battery: `9bd792494ca042d840371e525ed6ea6a1f841f68415e4c405c41c13057183dd1`; after: identical. `git status --porcelain -- tools/round-40/`: empty. No VCS mutation anywhere; mutants never touched the lane or a sibling.
- Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2C2CounterMutants` removed after archiving cited evidence into `.ufo/waves/round-40/w2/artifacts/R40W2C2CounterMutants/`. No vendor bytes copied anywhere.
