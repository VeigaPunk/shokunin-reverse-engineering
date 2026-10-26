# R39W2C2Rescore — re-score R39-C2 with the frozen counter, at 6fdaf4f1 and 52b0eb29

**Verdict: CONFIRMED.** R39-C2 `met_target` reproduces at `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` (20/20, every
binding true, exit 0) and at the later `52b0eb2907c704ed5f184c47b14c723208e5cbbc` (20/20, exit 0); at the freeze
`8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` the same counter exits 2 `no_manifest_at_rev`. No frozen path is touched
anywhere in `8fcda41c..52b0eb29` (nor to lane HEAD), the triage table block is byte-identical at both revs, the held-out
set regenerates byte-identically (carriers *and* manifest) from the freeze archive with no `--run`, and three independent
tamper mutants each drive the frozen counter to exit 1. Nothing landed to falsify; the residual items below are
caveats, not defects against the frozen predicate.

Seat bounds honoured: read-only on the lane (no `corpus/`, `tools/`, `plans/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`,
`LOG.md` writes), no VCS mutation in the lane or fleet, no REA run, no tool install (nothing needed). Scratch
`/fast/scratch/hyaku/kaidoku-r39/R39W2C2Rescore` removed at exit; every cited receipt is copied to
`.ufo/waves/round-39/w2/artifacts/R39W2C2Rescore/`.

---

## 1. Re-score with the frozen counter (shared clone)

Setup:

```
S=/fast/scratch/hyaku/kaidoku-r39/R39W2C2Rescore; mkdir -p "$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"      # clone HEAD = e40a25df
export HYAKU_SCRATCH=/fast/scratch/hyaku
python3 -I -B tools/round-39/c2-counter.py --root "$S/clone" --rev <REV> \
        --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --json-out "$S/out-<REV>.json"
```

| REV | stdout | exit | receipt |
|---|---|---|---|
| `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` | `{"bindings_false": [], "matched": 20, "met_target": true, "met_target_consistent": true, "n": 20, ...}` | **0** | `out-6fdaf4f1.json` (sha256 `dae5731ab4134c507460312c4281be46443372c3f838d5e9bd77264fca535fc0`) |
| `52b0eb2907c704ed5f184c47b14c723208e5cbbc` | same, `matched: 20`, `met_target: true` | **0** | `out-52b0eb29.json` (sha256 `833898160a30199a44eb79c200d8091d677d8a5ad8dc7e2f79a45767832c6c09`) |
| `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` (freeze) | `{"freeze": "8fcda41c...", "frozen_paths_changed": [], "revision": "8fcda41c...", "unevaluable": "no_manifest_at_rev"}` | **2** | `out-8fcda41c.json` |

The two measured receipts are equal to each other and to the L1 score
`.ufo/waves/round-39/l1/scores/c2-at-6fdaf4f1.json` after dropping only `argv`, `revision`, `revision_arg`
(`equal_modulo_rev_and_argv True`); the freeze receipt carries the expected `unevaluable` and an empty
`frozen_paths_changed`.

Same counter against the **real lane** (not the clone), read-only, receipt to scratch:

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-39/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 52b0eb2907c704ed5f184c47b14c723208e5cbbc --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b \
  --json-out "$S/lane-52b0eb29.json"                                        # exit 0
```
→ stdout `matched 20, met_target true`; `lane-52b0eb29.json` equals the clone receipt modulo the same three fields
(`lane_vs_clone_equal True`). So the clone is not the source of the result.

All 20 per-carrier rows report `commit_ok`, `regen_ok`, `digest_ok`, `operation_ok`, `class_match` = true, with
`manifest_sha256 == committed_sha256 == regenerated_sha256` for every id, `manifest_first_add = 3c07eed7da595b815ce3064dcb12bd5c0788e564`,
`envelope_first_add = 3c07eed7...` for all 20, `envelope_inferred: true` (the manifest's carriers carry `carrier`, not
`envelope`; the counter accepts the frozen generator's sibling `envelope.json`, a documented fallback in the tool).

## 2. Selftests

```
cd "$S/clone"
python3 -I -B tools/round-39/c2-counter.py  --selftest   → "SELFTEST cases=27 pass=27 fail=0", exit 0
python3 -I -B tools/round-39/sqfs-triage.py --selftest   → 35 × "ok ...", "SELFTEST cases=35 pass=35 fail=0", exit 0
```
Captured verbatim in `artifacts/R39W2C2Rescore/c2-counter-selftest.txt` and `sqfs-triage-selftest.txt`. Both files run
here are byte-identical to the freeze copies (§3), so the counts cover the frozen instruments.

## 3. Frozen-path integrity, both revs and to lane HEAD

Blob hashes of `git show <rev>:<path>` (first 16 hex of sha256):

| path | 8fcda41c (freeze) | 6fdaf4f1 | 52b0eb29 | e40a25df (HEAD) |
|---|---|---|---|---|
| `tools/round-39/c2-counter.py` | `775766d86de0f1ad` | same | same | same |
| `tools/round-39/sqfs-triage.py` | `ef4a8a8b7428cf72` | same | same | same |
| `tools/round-39/heldout-gen.py` | `8b3eddf8225cfb10` | same | same | same |
| `plans/round-39-claims.md` | `b806f0a7743fe492` | same | same | same |

```
git log --format='%H %s' --no-renames 8fcda41c..52b0eb29 -- \
  tools/round-39/sqfs-triage.py tools/round-39/heldout-gen.py tools/round-39/c2-counter.py plans/round-39-claims.md
