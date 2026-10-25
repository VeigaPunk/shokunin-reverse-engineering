# AQuality67Route — did round 34 execute QUALITY 67's route?

Seat: `L1Kaidoku34-2.AQuality67Route` (leaf), wave 2, run-6 re-dispatch.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: whether this round actually executed QUALITY 67's route — read the criterion, the
previous attempt in `.ufo/waves/round-34`, and this round's artifacts; name the exact step the
route forces and whether the round took it. I did not reopen the claim, repair a frozen
instrument, or award any score; no frozen instrument, `claims.json`, `claim-stop.json`, doc or
corpus byte was written. Probes ran on a byte-copy in
`/fast/scratch/hyaku/kaidoku-r34b/w2/AQuality67Route/`; the copy's pinned bytes match the frozen
pins (sha256 of `replay-gate.py`, `c2-shortcut-gate-counter.py`, `gate-config-mini.json`,
`mini-counter.py`, `size_keyed.py` = the 26-pin map, re-checked 2026-10-25T07:36:19Z, exit 0).
No ELF carrier or fixture was executed as a program; readers ran only as python children of the
pinned counters. Tooling: none installed; `/usr/bin/python3` 3.14.8, `git` 2.56.0.

---

## 1. The criterion

`corpus/QUALITY.md:77` (row 67), landed in commit `abbd76042fd23b1ba049350fc37a360f793892b7`
(2026-10-23T11:07:18Z):

> Before freezing a finite ELF structural-decoding counter, exercise a structure-blind replay
> keyed on invariant fixture identity (for example, size) that memorizes topology/scalars and
> reads only fixed name slices. Randomized names or opaque paths alone do not force record
> traversal. Retain the replay source and exact score under the prospective predicate; if it
> meets a frozen target, stop without amending, re-scaling or relabelling the claim.

Presence check (exact argv, per revision):

