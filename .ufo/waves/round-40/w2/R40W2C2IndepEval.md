# R40W2C2IndepEval — independent evaluator for the SKILL SquashFS triage table v2

**Verdict: CONFIRMED.** An evaluator written from the table's column header and the round-40 v2
knowledge entry alone — never importing or reading `tools/round-40/sqfs-triage-v2.py` — labels all
26 committed held-out envelopes `(clean, none)` … `(unclassified, none)` exactly as
`corpus/evidence/round-40/c2/heldout/manifest.json` assigns them: **26/26, exit 0**, at
`42c10a58cb2cae3a4a0122af35a0cf95ac718043`. No disagreement exists to report. The same evaluator
reproduces **all seven frozen control scores (7/7, 182 decisions, wrong-class sets included)** and
every per-carrier row index in the C2 score receipt. Ambiguities in the grammar are real and
measurable; four are non-load-bearing on this set, one (`none` = empty set) is load-bearing. Two
structural facts the claim does not state are recorded below as calibration, not as defects.

I attacked: (1) whether the 26 pairs survive an independently written reader; (2) whether the
grammar I resolved is the frozen interpreter's grammar, via the controls; (3) how much of the table
is actually exercised by the held-out set (column ablation + row-order swaps); (4) whether the
envelopes are genuine REA 6.5.0 runs on the committed carriers (raw-vs-normalized agreement, digests,
oracle membership, and two live reruns).

Not attacked, by assignment: the C1 surface, `corpus/`, `tools/`, `SKILL.md` itself (read-only), and
the counter's own self-tests. I wrote only this report and
`.ufo/waves/round-40/w2/artifacts/R40W2C2IndepEval/`.

## 1. What I built

`artifacts/R40W2C2IndepEval/eval-v2-indep.py` (sha256 `83414ab4a33bf86b9bd66afd8cf1299f6524bc7d9d0eb7a93e20800d9fc11abb`).

Parse: locate `<!-- sqfs-triage-table v2 -->`, then the `<!-- sqfs-triage-actions: … -->` line, then a
header row that must equal the twelve expected column names, a separator row, and the data rows. A
malformed or missing block exits 2 before any envelope is read (grammar check: ≥1 row, unique labels,
every row action in the actions line). Rows are first-match, top to bottom; no match is
`(unclassified, none)`.

Features are read from `envelope.json` only:

| feature | source in the envelope |
| --- | --- |
| operation | `operation` |
| provider | `provider.id` |
| handler | set of `normalized_result.chunks[].handler` |
| gap kinds | set of `normalized_result.extraction_gaps[].kind` |
| dependencies | union of `normalized_result.extraction_gaps[].dependencies` |
| -be in child argv | tokens of `normalized_result.diagnostics[].report.command` (shlex): `yes` if a child command was recorded and carries the exact token `-be`, `no` if recorded without it, `n/a` if none recorded |
| symlink removed | present of a `MaliciousSymlinkRemoved` diagnostic report |
| published files | `len(normalized_result.files)` |

## 2. Result: 26/26, no disagreement

Command (scratch, table extracted with `git show 42c10a58…:SKILL.md`):

```
python3 -I -B eval-v2-indep.py --skill SKILL-at-42c10a58.md \
  --envelopes <lane>/corpus/evidence/round-40/c2/heldout \
  --manifest  <lane>/corpus/evidence/round-40/c2/heldout/manifest.json \
  --json-out labels-heldout-26.json
→ matched 26/26, exit 0
```

