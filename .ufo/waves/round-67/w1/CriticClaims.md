# CriticClaims — round-67 w1 attack report

Seat: critic. Scope: falsify R67-C1 and R67-C2 by execution; no edits outside this directory.
Full attack detail and the clause-by-clause receipts are in `w1/CriticClaims/attacks.md`; every
receipt named below is committed under `w1/CriticClaims/receipts/` with its driver under
`w1/CriticClaims/scripts/`.

Verified first: freeze = first-add commit `3663e6b2…`; carry-in `cf705c53` and instruments
`39a91a99` are ancestors of the freeze; all pins match the freeze blobs; both predicates are
byte-identical across `claims.json`, the instruments' `PREDICATE` and the plan.

## Verdicts

- **R67-C2 — survives every attack.** Reproduced green on the shipped bytes
  (`receipts/score-c2.json`): `killed_before 0`, `survived_before 2`, `killed_after 2`, pristine
  counters 30/26 cases CLEAN, exit 0. The false-kill attack (a mutant failing `arm-true-bound`
  instead of the named `arm-false-bound`) is correctly **not** counted as a kill. The false-survive
  attack found a *new* survivor of the same class (see D2) but does not touch the literal predicate.
- **R67-C1 — falsified as frozen; unverifiable as it stands.** The frozen counter (`f78ed365…`)
  exits 2 for every input before any carrier clause: `receipts/score-c1-frozen-blob.json`,
  `unevaluable "gap-rule.json absent at freeze"`. The lane has since corrected the counter
  (`1e7fe7b7`) and disclosed the supersession (`6dcc447e`); on the corrected bytes the rule read
  passes (`receipts/probe-fixed.json`), so the claim is now evaluable but its positive half still
  needs the after-arm data.

## Findings, by severity

### 1. F0 — the frozen C1 instrument was dead on arrival (fatal; lane has corrected it)

`patch_engine()` passed the gap rule as an **absolute** path; the pinned engine reads it as
`git show <rev>:<path>`, which misses for an absolute path, so `measure()` raised
`gap-rule.json absent at freeze` before the carrier loop. Evidence: `receipts/score-c1-frozen-blob.json`
(exit 2), and `receipts/attack-A-B-c1.json` block A (`show_absolute_rule_at_freeze false` vs
`show_relative_rule_at_freeze true`). The before-arm could not catch it because `control()` never
calls `measure()` — the control and the after-arm did not share an entry point.

State now: `1e7fe7b7` makes the name lane-relative; `6dcc447e` re-pins the counter (`f78ed365… →
55decb51…`), adds atom `A10` and an `instrument_supersessions` entry. `tools/round-29/freeze-gate.py`
audits round-67 **CLEAN** at `6dcc447e` (`receipts/freeze-gate.json`) and **FLAGGED**
`INSTRUMENT_REVISED` at `1e7fe7b7` (`receipts/freeze-gate-at-correction.json`) — the round-24
pattern: CLEAN only after a self-disclosed post-freeze revision.

Two residual costs the L1 should state, not bury: (a) `A0` says "no claim amendment after this
file", but the container was amended after the freeze (pin, `A10`, supersession block) — the gate
sanctions the mechanism, so say "amended only through the disclosed supersession"; (b) the re-taken
before record (21:57:37) postdates the data-run commit `a4c1d0fc` (21:56), so the declared order
controls → data is inverted. The control reads only round-50 envelopes, so it is not contaminated.
Cheap hardening: emit the `counter {path, sha256}` block on the **unevaluable** path too — both
exit-2 receipts currently carry no instrument identity.

### 2. A — the `carrier_fresh_ok` drop is a no-op, and the plan's reason for it is false

The plan says a re-measurement of the same pins "cannot be fresh". Evaluated with the engine's own
`prior_pins()` at the freeze: the prior set is 18 pins from the round-41, round-49 and round-42
tables; **none of the four round-50 pins is in it**, so `carrier_fresh_ok` is **true 4/4**
(`receipts/attack-A-B-c1.json` block A). Dropping the clause changes nothing. The reuse is disclosed
in the plan's prose ("re-freeze", "on the same four pinned carriers") but not in the predicate.
Smallest correction: delete `DROPPED_CLAUSES` (keep all 23 clauses — they pass) and fix the plan
sentence; alternatively leave the counter alone (it is already superseded once, another edit costs
another disclosure) and correct the prose, noting the drop is a no-op. Latent engine gap worth a
lesson: `prior_pins()` never reads the immediately previous C1 freeze's own `carriers.json`, so a
genuine relabelling would pass all clauses.

