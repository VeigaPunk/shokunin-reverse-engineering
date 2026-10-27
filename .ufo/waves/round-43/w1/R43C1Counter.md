# R43C1Counter — `tools/round-43/c1-counter.py` (port of the round-42 C2 counter)

**VERDICT: DONE (with one plan-text defect and two disclosed deviations).**
The round-43 C1 counter is authored at
`.ufo/waves/round-43/w1/artifacts/R43C1Counter/c1-counter.py` (sha256
`3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79`, 4112 lines) for the L1 to install at
`tools/round-43/c1-counter.py`. It ports `tools/round-42/c2-counter.py`
(`f1089167…52cb59`, 3026 lines) to `plans/round-43-claims.md` `## R43-C1` **as amended by the L1** (the
amendment commit `1ede187d`), and carries every item the L1 sent mid-wave: tuple_check presence/all_equal,
observed features from envelope bytes only, `declared_extras`, `run.json` digests, the OOD effective-n
disclosure, `--carriers-only` regeneration, the `combo_count` location fix, `counter_sha256_at_freeze` on all
exit paths, and a configurable scratch base.

Report: `.ufo/waves/round-43/w1/R43C1Counter.md`. Artifacts:
`.ufo/waves/round-43/w1/artifacts/R43C1Counter/`. Scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43C1Counter`
(removed). Base `6b9e64fe7e0de202d9383baad5792fbfe039a743`; anchor `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b`.
No VCS mutation, no tool installed or upgraded, no REA/unblob/sasquatch/unsquashfs/7z run, no published image
or carved byte read.

## 1. Interface contract — manifest keys the counter reads

Everything below is read from the **committed manifest at REV** unless the column says otherwise. Binding names
are the receipt's `bindings` keys; every one must be `true` for `exit 0`.

| Manifest key | Shape accepted | Binding(s) it feeds |
|---|---|---|
| `seed` | string, compared lowercased to the freeze commit hash | `seed_matches_freeze` |
| `generator.name` | `heldout-gen-v4r43.py` or the counter's `GEN` path | `manifest_generator_path` |
| `generator.sha256` | string or absent (absent ⇒ not checked) | `generator_sha_matches_freeze` |
| `generator.writer.path` / `.sha256` | lane-relative path present at the freeze, optional sha | `writer_matches_manifest` |
| `generator.fixtures.pins_sha256` / `.license` / `.project` / `.version` / `.commit` / `.count` | object | `fixtures_pinned` (with `tools/round-42/fixtures.json` and its committed copies, both read at the **freeze**) |
| `generator.tuple_check` | dict keyed by carrier id, or `{carriers: <dict|list>}`, or a list of records with `id`/`carrier`; verdict under `equal` or `matches` | `generator_tuple_check_all_equal`, `generator_tuple_check_consistent` |
| `classes` | list of class names, `combo` included | `classes_unique`, `classes_two_each`, `n_equals_twice_classes` |
| `combo_count` | int, top-level **or** under `generator` (round 42 wrote neither, which the port fixes) | `combo_family_wellformed` (compared when declared; presence reported in `combo_count`) |
| `carriers[].id` / `.class` / `.arm` / `.carrier` / `.envelope` / `.sha256` | as round 42 | `ids_unique`, `arms_valid`, `carrier_paths_unique`, `envelope_paths_unique`, `carriers_committed`, `envelopes_valid`, `carriers_regenerated` |
| `carriers[].declared_features` | the ONE key (R41-CL1); six fields | `observed_features_match_declared` |
| `carriers[].declared_extras` | `{extraction_failed, max_depth}` | `declared_extras_match` (the eight-field match) |
| `corpus/evidence/round-43/c1/heldout/<id>/envelope.json` | bare data object or `{ok,data,meta}` | every pair binding; observed features; digest |
| `corpus/evidence/round-43/c1/heldout/<id>/run.json` | generator's run record; `handlers` names EVERY chunk handler (`tar` included), `gap_kinds` its own summary | `runjson_digests` (subject digest, `digest_matches_carrier`, and summary == the counter's own chunk-handler / gap-kind extraction) |
| `corpus/evidence/round-43/c1/heldout/<id>/carrier.sqsh` | bytes | `carriers_committed`, `carriers_regenerated` |

Read from **git**, not the manifest: `SKILL.md` (table region), `tools/round-42/{sqfs-triage-v4.py,indep-eval-v4.py}`
(the frozen tools), `tools/round-42/fixtures.json` + `corpus/evidence/round-42/c2/fixtures/` (the pinned
fixtures), `corpus/evidence/round-42/c2/dev/` (the dev arm), `.ufo/waves/round-42/controls/c2/` (the r42 control
tables and their prefreeze receipt), the round-41 C1 receipts, the r42 lookup controls and the frozen generator.

Frozen tool interfaces are **probed, not assumed** (unchanged from round 42): the interpreter is driven through
`--skill/--json/--table-only/--envelopes` and the evaluator through `--envelopes[--json|--format|--out|--json-out]`,
each attempt's exit code recorded in `interpreter_attempts`/`evaluator_attempts`. The generator's CLI is read off
the frozen source (`generator_flags()`), because round 43's generator refuses to write a manifest before its REA
run.

### Binding list (31 claim bindings + 14 instrument bindings = 45)

Claim: `seed_matches_freeze, manifest_generator_path, generator_sha_matches_freeze, writer_matches_manifest,
regenerated_seed_matches_freeze, carriers_regenerated, carriers_committed, envelopes_valid, manifest_after_freeze,
manifest_before_envelopes, v4_block_present, v4_block_identical, v4_table_region_at_anchor,
interpreter_pinned_at_anchor, evaluator_pinned_at_anchor, evaluator_covers_all,
observed_features_match_declared, generator_tuple_check_all_equal, generator_tuple_check_consistent,
declared_extras_match, runjson_digests, fixtures_pinned, legacy_chunks_not_no_squashfs,
new_legacy_label_exercised, handler_families_exercised, lookup_control_identical, combo_unseen_majority,
real_receipts_depth_limited, legacy_dev_envelopes, r42_controls_reproduced, r42_control_reference_full`.
Instrument: `classes_unique, classes_two_each, n_equals_twice_classes, combo_family_wellformed, ids_unique,
arms_valid, carrier_paths_unique, envelope_paths_unique, v4_block_columns, v4_actions_declared,
observed_actions_declared, decisions_reported, row_decisions_consistent, bindings_complete`.

`bindings_complete` refuses an undeclared binding and a declared-but-unset one, so "every binding evaluated in
the receipt" (QUALITY 84) is itself a binding.

## 2. What is new against round 42 (each item is a receipt field)

| Round-43 clause | Implementation | Receipt evidence |
|---|---|---|
| table region byte-identical at `d1681696`, freeze **and** REV | `table_region()` = marker line → end of the first markdown table after it (the rule the frozen interpreter documents); compared three ways | `v4_table_region_at_anchor`; `table_region.{anchor,freeze,rev}_bytes/_sha, rev_equals_anchor, freeze_equals_anchor` |
| interpreter + evaluator byte-identical at `d1681696`, freeze, REV | sha of three blobs each | `interpreter_pinned_at_anchor`, `evaluator_pinned_at_anchor`; `pinned.<path>.{anchor,freeze,rev}` |
| no commit in `d1681696..REV` touches a pinned tool | `git log anchor..rev -- <path>` | reported `no_commit_touches_pinned`, `pinned_commits` (not bound; the three-way equality is the binding) |
| manifest records the generator's own tuple check, all equal | `tuple_check_entries()` accepts map / `{carriers:…}` / list, verdict under `equal` or `matches`; every carrier must be covered and `true` | `generator_tuple_check_all_equal`; `generator_tuple_check.{present,verdict_spelling,entries,carriers,effective_n,vacuous_carriers,missing,not_equal}` |
| the record must not be self-certifying | recorded `observed` must equal the counter's own extraction from the envelope; recorded `declared` must equal `carriers[].declared_features` | `generator_tuple_check_consistent`; `generator_tuple_check.cross_checked/cross_check_no_tuple/cross_check_mismatch` |
| observed tuple from **envelope bytes**, never from `tuple_check` | `observed_features(envelope_data(json.loads(envelope)))`; `tuple_check` is read by a different function only | `observed_features_match_declared` (CTL-C1-4 shape) |
| `declared_extras` (eight-field match) | `extraction_failed` from the envelope's chunks/gaps, `max_depth` from `parameters.max_depth` | `declared_extras_match`; `declared_extras.rows/mismatch/missing` |
| per-carrier `run.json` digests | subject digest == carrier sha256, `digest_matches_carrier` true, and the record's own `handlers`/`gap_kinds` == the counter's extraction. `handlers` is compared against ALL chunk handlers, not the squashfs subset: 15 of the 78 committed round-42 carriers carry a `tar` chunk (L1 dry-run blocker R43DryRun D1, fixed) | `runjson_digests`; `runjson.rows/mismatch/missing` |
| pinned unblob fixtures actually frozen | the round-42 `fixture_scope()` read a top-level `fixtures` key the generator never writes, so the fixture dir was unfrozen; the port reads `tools/round-42/fixtures.json` and checks every pinned copy (`<id>--<file>`) at the freeze, and both paths are in `FROZEN_PATHS` | `fixtures_pinned`; `fixtures.{pins,pins_present_at_freeze,pins_sha256_at_freeze,pins_sha256_declared,pins_sha256_match,license,files_all_match,files}` |
| regeneration arm without a manifest | probes the frozen generator for `--carriers-only` and uses it; carrier bytes are read off the **output tree**, so no regenerated manifest is required; `regenerated_seed_matches_freeze` is taken from the regenerated manifest's seed when one exists, else proven by byte-identity (`regenerated_seed_source`) | `carriers_regenerated`, `regenerated_seed_matches_freeze`; `regen_{argv,manifest_present}` |
| the round-42 control receipts are reproduced by this counter | every frozen `CTL-C2-*.md` re-scored with the frozen interpreter+evaluator over the frozen dev arm; matched/label_hits/action_hits compared to `.ufo/waves/round-42/controls/c2/dev-scores-prefreeze.json` | `r42_controls_reproduced`, `r42_control_reference_full`; `r42_controls.{receipt,receipt_present,controls,mismatched,missing,reference,rows}` |
| `combo_count` read where it is | top-level **or** `generator.combo_count`; absence reported instead of silently skipped | `combo_count.{declared,carriers,declared_present}` |
| D4 digests on every exit path | assigned in `main()`'s `Unevaluable` handler too | `counter_sha256`, `counter_sha256_at_freeze`, `counter_path` on exit 2 as well |
| no hardcoded scratch | `--scratch` > `$HYAKU_SCRATCH` > `$TMPDIR` > system temp | `--scratch` is optional and defaults correctly |

## 3. Round-42 clauses I could not implement as written (plan text at fault)

**(a) The lookup-control clause is unreachable as drafted, and the amended plan now says so — but the parenthetical
and the prose still disagree.** The first draft's P43-C1 read *"the frozen lookup control … scores strictly fewer
than half of the held-out `combo` envelopes (`combo_unseen_majority` ≥ 12 of 24)"*. Read as a binding, that is
falsified by the committed round-42 receipt on the *same* control and the *same* class structure: `lookup.score =
19` of `n_combos = 24`, `below_half: false` (`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`). The two things
the sentence names are different quantities, and the L1's amendment resolved it correctly: the plan now binds
`combo_unseen_majority` only and says the lookup score is *reported, not bound*. Implemented exactly that way —
`lookup` is a reported section with `binding: false`, and `combo_unseen_majority` is bound as round 42 computes it
(`len(unseen) >= ceil(n_combos/2)`, UNSEEN against the **frozen round-42 dev-arm** named union).

**(b) A five-byte discrepancy in the amended plan's own numbers.** P43-C1 states the region's sha256
`92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2` *"under the counter's `rule_block` extraction —
13 851 bytes"*. Measured on the committed bytes, that sha256 is **13 856 bytes** at both `d1681696` and the base
(§5). The sha is authoritative and agrees; the byte count in the plan is short by five. Both extractions
(`rule_block` and the marker→end-of-first-table rule) are byte-identical here, so no binding is affected — the
counter binds the region bytes, not the plan's prose count.

**(c) `counter_sha256` is `null` before the counter is installed.** The port reads the counter's own blob from
git at REV/freeze, as round 42 did, so the field is `null` until the L1 installs the file at
`tools/round-43/c1-counter.py` and freezes it. This is not a defect, but it means CTL-C1-0's receipt is only
complete when run against an installed counter (§7).

## 4. Selftest

`python3 -I -B c1-counter.py --selftest` builds synthetic git repos under
`$HYAKU_SCRATCH/kaidoku-r43` (no network, no lane writes). Each fixture has three commits — **anchor** (the
round-42-freeze analogue: SKILL v4 region + frozen interpreter/evaluator + the r42 dev arm, r42 control tables and
their receipt + the pinned fixture pins/copy), **freeze** (adds `tools/round-43/*` and the r43 claims), and the
**claim-data** commit — plus, when a case needs it, freeze-time mutations of the region or the interpreter.

```
$ cd /fast/scratch/hyaku/kaidoku-r43/w1-R43C1Counter
$ HYAKU_SCRATCH=$PWD TMPDIR=$PWD python3 -I -B c1-counter.py --selftest
{"selftest": "c1-counter r43 (v4)", "cases": 91, "green": 18, "red": 73,
 "pass": 88, "fail": 0, "failures": []}
SELFTEST cases=91 pass=91 fail=0                                            exit=0
```

Receipt retained at `artifacts/R43C1Counter/evidence/selftest.txt` (sha256
`81e2110d5b35de4bec317387297adb96f668b42e36d24ad41608c7824f374b4a`). The run leaves nothing behind: every
fixture temp dir (`c1v4.`, `gen.`, `dev.`, `ctlscore.`) is registered and removed per case, so a red case cannot
leak either. The green cases cover the held-out set
(27 named classes × 2 + 24 combos, n = 78, `matched == 78`, every binding true) under each frozen-tool
interface variant; the 73 red cases each assert the exact binding that must go false.

Ported from round 42: every green interface variant (full CLI envelope, lane-relative paths, inferred envelope
path, interpreter via `--envelopes`, tab/row-only/1-based/`--table-only` row recovery, wrapped/list/`--out`
evaluator shapes, marker quoted inline, prose edited outside the region, json without a row index, writer
declared) and every red case (the `declared`/`features` key spellings, feat mismatches, feature-absent,
feature-envelope, combo-feature, v1–v3-labelled-`no-squashfs-chunk`, non-`none` handler cell, missing legacy row,
unexercised legacy label, missing v1/v2 families, lookup v3, dev-arm missing/short/disagreeing, real receipts
missing/mislabelled/disagreeing, truncated/catch-all/`*`-trailing tables, missing action column, missing actions
line, undeclared `raise-depth`, blind interpreter, shared carrier path, wrong generator sha, writer not in the
freeze/ wrong writer sha, do-nothing at the freeze, evaluator/interpreter failures, unparsable manifest, unknown
revision, freeze-not-ancestor) plus the round-42 freeze-integrity set (interpreter/generator/evaluator/counter/
claims/lookup/evidence/block edited after the freeze, block mutated then restored, actions line edited, both
writers touched while declared).

Added for round 43: **tuple_check absent**, **one carrier `equal:false`**, **verdict under a wrong key**
(`declared_verdict` instead of `equal`) — all three must take `generator_tuple_check_all_equal` false; a **green
list-form tuple_check**; **a table-region byte changed between the anchor and the freeze** (region binding false,
and no post-freeze drift, so exit 1 not 2); **an interpreter byte changed between the anchor and the freeze**
(`interpreter_pinned_at_anchor` false); **the manifest committed in the freeze commit itself**
(`manifest_after_freeze` false, `first_add == freeze`).

## 5. Retained evidence

Table region, measured with the counter's own extraction on committed bytes (`git show <rev>:SKILL.md`):

```
d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b  13856  92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2
6b9e64fe7e0de202d9383baad5792fbfe039a743  13856  92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2
```

Round-42 control receipts re-scored by this counter's machinery over the committed dev arm (probe, before the
port; all 14 controls, `matched`/`label_hits`/`action_hits` identical to
`.ufo/waves/round-42/controls/c2/dev-scores-prefreeze.json`):

```
OK  CTL-C2-0-base-SKILL.md      exit=2 matched=0/78  want 0
OK  CTL-C2-0c-v3-rows-13col.md  exit=0 matched=51/78 want 51
OK  CTL-C2-1-catch-all.md       exit=0 matched=8/78  want 8
OK  CTL-C2-10-no-container-residue.md exit=0 matched=67/78 want 67
OK  CTL-C2-4-exact-gap-sets.md  exit=0 matched=52/78 want 52
OK  CTL-C2-7-lookup.md          exit=0 matched=66/78 want 66
OK  CTL-C2-7c / 7x / 8 / 9 / REF → 59 / 26 / 75 / 2 / 78, all equal to the receipt
```

Do-nothing control on the real lane (before install; receipt retained at
`artifacts/R43C1Counter/evidence/ctl-c1-0-do-nothing.json`):

```
$ c1-counter.py --root <LANE> --rev 6b9e64fe... --freeze 6b9e64fe... --json-out ctl0.json
{"exit_code": 2, "unevaluable": "no_manifest_at_rev", "frozen_paths_changed": []}   exit=2
receipt: unevaluable=no_manifest_at_rev, exit_code=2,
         manifest_path=corpus/evidence/round-43/c1/heldout/manifest.json,
         anchor=d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b, frozen_paths_changed=[],
         fixtures.files_all_match=true   (all 14 committed fixture copies match their pins at the base)
         fixtures.pins_sha256_match=false (no round-43 manifest yet, so nothing declares the pins)
         counter_sha256=null, counter_sha256_at_freeze=null   (file not installed yet)
```

That is CTL-C1-0's exact shape, and it is also the only runnable state before the L1 installs the counter and the
generator.

### The run.json binding measured on the 78 committed round-42 carriers (L1 blocker D1)

`evidence/runjson-probe.py` (kept) evaluates both comparisons with the counter's own `observed_features` over
committed bytes only — no REA, no network. Output `evidence/runjson-probe.txt`:

```
carriers with run.json: 78
OLD (handlers vs squashfs_handlers) mismatches: 15
   C01  want=['tar']                 got=[]
   C05  want=['tar']                 got=[]
   C08  want=['squashfs_v3', 'tar']  got=['squashfs_v3']
   C09  want=['tar']                 got=[]
   H52  want=['tar']                 got=[]
   … (15 total: every carrier whose chunk set holds a non-squashfs handler)
NEW (handlers vs chunk_handlers) mismatches: 0
```

The binding now compares the record's `handlers` to the counter's **chunk** handler list (all of them), so it is
green on all 78 committed carriers instead of red on 15. `observed_features()` gained an explicit
`chunk_handlers` key for this (the six-field tuple and `handler_set` are untouched, so
`observed_features_match_declared` and the declared-tuple contract do not move). Two red selftest cases pin the
new behaviour: a run.json whose subject digest is wrong, and one whose handler list disagrees with the envelope.

### Fidelity notes (differences from the round-42 counter that the L1 should know)

- `handler_families_exercised` now matches **families by prefix** (`squashfs_v1*`, `squashfs_v2*`, `squashfs_v3*`,
  a `squashfs_v4_*`) instead of the round-42 exact-name test `{'squashfs_v1','squashfs_v2','squashfs_v3'} ⊆ F`.
  The clause says "v1, v2, v3 and a v4 family", and unblob 26.6.4 names the members
  `squashfs_v2_nonstandard`, `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard` — the exact
  test reads false on the very class list round 42 shipped. The exact names found are still reported in
  `handler_families.legacy_present`.
- `score_control()` scores through the **same interface prober** as the main measurement (`run_interpreter`), not
  by guessing one output shape; the round-42 control tool assumed a three-field tab row.
- The fixture's `score_fixture_controls()` measures the r42 receipt with `run_evaluator`, so the reproduction
  binding cannot disagree with the counter merely because the harness read a different evaluator interface.
- The r43 vocabulary keeps round 42's seven-key extraction (`… + extraction_failed`); the claim's "six declared
  fields" are `REQUIRED_FEATURES`, and `extraction_failed`/`max_depth` are bound separately under
  `declared_extras_match` (the eight-field match).

### Freeze integrity hardening (R43RevFreeze review, implemented)

`frozen_drift` now runs three independent nets instead of one walk:

1. **merge-aware walk** — `git log -m --diff-merges=first-parent --name-status` over `FREEZE..REV`; plain
   `git log` suppresses a merge's diff entirely, so a merge that carries a frozen-path change in was invisible.
2. **A-as-change for frozen blobs** — status `A` counts when the frozen path was a **blob** at the freeze, so a
   delete-then-re-add (byte-identical or not) is a change.  A file added *inside* a frozen **directory** is a new
   file, not a rewrite of a frozen one, and is left to the ordering bindings; `kind_at()` makes the distinction so
   the rule cannot misfire on the held-out evidence.
3. **tree-level blob backstop** — for every frozen blob the bytes at FREEZE and at REV are compared directly, so a
   change no commit in the walk reports still fails.

**corpus/SOURCES.md is frozen too**, because P43-C1 reads the S135 licence row out of it: the whole registry is a
frozen blob, so no post-freeze edit can move a licence row under the fixtures' licence basis (the C2 predicate only
requires no post-freeze edits; the round-43 rows are pre-freeze).  Selftest case: **the S135 row rewritten after the
freeze -> exit 2**.

**SKILL.md is frozen WHOLE**, not just by its v4 table region: the round-43 plan adds status paragraphs *before*
the v3/v4 markers, which sit outside the region, so a region-only check could not see a post-freeze prose edit.
`SKILL` now sits in `FROZEN_PATHS` and rides net 1/3 above as a blob; the region check and `skill_block_drift`
remain as the finer-grained witness. The selftest case that used to accept a prose edit (round-42 behaviour) is now
a frozen case: **SKILL status prose outside the table region edited after the freeze -> exit 2**.

`skill_block_drift` walks with the same merge-aware `commits_touching` and gained a tree-level backstop on the
region: the SKILL v4 table region at REV must equal the region at the freeze whatever the walk says.  Ancestry is
checked both ways — `freeze_not_ancestor_of_rev` and (new) `anchor_not_ancestor_of_rev`, each exit 2.

Two new red selftest cases pin this: **a merge that carries a frozen-interpreter edit in on a side branch**
(invisible to a plain walk) and **a frozen path deleted then re-added byte-identically** (invisible to the tree
backstop and to an `M`-only status rule).

## 6. Risks and disclosed limits

- **`counter_sha256*` is `null` until the L1 installs the counter** at `tools/round-43/c1-counter.py` before the
  freeze (§3c). Every other exit-2 receipt field is complete.
- **The generator does not exist at the base.** `tools/round-43/heldout-gen-v4r43.py` is another seat's artifact;
  until it lands, a run at REV reaches `generator_absent_at_freeze` (exit 2). The counter never assumes its CLI:
  `--carriers-only` is used only when the frozen source advertises it, and a manifest is never required from a
  non-`--run` run.
- **`generator.tuple_check` is generator-self-reported**; the counter bounds it with
  `generator_tuple_check_consistent` (recorded observed vs the counter's own extraction) and keeps the substantive
  six-field check on envelope bytes (`observed_features_match_declared`). A fabricated-but-internally-consistent
  envelope set that both frozen tools label identically remains indistinguishable by design — the claim's own
  disclosed limit, unchanged.
- **OOD vacuity.** The tuple check is vacuous for the two `out-of-domain` carriers (empty envelope, empty declared
  tuple); the receipt records `generator_tuple_check.effective_n = 76` and names `vacuous_carriers`.
- **`combo_unseen_majority` is factor-draw dependent** (round 42 measured 19/24 unseen); it is bound with the
  round-42 threshold and computed against the frozen dev arm, not against the round-43 set's own named tuples.
- **Reported, not bound:** the lookup control's held-out combo score, `no_commit_touches_pinned` (the three-way
  byte equality is the binding), the two lookup variants (`lookup`, `lookup_7b`), and every interface attempt.
