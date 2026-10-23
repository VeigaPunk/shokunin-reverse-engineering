# Round 34 correction record: Round 33 report and routed defects

**Status:** append-only correction draft for Main; not integrated into shared files. The filed Round 33 report and its historical pin JSON were not rewritten.

## Behavior and evidence

The non-author closure at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-33-verifier-spotcheck.md:27-29` records that Round 33 report:8 said `SKILL.md` and `PROVINCE.md` were unchanged. The spot-check's exact command and result were:

```text
git diff --numstat 428315a8 4ead4313 -- SKILL.md
72 0
```

It separately records `git diff --quiet` for `PROVINCE.md` as exit 0. Therefore the report statement is false for `SKILL.md` (72 insertions, zero deletions) and supported for `PROVINCE.md`. The spot-check attributes the additions to the CHPE decision table and registry rows (lines 64 and 85). The cited filed report path, `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/reports/round-33/kaidoku.md`, was not present in this checkout; the quoted report claim and measured diff are taken from the non-author spot-check, not represented as a direct re-read or remeasurement by this scribe.

### Forward pointer for the old parser pin

Preserve `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/prep/R33ChpeParser-independent.json` as filed. Its `tools/round-33/measure_driver.py` pin at line 6 is the historical digest `af5d86f15c22f9d1fc148d2a6b81004eb76967d50c314c9078633bc6ccee32ac`.

The forward pointer is `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/text-checker-supersession.json`: `old_source_revision` is `d7076120e4f00c6d18aa77b8764d14861e820eb2`, `old_driver_sha256` is that historical digest, and `new_driver_sha256` is `c5efebfda52e069c29cc2312e8a73f690411ffe6a01a8568a7243f4357b00a3e`. Its reason is the asymmetric canonical-section normalization repair and blank-margin regression; its scope explicitly says this is an unfrozen text-quality repair, not a replacement for the stopped 32-row claim or carrier data. The spot-check at line 35 says the retained driver differs only by this normalization fix. This record supplies the forward pointer; it does not rewrite the old JSON, upgrade the historical pin, or create production-measurement evidence.

## Routed-defect disposition

| Spot-check route | Disposition in this correction | Admission boundary |
|---|---|---|
| 1. Report:8 says `SKILL.md` was unchanged. | Correct by an appended LOG/lesson erratum using the exact `72 0` result above; leave the filed report intact. Draft text follows. | This is a reporting correction only, not an axis improvement. |
| 2. R33-C1 remains unprovable. | Preserve the stop in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/claim-stop.json`; do not revive the claim, rebuild its held task, or use quarantined builder outputs. | Explicitly exclude the original claim and all held-derived controls from Round 34 admission. Keep `U064N008Hf47eb933` untouched. The basis is the spot-check at lines 31-38, 68-82, and 125-129, plus the Round 33 lesson at lines 36-47. |
| 3a. Seven empty/malformed freeze maps falsely report CLEAN. | No repair is evidenced by the records reviewed for this correction. | Keep disclosed; do not use the affected instrument as admission evidence. |
| 3b. Parser count-limit `>`/`>=` boundary mutant survives. | No kill is evidenced here. A proposed or running probe is not a result. | Keep disclosed; exclude count-gate admission until a retained result demonstrates the boundary mutant is rejected. |
| 3c. Metadata-span mutation was inconclusive after baseline EAGAIN. | Inconclusive remains inconclusive; no pass/fix is inferred. | Keep disclosed and exclude that mutation result from admission. |
| 3d. Tag mutant was detected only via a detector error. | Do not count the detector error as a successful mutation kill. | Keep disclosed; exclude any robustness claim based on this result. |
| 3e. Disk scanner has lexical blind spots. | Preserve the old scope statement: it misses cwd/variables and relative multi-segment forms; retained quoted command examples scan red (Round 33 lesson line 57; spot-check line 134). | Keep disclosed. A clean lexical scan is not proof of non-execution and cannot support a broader absence claim. |
| 4. Five Round 32 wrapper mutants and secondary-gate selftest gaps remain open. | No repair evidence is supplied in this correction. | Explicitly exclude claims of closure/conformance for the five wrapper mutants and `pe_own_compare`, `verify_quotes`, and `independent-pe`; retain the spot-check's line 136 limitation. |
| 5. Old `measure_driver.py` digest has no forward pointer. | Add the separate forward-pointer record above, pointing from the historical pin to the existing supersession record. | Pointer resolves provenance only. It does not replace the original digest, re-freeze a claim, or turn the text checker into carrier evidence. |

No Round 34 result is inferred from an in-progress seat or from the proposed wording below. If another retained Round 34 artifact later demonstrates a routed fix, Main should replace that row's explicit exclusion with the exact artifact, command, and outcome before making an admission claim.

## Append-ready LOG text

