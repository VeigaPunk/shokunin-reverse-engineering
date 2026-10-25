# ASiblingStop — cross-lane precedent for an honest stop on a shortcut falsification

Seat: `L1Kaidoku34-2.ASiblingStop` (wave 2, attack-the-stop). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Assignment: find other lanes' recent rounds that stopped honestly on a shortcut/baseline falsification, name the
closest precedent and its routing (what the closure accepted and rejected), and say what this lane should copy or
avoid. Read-only. No lane file written except this one. No score awarded or proposed. The R34-C2 claim is not
reopened, no frozen instrument is edited, and the twelve R34-C1 carriers and the production reader were not run.

Method: MANIFEST rounds ledger + committed lane and fleet reports + committed lesson/QUALITY rows + the
round-33/34 verifier spot-checks, plus a set of bounded probes of the round's own mini surface (below). Everything
cited was read from committed bytes or from a lane working tree; the only executions were python counters in my
own `/fast/scratch/hyaku/kaidoku-r34b/w2/ASiblingStop/` scratch, with readers run by counters, never as programs
of interest.

## 1. Precedent inventory

The fleet has a large, well-recorded population of honest stops. `MANIFEST.json` rounds ledger at 2026-10-25T07:37Z:
**95 `rejected-honest-stop` entries across 18 lanes** (`/fast/scratch/hyaku/kaidoku-r34b/w2/ASiblingStop/fleet-stops.txt`).
Five are close enough to R34-C2 to be load-bearing:

| Lane / round | Falsifier | Closure verdict | Recovery |
|---|---|---|---|
| **chousa r33** (2026-10-23) | a fixture-literal mask gate scored 156/156 on the frozen C1 counter post-data | `rejected-honest-stop`; C1 `unprovable-but-better`; no score | chousa r34 rebuilt the counter with per-seed content, admitted |
| chousa r32 (2026-10-23) | a no-reader metadata-order control scored 132/132 on C2 | same class, first instance; C1 capability row kept with caveat | r33 routed the same remedy |
| **kake r34** (2026-10-22) | do-nothing lookup/transcription controls met both declared targets (28/28, 5/5) | `rejected-honest-stop`; work judged real, `unprovable-but-better`; no capability row | kake r35 sealed inputs, r36 admitted |
| kake r37 (2026-10-23) | the shortcut follow-up control met C1 before any build and the declared consequence was not applied | `rejected-honest-stop`, "no axis harmed" | r38 re-froze classes incl. the build/control boundary |
| mado r24 (2026-10-23) | v2 counter still met by a post-data shortcut control; 12/23 passing rows were attribution content | `rejected-honest-stop`, both claims `unprovable` | mado r25 rebuilt v4 with an external oracle, 10 shortcut shapes scored pre-data, admitted |

## 2. Closest precedent — chousa r33 (with chousa r32 as the class's first instance)

