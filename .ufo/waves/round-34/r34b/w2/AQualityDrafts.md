# AQualityDrafts — QUALITY.md rows 68–72, drafted from the R34-C2 stop

Seat: `L1Kaidoku34-2.AQualityDrafts` (scribe, leaf). Round 34, run-6 re-dispatch, wave 2:
falsify the stop. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Frozen revision
`c79bbe7b0959132b9873ff3431cf5eb313b58b33`; stop record `.ufo/waves/round-34/r34b/claim-stop.json`
(landed `cd75b92e`). R34-C1 production reader and twelve carriers not executed or scored.
This file is the only lane path written.

Axes named (Godspeed): (A1) wording fidelity — each drafted row names exactly the mechanism a
wave-1 defect broke, no wider; (A2) evidence binding — every row cites a committed report or
pinned file, never a memory claim; (A3) numbering correctness against the L1's own routes in
`corpus/lessons/round-34.md` M34-5..M34-11 and the uncommitted `corpus/QUALITY.md` worktree
draft; (A4) sharpening discipline — the `supersedes` column names only rows the new text
genuinely extends. Assignment order kept; where the landed (uncommitted) lesson/QUALITY draft
assigns different numbers, the conflict is reported verbatim in §5 rather than silently
renumbered.

No tool was installed or upgraded (nothing needed; `sha256sum`, `grep`, `sed`, `git` read-only
verbs, `/usr/bin/python3` not invoked by me). pacman untouched. No ELF/fixture/reader executed;
no counter re-run — drafting seat on read-only wave; every measured fact is cited to a wave-1
committed report, the pinned sources, or a read-only command I ran.

## 1. Assignment

Draft `corpus/QUALITY.md` rows 68–72 (L1 numbering, in assignment order):
(68) predicate byte-identity across claims/config/counter/receipt with an instrument that
reads it; (69) a gate's registered class set is asserted against its pinned set before CLEAN;
(70) a fixture transformation must be shown to break every invariant a shortcut can key on,
not just one; (71) gate mutant selftests must place the over-target reader in every slot and
assert row counts; (72) a capability claim's target must not be reachable by a counter that
runs no reader.

## 2. Draft rows (for the L1 to land; column order `# | criterion | why (lesson) | supersedes`)

