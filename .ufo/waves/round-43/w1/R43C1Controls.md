CONFIRMED — all **five** R43-C1 controls score as expected at the round-42 freeze rehearsal (CTL-C1-0 exit 2 `no_manifest_at_rev`; CTL-C1-1 exit 1 with `seed_matches_freeze` AND `manifest_after_freeze` false; CTL-C1-2 red exit 3 / green exit 0 with no manifest written; CTL-C1-3 all eight shortcut controls reproduce their round-42 receipts and none reaches 78/78; CTL-C1-4 the unedited baseline keeps `observed_features_match_declared` true while a one-field manifest hand-edit flips it false with every envelope byte unchanged), and two round-42 defects that the round-43 controls had to be redesigned around are reported in §4.

# R43-C1 controls — wave 1 (pre-freeze build)

Seat `R43C1Controls` (executor). Lane base `6b9e64fe7e0de202d9383baad5792fbfe039a743`. The draft is
`plans/round-43-claims.md` (`## R43-C1`); its kill rule names the five controls below and the frozen paths are
`tools/round-43/{c1-counter.py,heldout-gen-v4r43.py,c2-controls-r43.py}`, the round-42 frozen tools
`tools/round-42/{sqfs-triage-v4.py,indep-eval-v4.py,fixtures.json}`, the round-42 lookup control
`.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md`, the SKILL v4 table region, the round-42 fixtures, the round-42
dev arm and the round-41 C1 receipts.

**Nothing is frozen yet; this output feeds the freeze.** The L1 integrates and commits; I do not.

## 1. What is delivered

| file | kind | what it is |
| --- | --- | --- |
| `c2-controls-r43.py` | tool | the round-43 control driver: builds the control tables, scores the five controls, writes one receipt per control plus a summary |
| `controls/CTL-C2-*.md` | control tables | the ten frozen round-42 control documents, copied byte-exact (sha256-verified) — 8 shortcut controls + the reference witness + the do-nothing document |
| `receipts/CTL-C1-{0,1,2,3,4}.json` | receipts | one receipt per control: expected exit, actual exit, the bindings that fired, the argv |
| `summary.json` | receipt | the whole run: control tables + provenance + every control's verdict + the kill-rule flag |

