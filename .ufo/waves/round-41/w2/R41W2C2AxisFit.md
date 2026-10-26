# R41W2C2AxisFit — axis/verdict attack on R41-C2 (godspeed seat)

**Verdict: DEFECTS FOUND** — I attacked the R41-C2 verdict (honest stop, depth-if-met, residual quality). The author's `NOT MET` stop is **correct under the frozen rule** (no rule changed after scoring; the failing binding is frozen; exit 1 is faithful), **but the specific failing binding is a scorer/manifest key blind spot, not a data failure**: every one of the 52 held-out envelopes' observed feature tuple equals the tuple its manifest declares (`carriers[].declared`; 0 missing, 0 mismatches, independently recomputed), while the frozen counter never reads that key and only looks in `class_expected.features` / `features` / `declared_features` (all null on the 12 combo carriers). Had the counter read the manifest's own documented declaration location, the claim would have met its target (52/52, every other binding true). Depth-if-met is thin (1 of 13 decisions new; evaluator from the same precedence text) but honestly bounded by the claim itself; the SKILL v3 table + prose repairs stand as quality work regardless.

---

## What I attacked

The three axes in the seat spec: (1) is the author's honest stop correct under the frozen rule (the prompt: a rule changed after scoring is not the claim's rule)? (2) would the claim be depth even if met — 13 pairs, 1 new, contains-form, evaluator from the same text (`w1/R41CritC2Draft.md`)? (3) what part of the SKILL change stands as quality work regardless?

## Axis 1 — the honest stop under the frozen rule

### 1a. The failing binding is part of the frozen rule (no post-scoring rule change)

- The frozen claims at the freeze commit state `observed_features_match_declared` verbatim:
  `git show d764389e9cbe61b9d1b07538ff3bff02d50bb34f:plans/round-41-claims.md` line 140:
  "every envelope's observed feature tuple equals the tuple its manifest declares (`observed_features_match_declared`);".
- The freeze commit is `d764389e` ("round-41: freeze — claims R41-C1 … R41-C2 (triage table v3 vs independent evaluator), tools, carriers, controls, …"); the binding was added as a wave-1 change *from the draft* (`## Changes from the draft`: "C2 bindings: `class_expected` is reported, not scored; `observed_features_match_declared` and the real-receipt binding were added (`w1/R41CritC2Draft.md` §3, §8)"), i.e. it predates scoring. No rule was changed after scoring.
- Freeze integrity holds at the measured revision: `frozen_paths_changed: []`, `generator_sha_matches_freeze: true`, `v3_block_identical: true`, `manifest_first_add: 8a1f4c7305…` (after freeze). The counter is a frozen path; the author could not have patched it without breaking freeze-integrity.

### 1b. The counter's failure is a schema blind spot, not a data failure

Counter code (`tools/round-41/c2-counter.py`, lines 1480–1505) reads declared tuples only from:

- `c['class_expected']['features']` (dict),
- `c['features']` (dict),
- `c['declared_features']` (dict),
- manifest-level `class_features` / `classes_features` / `feature_tuples` / `features_by_class` / `class_tuples`.

It never reads `c['declared']`. The generator (`heldout-gen-v3.py`) writes the six-field binding tuple to exactly that key for **every** carrier (lines 1372, 1410, 1464; selftest asserts `set(DECLARED_FIELDS) == set(c['declared'])` for all entries, line 1993), and writes `class_expected: null` for the 12 combo carriers (lines 1469, 1475; selftest line 1998 "named carriers keep a reported class_expected; combos null"). The manifest itself documents the location: `declared_schema.location = "carriers[].declared (every carrier); declared_extras carries extraction_failed and max_depth, which are NOT part of the binding"`.

