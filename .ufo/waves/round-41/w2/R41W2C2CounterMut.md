# R41W2C2CounterMut — mutation sweep of the R41-C2 counter (`tools/round-41/c2-counter.py`)

**Verdict: DEFECTS FOUND.** The C2 NOT-MET verdict is not robust: a one-line mutant that reads the held-out
manifest's *documented* declaration location (`carriers[].declared`) flips R41-C2 from NOT MET to **MET**
(exit 0, 52/52, every binding true) while the counter's own 70-case selftest passes unchanged — a survivor.
Nine further selftest-blind survivors mark untested binding branches. 29 single-point mutants run; 19 killed.

**Attacked:** the frozen C2 counter at `tools/round-41/c2-counter.py`
(sha256 `c6c1ea64f07884a3b160a7e52268d295d54c8ef3bc2005704d5fae3398720af8`), binding areas named in the tasking:
evaluator comparison, `observed_features_match_declared`, `real_receipts`, `seed==freeze`, manifest first-add,
table bytes, frozen-path drift — plus `ids_unique`/`decisions_reported`/`envelopes_valid`/regeneration checks.
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; freeze `d764389e9cbe61b9d1b07538ff3bff02d50bb34f`;
measured revision `e9a24d07256d1606f01aa4d2d65f74e649c5f3d4`.

## Detector (bounded, identical on pristine / mutated / restored bytes)

- **D1 — selftest:** `HYAKU_SCRATCH=<S>/hs TMPDIR=<S> python3 -I -B <counter> --selftest`
- **D2 — real score:** `HYAKU_SCRATCH=<S>/hs TMPDIR=<S> python3 -I -B <counter> --root <LANE> --rev e9a24d07… --freeze d764389e… --json-out <receipt>`

`<S>` = `/fast/scratch/hyaku/kaidoku-r41/R41W2C2CounterMut` (seat scratch; removed at the end). Mutants are
scratch copies (`<S>/muts/<id>.py`) produced by `driver.py` (artifact), which asserts each patch matches exactly
once. The lane tree was **never modified**: the counter only issues read-only `git -C <LANE>` commands
(show/log/ls-tree/merge-base/rev-parse/cat-file), so no sandbox clone or fixture commit was needed; every probe
pins `--rev`, so the tip moving during the sweep (7a24ff74… → 74064474…, other seats' commits) does not affect
any result.

## Baseline (pristine)

- D1: `{"selftest": "c2-counter r41 (v3)", "cases": 70, "green": 20, "red": 50, "pass": 70, "fail": 0, "failures": []}`, exit 0, 35 s.
- D2: exit 1; `matched 52/52 (matched_classes 40, matched_combos 12), distinct_decisions 13, met_target false, met_target_consistent true, bindings_false ["observed_features_match_declared"]`; 1.2 s; receipt 93 537 B, sha256 `1a67ac540061fc87751f77e498dc7f740279c7d27b2ed16c7d315052bca49a88` (artifact `BASELINE.receipt.json`).
- Reproduces the L1 receipt `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json` field-for-field.

## Headline survivor M05 — the asked-for `declared` mutant

**Mutation (one point, counter lines 1497–1506).** The declared-tuple lookup chain is
`class_expected.features` → `features` → `declared_features` → manifest-level map (`class_features`,
`classes_features`, `feature_tuples`, `features_by_class`, `class_tuples`). `declared` is never read anywhere in
the file. M05 inserts one branch before the `elif decl_key:` fall-through:

```python
elif isinstance(c.get('declared'), dict):
    decl = c['declared']
```

Mutant sha256 `897cc8b35394b8bf61e18e98fd9cb4b07bfff0e773630fef4e1f41332569bdde`.

**Why it bites.** The held-out manifest itself declares the schema
(`corpus/evidence/round-41/c2/heldout/manifest.json`, key `declared_schema`):

> `"binding": "observed_features_match_declared", "location": "carriers[].declared (every carrier); declared_extras carries extraction_failed and max_depth, which are NOT part of the binding"`

All 52 carriers carry tuples at `carriers[].declared`; the 12 `combo` carriers additionally have
`class_expected: null` and no `features` key, so the frozen counter finds no tuple for them →
`declared_features.missing = [C01..C12]`, `by_class.combo = "declared-tuple-incomplete"`, `mismatch = []` —
the binding fails on **lookup**, not on disagreement.

**D2 on the mutant (real score at e9a24d07):** **exit 0, `met_target: true`, matched 52/52 (40+12),
`bindings_false: []`**, `declared_features` missing 0 / mismatch 0, `by_class.combo = "match"`,
`distinct_decisions 13` (unchanged). Receipt sha256 `0d5f577723bc299e7f7568b0ba1fc44780e0785d916c9c795d47b1c8735b58c1`
(artifact `M05.receipt.json`). **The claim flips to MET.**

**D1 on the mutant:** **70/70 pass, exit 0** — byte-for-byte the pristine selftest result. No fixture ever emits
a `declared` key: the stub generator and all feature-mismatch fixtures declare tuples only via
`class_expected.features` (counter lines 1704–1705, 2122–2140) or `features` (1718, 2128). The selftest cannot
notice this class of counter change.

**Independent corroboration (no mutant involved).** Manual recomputation of C01's observed
(H, G, D, BE, SR, P) from `corpus/evidence/round-41/c2/heldout/C01/envelope.json` at e9a24d07:
`{handler_set: ["squashfs_v4_be"], gap_kinds: ["extractor-failure", "unpublished-entry"], gap_dependencies: [], be_argv: "yes", symlink_removed: true, published: "nonzero"}` —
exactly equal to C01's `declared` tuple. (The envelope records one sasquatch child argv,
`sasquatch-v4be -be -no-exit-code …`, hence `be_argv: "yes"`.) The flip reflects the data at the documented
location, not a mutant artifact.