| command | revision | result | exit | UTC |
|---|---|---|---|---|
| `git show <rev>:corpus/QUALITY.md \| grep -c 'structure-blind replay keyed on invariant'` | `54a87a51a865ab931fd355e767303337b05cccf4` (R34-C1 freeze) | `0` | 1 | 07:35:14Z |
| same | `ec3125ad3d130d92f888a4128dfaa2982f36fff7` (r34b base) | `0` | 1 | 07:35:14Z |
| same | `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (R34-C2 freeze) | `1` | 0 | 07:35:14Z |

### 1.1 Q1 — Did QUALITY 67 ask for the replay BEFORE the freeze?

**Yes, explicitly and only that way.** The operative clause is "Before freezing … exercise …".
The criterion is a *pre-freeze refusal* obligation; its terminal clause ("if it meets a frozen
target, stop without amending…") is the fallback the route prescribes when prevention was not
possible.

Two qualifications matter and are visible in the same check:

1. The criterion is **retroactive to the previous attempt**. It did not exist at R34-C1's freeze
   (`54a87a51`, 2026-10-23T10:47:21Z; grep = 0). It was authored 20 minutes later, in the R34-C1
   *stop* commit, from that attempt's own post-freeze discovery. So Q1 is "yes for r34b, and the
   criterion could not have governed the attempt it was derived from."
2. The round knew it was in force. `tools/round-34/replay-gate.py:4-8` (frozen at `c79bbe7b`)
   prints the obligation verbatim: *"Obligation (QUALITY 67): before a finite ELF
   structural-decoding counter is frozen, exercise readers that memorize the fixture set by an
   invariant key -- input size, input label, whole-file digest, fixed byte slices, the record
   order itself -- under the counter's own predicate."* The round therefore did not claim the
   route was inapplicable; it claimed to implement it.

## 2. The previous attempt (R34-C1) — why the route exists

| UTC | commit / artifact | fact |
|---|---|---|
| 2026-10-23T10:46:14Z | `8897a67f` | C1 instruments committed (reader, counter, freeze-integrity) |
| 2026-10-23T10:47:21Z | `54a87a51` | C1 freeze: `claims.json` + two `claim-freezes` tsv rows only — **no shortcut replay, no receipt** |
| 2026-10-23T11:00:35.635552Z | `.ufo/waves/round-34/w1/CtlLabels-files/size-pristine.receipt.json` | decisive size-keyed fixed-slice replay **after** the freeze: 12/12 both schedules, `exit 0`, `documents_ok=true`, no ELF structure decoding |
| 2026-10-23T11:07:18Z | `abbd7604` | C1 stopped; same commit adds QUALITY 67 (`corpus/QUALITY.md` diff `+1` row 67) and the replay sources |

Evidence: `git show --stat 54a87a51…` shows only `.ufo/waves/round-34/claims.json`,
`corpus/claim-freezes-v2.tsv`, `corpus/claim-freezes.tsv`; `git show --stat abbd7604…` shows the
whole `CtlLabels-files/` tree; `CtlLabels.md:1-5` and the receipt's `observed_utc`
`2026-10-23T11:00:35.635552+00:00`, `exit 0` support the 12/12 claim.
So the previous attempt is exactly the shape QUALITY 67 forbids: **freeze first, discover the
replay afterwards**. The criterion was the durable fix for that ordering.

## 3. This round (R34-C2) — freeze vs. replay, exact chronology

All commits below; UTC derived from `git log --date=iso-strict` (`-03:00` offset, converted).

| UTC | commit / artifact | fact |
|---|---|---|
| 2026-10-25T07:11:52Z | `claims.json:declared_at_utc` | target/prospective predicate declared (target 8, six clauses) |
| 2026-10-25T07:13:11Z | `c79bbe7b` | **freeze**: instruments, 8 fixtures, **7 registered shortcut classes**, red+green configs; first r34b commit (`git log -- .ufo/waves/round-34/r34b` has no earlier commit) |
| same minute | `.ufo/waves/round-34/r34b/after/c2-at-instruments.json` | six-clause verdict; `measured_revision: c79bbe7b…` — a hash that exists only *after* the freeze commit, so **the only retained score postdates the freeze** |
| 07:15Z | `w1-payload.json`, `w1-spec.json` (mtime) | wave 1 starts — there is **no pre-freeze seat**: no `prep/` phase, first r34b artifact is the freeze |
| 07:18:33Z–07:20:05Z | `.ufo/waves/round-34/r34b/w1/ExecRedReproduce.md` | wave-1 seat: path/digest keys defeated by the permutation; **content-multiset reader 8/8** (07:19:02Z), seeds alt-1/alt-2/alt-3 (07:19:56Z), invariance probe 07:20:05Z |
| 07:22:31Z | `b917ea64` | receipts/`instruments.json` landed (untracked before this) |
| 07:22:55Z (mtime) | `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` | decisive replay source copied into the lane, **after** the freeze |
| 07:23:47Z | `cd75b92e` | stop record landed |
| 07:28:00Z ("approximate") | `claim-stop.json:l1_rerun_utc` | cited L1 rerun **after** the stop commit; cannot be the evidence that justified it (producer receipts are 07:19Z) |
| 07:32:25Z | `66b84027` | docs landing: lesson M34-5..M34-12, QUALITY 68-73 |

### 3.1 Q2 — Was this round's replay registered before the freeze or after?

Split by class, because the two answers differ:

- **Registered set: at the freeze, never exercised before it.** The seven classes
  (`all-false`, `size-keyed`, `fixed-slice`, `digest-keyed`, `string-scan`,
  `record-order-replay`, `label-memorization`) are pinned in `c79bbe7b` and named in
  `gate-config-mini.json`. No pre-freeze scoring receipt exists anywhere: `c79bbe7b`'s stat has
  no `.ufo` receipts, and the only retained score (`after/c2-at-instruments.json`) names the
  frozen revision `c79bbe7b` and was untracked until `b917ea64` (07:22:31Z). The claim's own
  predicate ordering ("frozen only after registered … readers are scored") is therefore
  **unevidenced by retained bytes**; the one retained measurement necessarily postdates the
  freeze.
- **Decisive replay: after the freeze.** `nameset.py` (sha256
  `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97`, matching
  `claim-stop.json:decisive_counterexample.source_sha256`) was authored by a wave-1 seat at
  07:19Z and landed in the lane at 07:22:55Z. It is registered in **no** config — the stop says
  so itself ("satisfied only because this class is unregistered").

So: **registered at the freeze; scored only afterwards; the class that decides the round was
authored and registered nowhere, ten minutes after the freeze.**

## 4. The exact step the route was supposed to force — and whether the round took it

### 4.1 The step, decomposed

QUALITY 67 forces a four-part pre-freeze sequence on the *author* of the counter, before the
freeze commit:

1. Determine what the counter's own transformation `T` actually varies (here
   `tools/round-34/mini-fix/mini-counter.py:permute`: reorder the name pool, rewrite
   `name_off`; size, record order, `flags`, `value` and the name set unchanged).
2. Enumerate the public invariants `g` with `g(T(x)) = g(x)` — i.e. the key space that survives.
3. Build a structure-blind memoriser `S(x) = TABLE[g(x)]` for **each such** invariant and score
   it under the prospective predicate (the green config, target 8).
4. If any meets the target, **refuse the freeze**; do not freeze, register, amend, rescale or
   relabel.

Step 1-3 is what "keyed on invariant fixture identity" means; the size example in the criterion
is the R34-C1 instance, not the whole class space. Step 4 is the terminal clause.

### 4.2 What the round actually did

- It froze a counter whose docstring advertises the covered keys as *"input size, input label,
  whole-file digest, fixed byte slices, the record order itself"* — i.e. it enumerated the key
  space **without the content invariants**, in the frozen bytes, before the freeze. The
  content-multiset key is absent from the freeze tree (`git grep -n -i 'soname\|multiset\|sorted
  set\|name set' c79bbe7b -- tools/round-34` → no output, exit 1).