### 3. B — `--score` cannot distinguish the round-67 rule from a laxer rule

Over the four committed envelopes, `v2`, a v2-with-symlinks-waived rule and an all-`required`-off
rule all score 4/4; only the red fixture (one symlink gap removed) separates them — v2 fails, the
lax rules pass (`receipts/attack-A-B-c1.json` block B). `--score` runs no such fixture and pins no
rule sha: `score()` records `sha256_file(rule)` (the **working-tree** file, while the model comes
from the freeze **blob**), and never compares it to the claims pin `e66ba0…`. Two more binding gaps:
the receipt's rule sha can describe bytes that were never scored if the worktree is dirty, and the
predicate's "2 of 4 under the round-50 rule" clause lives only in `control()` — the `--score`
receipt has no `gaps_ok_round50` field, so the after-arm cannot evidence that clause alone.
Exact detectors: (i) in `score()`, require the rule's freeze blob sha to equal the claims pin and
record the blob sha; (ii) in the landing gate, require `red_controls.round67_rule_still_fails true`
from `--control`; (iii) embed the round-50 control count in the score receipt, or name both commands
in the predicate.

### 4. D2 — the C2 repair rule is a class claim that a text-reading mutant defeats

A `recipe_a_equivalence` that never calls `subprocess` — it returns True iff the block **text**
contains `"mapped": 1` — passes the battery (rc 0, no failed cases) and blesses a lying block
(pristine: not equivalent, diff `knowledge_files`; mutant: equivalent, no diff, never executing).
`receipts/attack-C-D-c2.json` block D. The predicate's literal survivor (unconditional M2) is still
killed, so the predicate survives as worded; the **rule** ("a false-input case closes the survivor")
is falsified as a class closure: the shipped doctored fixture differs from the honest one only in
block text. Corrections: doctor the **data**, not the block text (byte-identical block, different
corpus), and/or add an `equiv-block-executed` sentinel case. `receipts/attack-C2-corrected.json`
block `D_correction` shows a no-run mutant keyed on text common to both fixtures *is* killed, which
is the behaviour the fixture pair must force.

### 5. C — no false kill in C2 (attack failed; guard confirmed)

A closure mutant returning `"passed": False` for every input fails `arm-true-bound` (rc 1) and is
**not** reported killed, because `EXPECTED_CASE` is `arm-false-bound`
(`receipts/attack-C2-corrected.json` block C). Limit to state in the close: the verdict is one case
wide per survivor and `--score` scores only the two mutants it builds — it is not a new-survivor
search. Dead end recorded: mutating the counter's own `--selftest` is invisible, because the battery
skips `closure-selftest-green` when `--closure` is passed.

### 6. C1 after-arm blocker (state, not a claim defect)

At `6dcc447e` the four `corpus/evidence/round-67/c1/<id>/after.json` are **untracked** (`git status
--porcelain` → `??`; `git cat-file -e HEAD:…/g7581/after.json` → rc 128); the data-run commit
`a4c1d0fc` carries only `run.json`. The engine reads receipts from git at `--rev`, so
`receipt_present` is false and `--score` must exit 1 until the after.json are committed. The
corrected counter is otherwise evaluable: `receipts/probe-fixed.json` reaches the package gate with
the rule read clean.

## Axis impact

- **coverage (C1):** the claim's own instrument could not measure it at the freeze; the surface move
  is currently evidenced by prose + the control, not yet by a score receipt.
- **depth (C2):** the two named mutants are killed; the class is not closed (D2), and the kill verdict
  is one case wide (C).
- **calibration:** the freeze disclosure mechanism worked (gate CLEAN after disclosure), but a dead
  score path passed the freeze because the before-arm never exercised it. A score claim's control
  must run the score entry point to its first input failure.

## What would change a verdict

- C1: a carrier clause false under v2 at the record, `met_target` false, or a non-zero score exit.
- C2: `killed_before > 0`, a kill whose failing case is not the `EXPECTED_CASE`, or a pristine
  counter not green.

Neither was observed for C2. C1 needs the committed after-arm data before any verdict is possible.

Receipts: `w1/CriticClaims/receipts/` (10 JSON files, hashed in `attacks.md`); drivers:
`w1/CriticClaims/scripts/`.
