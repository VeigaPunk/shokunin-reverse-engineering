# R39W2C2Mutants — mutation probe of `tools/round-39/c2-counter.py`

**Verdict: DEFECTS FOUND** — no mutant flips the C2 verdict at REV (met 20/20 under all 29 mutants), but 9 non-equivalent mutants survive both detectors, so `--selftest` (27 cases) has real coverage gaps in exactly the clauses the predicate leans on: byte-identical regeneration, first-add ordering, and freeze descent.

- Seat: R39W2C2Mutants (leaf; no subagents dispatched, no `async` jobs started — two long selftest batches were auto-backgrounded by the harness at ~60 s and delivered unprompted; never polled).
- Attacked artifact: frozen `tools/round-39/c2-counter.py` at freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`, scored at REV `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` (author score `.ufo/waves/round-39/l1/scores/c2-at-6fdaf4f1.json`: met, 20/20).
- Claim under test (frozen `plans/round-39-claims.md`, R39-C2): the counter's `met_target` = matched 20/20 ∧ every binding true, with `--selftest` (27 cases) as the stated self-test.

## 1. Method

Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39W2C2Mutants` (removed at end; cited files copied to `w2/artifacts/R39W2C2Mutants/`). `TMPDIR=$S`, `HYAKU_SCRATCH=/fast/scratch/hyaku` per lane bounds.

1. **Copy, never touch the lane.** `cp tools/round-39/c2-counter.py $S/pristine.py`; sha256 `775766d86de0f1adbb2b7836664bc5641f92c0493bf0aa012b176ce03e7f0e41`. 29 mutant copies (`m01.py`…`m29.py`), each = pristine + **one** minimal edit, applied with in-place string replacement; every edit verified in the tool output. The lane file was never written.
2. **Baseline (admissibility).**
   - `python3 pristine.py --selftest` → exit 0, `{"cases": 27, "pass": 27, "fail": 0}` (8.0 s).
   - `git clone -q --shared <lane> $S/clone`; `python3 pristine.py --root $S/clone --rev 6fdaf4f1… --freeze 8fcda41c…` → exit 0, `matched 20, n 20, met_target true, bindings_false []` (1.1 s) — identical to the author's score.
