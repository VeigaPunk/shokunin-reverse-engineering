# R41W2C2Rescore — re-score of R41-C2 at the measured revision

**VERDICT: CONFIRMED (author's NOT MET and its stated cause) / DEFECTS FOUND (instrument-side).**
The frozen counter reproduces the L1 receipt exactly — exit 1, `matched 52/52`, `distinct_decisions 13`,
exactly one false binding `observed_features_match_declared` — and the stated cause is exact: the 12 `combo`
carriers publish their declared tuple under `carriers[].declared`, which the frozen read chain never consults.
The *substantive* binding intent holds on every one of the 52 carriers (my own reader: observed tuple ==
`declared` 52/52, and == `class_expected.features` on all 40 carriers that have one). The same bytes score
`met_target true`, exit 0, 29/29 bindings true once one key is added to the read chain — so round 41's NOT MET is
an artefact of a schema contradiction frozen into the tool pair, not a property of the table, the data or the
generator.

What I attacked: (a) reproducibility of the frozen C2 score at `e9a24d07`; (b) the observed feature tuple,
recomputed from the envelopes by an independent reader written from the claims' feature definitions; (c) the
honest-stop cause — is the key-name mismatch really the *only* reason, and is it on the counter side or the data
side; (d) whether any in-round repair exists; (e) whether the instrument's own calibration could have caught it;
(f) what the held-out carriers actually ran at, since the receipt's advisory depth report contradicts the run
records.

---

## 1. Reproduction of the frozen score

```
python3 -I -B <LANE>/tools/round-41/c2-counter.py --root <LANE> \
  --rev e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 \
  --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f --json-out "$S/c2.json"
```

exit **1**; stdout:

```json
{"bindings_false": ["observed_features_match_declared"], "distinct_decisions": 13, "exit_code": 1,
 "freeze": "d764389e9cbe61b9d1b07538ff3bff02d50bb34f", "matched": 52, "matched_classes": 40,
 "matched_combos": 12, "met_target": false, "met_target_consistent": true, "n": 52,
 "revision": "e9a24d07256d1606f01aa4d2d65f74e649c5f3d4"}
```

- `02-rerun-vs-frozen.txt`: my receipt vs `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json` — the **only**
  differing top-level key is `argv` (absolute vs lane-relative spelling); all other 64 keys are equal. The
  receipt's scoring half is deterministic.
- Two L1 receipts, `c2-at-042b8769.json` and `c2-at-e9a24d07.json`, differ only in `revision`, `revision_arg`,
  `argv` — the score is revision-stable across the landing commits.
- Bindings: 29 total, **28 true**, `frozen_paths_changed: []`, `manifest_first_add:
  8a1f4c73057405a4b470af11d1d351a0f03f6c34`, `instrument_*` all true, `class_map_agreement {agree: 40,
  disagree: [], missing: []}`. Real-receipt binding true: `V1,V2,L1,L2` each
  `(depth-limited, raise-depth)` from **both** the interpreter and the evaluator (`ok: true`).
- `declared_features`: `{source: "class_expected.features", missing: [C01..C12], mismatch: []}`, per-class map
  `combo: declared-tuple-incomplete`, every other class `match`.

## 2. Independent recomputation of the observed tuple

`03-indep-tuple-check.py` re-derives (H, G, D, BE, SR, P) straight from
`corpus/evidence/round-41/c2/heldout/<id>/envelope.json` using the claims' definitions (H = handler names in
`normalized_result.chunks[].handler` ∪ `extraction_gaps[].handler`, nulls dropped — no `squashfs*` filter; D =
union of gap `dependencies` by exact name; BE from recorded child argv tokens; SR from a
`MaliciousSymlinkRemoved` producer report; P = `len(files)`). It never imports the counter.

| check | result |
|---|---|
| observed tuple == `carriers[].declared` (the six bound fields) | **52 / 52**, `observed_neq_declared: {}` |
| observed tuple == `class_expected.features` (where present) | **40 / 40** carriers that carry it, `{}` |
| `declared` == `class_expected.features` (where both exist) | **0** differences |
| carriers with a `declared` key | 52 |
| combos with `class_expected.features` | **0** of 12 (`class_expected` is `null` by design) |
| handler / gap / dependency vocabulary observed | `{squashfs_v4_be, squashfs_v4_le}` / `{depth-limited, extractor-failure, missing-extractor-dependency, unpublished-entry}` / `{sasquatch, sasquatch-v4be}` |
| BE distribution | `n/a` 32, `no` 8, `yes` 12 |

`09-xengine-output.json`: my reader vs the counter's own `observed_features()` on all 52 envelopes → **0
differences** in every bound field, so the disagreement is not a feature-reading disagreement. Two immaterial
divergences from the text worth noting: the counter filters H to names starting `squashfs` (no envelope carries a
non-`squashfs` handler, so no effect) and reads BE from a wider set of `command` sites than the frozen text names
(also no effect here: 40 named carriers already matched).

