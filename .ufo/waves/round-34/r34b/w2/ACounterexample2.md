# R34b w2 — ACounterexample2: independent reproduction B (payload-only class, name-erased scoring)

Seat: `L1Kaidoku34-2.ACounterexample2` (executor). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scratch and all writes: `/fast/scratch/hyaku/kaidoku-r34b/w2/ACounterexample2/` (referred to below as `$S`).
Claim under attack: **R34-C2**, frozen at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`; stop record
`.ufo/waves/round-34/r34b/claim-stop.json`. This seat does not reopen the claim, does not repair a frozen
instrument, and awards no score.

**Answer in one line:** a name-blind payload key — `(record count, ordered (flags, value) sequence)`, with
the names replayed from a hardcoded table — scores **matched 8 / target 8** under the frozen `permute()`
transform (8 seeds) *and* **8 / 8** with every name byte of the input zeroed (3 seeds); the pinned structural
reader scores **8 / 8** under `permute()` and **0 / 8** under name erasure (it emits all 25 records with empty
names). The stop's second independent class reproduces, but it is name-blind and record-aware, not
traversal-free, and it is not present in the landed stop record.

---

## 0. Axes named before acting (Godspeed)

| axis | question | answer location |
|---|---|---|
| A1 | does a name-blind payload key reach the frozen green target under the counter's own predicate? | §3 |
| A2 | does it survive name erasure where the structural reader does not? | §4 |
| A3 | does the frozen whole-command verdict machinery mean anything in a name-erased world? | §5 |
| A4 | does an independently written implementation reproduce the stop's second class, or falsify it? | §6 |

Cheap iterations: one reader + one driver; every extra axis (order-insensitive key, count-only ceiling,
offset-corruption blindness probe, 200-seed invariance, whole-command arms) is a variant on the same two
commands, and all arms are re-runnable from `$S/run_arms.sh`.

---

## 1. Setup, independence, containment

**Independence.** I wrote `$S/payload_keyed.py`, `$S/payload_multiset.py`, `$S/count_only.py` myself from the
fixture authoring spec (`tools/round-34/mini-fix/build.py:21-34`, `expected.json`) and the fixture bytes. I did
not copy any sibling seat's reader; the L1's post-stop `w1/CtlMultiset-files/payload_keyed.py` was read only
*after* my reader was written and scored (comparison in §7). Reader hashes:

| artifact | sha256 |
|---|---|
| `$S/payload_keyed.py` | `3b61629584491181a3892f097c1f2bf0d6bc9e553d8119b6f33ff8529d8d64e3` |
| `$S/payload_multiset.py` | `8156d48e388e6b1d1c606a5195e59f8691bdf1cdd01fabb0ee592b1357ed03eb` |
| `$S/count_only.py` | `cacfbedc6e5941d2954e8c5b19c42dabc1a1b57c048907ea1c4c009216ebea93` |
| `$S/run_arms.sh` (driver for §3–§5) | `d80a0383823352e046eeb43cc59e4242c4cfde0f12bf6dafcacf986b6ad805e1` |

**Frozen instruments, byte-identical.** `$S/pin_audit.py` (exit 0, `out/pin-audit.json`, 07:34:25Z) hashes
every root against the 26-entry pin map in `.ufo/waves/round-34/r34b/instruments.json`:

| root | pinned files byte-identical | diffs |
|---|---|---|
| `root-permute` (pristine copy) | **26 / 26** | none |
| `root-zero` (name-erased fixtures) | 18 / 26 | the 8 fixtures only |
| `root-zeropool` (tail-erased fixtures) | 18 / 26 | the 8 fixtures only |
| `root-permute-reg` | 25 / 26 | `gate-config-mini.json` (payload class appended, scratch only) |
| `root-zero-posmem` | 17 / 26 | mini config (positive control), 8 fixtures |
| `root-zero-posmem2` | 16 / 26 | mini + naive configs (positive controls), 8 fixtures |

So every counter, gate, reader, `expected.json` and `build.py` byte used in the name-erased arms is the frozen
pin; only the fixture bytes (the input) and, where stated, the positive-control pointer in a scratch config
differ. `mini-counter.py` is `43ef669ff6ea…` in all six roots.

**Name erasure.** `$S/zero_fixtures.py` (exit 0, `out/zero-fixtures.json`, 07:31:59Z; first invocation exited 1
because the `root-zeropool` tree did not exist yet — created, rerun exit 0) zeroes name characters via the
header's `names_off` and each record's `name_off`. Audit: header and record array byte-equal to the originals
(`header_equal`/`record_array_equal` true for all 8 × 2 roots), size 512 kept, and the only surviving printable
run ≥4 chars is `MREC` (intact fixtures carry 25 name tokens + `MREC`). Zeroed fixture hashes:

```
alpha   e02d07764e9ef4afcfbb7892373b7ad17cfd260830aae4b0524c24b87a688442
beta    5b86ac7b5013e878115737fa12a60c02ff88257085d9f76e9c496b887207cb1e
delta   764688bf8204856697edda91664765bffb9115a28bae5e8fb91a92ed90e613f8
epsilon e0841cfae4497ba9c3014dd57ba9ed000b9ec740790ba421b17be6b2d388802b
eta     ddfa1a17c37996498d1fdee3d41d429cbca8dae18a4dbcd82e0bb45e9fa07f7c
gamma   da33a29b15c986b4b1e2e1ef126e95682878acbed7efa8dad109de1466622d24
theta   94cfd4d25c19e5fa99effd455c4594809f36b6e2dddcef3a900b112a4b02915d
zeta    303d9a24747f7752136896747714de35cdbe72f66155f85586125d4a50a04f84
```

`root-zero` and `root-zeropool` are byte-identical (same hashes): in this fixture family the padding after the
name pool is already NUL, so "every name byte zeroed" and "whole tail zeroed" coincide. The erasure is
therefore unambiguous here, not a wording choice. (These eight hashes also match the L1's post-stop receipt,
§7 — an external cross-check of the transform, not of the scoring.)

Host: `/usr/bin/python3` 3.14.8, kernel 7.2.11-arch1-1. No tool installed or upgraded (pacman paused; not
touched). No ELF carrier, fixture or reader executed as a program: readers ran only under
`/usr/bin/python3 -I -B` spawned by the frozen counters and gates, fixtures only as data. No build, lint or
test suite.

---

## 2. What the class keys on

`payload_key(data) = (count, ((flags_i, value_i) for i in 0..count-1))`, read from the header `count` and each
record's `flags`/`value` fields only. No read at header offset 12 (`names_off`), no `name_off` use (the field is
unpacked and discarded), no NUL scan, no pool byte. The name↔flags/value **association** is the hardcoded
`TABLE` (25 records across 8 keys). This is a memorization class keyed on the record array's scalar payload; it
*does* walk the record array, unlike the stop's decisive class (`w1/CtlMultiset-files/nameset.py`, which walks
no record array and reads no header).

Two derived variants measure what carries the 8:

* `payload_multiset.py`: same fields, multiset (record order ignored) — still 8 distinct keys, 8/8.
* `count_only.py`: header count only — ceiling **6/8** (counts `1` and `3` are each shared by two fixtures),
  measured 6 at both transforms, missing `epsilon` and `eta`.

---

## 3. In-predicate result (frozen `permute()`, pinned fixtures, pinned counter)

All runs: `/usr/bin/python3 -I -B $LANE/tools/round-34/mini-fix/mini-counter.py --root $LANE --control-reader <reader> [--seed <s>]`,
cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, window `2026-10-25T07:33:36Z → 07:33:37Z`
(`out/arms.log`; per-arm stdout in `out/A*.txt`).

| arm | reader | seed | matched/target | met_target | exit |
|---|---|---|---|---|---|
| A1 | `payload_keyed.py` | `kaidoku-r34-mini-v1` (default) | **8 / 8** | true | 0 |
| A2 ×7 | `payload_keyed.py` | `0, 17, 88, 410, 999, alt-1, alt-2` | **8 / 8** each | true | 0 |
| A3 | `payload_multiset.py` | default | **8 / 8** | true | 0 |
| A4 | `count_only.py` | default | 6 / 8 | false | 1 |
| A5 | pinned `structural.py` | default | 8 / 8 | true | 0 |
| A5b | pinned `structural.py` | 410 | 8 / 8 | true | 0 |

So the frozen green surface is met by a class that reads no name byte, at the default seed and at all seven
alternative seeds I ran (including the stop's `alt-1`/`alt-2`). Mechanically this is not seed luck: `permute()`
rewrites only `name_off` and the pool layout; `$S/invariance.py` (`out/invariance.json`, exit 0, 07:32:03Z)
asserts over 200 seeds × 8 fixtures that the payload key is unchanged (`permutation_invariant_200_seeds: true`)
and that every record's `(flags, value)` columns are byte-stable under `permute()`.

Whole-command corroboration, same window:

* `C0` frozen counter on the lane root: `GATE_COUNTER_OK … red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN
  green_positive_matched=8 clauses_failed=-`, exit 0 (`out/c2-lane-baseline.json`) — the green verdict is
  CLEAN **while** an unregistered class passes 8/8 (A1). A negative control for the receipt's meaning.
* `C0b` frozen counter on the pristine scratch copy (`$S/root-permute`): same line, exit 0
  (`out/c2-permute-copy.json`) — the copy is behaviourally identical to the lane.
* `G1` pinned gate, lane root, scratch config = pinned mini config + `{"class":
  "payload-keyed-ACounterexample2"}`: `REPLAY_GATE_REFUSED finding=shortcut_meets_target
  shortcuts_below_target=7 shortcuts_over_target=payload-keyed-ACounterexample2`, exit 2
  (`out/G1_gate_lane_plus_payload.txt`).
* `C1` frozen counter on `$S/root-permute-reg` (payload class registered, everything else pinned):
  `GATE_COUNTER_MISS … red=REPLAY_GATE_REFUSED green=REPLAY_GATE_REFUSED green_positive_matched=8
  clauses_failed=green_clean`, exit 1 (`out/c2-permute-reg.json`); green gate line exactly
  `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=payload-keyed-ACounterexample2`.

The gate mechanism discriminates the moment the class is registered; the frozen receipt is CLEAN only because
the class list is frozen.

---

## 4. Name-erased result (every name byte zeroed, pinned instruments)

Same commands with `--root $S/root-zero`. Window `07:33:53Z → 07:33:55Z`.

| arm | reader | seed | matched/target | met_target | exit | notes |
|---|---|---|---|---|---|---|
| Z1 | `payload_keyed.py` | default | **8 / 8** | true | 0 | all 8 rows ok |
| Z1b | `payload_keyed.py` | 0 | **8 / 8** | true | 0 | |
| Z1c | `payload_keyed.py` | 410 | **8 / 8** | true | 0 | |
| Z2 | `payload_multiset.py` | default | **8 / 8** | true | 0 | order also irrelevant |
| Z3 | `count_only.py` | default | 6 / 8 | false | 1 | same two misses |
| Z4 | pinned `structural.py` | default | **0 / 8** | false | 1 | reader exits 0 per fixture; output is wrong |
| Z4b | pinned `structural.py` | 410 | **0 / 8** | false | 1 | |

**Does the structural reader survive name zeroing? No.** On the erased inputs it runs (exit 0) and emits every
record with an empty name: `out/structural-zeroed.json` (exit 0, 07:35:12Z) reports 25 records, 25 empty names,
0 non-empty names across the eight fixtures, e.g. gamma:
`{"records": [{"flags": 0, "name": "", "value": 0}, … 5 rows …]}`. Canonical comparison against the pinned
`expected.json` (which names the records) misses all eight.

The payload readers' outputs are provably independent of both name locations, not merely "not obviously
using" them (`$S/blindness_probe.py`, exit 0, `out/blindness.json`, 07:34:25Z; 2 variants × 8 fixtures):

| reader | `names_off` (u32@12) := 0xFFFF | every `name_off` (u16) := 0xAAAA |
|---|---|---|
| `payload_keyed.py` | output byte-identical to pristine, exit 0 (8/8) | identical, exit 0 (8/8) |
| `payload_multiset.py` | identical, exit 0 | identical, exit 0 |
| `count_only.py` | identical, exit 0 | identical, exit 0 |
| pinned `structural.py` | changed, **exit 1** (8/8) | changed, **exit 1** (8/8) |

Blindness is behavioural: two inputs that differ only in the bytes a reader claims not to use produce
byte-identical output.

---

## 5. Whole-command scoring on the name-erased world

Window `07:33:55Z → 07:34:04Z`; receipts `out/c2-zero-*.json`.

| arm | root | positive controls | verdict line | exit |
|---|---|---|---|---|
| Z5 | `root-zero`, pinned gate + payload class registered | green: pinned structural | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target shortcuts_below_target=7 shortcuts_over_target=-` | 3 |
| Z6 | `root-zero`, frozen counter, configs pinned | both pinned structural | `GATE_COUNTER_MISS … red=REPLAY_GATE_UNEVALUABLE green=REPLAY_GATE_UNEVALUABLE green_positive_matched=0 clauses_failed=green_clean,green_positive_meets_target,red_refused` | 1 |
| Z7 | `root-zero-posmem` (green positive := payload reader, class label `structural`) | green: payload; red: pinned | `GATE_COUNTER_MISS … red=REPLAY_GATE_UNEVALUABLE green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=red_refused` | 1 |
| Z8 | `root-zero-posmem2` (both positives := payload reader) | both: payload | `GATE_COUNTER_OK … red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` | 0 |

