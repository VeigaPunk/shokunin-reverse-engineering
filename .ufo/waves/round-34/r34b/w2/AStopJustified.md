# AStopJustified — does "falsified measure / honest stop" survive an outside closure?

Seat: `L1Kaidoku34-2.AStopJustified` (critic, leaf — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only; no VCS mutation; no lane write).
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/AStopJustified/` (`root/` = a byte copy of `tools/round-34`;
`out/` = receipts; readers and configs in the scratch root only).
Tooling: **none installed or upgraded**. `/usr/bin/python3` = Python 3.14.8 (preexisting), stdlib + `git`
reads only. `pacman` untouched (transactions paused host-wide); no network.
Scope: the stop record `.ufo/waves/round-34/r34b/claim-stop.json` (landed `cd75b92e`), its evidence, its
five disclosed defects and its proposed repair. Not reopened: the claim, the frozen instruments, any score.

## 0. Axes named (Godspeed)

| axis | proxy | direction |
|---|---|---|
| A1 predicate fidelity | does the frozen predicate hold on the frozen bytes? | ↑ |
| A2 measure validity | is the frozen target reachable by a control that skips the claimed work? | ↑ |
| A3 record completeness/provenance | do the stop's evidence and defect list bind, and are they orderable against the commits that contain them? | ↑ |
| A4 repair adequacy | does each proposed repair close the defect it names, and nothing weaker? | ↑ |

Every finding below adds a binding or corrects a pointer; no finding trades one axis down for another.

## 1. What I re-derived from the frozen bytes (recomputed, not quoted)

| # | check | command (cwd as noted) | exit | UTC | result |
|---|---|---|---|---|---|
| 1 | 26 claim pins recompute | `python3 -c` sha256 over `claims[0].pins` | 0 | 07:37:21Z | `mismatch []`, 26/26 |
| 2 | predicate A (claims + both configs) | sha256 of the sentence | 0 | 07:31Z | `7c6c17f0…96279b`, 31 words, all three sites equal |
| 3 | predicate B (counter constant + receipt) | sha256 of the sentence | 0 | 07:31Z | `8340aea5…611c8`, 46 words; `A == B` → **False** |
| 4 | stop's `predicate_frozen` is sentence A | string equality vs `claims[0].predicate` | 0 | 07:37Z | `True` |
| 5 | six clauses on the frozen receipt | `.ufo/waves/round-34/r34b/after/c2-at-instruments.json` | 0 | 07:31Z | six `true`, `exit 0`, line equals `after/c2-at-instruments.txt` |
| 6 | the seven registered classes stay below the green target | `replay-gate.py --root … --config` with nameset appended | 2 | 07:36:07Z | `shortcuts_below_target=7 shortcuts_over_target=content-multiset` |
| 7 | nameset reaches the counter target | `mini-counter.py --root . --control-reader …/nameset.py` (3 seeds) | 0/0/0 | 07:32:26Z, 07:36:05Z | `matched 8`, `met_target true`, every reader exit 0 |
| 8 | nameset source binds | `sha256sum …/CtlMultiset-files/nameset.py` | 0 | 07:31Z | `2e8feaea…8b297` = stop `source_sha256`; committed in `cd75b92e` |
| 9 | the pin container is a real map | `freeze-integrity.py --root . --round 34 --claims …/instruments.json` | 0 | 07:35:09Z | `CLEAN pins=26 freeze=b917ea64ebbe` |
| 10 | the frozen claims file is **not** such a map | same, `--claims …/claims.json` | **3** | 07:35:09Z | `ERROR schema code=instruments_missing where=instruments` |

The stop's factual core is therefore reproducible from committed bytes: on the frozen green surface an
unregistered, structure-blind reader reaches 8/8 on three seeds; the seven registered classes do not; and the
gate's own refusal branch bites the new class when it is registered (§2).

## 2. The two readings, re-derived

### 2.1 Reading A — registered-scope literalism

The governing sentence (A) is: *"a finite structural-decoding counter is frozen only after **registered**
structure-blind shortcut readers are scored under the counter's own predicate and none meets the target, while a
registered structural reader does."*

* The quantifier is explicit: **registered**. It is not "all structure-blind classes", nor "no shortcut
  whatsoever".
* Its asserted facts hold at `c79bbe7b`: seven registered classes scored, none at target (green
  `shortcuts_below_target=7`), the registered structural control at 8/8 (receipt `positive_matched: 8`).
* The claim's own `kill_rule` (six clauses) is also satisfied; the stop itself says so
  (`frozen_counter_verdict.note`).
* **Implied admission standard:** predicate literalism — the frozen predicate + the frozen six-clause kill rule
  *are* the whole test.
* **Consequence:** R34-C2's target is met, so the claim is a hit and the stop **over-reads**.

### 2.2 Reading B — measure validity

A is a *procedure* clause ("is frozen only after …"), a necessary condition on a freeze, not a sufficiency test
on what the freeze produced. It also **delegates**: "scored under the counter's own predicate". That delegated
predicate is `mini-counter.py:PREDICATE` — *"only record-array traversal associates a name with its record"* —
and the nameset falsifies it directly: it reads no header, no record entry, no `name_off` (verified by reading
`nameset.py`: a SONAME regex plus a stored table). The freeze procedure was followed; the thing it was
supposed to certify is false.

The lane's admission standard is explicit and recoverable:

* QUALITY 48 (`corpus/QUALITY.md:58`): every claim's counter is scored on controls *"and a control that meets
  the target forces a re-design before data."*
* QUALITY 67 (`corpus/QUALITY.md:77`): *"if it meets a frozen target, stop without amending, re-scaling or
  relabelling the claim."*
* r29-C1 (`corpus/lessons/round-29.md:9`): a target a trivial baseline also met was rejected as an honest
  stop, not credited.
* r32-C2 (`corpus/lessons/round-32.md:10`; spot-check `round-32-verifier-spotcheck.md:61-75`): *"an explicitly
  negative assessment meets that target … The measure cannot support a calibration improvement; it is not
  re-frozen, re-scaled or relabelled exploratory."* Same shape as this stop.
* **Same-round precedent:** R34-C1 was stopped on exactly this rule one claim earlier (size-keyed fixed-slice
  replay 12/12 → *"falsified measure / honest stop"*, `corpus/lessons/round-34.md:41-45` region).

**Implied admission standard:** §9's *"a do-nothing control must not reach the target"* (the assignment's
wording; its landed equivalents are QUALITY 48 and 67, plus the r29/r32/R34-C1 precedents).
**Consequence:** the stop is right, and the verdict word must be **falsified measure**, not *miss*.

*Note.* I could not find a lane document literally numbered §9 carrying that sentence; the sentence's landed
equivalents are QUALITY 48/67 as quoted above. I treat the assignment's quotation as the standard.

### 2.3 The decisive test between A and B, measured

A cannot be the admission test, because it is nearly vacuous. Through the **frozen, unmodified** gate and the
**frozen, unmodified** C2 counter (only scratch configs differ; cwd = scratch root):

| configuration | gate verdict | exit | UTC |
|---|---|---|---|
| green config trimmed to 3 classes (the floor) | `REPLAY_GATE_CLEAN … below=3` | 0 | 07:36:05Z |
| 7 classes, `label-memorization` removed, a different reader re-registered under a new class name | `REPLAY_GATE_CLEAN … below=7` | 0 | 07:36:05Z |
| 7 classes, over-target reader relabelled `structural` (the positive control's reserved label) | `REPLAY_GATE_CLEAN … below=6` | 0 | 07:36:06Z |
| the third config installed as the pinned green config, frozen C2 counter | `GATE_COUNTER_OK … green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` | 0 | 07:33:19Z |

Under A all four are admissible: a gate whose class set is a floor of three, or whose over-target reader is
hidden by a free-text label, still satisfies "registered readers were scored and none met the target". A
closure that accepted that would be accepting a gate that cannot refuse the very class it names. B is the only
non-vacuous reading, and it is the reading the lane already applied to R34-C1 in the same round. **I would
defend B to an outside closure.**

## 3. Attacking the stop — the strongest counterexamples I can build

**CE-1 (the one that lands).** The stop's own producer recommended the opposite verdict and the stop does not
say so. `w1/ExecRedReproduce.md:163`: *"**Retain R34-C2 as CLEAN.** No clause moved; the two pinned configs
and `label-memorization` are intact."* Its §9 concedes the finding *"does not falsify any of the six frozen
clauses, and under the kill rule … cannot be repaired inside R34-C2 — it is next-round material or an honest
LOG entry."* So the L1 converted a producer's "retain + route" into "falsified measure + stop" without
recording the dissent. That is the sharpest thing an outside closure can say about this record.
*Resolution:* the producer's alternative is `not_claimed`-grade (no credit either way). The L1's choice is the
stricter of two admission judgments, is `not_claimed` on capability and score, and is the same judgment the
lane applied to R34-C1. It is defensible — but only as an **admission judgment**, and the record must show the
dissent. Smallest correction: one `dissent` field quoting `ExecRedReproduce.md:163` and §9.

**CE-2 (a wording defect, not a factual one).** The stop's field `kill_rule_applied` is *not* the claim's
`kill_rule`. The claim's rule reads *"if any of the six clauses … is false at the measured revision, the claim
is a miss …"*; the stop's applied sentence is *"a target met by a control that skips the claimed work is not an
improvement."* An outside reader of `claim-stop.json` alone sees a miss rule that the frozen claim does not
contain. The content is correct **as the admission standard** (QUALITY 48/67) but is mislabelled as the frozen
kill rule. Smallest correction: name both — "claim kill_rule (six clauses) satisfied; admission standard
QUALITY 48/67 + r29-C1/r32-C2 applied to the measure" — and add `predicate_status: "satisfied as written
(registered scope)"`.

