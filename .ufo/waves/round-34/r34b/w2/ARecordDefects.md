# ARecordDefects — re-derivation of the five disclosed record defects at `cd75b92e`

Seat: `L1Kaidoku34-2.ARecordDefects` (reviewer, Godspeed, leaf — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Scratch:
`/fast/scratch/hyaku/kaidoku-r34b/w2/ARecordDefects/` (`lane/` = `git clone --shared` at `cd75b92e`, `p3/`,
`p4/`, `p5/` = disposable instrument copies).
Subject: the five record defects `F1..F5` in `.ufo/waves/round-34/r34b/claim-stop.json` (blob `e6303d06…`, landed
`cd75b92e`). Method: re-derive each from **committed bytes** and from bounded probes, not from the stop's prose or
from wave-1 reports.

Revision facts (read-only):
`cd75b92e583735729546b0ea3b250f2df6d0652a` is the stop commit; its tree carries `claim-stop.json` + the three
`CtlMultiset-files/*.py` only. The lane tip moved **during** this audit to `66b840274390d0868c913a544947f9eb40a4ffe6`
(= `origin/main`, "land the stopped claim's record — SCORECARD section, LOG entry, lesson M34-5..M34-11, …"), which
does **not** touch `tools/round-34/`, `claims.json`, `instruments.json` or `claim-stop.json`
(`git diff --stat cd75b92e HEAD -- tools/round-34 …/claims.json …/instruments.json` → empty, exit 0, 07:34:08Z).
No post-freeze amendment of frozen bytes exists at either tip:
`git diff --stat c79bbe7b cd75b92e -- tools/round-34 .ufo/waves/round-34/r34b/claims.json` → empty, exit 0 (07:33:05Z).

## 0. Axes (named before probing)

| axis | proxy | direction |
|---|---|---|
| A1 re-derivability | does the defect reproduce from committed bytes / from a run of committed instruments, without trusting a report? | more reproducible = better |
| A2 state | still true / resolved by a later commit / false | true = the stop's disclosure is honest |
| A3 reach at the counting command | does the defect let the documented counting command print `GATE_COUNTER_OK` on bytes the claim does not freeze? | more false-green = worse |
| A4 repair sufficiency | does the repair the stop names close A3? | more closure = better |

Baseline control (so every mutant below is readable): on a clean clone at `cd75b92e`, the documented counting
command reproduces the frozen verdict and the committed receipt field-for-field except the argv echo:

```
python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . \
  --rev cd75b92e583735729546b0ea3b250f2df6d0652a --json-out …/P0-baseline.json
→ exit 0, 07:33:14Z–07:33:20Z
  GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3
  red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-
```
Leaf-field diff vs committed `after/c2-at-instruments.json`: keys identical, **29/30 fields equal**, only
`measured_revision` differs (mine `cd75b92e…`, committed `c79bbe7b…`) — i.e. the frozen instrument bytes behave
identically at the stop commit.

## 1. F1 — declarative pins — **STILL TRUE**

Stop text: *"claims pins live under `claims[0].pins`; `tools/round-34/freeze-integrity.py` requires a top-level
instruments map and exits 3 `instruments_missing`; no instrument hashes a pinned file."*

Re-derived, all three clauses:

1. **Container shape.** `claims.json` top-level keys are
   `[attempt, base_revision, claims, declared_at_utc, inherited_tip, instrument_notes, lane, planner,
   retained_claim, round]` — **no `instruments`**; the 26 pins sit at `claims[0].pins` (python/json read, 07:32Z).
2. **The lane's own verifier still rejects it** (run against committed bytes in the clone):
   ```
   python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34/r34b \
     --rev cd75b92e583735729546b0ea3b250f2df6d0652a
   → exit 3, 07:29:42Z
     freeze-integrity: ERROR schema code=instruments_missing \
       claims=.ufo/waves/round-34/r34b/claims.json where=instruments
   ```
3. **No R34-C2 runtime instrument hashes a pinned file.**
   `grep -n "instruments|claims.json|sha256|hashlib" tools/round-34/c2-shortcut-gate-counter.py tools/round-34/replay-gate.py`
   → **no match, grep exit 1** (07:33Z). The only `hashlib` uses in the C2 surface are `mini-counter.py:114,127`
   (opaque-path naming, not pin checks); `naive-counter.py` and `build.py` have none. (The R34-C1
   `version-needs-counter.py` does hash pinned paths, but it is not part of this counting command.)
   Demonstrated by drift: a green config dropped to three classes hashes `2b7c419f…` (pin `4483f385…`) and still
   returns `GATE_COUNTER_OK` exit 0 (P3, §3); a count-preserving path swap hashes `c688ac12…` and still returns
   `GATE_COUNTER_OK` exit 0 (P5, §3).

What *did* change: the repair container exists and its values are true.
```
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34/r34b \
  --claims .ufo/waves/round-34/r34b/instruments.json --rev cd75b92e583735729546b0ea3b250f2df6d0652a
→ exit 0, 07:29:42Z
  freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=cd75b92e583735729546b0ea3b250f2df6d0652a
```
`instruments.json` map == `claims[0].pins` (26/26 byte-identical, 0 conflicts), `frozen_claims_sha256`
`de3afbfb61d7…` recomputes exactly, and all 26 digests equal the bytes at `cd75b92e` (0 mismatches; the five
load-bearing blobs hashed from `git show`: counter `41d59703…`, gate `8fa94b23…`, mini config `4483f385…`, naive
config `72b12941…`, mini-counter `43ef669f…`).

But the container is **not enforced and not receipted**:
- its own "freeze" commit is `b917ea64` (2026-10-25T04:22:31-03:00 = 07:22:31Z), i.e. **9 minutes after** the
  production/control receipts (07:13:21–07:13:52Z). The digests therefore bind post-run bytes; only the fact that
  they are byte-identical to the pre-run pins (claims `declared_at_utc` 07:11:52Z) keeps the record honest.
- no committed **receipt artifact** exists for that run: `grep -rl "CLEAN pins=26" .ufo/waves/round-34/` returns only
  two *prose* files (`w1/ScribeSkillRegistry.md` E16, `w2/AStopCompleteness.md`); no JSON under
  `.ufo/waves/round-34/r34b/` records the invocation.

→ **STILL TRUE**, both halves. The stop's `repair_landed` is accurate only as "a container that `freeze-integrity`
accepts"; its "+ freeze-integrity receipt over it" points at a report line, not a receipt.

## 2. F2 — predicate identity — **STILL TRUE**

Stop text: *"predicate identity false: claims/config sentence A vs counter/receipt sentence B; no instrument reads
the predicate value."*

```
A (claims[0].predicate, gate-config-mini.predicate, gate-config-naive.predicate):
  sha256 7c6c17f0cca6c680507d4eec33b4c0c82a76c4f73e9a98ceb4bde54a9a96279b, 237 chars, 31 words
B (c2 counter PREDICATE extracted by ast, after/c2-at-instruments.json predicate, controls/do-nothing.json predicate):
  sha256 8340aea51154fc0e4e2c00684a12893603677c5caa7769d7e63b70f5392611c8, 351 chars, 46 words
A == B → False        (07:29Z)
```
The frozen `claims[0].predicate_identity` still asserts *"The same sentence is the gate config's `predicate` field,
the C2 counter's PREDICATE constant and the receipt label"*; the receipt has **no `label` key**
(`after/c2-at-instruments.json` keys: `clauses, exit, finding, gate_path, gate_present, green, measured_revision,
met_target, mutants_killed, predicate, red, selftest_exit, selftest_failures, selftest_line, target`).

No instrument reads the value: the counter emits its own constant (`c2-shortcut-gate-counter.py:73`), and the gate
only tests for key *presence* (`replay-gate.py:43`) — it never compares `config["predicate"]` to anything. Both files
are byte-unchanged from `c79bbe7b` through both later tips.

→ **STILL TRUE**; nothing was repaired (the stop says so: "disclose only"). Note for traceability: the stop's own
`predicate_frozen` field quotes **A**, while the receipt it cites in `frozen_counter_verdict` carries **B**; only the
stop's `predicate_note` explains the mismatch.

## 3. F3 — class drop invisible — **STILL TRUE**

Stop text: *"removing classes down to the `MIN_SHORTCUTS` floor still returns CLEAN; nothing asserts the registered
set equals the pinned set."*

Probe on committed instruments, gate floor `MIN_SHORTCUTS = 3` (`replay-gate.py:31`, enforced at line 58), green
config reduced 7 → 3 classes (kept `string-scan`, `record-order-replay`, `label-memorization`; dropped `all-false`,
`size-keyed`, `fixed-slice`, `digest-keyed`):
```
python3 -I -B tools/round-34/replay-gate.py --root . --config tools/round-34/gate-config-mini.json
→ exit 0, 07:30:18Z
  REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=3 shortcuts_over_target=-
  rows=4 classes=['structural','string-scan','record-order-replay','label-memorization']

python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev cd75b92e… --json-out …/P3-counter.json
→ exit 0, 07:30:18Z–07:30:20Z
  GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 \
  red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-
  met_target=true  clauses all true  green.shortcuts_below_target=3
```
So the `kill_rule` sentence "no shortcut class may be dropped to reach CLEAN" is violated with **zero failing
clause**, at the floor, and the modified config's digest (`2b7c419f…`) is outside the pin map (`4483f385…`) with no
effect (§1).

Second, sharper probe (kills the count-only repair): 7 entries kept, but the `size-keyed` entry re-pointed at the
pinned-but-unregistered `readers/label_keyed.py`:
```
python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev cd75b92e… --json-out …/P5-counter.json
→ exit 0, 07:32:51Z–07:32:56Z, GATE_COUNTER_OK, all six clauses true, green.shortcuts_below_target=7
  config sha256 c688ac129dba9edbc56606f21646891a3003cfecc6f935322c3b49857dcb83ff (pin 4483f385…)
```
Count is preserved and the registered *content* changed; nothing notices.

→ **STILL TRUE**; no resolving commit (the six clauses contain no class-count/set member — verified by reading
`clauses` in the counter).

## 4. F4 — gate mutant M3 survives — **STILL TRUE**

Stop text: *"gate mutant M3 (ignore last shortcut row) survives its own selftest and turns the red case CLEAN."*

Rebuilt from the committed gate (`8fa94b23…`) with one anchor, `for item in config["shortcuts"]:` →
`[:-1]` (scratch copy `p4/`, sha256 `9ffbb7e9df0fa6a02da98cb4b6dacef79eeecb099002b8a94805b3d738b78844`, equal to the
sha wave-1 reported):

| probe | argv tail | UTC | exit | line |
|---|---|---|---|---|
| P4a selftest | `replay-gate.py --selftest` | 07:30:25–26Z | **0** | `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}` |
| P4b mutant on pinned red config | `replay-gate.py --root . --config tools/round-34/gate-config-naive.json` | 07:30:26Z | **0** | `REPLAY_GATE_CLEAN … shortcuts_below_target=6 shortcuts_over_target=-` |
| P4c pristine control, same config | `p3/…/replay-gate.py --root p3 …` | 07:30:26Z | **2** | `REPLAY_GATE_REFUSED … shortcuts_over_target=label-memorization` |
| P4d counter scoring M3 gate | `c2-…-counter.py --gate tools/round-34/replay-gate.py` | 07:30:28–30Z | **1** | `GATE_COUNTER_MISS … clauses_failed=red_refused` |
| P4e pristine, reordered config (over-target row in the middle) | `--config config-reorder.json` | 07:31:59Z | 2 | `REFUSED … shortcuts_over_target=label-memorization` |
| P4f M3, same reordered config | `p4/… --config p4/config-reorder.json` | 07:31:59Z | **2** | `REFUSED … shortcuts_below_target=1` (verdict identical → M3 undetected) |
| P4g M3 on green config | `--config …/gate-config-mini.json` | 07:32:19Z | **0** | `REPLAY_GATE_CLEAN … shortcuts_below_target=6` |

Reading: the gate's own selftest gives **zero** detection (`SELFTEST_CASES` places over-target readers only in slots
`s1`/`s2`; no case asserts `shortcuts_below_target` or `len(rows)`); the claim layer's `red_refused` catches M3 only
because the single over-target class happens to be the last row — reorder it and both layers are blind. The green
clause also passes with M3, so the surviving mutant is not confined to the red surface.

