# CriticCausal — R22 separability (C1 vs C2), author-side critique

Seat: `KaidokuR22R.CriticCausal-6`, recovery wave W2. This review covers only the current authored evidence at HEAD `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`, measured against baseline B `7787fea4d6fd718726de92ed20759d11ce7b8b48` and declaration commit `75f04a4`. Nothing in the lane was edited. All mutations happened in temporary clones (`/tmp/kaidoku-r22-criticcausal-*`), which have been removed. No REA calls, no target execution, and no installs.

## Verdict

**Separability of the counted outcomes holds empirically, but the separability claim as written is false.** It is falsified in three places:

- **Read set and touches are under-declared.** C1 also depends on `corpus/SOURCES.md`, which neither the frozen read-set statement nor C1's `touches` list names.
- **C1's measurement is not pinned to the revision.** C1's count at a fixed revision changes when the working tree changes; C2's does not.
- **`PROVINCE.md` mixes both claims.** It carries C1 prose inside what `verify.py` treats as C2's "own diff". Applied alone, C2 lands a dangling citation.

The `verify.py` separability matrix that SCORECARD describes has no retained record.

## Commands and observed exits

All counter runs used `python3 -I -B`. stderr was empty in every case. Unless marked otherwise, "the counters" are the HEAD-content counters in `tools/`.

| # | Command (abbreviated) | Exit | Key output |
|---|---|---|---|
| 1 | `tools/count-c1.py --root <LANE> --rev 7787fea` | 1 | `t1_exercised_count 0`, `catalog_zero_count 20` |
| 2 | `tools/count-c1.py --root <LANE> --rev 2ee3d9f` | 1 | `t1_exercised ['identify-flutter-build']`, count 1, zero 19 |
| 3 | `tools/count-c2.py --root <LANE> --rev 7787fea` | 1 | `accounted_count 0` |
| 4 | `tools/count-c2.py --root <LANE> --rev 2ee3d9f` | 0 | `accounted_count 14`, `mismatched []`, `foreign_rows []` |
| 5 | `frozen/count-c1.py --root <LANE> --rev 2ee3d9f` | 1 | count 1 (`identify-flutter-build`) |
| 6 | `frozen/count-c2.py --root <LANE> --rev 2ee3d9f` | 0 | `accounted_count 14`, `mismatched []` |
| 7 | `git show 75f04a4:…/tools/count-c{1,2}.py \| cmp - frozen/count-c{1,2}.py` | 0, 0 | the frozen copies are byte-identical to the declaration commit |
| 8 | AST comparison of T1 and T2 across `claims.json`, both counters and `counter-fixtures.py` | — | all identical; T1 and T2 do not overlap |

The cross-application matrix (rows 9–13) was built like this: `git clone --shared` the lane, check out B detached, write the selected paths from 2ee3d9f, commit, then run both counters with `--root <clone> --rev <tip>`. The `= B output` columns compare each counter's full JSON output, minus `rev`, against its output at B.

| Sandbox (paths applied onto B) | c1 exit / count | c1 = B output | c2 exit / count | c2 = B output |
|---|---|---|---|---|
| 9. **C1 per `verify.py`:** `evidence/c1/*`, `corpus/knowledge/2026-10-21-r22-*`, `corpus/SOURCES.md` | 1 / **1** (zero 19) | False (expected) | 1 / 0 | **True** |
| 10. **C1 per its frozen `touches`:** `evidence/c1/*`, `corpus/knowledge/2026-10-21-r22-*`, `corpus/README.md` | 1 / **0** | False | 1 / 0 | True |
| 11. **C2 per `verify.py`:** `evidence/c2/*`, all of `PROVINCE.md` | 1 / 0 (zero 20) | **True** | 0 / **14** | False (expected) |
| 12. **C2 with the dispositions section only:** `PROVINCE.md` cut before `### Round-22 narrowly added static ground` | 1 / 0 | True | 0 / **14** | False (expected) |
| 13. **C2 receipts only:** `evidence/c2/*`, no `PROVINCE.md` | 1 / 0 | True | 1 / 0 | True |