**CE-3 (what would overturn B, and does not).** If the 8/8 class were doing the claimed work — e.g. resolving
`name_off` — the stop would be wrong. `nameset.py` never touches a header or a record; its association comes
from `TABLE`, keyed by the sorted SONAME set, which `permute()` provably preserves (`permute()` rewrites only
the pool order and each `name_off`; decoded content and the name multiset are invariant). So no such
counterexample exists in the frozen bytes.

**CE-4 (a stronger class than the stop's, same surface).** The green surface is defeated *without any
memorized table*: the reader's cwd is the judge's root, where `tools/round-34/mini-fix/expected.json` and the
pristine fixtures are readable by relative path.

* `cwdprobe.py` (scratch) run by the frozen counter: `{"cwd": "<root>", "expected_exists": true,
  "fixtures_exists": true}` (07:32:14Z).
* `keyleak.py` (scratch; keys the pristine fixture by its name multiset, then replays `expected.json`):
  `matched 8`, `met_target true`, **exit 0** (07:32:14Z, re-verified 07:36:04Z).
* `pathhash.py` (scratch; reads **zero input bytes**, keys only on the basename the counter itself wrote —
  `opaque-<sha256(transformed)[:20]>.data` — using a table computed offline from the committed default seed
  `kaidoku-r34-mini-v1`): `matched 8`, **exit 0** at the production seed (07:36:04Z); `matched 0`, exit 1 at
  `--seed alt-1` (07:36:04Z).

So the production green receipt (default seed, the seed actually used) is defeated by a *pure path replay* —
the class the naive red case exists to expose — and the stop's class is not even the cheapest one. This
strengthens the stop's conclusion and weakens its framing: "opaque temporary paths" is the only opacity the
surface has.

## 4. The stop's decisive evidence — does it bind?

| item | check | result |
|---|---|---|
| source identity | `nameset.py` sha256 `2e8feaea…8b297` = stop `source_sha256`; added in `cd75b92e` | binds |
| pre-stop producer receipts | `ExecRedReproduce.md` green 07:19:02Z, `alt-1/alt-2` 07:19:56Z, exit 0/0/0, committed `b917ea64` (`2026-10-25T04:22:31-03:00` = **07:22:31Z**) | **predates the stop** (07:23:47Z) |
| reproduction, independent | my three-seed run, §1 row 7 | reproduces |
| `decisive_counterexample` receipt field | absent; `l1_rerun_utc` = `07:28:00Z (approximate; exact clock in the wave report)` and names no report file | **does not bind** |
| ordering of that rerun | stop commit = 07:23:47Z; cited rerun = 07:28:00Z | rerun **postdates** the record citing it |
| the only on-disk rerun receipt | `w1/CtlMultiset-files/nameset-green-receipt.json`, mtime `2026-10-25T04:34:01-03:00` = **07:34:01Z**, `git ls-files --error-unmatch` → *did not match any file(s) known to git*; all four `utc_start`/`utc_end` values identical | untracked, post-stop, batch-stamped |

Peer `w2/AStopCompleteness.md` P1-1/P1-2 reached the same dates independently; I confirm them from my own reads.
The stop is **not** evidence-free — the producer's clocked run precedes it and reproduces — but the L1's own
rerun is post-dated and unbound. This is a QUALITY 73-class defect (`receipt carries argv, reader digest and
the commit it read`) that the stop does not list.

## 5. The five disclosed defects — verified, with one correction each

| id | stop's claim | my measurement | verdict on the claim | correction |
|---|---|---|---|---|
| F1 | frozen pins live under `claims[0].pins`; `freeze-integrity.py` exits 3 `instruments_missing`; no instrument hashes a pinned file | exit **3** `instruments_missing` on `claims.json` (07:35:09Z); `CLEAN pins=26` on `instruments.json`; `grep -n hashlib\|sha256` in `c2-shortcut-gate-counter.py` and `replay-gate.py` → **exit 1, no match** | **accurate** | `repair_landed` overstates: the container is clean *when freeze-integrity is invoked*; the counting command still hashes nothing, and `after/c2-at-instruments.json` carries no pin digest. Say "separately enforceable, not enforced in-run". |
| F2 | predicate identity false: A (claims/configs) vs B (counter/receipts) | A `7c6c17f0…`, B `8340aea5…`, `A==B False` (§1 rows 2-3) | **accurate** | none; disclose-only is correct for frozen bytes. The cited repair route, QUALITY 68, now exists at `corpus/QUALITY.md:78` (landed `66b84027`). |
| F3 | a class drop down to the `MIN_SHORTCUTS` floor still returns CLEAN | 3-class config → `REPLAY_GATE_CLEAN` exit 0; **and** a 7-class config with a substituted class → CLEAN; **and** a relabelled over-target class → CLEAN; the third one turned the frozen C2 counter to `GATE_COUNTER_OK` | **accurate, and understated** | "assert class count == pinned count" does **not** close it: substitution and relabelling preserve the count. Require the pinned **digests** (config + reader paths), i.e. QUALITY 70's "count, class names and reader digests" (`corpus/QUALITY.md:80`). |
| F4 | gate mutant M3 (ignore last shortcut row) survives its selftest and turns the red case CLEAN | scratch mutant (`for item in config["shortcuts"][:-1]:`): selftest `{"cases":12,"failures":0,"mutants_killed":3}`, exit **0** at 07:36:08Z; red config → `REPLAY_GATE_CLEAN`, exit **0** at 07:36:09Z (unmutated gate on the same config: `REPLAY_GATE_REFUSED`, exit 2) | **accurate** | the proposed red-last case kills M3 specifically; "every slot" plus an over-set name assertion is the stronger form already landed as QUALITY 71 (`:81`). |
| F5 | receipts were untracked at first audit; repaired at `b917ea64` | `git ls-tree -r c79bbe7b -- .ufo/waves/round-34/r34b/` → only `claims.json`; `after/c2-at-instruments.json` first appears in `b917ea64` | **accurate** | none for the five control/production receipts. The stop's own decisive rerun receipt is still untracked (§4). |

## 6. Defects the stop does **not** disclose (same frozen bytes)

| id | defect | evidence | later capture |
|---|---|---|---|
| X1 | the judge's answer key is reachable from the reader: `cwd` is inherited from the counter, so `expected.json` and the pristine fixtures open by relative path | `cwdprobe.py` → `cwd=<root>, expected_exists=true, fixtures_exists=true` (07:32:14Z); `keyleak.py` → `matched 8`, exit 0 (07:36:04Z) | not in the stop; QUALITY 69 (`:79`) covers the invariant set, not the cwd |
| X2 | the "opaque" path is `opaque-<sha256(transformed)[:20]>.data` and the default seed is a committed constant, so a zero-byte path reader replays the production run | `pathhash.py` 8/8 exit 0 at default seed, 0/8 at `alt-1` (07:36:04Z) | QUALITY 69 names "transform/seed reuse"; the stop's one class is invariant-only |
| X3 | the positive control's class label is reserved but not validated: an over-target reader labelled `structural` is filtered out of `over` | relabelled green config → gate CLEAN (07:36:06Z); installed as the pinned config → frozen C2 counter `GATE_COUNTER_OK`, all six clauses true (07:33:19Z) | M34-9 / QUALITY 71, landed `66b84027` — **after** the stop |
| X4 | `--rev` is echoed, never bound: neither P34 instrument reads a commit; the receipt's `measured_revision` is caller-asserted | `grep` shows no `hashlib`/git use in either instrument; `c2-shortcut-gate-counter.py` only stores `args.rev` | M34-10/M34-11, QUALITY 72/73 |
| X5 | the stop's "five defects" were closed before wave 1 closed: `CritCounterLimits.md`, `MutShortcutClasses.md`, `RevFreezeOrder.md`, `ExecSeatSelftests.md` all landed at `66b84027` (07:32:25Z), eight minutes **after** the stop | `git log -1 --format='%h %cI'` per file | lesson `M34-5..M34-12` (`corpus/lessons/round-34.md:57-61`) |

X1-X4 do not weaken the stop; they show the stop's defect list is a *subset* of the wave's findings, and that
the binding record and the landed lesson disagree about what wave 1 found. The lesson is authoritative for the
extra defects; the stop should point at it.

## 7. The proposed repair — attack, and the smallest safe correction

1. **F1's container.** `.ufo/waves/round-34/r34b/instruments.json` is a second authority for the same 26 pins,
   and it is itself unpinned (nothing anchors its own bytes; `freeze-integrity` measures from the commit that
   **added** it — `commits[-1]`, the oldest add — so a delete/re-add does not reset the freeze, but a rewritten
   container is still self-declared). More importantly, no in-run consumer reads it (X4). *Correction:* one
   change closes F1-in-run, F3 and X3 — the counting command re-hashes `claims[0].pins` (26 digests) and exits
   2 `pinned_input_changed` before running, exactly QUALITY 68's route (`corpus/QUALITY.md:78`). Every model of
   F3/X3 I built requires editing a pinned file, so a digest check refuses all three. No second map is needed;
   if the container stays, its own digest must be pinned somewhere the container does not control.
2. **F3's count assertion.** Insufficient (§5). Count+names+digests per QUALITY 70, or the digest check above.
3. **F4's red-last case.** Sufficient for M3; extend to every list slot and assert the over-set **name**, per
   QUALITY 71.
4. **The measure itself.** The class-set repair cannot close X1/X2, because they are not classes — they are the
   surface's reachability and naming. The validated successor is `w1/CtlMultiset-files/mini-counter-fresh.py`
   (sha `5181330d…`): content generated per run from `os.urandom`, expectation computed from the generation
   (so `expected.json` replay is useless), reported 8/8 for the structural control and 0/8 for all nine
   shortcut classes (`ExecRedReproduce.md` §7). *Correction:* also run the reader with a cwd outside the
   judge root and stop putting a content digest in its input path — the fresh surface survives X2 only because
   the content is fresh, not because the path is opaque.
5. **What must not change:** the six clauses, the target, the registered class set, the labels — the stop
   already respects this, and nothing I did moves a clause (I only ran scratch configs and scratch readers).

## 8. Impacted axes

| axis | impact |
|---|---|
| depth (the claim's axis) | the capability is not admitted; no score moves (`10 → 10` stands). My findings add no depth credit. |
| calibration / coverage | untouched by this review; no receipt or class edit. |
| record provenance (A3) | F1-F5 verified; X1-X5 and §4 add bindings the stop lacks; the decisive rerun must be bound or marked post-landing. |
| measure validity (A2) | independently reconfirmed and strengthened (X1, X2, X3). |
| no harm | lane `tools/` unchanged (`git status --porcelain -- tools/` empty), 26/26 pins recompute after all probes (07:37:21Z), `__pycache__` mtime unchanged at 04:19. No lane file written by this seat. |

## 9. Verdict line

**B is defensible: the stop's verdict is right on the measure — an unregistered, structure-blind reader
reaches the frozen green target at 8/8 on three seeds, and the target is reachable without any embedded answer
table (the judge's own `expected.json`, readable from the reader's cwd) and by a reader that reads zero input
bytes at the committed default seed — but the stop over-reads only in wording, not in outcome: the frozen
predicate (registered scope) is *satisfied as written*, so the stop's ground must be the admission standard
(§9 / QUALITY 48 & 67 / r29-C1, r32-C2, R34-C1), its `kill_rule_applied` must say so, and its five-defect list
must add X1-X5 and the producer's recorded dissent (`ExecRedReproduce.md:163`). Reading A is refuted as an
admission test by three measured CLEAN configurations through the frozen instruments.**
