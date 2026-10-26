# R39-C2 depth attack — R39W2C2Shortcut

**Verdict: CONFIRMED** — the landed table scores 20/20 and its discrimination is real but
thin: 20/20 is unreachable without both `-be` and `symlink removed` (16/20 without either,
18/20 without one), while the *smallest* grammar table that also scores 20/20 is 8 rows and
**7** discriminating cells. One documentation defect (D1) and one predicate-shallowness
note (D2) are reported; neither blocks the score.

**No label leakage of any kind.** The frozen interpreter reads exactly the six features and
nothing else; injected `class`/`label` fields and a full envelope-field ablation change
neither a feature nor a label.

## 0. Answers to the assigned questions

| question | answer |
|---|---|
| smallest frozen-grammar table labelling all 20 | **8 rows, 7 non-`*` cells** (`artifacts/MIN-8row-7cell.md`), 20/20 held-out and 16/16 dev — and 8 rows / 7 cells is a proved floor |
| best table with no `-be` cell and no `symlink removed` cell | **16/20** (`artifacts/SHORTCUT-no-be-no-sr.md`), which is the exact ceiling, not a weak attempt |
| label leakage in envelopes? | **none** — 10 class/label tokens, 20 envelopes, 0 hits; injection and ablation tests are bit-neutral |
| interpreter reading beyond the six features? | **no** — five reads, mapped to the six columns in §6 |
| is the landed discrimination real or shallow? | **real, but the depth it buys is 4 envelopes**: `-be` = 2 envelopes, `symlink removed` = 2; 16/20 is reachable with neither |

## 1. Held-out feature matrix (frozen interpreter, exit 0)