Worktree-dependence probe, run in sandbox 9 at fixed tip `afe728b`:

- I appended `def bind(...): return {...}, 1` to `.ufo/waves/round-21/tools/verb-coverage.py`, uncommitted.
- `count-c1.py --rev afe728b` then gave exit 1, `t1_exercised_count 0`.
- After `git checkout -- <file>`, the same command gave exit 1, `t1_exercised_count 1`.

## Findings

### F1. The frozen separability statement is false: C1 reads more than it declares, and its `touches` list is incomplete

Impacted axes: coverage, calibration. This is a fixable declaration defect, not a counted-outcome coupling.

- The frozen claim at `claims.json:35` says: "C1 counter reads only corpus/knowledge and evidence/c1". The C1 counter also reads:
  - `corpus/SOURCES.md` at REV, in `count-c1.py:44-48`;
  - the retained catalog `.ufo/waves/round-20/verify/round20/verb-coverage.json` at REV, through `r21._measure` in `round-21/tools/verb-coverage.py:125`;
  - the full tree listing, in `count-c1.py:49`;
  - the helper modules round-20/21 `verb-coverage.py`, loaded from the working tree (see F2).
- C1's `touches` at `claims.json:22` lists knowledge, the README coverage map and `evidence/c1`, but not `corpus/SOURCES.md`.
- **Counterexample:** sandbox 10 applies exactly the declared C1 surface. C1 drops from 1 to **0**, because the `source:` gate (`count-c1.py:47-58`) finds no S051+ rows. C1 therefore cannot be "verified by applying its own diff alone" as `claims.json` defines that diff.
- **Causal origin:** the frozen counter (`frozen/count-c1.py`, identical to `75f04a4`) contains no `SOURCES` reference at all; `rg -c SOURCES` printed no count. The read of `SOURCES.md` arrived with the post-freeze edit in 2ee3d9f (+32 lines, `count-c1.py:43-58`). The frozen statement was true for the frozen counter and became false through that edit.
- **Duplicate authorities that disagree:** SCORECARD `SCORECARD.md:2741-2742` ("C1 reads sourced knowledge/evidence-c1 and its source registry") and `verify.py:83` (which adds `corpus/SOURCES.md` to the C1 partition) both contradict the frozen `claims.json:35`.
- **Smallest safe correction:** leave `claims.json` untouched, since it is frozen. L1 should record an explicit correction in LOG/SCORECARD: C1's true read set includes `corpus/SOURCES.md` and the retained catalog, and C1's attributable diff includes the S051–S053 `SOURCES.md` rows. Separability should then be judged on the `verify.py` partition, not on the frozen sentence.

### F2. C1's measured value is not a function of `--rev` alone

Impacted axis: calibration (an identity defect).

- `count-c1.py:26-35` and `:34-35` load `round-21/tools/verb-coverage.py` from `Path(root)` on the working tree. That module loads round-20 the same way (`round-21/tools/verb-coverage.py:104-109`). Neither is loaded from `git show REV:`.
- **Counterexample:** the worktree probe above. The same tip `afe728b` gives count 1 with a clean tree and 0 with one uncommitted helper edit.
- C2 has no such path: `count-c2.py:38-43` and `:124-142` read only through `git show` at the resolved revision.
- `verify.py:52-53` (`dep_same`) guards this only inside `verify.py` runs. The published counting command at `claims.json:19`, run bare, has no such guard.
- **Smallest safe correction:** in `count-c1.py`, refuse with exit 2 when the working-tree bytes of the two helper files differ from `git show REV:<path>`, or execute the helpers from `git show REV:` bytes in a temporary file. C2 needs no change.

### F3. `PROVINCE.md` mixes C1 prose into C2's "own diff"; applied alone, C2 leaves a dangling citation

Impacted axes: calibration and coverage (false provenance, two authorities for one file).

