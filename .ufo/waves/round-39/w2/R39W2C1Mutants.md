# R39W2C1Mutants — mutation test of the frozen R39-C1 counter

**Verdict: DEFECTS FOUND.** The R39-C1 landing itself reproduces (pristine counter scores
`met_target: true`, 6/6 carriers at REV `6fdaf4f1` with `--freeze 8fcda41c`, exit 0 — byte-for-byte
the same bindings as the author receipt `.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json`), and
10 of 18 single-logic mutants are killed by `--selftest`. But **7 mutants survive both the selftest
and the REV scoring**, i.e. the 33-case selftest (1 green + 32 red) does not pin seven pieces of
the frozen predicate; a receipt fabricated in those shapes would still be scored `met`. One further
mutant is equivalent (redundant guard), not a coverage gap.

## Method

- Subject: `git show 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b:tools/round-39/c1-counter.py`
  (969 lines). Pristine sha256 `efb4b52658b6ccfaebe68516ce2a80794b38ff041a81f464c073974853577a91`;
  the lane working-tree file at HEAD `e40a25df` has the same sha, and the freeze blob hashes the
  same, so the mutated subject is exactly the frozen counter.
- Fixtures + xpin also extracted from the freeze commit (`tools/round-39/selftest/{dev-after.json,
  dev-oracle.tsv,dev-symlinks.tsv,r38-k2-after.json}`, `tools/round-27/xpin-attribute.mjs`).
- Each mutant = one `edit` on a scratch copy under
  `/fast/scratch/hyaku/kaidoku-r39/R39W2C1Mutants/mut/<name>/tools/round-39/c1-counter.py`
  (mirrored layout with symlinked `selftest/` and `tools/round-27/`), then two detectors:
  1. `C1_SELFTEST_DETAIL=1 python3 -I -B <mutant> --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
  2. `python3 -I -B <mutant> --root <shared clone> --rev 6fdaf4f162aff156fcef0e52998a5469c64fd6f0 --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --pkg65 <same> --json-out <out>`
  with the shared clone made per bounds: `git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"`.
- Baselines first: pristine selftest `{"cases": 33, "green_ok": 1, "red_ok": 32, "failures": []}`
  exit 0 (7.2 s); pristine REV measure exit 0, `met_target: true`, `carriers_matched: 6`,
  `frozen_path_changed: []` (0.22 s). Every mutant run was compared against those.
- No VCS mutation anywhere (clone + fixture repos only); no tool installs (system python3, node
  v24.21.0, git only — nothing added/updated, so no tooling ledger entry beyond this note).

## Matrix (18 mutants)

