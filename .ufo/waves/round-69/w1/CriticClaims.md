# CriticClaims — round 69 w1 predicate attack report

Scope: falsify R69-C1, R69-C2, R69-C3 as written by finding the cheapest fixture that satisfies each
predicate sentence while the claimed capability is absent, plus re-derivation of the before-arms, the
do-nothing controls, and the C3 arithmetic. Full fixture records, commands and outputs are in
`attack.md` and the `CriticClaims/` directory beside this file. Nothing was edited or committed; all
fixtures live in scratch and in `CriticClaims/`.

## Frozen inputs (obs)

All four round-69 instruments at HEAD `3f3d20fc…` hash to the container pins; `tools/round-68/packed-elf.py`
at base `d7d9a62…` hashes to `48ef4c68…`; `claims.json` at freeze and in the worktree hashes to
`ebc68ac5…`. After-arms were run at HEAD because the A9 landing commit does not exist yet and
`tools/round-69/` first appears at `616a5f2f` (so the base revision cannot `git show` it).

## Findings per claim

### R69-C1 — not falsified as written, two counter hazards (routed)

- Serial battery at the base: rc 0, survivors exactly `M1_identity, M2_recovery, M3_detected,
  M4_before, M5_control`, `pristine.cases 13`, `target_sha256 48ef4c68…` — reproduces `c1-at-base.json`.
- Serial battery at HEAD: rc 0, survivors `[]`, five `killed`, each `failed` list naming exactly its
  declared case, `pristine.cases 20`, `pristine.ok true` — reproduces the predicate's after clause.
- A fabricated green battery receipt passes `mutation-check --validate` (rc 0); `--validate` is
  structural, but it is not the counting command, so this is not a predicate gap.
- A doctored instrument at `tools/round-69/packed-elf.py` (commit `0a9c2d07`, five arm-false cases
  gated by a sha256 of the `evaluate_carrier` body instead of a false model) yields battery rc 0 with
  the full after sentence, `target_sha256 2368bbc3…`. That is excluded by container A1 and the kill
  rule's post-freeze-edit clause, not by the counter. **Correction (routed):** have the battery refuse
  unless `target_sha256` equals the declared pin (it already computes the hash).
- **Hazard 1 — shared scratch.** Two battery runs under one `--work` race on `<work>/mutation-check`
  (rmtree). Observed: an r68 run recorded `pristine.cases 20` (round-69 bytes) while its mutants were
  round-68 bytes, `ok true` (`CriticClaims/receipts/raced-c1-r68-base.json`). Run the before- and
  after-arms serially or with distinct `--work` roots.
- **Hazard 2 — `pristine.cases` is not enforced.** `check()` sets `ok` from survivor count and wrong-case
  kills only; the predicate's `pristine.cases 20` / `13` must be read from the receipt by the L1.

### R69-C2 — falsified as a counter proposition

The probe's A1–A4 arms are genuine black-box invocations. A5/A6 read the `--receipt` file and never
bind it to the instrument or the measured revision, even though the real payload carries
`instrument.sha256` and `rev`. Measured:

- fabricated receipt (3 rows from real host sources, `instrument.sha256 0*64`, `rev e*40`, invented
  runs): **6/6, rc 0**;
- same with **one** carrier: 6/6, rc 0;
- single row whose source is **`/bin/ls`** (not a declared carrier): 6/6, rc 0 (A5 re-derived the
  `/bin/ls` pin and format);
- a six-arm probe receipt with `observed: {"invented": true}`: `--validate` rc 0.

Before-arm is reproducible: probe against `tools/round-68/packed-elf.py` at base with the round-68
receipt → 0/6, all six named, `instrument_sha256 48ef4c68…`, rc 1. The round-69 instrument with the
*old* receipt is 4/6 (A5/A6 false), so the after-target does not follow from the do-nothing receipt —
but it does follow from a fabricated one. **Correction (routed):** compare
`receipt["instrument"]["sha256"]` to the probe's `instrument_sha256` and `receipt["rev"]` to the
measured rev; require the three pinned carrier ids. No predicate change needed.

