# ScribeShonen — round-20 SHONEN draft and rev-scoped falsification (wave 2)

Verdict: **PARTIAL.** The four round-20 SHONEN boxes can be drafted as `[~]` with every pointer resolving at S=`5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` (checked with `git show S:<path>`). Round-20 C2 and C3 counts hold at S. C1 is **FALSIFIED at S**: routed-r19 exits 1 with one substance-open item (D5, `final-census.json` absent). The S copy of `corpus/lessons/round-20.md` lacks the recovery narrative and Mistakes 9-11 that exist only in the working tree. No box is `[x]`.

Scope: read-only. Revision facts come from Git objects at S, B and F. Counting commands ran on a `git clone --no-hardlinks` of the lane, checked out detached at S, under `~/.cache/scribe-shonen-*` (removed after use). No lane file was written except this report. Observation is labelled OBS; inference is labelled INF.

## 1. Revision anchors (OBS)

| Rev | Role | Committer time (`%cI`) | Ancestor of S |
|---|---|---|---|
| `14f0260ad319ecc26994381b2415d5a999003375` (B) | baseline | n/a | yes (`merge-base --is-ancestor` exit 0) |
| `808cbb31a1e24656da5ba4967497e602fbca7415` (F) | C3 freeze | 2026-10-20T18:01:54-03:00 | yes (exit 0) |
| `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` (S) | measured source | 2026-10-21T03:00:00-03:00 | — |

- `git diff --stat B S` → 23 files, 1371 insertions, 129 deletions. Round-20 changes to shared files are additive only (`LOG.md` +25, `SCORECARD.md` +31, `SKILL.md` +9, `PROVINCE.md` +9, `corpus/QUALITY.md` +3, all zero `-` lines). `corpus/SOURCES.md` has 3 `-` lines: the used-by cells of S003, S023, S035 rewritten with the appended suffix, as the lesson states (`corpus/lessons/round-20.md:131-139` at S).
- `SHONEN.md` is unchanged B→S. The four current boxes still carry round-14/round-1 pointers; the drafts below are new.
- Lane working tree is dirty and must not be cited for rev-scoped claims: `M corpus/lessons/round-20.md` (+28 lines), plus untracked `.ufo/waves/round-20/w2/`, `wave2-*.json`, `verify/recovery/`. (`git status --short`, 11 entries, OBS.)

## 2. Attack items

### A. C1 closure at S (routed r19 items 11→0) — FALSIFIED at S

- `python3 -I -B .ufo/waves/round-20/tools/routed-r19.py --root <clone> --rev 5c0b46c… --strict` → **exit 1**. `named_open 0`, `substance_open 1`, `open_count 1`. Open: **D5** "final-census.json absent or invalid at REV".
- D1, D2, D3, D4, D6a, D6b, D6c, D6d, D6e, D6f: named and substance both true.
- `git cat-file -e S:.ufo/waves/round-20/verify/final-census.json` → absent; `git log --all -- .ufo/waves/round-20/verify/final-census.json` → empty. `verification.json` is also absent at S. `verify/recovery/` is untracked on disk and holds only `routed-*-live-strict.json` and `d3-d5-redgreen.txt`.
- `claims.json` C1 `falsified_if` says "any item open at the measured source revision" → FALSIFIED at S.
- Calibration: the "open 11→0" and "census FAIL/1→PASS/0" language in the lesson and SCORECARD (`corpus/lessons/round-20.md:9-18`, `SCORECARD.md:2596`) is not supported at S for D5. SCORECARD.md:2578 and 2596-2598 still read "Final measured verdict appended after verification".
- Census live: `python3 -I -B .ufo/gates/c1-census-v10.py --root <clone>` → **exit 0**, `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`. "census exit 0 at the delivered tip" HOLDS at S. "D5 record committed" does not.
- Environment caveat (OBS): the same routed-r19 command on a clone under `/tmp` gave exit 1 with **5** substance-open items (D1 "/tmp is excluded scratch (EDQUOT hazard)", D2, D5, D6a, D6c). Its counter and revexec refuse `/tmp`. Moving the clone to `~/.cache` removed D1, D2, D6a and D6c. The SKILL row for routed-r19 (`SKILL.md:603`) does not warn about this. Source-side defect: none found; instruction defect: yes (INF that a lane-path run is unaffected; not run in the lane).

### B. C2 coverage — HOLDS at S