The L1 installs the tool at `tools/round-43/c2-controls-r43.py` and the tables at
`.ufo/waves/round-43/controls/c1/` (the path the plan's kill rule names).

## 2. The five controls, expected vs actual

The receipts in `receipts/` were produced against the **round-42 frozen tools at the round-42 freeze `d1681696`**, which is
the rehearsal available before the round-43 counter and generator exist (§6 states the residual gap). Every control is
driven through its real interface; nothing is simulated.

| control | expected | actual | verdict |
| --- | --- | --- | --- |
| **CTL-C1-0** do-nothing | counter at the freeze exits **2** `no_manifest_at_rev` | exit **2**, `unevaluable: no_manifest_at_rev`, `counter_sha256 f1089167…` | PASS |
| **CTL-C1-1** stale manifest | counter exits **non-zero**; `seed_matches_freeze` AND `manifest_after_freeze` both false | exit **1**; fired: `seed_matches_freeze`, `manifest_after_freeze`, `carriers_regenerated`, `observed_features_match_declared` | PASS |
| **CTL-C1-2** refusal | tuple check exits **3** and writes **no manifest** (red); a manifest the check passes exits **0** (green) | red exit **3**, manifest sha256 unchanged; green exit **0** | PASS |
| **CTL-C1-3** shortcut controls | the eight controls reproduce their round-42 receipts; **none** reaches 78/78 | all eight reproduce exactly (matched **and** missed-set); max control 75/78; the witness reaches 78/78 | PASS |
| **CTL-C1-4** hand-edit rejection | counter exits **non-zero** with `observed_features_match_declared` false on a one-field manifest edit, true on the unedited baseline | baseline **true** (exit 1 on other bindings); hand-edit **false** (exit 1); 78/78 envelopes byte-unchanged | PASS |

`kill_rule_fires: false`.

### 2.1 CTL-C1-1 — which binding fired

**The plan asks for the binding that fired; here is the precise answer, per placement.** The stale manifest is planted
in a sandbox clone in two placements, and the two fire **different** bindings:

| placement | counter exit | bindings that fired |
| --- | --- | --- |
| **at-freeze** (the stale manifest is already in the tree when the freeze is cut) | 1 | `seed_matches_freeze`, `manifest_after_freeze`, `carriers_regenerated`, `observed_features_match_declared` |
| **after-freeze** (the stale manifest is committed after the freeze, as if it were the held-out data) | 1 | `observed_features_match_declared` only |

The **at-freeze** placement is the primary one: it is the one that makes the counter's own two ordering bindings fire.
`manifest_after_freeze` is false because the manifest was **first added at** the freeze, not after it.
`seed_matches_freeze` is false because the planted manifest's `seed` field is the **round-42** freeze
`d1681696…`, while the sandbox freeze is a different commit. Both are the bindings the plan names.

The after-freeze arm is reported because it isolates them. There the manifest *was* added after the freeze, so
`manifest_after_freeze` holds; and `seed_matches_freeze` holds **in the rehearsal only** — because the rehearsal freeze
*is* `d1681696…`, the very hash the planted manifest declares as its seed. **At the round-43 freeze the freeze hash
differs from the planted seed, so `seed_matches_freeze` will be false in that arm too**, and the only binding that will
relax is `manifest_after_freeze` (true there, false in the at-freeze arm). The receipt records
`planted_manifest_seed` and `sandbox_freeze` side by side so the L1 can confirm this at the real freeze rather than
assume it. What does not change is that the counter refuses in **both** placements (exit 1) — the after-freeze arm on
`observed_features_match_declared`, which is the round-42 stop binding the round-43 claim is built to repair.

The planted manifest is **byte-exact**: `656c22d52ef038f28d77391324f23223d4b893ad2b4775f4a147d50734fde557`, identical to
`corpus/evidence/round-42/c2/heldout/manifest.json` at `d5e22b51`. The sandbox is a `git clone --shared` under
scratch with fixture identity only (`-c user.name=fx -c user.email=fx@fx`); the lane's VCS is never touched.

### 2.2 CTL-C1-2 — the red/green pair

Red (the committed round-42 held-out set, whose C02 declares a gap set its own envelope does not show):

```
REFUSE C02  combo  gap_kinds: declared ['extractor-failure', 'unpublished-entry'] observed ['depth-limited', 'extractor-failure', 'unpublished-entry']
tuple check over 78 carriers (77 declare what their envelope shows) -> REFUSE
exit 3, manifest sha256 unchanged (656c22d5… before and after)
```

Green (the same set with C02's declared tuple set to what the check itself observed): **exit 0**, 78/78 carriers. The
correction is taken from the **check's own stdout**, so the green half does not depend on which file the check reads its
observation from (`run.json` or the emitted `rea-full.json`).

### 2.3 CTL-C1-3 — the shortcut controls, re-scored

Re-scored on the frozen round-42 dev arm (`corpus/evidence/round-42/c2/dev`, 78 envelopes: 24 `combo` + 54 named) with
the frozen round-42 interpreter `tools/round-42/sqfs-triage-v4.py` and evaluator `tools/round-42/indep-eval-v4.py`.

| control | role | interp exit | matched | combo | named | reproduces the r42 receipt | at target |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CTL-C2-0-base-SKILL | do-nothing | 2 | 0/78 | 0/24 | 0/54 | yes | no |
| catch-all | control | 0 | 8/78 | 0/24 | 8/54 | yes | no |
| actions-rotated | control | 0 | 2/78 | 0/24 | 2/54 | yes | no |
| exact-gap-sets | control | 0 | 52/78 | 8/24 | 44/54 | yes | no |
| no-legacy-row | control | 0 | 75/78 | 23/24 | 52/54 | yes | no |
| v4-handler-glob | control | 0 | 2/78 | 0/24 | 2/54 | yes | no |
| no-container-residue | control | 0 | 67/78 | 17/24 | 50/54 | yes | no |
| **lookup** | control | 0 | **66/78** | **19/24** | 47/54 | yes | no |
| **lookup-fallback** | control | 0 | **66/78** | **19/24** | 47/54 | yes | no |
| CTL-C2-REF-v4-precedence | **witness** | 0 | 78/78 | 24/24 | 54/54 | yes | **yes (by design)** |

Every control reproduces its round-42 receipt exactly — the `matched` count **and** the missed-carrier **set** (the
receipt's `missed` list is a different *order* because it was computed on two scratch slices; the sets are equal). No
control reaches the target; the reference table does, which is what proves the arm is scoreable at all.

### 2.4 CTL-C1-4 — counter-side hand-edit rejection

The claim's fifth control (added by the L1 in the amended `plans/round-43-claims.md`) asks the counter to reject a
*hand-fabricated* declaration. Two arms, both on the **frozen round-42 dev arm** (whose declarations agree with their
envelopes in every carrier — 0 mismatches of 78), both planted at the counter's evidence path in an `at-freeze` sandbox:

| arm | manifest | envelopes | `observed_features_match_declared` | counter exit |
| --- | --- | --- | --- | --- |
| **baseline** | byte-exact, unedited | unchanged | **true** | 1 (other bindings) |
| **hand-edit** | one field changed: `H01.published` `"nonzero"` → `"zero"` | **byte-identical** (78/78) | **false** | 1 |

Baseline true → hand-edit false, with every envelope byte unchanged, is the red/green of the binding itself. It proves
the counter derives the observed tuple from the **envelope bytes**, not from the manifest's own `generator.tuple_check`
record: a counter that trusted the manifest's self-report would pass the edited manifest. The receipt records the edit
(`carrier`, `class`, `field`, `declared_before`, `declared_after`), the per-envelope digests before and after
(`envelopes_untouched: true`), and every binding that fired.

Note for reading the arm: the dev arm carries `envelope.json` + `run.json` but **not** `carrier.sqsh`, so the
carrier-path bindings (`carrier_paths_unique`, `carriers_committed`, `carriers_regenerated`) are false for a reason
unrelated to the edit. The discriminator is `observed_features_match_declared`, which is why the control is defined on
that binding and on the baseline-versus-edit pair rather than on the aggregate exit alone.

## 3. What the round-43 counter and generator must be, for these controls to run at the freeze

The tool drives the real tools and probes their interfaces rather than assuming them.

* The **counter** is invoked as `--root LANE --rev REV --freeze FREEZE --json-out OUT` and its receipt is read for
  `exit_code`, `unevaluable`, `bindings`, `bindings_false`, `counter_sha256`. CTL-C1-1 asks the counter where it reads
  its manifest (`manifest_path` in the receipt) and plants the stale manifest **there**, so the control does not hard-code
  a path that may move.
* The **generator** must expose the tuple check over a committed directory. The tool probes `--tuple-check DIR`, then
  `--check-tuples DIR`, then `--verify-declared DIR`, and if no CLI answers it imports the generator module and calls its
  own `run_tuple_check` / `tuple_check` / `refusal_check` function. Exit **3** is read as the refusal
  (`declared_tuple_unobserved`), **0** as the pass, **2** as unusable input. Every probe is recorded in the receipt
  (`interface_attempts`), so the receipt names the interface that answered.
* **The round-43 counter must populate `counter_sha256_at_freeze` on every exit path.** The amended freeze-integrity
  rule requires it, and the round-42 counter does **not** satisfy it on the unevaluable path: it assigns the field at
  line 1796, after its `raise Unevaluable('no_manifest_at_rev', res)` at line 1106, so the CTL-C1-0 receipt records
  `counter_sha256_at_freeze: null` and `counter_sha256_at_freeze_present: false`. The receipt carries that boolean
  precisely so the gap is visible rather than assumed.

  **Confirmed with the counter owner (`R43C1Counter`) after this report's first draft:** the round-43 counter sets
  `counter_sha256` **and** `counter_sha256_at_freeze` on every exit path (assigned in `main()`'s handler before any
  write), carries `counter_path`, and keeps `manifest_path` = `corpus/evidence/round-43/c1/heldout/manifest.json`. It
  also warns — and this matters for reading CTL-C1-0 — that on the exit-2 `no_manifest_at_rev` path `bindings` is an
  **empty map** (round-42 behaviour), so no binding may be read from that receipt; my `ctl_c1_0` reads only `exit_code`
  and `unevaluable`, and records `bindings_present` so the emptiness is explicit.
* **`observed_features_match_declared` stays a distinct six-field binding** computed from the committed envelope bytes
  (the counter owner confirms `observed_features(envelope_data(json.loads(envelope)))`, never `generator.tuple_check`).
  The eight-field check (the two extras included) is a separate binding, `declared_extras_match`, and the recorded
  self-report is cross-checked by `generator_tuple_check_consistent` — which can never make the declared-match binding
  pass. That is exactly the separation CTL-C1-4 relies on.
* **Extra claim bindings** the round-43 counter adds beyond round 42 (all must be true for exit 0):
  `v4_table_region_at_anchor`, `interpreter_pinned_at_anchor`, `evaluator_pinned_at_anchor`,
  `generator_tuple_check_all_equal`, `generator_tuple_check_consistent`, `declared_extras_match`, `runjson_digests`,
  `fixtures_pinned`, `r42_controls_reproduced`, `r42_control_reference_full`. They do not change the controls: CTL-C1-1
  asserts only that its two named bindings are present-and-false, so additional bindings neither rescue nor break it;
  `r42_controls_reproduced` / `r42_control_reference_full` are the counter's own view of what CTL-C1-3 measures
  independently.
* **The counter's held-out lookup score is reported, not bound** (the round-42 L1 freeze decision — the round-42 receipt
  measured 19/24, so a below-half binding was unreachable); `combo_unseen_majority` against the frozen round-42 dev-arm
  named union is the bound anti-enumeration witness. CTL-C1-3 for its part measures the lookup on the **dev** arm, which
  is a different question and is labelled as such (§4.2).

## 4. Two round-42 receipts that were wrong, and the controls redesigned around them

These are the two things the seat brief asks for ("any control you had to redesign because the round-42 receipt was
wrong"). Both are round-42 defects, both are reproducible from committed bytes, and both change what the round-43
control must do.

### 4.1 The do-nothing control is not rebuildable — it must be copied

`tools/round-42/c2-controls.py` copied the **live** `SKILL.md` into `CTL-C2-0-base-SKILL.md` ("the do-nothing document")
and rebuilt the lookup rows from the dev arm. At round-43 the live `SKILL.md` already carries the frozen v4 table, so a
rebuild turns the do-nothing control into the reference table. Measured, running the round-42 builder unchanged against
the base lane:

```
SKILL.md (live v3 table)          exit=0 matched=78/78
CTL-C2-0-base-SKILL.md            exit=0 matched=78/78     <-- the do-nothing control is now the witness
kill_rule_fires True
```

The kill rule would fire on the control set itself. **Redesign:** the round-43 control tables are the frozen round-42
documents **copied byte-exact and sha256-verified**, never rebuilt from the live `SKILL.md`. The copy is what keeps the
do-nothing document at exit 2 / 0-of-78. The tool records each table's sha256 and its source path in
`summary.json` (`control_tables`).

This also reproduces the round-42 tables exactly, which is the calibration proof for the copy: rebuilding the round-42
control set from the committed dev arm **in two slices** (the 54 named carriers, then the 24 combo carriers) yields
**byte-identical** documents for all ten (`diff` empty for every one, including the lookup and its fallback). The
round-42 builder's `combo_ids()` reads `manifest.json` **inside each `--dev` directory**, so the round-42 receipt was
produced against two scratch slices without a `manifest.json` — and the tables it built are reproducible only when the
same two-slice layout is used. A single-directory rebuild differs (§4.2).

### 4.2 The round-42 receipt's combo/named split is degenerate — it must be recomputed

`.ufo/waves/round-42/controls/c2/dev-scores-prefreeze.json` records, for **every** one of its 14 documents:

```
"combo": [0, 0],  "named": [<matched>, 78]
```

A zero of zero combos. The cause is the same scratch slices: `combo_ids()` found no `manifest.json`, so no carrier was
classified as `combo`, and all 78 envelopes were counted as *named*. The receipt's `dev_slices` field names the vanished
scratch paths (`/fast/scratch/hyaku/kaidoku-r42/l1-ctl/{named,combo}`), which no longer exist.

The `matched` numbers are right — all fourteen reproduce exactly (§2.3). The **split** is wrong, and it is the split the
round-43 claim needs: the round-43 counter's `combo_unseen_majority` binding and the lookup control's
below-half test are both **combo** measurements, and the round-42 receipt cannot answer either.

**Redesign:** the split is recomputed from the committed dev arm's `manifest.json` (`class == "combo"`), which names 24
combos and 54 named carriers. The recomputed split is materially different, and the lookup control is the case that
matters:

| control | round-42 receipt (degenerate) | recomputed from the committed dev arm |
| --- | --- | --- |
| lookup | combo `[0, 0]`, named `[66, 78]` | combo **19/24**, named 47/54 |
| lookup-fallback | combo `[0, 0]`, named `[66, 78]` | combo **19/24**, named 47/54 |
| no-legacy-row | combo `[0, 0]`, named `[75, 78]` | combo 23/24, named 52/54 |
| exact-gap-sets | combo `[0, 0]`, named `[52, 78]` | combo 8/24, named 44/54 |

The lookup control scores **19 of 24** dev-arm combos. That is a *dev-arm* number and it says nothing about the
held-out set the claim scores (the round-42 counter measures the lookup on the held-out combos, where it scored below
half). But it is the number a reader would otherwise take from the round-42 receipt as "0 combos tested", and it is the
split the round-43 kill rule has to be read against. The receipt carries both (`r42_receipt_combo` and the recomputed
`combo`), so the difference is visible rather than silent.

**A second, smaller mislabel in the same receipt:** the row keyed `"SKILL.md (live v3 table)"` is not the v3 table. At the
round-42 freeze the live `SKILL.md` already carried the v4 table, and the row's 78/78 with exit 0 is the **v4
reference** scoring the arm — the same numbers as the `CTL-C2-REF` row. The round-42 builder excluded it from the kill
rule by name (`k != 'SKILL.md (live v3 table)'`), so the mislabel did not fire the rule, but the row cannot be read as
a v3 measurement. The round-43 tool classifies by **role** (`control` / `witness` / `do-nothing`) instead of by key
name, so a renamed or re-scored document cannot silently enter or leave the control set.

## 5. Calibration

1. **Every round-42 receipt reproduces.** 14/14 documents: `matched` equal, `missed` **sets** equal, `label_hits` and
   `action_hits` equal. The frozen interpreter and evaluator are byte-identical to the round-42 freeze
   (`497bab6766a0…`, `7a135dd36b3…`).
2. **The ten control tables are byte-identical to the frozen round-42 documents** and reproduce them when the round-42
   builder is run on the same two-slice layout (§4.1).
3. **The reference table reaches 78/78** on the same arm with the same tools, so "none of the controls reaches the
   target" is a property of the controls, not of a broken arm.
4. **The arm's own tuple agreement is 78/78** — the frozen generator's `feature_diff` over the committed dev arm's
   `run.json` records finds **no** mismatch, while the same function over the committed **held-out** set finds exactly
   **one** (C02, the round-42 stop binding). The dev arm is therefore a sound base for the red/green pair and the
   held-out set is not — which is the shape the round-43 claim needs.
5. The v4 table region of `SKILL.md` is byte-identical at the round-42 freeze and at the base
   (`dfbbc5e44453bf54277c29944b5ba72e67fc1fe0b27a48c2cc8826bd9984e56b` over the region from the
   `<!-- sqfs-triage-table v4 -->` marker through the end of the first table after it).

## 6. Limits, risks, and the residual gap

1. **The round-43 counter and generator do not exist yet.** The receipts in `receipts/` were produced against the
   **round-42 frozen tools at the round-42 freeze `d1681696`** — the rehearsal available pre-freeze. Each receipt names
   the exact argv, the tool sha256 and the freeze it ran against, so the L1 can re-run the identical tool at the
   round-43 freeze with `--counter tools/round-43/c1-counter.py --generator tools/round-43/heldout-gen-v4r43.py
   --freeze <the round-43 freeze>`. The counter interface is already the plan's (`--root/--rev/--freeze/--json-out`); the
   generator's tuple-check entry point is probed three ways plus a module-function fallback, so an interface that
   differs from the round-43 revenger's patch is still found (or reported as absent, which fails the control loudly
   rather than silently passing).
2. **The rehearsal's freeze is the round-42 freeze.** CTL-C1-1's at-freeze arm plants the stale manifest in a commit
   that *becomes* the sandbox freeze, so `manifest_after_freeze` is false. At the round-43 freeze the same arm plants it
   in a commit that becomes a child of the real freeze, and the counter sees `manifest_after_freeze` false because the
   manifest was first added **at** the freeze. The binding semantics are the same; the L1 should confirm the receipt
   names the same two bindings when re-run at the real freeze. One rehearsal-specific asymmetry to re-check there:
   the planted manifest's `seed` field is `d1681696…`, which **is** the rehearsal freeze, so the after-freeze arm's
   `seed_matches_freeze` is true in the rehearsal and will be false at the round-43 freeze (§2.1).
3. **`observed_features_match_declared` also fires in CTL-C1-1.** That is the round-42 stop binding (routed defect
   R42-CL1) and it fires on the planted round-42 manifest because C02's declared tuple is the unobserved one. It is a
   *third* independent reason the counter refuses the stale manifest, not a substitute for the two the plan names. The
   receipt separates them (`required_false` vs `bindings_fired`).
4. **The CTL-C1-0 receipt's `counter_sha256_at_freeze` is `null` — in the rehearsal only.** That is the round-42
   counter's own behaviour on the exit-2 path (it assigns the field at line 1796, after its
   `raise Unevaluable('no_manifest_at_rev', res)` at line 1106), and the receipt records
   `counter_sha256_at_freeze_present: false` so the gap is explicit. The round-43 counter sets it on every exit path
   (confirmed with `R43C1Counter`, §3), so at the real freeze that boolean should read `true`. The same receipt shows
   `bindings_present: false`, which is the round-42 empty-`bindings` behaviour on this path — no binding may be read
   from CTL-C1-0's receipt.
5. **The dev-arm combo split is recomputed, not the held-out one.** CTL-C1-3's split is a dev-arm measurement (§4.2).
   The claim's own combo measurement is the counter's, on the held-out set, and is the counter's job, not this seat's.
6. **Scope.** No REA, no unblob, no sasquatch was run: every number here comes from committed envelopes and committed
   tool bytes. No published third-party firmware image was opened or copied. No lane file was modified; the only lane
   writes are this seat's own artifact directory and this report. No VCS mutation in the lane (the CTL-C1-1 clones are
   scratch fixtures with `fx` identity). No tool was installed or upgraded. Scratch
   `/fast/scratch/hyaku/kaidoku-r43/w1-R43C1Controls` was removed before this report was written; every cited artefact
   is copied into the artifacts directory.