```text
- Round-34 append-only correction to Round-33 report:8, per the non-author spot-check at corpus/lessons/round-33-verifier-spotcheck.md:27-29: report:8 said `SKILL.md` and `PROVINCE.md` were unchanged, but `git diff --numstat 428315a8 4ead4313 -- SKILL.md` returned `72 0`; the spot-check's `git diff --quiet` for `PROVINCE.md` exited 0. The SKILL additions are its CHPE decision table and registry rows. The filed report is not rewritten. R33-C1 remains unprovable; the held builder outputs and all derived controls remain excluded, and U064N008Hf47eb933 remains untouched. The seven false-CLEAN freeze-map cases, count-boundary survivor, EAGAIN-inconclusive metadata-span mutation, detector-error-only tag mutant, disk scanner's cwd/variable/relative-multi-segment lexical gaps, five Round-32 wrapper mutants, and secondary-gate gaps (`pe_own_compare`, `verify_quotes`, `independent-pe`) remain disclosed and are not cited as admission evidence. The historical measure_driver.py digest in .ufo/waves/round-33/prep/R33ChpeParser-independent.json:6 is linked forward to .ufo/waves/round-33/text-checker-supersession.json; neither historical JSON is rewritten, and the text-only repair is not a substitute carrier measurement. No axis gain or promotion follows from this correction alone. See .ufo/waves/round-34/prep/R34Corrections.md.
```

## Append-ready Round 34 lesson text

```markdown
## Round 34 appended correction to Round 33 report:8

The non-author spot-check (`corpus/lessons/round-33-verifier-spotcheck.md:27-29`) found that Round 33 report:8 called both `SKILL.md` and `PROVINCE.md` unchanged. Its exact `git diff --numstat 428315a8 4ead4313 -- SKILL.md` result was `72 0`; its `git diff --quiet` check for `PROVINCE.md` exited 0. Correct the SKILL statement only: the file gained the CHPE decision table and registry rows. This is an append-only report correction; the filed report remains unchanged.

R33-C1 remains unprovable, not repaired by source work, selftests, or a text-quality check. Do not reconstruct the held builder task or admit its quarantined outputs/derived controls; keep U064N008Hf47eb933 untouched. The freeze-map false-CLEAN cases, count-boundary survivor, EAGAIN-inconclusive metadata-span mutation, detector-error-only tag mutant, and the disk scanner's cwd/variable/relative-multi-segment lexical gaps remain disclosed and excluded from admission. The five Round-32 wrapper mutants and `pe_own_compare`, `verify_quotes`, and `independent-pe` selftest gaps also remain open absent retained repair evidence. The old parser JSON's measure_driver pin is historical; this correction points to `text-checker-supersession.json` for the old/new digest and its text-only scope, without rewriting the old pin or treating the repair as carrier evidence.
```

## Proposed QUALITY criterion text

Candidate new row `#65` (not yet added; keep existing rows unchanged):

```markdown
| 65 | A report's assertion that a tracked file is unchanged names the exact base and tip and is supported by a per-file diff result (for example, `git diff --numstat <base> <tip> -- <path>`); a whole-tree additions-only summary does not establish an individual file's status. If an outside recheck finds the assertion wrong, append the measured correction to the next LOG/lesson and leave the filed report intact. | `corpus/lessons/round-33-verifier-spotcheck.md:27-29` (report:8 said SKILL unchanged; measured `72 0`; PROVINCE diff was empty); `.ufo/waves/round-34/prep/R34Corrections.md` | — |
```

This is a proposed criterion grounded in one observed reporting error, not evidence that quality improved or that the criterion has been adopted.

## Gates, provenance, limits, and surfaces

- **Gates:** no build, test, counter, parser, REA, or production-reader command was run by this scribe. The exact diff commands and outcomes above are quoted as evidence from the non-author Round 33 spot-check, not re-executed. No tool was installed or updated.
- **Touched surface:** only `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34Corrections.md` is produced by this assignment. The Round 33 report, `SKILL.md`, `LOG.md`, `QUALITY.md`, lesson files, and both old JSON records are inputs and remain unedited by this scribe.
- **Out of scope:** editing shared LOG/lesson/QUALITY or product files; rewriting the filed report or old JSON; using held builder outputs; touching `U064N008Hf47eb933`; rerunning gates; claiming the original study, instrument limits, or a Round 34 fix are resolved without retained evidence.
- **Operator teaching:** the Round 33 non-author note (`corpus/lessons/round-33-verifier-spotcheck.md:115-123`) leaves all four SHONEN boxes `[~]`: Box 1 is checkable and re-opened; Box 2 still lacks a new end-to-end R33 carrier study; Box 3 still needs a non-author to execute the written instructions and was not done by that spot-check; Box 4 arbitration remains unresolved. This correction closes none of those teaching/promotion gates. The two operator lessons reviewed, `corpus/lessons/2026-10-18-wave-dispatch-counting.md` and `corpus/lessons/2026-10-18-caller-independent-services.md`, concern parent dispatch counting and long Ghidra runs respectively; neither supplies evidence for these Round 33 defects.
- **Model/errors:** the project context exposes model label `openai-codex/gpt-6-luna`; no safety refusal or automatic model switch was observed in this scribe work.
- **Read evidence:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-33-verifier-spotcheck.md`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/prep/R33ChpeParser-independent.json`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/text-checker-supersession.json`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-33.md`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/2026-10-18-wave-dispatch-counting.md`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/2026-10-18-caller-independent-services.md`.

---

Artifact: `.ufo/waves/round-34/prep/R34Corrections.md`
