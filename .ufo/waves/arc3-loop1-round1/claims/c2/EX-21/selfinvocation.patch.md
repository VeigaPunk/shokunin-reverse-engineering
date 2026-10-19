# EX-21 — SKILL.md citation-drift self-invocation cell patch text (selftest 11 → 13)

Seat EX-21, chain c2, wave `arc3-loop1-round1`, 2026-10-19.
Target: `SKILL.md:371`, cell 4 (Self-invocation) of the `citation-drift` registry
row. **NOT APPLIED by this seat** — patch text only (seats never write SKILL.md).

Base: HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`; `SKILL.md` sha256
`5c93c7c1bf45c72ca518f87fbba6f2a0bbf5685f67d263714b210a9a058830d4`; row sha256
`6413e8dc6384b9e0e34fca9903b55a4b8bba96066c26ca28789dc1939361d57f` (both match
EX-20's recorded values for the same base).

## Why this cell must change

C2's frozen claim (`claims-frozen.md:46-50`): "selftest 11 → 13 cases
(clean-tree, tampered-table, absent-table) at exit 0". The cell today advertises
`11 isolated-fixture cases` and names only the eleventh
(`revision_unresolvable`). The patch updates the count, names the two new guard
cases, and updates the instruction text so the cell states what the selftest now
runs. Cells 3 and 5 (guard semantics; the table self-digest pin) are EX-20's
artifact (`claims/c2/EX-20/registry-row.patch.md`); this patch is the cell-4
piece of the row.

## Before (measured at HEAD, 2026-10-19, by this seat)

- `python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest` →
  `CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0`
- entry: `CITATION_DRIFT_VERDICT: reported findings=0 exit=0` (strict: `clean`)
  — matches EX-25's independent before-logs.
- The hazard the guard closes (real probe, scratch tables, read-only over the
  repo): emptied-`entries` table → `reported findings=0 exit=0`; appended-space
  table (semantically identical JSON) → `reported findings=0 exit=0`. Silent in
  both modes.

## The patch (unified diff, applies to `SKILL.md` at HEAD)

Apply from the repo root with `patch -p1 < selfinvocation.diff`.

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -368,4 +368,4 @@
 | Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
 |---|---|---|---|---|
 | interactive-r1-recovery | gate / kaidoku | `python3 .ufo/rounds/interactive-r1/verify-recovery.py`; 0 clean, 1 failed, 2 could-not-evaluate; `--admission` checks this recovery's unresolved prerequisites and returns 2, never native judgment | same command with `--selftest`; asserts isolated subprocess exit codes and stable finding IDs | `.ufo/rounds/interactive-r1/expected.json` pins every snapshot input and expected outcome; normal entry read-only in this repo; selftest creates and removes only its isolated fixture directory under `.ufo/rounds/interactive-r1/` |
-| citation-drift | probe / kaidoku | `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`; **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate** | same command with `--selftest`; 11 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent `--rev` → exit 2, finding `revision_unresolvable`), the case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation and `expected.json` pins the self-test case table; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11) |
+| citation-drift | probe / kaidoku | `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`; **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate** | same command with `--selftest`; 13 isolated-fixture cases asserting exit code and a stable finding id (the dead/absent `--rev` case → exit 2, finding `revision_unresolvable`; the guard cases `table_tampered` and `table_absent` → exit 2, findings `table_tampered` and `pointer_table_unreadable`, each fixture's `expected.json` pinning that fixture's table digest — the guard-pass path rides the existing `clean` case), the case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation and `expected.json` pins the self-test case table; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11) |
```

- Diff file: `claims/c2/EX-21/logs/selfinvocation.diff`, sha256
  `7e9ca4372f83215ea7569f92c66693dcd5e6350fb37ab3316e9a79cac28b55bd`.
- Exact old cell-4 string (between the delimiting `|`s, surrounding spaces
  preserved):

  ```
   same command with `--selftest`; 11 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent `--rev` → exit 2, finding `revision_unresolvable`), the case table committed in `expected.json` rather than in the script 
  ```

- Exact new cell-4 string (splice-ready, same leading/trailing spaces):

  ```
   same command with `--selftest`; 13 isolated-fixture cases asserting exit code and a stable finding id (the dead/absent `--rev` case → exit 2, finding `revision_unresolvable`; the guard cases `table_tampered` and `table_absent` → exit 2, findings `table_tampered` and `pointer_table_unreadable`, each fixture's `expected.json` pinning that fixture's table digest — the guard-pass path rides the existing `clean` case), the case table committed in `expected.json` rather than in the script 
  ```

- Row sha256: old `6413e8dc…` → new
  `fa1496c9a2d639844f9e218b98566de91dd68d7974e712af1c771613aac77e48`.
- Whole-file sha256: old `5c93c7c1…` → new
  `47ad6fdb92d0eb89d9f35a70533a44b714f59c2ca5cfe2cb54015d401cd9aea5`.
- Shape: line count unchanged 371 → 371; row still one table line
  (7 `|`-split pieces = 5 cells); diff touches only line 371.
- Apply-verify (run by this seat on a scratch copy, `patch -p1`): rc 0; result
  byte-identical to the generated file (`cmp` clean, sha `47ad6fdb…`).

