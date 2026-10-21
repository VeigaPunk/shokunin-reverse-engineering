# Fixture03 — R23 `same_verb` control, source review

Candidate: 2838351450ff1ee4baa620c962a1153450d53311. Baseline: aa1450b82f9ede35aada63efe8a34e01c6e02f72.
All candidate bytes were read with `git show` / `git grep` / `git ls-tree`. Nothing was executed: no selftest, counter, or suite run. No installs. No peer report or lane file was modified.

## Findings

**Verdict.** The `same_verb` expectation `{exit 1, count 1, finding c1_incomplete}` is correct, and the case does catch witness double-counting of a held verb. It is weaker than its name suggests. It cannot observe its own new witness, it adds no kill that `mention_only` or `all_six` lack, and the suite has a surviving multiplicity gap for a non-held verb.

### F1 — Expected triple is correct [static trace, not executed]

- Expectation: `frozen/expected-v2.json:18-22` = `{exit 1, count 1, finding c1_incomplete}`.
- Writer: `tools/counter-fixtures.py:41-42` selects only `identify-flutter-build`. The envelope is written unmodified from `frozen/fixture.json:4-16` (`evidence_id` `ev_1111…` is 64 hex; `ok:true`; `meta.command` equals the verb; `data.operation` is `identify_flutter_build`). The entry line is `identify-flutter-build ev_1111… .ufo/waves/round-23/evidence/c1/identify-flutter-build.json`.
- Source row: synthetic S058, tier A, status mined, opened 2026-10-21, used-by = the entry. Baseline's highest id is S057, so there is no collision. The counter's cell indices 1/4/8/9/11 match the baseline header `id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by` (`corpus/SOURCES.md` line 5).
- Historical side [observed]: the recorded baseline R22 output (`.ufo/waves/round-23/before-r22-c1.json`, stdout) gives `t1_exercised=["identify-flutter-build"]`, `t1_exercised_count=1`, and **two** bound identify witnesses: `ev_6a84…` (saber, `flutter_detected:true`) and `ev_3458…` (godot, `flutter_detected:false`, `coverage:"complete"`).
- New side [inferred]: `bind_new` (`tools/count-c1.py:42`) finds no refusal ancestry, `bind_cli` returns 0, and `r21.bind` returns `evidence_bound`. Line 123 gates and line 124 appends the witness.
- Count [inferred]: `exercised = bool(historical or new)` (line 126) and `held` (line 127) collapse identify to one verb, so count = 1. `code = 0 if count == 6 else 1` (line 166) gives exit 1. Finding `c1_incomplete`.
- Consistency: count 1 equals the recorded R22 baseline 1/6 that the claims' `no_harm` rule preserves.

### F2 — Expectation and template are independent [observed]

- No script in the round-23 tree writes `expected-v2.json`. `git grep` finds only pins (`count-c1.py:25`, `verify/initial/source-pins.json:6`, `verify.py:108` as a read), the `gen-wave2.py` ticket text, and W1 notes.
- The literal triple is identical in `frozen/expected.json:18-22`, `frozen/expected-v1.json:18-22`, and `frozen/expected-v2.json:18-22`. The branch is identical in `frozen/counter-fixtures-v1.py:41-42` and `tools/counter-fixtures.py:41-42`. There is no drift between versions that would suggest tuning to output.
- No round-22 carry-over: baseline `round-22/tools/counter-fixtures.py` and `round-22/frozen/expected-v2.json` contain no `same_verb`.
- Template shape matches the producer. Baseline envelopes (`round-22/evidence/c1/identify-flutter-build-saber.envelope.json`, `identify-godot.envelope.json`) carry `ok`, `data{evidence_id, operation, raw_result:null, normalized_result}`, and `meta{command}`. These are the only keys the counter reads. The fixture's `normalized_result` is a stub; the refusal walk reads only structural keys, so the stub does not change binding.
- Pins verified at candidate: `counter-fixtures.py` `f2990b35…`, `fixture.json` `a1f5aff8…`, `expected-v2.json` `458b30d5…` (equal to `count-c1.py:25`).

