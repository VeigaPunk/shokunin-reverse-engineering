# R41W2C2Regen — the R41-C2 held-out set regenerates byte-identically; the failing binding is a frozen-counter defect

**Verdict: DONE.** I attacked the *data* half of R41-C2: does
`corpus/evidence/round-41/c2/heldout/` (commit `8a1f4c73`, seed = freeze `d764389e`) regenerate from the
frozen seed, and do its envelopes carry the same decision features and the same
interpreter/evaluator pairs as a fresh, independent REA 6.5.0 run?

Everything on the data side reproduces: 52/52 carriers and 52/52 `tree.json` byte-identical (two
independent rebuilds, one with `--run`), `manifest.json` byte-identical
(`7717df938128bab093b6e6817c032d18e9f351934f441639317702cf2114d91d`), every regenerated envelope binding to its
carrier pin, **0** decision-feature differences across 52 envelopes, and **52/52** interpreter-vs-evaluator
pairs on both the committed and the regenerated set (13 distinct labels).

The one false binding in the frozen score, `observed_features_match_declared`, is **not** a data fault: the
frozen `c2-counter.py` resolves a carrier's declared tuple from `class_expected.features` / `features` /
`declared_features` / manifest-level class maps and never from `declared`, which is where the frozen
generator documents and emits it (`manifest.declared_schema.location = "carriers[].declared (every
carrier)"`). With a two-line `declared` fallback applied in scratch only, the *same* frozen counter at the
*same* revision returns `matched 52`, `bindings_false []`, `exit 0`, `met_target true`. Whether C2 may
therefore be scored MET is the L1's call (it needs a counter fix plus a defence of the fix under the
freeze-integrity rule); my measurement is that the honest stop currently attributes a tool-side key mismatch
to the data.

I did not touch C1, any lane file, or VCS.

## 1. Commands (all read-only against the lane; scratch under `/fast/scratch/hyaku/kaidoku-r41/R41W2C2Regen`)

```sh
S=/fast/scratch/hyaku/kaidoku-r41/R41W2C2Regen            # TMPDIR=$S, HYAKU_SCRATCH=/fast/scratch/hyaku
cd "$S"
# (1) full regeneration, one REA run per carrier, generator's own verify
python3 -I -B .../tools/round-41/heldout-gen-v3.py --seed d764389e9cbe61b9d1b07538ff3bff02d50bb34f \
        --out "$S/h" --run --verify                       # EXIT 0, wall 1m37.346s
# (2) carrier-only rebuild, no REA (determinism without the run)
python3 -I -B .../tools/round-41/heldout-gen-v3.py --seed d764389e... --out "$S/h2"   # EXIT 0, 0.376s
# (3) frozen C2 counter at the measured revision
TMPDIR=$S/tmp python3 -I -B .../tools/round-41/c2-counter.py --root <LANE> \
  --rev e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 --freeze d764389e... --json-out "$S/c2-at-e9a24d07.json"
#                                                                          EXIT 1
# (4) same counter + a 2-line `declared` fallback, scratch copy only
TMPDIR=$S/tmp2 python3 -I -B "$S/c2-counter-patched.py" ... (same args)     # EXIT 0
# (5) frozen tools on both envelope surfaces
python3 -I -B .../sqfs-triage-v3.py --skill SKILL.md --json <SH>/[HC][0-9][0-9]/{envelope,rea-full}.json
python3 -I -B .../indep-eval-v3.py --envelopes <SH> --full --out ...
python3 -I -B .../tools/round-40/sqfs-triage-v2.py --skill SKILL.md --json <committed>/[HC][0-9][0-9]/envelope.json
# (6) all comparisons, one script, reproducible
python3 "$S/compare.py" > "$S/compare.out"                                  # EXIT 0
```

`--run --verify` printed `52/52 carriers reached their declared tuple`. Toolchain observed by the run:
`rea-agents 6.5.0`, `unblob 26.6.4`, `sasquatch` and `sasquatch-v4be` `unsquashfs version 4.5.1`,
`Python 3.14.8`. No tool was installed, upgraded or removed.

## 2. Byte-level reproduction

