# CritBand — r52-w1 attack on the round shape

Verdict: the round shape is NOT sound as written. Two high-severity gates pass defects they
claim to catch (interpolation check, never-started seats), one binding rule is contradicted by
the claims (residual `task` call), and items 9..31 have no compliant route. Full numbered
findings (F1–F13, severity, evidence, fixes): `.ufo/waves/round-52/w1/CritBand/findings.md`.
Receipts (11, with command, exit, stdout sha256, UTC): `.ufo/waves/round-52/w1/CritBand/probe-receipts.txt`.

## Most important

1. **F1/F2 (HIGH) — interpolation check is vacuous on the spawning artifact and blind to common
   forms.** `check-dispatch.py` scans only spec-shaped `context`/`items`. A rendered dispatch with
   planted `{LANE}`/`{UNRESOLVED_X}` in `taskCall` returns clean (exit 0). Lowercase `{lane}`,
   single-char `{X}`, and angle `<BASE>` (used live in an executable command) also pass.
2. **F3 (HIGH) — never-started seats are invisible.** `wave-accounting.py` enumerates directories,
   so a seat with no directory is absent from output; `--check` exits 1 but does not name the
   failing seat. The r51 "dead seats stay dead in the evidence" lesson is not kept for this case.
   Partial/truncated JSON and missing status files ARE visible (verified).
3. **F6 (MED→binding conflict) — residual `task` call is prohibited.** Claims route a <=8-seat
   residual through a `task` call; addendum §6 (lines 140–142) forbids the L1 calling `task` for a
   wave or residual. A <=8 wave also fits neither listed shape (v2 waveMinLanes 64; v1 32).
4. **F7/F8 (HIGH) — falsify route.** Items 9..31 have no compliant path. A v2 w1 + v1 falsify is a
   mixed round the addendum's shape rule does not list.

## Answers

- Round total <=128: holds for every defined outcome (96..128 with a falsify of 32..64; 65..72
  with a residual), but no tool enforces it (F9).
- Attack share: definition used = reviewer, critic, mutation-tester, labrat, sentinel, revenger.
  w1 = 24/64 = 37.5%. Round-wide >=25% holds only with an attack-heavy falsify: a zero-attack
  falsify of 33+ seats drops the share below 25% (F12; three definitions are in circulation).
- Dead/partial status.json: partial JSON and missing files are visible; never-started and
  `blocked` are not (F3, F4). Roles are self-reported and disagree with the spec for 7 seats (F5).
- Falsify <32: unresolved by the claims (F7); the residual conflicts with the addendum (F6).

## Other findings (MED/LOW)

F4 `--check` passes `blocked`; F5 self-reported roles; F9 cap unenforced; F10 30 of 64 dispatch ids
carry runtime suffixes, 28 reuse round-51 seat names (name collision); F11 four artifact references
do not exist and three summaries exceed 40 words; F12 attack-share definition unfrozen; F13 dispatched
text carries trailers the spec does not.

## Verified clean

Spec has no `{UPPER}` placeholders (64 prompts + context). `LOG.md` carries `646d29c9` (r51
spotcheck item 1 resolved). `SHONEN.md` body equals the PROTOCOL seed with `<name>` substituted
(r51 spotcheck item 2 resolved). r51 spotcheck item 3 (C3 freeze-drift gating) is NOT evidenced in any
round-52 draft I read; left open for the L1.

## Snapshot caveat

Read mid-wave (59 seat dirs, 49 settled at last read). ExecCounterV2 failed, ExecControls and
ExecFetchVendor blocked at that read — the freeze-critical seats, for the L1 to act on.

## Scope and tooling

Read-only on the lane. Wrote only under `.ufo/waves/round-52/w1/CritBand/` and this file. No commit,
stage, stash, or push. No REA, no `--data-run`, no vendor download, no spawn. Tooling installed: none.
Fleet-root `git status --porcelain` shows two modified tracked files (`.scratch/goal-20261029-hyaku-run12.md`,
`.ufo/l0-questions.md`) and no untracked strays; not touched by this seat.