- `python3 -I -B .ufo/waves/round-20/tools/verb-coverage.py --root <clone> --rev 5c0b46c…` → **exit 0**, `package_version 6.5.0`, 153 CLI commands, `mentioned` 133, `zero` 20 (claim threshold ≥131 MET).
- Target verbs (`targets`): `inspect-wasm-artifact` entries 1, exercised true, 3 bound ids; `compare-wasm-interfaces` 1, true, 5; `execute-rizin-command` 2, true, 5; `list-objdump-architectures` 1, true, 1; `project-harmony-application-graph` 1, true, 4. Five of five exercised (≥3 threshold MET).
- Not measured: README coverage-map integrity (command A, `claims.json` C2 `falsified_if`). I did not locate a runnable command A; gap, not a pass.
- The "128/153 at B" baseline is quoted from the lesson, not re-measured (INF from wording).
- Limit: `bound_evidence` is a substring/token check; mention-level, as the claim itself says.

### C. C3 depth — HOLDS at S

- `python3 -I -B .ufo/waves/round-20/measure.py 5c0b46c… --freeze 808cbb3…` → **exit 0**. `c3`: `status evaluated`, `first_failure_bound 19`, `matched 19`, `freeze_equal_predictions 19`, `receipt_valid 19`, `receipt_invalid_or_unusable 0`, `compare_records 19`, `compare_matched_records 19`. `compare_exit_files` reads 0 while `compare_files` is 19; I did not inspect that field's definition, so it is unexplained here.
- `git diff --stat F S -- .ufo/waves/round-20/predictions .ufo/waves/round-20/tools/swiss-misread-v2.py .ufo/waves/round-20/tools/compare-first-failure.py .ufo/waves/round-20/tools/first-failure-extract.py` → empty. No prediction blob or comparator/emulator byte changed after the freeze (claim `falsified_if` clause HOLDS).
- `.ufo/waves/round-20/verify/receipt-validation/summary.txt` at S: 19 `t1246-*` lines, all exit `0`.
- Counts: 19 labels; freeze predictions `predictions/swiss-misread-v2/` = 19 files at S.

### D. Lesson at S versus working tree — FALSIFIED as a citable source for recovery claims

- `git show S:corpus/lessons/round-20.md | wc -l` → 137. Working tree → 165. `grep -c "Recovery attempt 2"` at S → 0. Mistakes rows 9-11 at S → 0. The S Mistakes table ends at row 8 (`corpus/lessons/round-20.md:107`).
- Consequence: the SHONEN drafts cite only S lines 9-20, 66, 96-111, 119-131. Nothing from the working-tree recovery section is used.

### E. Evidence timestamps — HOLDS at S; D2 mechanism observed at B

- `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root <clone> --rev S --path .ufo/waves/round-20 --strict` → **exit 0**, `findings: []`.
- At B, `--path .ufo/waves/round-19 --strict` → exit 1, `future_dated claims.json:36` (stamp 2026-10-20T16:20:00-03:00, committer 19:09:17Z). At B, `--path .ufo/waves/round-18` → exit 1, `future_dated claims.json:35` (stamp 13:25:00-03:00, committer 16:23:55Z, +65 s). Matches lesson Mistake 2 (`corpus/lessons/round-20.md:101`).

### F. D6 probes and routed-r19 "substance" items — HOLD in the non-/tmp clone

- Routed items D1 (custody scratch refuses in-worktree), D6a (head-rev-lint nested), D6c (citation slug `../x` → exit 2 `slug_unsafe`) pass in the `~/.cache` clone. Their pass depends on scratch location, per A.

### G. Additive-only shared docs — HOLDS

- PROVINCE.md: Round-20 Core additions at S lines 164-171; lines 88-116 unchanged B→S (`git diff` shows no `-` lines).
- SKILL.md: craft section 81-314 unchanged; round-20 rows 603-611 added.

### H. Instruction defects found while drafting — PARTIAL

- `SKILL.md:611` (`round20-measure`) gives `measure.py <REV>` without `--freeze`. SCORECARD.md:2598 and `measure.py` usage (`REV --freeze COMMIT`) require the freeze argument for C3 freeze identity. Whether the row without `--freeze` leaves `c3` unevaluated is not tested (INF).
- `SKILL.md:603` routed-r19 row: no `/tmp` scratch warning (see A).
- `claims.json` C2 cites a README command A; I could not locate a runnable form. Not measured.

