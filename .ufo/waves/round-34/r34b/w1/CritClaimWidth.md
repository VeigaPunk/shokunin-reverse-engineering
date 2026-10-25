# CritClaimWidth — width attack on R34-C2 (P34-shortcut-replay)

Seat: leaf critic, round 34 / run-6 re-dispatch / wave 1. Scope: width attack only — what
`registered` hides, what the single green surface proves, whether a universal is implied, and the
narrowest true sentence. No lane file was written except this report; every probe ran on copies under
`/fast/scratch/hyaku/kaidoku-r34b/w1/CritClaimWidth/`. No ELF carrier, fixture or reader was executed
as a program of interest; readers ran as `python3` under the counters only. No tool installed
(`python3 --version` = Python 3.14.8); nothing to record under the tooling directive.

`$S` below = `/fast/scratch/hyaku/kaidoku-r34b/w1/CritClaimWidth` (`$S/lane` = copy of the pinned
`tools/round-34` tree; `$S/probe`, `$S/mut`, `$S/liar2` = probes).

Claim under attack: R34-C2, frozen at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`.
Inherited R34-C1 was not run, read as a program, or scored.

---

## 1. Provenance verified before attacking (26/26 pins match at the frozen commit)

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
$ git rev-parse HEAD
c79bbe7b0959132b9873ff3431cf5eb313b58b33        # 2026-10-25T07:21:36Z
$ git status --porcelain      # only untracked .ufo/waves/round-34/r34b/** wave artifacts
```

For every one of the 26 `pins` entries in `.ufo/waves/round-34/r34b/claims.json` I hashed the blob
from the commit object (`git show <rev>:<path> | sha256sum`) and compared to the pin:
`{"pins": 26, "mismatched": []}` (2026-10-25T07:22:42Z). So the instrument set under attack is the
pinned one, not the working tree. `tools/round-34/replay-gate.py` pin
`8fa94b23…081c7558`; `c2-shortcut-gate-counter.py` `41d59703…e5a72`; both gate configs
`4483f385…c12ac9c` / `72b12941…6b1428`.

`before` state confirmed independently: `git cat-file -e ec3125ad…:tools/round-34/replay-gate.py`
→ absent. The gate is genuinely new this round; the claim's `before` is not misstated.

## 2. Independent reproduction (the claim's six clauses hold)

Scratch copy `cp -a tools/round-34/. $S/lane/tools/round-34/`, then (2026-10-25T07:19:36Z):

| probe | command (root = scratch lane copy) | exit | line |
|---|---|---|---|
| P1 green | `python3 -I -B tools/round-34/replay-gate.py --root . --config tools/round-34/gate-config-mini.json` | 0 | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-` |
| P2 red | same, `--config tools/round-34/gate-config-naive.json` | 2 | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization` |
| P3 selftest | `… replay-gate.py --selftest` | 0 | `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}` |

P1/P2/P3 reproduce `after/c2-at-instruments.json` (`green.line`, `red.line`, `selftest_line`) exactly,
including `positive_matched=8`. **The claim’s six clauses are true at the measured revision.** The
attack below is therefore about what those clauses can license, not about whether they hold.

## 3. The actual width of the green/red evidence: 1 discriminating class out of 7

I scored all nine reader programs in `tools/round-34/mini-fix/readers/` under both pinned counters
(`mini-counter.py` = permuting, `naive-counter.py` = raw), matched/8 (2026-10-25T07:22:06Z):

| reader | green counter | red counter | moves? |
|---|---|---|---|
| structural.py | **8**/T | **8**/T | yes (positive) |
| label_replay_full.py | 0 | **8**/T | **yes** |
| size_keyed.py | 1 | 1 | no |
| all_false.py | 0 | 0 | no |
| digest_keyed.py | 0 | 0 | no |
| fixed_slice.py | 0 | 0 | no |
| label_keyed.py *(unregistered)* | 0 | 0 | no |
| record_order_replay.py | 0 | 0 | no |
| string_scan.py | 0 | 0 | no |