| object | result |
|---|---|
| `manifest.json` committed vs regen(`--run`) vs regen(no-run) | identical, sha256 `7717df938128bab093b6e6817c032d18e9f351934f441639317702cf2114d91d` |
| 52 `carrier.sqsh` vs the manifest pins | 52/52 equal in both rebuilds (`carriers_byte_identical_to_pin {run: true, no_run: true, bad: []}`) |
| 52 `tree.json` (oracle) | 52/52 byte-identical to committed, in both rebuilds |
| manifest `seed` | equals the freeze commit `d764389e…` |
| shape | 21 classes (20 named × 2 replicates + `combo` × 12) = 52 carriers |

The pins are listed per carrier in `artifacts/R41W2C2Regen/hashes.txt`, so a reviewer can check the carrier
bytes without re-running REA. Because the committed carriers are byte-equal to a rebuild keyed by the freeze
hash, the set cannot have been produced from another seed and relabelled.

## 3. Envelopes: tuples, digests, pairs

Using the frozen counter's own `envelope_data`, `subject_sha`, `observed_features` (imported read-only):

- `observed_features` committed vs regenerated: **0 differences / 52** (handler set, gap kinds, gap
  dependencies, `-be` argv, `MaliciousSymlinkRemoved`, published 0/>0, `extraction_failed`).
- `subject_sha(envelope) == carrier pin`: **52/52 committed**, **52/52 regenerated** (the digest really does
  bind the envelope to the committed image).
- `rea-full.json["data"] == envelope.json`: 52/52.
- Declared tuple vs observed (reading `class_expected.features` for the 40 class carriers and
  `declared` for the 12 combos, plus `declared_extras` for `extraction_failed`/`max_depth`): **missing 0,
  mismatch 0, extras mismatch 0**.
- Interpreter ↔ evaluator, both files of each envelope (features, label/action/row identical between the
  `rea-full.json` and `envelope.json` surfaces):

| comparison | result |
|---|---|
| committed: `sqfs-triage-v3.py` vs `indep-eval-v3.py` | 52/52 |
| regenerated: `sqfs-triage-v3.py` vs `indep-eval-v3.py` | 52/52 |
| committed pairs vs regenerated pairs | 52/52 (and 52/52 rows) |
| distinct (label, action) pairs | 13, both sets |

Label histogram (identical in both sets): `partial-body-failure` 14, `depth-limited` 10,
`body-extractor-failure` 4, `clean` 4, `in-tree-symlink-metadata` 3, `mixed-symlinks` 3, and 2 each of
`clean-empty`, `escaping-symlink-removed`, `dep-missing-be`, `dep-missing-le`, `avm-marker-be-dropped`,
`no-squashfs-chunk`, `unclassified` (the unclassified pair is the out-of-domain arm). Interpreter rows:
12 distinct, decisions 13.

## 4. What does differ between committed and regenerated envelopes

An exhaustive JSON walk of the 52 `envelope.json` pairs finds differences on 28 field paths, all run
locators, and on `meta.duration` (52/52). Ranked: `raw_result.report[].reports[].path` (250),
`raw_result.report[].task.path` (250), `raw_result.execution.args[]` (204),
`report[].task.blob_id` / `subtasks[].blob_id` / `subtasks[].path` / `normalized_result.derivations[].provider_blob_id`
(200 each), `normalized_result.files[].path` (178), `subject.local_path`, `parameters.path`,
`evidence_id`, `parameters.output_directory`, `chunks[].provider_id`, `output_directory`,
`extraction_gaps[].provider_id`, `diagnostics[].report.command` and `.stderr`, `.target`, `.link`,
`Analysis.file_map[].id`, `Analysis.file_path`, `regions[].provider_id`, `carve_dir`.

No decision-bearing field appears in that list. Two checks make this concrete rather than assumed:
(1) the feature tuples are equal (§3), so handler sets, gap sets, gap dependencies, `-be`, removal and
P>0/P=0 are unchanged; (2) the *relative* published-path list per carrier (file paths with the run's
extraction root stripped) is identical for all 52 — the publication layout did not move, only the run root
prefix and the run-scoped ids did.

## 5. The failing binding: mechanism, evidence, and a two-line experiment

