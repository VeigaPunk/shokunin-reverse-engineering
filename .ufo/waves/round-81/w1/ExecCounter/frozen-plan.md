# Round 81 — frozen claims

Base: `5b59ae615a2ab68e3b421820d1c72751e1185385`. Lowest-axis: calibration, tied with coverage, depth and freshness at 10.0. No stagnation waiver: recent capabilities remain within the window. Two claims, distinct axes. No domain mastery inferred.

## R81-C1 — calibration: seven malformed registry rows close

Predicate: the FROZEN `tools/round-71/registry-census.py` at the base, run against the measured commit, exits 0 with `rows >= 129`, `nonconformant []`, `duplicates []`, `multicell_rows 4`, and exactly the four round-69 legacy rows. The seven nonconformant rows at base become seven-cell rows; no population deletion or broadened grammar counts. The frozen instrument's selftest remains green. Repair field meanings, not just delimiter count. Sources opened this round ground escaped-pipe semantics.

Before: 129 rows, seven nonconformant (six `cells>7`, one `pinned-empty`), four legitimate legacy rows plus six extra multicell rows. Receipt `.ufo/waves/round-81/pre/c1-base.json`, exit 1. Do-nothing control: the same seven findings; target unreachable without changes. Counter immutable at `tools/round-71/registry-census.py`; changing it or deleting registry entries kills the claim.

<!-- counting-command: C1 -->
```sh
python3 -I -B tools/round-71/registry-census.py --root . --rev $REV --json-out $OUT
```
<!-- /counting-command -->

## R81-C2 — depth: the record selftest crosses the committed fixture boundary

Predicate: frozen `tools/round-81/record-integration.py` scores a revised `tools/round-81/strictness-battery.py` at the measured commit with `mutants 1`, `killed 1`, `survivors 0`, pristine exit 0 with at least eleven cases and zero failures. Its omission of the sole git-commit call in `make_fixture_repo()` must fail the unique declared case `record-fixture-committed-clean`, exit 1 with a SELFTEST summary. Absent declared case, wrong-case kill, crash or absent summary does not kill. Revised selftest must exercise the REAL round-80 binder battery on clean and duplicate committed PROVINCE fixtures, without reading real client configs. `pointer-bind.py` is supplied beside the measured battery by the counter, byte-identical to committed round-80 binder. Mocking the real binder's battery, parser, git reader, declared-object check or bind is forbidden; redirect only live input paths/read_lines to controlled fixtures.

Before/control: the exact commit-omission mutant survives the round-80 selftest (pristine 9/0 and mutant 9/0; `.ufo/waves/round-81/pre/c2-base.json`, counter exit 1, survivors 1). This skips committed-record work while the old FakeModule reads worktree bytes. Kill rule and detector fixed before candidate data. Preserve existing nine cases and existing battery CLI semantics; do not alter older round instruments. One additional clean and one duplicate integration case is the intended bounded change; unrelated refactors are not claimed.

<!-- counting-command: C2 -->
```sh
python3 -I -B tools/round-81/record-integration.py --root . --rev $REV --work $WORK --json-out $OUT
```
<!-- /counting-command -->

## Separability and standing duties

C1 changes SKILL registry rows and measures them with an unchanged round-71 instrument. C2 changes a new battery copy and scores it with its own frozen counter, never reading SKILL. Either can verify without the other. C1 is calibration of the registry's own claims; C2 is technical depth at the record integration boundary, not new artifact coverage.

Carry-in repairs: r80 outside spot-check D1 search-log correction append-only; D2 three selftest tallies corrected from measured committed tools; D3/D4 append-only report errata in this round's record/report; D5 fleet helper uses fresh author/committer timestamps; D6 freshness row revision aligned; D7 stale seat selftest marked superseded, not rewritten. Open sources, census before/after, lesson, knowledge entry and indexes; source reuse logged old→new; no duplicate URL row. `Assimilation: none` unless a scoped theme is actually adopted. Report only after WAVE-DONE. Future plan-command generalization and receipt-auth/gate-exits limits stay explicit debt, not a third claim.