Reading, stated precisely:

1. With the frozen configs, name erasure makes **both** cases unevaluable, because both configs'
   positive control is `structural.py`, which cannot decode name-erased bytes. The whole frozen command
   therefore returns **MISS**, not OK, on erased input. Name zeroing is not a world in which the frozen
   receipt can be reproduced unchanged.
2. Registering the payload class does not help (Z5): the gate refuses to score shortcuts when its positive
   control is below target, so "register the class" is not a name-erasure remedy either.
3. Only when the *positive control itself* is replaced by the memorizer do all six clauses reproduce (Z8) —
   which is the point: in a world with no name byte, the receipt is satisfiable only by a table, and the
   counter cannot tell that table from structure (it never inspects reader internals; `replay-gate.py:88-110`
   reads only `matched`/`target`/`met_target` from the child's stdout).
4. Z8 is an out-of-predicate control probe, not a claim result. The in-predicate claim result is §3 (A1/A2/A3).

---

## 6. Verdict on the stop's second class

**B reproduces; the stop is not falsified by non-reproduction, and its evidence is not stronger than
one class plus one association-blind class.**

* In-predicate (`permute`): payload-only 8/8 at 8 seeds, order-insensitive variant 8/8, against a structural
  control 8/8 and a gate receipt that stays CLEAN until the class is registered. This is an independent second
  demonstration that the green surface does not force name resolution.
* Name-erased: payload-only 8/8, structural 0/8. Under this transform the target is reachable **only** by
  memorization: the erased inputs contain 0 of the 25 name tokens, so no decoder can produce the expected names
  from the bytes. The 8/8 is therefore proof of an external table, not of decoding.
* **Precise scope.** My class falsifies the predicate's association clause — "only record-array traversal
  associates a name with its record" — because the association here is replayed from `TABLE`. It does not
  falsify a traversal requirement: the class must walk `count` records to read the scalar columns, and
  `count_only.py` (count alone, no record walk) scores only 6/8 on this fixture set, so the scalar columns are
  load-bearing. The stop's own decisive class (`nameset.py`) is the stronger one: it reads no header and walks
  no record array. A stop narrative that says "readers meet the target without walking records", applied to
  this class too, overstates what B shows; applied to `nameset.py`, it is exactly what that reader does.

---

## 7. Attack on the stop record's evidence chain (observations, nothing repaired)

1. **The stop record carries only the first class.** `claim-stop.json` (`decisive_counterexample`) names
   `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` (content-multiset), its sha256, its producer
   seat, its argv, and `matched=8` at three seeds. There is **no** payload-keyed receipt, argv, exit, seed,
   zeroed-fixture hash, or evidence pointer anywhere in the landed stop JSON — the second class exists only in
   the wave-2 context that re-dispatched this seat. A reader of the stop alone cannot verify the second class.
2. **The second-class receipts are post-stop and untracked.** `w1/CtlMultiset-files/nameset-green-receipt.json`
   (mtime `2026-10-25T07:34:01Z`) and `payload-keyed-receipt.json` (`07:34:34Z`) are untracked
   (`git status --porcelain`, 07:34:41Z) and the payload receipt says of itself `authored_by: "L1, 2026-10-25,
   AFTER the stop (evidence for the stop, not a frozen instrument)"`. That is honest, but it means the stop's
   second class was evidenced after the stop it is offered to support; it cannot be part of the frozen surface.
3. **The payload receipt's cross-reference is wrong.** It cites `seat evidence w1/ACounterexample2.md`; there is
   no `w1/ACounterexample2.md` (this seat's report is `w2/ACounterexample2.md`). Its `source_sha256`
   (`0e125169cabe…`) is the L1's own reader, not mine (`3b6162958449…`). Its `names_zeroed_runs` entries carry
   `exit` and `decisive sha` but no argv, no seed, no per-run verdict; only `plain_green_run` has argv.
   **What does cross-check:** its eight `zeroed_sha256` values match my independently produced erased fixtures
   byte-for-byte (all eight above). So the erasure is corroborated; the zeroed scoring runs in that receipt are
   not independently re-derivable from the receipt alone — they are re-derivable from *this* report (Z1–Z3).
4. **Clock.** The stop's `l1_rerun_utc` is `"2026-10-25T07:28:00Z (approximate; exact clock in the wave
   report)"`. The only nameset receipt I can find is stamped `07:34:01Z`; no artifact I found is stamped
   `07:28`. The stop labels the value approximate, so this is a traceability gap, not an inconsistency proven.
5. **The class can be added to the vocabulary without instrument change** (same predicate, same target, same
   seven pinned classes): `G1`/`C1` above. That is evidence the omission is a registration choice, not a
   capability gap — but registration is frozen, so it supports the stop rather than reopening it.

---

## 8. Limits of this seat's evidence

* The name-erased arm is **out of predicate** (the predicate's transformation is `permute`, which preserves
  names); the in-predicate evidence is A1/A2/A3. The erasure arm measures what the surface can and cannot
  force, and it shows the structural positive control is name-dependent, not that `structural.py` is a weak
  decoder.
* "Structural 0/8 under erasure" is partly information-theoretic (no name byte exists in the input); the
  measurement confirms the readers behave accordingly rather than crashing or inventing names.
* I did not test the red case, the gate selftest internals, or mutant kills beyond what the frozen counter
  reports; those are other seats' assignments. My Z8 control deliberately changes two positive controls in
  scratch copies only and is labelled as such.
* Harness transparency: my first `payload_multiset.py` table had a tuple-ordering error (integer ordering
  `0x0B60 < 0x0601020F` ignored), which scored 4/8 at 07:32:19Z. Fixed, then the **entire** driver was re-run
  (`out/arms.log`, `07:33:36Z → 07:34:04Z`); every number in this report is from the post-fix log. The failing
  run is not cited as evidence.

---

## 9. Bounded implication for the proposed repair (advisory; nothing applied)

The disclosed F3 repair is "assert class count == pinned count before CLEAN"
(`claim-stop.json.record_defects_disclosed[F3]`). Measured consequence here: on the frozen world the receipt is
already `GATE_COUNTER_OK` while the unregistered payload class meets the target (C0 + A1). A count-equality
assertion would still pass, because the pinned set and the registered set are equal — the missing class is
missing from **both**. Registering it makes the gate refuse (G1/C1), so registration, not counting, is the
lever. Separately, `count_only.py` at 6/8 and the 200-seed column stability show the payload columns are exactly
the invariant that survives `permute()`. No change to any instrument, config or predicate is proposed for this
round; the L1 lands any repair.

---

## 10. Command / exit / UTC ledger

All commands `/usr/bin/python3 -I -B`, cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless noted;
`$LANE` = lane root, `$S` = `/fast/scratch/hyaku/kaidoku-r34b/w2/ACounterexample2`.

| UTC (2026-10-25) | command (abridged) | exit | artifact |
|---|---|---|---|
| 07:31:59Z | `cd $S && zero_fixtures.py` (2nd run; 1st failed on missing `root-zeropool` tree) | 0 | `out/zero-fixtures.json` |
| 07:32:03Z | `cd $S && invariance.py` (200 seeds × 8, reader-output equality) | 0 | `out/invariance.json` |
| 07:32:19Z | `mini-counter.py` with pre-fix multiset reader | 1 (4/8) | superseded; not evidence |
| 07:33:24Z | scratch configs written (`out/gate-config-mini-plus-payload.json`, `root-permute-reg`, `root-zero-posmem`, `root-zero-posmem2`) | 0 | pin audit below |
| 07:33:36Z | `mini-counter.py --root $LANE --control-reader $S/payload_keyed.py` | 0 | `out/A1_payload_lane_default.txt` |
| 07:33:36–37Z | same, `--seed 0 17 88 410 999 alt-1 alt-2` (7 runs) | 0 each | `out/A2_*.txt` |
| 07:33:37Z | same with `payload_multiset.py` | 0 | `out/A3_multiset_lane_default.txt` |
| 07:33:37Z | same with `count_only.py` | 1 (6/8) | `out/A4_count_only_lane_default.txt` |
| 07:33:37Z | same with pinned `structural.py` (default; `--seed 410`) | 0 / 0 | `out/A5*.txt` |
| 07:33:38Z | `replay-gate.py --root $LANE --config $S/out/gate-config-mini-plus-payload.json` | 2 | `out/G1_gate_lane_plus_payload.txt` |
| 07:33:39Z | `c2-shortcut-gate-counter.py --root $LANE --rev c79bbe… --json-out $S/out/c2-lane-baseline.json` | 0 | `out/c2-lane-baseline.json` |
| 07:33:43Z | same, `--root $S/root-permute` | 0 | `out/c2-permute-copy.json` |
| 07:33:48Z | same, `--root $S/root-permute-reg` | 1 | `out/c2-permute-reg.json` |
| 07:33:53Z | `mini-counter.py --root $S/root-zero --control-reader $S/payload_keyed.py` | 0 | `out/Z1_payload_zero_default.txt` |
| 07:33:53Z | same, `--seed 0` / `--seed 410` | 0 / 0 | `out/Z1b`, `out/Z1c` |
| 07:33:54Z | same root with `payload_multiset.py` / `count_only.py` | 0 / 1 (6/8) | `out/Z2`, `out/Z3` |
| 07:33:54Z | same root with pinned `structural.py` (default / 410) | 1 / 1 (0/8) | `out/Z4`, `out/Z4b` |
| 07:33:55Z | `replay-gate.py --root $S/root-zero --config …plus-payload.json` | 3 | `out/Z5_gate_zero_plus_payload.txt` |
| 07:33:57Z | `c2-shortcut-gate-counter.py --root $S/root-zero …` | 1 | `out/c2-zero-unmodified.json` |
| 07:33:59Z | same, `--root $S/root-zero-posmem` | 1 | `out/c2-zero-posmem.json` |
| 07:34:02Z | same, `--root $S/root-zero-posmem2` | 0 | `out/c2-zero-posmem-paired.json` |
| 07:34:25Z | `cd $S && blindness_probe.py` | 0 | `out/blindness.json` |
| 07:34:25Z | `cd $S && pin_audit.py` | 0 | `out/pin-audit.json` |
| 07:35:12Z | structural reader over the 8 erased fixtures (record/empty-name census) | 0 | `out/structural-zeroed.json` |
| 07:34:41Z | `git -C $LANE status --porcelain` (read-only) | 0 | no `tools/` modification; only other seats' corpus/.ufo changes |

**No-harm.** The only lane file I wrote is this report. No lane VCS mutation (`git add/commit/stash/checkout/
reset/pull/push` never run; no `jj`), no ELF execution, no frozen instrument edited, no `claims.json` /
`claim-stop.json` / SCORECARD / LOG / SKILL / PROVINCE / corpus file touched. All receipts, roots, readers and
logs live under `$S`.

---

## 11. Final verdict line

**Reproduction B: CONFIRMED — payload-only (count + ordered `(flags,value)`, names replayed from a table)
scores 8/8 at target 8 on the frozen green surface under `permute()` (8 seeds) and 8/8 with every name byte
zeroed (3 seeds), while the pinned structural reader scores 8/8 under `permute()` and 0/8 under name erasure
(25/25 records emitted with empty names); the frozen whole counter returns CLEAN while this class is
unregistered, REFUSED once registered, and MISS/UNEVALUABLE on the name-erased world unless both positive
controls are replaced by the memorizer. The stop's second class is real and its class-2 wording ("8/8 with
names zeroed") holds; the stop record itself carries no receipt for it, and the class is name-blind and
record-aware, not traversal-free — so it corroborates the stop's falsification of the name-associated clause
without strengthening it to "no traversal is forced."**