`python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json corpus/evidence/round-39/c2/heldout/H*/envelope.json`
→ rc 0, `rules: 8`, 20 results. Features per envelope (identical for the two carriers of a
class; `P` is the grammar's 0 / `>0` bucket):

| id | class | H | G | D | BE | SR | P | landed label (rule) |
|---|---|---|---|---|---|---|---|---|
| H01 H02 | clean-be | {`squashfs_v4_be`} | {} | {} | n/a | no | 7 / 5 | clean (8) |
| H03 H04 | clean-le | {`squashfs_v4_le`} | {} | {} | n/a | no | 5 / 5 | clean (8) |
| H05 H06 | escaping-symlink-removed | {`squashfs_v4_be`} | {} | {} | n/a | **yes** | 3 / 8 | escaping-symlink-removed (6) |
| H07 H08 | in-tree-symlink-metadata | {`squashfs_v4_be`} | {`unpublished-entry`} | {} | n/a | no | 3 / 6 | in-tree-symlink-metadata (7) |
| H09 H10 | dep-missing-be | {`squashfs_v4_be`} | {`missing-extractor-dependency`} | {`sasquatch-v4be`} | n/a | no | 0 / 0 | dep-missing-be (2) |
| H11 H12 | dep-missing-le | {`squashfs_v4_le`} | {`missing-extractor-dependency`} | {`sasquatch`} | n/a | no | 0 / 0 | dep-missing-le (3) |
| H13 H14 | avm-marker-be-dropped | {`squashfs_v4_be`} | {`extractor-failure`} | {} | **no** | no | 0 / 0 | avm-marker-be-dropped (4) |
| H15 H16 | body-extractor-failure | {`squashfs_v4_be`} | {`extractor-failure`} | {} | **yes** | no | 0 / 0 | body-extractor-failure (5) |
| H17 H18 | no-squashfs-chunk | {} | {} | {} | n/a | no | 0 / 0 | no-squashfs-chunk (1) |
| H19 H20 | version-minor-mismatch | {`squashfs_v4_be`} | {`extractor-failure`} | {} | **yes** | no | 0 / 0 | body-extractor-failure (5) |

Nine blocks, 20 envelopes, every block label-homogeneous. Full machine record
`artifacts/results.json` (`matrix[]` carries features, commands, landed rule index, my
tables' labels). Carrier sha256 recomputed from `H*/carrier.sqsh` equals the manifest pin for
all 20 (`carrier sha mismatches: none`).

Two provenance details read from the frozen bytes, not taken on faith: H13/H14 diagnostics
record `sasquatch-v4be -no-exit-code -f -d …` (no `-be`) with stderr
`SquashFS version [1024.0] / inode count […] suggests a SquashFS image of a different endianess`,
while H15/H16 carry `sasquatch-v4be -be -no-exit-code …` with
`read_id_table: failed to read id table block` and H19/H20 with
`FATAL ERROR: Block size too small. File system is corrupt.` The `-be` split is unblob's own
AVM test, not something the generator writes into the envelope.

## 2. Smallest table in the frozen grammar — 8 rows, 7 cells

`artifacts/MIN-8row-7cell.md` — seven one-cell lookups, then one default row:

| # | label | the single discriminating cell |
|---|---|---|
| 1 | no-squashfs-chunk | handler `none` |
| 2 | escaping-symlink-removed | symlink removed `yes` |
| 3 | dep-missing-be | dependencies `sasquatch-v4be` |
| 4 | dep-missing-le | dependencies `sasquatch` |
| 5 | in-tree-symlink-metadata | gap kinds `unpublished-entry` |
| 6 | avm-marker-be-dropped | `-be` `no` |
| 7 | body-extractor-failure | gap kinds `extractor-failure` |
| 8 | clean | all `*` (remainder) |

Scores: **20/20** held-out, **16/16** on the independent wave-1 dev set (seed
`sha256("dev1")`, 8 classes), both via the frozen interpreter, rc 0.

**Floor proof.** (a) 8 distinct labels, one label per row ⇒ ≥ 8 rows. (b) A row whose six
condition cells are all `*` matches every envelope, so any row except the last one in that
form makes all later rows unreachable ⇒ at most one all-`*` row, and it must be last ⇒ the
other 7 rows each carry ≥ 1 non-`*` cell ⇒ ≥ 7 cells. The table above attains 8/7; no
grammar table can be smaller on either count. (`artifacts/MIN-8row.md` is the same table
without the default row: 8 cells, also 20/20; it is the variant to prefer, see D2.)

## 3. Best no-BE / no-SR table — 16/20, and that is the ceiling

`artifacts/SHORTCUT-no-be-no-sr.md`: six rows, both hidden columns `*` on every row.
Score **16/20**; misses are exactly `H05 H06 → clean` and `H13 H14 → body-extractor-failure`
(the two blocks those features were hiding). Dev set: 12/16 (same two classes).

Ceiling proof (block argument, not an argument from my table): a table whose `-be` and
`symlink removed` cells are all `*` computes a function of {H, G, D, P-bucket} only, so two
envelopes with the same projected features must receive the same label. Under that
projection the 20 envelopes form 7 blocks:

| block | envelopes | labels present | best |
|---|---|---|---|
| H01 H02 H05 H06 | 4 | clean ×2, escaping ×2 | 2 |
| H03 H04 | 2 | clean ×2 | 2 |
| H07 H08 | 2 | in-tree ×2 | 2 |
| H09 H10 | 2 | dep-be ×2 | 2 |
| H11 H12 | 2 | dep-le ×2 | 2 |
| H13–H16, H19 H20 | 6 | avm ×2, body ×4 | 4 |
| H17 H18 | 2 | no-squashfs-chunk ×2 | 2 |

Σ = **16**. So no no-BE/no-SR table can reach the target, and 16 is attained.

Dropping only one hidden feature also caps below the target (measured with
`artifacts/VARIANT-no-be-only.md` **18/20** and `VARIANT-no-sr-only.md` **18/20**; block
argument: only one of the two 4-envelope blocks then splits). Each hidden feature is worth
exactly **2 envelopes = 10 points**.

## 4. Which columns are actually load-bearing

Ceilings computed by projecting the 20 envelopes onto facet subsets (`P` bucketed 0 / >0,
handler as exact set — the only partitions the grammar can express):

| dropped facet | ceiling /20 |
|---|---|
| none (all six) | 20 |
| `handler` | **20** |
| `dependencies` | **20** |
| `published files` | **20** |
| `gap kinds` | 18 |
| `-be in child argv` | 18 |
| `symlink removed` | 18 |
| `-be` and `symlink removed` | 16 |

No subset of **three** facets reaches 20 (searched all 41 subsets of size ≤ 3). The smallest
sufficient sets are four facets — **{H, G, BE, SR}**, 9 blocks — and five facets —
{G, D, BE, SR, P}, 8 blocks.
Since H/D/P are individually redundant, the only irreducible core is **{gap kinds, `-be`,
`symlink removed`} plus one endianness/dependency discriminator**.

Consequence for the depth axis: the landed table's `handler`, `dependencies` and
`published files` cells are decoration for the score — they add safety (a mismatched
envelope falls to `unclassified` instead of being mislabelled) but not discrimination.
The landed table's 20/20 rests on `-be` and `symlink removed` for 4 of 20 envelopes; the
other 16 are separable without either.

## 5. Does the interpreter read beyond the six features? No.

`tools/round-39/sqfs-triage.py` touches exactly these envelope reads (line numbers in the
frozen file, byte-identical at `8fcda41c` and HEAD):

| read | feeds |
|---|---|
| `normalized_result.chunks[].handler` (prefix `squashfs`) | **handler** |
| `normalized_result.extraction_gaps[].kind` | **gap kinds** |
| `normalized_result.extraction_gaps[].dependencies` | **dependencies** |
| `sasquatch*` argv from `nr.diagnostics[].report.command`, `data.diagnostics[].report.command`, any `raw_result` `command` | **`-be in child argv`** |
| `MaliciousSymlinkRemoved` typename in `nr.diagnostics[].report` or anywhere under `raw_result` | **symlink removed** |
| `len(normalized_result.files)` | **published files** |

Nothing else: not `subject`, `parameters`, `coverage`, `unpublished_entries`,
`derivations`, `depth_limited_paths`, `limitations`, `confidence`, `evidence_id`, and not the
manifest, `tree.json`, `run.json` or the carrier. `raw_result` is walked for two keys only
(`command`, `__typename__`); the recorded sasquatch stderr — which does differ by class — is
never read.

## 6. Label leakage: three tests, all negative

1. **Token scan.** `grep -l -F` over `H*/envelope.json` for `clean`, `escaping`, `in-tree`,
   `intree`, `dep-missing`, `avm`, `body-extractor`, `no-squashfs`, `version-minor`, `label`,
   `class`, `arm` → **0 files** each. The only identifier present is the carrier id
   (`H01`…`H20`) inside `parameters.output_directory`
   (`…/r39-heldout-u1ksej3n/rea-H13/out`) and `subject.local_path`; the grammar has no
   path-valued cell and the interpreter never reads those fields.
2. **Injection.** Each envelope rewritten with top-level `class`, `label`, `arm` and an
   `annotations.triage_label` carrying its true class → interpreter rc 0, **no label and no
   feature changed** for any of the 20.
3. **Ablation.** Each envelope reduced to `normalized_result.{chunks, extraction_gaps,
   diagnostics, files}` + `raw_result` (everything else deleted) → features and labels
   bit-identical for all 20; MIN-8row-7cell still 20/20, SHORTCUT still 16/20.

The manifest is the oracle and the interpreter never sees it; the counter grades with the
interpreter (`c2-counter.py` `measure()` `labels` map) after checking subject digest,
`operation == extract_firmware`, regeneration, and first-add ordering.

## 7. Defects

**D1 (documentation, frozen path) — `corruption_bad_minor`'s docstring is false.** In the
freeze bytes of `tools/round-39/heldout-gen.py`:

```
def corruption_bad_minor(payload, endian):
    """s_minor 4 -> 5 so no unblob v4 handler matches; the image stays a plain unknown chunk."""
```

measured opposite: H19/H20 carry chunk handler `squashfs_v4_be` with `extraction_failed:
true`, gap `extractor-failure`, and a recorded `sasquatch-v4be -be …` command. The file
contradicts itself — the `RECIPES` comment for `version-minor-mismatch` says the pattern
"pins `s_major`", i.e. s_minor 5 still matches. A reader trusting the docstring would
predict `no-squashfs-chunk` output and mis-triage H19/H20.
*Smallest safe correction:* carry it as a known erratum in the lesson/QUALITY text and fix
the docstring at the **next** freeze — editing `heldout-gen.py` now would itself make
`frozen_path_changed` true for every C2 score.

**D2 (predicate shallowness, no action needed on the landing) — the target admits a
degenerate default row.** `matched == 20` is satisfied by a table whose last row is all `*`,
which labels every envelope outside the held-out set (`clean`). Measured: a BE clean
envelope with `gap kinds [depth-limited]` is labelled `clean` by `MIN-8row-7cell`, while the
landed table, `MIN-8row` and the intended design all return `unclassified`. The landed table
is on the safe side of this; the kill rule (CTL-C2-1 catch-all) does not catch it, because a
7-lookup + default table is not a catch-all. If a later round wants depth to mean
"triage table", the counter needs an out-of-set envelope that must return `unclassified`.

**Not a defect (checked because it looks like one).** Commit `52b0eb29` edits `SKILL.md`
(+28 lines, the `### Round-35/37/38/39 instrument registry`) but it is **not** an ancestor of
the measured revision `6fdaf4f1` (`git merge-base --is-ancestor` → NO), and the frozen C2
paths — `sqfs-triage.py`, `heldout-gen.py`, `c2-counter.py`, `plans/round-39-claims.md`,
`SKILL.md` — are untouched in `8fcda41c..6fdaf4f1`. The triage table block is
**3086 bytes and byte-identical** at freeze and HEAD (`table_block` from the counter run on
both). So the freeze-integrity rule is not tripped by the later SKILL.md edit.

## 8. Commands, exit codes, artifacts

All interpreter runs used `python3 -I -B` (Python 3.14.8) with the frozen tool; cwd was the
lane except for scratch writes under `S=/fast/scratch/hyaku/kaidoku-r39/R39W2C2Shortcut`
(removed at the end) and one 1 KB selftest log at `/tmp/c2self.txt` (removed). No REA run, no unblob
run, no carrier built: the held-out data already exists and this seat only reads it. No tool
installed or updated (nothing to record under the tooling directive). No VCS mutation; only
`git show/log/merge-base/diff/status`.

```
# landed
python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json corpus/evidence/round-39/c2/heldout/H*/envelope.json   # rc 0, rules 8, 20/20
# the four tables (frozen interpreter, same envelopes)
--skill .ufo/waves/round-39/w2/artifacts/R39W2C2Shortcut/{MIN-8row-7cell,MIN-8row,SHORTCUT-no-be-no-sr,VARIANT-no-be-only,VARIANT-no-sr-only}.md
  -> 20/20, 20/20, 16/20, 18/20, 18/20   (all rc 0)
# dev set (wave-1, seed sha256("dev1"))
.ufo/waves/round-39/w1/artifacts/R39C2HeldoutGen/dev-run/H*/envelope.json
  -> landed 16/16, MIN-8row-7cell 16/16, MIN-8row 16/16, SHORTCUT 12/16
# tool sanity
python3 -I -B tools/round-39/sqfs-triage.py --selftest    # rc 0, cases=35 pass=35
python3 -I -B tools/round-39/c2-counter.py --selftest     # rc 0, cases=27 pass=27
# leakage
grep -l -F <token> corpus/evidence/round-39/c2/heldout/H*/envelope.json   # 0 files for 12 tokens
# freeze integrity
git merge-base --is-ancestor 52b0eb29 6fdaf4f1            # rc 1 (NOT ancestor)
git log --format=%h 8fcda41c..6fdaf4f1 -- tools/round-39/sqfs-triage.py tools/round-39/heldout-gen.py tools/round-39/c2-counter.py plans/round-39-claims.md SKILL.md   # empty
```

Artifacts (`.ufo/waves/round-39/w2/artifacts/R39W2C2Shortcut/`): `MIN-8row-7cell.md`,
`MIN-8row.md`, `SHORTCUT-no-be-no-sr.md`, `VARIANT-no-be-only.md`, `VARIANT-no-sr-only.md`,
`results.json`.

Housekeeping note for the L1: this seat first resolved two relative `write` paths against the
session cwd, so files landed briefly at `<fleet>/.ufo/waves/round-39/w2/artifacts/…`; they
were moved into the lane and the empty directories removed. Sibling report files
(`R39W2HeldReproB.md` and a `R39W2ReproK*` file, still changing as their owners rewrite them)
sit at `<fleet>/.ufo/waves/round-39/w2/`; they are not mine and were left untouched.

## 9. Limits and inferences

- The floor proof (§2) and the ceilings (§3, §4) are proofs about the *frozen grammar and
  this held-out set*, not about the class population. [INFERENCE] a held-out set with a
  different class mix (e.g. one AVM carrier, three escaping carriers) would move the
  marginal value of `-be`/`symlink removed` without changing the structure of the argument.
- "Eight labels" is what the predicate scores; ten generator classes fold into eight labels
  (both endiannesses of `clean`; `version-minor-mismatch` into `body-extractor-failure`), so
  the 20 envelopes carry 8 label decisions, and 4 of 20 sit in the two hidden-feature blocks.
- My tables are post-hoc fits to the held-out set; that is the point of the exercise (they
  answer "could a shallower table have passed?"), not evidence that a pre-freeze author would
  have written them. That MIN-8row-7cell also scores 16/16 on the independent dev set is a
  weak generalisation check only.
- The `-be` feature is a token test on the recorded argv; [INFERENCE] any future envelope that
  records a sasquatch command for a purpose other than extraction could move it, but no such
  envelope is in scope here.