## 3. The read chain that reads the declared tuple

`tools/round-41/c2-counter.py:1496-1506` (identical bytes at the freeze — `git show d764389:…`):

```python
            decl = None
            cex = c.get('class_expected')
            if isinstance(cex, dict) and isinstance(cex.get('features'), dict):
                decl = cex['features']
            elif isinstance(c.get('features'), dict):
                decl = c['features']
            elif isinstance(c.get('declared_features'), dict):
                decl = c['declared_features']
            elif decl_key:                       # manifest top-level: class_features /
                d = man[decl_key].get(c.get('class'))   # classes_features / feature_tuples /
                decl = d if isinstance(d, dict) else None  # features_by_class / class_tuples
```

`carriers[].declared` is **not** in that chain. For a combo carrier the real manifest record is
`class_expected: null`, no `features`, no `declared_features`, and none of the five top-level `decl_key`
alternatives exist (`declared_schema` is the only related key), so `decl = None` → `canon_features(None)` →
`declared-tuple-incomplete` → `feat_missing` → binding false. That is exactly the 12 IDs the receipt lists.

**The two frozen tools disagree at freeze time, and the disagreement is documented.** The counter's own
"Frozen tool interfaces" docstring (freeze lines 81-84) states the generator contract as
`carriers[] {id, class, arm, class_expected (label, action, features) or 'features', carrier, sha256}` — it never
mentions `declared`. The generator at the freeze writes, on **every** carrier,
`'declared': declared_tuple(features)` (`heldout-gen-v3.py:1372`) and additionally
`class_expected: {…, features: features}` only for named classes (`:1375-1382`), with
`'class_expected': None` for combos (`:1459-1470`). The manifest itself documents the location it chose:
`declared_schema.location = "carriers[].declared (every carrier)"`. So the data is where it says it is; the
counter's contract text and read chain are the side that is wrong. See `12-read-chain-citation.txt`.

## 4. Proof that the key name is the *only* cause

One hunk on a **scratch copy** of the frozen counter (lane untouched; `06-patched-counter.diff`):

```diff
             elif isinstance(c.get('features'), dict):
                 decl = c['features']
+            elif isinstance(c.get('declared'), dict):
+                decl = c['declared']
             elif isinstance(c.get('declared_features'), dict):
```

Run at the same root, rev and freeze (`07-c2-patched-receipt.json`):

| field | frozen counter | one-key read |
|---|---|---|
| exit_code | 1 | **0** |
| met_target | false | **true** |
| bindings_false | `[observed_features_match_declared]` | **`[]`** (29/29 true) |
| matched / n | 52 / 52 | 52 / 52 |
| `declared_features.missing` | C01…C12 | **`[]`** |
| `declared_features.by_class.combo` | declared-tuple-incomplete | **match** |
| `declared_features.mismatch` | `[]` | `[]` |
| distinct_decisions | 13 | 13 |

Nothing else changed: same data, same revision, same evaluator, same table. No second defect hides behind the
first — if a combo tuple genuinely mismatched its envelope, `feat_bad` would be non-empty once the key is read,
and it is empty.

## 5. No in-round repair exists (so the honest stop stands)

