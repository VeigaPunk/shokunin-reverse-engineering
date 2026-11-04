2026-11-03
# MutCounter — round 67 w1: four mutants of the R67-C1 counter

Mutation-test seat for `tools/round-67/avm-le-counter.py`. Scratch copies only; the lane's counter
was never edited. Full detail — per-mutant diffs, receipts, driver shas, commands, baselines — in
`.ufo/waves/round-67/w1/MutCounter/mutants.md` and its `M1…M4/`, `baseline/`, `fixtures/`
subdirectories.

## Verdicts (all measured on the live instrument, sha `e44cacf5…`, `HEAD = 66389549`)

| mutant | mutation | verdict | what killed it |
|---|---|---|---|
| M1 | `DROPPED_CLAUSES ("carrier_fresh_ok",)` → `()` | **survived — equivalent mutant** | nothing; zero behavioural leaves against the real after-arm receipts (identical 24-entry `failing`, identical per-carrier clauses, identical `matched`). `carrier_fresh_ok` is true 4/4: the engine's `prior_pins()` at the freeze yields 18 pins and none of the four carriers is among them |
| M2 | rule `required.char-device` false→true | **killed** | control field + exit code: exit 0→1, `control_ok` true→false, `gaps_ok_round67` 4→0 |
| M3 | `control_ok` conjunction → `ok = True` | **killed on the red fixture** | control field + exit code: the honest control on the red rule exits 1 / `control_ok` false; the mutant exits 0 / `control_ok` true while `gaps_ok_round67` is 0. Invisible on the green control, as a forced-true flag must be |
| M4 | `PROV_BASE` `kaidoku-r67/` → `kaidoku-r50/` | **killed** | receipt field `run_provenance_ok` true ×4 → false ×4 on the committed round-67 receipts — the clause takes no data, so a carrier cache cannot rescue it. (Exit code is unchanged only because my run has no cache; the clause delta is measured) |

Baselines: shipped `--control` green (`exit 0`, `control_ok` true, `gaps_ok_round67 4`,
`gaps_ok_round50 2`); shipped `--score` at `66389549` / freeze `3663e6b2`, no carrier cache, exits 1
with exactly 24 failing clauses — the six cache-dependent ones (`carrier_present`, `carrier_pin_ok`,
`carve_ok`, `layout_ok`, `oracle_rederived_ok`, `projection_ok`) × 4, and nothing else. So on the
real receipts the class rule gives `gaps_ok` 4/4, `run_provenance_ok` 4/4, `evidence_id_ok` 4/4,
`receipt_fresh` 4/4, `subject_pin_ok` 4/4, `parameters_ok` 4/4.

## What the L1 should act on

**1. The documentation bindings are the other half of R67-C1.** At `66389549` six of the nine
bindings are false — `province_core_section`, `province_core_row`, `frontier_note`, `entry_present`,
`sourced`, `coverage_map_row` — so `met_target` cannot hold even once the carrier cache is supplied.
The carrier side of the score is otherwise clean (see baselines).

**2. One of the six declared patches is a no-op and its stated reason is false** (M1). The docstring
justifies dropping `carrier_fresh_ok` with "freshness cannot hold by construction"; measured against
the pinned prior tables it holds 4/4, so the drop moves nothing in either direction. Same conclusion
as `w1/CriticClaims.md` §2 by a different route.

**3. The v2 rule is not "`allowed`/`removed`/`structural` unchanged from round-50"** as the counter
docstring (item 1) and the wave description state: `removed.silent.char-device = ["247:0"]` is gone
(`baseline/rule-delta-vs-r50.diff`; the only other delta is `required.char-device`). Inert while a
char device is not required; load-bearing when it is — M2's red rule lands at 0 of 4, not round 50's
2 of 4, because the Cable carriers' silent `247:0` is no longer admitted.

