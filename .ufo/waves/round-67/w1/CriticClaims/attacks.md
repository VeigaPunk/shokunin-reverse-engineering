# Round-67 claim attacks — CriticClaims

Adversarial review of R67-C1 and R67-C2 by execution, not by re-reading. Every receipt below was
produced with `python3 -I -B` and `TMPDIR` inside the seat scratch
(`/fast/scratch/hyaku/kaidoku-r67/CriticClaims`, since deleted); the JSON receipts are copied into
`receipts/` and the driver scripts into `scripts/` beside this file. The lane was moving while this
seat ran: the correction commit `1e7fe7b7` and the disclosure commit `6dcc447e` landed mid-flight, so
each receipt names the instrument bytes it ran (`counter_sha256` / hashes of the copied scripts).

Frozen inputs used: base `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92`, operative freeze
`3663e6b21dccf4c4957f459301156664d8b151d6`, claim container
`.ufo/waves/round-67/claims.json`, plan `plans/round-67-claims.md`.

Verified before attacking:

- freeze = the commit that first adds `claims.json` (`git log --diff-filter=A --format=%H --
  .ufo/waves/round-67/claims.json` → `3663e6b2…`);
- carry-in `cf705c53` and instruments commit `39a91a99` are ancestors of the freeze (`merge-base
  --is-ancestor`, exit 0 both);
- every pin in the frozen container matches the blob at the freeze; the C1 and C2 predicate strings
  are byte-identical between `claims.json`, `PREDICATE` in each instrument, and (modulo the
  blockquote wrapping) the plan;
- C2 reproduces green on the shipped bytes: `receipts/score-c2.json` — `killed_before 0`,
  `survived_before 2`, `killed_after 2`, pristine 30/26 cases CLEAN, exit 0.

---

## F0 — the frozen C1 instrument could not verify anything (counterexample, fatal)

**Clause attacked:** the whole C1 predicate — specifically "reports carriers_matched 4 of 4 … and
exit 0".

**Attack.** Run the frozen counter blob itself (`git show 3663e6b2:tools/round-67/avm-le-counter.py`,
sha256 `f78ed365…`) at the base revision with the operative freeze:

```
python3 -I -B <frozen-blob> --score --root <lane> --rev a7a4ce6… --freeze 3663e6b2… \
        --pkg65 /nonexistent --claims <lane>/.ufo/waves/round-67/claims.json --out <receipt>
```

**Result.**
`receipts/score-c1-frozen-blob.json`: `exit_code 2`, `unevaluable "gap-rule.json absent at freeze"`.
No carrier clause is ever evaluated. C1 was unsatisfiable as frozen, for every possible data run.

**Cause (traced, not guessed).** `patch_engine()` sets `mod.GAPRULE = str(rule)` where
`rule = Path(args.gap_rule).resolve() if args.gap_rule else repo / RULE_V2` — always absolute. The
engine reads its rule through `show(root, freeze, GAPRULE)` = `git show <freeze>:<path>`; an absolute
path is a git-object miss (`git show HEAD:/home/...` → rc 128), `show()` returns `None`, and
`measure()` raises `Unevaluable('gap-rule.json absent at freeze')` before the carrier loop. Receipt:
`receipts/attack-A-B-c1.json`, block `A`: `show_absolute_rule_at_freeze false`,
`show_relative_rule_at_freeze true`.

**Why the before-arm missed it.** `control()` never calls `measure()`; it re-derives the disposition
check from the committed round-50 envelopes with `repo / RULE_V2` read directly. The do-nothing
control therefore passed (`receipts/control-c1.json`, exit 0, 2/4 vs 4/4) while the score path was
dead. The control and the after-arm do not share an entry point.

**Lane response (observed, mid-flight).** `1e7fe7b7` changes the patch to a lane-relative name
(`rule.resolve().relative_to(repo)`), re-takes the before record, and `6dcc447e` discloses the
supersession in `claims.json` (pin `f78ed365… → 55decb51…`, atom `A10`, `instrument_supersessions`).
Probe on the corrected bytes (`receipts/probe-fixed.json`): patched rule
`tools/round-67/gap-rule-v2.json`, `show_at_freeze true`, `show_at_rev true`; `measure()` now reaches
the package gate (`Unevaluable: rea package does not match the freeze …`), i.e. past the rule read.

