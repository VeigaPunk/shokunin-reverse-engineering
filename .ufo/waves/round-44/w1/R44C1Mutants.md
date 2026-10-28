# R44C1Mutants — mutate-and-run probe of the C1 dev-arm (`c1-counter.py --selftest`)

Seat `R44C1Mutants` (wave 1, attack-of-the-draft). Claim under test: R44-C1 in
`plans/round-44-claims.md` (draft; pre-freeze). Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; counter under test
`tools/round-44/c1-counter.py` sha256
`9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993`
(identical bytes at `.ufo/waves/round-44/w1/artifacts/R44C1Counter/c1-counter.py`,
per R44C1Counter's note and re-hashed here before and after the probe).

## Verdict

**Every mutation was flagged red (exit 1). ZERO mutants scored GREEN — no
counter hole found.** 68 injected cases across 17 mutation shapes × 4 carriers
(v1le, v1be, v2le, v2be), each scored red on at least one predicate clause;
the green baseline still matched 4/4. The stock selftest (47 cases) is also
all-pass at exit 0.

Cross-reference (R44C1Counter's recorded state): counter report
`.ufo/waves/round-44/w1/R44C1Counter.md` sha256
`f2a8ccfd29225501f13c81bbf156d8d621f7a95d6443d02c15b699a35a9f4150`, receipts
`artifacts/R44C1Counter/receipts.json` sha256
`3257dbcdc128056840e775d5ec7726d4e15c3347546a44e363f661acc5bbda75`.

## Method

`--selftest` builds synthetic v1/v2 carriers + REA receipt envelopes in per-case
git fixture lanes and calls `measure()`. My probe splices additional
`add('R44MUT/…')` cases into a scratch copy of the counter (never the in-tree
file, never a sibling artifact): cases reuse the counter's own selftest
closures (`mutant()`, `build()`, `frozen_files()`, `spec_data`, `carriers`,
`handlers`, `nonreg`, `frozen`, `good`) so each mutation rides the counter's own
green fixture set and the counter itself decides the verdict. The spliced copy
restricts the loop to the green baseline plus `R44MUT/*`.

Injector: `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Mutants/inject44.py`.
Spliced copy: `probe-R44C1Mutants/r44/tools/round-44/c1-counter.py`
(sha256 `c36ec6ff…`); `tools/round-27/xpin-attribute.mjs` copied beside it so
`find_xpin()` resolves inside scratch. `want_fail` uses the port's
`<carrier>:<clause>` form.

## Runs and receipts

| run | command | exit | wall | stdout sha256 |
|---|---|---|---|---|
| stock selftest (pristine lane counter, 47 cases) | `cd LANE && C1_SELFTEST_DETAIL=1 python3 -I -B tools/round-44/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work $SCR/work-stock` | 0 | 17.9 s | `fbe23fef…da1c` (`stock-selftest.json`: cases 47, green 1, red 46, failures []) |
| mutant selftest (spliced copy, 69 cases) | `cd $SCR/r44 && HYAKU_SCRATCH=/fast/scratch/hyaku C1_SELFTEST_DETAIL=1 python3 -I -B tools/round-44/c1-counter.py --selftest --pkg65 <same> --work $SCR/work-mut2` | 0 | 27.7 s | `3268681e…2369` see `mut-selftest.json` (cases 69, green 1, red 68, failures []) |

Per-case DETAIL capture (exit, failing clause names, drift):
`probe-R44C1Mutants/stock-detail.log`, `probe-R44C1Mutants/mut-detail.log`.

## Verdict matrix (failing clauses per case; all exit 1, carriers_matched 3)

| mutation | all 4 carriers | clauses that fired |
|---|---|---|
| M1a cross-family handler on `chunks[]` only (v2↔v1) | red | `handler_ok`, `projection_ok` |
| M1b `squashfs_v3` on every non-null handler field | red | `handler_ok` + `gaps_ok`, `nonregular_unpublished_ok`, `oracle_hits_ok`, `projection_ok` |
| M1c prefix-hazard handler (`squashfs_v2_nonstandard` on v2, `squashfs_v4` on v1) | red | `handler_ok` + same downstream set |
| M2a carrier bytes truncated to 24 B (< 32 B superblock) | red | `layout_ok`, `carve_ok`, `subject_pin_ok`, `projection_ok` |
| M2b carrier bytes truncated to 31 B (cuts `s_minor` u16@30) | red | same as M2a |
| M3 symlink nonregular row; gap+unpub replaced by fabricated file claim | red | `gaps_ok`, `nonregular_unpublished_ok`, `oracle_hits_ok`, `projection_ok` |
| M3c proper gap+unpub kept AND file also published (over-publish) | red | `nonregular_unpublished_ok`, `oracle_hits_ok`, `projection_ok` |
| M3b fabricated extra published file | red | `oracle_hits_ok`, `projection_ok` |
| M4a `child_path` = `$output/../escaped_extract` | red | `path_shape_ok`, `oracle_hits_ok`, `projection_ok` |
| M4b `child_path` interior `..` (`firmware.bin_extract/../side_extract`) | red | `path_shape_ok`, `oracle_hits_ok`, `projection_ok` |
| M4c `files[].relative_path` = `firmware.bin_extract/../escaped.txt` | red | `path_shape_ok`, `oracle_hits_ok`, `projection_ok` |
| M4d `output_directory` climbs out with `..` | red | `run_provenance_ok` (only — surgical) |
| M5a frozen oracle member `sha256` flipped (spec_over) | red | `oracle_hits_ok`, `tree_ok` |
| M5b published member `sha256` flipped in receipt | red | `oracle_hits_ok`, `projection_ok` |
| M5d declared `output_tree` digest flipped (members honest) | red | `tree_ok` (only — surgical) |
| M6 `evidence_id` left stale after a receipt edit | red | `evidence_id_ok`, `oracle_hits_ok`, `projection_ok` |
| M7 `subject.digest` names a foreign pin | red | `subject_pin_ok`, `projection_ok` |

Every required ticket shape is covered on all four carriers: wrong handler
(`squashfs_v3` on a v1 carrier — M1b — and cross-family/prefix variants),
truncated superblock (M2a/M2b), symlink-gap → fabricated file (M3, with
gap-kept over-publish M3c and fabricated-extra M3b), `..` in the extract-root
derivation path (M4a/M4b) plus file-path and provenance `..` (M4c/M4d), and an
oracle member flipped sha256 input-side (M5a) plus receipt-side (M5b) and
tree-digest (M5d) variants.

## Notes for the port reviewer

- `run_provenance_ok` (M4d) and `tree_ok` (M5d) fired *surgically* — each was
  the only clause to fail on its case — so neither binding is dead weight.
- `handler_ok` binds per-carrier exact equality: `squashfs_v2_nonstandard` on a
  v2 carrier and `squashfs_v4`/`squashfs_v3` on v1 all fail it (M1a–M1c). Null
  member `derivations` edges were preserved in the mutants, matching the real
  REA envelope shape (R44C1Revenger §2).
- The real frozen carriers have zero non-regular members (`unsquashfs` census +
  S138 trees); M3 synthesises a `{'path','kind':'symlink'}` row through the
  spec's `oracle.nonregular` spelling — the key is `kind`, not `type` (a first
  run with `type` failed `carriers_spec_ok` + `oracle_ok` at spec validation,
  i.e. the counter also refuses malformed frozen rows, which is itself a
  red-shaping point worth noting).
- The frozen table requires exactly `v1le/v1be/v2le/v2be`; v2.1 entries make
  `carriers_spec_ok` false by design (R44C1Counter note). My cases therefore
  exercise the 4 claim carriers.
- Dev-harness validation: the same injection was first proven on the r42
  counter (44 cases, 1 green, 43 red, failures []) — see
  `probe-R44C1Mutants/r42dry/detail.log`.

## Restoration evidence

- In-tree `tools/round-44/c1-counter.py` sha256 before the probe
  `9f2cc140…ea993` = after the probe `9f2cc140…ea993` (re-hashed post-run;
  `lane-counter.sha256.before`). The mutated counter existed only as the
  scratch copy `probe-R44C1Mutants/r44/tools/round-44/c1-counter.py`
  (sha256 `c36ec6fffa178fb293ca5389f8d6191a3bcfaf2c03806275b25ac663b9a55c22`),
  which is disposable per the seat spec and left in place as evidence.
- Fixture lanes were created by the selftest under
  `$SCR/work-stock`/`work-mut2` and removed by the counter itself.
- No writes outside `probe-R44C1Mutants/` and this report file.

## Mutation tool

`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Mutants/inject44.py` — deterministic
splice (text insert before the `for c in cases:` executor; syntax-verified by
`ast.parse` before each run). Re-runnable:
`python3 inject44.py <c1-counter.py> <out.py>` then
`C1_SELFTEST_DETAIL=1 python3 -I -B out.py --selftest --pkg65 <rea-pkg> --work <scratch>`.
