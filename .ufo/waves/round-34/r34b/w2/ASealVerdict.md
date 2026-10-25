# ASealVerdict — non-author closure read, round 34 (run-6 re-dispatch, attempt 1), wave 2

Seat: `L1Kaidoku34-2.ASealVerdict` (critic, leaf). I authored no part of this round: not the
claim, the gate, the counter, the configs, the fixtures, the readers, the stop record or the
addendum. This is the final adversarial read of `.ufo/waves/round-34/r34b/claim-stop.json`
(sha256 `e6303d061da219bb100f3a9acfc7492c9880acc177c4b98f5b695392b5cbcbfc`, landed `cd75b92e`) and
of `claim-stop-addendum.json` (sha256 `d233c3eca813ebb72ba8ffca537513b28efa8a4e218b82d0c5776599b3d3bbec`,
landed `5a0435ff`).

Every run below is on a **copy** under `/fast/scratch/hyaku/kaidoku-r34b/w2/ASealVerdict/`. The lane
was read only (`git rev-parse/log/show/cat-file/ls-files/status`); no mutating VCS command, no lane
write except this report. No ELF carrier, fixture or reader was executed as a program of interest;
readers ran only as `python3` children of the frozen counters. `/usr/bin/python3` = Python 3.14.8.
No tool was installed or upgraded (no pacman/uv/npx/cargo transaction).

**Verdict up front: `ok+conformance-defect`.** The stop's substantive disposition is correct and
reproduces; three record-level conformance defects remain, all repairable append-only without
touching frozen bytes. Details in §3–§5.

## 0. Axes named (Godspeed)

| critic axis | proxy | harmful pole |
|---|---|---|
| C1 disposition soundness | does the stop's verdict follow from the frozen text + round contract? | a label the record cannot support |
| C2 receipt binding | can the quoted receipt be produced without the pinned instrument at the named revision? | an unbound receipt that reads as proof |
| C3 repair reach | does the proposed/landed repair close the demonstrated bypass? | a guard that passes its own bypass |

Lane axes touched (all remain 10 → 10; I award nothing): **depth** (the claimed capability is the
gate itself, so the gate's evidential weight is the axis surface), **calibration** (the admission
standard applied to the stop), **coverage** (none claimed or moved).

## 1. Baseline: the stop's counterexample reproduces (so the stop is not vacuous)

Scratch lane copy made 2026-10-25T07:29:19Z. Instrument bytes in the copy are byte-identical to
`HEAD` (pins verified: `replay-gate.py` `8fa94b2332a6…`, `c2-shortcut-gate-counter.py`
`41d597036eb6…`, `mini-counter.py` `43ef669ff6ea…`, `gate-config-mini.json` `4483f3852429…`).

```
cd /fast/scratch/hyaku/kaidoku-r34b/w2/ASealVerdict/lane
python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . \
  --control-reader .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py
```
exit **0**, `{"finding":"records_match","matched":8,"met_target":true,"target":8,…}`,
**2026-10-25T07:29:25Z**. `nameset.py` sha256 `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97`
== the stop's `source_sha256`.

Full reader matrix under the same frozen counter (2026-10-25T07:29:27Z), matched/target:

```
all_false 0/8   digest_keyed 0/8   fixed_slice 0/8   label_keyed 0/8
label_replay_full 0/8   record_order_replay 0/8   size_keyed 1/8   string_scan 0/8
structural 8/8 (exit 0)   nameset 8/8 (exit 0)   pathkey 0/8
```

