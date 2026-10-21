# Fixture02: R23-C1 control `all_six`, source review

Candidate 2838351450ff1ee4baa620c962a1153450d53311. Baseline B aa1450b82f9ede35aada63efe8a34e01c6e02f72.
Seat KaidokuR23.Fixture02. Source review only. Nothing executed: no selftest, no counter run, no REA, producer, device, or remote access. Candidate bytes read with `git show <candidate>:PATH`.
Labels: OBSERVED = bytes or a recorded artifact read here. INFERRED = static trace of source. UNKNOWN = not established.

## Verdict

1. **Expectation correct and independent.** `frozen/expected-v2.json:13-17` is `{exit 0, count 6, finding c1_complete}`, hand-written constants. The same block is in `frozen/expected-v1.json:13-17`, and `frozen/expected.json` is byte-identical to v1. It matches the counter contract: `tools/count-c1.py:166` gives exit 0 iff count == 6, and `:129` gives `c1_complete` iff six are held. OBSERVED.
2. **Passes at candidate.** INFERRED from the trace below. Also OBSERVED in the recorded run `verify/initial/selftest.json`: `all_six` observed count 6, exit 0, `c1_complete`, empty stderr; selftest `selftest_clean` 21/21, exit 0. That run was at `source_rev 6615aeae`. Every input it used is byte-identical at candidate (table below), so the record transfers. I did not re-run it.
3. **Discriminates** under-count faults (matrix below). It is the sole detector for the gdb, rizin, dart, and decode-signal bindings.
4. **Does not discriminate** (a) loss of the inherited identify witness, (b) any completeness threshold below 6, or (c) any over-count fault. (c) follows from the design: all_six is a positive-only case.

Stated fault taken as: a fully evidenced six-verb record must reach 6/6 and exit 0, so the counter cannot report a false incomplete. On that fault all_six discriminates the five non-identify verbs and the mapping faults. It is blind to identify inheritance, which the claims list as a falsifier ("inherited identify lost").

## Findings

### F1: MEDIUM. Weak mutation. all_six masks inherited-identify loss (mitigated by `positive`)
- OBSERVED `tools/counter-fixtures.py:40`: `selected = list(documents)`. All six envelopes are written, including a fresh `identify-flutter-build` (`frozen/fixture.json`, evidence_id `ev_1111...`).
- OBSERVED `tools/count-c1.py:81-83`: historical identify is `r22.measure(root, BASELINE)` and must equal `['identify-flutter-build']`. `:126`: `exercised = bool(historical or new)`.
- M1, drop the inherited witness from the union (`exercised = bool(target['new'])`): all_six still gives 6 and survives. `positive` expects 2 and observes 1, so it is killed. Only `positive` kills M1.
- M2, identify's new binding made dead: observationally equivalent under the pinned baseline. The historical identify always supplies the verb, so no expectation can change. This means identify's new evidence is never load-bearing in R23.
- W1 re-evaluation of `w1/CriticSeparation.md` (written against lane HEAD a3c92eb):
  - F1 (historical-root backdoor) is closed at candidate. Historical is measured at BASELINE (`count-c1.py:81`), and the round-22 root is tree-pinned against BASELINE (`:66-68`, `historical_evidence_changed`, exit 2). Fixture cases `historical_root_injection` and `inherited_lost` expect exit 2.
  - F2 (union-by-verb hides inherited loss) is reduced to code-level. The data-level route (editing R22 entries) cannot change `historical`, which is measured at B. The union at `:126` remains, and all_six cannot catch M1.
- Smallest correction, not applied (frozen v2): a derivative of all_six that withholds one non-identify verb, plus, optionally, a case asserting `t1_exercised` membership.

### F2: MEDIUM. Weak threshold. No case between 2 and 6
- OBSERVED expected counts over the 21 cases: 6 (all_six, 1 case), 2 (positive, 1 case), 1 (13 cases), null (6 unevaluable). Exits are 0, 1, 2. No case at 3, 4, or 5.
- M8, exit threshold `count >= 5` (`count-c1.py:166`), and M9, finding threshold `len(held) >= 5` (`:129`): both survive all 21 cases. all_six expects 6, which satisfies both.
- Smallest correction, not applied: a five-of-six derivative (withhold one non-identify envelope; expect exit 1, count 5, `c1_incomplete`).

### F3: MEDIUM. Structural. all_six can only fail by under-counting
- It cannot kill over-count mutants: mention counting, binding without a source row, refusal ignored. Those must be killed by negatives. Some are not (F4).

