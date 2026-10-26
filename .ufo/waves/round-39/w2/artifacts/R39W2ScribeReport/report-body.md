# Round 39 — drafted report sections (seat R39W2ScribeReport)

Draft only; not filed into the round report by this seat. Every number below is either read from a
committed artifact named beside it or computed by a command listed in `checks.md`. Frozen rule:
`git show 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b:plans/round-39-claims.md`.

## Work performed

Two claims, two axes: **R39-C1** works *coverage* (standard big-endian SquashFS v4, Frontier → Core on
six frozen carriers) and **R39-C2** works *depth* (an executable outcome-triage table in `SKILL.md`
scored on a held-out set whose seed is the freeze hash). Base `a2f64e1d`, freeze `8fcda41c`, controls
`72359309`, C2 data `3c07eed7`, C1 receipts + Core landing `6fdaf4f1`, record/lesson `52b0eb29`,
wave-2 dispatch `e40a25df`.

- **Claims frozen** with the freeze-integrity rule, per-claim predicates, targets, counting commands
  and kill rules: `plans/round-39-claims.md:14` (freeze rule), `:26` (C1 surface), `:34` (P39-C1),
  `:69` (C1 counting command), `:86` (C2 surface), `:97` (P39-C2), `:112` (C2 counting command),
  `:130` (`## Changes from the draft`). Freeze commit `8fcda41c` (1277 files, 98,390 insertions).
- **C1 carriers** (6, with 18 sha256 pins — carrier, oracle, symlink table per carrier):
  `.ufo/waves/round-39/c1/carriers.json`; K1–K4 reuse the round-37 carriers, K5/K6 are round-39
  bodies under `corpus/evidence/round-39/c1/K5/` and `K6/`. I recomputed all 18 pins at `8fcda41c`
  and `6fdaf4f1`: 36/36 match (see `checks.md` C3).
- **Carrier writer fixes** (UTF-8 name length, real xz container, comp id 4): `tools/round-39/gen-squashfs.py`;
  K6 reports `superblock_compression 4` and `xz_leg K6: 4` (`.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json`).
- **Independent SquashFS reader** and cross-checked oracles/symlink tables: `tools/round-39/sqfs-list.py`,
  `corpus/evidence/round-39/c1/K{1..4}/symlinks.tsv`, `K5|K6/{oracle.tsv,symlinks.tsv}`.
- **C1 harness** (`after`/`oracle`, scratch under `/kaidoku-r39/`): `tools/round-39/c1-run.sh`; run
  records `corpus/evidence/round-39/c1/K{1..6}/run.json`.
- **C1 counter** with its self-test (33 cases, registry `SKILL.md:1346`) and the receipt/doc
  bindings: `tools/round-39/c1-counter.py` (`met_target` at `:549`, exit map `:586`).
- **Pre-data controls** landed before any claim data: `72359309`, receipts in
  `.ufo/waves/round-39/controls/` (9 C1 receipts, `ctl-c2-dev-scores.json`, two repaired C2 tables)
  plus the wave-1 suite `.ufo/waves/round-39/w1/artifacts/R39C1Controls/evidence/suite.json` (10 C1
  controls). See findings D1/D2/D3 for what the two control records do and do not agree on.
- **Sources opened before data** S118–S122: `corpus/SOURCES.md:124-128`; opened stamps and located
  quotes in `corpus/lessons/round-39.md` `## Gate` (`:37`).
- **C2 field characterisation** (clean, dep-missing, AVM marker, body damage, truncation, determinism,
  mixed images): `w1/R39C2Recon*.md`, `w1/R39C2LabDeterminism.md`, `w1/R39C2LabMixed.md`.
- **Triage rule block 18 + table** (marker `<!-- sqfs-triage-table v1 -->` at `SKILL.md:333`, header
  `:334`, eight label rows `:336-343`):
  entry `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` (freeze commit `8fcda41c`, `SKILL.md`
  +29 lines).
- **Triage interpreter** (reads only the SKILL table; 35 self-test cases): `tools/round-39/sqfs-triage.py`;
  registry row `SKILL.md:1351`.
- **Held-out generator** (seed = freeze hash, 10 classes × 2) and its data:
  `tools/round-39/heldout-gen.py`, `corpus/evidence/round-39/c2/heldout/manifest.json` (seed
  `8fcda41c…`, generator sha `8b3eddf8…`), 20 × `{carrier.sqsh,envelope.json,rea-full.json,run.json,tree.json}`
  (`3c07eed7`, 101 files, 16,613 insertions).
- **C2 counter** (bindings incl. `triage_table_identical`, `carriers_regenerated`; 27 self-test cases):
  `tools/round-39/c2-counter.py`; registry row `SKILL.md:1353`.
- **C1 after-runs, receipts and Core landing**: `6fdaf4f1` — `corpus/evidence/round-39/c1/K{1..6}/after.json`,
  entry `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`, `PROVINCE.md:378` (Core row) and
  `:384` (round-39 frontier note), `corpus/README.md:93,203,245`, `corpus/SOURCES.md` S122.
