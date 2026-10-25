# AStopNarrative — R34-C2 stop causality: registration (config) vs fixture design

Seat: `L1Kaidoku34-2.AStopNarrative` (critic, wave 2). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Frozen claim revision: `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (commit time 2026-10-25T04:13:11-03:00).
Stop record: `.ufo/waves/round-34/r34b/claim-stop.json` (commit `cd75b92e583735729546b0ea3b250f2df6d0652a`, 04:23:47-03:00).
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/AStopNarrative/`. Lane VCS read-only; no lane file written except this report.
Tooling: **nothing installed or upgraded**; `pacman` untouched (transactions paused host-wide); `python3` 3.14.8 preexisting; no network.

Assignment: attack the **causality** of the stop — incomplete registration set (configuration error) or
fixture-design error (the permutation preserves a keyable invariant)? No claim reopened, no frozen instrument
repaired, no score awarded.

---

## 0. What I verified before reasoning (pins, equivalence, read-only)

| check | argv (exact) | exit | UTC | result |
|---|---|---|---|---|
| 26 pinned digests match bytes | `python3 - <<…` hashing every `claims.json:claims[0].pins` entry and comparing to `.ufo/waves/round-34/r34b/instruments.json` | 0 | 07:40:06Z | 26/26 match; `instruments` map == `pins` map |
| frozen bytes == working tree | `git show c79bbe7b…:<path> \| sha256sum` for `mini-counter.py`, `build.py`, `expected.json`, both configs, `replay-gate.py`, `c2-shortcut-gate-counter.py`, `freeze-integrity.py` | 0 | 07:40:06Z | 8/8 **SAME** — running against the working tree measures the frozen revision for these instruments |
| frozen claim counter still OK | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out /fast/scratch/hyaku/kaidoku-r34b/w2/AStopNarrative/out/e13-c2-frozen.json` (cwd lane) | 0 | 07:39:26Z | `GATE_COUNTER_OK … green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` |
| stop counterexample source matches its stated sha | `sha256sum .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` | 0 | 07:42:00Z | `2e8feaea…a88b97` == `claim-stop.json:source_sha256` (also `pathkey.py 28acfe5a…`, `mini-counter-fresh.py 5181330d…`) |

The stop's premise — six frozen clauses hold, and the counterexample is reproducible from committed bytes —
is **correct**. Everything below attacks what the stop says *caused* that.

---

## 1. Three different sentences can be "falsified"; the stop does not say which

This is the hinge of the whole causality question. The committed bytes contain three distinct claims:

| label | site | quantifier | content |
|---|---|---|---|
| **A** | `claims.json:51` (`claims[0].predicate`), `gate-config-mini.json:3`, `gate-config-naive.json:3` | "**registered** structure-blind shortcut readers" | the freeze predicate |
| **B** | `tools/round-34/c2-shortcut-gate-counter.py:23-27` + receipts | "**registered** shortcut class stays below target" | a longer paraphrase (F2, already disclosed) |
| **C** | `tools/round-34/mini-fix/mini-counter.py:23` | **no registration qualifier** | "…only record-array traversal associates a name with its record" |
| **O** | `tools/round-34/replay-gate.py:4-9` (docstring obligation) | "**If any shortcut** meets the frozen target, the counter measures shape, not structure, and the freeze is refused" | the instrument's stated obligation |

Measured consequence:

- **A and B are not falsified.** E13 above: all six clauses true at the frozen revision, `clauses_failed=-`.
  Under `claims.json:22` (`kill_rule`: "if any of the six clauses … is false … the claim is a miss") R34-C2 is a
  **hit**, not a miss.
- **C and O are falsified** by `nameset.py` at 8/8 (E1). C is the sentence the stop's counterexample actually
  breaks; O is the sentence that licenses refusing the freeze.

The stop's prose blurs this. `why_this_falsifies_the_surface` says: "…so the green surface does not force
structural traversal **and the gate's green clause is satisfied only because this class is unregistered**".
The first clause is a design statement (C/O). The second is a registration statement (A/B). The record never
says which one the verdict rests on, and `kill_rule_applied` leans on the registration one ("an unregistered
structure-blind class reaches it, so the capability's central demonstration … is falsified"). §5 shows the
registration reading carries no repair.

---

## 2. Reading A — "incomplete registration set (configuration error)"

### Steelman

- `gate-config-mini.json` registers exactly seven classes (`all-false`, `size-keyed`, `fixed-slice`,
  `digest-keyed`, `string-scan`, `record-order-replay`, `label-memorization`); `content-multiset` is absent.
- The gate is a finite enumeration: `replay-gate.py:58-66` only enforces `len(shortcuts) >= MIN_SHORTCUTS` (3)
  and class uniqueness; `:112-118` scores only listed rows; `:123` collects only those rows into
  `classes_over_target`. **The registry is the sole authority.**
- The drop is invisible (stop F3, independently verified): a 3-class config returns
  `REPLAY_GATE_CLEAN … shortcuts_below_target=3`, exit 0 (07:37:58Z). Nothing asserts registered == pinned.
- The gate's own docstring *enumerates five keys* ("input size, input label, whole-file digest, fixed byte
  slices, the record order itself", `replay-gate.py:5-7`) — and content-multiset is not one of them. So both
  the config and the obligation's illustrative list omit the class that won.
- Wave-1 evidence already shows this is not one class but a family: `MutShortcutClasses.md` §3.2 measures
  **five** independent 8/8 classes (`s2b_string_name_keyed`, `s2c_string_pool_noheader`, `s2b_record_sig`,
  `s2b_digest_replay`, `s2b_label_hash_replay`), plus `CritCounterLimits.md` §1 (`prefix-keyed`, 8/8) and
  `LabratSeedSensitivity.md` §8 (payload-keyed, 8/8). Three seats, at least seven unregistered 8/8 specimens.

Steelman conclusion: the CLEAN was an artefact of a list the claimant chose; the gate cannot see what it was
not told to look at.

### Why this reading cannot be the cause of the stop

**(a) Registration does not affect the score.** `nameset.py` reaches 8/8 on the counter; the registry is not
an input to `mini-counter.py:score()`. The capability demonstration "the fixture set forces record traversal"
is falsified at fixture level, before any registry exists.

**(b) The registration repair destroys the claim instead of restoring it.** Two measurements:

- Gate with the frozen config plus the class registered (8 shortcuts, class `content-multiset`, absolute
  reader path):
  `python3 -I -B tools/round-34/replay-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --config /fast/scratch/hyaku/kaidoku-r34b/w2/AStopNarrative/probe/gate-config-nameset.json`
  → `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=content-multiset`,
  **exit 2**, 07:33:08Z. (Frozen config control, same argv with `tools/round-34/gate-config-mini.json`:
  `REPLAY_GATE_CLEAN`, exit 0, 07:33:09Z.)
- The claim's own counter against a scratch root holding byte-identical copies of the frozen instruments,
  with that class registered — exact argv `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b… --json-out …/e6-c2-nameset.json`,
  cwd `/fast/scratch/hyaku/kaidoku-r34b/w2/AStopNarrative/root2`
  → `GATE_COUNTER_MISS finding=shortcut_gate_miss … green=REPLAY_GATE_REFUSED green_positive_matched=8 clauses_failed=green_clean`,
  **exit 1**, 07:33:51Z; `clauses = {green_clean: False, others True}`.

So "register the missing class" converts a false CLEAN into a **claim miss** (`green_clean` false). There is
no configuration under which the frozen claim is both complete (in the sense the obligation asks) and CLEAN.
The registry is a *detection* authority, not a *capability* authority.

---

## 3. Reading B — "fixture-design error: the permutation preserves a keyable invariant"

### The invariant surface, measured (E5)

`python3 -I -B /fast/scratch/hyaku/kaidoku-r34b/w2/AStopNarrative/probe/invariant-surface.py`
→ exit 0, 07:33:45Z. Per fixture (all eight identical in shape):

| property under the counter's only transformation (`mini-counter.py:57-83`) | result |
|---|---|
| header bytes identical | true 8/8 |
| total size identical | true 8/8 |
| SHA-256 differs (so digest-keyed fails) | true 8/8 (digest differs) |
| `name_off` slots rewritten | = record count (1,2,3,4,5,6 …) |
| `(flags, value)` pairs, same order | **true 8/8** |
| name multiset | **true 8/8** |
| **decoded answer (sorted records) invariant** | **true 8/8** |
| pairwise name-set overlaps over 28 pairs | **none**; 8 distinct name sets |

The counter's own docstring states the result in prose: `mini-counter.py:58` —
"Reorder the name pool; rewrite name_off per record. **Decoded output unchanged.**"

And the oracle answer is a *pinned public constant*: `tools/round-34/mini-fix/expected.json`, which is in
`claims.json:claims[0].pins`. So the green surface compares the reader's output to a published constant while
its only transformation is, by construction, an endomorphism of that constant. Any program that can recognise
the instance and recall the constant wins; recognition needs only *one* invariant of the transformation, and
the name multiset is one (the reader's own docstring says so: `nameset.py:13-14`). The all-false/size/keyed
classes fail only because they chose *bad* invariants (size is constant, digest changes); the surface never
asked them to be good.

Two further design channels, measured:

- **Payload signature is a second perfect instance key.** `(count, ordered (flags,value) pairs)` is distinct
  for all 8 fixtures (`distinct_signatures 8 of 8`, 07:40:06Z) — so a reader that never uses names can identify
  the fixture and replay. (`MutShortcutClasses.md` §3.2 measures `s2b_record_sig` at 8/8 on exactly this.)
- **Homogeneous payloads make association unobservable.** `gamma.mrec` has `(0,2912)` twice, `theta.mrec` has
  `(0,2819)` five times, `zeta.mrec` has `(0,2912)` three times (07:40:06Z). Because `canonical()`
  (`mini-counter.py:85-97`) compares a **sorted multiset**, any name↔payload permutation inside a group of
  equal payloads is accepted. Demonstrated: the ordinal reader (§6) scores **5/8 on the frozen surface even
  though it misassociates**, and `theta` passes purely because five of its six payloads are indistinguishable.

### Isolating the cause (E3)

Same harness, same registry, same fixtures; only the transformation's *effect on the answer* changes
(`probe/probe-counter.py`, `--transform`):

| transform | nameset (content-multiset) | structural (positive control) |
|---|---|---|
| `permute` (verbatim copy of `mini-counter.permute`) | **8/8**, exit 0 | 8/8, exit 0 |
| `permute-reord` (+ shuffle record array) | **8/8**, exit 0 | 8/8, exit 0 |
| `revalue` (permute + fresh per-record flags/value; expected read off the instance) | **0/8**, exit 1 | **8/8**, exit 0 |

UTC 07:33:07–07:33:08Z. Because `revalue` changes only whether the answer is a function of the instance,
and that single change kills the shortcut while the positive control survives, the cause of the shortcut's
success is the **answer-preserving transformation**, not the registry. Shuffling the record array
(`permute-reord`) does not help, because the comparison is order-insensitive.

---

## 4. Adjudication

**The stop is caused by the fixture-design error; the incomplete registration set is the reason the
instrument reported CLEAN, i.e. the cause of a false positive, not of the falsification.**

- Cause of the *falsification of C/O*: the transformation is an identity on the answer and the answer is a
  pinned constant (§3, E5/E3). No registration set changes that.
- Cause of the *false GREEN*: the registry (`gate-config-mini.json`) did not list the winning class, and the
  gate has no completeness obligation of its own (`replay-gate.py:58,112,123`; F3 reproduced).
- The two are not interchangeable: repairing the registry produces a MISS (E6), repairing the surface
  produces a CLEAN with a *larger* registry (§6, E12).

**Verdict on the stop: the verdict "falsified measure; honest stop" is correct.** What is imprecise is the
record's causal sentence. `kill_rule_applied`'s "an unregistered structure-blind class reaches it, so the
capability … is falsified" reads as if registration were load-bearing. The defensible formulation is:

> the green surface does not force record traversal, and the gate's CLEAN could not see it because the class
> was unregistered; registering the class does not restore the capability — it makes the claim a miss — so the
> fixture (not the registry) is the defective part.

This also explains why the stop is a *purpose-level* refusal rather than a kill-rule miss: the six clauses (A/B)
hold (E13). The refusal rests on O (`replay-gate.py:4-9`) and C (`mini-counter.py:23`), both committed before
data and both registration-free. That is legitimate, but it should be *stated* as such, and the falsified
sentence should be named (C/O), not left as the registration-relative A.

---

## 5. Which reading an outside reader adopts from the committed bytes alone

**The design reading.** The committed bytes carry the proof without any receipt:

1. `mini-counter.py:58` says "Decoded output unchanged" — the counter documents its own answer-invariance.
2. `expected.json` is a pinned public constant (`claims.json:23-50`), so recall is available to anyone.
3. `mini-counter.py:23` (C) is registration-free and false under `nameset.py`.
4. `claims.json:51` (A) is registration-qualified and **true** (E13). A reader who adopted the config reading
   would therefore have to call R34-C2 a **hit** and the stop an extra-claim refusal — not a miss; the record
   itself does neither, and its reproduction of the 8/8 shortcut is data about the *fixture*, not the registry.
5. The config repair is self-defeating from the bytes alone: adding the class to `gate-config-mini.json`
   makes `green_clean` false (E6 reproduces it). A configuration "error" whose repair destroys the claim is
   not a configuration error.
6. The producing seat's own committed report (`ExecRedReproduce.md`) says in §9 "strictly a
   registration-completeness/rationale gap … does not falsify any of the six frozen clauses" and §8
   "Retain R34-C2 as CLEAN" — yet the fix it validates in §7 is a **counter rewrite** (design change). The
   report's label is config; its fix and its §3.4/§6 root-cause ("the transformation is a re-encoding, not a
   perturbation") are design. An outside reader resolves that internal contradiction toward the design
   reading, because only the design repair changes any measurement.

So: **design for the falsification, config for the detection defect (F3 species).** The stop record should
say exactly that.

---

## 6. Attack on the proposed repair (`mini-counter-fresh.py`): it repeats the defect in a new place

The stop record does not cite it, but the stop commit lands `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/mini-counter-fresh.py`
— the producing seat's "validated fix" (`ExecRedReproduce.md` §7, Appendix C). It is defeated 8/8 by a
structure-blind class the seat did not try, because its generator **writes the name pool in record order**:

- `mini-counter-fresh.py:66-67` builds `pool` in `records` order (`offsets[name] = len(pool)`), and
  `:77-78` writes record *i* with `offsets[name_i]`. Therefore pool-string *i* is the name of record *i*:
  the association is published by an order equality. The predicate's "the association is unpublished, so only
  record-array traversal recovers it" is false as written.

Counterexample reader (`ctl/ordinal.py`): reads header, reads each record's `flags`/`value` at `+2` (it never
touches the `name_off` column at all), splits the pool in file order, pairs the i-th string with the i-th
record. Class: **ordinal-association replay** — a strengthened representative of the registered
`record-order-replay` class, which the gate's own obligation names ("the record order itself",
`replay-gate.py:5-7`).

| surface | ordinal | structural | UTC |
|---|---|---|---|
| frozen `mini-counter.py` (pool permuted) | **5/8**, exit 1 | 8/8 | 07:35:36Z |
| committed `mini-counter-fresh.py`, seed `kaidoku-r34b-w2-seed1` | **8/8**, exit 0 | 8/8 | 07:35:36Z |
| committed `mini-counter-fresh.py`, seeds `…-s1/s2/s3` | **8/8** ×3, exit 0 | 8/8 ×3 | 07:35:36Z |
| my `probe/fresh-poolperm.py` (pool shuffled, not deranged) | 1/8, exit 1 (identity permutation, `gen-6`) | 8/8 | 07:35:36Z |

Gate with the committed fresh counter and **nine** registered classes (the seven + `content-multiset` +
`ordinal-association`): `python3 -I -B tools/round-34/replay-gate.py --root <lane> --config …/probe/gate-config-fresh9.json`
→ `REPLAY_GATE_REFUSED … shortcuts_over_target=ordinal-association`, exit 2, 07:37:27Z. Its rows:
structural 8, ordinal 8, all other seven + nameset 0.

Two further reasons the candidate is not sufficient even with a shuffle:
- **Identity permutations**: `rng.shuffle(pool_order)` is the identity with probability 1/n!; at seed
  `kaidoku-r34b-w2-seed1` the 2-record `gen-6` got `[0,1]`, which is why `fresh-poolperm` still leaked 1/8.
  A *derangement* is required, not a shuffle.
- **Duplicate payloads**: replaying the candidate's own `generate()` at seed `kaidoku-r34b-w2-seed1` gives
  `gen-0` (5 records) with `(1,0)` twice and `gen-7` (2 records) with `(3,0)` twice — the 2-record `gen-7` is
  fully homogeneous, so no association is observable there at all (measured 07:42:00Z);
  equal payloads make the association unobservable under a sorted-multiset comparison (the `theta` channel, §3).

Ironically the frozen surface's `permute` is *stronger* here than the candidate: it reorders the pool
independently, and ordinal never reaches 8/8 on it (5/8, and only via the two 1-record fixtures, one identity
permutation and `theta`'s homogeneity).

### Smallest safe correction, validated (E11/E12)

1. **Generate the eight fixtures per run from entropy** (no published corpus). — kills content-multiset.
2. **Lay the pool out as a derangement of the record order**, rewriting every `name_off`. — kills ordinal.
3. **Give every record in a fixture a distinct `(flags,value)` payload.** — makes association observable
   under a sorted comparison.
4. **Require ≥2 records per fixture.** — a 1-record fixture is associative without any link.
5. **Register `content-multiset` and `ordinal-association`; assert registered set == pinned set before
   CLEAN** (the F3 route). — keeps the registry honest.
6. **New claim revision.** The frozen instruments cannot be edited (`claims.json:22`); this is next-round
   material, not a post-freeze patch.

Validated in scratch as `probe/fresh-corrected.py` + `probe/gate-config-corrected.json`:

| check | result | exit | UTC |
|---|---|---|---|
| structural, seeds s1/s2/s3 | **8/8** ×3 | 0 | 07:38:43Z |
| `content-multiset` (nameset), seeds s1/s2/s3 | **0/8** ×3 | 1 | 07:38:43Z |
| ordinal-association, seeds s1/s2/s3 | **0/8** ×3 | 1 | 07:38:43Z |
| gate, corrected counter + **9** registered classes | `REPLAY_GATE_CLEAN … shortcuts_below_target=9`, exit 0 | 0 | 07:38:57Z |

That is the only repair I measured that both keeps the positive control and kills the classes that killed the
frozen surface. It is a *design* repair; no configuration change produces it.

---

## 7. The stop's five record defects: verified, and what is missing

| id | stop's claim | my check | verdict |
|---|---|---|---|
| F1 | pins live under `claims[0].pins`; `instruments.json` repairs container only | 26/26 digests equal, `instruments == pins`, no file mismatch (07:40:06Z) | **verified**; repair did not change any pinned byte |
| F2 | predicate identity false, A ≠ B; disclosed not repaired | A sha `7c6c17f0…` (31 words) vs B `8340aea5…` (46 words), recomputed | **verified** |
| F3 | class drop invisible down to the floor; no set equality | 3-class config → `REPLAY_GATE_CLEAN … shortcuts_below_target=3`, exit 0 (07:37:58Z); code `replay-gate.py:58,112,123` | **verified** |
| F4 | gate mutant ignoring the last row survives selftest and turns red CLEAN | mutant `probe/replay-gate-mut-lastrow.py`: `--selftest` → `cases 12, failures 0, mutants_killed 3`, exit 0 (07:38:04Z); `--config gate-config-naive.json` → `REPLAY_GATE_CLEAN`, exit 0 (07:38:05Z); green config also CLEAN (07:38:06Z) | **verified** (the mutant is invisible to the selftest, and it converts the frozen red case to CLEAN) |
| F5 | receipts untracked at first audit, landed in `b917ea64` | `git merge-base --is-ancestor b917ea64 cd75b92e` true; `after/`, `controls/`, `instruments.json` all in `git ls-files` | **verified** |

**Undisclosed in the stop record:**

- **N1 — causal mis-assignment.** `why_this_falsifies_the_surface` / `kill_rule_applied` attribute the
  falsification to the class being *unregistered*; E6 shows registering it makes the claim a miss. The
  sentence implies a repair that does not exist. This is the defect the assignment asked me to find.
- **N2 — committed-but-unvalidated repair.** The stop commit lands `mini-counter-fresh.py` and `pathkey.py`
  but cites neither. `claim-stop.json` contains no reference to either (checked). The candidate fix is
  defeated 8/8 by ordinal association (§6), and its receipts live only in scratch — no `gate-fresh.json` or
  `gate-gap.json` exists anywhere under `.ufo/waves/round-34/r34b`.
- **N3 — unnamed falsified sentence.** The record does not say A/B (not falsified) vs C/O (falsified). This is
  the same species as F2, at a different site: the stop narrative rather than the instrument.
- **N4 — approximate timestamp, no in-lane receipt.** `l1_rerun_utc` is "~07:28:00Z (approximate)". I reproduce
  at 07:32:58Z (three seeds) and 07:35:36Z (ordinal). The L1's exact rerun receipt is not in the lane; the
  producing seat's own receipt is 07:19:02Z. Fine for a stop, but "exact clock in the wave report" points at a
  clock that is not there.
- **N5 — producer verdict overridden silently.** `producer_seat` is `ExecRedReproduce.md`, whose §8 says
  "Retain R34-C2 as CLEAN" and whose §9 calls the gap "registration-completeness/rationale gap". The stop
  reaches the opposite verdict without recording the disagreement. The override is the L1's to make; the
  *disagreement* belongs in the record.

---

## 8. What the next round must do differently — per reading

| if the reading is … | next round must … | why that is not enough alone |
|---|---|---|
| **config (registration)** | pin the class list; assert `registered == pinned` before CLEAN (close F3); register content-multiset, ordinal, and the five `MutShortcutClasses` 8/8 variants; re-freeze | E6: with the class registered, the claim's own counter returns MISS (`clauses_failed=green_clean`). A complete registry kills the claim rather than certifying it. The class space is unbounded (three seats found seven 8/8 specimens); a finite list can never satisfy O's "any shortcut". |
| **design (invariant)** | replace the green surface: per-run entropy generation, **pool derangement**, **distinct payloads**, **count ≥ 2**; register the killed classes; re-freeze as a new claim revision | A fresh corpus alone is not enough — `mini-counter-fresh.py` is 8/8 for ordinal association (§6). Fresh content and layout independence are two independent requirements; the frozen surface had the second but not the first, the candidate has the first but not the second. |

Both readings require a **new instrument revision and a new claim**, because the frozen instruments cannot be
edited (`claims.json:22`) and the frozen green clause cannot survive a complete registry (E6). Neither reading
permits a post-freeze patch.

---

## 9. Impacted axes

- **depth** (the claim's axis): no capability credit and no score movement (owned 10 → 10 unchanged). The
  *rationale sentence* of the instrument (C) is false, which is a depth-surface defect, not a depth gain.
- **calibration**: the stop is honest and the falsification is real (positive); the causal mis-assignment (N1)
  and the silently overridden producer verdict (N5) are calibration defects to correct in the record.
- **operability**: the committed candidate fix is not operable as an instrument — no selftest, receipts not
  in-lane, and defeated 8/8 by a class it did not test.
- **coverage**: the registered set versus the class space (F3; ≥7 unregistered 8/8 specimens in wave-1 alone).
- **freshness**: frozen instruments versus a required redesign; correction is next-round.
- **adjacency**: unaffected (no cross-domain evidence involved).

---

## 10. Verdict

**STOP_CAUSE = FIXTURE DESIGN, NOT REGISTRATION.** The stop's verdict ("falsified measure; honest stop") is
correct, but its causal sentence is not: the transformation is answer-preserving (`mini-counter.py:58`;
E5 decoded answer invariant 8/8; oracle answer a pinned constant), so the green surface cannot force traversal
for any class that can recall the constant. The registration gap is a *detection* defect: registering the
winning class makes the gate REFUSED (exit 2, 07:33:08Z) and the claim's own counter MISS with
`clauses_failed=green_clean` (exit 1, 07:33:51Z) — it never restores the capability. An outside reader of the
committed bytes alone adopts the **design** reading: the instrument states its own answer-invariance, the
oracle is public, predicate A is registration-qualified and still true (E13), and the config "repair" is
self-defeating. The producing seat's proposed fix (`mini-counter-fresh.py`) is itself defeated 8/8 on three
seeds by ordinal association because its generator writes the pool in record order (§6); the smallest safe
correction is per-run generation + pool derangement + pairwise-distinct payloads + count ≥ 2 + registering
`content-multiset` and `ordinal-association` + asserting registered == pinned, validated at structural 8/8,
both shortcut classes 0/8 on three seeds, and gate CLEAN with nine classes (07:38:57Z).

No claim reopened, no frozen instrument edited, no score awarded. utc=2026-10-25T07:42:57Z.
