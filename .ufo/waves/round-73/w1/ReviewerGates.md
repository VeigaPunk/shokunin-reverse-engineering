# ReviewerGates — round-73 instrument false-green review

Axes: coverage (non-vacuous kernel witness), calibration (record predicates and complete mutant census), operability (controls exercising the intended route); security is a no-regression constraint. Recommendation only; no admission or integration performed.

## Findings, highest severity first

### High — c3_no_case goes green without ever executing the case-deleted route

`tools/round-73/controls.py:200-209` passes an absolute scratch filename as `--tool` to a battery that only reads `git show <rev>:<tool>` (`mutation-check.py:181-186,196`). That object does not exist, so any scratch file, even one that raises immediately, yields exit 2 and an `unevaluable` string and satisfies the control. Neither its pristine selftest nor its mutant cases run. This contradicts both the control docstring's pristine-selftest-red claim (`controls.py:25-28`) and the frozen plan's three-survivor expectation (`plans/round-73-claims.md:129-132`). Actual CLI counterexample: exit 2, `git show ... failed rc=128`, control predicate true, no fixture execution.

Proposed fix: provide a deliberately supported scratch-blob battery entrypoint or directly run the case-deleted target's pristine and mutant selftests with its sibling modules. Bind the control to the frozen expected experiment, verify all three deletions, and require the specific observed selftest/mutant result; never accept an arbitrary acquisition failure.

### High — D1 accepts the wrong hash without a correction supplying the right hash

`record-audit.py:121-128` only requires the wrong token to reappear after the correction marker. It never requires the receipt's correct value in that block, nor a statement superseding the old value. A synthetic section saying `target sha 01234567` and `**Correction (round 73):** old token 01234567 remains correct.` passes while the actual digest is absent. Removing every `target sha` mention also makes `wrong` empty and passes given the receipt/blob check. The docstring promises a correction naming both values (`:130-131`), which is not implemented.

Proposed fix: require the affected record statement to exist and either match the measured hash or have a narrowly parsed correction mapping that exact old token to the re-derived correct digest (and check every record surface the atom claims to repair).

### High — mutation receipt validation accepts omitted mutants and inconsistent zero-survivor claims

`mutation-check.py:292-309` requires only a nonempty list, not the exact unique IDs of `PATCH_SETS[patch_set]`; it only compares the `survivors` list to whatever rows remain. It never checks `survivor_count`, `expected_survivors`, top-level `ok`, named-case membership, or agreement between the verdict and failed cases. A receipt with patch set r73, one invented `killed` row, no failed case, `survivors: []`, and `survivor_count: 99` validates with exit 0. Thus removing a real surviving mutant row and updating `survivors` can be accepted.

Important distinction: the actual producer `check()` iterates every frozen patch tuple (`:233-252`) and raises on a missing/ambiguous site; its derived count (`:253-257,272`) does not silently omit a mutant. The defect is receipt validation, not evidence that a normal producer run skipped rows.

Proposed fix: require a recognized patch set, exactly its unique mutant IDs, valid verdict vocabulary, rc/failed/expected-case consistency, and recompute all survivor/kill/count/overall verdict fields plus pin and pristine requirements.

### High — record audit can report seven green atoms with missing evidence

`record-audit.py:247,254-259` records missing population as metadata, not failure. `atom_before_pointer` strips round identity (`:211-216`), de-duplicates references and resolves each suffix first in round 72 and then round 73. A round-73 pointer to a missing receipt therefore passes on a same-named round-72 receipt. It also does not enforce one before receipt per round or reconcile the report and SCORECARD as routed defect 7 requires (`corpus/lessons/round-72-verifier-spotcheck.md:123`).

The isolated synthetic audit returns `mismatch_count: 0`, seven green rows, `population.present: false`, with no round-73 before receipt. D2/D3/D4 have their required landing receipt objects in this counterexample: this is not a claim that all receipts may be absent.

Proposed fix: fail closed on absent population, retain the full round-qualified path, require each round's own required pointer and revision, and compare the report/SCORECARD pointer pair rather than testing a cross-round union.

### High security risk on a failed genuine environment test — A12 serializes environment values

`seam-probe.py:533-540` returns `values: env`, and `:599-601,636-637` nests that object in the arm receipt. If the genuine child inherits dirty caller environment, precisely the regression this probe is meant to detect, its truthful shim dump contains those values and the JSON output can carry them into a filed receipt. This is a source-established conditional disclosure path, not a claim that this review captured host secrets. No live environment dump was produced.