7. The **reference table is a witness, not a control**, and reaches the target by design. If the round-43 kill rule is
   read as "every document in the control directory must stay below the target", the witness trips it. The tool keeps
   them apart by role and reports `controls_at_target` and `witness_at_target` separately.

## 7. How the L1 re-runs this at the freeze

```
S=/fast/scratch/hyaku/kaidoku-r43/w1-R43C1Controls; mkdir -p "$S"
cd "$S" && export TMPDIR="$S"
python3 -I -B tools/round-43/c2-controls-r43.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --out .ufo/waves/round-43/controls/c1 \
  --json-out .ufo/waves/round-43/controls/c1/summary.json \
  --receipts .ufo/waves/round-43/controls/c1/receipts \
  --freeze <the round-43 freeze commit>
```

`--out` receives the ten control tables, `--receipts` one receipt per control, `--json-out` the summary. Defaults:
`--counter tools/round-43/c1-counter.py`, `--generator tools/round-43/heldout-gen-v4r43.py`,
`--interp tools/round-42/sqfs-triage-v4.py`, `--eval tools/round-42/indep-eval-v4.py`,
`--dev corpus/evidence/round-42/c2/dev`. Exit **0** = every control behaved as expected and the kill rule did not fire;
**1** = a control reached the target or disagreed with its expectation; **2** = usage, IO, or a required frozen tool is
absent. `TMPDIR`/`--scratch` are honoured; nothing is written outside `--out`, `--receipts` and `--json-out`.

