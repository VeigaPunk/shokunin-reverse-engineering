# R41C2Counter — the round-41 C2 counter (triage table v3 vs an independent evaluator)

**Verdict: DONE** — the v3 counter is delivered, selftested and mutation-swept, and it reads the *real* integrated
`tools/round-41/sqfs-triage-v3.py` / `indep-eval-v3.py` end to end. It cannot produce a score yet: nothing is
frozen, `tools/round-41/heldout-gen-v3.py` does not exist, and `corpus/evidence/round-41/c2/heldout` is not
committed. Two freeze blockers measured on current bytes are in §6.

## 0. Artifacts (all under `.ufo/waves/round-41/w1/artifacts/R41C2Counter/`)

| file | sha256 | role |
|---|---|---|
| `c2-counter.py` (2499 lines) | `c6c1ea64f07884a3b160a7e52268d295d54c8ef3bc2005704d5fae3398720af8` | the counter; `--root/--rev/--freeze/--json-out`, `--selftest` |
| `c2-counter.v2-to-v3.diff` | `efd8b9844ea553ca56f42ced09f8125d88ad46506151c20b8c1ee8ea0fb6e118` | `diff -u` from `49096c7e:tools/round-40/c2-counter.py` to this file |
| `selftest.txt` | `f3db407a7763381d5a7b16c7c2ef5361b90a036f94c5855cc9cb301e00bb29a6` | `--selftest` output: `cases=70 pass=70 fail=0`, exit 0 |
| `mutants.py` | `d046c0af844a1a0e50e5b53f1ff0adccfab3bd8bc087713e4df3b7ec113d09b0` | mutation driver over the counter's own battery |
| `mutants.json`, `mutants.txt` | `861b194e…`, `c906b189…` | sweep result: 10 mutants, 10 killed, 0 survived |
| `real-tool-interface-check.json` | `36d7a0c58bb5bcb99bb816f0d1a713cc340c72111d058418f8ba56fbd480e2d9` | measurement against the integrated v3 tools (§5) |
| `smoke-lane-49096c7e.json` | `b3fad9fcf3167fb69455080f98a39d810fb9da2d26fb2a3eb9300be26a273993` | receipt of a run on the lane at the base: exit 2 `no_manifest_at_rev` |

No vendor bytes, no extracted vendor file and no evidence file is copied into the lane (nothing was downloaded or
extracted for this seat).

## 1. What the counter decides — 29 bindings, mapped to claim clauses

`Exit 0` = `matched == N` and all 29 bindings true; `1` = a pair miss or a binding false (receipt written);
`2` = inadmissible/unevaluable (freeze integrity or a structural prerequisite). The receipt always records its own
`exit_code`, so a re-minted receipt cannot claim a result the run did not produce (R39-CL6), and `met_target` is
recomputed from the raw numbers before it is trusted (`met_target_inconsistent` → exit 2).

Claim bindings (15), each a sentence of `Predicate P41-C2` as amended:

| binding | claim clause |
|---|---|
| `seed_matches_freeze` | seed = freeze hash |
| `manifest_generator_path`, `generator_sha_matches_freeze` | the manifest names the frozen generator at the frozen bytes |
| `writer_matches_manifest` | the declared writer is the one in scope, present at the freeze, at the declared sha |
| `regenerated_seed_matches_freeze`, `carriers_regenerated` | every carrier regenerates byte-identically from the freeze seed |
| `carriers_committed` | committed carrier bytes hash to the manifest pin |
| `envelopes_valid` | every envelope's subject digest equals its carrier's sha256 |
| `manifest_after_freeze`, `manifest_before_envelopes` | manifest first added in a commit descending from the freeze, no later than its envelopes |
| `v3_block_present`, `v3_block_identical` | the v3 block at REV == the freeze block (whole block, marker → next rule block) |
| `evaluator_covers_all` | the frozen evaluator answers for every envelope |
| `observed_features_match_declared` | observed (H, G, D, BE, SR, P) == the declared tuple, for class **and** combo carriers |
| `real_receipts_depth_limited` | the four committed round-40 C1 receipts get `depth-limited` from the interpreter **and** equal the evaluator |