**Restore discipline (mutate → detect → restore, artifact `restore-demo.json`).** Scratch copy mutated → D2
exit 0/MET; exact pristine bytes written back (sha256 `c6c1ea64…` verified equal to the lane file) → D2 exit 1/
NOT-MET, `bindings_false ["observed_features_match_declared"]` — the baseline result returns. Lane file sha256
identical before and after the whole sweep; `git status --porcelain -- tools/round-41/c2-counter.py
plans/round-41-claims.md SKILL.md corpus/evidence/round-41/c2/heldout` empty.

**Consequence (finding, not a verdict change by me).** The C2 "honest stop" rests entirely on where the counter
looks for declared tuples. Three one-line mutants flip C2 to MET: **M05** (read the documented location —
selftest-blind), **M06** (force the binding true — selftest-killed 62/70), **M07** (drop the missing-half of the
conjunction — selftest-killed 68/70). The most data-faithful of the three is precisely the one the selftest
cannot defend against. Whether C2 is MET is L1's call; what is falsified is the instrument-robustness of the
NOT-MET verdict. [INFERENCE] Two readings, both defects: (a) the counter should read the location its own input
manifest documents → C2 likely MET; (b) the manifest should have declared under a key the frozen counter reads
→ NOT MET stands but for fixable packaging. The frozen predicate text says "the tuple its manifest declares"
without pinning a key; the lookup chain is an implementation choice frozen at d764389e.

## Full results — 29 mutants