| id | class | handler | gaps | deps | -be | SR | P | decided (row) | expected | agree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H01 | clean-be | `squashfs_v4_be` | — | — | n/a | no | 5 | clean/none (10) | clean/none | ok |
| H02 | clean-be | `squashfs_v4_be` | — | — | n/a | no | 3 | clean/none (10) | clean/none | ok |
| H03 | clean-le | `squashfs_v4_le` | — | — | n/a | no | 8 | clean/none (10) | clean/none | ok |
| H04 | clean-le | `squashfs_v4_le` | — | — | n/a | no | 5 | clean/none (10) | clean/none | ok |
| H05 | clean-empty | `squashfs_v4_be` | — | — | n/a | no | 0 | clean-empty/confirm-empty (11) | clean-empty/confirm-empty | ok |
| H06 | clean-empty | `squashfs_v4_le` | — | — | n/a | no | 0 | clean-empty/confirm-empty (11) | clean-empty/confirm-empty | ok |
| H07 | escaping-symlink-removed | `squashfs_v4_be` | — | — | n/a | yes | 3 | escaping-symlink-removed/expect-link-absent (8) | escaping-symlink-removed/expect-link-absent | ok |
| H08 | escaping-symlink-removed | `squashfs_v4_le` | — | — | n/a | yes | 8 | escaping-symlink-removed/expect-link-absent (8) | escaping-symlink-removed/expect-link-absent | ok |
| H09 | in-tree-symlink-metadata | `squashfs_v4_be` | unpublished-entry | — | n/a | no | 8 | in-tree-symlink-metadata/count-gap (9) | in-tree-symlink-metadata/count-gap | ok |
| H10 | in-tree-symlink-metadata | `squashfs_v4_le` | unpublished-entry | — | n/a | no | 5 | in-tree-symlink-metadata/count-gap (9) | in-tree-symlink-metadata/count-gap | ok |
| H11 | mixed-symlinks | `squashfs_v4_be` | unpublished-entry | — | n/a | yes | 5 | mixed-symlinks/audit-symlinks (7) | mixed-symlinks/audit-symlinks | ok |
| H12 | mixed-symlinks | `squashfs_v4_le` | unpublished-entry | — | n/a | yes | 4 | mixed-symlinks/audit-symlinks (7) | mixed-symlinks/audit-symlinks | ok |
| H13 | dep-missing-be | `squashfs_v4_be` | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | dep-missing-be/install-extractor-be (2) | dep-missing-be/install-extractor-be | ok |
| H14 | dep-missing-be | `squashfs_v4_be` | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | dep-missing-be/install-extractor-be (2) | dep-missing-be/install-extractor-be | ok |
| H15 | dep-missing-le | `squashfs_v4_le` | missing-extractor-dependency | sasquatch | n/a | no | 0 | dep-missing-le/install-extractor-le (3) | dep-missing-le/install-extractor-le | ok |
| H16 | dep-missing-le | `squashfs_v4_le` | missing-extractor-dependency | sasquatch | n/a | no | 0 | dep-missing-le/install-extractor-le (3) | dep-missing-le/install-extractor-le | ok |
| H17 | avm-marker-be-dropped | `squashfs_v4_be` | extractor-failure | — | no | no | 0 | avm-marker-be-dropped/wrap-extractor-be (4) | avm-marker-be-dropped/wrap-extractor-be | ok |
| H18 | avm-marker-be-dropped | `squashfs_v4_be` | extractor-failure | — | no | no | 0 | avm-marker-be-dropped/wrap-extractor-be (4) | avm-marker-be-dropped/wrap-extractor-be | ok |
| H19 | body-extractor-failure | `squashfs_v4_be` | extractor-failure | — | yes | no | 0 | body-extractor-failure/preserve-failure (5) | body-extractor-failure/preserve-failure | ok |
| H20 | body-extractor-failure | `squashfs_v4_be` | extractor-failure | — | yes | no | 0 | body-extractor-failure/preserve-failure (5) | body-extractor-failure/preserve-failure | ok |
| H21 | partial-body-failure | `squashfs_v4_be` | extractor-failure | — | yes | no | 5 | partial-body-failure/salvage-partial (6) | partial-body-failure/salvage-partial | ok |
| H22 | partial-body-failure | `squashfs_v4_be` | extractor-failure | — | yes | no | 3 | partial-body-failure/salvage-partial (6) | partial-body-failure/salvage-partial | ok |
| H23 | no-squashfs-chunk | — | — | — | n/a | no | 0 | no-squashfs-chunk/inspect-input (1) | no-squashfs-chunk/inspect-input | ok |
| H24 | no-squashfs-chunk | — | — | — | n/a | no | 0 | no-squashfs-chunk/inspect-input (1) | no-squashfs-chunk/inspect-input | ok |
| H25 | out-of-domain | — | — | — | n/a | no | 0 | unclassified/none (—) | unclassified/none | ok |
| H26 | out-of-domain | — | — | — | n/a | no | 0 | unclassified/none (—) | unclassified/none | ok |

`distinct_decisions = 12` (11 rows + the no-match pair); rows used are `1..11` and `—`, each once, so
the predicate's "each expected pair maps to one table row (the no-match pair to none) and different
pairs to different rows" holds under my parse. `label_actions` in the manifest equals my parsed
label→action map plus the synthetic `unclassified/none`; the actions line set equals the row-action
set equals `action_vocabulary` (11 tokens, 11 rows, none unused).

The same table on the 26 **development** envelopes: 26/26, matching `c2-dev-scores.json`
`ADOPTED:SKILL.md`.

