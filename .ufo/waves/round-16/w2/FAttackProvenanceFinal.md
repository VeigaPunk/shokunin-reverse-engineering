# FAttackProvenanceFinal — marker green vs executed producer, semantic repair, outside review

Seat: wave-2 critic (author side; advisory, not an outside reviewer). Axes: **calibration** (primary), **depth** (C1 provenance only).
Method: static reads of current worktree + baseline `6235498` Git objects + `.ufo/waves/round-15/verification.json`. Nothing was executed or edited, and nothing was installed. `[INFERENCE]` marks conclusions drawn from reading code without running it.
All paths are relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Not repeated here: `w1/AttackRedBefore.md` already shows that the `documentation-red.json` predicates are vacuous (`'argv' in co`; an inverted correction text still satisfies `invocation_correction`) and that the label `resolved` is wrong. Both points still hold for the current bytes. The findings below are additional problems in the integrated artifacts.

## Content check of the four routes (done by reading, no marker involved)

| Route | Current text | Grounding I checked | Verdict |
|---|---|---|---|
| 1 invocation | r15 entry `## Round-16 correction` (r15 entry :76-91); SKILL go-snapshot-inventory row | Labels `snapshot-inventory`/`inventory-determinism` in `round-15/verification.json` have exactly `python3 -I /home/…/round-15/snapshot-inventory.py --ghidra … --select 1.24.7 1.25.7 1.26.8`, exit 0, top-level `revision` `7ad23fe…`. `snapshot-inventory.py` is unchanged in `7ad23fe..HEAD` | Correct for r15. **A new instance of the same defect exists for r16 (F1)** |
| 2 supplement | SKILL.md:450 pinned-values cell | `round-15/verification.json` label `boundary-frozen` ran `quote-fidelity.py --frozen …/round-15/boundary-fixtures/expected.json`, exit 0 | Correct |
| 3 producer | `controls.py` | Retains argv/orig_argv, executable, isolated flag and resolved revisions (controls.py:281-296) | Partial (F4) |
| 4 SHONEN | SHONEN.md:10 | Title of `corpus/lessons/2026-10-15-round-1.md`:1 is "operator-steered round 1"; commit `c265db9` dated 2026-10-15 | Correct; mark stays `[~]` |

None of these four checks can be produced by any marker in `documentation-red.json` or `measure.py`. A marker green says only that the text is present; these content checks are what support the corrections.

## Findings

### F1 — high — calibration: a new route-1 defect exists, and a marker green does not catch it
- **Counterexample:** `corpus/README.md:36` gives the r16 recheck as `python3 -I .ufo/waves/round-16/selection.py --root <installed-golang-dir> …`. That is a relative script path with a placeholder root.
  - The guidance elsewhere is absolute: `SKILL.md:506` and r16 entry :3 both use `/home/vgpnk/…/selection.py --root /home/vgpnk/.local/opt/…/golang`.
  - New QUALITY #18 (`corpus/QUALITY.md:28`) requires that recheck guidance "matches the exercised isolation flags and paths or explicitly names an unexercised variant".
- **Why markers miss it:** the red snippet's `invocation_correction` and `measure.py:109-114` look only at the r15 entry. They will be green while the README map row repeats the round-15 relative-spelling defect.
- **Smallest correction:** make the README row use the same absolute argv as `SKILL.md:506`, or label it explicitly as an unexercised relative variant.

### F2 — high — depth: the registered fixture command never runs `negative-fixtures.json`
- **Counterexample:** the Fixture check cell at `SKILL.md:506` is `python3 -I …/selfcheck.py` with no `--fixtures`.
  - `selfcheck.py:81` sets the default to `selection-fixtures.json` only.
  - Yet the pinned-values cell in the same row cites both `selection-fixtures.json` and `negative-fixtures.json`.
  - So a green from the registered command proves nothing about the 17 negative cases (invalid requests, unreadable base, two-part name with no fallback, corrupt diff still selected) `[INFERENCE]`.
- **Smallest correction:** register `…/selfcheck.py --fixtures /abs/selection-fixtures.json --fixtures /abs/negative-fixtures.json`, use the same argv in L1's receipt, and require the stdout tally of 26 cases. I counted 9 + 17 ids by reading the files; none are duplicated.

### F3 — medium — depth/calibration: the "exercised" 1.24.5 contrast has no fixture and no registered argv
- **Counterexample:** current docs present 1.24.5 → patch 5 as already done or observed:
  - `corpus/lessons/round-16.md:73`: "the exercised contrast includes 1.24.5→patch 5 despite installed patch 6"
  - r16 entry :9, under an `**OBSERVATION:**` label
  - `LOG.md:1935`
  - `SKILL.md:499` decision row
- **What actually exists:**
  - No case in `selection-fixtures.json` or `negative-fixtures.json` has an exact diff together with a higher installed diff. `future_diff_ignored` uses 1.22.1 with diffs 3 and 9; `lower_fallback` uses 1.21.5 with diffs 2 and 4.
  - Every registered or recheck argv uses `--request 1.24.7`, which is the 1.24.6 fallback already held in r15.
  - `verification.json` does not exist yet.
  - The only 1.24.5 identity comes from `w1/AttackNovelty.md:22`, which was derived from round-15 inventory pins, not from running `selection.py`.