## 3. Drafted SHONEN lines (round 20; all `[~]`; none `[x]`)

Pointers are rev-scoped to S `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`, checked with `git show S:<path>`. Box text unchanged from `SHONEN.md:5-11`.

```
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  asserted: `SKILL.md:81-314` (craft section; unchanged B→S) at round-20 measured source `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`; round-20 additions are gate/probe command rows at `SKILL.md:603-611` (pinned values and write scope), not new decision tables or error patterns; the rows cite paths, not S-ids (S-id citations are in `corpus/SOURCES.md:46-53` and `corpus/knowledge/2026-10-20-r20-*.md`); no promotion verifier.
- [~] At least one end-to-end domain task executed and logged in LOG.md
  asserted: round-20 C3 domain run on 19 go1.24.6 toolchain ELFs; first-failure forecasts frozen at `808cbb31a1e24656da5ba4967497e602fbca7415` (`git diff --stat 808cbb3 5c0b46c -- .ufo/waves/round-20/predictions` empty); `measure.py 5c0b46c… --freeze 808cbb3…` exit 0, `c3.first_failure_bound` 19, `matched` 19, receipts 19/19 valid (`.ufo/waves/round-20/verify/receipt-validation/summary.txt`); run dirs `.ufo/waves/round-20/runs/t1246-*`; logged `LOG.md:2289-2312`; entry `corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md`; lesson `corpus/lessons/round-20.md:122-131`; C2 run evidence `.ufo/waves/round-20/evidence/c2/`; no identified outside verifier (hyaku spot-check pending, `corpus/lessons/round-20.md:62-64`).
- [~] Instructions executable by an agent without oral context
  asserted: round-20 counting commands `SKILL.md:603-611` and `SCORECARD.md:2596-2598`, re-run at `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` from a clone outside `/tmp`: `routed-r19.py --strict` exit 1 (one open: D5, `final-census.json` absent at REV); `verb-coverage.py` exit 0 (133/153 mentioned, 5/5 targets exercised); `c1-census-v10.py` exit 0 `VERDICT: PASS`; `evidence-timestamps.py --path .ufo/waves/round-20 --strict` exit 0; `measure.py --freeze` exit 0 (`c3` 19/19). Known instruction defects: routed-r19 exits 1 with five open under a `/tmp` clone (not warned at `SKILL.md:603`); `SKILL.md:611` omits `--freeze` used at `SCORECARD.md:2598`; no promotion verifier.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  asserted boundary: `PROVINCE.md:88-116` (unchanged B→S; safety refusal at :114-116); round-20 Core additions `PROVINCE.md:164-171` (WABT, Rizin, objdump, HarmonyOS rows, "verified 2026-10-20", each pointing at a `corpus/knowledge/2026-10-20-r20-*.md` entry); adjacency contest `corpus/lessons/round-20.md:119-120` (revenger-shokunin's PROVINCE still claims the REA toolset; reported, not absorbed; no L0 line); province-version alignment still contested per `corpus/lessons/2026-10-15-round-1.md`; no promotion or complete accuracy claimed.
```

## 4. Blockers before any box could become `[x]` (for the L1)

1. Commit `.ufo/waves/round-20/verify/final-census.json` (D5) at the measured tip; until then `routed-r19 --strict` at S is exit 1 and C1 is FALSIFIED at S.
2. Commit or drop the working-tree recovery section and lesson Mistakes 9-11 (`corpus/lessons/round-20.md`, +28 uncommitted). The S lesson does not contain them.
3. Replace the placeholders "Final measured verdict appended after verification" (`SCORECARD.md:2578`, `:2596-2598`) and create `verification.json` if the SKILL/SCORECARD rows cite it.
4. Fix or document routed-r19 behaviour under a `/tmp` clone (`SKILL.md:603`); add `--freeze` to `SKILL.md:611`.
5. Run and retain the README command-A coverage check the C2 claim names; not measured here.

## 5. Not verified / limits

- Lane working tree was not used as evidence for any pointer above.
- No Go toolchain binary was executed; no REA analyze/search/decompile or Ghidra run was made. `measure.py` read retained receipts and logs only.
- `compare_exit_files = 0` in the C3 record is unexplained (see C).
- Outside verification is not claimed.

Tool installs: none. Scratch removed: `/tmp/scribe-shonen-gCFeM5`, `~/.cache/scribe-shonen-L4cKoB`.
Timestamp of this report: 2026-10-21T04:12:36-03:00.
