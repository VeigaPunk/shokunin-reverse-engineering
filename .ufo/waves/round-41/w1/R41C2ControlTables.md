DONE — 11 v3-grammar control documents written and scored (no shortcut above 32/36 on the planned class set; reference row set 36/36), with a reusable scorer harness, and two draft-level risks found in the `**Label precedence**` list (step-3 unnamed dependency; step-7 position versus step 4 when a depth envelope also carries `extractor-failure`).

# R41-C2 control tables — wave 1 (pre-freeze)

Seat: `R41C2ControlTables` (executor). Base `49096c7e6f226af0c750c4b003be58883cb6049f`. Nothing here is frozen; the L1 integrates and commits.

## 1. What was delivered

All files under `.ufo/waves/round-41/w1/artifacts/R41C2ControlTables/`; sizes and hashes at §9. Shorthand for the precedence bullets: **s1–s12** = the twelve numbered items of `**Label precedence**` in `plans/round-41-claims.md`.

| control | file | rows | measured 26 committed | measured 10 predicted | measured 36 planned | must miss |
| --- | --- | --- | --- | --- | --- | --- |
| CTL-C2-0 | `CTL-C2-0-base-SKILL.md` (byte copy of base `SKILL.md`, sha `926dac30…0054`) | — | 0/26, interp exit 2 | 0/10, exit 2 | **0/36** | every step, because the v3 interpreter refuses a document whose craft section carries only a v2 marker (`v2-interp-gate.txt` shows the same document is a working v2 surface: round-40 interpreter exit 0, `H01 → clean/none`) |
| CTL-C2-1 | `CTL-C2-1-catch-all.skill.md` | 1 | 4/26 | 0/10 | **4/36** | s1 on out-of-domain, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11 (both `clean` and `clean-empty`) |
| CTL-C2-2 | `CTL-C2-2-v2-verbatim.skill.md` | 11 | 26/26 | 0/10 | **26/36** | s4 on `partial-in-tree`, `partial-mixed`; s7 on `depth-limited-alone`, `depth-limited-in-tree`, `depth-limited-mixed` |
| CTL-C2-3 | `CTL-C2-3-actions-rotated.skill.md` | 12 | 2/26 | 0/10 | **2/36** | the action cell of s2–s11 on every class those steps cover (labels stay right; only s1 survives, because the default pair is emitted) |
| CTL-C2-3b | `CTL-C2-3b-v2-actions-rotated.skill.md` | 11 | 2/26 | 0/10 | **2/36** | same, composed onto the v2 row gaps (so the five combined classes also lose their label) |
| CTL-C2-4 | `CTL-C2-4-no-contains.skill.md` | 12 | 26/26 | 2/10 | **28/36** | s4 on `partial-in-tree`, `partial-mixed`; s7 on `depth-limited-in-tree`, `depth-limited-mixed` (s7 survives on `depth-limited-alone`, whose gap set is a singleton) |
| CTL-C2-5 | `CTL-C2-5-default-row.skill.md` | 12 | 26/26 | 4/10 | **30/36** | s4 on `partial-in-tree`, `partial-mixed`; s7 on `depth-limited-mixed` only |
| CTL-C2-5b | `CTL-C2-5b-all-star-default-row.skill.md` | 12 | 24/26 | 4/10 | **28/36** | s1 on out-of-domain, plus everything CTL-C2-5 misses |
| CTL-C2-5c | `CTL-C2-5c-inert-default-row.skill.md` | 12 | 26/26 | 0/10 | **26/36** | identical to CTL-C2-2: an `unclassified`/`none` `*` row restates the no-match default |
| CTL-C2-6 | `CTL-C2-6-depth-row-only.skill.md` | 12 | 26/26 | 6/10 | **32/36** | s4 on `partial-in-tree`, `partial-mixed` only |
| CTL-C2-REF (**not a control**) | `CTL-C2-REF-precedence.skill.md` | 12 | 26/26 | 10/10 | **36/36** | none — the positive reference: the row set the frozen v3 table must reach |