Independent recomputation (probe `probe-observed-vs-declared.txt`, artifact; mirrors the counter's canonicalization of the six required fields `handler_set, gap_kinds, gap_dependencies, be_argv, symlink_removed, published`):

```
carriers checked: 52 missing: 0 []
mismatches: 0
```

So the substantive predicate clause "every envelope's observed feature tuple equals the tuple its manifest declares" **holds on the actual data**. The `observed_features_match_declared=false` result is produced solely because the counter looks in places that are null for combos. This is a defect in the frozen scorer (it never learned the manifest's own declaration key), not in the landing.

### 1c. Verdict on axis 1

The honest stop is **correct as scored**: under the frozen rule, the counter is the arbiter ("the rule for each claim is the bytes of this file, its tools and its frozen inputs in the commit that first adds this version"), it exits 1 with `met_target=false`, and the author reported it faithfully instead of papering over it. Reproduced: `c2-counter.py --root <lanE> --rev e9a24d07… --freeze d764389e…` → `exit=1`, `{"bindings_false": ["observed_features_match_declared"], "matched": 52, "n": 52, "met_target": false, "distinct_decisions": 13}` (identical to committed score at `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`; also identical at the intermediate `042b8769` revision).

However, the stop is **substantively a false negative**: the specific failure is a counter/manifest key mismatch, not a data mismatch. A corrected reader (reading `carriers[].declared`) would find the clause satisfied and the claim met 52/52 with every other binding true (real-receipt binding true, 4/4 round-40 C1 receipts → `depth-limited`/`raise-depth`). "NOT MET" is therefore *correct-but-shallow*: it reflects a scorer defect, not a landing defect. This distinction should be recorded in the round's calibration: the author's explanation of the cause is accurate (they correctly diagnosed that the declared tuples sit under `declared` while the counter reads `class_expected.features`/`features`/`declared_features`); what is missing is the recognition that the *data* satisfies the predicate, so the failure is tooling.

## Axis 2 — would the claim be depth even if met?

Even if the binding had passed, the depth increment is **thin but real, and honestly bounded**:

- **13 decisions, 1 new**: `new_labels = ["depth-limited"]` (manifest), `distinct_decisions = 13`, `distinct_rows = 12` (+ `unclassified`). 12 of 13 pairs existed in v2's vocabulary. The depth-limited/raise-depth row is the only decision exercised against real firmware bytes — the four committed round-40 C1 receipts, which frozen v2 labeled `unclassified`/`none` (4/4) and v3 labels `depth-limited`/`raise-depth` (4/4, binding true).
- **Contains-form and pinned cells carry the rest of the delta**: control scores (`.ufo/waves/round-41/controls/c2/dev-scores-prefreeze.json`) — v2-verbatim 34/52 vs v3 52/52; no-contains (CTL-C2-4) 38/52, so ~14 envelopes depend on the contains-form precedence (step 4/7 fire regardless of accompanying link gaps); depth-row-only (CTL-C2-6) 42/52; lookup (CTL-C2-7) 44/52 < 52, so the anti-lookup design works (dev seed likewise puts 6/12 combos outside the named tuples).
- **Evaluator from the same text**: `indep-eval-v3.py` is written from the `**Label precedence**` list in the same claims file (header: "the twelve steps, verbatim in PRECEDENCE below"), reading only REA envelope structure. It never reads the table/interpreter/generator — so independence is *implementation*-level, not *judgment*-level. The metric validates that the table transcribes the precedence, not that the precedence is good triage; the claim itself says exactly this ("it does not measure whether the precedence itself is the best triage").
- **Corpus mostly synthetic**: 48 of 52 envelopes are generator-built; the four real receipts all land on the one new row.

Verdict: if met, the claim would be defensible as **modest depth** (one new decision class validated on real firmware, contains-form robustness, anti-lookup controls) but it is closer to engineering-consistency than to a deep new capability. The claim's honest-partition paragraph (line 155) discloses all of this, so no overclaim occurs; the round should credit C2 as quality work, not as a large depth gain.

## Axis 3 — what stands as quality work regardless of the metric

- **The v3 table itself** (`SKILL.md` block 20, `<!-- sqfs-triage-table v3 -->`, lines 434–453): 13 rows, per-row cause + action + source chains (S112, S118–S124, S119, knowledge docs), byte-identical freeze→rev (9,659 bytes both).
- **Precedence text**: resolves the 17 ambiguities of `w1/artifacts/R41C2Eval/precedence-ambiguities.md` (H/D/BE/SR/P definitions, step-3 else branch, step-5 failing-chunk handler, an action per clause, supersession sentence in block 19).
- **Prose repairs riding the block** (unscored): R40-CL5 M1–M3, L1–L6, R40-CL4 partial-recipe pinning (damaged-block compressed length).
- **Controls and discipline**: eight controls + dev scores committed pre-freeze, kill-rule framing, real-receipt control, and the honest stop itself — the author diagnosed and reported the counter blind spot rather than rewriting the frozen counter or silently claiming MET.

## Tooling / installs

No tools installed or upgraded (Python 3 stdlib only; probe mirrors the frozen counter's canonicalization). No git mutation; read-only `git show` only. Scratch `/fast/scratch/hyaku/kaidoku-r41/R41W2C2AxisFit` created, used, and removed; artifacts copied to `.ufo/waves/round-41/w2/artifacts/R41W2C2AxisFit/` (`probe_features.py`, `probe-observed-vs-declared.txt`, `c2-counter-repro-summary.json`).

## Files / evidence

- `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json` (+ `.stdout`) — committed score: exit 1, `declared_features.source = "class_expected.features"`, `missing = [C01..C12]`, `by_class.combo = "declared-tuple-incomplete"`, matched 52/52, real receipts 4/4.
- `plans/round-41-claims.md` lines 140, 155, 200 — frozen binding text and honest partition.
- `tools/round-41/c2-counter.py` lines 1480–1505 (key reading), 576–680 (`observed_features`/`canon_features`).
- `tools/round-41/heldout-gen-v3.py` lines 1370–1475, 1807–1826, 1993–1998 (declared tuple per carrier, `declared_schema.location`, selftest).
- `corpus/evidence/round-41/c2/heldout/manifest.json` — `declared_schema`, `new_labels = ["depth-limited"]`, `classes` (21), `carriers` (52).
- `w1/R41CritC2Draft.md` §3b (the binding's origin: replace pair-only `class_expected` with observed-feature-set binding) and §8.
- `.ufo/waves/round-41/controls/c2/dev-scores-prefreeze.json` — control scores.
- `git log d764389e..e9a24d07` — five commits, no frozen-path change; `frozen_paths_changed: []`.

## Limits / inference

- [INFERENCE] "Had the counter read `carriers[].declared`, the claim would have met its target" — counterfactual, grounded directly in the code reading plus the recomputation (52/52 observed==declared, all other bindings true); not executed as a modified counter (a modified counter would violate freeze-integrity).
- I did not re-run REA/unblob; all envelope evidence is from the committed held-out envelopes and receipts.