Consequences for the width of `shortcuts_below_target=7`:
- **Six of the seven registered classes score identically on both counters**, so their "below target"
  carries no information about identity defeat; the entire red/green discrimination is one class
  (`label-memorization`) plus the positive control. `size-keyed`'s 1 is a coincidence with `alpha`
  (same value on both counters), not a defeat — the count "7 below target" is arithmetically right and
  evidentially 1.
- `label_keyed.py` is in the pinned tree but in neither config: registration is a selection, and the
  selection is already narrower than the authored reader set.

## 4. Counterexamples (all run, all reproducible from this report)

### CE-1 — an *unregistered* structure-blind class meets the target while the gate prints CLEAN
I generated `$S/probe/value_keyed.py`: it keys a memorized answer on header fields plus each record's
`(flags, value)` in record order, ignoring `name_off` and the name pool entirely — a canonical
"memorize the fixture set by an invariant key" class in the same family as `digest_keyed.py`.
Key invariance under the pinned permutation was checked against `mini-counter.permute` itself:
`{"distinct_keys": 8, "fixtures": 8, "permutation_invariant": true, "sizes": [512]}`.

```
$ python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader $S/probe/value_keyed.py
matched=8 target=8 met_target=true   (all eight fixtures ok)          P4_EXIT=0   2026-10-25T07:19:55Z
```
So on the *pinned green surface*, a shortcut class that no config registers reaches **8/8**. The
predicate's "none meets the target" is false as a universal and true only over the config's list.

### CE-2 — registering it flips the same gate to REFUSED
`$S/probe/config-green-plus-payloadkey.json` = pinned green config + `{"class":"payload-key"}`:
```
REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=payload-key
P5_EXIT=2   2026-10-25T07:19:55Z
```
Same gate, same counter, same eight fixtures; the verdict is a function of the **config**, not of the
counter. `REPLAY_GATE_CLEAN` therefore attests "the classes I listed fail", never "identity-defeating".