```
| 68 | The predicate sentence is byte-identical in the claims file, every gate config's `predicate` field, the counter's `PREDICATE` constant and the receipt's `predicate` field, and an instrument reads it out of the claims file and compares digests — a `predicate_identity` claim asserted only in prose is inadmissible. A frozen claims file asserting one sentence across carriers that hold two (or three) is a disclosed record defect, and no post-freeze patch fixes it. | `corpus/lessons/round-34.md` M34-6 (r34b append); `.ufo/waves/round-34/r34b/predicate-reconciliation.json` (`PREDICATE_IDENTITY_FALSE`: A `7c6c17f0…` 31 words in claims+configs vs B `8340aea5…` 46 words in `c2-shortcut-gate-counter.py:23` and every receipt, vs C `09988625…` in `mini-counter.py`); `.ufo/waves/round-34/r34b/w1/RevPredicateIdentity.md` (probes M1/M2/M4 pass `GATE_COUNTER_OK` with the predicate text rewritten, empty or relabelled — `replay-gate.py:43` requires the key and never reads the value, `c2-shortcut-gate-counter.py:73` echoes the constant) | sharpens 18, 66 |
| 69 | Before a replay gate prints `REPLAY_GATE_CLEAN` it asserts the registered shortcut set equals the pinned class set — count, class names and reader digests — not merely `len(shortcuts) >= MIN_SHORTCUTS`. A count floor is not an equality: dropping classes to the floor, padding it with renamed duplicates of one dead reader, or dropping a class to reach CLEAN must all fail before scoring, not after an audit. | `corpus/lessons/round-34.md` M34-8; `.ufo/waves/round-34/r34b/claim-stop.json` record defect F3; `w1/RevPredicateIdentity.md` M3 (green config trimmed 7→3 classes still `GATE_COUNTER_OK` exit 0, `shortcuts_below_target=3`); `w1/RevClaimsVsInstruments.md` F2 (7→4 classes, `GATE_COUNTER_OK`); `w1/CritCounterLimits.md` §1 (three class names pointing at `all_false.py` clear the floor → `REPLAY_GATE_CLEAN`); `w1/ExecRecountC2.md` F3 (single green-surface drop invisible); `w1/CritClaimWidth.md` CE-3 (shape-only counter CLEAN on three weak classes) | sharpens 61, 67 |
| 70 | A fixture transformation defeats only the keyable invariants it breaks; the pre-freeze replay set names one class per surviving invariant — size, label, whole-file digest, fixed slice, record order, payload/scalars, value multiset, name multiset, transform/seed reuse — and each is scored under the counter's own predicate, or the frozen CLEAN says nothing about the class space. A transform constrained to preserve decoded content (layout-only: pool reorder + `name_off` rewrite) cannot break any content-invariant key, so fresh generated content with an unpublished expectation is the preferred green surface. | `corpus/lessons/round-34.md` M34-7; `.ufo/waves/round-34/r34b/claim-stop.json` decisive counterexample (`w1/CtlMultiset-files/nameset.py`, sha256 `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97`, 8/8 on three seeds); `w1/ExecRedReproduce.md` §5.1 invariance lemma and `mini-counter-fresh.py` (structural 8/8, all nine shortcut classes 0/8); `w1/CritClaimWidth.md` CE-1/CE-2 (payload-keyed, names ignored, 8/8 → REFUSED when registered); `w1/CritCounterLimits.md` §1 ((flags,value)-tail key 8/8); `w1/MutShortcutClasses.md` F1 (five readers 8/8; F6 payload-perturbing surface kills all memorizers); `w1/ScribeKnowledgeEntry.md` F1 (topology/scalar keys 8/8); `w1/ExecPermuteAudit.md` (single-record fixtures draw the identity permutation at ≈1/474) | sharpens 67 |
| 71 | A gate's mutant selftest places the over-target reader in every shortcut slot (at minimum the last row), asserts `len(rows) == 1 + len(shortcuts)` and pins the printed `shortcuts_below_target`, and runs at least one refusal through the shipped CLI asserting the exit code and the printed verdict equal the JSON payload — mutant kills are scored on the `(exit, verdict, over-set)` triple, never on exit code alone, and the positive control's class label is reserved (a duplicate label is a schema refusal). Detection of a dropped or relabelled class must not be an accident of config row order. | `corpus/lessons/round-34.md` M34-9; `.ufo/waves/round-34/r34b/claim-stop.json` record defect F4; `w1/MutGateBranches.md` (M3 `[:-1]` ignores the last shortcut row: selftest 12/12, mutants 3/3, frozen red case → `REPLAY_GATE_CLEAN` exit 0; every shipped case puts the over-target reader at s1/s2, none asserts `len(rows)`; detection by the C2 `red_refused` clause is order-coincidental — probe (ii)); `w1/RevengerGateFailModes.md` F1 (`structural`-labelled shortcut excluded from `over` → CLEAN on the red config); `w1/CritCounterLimits.md` §2 label-collision probe and §4 (counter-target-binding mutant survives its own selftest); `w1/CritClaimWidth.md` CE-4/CE-6 (label is free text; kills scored by exit code only) | sharpens 61, 67 |
| 72 | A capability claim's target must not be reachable by a counter that runs no reader: before a verdict counts, the counter carries execution evidence per scored row (reader path + digest, or per-row `exit`/liveness propagated to the gate), the gate cross-checks `met_target == (matched == target)` and `0 <= matched <= target` and treats a crash-only row as unevaluable rather than "below target". A receipt of `met_target=true` from a counter that measured nothing is not evidence; a self-reported flag is a claim about itself. | `corpus/lessons/round-34.md` M34-10; `w1/CritClaimWidth.md` CE-5 (liar counter runs no reader, answers by basename: `GATE_COUNTER_OK`, all six clauses, exit 0) and `w1/CritCounterLimits.md` probe E (1,979-byte mock gate keyed on the config basename → `GATE_COUNTER_OK`); `w1/RevengerGateFailModes.md` E2 (`const_counter` and `inconsistent_counter` — `matched=8, met_target=false` on every shortcut still `REPLAY_GATE_CLEAN`, and the gate receipt records no counter argv/reader path); `w1/MutShortcutClasses.md` F4 (`matched=3, met_target=true` → CLEAN; `replay-gate.py:93-100` never recomputes `met`); `w1/CritCounterLimits.md` §2 rows 2–3 (crash-as-refutation: `sys.exit(7)` reader scored "below target"); `w1/CritClaimWidth.md` CE-5.1 (green counter never itself subjected to a refusal test) | sharpens 18, 67 |
```

