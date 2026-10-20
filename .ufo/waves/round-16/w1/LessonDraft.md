# Round 16 — LessonDraft report (w1)

scope: draft Mistakes rows for the four round-15 outside routes (`corpus/lessons/round-15-verifier-spotcheck.md:181-188`). Draft only; no existing doc was edited.
artifact: `.ufo/waves/round-16/w1/LessonDraft.candidate.md`
tools installed or updated: none. No checks, builds, tests or gates executed; reads and read-only greps/JSON parses only.

## Findings (each verified against source bytes read in this session)

1. **Invocation drift — confirmed, and wider than routed.** `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3` omits `-I` and uses a cwd-relative script path; the recorded execution (`.ufo/waves/round-15/verification.json`, commands `snapshot-inventory`, `inventory-determinism`) is `python3 -I <absolute path>`. The same no-`-I` form exists at `SKILL.md:487`, which the routed defect did not name. That extra line is this seat's finding, not closure-adjudicated.
2. **Supplemental baseline not discoverable — confirmed.** `SKILL.md:450` quote-fidelity row pins only `.ufo/waves/round-14/fixtures/expected.json`; `boundary-fixtures` has zero hits in `SKILL.md`. The file exists and its frozen run exited 0 in `verification.json`.
3. **Controls without producer — confirmed.** `.ufo/waves/round-15/no-harm-controls.json` carries no command, no producer key, and nothing in `.ufo/waves/round-15/` references it. Its values were reproduced by the closure's own session, not by a retained repo command.
4. **Historical SHONEN wording — confirmed.** `SHONEN.md:10` box 3 says "this round" while citing the round-1 lesson (2026-10-15). It is the only "this round" hit in the file.

## Authored vs closure

- Each of the four rows was missed by the authored side and captured by the independent closure's routed defects 1–4. The `SKILL.md:487` extension is the only item with no closure attribution.
- Closure seats are not the author's L2 seats; their reproductions do not turn the original author counts into retained invocations.

## Red-before

Four red-before command blocks (R1–R4) are in the candidate file. Predicted reds are inferred from bytes; the observed-by-this-seat values are: `grep -c boundary-fixtures SKILL.md` → 0; `grep -rl no-harm-controls .ufo/waves/round-15` → no hit; `grep -n 'this round' SHONEN.md` → line 10 only. L1 must capture the actual red outputs and exit codes before any edit.

## Limits

- The rows do not claim resolution; "resolved with reproducible command evidence" needs L1's post-fix outputs.
- SHONEN is a canonical seed, not append-only: change box 3 only at its next evidence-line update, and never change marks.
- Corrections to committed knowledge/lesson entries should be named append-only corrections (precedent: round-15 `Round-15 correction`).
- No numeric score, pass, or target capability is claimed.