## 8. Files and hashes

Under `.ufo/waves/round-43/w1/artifacts/R43C1Controls/` (the tool is 51,424 bytes and the whole directory is 399,458
bytes, well under 5 MB, so nothing needs a rebuild-by-hash citation):

```
ac9547fc2cd41bd1c33d04bf42562f86eeadb6cdacd69ade49ca024561b38548  c2-controls-r43.py
5d7d98c51cd97ff28dc97d88af08c6839ab49b4eb9a1e8f33461d98568b09147  summary.json
912648957d4aebf27328b643cc2700cd6a8c350e4b81fdbff616ad64aa033b22  receipts/CTL-C1-0.json
7909db04373f95a0ad0d2c8410563cc8583c7b335a0c897762b1bde32eaf74de  receipts/CTL-C1-1.json
a5faa2feca934decf7078c5fb46ad79b781fdf6fd6509e883c1a4351a79f83cf  receipts/CTL-C1-2.json
e3991b284d0eafe69ca401508ab35834435ad282afcdcb24f8ba2106e8091d27  receipts/CTL-C1-3.json
4a94a3e3654d39de6808b4ea1c7f859556dde9c66592e13668ce047f5daaae51  receipts/CTL-C1-4.json
94d13b445701609f110ca6512e99f87afbdc00ccee3123b817853107f3cd725c  controls/CTL-C2-0-base-SKILL.md
265216e8952f8c3d4d9ebaf38dc0ccde1bd6688ff18618df5216cf836b897cfc  controls/CTL-C2-1-catch-all.md
39346bf2403f3b2e4d7f9da638fa3bb1bbd5fff74ab5c33a287a05df1edfbb0c  controls/CTL-C2-10-no-container-residue.md
f5db0f5dd387470a7c53f6e1843d5f12c5e9ca4aae0f48c5cdf596ca70d683be  controls/CTL-C2-3-actions-rotated.md
667ef6fd2b16bb1fb9765d9bb4ba6a8d950591a6b3d4f174fb84d36b4315024f  controls/CTL-C2-4-exact-gap-sets.md
7f193c8fdea23e2410909b7b6d6da6965f66e58052e6d576db2dc83429f4304f  controls/CTL-C2-7-lookup.md
29ba338a002c78baf278897224e14126d67d0e35a5f7906a7d74452586448e71  controls/CTL-C2-7b-lookup-fallback.md
d5d3d3566f98c872cb55d3263b8ed809ecd32e2a0448276ca05601b8d50b87f1  controls/CTL-C2-8-no-legacy-row.md
6f09b440f39b6a193a05bf55c4bfd82ead88b36bd72684ecf9710ee7057fe664  controls/CTL-C2-9-v4-handler-glob.md
70f908e04d9d625a5d506316e6ceaaa29f5d476be7da0ac10cdd949e18d80e7e  controls/CTL-C2-REF-v4-precedence.md
```