## 3. Result: the grammar is the frozen interpreter's, not my invention

Seven control tables on the 26 dev envelopes, my evaluator vs `.ufo/waves/round-40/controls/c2-dev-scores.json`:

| control | mine (exit, matched) | frozen (exit, matched) | wrong classes equal | agree |
| --- | --- | --- | --- | --- |
| CTL-C2-0 (base SKILL) | 2, 0 | 2, 0 | n/a (no table) | yes |
| CTL-C2-1 (catch-all) | 0, 4 | 0, 4 | 11 classes | yes |
| CTL-C2-2 (v1 rows + v2 actions) | 0, 18 | 0, 18 | clean-empty, mixed-symlinks, out-of-domain, partial-body-failure | yes |
| CTL-C2-3 (rotated actions) | 0, 2 | 0, 2 | 12 classes | yes |
| CTL-C2-4 (no domain guard) | 0, 24 | 0, 24 | out-of-domain | yes |
| CTL-C2-5 (no mixed row) | 0, 24 | 0, 24 | mixed-symlinks | yes |
| CTL-C2-6 (final `*` row) | 0, 24 | 0, 24 | out-of-domain | yes |

Receipt: `artifacts/R40W2C2IndepEval/controls-reproduction.json` (`all_agree: true`). Reproducing the
*wrong-class sets* of six mutants, not just their counts, is a constraint the evaluator had to satisfy
with no tuning; it is the main defence against my reading being fitted to the landing.

Row-level cross-check against `l1/scores/c2-at-42c10a58.json`: for all 26 carriers my
`(row, label, action)` equals the receipt's — `{}` disagreements over 26 comparisons; the receipt's
`distinct_row_list` `[1,10,11,2,3,4,5,6,7,8,9,null]` equals my used-row set. The counter's
`table.v2.bytes` is `6603`; my parsed block — marker line through the last row, joined with `\n` — is
**6603 bytes, sha256 `51e17a8d67acd574671c1848ade88609d46dbbe2405fd3ddf569c8f67ab122e6`**, byte-identical
at the freeze `7fce3086` and at `42c10a58` (15 lines: marker, actions, header, separator, 11 rows), and
absent at the base `fa6a8a3` (0 marker occurrences; my evaluator exits 2 there, as CTL-C2-0 requires).

## 4. Grammar ambiguities and what each costs

The header plus the knowledge entry do not pin these five readings down. I measured each alternative
(`artifacts/R40W2C2IndepEval/variants-matrix.json`):

| # | ambiguity | my primary reading | alternative | measured |
| --- | --- | --- | --- | --- |
| A1 | `gap kinds` / `dependencies` cell vs a set | exact set equality (singleton cell = singleton set) | membership ("the set contains this kind") | 26/26 both — **not load-bearing on this set** (every envelope has an empty or singleton gap set) |
| A2 | `none` cell in a set column | empty-set predicate | literal token `none` as a value | primary 26/26, literal **10/26** (16 envelopes fall to `unclassified`) — **load-bearing**; the prose carries it (row causes say "no gap was recorded") but the entry never states it |
| A3 | `-be in child argv: no` | a child command was recorded and lacks the token `-be` | "not yes", also covering an unrecorded command | 26/26 both — not load-bearing (`n/a` rows have `*` or match earlier rows) |
| A4 | domain columns | exact equality; no-match falls through to `(unclassified, none)` | drop the guard | 26/26 vs **24/26** (H25, H26 → `no-squashfs-chunk`) — load-bearing, and the only thing separating `inspect_firmware_regions`/`binwalk` from an empty `extract_firmware` envelope |
| A5 | `published files` | count of every `normalized_result.files` entry, nested carves included | top-level only | not load-bearing: only the `0` vs `>0` split is asked, and no envelope sits on that boundary differently |

Unresolvable from this set (declared untested, not defects): handler cell read as *all* handlers vs
*any* handler — no envelope has more than one chunk; the empty-handler-set-vs-pattern question — a
pattern cell on an empty set would match vacuously, but row 1 (`handler none`) is first and absorbs
every such envelope (H23/H24 unchanged under that reading); and the `yes` value for `-be`, which no
row carries, so a `-be`-carrying failure is distinguished only by row 4 requiring `no`.

## 5. How much of the table the held-out set actually exercises

Ablation — every cell of one column replaced by `*`, everything else untouched:

