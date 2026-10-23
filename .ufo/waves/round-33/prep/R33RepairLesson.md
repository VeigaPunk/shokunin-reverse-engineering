# Round 33 repair/lesson draft — R33RepairLesson

**Status:** draft for L1 integration; this is not a corpus `QUALITY.md` or lesson edit, and does not claim that any round-33 repair or gate was exercised.

## Behavior and axes

No product behavior was changed. This seat turns the round-32 non-author verifier findings into proposed round-33 Mistakes entries and proposed QUALITY criteria. The relevant axes are evidence integrity and gate/testability; no claim score, admission judgment, or CHPE coverage expansion is made.

## Proposed round-33 `Mistakes` table

Draft IDs below are for integration only. Evidence is from round 32; the fix column is a required repair/evidence recipe, not a claim that round 33 executed it.

| id / class | evidence | captured-by | fix / able-to-fail evidence |
|---|---|---|---|
| M33-1 / planned-deadline timestamp | At measured revision `9ef97f08b655d951650ba5d32f41f1b1cf9653f4`, strict timestamp check had `allow=[]`, `finding_count=4`, `unexempted_finding_count=4`, exit 1. The four findings are `a2audit-gate.json:14`, `a2audit-settle.json:3`, `a2residual-dispatch.json:17`, and `a2residual-settle.json:3`; the values describe planned settle deadlines, not observed execution. | Round-32 non-author verifier, `corpus/lessons/round-32-verifier-spotcheck.md:113`; measured receipt `.ufo/waves/round-32/a2after/timestamps-strict-at-9ef97f08.txt:1-5`. | Follow the round-33 prep contract: represent planned deadlines as durations in seconds, not future wall-clock evidence. If an explicit exemption is retained for a legacy/planned-deadline field, scope it to exact path/field, document its reason, and show a fail-closed fixture: the intended field is exempted while an unlisted future timestamp and an observed-run timestamp still fail. Record the strict check at the measured revision. No round-33 repair or green result is evidenced here. |
| M33-2 / prohibited scratch inventory | The round-32 attempt-forensics report records two `find /fast/scratch/...` inventories and counts (`20336`, `11094`); the verifier identifies this as contrary to the disk directive. This establishes that the scoped commands were issued, not that their inventory was needed or supports a claim. | `a2audit/A2AttemptForensics.md:77-83`, recognized as M32-4 in `corpus/lessons/round-32.md:33-40` and routed at `corpus/lessons/round-32-verifier-spotcheck.md:114`. | Repeat the literal no-`find`/`du` instruction in every wave context. A record-level checker scans retained seat transcripts/receipts (not `/fast/scratch` itself) for the forbidden `find /fast/scratch` invocation and includes an able-to-fail fixture containing such a command. Report scan scope and result; a scan of retained records cannot certify unretained activity. No round-33 scan result is evidenced here. |
| M33-3 / gate-selftest-or-probe | `Freeze integrity, selectable claims` was registered as a gate without a self-invocation mode; the verifier says this violates the gate self-test standard. Round-32 lesson also records the missing self-invocation mode. | `corpus/lessons/round-32-verifier-spotcheck.md:115`; `corpus/lessons/round-32.md:64-69`. | Add a runnable fixture selftest with CLEAN and tampered-pin cases, or register the item as a probe instead of a gate. Report the actual classification and exercise/result; do not describe a probe as a passing gate. No round-33 selftest or reclassification is evidenced here. |

## Proposed `corpus/QUALITY.md` rows (draft only)

Rows 59–61 are provisional next numbers after current rows 57–58; do not append them without L1 review and round-33 execution evidence. Existing QUALITY 58 remains the rule for the falsified lexical calibration measure.

| # | criterion | why (lesson) | supersedes |
|---|---|---|---|
| 59 | Planned deadlines in committed evidence are durations in seconds, not future-dated wall-clock instants. A strict timestamp gate never silently treats a deadline as observed run evidence. If a specific planned-deadline field is explicitly exempted instead, the allowlist names its exact path/field and reason, and an able-to-fail control accepts only that exception while rejecting an unlisted future timestamp and a future-dated observed event. Report the allowlist and strict-gate result at the measured revision. | Round-32 verifier defect 1 (`corpus/lessons/round-32-verifier-spotcheck.md:113`); four unexempted findings at `.ufo/waves/round-32/a2after/timestamps-strict-at-9ef97f08.txt` | — |
| 60 | Every wave context repeats the literal disk-inventory restriction. A checker searches retained seat transcripts/receipts for prohibited `find /fast/scratch` (and any specifically forbidden `du` form), without walking `/fast/scratch`; its committed red fixture must make it fail. State exactly which retained records were scanned. A clean scan is evidence only about that bounded record set. | Round-32 M32-4 and verifier defect 2 (`corpus/lessons/round-32.md:40`; `corpus/lessons/round-32-verifier-spotcheck.md:114`); actual commands in `a2audit/A2AttemptForensics.md:77-80` | — |
| 61 | An item registered as a gate has a runnable self-invocation test and an observed CLEAN case plus a tampered-pin case. If it has no such selftest, register and report it as a probe, not a gate; do not claim a gate pass from its name or from an inherited result. Apply the same distinction to archived/secondary checks before relying on them as gates. | Round-32 verifier defect 3 and disclosed archived-gate limitation (`corpus/lessons/round-32-verifier-spotcheck.md:115`; `corpus/lessons/round-32.md:69,73`) | — |