## 3. Evidence pointer per claim (what grounds each row)

| row | defect class | ground |
|---|---|---|
| 68 | record defect F2 — `predicate_identity` false; nothing reads predicate values | `predicate-reconciliation.json` `PREDICATE_IDENTITY_FALSE` (three sentences: A `7c6c17f0…` claims+2 configs, B `8340aea5…` counter+6 receipts, C `09988625…` mini counter); `RevPredicateIdentity.md` HIGH-1 + probes M1/M2/M4 exit 0 with predicate rewritten; my read of `replay-gate.py:43` (key-existence only) and `c2-shortcut-gate-counter.py:23,73` (constant → receipt echo) |
| 69 | record defect F3 — registered-set drop invisible | `RevPredicateIdentity.md` M3 (7→3 CLEAN); `RevClaimsVsInstruments.md` F2 (7→4 `GATE_COUNTER_OK`); `ExecRecountC2.md` F3 (1-class drop undetected); `CritCounterLimits.md` §1 (floor met by one dead reader ×3 labels); `CritClaimWidth.md` CE-3; my read of `replay-gate.py:31,58` (`MIN_SHORTCUTS = 3` floor) |
| 70 | decisive counterexample + invariance lemma | `claim-stop.json` `decisive_counterexample` (nameset 8/8 ×3 seeds, sha256 verified by me §4); `ExecRedReproduce.md` §5.1 lemma (decode-preserving transform can't break content keys) + §7 fresh-content counter 9-class CLEAN; `CritClaimWidth.md` CE-1/CE-2 (payload-keyed 8/8 → REFUSED on registration); `MutShortcutClasses.md` F1/F6; `ScribeKnowledgeEntry.md` F1; `ExecPermuteAudit.md` (identity-permutation leak ≈1/474 on single-record fixtures) |
| 71 | record defect F4 — selftest blind to row drop and label collision | `MutGateBranches.md` §3 M3 (survivor: selftest exit 0, naive → CLEAN exit 0, mini → CLEAN; probes (i) `red-last` and (ii) reorder kill it — order-coincidence proven); `RevengerGateFailModes.md` F1/E5-name (label collision → CLEAN on red); `CritCounterLimits.md` §4 (`counter_target_mismatch` mutant survives selftest); `CritClaimWidth.md` CE-6 (exit-code-only kills; class names `s1..s3` never collide with production names); my read of `replay-gate.py:156-172` (SELFTEST_CASES over-target only at s1/s2; no row-count assert) |
| 72 | record defect (no-reader satisfiability) | `CritClaimWidth.md` CE-5 (basename-keyed liar counter → `GATE_COUNTER_OK` exit 0, six clauses true); `CritCounterLimits.md` probe E (mock gate → OK) and §2 (inconsistent `matched=8/met=false` → CLEAN; `sys.exit(7)` scored below target); `RevengerGateFailModes.md` E2 (const + inconsistent counters CLEAN; receipt carries no argv/reader path); `MutShortcutClasses.md` F4 (fake counter `matched=3, met=true` → CLEAN); my read of `replay-gate.py:93-100` (`met` trusted, `target` only cross-checked vs config) |

## 4. Commands run by this seat (read-only; every exit recorded)

| UTC (2026-10-25) | command (cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`) | exit |
|---|---|---|
| 07:31–07:32Z | `find … -name "QUALITY.md"` → `corpus/QUALITY.md` | 0 |
| 07:31Z | `wc -l corpus/QUALITY.md` → 107 | 0 |
| 07:31Z | `grep -n '^\|' corpus/QUALITY.md \| tail -30` → last row is 67 | 0 |
| 07:31–07:32Z | `sha256sum .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` → `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97` (== `claim-stop.json` `source_sha256`) | 0 |
| 07:32Z | `grep -n "MIN_SHORTCUTS\|predicate" tools/round-34/replay-gate.py` → `MIN_SHORTCUTS = 3` :31; key-only check :43; floor :58 | 0 |
| 07:32Z | `grep -n "PREDICATE" tools/round-34/c2-shortcut-gate-counter.py` → `:23` constant B, `:73` receipt echo | 0 |
| 07:32Z | `sed -n '90,135p' tools/round-34/replay-gate.py` → `run_counter` never recomputes `met == matched`; `over` filters `row["class"] != positive_spec["class"]`; `evaluate` CLEAN/REFUSED/UNEVALUABLE | 0 |
| 07:32Z | `sed -n '150,175p' tools/round-34/replay-gate.py` → SELFTEST_CASES put over-target readers only at s1/s2; MUTANTS = 3 anchors | 0 |
| 07:32Z | `date -u`; `cat /home/vgpnk/.omp/agent/RULES.md`; `git status --porcelain`; `git log --oneline -3` | 0 |
| 07:32–07:33Z | `git diff corpus/QUALITY.md` (read-only) → uncommitted rows 68–73 already drafted by the L1; `git diff corpus/lessons/round-34.md` (read-only) → uncommitted r34b append with M34-5..M34-11 | 0 |
| 07:32Z | `grep -rn "payload" w1/CritClaimWidth.md` → CE-1/CE-2 payload-keyed reader anchors | 0 |

No `git add/commit/stash/checkout/reset/pull/push` and no mutating `jj` anywhere; no lane file
other than this report was written. No builds, linters or test suites run (wave is read-only
verification + drafting); no counter executed by me — the measured claims above are cited to
wave-1 committed reports and the pinned source I read directly.

## 5. Conflicts reported verbatim (for the canonical judge)

**C1 — numbering swap between the landed lesson routes and this assignment.** The landed
`corpus/lessons/round-34.md` r34b append (uncommitted, worktree) routes: M34-7 → "QUALITY 69"
for the keyable-invariant class set, M34-8 → "QUALITY 70" for the registered-set equality.
My prompt assigns the same two criteria the other way round — "(69) a gate's registered class
set is asserted against its pinned set before CLEAN; (70) a fixture transformation must be
shown to break every invariant a shortcut can key on". The uncommitted `corpus/QUALITY.md`
worktree rows follow the lesson order (row 69 = invariants, row 70 = registered set). The
drafts above carry the assignment's numbering; the substance is identical either way, so the
L1 can land either order — but exactly one numbering must win, and the lesson's cross
references currently name the other one.

**C2 — `corpus/QUALITY.md` worktree row 68 fuses two criteria.** The uncommitted row 68 joins
(a) predicate byte-identity (my row 68, lesson route M34-6) with (b) the pins living in the
`freeze-integrity`-accepted container + the counting command re-hashing its pins (lesson
route M34-5). They are two defects with two instruments (F1's container/enforcement gap
repaired via `instruments.json`; F2's unread predicate disclosed only). Fusing is defensible —
both are "the claims file is the single source for its own freeze" — but it silently swallows
the M34-5 repair that already landed (`r34b/instruments.json`, 26 byte-identical pins +
receipt, `b917ea64`), which reads as stronger than "read it" in my draft. Verbatim, landed
row 68: *"A claim file is the single source for its own freeze: its pins live in the container
the lane's freeze gate accepts (top-level `instruments`), and its predicate sentence is
byte-identical in the claim, every config, the counter constant and the receipt. The counting
command re-hashes the pins and reads the predicate from the claim file rather than echoing a
constant; a paraphrased sentence or a map in the wrong shape is a defect, not a formatting
choice."* My draft keeps the predicate criterion standalone (as assigned); the L1's fused
form is a legitimate alternative — flagging so the choice is deliberate, not default.

**C3 — the landed row 71 omits the row-count assertion and CLI-level case my assignment
names.** Landed 71 covers (exit, verdict, over-set) kills, every-slot placement and the
reserved positive class. It does not require `len(rows) == 1 + len(shortcuts)` /
`shortcuts_below_target` pinning (the assertion that alone would have caught M3 without
ordering luck — `MutGateBranches.md` §3 draft cases `red-last` + `all-shortcuts-scored`), the
`cli-red-refused` case (`SELFTEST_CASES` invoke `evaluate()` in-process, never `main()` — M2b
was killed only incidentally by the mutant block), or `exit-status-ignored` (a counter whose
exit contradicts `met_target` is invisible to `run_counter`, which records `exit` but never
tests it). My draft above retains all three; they are each named by the wave-1 reports with
verbatim draft code.

**C4 — the landed row 72 is consistent-but-insufficient on my assignment's wording.** Landed
72 requires `met_target == (matched == target)`, crash-row drops and `--rev` binding. It does
not require that any reader ran: a basename-keyed counter (CE-5, `w1/CritClaimWidth.md`)
reports a perfectly consistent receipt and satisfies all six clauses while measuring nothing.
The consistency clause kills `inconsistent_counter` but not `const_counter`. My draft states
the missing leg — per-row execution evidence (reader digest, per-reader `exit`, or
name-invariance re-run) — as the criterion the assignment's phrase "runs no reader" requires.

**C5 — lesson row numbering inside the landed append vs QUALITY numbers.** The lesson's M34-5
fix column reads "QUALITY 68 route" while M34-6's also reads "QUALITY 68"; the number 68 is
assigned twice (consistent with the row-68 fusion in C2, but the lesson names it a "route"
for two different mechanisms). My rows 68 (predicate) and the pin-container content both
remain named in C2.

## 6. Out-of-scope and unrun items

- Did not edit `corpus/QUALITY.md`, `corpus/lessons/round-34.md`, `claims.json`,
  `claim-stop.json`, `tools/round-34/*`, SCORECARD/LOG/SKILL/PROVINCE — drafts live here only,
  per the hard rule that the L1 lands every doc edit.
- Did not re-run any counter or gate: wave-2 is read-only verification and drafting; the
  receipts cited are the committed wave-1 ones (`w1/*.md` each record argv/exit/UTC).
- The `MutFixtures.md` seat report is absent from `w1/` (prompt exists, no landed report);
  its four planned fixture-mutation results are not cited in any row above because no
  committed report grounds them. Row 70 rests on `MutShortcutClasses.md` F6 + `CritClaimWidth`
  CE-1 + `ExecPermuteAudit` + `nameset` instead — same mechanism class, committed evidence.
- Scratch: nothing written under `/fast/scratch/hyaku/kaidoku-r34b/w2/AQualityDrafts/` was
  needed (all reads were direct); no scratch artifacts to retain.

## 7. Verdict

`DRAFTS_COMPLETE` — five QUALITY rows (68–72 in the assignment's numbering) drafted above
with a lesson/evidence pointer and a `supersedes` column per row; every factual clause is
bound to a committed wave-1 report, the pinned sources, or a read-only command in §4. Two
numbering conflicts with the L1's uncommitted landed drafts (69/70 swap, row-68 fusion) and
two coverage gaps my drafts add back (row-count/CLI/exit-status legs on 71; the
execution-evidence leg on 72) are reported verbatim in §5 for the L1 to resolve at landing.
No claim re-opened, no instrument repaired, no score asserted.
