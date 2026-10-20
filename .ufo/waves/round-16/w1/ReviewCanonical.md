# ReviewCanonical — SHONEN canonical seed and historical box-3 wording (round 16, w1)

Scope: read-only review of `SHONEN.md` (HEAD `6235498`, plus the uncommitted worktree edit), the protocol seed, and the anchors each box cites. No gate or probe was executed; all checks were reads (`read`, `grep`, `git show`/`diff`/`log`). No `[x]` authority is asserted or recommended; all four marks stay `[~]`. No numeric score is proposed.

## Current state (observed)

- HEAD `SHONEN.md` (12 lines) still reads `this round executed …` at line 10. This is the round-15 routed defect 4 (`corpus/lessons/round-15-verifier-spotcheck.md:188`).
- The worktree is modified: `git status` shows ` M SHONEN.md`, with a one-line change at line 10. It now reads `historical 2026-10-15 operator-steered round 1 executed …`. `grep 'this round' SHONEN.md` returns 0 hits and `[x]` returns 0 hits. Box text, title, and marks are unchanged, so the edit is evidence-line-only. Nothing is committed.
- Other uncommitted files are also modified by siblings or the integrator (`SKILL.md`, `corpus/QUALITY.md`, `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`). Only the SKILL edit touches a cited range (see Verified below).

## Findings (severity order)

**F1 — medium, integration blocker. Box-3 "this round" is defective at HEAD; the fix exists only in the worktree.**
- Anchor: HEAD `SHONEN.md:10`; worktree `SHONEN.md:10`.
- The HEAD wording is the exact defect routed at `round-15-verifier-spotcheck.md:188`. The round-16 claim C2 (`.ufo/waves/round-16/claims.json:12`) is discharged only if the worktree line is committed.
- The worktree wording is correct. It names the historical round, keeps `corpus/lessons/2026-10-15-round-1.md`, and keeps the `historical audit claims are not current outside verification` clause.
- Action for L1: commit the one-line `SHONEN.md:10` change with a LOG entry (`LOG.md` is append-only). Do not change marks.

**F2 — medium, cross-document contradiction. A live corpus entry says the four gates are "closed".**
- Anchor: `corpus/knowledge/2026-10-14-r14-02-final-sweep.md:149-151`: "The four SHONEN gates are closed with named non-author verifier evidence (SHONEN.md:11-18 …)".
- This contradicts the current seed (all four `[~]`), `LOG.md:1919` ("All four SHONEN marks remain author-only `[~]`"), and `round-15-verifier-spotcheck.md:192` ("SHONEN boxes are **not all independently established**").
- The entry's own status line ("records eligibility only") and its box-4 caveat qualify only part of this. `SHONEN.md:11-18` no longer exists as a 6-line-plus-footer seed; the file is 12 lines.
- Recommended: a dated append-only correction in the corpus/LOG, not an edit to the committed entry.

**F3 — low-medium, calibration. Box-1 verifier disclaimer was weakened in an undisclosed edit.**
- Anchor: `SHONEN.md:6` at HEAD and in the worktree reads `…; no promotion verifier.`. Before commit `856d193` it read `…; no identified outside verifier.` (`git show 856d193 -- SHONEN.md`, the `-`/`+` pair on that line).
- Box 2 (`SHONEN.md:8`) still says `no identified outside verifier`, so the boxes are now inconsistent.
- `grep` of `LOG.md`, `SCORECARD.md`, and `corpus/lessons/round-15*.md` finds no disclosure of this wording change. `LOG.md:1868-1870` discloses only the 17/17 footer move.
- Recommended: restore `no identified outside verifier` on line 6, or disclose the change in LOG. Either is mark-neutral.

**F4 — low, calibration. Box-4 evidence line is undated and partly stale.**
- Anchor: `SHONEN.md:12`: "province-version alignment **is contested** by the 6.5.0/207/v42 observations in `corpus/lessons/2026-10-15-round-1.md`".
- The lesson's observations are 2026-10-15 values. The lesson's Kimi pin was 6.4.0 (`round-1.md:80-83`). Current `PROVINCE.md:12-25` records Kimi 6.7.0, re-read 2026-10-18/19.
- The present tense overstates currency. Recommended: "as observed 2026-10-15".
- Range note (not a defect): `PROVINCE.md:88-116` spans the Frontier bullets (88-93) and the Adjacent header (95). The load-bearing refusal bullet sits at 114-116 and is verified verbatim there.

**F5 — low, stale pointer text. Gate note and historical references.**
- `.ufo/gates/citation-drift/pointer-table.json` note on `shonen-skill-range` says "13/13 count"; box 1 says 17/17. The needle still matches (`SKILL.md:233` is inside 81-314), so this is only stale note text.
- Historical records cite `SHONEN.md:11-18`, `SHONEN.md:18`, and `PROTOCOL.md:430` (`LOG.md:141-151`, `corpus/knowledge/2026-10-14-r14-02-final-sweep.md:150-151`). The protocol seed now sits at `PROTOCOL.md:446-465`. These are historical and should not be rewritten; a dated note suffices.

**F6 — info. Box-2 evidence path differs from the run record; the box-2 qualifier should stay.**
- `evidence/round-1-2026-10-15/result.json:120-130` records `fresh_bundle: ".ufo/rounds/interactive-r1/rea-bundle.json"`. Box 2 cites `evidence/round-1-2026-10-15/rea-bundle.json`, which exists and contains `ev_f5e5da50…` and subject `7e8bccc6…`. The seed does not cite the `.ufo` path, so this is a record-level inconsistency only.
- Box 2 says "end-to-end domain task". The evidence is one instruction decode (`0x117070`, ENDBR64) plus open/export/close, and the lesson itself says "one retained holding, not all holdings" (`round-1.md:140`). The box text is canonical and cannot change, so the evidence line's "Executed native smoke" qualifier must stay.

## Verified (by reading; not gate-executed)

- Seed form: title `# kaidoku-shokunin — Promotion checklist` matches `<name>` = directory name. The four box texts match the protocol seed (`kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:455-462`) and the mint template (`templates/mint/SHONEN.md:7-14`) by reading, not by diff. Marks are `[~]` only.
- Box 1 range: `SKILL.md:81` is the `## Queue-drain craft` heading and `SKILL.md:319` is the next section. 17 `- **` rule bullets fall in the range at HEAD and in the worktree. Needle `A mitigation claim carries its natural control` is at `SKILL.md:233`. SKILL worktree edits are single-line at 450 and 487, outside the range. Pinned commit `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22` exists.
- Box 3 execution claim: `SCORECARD.md:172` records command B executed for both revisions (0/9 → 9/9). `result.json` `controls` records recipe A independently executed, both revisions, 9.72/10.0.
- Box 4 anchor: `PROVINCE.md:114-116` is the refusal bullet, verbatim.
- The worktree edit changes line 10 only, so line-keyed pointers at lines 6 and 12 are unshifted.

## Residual risk and verification gaps

- No gate or probe was executed (per assignment). L1 should run once after integration: the citation-drift strict probe (`.ufo/gates/citation-drift/`) and a byte diff of `SHONEN.md` against the protocol seed block modulo `<name>`. The probe's `shonen-*` needles are the mechanical check I could not run.
- The seed-vs-template identity is by reading. A byte diff is needed to confirm it.
- Whether the worktree line-10 edit was authored by the integrator or a sibling was not verifiable from git (uncommitted). L1 should confirm authorship before committing.
- No tool install or update was performed.