### F3 — What the case distinguishes [inferred from code]

The harness compares only exit, count, and finding (`tools/counter-fixtures.py:112`). Mutants below are evaluated on that count-level observable.

| # | Mutant | same_verb count | Result | Also decided by |
|---|---|---|---|---|
| M1 | count every witness (historical + new) | 3 | KILLED | mention_only (2), all_six (8) |
| M2 | extra count for new witnesses of held verbs | 2 | KILLED | all_six (7) |
| M3 | multiplicity on historical side only | 2 | KILLED | mention_only (2), all_six (7) |
| M4 | ignore new witnesses | 1 | survives | all_six (1≠6), positive (1≠2) |
| M5 | ignore historical, keep new | 1 | survives | positive (1≠2), mention_only (0≠1) |
| M6 | drop both | 0 | KILLED | positive, mention_only |
| M7 | multiplicity on new witnesses of non-held verbs | 1 | survives all 21 cases | none |
| M8 | exercised=False when historical and new both present | 0 | KILLED | all_six (5) |
| M9 | candidate: per-verb boolean (lines 126–127) | 1 | pass | none |

- **F3a (weak; positive-preservation).** The new same-verb witness is invisible to this case. Accepted or rejected, it yields count 1. The case does not test that a valid same-verb witness binds.
- **F3b (weak; no unique kill).** Every mutant this case kills here (M1, M2, M3, M6, M8) is also killed by `mention_only` or `all_six`. It is a minimal isolating control for held-verb overlap, not a unique detector.
- **F3c (gap; falsifier-relevant).** No case gives any verb two new witnesses. The writer's default selects one envelope; `all_six` has one per verb; `same_verb` has one; `mention_only` has none; all others have one. M7 survives all 21 cases. The candidate is correct here (line 127 is per-verb). Suggested control: non-held `inspect-signal-decoders` with two distinct bound envelopes in one entry, expecting `{exit 1, count 2, c1_incomplete}`. The writer names files by verb (`PREFIX+verb+'.json'`), so this needs a per-document path.
- **F3d (observability limit).** Count-only comparison cannot tell which witness holds a verb. Baseline identify is held by both a positive and a negative, so dropping either leaves the count unchanged. This is not a `same_verb` defect. The falsifier "inherited identify lost" is covered by `inherited_lost` (exit 2 through `historical_evidence_changed`), not by any positive-witness count.

### F4 — Cosmetic (fixture only)

- `body.replace('\n## Paths', '\n'+row+'\n## Paths', 1)` leaves a blank line between the S057 row and the new S058 row, so S058 sits outside the Markdown table. The counter parses lines by regex, so the outcome is unaffected.

### F5 — Adjacent (outside `same_verb`)

- Baseline `identify` "exercised" includes a parsed negative (godot). It is `ok:true` and not a refusal, so the "refusal counted" falsifier is not triggered. Semantic note for the claim author only.
- Stale W1: `w1/ReviewRegistryHome.md:17` attributes the R22 digest `1abdd9df…` to the R23 selftest constant. The candidate constant is `458b30d5…` (`count-c1.py:25`).

## Recommended (not applied)

1. Add the two-witness non-held control in F3c. It kills M7.
2. Rename `same_verb` to describe "held verb gains a third witness", or keep the name and document it.
3. Any change to `expected-v2.json`, including added observed fields, changes the pinned digest `458b30d5…`. Do it as a new manifest version with re-pinned `count-c1.py` and `source-pins.json`, not in place.
4. Optional: move the S058 row inside the table (F4).

## Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture03.md` (this file). Digest recorded in the hand-off as computed by `sha256sum` after writing.

## Installs or none

- None. Only read-only git plumbing and `sha256sum` were used.

## Open risks

- F1's outcome is a static trace [INFERENCE]; only the historical half is observed, from recorded output. Nothing was executed.
- Mutant kill sets are reasoned from code, not run.
- The ignored `runtime/` directory and the lane worktree were not inspected.