**What was falsified.** C1 operability met its frozen predicate on the landed gate (60/156 → 156/156) but a control
that "masks the counter's six fixed confuser strings, regex-strips nested containers and counts repeated keys"
also scored 156/156 (`chousa-shokunin/corpus/lessons/round-33-verifier-spotcheck.md:30-31`, gate `ae7d4bfc`). The
spot-check's line 72 pins the mechanism: *"The six masked literals equal the counter's six module-constant
confusers; no confuser content varies by seed. Counter unchanged after it."* The lane reported this itself
(`.ufo/reports/round-33/chousa.md`: "the counter does not verify clause 3… this is not a clean verification under
§9"), so the stop was not extracted by a closure — it was authored by the producing lane and confirmed from bytes.

**What the closure accepted.** The report; the rule application; "no axis harmed"; the instrument stays; the lane's
capability row lands with an explicit counter caveat while the round adds no admitted capability (MANIFEST
`rounds[529].capabilities_added` is empty); QUALITY rows 40–41 land with able-to-fail pointers; the differential
fuzz evidence stays but is not counted as the frozen measure ("The differential fuzz is not the frozen measure…
It cannot rescue the claim"). Axis verdict `unprovable-but-better`, score 3 → 3.

**What the closure rejected.** Admission, any score movement, and the counter as verification of clause 3
(`reject (post-data)` in the claim table, `:107`). It also recorded the blocker class and its recurrence:
"the same as round 32 (a frozen counter met by a post-data shortcut control…). Recorded for the orchestrator"
(`:40-41`).

**How the lane recovered.** chousa r34's C2 counter generates *content* per seed — "37 records in 17 classes… all
content generated per seed: random lowercase vocabulary, random separators, span lengths drawn… ids and file names
random hex; record and file-creation order shuffled; random mtimes" (`chousa-shokunin/corpus/evidence/round34/c2-count.py:22-28`);
the do-nothing control on the unfixed gate scored 21/37, and r34 was admitted (ledger, chousa r34). The remedy was
written down in chousa QUALITY 40 *before* it was built: "draws that content per seed… and a control that masks the
counter's literal fixture strings is scored before freezing; it must score below total"
(`chousa-shokunin/corpus/QUALITY.md:308-313`). QUALITY 41 adds the companion rule: repairs are built in a scratch
copy and installed after the wave settles; every receipt names the gate SHA-256 it measured.

**Closest because:** the falsifier is the same *kind* (a control that skips the claimed work meets the frozen
target), found in the same position (after the counter was frozen, by a wave seat, against a lane-owned counter),
and dispositioned with the same vocabulary the R34-C2 stop uses. It is also the cheapest precedent to copy,
because its remedy is one generation function, not a new instrument family.

## 3. Routing twin — kake r34 and kake r37

kake r34 is the nearest precedent for how the *stop record itself* should be written. Both declared targets were met
by controls that do no work (C1 lookup tool 28/28, C2 transcription 5/5). The closure refused admission while
keeping the work: "Not admitted: both declared targets reached by do-nothing controls; work itself judged real
(`unprovable-but-better`)" (MANIFEST rounds[485].notes), and its own re-measures showed the landed tool did
discriminate (28/28 real vs lookup 7/28, `rounds[485].verification.rechecks`) — the stop still held, because a
target a control can reach cannot verify the claim. The routing is the transferable part:

> "(1) declare a target a do-nothing control cannot reach, scoring retained controls before build"

It also kept the falsifiers as committed artifacts (`.ufo/waves/round-34/retained/`), wrote a QUALITY criterion with
a check, and documented the check's own limit: *"The check cannot tell a lookup control from an honest one: an
honest tool also reaches total and also gives exit 1"*
(`kake-shokunin/.ufo/waves/round-34/criteria/lookup_control_check.py:20-22`). kake r37 restates the same failure
from the other side: the shortcut control met the predicate and "the declared consequence (counter fixed before
any build) was not applied, so C1 is not admitted; no axis harmed" (MANIFEST rounds[508].notes).

## 4. Fleet statistics: a shortcut-falsified stop is effectively final

Across 95 honest stops in 18 lanes, exactly one round has a later `admitted` closure for the same lane+round:
souji r22 (`rounds[438]` → `rounds[639]`). That reversal is not a shortcut reversal — attempt 2 "does not re-claim
attempt 1's strict-adequacy claim and lands two new claims instead". No lane in the sample reversed a stop that
rested on a control meeting a frozen target. The observed dispositions are: carry the work as
`unprovable-but-better`, keep the instrument, write the criterion, and rebuild the measure in a later round.
The "parking" language appears once (chousa r33, "parking is orchestrator-owned") and did not park the lane:
chousa r34 was dispatched and admitted the next day. Recurrence is a routing signal, not an automatic penalty.

## 5. What this lane should copy

1. **Separate the claim from the work in the stop record.** chousa r33 and kake r34 both reject the claim *as
   declared* while keeping the artifact, the axis verdict at `unprovable-but-better`, and the score unchanged.
   kaidoku's stop record already does this ("owned scores stay 10->10"); it should also state, in one line, that
   the gate and its seven controls are retained and not relabelled — kake's version of that sentence is what keeps
   a later round from re-litigating the artifact.
2. **Name the blocker class and its recurrence for the orchestrator.** chousa's `:40-41` line is the pattern.
   kaidoku is now at its fourth straight honest stop (r32, r33 provider hold, r34-C1, r34-C2), and the third in the
   "counter cannot tell structure from shape" family (r32 text-presence, r34-C1 fixed-offset replay, r34-C2
   multiset replay). The lane's own r34 report already says "third straight rejection"; the stop record does not
   carry the count, and the closure needs it to route.
3. **Route the counter repair as a written criterion with an able-to-fail pointer, before building it.** chousa
   QUALITY 40/41 and kake's round-34/35 criteria are the form. kaidoku's QUALITY 67 ("the next counter must face a
   structure-blind replay control before it is frozen") is the right *shape* but, as written, it is satisfied by a
   roster of registered classes — which is exactly what wave 1 falsified.
4. **Make the falsifier a committed artifact under the lane, not a scratch path.** kake's round-34 criterion (a)
   rejects sandbox-only pointers outright, and its closure note records that the retained control bundles resolve
   only from the lane. kaidoku already commits `CtlMultiset-files/nameset.py` (sha256 `2e8feaea…a88b97`, verified
   below); the *fix* the wave produced is still scratch-only — see §6 item 5.
5. **Recover by regenerating content, not by adding a class.** chousa r34 (per-seed content) and mado r25 both
   rebuilt the surface instead of extending the roster. mado names the defect it was fixing: "v1–v3 took the
   expected table for each generated case from the counter's own line model, so a transcription of that model would
   meet them by construction"; v4's answer is that "Every expected table now comes from Hyprland itself"
   (`.ufo/reports/round-25/mado.md` §Work performed). Both lanes were admitted in the next round.

## 6. What this lane should avoid

1. **Do not register the multiset class as an eighth class and re-freeze R34-C2.** That is the roster race: chousa
   stopped twice on the same blocker class (r32 C2 metadata control, r33 C1 fixture-literal mask) while the remedy
   stayed a routing item, and kake r37 stopped because the declared consequence was not applied. A new class is
   always found next.
2. **Do not let a differential or auxiliary check rescue the claim.** chousa r33 closed that door explicitly ("the
   fuzz… cannot rescue the claim"). kaidoku's equivalent temptation is the `RevControls` / selftest / mutant
   evidence: it is attack evidence, not the frozen measure.
3. **Do not amend the counter after seats have scored it.** chousa QUALITY 41 exists because the gate was edited in
   place while wave-2 seats scored it, and its defect E4 because five receipts named gate bytes that were never
   committed; kake r34's criterion (a) closes the same hole for cited artifacts. Any successor instrument must
   name the gate SHA-256 in every receipt.
4. **Do not argue the stop is over-broad because the tool "really works".** kake r34's closure measured exactly
   that (28/28 vs 7/28) and still refused admission. That argument has no precedent in the sample.
5. **Do not cite the wave's fix from `/fast/scratch`.** The wave-1 seat wrote `mini-counter-fresh.py` to its scratch
   only ("Prototype in scratch…", `w1/ExecRedReproduce.md:§7`). Under kake r34 criterion (a) that pointer does not
   resolve from committed lane bytes, so a successor instrument that cites it must land it in-lane first.

## 7. Axes and the one proposed move

**Axes named (round axis in bold).** **depth** (whether the green surface forces record traversal); calibration
(whether a GREEN verdict means what it says); operability (the counter/gate instrument); and, as the router's
view, discernment (whether the stop and its remedy are written honestly). No score is proposed on any axis.

**Evidence that the round's own validated fix still leaks.** The wave-1 seat's fix — per-run unpublished content,
expected records computed from the generation — defeats content-keyed memorisation (nameset 0/8 on its sweep,
`w1/ExecRedReproduce.md:§7`). It does not close the layout channel. In `mini-counter-fresh.py` the name pool is
written **in record order** (`for name, _flags, _value in records: offsets[name] = len(pool); pool += …`,
`mini-counter-fresh.py:64-68`), so `name_off` is redundant: the i-th pool string is the i-th record's name. A reader
that reads only the header's `count`/offsets, pairs pool strings in file order with the record array's
`flags`/`value` fields, and **never dereferences `name_off`**, satisfies the fresh counter. Measured
(2026-10-25T07:35:52Z, seed `probe-a`, my scratch copy of the seat's counter, unchanged):

| counter | reader | matched | exit |
|---|---|---|---|
| `fresh-counter-copy.py` (seat's fix, byte-copy) | `structural.py` (positive control) | 8/8 | 0 |
| `fresh-counter-copy.py` | `zip_reader.py` (ordered-pool zip, no `name_off`) | **8/8, met_target true** | **0** |
| `fresh-counter-poolshuffle.py` (one-line variant: pool order drawn independently) | `structural.py` | 8/8 | 0 |
| `fresh-counter-poolshuffle.py` | `zip_reader.py` | **1/8, met_target false** | **1** |

The same zip reader scores 3/8 on the frozen counter (2026-10-25T07:36:03Z), because the frozen counter's pool
permutation happens to break the canonical layout — so this is *not* a new falsification of R34-C2. It falsifies
the proposed successor's claim that "only record-array traversal recovers the association". The 3/8 is itself
informative: the frozen set contains two single-record fixtures (`beta`, `epsilon`, record count 1 per R2) where any
association shortcut is trivially right, plus one four-record fixture (`zeta`) whose seeded shuffle for `probe-a`
was the identity (per-fixture rows, 07:39:04Z). A surface containing single-record fixtures cannot test the
association clause at all. The successor generator draws 2–6 records, so that particular hole is already closed
there; the layout channel is what remains.

**The move (one, bounded, routed to the next instrument — not applied here):** make the successor's surface
invariant-free instead of roster-complete. Generate the eight fixtures per run with (a) fresh names, flags and
values, (b) the name pool written in an order drawn **independently of record order**, (c) expected records computed
from the generation, and (d) a per-fixture assertion that the pool order is not the record order (a lucky identity
shuffle hands out a free pass: my probe's single match is `gen-6`, a two-record fixture where identity is a 1-in-2
event, 07:39:23Z). Target stays 8. With that surface no
reader that omits `name_off` can meet the target, whatever class anyone invents, so the green verdict stops
depending on an enumerated roster; the association clause of the predicate becomes true by construction rather than
by delegation.

This is a synthesis of moves already routed by three lanes: kake r34's "declare a target a do-nothing control
cannot reach" (target design, not roster), chousa QUALITY 40's per-seed adversarial content, and mado r25's
expectation-from-an-external-oracle principle. It is one generation-function change plus one assertion; measured
cost 0.127 s for eight fixtures (2026-10-25T07:37:26Z, exit 1 on the zip probe as expected).

**Second-order effects.**
- *Predicate/claim surface:* none on frozen bytes. c79bbe7b and its six clauses are untouched; the move requires a
  new predicate and a new freeze, which is what a successor claim needs anyway. The ten-point owned score is not
  touched.
- *Gate surface:* the `replay-gate.py` docstring enumerates invariant keys ("input size, input label, whole-file
  digest, fixed byte slices, the record order itself") — that enumeration stops being load-bearing. F3's route
  (assert class count == pinned count) remains necessary for gate *integrity* (an invisible class drop), but it is
  no longer the answer to "is the surface complete"; the two are complementary, not substitutes.
- *Verification surface:* the successor is falsifiable by construction with a reader of the zip class; the check is
  one command and one receipt, and it binds to committed gate bytes under chousa QUALITY 41.
- *Runtime/substrate:* no ELF carrier, no fixture execution, no new dependency; generation is in-memory.

**Risks.**
- A new predicate freeze is a new claim; it must not be folded into R34-C2's record as a repair (the frozen six
  clauses cannot absorb it, and doing so would repeat kake r37's defect — declared consequence not applied).
- Random generation can still emit a degenerate fixture (pool order == record order, duplicate name, saturated
  value); the per-fixture assertion in (d) is not optional.
- `canonical()` sorts rows before comparison, so the counter checks the *multiset* of name/flags/value triples; a
  reader that recovers names but mis-associates still fails, but a reader that sorts both sides could pass a fixture
  whose association is monotone in the sort key. The assertion in (d) should therefore also reject fixtures whose
  association is monotone w.r.t. sorted names [INFERENCE from reading `canonical()`; not probed].
- The move does not repair F1/F2/F4/F5; those stay as routed in the stop record.

## 8. What this seat ran (exact receipts) and what it did not

Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/ASiblingStop/` (`probe-fixtures.py`, `probe-assoc.py`, `zip_reader.py`,
`fresh-counter-copy.py`, `fresh-counter-poolshuffle.py`, `receipts-1.txt`, `receipts-2.txt`, `fleet-stops.txt`).

| # | UTC | command (abbreviated) | exit | observation |
|---|---|---|---|---|
| R1 | 07:32:53Z | `git -C <fleet> log -1 --format='%H %cI' --` five cited reports (chousa r32, chousa r33, kake r34, mado r24, mado r25) | 0 | chousa r33 `6467ba90cff0…` 2026-10-23T06:27:18-03:00, r32 `b6c90b57…`; kake r34 `6d7e9971…`; mado r24 `17cb0923…`, r25 `db62c5d7…` |
| R2 | 07:33:03Z | `python3 -I -B probe-fixtures.py` (static parse of the eight `.mrec`) | 0 | 8/8 distinct name multisets, no collisions, all 512 B, record counts 1–6 |
| R3 | 07:33:30Z | `grep`/`sed` over chousa r33 counter (`CONFUSERS`), chousa r34 counter (`generated per seed`), spotcheck `:30,:72`, mini-counter docstring | 0 | receipts in `receipts-1.txt` |
| R4 | 07:34:22Z | `python3 -I -B probe-assoc.py` (re-implemented `permute`, five seeds) | 0 | all eight: `triples_invariant_under_permutation=True` |
| R5 | 07:34:55Z | `sha256sum .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py`; `git log -1 -- claim-stop.json` | 0 | `2e8feaea92ee…a88b97` matches the stop record; stop commit `cd75b92e5837…` 2026-10-25T04:23:47-03:00 |
| R6 | 07:35:52Z | four counter runs on the seat's fresh counter and its one-line pool-shuffle variant, seed `probe-a` | 0/0/0/1 | table in §7 |
| R7 | 07:36:03Z | three counter runs on the frozen `mini-counter.py`, seed `probe-a` | 1/0/0 | zip 3/8, nameset 8/8, structural 8/8 |
| R8 | 07:37:06Z | `python3` over `MANIFEST.json` (stop count, lanes, reversal candidates) | 0 | 95 stops / 18 lanes / 1 reversal candidate (souji r22, new claims) |
| R9 | 07:37:26Z | `bash -c 'time python3 … fresh-counter-poolshuffle.py … zip_reader.py'` | 1 | wall 0.127 s; exit 1 is the counter's `met_target=false`, expected. A prior `/usr/bin/time` attempt returned 127 (binary absent) at 07:37:23Z; timing was therefore taken with the shell builtin |

**Not run / not verified.** The successor surface (pool-order decoupling inside a *frozen* instrument) does not
exist and was not built in-lane; the zip reader was not scored under `replay-gate.py` with a registered-class config;
F3's class-count assertion and F4's red-last selftest mutant were not exercised; no ELF carrier, fixture or reader
was executed as a program; the R34-C1 production reader was not run. No tool installed or upgraded (no `pacman`,
`uv`, `npx`, `cargo`; host pacman pause respected). No VCS mutation, no other lane written, no `agent://all`.

**Limits.** Sibling evidence is prose, JSON and Python read from working trees and committed reports; no language
server was available, so all claims are text-literal. Git history was not exhaustively searched; the 95-stop count
is the ledger's own accounting, read at 07:37Z, not an independent recount. The zip-reader finding is a probe on a
*scratch* copy of the wave's candidate fix, not on any frozen instrument.

## Verdict

`SIBLING_PRECEDENT: chousa r33 (closest, with r32 as the class's first instance) — closure accepted the report, the retained instrument and an unprovable-but-better axis verdict, rejected admission and any score, routed a written per-seed-content criterion (QUALITY 40) and recorded the blocker class for the orchestrator; the lane rebuilt the counter with per-seed content and was admitted next round. Routing twin: kake r34, whose routed item (1) "declare a target a do-nothing control cannot reach" is the exact repair R34-C2 needs and whose criteria/retention practice this lane should copy. Across 95 honest stops in 18 lanes no shortcut-falsified stop was reversed. Copy: claim/work separation, blocker-class recurrence line, criterion-before-build, committed falsifier, content regeneration over roster growth. Avoid: re-freezing with one more registered class, auxiliary-check rescue, post-scoring amendment, "the tool really works" argument, and citing the fix from /fast/scratch. One routed move: per-run generation with pool order drawn independently of record order plus a non-identity assertion (measured: ordered-zip 8/8 on the wave's candidate fix, 1/8 after the one-line decoupling, structural 8/8 both) — no frozen byte touched, no score proposed.`