Instrument bindings (14) are calibration guards whose failure means the score is not trustworthy rather than that
the table is wrong: `classes_unique`, `classes_two_each`, `n_equals_twice_classes`, `combo_family_wellformed`
(12 carriers `C01..C12`), `classes_cover_planned` (20 classes), `ids_unique`, `arms_valid`,
`carrier_paths_unique`, `envelope_paths_unique`, `v3_block_columns` (the ten decision columns of the twelve),
`v3_actions_declared`, `observed_actions_declared`, `decisions_reported`, `row_decisions_consistent`.

Reported, never bound (wave-1 amendment): `class_map_agreement` (per-carrier `class_expected` vs the evaluator,
`agree`/`disagree`/`missing`), `class_expected_missing`, per-carrier `class_expected_match`,
`regen_class_expected_matches`, `declared_features` (source key, per-class match state, mismatches with the keys
that differ), `matched_classes` / `matched_combos` / `matched` / `n`, `distinct_decisions` (v2 numbering: the
no-match fall-through counts as a decision) and `distinct_rows`, `expected_source`, `advisory_rea_params`
(declared max_depth per class, `binding: false`), `combos.class_expected_null`, `exec_attempts` for both tools.

## 2. What changed from the round-40 counter

Ported clauses kept: manifest/envelope resolution and inferred envelope sibling, digest binding, first-add ordering,
`distinct_decisions`, the no-match row acceptance, the tab/JSON/`--table-only` interpreter plumbing with the row
index base inferred (never assumed) and pairs read off the row the interpreter chose.