| # | mutant | target logic | selftest (33 cases) | killer case | REV verdict at 6fdaf4f1 | reading |
|---|--------|--------------|---------------------|-------------|-------------------------|---------|
| 1 | `gaps-set` | `gaps_ok` multiset→set (`sorted(seen) != sorted(in_tree)` → `set(...)`) | **survives** (33/33 pass) | — | met, 6/6 | **SURVIVOR** — duplicate same-kind gaps accepted |
| 2 | `gaps-kind` | `gaps_ok` kind check removed | **survives** (33/33 pass) | — | met, 6/6 | **SURVIVOR** — wrong-kind gap with a real path accepted |
| 3 | `esc-neutral` | `escaping_published` match disabled | killed (32/33) | `escaping symlink published` | met, 6/6 | selftest is the only guard; REV data clean |
| 4 | `oracle-exact` | `oracle_hits` suffix→exact path | killed (green fails) | `green` | **not met, 0/6** | double-killed; real published paths carry the extract-dir prefix |
| 5 | `oracle-nosha` | `oracle_hits` sha256 check dropped | **survives** (33/33 pass) | — | met, 6/6 | **SURVIVOR** — wrong-content publication at an oracle path accepted |
| 6 | `prov-dotdot` | `provenance_ok` `..`-climb check removed | killed (32/33) | `provenance path climbs out … with ..` | met, 6/6 | killed |
| 7 | `prov-seg` | `provenance_ok` `/kaidoku-r39/` segment check removed | killed (32/33) | `strong copy: round-38-provenance …` | met, 6/6 | killed |
| 8 | `prov-isabs` | `provenance_ok` `os.path.isabs` check removed | **survives** (33/33 pass) | — | met, 6/6 | **SURVIVOR** — relative `output_directory` accepted |
| 9 | `fresh-anc` | `receipt_fresh` ancestry check removed | killed (32/33) | `receipt added before freeze` | met, 6/6 | killed |
| 10 | `fresh-frz` | `receipt_fresh` `add != freeze` removed | killed (32/33) | `receipt added at freeze` | met, 6/6 | killed |
| 11 | `subj-anystr` | `subject_pin_ok` pin equality → any-string digest | killed (32/33) | `subject digest mismatch` | met, 6/6 | killed |
| 12 | `chunks-all` | `chunk_failed` `any`→`all` | **survives** (33/33 pass) | — | met, 6/6 | **SURVIVOR** — but equivalent on all current data (see below) |
| 13 | `ev-noprefix` | `evidence_id_ok` `ev_` prefix check removed | survives (33/33 pass) | — | met, 6/6 | **equivalent mutant** — `xpin-attribute.mjs:210` always mints `ev_${digest}`, so `stored == recomputed` already implies the prefix; redundant guard, not a missing test |
| 14 | `ev-noeq` | `evidence_id_ok` stored==recomputed dropped | killed (32/33) | `edited files list breaks evidence id` | met, 6/6 | killed |
| 15 | `symcov-max` | `symlink_coverage` `max_in_tree >= 2` clause removed | killed (32/33) | `no carrier exercises two in-tree symlinks` | met, 6/6 | killed |
| 16 | `xz-ver` | `superblock_compression` `(4,0)` version check removed | **survives** (33/33 pass) | — | met, 6/6 | **SURVIVOR** — non-v4 superblock satisfies `xz_leg` |
| 17 | `sid-bounds` | `SID_RE` boundary lookarounds removed | **survives** (33/33 pass) | — | met, 6/6 | **SURVIVOR** — S-id embedded in a longer token counts |
| 18 | `drift-specpaths` | `frozen_drift` spec-listed carrier/oracle/symlink paths not frozen | killed (30/33) | `carrier bytes changed after freeze`, `oracle changed after freeze` (both want 2 got 1) | met, 6/6 | killed; `carriers.json`/counter/plan cases still exit 2 via `FROZEN_PATHS`, exactly as the diff predicts |

Score: **10 killed, 7 survivors, 1 equivalent.**

## Survivors — the defect each admits (function-level demo, pristine vs mutant)

Demo inputs and outputs are recorded in `artifacts/R39W2C1Mutants/survivor-demos.json`.

1. **`gaps-set`** — two `unpublished-entry` gaps on the *same* in-tree symlink:
   pristine `(False, "2 gaps on 1 in-tree symlinks")`, mutant `(True, …)`. The exact-once multiset
   semantics is untested; the red cases only cover a missing gap and a wrong-kind gap.
2. **`gaps-kind`** — gap `{'kind': 'extractor-failure', 'relative_path': 'usr/share/doc/notice-link'}`
   (a real in-tree path): pristine rejects on kind, mutant accepts. The selftest's wrong-kind case
   uses `relative_path: None`, which the *path-coverage* branch rejects anyway — so the kind check
   is never load-bearing in any fixture.
3. **`oracle-nosha`** — published file at an oracle path with a wrong sha256: pristine `oracle_hits`
   0, mutant 1. No red case publishes right-path/wrong-content.
4. **`prov-isabs`** — `output_directory = 'x/kaidoku-r39/y'` (relative, embeds the segment):
   pristine `False`, mutant `True`. No red case uses a relative path.