| id | area | mutation (one point) | selftest | real @ e9a24d07 | classification |
|----|------|----------------------|----------|-----------------|----------------|
| M05 | observed_features_match_declared | lookup chain + `declared` key | 70/70 pass (blind) | **exit 0, MET, 52/52, bindings []** | **survivor, verdict-flipping** |
| M06 | 〃 | binding := True | 62/70 killed | exit 0, MET | killed, flips |
| M07 | 〃 | drop missing-half of conjunction | 68/70 killed | exit 0, MET | killed, flips |
| M08 | 〃 | skip feature mismatch for combos | 68/70 killed | exit 1 unchanged | killed |
| M01 | evaluator comparison | `evaluator_covers_all` := True | 69/70 killed | exit 1 unchanged | killed |
| M28 | 〃 | `evaluator_covers_all` := bool(exp) | 69/70 killed | exit 1 unchanged | killed |
| M02 | 〃 | pair match ignores action | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M03 | 〃 | pair match ignores label | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M11 | real_receipts | drop `REAL_LABEL` check | 68/70 killed | exit 1 unchanged | killed |
| M12 | 〃 | ignore evaluator on real receipts | 68/70 killed | exit 1 unchanged | killed |
| M13 | 〃 | ignore missing receipts | 68/70 killed | exit 1 unchanged | killed |
| M30 | 〃 | receipt list drops L2 | 69/70 killed | exit 1 unchanged | killed |
| M14 | seed==freeze | compare first 8 hex chars | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M15 | 〃 | `regenerated_seed_matches_freeze` := True | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M16 | manifest first-add | drop `ma != freeze` | 69/70 killed | exit 1 unchanged | killed |
| M17 | 〃 | drop `is_ancestor(ma → envelope)` | 68/70 killed | exit 1 unchanged | killed |
| M35 | 〃 | anchor envelope first-adds at freeze | 68/70 killed | exit 1 unchanged | killed |
| M18 | table bytes | `v3_block_identical` drops byte equality | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M19 | 〃 | block-drift scans newest commit only | 69/70 killed | exit 1 unchanged | killed |
| M20 | frozen-path drift | creations (`A`) count as touches | 19/70 killed | exit 2 `frozen_path_changed` | killed |
| M21 | 〃 | deletions (`D`) ignored | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M22 | 〃 | CLAIMS unfrozen | 69/70 killed | exit 1 unchanged | killed |
| M23 | 〃 | writer scope empty | 66/70 killed | exit 1, +`writer_matches_manifest` false | killed |
| M37 | ids_unique | := True | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M40 | decisions_reported | drop NOMATCH_PAIR escape | 49/70 killed | exit 1 unchanged | killed |
| M45 | envelopes_valid | drop subject-digest check | 66/70 killed | exit 1 unchanged | killed |
| M46 | carriers_committed | pin vs regen sha | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M47 | carriers_regenerated | drop class/arm equality | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M32 | envelope unwrap | no `ok/data` unwrap | 69/70 killed | exit 1 unchanged | killed |

Tally: 29 mutants, 19 killed by the selftest, **10 selftest-blind survivors**
(M02 M03 M05 M14 M15 M18 M21 M37 M46 M47); of the survivors only **M05** changes the real verdict.
M06/M07 also flip the real verdict but are selftest-killed (the binding is load-bearing either way).

Killing cases (examples, from the selftest failure records): M01/M28 ← "red: evaluator omits one envelope";
M06 ← "red: a class declares a tuple the envelope does not carry"; M07 ← "red: a class declares no tuple";
M08 ← "red: a combo carrier declares the wrong tuple"; M11 ← "red: a real receipt is labelled otherwise";
M12 ← "red: the evaluator disagrees on a real receipt"; M13 ← "red: a real receipt is missing";
M16 ← "red: manifest added before the freeze"; M17/M35 ← "red: envelopes before manifest";
M19 ← "frozen: v3 block mutated then restored"; M20 ← every green case (exit 2 instead of 0);
M22 ← "frozen: claims edited after freeze"; M23 ← "green: writer declared and present at the freeze";
M32 ← "green: full CLI envelope ok/data/meta"; M45 ← "red: subject digest mismatch".

## Survivor notes (each = a branch no selftest fixture exercises)

- **M05** — the declared-tuple lookup location (headline above). The dangerous one: selftest-blind *and* verdict-flipping.
- **M02/M03** — the (label, action) pair comparison has no direct selftest guard on either half: the
  evaluator-disagreement cases are caught only indirectly, because a flipped half makes one expected pair share
  a table row with another pair and trips `row_decisions_consistent`. A mutant breaking both the pair comparison
  and that check would slip through; the halves are never tested directly.
- **M14** — seed equality untested below full-string granularity (an 8-hex-char colliding seed passes).
- **M15** — `regenerated_seed_matches_freeze` has no isolating fixture: the `seed != freeze` case flips both seed
  bindings at once, so this one is never the detected failure.