- Its `size-keyed` class (`tools/round-34/mini-fix/readers/size_keyed.py`) is a one-entry
  template `512 -> [alpha's three records]`. The fixture builder deliberately makes every
  fixture exactly 512 bytes (`build.py` docstring: *"Every fixture is exactly SIZE bytes so
  input size cannot identify a fixture"*; `stat` confirms 8/8 at 512 bytes). This control is
  therefore **structurally incapable of discriminating** and cannot be "exercised" in the
  criterion's sense; it scores 1/8 by construction. A reader that cannot test the class is not
  evidence that the class fails.
- The counter's transformation is exactly the pair the criterion names as insufficient:
  pool reorder (= randomized names, weaker than C1's same-length renaming) plus opaque paths.
  The criterion's sentence *"Randomized names or opaque paths alone do not force record
  traversal"* describes this round's green surface precisely.
- The only independent exercise of the surviving invariant happened in wave 1, **after** the
  freeze, and the round then executed the criterion's terminal clause (stop without amendment).

So the round took the **terminal** step of the route (stop, no amendment, no score) and skipped
its **preventive** steps (pre-freeze invariant closure → score → refusal). The route was executed
backwards: post-mortem instead of gate.

### 4.3 What the skipped step would have produced (measured, scratch copy)

| probe (cwd = `/fast/scratch/hyaku/kaidoku-r34b/w2/AQuality67Route/lane`, frozen bytes) | argv | observed | exit | UTC |
|---|---|---|---|---|
| P1 registered set | `python3 -I -B tools/round-34/replay-gate.py --root . --config tools/round-34/gate-config-mini.json --json-out …/green-rows.json` | `REPLAY_GATE_CLEAN … shortcuts_below_target=7`; rows: `structural 8/True`, `size-keyed 1/False`, all others 0/False | 0 | 07:34:12Z |
| P2 surviving-invariant replay | `python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader …/nameset.py` (seeds default, `alt-1`, `alt-2`) | `matched 8`, `met_target true` on all three seeds | 0 / 0 / 0 | 07:34:12Z |
| **P3 the route's refusal** | same gate, config copy `gate-config-multiset.json` = frozen green config **plus** `{class: content-multiset, path: nameset.py}` | `REPLAY_GATE_REFUSED finding=shortcut_meets_target … shortcuts_over_target=content-multiset` | **2** | 07:34:19Z |

P3 is the decisive counterfactual: **had the class been exercised before the freeze under the
gate's own predicate, the gate would have refused the freeze** (exit 2, REFUSED). The route's
step was available, cheap, and decisive; it was simply not run. Note P3 changes no frozen byte —
it is a scratch config; the frozen configs still produce CLEAN.

## 5. Attack on the stop's evidence

What survives:

- The decisive class is real and reproducible: P2 gives 8/8 at three seeds on the frozen
  counter, exit 0, and the source hash matches the stop's binding (`2e8feaea…`).
- The seven registered classes really do stay below target (P1), so the six frozen clauses and
  the claim's own registered-set predicate are genuinely true at `c79bbe7b`. The stop does not
  misreport its counter.
- VERDICT "falsified measure; honest stop after wave-1, before any capability or score credit"
  is correct as credit accounting: no capability row, no score movement.

What does not survive, in route terms:

1. **The stop is not a pre-freeze gate result; it is a post-freeze falsification.** Both the
   decisive source (07:22:55Z) and the only six-clause receipt (`measured_revision: c79bbe7b…`)
   postdate the freeze (07:13:11Z). The record presents the falsification as a clean kill under
   "Frozen before data" — true for the *target* (declared 07:11:52Z), false for the *route*
   (data preceded the freeze). The record never states that QUALITY 67's pre-freeze exercise was
   skipped; it only says the winning class is unregistered.
2. **The stop's cited L1 rerun postdates the stop commit.** `l1_rerun_utc`
   `2026-10-25T07:28:00Z (approximate)` is 4m13s *after* `cd75b92e` (07:23:47Z); the producer's
   receipts are 07:19Z. A rerun that cannot have informed the stop is recorded as if it did.
   Record-order defect (report-only; it does not change the verdict because the producer
   receipts predate the stop).
3. **The stop's own repair list omits the root cause.** F1-F5 are container/identity/class-drop/
   mutant/receipt-binding defects. None of them says "the pre-freeze replay the criterion
   demanded was never exercised". The root cause is in the later-landed lesson M34-7
   (`corpus/lessons/round-34.md`, 07:32:25Z) and QUALITY 69, not in `claim-stop.json`. A future
   round reading only the stop record would not learn the timing failure.
4. **The round's adversarial transform is weaker than the one that produced the criterion.**
   C1 randomized same-length name strings and the size replay still won 12/12; r34b merely
   reorders the name pool, so the name multiset survives trivially. The round called its surface
   "identity-defeating" while weakening the transform relative to the attempt the criterion was
   written from. The frozen `mini-counter.PREDICATE` sentence ("only record-array traversal
   associates a name with its record") is false under that transform; the association can come
   from a table keyed on the name set.

## 6. The five disclosed defects and the proposed repair, as they bear on the route

| id | stop record claim | independent check | load-bearing for the route? |
|---|---|---|---|
| F1 | pins nested under `claims[0].pins`; freeze-integrity wants top-level `instruments`; `instruments.json` is a byte-identical 26-pin container | `claims[0].pins` has 26 entries, `instruments.json` has 26, **maps equal**, 0 digest mismatches, exit 0, 07:34:18Z; `freeze-integrity.py` requires top-level map (source) | No. Container hygiene; repaired post-data and disclosed |
| F2 | predicate identity false: sentence A (claims/configs, sha `7c6c17f0…`, 31 words) vs B (counter/receipts, sha `8340aea5…`, 46 words) | read both; `predicate-reconciliation.json` matches; third sentence in `mini-counter.PREDICATE` (sha `09988625…`) | No. Identity, not execution |
| F3 | dropping registered classes down to `MIN_SHORTCUTS` still returns CLEAN | `replay-gate.py:31` `MIN_SHORTCUTS = 3`, no equality assertion; **P4** trimmed green config to 3 classes → `REPLAY_GATE_CLEAN … shortcuts_below_target=3`, exit 0, 07:34:49Z | Proposed repair ("assert class count == pinned count before CLEAN") is **not** load-bearing for this round: the winning class was never in the pinned set, so an equality check against 7 would still pass |
| F4 | gate mutant M3 (ignore last shortcut row) survives its selftest and flips the red case CLEAN | inspection: `SELFTEST_CASES` never place the over-target reader in the last slot (`red-one` s1=4, `red-two` s1,s2=4, `s3` always 0); mutant anchor `if over:` is exercised only by those cases | Proposed repair (red-last case) hardens mutant scoring; no effect on the class space |
| F5 | receipts untracked at first audit | `b917ea64` (07:22:31Z) lands them; `c79bbe7b` stat carries none | Partly: it is the same ordering weakness that makes "scored before freeze" unevidenced |

The stop record's proposed repairs (F3 count equality, F4 red-last case) are **orthogonal to the
route failure**. They protect the *registered* set — the very quantifier that let the round print
CLEAN. The load-bearing successor is the later-landed **QUALITY 69**
(`corpus/QUALITY.md:79`): one class per keyable invariant (size, label, digest, fixed slice,
record order, payload, value multiset, name multiset, transform/seed reuse) and a green surface
that varies size, order, payload and name vocabulary together. That is the correct repair for the
step that was skipped, and it is **not** in `claim-stop.json`.

Residual risk after QUALITY 69 (inference, forward-looking): the gate still cannot verify
class-space completeness — it only reads the config it is given. Closure depends on the author
enumerating the invariants of `T` correctly; no criterion yet requires an independent,
registration-blind pre-freeze attempt, which is the mechanism that actually found this class.

## 7. Confidence

- **High** (direct bytes, git objects, re-run probes): the criterion demands pre-freeze exercise;
  it was absent at the C1 freeze and present at the C2 freeze; the seven registered classes are
  pinned in the freeze commit; the content-multiset class was authored after the freeze; the
  registered set is CLEAN while the unregistered class is 8/8; registering it flips the gate to
  REFUSED (exit 2); the six-clause receipt names the frozen revision and postdates the freeze.
- **Medium-high**: the L1 did not retain any pre-freeze score (a pre-commit run may have
  happened but is not retained; criterion 67 requires retention, so the ordering is unevidenced).
- **Inference, marked**: the L1 did not know/execute the content-multiset class pre-freeze. No
  artifact of the freeze tree mentions it; the frozen docstring's key list omits it; the fixture
  builder removes size as a discriminator. Absence of evidence in the retained tree is not proof
  of non-execution; the ordering argument above does not depend on it.

## 8. Verdict

**The round did not execute QUALITY 67's route.** The criterion asked for the structure-blind
replay *before* the freeze, keyed on an invariant the counter's own transform leaves intact. The
round registered seven classes at the freeze (none exercising the content invariant, and its
`size-keyed` control degenerate by fixture design), retained no pre-freeze score, froze at
`c79bbe7b` (07:13:11Z), and only then — in wave 1, at 07:19-07:22:55Z — exercised the
content-multiset replay that scores 8/8, and stopped at 07:23:47Z. The skipped step was decisive
and cheap: registering that class in a scratch copy of the frozen gate returns
`REPLAY_GATE_REFUSED` exit 2 (07:34:19Z, P3). The stop is an honest *post-freeze* falsification
under the criterion's terminal clause, not a pre-freeze refusal under its operative clause; it
contains no record of the timing failure, and its own proposed repairs (F3/F4) do not address it
(QUALITY 69, landed later, does). No claim reopening, instrument repair or score is made here.

**FINAL VERDICT: QUALITY 67 WAS IN FORCE AND WAS NOT EXECUTED — THE REPLAY WAS REGISTERED AND
SCORED AFTER THE FREEZE (DECISIVE CLASS AUTHORED 07:19Z-07:22:55Z; FREEZE 07:13:11Z; STOP
07:23:47Z), AND THE ROUTE'S REFUSAL STEP WOULD HAVE RETURNED REPLAY_GATE_REFUSED EXIT 2.
CONFIDENCE: HIGH ON ORDERING AND ON THE COUNTERFACTUAL REFUSAL; MEDIUM-HIGH ON
NON-EXECUTION (NO PRE-FREEZE SCORE RETAINED).**