| ablated column | matched | envelopes that changed decision |
| --- | --- | --- |
| `handler` | 4/26 | 22 (everything except H23–H26, because row 1 becomes a catch-all) |
| `symlink removed` | 18/26 | 8 (H01–H06, H09, H10) |
| `-be in child argv` | 22/26 | 4 (H19–H22 → `avm-marker-be-dropped`) |
| `published files` | 22/26 | 4 (H05, H06 → `clean`; H21, H22 → `body-extractor-failure`) |
| `gap kinds` | 14/26 | 12 (H01–H12) |
| `operation` alone | 26/26 | 0 — `provider` still excludes the out-of-domain pair |
| `provider` alone | 26/26 | 0 — `operation` still excludes it |
| `operation` + `provider` | 24/26 | 2 (H25, H26) |
| `dependencies` | 26/26 | **0** |

Two findings for calibration, neither a defect against the stated claim:

1. **The `dependencies` column carries no load on this set.** `dep-missing-be` and `dep-missing-le` are
   already separated by the handler cell (`squashfs_v4_be` vs `squashfs_v4_le`), and no other row names
   a dependency; ablating the column changes nothing. The claim's disclosed limits mention the
   provider cell being untested alone; the dependencies column is untested *entirely* and would survive
   as prose. Same for each domain column individually — the pair is load-bearing, neither half is.
2. **Row order is load-bearing at two boundaries**, and the entry documents only one of them. Swapping
   the `mixed-symlinks` and `escaping-symlink-removed` rows (nothing else changed) scores 24/26
   (H11, H12 → `escaping-symlink-removed`); the entry does say v2 puts the mixed row first. Swapping
   `avm-marker-be-dropped` behind `body-extractor-failure` also scores 24/26 (H17, H18 →
   `body-extractor-failure`); the entry does not say the AVM row must precede the body row, and the
   AVM row is dead code behind it (`body` has `-be *`, `published 0`). The ordering principle
   (more specific row first) is sound; it is simply unstated.

## 6. Evidence integrity I re-derived independently

- **Digests**: for all 26, `sha256(carrier.sqsh)` = manifest `sha256` = `envelope.subject.digest.sha256`
  — 0 mismatches. Manifest: seed = freeze hash `7fce3086…`, 13 unique classes × 2, `label_actions`
  consistent with the table, action vocabulary = actions line, 131 tracked files under
  `corpus/evidence/round-40/c2/heldout` (manifest + 26 × 5).
- **Replicate variation**: every class's two carriers differ (all shas distinct); the differing
  manifest axes are compression (all 13 classes), endianness (clean-empty, both symlink classes,
  no-squashfs-chunk, out-of-domain) and damage (partial-body-failure) — consistent with the declared
  "differ in endianness, compression or tree".
- **Raw vs normalized**: descending `raw_result` report chains for `ChunkReport.handler_name`,
  nested `extraction_reports[].command` and `MaliciousSymlinkRemoved`, all 26 agree with the normalized
  fields my features come from — 0 mismatches. So my decisions do not depend on REA's normalization
  hiding raw evidence. `run.json`'s summaries (handlers, failed chunks, gap kinds, dependencies, file
  count) equal my independently derived features on all 26 — the L1's per-carrier summary is not a
  transcription drift.
- **Partial-body class is genuinely partial**: H21 publishes 5 files of which 4 match the oracle
  sha256 and one — `ctrl-f` — is a 16384-byte truncation of an 19873-byte oracle file; H22 publishes
  3 with one 8192-byte truncation of a 9389-byte oracle file. That is a real `extractor-failure` with
  a real partial publication, exactly the case the `salvage-partial` cause describes. `clean-empty`
  (H05, H06) has an empty oracle and 0 published files; `dep-missing` and body-failure classes publish
  0 of 4–6 oracle files.
- **Placement**: `git merge-base --is-ancestor 7fce3086 2d1acbcd` → true; `git log --diff-filter=A -1 --
  corpus/evidence/round-40/c2/heldout/manifest.json` → `2d1acbcd… round-40: R40-C2 held-out data`.
  `git log 7fce…42c10a58 -- SKILL.md` is empty: SKILL.md did not change between freeze and the
  measured revision, so the v2 block at the measured revision is the freeze block.

## 7. Live reruns (two carriers)

Local toolchain identity matches the envelopes exactly: `~/.local/bin/unblob` is a symlink to
`~/.local/share/uv/tools/unblob/bin/unblob`, sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`,
equal to every envelope's `normalized_result.engine.executable_sha256`.

```
cd <scratch> && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  <lane>/corpus/evidence/round-40/c2/heldout/H01/carrier.sqsh <scratch>/rerun/H01   → exit 0, 2.9 s
  (same for H17)                                                                   → exit 0, 2.9 s