The seven required controls are CTL-C2-0…CTL-C2-6 (CTL-C2-3b/5b/5c are the cheap extra shapes that make the reading unambiguous; CTL-C2-REF is the reachability witness, not a kill-rule control). `CTL-C2-5` keeps operation/provider `extract_firmware`/`unblob` so it is the *strongest* domain-guarded catch-all; CTL-C2-5b is the literal all-`*` reading and is strictly worse because it also swallows s1.

## 2. How the controls were scored, and how to re-score with the frozen tools

```
A=.ufo/waves/round-41/w1/artifacts/R41C2ControlTables
$A/score-controls.sh --interp <interpreter> --eval <independent evaluator> \
  --envelopes corpus/evidence/round-41/c2/heldout \
  --control "CTL-C2-0-base-SKILL=<base SKILL.md>" [--detail]
```
* `score-controls.sh` scores every `*.skill.md` in its own directory (or `--controls DIR`), plus any `--control NAME=PATH` (used for CTL-C2-0, which is not `*.skill.md`), and prints `NAME matched/n` plus the interpreter exit code. `--envelopes` is repeatable (used for the 26+10 = 36 planned set). Exit 0 = scored, 2 = usage/IO/evaluator failure — never a control verdict.
* Evaluator contract accepted: `eval ENV...` printing TSV `path<TAB>label<TAB>action`, a JSON list of `{path,label,action}`, or a JSON object with a `results` list. The script falls back to one-envelope invocations if the batch call fails. If `tools/round-41/indep-eval-v3.py` prints some other shape, add a thin adapter or extend `pairs_from` in the script.
* Interpreter contract: `--skill SKILL --json ENV...` (the v2 CLI, which the v3 contract inherits). A non-zero interpreter exit is reported as exit=N and scores 0.
* For this wave I ran the DEV tools in this artifact directory, because `tools/round-41/sqfs-triage-v3.py` and `tools/round-41/indep-eval-v3.py` do not exist yet (§6, risk 1):
  * `v3-check-interp.py` — my replica of the v3 contract (marker v3, `none`/`*`/exact/contains set cells, first match, no match → `unclassified`/`none`, exit 2 on v2 marker, duplicate label, undeclared action). Its 9 inline selftests pass. **Parity evidence:** on a v2-row table it reproduces `tools/round-40/sqfs-triage-v2.py` on all 26 committed envelopes — identical `(label, action)` and identical feature tuples (`OP, PV, H, G, D, BE, SR, P`), 0 differences.
  * `preview-precedence.py` — the twelve bullets executed literally, with actions taken from the round-40 manifest `label_actions` map plus the draft's `raise-depth` for `depth-limited-nested`. **Calibration:** on the 26 committed carriers it agrees with the round-40 held-out manifest's declared `label`/`action` 26/26 (`precedence-vs-manifest.txt`), so the action half of every expected pair is anchored, not invented.

## 3. Control-by-control: what each one must miss, and why (observed)

Class names: v2's 13 (`clean-be`, `clean-le`, `clean-empty`, `escaping-symlink-removed`, `in-tree-symlink-metadata`, `mixed-symlinks`, `dep-missing-be`, `dep-missing-le`, `avm-marker-be-dropped`, `body-extractor-failure`, `partial-body-failure`, `no-squashfs-chunk`, `out-of-domain`) plus the five planned combined classes (`partial-in-tree`, `partial-mixed`, `depth-limited-alone`, `depth-limited-in-tree`, `depth-limited-mixed`).