→ **STILL TRUE**. Caveat on the stop's evidence pointer, not on the defect: `w1/MutGateBranches.md` is **not in
`cd75b92e`** (`git cat-file -e` exit 128) and entered VCS only after the stop commit — in `98bcb34a` (parent
`cd75b92e`, committer 07:32:24Z, reachable only from `refs/jj/keep/98bcb34a…`, not from `main`) and on `main` at
`66b84027`; the blob is the same (`284e0283…`) in both. The defect itself reproduces from committed instrument bytes,
so it survives the pointer defect.

## 5. F5 — receipts unbound — **RESOLVED by `b917ea64`** (with a pointer-binding rider resolved only after the stop)

Stop text: *"receipts were untracked at first audit time"*, `repair_landed: b917ea64…`.

- Historically true: at the freeze commit the whole `r34b` tree is one file —
  `git ls-tree -r c79bbe7b --name-only …/r34b` → `claims.json` only; `git cat-file -e c79bbe7b:…/after/c2-at-instruments.json`
  and `…/before/c2-at-base.txt` → **exit 128** (07:33Z).
- Resolved: at `cd75b92e` every cited receipt/container path exists (`git cat-file -e` **exit 0** for
  `after/c2-at-instruments.{json,txt}`, `before/c2-at-base.txt`, the five `controls/*.json`,
  `instruments.json`, `predicate-reconciliation.json`). First-add commit of the after receipt:
  `git log --format='%h %cI' --diff-filter=A -- …/after/c2-at-instruments.json` → `b917ea64 2026-10-25T04:22:31-03:00`
  (07:22:31Z), whose subject says exactly "retain before/production/control receipts…".