Repairing on the data side (adding `class_expected.features` to the 12 combos, in a `--shared` clone, commit
`c90eadd3…` on top of the clone's HEAD, identity `-c user.name=fx -c user.email=fx@fx`) makes the frozen counter
refuse the score:

```
{"exit_code": 2, "frozen_paths_changed": ["corpus/evidence/round-41/c2/heldout"],
 "unevaluable": "frozen_path_changed", "revision": "c90eadd3fccc…"}
```

`FROZEN_PATHS = (CLAIMS, 'tools/round-41', MANIFEST_DIR)` (`c2-counter.py:115`) covers both sides of the fix.
Round 41 therefore cannot score C2 met no matter who is at fault; the repair belongs to a round-42 refreeze.

## 6. Calibration: why the instrument could not see this

- `08-selftest.txt`: `cases=70 pass=70 fail=0` — the instrument reports itself fully calibrated, and the suite
  contains red cases named for exactly this binding (`feat_mismatch`, `feat_absent`, `feat_env`,
  `combo_feat_mismatch`).
- But the selftest's stub generator emits its **combos as `'class_expected': None, 'features': dict(FEATURES)`**
  (`c2-counter.py:1717-1719`) — a record shape the frozen generator never writes — and the `combo_feat_mismatch`
  mutation edits `entry['features']['gap_kinds']` (`:2131-2132`). The fixture therefore validates the read chain
  against a shape that matches the counter's contract text and *not* the frozen generator. Every green case is
  green for a manifest that could not occur.
- Consequence for the landing: a green self-test is not evidence that the counter and the generator agree on the
  record schema. This is the class of defect the C2 instrument bindings (`classes_two_each`,
  `combo_family_wellformed`, …) do not cover: they check set shape, not the declared-tuple location.

## 7. Secondary defect (reported, not bound): the advisory REA-parameter block is blind

`advisory_rea_params` in the frozen receipt is meaningless — `per_class_max_depth` all `null`,
`depth_classes_at_depth1: []`, `depth_classes_missing: [depth-limited-alone, depth-limited-in-tree,
depth-limited-mixed]`, i.e. it claims the three depth classes were *not* run at depth 1. Cause: the counter reads
`man.get('rea_params')` (`:1459`) and falls back to `c.get('max_depth')` (`:1471`), while the real manifest
carries `rea.per_class` / `rea.default_max_depth` and per-carrier `rea.max_depth`. The binding is `False` by
design ("advisory"), so it does not affect the score — but the receipt's own evidence section contradicts the run
records. Verified independently from `run.json` (`10-depth-check-output.json`):

- 52/52 carriers `exit_code 0` (real REA 6.5.0 runs, not stubs);
- 15 carriers at `--max-depth 1`, 35 at `3`, 2 without (`out-of-domain`), recorded `max_depth` vs argv:
  **0 disagreements**;
- all 8 depth-class carriers (`H31-H36, H39, H40`) at depth 1; combos split 7 at depth 1 / 5 at depth 3;
- the manifest's own `rea.per_class` matches those runs class by class.

A reviewer reading only the receipt's advisory block would understate depth coverage. Recommend the same fix
(`rea` / `rea.max_depth`) ride the round-42 refreeze.

## 8. Is `declared` predictive or post-hoc? (predictive)

- Combos: `declared = combo_declared(factors)` where `factors` are the five seeded rng draws
  (`endian, in_tree, escaping, partial, comp, max_depth`); the function is pure over those draws
  (`heldout-gen-v3.py:411-440`) — it cannot see an envelope.
- Named classes: `features = expected_features(name, endian)` from the static `EXPECTATIONS` table
  (`heldout-gen-v3.py:1348`, table at `:456`), declared before any run.
- Ordering: `manifest.json` is written at `:1837`, the REA loop runs at `:2102` in the same invocation, and the
  binding `manifest_before_envelopes` is true.
- Therefore `observed == declared` on 52/52 (including mixed sets such as `C06 = {depth-limited,
  extractor-failure, unpublished-entry}` and the 3 BE-damaged / 3 LE-damaged combos) is a genuine prediction
  result, and it is the depth evidence the exit-1 receipt hides.

## 9. Disposition

- The author's **NOT MET** stands: the frozen bytes are the claim's rule, the counter exits 1, `met_target`
  false and `met_target_consistent` true. No score is re-minted and round 41 cannot be repaired in place (§5).
- But the failure is **not** the table's, the evaluator's, the generator's or the evidence's. It is the frozen
  `c2-counter.py` read chain (instrument), with a matching fixture blind spot (§6) and a second schema drift in
  its advisory block (§7). Round 42 should refreeze C2 with: (i) `declared` in the read chain, (ii) the selftest
  stub generator emitting the real record shape (`declared`, `class_expected: null` for combos, `rea.max_depth`),
  (iii) the advisory block reading `rea`. Hunk (i) is proven sufficient for the score by §4.
- [INFERENCE] Residual risk unchanged by this re-score: table and evaluator are two renderings by the same
  author group from one precedence text, so a shared misreading of REA's envelope would not be caught; the claim
  says so itself. Also, all 52 envelopes are lane-built synthetic carriers; C2 claims nothing about vendor bytes.
  `carriers_regenerated` true is the counter's own byte-identity check — I did not regenerate the carriers myself.

## 10. Bounds compliance

Read-only in the lane: `tools/round-41/*`, `corpus/evidence/round-41/c2/heldout/*`, the L1 receipts under
`.ufo/waves/round-41/l1/`, `plans/round-41-claims.md`. Wrote only `../R41W2C2Rescore.md` and
`artifacts/R41W2C2Rescore/`. VCS: `show`/`log`/`rev-parse` only in the lane; the single `commit` was inside a
throwaway `--shared` clone under scratch whose `rev-parse --show-toplevel` was asserted first, with `-c
user.name=fx -c user.email=fx@fx`. No tool installs or upgrades. Scratch removed; artifacts carry sha256s and
rebuild commands (no vendor bytes anywhere in C2).

Artifacts: `artifacts/R41W2C2Rescore/INDEX.md` (hash list) and the 14 files it indexes.
