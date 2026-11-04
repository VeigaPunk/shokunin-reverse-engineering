# ScoutSurface — insertion-surface map (round 85, wave r85-w1)

Full map: `.ufo/waves/round-85/w1/ScoutSurface/map.md` (189 lines). Receipts:
`.ufo/waves/round-85/w1/ScoutSurface/receipts/`. Lane tree unmodified; no installs.

## Key numbers (all measured at declaration rev 91eeb72f)

- **21/21 frozen mutant rows: anchor count exactly 1** — no defect in `.ufo/waves/round-85/mutants.json`.
- **17 of 21 declared case names exist in no pristine selftest inventory**; only 4 exist
  (`sourced-row-rejected-status` printed-command.py:691, `late-single-header` source-bind.py:95,
  `duplicate` source-bind.py:88, `genuine-synthetic-passes` conjunction-gate.py:311).
- BASE C2 receipt: **killed 3 / 21** (survivors 18) vs target ≥ 16 / 21.
- Frozen r84 (13 rows): **killed 13 / 13**, ok true; re-measured selftest rc = 0 for all three targets
  (printed-command 22 cases, source-bind 8 checks, conjunction-gate 21 cases; 0 failures).
- Census validate → **rc 0**, 27 × W04, last line `kaidoku ok …/corpus/SOURCES.md`; manual census
  **rows 208**, malformed (NF≠13) **0**, tiers A=190 B=10 C=8. S304 will make it 209.

## Insertion points handed to the executors

- `tools/round-82/printed-command.py`: selftest 485 (returns 721); cases via `check` 488–489 or
  `guarded` 614–618; **new `guarded(...)` after 707, before cleanup 709**; fixtures `fixture_repo` 583,
  `run_case` 623, `static_case` 645, `sourced_case` 675, `with_sources` 686.
- `tools/round-83/source-bind.py`: selftest 104 (returns 149); **cases are tuples in `FIXTURES` 81–101** —
  add one named exactly the declared case (counter parses `selftest <name>: ok|FAIL` lines).
- `tools/round-82/conjunction-gate.py`: selftest 303 (returns 432); cases are direct `check(...)`
  306–307; **add after 424, before `failures = sorted` 426**; fixture `synthetic_genuine` 283.
- Counter kill binding: `tools/round-84/mutation-closure.py` 222–228 — a declared case absent from the
  pristine inventory scores `survived`, never a pass.
- Anchors shared with the frozen r84 table (keep r84 counts at 1): `cells[8] == "mined"` (r85 rows 4, 13),
  `cells[9] == "2026-11-04"` (row 14), `if script not in pins:` (row 6), `if len(fields) != 1 or
  fields[0][0] >= 12:` (rows 18, 19), `len(cases) < PRISTINE_FLOOR` (row 21).

## Blockers

None. Note for the executor: rows 4 and 13 both mutate `cells[8] == "mined"` at printed-command.py:273 —
their new cases must be distinguishable; and `tools/round-85/predicate-bind.py` plus the r85 container
`.ufo/waves/round-85/claims.json` do not yet exist at the declaration rev.