Rider of the same class, true at `cd75b92e`, resolved only after it: two of the stop's five **evidence pointers**
were unbound at the stop commit — `w1/MutGateBranches.md` (F4) and `w1/RevFreezeOrder.md` (F5) were absent
(exit 128); so was `w1/ScribeSkillRegistry.md`, the only record of the freeze-integrity CLEAN over the F1 container.
`git log --all --diff-filter=A` for those paths returns nothing up to `cd75b92e`; they first appear afterwards in
`98bcb34a` (empty message, parent `cd75b92e`, 07:32:24Z, reachable only from `refs/jj/keep/`) and on `main` in
`66b84027`, with identical blobs. All three are present at `HEAD` (exit 0), and the committed
`MutGateBranches.md` blob is byte-identical to the worktree text I read (`e3d2e1ae…` file sha256; tree blob
`284e0283…` at both commits).

→ **RESOLVED** (`b917ea64`); the stop's own wording was scoped to the receipts and remains accurate as a historical
statement.

## 6. The proposed repairs, attacked

- **F1 — "byte-identical 26-pin container + freeze-integrity receipt".** Insufficient for A3: the documented counting
  command still consumes nothing pinned (drift probes P3/P5 return OK with configs outside the pin map), the container
  commit is post-run, and no machine receipt exists. Closing A3 needs the counter itself to re-hash each pin and exit 2
  before scoring — exactly what the wave-1 report recommended — plus a committed receipt file.
