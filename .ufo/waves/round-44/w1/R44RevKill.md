# R44RevKill — kill rules and causal separability of plans/round-44-claims.md (draft at fc5eb54a)

Read-only review. Commands: `git log/show --numstat`, `grep`, a python stem count, `7z l` on the four frozen carriers. Nothing was written outside this file.

Verdict: **do not freeze as drafted.** There are 3 blocking and 5 non-blocking findings. The two blockers that matter most are the same defect seen from each side: the frozen-path list contradicts both claims' own landings (K1, S1).

## (a) Kill rules

### K1 (BLOCKING, both claims): the frozen-path list makes both landings trip `frozen_path_changed`
- The Freeze-integrity rule says any commit in `FREEZE..REV` touching a frozen path, or any blob that differs at REV, gives exit 2 `frozen_path_changed`.
- The draft's frozen list (lines 207-222) freezes whole files: `corpus/README.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`.
- C1's predicate needs a post-freeze `corpus/README.md` map row. It also needs an S138/S139 row whose `used-by` names the entry, which is only known once the entry exists.
- C2's landing edits `SCORECARD.md`, `SHONEN.md` and `corpus/README.md`.
- Round close also edits `SCORECARD.md` and `SHONEN.md`. That is after REV, but the draft does not say so.
- So the target is unreachable. The control set would show only "red", and the kill rule would mean nothing.
- The draft half-admits this in "C2 landing mechanics" (lines 224-233). It first says the blobs stay equal, then says the repair is appended lines, which changes the blob.
- It then relaxes the arm "only for rubric-named paths" and binds the diff to "exactly the rubric's expected edit bytes". Those bytes cannot exist before the landing. A bound on bytes that are unknown pre-landing is either vacuous or forces the rubric to be written after the data.
- Precedent: round 42 froze neither `README`, `SOURCES`, `PROVINCE`, `SCORECARD` nor `SHONEN` (`tools/round-42/c1-counter.py:420-433`). Its landing eb8215ac then edited `PROVINCE` +8, `README` +3 and `SOURCES` +4.
- Round 43 froze `SOURCES.md` because S135-S137 were added at the freeze, and its landing never touched `SOURCES`.
- Fix:
  - Freeze only files the landing does not edit, plus the byte pins of the specific frozen statements.
  - For README/SOURCES/PROVINCE/SCORECARD/SHONEN, bind row-identity (the frozen rows still present byte-for-byte) and append-only. Do not bind whole-file blobs. This matches the registry-immutable rule at `SKILL.md:1542`.
  - Put S138/S139 into SOURCES at the freeze, with `used-by` already naming the planned entry stem.
  - Write each claim's own frozen set explicitly. The "Separability" paragraph claims "each predicate names its own set", but the list at lines 207-222 is a single union.

### K2 (BLOCKING, C2): CTL-C2-1 cannot fail
- The seeded-mismatch control is applied to a clone of the base, and the base is already red (the claim only exists if the census finds >0 mismatches there). Any clone exits non-zero regardless of the seed, so the control is vacuous.
- Fix:
  1. Add a positive control first: a scratch clone with the rubric's flagged statements repaired must exit 0.
  2. Then seed exactly one mismatch into that clean clone. It must exit 1 and report `mismatches == 1` for the seeded entry id.
  3. Repeat per rubric category (a)-(f). Otherwise a counter that checks only some categories passes.
- A GREEN seeded control (exit 0) then unambiguously stops C2.

### K3 (BLOCKING, C1 and C2): the control sets are red-only, with no positive control
- C1's CTL-0/1/2/3 and C2's CTL-0/1/2/3 are all expected non-zero. A counter that always exits 1 passes every one. The draft's own freeze rule asks for a dev-arm dry run "as frozen" (lines 27-29) but names no control that reaches the target.
- Required:
  - C1: a dev-arm positive on a scratch copy with a real REA 6.5.0 receipt for the 4 carriers, run from the control's own scratch. It must give `carriers_matched 4`, every binding true, exit 0. It must not use `c1-run.sh` and must not commit under `corpus/evidence/round-44/c1/`.
  - C2: see K2.