Proposed fix: remove raw `values` from serialized observations; retain key names and canary presence only, perform necessary containment checks in memory, and keep raw evidence exclusively in scratch with guaranteed cleanup.

### Medium — D5 confuses repeated/single field names with the required provenance trio

`record-audit.py:192-197` treats any single opening r72 provenance field as enough; r73 checks a count of three matches, not the set of field names. The correction alternative likewise counts matches without checking field identity (`:193-194`). Counterexample: r72 contains only `source:`, r73 contains three `source:` lines, and D5 is true; `verified-at` and `recheck` remain absent.

Proposed fix: require exactly the distinct set `{source, verified-at, recheck}`, with nonempty values, in the designated opening/correction block for each entry. Add duplicate-field and single-field negative cases.

### Medium — record receipt validation does not bind the seven-atom population

`record-audit.py:273-289` accepts any nonempty all-green list with matching summary fields. A single invented atom with a detail validates with exit 0. The lying-receipt control exercises count disagreement, but not deletion/substitution of an atom.

Proposed fix: require exactly the seven unique frozen atom IDs and expected schema/population before deriving mismatches; retain summary agreement checks.

## Requested negative checks that are already sound

- `seam-probe.py:475-479`: genuine rc 0 with no kernel samples cannot pass; both git and readelf names are required. Counterexample exercise returns `ok: false`.
- `seam-probe.py:483-485`: empty forged kernel samples cannot pass. Exercise returns `ok: false`.
- Forged fixture really inherits the caller environment: `f_env = dict(os.environ)` plus canary (`:615-616`), passed to producers (`:621-623`), whose child call explicitly uses `env=None` (`:510-512`). This is source inspection, not a live host-environment observation.
- A12 intentionally permits one dirty forged kernel child (`:483-485`; explicit selftest `:1188-1190`). The review's one-child fixture passes. The frozen claim only says the forged kernel samples read dirty, so this is a coverage limitation, not separately classified as a contract violation.
- Controls aggregate is strict: `controls.py:211` requires every arm's `met is True`; `:221` converts it to exit status. There is no aggregate truthiness bug. Its inputs can still be false greens as above.

## Six-control disposition

| Arm | Review result |
|---|---|
| c1_no_kernel_channel | Invokes the old eleven-arm probe and checks target/no-A12/rc; genuinely skips adding A12 (`:110-124`). Not rerun here. |
| c1_blind_witness | Pure-function blind/positive/no-lie fixtures check strict booleans (`:126-145`); matching A12 cases exercised directly. |
| c2_do_nothing | Audits base and requires exact six mismatch IDs (`:147-158`); not a record repair. Not rerun here. |
| c2_lying_receipt | Runs validator against summary/count inconsistency (`:160-171`); valid narrow negative control but not a population-deletion detector. |
| c3_base_world | Runs r73base on round-72 target and checks all three named survivors (`:173-185`); genuine intended baseline path by inspection. Not rerun here. |
| c3_no_case | Invalid-target acquisition refusal, not the claimed experiment; demonstrated above. |

## Evidence and verification gaps

Receipt: `.ufo/waves/round-73/w1/ReviewerGates/counterexamples.json`; reproducible driver: `.ufo/waves/round-73/w1/ReviewerGates/review-probes.py`. Executed once with `python3 -I -B`, explicit seat TMPDIR and EXIT cleanup. Result: synthetic audit mismatches 0; partial-record validation rc 0; partial/inconsistent mutation validation rc 0; actual no-case battery rc 2 with control predicate true; both empty-channel A12 cases false. Source SHA-256 values are recorded in the receipt. No tool installations, source changes, git writes, external runtime, or environment-value capture.

Read-only actual diff against declaration was checked: only the two mutation patch-site changes appeared among these four files at observation time. Those patch-site changes do not address the validator omissions; all findings describe the observed working sources, not an assumed landing revision.

LSP device is unavailable (`read xd://lsp`: No such tool), so definitions/callers were inspected with targeted reads and literal search; no semantic-reference/diagnostic completeness is claimed. Full probe, mutation battery and six-arm controls were not run. Review does not decide runtime identity, rerouting, saturation or resume continuity: no such behavior is changed in these scoped instruments. No actionable claim is made about those out-of-scope surfaces.

Report: `.ufo/waves/round-73/w1/ReviewerGates/ReviewerGates.md`