- **F2 — "disclose only".** Disclosure is honest but leaves a frozen file asserting a false identity and leaves every
  receipt's `predicate` field quoting a sentence the claim does not freeze. Any downstream quote of a receipt's
  `predicate` as "the frozen predicate" is false; the stop's `predicate_note` is the only mitigation.
- **F3 — "assert class count == pinned count before CLEAN".** Count is not identity: P5 keeps the count at 7 with a
  swapped path and stays CLEAN. Also, the "pinned count" has no reader today (F2 shows no instrument reads
  claims/pins), so a count constant would be self-referential in the same way the `PREDICATE` constant is. The
  sufficient form is set equality over `(class, path, sha256)`, or the config digest check — i.e. F3 is a consequence
  of F1 and cannot be closed by a count alone.
- **F4 — "red-last selftest case + row-count assertion".** `red-last` does kill M3 (over-target row in the last slot),
  and a row-count assertion kills row drops in any order — but only if the assertion lives in `evaluate()`, not merely
  in a selftest case, because the shipped red config's detection is order-coincidental (P4e/P4f). Neither change
  addresses the label-based exclusion that lets a re-labelled over-target reader print CLEAN, nor the class floor (F3).

## 7. Findings beyond the five (record-level, from committed bytes)

1. **R1 — numbering divergence.** `claim-stop.json` F1–F5 do not align with the numbering landed at `66b84027`
   (SCORECARD/LOG/`corpus/lessons/round-34.md` list six defects: pins, predicate, class drop, re-labelled
   `structural`, vacuous gate, `--rev` echo). F4 (M3 last-row survival) lands as lesson **M34-9**, while the docs' item
   4 is a different defect (a shortcut re-labelled `structural`). Anyone resolving "F4" from the docs lands on the
   wrong defect.
