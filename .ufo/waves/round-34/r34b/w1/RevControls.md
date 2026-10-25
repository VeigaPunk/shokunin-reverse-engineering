# RevControls — control audit (R34-C2 pre-freeze shortcut-replay gate)

Seat: `L1Kaidoku34-2.RevControls`, wave 1, round 34 run-6 re-dispatch.
Date of runs: 2026-10-25, 07:18:54Z–07:19:56Z. Host `linux 7.2.11-arch1-1`, `python3=/usr/bin/python3`.
Lane tip at audit time: `jj @` = `1f383c12970e` (working copy); instruments and receipts are pinned to `c79bbe7b0959132b9873ff3431cf5eb313b58b33`.

Scope: the five control receipts in `.ufo/waves/round-34/r34b/controls/`, their JSONs, and the four gate
copies in `.ufo/waves/round-34/r34b/controls/gates/`. Read-only on lane VCS; every execution below ran on a
byte-identical copy of `tools/round-34` under
`/fast/scratch/hyaku/kaidoku-r34b/w1/RevControls/root` (copy hashes equal the claims pins, see §Reproduction).
No ELF carrier, fixture or reader was executed as a program; only `python3` gates and the counter.
No tool was installed or upgraded (nothing needed).

## 1. Clause arithmetic — stored receipts

Computed from each stored JSON by re-deriving the six clause booleans from the receipt fields
(`c2-shortcut-gate-counter.py:112-119` is the arithmetic reproduced), not from the printed line:

| control | clauses (T/6) | failing clause(s) | exit | finding | meets target? |
|---|---|---|---|---|---|
| `do-nothing` | 0 (key `clauses` absent) | `gate_present` (implied by `finding=gate_absent`) | 2 | `gate_absent` | no (`met_target:false`) |
| `gate-always-clean.py` | 4/6 | `red_refused`, `selftest_clean` | 1 | `shortcut_gate_miss` | no |
| `gate-junk-clean.py` | 5/6 | `red_refused` | 1 | `shortcut_gate_miss` | no |
| `gate-no-positive-check.py` | 4/6 | `mutants_killed`, `selftest_clean` | 1 | `shortcut_gate_miss` | no |
| `gate-vacuous-no-floor.py` | 5/6 | `selftest_clean` | 1 | `shortcut_gate_miss` | no |

Clause-to-field agreement was checked for all four scored controls (selftest, mutants, red, green, positive:
all `True`). **No control accidentally meets the target.** The maximum is 5/6, reached by two controls; in
both the missing clause is not the one the frozen control plan names (F3, F4).

Inputs: `.ufo/waves/round-34/r34b/controls/do-nothing.json`,
`gate-always-clean.py.json`, `gate-junk-clean.py.json`, `gate-no-positive-check.py.json`,
`gate-vacuous-no-floor.py.json`; clause arithmetic at `tools/round-34/c2-shortcut-gate-counter.py:112-119`;
target at `:28`.

## 2. Per-control: does it genuinely skip the claimed work?

**2.1 `do-nothing` — yes, skips all three phases.** The counter early-returns at the `gate_present` test
(`c2-shortcut-gate-counter.py:74-81`) before the selftest, the red run and the green run. Nothing executes.
Receipt: `controls/do-nothing.json` (`gate_present:false`, `finding:gate_absent`, exit 2); stdout
`controls/do-nothing.txt`. The path `tools/round-34/absent-gate.py` is genuinely absent from the lane
(`test -e tools/round-34/absent-gate.py` → `ABSENT`).

Caveat (F5): the frozen control plan (`claims.json`, `control_plan[0]`) says "pinned counter **against a root
with no gate**", but the executed command kept the pinned gate present in the root and instead pointed
`--gate` at an absent path. That exercises only the absent-path branch. Independently reproduced the plan's
stated state — a root with `tools/round-34/replay-gate.py` deleted and the **default** `--gate` — at
2026-10-25T07:19:47Z: `exit=2`, `GATE_COUNTER_UNEVALUABLE finding=gate_absent ... gate_path=tools/round-34/replay-gate.py`
(`/fast/scratch/hyaku/kaidoku-r34b/w1/RevControls/out/nogate-default.{txt,json}`). Conclusion survives; the
filed receipt does not evidence the claimed root state. Also note exit 2 is shared with
`REPLAY_GATE_REFUSED`; do-nothing is only distinguishable by `finding=gate_absent`.

