# R38ReviewerControlReplay — frozen-control re-score at freeze e059ca93

Seat: reviewer (leaf), kaidoku round 38 wave 1. Task: re-score the seven frozen control
receipts with the frozen counters at freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`,
running each receipt's recorded argv verbatim (only `--out` redirected to scratch — never
overwriting the frozen receipts), and compare exit codes. Rule under test: every control must
exit non-zero and `met_target` must stay false; a control meeting the target is a kill.

## Verdict

**ALARM — the control suite does not reproduce at the frozen revision.** All four C1-side
controls and `ctl-c2-0` reproduce exactly (counter exit 1, target not met). But
`ctl-c2-1`, `ctl-c2-2`, `ctl-c2-3` replayed against the freeze-revision bytes meet the
target (`met_target: true`, counter exit 0) — the kill condition for C2 — and the
freeze-revision generator's kill logic is inverted for all seven. The recorded receipts
(committed at `efd5c47a`) were produced by a *fixed* generator that landed in the same
commit as the receipts, one commit after the freeze; the counters themselves are frozen and
byte-identical throughout. The counter-side freeze is intact; the control-suite
reproducibility at the frozen bytes is not.

## Method

- Frozen bytes extracted from git objects, never the worktree:
  `git archive e059ca93… tools | tar -x -C $S/frozen` (freeze revision) and the same at
  `efd5c47a…` (receipts commit). Replay runs `python3 -I -B tools/round-38/gen-controls.py
  <kind> …` with each receipt's argv argument-for-argument, cwd = extracted tree,
  `--out` redirected to scratch, `HYAKU_SCRATCH`/`TMPDIR` inside seat scratch.
- Counters verified frozen: `c1-counter.py` sha256 `a7a62b0987090356…` and `c2-counter.py`
  `7f137b664984595e…` are byte-identical at `e059ca93`, `efd5c47a`, and `HEAD 9c9d496b`
  (`git cat-file blob | sha256sum`). The counters read only git objects
  (`git show REV:path`, c1-counter.py:23), so sibling worktree edits cannot contaminate a
  re-score. Receipt `exit` = the counter subprocess exit; gen-controls exits 0 when the
  control does not meet the target, 1 on kill (post-fix semantics).
- All 14 replay receipts + stdout/stderr are preserved at
  `.ufo/waves/round-38/w1/artifacts/R38ReviewerControlReplay/replay{A,B}/`
  (A = freeze bytes, B = receipts-commit bytes).

## Per-control table

| control | recorded exit | replay@e059ca93 exit | replay@e059ca93 met_target | replay@efd5c47a exit | replay@efd5c47a met_target | alarm |
|---|---|---|---|---|---|---|
| ctl-c1-0-do-nothing | 1 | 1 | false | 1 | false | none |
| ctl-c1-1-three-carriers | 1 | 1 | false | 1 | false | none |
| ctl-c1-2-wrong-handler | 1 | 1 | false | 1 | false | none |
| ctl-c2-0-do-nothing | 1 | 1 | false | 1 | false | none |
| ctl-c2-1-junk-count | 1 | **0** | **true (kill)** | 1 | false | **replay@freeze meets target** |
| ctl-c2-2-delete-bad-pointer | 1 | **0** | **true (kill)** | 1 | false | **replay@freeze meets target** |
| ctl-c2-3-substitute-other-document | 1 | **0** | **true (kill)** | 1 | false | **replay@freeze meets target** |

Corroborating detail:

- C1-side outputs are field-identical to the recorded receipts (modulo freshly minted fixture
  commit hashes for c1-1/c1-2, which are timestamp-dependent by construction); the lane-run
  controls c1-0/c2-0 reproduce including the exact `revision` field (`e059ca93…` / `77091b49…`).
  c1-1 still shows `carriers_matched: 3`, c1-2 `carriers_matched: 0` with the wrong-handler
  binding picture — the three C1 controls are live and discriminating.
- Replay@freeze fixture fingerprint: ctl-c2-1/2/3 all minted the **same** fixture commit
  `3cc1226227cf25611de6f3d2611a74b4216f72cf` (1 distinct tree for 3 supposedly distinct
  defects), with `assertion_mismatches: []`. Replay@efd5c47a mints 3 distinct trees and c2-1
  carries the junk assertion `stated [999,999] vs observed [3,3]`, matching the recorded
  receipt.

## Findings

**F1 (HIGH, blocks the control suite as frozen): degenerate c2 defect fixtures at the
freeze revision.** Frozen `gen-controls.py:199` calls
`c2_fixture(a.kind, a.kind.split('-')[1])`, passing defect `'1'`/`'2'`/`'3'`; `c2_fixture`
branches only on `'junk'`/`'delete'`/`'substitute'`, so all three fall into the final
`else` — the *pointer-repaired green* fixture. The counter then correctly reports
`mismatches: 0`, `guards_ok: true`, `met_target: true`, counter exit 0. Under the claims
doc's kill rule ("a frozen control meeting the target stops C2 before data"), re-scoring the
frozen suite at `e059ca93` stops C2 before any after-run. The three controls also stop being
controls at the freeze: they test the repair case three times and never exercise junk
counts, pointer deletion, or document substitution.

**F2 (HIGH): inverted kill signal in the frozen generator.** Frozen `gen-controls.py:217`:
`return 0 if res.get('exit') != 1 else 1` ("exit 1 = control met target"). Both counters
return `0 if res['met_target'] else 1` (c1-counter.py:276, c2-counter.py:264) — counter
exit 1 means target NOT met. The frozen logic therefore flags exactly the well-behaved
controls as failures (replay A: gen_exit=1 for c1-0/c1-1/c1-2/c2-0) and returns success
(gen_exit=0) for the three c2 controls that actually met the target. If the frozen bytes
were used as the wave gate, the gate would fire on good news and bless the kill. The
receipts commit `efd5c47a` fixes both F1 and F2 and regenerates all seven receipts — i.e.
the committed receipts are correct, but they are not reproducible at the revision the
round froze.

**F3 (MEDIUM, process): receipts committed one commit after the freeze they certify.**
`e059ca93` froze claims+counters without the receipts; `efd5c47a` ("control receipts … all
target-not-met") contains both the receipts and the generator fix that makes them true. A
verifier asked to reproduce "at the freeze revision" (as this seat was) gets three kills
that the receipts deny. Either the fix belongs inside the freeze commit, or the freeze
commit should not carry the generator at all.

**F4 (INFO, observation): worktree churn during scoring.** Mid-review the lane worktree's
`tools/round-38/c1-counter.py` became modified (uncommitted; worktree sha256 `733be016…` vs
committed `a7a62b09…` at all three revisions) — consistent with a sibling mutation lane in
flight. No conclusion in this report depends on worktree bytes; all scoring ran from
`git archive` trees. L1 should re-verify `git status` cleanliness of `tools/round-38/`
before integrating wave 1 so no seat scores mutated counters.

Routed-defect note: R37-CL1 (cite only committed bytes) is respected — the seven receipts
are tracked, clean, and match `efd5c47a`'s tree. This report cites only committed or
artifact-copied bytes.

## Residual risk and verification gaps

- I did not judge which revision is canonical for the wave gate (L1's call): if the gate is
  defined on `efd5c47a` bytes, the recorded receipts stand and F1/F2 are freeze-hygiene
  defects, not live kills; if defined on `e059ca93` bytes, C2 is killed by its own frozen
  controls and the claims doc's kill rule fires literally.
- Fixture commit hashes are timestamp-dependent; equality of `revision` across replay A's
  three c2 fixtures is exact (identical trees, same-second commits) but a slow machine could
  in principle mint equal trees under different hashes. The defect does not hinge on this:
  the `met_target: true` flip and empty `assertion_mismatches` are hash-independent.
- Out of scope here: carrier/oracle byte integrity, after-receipts, selftest case counts,
  and the c1 harness (`c1-run.sh`) — not part of the seven control argvs.

Tooling: no installs or upgrades performed (system `python3`, `git`, `node v24.21.0`;
`sasquatch-v4be` untouched). Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ReviewerControlReplay`
removed after copying artifacts.