1. **Expected pairs now come only from the frozen independent evaluator** (`indep-eval-v3.py` at the freeze bytes,
   envelopes at REV). `class_expected` is compared and reported, never scored. Mutant M5 ("expected from
   class_expected") is killed by 4 cases including the `report:` ones.
2. **`observed_features_match_declared`** (new): the counter extracts (H, G, D, BE, SR, P, and `extraction_failed`
   when declared) from each envelope with a port of the frozen round-40 interpreter's own extractor
   (`sqfs-triage-v2.py:424-580`: handler set from `normalized_result.chunks[].handler`, gap kinds and
   dependencies from `extraction_gaps`, BE from a standalone `-be` in any recorded sasquatch argv, SR from a
   `MaliciousSymlinkRemoved` report anywhere, P from `normalized_result.files`), and compares it with the tuple the
   manifest declares per carrier (`class_expected.features`, else carrier `features`/`declared_features`, else a
   per-class map). Values are canonicalised (00/zero/`0`, nonzero/`>0`, yes/no/n-a, bool) so the manifest's
   spelling does not decide the verdict. The six required keys must be present; a missing tuple fails the binding
   and names the carrier.
3. **`real_receipts_depth_limited`** (new): `corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json` are read at REV,
   run through both frozen tools, and the receipt must have label `depth-limited` and interpreter pair == evaluator
   pair. Their sha256s are recorded in the receipt.
4. **Combo family**: carriers with class `combo` are partitioned out of the class statistics
   (`classes_two_each`, `n_equals_twice_classes = 2·classes + combos`), `class_map_agreement` covers class carriers
   only, and `combo_family_wellformed` binds exactly `C01..C12`.
5. **Freeze integrity, both directions (R40-CL3 F2/F3)** — this is the substantive repair:
   * the frozen generator's **writer** is in scope when the frozen generator's source names it *or* the manifest
     declares it (textual import detection plus `manifest.generator.writer.path`); the writer's freeze sha is
     checked and it is materialised for regeneration;
   * the **SKILL v3 block** is compared at *every* commit in `FREEZE..REV` that touches `SKILL.md`, so
     mutate → restore is exit 2 (round-40's R11 un-blocked; here it does not). The block is marker → next rule
     block, so the `sqfs-triage-actions` line is inside it and an edit there is a drift (M1 kills this: narrowing
     the block to the table rows loses both the actions binding and the drift detection);
   * the marker match requires the marker to *be* the line: rule prose quoting `<!-- sqfs-triage-table v3 -->`
     inline neither starts nor ends a block (selftest case 14, "a rule bullet quotes the marker inline, block
     still found", and the real-tool check);
   * `frozen_drift()` reads one `git log --name-status` per frozen path: a **creation is not a touch** (the held-out
     evidence must be first added after the freeze; its ordering is bound separately), a modification, deletion,
     rename or typechange is (M7, which counts creations, breaks 51 cases).
6. **Round-40 D2 closed strictly**: the `(unclassified, none)` pair must resolve to **no row** (`v == {None}`);
   a table whose correct rows are followed by a `*` row carrying `(unclassified, none)` is exit 1 (case 55), and a
   `*` row carrying any other pair fails `matched`. M4/M8 kill both relaxations.
7. **Dropped as dead weight** (YAGNI, and not in P41-C2): the `--base` commit derivation and the v1/v2 rule-block
   invariance bindings of the round-40 counter. Nothing in the amended predicate needs them, and the v2 block
   legitimately gains a supersession sentence at the freeze.
8. **Interface probing with recorded attempts**: interpreter probed as `--skill S --json ENV…`, `--skill S ENV…`,
   `--skill S --envelopes DIR --json`, `--skill S --envelopes DIR`; evaluator as `--envelopes DIR`,
   `+ --json`, `+ --format json`, `+ --json-out FILE`, `+ --out FILE`; output shapes `{id:{label,action}}`,
   `{"labels":…}`, `{"results":[…]}` and a bare list all parse. The interface that answered is in the receipt.

## 3. Evidence — selftest

`python3 -I -B c2-counter.py --selftest` → `{"cases": 70, "green": 20, "red": 50, "pass": 70, "fail": 0}`, exit 0
(33-36 s; `selftest.txt`). Every case runs the real counter as a subprocess against a throwaway git fixture and
also asserts that the counter left the measured repo clean (`git status --porcelain` empty) and that the receipt's
`exit_code` equals the process exit.

Green (20): 20 classes × 2 + 12 combos with evaluator == interpreter; full `{ok,data,meta}` envelope;
lane-relative paths; inferred sibling envelope; interpreter through `--envelopes`; tab rows; row-only; 1-based
rows; evaluator `labels` wrapper; evaluator result list; evaluator `--json-out` with a human table on stdout;
generator object with matching sha; a prose bullet outside the block edited; JSON without rows recovered from
`--table-only`; writer declared and present; a rule bullet quoting the marker inline.

Red exit 1 (50) include, in the words the item asks for: **evaluator/table disagreement** (action and label),
**class_expected disagreement / absence / unparsable** (now `report:` cases that stay *met* and assert the
`class_map_agreement` payload is populated), **touched writer** (declared-not-in-tree, wrong sha),
**v2 marker** (a craft section carrying only `<!-- sqfs-triage-table v2 -->` → `v3_block_present` false),
declared-tuple mismatches (class, combo, envelope, absent tuple), missing/short combo family, real-receipt
missing / mislabelled / evaluator-disagreeing, seed ≠ freeze, manifest before the freeze, envelopes before the
manifest, carrier not pinned, digest mismatch/swap, missing envelope, three carriers in one class, a missing
planned class, truncated/catch-all/`*`-default tables, missing action column, missing actions line,
`raise-depth` undeclared, row-blind interpreter, shared carrier path, wrong generator sha.

Exit 2 (8): do-nothing at the freeze, interpret/instrument edited after freeze, generator/evaluator/counter/claims
edited after freeze, evidence rewritten by a later commit, block edited after freeze, block mutated then restored,
actions-line-only edit, writer touched when named, manifest unparsable, evaluator failure and non-JSON output,
interpreter failure, unknown revision, freeze not an ancestor.

## 4. Evidence — mutation sweep over the battery (10/10 killed)

`python3 -I -B mutants.py --jobs 5` → `MUTANTS total=10 killed=10 survived=0` (72-96 s).

| mutant | cases passing | caught by |
|---|---|---|
| M1 block starts at the first table row (drops the actions line) | 49/70 | green |
| M2 no SKILL block drift scan (path check only) | 67/70 | frozen |
| M3 writer never frozen | 66/70 | frozen, green |
| M4 no-match pair accepts any single row (round-40 D2) | 68/70 | red |
| M5 expected pair taken from `class_expected`, not the evaluator | 66/70 | red, report |
| M6 declared feature tuple not bound | 62/70 | red |
| M7 a plain creation counts as a frozen touch | 19/70 | green |
| M8 row consistency not bound (D2 shortcut unbound) | 67/70 | red |
| M9 real-receipt binding not bound | 64/70 | red |
| M10 combo family size not bound | 67/70 | red |

## 5. Evidence — against the real integrated tools (not stubs)

`tools/round-41/sqfs-triage-v3.py` and `tools/round-41/indep-eval-v3.py` appeared in the lane at 17:46 while this
seat was running. I drove them with my own parsers (details in `real-tool-interface-check.json`):

* Fixture SKILL: the lane `SKILL.md` at the base with the v2 marker rewritten to a supersession comment and the
  draft block 20 (`.ufo/waves/round-41/w1/artifacts/R41C2Interp/sqfs-triage-v3-table.md`) inserted in the craft
  section. My `rule_block` sees exactly that block: 16 lines, 12 rows, ten decision columns present, 12 declared
  actions.
* `sqfs-triage-v3.py --skill F --json <26 committed round-40 c2 envelopes>` → exit 0, 26 entries with keys
  `row` (1-based int) and `cells`, `infer_index_base` = 1, every row-carried pair equals its row's cells, and the
  two out-of-domain envelopes carry `(unclassified, none)` with `row: null` — my no-match path.
* `--table-only` → 12 label→row pairs, 1-based; parsed unchanged.
* `indep-eval-v3.py --envelopes DIR` → `{"labels": {"H01": {…}}}`, 26 pairs; my `parse_eval_pairs` reads it.
  Its discovery accepts both `<id>/envelope.json` and flat `<id>.json` (so the counter's scratch layout is fine).
* Draft block 20 vs the evaluator on those 26 envelopes: **26/26 agree**, 0 disagreements.
* The four real receipts: interpreter → (`depth-limited-nested`, `raise-depth`) on all four; evaluator →
  (`depth-limited`, `raise-depth`) on all four.
* The lane at the base, `--rev = --freeze = 49096c7e`: exit 2 `no_manifest_at_rev`, `frozen_paths_changed: []`,
  and `git status --porcelain` shows no change attributable to the counter.

## 6. Freeze blockers measured on current bytes (reported to L1)

1. **Rename lag.** The L1 renamed the label to `depth-limited`; the evaluator carries it, the draft block 20 row
   does not. As bytes stand, `real_receipts_depth_limited` fails 4/4 (exit 1, not 2) and any held-out envelope on
   that row would miss. Rename the block-20 row label before the freeze.
2. **The superseded v2 marker must not survive in the craft section.** The v3 interpreter exits 2 —
   `refused marker '<!-- sqfs-triage-table v2 -->' … this interpreter reads only '<!-- sqfs-triage-table v3 -->'` —
   whenever the base SKILL's marker line (line 361) is still there. With it rewritten to a supersession comment:
   exit 0. If it survives, the counter exits 2 `interpreter_failed` with `interpreter_refusal` naming the cause.
3. Interfaces confirmed, so the L1 can freeze without re-probing: interpreter positional + `--json`/`--table-only`,
   evaluator `--envelopes DIR` to stdout. The evaluator also accepts `--out FILE`; the counter probes it.

## 7. Constants the L1 must reconcile with the frozen claims text (the only ones)

* `PLANNED_CLASSES` (20 names: the 13 v2 classes, the 5 combined, plus `body-extractor-failure-le` and
  `failure-depth-limited`) — a rename or a dropped class shows as `classes_cover_planned` false with
  `classes_missing_planned` naming it, exit 1.
* `COMBO_COUNT = 12` and ids `C01..C12` (`combo_family_wellformed`).
* `REAL_RECEIPTS` (the four `corpus/evidence/round-40/c1/*/after.json`) and `REAL_LABEL = 'depth-limited'`.
* `PLANNED` envelope count: `N = 2·20 + 12 = 52`; the counter derives `N` from the manifest and binds the relation,
  it does not hardcode 52.

## 8. Risks and limits

* **Not yet run on frozen data.** The tool chain it scores does not exist at a freeze commit; the strongest
  present evidence is §5 (real tools, real envelopes) and the fixture battery. A first real run will very likely
  surface one interface or key mismatch (e.g. the declared-feature key), which the receipt names precisely
  (`declared_features.source`, `features_missing`, `evaluator_attempts`).
* **Commit granularity.** A mutation and its restore *inside one commit* are byte-invisible; the counter does not
  claim to catch that (nor does any byte-level check).
* **`extraction_failed` is my reading** — a squashfs chunk flag, or an `extractor-failure` gap. If the generator's
  own analyzer counts a `missing-extractor-dependency` gap as a failure (its dev table shows
  `extraction_failed: true` for `dep-missing-*`), the two sides will differ on those four classes and the binding
  will be false with the differing key named. The generator's own dev feature table
  (`.ufo/waves/round-41/w1/artifacts/R41C2Gen/dev-feature-table.md`) is the reference to reconcile — I did not read
  or adapt to its analyzer to keep the counter's extraction a port of the *interpreter's*.
* **`max_depth` is not observable from an envelope**, so it is reported (advisory, from `rea.per_class`) and not
  bound; the binding covers the six features the L1 named plus `extraction_failed` when declared.
* **The real-receipt binding reads round-40 evidence that is not in the frozen path list** (the claim does not
  freeze it). Their sha256s are recorded in the receipt instead; a rewrite is visible but does not block.
* Cost: 52 envelopes × (2 carriers regenerated + 2 tool runs) ≈ tens of seconds once the generator exists; the
  fixture battery is ~35 s and the sweep ~75 s.

## 9. Method record (re-runnable)

```
S=/fast/scratch/hyaku/kaidoku-r41/R41C2Counter; mkdir -p "$S"; cd "$S"
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
A=<lane>/.ufo/waves/round-41/w1/artifacts/R41C2Counter
python3 -I -B "$A/c2-counter.py" --selftest                 # exit 0, cases=70 pass=70
python3 -I -B "$A/mutants.py" --jobs 5                      # exit 0, 10 killed / 0 survived
python3 -I -B "$A/c2-counter.py" --root <lane> \
  --rev 49096c7e6f226af0c750c4b003be58883cb6049f \
  --freeze 49096c7e6f226af0c750c4b003be58883cb6049f --json-out "$A/smoke-lane-49096c7e.json"   # exit 2
# real-tool check (derived fixture, no vendor bytes):
#   cp SKILL.md; rewrite "<!-- sqfs-triage-table v2 -->" -> supersession comment; insert block 20
#   python3 -I -B <lane>/tools/round-41/sqfs-triage-v3.py --skill SKILL-v3.md --json <26 envelopes>  # exit 0
#   python3 -I -B <lane>/tools/round-41/indep-eval-v3.py --envelopes <heldout dir>                   # exit 0
#   python3 -I -B <lane>/tools/round-41/sqfs-triage-v3.py --skill SKILL-v3.md --json <4 receipts>    # exit 0
```
All fixture git mutations happened in `mktemp` dirs under `$HYAKU_SCRATCH` with `-c user.name=fx -c user.email=fx@fx`;
the lane, the fleet root and `~/Projects/shokuknow` were never written. Scratch and `/tmp` files were removed.

## 10. Tooling / environment

No tool was installed, upgraded or moved (no pacman transaction, no `uv tool`, no `npx` install): the counter is
stdlib-only and the runs used the installed `python3` only. `sasquatch`, `sasquatch-v4be`, `unblob` and `REA` were
not run at all by this seat — no extractor work is needed to score C2, and no reserved carrier was touched.