→ (empty)
git log --format='%H %s' --no-renames 8fcda41c..e40a25df3987d881513de581112d2dad30605673 -- <same four paths>
→ (empty)
```
The only commits in the measured range are `72359309`, `3c07eed7`, `6fdaf4f1`, `52b0eb29`; ancestry verified
`freeze < 72359309 < 6fdaf4f1 < 52b0eb29` (`git merge-base --is-ancestor`, all exit 0). `plans/round-39-claims.md`
freezes C2's frozen set as exactly these three tools plus itself plus the SKILL table block (`claims:22-24`), and the
counter's `FROZEN` tuple matches it.

## 4. Triage table block byte-identity

Extracted with the counter's own `table_block()` (imported from the frozen module), not a re-implementation:

```
freeze_block_sha256 21759e9f33e05d5b305a5a2ccc37e69f0f19fc9c8b5a2bb7f89bdb4887781bda
later_block_sha256  21759e9f33e05d5b305a5a2ccc37e69f0f19fc9c8b5a2bb7f89bdb4887781bda
byte_identical True   len 3086 == 3086   header_ok True True   marker_present True   rows 10 (header + separator + 8 labels)
```
(`tbl.out` holds the extracted block verbatim.) Whole-file `SKILL.md` sha256 does change
(`29372524a963f5d0…` → `f31ebd633e9fff33…`), and `git diff --unified=0 8fcda41c 52b0eb29 -- SKILL.md` shows exactly
**one** hunk, `@@ -1326,0 +1327,28 @@` — a 28-line append to the instrument registry, ~1000 lines below the table. The
table, and only the table, is the frozen surface.

Two structural facts on the table's home: at the freeze `SKILL.md` has one `## Queue-drain craft` section and one real
marker line (`:333`); the triage bullet (`:316`) is preceded by exactly 17 `- **` blocks in that section, so it is
**rule block 18** as the claim states. At `52b0eb29` the string `<!-- sqfs-triage-table v1 -->` occurs a second time
at `:1351`, inside an instrument-registry row that *describes* the marker (backticked, outside the craft section, which
ends at `## Config custody` `:348`); the counter and interpreter both take the first marker after the craft heading, so
the duplicate has no scoring effect (see §8, caveat 5).

## 5. Independent regeneration from the freeze archive

```
cd "$S/clone" && git archive 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b | tar -x -C "$S/ga"
cd "$S/ga"    && python3 -I -B tools/round-39/heldout-gen.py \
                  --seed 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --out "$S/regen"      # exit 0, no --run
```
Result: `H01..H20` + `manifest.json`, exactly the ids/classes/arms/labels the committed manifest declares. Comparison
(`cmp.out`), for each of `6fdaf4f1`, `52b0eb29`, `e40a25df`:

* `manifest_equal_regen True`; committed manifest sha256 `a1239e556151669f6781eab7fb45c3ccdd487e3775b960507770b2b5992e4f54`
  at all three revs (`git show <rev>:corpus/evidence/round-39/c2/heldout/manifest.json | sha256sum`), and my regenerated
  `manifest.json` hashes to the same `a1239e55…4f54` — the regenerated manifest is byte-identical to the committed blob
  (`regen-manifest.json`, copied).