The `controls/` documents are byte-identical copies of the frozen round-42 controls (their sha256 are the round-42
commit's own), so the L1 can install them without re-deriving anything.

### 8.1 How the rehearsal was produced (so the L1 can reproduce it exactly)

* **Counter** — the frozen round-42 counter
  `f108916713b38d860acdd60d78dd1d1a541b9feccb1bd1979742dd8dd952cb59` with **one constant** changed so it reads the
  round-43 evidence path the way the installed round-43 counter will:

  ```
  - MANIFEST = 'corpus/evidence/round-42/c2/heldout/manifest.json'
  + MANIFEST = 'corpus/evidence/round-43/c1/heldout/manifest.json'
  ```

  That single-line variant is sha256
  `ce5a48fd883aebfbbaeb73953d3f522c8dd011b9728fb526a4e47ff5268be6d0`. With it the control discovers the evidence
  directory from the counter's own receipt (`manifest_path`) and plants the stale manifest at
  `corpus/evidence/round-43/c1/heldout/`, which is what the receipt shows.
* **Generator** — `tools/round-42/heldout-gen-v4.py` with the round-43 revenger's `placement.patch` applied
  (`.ufo/waves/round-43/w1/artifacts/R43RevRevenger/placement.patch`), which adds `--tuple-check DIR` and the exit-3
  refusal. The patch is the revenger seat's artefact; my tool does not depend on it and probes three CLI spellings plus
  the module-function fallback (§3).
* **Freeze** — the round-42 freeze `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b` (the rehearsal freeze; §6.1
  records the residual gap).
* **Scratch** — `/fast/scratch/hyaku/kaidoku-r43/w1-R43C1Controls`, removed before this report was written; every
  cited artefact is in the artifacts directory.

**One receipt field is legitimately absent:** the CTL-C1-0 receipt's `counter_sha256_at_freeze` is `null`. The
round-42 counter sets that field at line 1796, *after* its `raise Unevaluable('no_manifest_at_rev', res)` at line 1106,
so on the exit-2 unevaluable path — which is exactly CTL-C1-0 — the counter never reaches the assignment. It is a
property of the counter on that path, not a missing measurement; `counter_sha256` (the counter's own digest at the
measured revision) is present.