- Each red control must name the exact `bindings_false` and require exit 1, not just "non-zero". Exit 2 (`frozen_path_changed`, unevaluable) proves nothing about the predicate, and the draft's "exits non-zero" lets a crash or an unevaluable result count as a pass.

### K4 (non-blocking): CTL-C2-0 and its stop rule are partly tautological
- The claim says the counter "exits non-zero with mismatch count equal to the frozen value". That pins the base count into the rubric: fine, but it must be stated that this value is the census output.
- If the rubric lists only statements the census already flagged, `mismatches>0` at base holds by construction. If it lists every statement checked, the CTL-C2-0 stop (0 mismatches at base) is the real signal. State which one it is, and record the ratio of flagged to checked entries. The claim's final sentence ("if the census finds zero mismatches the claim stops") is the right kill rule and should be the only one.

### K5 (non-blocking): CTL-C2-3 is not a control
- "Impossible by construction" is not scored and cannot be shown to fail. Replace it with a concrete case: edit one frozen rubric byte in a scratch clone and require exit 2 `frozen_path_changed`. This is also the only control for the K1 relaxation, which is currently unbounded.

### K6 (non-blocking): "repaired" must not mean "a correction note exists"
- Landing mechanics (lines 227-229) let the counter treat "(frozen-text mismatch at BASE) + (appended correction at REV)" as repaired.
- The check must re-derive the value from the repo at REV: resolve the pointer in the appended note, recount rows. It must not pass on a note's presence or on the string "corrected". Otherwise a one-line note turns any mismatch green.
- Add a control that appends a note carrying a wrong value and expects exit 1.

### K7 (non-blocking): CTL-C1-3, sasquatch-absent, is unmeasured for v1/v2
- **`7z l` reads all four frozen carriers.** Measured now: v1 LE/BE list 3 files each, v2 LE/BE list 4 files each. The draft (line 54) records only that `7z` refuses `v2ns`.
- The draft assumes "no sasquatch ⇒ `missing-extractor-dependency` gap, no match". That holds for the v4 arms measured in rounds 36-39. Those rounds recorded a REA-side 7z fallback only for the carve-then-7z path, not for REA itself.
- Not measured for `squashfs_v1`/`squashfs_v2`. The control must be run at the freeze, before data, to see whether it fails as expected. If it goes green, the kill rule stops C1 on exactly that evidence.
- Consequence for the oracle: `7z` is a third independent reader for the 4 carriers. Either record it as an additional cross-check, or state why it is not used.
- Hard-coded `sasquatch` on the child PATH is `~/.local/bin/sasquatch` on this host. The control's PATH strip and `FIXED_PATH` (`tools/round-42/c1-counter.py:414-419`) must both be reproduced, or the stripped arm will not strip the same dir.

## (b) Causal separability

### S1 (BLOCKING): shared frozen files
This is the same defect as K1. C2's frozen `corpus/README.md`, `SCORECARD.md` and `SHONEN.md` blobs are changed by C1's landing (README map rows) and by closure. As drafted, C1 landing alone gives C2 `frozen_path_changed`, and C2's repair gives C1 the same. The claims are not separable under the current frozen list.

### S2: README line pins — C1's landing breaks C2 category (a) pointers (not blocking if handled)
- `SCORECARD.md` pins bare line numbers into `corpus/README.md`: 22, 77, 79, 90, 126, 138, 177, 178, 179, 180 (measured via grep).
- README structure: `## Coverage map` at line 11, `## Knowledge` at 105, `## Lessons` at 224.
- C1 inserts a row at the end of the Coverage map, before line 105. The round-42 landing did the same: `@@ -98,6 +98,7 @@`, +1 line.
- Every pin after the insertion point shifts by 1 (177-180 sit in the Knowledge table and shift by 1 from the map row and by more from the Knowledge-table row). They no longer point where SCORECARD says.
- A C2 rubric that evaluates "pointer resolves at REV" on these will fail because of C1, not because of calibration error.
- Fix: bind any README/PROVINCE/SOURCES line-pinned pointer at its own revision qualifier (as category (c) does for SHONEN). Prefer row-identity, not line number.