## Run instructions — what was updated

- Invocation retained verbatim ("same command with `--selftest`"): in selftest
  mode the probe ignores `--root/--rev/--table` and reads the case table from
  `--expected` (`citation-drift-probe.py:454-455`, `:382-385`), and the entry
  command already passes `--expected .ufo/gates/citation-drift/expected.json` —
  so the fragment stays correct as written. No invocation change is needed.
- What the instruction text now says: the selftest runs 13 cases, names the two
  guard cases and their findings, and records the fixture-pinning requirement
  ("each fixture's `expected.json` pinning that fixture's table digest") that the
  13/13 run depends on — without per-case pins a fail-closed guard exits 2 on
  every case (SC-4 measured the failure shape; EX-24 recorded `passed=2 failed=9`
  for a related missing-pin shape).
- Entry-path run semantics (a scratch/alternate `--table` now exits 2) live in
  cell 3 — EX-20's artifact, not this one.

## Case-token reconciliation (EX-16 dependency)

EX-16 had NOT landed at this seat's close (`git status` clean over
`.ufo/gates/`; real files still `3067621a…` / `4e28ba90…` / `738b3a56…`). The
tokens written here are the best-grounded pair; substitute at integration if
EX-16's landed `expected.json` differs:

| token | written here | grounds | substitution if EX-16 differs |
|---|---|---|---|
| case (tampered) | `table_tampered` | `arc2-loop1-round3/E14.md:493` case name | hyphenated `tampered-table` (claim prose only) |
| case (absent) | `table_absent` | claim's "absent-table", snake_case convention | `table_missing` (E14's absent-class finding name) |
| finding (tampered) | `table_tampered` | `E14.md:391` finding id; EX-20's verified row text | `pointer_table_tampered` |
| finding (absent) | `pointer_table_unreadable` | landed class, already exit 2 (EX-25 before-log) | — |

Count: 13 is fixed by the claim (11 + 2; "clean-tree" is the existing `clean`
case, whose fixture expected must also pin its fixture table digest). If EX-16
lands a third new case (e.g. an unpinned-table case) → 14 and the parenthetical
must be corrected (EX-20 coupling point 4).

## Composition with EX-20's row patch

If the parent applies EX-20's `registry-row.patch.md` wholesale, replace its
cell-4 segment — "the guard cases: a clean tree passes, a digest-mismatched
table → exit 2, finding `table_tampered`, an absent table → exit 2, finding
`pointer_table_unreadable`" — with this artifact's new cell-4 string (which
names the case tokens and adds the fixture-pin clause). Cells 3/5 are
intent-identical to EX-20's; no other token differs.

## Evidence (all under `claims/c2/EX-21/`)

- Proto v2 (guard + fail-closed unpinned + 2 cases; scratch copies only):
  `tmp/proto/probe.py` sha256
  `794e57bc951eabd5f91da82bbba14715561c0f30ad9d402b60c038dd0df4915a`;
  `tmp/proto/expected.json` `3f45a2b5…`; `tmp/proto/pointer-table.json`
  `738b3a56…` (byte-identical copy of the real table).
- Proto diff (v2): `logs/proto-probe.diff` sha256
  `9d3460183cad62e4a2c3e3c4ae998561ebca78d956402d0aa46e0588460cf789`;
  apply-verify: patched HEAD probe == `794e57bc…`; its selftest
  `CLEAN cases=13 passed=13 failed=0 exit=0`.
- Selftest transcript: `logs/proto-selftest.txt`.
- Entry demos: `logs/entry-demos.txt` — tampered (emptied) → `table_tampered`
  exit 2; absent path → `pointer_table_unreadable` exit 2; byte-tamper →
  `table_tampered` exit 2; clean path → `reported findings=0 exit=0` (strict
  `clean`); unpinned expected + real table → `table_pin_absent` exit 2
  (fail-closed); before-leg silents recorded.
- Patch generation/verification transcript: `logs/patchgen.txt`.

## Defect log

- **D1 (found by SC-4, confirmed, fixed here).** The first published
  `proto-probe.diff` (v1, sha `bb22aa8a…` as SC-4 measured) was generated before
  a fixture fix and reproduced a 9/13 selftest when applied. v2 regenerated the
  diff after the fix; the current `logs/proto-probe.diff` (`9d346018…`) applies
  cleanly and reproduces `794e57bc…` with 13/13. Supersession recorded, not
  silent.
- v1 → v2 changes: finding id `pointer_table_tampered` → `table_tampered`
  (EX-20 alignment); skip-on-unpinned → fail-closed `table_pin_absent` (EX-24's
  pin-deletion attack, their §1/T3–T4).

## Attacks / limits

- Pin deletion (EX-24's attack on the v1 shape): under fail-closed a deleted pin
  exits 2 (`table_pin_absent`, demo D6). This cell's text is invariant to the
  shape choice; the shape itself is EX-16's implementation call.
- `expected.json` carries no self-digest: the pin chain terminates at a
  same-authority file (EX-20 records it; SC-4 §6 confirms). Not addressed by
  this cell.
- Count risk 13 vs 14: see reconciliation table.
