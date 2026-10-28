# R44C1Mutants — mutate-and-run probe of the C1 dev-arm (`c1-counter.py --selftest`)

Seat `R44C1Mutants` (wave 1, attack-of-the-draft). Claim under test: R44-C1 in
`plans/round-44-claims.md` (draft; pre-freeze). Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; lane HEAD observed during the
probe `9a8de923` → later commits (wave-1 seat outputs, pre-freeze).

## Method

The counter's `--selftest` builds synthetic fixture lanes in git repos under the
seat scratch and runs `measure()` over each `(frozen inputs, committed receipts)`
pair, asserting a verdict per case (0 = green/met, 1 = red/failed, 2 =
unevaluable). My probe splices additional `add('R44MUT/…')` cases into a scratch
copy of the counter (never the in-tree file, never a sibling artifact): the
mutant cases reuse the counter's own selftest closures (`mutant()`, `build()`,
`frozen_files()`, `spec_data`, `carriers`, `handlers`, `CARRIERS`) so each
mutation is applied on top of the counter's own green fixture set and the
counter itself decides the verdict. The spliced copy restricts the case loop to
the green baseline plus `R44MUT/*` for speed; the counter's own arms are
exercised by the stock `--selftest` run of the same file.

Injection tool: `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Mutants/inject.py`
(writes the spliced copy + `tools/round-27/xpin-attribute.mjs` needed by
`find_xpin()` into the scratch fixture tree; nothing outside scratch is
touched).

## Mutation classes (per carrier)

| id | mutation | the clause it must trip |
|---|---|---|
| M1a | wrong handler string on `chunks[]` only (e.g. `squashfs_v3` on a v1 carrier) | `handler_ok` |
| M1b | wrong handler consistently on every non-null handler field (`chunks`, root `derivations` edge, `extraction_gaps`) | `handler_ok` (+ downstream) |
| M2  | carrier bytes truncated mid-superblock (input mutation via `blob_over`) | `layout_ok` |
| M3  | a non-regular member's gap replaced by a fabricated regular-file claim ("symlink-as-file") | `gaps_ok` |
| M3a | fallback: fabricated `unpublished-entry` gap swallows a regular oracle member (used when the fixture has no non-regular rows — **the real r44 carriers have none**: 4–7 regular files, zero non-regular, per `artifacts/R44C1Oracle/c1-oracle.json`) | `gaps_ok` |
| M3b | fallback: fabricated extra published file the oracle never names | `oracle_hits_ok`/`extra_published` |
| M4a | `derivations[].child_path` = `$output/../escaped_extract` | extract-root / `path_shape_ok` |
| M4b | `derivations[].child_path` with interior `..` segment | extract-root / `path_shape_ok` |
| M4c | `files[].relative_path` = `firmware.bin_extract/../escaped.txt` | `path_shape_ok` / oracle set |
| M5a | frozen oracle member `sha256` flipped (input mutation; `oracle.tsv` file or embedded `carrier.oracle.members[]` — whichever the frozen spec uses) | `oracle_ok`/`oracle_hits_ok` |
| M5b | published member `sha256` flipped in the committed receipt | `oracle_hits_ok`/`projection_ok` |

## Verdict matrix — tools/round-44/c1-counter.py

PENDING: `tools/round-44/c1-counter.py` (authored by R44C1Counter, artifact
`.ufo/waves/round-44/w1/artifacts/R44C1Counter/c1-counter.py`) was not yet
written when this probe started. Results land here when the draft lands.

## Dev-harness validation (r42 counter, dry run only)

To prove the injection machinery before the r44 port lands, the identical block
was spliced into `git show`-equivalent `tools/round-42/c1-counter.py` at base
(same selftest closures) and run:

- command: `HYAKU_SCRATCH=/fast/scratch/hyaku C1_SELFTEST_DETAIL=1 python3 -I -B
  tools/round-42/c1-counter.py --selftest --pkg65
  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (cwd =
  `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Mutants/r42dry`)
- result: `{"cases": 44, "green_ok": 1, "red_ok": 43, "failures": []}`,
  exit 0 — the green baseline matched all 4 carriers and every one of the 43
  injected mutants was flagged red (per-case failing clauses in
  `probe-R44C1Mutants/r42dry/detail.log`).
- r42 note: its selftest carriers include non-regular rows, so M3 (true
  symlink-as-file) ran there and red'd on `gaps_ok` + `nonregular_unpublished_ok`
  + `oracle_hits_ok` + `projection_ok`.

## Notes for the port reviewer

- M1b in the r44 port must preserve the null-handler member `derivations` edges
  the real REA emits (one per published member, `handler: null` —
  `.ufo/waves/round-44/w1/R44C1Revenger.md` §2); the injection only rewrites
  non-null handler fields, matching the true envelope shape.
- The real frozen carriers have **no non-regular members** (`unsquashfs -lls`
  census: 3 regular files on v1, 4 on v2.0/v2.1, zero symlinks/devices). A
  port whose selftest fixtures mirror the real carriers can only exercise the
  gap-accounting clause through M3a-style fabrications; a port whose selftest
  keeps synthetic symlinks still gets the M3 shape.
