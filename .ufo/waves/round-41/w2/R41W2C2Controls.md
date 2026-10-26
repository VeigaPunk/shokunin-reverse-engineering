# R41W2C2Controls — C2 controls re-scored on the held-out set

**Verdict: CONFIRMED (no falsification of C2's discrimination).** Attacked: the claim's kill-rule
guarantee — that the eight C2 controls are genuinely beaten by the v3 table and that the dev scores in
`plans/round-41-claims.md` were not carrying the discrimination. Every control was re-scored on the
**held-out** envelopes, not dev; none reaches 52/52, the best non-precedence table loses 10 pairs, and
all eight score at or below their dev values. The claim's own NOT-MET binding
(`observed_features_match_declared`) is reproduced independently and traced to a counter-side key gap,
not to the data.

## 1. Required measurement (held-out vs dev, same tool, same envelopes)

Command (seat's spec; exit 0, `kill_rule_fires False`):

```
python3 -I -B tools/round-41/c2-controls.py --root <LANE> \
  --dev corpus/evidence/round-41/c2/heldout --out "$S/ctl" \
  --json-out "$S/scores-heldout.json" --build
```

`--build` wrote into the scratch copy only; the rebuilt `CTL-C2-3`, `CTL-C2-5` and `CTL-C2-7` are
**byte-identical** to the committed files (`sha256 2ab3e8ae…`, `73c9d5f9…`, `14e4a896…`, verified with
`cmp`), so the rebuild added no held-out-derived rows.

| table | held-out matched/52 | dev matched/52 | delta | interp exit (held-out) |
|---|---|---|---|---|
| **SKILL.md v3 (the claim's table)** | **52** | **52** | 0 | 0 |
| CTL-C2-0 base SKILL | 0 | 0 | 0 | 2 (no v3 marker) |
| CTL-C2-1 catch-all | 4 | 4 | 0 | 0 |
| CTL-C2-2 v2 verbatim | 30 | 34 | −4 | 0 |
| CTL-C2-3 actions rotated | 2 | 2 | 0 | 0 |
| CTL-C2-4 no contains form | 35 | 38 | −3 | 0 |
| CTL-C2-5 `*` gap kinds in partial row | 30 | 31 | −1 | 0 |
| CTL-C2-6 v2 + depth row only | 40 | 42 | −2 | 0 |
| CTL-C2-7 lookup (declared tuples) | 42 | 44 | −2 | 0 |

- Held-out is **not weaker** than dev for any control: six lose 1–4 pairs, two are unchanged.
  The largest held-out score is 42/52 (`CTL-C2-7`), i.e. a 10-pair margin below the table — the
  answer to the seat's question is no, no control reaches 52/52 on the held-out set.
- Dev column reproduces `.ufo/waves/round-41/controls/c2/dev-scores-prefreeze.json` exactly
  (0, 4, 34, 2, 38, 31, 42, 44 and SKILL 52), re-run by this seat rather than quoted.
- Determinism: a second invocation without `--build` into a fresh out dir gave identical
  `(matched, exit)` for all nine tables.
- Miss structure on held-out (missed carriers by family): CTL-2 10 combo / 12 named; CTL-4 7/10;
  CTL-5 6/16; CTL-6 6/6; CTL-7 4/6. No control is held up by a single class family.

## 2. Extra attacks that succeeded in strengthening (not weakening) the claim

**(a) Every v3 row is individually load-bearing.** Flipped the action cell of each of the 12 rows in a
scratch copy of `SKILL.md`, scored with the frozen interpreter over the 52 held-out envelopes keyed by
envelope path:

```
no-squashfs-chunk 50/52 (2 wrong) | dep-missing-be 50 (2) | dep-missing-le 50 (2)
partial-body-failure 38 (14) | avm-marker-be-dropped 50 (2) | body-extractor-failure 48 (4)
depth-limited 42 (10) | mixed-symlinks 49 (3) | escaping-symlink-removed 50 (2)
in-tree-symlink-metadata 49 (3) | clean 48 (4) | clean-empty 50 (2)
```

Each flip breaks exactly the carriers carrying that row's label and **nothing else** (`elsewhere=0`
for all 12). 50 of the 52 envelopes are attributed to a row; the remaining 2 are the `unclassified`
fall-through (step 12). This rules out "one row does the work and the rest are inert".

**(b) Label uniqueness structurally caps lookup controls.** The interpreter refuses duplicate labels
(run unevaluable, exit 2), so a table can carry at most one row per decision — 13 pairs exist on the
held-out set (`partial-body-failure` 14, `depth-limited` 10, `clean` 4, `body-extractor-failure` 4,
`in-tree-symlink-metadata` 3, `mixed-symlinks` 3, then six labels ×2). A tuple-enumerating memoriser
cannot be expressed in this format at all; `CTL-C2-7` (12 rows, 3 `*` cells) is the strongest legal
approximation and still loses 10. [INFERENCE] this is why the lookup control saturates near 42 rather
than 52.

**(c) Held-out independence is 31 tuples / 13 decisions, not 52.** Observed feature tuples (the counter's
7-key observation) collapse to **31 distinct tuples over 52 envelopes**; 17 tuples are shared by two
carriers. One tuple is shared by four: `H23`/`H24` → (`no-squashfs-chunk`, `inspect-input`) and
`H25`/`H26` → (`unclassified`, `none`). Those four envelopes carry identical H/G/D/BE/SR/P but differ in
`operation`/`provider` (`extract_firmware`/`unblob` vs `inspect_firmware_regions`/`binwalk`).

**[INFERENCE] Consequences (limits, not defects):** (i) the declared-tuple binding
`observed_features_match_declared` cannot adjudicate precedence step 1, because the claim's own
`FEATURE_KEYS`/`REQUIRED_FEATURES` omit OP/PV — the two domains are indistinguishable at tuple level;
(ii) a per-envelope 52/52 overstates statistical independence (2 replicates per class), so the honest
unit is 13 (label, action) pairs on 31 distinct observable tuples.

## 3. The claim's NOT-MET binding, reproduced and localised

`c2-counter.py` at the measured revision (`--rev e9a24d07…`, `--freeze d764389e…`) exits **1** with
`matched 52`, `distinct_decisions 13`, `matched_classes 40`, `matched_combos 12`,
`bindings_false ["observed_features_match_declared"]` — exactly the claim's honest stop. Every other
binding in the receipt is true (27 of 28). The 12 `missing` ids are precisely `C01…C12`, and:

- carrier declaration location: **40 named carriers under `class_expected.features`, 12 combos under
  top-level `declared`** — the same split on the dev seed;
- the counter resolves declared features only from `class_expected.features` → `features` →
  `declared_features` (`c2-counter.py:1497-1503`), so all 12 combos resolve to nothing;
- when `declared` is used, the 12 combos match observed on the 6 required features **12/12 on both
  seeds** (`combo-declared-key-check.json`).

So the C2 depth claim's NOT MET is a **key-resolution gap in the frozen counter**, and the underlying
held-out data is consistent with its declarations. Pair-level depth (52/52, 13 distinct decisions, four
real round-40 receipts bound `depth-limited`) is intact; only that one binding fails.

## 4. Chronology / integrity evidence (read-only git)

- Controls and `dev-scores-prefreeze.json` were first added **in the freeze commit**
  `d764389e` (2026-10-26 18:08:13); the held-out manifest was first added in `8a1f4c73`
  (18:12:47) and `git merge-base --is-ancestor d764389e 8a1f4c73` holds. Controls before data.
- No commit in `d764389e..e9a24d07` touches a frozen C2 path, and `git diff e9a24d07 HEAD -- SKILL.md
  tools/round-41 corpus/evidence/round-41/c2 plans/round-41-claims.md` is empty — the bytes this seat
  scored are the measured revision's bytes (`SKILL.md` sha256 `94d13b44…`, `sqfs-triage-v3.py`
  `6ad2b4e1…`, `indep-eval-v3.py` `26178d71…`).
- Held-out carrier integrity: all 52 `carrier.sqsh` files hash to their manifest `sha256` (0 mismatches).
- Evaluator/tables agree per envelope keyed by path (52/52), independent of the controls runner's
  `zip()` — this seat re-derived expected pairs from `eval-heldout.json` and scored the interpreter
  directly.

## 5. Report of work / limits

- Files written: this report and `.ufo/waves/round-41/w2/artifacts/R41W2C2Controls/` only
  (`heldout-control-scores.json`, `heldout-control-scores-rerun.json`,
  `dev-control-scores-reproduced.json`, `eval-heldout-labels.json`, `row-perturbation-heldout.json`,
  `c2-counter-at-e9a24d07.json`, `c2-counter-stdout.log`, `combo-declared-key-check.json`,
  `CTL-C2-7-lookup-rebuilt-from-heldout-manifest.md`, `commands.txt`). The lane's `SKILL.md`, tools,
  controls, evidence and plans were never modified (`git status --porcelain` on those paths empty);
  no VCS mutation; scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41W2C2Controls` removed before yield.
- No tool install/upgrade (Python 3.14.8, stdlib only); no REA/unblob run was needed for this seat —
  the envelopes are committed evidence, and the counter re-derives features with its own port.
- No subagent/labrat dispatch, no background jobs.
- Not covered by this re-score: whether the precedence text is the *best* triage (the claim discloses
  this), and whether the interpreter honours `--max-depth` semantics; scoring here is table-vs-evaluator
  discrimination on committed envelopes.
- Residual risk: the control set is bounded above by `CTL-C2-7` at 42/52 (10-pair margin). A future
  table edit that only re-labels the six 2-carrier classes could move several pairs per row; the
  margin is comfortable but not enormous.
