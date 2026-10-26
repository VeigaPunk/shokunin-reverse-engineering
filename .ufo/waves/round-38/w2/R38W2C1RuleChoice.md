# R38W2C1RuleChoice — attack on the rule choice (round 38, attempt 2, wave 2)

Seat: critic (leaf; no dispatch, no background jobs, no `agent://all`). Judged on coverage, calibration.
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Attacked object: attempt 2's ruling that
R38-C1/R38-C2 are judged by the **first freeze** `e059ca9391642d5b71b6662cabcbdce0d9308719`, not by
attempt 1's amendments `79f69347` (v2, 03:30:33 -03) and `f1010f67` (v3, 03:32:55 -03).
Everything below is measured on committed bytes plus the committed wave-1 evidence; nothing was
written outside this report and `.ufo/waves/round-38/w2/artifacts/R38W2C1RuleChoice/`.

**Verdict (one line): CONFIRMED — attempt 2's first-freeze rule choice is correct and is the only
reading the prompt rules permit; the v2 note's sentence "No claim was scored under v1" is
FALSIFIED (a seat had both produced claim data and run the first-freeze counter ~7–13 min before
v2), and attempt 2's own lesson/SCORECARD already record that contradiction; two record defects
remain (QUALITY 79 self-contradiction; the v1 counter accepts exactly the receipts its own predicate
sentence excludes), neither of which changes the verdict.**

## 0. Timeline (all times -03:00; commit times from `git log --format='%H %ci %s'`)

| time | event | source |
|---|---|---|
| 03:06:32 | **first freeze** `e059ca93` (claims doc, counters, harness, carriers, instruments, census start) | `git log` |
| 03:09:14 | controls `efd5c47a` (7 controls, all exit 1) | `git log` |
| 03:15:59 | wave-1 spec/dispatch commit `9c9d496b`; `w1.ready` 03:16, `.dispatched` 03:20, results 03:40 | `git log`; `.ufo/waves/round-38/` |
| 03:17:22–03:18:23 | K1 seat REA arms (outdir-precreated exit 1; fresh exit 0; diagnostic with `sasquatch-v4be` on PATH, 5/5) | `w1/R38ExecAfterK1.md` §2a–2c |
| 03:17:38 | **K1 after envelope produced** (claim data), 7 934 B assigned arm / 18 928 B diagnostic | `w1/R38ExecAfterK1.md` §2a/§2c |
| 03:19:01 | `cb4326b2` harness fix (post-freeze instrument change; `mkdir -p` → `rm -rf`) | `git log` |
| ~03:18–03:19 | R38ExecRecountBase runs the **first-freeze counters** at base/freeze/tip (`carriers_matched 0`) | `w1/R38ExecRecountBase.md` §1; report mtime 03:19:09 |
| 03:20 | K1 counter fixtures on the lane worktree (`counter-fixture.K1-*.json`, mtime 03:20) | `w1/artifacts/R38ExecAfterK1/` |
| 03:22:17 | first observed working-tree drift of `c1-counter.py` (`f27f982b…`, v2 draft rewriting the frozen docstring) | `w1/R38SentinelBounds.md:57-60` |
| **03:23** | K1 re-runs the counter against the **frozen bytes** restored from git (`c1-counter.frozen.py`, sha `a7a62b09…`), K1 block `matched: true`, exit 1 | `w1/R38ExecAfterK1.md:119-131`; receipt files mtime 03:23 |
| **03:23–03:24** | EnvelopeRules scores **all four draft receipts**: `carriers_matched 3`, K2 `after_gaps_empty False`, exit 1 (fixture `f28904a8`) | `w1/R38ExecEnvelopeRules.md:114-127`; `artifacts/R38ExecEnvelopeRules/counter-fixture-four-receipts.json` |
| 03:23:54 | K1 report finalized; 03:25:45/03:27:58 claims doc + counter mtimes (v2 draft, uncommitted) | K1 report mtime; `w1/R38ReviewerEntryQuality.md:221-222` |
| 03:26:24 | ExecBeforeArmRecheck: "K1/K3/K4 matched, K2 unmatched → `carriers_matched == 3`" | `w1/R38ExecBeforeArmRecheck.md:28` |
| **03:30:33** | **v2 commit `79f69347`** (predicate + counter rewritten; note calls itself "pre-scoring") | `git log` |
| 03:31:12 | `3b0da5d` C1 controls re-scored under v2 | `git log` |
| 03:32:55 | **v3 `f1010f67`** (after-gap binding narrowed: `unpublished-entry` gaps admitted) | `git log` |
| 03:33:18 | `077e212` c1-0 re-scored under v3 | `git log` |
| 03:37:05 | attempt-1 L1 dies without a report | `corpus/lessons/round-38.md:6` |
| 03:46:44 | **landing** `3b960fe5` (receipts, entries, SOURCES, QUALITY 79–80) | `git log` |
| 03:50:00 | `0fc6113` (SCORECARD coverage row + round-38 section, LOG, lesson, L1 scores) | `git log` |