## Known limits intentionally not repaired / scope boundary

These are disclosures from the round-32 lesson, not successful round-33 repairs. Keep them separate from the three proposed repair rows above:

- The frozen C2v3 lexical counter is falsified: explicit denial and vocabulary-only word bags meet its 4/4 target. QUALITY 58 captures the pre-data control requirement; the verifier expressly says not to reuse C2v3 as admission evidence. No post-score predicate edit or relabel is proposed.
- The metadata-only ARM64X classifier accepts forged map tags on a pure ARM64 fixture. Round-32 limits its evidence to declared structure; this draft does not claim valid EC instructions/ABI, Windows loading, or wider coverage.
- Five of eight bounded C1/C2 selftest mutations survive. They remain frozen-test limitations, not repairs claimed here.
- Archived secondary gates lack separate selftests; the proposed row 61 is a forward criterion, not evidence that those gates are repaired.
- Round-33 prep contract bounds the proposed depth work to source-backed CHPE structural decisions / bounded parser and no coverage widening beyond round-32 synthetic exported-leaf DLLs. This report does not modify the parser, classifier, counter, claims, freezes, or production data.

## Gates and verification

- The round-32 timestamp gate was **red**, not green: its retained receipt reports exit 1 and the four unexempted planned-deadline findings above. This is historical evidence at `9ef97f08b655d951650ba5d32f41f1b1cf9653f4`, not a round-33 run.
- No round-33 checker, fixture, test, build, formatter, or production gate was run by this seat. The disk scanner and selftest/probe tests above are proposals only.
- No tool was installed or updated.

## Touched surfaces and out-of-scope items

Only this assigned report was written: `.ufo/waves/round-33/prep/R33RepairLesson.md`. Read-only inputs were the shared prep contract, round-32 verifier spot-check lines 111–117, round-32 lesson, QUALITY rows 57–58, the timestamp receipt, and the attempt-forensics lines recording the scratch inventories. `QUALITY.md`, round-32 records, product code, claims/freezes, LOG, SKILL, SCORECARD, SOURCES, and fleet state were not edited. No git/jj writes, scratch scans, held-item inspection, or REA/runtime invocations occurred.

## Provenance and exact commands

- Contract base as stated by the shared contract: `428315a8`; round-32 measured revision: `9ef97f08b655d951650ba5d32f41f1b1cf9653f4`. The round-32 lesson records C1 freeze `9a73680a` and C2v3 freeze `f382e3b7978e6091a19ca93277c15a75c0016b43`; no counter was run here.
- Report timestamp command: `date -u '+%Y-%m-%dT%H:%M:%SZ'` → `2026-10-23T08:09:09Z`. The tool wrapper did not expose a separate exit-code field.
- No production command was run. The strict timestamp argv/output/exit cited above are copied from the existing receipt; its argv is the recorded `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I -B .../evidence-timestamps.py --root ... --rev 9ef97f08b655d951650ba5d32f41f1b1cf9653f4 --path .ufo/waves/round-32 --strict`, and its receipt records exit 1. No rerun was made.
- No checks were run for this draft. The report does not claim an exit code for reads or any unobserved test outcome.

## Artifact paths

- This draft: `.ufo/waves/round-33/prep/R33RepairLesson.md`
- Contract: `.ufo/waves/round-33/prep-contract.txt`
- Verifier source: `corpus/lessons/round-32-verifier-spotcheck.md:111-117`
- Mistakes/known limits source: `corpus/lessons/round-32.md:33-40,64-73`
- QUALITY source: `corpus/QUALITY.md:67-68`
- Timestamp receipt: `.ufo/waves/round-32/a2after/timestamps-strict-at-9ef97f08.txt`
- Disk-command evidence: `.ufo/waves/round-32/a2audit/A2AttemptForensics.md:77-83`