5. **`chunks-all`** — 2 chunks, exactly one `extraction_failed`: pristine `chunk_failed` `True`,
   mutant `False`. Caveat: the dev fixture has 1 chunk and **all six real REV receipts have exactly
   1 chunk** (counted from `corpus/evidence/round-39/c1/K*/after.json` at REV), so the mutant is
   behaviorally identical on every current input — a missing test for the future, not a live hole.
6. **`xz-ver`** — BE `sqsh` superblock with major=3 and xz id: pristine `None`, mutant `2`
   (`xz_leg` would bind on a v3 image). All fixtures and all six carriers are v4, so untested.
7. **`sid-bounds`** — entry source line `see RES1121 for context`: pristine extracts no token,
   mutant extracts `S1121` (the `sourced` binding could be satisfied by an id embedded in a word).

Practical reach of 1–5 as *fabrication* channels still requires re-minting `evidence_id` under the
6.5.0 rule (the mutated fields sit inside the hashed `semanticProjection`), i.e. they extend the
already-disclosed CTL-C1-3 limit rather than beating the hash. 6–7 weaken non-vacuity bindings only.

## Missing tests to add (one red selftest case each)

1. duplicate `unpublished-entry` gap on one in-tree symlink (kills `gaps-set`);
2. wrong-kind gap carrying a real in-tree symlink `relative_path` (kills `gaps-kind`);
3. published file at an oracle path with a wrong sha256 (kills `oracle-nosha`);
4. receipt with a relative `output_directory` embedding `/kaidoku-r39/` (kills `prov-isabs`);
5. multi-chunk fixture with exactly one failed chunk (kills `chunks-all`; also removes the
   single-chunk fixture limitation);
6. non-v4 superblock with an xz compression id → `xz_leg` must stay false (kills `xz-ver`);
7. entry `source:` line embedding the S-id inside a longer token, e.g. `RES1121` (kills `sid-bounds`).

## Restoration / hygiene

- Mutants lived only in scratch `$S=/fast/scratch/hyaku/kaidoku-r39/R39W2C1Mutants` (removed at the
  end of this run; per-mutant outputs and hashes copied to the artifacts dir first). The pristine
  scratch copy hashed `efb4b526…` before and after all runs; the lane working-tree counter still
  hashes `efb4b526…` — the frozen counter was never modified.
- Lane `git status --porcelain` shows 7 entries, all pre-existing sibling state in
  `.ufo/waves/round-39/w1/*` plus `w2.ready` — none created or touched by this seat. This seat
  wrote only `.ufo/waves/round-39/w2/R39W2C1Mutants.md` and
  `.ufo/waves/round-39/w2/artifacts/R39W2C1Mutants/**`.
- No `find`/`du` outside my own scratch; no pacman transactions; no installs.

## Artifacts

- `artifacts/R39W2C1Mutants/baseline/` — pristine REV receipt (`baseline-rev.json`), selftest
  stderr with per-case DETAIL, pristine sha256 (scratch copy == freeze blob).
- `artifacts/R39W2C1Mutants/mutants/<name>/` — per mutant: `mutant-sha256.txt`, selftest stdout
  (`*.st.out`), selftest stderr with DETAIL lines (`*.st.err`), REV measure JSON (`*.rev.json`),
  REV stdout (`*.rev.out`).
- `artifacts/R39W2C1Mutants/survivor-demos.json` — the seven function-level demos above.

## Limits

- Mutants are single-logic edits chosen by the seat list; other mutation shapes (e.g. loosening
  `same_rel` itself, or `HANDLER_RE`) were not generated.
- The REV arm of every run scores committed bytes at one revision; it cannot distinguish a mutant
  that only diverges on inputs absent from the frozen data — that is exactly what the survivor
  column measures.
- [INFERENCE] The `ev-noprefix` equivalence rests on reading `xpin-attribute.mjs:210`
  (`return \`ev_${digest}\``) plus every observed mint in this run starting with `ev_`; I did not
  prove the 6.5.0 digest can never produce an empty/odd-prefixed value.