### CE-3 — a shape-only counter reaches CLEAN with three weak registered classes
Pinned `naive-counter.py` (the claim's own "shape-only" counter), config restricted to
`{all-false, fixed-slice, digest-keyed}` (`MIN_SHORTCUTS` = 3, satisfied):
```
REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=3 shortcuts_over_target=-
P6_EXIT=0   2026-10-25T07:19:55Z
```
The kill rule's "no shortcut class may be dropped to reach CLEAN" is prose; the gate enforces a
**count** floor, not a taxonomy. A future claim can reach CLEAN on a counter that memorizes labels.

### CE-4 — "structural" is a free-text label, not a verified property
Naive counter with `positive_control = label_replay_full.py` (class renamed `structural`) and the
label class removed from `shortcuts`:
```
REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=-
P7_EXIT=0   2026-10-25T07:19:55Z
```
The pure label-memorizer is pronounced the structural control and the shape-only counter is cleared.
Nothing in the gate checks that the positive control decodes by structure; the gate measures a
**separation between two authority-chosen reader populations**, not structuralness.

### CE-5 — a counter that never measures anything reproduces the whole six-clause receipt
`$S/liar2/tools/round-34/mini-fix/mini-counter.py` (control probe) runs no reader, never reads
`expected.json`, and answers from the reader's basename (`structural.py` → 8, everything else → 0).
Through the pinned gate:
```
REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-
P9B_GATE_GREEN_EXIT=0
```
and through the claim’s own counting command:
```
$ python3 -I -B …/c2-shortcut-gate-counter.py --root $S/liar2 --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33
GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3
  red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-
P9B_EXIT=0   2026-10-25T07:22:04Z
```
All six clauses true, receipt `met_target: true`, over a tree that is **not** the pinned one.
Two separate defects surface here:
1. **Self-report trust.** `run_counter` reads `matched`, `target`, `met_target` from the counter's own
   JSON and `evaluate` never recomputes `matched == target`, so `green_positive_matched=8` is a number
   the instrument under admission prints about itself. The gate is a receipt-shape check plus a
   differential; it is not an independent decode verification.
2. **The red clause scores a different programme.** `gate-config-naive.json` names
   `naive-counter.py`; `gate-config-mini.json` names `mini-counter.py`. The green counter is never
   itself subjected to a refusal test, so a counter that reports without measuring is inside the
   claim's own evidence path.
3. **The revision label is unverified.** The receipt above prints `measured_revision=c79bbe7b…` for a
   modified instrument tree: the counting command never invokes the pinned
   `tools/round-34/freeze-integrity.py` (which is itself outside the 26 pins). Pins live in
   `claims.json` only; enforcement is manual. My §1 check is what makes this report's reproduction
   meaningful — the command does not.

### CE-6 — the mutant count is a sample, not coverage
Mutant gate: `over = sorted(… if row["met_target"] and row["class"] != positive_spec["class"]
and row["class"] not in ("fixed-slice",))` — silently drops a registered class from the refusal set:
```
$ python3 -I -B tools/round-34/replay-gate.py --selftest
{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}   P8_SELFTEST_EXIT=0
REPLAY_GATE_REFUSED … shortcuts_over_target=label-memorization                  P8_RED_EXIT=2
REPLAY_GATE_CLEAN  … shortcuts_below_target=7                                   P8_GREEN_EXIT=0
2026-10-25T07:21:27Z
```
Every pinned signal survives (the pinned pair never makes `fixed-slice` exceed target). The selftest
also scores kills by **exit code only** (`run.returncode != expected_exit`), and its synthetic class
names are `s1..s3`, so any mutation keyed to a production class name is invisible to it.
`mutants_killed=3` means "the three registered mutants die", not "the refusal branch is correct".

## 5. What the single green surface proves

Facts extracted from the pinned bytes (2026-10-25T07:21:36Z): 8 fixtures, **all exactly 512 bytes**,
one format (`MREC` v1, `records_off=16`), one generator (`build.py`, one `SPEC`), expected.json
derived from the writer's `SPEC` (not from a decoder — the provenance is sound and not circular).
The only transformation `mini-counter.py` applies is **name-pool reordering with `name_off`
rewriting**; total size, record order, `(flags, value)` payload and header fields are invariant.

Green therefore proves exactly: *on eight author-built synthetic 512-byte fixtures, `structural.py`
reproduces the writer's records through a name-pool permutation, and the seven named programs do not.*
It says nothing about other sizes, record counts, record orderings, header corruption, multiple
pools, or the ELF domain (the fixtures are declared "never domain evidence"). CE-1 is the concrete
demonstration that the surface is narrow: a class invariant under its only perturbation scores 8/8.

## 6. Is a universal implied? Yes, two, and both fail

- The predicate's "…and none meets the target" reads as a universal over shortcut classes; §4 CE-1
  exhibits a structure-blind class that meets it on the same eight fixtures.
- `replay-gate.py`'s own docstring draws the converse — "If any shortcut meets the target, the counter
  measures shape, not structure, and the freeze is refused" — whose contrapositive, CLEAN ⇒ "not
  shape", CE-4 and CE-5 falsify: the same CLEAN is produced with a label-memorizer as the positive
  control, and by a counter that measures nothing.

## 7. Claim-record defects (independent of the six clauses)

1. **`predicate_identity` is literally false.** Verified by string comparison (2026-10-25T07:22:04Z):
   `claims.predicate == gate-config-mini.predicate == gate-config-naive.predicate` → **True**;
   `claims.predicate == c2-shortcut-gate-counter.PREDICATE` → **False**;
   `receipt.predicate == claims.predicate` → **False**. The counter's constant is a different,
   narrower sentence ("…refuses the shape-only counter whose label-keyed memorization meets its
   target, clears the identity-defeating counter on the same eight fixtures where every registered
   shortcut class stays below target…"), and it is that sentence the receipt carries. The record
   asserts one sentence in three places; only two places have it.
2. **Pin coverage is complete but unenforced** (§4 CE-5): 26 pins cover 26 of the 29 files in
   `tools/round-34` at the commit; the three unpinned files are R34-C1's
   (`elf-version-needs.py`, `version-needs-counter.py`) and `freeze-integrity.py`, and no C2 clause
   requires hash checking.
3. `MIN_SHORTCUTS = 3` is the only breadth constraint, and 3 weak classes pass (CE-3).

## 8. Impacted axes

- **depth (the claim's own axis): survives but thinner than the record suggests.** The surface moved
  from "no gate" (verified absent at `ec3125ad`) to a gate that discriminates two named counters on
  one surface. That is a real, non-zero capability increment and no numeric proxy was touched
  (`scores_unchanged` 10/10/10 is consistent with my read of the receipts).
- **coverage / calibration: untouched** — I make no claim on them, and nothing here retires them.
- **Risk if read broadly:** any future pre-freeze claim citing `REPLAY_GATE_CLEAN` as evidence that a
  counter is identity-defeating would be relying on a config-relative refusal test over one class that
  actually moves (CE-2, CE-3), a free-text positive label (CE-4), and a self-reported score (CE-5).
- **R34-C1: not touched.** No carrier, no production reader, no receipt of that claim was read as
  evidence here.

## 9. Smallest safe correction (draft only — nothing applied; `c79bbe7b` must not be edited)

Because all six clauses hold, no post-freeze instrument change is warranted *for this claim*. The
corrections are documentary plus next-round binding:

1. LOG/SCORECARD note (L1 lands it): record defect §7.1 — `predicate_identity` overstates identity;
   the scored sentence is the counter's narrower one. Do not rewrite the pinned predicate; record the
   fact and carry the quantified form forward.
2. Next pre-freeze claim states the predicate config-relative: "every class listed in the gate config
   **at that revision**" and quotes the class list (the gate payload already carries `rows`; lift the
   names into the receipt top level) with "not exhaustive" said out loud.
3. Register at least one class the counter author did not write — `$S/probe/value_keyed.py`
   (permutation-invariant payload key, 8/8 today) — plus one class per invariant axis (label, size,
   whole-file digest, fixed slice, record order, payload). This forces the green counter to perturb
   record order and payload position, not only the name pool; replacing `MIN_SHORTCUTS=3` with an
   axis-coverage check is the smallest gate change that makes CLEAN mean what the prose says.
4. The C2 counting command should verify the 26 pins (invoke `freeze-integrity.py`) before scoring;
   today `measured_revision` is an unchecked argv string (CE-5's receipt).
5. Selftest: score kills by `(exit, verdict, over-set)`, not exit code alone, and use at least one
   production class name, so class-name-keyed mutations are reachable (CE-6).
6. Accept in the record that the gate cannot attest the counter's *measurement* (CE-5); it attests the
   receipt's shape. Any claim that the admitted counter decodes structure needs an independent
   re-score, not a CLEAN line.

## 10. Narrowest true sentence the evidence supports

> For the two counters and the seven registered readers pinned at `c79bbe7b`, on eight author-built
> 512-byte synthetic fixtures whose only perturbation is name-pool reordering, the gate prints
> `REPLAY_GATE_CLEAN` when the counter renames and permutes (structural 8/8, six registered classes at
> 0, size-keyed at 1, label-memorization 0) and `REPLAY_GATE_REFUSED` naming `label-memorization`
> when it does not, and its selftest kills the three mutants it registers.

What that sentence does **not** say, each falsified above: that no structure-blind class meets the
target (CE-1: 8/8 unregistered), that the class list is not a choice (CE-2, CE-3, `label_keyed.py`
unregistered), that "structural" is verified (CE-4), that the admitted counter measured anything
(CE-5), or that the refusal branch is mutation-complete (CE-6).

---

VERDICT: R34-C2 SURVIVES AS WRITTEN — six clauses reproduce exactly at c79bbe7b (P1/P2/P3, pins 26/26) — SURVIVES NARROW ONLY: the receipt licenses a config-relative refusal test on one discriminating class over one 512-byte surface, and the claim record's `predicate_identity` sentence is false as stated (§7.1); no universal reading is supported and the next pre-freeze use must adopt §9.2–§9.5.