### F4: MEDIUM. Gate literals in `count-c1.py:107` have no discriminating case
- Each survives all 21 cases (OBSERVED from the per-case edits in `counter-fixtures.py:71-86`; outcome INFERRED):
  - M10: drop `row[9] == '2026-10-21'` (opened-date gate).
  - M11: drop `row[4] in ('A','B')` (tier gate).
  - M12: drop `row[8] == 'mined'` (status gate).
  - M13: drop `int(sid[1:]) >= 58` (range gate). Also masked for `old_source`, which exits 2 at `:72-73` before reaching `:107`.
- No case has a non-A/B tier, a non-mined status, a different opened date, or a pre-S058 source whose row is unchanged.

### F5: LOW. Decision-coupled input template
- OBSERVED `counter-fixtures.py:83`: the S058 row is tier `A`, status `mined`, opened `2026-10-21`. These are the literals of the gate at `count-c1.py:107`.
- `claims.json` `sourced` requires "opened/mined S058+ with exact used-by". It does not name tier A or the date. The positive therefore proves consistency with the counter's gate literals, not with the claim text.
- The expected values remain independent constants. Only the input template is coupled.

### F6: LOW. Template representativeness
- OBSERVED `frozen/fixture.json`: each envelope has only `ok`, `meta.command`, and `data` with `evidence_id`, `operation`, and `normalized_result: {control}`.
- OBSERVED real round-23 positives (`inventory`, `uart-help`, `decode-official-uart`, `decode-uart-hi`, `inspect-dart-legacy-saber` `.envelope.json`): `meta` has `command` and `duration`. `data` has at least 12 keys (my survey printed the first 12 alphabetically), including `raw_result: null` and a nested `normalized_result`. A structural key survey found no nested `ok`, no nested `error(s)`, `code`, `status`, `completion_status`, or `exit_code`, and no non-null `raw_result`. Nothing in these five indicates false refusal. all_six does not exercise these shapes.

### F7: ADJACENT (outside all_six; route to Fixture05 and L1). Expectation re-fitted to a new guard
- OBSERVED `frozen/expected-v1.json:33-37`: `old_source` = exit 1, count 1, `c1_incomplete`. `expected-v2.json:33-37`: exit 2, null, `unevaluable`.
- OBSERVED the fixture edit is unchanged (v1 `frozen/counter-fixtures-v1.py:77-78`, v2 `counter-fixtures.py:85-86`). It still rewrites historical row S051. In v2 the historical-sources guard (`count-c1.py:69-73`) fires before the eligibility gate (`:107`), so no case reaches the range gate.
- Effect: the expected value now follows the guard's output while the case name still denotes an ineligible-source check. This is the pattern that the `expected exits not self-derived` check (`gen-wave2.py:65`) exists to catch. Decide whether `old_source` should test eligibility (exit 1, row unchanged) or tamper (exit 2, own name).

### Checked, no defect
- The all_six branch is unchanged v1 to v2: `counter-fixtures.py:39-40` matches `frozen/counter-fixtures-v1.py:39-40`. The diff hunks begin at line 55.
- The all_six expectation is unchanged v1 to v2 (`expected-v2.json:13-17` matches `expected-v1.json:13-17`).
- No mutation branch matches all_six. Each branch tests a named case (`counter-fixtures.py:41-97`).
- Baseline registry (`corpus/SOURCES.md@B`): 57 rows, S001 to S057, no duplicates, no S058 or S059 (python check). No `duplicate_source_id` risk.
- Prerequisites exist at B (`git cat-file -e`, exit 0): `.ufo/waves/round-20/verify/round20/verb-coverage.json`, `.ufo/waves/round-22/tools/count-c1.py`, `.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json`. The `git add` at `counter-fixtures.py:100-102` cannot fail for all_six.
- Per-case reset (`counter-fixtures.py:35-36`, `reset --hard` and `clean -fd` on a disposable clone) prevents leakage from `positive` into `all_six`.
- `gen-wave2.py` writes only `wave2-spec.json` (`:79`). It emits no expected values, so the expectations are not generator-derived. Its 21 case names (`:23`) match `expected-v2.json`.

