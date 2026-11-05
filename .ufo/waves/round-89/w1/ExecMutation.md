# ExecMutation — scoped findings (round 89, kaidoku)

Full table, verbatim outputs and receipts: `.ufo/waves/round-89/w1/ExecMutation/report.md`
(receipts in `.ufo/waves/round-89/w1/ExecMutation/receipts/`).

## What was run

28 single-anchor mutants (14 × `upx-field-value-repair.py`, 14 × `depth-blocks-v2.py`), each run
through `--selftest` plus the counter arms that should catch it: for the repair, the full pristine
C1 battery (`upx-field-battery.py`, REA on, `--expect-recovered 4`) for **all 14** mutants; for the
depth counter, the declared arms (base-red at `0ec2bb40…`, stub-red, green at `8bbb40cc…`,
no-target) plus five supplementary demo worlds. Pristine proofs first: repair selftest 16/16 rc 0;
depth selftest 10/10 rc 0; battery `recovered 4 of 4 … met=True exit=0` (wall 197 s, regression arm
met); depth base-red exit 1 (blocks 28), stub-red exit 1 (29/28), green exit 0 (29/29), live lane
worktree green exit 0.

## Result: 22 of 28 killed; 6 declared-arms gaps, 3 equivalents

- **Killed, both instruments (repair):** R02/R03/R04 (drop `fits_u_len` key / last-wins /
  first-wins) — caught **only via the `dinit` carrier**: case arms `test_ok`+`identity`
  (`upx: … field.repaired: Exception: compressed data violation`), control `N3-intact-idempotent`
  false, and the round-88 regression arm. R06 (inverted intact test), R13 (patch at `block0+8`,
  `field_only`: `byte 584 changed outside the sz_cpr window 580-584`). R05/R08/R12 (intact-branch
  drop, class-label swap, delta sign) are caught **only by the repair's selftest** — the battery
  passes them `met=True` because no arm reads `info["class"]`/`info["delta"]`.
- **Killed (depth):** D01 target-blind `met` (base-red flips green at 28 blocks — the M88-7 guard
  works), D03/D13 word floor, D06 absent file, D07 no-citation, D08 bare-citation start (also green
  arm: 2 landed blocks cite bare files), D09 section-end split (green arm: 8 stray `- **` bullets
  past the craft section; selftest alone would miss it), D11 missing-target refusal (rc 2 → 1),
  D12 rev-ignored (base-red reads the green worktree).
- **Declared-arms gaps (survived selftest + every declared arm; killed only by my demo worlds):**
  - **G1** R01 drop `derived <= sz_unc0`, **G3** R09 drop method-byte filter, **G4** R14 drop
    sentinel gate — the derivation's defensive filters have no red arm on any declared input.
  - **G2** R07 drop re-validation — outcome-equivalent on the battery (refuse vs write-garbage
    differ only in `false_arms` labels, which `met_target` ignores).
  - **G5** D04/D14 span floor — no words-ok/spans-short case anywhere declared.
  - **G6** D05 `start > end` ranges — no such citation in any declared world.
  - **G7** D10 `>=` target — no blocks>expect world declared.
- **Equivalents:** D02 (`resolved == expect` is implied by the other conjuncts — dead weight),
  R10/R11 (bounds subsumed by the empty `s1` range / `0 < sc <= su` on this population).

## Guard reading for the L1

1. The candidate-selection law is policed **only through identity-shaped arms on dinit**; jq/xxd/
   libz chains are single-candidate. The frozen predicate's selection strength rests on one carrier.
2. The battery never inspects the repair's info fields; a `class`/`delta` consistency arm would
   close R05/R08/R12 at counter level.
3. The derivation's defensive filters (G1/G3/G4) and the re-validation refusal (G2) are untested
   guards — one decoy-candidate selftest fixture per filter would pin them.
4. Depth: add three tiny selftest cases (words-ok/spans-short, `start>end` citation, blocks>expect
   with expect N) to close G5/G6/G7 statically; the live green arm currently carries D08/D09 alone.

## Flags

- **Pin discrepancy:** the dispatch header pins the repair at `048e2c8e…`; disk, the frozen plan
  and the pristine battery receipt's `repair_sha256` all say `332917f2…070`. The plan pin matches.
- No tools installed (nothing to record); no pacman; no mutating git outside the sanctioned scratch
  fixture (toplevel-asserted); scratch `/fast/scratch/hyaku/kaidoku-r89/ExecMutation/` deleted
  before yield; nothing cited was ever written under `/tmp`.
