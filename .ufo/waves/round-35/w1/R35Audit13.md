# R35Audit13 — mutation evidence & first falsifications (round 35, wave 1)

Seat: `R35Audit13` (executor, leaf). Item: *Mutate malformed row in /tmp. Read-only or
private /tmp only; no lane writes.* Frozen claims: C1 (coverage, `.jsc -> source mapping` via
S125/S129) and C2 (calibration, closes round-34 D-1..D-4). Counters:
`tools/round-35/c1-coverage-counter.py`, `tools/round-35/c2-calibration-counter.py`.

## Method

- Counter bytes verified frozen: sha256 of worktree counters equal the canonical pins
  `e28792c7…` / `576c14dd…` (claims-canonical.json instruments).
- Freeze rev used at runtime: `2323d197456f1328459d9420aff025cffbcb3e27` — the first commit
  that adds `.ufo/waves/round-35/claims-canonical.json` (bytes identical at tip `3ecf4298`).
  Base rev `aa04633a686d49756763b1feed4be6830d5bb479`.
- Harness: private scratch only, `/tmp/r35audit13/` (clone of lane `lane-clone`, per-case
  repos under `mt/`). No lane/vcs mutation, no background jobs, no `find`/`du` under
  `/fast/scratch`, no installs. Each mutation = one clone at green scaffold tip + one commit;
  counter run with `--root <scratch> --freeze 2323d197 --rev <mutant> [--base aa04633]`.
- Green scaffolds (synthetic data authoring for harness only, not lane data) built at base+1
  commit (C1) and base+2 commits (C2: census commit then data commit incl. post-base SOURCES
  change). Both green tips score exit 0.
- Note: in this shell, `str.replace` intermittently no-ops on these large tracked files;
  mutations therefore use index-based find+slice replacement and are applied in a child
  subprocess (payload via stdin) to keep results deterministic. All mutated rows were verified
  committed (`git status` dirty) before scoring.

## Do-nothing controls (measured, base `aa04633`)

| Counter | exit | First failures |
|---|---|---|
| C1 | 1 | entry_missing ×2; registry_row_missing S125/S129; province_missing ×2; readme_missing ×2 |
| C2 | 1 | D1_census_start_missing; D2_lesson_missing; D3_source/verified_at/recheck_missing, D3_source_not_s106; D4_not_eight_cells(round-32 line1081 cells=4); D4_section_missing(round-34 heading) |

Both do-nothing controls fail as required, so the red-at-base requirement holds on real lane
objects today.

## Green baselines

| Scaffold | rev (scratch) | Counter exit |
|---|---|---|
| C1 (entries S125/S129, SOURCES rows, PROVINCE, README map) | `874880c4b9a8` | 0 |
| C2 (census + lesson + w1/w2 settles + r34b trio + SKILL 8-cell tables) | `aa892d1b9e66` | 0 |

## C1 mutation matrix (13/13 falsified; all exit 1)

| Mutation | First failing check(s) |
|---|---|
| m1 entry deleted | entry_missing:…mapper-contract.md |
| m2 trio `source:` removed | trio_missing_source (+ row_citation_missing) |
| m3 trio `verified-at:` removed | trio_missing_verified_at |
| m4 trio `recheck:` removed | trio_missing_recheck |
| m5 entry cites S129 instead of S125 | row_citation_missing:S125 |
| m6 SOURCES row S125 deleted | registry_row_missing:S125 |
| m7 S125 status `mined`→`held` | registry_status_not_mined:S125=held |
| m8 S129 opened 2026-10-25→24 | registry_opened_not_this_round:S129=2026-10-24 |
| m9 S125 used-by points elsewhere | registry_usedby_missing:S125 |
| m10 PROVINCE stem removed | province_missing:…release-inventory |
| m11 README filename loses `.md` | readme_missing |
| m12 SOURCES row with a cell removed (fewer pipes) | registry_row_missing:S129 (regex no match) |
| m13 SOURCES row split into extra pipes | registry_usedby_missing:S125 (column shift) |

## C2 mutation matrix (18/18 falsified; all exit 1)

| Mutation | First failing check(s) |
|---|---|
| D-1 census file deleted | D1_census_start_missing |
| D-1 census content rows=106→105 | D1_census_content_missing (+ after-first-change) |
| D-1 census commit after first SOURCES change | D1_census_after_first_sources_change |
| D-1 control at census commit (no post-base SOURCES change) | D1_no_sources_change_after_base |
| D-2 lesson deleted | D2_lesson_missing |
| D-2 correction token removed | D2_r34w2_correction_missing |
| D-2 seat line removed | D2_lesson_seat_line_missing |
| D-2 seat numbers ≠ settles | D2_lesson_seat_mismatch |
| D-2 w2 settle unparseable | D2_settle_unparseable |
| D-2 w2 settle missing `dead` | D2_settle_missing_field |
| D-2 w1 settle non-dict | D2_settle_shape |
| D-3 r34b entry deleted | D3_entry_missing |
| D-3 `source:` removed | D3_source_missing (+ not_s106) |
| D-3 `verified-at:` removed | D3_verified_at_missing |
| D-3 `recheck:` removed | D3_recheck_missing |
| D-3 cites S105 | D3_source_not_s106 |
| D-4 round-34 heading renamed | D4_section_missing |
| D-4 5-cell row | D4_not_eight_cells cells=5 |
| D-4 9-cell row | D4_not_eight_cells cells=9 |

## Findings / risks for main agent

1. **Both claims are falsified at the do-nothing base today** (C1: all entry/registry/
   province/readme checks missing; C2: all four D's failing). Real data commits are required
   for any pass.
2. **`instrument_revision` field mismatch**: claims-canonical.json lists
   `d2729cba…` as instrument revision, but that commit does **not** contain
   `.ufo/waves/round-35/claims-canonical.json` (it exists only from `2323d197`).
   Passing `--freeze d2729cba…` makes both counters exit 2 (`claims file absent at freeze
   revision`). Score with `--freeze 2323d197…` (or tip).
3. **D-4 substrate reality**: current SKILL.md round-34 heading is
   `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)` —
   the frozen counter looks for the exact string `### Round-34 run-6 instrument registry`, so
   the real section is never scanned (`D4_section_missing`), and existing round-32 rows are
   only 4–5 cells. D-4 additionally requires the round-34 heading to be re-rendered exactly
   (8-cell rows incl. header/separator) to pass.
4. C1 requires rows S125/S129 with `status=mined`, `opened=2026-10-25`, `used-by` naming the
   entry path, PROVINCE stems, and README coverage-map filenames with `.md` — verified as the
   exact tokens the counter matches.
5. D-1 census content must contain `rows=106`, `EXIT=0`, `W04` and be committed before the
   first post-base SOURCES change; the current real tip has no post-base SOURCES change yet
   (`D1_no_sources_change_after_base` would fire at score time).
6. D-2 lesson must contain `31/32`, `AAdjacencyCite`, and a
   `Seat accounting (round 35): spawned=<N> settled=<M> dead=<K>` line that equals the SUM of
   w1+w2 settle JSON fields; w1/w2 settle files do not exist at tip yet.
7. D-3: base r34b entry has no provenance trio; an appended trio citing S106 is required.

## Constraints honored

No lane production writes (reports aside), no VCS mutation, source trees read-only, no nested
delegation, no background jobs, no package installs. All scratch evidence lives in
`/tmp/r35audit13/` (results.json captures every run: rev, exit, failing list, full output).