### R69-C3 — falsified as a counter proposition

`--check-receipt` returns `met true`, rc 0, on all of:

- invented counts (`f1`);
- an executable relabelled `kind: shared-object` with source `/usr/bin/xxd` and xxd's pin (`f2`);
- `packed_counts.procedure_count 183` against `before_ceiling 120` with a declared ratio 0.6522 (`f3`);
- anonymous carriers with `orig_counts {}` and packed procedure 0 (`f4`);
- **two** carrier rows while `carriers_matched` declares 3 (`f7`).

Boundary behaves: ratio 0.75 passes, 0.7501 fails; a receipt with no `shared-object` kind fails. The
checker never re-derives the ratio, never compares ids/pins/sources to `CARRIERS`, never compares
`packed_counts` to `before_ceiling`, and takes no revision. The round's own control `c3-synthetic-met`
already demonstrates the same fact (rc 0, no run). **Correction (routed):** derive
`ratio = before_ceiling / orig_counts.procedure_count`, require
`packed_counts.procedure_count <= before_ceiling`, require the three pinned ids/pins/sources, and
bind `instrument.sha256`/`rev`. No predicate change needed.

## C3 arithmetic and libz ceiling (obs)

10/167 = 0.059880, 10/99 = 0.101010, 120/184 = 0.652174 — none exceeds 0.75. Independent re-derivation
with upx 5.2.0 + REA 6.5.0 on the pinned `libz` (`6c78c5e5…`): original 184/29/199, packed 98/6/136
(the plan's numbers). The 120 ceiling sits 22 above the measured packed 98 (measured/original 0.5326),
so it is justified as a class bound with headroom; the counter cannot verify that (f3).

## Do-nothing controls

Re-ran `controls.py` at HEAD: rc 0, all seven arms ok, observations equal `controls-at-base.json`.
C1 and C2 after-targets do not follow from their do-nothing arms (5 survivors; 0/6). **C3's after-target
does follow from a synthetic receipt with no run** — `c3-synthetic-met` rc 0 (the round's own control),
matching the f1–f4/f7 fixtures. That is the crux of the C3 gap.

## Verdicts

- **R69-C1:** predicate holds within the pinned bytes; fixture attack fails without a pin violation.
  Counter robustness defects routed (pin binding, `pristine.cases` enforcement, scratch race).
- **R69-C2:** predicate sentence satisfiable by a fabricated receipt (6/6) that the counter cannot
  distinguish from the measured run's. Routed.
- **R69-C3:** predicate sentence satisfiable by fabricated receipts (met true) with invented counts,
  a relabelled executable as shared-object, an inconsistent ceiling, anonymous carriers or a missing
  row. Routed.

No claim was narrowed, widened or re-frozen. Impacted axes: C1 calibration, C2 operability, C3
coverage.

## Artifacts

- `CriticClaims/attack.md` — fixture-by-fixture commands, rcs and outputs.
- `CriticClaims/fixtures/` — the fabricated receipts and the checker outputs.
- `CriticClaims/receipts/` — serial before/after battery receipts, the raced receipt, the doctored
  fixture receipt, the C2 base/after probes, the controls run, the C3 base check.
- Scratch `/fast/scratch/hyaku/kaidoku-r69/CriticClaims/` was removed before yield; the fixture git
  repo lived there and is gone (its commit id and battery receipt are preserved above).

## Unknown

- The L1's real after-run receipt does not exist yet; whether it will carry the same self-declared
  fields the checker trusts is not measured here (**unk**), though the instrument's writer emits them.
- Whether the landing commit modifies any instrument after the freeze (**unk**); the battery cannot
  detect it, so the L1 must compare the four pins before scoring.