Frozen score at `e9a24d07` (`.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`) reproduced exactly
(§6): `exit 1`, `matched 52`, `matched_classes 40`, `matched_combos 12`, `distinct_decisions 13`,
`bindings_false ["observed_features_match_declared"]`, `declared_features.missing` = the 12 combos,
`declared_features.mismatch` = `[]`, `by_class.combo = "declared-tuple-incomplete"`.

Where it comes from, read off the frozen bytes:

1. `c2-counter.py:1486-1509` builds the declared tuple from `class_expected.features`, then
   `carrier.features`, then `carrier.declared_features`, then a manifest-level key from the list
   `class_features | classes_features | feature_tuples | features_by_class | class_tuples`. It never looks at
   `carrier.declared`.
2. `heldout-gen-v3.py` documents and emits the opposite: `manifest.json["declared_schema"]` =
   `{"binding": "observed_features_match_declared", "fields": [...6...], "location": "carriers[].declared
   (every carrier); declared_extras carries extraction_failed and max_depth ..."}`, `families.combo
   .class_expected = null`. All 52 carriers carry `declared`; the 40 class carriers additionally carry
   `class_expected.features`. That is why only the 12 combos are "missing" and nothing mismatches.
3. The counter's own selftest cannot see this: its stub generator (`STUB_GEN`, combo entry at
   `c2-counter.py:1717-1720`) emits `'class_expected': None, 'features': dict(FEATURES)` for combos — a shape
   the frozen generator never produces — and the red case `combo_feat_mismatch`
   (`c2-counter.py:2131`) mutates `entry['features']['gap_kinds']`, i.e. it exercises the stub's key, not the
   generator's. The fixture models the counter's assumption, so the assumption is never tested against real
   generator output.
4. The same schema drift appears, non-binding, in the advisory reader: `c2-counter.py:1459-1472` looks for
   `manifest["rea_params"]` and `carrier["max_depth"]`, while the v3 manifest uses `rea.per_class` and
   `carrier.rea.max_depth`. Result at `e9a24d07`: `advisory_rea_params.per_class_max_depth` all `null`,
   `depth_classes_missing` = all three depth-limited classes, although the manifest records `max_depth: 1`
   for exactly those classes and the envelopes show `parameters.max_depth: 1`.

Experiment (scratch copy only, never written into the lane): add
`elif isinstance(c.get('declared'), dict): decl = c['declared']` after the `declared_features` branch
(`artifacts/R41W2C2Regen/declared-key.patch`, 11 diff lines). Same counter, same `--root`, same `--rev`,
same `--freeze`:

```
{"bindings_false": [], "distinct_decisions": 13, "exit_code": 0, "matched": 52,
 "matched_classes": 40, "matched_combos": 12, "met_target": true, "met_target_consistent": true, "n": 52}
```

with `declared_features.missing []`, `mismatch []`, `by_class.combo "match"`. This is an experiment, not a
score: the scored instrument is the frozen one, and the data alone cannot lift the binding.