```

| carrier | class | fresh features = committed | fresh decision | committed decision |
| --- | --- | --- | --- | --- |
| H01 | clean-be | all 8 equal | clean/none, row 10 | clean/none, row 10 |
| H17 | avm-marker-be-dropped | all 8 equal | avm-marker-be-dropped/wrap-extractor-be, row 4 | same |

Path-normalised `normalized_result` diffs between a fresh run and the committed envelope are only REA's
own blob ids (`provider_id`, `provider_blob_id`) — H01: 9 such fields, H17: 2; no semantic field
differs. The fresh H17 child command is `sasquatch-v4be -no-exit-code -f -d …` — no `-be` token, i.e.
the AVM branch fired, which is the feature that row 4 keys on; H01's fresh chunk handler is
`squashfs_v4_be` with zero gaps. Both fresh runs record `parameters.max_depth = 3`, the same value the
committed envelopes record, so the comparison is like-for-like (no `--max-depth` flag was passed).

`evidence_id` is **not** reproducible by a fresh run (`ev_beccc198…` vs committed `ev_f0ef96c3…` for
H01; `ev_25d9d11a…` vs `ev_1ca7914d…` for H17) because it binds `parameters.output_directory` and the
execution record. P40-C2 claims nothing about evidence-id recomputation (that is C1's binding), so this
is a note, not a defect — but no C2 argument should lean on envelope ids being stable.

## 8. Disagreements, risks, limits

- **Disagreements with the manifest: none.** All 26 `(label, action)` pairs, and all 26 row indices,
  match.
- **Prior exposure (calibration honesty).** Before writing the evaluator I read
  `l1/scores/c2-at-42c10a58.json` (which per-carrier row each envelope landed on) and
  `controls/c2-dev-scores.json` (control match counts and wrong classes) as background. Those are the
  two artifacts my result is compared against, so my parse is not blind; the counter-evidence is that
  the evaluator was written from the header and the entry, that it reproduces six mutants' *wrong-class
  sets* rather than being fitted to one table, and that its feature layer is independent (the receipts
  do not expose feature extraction, which I re-derived from `envelope.json` and cross-checked against
  raw reports). A blind re-derivation by another seat would strengthen this.
- **The set is closed and the classes were chosen by the round-39 defects** (disclosed in the entry):
  8 of 26 envelopes are decided by the distinguishing cells (clean-empty, mixed, partial, out-of-domain),
  the rest by cells that v1 already had. My ablation adds the same shape of statement for
  `dependencies` (§5) and for each domain column alone.
- **Untested by construction**: multi-handler envelopes, `unknown-chunk-handler`, `encrypted-chunk`,
  `depth-limited`, an envelope whose only gap is `unpublished-entry` *plus* `extractor-failure`
  (exact-set vs membership would then diverge and A1 becomes load-bearing), a `-be`-carrying
  dependency-missing envelope, and the `cause` column (prose, unscored, never read by my evaluator).
- **Tooling**: nothing installed or upgraded. Used the in-lane REA 6.5.0 package via `npx -y`
  (cache hit), `unblob` 26.6.4 via the existing `~/.local/bin` symlink, `python3` 3.14.8 stdlib only,
  and read-only git (`show`, `log`, `merge-base`, `ls-tree`, `diff`, `cat-file`). No pacman, no VCS
  mutation, no vendor bytes fetched or copied (the two rerun carriers are lane-built BE SquashFS
  images, not AVM firmware).

## 9. Retained evidence

All under `.ufo/waves/round-40/w2/artifacts/R40W2C2IndepEval/`:

| file | content |
| --- | --- |
| `eval-v2-indep.py` | the evaluator (sha256 `83414ab4…c11abb`) |
| `table-block-at-42c10a58.md` | the exact parsed block, 6603 bytes, sha256 `51e17a8d…b122e6`, identical at the freeze |
| `labels-heldout-26.json` | all 26 decisions + features + evidence ids + subject digests |
| `adopted-table-on-dev-26.json` | the same table on the 26 dev envelopes (26/26) |
| `score-CTL-C2-{1..6}.json` | per-control runs on the dev envelopes |
| `controls-reproduction.json` | mine vs `c2-dev-scores.json`, `all_agree: true` |
| `variants-matrix.json` | 17 variants: grammar alternatives, ablations, row-order swaps, base SKILL |
| `rerun-comparison.json` | H01/H17 fresh-vs-committed features, decisions, path-normalised diffs |

Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2C2IndepEval` is removed; nothing outside this report and
that artifacts directory was written.