**Freeze-gate facts.** `tools/round-29/freeze-gate.py --root . --rev 6dcc447e` audits round-67
**CLEAN**, no findings (`receipts/freeze-gate.json`). At the correction commit itself
(`--rev 1e7fe7b7`) round-67 is **FLAGGED**, `INSTRUMENT_REVISED` with `disclosed: 0`
(`receipts/freeze-gate-at-correction.json`). This is the round-24 pattern: CLEAN only after a
self-disclosed post-freeze revision, FLAGGED at the revision.

**Smallest safe corrections.**
1. (Power) the corrected counter should emit its `counter {path, sha256}` block on the *unevaluable*
   path too — the two exit-2 receipts above carry no instrument identity, so a "could not evaluate"
   verdict cannot be attributed to the bytes that produced it. `control()` already emits it.
2. The before-arm for a score claim must exercise the score entry point to its first input failure
   (a `--score` probe with an empty cache and a valid rule), not only the control branch. One probe
   of this shape would have caught F0 before the freeze.
3. The `A0` atom says "no claim amendment after this file"; the container *was* amended after the
   freeze. The gate sanctions it, but the disclosure should say so in those words, and the re-taken
   before record postdates the data-run commit `a4c1d0fc` (21:56) at 21:57:37 — the declared order
   instruments → controls → data is inverted for the corrected instrument. The control reads only
   round-50 envelopes, so it is not contaminated; the inversion is a provenance fact, not a
   measurement error.

**Impacted axis:** coverage (C1), calibration (the freeze disclosure / before-arm order).

---

## A — relabelled carrier: the freshness drop (predicate survives; the stated rationale is false)

**Clause attacked:** "carriers_matched 4 of 4" — its clause set is patched to drop
`carrier_fresh_ok` (`DROPPED_CLAUSES`), and the plan justifies it: "a re-measurement of the same
pinned carriers cannot be fresh".

**Attack.** Evaluate the engine's own freshness predicate on the four pins without any carrier
bytes: load the pinned engine through the frozen counter's `load_engine()`, read
`tools/round-50/carriers.json` at the freeze, call `prior_pins(root, freeze, spec)` (the engine's own
function, exactly the expression `d['carrier_fresh_ok'] = pin not in prior`), and compare.

**Result** (`receipts/attack-A-B-c1.json`, block `A`, run on the frozen counter):

- prior set = 18 pins from `.ufo/waves/round-41/c1/carriers.json`,
  `tools/round-49/carriers.json`, `tools/round-42/prior-pins.json`;
  `tools/round-50/prior-pins.json` does not exist.
- `pin_in_prior`: **false for all four** (`g7581`, `g7582`, `c6490`, `c6430`).
- Therefore `carrier_fresh_ok` is **true 4/4**. Dropping the clause changes nothing; with the full
  23-clause conjunction the same four carriers would still match on freshness.