- **Lesson, QUALITY, registry, round-38 gate self-tests, routed-defect ledger**: `52b0eb29` —
  `corpus/lessons/round-39.md` (M39-1..8 `:24`, Gate `:37`, corrections `:67`, routed `:85`,
  criteria `:99`), `corpus/QUALITY.md:90` (row 82), `SKILL.md:1328-1354` (22 tool rows,
  `### Round-35/37/38/39 instrument registry`), `--selftest` added to
  `tools/round-38/{freeze-drift.py:49,intended-doc.py:45,registry-immutable.sh:22}`.
- **Absence gate for QUALITY 82**: `tools/round-39/absence-sweep.py`, receipts
  `.ufo/waves/round-39/l1/absence/summary.txt` (fleet root `rc=0`, both roots `rc=1`, selftest `rc=0`).
- **Scores at the measured revision**: `.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json` (6/6),
  `c2-at-6fdaf4f1.json` (20/20), plus before arms `c1-at-base.json` (unevaluable),
  `c2-at-freeze.json` (unevaluable) and `controls/ctl-c1-0-do-nothing.json` (0/6).
- **Wave 1** (pre-freeze build and attack): 43 seats, 43 reports under `.ufo/waves/round-39/w1/`,
  ledger `.ufo/waves/round-39/r39-w1-results.json` (43 results: 20 `DONE`, 14 `DEFECTS FOUND`,
  4 `CONFIRMED`, 5 non-scalar/qualified verdict strings), committed in the freeze per M39-3.
- **Wave 2 dispatch** (this wave): `.ufo/waves/round-39/w2-spec.json` (39 items),
  `w2-dispatch.json` (`spawn 39`), `e40a25df`.

## Landed changes

`git show --stat` totals (names omitted; full lists at the commit):

| commit | role | stat |
|---|---|---|
| `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` | freeze: claims, all round-39 tools, `carriers.json`, K5/K6 bodies + oracles + symlink tables, K1–K4 symlink tables, triage entry, `SKILL.md` +29, `corpus/README.md`, `corpus/SOURCES.md` (S118–S121), census start, 43 wave-1 reports/artifacts, dispatch/spec/gen | 1277 files changed, 98,390 insertions(+) |
| `72359309a052284029f8e0331ef211a67fe4b13b` | pre-data controls: 9 C1 receipts + logs, `ctl-c2-dev-scores.json`, 2 repaired C2 tables, wave-1 results ledger | 22 files changed, 1,430 insertions(+) |
| `3c07eed7da595b815ce3064dcb12bd5c0788e564` | C2 held-out data (seed = freeze): manifest + 20 carriers with envelopes, `rea-full.json`, run and tree records | 101 files changed, 16,613 insertions(+) |
| `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` | C1 after-receipts K1–K6 (+`run.json`), Core row in `PROVINCE.md` (+8), `corpus/README.md` (+3), `corpus/SOURCES.md` (+1), BE-v4 Core entry (+45) | 16 files changed, 841 insertions(+) |
| `52b0eb2907c704ed5f184c47b14c723208e5cbbc` | lesson + QUALITY 82 + SKILL instrument registry + round-38 gate `--selftest` + absence receipts + scores at `6fdaf4f1` + PROVINCE pointer fix | 18 files changed, 1,355 insertions(+), 5 deletions(-) |
| `e40a25df3987d881513de581112d2dad30605673` (context, wave 2) | wave-2 spec, generator, validated dispatch (39 seats, policy v1) | 3 files changed, 1,116 insertions(+) |

Not in these commits, and absent from the lane at `e40a25df`: a round-39 `SCORECARD.md` section and a
round-39 `LOG.md` entry (finding D4).

## Before → after measurements

Counting commands are the frozen ones (`plans/round-39-claims.md:69` and `:112`), run with
`python3 -I -B`, the lane root, the frozen `--freeze`, and (C1) `--pkg65
/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`.

### R39-C1 — coverage (`carriers_matched == 6` and every binding true)

```
python3 -I -B tools/round-39/c1-counter.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 6fdaf4f162aff156fcef0e52998a5469c64fd6f0 \
  --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --json-out <RECEIPT>
```

- **Before** — `.ufo/waves/round-39/controls/ctl-c1-0-do-nothing.json` (rev = freeze = `8fcda41c`,
  clone root under `/fast/scratch/hyaku/kaidoku-r39/l1/ctl/c0`): `carriers_matched 0` of 6,
  `met_target false`, six false bindings (`coverage_map_row`, `entry_present`, `frontier_note`,
  `province_core_row`, `province_core_section`, `sourced`), exit 1 (`tools/round-39/c1-counter.py:586`
  returns `0 if met_target else 1`). The base arm is unevaluable:
  `.ufo/waves/round-39/l1/scores/c1-at-base.json` → `"unevaluable": "carriers.json absent at freeze"`.