**4. The REA lock drift was real, and the fix widens the patched surface.** The dispatched REA pin
(`tools/round-42/rea-pkg.json`, lock `d42d56f0…`) is no longer reproducible: the local npx
`rea-agents` 6.5.0 keeps `package.json` `a5003023…` but the lock is `815c18f1…`, and no
`package-lock.json` with the frozen digest exists under `/home/vgpnk` or `/fast/scratch` (find at
depth 8, every file hashed). Recorded at 21:59 as exit 2
(`baseline/score-shipped-unevaluable.json`); the lane re-pinned at `ecc4de0e` (atom A11), and the
score runs again. Two residues for the clause/claim review: (i) `patch_engine` now also patches
`mod.rea_package_problems`, so the engine's frozen `rea-pkg` document is no longer consulted — REA
identity rests on a wrapper constant; (ii) atom **A4** still says the patched names are *exactly*
`GAPRULE, AFTERDIR, ENTRY, STEM, CORE_HEADING, FRONTIER_MARK, OPENED_DATES, PROV_BASE, PROV_SEGMENT,
WORK_OVERRIDE, CLAUSES`, and the docstring still says "exactly six things" / "The six disclosed
patches" — there are now seven engine bindings patched (`patches.rea_pkg` discloses it in the
receipt, but A4 and the docstring are false as written).

**5. The instrument moved twice under the wave**: `f78ed365…` (dispatch) → `55decb51…`
(`1e7fe7b7`, worktree restored 21:57:31) → `e44cacf5…` (`ecc4de0e`/`66389549`). Any hash or receipt
taken in an earlier window names the earlier bytes. Confirmed on the dispatched bytes: exit 2
`gap-rule.json absent at freeze` even at `--rev == --freeze`
(`baseline/score-superseded-pin-f78ed365.json`), exactly the failure A10 describes.

**6. A fourth, uncommitted instrument state was being written as this seat closed.** Between
22:03:53 and 22:04:15 `tools/round-67/avm-le-counter.py` and `tools/round-67/gap-rule-v2.json` were
modified in the worktree by another actor and left uncommitted: the counter reached `107211b5…`
then `aa73e0da…` while last read, the rule reached `b55d5e87…`, and the file still carried the
placeholder `RULE_V2_PIN = "RULE2PIN"`. The direction is the one my findings point at — the
docstring now says "five things", keeps `carrier_fresh_ok`, keeps the round-50 `removed.silent` row
and binds the control receipt — but those bytes are not committed, not stable, and not the
instrument these four mutants were measured against. Re-hash before scoring; if that state lands,
M1 no longer has a `DROPPED_CLAUSES` to empty and becomes inapplicable (F1's correct remedy).

## Limits of this seat

- No cache-backed `--score` was run: that performs the REA re-extraction and the unsquashfs oracle
  re-derivation for four carriers, which is the L1's data procedure. My score runs read the four
  committed receipts and leave the six cache-dependent clauses failing on both sides of every A/B,
  so the deltas isolate the mutation.
- M1's inertness is proven at the clause-value level and by an executed A/B against the real
  receipts; the inverse mutant (a synthetic *false* `carrier_fresh_ok`) was not created — it would
  require mutating the pinned engine, outside this seat's bounds. Its detectability follows from the
  engine's `failing_lists()`, which names any `CLAUSES` entry that is not `True`.
- M2 and M3 are scored on the control path only; the control path is unchanged across the three
  instrument states, so those verdicts are lineage-independent.

## Evidence map

- `MutCounter/mutants.md` — the four mutants, diffs, shas, commands, per-field deltas, instrument
  lineage table
- `MutCounter/M1/` — `mutation.diff`, `counter.py`, `receipt.json` (real receipts),
  `lineage-b-receipt.json`, `prior.py`/`prior.out` (the fresh-pin measurement), `run.txt`
- `MutCounter/M2/` — `rule-mutation.diff`, `rule-red.json`, `driver.py`, `m2_green.json`, `m2_red.json`
- `MutCounter/M3/` — `mutation.diff`, `base-counter.py`, `counter.py`, four red/green receipts
- `MutCounter/M4/` — `mutation.diff`, `counter.py`, `receipt.json`, `lineage-b-receipt.json`,
  `provenance-probe.py`/`.txt`
- `MutCounter/baseline/` — pristine control, real-receipt score baseline, the two exit-2 records,
  the rule delta against round 50
- `MutCounter/fixtures/` — the B-lineage fixture diff and its baseline receipt
- `MutCounter/mutant-shas.txt` — every mutant, driver and fixture digest