## Trace: all_six at candidate (INFERRED)
1. Selection is all six documents (`counter-fixtures.py:39-40`).
2. Each envelope is written to `.ufo/waves/round-23/evidence/c1/<verb>.json` (`:65`, `:69`). Entry lines are `verb eid path` (`:70`). The first line is `source: S058 ...` (`:47`).
3. The S058 row is inserted before `## Paths` (`:83-84`). It has 13 cells and is parsed at `count-c1.py:86-91`.
4. Eligibility (`count-c1.py:101-110`): S058 >= 58, tier A, mined, opened 2026-10-21, and the entry is in used-by. Eligible.
5. Cited paths (`:97`, `:112-118`). For each verb (`:119-124`), `bind_new` then `bind_cli` (`r22-count-c1.py:69-98`):
   - `meta.command` equals the verb.
   - `CLI_BIND_VERB` (`r22-count-c1.py:34-35`) maps debug-with-gdb to gdb-console and debug-with-rizin to rizin-debug-command.
   - The round-21 helper derives the operation as `verb.replace('-','_')` (`round-21 verb-coverage.py:85`). This equals the fixture `data.operation` for all six: gdb_console, rizin_debug_command, identify_flutter_build, inspect_dart_aot, inspect_signal_decoders, decode_signal_recording.
   - Each returns 0.
6. Historical identify from baseline (`:81-83`). `:126-127`: held is six. `:129`: `c1_complete`. `:166`: exit 0.
Result: (6, 0, c1_complete), matching the expectation.

Hash equality, candidate and recorded source 6615aeae (both via `git show`):

| file | sha256 (prefix) | identical at 6615aeae |
|---|---|---|
| tools/count-c1.py | f4b8d16a... | yes |
| tools/counter-fixtures.py | f2990b35... | yes |
| frozen/fixture.json | a1f5aff8... | yes |
| frozen/expected-v2.json | 458b30d5... (= `SELFTEST_MANIFEST_SHA256`, `count-c1.py:25`) | yes |
| round-22 tools/count-c1.py | c925918f... (= `LEGACY_SHA256`, `count-c1.py:23`) | pinned constant |

Round-20 and round-21 helper hashes (cfbf1880..., 61536938...) match `HELPER_SHA256` in `r22-count-c1.py:36-39` at candidate. They are pinned, so a mutation there fails closed with exit 2.

## Mutation matrix (lane-level `count-c1.py` unless noted)

| # | mutant | all_six | killed by |
|---|---|---|---|
| M1 | drop inherited identify from union (`:126`) | PASS (6) | positive only |
| M2 | identify new binding dead | PASS (6) | none; equivalent under pinned baseline |
| M3 | one non-identify verb's new binding dead | FAIL (5) | all_six; positive also for inspect-signal |
| M4 | `CLI_BIND_VERB` removed (gdb, rizin) | FAIL (4) | all_six only |
| M5 | inspect-dart-aot or decode-signal binding dead | FAIL (5) | all_six only |
| M6 | count bindings instead of verbs (`:127`) | FAIL (7) | all_six, same_verb |
| M7 | cap held at 5 | FAIL (5) | all_six |
| M8 | exit `count >= 5` (`:166`) | PASS | none |
| M9 | finding `len(held) >= 5` (`:129`) | PASS | none |
| M10 | opened-date gate removed (`:107`) | PASS | none |
| M11 | tier gate removed (`:107`) | PASS | none |
| M12 | status gate removed (`:107`) | PASS | none |
| M13 | range gate removed (`:107`) | PASS | none (old_source masked by `:72-73`) |
| M14 | mention counts (bind check bypassed at `:123`) | PASS (6) | mention_only |

Counts for FAIL rows are INFERRED from the trace. The matrix does not claim any mutant was executed.

## Produced files and hashes
- `.ufo/waves/round-23/w2/Fixture02.md`: this report. Its hash is given in the final message, since a file cannot contain its own hash.
- Scratch copies, git-ignored, under `.ufo/waves/round-23/runtime/KaidokuR23.Fixture02/`: `count-c1.py`, `counter-fixtures.py`, `expected-v2.json`, `fixture.json`, `r22-count-c1.py`, `frozen_expected.json`, `frozen_expected-v1.json`, `frozen_counter-fixtures-v1.py`, `gen-wave2.py`, `w1_CriticSeparation.md`. Hashes are in the table above and in the session transcript.
- Process disclosure: early in the review I wrote four candidate-byte copies to `/tmp`, outside the permitted write set. I removed them all. The two that were needed were re-extracted into the seat runtime directory. No peer report was edited.

## Installs
None.

## Open risks and unknowns
- The selftest was not executed by this seat. The pass at candidate is INFERRED from source, and the recorded pass at 6615aeae is OBSERVED. Transfer depends on the hash equalities above and on B being present in the snapshot (the fixture runs `git checkout B`).
- The recorded run has empty stderr for all_six. Its single verdict agrees with my trace but was not independently re-observed.
- F1, F2, F4, and M1 to M14 are conclusions from code and expectations, not executed mutants.
- Helper logic in r20, r21, and r22 is hash-pinned, so mutations there fail closed rather than survive. They are outside this control's discriminative remit.

Report: .ufo/waves/round-23/w2/Fixture02.md