- **Why it matters:** this contrast is the distinguishing novelty for C1, and nothing currently produces it. Installed `patchverdiffs` contains `go1.24.1–6`, so the expected choice of patch 5 follows from reading the source `[INFERENCE]`; it has not been observed.
- **Smallest correction:** retain an L1 receipt for `selection.py … --request 1.24.5 --goos linux --goarch amd64` and add a hand-authored fixture with exact diff 5 and higher diff 6 (wave-2 `FBoundedNumeric` is drafting this). Until both exist, change "exercised" to "planned" and remove the OBSERVATION label from that sentence.

### F4 — medium — calibration: controls.py records its argv but not its own code
- **Gaps:**
  - controls.py:281-296 records `argv`, `orig_argv`, `executable` and `repo_root`. It records neither the bytes of the producing script nor the cwd.
  - The script being executed is a worktree file (`.ufo/waves/round-16/` is currently untracked), while its inputs are immutable Git objects. If `controls.py` is edited after a run, the stored argv still points at the same path but would produce different output. A relative `orig_argv` also cannot be reproduced without the cwd.
  - `selfcheck.py:392` prints only `sel_path.name`, so `--selection /tmp/x/selection.py` produces the same header as the real module, and it prints no fixture or module digests.
- **Smallest correction:**
  - Add to `invocation`: `producer_sha256` (sha256 of `Path(__file__).read_bytes()`), `producer_blob_at_after` (`after.sha(".ufo/waves/round-16/controls.py")`), the computed Git blob id of the running file plus an equality boolean, and `os.getcwd()`.
  - In selfcheck, print the resolved path and sha256 of the selection module and of each fixture file.

### F5 — medium — calibration: two no-harm claims have no producer
- **Claims:** `LOG.md:1950` says "#17 remains intact" and `LOG.md:1949` says "four marks remain `[~]`".
- **Gap:** neither `controls.py` nor `measure.py` reads QUALITY rows 1–17 or counts SHONEN marks. QUALITY.md is not in `APPEND_ONLY`, because rows are inserted mid-file, so prefix checks cannot cover it.
  - `w1/ReviewMeasure.md:11` (finding 3) asked for a byte comparison of rows 1–17. That is still not done in the current artifacts.
  - The r15 precedent had `row16_unchanged` in `round-15/no-harm-controls.json`.
- **Content today:** the diff adds only row 18, and SHONEN changes only line 10. So the content is fine; only the producer is missing, which is the route-3 requirement.
- **Smallest correction:** in `controls.py`, add a QUALITY row-cell comparison (same shape as `source_rows`) for row ids present at BEFORE, plus counts of `- [~]`/`- [x]` in SHONEN at BEFORE and AFTER. Until then, cite the logged claims to a reviewer's diff read, not to `controls.py`.

### F6 — low/medium — calibration: the red-before result cannot be told apart from a failed read
- **Gap:** `documentation-red.json:6` uses `get()`, which returns `''` for any non-zero `git show`. A wrong repo path or revision would also print 0/4 with exit 1. The stdout `revision` field only echoes argv, and the retained output has no per-path read status.
- **Smallest correction:**
  - Pair the red result with a retained `measure.py 6235498` receipt. `measure.py` exits 2 on any unreadable anchor (measure.py:64-68), so exit 0 there shows the same baseline objects were readable.
  - Alternatively, wrap the after-run so it records `git cat-file -e` for each of the four paths. The snippet itself must stay byte-identical so red and after-run remain comparable.

### F7 — low — calibration: smaller documentation and naming mismatches
- **selfcheck exit codes:** `selfcheck.py:63-66` documents exit 2 for a "malformed case schema". In fact a `FixtureError` raised per case is caught at :400 and counted as a failure, giving exit 1 (:410), the same exit as a model mismatch `[INFERENCE]`.
- **measure.py marker name:** `C2_named_r15_correction_isolated_absolute_recheck` anchors on the first line containing "correction". That is r15 entry :37, the round-15 "outside correction" heading, not the `Round-16 correction` heading. Any later `-I` plus an absolute path satisfies it, so the "named" in the key is not checked.
- **Forward references:** r16 entry :2 says receipts "are recorded in the execution addendum", and `SKILL.md:506` and `README.md:36` cite `.ufo/waves/round-16/verification.json`. Neither exists yet. If the source commit is measured without them, every C1 presence marker can be 1 while the evidence it cites is absent.
  - Correction: land the addendum and `verification.json` before the after-measurement revision, or reword them as future records.

## Outside review
No current artifact claims outside review. `corpus/lessons/round-16.md:20`, `LOG.md` and the r14 correction all keep seat work on the author side, and promotion and `[x]` remain withheld. This holds as long as the after-receipt for the red snippet is not reported as "4/4 resolved" (see `w1/AttackRedBefore.md`).

## Limits
- This is a static review only. Expectations about selector behaviour (F2, F3, F7) are `[INFERENCE]` from reading the code, not observed runs. Line numbers refer to the current worktree bytes.
- I did not judge the fixture expected values, the SOURCES `used-by` deltas or the craft section.
- No checks, builds, tests, linters or formatters were run. No implementation or corpus file was edited.
- Tool installs/updates: none.