**2.2 `gate-always-clean.py` — no, it is a decision-branch mutant, not a work skip.** It is
`replay-gate.py` with `if over:` → `if False:` (one hunk, line 124; diff below). It still runs its full
12-case self-test and both configs over the eight fixtures against the real counters. Receipt:
red `exit 0 / REPLAY_GATE_CLEAN / classes_over_target []` while the naive config's `label-memorization`
reader meets target — the refusal branch is dead; `selftest_failures=2` (`red-one`, `red-two`).
`controls/gate-always-clean.py.json`.

**2.3 `gate-junk-clean.py` — yes, skips everything.** The file is an 11-line stub that prints a fixed
`REPLAY_GATE_CLEAN ... shortcuts_below_target=7` line, writes a fabricated payload with one
`{"class":"structural","matched":8,"met_target":true}` row, and fabricates the selftest summary
`{"cases":12,"failures":0,"mutants_killed":3}`. It never spawns the counter or any reader. Consequences:
`green_clean`, `green_positive_meets_target` (`positive_matched=8` from the stub's own JSON),
`mutants_killed=3` and `selftest_clean` all pass **by assertion**; only `red_refused` fails (CLEAN where
REFUSED is required). `controls/gate-junk-clean.py.json`; the stub is
`controls/gates/gate-junk-clean.py:5-10` (fabricated selftest at 5-7, fixed CLEAN line at 8, fabricated
`structural matched=8` payload at 9-10).

**2.4 `gate-no-positive-check.py` — no, decision-branch mutant.** One hunk: `if not positive["met_target"]:`
→ `if False:` (line 119). Every reader still runs on both configs; only the positive-control UNEVALUABLE
branch is dead. Red is still refused (`label-memorization` present), all green clauses true, but its own
self-test catches it: `positive-below` fails and `mutants_killed=2` (see F3 for why 2 rather than 3).

**2.5 `gate-vacuous-no-floor.py` — no, config-floor mutant.** One hunk: the `MIN_SHORTCUTS` floor removed
from `load_config` (line 58). Everything executes; red and green are unchanged and both green clauses pass.
Only `selftest_clean` fails, via the case `two-shortcuts-unevaluable`. Closest control to an accidental pass
(F4).

## 3. Findings by severity

**F1 [High] — the control evidence is uncommitted and hash-unbound.**
- `jj status` at 2026-10-25T07:19Z lists `? .ufo/waves/round-34/r34b/controls/` (untracked). At the frozen
  commit, `jj file list -r c79bbe7b | grep r34b` returns only `.ufo/waves/round-34/r34b/claims.json` — no
  receipt existed at the freeze, and none is tracked now.
- No control receipt records a gate hash, a command line, a root, or a UTC timestamp. The four scored
  receipts carry `{clauses, exit, finding, gate_path, gate_present, measured_revision, met_target,
  predicate, red, green, selftest_*, target}`; `do-nothing.json` carries the same minus `clauses`,
  `red`, `green` and `selftest_*`. None carries a content digest.
- `measured_revision` is a caller-supplied echo: `--rev` is copied into the receipt at
  `c2-shortcut-gate-counter.py:73,80` and never checked against the gate bytes; neither the counter nor the
  gate contains `hashlib`/`sha256` (grep, no hits).
- The sole current binding is this seat's out-of-band reproduction (§4) plus the pin table in
  `claims.json`, which I verified against both disk and the frozen commit:
  `jj file show -r c79bbe7b tools/round-34/{replay-gate.py,c2-shortcut-gate-counter.py,gate-config-mini.json,gate-config-naive.json} | sha256sum`
  = `8fa94b23…7558`, `41d59703…a5a72`, `4483f385…ac9c`, `72b12941…1428`, all equal to the `pins` values.
  Without that external check the receipts are attestations by the same process they attest.

**F2 [High] — two of six clauses have no negative control, and both are forgeable.**
No control in the set makes `green_clean` or `green_positive_meets_target` false. `claims.json`
`control_plan[3]` promised "gate whose positive control is all-false -> green clause fails"; the implemented
`gate-no-positive-check.py` disables the *decision* on a real positive control, leaves
`positive_matched=8`, and fails `mutants_killed`/`selftest_clean` instead. So the executed control does not
test the clause it was designed for. Worse, `gate-junk-clean.py` passes both green clauses with a fabricated
payload: `green_positive_meets_target` only compares `positive_matched == 8`
(`c2-shortcut-gate-counter.py:118`), a value any stub can print. The green side of the predicate
("identity-defeating counter … every registered shortcut class stays below target") is therefore asserted,
not demonstrated, by the filed controls.

**F3 [Medium] — `mutants_killed=3` in two controls is a vacuous kill.**
`MUTANTS` mutations use `source.replace(needle, replacement, 1)`. In `gate-always-clean.py` the code branch is
already `if False:`, so the needle `if over:` survives only inside the MUTANTS table (line 166); the generated
"mutant" differs from the gate under test by exactly one table line (verified: single line diff at 166) and
produces byte-identical output (`gate-always-clean gate exit=3 out=…config_shortcut_count…`,
`mutant exit=3` same string). Same for `gate-vacuous-no-floor.py` (needle survives at line 169; mutant == gate
under test, both `exit 0 / REPLAY_GATE_CLEAN` on my two-shortcut config). The kill is counted because the
mutated expectation (`expected_exit`) differs from the already-mutated gate's own behavior, not because a
mutation was detected. `gate-no-positive-check.py` is the honest case: its needle is escaped in the table, so
it is genuinely absent, the selftest records `no-positive-check-anchor-missing`, and `mutants_killed=2`.
Production gate: all three needles first occur on code lines (`replay-gate.py:58,119,124`), so the production
`mutants_killed=3` is a real branch kill — this finding is about the controls' evidential value, not the
claim.

**F4 [Medium] — the vacuous control's predicted failure mode is wrong in kind, and its only discriminator is
self-reported.** `claims.json` `control_plan[2]` says "vacuous gate without the shortcut floor ->
UNEVALUABLE, MISS". The gate itself returns CLEAN: with a real 2-shortcut config
(`out/two-shortcuts.json`, mini-counter, target 8) `gate-vacuous-no-floor.py --config …` exits 0 with
`REPLAY_GATE_CLEAN` (2026-10-25T07:19:56Z). Only the self-test case `two-shortcuts-unevaluable` fails, and
that summary is text the gate prints about itself — the junk stub proves such text can be fabricated and
still satisfy `selftest_clean`. This is the exact seam the MutCounterClauses seat is probing; if
`selftest_clean` is dropped or forged, this control reaches 6/6.

**F5 [Low] — see §2.1**: do-nothing evidences the absent-path branch, not the "root with no gate" state;
its exit 2 collides with REFUSED.

**F6 [Low] — line/payload divergence is silently accepted.** `gate-junk-clean.py` prints
`shortcuts_below_target=7` while its payload yields 0 rows below target; the counter stores both
(`green.line` = 7, `green.shortcuts_below_target` = 0) and no clause notices, because verdicts and counts are
read from the payload (`c2-shortcut-gate-counter.py:96-109`). Production line and payload agree (7/7).

## 4. Reproduction (stored vs scratch) — the strongest evidence in this report

Copies used: `cp -a tools/round-34/. /fast/scratch/hyaku/kaidoku-r34b/w1/RevControls/root/tools/round-34/`
plus the four gate copies at `…/root/tools/round-34/gates/`. Copy hashes before running:
`8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558` (gate),
`41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72` (counter) — equal to the pins.

Command template, run once per control with `G` substituted (scratch cwd):
`python3 -I -B root/tools/round-34/c2-shortcut-gate-counter.py --root root --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --gate tools/round-34/gates/<G>.py --json-out out/<G>.json`

| run (UTC) | gate | exit | verdict line |
|---|---|---|---|
| 07:18:57Z | `gate-always-clean` | 1 | `GATE_COUNTER_MISS … selftest_failures=2 mutants_killed=3 red=REPLAY_GATE_CLEAN green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=red_refused,selftest_clean` |
| 07:19:19Z | `gate-junk-clean` | 1 | `… selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_CLEAN … clauses_failed=red_refused` |
| 07:19:22Z | `gate-no-positive-check` | 1 | `… selftest_failures=2 mutants_killed=2 red=REPLAY_GATE_REFUSED … clauses_failed=mutants_killed,selftest_clean` |
| 07:19:22Z | `gate-vacuous-no-floor` | 1 | `… selftest_failures=1 mutants_killed=3 red=REPLAY_GATE_REFUSED … clauses_failed=selftest_clean` |
| 07:19:19Z | `absent-gate.py` (`do-nothing`) | 2 | `GATE_COUNTER_UNEVALUABLE finding=gate_absent …` |
| 07:19:47Z | default path, gate file deleted | 2 | `GATE_COUNTER_UNEVALUABLE finding=gate_absent … gate_path=tools/round-34/replay-gate.py` |
| 07:19:49Z | production `replay-gate.py` | 0 | `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` |

Stored-vs-reproduced comparison (JSON parsed, `gate_path` removed because I placed the copies at a different
relative path; every other key compared): **IDENTICAL for all five** (`do-nothing`, and the four
`.py.json` receipts). Scratch receipts: `/fast/scratch/hyaku/kaidoku-r34b/w1/RevControls/out/*.json`;
stdout/stderr `.txt`/`.err` alongside. So the filed controls are reproducible beat-for-beat from the pinned
gate bytes — the receipts are not fabrications — while F1 (no self-binding, uncommitted) remains.

## 5. The `controls/gates/` leftovers: copies, not instruments

`sha256sum controls/gates/*.py`:
`fbb2eca6…dfce` (always-clean, 14903 B), `777013c2…8255` (junk-clean, 753 B),
`d0b03f1b…e341e` (no-positive-check, 14881 B), `0646a3df…e78a8` (vacuous-no-floor, 14868 B).
None equals the pinned instrument `8fa94b23…7558` (`replay-gate.py`, 14902 B, mode 0755 vs 0644 here).
Three are one-hunk mutants of `tools/round-34/replay-gate.py`:
- always-clean: `- if over:  # MUT-D` / `+ if False:  # MUT-D` (line 124)
- no-positive-check: `- if not positive["met_target"]:  # MUT-C` / `+ if False:  # MUT-C` (line 119)
- vacuous-no-floor: `- if not isinstance(shortcuts, list) or len(shortcuts) < MIN_SHORTCUTS:  # MUT-A` /
  `+ if not isinstance(shortcuts, list):  # MUT-A` (line 58)
One (junk-clean) is an independent 11-line stub sharing only the verdict vocabulary.
They are not listed in `claims.json` `pins` (`grep -c controls/gates claims.json` → `0`, grep exit 1), are
untracked, and live under the evidence directory, not the pinned tools path. Their only legitimate use is as
`--gate` inputs to the counter's explicitly control-only flag
(`c2-shortcut-gate-counter.py:69-70`: "Control only: score an alternative gate. Production runs use the
pinned default."). **They must never be cited as instruments**, and no receipt that names a
`.ufo/.../controls/gates/…` path may be used as a production measurement.

## 6. Residual risk and verification gaps

- Residual: `selftest_clean`, `mutants_killed`, `green_clean`, `green_positive_meets_target` are all
  satisfiable by a stub's own printed JSON (proved by `gate-junk-clean`), so the counter's refusal strength
  rests on `red_refused` and on the pin table binding the gate bytes. If a future round changes the counter's
  `--gate` or the pins without re-running the five controls, F2/F4 become live.
- Residual: `red_refused` requires `"label-memorization" in classes_over_target`
  (`:115-116`) — a class-name string, not a behavioral check; the junk stub could have printed it. Binding
  again rests on the pinned gate content, not on the counter.
- Gap: I did not run the stored gate files in place under the lane root (read-only rule); scratch copies are
  byte-identical and the receipts reproduced exactly, so this is not a material gap.
- Gap: I did not inspect how `tools/round-34/freeze-integrity.py` consumes the pin table (out of scope);
  my pin check was `jj file show -r c79bbe7b` + `sha256sum` + `diff` against disk.
- Gap: I did not run any ELF carrier and did not touch R34-C1's reader or its twelve carriers.
- Depth note for the MutCounterClauses seat: the load-bearing seams this audit found are `red_refused`
  (string + exit + payload class list), `selftest_clean` (self-reported), and the green pair
  (payload-only, no negative control). A counter mutation that drops `green_positive_meets_target` should be
  admitted by no control — predicted, not observed by me.

REV_CONTROLS_VERDICT: controls reproducible, none accidentally meets target (max 5/6); failing clauses —
do-nothing `gate_present`; always-clean `red_refused,selftest_clean`; junk-clean `red_refused`; no-positive-check
`mutants_killed,selftest_clean`; vacuous-no-floor `selftest_clean`. `controls/gates/*` are copies/mutants, not
instruments, and must never be cited as such. Green pair and selftest clause lack negative controls (F2) and
are forgeable; control receipts are uncommitted and hash-unbound (F1). No falsifier of the production
R34-C2 receipt from this seat; production gate on the pinned bytes scores 6/6 at 07:19:49Z.