3. **Detectors per mutant.** D1 = `--selftest` (exit ≠ 0 ⇒ killed). D2 = verdict run `python3 <mutant>.py --root $S/clone --rev 6fdaf4f162aff156fcef0e52998a5469c64fd6f0 --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --json-out $S/<m>.v.json` (exit ≠ 0 or payload ≠ baseline ⇒ killed). Every mutant ran both arms.
4. **Survivor triage.** Each survivor got a differential fixture (scratch git repos, reusing the counter's own `STUB_GEN`/`STUB_INTERP` and green-table helpers via import): a repo where pristine and the mutant disagree proves the survivor is a *missing test*, not an unkillable mutant. Driver: `drive.py` (artifact), output `driver_output.txt`.

No tools were installed or upgraded (none needed; `python3` + `git` present). No pacman transactions. No VCS mutation anywhere: lane git usage was read-only (`show`/`cat-file`/`rev-parse`/`merge-base`/`log`/`ls-tree` inside the counter); the only clones/commits are inside $S fixture repos and the shared clone.

## 2. Mutant table

`selftest`/`verdict` = exit codes (0 = pass/met). "S" = survived both detectors.

| id | target binding | mutation (one edit) | selftest | verdict | class |
|----|----------------|---------------------|----------|---------|-------|
| m01 | `seed_matches_freeze` | drop `.lower()` on the manifest seed | 0 | 0 | **S — genuine (false-negative direction)** |
| m02 | `seed_matches_freeze` | compare `rev` instead of `freeze` | 1 | 1 | killed |
| m03 | `regenerated_seed_matches_freeze` | compare regenerated seed to *declared* seed | 0 | 0 | S — masked (equivalent for the target) |
| m04 | `regen_ok` | drop `r.get('label') == c.get('label')` conjunct | 0 | 0 | **S — genuine** |
| m05 | `regen_ok` | drop `r.get('arm') == c.get('arm')` conjunct | 0 | 0 | **S — genuine** |
| m06 | `regen_ok` | `regen_sha == msha` → `regen_sha != ''` | 0 | 0 | **S — genuine (highest severity)** |
| m29 | `carriers_regenerated` | `all` → `any` | 0 | 0 | **S — genuine** |
| m07 | `commit_ok` | drop `committed_sha == msha` | 1 | 0 | killed |
| m08 | `carriers_committed` | `all` → `any` | 1 | 0 | killed |
| m09 | `digest_ok` | `subject_sha(eo) == msha and bool(msha)` → `is not None` | 1 | 0 | killed |
| m10 | `envelopes_valid` | drop `digest_ok` from the all() | 1 | 0 | killed |
| m11 | `manifest_after_freeze` | drop `ma != freeze` | 1 | 0 | killed |
| m12 | `manifest_after_freeze` | drop `is_ancestor(freeze, ma)` | 0 | 0 | **S — genuine** |
| m13 | `manifest_before_envelopes` | `all` → `any` | 0 | 0 | **S — genuine** |
| m14 | `manifest_before_envelopes` | ancestors reversed (`is_ancestor(fa, ma)`) | 1 | 0 | killed |
| m15 | `triage_table_identical` | compare marker line only | 1 | 0 | killed |
| m16 | `triage_table_identical` | drop both `is not None` guards | 0 | 0 | S — equivalent for the target |
| m17 | label comparison | `row['label'] == row['expected_label']` → `== row['class']` | 1 | 1 | killed (both; real verdict would drop to matched 14) |
| m18 | label comparison | `class_match` = presence-only | 1 | 0 | killed |
| m19 | label comparison | `expected_label` returns `c.get('class')` | 1 | 1 | killed (both; matched 14) |
| m20 | `classes_two_each` | `per.get(k) == 2` → `>= 2` | 1 | 0 | killed |
| m21 | `classes_two_each` | `per.get(k)` → `per.get(k, 2)` | 0 | 0 | S — masked |
| m22 | met_target consistency | `consistent = met == recomputed` → `= True` | 0 | 0 | S — equivalent (vacuous guard) |
| m23 | met_target consistency | `if not consistent:` → `if False:` | 0 | 0 | S — equivalent (vacuous guard) |
| m24 | `met` | drop `bindings_ok` conjunct | 1 | 0 | killed (via the consistency guard: 11 cases want 1, got 2) |
| m25 | frozen-path check | `FROZEN` drops `COUNTER` | 1 | 0 | killed |
| m26 | frozen-path check | `if changed:` → `if False:` | 1 | 0 | killed |
| m27 | freeze-ancestor precheck | `if not is_ancestor(freeze, rev):` → `if False:` | 0 | 0 | **S — genuine (low)** |
| m28 | `first_add` | drop `--reverse` (latest add wins) | 0 | 0 | **S — genuine** |

Tally: 29 mutants; 15 killed by `--selftest` (m02 m07 m08 m09 m10 m11 m14 m15 m17 m18 m19 m20 m24 m25 m26; m17/m19 would also flip the real verdict to matched 14/20, exit 1); **14 survived both detectors**. All 14 survivors' verdict stdout is byte-identical to baseline and their `--json-out` payload differs from baseline only in `argv` — no mutant produces a wrong `met_target` on this lane at this REV.

## 3. Killed mutants — killing selftest cases (evidence)

- m02: `green`, `generator object with matching sha`, `envelope path omitted…`, `full CLI envelope…`, `lane-root-relative…` — want 0 got 1.
- m07/m08: `carrier not regenerable` — binding `carriers_committed` not false (got True); want 1 got 0.
- m09/m10: `subject digest mismatch` — binding `envelopes_valid` not false (got True); want 1 got 0.
- m11: `manifest before freeze` — binding `manifest_after_freeze` not false (got True).
- m14: `envelope before manifest` — binding not false; want 1 got 0.
- m15: `table edited after freeze` — binding `triage_table_identical` not false; want 1 got 0.
- m17/m19: green-family cases — want 0 got 1.
- m18: `catch-all table`, `unclassified` — want 1 got 0.
- m20: `3 carriers in one class` — binding `classes_two_each` not false.
- m24: 11 red cases — want 1 got 2 (`met_target_inconsistent`): the consistency guard *does* have teeth against `met` mutations.
- m25: `counter edited after freeze` — want 2 got 0.
- m26: the four `* edited after freeze` cases — want 2 got 0.

## 4. Survivors — 9 genuine missing tests (differential-fixture proof)

Each row: fixture repo where pristine and the mutant disagree (`driver_output.txt` has the full run; `bindings_false` shown for the losing side).

| id | missing test | fixture | pristine | mutant |
|----|--------------|---------|----------|--------|
| m06 | **byte-identical regeneration is never the deciding binding.** `regen_sha == msha` is untested: the only regeneration fixture (`carrier not regenerable`) corrupts the *committed file*, which trips `carriers_committed` instead. A carrier whose committed bytes match the manifest sha but diverge from regeneration passes. | H01 body committed = regen body + `X`; manifest sha = sha(committed) | exit 1, `carriers_regenerated` false | exit 0, met |
| m29 | `carriers_regenerated` all→any: one non-regenerable carrier among many passes. Same fixture as m06 (mixed: H01 divergent, H02–H06 identical) kills both. | as m06 | exit 1 | exit 0, met |
| m04 | regenerated **label** drift vs the committed entry is invisible while the interpreter agrees with the committed entry (predicate says the interpreter must match "the label its frozen generator assigned" — that clause rests solely on this conjunct). | H05 (`dep-missing-be`) committed label `clean`, regen label `dep-missing-be`, stub_class `clean` | exit 1, `carriers_regenerated` false | exit 0, met |
| m05 | regenerated **arm** drift, same shape. | H01 committed arm `before`, regen arm `after` | exit 1 | exit 0, met |
| m12 | the "descending from the freeze" conjunct of `manifest_after_freeze` is untested: every fixture has the manifest either equal to the freeze commit (caught by `ma != freeze`) or a linear descendant. A manifest first-added on a sibling branch merged into REV passes. | plumbing: base → freeze; side branch off base with SKILL+claim data (`ma`); rev = commit-tree(parents freeze, ma) | exit 1, `manifest_after_freeze` false | exit 0, met |
| m13 | `manifest_before_envelopes` all→any: a *mixed* ordering (some envelopes before the manifest, some after) passes; the fixture only has all-before. | H01 files → manifest commit → H02 files → rev | exit 1, `manifest_before_envelopes` false | exit 0, met |
| m28 | `first_add` without `--reverse` returns the *latest* add; no fixture re-adds a file. Live-lane check: all 101 held-out paths at REV have exactly 1 add-event, so the mutant is currently harmless here — but the detector would not notice a re-add. | H01 files added → manifest → H01 deleted → H01 re-added | exit 1, `manifest_before_envelopes` false | exit 0, met |
| m27 | the `freeze_not_ancestor_of_rev` precheck never fires in any fixture; disabled, a non-descending REV is measured (honest-miss exit 1) instead of refused (exit 2). Never reaches a wrong `met` (the frozen-path check still blocks orphan roots that add frozen paths). | orphan-branch rev | exit 2, unevaluable | exit 1 |
| m01 | no fixture exercises seed case-insensitivity; dropping `.lower()` makes the counter *stricter* (rejects an uppercase-seeded manifest) — a false-negative direction, so it cannot cause a false pass, but the green path is untested for it. | manifest seed = freeze.upper() | exit 0, met | exit 1, `seed_matches_freeze` false |

## 5. Survivors — 5 equivalent/masked (no test can or needs to kill; proofs)

- **m22 / m23 (consistency guard):** `met = bool(matched == N and bindings_ok)` and `recomputed = bool(matched == N and all(v is True for k, v in b.items()))` are the *same expression* over the same dict (`bindings_ok = all(v is True for v in b.values())`), so `consistent` is True by construction and the `met_target_inconsistent` raise is unreachable. The mutants are equivalent. Corollary finding: `met_target_consistent: true` in every receipt is guaranteed, not evidence; and the selftest's "consistency detector exercised directly" block tests an inline reimplementation of the formula, not `measure()`'s wiring. The guard is not dead weight overall — m24 shows it kills `met` mutations — but its own wiring is untestable as written. Fix (test-side or counter-side, owner's call): make `recomputed` an independently re-walked binding set, or drop the guard.
- **m03:** `met` requires `seed_matches_freeze` (declared seed == freeze); under that, "regenerated seed == declared seed" ⟺ "regenerated seed == freeze", so the binding value can differ but `met_target` cannot. Masked by construction (the counter itself invokes the generator with `--seed freeze`).
- **m16:** differs from pristine only when the table is absent at *both* REV and freeze (`None == None` → True); there `triage_table_present` is false, so `met` is false either way.
- **m21:** `per.get(k, 2) == 2` fails only for a declared class with zero carriers; then N = 2·(|classes|−1) ≠ 2·|classes|, so `n_equals_twice_classes` is false and `met` is false regardless. Masked by a sibling binding.

## 6. Suggested missing fixtures (test-side only; I changed nothing)

1. Regeneration diverges while the manifest sha matches the committed body (kills m06 + m29; variants with label/arm drift kill m04/m05). This is the predicate's "every carrier regenerates byte-identically" clause — today it is only ever exercised through `carriers_committed`.
2. Regenerated label/arm differs from the committed entry while the interpreter agrees with the committed entry (m04, m05).
3. Manifest first-added on a non-descendant commit, via merge plumbing (m12).
4. Mixed envelope ordering around the manifest commit (m13).
5. Held-out file added → deleted → re-added (m28).
6. REV not descending from the freeze, expecting exit 2 `freeze_not_ancestor_of_rev` (m27).
7. Green case with an uppercase seed (m01).
8. Either make `recomputed` independent or drop the consistency guard (m22/m23 — untestable as written).

## 7. Bounds, restoration, artifacts

- **Restoration evidence:** the lane file was never modified; sha256 of `tools/round-39/c2-counter.py` before (`775766d86de0f1adbb2b7836664bc5641f92c0493bf0aa012b176ce03e7f0e41`) and after the full campaign: identical. All mutants lived and died in $S. No frozen predicate, counter, carrier, oracle, or table changed; no VCS mutation; no writes outside this report + `w2/artifacts/R39W2C2Mutants/`.
- **Scratch:** `rm -rf -- $S` executed at the end (trap equivalent done explicitly); only $S and the counter's own self-cleaning `c2-counter.*`/`c2-case.*` dirs under `$HYAKU_SCRATCH/kaidoku-r39` were used; no `find`/`du` outside $S.
- **Artifacts** (`w2/artifacts/R39W2C2Mutants/`, 78 files): `pristine.py`, `baseline.json/.stdout/.stderr`, `drive.py`, `driver_output.txt`, `mutants.tsv` (machine table), per-mutant `m*.st.out` (selftest) and `m*.v.out` (verdict stdout) for all 29, and the 14 survivors' `m*.v.json` receipts.

## 8. Limits

- Hand-picked mutant set (29) over the ten tasked targets; not an exhaustive operator sweep (no automated AOR/ROL over the whole file).
- Equivalent/masked classifications (m03, m16, m21, m22, m23) are proofs by reasoning over the code — by construction no fixture can demonstrate them, which is the point of the classification.
- The verdict arm ran each mutant once at the single frozen (REV, FREEZE) pair; no other revisions probed. m28's live-lane harmlessness was checked for the 101 held-out paths at REV only.
- [INFERENCE] Severity labels (high/medium/low) are my judgment about exploit difficulty, not measured attack cost.