- 2ee3d9f adds one hunk at `@@ -171,0 +172,34 @@`. It contains `### Round-22 catalog dispositions` (C2) and also `### Round-22 narrowly added static ground` (C1's `identify-flutter-build` result, around lines 199-205 at HEAD).
- `verify.py:84` assigns the whole of `PROVINCE.md` to C2-only.
- **Counterexample:** in sandbox 11, `PROVINCE.md:203` cites `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md`, which is **absent** there. So are `evidence/c1/identify-godot.evidence.json` and `corpus/lessons/round-22.md`. If C2 is admitted and C1 rejected, the lane would assert an unbacked C1 result under C2.
- Sandbox 12 shows C2 does not need that section: it still counts 14/14, exit 0.
- Claims list `PROVINCE.md` only under C2's touches (`claims.json:33`), never under C1's.
- **Smallest safe correction:** attribute the static-ground section to C1. In `verify.py`, apply to the C2 partition only the `### Round-22 catalog dispositions` section; apply the static-ground section with C1, or move it out of `PROVINCE.md`. Record `PROVINCE.md` (that section) as a C1 surface in the LOG correction.

A smaller, related point: in sandbox 9, the S051–S053 `used-by` cells in `SOURCES.md` cite `corpus/lessons/round-22.md`, which is absent in both partitions. That file is modified but uncommitted in the lane (`git status`: ` M corpus/lessons/round-22.md`). It is a shared, unpartitioned surface. It does not affect any count.

### F4. The SCORECARD separability claim has no retained record

Impacted axis: calibration (premature saturation).

- `SCORECARD.md:2742-2744` says `verify.py` "applies each claim's data diff alone onto B … and records both counters".
- Neither the tree at HEAD nor the working tree contains `verify/separability.json` or `verify/summary.json`. `git log --all -- .ufo/waves/round-22/verify/separability.json` is empty. `verify/` holds only `before-c1/c2`, `red-C1/C2`, `capture-probes` and an untracked `frida-unsupported-env.json`.
- The retained `before-*` and `red-*` records were not produced by `verify.py` either. Their argv invoke the counters and fixtures directly from the lane's `tools/` path. `verify.py` would have run copies pinned in a `kaidoku-r22-pinned-tools-*` temporary directory.
- The matrix in rows 9–13 above is this seat's author-side evidence. It supports the counted-outcome separation, with SOURCES attributed to C1. It does not substitute for the producer record SCORECARD cites.
- **Smallest safe correction:** run `verify.py --root <LANE> --rev <REV> --out .ufo/waves/round-22/verify/<new-dir>` once the integration is final, and retain `separability.json`. Until then, change the SCORECARD wording to planned/unretained.

### F5. The `verify.py` separability predicate checks counts only

Impacted axis: calibration. This is hardening, not a current failure.

- `verify.py:102` passes when the cross-cells count 0. It does not check that each counter's full output is unchanged from B when the other claim's diff is applied.
- A coupling that changes `catalog_zero_count`, `per_verb` or `foreign_rows` without moving the headline count would pass. `foreign_rows` alone flips C2's exit code (`count-c2.py:174`).
- Current evidence already passes the stronger check: `= B output` is True in every cross cell of rows 9–13.
- **Smallest safe correction:** for the cross cells, add the assertion "output minus `rev` equals the B output". This is a one-line change to the `separation` expression.

### F6. The counters changed after the freeze, under the same mutable path the claims name

Impacted axis: calibration. This is a tradeoff for the canonical judge, not something I resolve here.

- `claims.json:19` and `:29` name `tools/count-c{1,2}.py`. 2ee3d9f rewrote both after `75f04a4` (`count-c1.py` +45/−3 versus `frozen/`; `count-c2.py`: probe-alias guard at `:104` plus selftest).
- The frozen counters violate their own frozen falsifiers. In the retained `verify/red-C1.json` and `verify/red-C2.json`:
  - case `missing_source` gives exit 0, count 6 (falsifier 4 of `claims.json:21`);
  - case `probe_alias` gives exit 0, count 14 (falsifier 2 of `claims.json:32`).
- At HEAD, frozen and current counters measure the same values (rows 5–6 versus rows 2 and 4). The edits tightened the checks without moving the outcome.
- **Smallest safe correction:** report both frozen and current measurements at the final revision next to each other, and state the edit as a post-freeze tightening. Admissibility belongs to the judge.

### F7. Shared control oracle and constants (low severity)

Impacted axis: calibration.

- Both counters' `--selftest` load the same `counter-fixtures.py` (`count-c1.py:99-100`, `count-c2.py:160-163`), so a defect in `run()` at `counter-fixtures.py:110-134` would falsely green both claims.
- Fixture dependencies are copied from the working tree, not REV (`counter-fixtures.py:118-119`).
- No fixture case tests insensitivity across claims. For example, there is no case with C2 dispositions plus a T2 mention in a knowledge entry that checks C1 is unchanged.
- T1 and T2 are triplicated across `claims.json`, the counters and the fixtures. They are currently identical (row 8).
- **Smallest safe correction:** add one cross-claim case per claim, or rely on the corrected F4/F5 matrix as the single separability authority. Read fixture dependencies through `git show REV:`.

## What survived falsification

- The C2 counter's read set really is limited to `PROVINCE.md` plus receipts at REV (`count-c2.py:124-142`).
- T1 and T2 are disjoint.
- In every cross cell, the C1-attributed diff left C2's full output identical to B, and the C2 diff left C1's full output identical to B.
- C1 reaches 1 without any C2 path (sandbox 9); C2 reaches 14 without any C1 path (sandboxes 11 and 12).
- Counted-outcome separability therefore holds once `corpus/SOURCES.md` is attributed to C1.

## Not established

- Whether `verify.py` itself, run end to end, exits 0. It was not run by this seat (no out-dir write is permitted in the lane).
- Admission: this review is author-side only.

## Tooling

None installed or updated. The REA CLI was not invoked.

## Follow-up (2026-10-21, source-only review of the narrow fix requested by KaidokuR22R)

Scope: uncommitted working-tree versions of `verify.py`, `tools/count-c1.py`, `tools/count-c2.py` and `tools/counter-fixtures.py`, compared with HEAD `2ee3d9f`. As instructed, nothing was run: no counter, selftest, fixture or verify call. The only commands were read-only `git diff`/`git status`, `ls` and `rg`. Line numbers refer to the current working-tree files.

### What the fix resolves

- **F3 (`PROVINCE.md` mixing), resolved in source.** `verify.py:98-115` now builds `PROVINCE.md` in each sandbox from the B text plus one section only:
  - C1-only gets `### Round-22 narrowly added static ground` (`verify.py:112`) and has `PROVINCE.md` in `c1paths` (`:98`).
  - C2-only gets `### Round-22 catalog dispositions` alone.
  - The dangling citation is gone: the static section, which cites `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md`, now lands only where that file is present.
  - `PROVINCE.md` is unchanged from HEAD in the working tree, and its section order (`173` dispositions, then `200` static, then end of file) matches the split's assumptions.
- **F5 (count-only predicate), resolved in source.** `verify.py:125-130` compares each cross cell's full counter output, minus `rev`, against the counter's own output at B, and checks the cross-cell exits (C1-only/c2 = 1, C2-only/c1 = 1, C2-only/c2 = 0).
- **F2 (worktree dependence), resolved in source.** `count-c1.py:38-52` (`revision_helpers`) writes both helper files from `git show <rev>:<path>` into a temporary directory and loads round-21, and through it round-20, from there. No helper code is read from the working tree. The fixture `helper_drift` (`counter-fixtures.py:84`, `:147-148`) replaces the worktree helper with code that raises, and expects count 6 and exit 0. That is the right falsifier for my worktree probe above.
- **Git environment.** `count-c1.py:166-170`, the `count-c2.py` `main()` and `verify.py:21-24` delete inherited `GIT_*` variables and set `GIT_NO_REPLACE_OBJECTS=1`. The new fixtures `git_dir_control` and `replace_ref_control` exercise both claims, and the replace control drops the variable from the child environment, so the counter must set it itself. Correct shape.
- **F1 (read set).** Frozen `claims.json:35` stays unchanged, which is correct. The resolution depends on the promised LOG/SCORECARD correction that allocates `corpus/SOURCES.md`, the retained catalog and the static `PROVINCE.md` section to C1. **That correction is not in the tree yet.** Until it lands, F1 stays open as a record defect, even though `verify.py:98` now partitions correctly.

### Residuals: narrow, none blocking, each with a one-line correction

1. **Changes to `PROVINCE.md` outside the two sections go unattributed without any signal.** The sandboxes are rebuilt from B plus one section (`verify.py:100-112`). Any other final-revision edit to `PROVINCE.md` would be dropped from both partitions, so separability would pass without testing it. Likewise, `static` runs to end of file (`:103`), so a section appended after it would silently be attributed to C1.
   - **Correction:** add a check that `base_province + '\n' + '### Round-22 catalog dispositions' + dispositions + '### Round-22 narrowly added static ground' + static == final_province`, recorded in `checks`. This is byte-exact for HEAD's single appended hunk.
2. **`corpus/SOURCES.md` is assigned to C1 as a whole file** (`verify.py:98`). This is correct today: the working tree adds S054 and S055 on top of S051–S053, and all five are C1 rows. A future C2-attributed row would be credited to C1 without notice.
   - **Correction:** in the LOG correction, state that every new row from S051 onward is C1, or check that each new row's `used-by` cites only C1 paths.
3. **The C1-only/c1 exit is not asserted.** `verify.py:127-130` checks C1-only/c1 `count >= 1` but not its exit.
   - **Correction:** also assert `exit == (0 if count == 6 else 1)`.
4. **Failures crash the producer instead of being recorded.**
   - `verify.py:102-103` raises `IndexError` if either heading is missing.
   - `:122` `json.loads` is uncaught.
   - `without_rev(baseline_data[claim])` fails if a `before-*` run returned non-JSON (`record` returns `None`).
   - Each of these ends in a nonzero traceback with no `summary.json`. That is visible rather than a false pass, but it is unretained.
   - **Correction:** wrap these and record a failed `separability` check.
5. **A symbolic revision is resolved twice.** `count-c1.py:84` passes the raw `rev` to `revision_helpers` (via `git show`) and separately to `r21._measure`, which resolves it again. A moving ref could pair helper bytes from one commit with data from another. `verify.py` always passes resolved SHAs, so the final suite is unaffected; only a bare CLI call with a symbolic ref is exposed.
   - **Correction:** resolve once at the top of `measure` and pass the SHA to both.
6. **Fixture dependencies still come from the working tree** (`counter-fixtures.py`, the `put(root, dependency, (Path(source)/dependency).read_text())` loop). This is my earlier F7 residual and is unchanged. It is low severity, because `verify.py:94-95` (`selftest-source-equal-revision-at-check`) and `:60` (`dep_same`) cover the final run.

### Dependency to note for the final suite (no claim of outcome)

C1-only's `count >= 1` now relies on `bind_cli` (`count-c1.py:55-81`), which accepts only a full CLI envelope (`ok`/`data`/`meta.command`). The extracted `identify-godot.evidence.json` has no `ok` member, so it will be `unsupported` (code 2). The count must therefore come from the cited `identify-godot.envelope.json`, or from the new Saber envelopes for S055. Whether that holds is for the L1 final suite to measure; I did not run it.

### Updated status

Of my findings, F2, F3 and F5 are fixed in source and await the final suite's retained `separability.json` (F4). F1 is pending the LOG/SCORECARD correction. F6 is pending disclosure, and `verify.py` now records `original-after-*` from the frozen counters at REV (`verify.py:71-73`), which supports that disclosure. F7 is partly addressed: the GIT and replace controls were added, but fixture dependencies are still read from the working tree.