So: all seven **registered** classes stay below target, the registered structural control meets it,
and one **unregistered** structure-blind class meets it. The stop's factual sentence
("the registered seven classes stay below the green target, but an unregistered structure-blind
class reaches it") is true. The addendum's decisive receipt also verifies: 4 runs
(`kaidoku-r34-mini-v1`, `alt-1`, `alt-2`, `alt-3`), all 8/8 exit 0, UTC 2026-10-25T07:34:01Z,
receipt sha256 `fa6e8f0913f96237948f691a8186755958d46eef05aac4051c9cf2815be44356` — matches the
addendum. Nothing below reopens that finding.

## 2. What is already fixed since `cd75b92e` (checked, not assumed)

- Evidence files cited by F4/F5 (`MutGateBranches.md`, `RevFreezeOrder.md`) were **absent at
  `cd75b92e`** (`git cat-file -e` → missing) and are **tracked at HEAD** (landed `66b84027`); the
  working tree is clean for `.ufo/waves/round-34/r34b/` and `tools/round-34` (2026-10-25T07:38:16Z).
- Addendum `F6` (deterministic seed + published transformed digest) is real and correctly routed to
  fresh content.
- Addendum `D1`/`D2`/`A5` corrections are consistent with the evidence I re-derived.

## 3. Finding 1 (critical) — the six-clause receipt is shape-fed: a gate that runs no reader, at the pinned path and at a nonexistent revision, returns `GATE_COUNTER_OK`

**Counterexample.** Take the production counting command, keep its default gate path, replace
`tools/round-34/replay-gate.py` in a scratch copy with a 1,226-byte mock that opens no file, runs no
reader and consults no counter, and pass an all-zero revision:

```
cd /fast/scratch/hyaku/kaidoku-r34b/w2/ASealVerdict/lane-fake   # copy of the lane at 07:29
sha256sum tools/round-34/replay-gate.py    # 3edb1b4880a6e10f5e528032c577033f886999ef31b590be24f37d2ba4e68395, 1226 bytes
python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . \
  --rev 0000000000000000000000000000000000000000 --json-out /fast/scratch/…/fakegate-fakerev.json
```

Observed **2026-10-25T07:37:41Z**, exit **0**:

```
GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3
red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-
measured_revision 0000000000000000000000000000000000000000
gate_path tools/round-34/replay-gate.py
```

The same counter on the pristine copy with the same all-zero revision also returns `GATE_COUNTER_OK`,
exit 0, `measured_revision=0000…` (**2026-10-25T07:32:31Z**). The pinned gate's sha is
`8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558`; the mock's is `3edb1b48…`; the
counter never compares them. `grep -c hashlib tools/round-34/c2-shortcut-gate-counter.py` → **0**;
`grep -cE '\bgit\b|\bjj\b'` → **0**. `--rev` is written straight into the receipt (`:73`), and
`--gate` is a production-legal override (`:69-70`, help "Control only", nothing enforces it).

**Evidence pointers.** `after/c2-at-instruments.json` (`measured_revision`, `gate_path`,
`clauses`); counter `:73`, `:108-120`; `claim-stop.json:frozen_counter_verdict.note` ("the six frozen
clauses hold on the frozen bytes"). Independent prior art: `w1/CritCounterLimits.md` §5 (probe E,
1,979-byte mock, 07:22:04Z) and §6 (probe G, `deadbeef…`, 07:22:11Z); `corpus/lessons/round-34.md`
M34-10; `corpus/QUALITY.md` #72.

**Why it is a finding against the record.** The stop's five disclosed defects do **not** include it,
and the addendum (which adds F6) does not add it either. F1 says "no instrument hashes a pinned
file"; the operative consequence is stronger and unstated in the stop: the **counting command itself**
establishes only that the file at the fixed path printed six expected shapes. The sentence "the six
frozen clauses hold on the frozen bytes" is established by the w1 manual sha256 sweep and by the
addendum's separate `freeze-integrity` receipt — not by the receipt it points at. A reader of
`claim-stop.json` alone cannot tell the difference.

**Impacted axes.** C2 (receipt binding) critical; depth (the capability's only positive artifact loses
its independent evidential weight); calibration (the stop's own receipt standard).

**Smallest safe correction.** Append (never edit) a stop-record correction naming the mock-gate and
rev-echo probes with argv/exit/UTC, and mark `measured_revision`/`gate_path` in the receipt as
`caller_asserted` until the counting command re-hashes the 26 pins and resolves `--rev` (the step
QUALITY 72/73 already require). No clause, target, predicate, class or score changes.

## 4. Finding 2 (high) — the F3 repair sentence is count-only and is defeated by a count-preserving class swap; the durable guard already says "count, names, digests"

**Counterexample.** The stop's F3 repair reads: *"route: assert class count == pinned count before
CLEAN (next instrument)"*. Keep the count at seven and swap one registered class for another:

```
# /fast/scratch/…/lane-swap/tools/round-34/gate-config-mini.json
# record-order-replay → {"class":"payload-keyed","path":"tools/round-34/mini-fix/readers/string_scan.py"}
# classes_before 7 [... 'record-order-replay' ...] | classes_after 7 [... 'payload-keyed' ...]
cd /fast/scratch/hyaku/kaidoku-r34b/w2/ASealVerdict/lane-swap
python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . \
  --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out /fast/scratch/…/swap.json
```

Observed **2026-10-25T07:34:32Z**, exit **0**:
`GATE_COUNTER_OK … green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`,
`green.shortcuts_below_target = 7`. A count assertion is satisfied while the registered set changed.

The second half is worse for reach: neither F3 nor F4 changes the green transformation, so the
decisive class is untouched by either repair. Under the frozen counter `nameset.py` is still
**8/8**; the validated replacement in wave-1 evidence is:

```
cd /fast/scratch/…/lane
python3 -I -B .ufo/waves/round-34/r34b/w1/CtlMultiset-files/mini-counter-fresh.py --root . \
  --control-reader tools/round-34/mini-fix/readers/structural.py --seed w2-aseal-1   # 8/8, exit 0, 07:37:59Z
python3 -I -B .ufo/waves/round-34/r34b/w1/CtlMultiset-files/mini-counter-fresh.py --root . \
  --control-reader .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py  --seed w2-aseal-1   # 0/8, met false, exit 1, 07:37:59Z
```

**Evidence pointers.** `claim-stop.json:record_defects_disclosed[F3].repair`; `corpus/QUALITY.md` #70
already requires "count, class names and reader digests"; addendum `A5` narrows #70 ("equality
detects a dropped class, not an unfaithful class set") and routes fresh content. The stop record is
append-only and unedited (`e6303d06…`), so its F3 text is what a reader still sees.

**Impacted axes.** C3 (repair reach) high; depth (the next instrument would inherit a guard that its
own bypass passes); calibration (the record's repair text contradicts the lane's own QUALITY bar).

**Smallest safe correction.** Append a repair-text correction for F3: set equality over
`(class, reader path, reader sha256)`, not count; note that equality still does not reach an
unregistered class, so the load-bearing repair is the per-run fresh-content surface
(`mini-counter-fresh.py`, 8/8 structural, 0/8 nameset at seed `w2-aseal-1`), exactly as `A5` says.
Mark the 07:34:32Z swap probe as the counterexample that rejects count-only.

## 5. Finding 3 (high) — F1 is recorded as `repair_landed`, but the container cannot certify the claim freeze; its anchor is post-data

**Counterexample.** Three invocations of the frozen freeze gate (2026-10-25T07:34:41–07:34:53Z):

```
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 \
  --claims .ufo/waves/round-34/r34b/claims.json --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33
→ exit 3  freeze-integrity: ERROR schema code=instruments_missing … where=instruments

python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 \
  --claims .ufo/waves/round-34/r34b/instruments.json --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33
→ exit 2  ERROR no commit adds .ufo/waves/round-34/r34b/instruments.json at c79bbe7b…

python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 \
  --claims .ufo/waves/round-34/r34b/instruments.json --rev HEAD
→ exit 0  freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=HEAD
```

The container's freeze is `b917ea64` — the commit that created it, two commits **after** the claim
freeze `c79bbe7b`. `commits_after_freeze` is measured from `b917ea64`, so any instrument change
between `c79bbe7b` and `b917ea64` is invisible to it. The stop record nonetheless carries
`"repair_landed": "…instruments.json (byte-identical 26-pin container) + freeze-integrity receipt
over it"`. The addendum's own `enforced_pin_receipt.note` admits the anchor difference, but the stop
record's status word does not; an append-only addendum that says "append-only, the stop record is not
edited" leaves the stronger word standing.

**Evidence pointers.** `claim-stop.json:F1.repair_landed`; `claim-stop-addendum.json:enforced_pin_receipt`
(`freeze=b917ea64…`, with the note); `after/freeze-integrity-instruments.txt` (sha
`d68e4e17552fa018b65a33c3b44e60ecce28cce78d5c054618df34fc2bb5dc47`, matches); independent:
`w2/APinsEnforced.md` verdict ("documentary, self-unverified and worktree-blind").

**Impacted axes.** C2 (binding) high; calibration (the record's repair status vs the tool's actual
reach).

**Smallest safe correction.** Append a status correction: F1 is **documentary, anchor `b917ea64`,
certifying post-audit drift only**; it does not repair the frozen `claims.json` shape and cannot
certify the measurement revision. The enforcement route remains QUALITY 72 (the counting command
re-hashes the pins and binds `--rev`). No pin, claim byte or score changes.

## 6. The five disclosed defects and the proposed repair, field by field

| id | stop's statement | my read after probing |
|---|---|---|
| F1 | pins declarative; container repair landed | **confirmed and overstated** — see Finding 3; container is real, byte-equal to `claims[0].pins` (26/26 verified), but documentary and anchored post-data |
| F2 | predicate identity false (A vs B) | **confirmed**; addendum `D2` adds the third sentence (mini counter `C`), which is the one the decisive run is scored under; the stop record still prints only A/B |
| F3 | class drop invisible to the floor; repair = count equality | **confirmed, and the repair is insufficient** — see Finding 2 (count-preserving swap passes) |
| F4 | gate mutant M3 survives its selftest, red→CLEAN | **confirmed** (`w1/MutGateBranches.md` §3); the C2 counter does catch M3 via `red_refused`, but only because the over-target class is the last row — the repair route (red-last + row-count) is apt |
| F5 | receipts untracked at first audit | **confirmed**; receipts landed `b917ea64`; the F4/F5 evidence reports were absent at `cd75b92e` and landed later at `66b84027` (verified) |
| F6 (addendum) | deterministic seed + published transformed digest | **confirmed**; the fresh counter defeats it (`structural` 8/8, `nameset` 0/8, seed `w2-aseal-1`) |

The proposed repair, taken as F3+F4+A5+F6 together, now reaches the decisive mechanism only through
the fresh-content surface. F3's *text* does not, and F1's *status* overstates. Those are the two
conformance repairs.

## 7. Verdict

**`ok+conformance-defect`.**

Why not `rejected-honest-stop`: the stop's disposition is right and does not need more measurement.
The decisive class reproduces (8/8, four seeds, exit 0), all seven registered classes stay below
target, the structural control meets it, and the round awarded no capability and no score. Applying
the round contract's §9 ("a do-nothing / work-skipping control must not reach the target"; r29-C1
precedent) to deny credit is correct on these bytes. No probe I ran suggests a different disposition.

Why not `ok`: three material record defects survive the addendum, and two of them are status/repair
claims that would mislead the next instrument — (1) the receipt the stop quotes is shape-fed and its
revision is an echo, with the defect absent from both the stop's five and the addendum; (2) F3's
count-only repair is defeated by a count-preserving swap while the lane's own QUALITY 70 already
requires count+names+digests; (3) F1's `repair_landed` overstates a documentary, post-data audit as
enforcement. All three are append-only repairable; none requires touching frozen bytes, the six
clauses, the target, the predicate or any score.

**Impact on scores: none.** Coverage, depth and calibration stay 10 → 10; no capability row is
awarded or removed by this read. R34-C1 remains stopped and untouched.

`SEAL_VERDICT: close round 34 (run-6, attempt 1) as ok+conformance-defect — the R34-C2 stop is substantively correct and reproducible, with three append-only-repairable record conformance defects (shape-fed receipt + echoed revision; count-only F3 repair defeated by a count-preserving swap; F1 "repair_landed" overstating a post-data documentary audit); no score, capability, clause, target, predicate or frozen byte is changed by this read.`

## 8. Repro ledger (exact argv, exit, UTC)

All paths under `/fast/scratch/hyaku/kaidoku-r34b/w2/ASealVerdict/`. Lane copy `lane/` made
2026-10-25T07:29:19Z; `lane-fake/`, `lane-swap/` derived from it. Interpreter `/usr/bin/python3`
3.14.8. Lane clean for `tools/round-34` and the three claim artifacts at 2026-10-25T07:38:16Z.

| # | run | exit | UTC |
|---|---|---|---|
| R1 | `mini-counter.py --root . --control-reader …/nameset.py` (lane) | 0 (8/8, met true) | 07:29:25Z |
| R2 | 11-reader matrix under the same counter | 0 for structural/nameset; 1 otherwise | 07:29:27Z |
| R3 | `c2-shortcut-gate-counter.py --root . --rev 0000…` (pristine lane) | 0 (`GATE_COUNTER_OK`) | 07:32:31Z |
| R4 | `mini-counter-fresh.py` structural / nameset, seed `w2-aseal-1` | 0 (8/8) / 1 (0/8) | 07:33:38Z, 07:37:59Z |
| R5 | `c2-…-counter.py` with 1,226-byte mock at the pinned gate path | 0 (`GATE_COUNTER_OK`) | 07:34:31Z |
| R6 | `c2-…-counter.py` with count-preserving swap config | 0 (`GATE_COUNTER_OK`, 7 classes) | 07:34:32Z |
| R7 | `freeze-integrity.py --claims claims.json --rev c79bbe7b…` | 3 (`instruments_missing`) | 07:34:41Z |
| R8 | `freeze-integrity.py --claims instruments.json --rev c79bbe7b…` | 2 (no commit adds container) | 07:34:41Z |
| R9 | `freeze-integrity.py --claims instruments.json --rev HEAD` | 0 (`CLEAN pins=26 freeze=b917ea64ebbe`) | 07:34:53Z |
| R10 | `git cat-file -e cd75b92e:…/MutGateBranches.md` (same for `RevFreezeOrder.md`) | 128 (missing; `exists on disk, but not in 'cd75b92e'`) | 07:39:17Z |
| R11 | `c2-…-counter.py` mock gate + all-zero rev, combined | 0 (`GATE_COUNTER_OK`, `measured_revision=0000…`) | 07:37:41Z |
| R12 | `git rev-parse HEAD`, `git status --porcelain -- tools/round-34 …` | 0 (`5a0435ff`, clean) | 07:35:11Z / 07:38:16Z |

## 9. Limits of this read

- The lane moved while I reviewed (`66b84027`, `5a0435ff` landed between 07:29Z and 07:37Z). I
  reviewed the **stop record as landed at `cd75b92e`** (unchanged, `e6303d06…`) plus the addendum;
  where a sibling commit fixed a finding I say so rather than charging it.
- The mock-gate probe uses the counter's documented production path (`--root` + default gate), not
  the `--gate` override; the override path is also production-legal but I did not need it.
- I did not execute the pinned gate end-to-end on the lane itself with a corrupted reader; the
  counter's own selftest and my mock cover the binding question. The manual 26/26 pin match is
  independently established by `w1/ExecRedReproduce.md` §2 and the addendum's receipt.
- I did not run the R34-C1 production reader or any of its twelve carriers.
- No score, capability, clause, target, predicate or frozen byte was changed by this read. Only this
  report was written.