### S3 (hidden coupling not in the draft's separability list): PROVINCE.md
- C2 category (c) and SHONEN/SCORECARD pin `PROVINCE.md` lines (`97-125`, `378-384`, `386-394`, `157`, `103-109`, ...). The draft lists PROVINCE as read by C1 only.
- C1 adds a `## Round-44 additions to Core` section at the end (safe) and a "round-44 frontier note". Round 42 put its frontier note at the end of its own section (line 416), so this is probably end-appended too. Bare pins earlier than the insertion point stay valid. State the rule that C1 appends only.
- C2's rubric must not read PROVINCE beyond the same row-identity rule.

### S4: README row-count check (f) — tolerates C1 only if counted correctly
- Measured: `corpus/knowledge/*.md` = 137 files. A naive count of backticked stems in README gives 36 matched and 35 map-table rows. The README is not a simple 1:1 count, which is why the repo uses command A (`mapped` via the Knowledge table).
- Under command A the base is 137/137. C1 adds one knowledge file and one Knowledge-table row, so REV gives 138/138.
- The rubric must therefore:
  - check "mapped == knowledge_files, missing [] dangling []" derived at REV, never a frozen 137 or 138;
  - not count the Coverage-map rows against the file count;
  - require C1's row in the **Knowledge** table, not only in the map. The r43 closure already says the proxy is satisfied by the index row.
- Also, SCORECARD says (round-43 correction) "knowledge_files=137, mapped=137 at 8de80f1d". That is revision-qualified. Rubric (b) must evaluate it at its own revision, not at REV. Otherwise C1's landing (138) makes it a "mismatch".

### S5: SOURCES row count
- The draft says the rubric does not pin the SOURCES row count. Confirmed in the draft text, but nothing enforces it.
- Round 43's R43-C2 failed on exactly this class: a frozen `numstat` of `3\t0` against the committed `4\t0` (three rows plus a blank separator). The draft keeps `numstat` out of C2 but does not forbid it.
- Add an explicit rule: no rubric entry may read `SOURCES.md` numstat, line count, or highest S-id. The only SOURCES check is row-identity of frozen rows: S001..S137 unchanged outside status/recheck/used-by (the existing `tools/round-38/registry-immutable.sh`). Also state whether the blank-separator style is allowed, since it changes `numstat`.

### S6: the plan file is shared
- `plans/round-44-claims.md` is in the frozen set of both claims. Its "Changes from the draft" section is edited before the freeze, fine, but the file must be committed in the freeze commit.
- Any later closure note must go in a separate file, or both claims lose to `frozen_path_changed`. The draft already marks it "frozen", but the closure appends to plan files in prior rounds are not checked here.

## Summary table

| id | where | severity | action |
|---|---|---|---|
| K1/S1 | frozen list vs both landings | BLOCKING | per-claim frozen sets; row-identity instead of whole-blob for README/SOURCES/PROVINCE/SCORECARD/SHONEN |
| K2 | CTL-C2-1 | BLOCKING | seed into a clean (repaired) clone; add positive control |
| K3 | all controls red-only | BLOCKING | add a positive control per claim; name the exact failing binding and exit 1 |
| K4 | CTL-C2-0 | note | state flagged vs checked ratio |
| K5 | CTL-C2-3 | note | replace with a concrete 1-byte rubric edit expecting exit 2 |
| K6 | "repaired by note" | note | counter re-derives; add a wrong-note control |
| K7 | CTL-C1-3 | note | run before data for v1/v2; 7z reads all 4 fixtures |
| S2 | README line pins | note | pins at revision qualifier or row-identity |
| S3 | PROVINCE pins | note | C1 appends only; C2 reads PROVINCE by row-identity |
| S4 | README count | note | derive from command A at REV; require Knowledge-table row |
| S5 | SOURCES | note | forbid numstat/count/max-S-id in the rubric |

## Residual risk and gaps
- No counter, rubric or `carriers.json` existed at review time (`tools/round-44/` absent). Findings are from the draft text and the committed round-42/43 tools only; nothing in the round-44 counter was evaluated.
- Not run: any REA run, the C1 data procedure, or CTL-C1-3. K7 rests on the `7z l` listing and the round-36/38/39 knowledge entries only.
- Line-pin shifts (S2/S3) were read from the round-42 landing diff and the current SCORECARD pins, not simulated against a draft landing.
- LSP was not used; the files reviewed are Markdown/Python/JSON and the greps are literal, so they are not semantic proof.
