# ExecMutation — round-90 kaidoku, R90-C1 instrument mutation sweep (scoped findings)

Declared-case mutation table over the two round-90 instruments; each mutant is one exact
textual edit on a scratch copy, scored by the instrument's own `--selftest`. Full table,
per-mutant receipts and replay driver:
`.ufo/waves/round-90/w1/ExecMutation/receipts/` (long-form report:
`.ufo/waves/round-90/w1/ExecMutation/ExecMutation.md`).

## Result

**Killed 2 of 17.** Survivors (15), each with the missing case that would close it:

- M01 (repair:219, exact-total filter deleted) — no chain-gap (libz-shape) fixture; the
  single chain-valid candidate already equals u_len.
- M02 (repair:219, filter weakened to `<`) — same missing case, over-accepting side.
- M04 (repair:210, `derived == sc_p` skip deleted) — stored value never both chains and
  passes downstream filters; need a candidates-set assertion or such a fixture.
- M05 (repair:210, sz_unc bound deleted) — one successor only; need a second chain-valid
  successor with derived > sz_unc.
- M06 (repair:204-207, successor method-byte clause deleted) — need a size-plausible
  wrong-method decoy successor fixture.
- M08 (repair:270, found-None handoff → refusal) — need an input whose every l_info
  candidate has sz_unc0 == 0 (must still hand off, not refuse).
- M09–M17 (battery:188/435-437/439/440/441/448/450/148/447) — the battery selftest (8
  cases) never calls invoke()/score()/main-with-args, so every arms_ok/met/expect/window
  mutant survives by construction; each names a score()-level harness case
  (stray-file isolation stub, blind_ok=False persistence, no_work > 0, cheat arms,
  any-control-false ⇒ met False, wrong --expect ⇒ exit 1, method-byte window escape,
  P1 len(p1) ≠ 6 ⇒ met False).

Kills: M03 (strictly-greater `<=`→`<`) fails `intact-idempotent`,
`anchor-class-composed`, `last-block-before-stop-unrepaired` (a chain-valid candidate
past the true successor, derived 80 / total 400, repairs the intact fixture); M07
(block-0 handoff fallthrough → refusal) crashes `repair(clean)`.

## Reading

Battery survivors are a selftest-coverage boundary, not a counter defect: the battery's
kill power lives in its frozen four-carrier run. The repair selftest kills routing but
not derivation-filter mutants (unique-successor fixture + r89 intact fallback absorb
them); a chain-gap fixture and decoy-successor fixture would close M01/M02/M04/M05/M06
in the repair's own selftest.

## Commands

Baseline: `python3 -I -B <mirror>/tools/round-90/<instrument>.py --selftest` → rc 0
(17 / 8 cases). Per mutant: same command on the edited copy; exit codes and outputs are
in `receipts/mut-selftest/`. Replay from receipts alone: `receipts/replay-driver.py`.

## Limits

Selftest-only per assignment; the full four-carrier frozen battery was not run against
mutants. No tool installs. Lane originals untouched; scratch
`/fast/scratch/hyaku/kaidoku-r90/ExecMutation` removed after receipts were secured.