## 1. Q1 — did any seat run the first-freeze counter or produce claim data before 79f69347?

**Yes, both.** Three independent instances, all before 03:30:33:

1. **Claim data**: the K1 after envelope was produced at 03:17:38 (`w1/R38ExecAfterK1.md` §2a; the
   diagnostic arm 03:18:20–03:18:23). The first-freeze claims doc itself defines
   `corpus/evidence/round-38/c1/K*/after.json` as "claim data, produced after the freeze"
   (`git show e059ca93:plans/round-38-claims.md:41`).
2. **First-freeze counter run on claim-shaped data**: at 03:23 the K1 seat re-ran the counter with
   the frozen blob restored from git, `sha256 a7a62b09…` (`w1/R38ExecAfterK1.md:119-131,167`). I
   verified `a7a62b09…` is exactly `git show e059ca93:tools/round-38/c1-counter.py`
   (see §4). The K1 per-carrier block came back `matched: true`, gaps 0, oracle 5/5 — a score of K1.
   This is bracketed: after the first observed worktree drift (03:22:17) and before the v2 commit
   (03:30:33).
3. **Full-carrier score before v2**: the same wave's EnvelopeRules seat built a fixture from
   committed bytes plus its four draft receipts (`f28904a8`) and measured `carriers_matched 3,
   met_target False` with v1-shaped per-carrier keys (`w1/R38ExecEnvelopeRules.md:114-127`;
   `counter-fixture-four-receipts.json`: keys `after_gaps_empty` … `oracle_frozen`, no `before_*`).
   ExecBeforeArmRecheck reproduced the same `3` at 03:26.
   Additionally R38ExecRecountBase ran the frozen counters at base/freeze/tip (report mtime 03:19:09).

So the amendment landed **after** both claim data and counter scores existed. The seat that
accepted the v2 note's sentence, R38ReviewerEntryQuality (`:234-236`, 03:29:47), wrote "the only
counter runs on record are the do-nothing recounts" — that statement is contradicted by two
sibling reports committed in the same wave directory.

## 2. Q2 — is the v2 note's "No claim was scored under v1" false?

**Yes, false.** `plans/round-38-claims.md` (tip; the note begins at `:9`) says at `:16`:
"No claim was scored under v1; v2 is the frozen bytes every receipt and score now complies with."

It is false under both available readings:

- **"produced claim data"**: K1's after envelope at 03:17:38 and all four draft receipts by 03:23
  (`w1/R38ExecEnvelopeRules.md:114`) — 13 and 7 minutes before v2 respectively.
- **"ran a counter"**: K1's frozen-bytes run at 03:23 (above); RecountBase; EnvelopeRules.
  The lane's own criterion spells the test disjunctively: QUALITY 79 — "whatever note calls it
  'pre-scoring' once any seat has run a counter or produced claim data"
  (`corpus/QUALITY.md:87`).
- Even the narrowest reading ("scored" = a full `met_target` decision on committed receipts) does
  not rescue v2: §6 item 9's first clause, *"judged on the counter, kill rule and predicate declared
  before data"*, is independent of the word "scored", and v2's predicate/counter were declared after
  the four-carrier draft data.