* `missing []`, `manifest_declared_sha_mismatch []`, `carrier_bytes_vs_manifest_mismatch []`,
  `regen_bytes_vs_committed_mismatch []` — i.e. declared sha256 = committed carrier bytes = my regenerated bytes for
  all 20, and my regenerated bytes equal the committed bytes byte-for-byte.
* Every committed `envelope.json`'s `subject.digest.sha256` equals its carrier (no `ENVELOPE_DIGEST_MISMATCH` printed).

Because regeneration ran with **no `--run`**, labels exist without any REA output at all. That settles the predicate's
"the label its frozen generator assigned *before any REA run*": the labels are a static recipe table in the frozen
generator (`heldout-gen.py` lines 63–106, `recipe['label']` written at line 374), not derived from `run.json`.

## 6. Labels are table-derived: direct interpreter probes

Interpreter = freeze `sqfs-triage.py`, table = `SKILL.md` at `52b0eb29`, envelopes = the 20 committed ones
(`tri/env/H01..H20.json`).

* Baseline, all 20: `clean`×4 (H01–H04), `escaping-symlink-removed`×2, `in-tree-symlink-metadata`×2,
  `dep-missing-be`×2, `dep-missing-le`×2, `avm-marker-be-dropped`×2, `body-extractor-failure`×4 (H15,H16,H19,H20),
  `no-squashfs-chunk`×2. Exit 0; identical to the manifest labels (`labels.txt`).
* **ID-leak probe.** Contents copied under reversed ids (`H01` content → `H20.json`, …, `perm.json`): 20/20 labels
  follow the *content*, `id_leak_failures 0 of 20` (`shuf_labels.txt`). Labels are not keyed on filename.
* **Table-sensitivity probes** (mutants written only under `$S/tri`, never in the repo):
  * `body-extractor-failure` `-be` cell `yes`→`no` → H15, H16, H19 become `unclassified`.
  * `avm-marker-be-dropped` handler `squashfs_v4_be`→`none` → H13 becomes `unclassified`.
  * `clean` row deleted → H01 becomes `unclassified`.
  So the labels are a read of the table bytes, not a hardcoded map.
* Typed refusal seen in passing: passing a non-envelope (`perm.json`) gives exit 2 with
  `sqfs-triage: …: no normalized_result (neither a bare data object nor a full {ok,data,meta} envelope)`.
* Control from the frozen claims ("the triage interpreter on the base `SKILL.md` exits 2 (no table)"):
  `--skill` = `SKILL.md` at base `a2f64e1da78afcf8cc39287106604dbcc270844c` → exit **2**,
  `marker '<!-- sqfs-triage-table v1 -->' absent from the craft section`; the same call on the freeze `SKILL.md`
  labels H01 `clean`, exit 0. The surface was genuinely unmoved before the freeze.

## 7. Falsifiability of the counter itself (three mutants + control)

Scratch copy of the clone (`cp -a "$S/clone" "$S/mut"`, commits confined to that scratch copy — **no commit in the
lane or the fleet**), each mutant one commit on top of `52b0eb29`, counter run exactly as in §1 with `--root "$S/mut"`:

| mutant | change | stdout summary | exit |
|---|---|---|---|
| `e26676c1` | manifest label of H01 `clean`→`dep-missing-be` | `matched 19`, `bindings_false ["carriers_regenerated"]` | **1** |
| `6bf90c5f` | one byte flipped at offset 60000 of `H01/carrier.sqsh` | `matched 20`, `bindings_false ["carriers_committed"]` | **1** |
| `723309c5` | `clean` row `published files` cell `>0`→`0` | `matched 16`, `bindings_false ["triage_table_identical"]` | **1** |
| unmutated `52b0eb29` in the same repo | — | `matched 20`, `bindings_false []` | **0** |

Receipts `mut-e26676c1.json`, `mut-6bf90c5f.json`, `mut-723309c5.json`. The counter is not vacuous: a wrong label, a
changed carrier byte, and a one-cell table edit are each caught, and the table edit also lowers the match count through
the interpreter.

## 8. Caveats and observations (none falsifies P39-C2)

1. **10 generator classes → 8 labels.** `version-minor-mismatch` (H19, H20) carries label `body-extractor-failure`; the
   generator's recipe table documents this explicitly (`heldout-gen.py:104-106`, "the label is 'extractor ran with -be
   and failed', not one recipe"), and the claim's own class→label list states it (`claims:106-109`). Verified against the
   data: H19/H20 `run.json` show handler `squashfs_v4_be`, gap `extractor-failure`, `ExtractCommandFailedReport`, 0
   files, `-be` recorded — the first matching row is `body-extractor-failure`. Consistent, and the 20/20 covers all 8
   table labels; only the *class* granularity exceeds the label set.
