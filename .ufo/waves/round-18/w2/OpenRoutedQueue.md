PARTIAL

# OpenRoutedQueue: spot-check routes from r12–r17 still open at REV (round 18, wave 2, author-side connector)

- REV: `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. Baseline: `9011581d84527ba34c675f9cf912e54d2e72d470`.
- Every anchor below is a `git show REV:path` line.
- Labels: **[OBS]** means bytes or command output I observed. **[INF]** means inference.
- This report is read-only. I wrote only this file. My scratch space was `/tmp/kr18orq` (removed).
- I ran no REA, no Ghidra and no carrier.
- I ran three lane tools against Git objects: `routed-defects.py`, `invocation-audit.py` and `temporal-sweep.py`. Their selftests use their own mkdtemp repos.
- Tool installs or updates: none.

Axes, named before measuring:

- **Calibration:** the open list matches the bytes.
- **Operability:** each open item has a revision-scoped check.
- **Depth:** the routed target is fixed, not a nearby note.

## Verdict

`corpus/lessons/round-18.md:73-75` ("## Open") is true but incomplete.

- **Both r12 items it names are still open [OBS].**
- **The list leaves out these items:**
  - One more lane-routed r12 item, the axis add/withdraw record. It has no discharge record [OBS].
  - Two minor r17 sub-items that no correction names.
  - The R16-INVOCATION defect class, which has re-opened inside round 18's own registry rows: 9/26 rows are `unlabelled_variant` at REV, measured before the verification pass [OBS].
- **All six R17 instances are closed** by the lane counter at REV: 0 open at REV, 6 at baseline [OBS].
- **That counter's own selftest is red at REV [OBS].** See "Adjacent finding" below.

## Queue at REV: every item routed by `corpus/lessons/round-1{2..7}-verifier-spotcheck.md`

The `C#` references point to commands in the last section.