- **M18** — `v3_block_identical`'s byte-equality conjunct is never the failing check in any case (its False
  branch is reachable only via the absent-block case); block mutation is guarded by the exit-2 drift scan
  instead — defense exists, but the binding itself is untested.
- **M21** — no selftest case deletes a frozen path; deletion is caught only by the drift scan's `D` status.
  Drop it and the deletion of any frozen path goes unnoticed (the counter materialises frozen tools from the
  *freeze* commit, so a deleted-at-rev tool would still run).
- **M37** — duplicate envelope ids untested.
- **M46** — committing bytes that match the regeneration but not the manifest pin is untested; transitively
  covered given `carriers_regenerated` (low impact).
- **M47** — class/arm equality in regeneration untested.

## Bounds compliance, tooling, restoration evidence

- Writes: only this report, `artifacts/R41W2C2CounterMut/`, and seat scratch `/fast/scratch/hyaku/kaidoku-r41/R41W2C2CounterMut` (removed at the end). No corpus/, tools/, plans/, PROVINCE/SCORECARD/SKILL/LOG writes; no fleet-repo or shokuknow writes; no VCS mutation anywhere (read-only git only); no subagents, no background jobs launched by me (the harness auto-backgrounded four long batch commands; their outputs are the recorded rows).
- Tooling authorization: **nothing installed or upgraded** — the sweep used the preinstalled `python3` and `git` only; sasquatch/sasquatch-v4be/unblob untouched; no pacman transactions.
- Lane restoration evidence: `tools/round-41/c2-counter.py` sha256 `c6c1ea64f07884a3b160a7e52268d295d54c8ef3bc2005704d5fae3398720af8` before the first probe and after the last; porcelain empty on the probed frozen paths; `restore-demo.json` shows byte-exact restore on a scratch copy with the detector returning to baseline.
- Runtime: selftest ≈ 33–35 s per probe, real score ≈ 1.2–2.7 s; sweep wall ≈ 18 min across four concurrent batches.

## Artifacts (this dir: `.ufo/waves/round-41/w2/artifacts/R41W2C2CounterMut/`)

| file | sha256 | note |
|---|---|---|
| `baseline.json` | — | pristine D1+D2 baseline, commands and outputs |
| `BASELINE.receipt.json` | `1a67ac540061fc87751f77e498dc7f740279c7d27b2ed16c7d315052bca49a88` | 93 537 B, pristine D2 receipt |
| `M05.receipt.json` | `0d5f577723bc299e7f7568b0ba1fc44780e0785d916c9c795d47b1c8735b58c1` | 95 397 B, the verdict-flipping survivor's D2 receipt |
| `M06.receipt.json` | `988c076b7e0cec1417f950d5c2ad74020e2c6344297f1aebb463e64f2e55510c` | forced-binding flipper (selftest-killed) |
| `M07.receipt.json` | `281202cec9be3d6d6f1246045afc37bcbf96c9284b1a22f9c5853313209ccccb` | dropped-missing flipper (selftest-killed) |
| `summary.jsonl` | `cea9f2fbf29a0a3be694cab653aa47cd5ccb13e30a5e657b0fc5ae033c4621b8` | all 29 mutant rows: patch provenance via `driver.py`, mutant sha256, D1+D2 outputs |
| `driver.py` | `d72d45e4a9f4f2d2cd61d3df10eac6e6e14d2a88c626ec3cf5a12ae8a9e7f5af` | every mutant's exact patch; rebuild any mutant with it |
| `restore-demo.json` | — | mutate→detect→restore evidence for M05 |

## Limits

- Detector D2 scores the mutant *program* against the unmodified lane tree at e9a24d07 (read-only git); it does not re-run REA or regenerate vendor bytes (C2 needs none).
- Commit-granularity blindness of the drift scan (delete+re-add inside one commit) is inherited from the counter and out of scope here.
- The selftest-survivor classification is relative to the counter's own 70-case selftest; no external oracle for the counter's bindings exists beyond D2.
- Whether R41-C2 should be re-verdicted MET (reading `carriers[].declared`) or the manifest re-packaged is a decision for L1; this seat makes no verdict change.
