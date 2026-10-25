# R35Audit24 — S125/S129 id-collision check (round 35, wave 1)

Seat: `R35Audit24` (executor, advisory; read-only). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Item: *Check S125/S129 id collisions.* No lane production writes; no subagent/background work; no VCS mutation.

## Verdict

**No collision for the claimed rows S125/S129** — both are absent from the registered registry (S001..S106) and appear exactly once in the staged set, so each maps cleanly to its new SOURCES row (S125 = jsc2js README capture, S129 = jsc2js Releases captures).

**One genuine collision in the staged block, adjacent to the claim: `S106`.** The staged-id list starts at S106, which is already the last *registered* row. `assimilation/collisions` (content: `S106`) documents this. Anyone appending staged rows wholesale to `corpus/SOURCES.md` would re-add S106 and duplicate its row ID (census/W04 class). For the claim's own data set this is not triggered — the counter only materializes S125/S129 rows — but the staged range used for row allocation should start at S107, not S106, before any registry edit.

## Evidence

### Sets (commands/output)
`assimilation/reg-ids` — 106 rows, S001..S106 (no duplicates); matches census-start receipt `rows=106`, `duplicate_ids=0`.
`assimilation/staged-ids` — 132 rows, S106..S237 (no duplicates).
Intersection `set(reg) & set(staged)` = **`{'S106'}`**.
`'S125' in reg` = False, `'S129' in reg` = False; `'S125' in staged` = True, `'S129' in staged` = True; S125 ≠ S129.

### Guard proof
`assimilation/id-guard-proof/`: fixture registry (S001 + an indented `  | S002 |` row) with staged set containing S002 ⇒ `collisions` = `S002`; `run-proof.log` states the extraction accepts 0–3 leading spaces and therefore catches indented rows, so the real `collisions` file (S106) is produced by the same functioning guard, not an artifact of formatting.

### Cross-round source
`round-34/r34b/assimilation/staged-ids` carries the same 132-row seed (S106..S237 incl. S125/S129), so the S106 boundary overlap is inherited from round-34 prep, not introduced in round-35 wave 1.

### Row identity / no duplicate source URI
`tools/round-35/c1-coverage-counter.py` `ENTRIES` maps `2026-10-25-r35-jsc2js-mapper-contract.md`→S125 and `2026-10-25-r35-jsc2js-release-inventory.md`→S129 (ROW_RE accepts `S\d{3,}`). Captures sit in `prep/jsc-sources/`: `jsc2js-readme.md` (README, S125) vs `releases-page1.json` + `releases-page7.json` (GitHub Releases API, S129) — distinct URI scopes; grep `jsc2js` in `corpus/SOURCES.md` = 0 matches, so no pre-existing row or URL collides with either.

## Risks / notes
- The C1 after-state requires adding S125/S129 as *new* mined rows. The safe append semantics (given the S106 overlap) are: only IDs not already in `reg-ids` (i.e., from S107 up) may be written; never re-add S106.
- Context (unchanged by this seat): `freeze-status.md` records `INSTRUMENT_REVISED` debt and that C1/C2 were not scored before the final freeze; per the plan this work proceeds as falsification of the frozen targets.

## Limits
- I did not run `c1-coverage-counter.py`/`c2-calibration-counter.py` (instrument gate is the parent's post-integration step); checks above are direct file reads and set computations, read-only.
- No network fetch performed (S125/S129 live re-open is seats R35Audit01/R35Audit02).