| Item (routing anchor) | Status at REV | Evidence |
|---|---|---|
| r12-a: create `corpus/SOURCES.md` (`round-12-verifier-spotcheck.md:17`) | closed | Added in `5ac7860` (C2) |
| r12-b: give the C1 entry an `S###` source row (`:17`) | **OPEN** [OBS], carried by the lesson | The entry has no `S###` (C3, exit 1). SOURCES never names it (C4, exit 1) |
| r12-c: disclose the unpaired custody legs in the entry (`:17`) | **OPEN** [OBS], carried by the lesson | C5 exit 1. The entry history is `4072ebb` only (C6) |
| r12-d: "operability improved (outside the lane's owned axes — debt: record the axis add or withdraw it next round)" (`:17`) | **OPEN — ADD** [OBS absence] | See A1 below |
| r13 | nothing routed (C7, exit 1) | The S017/S018 quote defects were fixed in-round (round-13 lesson errata) |
| r14-1: advisory evidence correction (`round-14-verifier-spotcheck.md:171`) | closed | `corpus/lessons/round-14.md:144`; `LOG.md:1847` (C8, C9) |
| r14-2: manual-only input boundary (`:172`) | closed | `corpus/QUALITY.md:27` (#17) (C10) |
| r15-1: recheck uses `-I` (`round-15-verifier-spotcheck.md:185`) | closed | `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:83` (C11) |
| r15-2: supplemental baseline is discoverable (`:186`) | closed | `SKILL.md:450` (C12) |
| r15-3: count-command provenance (`:187`) | closed | `.ufo/waves/round-16/controls.json:411` `orig_argv` (C13) |
| r15-4: SHONEN historical wording (`:188`) | closed | `SHONEN.md:10`. The `this round` count is 0 (C14, exit 1) |
| R16-PROVENANCE (`round-16-verifier-spotcheck.md:183`) | closed, no recurrence | temporal-sweep at REV: 4 sites, 4 corrected, 0 unqualified, 0 new (C16) |
| R16-INVOCATION (`:184`) | instance closed; **class RE-OPENED — ADD** | See A2 below |
| R17-PINMAP, -VALIDATE16, -PRODUCER-REV, -SUMS-RUNLOG, -REGISTRY, -S032-DIGEST (`round-17-verifier-spotcheck.md:137-147`) | closed 6/6 | routed-defects at REV: open 0, named 0, substance 0. At baseline: 6/6/6 (C18) |
| R17-SUMS-RUNLOG sub-bullet "…lists 7/8 carriers **and has no final exit line**" (`:142`) | **residue unnamed — ADD (minor)** | See A3 below |
| R17 install record: "say why the official tarball was chosen over pacman" (`:93`, `:149`) | **not discharged — ADD (minor, ownership ambiguous)** | See A4 below |
| Integrator/operator items: r16 "aggregator/integrator should mirror them" (`round-16-verifier-spotcheck.md:181`); r17 template/PROTOCOL item (`round-17-verifier-spotcheck.md:149`) | not lane-owned | Not assessed here |

## Additions

### A1. r12-d: axis record

**[OBS]**

- No `withdraw` appears in `SCORECARD.md`, `LOG.md` or the r13–r18 lessons (C15, exit 1).
- `## Owned axes` still has 3 rows, coverage, depth and calibration (`SCORECARD.md:23-25`). No add was made.
- The r12 verdict `| operability — C3 | … | improved (pending non-author verification) |` stands with no appended withdrawal (`SCORECARD.md:2095`).
- The nearest record is r13's row `| operability (not owned) | … | unchanged |` (`SCORECARD.md:2147`).

**[INF]**

- That r13 row records non-ownership for r13 only. It withdraws nothing, so neither branch of the debt is met.
- w1 scored this item "`[INF]` withdrawn by record" (`.ufo/waves/round-18/w1/ScoutOperatorLessons.md:78`) without citing any withdrawal. The lesson then took over a two-item list.
- The question is live again this round:
  - C2 is declared on `"axis": "operability"` (`.ufo/waves/round-18/claims.json:18`).
  - The dispatched prompt binds lane axes to "coverage + depth + calibration" (fleet `.ufo/prompts/kaidoku-round-18.md:6`).
  - `AXES.md:3-5`: "Every shokunin works its own subset".
- Remedy: one appended SCORECARD line, in either form:
  - add operability to `## Owned axes` with a proxy; or
  - name the `:2095` verdict withdrawn as a lane score.
- The lane chooses which. Severity is low; nothing numeric is gated on it.

### A2. R16-INVOCATION class

**[OBS]**

- `invocation-audit.py` (the lane's registered probe, `SKILL.md:544`) at baseline: 17 rows, 17 `exercised_match`, 0 unlabelled.
- At REV: 26 rows, 17 `exercised_match`, **9 `unlabelled_variant`** (C17). All nine are round-18 rows (`SKILL.md:565,586-593`):
  - `r18-prediction-freeze`
  - `routed-defects`
  - `head-rev-lint`
  - `revpin`
  - `jj-red-before`
  - `swiss-misread`
  - `go-carrier-run-r18`
  - `round18-measure`
  - `round18-structural-controls`
- This is the class QUALITY #18 (`corpus/QUALITY.md:28`) was written for: "future recheck guidance either matches the exercised isolation flags and paths or explicitly names an unexercised variant".

**[OBS] What the verification pass will exercise.** No round-18 `verification.json` exists at REV. `.ufo/waves/round-18/verify.py` plans these argv forms:

- `routed-defects … --strict` (`:178-179`)
- `head-rev-lint … --strict` (`:183-186`)
- `jj-red-before --out` (`:190`)
- `measure.py <rev>` (`:234-235`)
- `controls.py <base> <source>` (`:236`)

It uses the same `PY = ["python3", "-I", "-B"]` as round 17 (`verify.py:36`; r17 `verify.py:35`).

**[INF] Expected residue after the pass.** Those five rows should then match. Four rows still have no argv in a receipt-pattern file:

- `r18-prediction-freeze`
- `revpin`: `verify.py:90` imports it as a module, so no CLI argv is recorded.
- `swiss-misread`
- `go-carrier-run-r18`: its `run-log.txt` is not JSON.

So at least 4 unlabelled rows are expected at delivery, unless they are retained or labelled.

### A3. R17-SUMS-RUNLOG residue

**[OBS]**

- The last line of the pass-1 log at `da64646` is a carrier `end` line. There is no `run-carriers exit=` line.
- The pass-2 log at REV ends `run-carriers exit=0` (C20).
- The corrections at `LOG.md:2160` and `corpus/lessons/round-18.md:54` name only the 7/8 gap. A grep for `final exit|exit line` exits 1 (C19).
- `routed-defects.py` checks the 7/8 fraction only, so it cannot see this residue.

### A4. Install-record reason

**[OBS]** `corpus/lessons/round-17.md:135-141` records the Go 1.27.3 tarball install and "No pacman transaction was run.", but gives no reason. No r17/r18 lesson or SCORECARD line adds one (C21, exit 1).

The route sits in a paragraph headed "Operator/protocol (not lane debt)" (`:149`), but it concerns a lane-authored record (`:93`). Its ownership is therefore ambiguous.

## Adjacent finding: the C1 counter's selftest is red at REV (not a routed item)

**[OBS]**

- The REV blob is identical to the worktree file: `bd6390e6…`, from `git ls-tree` and `git hash-object`.
- `routed-defects.py --selftest` at REV exits **1** (C22).
- The `eb6c266` blob exits 0 with `SELFTEST: CLEAN cases=17` (C23).
- Cause, from the one diff hunk between the two blobs:
  - The L1 amendment at `routed-defects.py:277-283` now requires both `mid_map_sha256_mismatch` and `mid_map_compare_mismatch`.
  - The closed fixture still writes `FINDING = "mid_map_mismatch"` (`:914`) (C24).
- Effects:
  - Both closed-fixture cases fail.
  - Five token-only cases report `extra_open=['R17-PINMAP']`, so per-defect isolation is lost.
  - `corpus/lessons/round-18.md:67` cites "CLEAN 17", which is true at `eb6c266` but false at REV.
- `verify.py:157-159` expects exit 0 from every round-18 tool selftest. `run()` sets `exit_as_expected` (`verify.py:127`), `unexpected_exits` is built from it (`:286`), and the pass returns 1 whenever that list is non-empty (`:294-295`).

**[INF]** The pending verification pass would list `selftest-routed-defects` as unexpected and exit 1, unless the fixture is fixed first. The real-lane result (0 open at REV) is not affected.

## Proposed move (one, bounded): count routed *classes*, not only routed *instances*, before the verification pass

One lane commit, before `verify.py` runs:

1. **Fix the fixture.** Make `routed-defects.py:914` write both finding ids.
   - Red-before is REV: exit 1. Green is `CLEAN cases=17`.
2. **Report a separate class-recurrence leg with C1.** Keep it out of `open_count`, which stays the frozen R17 6→0 metric. Its three numbers at REV:
   - `invocation-audit` `unlabelled_variant` over rows added since baseline: **9**.
   - `temporal-sweep` `new_unqualified_at_rev`: **0**.
   - New registry rows missing `Pinned values` or `Write scope`: **0/9** (awk check below).
   - To discharge the 9: retain the argv of rows that actually ran (gen-predictions, run-carriers, swiss-misread), and label `revpin`'s CLI form "unexercised" (QUALITY #18).
3. **Make `## Open` equal this queue.** Add r12-d, the A3 sub-item and the A4 reason (or discharge each with one appended line).

**Axes**

- **Calibration up:** the Open list and the "CLEAN 17" claim match bytes, and the re-opened class is disclosed.
- **Operability up:** the round's own selftest loop can pass, and r12-d/A3/A4 get revision-scoped checks.
- **No harm** to depth or coverage. C1's declared before/after is untouched because the new leg is a separate number.

**Risks**

- Folding class checks or r12 items into `open_count` would silently change C1's frozen measure (`claims.json` C1). Keep them separate.
- Label-only discharge of A2 is cheap and can become vacuous. Prefer a retained argv wherever the row was really run.
- r12-d is a ruling (add or withdraw). Append it; never rewrite `SCORECARD.md:2095`.
- If `PY` or the receipt basenames change before the pass, the five expected matches in A2 may not happen. Both were checked equal at REV.

**Verification at the delivered revision**

- Rerun C17, C18 and C22.
- Expected:
  - routed-defects open 0 and selftest exit 0.
  - invocation-audit `unlabelled_variant` 0, or only rows whose text says `unexercised`.
  - `verification.json` `unexpected_exits` without `selftest-routed-defects`.

## Commands and exit codes (run 2026-10-20; `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin`; R=REV, B=baseline)

```text
C0  git rev-parse --verify R^{commit}                                   → b2aad08… [exit 0]
C1  git grep -n -F 'Debts carried to round 13' R -- corpus/lessons/round-12-verifier-spotcheck.md   → :17 [exit 0]
C2  git log --diff-filter=A --format=%h R -- corpus/SOURCES.md          → 5ac7860 [exit 0]
C3  git grep -n -E 'S[0-9]{3}' R -- corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md   → (none) [exit 1]
C4  git grep -n -e arc3-r12 -e evidence-id-domain R -- corpus/SOURCES.md → (none) [exit 1]
C5  git grep -n -i -E 'custody|unpaired|pre-pair|post-only' R -- corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md → (none) [exit 1]
C6  git log --format=%h R -- corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md       → 4072ebb [exit 0]
C7  git grep -n -i -E 'routed|debts? carried' R -- corpus/lessons/round-13-verifier-spotcheck.md → (none) [exit 1]
C8  git grep -n -F 'Round-15 correction — virtual-dispatch advisory' R -- corpus/lessons/round-14.md → :144 [exit 0]
C9  git grep -n -F 'Named correction — virtual-dispatch advisory' R -- LOG.md                     → :1847 [exit 0]
C10 git grep -n -F 'must not be submitted as machine-gradeable' R -- corpus/QUALITY.md           → :27 [exit 0]
C11 git grep -n -F 'python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py' R -- corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md → :83 [exit 0]
C12 git grep -n -F '.ufo/waves/round-15/boundary-fixtures/expected.json' R -- SKILL.md          → :450 [exit 0]
C13 git grep -n -F '"orig_argv"' R -- .ufo/waves/round-16/controls.json                        → :411 [exit 0]
C14 git grep -c -F 'this round' R -- SHONEN.md                                                  → (none) [exit 1]
C15 git grep -n -i withdraw R -- SCORECARD.md LOG.md corpus/lessons/round-1{3,4,5,6,7,8}.md     → (none) [exit 1]
    git grep -n -F '| operability — C3 | recheck-grading rows 0 → 3' R -- SCORECARD.md         → :2095 [exit 0]
    git grep -n -F '| operability (not owned) |' R -- SCORECARD.md                              → :2147 [exit 0]
    git grep -n -F '"axis": "operability"' R -- .ufo/waves/round-18/claims.json                 → :18 [exit 0]
C16 python3 -I -B .ufo/waves/round-17/tools/temporal-sweep.py --root <LANE> --rev B → corrected 4 sites 4 unqualified 0 new 0 [exit 0]
    python3 -I -B .ufo/waves/round-17/tools/temporal-sweep.py --root <LANE> --rev R → corrected 4 sites 4 unqualified 0 new 0 [exit 0]
C17 python3 -I -B .ufo/waves/round-17/tools/invocation-audit.py --root <LANE> --rev B → rows 17 match 17 unlabelled 0 [exit 0]
    python3 -I -B .ufo/waves/round-17/tools/invocation-audit.py --root <LANE> --rev R → rows 26 match 17 unlabelled 9 [exit 0]
C18 python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root <LANE> --rev B → open 6 named 6 substance 6 [exit 0]
    python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root <LANE> --rev R → open 0 named 0 substance 0 [exit 0]
C19 git grep -n -i -E 'final exit|exit line' R -- corpus/lessons/round-18.md LOG.md SCORECARD.md .ufo/waves/round-18/evidence/sums-runlog.json → (none) [exit 1]
C20 git show da64646:.ufo/waves/round-17/runs/run-log.txt | tail -n 1 → '== pro-op end 2026-10-20T11:00:05-03:00 carrier-run=0 compare=0' [exit 0]
    git show R:.ufo/waves/round-17/runs/run-log.txt | tail -n 1      → 'run-carriers exit=0' [exit 0]
C21 git grep -n -i -E '1\.27\.2|pacman (was )?paused|why .*pacman' R -- corpus/lessons/round-17.md corpus/lessons/round-18.md SCORECARD.md → (none) [exit 1]
C22 python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --selftest → SELFTEST: FAILED closed-fixture-cli … closed-fixture-inprocess … token-only-×5 extra_open=['R17-PINMAP'] [exit 1]
C23 git show eb6c266:.ufo/waves/round-18/tools/routed-defects.py > $(mktemp -d)/routed-defects.py; python3 -I -B <that> --selftest → SELFTEST: CLEAN cases=17 [exit 0]
C24 git grep -n -F 'mid_map_mismatch\"' R -- .ufo/waves/round-18/tools/routed-defects.py → :914 [exit 0]
    git grep -n -F 'need = ("mid_map_sha256_mismatch", "mid_map_compare_mismatch")' R -- .ufo/waves/round-18/tools/routed-defects.py → :282 [exit 0]
    git grep -n -F 'CLEAN 17' R -- corpus/lessons/round-18.md → :67 [exit 0]
    git grep -n -F 'run("selftest-" + n[:-3]' R -- .ufo/waves/round-18/verify.py → :159 [exit 0]
Row fields: git show R:SKILL.md | awk 'NR==565||(NR>=586&&NR<=593)' → 9/9 rows carry "Pinned values" and "Write scope" [exit 0]
```

## Context checks (not routed by any spot-check)

- **r12 review D6**, the census `--root` default. It is still present: `.ufo/gates/c1-census-v10.py:629` [OBS]. It was a reviewer follow-up in fleet `.ufo/waves/kaika-w3/kaidoku-review.md:126`, but the integrator never routed it.
- **r13 review hygiene residue**, the fleet `LOG.md` blank line. `git -C /home/vgpnk/Projects/shokunin status --porcelain -- LOG.md` prints nothing (exit 0): it is resolved and was never lane-owned.