2. **`class_match` compares the interpreter label to the manifest `label` (falling back to `class`), not to `class`.**
   Harmless here (all 20 carriers carry an explicit `label`), but a manifest with `label` omitted would be graded
   against the class name. That is the frozen counter's definition, so it is a property of the instrument, not of this
   landing.
3. **"Held out" means seed-derived, not author-unseen** [INFERENCE]: generator, interpreter and table were all authored
   before the freeze, so the epistemic gain is "the carriers cannot be tuned after the freeze hash exists", not
   independence from the author. The predicate as frozen asks for exactly the former, and §5 shows the latter
   contributes nothing (labels exist with no REA run).
4. **Three table `source` cells say `knowledge entry :NN` without the filename** (`:50-54`, `:29-40`, `:11-19`). They
   resolve: the paragraph 15 lines above names `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` five times with
   overlapping ranges, and that entry (60 lines, first added in the freeze commit `8fcda41c`) does contain the cited
   material at those lines — its stanzas start at `:11` Features (`:11-19`), `:20` dependency misses (`:20-28`), `:29`
   AVM-vs-damage (`:29-40`), `:41` symlinks (`:41-49`), `:50` no-chunk (`:50-54`), `:55` status — so the three
   `knowledge entry :NN` cells land on the intended stanzas. The rows are
   not self-contained out of context — a crispness nit, not a broken citation. The `S1xx` citations (`S112`, `S118`,
   `S119`, `S120`, `S121`) all resolve in `corpus/**/*.md`.
5. **Duplicate marker string** at `SKILL.md:1351` (`52b0eb29`) inside the instrument-registry prose. The scoring path
   takes the first marker inside the craft section, so it is inert, but any future whole-file "first occurrence" scanner
   would hit the wrong line. Worth a one-word wrap if the registry is edited again.
6. **Arms are real in the data:** `run.json` `home_bin_on_path` is `false` for exactly the four `before`-arm carriers
   (H09–H12) and `true` for the sixteen `after` ones, and `subject_sha256 == manifest sha256` for all 20 (asserted).
7. **The frozen selftest leaks one `gen.*` fixture per case into the shared scratch root.** `c2-counter.py --selftest`
   creates `gdir = mkdtemp(prefix='gen.')` inside `$HYAKU_SCRATCH/kaidoku-r39` and only removes the per-case `c2-case.*`
   tree in its `finally` (lines 700–760), so a 27-case run leaves 27 `gen.*` dirs behind; `measure()` itself cleans its
   own scratch. `/fast/scratch/hyaku/kaidoku-r39/` held 804 entries at 14:32 with fresh `c2-case.*`/`gen.*`/`c2-counter.*`
   dirs from peers running the same selftest concurrently. Not a defect of this landing (the counter is a frozen path;
   changing it would be `frozen_path_changed`), but whoever owns the scratch root should expect churn. I did not sweep
   that shared root — only my own `$S` was removed.

## 9. Limits

* C1 was not re-scored (other seat); nothing here speaks to P39-C1.
* No REA extraction was re-run — the counters read committed envelopes, and the predicate binds envelopes, not live
  behaviour. A fresh `extract-firmware` would test REA 6.5.0, not this claim.
* Mutant commits exist only in `$S/mut`, a scratch copy of the clone that was deleted with `$S`; the lane and the fleet
  saw no write and no VCS mutation (`git -C <lane> status --porcelain` shows only wave-1/2 peer artifacts that were
  already there, none of them mine).
* Exact commands, outputs and exit codes are quoted above; raw receipts are in
  `.ufo/waves/round-39/w2/artifacts/R39W2C2Rescore/` (`out-*.json`, `lane-52b0eb29.json`, `mut-*.json`, `labels.txt`,
  `shuf_labels.txt`, `cmp.out`, `tbl.out`, `regen-manifest.json`, `*-selftest.txt`, `env.txt` = python/git versions).

## Files changed

* `.ufo/waves/round-39/w2/R39W2C2Rescore.md` (this report)
* `.ufo/waves/round-39/w2/artifacts/R39W2C2Rescore/` (15 receipt/artifact files listed in §9)