**This is not a defect of attempt 2.** Attempt 2 does not repeat the sentence; it marks it:
`corpus/lessons/round-38.md:17` (M38-1: "amended after seats had scored, and the amendment called
itself 'pre-scoring'") and `SCORECARD.md:3402` ("Attempt 1 amended the C1 predicate and counter twice
after wave-1 seats had scored carriers"). The frozen claims doc cannot be rewritten (§10), so the
correction living in the lesson/SCORECARD is the correct handling.

## 3. Q3 — readings under which attempt 2 should have used v2/v3, or declared C1 "unprovable"

Tested each candidate reading against the prompt text; **none survives**.

| reading | claim | why it fails |
|---|---|---|
| R-a "scored" = full `met_target` only | v2 was pre-scoring, so v2 governs | draft claim data existed at 03:17:38/03:23; §6 item 9 requires the rule to be declared **before data**, independent of "scored"; QUALITY 79's gloss is disjunctive ("run a counter **or** produce claim data") |
| R-b v2 restates the same claim with a corrected premise | predicate unchanged in substance | v2 adds a **paired before-receipt clause** and counter bindings `before_present/subject/operation/missing_extractor_gap/oracle_hits`; that is a different predicate (`git show 79f69347 -- plans/round-38-claims.md`, counter diff; `w1/R38ReviewerPredicateIdentity.md` §1). §10: "predicate, counter, kill rule and target stay exactly as declared" |
| R-c v3 is a counter *bug fix*, not a rule change | adopt v3 | §6 item 9: "The claim is judged on the **counter**…"; v3 changes the acceptance condition and flips K2 fail→pass on the same receipts (3/4 → 4/4, `l1/scores/c1-v{1,3}-at-3b960fe5*.json`). §6 item 9 also: "Never narrow a target after landing: a miss is an honest stop." The frozen claims text still says "carries no extraction gap" while the v3 counter admits `unpublished-entry` gaps (`w1/R38RevengerPremise.md` §3.1; `git diff 79f69347 f1010f67 --stat` touches only the counter and controls) |
| R-d the freeze's instrument map binds the harness, so the receipts are inadmissible → C1 unprovable | v1 cannot be scored | strongest counter-reading, still fails: (i) §6 item 9's rule set is counter/kill rule/predicate, not the invoking wrapper; (ii) QUALITY 79's and `tools/round-38/freeze-drift.py`'s path sets exclude `c1-run.sh` (the tool's `DEFAULT` list is claims doc, both counters, carriers, oracles); (iii) receipt admissibility is checked on the envelope (subject digest, evidence id), not on which script called REA — K1's seat called REA directly; (iv) even an empty admissible set leaves the counter **evaluable** (exit 1, not 2), and the frozen kill rule says a non-meeting counter is "an honest stop" |
| R-e v1's sentence is factually false → C1 is `unprovable` | use the label `unprovable` | `unprovable` is available only to an **exploratory** claim (§2 item 8: "At most one claim may be exploratory… otherwise it lands `unprovable`"); C1 is a coverage claim with a counting command. §6 item 9: "A target must be one a do-nothing control cannot reach… a miss is an honest stop"; §8 honesty requires reporting the falsified premise — attempt 2 does (M38-3; PROVINCE frontier note "not promoted") |
| R-f no rule choice can pass anyway | — | v3 at the landed revision still gives `met_target false` because `province_core_row`/`province_core_section` are false (`l1/scores/c1-v3-at-3b960fe5-NOT-THE-RULE.json`). The rule choice changes the reported number (3 vs 4), never the pass/fail on the landed bytes |

The frozen kill rule is the final word, and it is quoted from the first freeze itself:
"If the counter at the measured revision does not meet the target, C1 is **an honest stop**; the
counter, predicate, carriers and oracle are never changed after this commit"
(`git show e059ca93:plans/round-38-claims.md`, R38-C1 kill rule). §10 independently binds:
a resumed attempt "runs those claims unchanged." So "honest stop" is not a discretionary label;
"unprovable" would contradict both frozen bytes and §2 item 8.

## 4. Independent reproduction of the author verdict

Counter bytes: I took `w1/artifacts/R38ReviewerPredicateIdentity/c1-counter-at-freeze.py`
(`sha256 a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8`) and confirmed it equals
`git show e059ca9391642d5b71b6662cabcbdce0d9308719:tools/round-38/c1-counter.py` (same sha).
Its selftest from the freeze blob (plus the freeze's `tools/round-27/xpin-attribute.mjs` and
`tools/round-38/selftest/*`) is green:

```
$ HYAKU_SCRATCH=$S python3 -I -B tools/round-38/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0>
{"selftest": "c1-counter", "cases": 15, "green_ok": 1, "red_ok": 14, "failures": []}   exit 0
```

Score at the measured revision (`artifacts/R38W2C1RuleChoice/repro-v1-3b960fe.json`,
`sha256 1de283e1…`):

```
$ python3 -I -B c1-counter-at-freeze.py --root <lane> --rev 3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8 \
    --freeze e059ca9391642d5b71b6662cabcbdce0d9308719 --pkg65 <rea-agents 6.5.0 root>
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S112","S113","S114"],
 "frontier_note": true, "opened_source_rows": ["S112","S113","S114"],
 "province_core_row": false, "province_core_section": false, "sourced": true},
 "carriers_matched": 3, "carriers_unchanged": true, "met_target": false, ...}          exit 1
K1 (True, gaps 0, 5/5)  K2 (False, gaps 1, 3/3)  K3 (True, gaps 0, 4/4)  K4 (True, gaps 0, 4/4)
```

Byte-identical to `l1/scores/c1-v1-at-3b960fe5.json` (`carriers_matched 3`, same bindings).
The author's verdict is re-derivable with one command over committed bytes; C2's counter was never
amended (same bytes at freeze and at measure), so C2's rule choice is trivial.

## 5. Defects found (nothing frozen was changed; smallest safe corrections only)

**D-1 (calibration, medium) — QUALITY 79 contradicts itself and the gate was never run at the
measured revision.** The row (`corpus/QUALITY.md:87`, added by attempt 2) says the gate
"`freeze-drift.py --freeze <first freeze> --rev <measured>` runs … and **must print zero commits**",
then says "**A non-empty list** means the claim is scored with the first-freeze bytes and the
amendment is reported, never adopted". Both cannot hold at the measured revision: at `3b960fe5` the
gate exits **1** with `["f1010f67", "79f69347"]`
(`artifacts/R38W2C1RuleChoice/freeze-drift-at-measured-rev.json`, `sha256 ba232acf…`; my run:
`freeze-drift exit=1, verdict drift`). The L1's receipts are at `077e212b` (drift) and `cb4326b2`
(clean) — not at the measured revision, so the literal command in QUALITY 79 was never run.
The tool's own docstring states the coherent rule ("if this gate prints any commit between the freeze
and the measured revision, the claim is scored with the first-freeze bytes and the amendment is
reported, never adopted", `tools/round-38/freeze-drift.py:6-10`).
*Smallest safe correction:* drop "and must print zero commits" (or scope zero-drift to the last
pre-data revision, here `cb4326b2`) and state the measured-revision invocation plus its drift list
in the SCORECARD row.

**D-2 (calibration/coverage, medium) — the v1 counter accepts exactly the receipts its own predicate
sentence excludes.** The first-freeze sentence requires the after receipt to be "run with stock
unblob 26.6.4; **no external extractor dependency**". The v1 counter checks only
`operation == extract_firmware and provider.id == 'unblob'`, `gaps == []`, handler, oracle hits, and
evidence id — it never sees PATH or dependency-freedom
(`git show e059ca93:tools/round-38/c1-counter.py`, `measure()`/`matched()`). A receipt made **with**
`sasquatch-v4be` on PATH has `gaps: []` and matches; a receipt made **without** it has
`missing-extractor-dependency` and fails. The scored receipts are the former: all four landed `after.json` publish their oracle files
(5/3/4/4) with no `missing-extractor-dependency` gap, which this toolchain cannot do without
`sasquatch-v4be`, and the paired `before.json` receipts prove the dependency (K1's carries
`kind: missing-extractor-dependency, dependencies: ["sasquatch-v4be"]`; all read from
`3b960fe5:corpus/evidence/round-38/c1/K*/{after,before}.json`). So `carriers_matched 3` is the
**counter-code** reading; under the sentence's own clause the admissible receipt set is empty
(0/4, not 3/4). The verdict label is unchanged (both are a miss), but the provenance of the number
must be stated. The lesson's M38-3 records the stale premise but not that the counter actively scores
the excluded receipts.
*Smallest safe correction:* one sentence in the SCORECARD C1 row (and the report): "3 is the
first-freeze counter's reading; the first-freeze sentence additionally demands dependency-freedom,
which none of the scored receipts meets — under the sentence C1 is false, not merely short; both
readings are a miss." A later QUALITY row should require a score to quote which predicate clauses
the counter actually enforces.

**D-3 (calibration, low) — the lesson's one-line verdict is narrower than the receipt.** It says
"`carriers_matched 3`, K2 fails on one `unpublished-entry` gap"
(`corpus/lessons/round-38.md:10-13`), but the same receipt also has
`province_core_row: false` and `province_core_section: false`, so `met_target` is false for three
independent reasons. `SCORECARD.md:3405` already says "Core-row bindings false"; only the lesson
omits it.
*Smallest safe correction:* append "and the round-38 Core row/section were not landed
(`province_core_row/section` false)".

**Non-defect, for the record — the false v2 sentence stays in the frozen claims doc.** It cannot be
edited (§10), and attempt 2 marks it in the lesson and SCORECARD (§2 above). The round report at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kaidoku.md` is still a stub; it must not repeat
"No claim was scored under v1" as fact. Its likely origin is
`w1/R38ReviewerEntryQuality.md:234-236`, a wave-1 seat that missed K1 §2e and EnvelopeRules §4 — a
lesson candidate, not a rule-choice defect.

## 6. Impacted axes and what I did not test

- **Calibration**: D-1 (criterion self-contradiction), D-2 (number vs sentence provenance), D-3
  (lesson narrower than receipt). Attempt 2's rule choice itself is calibrated correctly.
- **Coverage**: D-2 changes what the C1 number means (3 counter-side vs 0 sentence-side) without
  moving the axis; no domain surface moved (honest stop, entry not promoted).
- I did **not** re-run REA (the receipt bytes exist and the counter checks their identity; no new
  measurement was needed) and did **not** re-score C2 (its counter is byte-identical at freeze and at
  the measured revision). The `frontier_note` binding of the v1 counter is known to be pre-satisfied
  at the base (`w1/R38ReviewerPredicateIdentity.md`, D1) and stays true here — vacuous evidence, not
  a defect of attempt 2 (met_target is false anyway); noted only so a closure does not read
  `frontier_note: true` as proof of the round's note.
- [INFERENCE] The EnvelopeRules 03:23 counter run may have used a v2-draft worktree binary rather
  than the frozen blob (its receipt keys are v1-shaped, so the code path was v1-shaped); the
  load-bearing evidence for "scored under v1" is the K1 frozen-bytes run, whose counter sha is
  verified here.

## 7. Bounds, scratch, tooling

- No VCS mutation; only read-only git (`log`, `show`) and one read-only `python3 freeze-drift.py`
  run. No write to `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`,
  the fleet repo or shokuknow. No REA invocation, no subagents, no background jobs, no
  `agent://all`. No tool installs.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2C1RuleChoice` used for the reproduction, the
  counter copy and its selftest fixtures; removed before yielding. Citations here are committed
  paths plus the two artifacts below.
- Artifacts: `.ufo/waves/round-38/w2/artifacts/R38W2C1RuleChoice/repro-v1-3b960fe.json`
  (`sha256 1de283e1b26f72bc0abf0b76a3052f1c35d55e5017de99e3da9abc789909bd8e`) and
  `…/freeze-drift-at-measured-rev.json`
  (`sha256 ba232acf196f44cb0446dd9e93fdb6661f00ee7366da3b9b6a9575e70a159cdb`).