**Does the predicate disclose the reuse?** The *plan* does, twice ("a re-freeze of the round-50
LE-AVM measurement", "Frontier → Core on the same four pinned carriers"). The *predicate* does not:
"carriers_matched 4 of 4" is silent on both the reuse and the dropped clause. The receipt's
`patches.dropped_clauses` discloses the drop, so the run is auditable after the fact.

**Outcome:** predicate **survives** — no carrier is counted beyond what the plan's prose states, and
the drop is a no-op. The stated *reason* is **falsified by the engine**: a re-measurement of these
four pins is fresh under the engine's own definition. The latent defect is in the definition:
`prior_pins()` never reads the immediately previous C1 freeze's own `carriers.json`, so a genuine
relabelling (same bytes, new ids/table) passes all 23 clauses.

**Smallest safe correction.** Delete `DROPPED_CLAUSES` (keep all 23 clauses): freshness passes 4/4,
the receipt then shows it, and the claim carries no hidden premise. Doing nothing to the counter is
also safe *if* the plan's "cannot be fresh" sentence is corrected — as written it is false against
the pinned engine. Because the counter is already superseded once, prefer the prose correction plus
a note that the clause drop is a no-op; a second counter edit costs another disclosure.

**Impacted axis:** coverage (C1); the engine's freshness clause for future rounds.

---

## B — rule scope: `--score` cannot tell the round-67 rule from a laxer one

**Clause attacked:** "run under the round-67 gap rule" (and, secondarily, the predicate's "while the
four frozen envelopes … report gaps_ok on 2 of 4").

**Attack.** Build four rule documents and drive the engine's own `gap_rule_model` +
`disposition_check` over the four committed round-50 envelopes, exactly as `control()` does:
`r50` (the frozen round-50 rule), `v2` (the round-67 rule), `symlink-waived` (v2 with
`required.symlink=false` and a class note — the attack rule), `all-required-off` (every `required`
false). Then repeat with red fixture 1 (drop one symlink `unpublished-entry` gap, `bin/adsl` on
`g7581`).

**Result** (`receipts/attack-A-B-c1.json`, block `B`):

| rule | gaps_ok over the four envelopes | red fixture (symlink gap removed) |
|---|---|---|
| r50 | 2/4 | fails |
| v2 | 4/4 | **fails** (`bin/adsl`) |
| symlink-waived | 4/4 | **passes** |
| all-required-off | 4/4 | **passes** |

All four rules are structurally valid (`rule_problems` empty). So on the four carriers the
round-67 rule and a laxer rule produce the *same* `carriers_matched 4 of 4`; the only discriminator
is the red fixture, which `--score` never runs. `score()` pins the engine (`ENGINE_PIN`) but not the
rule: `rule = Path(args.gap_rule).resolve() if args.gap_rule else repo / RULE_V2`, then only
`rule_digest = sha256_file(rule)` is recorded — no comparison with the claims pin `e66ba0…`. After
the correction, `patch_engine` requires the rule to lie inside the lane, which narrows the input but
does not identify it: any pre-freeze in-lane JSON at another path is accepted and scored.

Two further bindings are weaker than the predicate reads:

- the receipt's `rule.sha256` is `sha256_file(rule)` — the **working-tree** file — while
  `measure()` builds its model from `show(root, freeze, GAPRULE)` and `gap_rule_unchanged` compares
  freeze against rev **blobs**. A dirty worktree yields a receipt whose rule sha describes bytes that
  were never scored;
- the "2 of 4 under the round-50 rule" clause exists only in `control()`; the `--score` receipt has
  no `gaps_ok_round50` field. The after-arm named by the predicate cannot evidence that clause by
  itself.

**Does the counter distinguish the attack without the red controls?** No. The `--score` receipt's
only identity evidence is the recorded path/sha, and neither is checked. As frozen (`f78ed365…`)
the point is moot — `--score --gap-rule` could not run at all (F0); with the corrected bytes any
in-lane rule is accepted.

**Exact detectors.**
1. In `score()`: refuse unless the rule's **blob at the freeze** equals the claims pin
   (`sha256_bytes(show(root, freeze, GAPRULE)) == "e66ba0…"`), and record that blob sha in the
   receipt instead of/alongside the working-tree sha.
2. In the landing gate: require `round67_rule_still_fails true` **and** `junk_rule_would_pass true`
   from the `--control` receipt (`red_controls`), i.e. make the red fixture part of the verified
   evidence, not only a pre-arm.
3. If the predicate is to be self-contained, `--score` must embed the round-50 control count (the
   `2 of 4` clause has no line in the score path, contrary to the plan's clause trace which points at
   `control()`).

**Outcome:** **needs data / detector gap** — not falsified as written (with the real v2 the
predicate holds), but a `--score` exit 0 does not prove the rule.

**Impacted axis:** coverage (C1), calibration (rule identity in the receipt).

---

## C — false-kill attack on C2 (no false kill; the guard holds)

**Clause attacked:** "kills both survivors" — the `killed_after` definition
`after_rc != 0 and EXPECTED_CASE[name] in failed_cases`.

**Attack.** Build a closure-counter mutant that fails a case **other** than the survivor's
`EXPECTED_CASE` (`arm-false-bound`): `arm()` returns `"passed": False` for every input. It passes
`arm-false-bound` (got False, want False) and fails `arm-true-bound` (got False, want True).

**Result** (`receipts/attack-C2-corrected.json`, block `C`): battery rc 1,
`failed_cases ["arm-true-bound"]`, `arm-false-bound` PASS, `killed_after_by_shipped_formula false`.
The battery does **not** report the mutant killed, which is correct: it is not the always-True
survivor.

**Dead end recorded honestly.** A first shape mutated the closure counter's own `--selftest`
(`count-constant 30 → 31`). The battery returned **rc 0** (`receipts/attack-C-D-c2.json`, block `C`):
when `--closure <mutant>` is passed the battery *skips* `closure-selftest-green`, so a mutant's own
selftest never scores it. That shape proves nothing about the guard and is not counted as a result.

**Residual (bounded).** The verdict is one case wide per survivor, and `--score` scores only the two
mutants it builds; it does not search for new survivors. A repair wave should treat the verdict as
"the two named mutants are dead", never as "the class is covered".

**Outcome:** **survives** — no false kill found.

**Impacted axis:** depth (C2).

---

## D — false-survive attack on C2 (the named mutant is killed; the class rule is falsified)

**Clause attacked:** "the coverage counter whose `recipe_a_equivalence` returns equivalent without
running the block" — via the claim's stated repair rule: a survivor is closed by a selftest case
that exercises the mutated function on a *false* input.

**Attack.** `recipe_a_equivalence` never calls `subprocess`; it returns
`recipe_a_equivalent: True` iff the extracted block **text** contains `"mapped": 1`, and False with
a synthetic diff otherwise. Both battery fixtures are reproduced without executing anything. Then
test it on a *lying block*: a fixture whose block text still says `"mapped": 1` but prints
`"knowledge_files": 99`.

**Result** (`receipts/attack-C-D-c2.json`, block `D`):

- battery on the mutant: **rc 0, no failed cases — it survives**; `equiv-honest-true`,
  `equiv-doctored-bound` and `equiv-doctored-diffs` all pass.
- lying-block fixture: pristine counter → `equivalent false`, diffs `["knowledge_files"]`; the mutant
  → `equivalent true`, no diffs, **without executing the block**.

**Why it survives.** The shipped doctored fixture differs from the honest one only in the block
*text* (`"mapped": 0` vs `1`, `coverage_score 0.0` vs `10.0`). A false input whose signal is visible
statically does not separate "ran the block" from "read the text"; the mutant reproduces both answers
without running.

**Arm-shaped variants are caught (contrast).** The example shape "`arm()` returns `passed: True`
only when `detail` is empty" is **killed**: `arm-false-bound` calls `arm("ctl", False, {})` with a
falsy detail, so the mutant returns True and the case fails
(`receipts/attack-D-arm-detail.json`, rc 1, `failed_cases ["arm-false-bound"]`). The arm survivor
family is covered because its binding case feeds the *falsy* value a conditional mutant would key
on; the coverage binding case feeds a text-doctored fixture, which a text reader can reproduce
without executing. That asymmetry is why the coverage class stays open.

**Scope of the falsification.** The predicate's *literal* survivor is the r66 M2 byte-patch
(unconditional `True`), and it is still killed (`killed_after 2`). So the predicate **survives as
worded**. The claim's stated **rule** — a false-input case closes the survivor class — is
**falsified**: a mutant that never runs the block passes the battery.

**Smallest safe corrections.**
1. Doctor the **data**, not the block text: honest and doctored fixtures share a byte-identical
   recipe-A block that computes from the corpus; only the corpus differs. A no-run mutant cannot
   answer differently. Receipt `receipts/attack-C2-corrected.json`, block `D_correction`: a no-run
   mutant keyed on text common to both fixtures returns one answer for both and **is killed**
   (`equiv-doctored-bound`, `equiv-doctored-diffs`; rc 1).
2. Or add an execution sentinel: the fixture block writes a sentinel file; a case
   `equiv-block-executed` asserts it exists after the call. This kills every `subprocess`-skipping
   mutant directly.
3. Record residual survivors (this one included) in the round lesson rather than claiming the class
   is closed.

**Impacted axis:** depth (C2), calibration (what "killed" covers).

---

## E — claims not falsified here, and what would falsify them

**R67-C2 — cannot falsify after A–D.** The three named clauses hold on the shipped bytes:
`killed_after 2` with the exact `EXPECTED_CASE` in each failed list, `killed_before 0` under the r66
selftests, both pristine counters CLEAN at 30 and 26 cases (`receipts/score-c2.json`, exit 0).
Would falsify: `killed_before > 0` (the r66 selftests already kill a survivor); a `killed_after < 2`
or a kill whose failing case is not the `EXPECTED_CASE`; a pristine counter non-zero; or an
`after_selftest_exit 0` for a mutant whose expected case failed. None occurs.

**R67-C1 — needs data.** The predicate's positive half cannot be evaluated without the carrier
cache, the `rea-agents 6.5.0` package, and committed receipts. Current lane state at
`6dcc447e`: the four `corpus/evidence/round-67/c1/<id>/after.json` exist on disk but are **untracked**
(`git status --porcelain` → `??`; `git cat-file -e HEAD:corpus/evidence/round-67/c1/g7581/after.json`
→ rc 128), so `receipt_present` is false at every commit rev and `--score` must exit 1 until they
land. The data-run commit `a4c1d0fc` carries only `run.json`. Would falsify: any carrier clause false
under v2 at the record, `met_target` false, or exit ≠ 0. The frozen instrument's exit 2 (F0) did
falsify the frozen artefact; the corrected-instrument probe gets past the rule read, and the rest is
the after-arm's to measure.

---

## Receipt index

| receipt | what it shows |
|---|---|
| `receipts/score-c1-frozen-blob.json` | frozen C1 counter `f78ed365…`: exit 2, `gap-rule.json absent at freeze` (F0) |
| `receipts/attack-A-B-c1.json` | A: 18 prior pins, none of the four; freshness true 4/4. B: gaps_ok r50 2, v2 4, symlink-waived 4, all-off 4; red fixture v2 fails, lax passes; absolute-vs-relative rule read (F0) |
| `receipts/control-c1.json` | the shipped `--control` on the frozen bytes: 2/4 vs 4/4, both red fixtures fire, exit 0 |
| `receipts/score-c2.json` | C2 green on shipped bytes: killed_before 0, killed_after 2, pristine 30/26 CLEAN, exit 0 |
| `receipts/attack-C-D-c2.json` | D: text-reading mutant survives the battery (rc 0) and blesses a lying block; C dead end recorded |
| `receipts/attack-C2-corrected.json` | C: unrelated failure `arm-true-bound` is not a kill; D correction: a no-run mutant keyed on common text is killed by a data-doctored pair |
| `receipts/attack-D-arm-detail.json` | D contrast: `arm()` passing on a falsy `detail` is killed by `arm-false-bound` |
| `receipts/probe-fixed.json` | corrected counter `55decb51…`: rule relative, show at freeze/rev true, measure reaches the package gate |
| `receipts/freeze-gate.json` | `tools/round-29/freeze-gate.py --rev 6dcc447e`: round-67 CLEAN, no findings |
| `receipts/freeze-gate-at-correction.json` | same gate `--rev 1e7fe7b7`: round-67 FLAGGED `INSTRUMENT_REVISED`, disclosed 0 |

Scripts: `scripts/attacks_c1.py` (A, B), `scripts/attacks_c2.py` (first C shape, D),
`scripts/attacks_c2b.py` (corrected C, D correction), `scripts/arm_detail.py` (D arm contrast),
`scripts/probe_fixed.py` (corrected-instrument probe).