* **CTL-C2-0 (base SKILL).** Must miss every step on every class: there is no v3 table, so nothing is labelled. Observed: exit 2, `line 361: a v2 marker is refused by the v3 interpreter`, 0/36. This is also the "command that shows C2 unmoved" fixture for the claim: the frozen v3 interpreter on the base `SKILL.md` must exit 2.
* **CTL-C2-1 (one all-`*` row, `clean`/`none`).** Must miss s1 (it labels `clean/none` where the domain guard demands `unclassified/none`), s2, s3, s4, s5, s6, s7, s8, s9, s10, s11 — every class except `clean-be`/`clean-le`. Observed 4/36; `clean-empty` is the sharpest evidence (`want clean-empty/confirm-empty got clean/none`), since a catch-all cannot even distinguish "no regular file" from "clean".
* **CTL-C2-2 (round-40 v2 rows, marker swapped).** The transcription is byte-identical to the `SKILL.md` v2 block except the marker line (verified: 15 block lines, 1 differing line). Must miss s4 on `partial-in-tree`/`partial-mixed` (both carry `G = {extractor-failure, unpublished-entry}`, and the row's `gap kinds` cell is the exact set `extractor-failure`), and s7 on all three depth classes. Observed: `partial-in-tree` → `unclassified/none`; `partial-mixed` → **`escaping-symlink-removed/expect-link-absent`** (the SR=yes `*`-gap row fires before anything else); `depth-limited-alone`/`-in-tree` → `unclassified/none`; `depth-limited-mixed` → `escaping-symlink-removed`. Note the two mislabels, not just abstentions: the v2 table does not merely fail to cover the combined classes, it answers wrongly on the ones that carry a removed symlink. It also cannot emit `depth-limited-nested`/`raise-depth` at all, because its actions line declares the 11 v2 actions.
* **CTL-C2-3 (reference rows, action column rotated by one).** Every label and feature cell is the reference; only the action cells move, and the rotation has no fixed point (asserted by the generator). Must miss the action half of s2–s11 on every class those steps cover; it cannot miss s1, where the interpreter emits the default pair without consulting a row. Observed 2/36 = exactly the two out-of-domain envelopes. This isolates the scoring surface: a counter that compared labels only would score this table 36/36.
* **CTL-C2-3b (v2 rows, action column rotated).** The composed shortcut. 2/36; on the five combined classes both halves are wrong.
* **CTL-C2-4 (reference rows, contains form removed).** Every `kind+` cell becomes the exact set `kind`. Must miss s4 on `partial-in-tree`/`partial-mixed` and s7 on `depth-limited-in-tree`/`depth-limited-mixed`; s7 survives on `depth-limited-alone` because `G = {depth-limited}` happens to be an exact match. Observed 28/36. The `depth-limited-mixed` miss is `unclassified/none`, not `escaping` — because the reference escaping row is `gap kinds = none` (s9 says `G = ∅`), whereas v2's was `*`.
* **CTL-C2-5 (v2 rows + one final `*` row, `depth-limited-nested`/`raise-depth`, domain cells fixed).** The `*` row can only catch envelopes that reach the bottom of the table. It rescues `depth-limited-alone` and `depth-limited-in-tree`, but **not** `depth-limited-mixed`, because the escaping row is above it. Must miss s4 on both partial-combined classes and s7 on `depth-limited-mixed`. Observed 30/36 — and the partial-combined envelopes are now labelled *confidently wrong* (`got depth-limited-nested/raise-depth`) instead of abstaining, which is worse for a human reader even though the score is the same.
* **CTL-C2-5b (the same `*` row with all twelve cells starred).** Adds a s1 miss on `out-of-domain` (28/36): the all-star row erases the domain guard, which s1 exists to keep. Recorded so the "a final `*` row" reading is closed in both directions.
* **CTL-C2-5c (`*` row restating `unclassified`/`none`).** Behaviourally inert: 26/36, identical to CTL-C2-2. A default row that agrees with the interpreter default cannot encode any step.
* **CTL-C2-6 (v2 rows + the depth row only, contains `depth-limited+`, placed after the failure rows and before the symlink rows).** Must miss s4 on `partial-in-tree`/`partial-mixed` only. Observed 32/36: all six depth envelopes correct (`depth-limited-mixed` included, because the contains row now precedes the escaping row), and the two partial-combined classes still abstain (`partial-in-tree`) or mislabel (`partial-mixed` → `escaping-symlink-removed`). This is the strongest shortcut and it is the one the round-40 defect list alone would produce.
* **CTL-C2-REF.** 36/36 on the planned set, and matches the precedence on every envelope by construction. Its order encodes two facts that are easy to get wrong: (a) the dependency rows sit above the failure rows (s3 before s4); (b) the depth row sits **below** the `extractor-failure+`/`P>0` row and above the symlink rows (s4 before s7 before s8/s9/s10). `published files` partitions the partial/avm/body rows (`>0`, `0`, `0`), so the relative order of those three is free.

The mechanical view is `step-matrix.md`: rows = controls, columns = s1…s12, cell = number of planned envelopes whose expected step is that column and whose observed pair differs; the `matched` column reproduces `score-controls.sh` exactly. `class-tuples.md` lists the feature tuple of all 36 fixtures with the expected pair and step.

## 4. Calibration

1. **Ceiling.** No shortcut control reaches the target. The best are CTL-C2-6 and CTL-C2-5 at **32/36**; they are different mistakes that happen to score the same (fix depth only vs guess depth at the bottom). Next: CTL-C2-4 and CTL-C2-5b at 28/36, CTL-C2-2/5c at 26/36, CTL-C2-1 at 4/36, CTL-C2-3/3b at 2/36, base at 0/36.
2. **Minimum edit to reach the reference.** From CTL-C2-6, the only scoring-relevant delta is **one cell**: `partial-body-failure`'s `gap kinds` from `extractor-failure` to `extractor-failure+` (worth exactly 4/36). The other 25 cell edits listed in `ref-deltas.txt` are fidelity relaxations (`-be n/a`→`*`, `symlink removed no`→`*`, `dependencies none`→`*` on rows whose expected tuples are always empty; escaping `*`→`none`) that no planned class exercises — they matter only for envelopes outside the planned set. The v2→v3 story is therefore: one new row (depth, in the right place) and the contains form on the failure/partial/symlink rows.
3. **Vocabulary gate.** CTL-C2-2 proves a v2 table transcribed verbatim is *grammar-legal* under v3 (exit 0, no change in labels): the v3 grammar must stay backward-compatible with single-member exact sets and with a v2 actions line that omits `raise-depth`. A table whose actions line lacks `raise-depth` cannot reach the depth label even with correct rows — the counter should treat a missing action token as a table defect, not as a label miss.
4. **Exact-vs-contains portability.** v2 separated exact-set members with `+`; v3 uses a trailing `+` for contains. Every set cell in these controls is either `*`, `none`, or a **single** member (with or without the trailing `+`), so the documents parse identically under a comma-separated exact form and under the old plus-separated one. No control depends on resolving that ambiguity — worth stating in the grammar review, because a multi-member exact set (`a,b` vs `a+b`) is the one place a v3 interpreter and a v3 table can silently disagree.
5. **v2 interpreter is a hard gate.** The round-40 interpreter exits 2 with `marker '<!-- sqfs-triage-table v2 -->' absent` on all ten `*.skill.md` controls (`v2-interp-gate.txt`), and exits 0 on the base SKILL. The marker therefore isolates v3 cleanly in both directions.
6. **A `*` row is not a shortcut, it is a relocation.** Every catch-all variant below the symlink rows loses `depth-limited-mixed`; above them it breaks the symlink labels. There is no position where a single `*` row buys more than 4 envelopes.
7. **Sensitivity to the depth tuple.** If the measured `depth-limited-*` envelopes also carry `extractor-failure` (a nested chunk at the ceiling whose `extraction_failed` is true), the precedence list gives `partial-body-failure` at s4, *not* `depth-limited-nested`. On that variant of the same ten fixtures every shortcut control collapses to **0/10** while the reference stays 10/10 (`sensitivity-depth-with-extractor-failure.txt`): the depth row must sit **after** the contains-`extractor-failure` + `P>0` row, and a table that puts depth first (CTL-C2-6) scores worse than v2. Both tuple shapes are handled only by the reference order.

## 5. Attacks on the draft (for the L1 / R41C2TableDraft / R41C2Eval)

* **D1 — s3 has no label for a dependency gap that names neither binary.** REA emits `missing-extractor-dependency` with an **empty** `dependencies` list when the producer names no dependency (`dist/cli-runtime/cli.js :14213-14225`: `UNNAMED_DEPENDENCY_CONTINUATION`, `dependencies: []`). s3 then yields no label, and s4/s6 only apply if `extractor-failure` is also in `G`; otherwise the envelope falls to s12 `unclassified/none`. My reference implements fall-through and both dependency rows require the named token (`sasquatch-v4be+`, `sasquatch+`), so the behaviour is well-defined — but the *text* is silent. Either state the fall-through in the precedence list or add `dep-missing-unnamed`; if the counter's `class_expected` ever meets such an envelope the generator's class map will disagree with the evaluator and the claim fails on that binding.
* **D2 — s7's position relative to s4/s6 is load-bearing and unverified.** See §4.7. The draft's own class names (`depth-limited-alone`, `-in-tree`, `-mixed`) predict no `extractor-failure`, but that is a prediction: REA builds `depth_limited_paths` from `record.task.depth >= context.maxDepth` (`cli.js :14741`) and separately emits `extractor-failure` for any chunk whose `extraction_failed` is true (`:14266-14272`). If the nested chunk reports a failure, the depth label is unreachable by s7 and the planned class expectation silently becomes s4. R41C2ReconDepth's measured tuples must settle this before the freeze; the table order that survives either answer is the reference order (contains-`extractor-failure`, `P>0` first, then `depth-limited+`).
* **D3 — "one depth-limited gap" is wrong.** `depths` collects **every** task at depth ≥ `maxDepth`, so a `--max-depth 1` carrier can carry several `depth-limited` gaps (plus one per further child at the ceiling). Any table or counter keyed on a count breaks; s7's set-membership reading is the correct one, and the counter should compare gap-kind *sets*, not gap lists. The `depth-limited` gap itself carries `dependencies: []`, `handler: null`, and an `input_path` of the form `$output/...` (`:14273`), so nothing in that gap identifies the inner handler.
* **D4 — the `*` row must not be read as the grammar's default.** Two of the three `*`-row readings are inert or harmful (CTL-C2-5b/5c). If the grammar review wants a "default row" concept, it should be the interpreter's no-match pair, not a row.
* **D5 — the counter should score the pair, and report the halves.** CTL-C2-3 is the witness: labels 36/36 right, pairs 2/36. A per-half report (label match, action match) makes an action-vocabulary defect visible instead of looking like a labelling failure.

## 6. Risks and blockers

1. **Not yet run against the frozen tools.** `tools/round-41/sqfs-triage-v3.py` (R41C2Interp) and `tools/round-41/indep-eval-v3.py` (R41C2Eval) are other seats' deliverables and did not exist when this ran. All numbers above come from my DEV replica and the executed precedence list, both of which are validated against committed ground truth (§2). Rerun with §2's command at the freeze; the expected pattern is *ordering preserved* (base 0, catch-all ~4, v2 ~26, rotated 2, no-contains ~28, catch-all `*` ~30, depth-only ~32, reference 36). If the real interpreter disagrees on any control, treat the disagreement as a grammar-contract defect first, not as a control failure.
2. **Predicted fixtures.** The ten combined-class envelopes are **synthetic** (`predicted-envelopes/`, stamped `_control_fixture.predicted = true`). Their tuples are my [INFERENCE] from the precedence text, the committed v2 envelope shapes, and REA source reading; the round-41 held-out set is generated from the freeze hash and will differ. The committed 26 genuine envelopes carry the v2-class evidence; every claim about the five new classes must be re-read once R41C2Gen/R41C2ReconCombined/R41C2ReconDepth report measured tuples.
3. **Harness/evaluator contract.** `score-controls.sh` assumes an evaluator callable per envelope or in batch with the accepted output shapes. If `indep-eval-v3.py` diverges, fix the adapter, not the controls.
4. **Scope.** No REA, unblob, sasquatch or extractor run was made at all (so no reserved carrier was touched, and the 3490/5490/5491/7560 images and L3/L4 were never opened); no vendor bytes copied; no VCS mutation; no tool installed; scratch `/fast/scratch/hyaku/kaidoku-r41/R41C2ControlTables` removed before this report was written.

## 7. Tie to the kill rule

The draft's kill rule for C2 is "a control at target on the development envelopes (seed `sha256("dev41")`) stops C2". This seat supplies the control corpus for that check, and on the planned set it is **already stopped**: no control reaches 36/36, so the target cannot be met by a shortcut, and any table that reaches it must encode s4 and s7 in the reference order (with s7 not reachable when the class carries `extractor-failure`, per D2). The controls also give the round-41 counter a ready regression pack: CTL-C2-3/3b catch a label-only counter, CTL-C2-5c catches an inert default, CTL-C2-5b catches a domain guard that a `*` row erased, CTL-C2-2 catches a v2 table that was only re-markered.

## 8. Files and hashes (all under `.ufo/waves/round-41/w1/artifacts/R41C2ControlTables/`)

Controls (the delivered tables; `CTL-C2-0` is the byte copy of the base document, 216,562 bytes):

```
926dac301cf0281e2b35b6736b6f6ee869a0a1b415fd5207f9de3959c4ca0054  CTL-C2-0-base-SKILL.md
d99e2dd7b321fca9820ae67d695233e4cf0a419ad58b1f8a6a1095531c498bfd  CTL-C2-1-catch-all.skill.md
83a8d25dad78714dbf0b9d5ab542c434ee68c861bf2e63393d42cd750d95115f  CTL-C2-2-v2-verbatim.skill.md
01b5b685ec6eec3837070084aac99858217d9dd424c1530cf4a6e8f91d060ae0  CTL-C2-3-actions-rotated.skill.md
f50216bce3e2ac3fedf277ba5767d081908b895f89285fbf55a9cd25c54c8722  CTL-C2-3b-v2-actions-rotated.skill.md
825b0631d5a79f893857cbe2afb447da32db6a11d21aeca88bd56c01402e6182  CTL-C2-4-no-contains.skill.md
5e2954f141c730fb37c0db4e8d98365b4a68a2b344ee51b8a4dce80d33e82e6f  CTL-C2-5-default-row.skill.md
d4110b1ff7d9314cfa0e393f1b549daa81c0eaeedbc4c959b4dd46561bfbeed8  CTL-C2-5b-all-star-default-row.skill.md
1a0d0615b5723e215bd6eb230a58352d99bd020284e57b5ef207aa810c139526  CTL-C2-5c-inert-default-row.skill.md
a9caafe707485ecda2737bc087823d43b0caf7e27f18255bc457bb937b48ba78  CTL-C2-6-depth-row-only.skill.md
f22dbc7a3858d918c0aa0c47d6cef6b2eecea6ebf39abbddab4a8346ea1aaf25  CTL-C2-REF-precedence.skill.md
```

Tools (authored here, never in `tools/`): `make-controls.py` `6e07e92…3b7b` (generator: marker swap, rotation, contains strip, row insertion; writes `controls-manifest.json` `a4a3049…f372`), `v3-check-interp.py` `6469785…afdb` (DEV replica interpreter, `--selftest` 9/9), `preview-precedence.py` `685e92b…3aaf` (precedence as code), `score-controls.sh` `8e452ff…e1a9` (the harness), `step-matrix.py` `18ee887…3af4`, `diff-controls.py` `cbf4f3e…22d7`, `dump-tuples.py` `81b9f66…56ee`, `make-predicted-envelopes.py` `82510c4…ab03` (with `--variant depth-with-extractor-failure`).

Evidence: `scores-committed.txt` `4dae08d…1203e`, `scores-predicted.txt` `aaa6384…354e`, `scores-combined-36.txt` `2c64d58…8c03`, `step-matrix.md` `417d674…0210`, `class-tuples.md` `3c15eaa…0aaf`, `predicted-tuples.json` `4239d96…2ee6`, `ref-deltas.txt` `9592a68…b137`, `sensitivity-depth-with-extractor-failure.txt` `16615ff…478b`, `v2-interp-gate.txt` `c4663c3…cba0`, `precedence-vs-manifest.txt` `1052746…f148`. Ten predicted fixtures under `predicted-envelopes/`. Whole directory 664,038 bytes; largest file is the base-SKILL copy at 216,562 bytes, so nothing needs a rebuild-by-hash citation.

## 9. Exit criteria for this seat

* All eleven documents parse under the v3 contract and are refused (exit 2) by the v2 interpreter; the base document is refused by the v3 replica and accepted by v2. ✅
* Every required control misses the named precedence steps on the named planned classes, measured both on the 26 committed envelopes and on the 36-envelope planned set. ✅ (`step-matrix.md`)
* A harness exists that takes `(interpreter, evaluator, envelope dir)` and prints `matched/n` per control. ✅ (`score-controls.sh`, exercised against both the TSV and the `--json` output shapes)
* Reference reachability witness at target. ✅ (`CTL-C2-REF` 36/36)
* No reserved carrier, no REA/unblob run, no VCS mutation, no install, scratch removed. ✅