- **After** — `.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json`: `carriers_matched 6`,
  `target 6`, `met_target true`, `carriers_unchanged true`, `frozen_path_changed []`,
  `bindings_false []`, exit 0 (`c1-counter.py:586`). Per carrier (oracle/published/in-tree/escaping/comp):
  K1 5/5/0/1/1, K2 3/3/1/0/1, K3 4/4/0/0/1, K4 4/4/0/0/1, K5 10/10/2/1/1, K6 8/8/1/2/4.
  **Measured commit: `6fdaf4f162aff156fcef0e52998a5469c64fd6f0`.**
- Control caveat carried from the freeze: a fabricated receipt with a re-minted evidence id reaches
  6/6 carriers and is refused only by a documentation binding (`controls/ctl-c1-3.json`,
  `counter_exit 1`, `frontier_note false`); the claims disclose this
  (`plans/round-39-claims.md:79` `Disclosed limit`), and provenance therefore rests on wave-2
  independent re-runs, not on this counter.

### R39-C2 — depth (`matched == 20`, N = 20)

```
python3 -I -B tools/round-39/c2-counter.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 6fdaf4f162aff156fcef0e52998a5469c64fd6f0 \
  --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b \
  --json-out <RECEIPT>
```

- **Before** — `.ufo/waves/round-39/l1/scores/c2-at-freeze.json` (rev = freeze): `unevaluable:
  "no_manifest_at_rev"`, no bindings, exit 2 (`tools/round-39/c2-counter.py:425-435` returns 2 after
  `Unevaluable`, raised at `:165`). Base arm: the frozen interpreter on the base `SKILL.md` exits 2,
  `matched 0`, stderr `sqfs-triage: marker '<!-- sqfs-triage-table v1 -->' absent from the craft
  section` (`controls/ctl-c2-dev-scores.json`, `CTL-C2-0-base-SKILL`). Best pre-data shortcut table on
  the 20 development envelopes: **12/20** (`CTL-C2-6-no-be-no-sr.formatfix`); the rest 10/8/6/6/4/0.
- **After** — `.ufo/waves/round-39/l1/scores/c2-at-6fdaf4f1.json`: `matched 20`, `n 20`,
  `bindings_ok true`, `bindings_false []`, `frozen_paths_changed []`, `seed_matches_freeze true`,
  `regenerated_seed_matches_freeze true`, `carriers_regenerated true`,
  `generator_sha_matches_freeze true`, `triage_table_identical true`, exit 0 (`c2-counter.py:443`).
  **Measured commit: `6fdaf4f162aff156fcef0e52998a5469c64fd6f0`.**

## Sources & frontier

**Registry (`corpus/SOURCES.md`)**: 117 → 122 rows, append-only (`git diff --stat` base→HEAD:
1 file, 5 insertions). Rows by column at base → HEAD:

| column | base (117) | HEAD (122) | delta |
|---|---|---|---|
| tier A | 109 | 114 | +5 |
| tier B | 7 | 7 | 0 |
| tier C | 1 | 1 | 0 |
| status `mined` | 112 | 117 | +5 |
| status `rejected` | 5 | 5 | 0 |
| kind `code` | 31 | 36 | +5 |

The five new rows S118–S122 are all tier A, status `mined`, opened 2026-10-26, and used by the two
round-39 entries (`S118`–`S121` → triage entry, `S122` → Core entry); row lines
`corpus/SOURCES.md:124-128`. No pre-existing row changed in any column.

**Start census**: `.ufo/waves/round-39/census-start.txt` — 13 lines (11 `W04` duplicate-url rows,
one `ok` line for `corpus/SOURCES.md`, `exit 0`).

**Frontier movement** (all at `6fdaf4f1` unless stated):

- Core gains one row: `PROVINCE.md:378` `## Round-39 additions to Core`, surface
  `standard big-endian SquashFS v4 recursion (squashfs_v4_be)`, probe = six frozen carriers
  (K1/K2 round-37 BE gzip, K3/K4 unblob 26.6.4 BE fixtures, K5 BE gzip, K6 BE xz comp id 4),
  evidence = entry + `carriers.json` + `K{1..6}` receipts.
- Frontier note `PROVINCE.md:384` supersedes the big-endian part of the round-4 `sasquatch` bullet
  (`PROVINCE.md:156-157`) and the round-38 note; AVM-BE bodies and vendor-mangled images stay
  Frontier. The round-36 pointer defect R36-CL2 is discharged in the same sentence (`52b0eb29`).
- `corpus/README.md`: coverage-map row `:93` (Core), knowledge row `:203`, frontier bullet `:245`.
- Knowledge files 127 (base) → 128 (freeze, triage entry) → 129 (`6fdaf4f1`, Core entry);
  `corpus/README.md` Knowledge-table rows beginning ``| `2026-`` 113 → 115, one per round-39 entry,
  plus one new coverage-map row (`:93`).
- Not restated: `SCORECARD.md:23` still reads `126/126` and `SCORECARD.md` has no round-39 section;
  `LOG.md` has no round-39 entry (finding D4; the lesson states "closure pending" at
  `corpus/lessons/round-39.md:11`).