2. **R2 — repair overstatement.** F1's `repair_landed` names a "freeze-integrity receipt"; no receipt artifact exists
   (only prose lines in two reports). M34-5 repeats the phrasing.
3. **R3 — pointer binding was fixed late.** At `cd75b92e` two of five defect evidence pointers were uncommitted
   (§5 rider); they enter VCS only afterwards (`98bcb34a` on `refs/jj/keep`, `66b84027` on `main`).
4. **R4 — two tracked reports changed after the stop.** `66b84027` modifies `w1/ExecAntiVacuityProbe.md` (7 lines) and
   `w1/RevScopeNoHarm.md` (25 lines) relative to `cd75b92e`; the stop's record therefore binds text that was
   superseded. No effect on F1–F5's evidence (their cited reports are unchanged and now committed).

## 8. Residual risk and verification gaps

- **Not run:** the R34-C1 production reader and its twelve carriers (never executed, never opened as programs); no ELF
  or fixture was executed; `freeze-integrity.py --selftest` was not run (out of scope); the stop's decisive
  counterexample (`nameset.py`) was not executed — its committed digest does match the stop
  (`2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97`, worktree and `git show` concur, 07:33Z).
- **Not adjudicated:** the stop's soundness, the validity of its counterexample, any score, or any capability label.
  Nothing here reopens R34-C2 or repairs a frozen instrument.
- **Pin coverage of this seat:** digests of 9 named paths were taken from `git show cd75b92e:<path>`; the remaining 17
  pins were checked against worktree bytes while `git diff --stat cd75b92e -- tools/round-34 …/claims.json
  …/instruments.json` was empty, so worktree == blob for the whole instrument set.
- **VCS discipline:** only `git rev-parse/log/show/diff/ls-tree/cat-file/clone --shared` were issued against the lane;
  no add/commit/stash/checkout/reset/pull/push and no jj command. All mutation, mutation-testing and reader execution
  happened in `/fast/scratch/hyaku/kaidoku-r34b/w2/ARecordDefects/{lane,p3,p4,p5}`.
- **Tooling:** none installed or upgraded (`/usr/bin/python3` 3.14.8, `git` 2.56.0 already present); nothing to record.
- The lane moved to `66b84027` mid-audit; every probe above ran against a clone pinned at `cd75b92e` (clone
  `rev-parse HEAD` = `cd75b92e…`, `git status --porcelain` = 0 lines, 07:29:33Z).

## Verdict

```
RECORD_DEFECTS at=cd75b92e583735729546b0ea3b250f2df6d0652a
  F1=STILL_TRUE (instruments_missing exit 3; no runtime instrument hashes a pin; container CLEAN but post-run and unreceipted)
  F2=STILL_TRUE (A 7c6c17f0…/237ch ≠ B 8340aea5…/351ch; no instrument reads the predicate; receipt has no label key)
  F3=STILL_TRUE (7→3 classes: CLEAN, all six clauses true, shortcuts_below_target=3; 7-class path swap: CLEAN, count blind)
  F4=STILL_TRUE (M3 sha 9ffbb7e9…: selftest 12/12 exit 0, red case CLEAN exit 0, detection order-coincidental)
  F5=RESOLVED b917ea64ebbe (receipts tracked; pointers MutGateBranches.md/RevFreezeOrder.md bound only after the stop: 98bcb34a jj-keep / 66b84027 main)
  repairs=F1_F3_insufficient count-is-not-identity F4_needs_evaluate_level_row_count
  baseline_reproduces=exit0 29of30_fields_equal
```