Consequence for the landing: under the frozen counter the C2 target ("`matched == n` and every binding
true") is held false by a resolution bug that is invisible to the counter's red selftests. The data meets
the binding the counter was trying to check. If L1 wants MET, the honest route is a counter fix (plus a
selftest whose fixture is the generator's `declared` shape) and whatever refreeze the freeze-integrity rule
requires; a report that says "the data failed to declare its tuples" would be wrong on the bytes.

## 6. Reproduction of the committed C2 score

`c2-counter.py --root <LANE> --rev e9a24d07 --freeze d764389e --json-out …` returns the committed score's
every field I compared — `exit_code`, `matched`, `n`, `matched_classes`, `matched_combos`,
`distinct_decisions`, `bindings_false`, `bindings` (all 29, `observed_features_match_declared` the only
false one), `met_target`, `met_target_consistent`, `declared_features`, `class_map_agreement`,
`class_expected_missing`, `manifest_first_add` (`8a1f4c73`), `frozen_paths_changed []`,
`actions_undeclared`, and the per-carrier rows — the only differing top-level key is `argv` (my `--json-out`
path). `class_map_agreement` is `{"agree": 40, "binding": false, "disagree": [], "missing": []}`.

## 7. Depth / calibration probes on the same bytes

- **v2 vs v3 separation on the held-out set.** The frozen round-40 table (`tools/round-40/sqfs-triage-v2.py`
  against the v2 history block in `SKILL.md`) agrees with the v3 evaluator on only **30/52**; the 22
  disagreements are the combined and depth cases (H27-H36, H39-H40, C01-C06, C08-C10, C12). The v2 label
  set has 12 labels and never emits `depth-limited`; `depth-limited` is the single v3-only label. So the
  held-out set does exercise the new precedence rather than only the v2 vocabulary.
- **Combos are not pure duplicates.** 8 of the 12 combo tuples coincide with a tuple some named carrier also
  reached on this seed; 4 (`C02`, `C03`, `C04`, `C06`) reach tuples no named carrier reaches. (On the dev
  seed wave 1 measured 6/12 outside; held-out is 4/12 — same order, different draw, which is what a seeded
  draw should do.)
- **Real-receipt binding.** The four committed round-40 C1 receipts get (`depth-limited`, `raise-depth`) from
  both frozen tools independently (interpreter rows match `gap kinds = depth-limited+`); the counter's
  `real_receipts_depth_limited` is true.
- **Table bytes.** `SKILL.md` is byte-identical at the freeze, at the measured revision and at the current
  head (`sha256 94d13b445701609f…`), and the `<!-- sqfs-triage-table v3 -->` block (9661 bytes) hashes
  `a1990986f6082ecf…` at the freeze and at `e9a24d07`. `git diff e9a24d07..HEAD` over
  `tools/round-41`, `tools/round-40/gen-squashfs.py`, `SKILL.md`, `corpus/evidence/round-41/c2/heldout`,
  `plans/round-41-claims.md`, `.ufo/waves/round-41/c1` is empty, so no C2 frozen path moved after the
  measured revision (the head is now `e1c83313`, one commit beyond the dispatch tip `7a24ff74`; that commit
  touches `corpus/README.md`, `corpus/SOURCES.md` and a new knowledge file only).
- **Held-out provenance.** `manifest.json` is first added in `8a1f4c73`, which descends from the freeze
  (`git merge-base --is-ancestor` yes; counter `manifest_after_freeze` true).

## 8. Limits

- Envelopes were regenerated **today, on this host**, with today's pinned toolchain. Equality of decision
  features and of all pairs is evidence that the outcomes do not depend on which run produced the envelope;
  it cannot prove which process wrote the committed files (the round-40 limit R40-CL2 stands, and R41-C2's
  predicate does not claim it). Run-scoped fields — extraction root, blob ids, `evidence_id`, durations,
  stderr text — necessarily differ and were excluded from every equality above.
- Only the freeze seed was exercised. I did not test other seeds, and I did not re-derive the v3 precedence
  text (the evaluator is treated as the frozen second rendering the claim says it is).
- The patched-counter result is a mechanism demonstration, not an admissible score: it uses a modified
  frozen tool on a tree whose freeze does not contain that modification.
- I ran no part of R41-C1 (no vendor fetch, no carrier extraction) and formed no verdict on it.

## 9. Files, artifacts, tooling

- Lane writes: this report plus `artifacts/R41W2C2Regen/` only. No `git`/`jj` mutation (read-only
  `show/log/diff/merge-base/rev-parse` only), nothing under `corpus/`, `tools/`, `plans/`, no PATH
  directory, no fleet-root file. Scratch removed at the end.
- Artifacts (≈690 KB, all regenerable by `compare.py` and the commands in §1): `compare.py`,
  `compare.out`, `compare.summary.json`, `hashes.txt` (manifest + all 52 carrier and tree hashes,
  committed vs both rebuilds), `combos.txt`, `relpaths.txt`, `l1-match.txt`, `toolchain.txt`, `gen.log`,
  `gen2.log`, `c2-at-e9a24d07.json`, `c2-at-e9a24d07-patched.json`, `c2counter.log`,
  `c2counter-patched.log`, `c2-counter-patched.py`, `declared-key.patch`, and the frozen tools' outputs
  (`committed-interp-env.json`, `regen-interp-env.json`, `committed-eval.json`, `regen-eval.json`,
  `v2interp.json`). Carrier bytes are not copied; `hashes.txt` carries their sha256.
- No tool installed or upgraded; no vendor or AVM bytes touched.
