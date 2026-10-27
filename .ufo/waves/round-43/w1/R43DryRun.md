# R43DryRun — pre-freeze dry-run harness (QUALITY 84)

**Verdict: DONE — harness green and deterministic on the installed round-43 tools, and D8 is
RESOLVED: the failing draw is replayed and accepted. `DRY_SEED=b8201bf474ab85c8f2af5010eb3191f084a63e8a`
(freeze-like `e94d650e…`) plus `DRY_SWEEP=8`: exit 0, G1–G7 all true, 45/45 bindings evaluated,
36/36 carriers `declared == observed`, sweep 8/8 accepted, refusal red+green, region equal (394 s).
The two findings this gate produced are closed: D1 (`runjson_digests`, counter) and D8 (the combo
`depth-limited` over-prediction, generator).**

All facts below were observed in this session; anything argued rather than observed is marked
`[INFERENCE]`.

---

## 1. What was delivered (all under `artifacts/R43DryRun/`)

| file | what it is |
|---|---|
| `dry-run-r43.sh` | **the deliverable** — the gate the L1 runs after integrating `tools/round-43/` and before the freeze. sha256 `51c68d261849188c7dc6933dcd45b1f0232d78549bdca21aa29f1be603b3512f`, 43269 B. |
| `DEV-ARM.md` | the exact dev-arm subset and the per-clause coverage argument (region hash, tuple_check, single-key, lookup-combo), plus the choices rejected. |
| `selftest-stub-gen.py` | a **self-test double**, not a lane tool: implements only the manifest/tuple-check contract so the harness's pass paths (G3, G6) can be exercised before the real tools exist. |
| `evidence/` | the ten receipts/logs quoted in §4–§6 (112 KB total). |

No tool was installed or upgraded (nothing was needed: `git`, `python3`, `jq`, `npx`, `unblob`,
`sasquatch` were already on PATH). No file outside my artifacts dir and my scratch was written;
`git ls-files -m` in the lane still shows only `plans/round-43-claims.md` (the L1's own), and the
lane HEAD was never moved by me.

## 2. How the L1 runs it

```bash
bash .ufo/waves/round-43/w1/artifacts/R43DryRun/dry-run-r43.sh \
     /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
     /fast/scratch/hyaku/kaidoku-r43/dry-run
```

Preconditions: `tools/round-43/heldout-gen-v4r43.py` **and** `tools/round-43/c1-counter.py`
installed in the lane (the harness fails with exit 10 and says which one is missing). Everything
else it needs is already at the base: `tools/round-42/{sqfs-triage-v4,indep-eval-v4}.py`,
`tools/round-42/fixtures.json`, `corpus/evidence/round-42/c2/{dev,fixtures}`,
`corpus/evidence/round-41/c1/*`, `.ufo/waves/round-42/controls/c2/*`, `d1681696` in history.

`DRY_GEN` / `DRY_COUNTER` accept **absolute** paths, so a seat's artifact can be dry-run before the
L1 installs it (the harness copies it into the clone at `tools/round-43/<basename>`). `TMPDIR` and
`HYAKU_SCRATCH` are forced under the work dir; the lane is only read.

Exit codes: `0` all gates · `2` usage · `10` preflight · `11` clone/freeze · `12` generator ·
`13` manifest contract · `14` region hash · `15` counter coverage · `16` refusal red ·
`17` counter-level red. The machine receipt is `$WORK/dry-run-receipt.json`, with every gate, its
observed value, the full binding table, and the refusal evidence.

## 3. The seven gates

| gate | asserts |
|---|---|
| G1 | a scratch clone of the lane whose toplevel is itself, plus a fixture-identity freeze-like commit `F` carrying the pre-freeze material |
| G2 | the frozen generator writes a dev-arm manifest (`--run`, exit 0) |
| G3 | that manifest's contract: the six-field tuple under **one** key `declared_features` (no `declared`, no `features`, no `class_expected.features`), the generator's `DECLARED_KEY`/`DECLARED_FIELDS` equal to the counter's, and `generator.tuple_check` present with every carrier `equal:true` |
| G4 | the `SKILL.md` v4 table **region** (marker line → end of the first markdown table after it) is byte-identical to the region at `d1681696` |
| G5 | the frozen counter runs against the dev arm **end to end** and its receipt carries **every declared binding with a boolean value**; all of them are printed; exit 2 (unevaluable) fails the gate |
| G6 | RED/GREEN of the refusal: a fixture manifest whose declared tuple the run did not observe makes the generator **exit 3** and leaves the manifest byte-identical; the untampered manifest is not refused |
| G7 | counter-level red: the same wrong declared tuple makes the counter report its observed-vs-declared binding **false** |

G5 is deliberately about *evaluation*, not the target: a 36-carrier dev arm cannot satisfy
`n = 78`, and three bindings are structurally false on a subset arm (§6). `met_target` is printed
for information.

## 4. Evidence — every run receipted in `evidence/`

| # | tool pair | arm | exit | elapsed | gates |
|---|---|---|---|---|---|
| 0 | **lane-installed round-43 tools, default invocation (post-fix, deterministic)** | 6 named + combo family = 36 | **0 (PASS)** | 78 s (receipt run) / 197 s with the 3-draw sweep | G1–G7 **all true**; `runjson_digests = true`; dev-arm seed `1ba7f65cb9f55ea073bcfc467634ba904a84126b`; sweep 0/3 refused |
| L1 | the L1's run on the plan/Skill/SOURCES-edited tree, pre-generator-fix | same arm | **12 (FAIL)** | — | G2 false: generator exit 3 on combo C05 (declared `depth-limited`, observed none) — D8 |
| R | **replay of that draw + 8-draw sweep, post-generator-fix (generator sha 6ab0114d…)** | 36 + 8x24 | **0 (PASS)** | 394 s | G1-G7 true; `DRY_SEED=b8201bf…` accepted (36/36 equal); sweep **8/8 accepted**; `false = [carriers_regenerated, handler_families_exercised, new_legacy_label_exercised, seed_matches_freeze]` (the first and last are consequences of forcing the seed, see D8) |
| 1 | round-43 seat tools pre-fix (via absolute paths) | same 36-carrier arm | 0 (PASS, gate-level) | 75 s | G1–G7 true but `runjson_digests = false` — the evidence for D1 |
| 2 | round-42 pair (the port base) | same 36-carrier arm | 13 (FAIL) | 77 s | G3, G6 false — the two round-43 deltas; G1,G2,G4,G5,G7 true |
| 3 | stub double + round-42 counter | 6 carriers | 15 (FAIL) | 6 s | G3, G6 **true** (pass paths proven; G5/G7 not exercisable with stub envelopes) |

Run 0 — the current default invocation (tools read from the lane), `evidence/receipt-real-r43-tools-default-mode.json`:

```
verdict PASS  exit 0
gates: G1_clone true  G2_generator_green true  G3_manifest_contract true  G4_region_hash true
       G5_counter_coverage true  G6_refusal_red true  G7_counter_level_red true
dev arm: 6 named (clean-be, clean-le, clean-empty, escaping-symlink-removed,
         in-tree-symlink-metadata, mixed-symlinks) + combo family = 36 carriers
counter: exit 1  n 36  matched 36  met_target false
         bindings 45/45 evaluated,  bindings_complete true,  missing [], nonbool []
         bindings_false = ["handler_families_exercised", "new_legacy_label_exercised"]
         runjson_digests = true   (D1 fixed)
region:  99cd54d7fe8847486175db9fbf06fa4da3c891a17dd74ffc00eacd64c8ddd6da  == d1681696  (equal)
refusal: --tuple-check <dir>  exit 3, manifest untouched;  green control exit 0
```

The exact refusal ladder that found the entry point (`evidence/refusal-tries.txt`):

```
--selftest-tuple/flag-manifest/rc=2/sha=same  --selftest-tuple/flag-dir/rc=2/sha=same
--selftest-tuple/out-flag-manifest/rc=2/sha=same
--tuple-check/flag-manifest/rc=2/sha=same     --tuple-check/flag-dir/rc=3/sha=same   <-- wins
```

## 5. Dev-arm subset and why it covers the four new clauses

Full argument in `DEV-ARM.md`; the short form:

* **named classes = the RECIPES-order prefix** (`clean-be`, `clean-le`, `clean-empty`,
  `escaping-symlink-removed`, `in-tree-symlink-metadata`, `mixed-symlinks`) **+ the combo family
  (24)**. The prefix is not cosmetic: the counter regenerates the full 78-carrier set at the freeze
  and compares **by id**, and a prefix gives the dev-arm carriers the same ids *and bytes* as that
  regeneration, so `carriers_regenerated` is a real green (it was true in run 1) instead of a
  subset artefact. Combo ids/bytes are selection-independent too.
* **region hash** — G4 (lane-level; it is the clause a `SKILL.md` status-sentence edit silently
  breaks) plus the counter's `v4_table_region_at_anchor` in G5.
* **tuple_check** — G3 on all 36 carriers (the combos make it non-trivial: their gap sets are drawn
  from factors, which is exactly where round 42's C02 declared what it had not observed) and G6's
  red/green on a tampered fixture.
* **single-key** — G3, including the generator↔counter key/field agreement that was the M41-1 seam.
* **lookup-combo** — the 24 combo carriers are what the frozen lookup control and
  `combo_unseen_majority` are scored on; both came back **true** in run 1.

`--combos N` is used only if the generator advertises it; the round-43 port does not (its family is
fixed at 24 in `FAMILIES`), so "6 named + 4 combos" is not expressible and the receipt records
`dev_arm.combos_flag_supported=false`. If the knob appears, `DRY_COMBOS` (default 4) is honoured.

## 6. Findings for the L1

### D1 — RESOLVED (was blocking, counter seat): `runjson_digests` compared unlike lists

**Status: fixed and re-verified.** The counter owner added `chunk_handlers` to `observed_features()`
and now compares `sorted(run.json["handlers"])` against it (counter sha256
`31f307eda772f9ffe7517382352ba367b8da4a14ad6c583639502f0d6ef6ece7`); the re-run in the L1's own
invocation reports `runjson_digests = true` (`evidence/counter-coverage-real-r43-tools-default-mode.json`).
The analysis below is kept as the record of what the gate caught.

Observed in run 1: `bindings_false = ["handler_families_exercised", "new_legacy_label_exercised",
"runjson_digests"]`, and the counter's own detail lists
`runjson.mismatch = [C01 C03 C04 C05 C07 C10 C12 C15 C16 C17 C19]` — 11 of 24 combos.

Mechanism, from the counter source (`tools/round-43/c1-counter.py`, the `runjson_digests` block):

```python
summary_handlers = sorted(rec.get('handlers') or [])            # run.json: ALL chunk handlers
ok = ... and summary_handlers == sorted(obs.get('squashfs_handlers') or [])
                                                                # observed_features: squashfs_* only
```

`run.json` records the generator's `_envelope_parts` shape, whose `handlers` is the union of **all**
chunk handlers; the counter compares it with `squashfs_handlers`, which filters to `h.startswith
('squashfs_')`. The container-wrap factor mints a `tar` chunk, so every wrapped combo fails:
`{"id":"C01","run_json_handlers":["squashfs_v4_be","tar"],"counter_squashfs_handlers":["squashfs_v4_be"]}`.

Not an artefact of my arm: the **committed** round-42 held-out set fails the same comparison on
15 of 78 carriers (`evidence/runjson-digest-defect.json`, e.g. C01 `["tar"]`, C08
`["squashfs_v3","tar"]`).

Impact: `runjson_digests` is in the counter's `CLAIM_BINDINGS`, so at the freeze the real held-out
set (24 combos, several wrapped) would make it false → `met_target` false → exit 1. That is the
round-42 shape of stop, replayed on a binding instead of on the predictor.

Two like-for-like fixes `[INFERENCE — the choice is the counter owner's]`:
1. keep a chunk-handler-only union (`chunk_handlers`) in `observed_features()` and compare
   `summary_handlers` against it — this preserves the "run.json's summary == the envelope" intent
   including the non-squashfs handlers; or
2. compare the squashfs subset on both sides
   (`sorted(h for h in summary_handlers if h.startswith('squashfs_'))`), which is a one-line change
   but stops checking the `tar`/container handlers.

Fix 1 is the one that keeps the binding's stated meaning ("the record's own summary == the
counter's extraction from the envelope").

### D2 — the refusal entry point is `--tuple-check DIR`; CTL-C1-2 must use it

The ported generator's `--tuple-check` is "read-only: run ONLY the declared-vs-observed tuple check
against an existing held-out directory … exits 3 `declared_tuple_unobserved`". The harness's
discovery ladder found it with no configuration and proved red (exit 3, manifest untouched) and
green (exit 0) in run 1. The controls seat's CTL-C1-2 should invoke exactly
`heldout-gen-v4r43.py --tuple-check <dir>`; `--verify` is *not* the entry point (it needs `--run`
and regenerates).

### D3 — region hash is currently satisfied; protect it

The v4 region at the worktree `SKILL.md` and at `d1681696` are the same 13 857 bytes, sha256
`99cd54d7fe8847486175db9fbf06fa4da3c891a17dd74ffc00eacd64c8ddd6da` (`evidence/region-hash.json`). An edit that appends a
status sentence **after** the first table keeps this green; an edit inside the table region turns
G4 and the counter's `v4_table_region_at_anchor` false. The harness re-checks it on every run.

### D4 — the counter still reads the round-42 dev arm

`DEV_DIRS[0] = corpus/evidence/round-42/c2/dev`, which is present at the base; `legacy_dev_envelopes`
was **true** in run 1. No round-43 dev directory has to be created for the freeze.

### D5 — two false bindings on the dev arm are class-selection artefacts, not table defects

`handler_families_exercised` and `new_legacy_label_exercised` need `squashfs_v1/v2/v3` among the
**named-class** (non-combo) envelopes; the id-aligned prefix is all v4. At the freeze the full
27-class set supplies the legacy families, so both must come back **true**; if they do not, the
cause is class selection, not the table.

### D6 — rehearsal caveat and one deliberate tree edit

* `manifest_after_freeze` is false when the evidence path already has history in the clone (a
  rehearsal on `corpus/evidence/round-42/c2/heldout`). On the fresh round-43 path it was **true** in
  run 1; the harness prints this note when it sees the binding false.
* The harness **purges any pre-existing evidence root** from the freeze-like tree so the dev-arm
  commit is an *addition* under the frozen path; a modification would trip the counter's
  `frozen_path_changed` (exit 2). The receipt records
  `evidence_root_purged_from_freeze_tree`.

### D7 — the harness reads the counter, it does not assume it

`MANIFEST`, `GEN`, `DECLARED_KEY`, `DECLARED_FIELDS`/`REQUIRED_FEATURES` are parsed out of the
installed tools with `ast` (literal assignments only) and reported in
`receipts/{counter,generator}-consts.json`. If the L1's integration moves the evidence root or
renames a key, the harness follows it instead of silently scoring the wrong path.

### D8 — RESOLVED (was blocking, generator seat): the tuple guard refused on a dev-arm draw

**Status: fixed and replayed.** The generator seat corrected the combo `depth-limited` predictor
(installed generator sha256 `6ab0114d555a09a93ab61459c7adb76a45957a35dc69671b64e7733225aca97a`).
My replay of the exact failing draw — `DRY_SEED=b8201bf474ab85c8f2af5010eb3191f084a63e8a` — now
finds `36/36` carriers with `declared == observed` and writes the manifest, and `DRY_SWEEP=8`
accepts 8/8 (`evidence/receipt-replay-b8201bf-sweep8.json`, `evidence/run-replay-b8201bf-sweep8.log`).
Corroboration from the generator seat: 78-carrier full `--verify` at `b820` and 17/17 C05-shape tuple
selftests. Note that with `DRY_SEED` forcing the seed, `seed_matches_freeze` and
`carriers_regenerated` evaluate false by construction (the counter regenerates from the freeze-like
hash); that is the replay mechanism, not a defect — the gate that matters for D8 is G2.

The L1's post-edit run of this harness exits **12** (gate G2): at freeze-like seed `b8201bf…` the
frozen generator draws combo **C05** with a declared tuple containing `depth-limited` while its own
`--run` envelope has no `depth-limited`, so the generator refuses (`exit 3`,
`declared_tuple_unobserved`), writes no manifest, and the counter step never runs. Reported by the
L1; **not reproduced on my draws**, which is itself the point: the failure is *seed-dependent*.

What I did observe (all in `evidence/`):

* `probe-r42-seed-combo-accepted.log` — the current generator at the **round-42 freeze seed**
  `d1681696…`, combo family only: `tuple_check: measured 24/24 … every observed tuple equals its
  declared tuple`, manifest written. The historical C02 shape is genuinely fixed
  (`C02 gaps=depth-limited,extractor-failure,unpublished-entry`, matching its declaration).
* run 0 — freeze-like seed `1ba7f65cb9f55ea073bcfc467634ba904a84126b`, 36 carriers, `36/36` equal,
  manifest written.
* `DRY_SWEEP=3` — three synthetic draws (`629b7b89…`, `b89c7a44…`, `d981f3b7…`), each accepted.
  So 4 independent draws accepted and 1 (the L1's) refused.

Mechanism `[INFERENCE, from the generator's own round-43 note and the draw]`: the declared
`depth-limited` is `reached = (not dep_effective) and published == 'nonzero'`, and `published` there
is a **prediction** from the factor vector. On a draw where the prediction says "something was
published" but the run publishes nothing while the extractor still runs, the prediction mints a
`depth-limited` the envelope does not have, and the guard refuses. That is M42-2 with the sign
flipped: over-prediction instead of under-prediction.

Why it is blocking: the freeze seed is only drawn at the freeze, so the data run can land on the
same shape; the generator would then write no manifest and the round stops. Also note the claim
wants the C02 shape *declared as observed* — a declaration the measurement already produced would
make the guard's comparison measured-vs-measured, which is the alternative fix `[INFERENCE]`.

How to reproduce it deterministically (either side can):

```bash
DRY_SEED=<the 40-hex b8201bf… hash> bash dry-run-r43.sh LANE WORK   # exits 12, prints the diff list
DRY_SWEEP=8 bash dry-run-r43.sh LANE WORK                            # samples 8 more draws, reports the rate
```

`DRY_SEED` replays one draw (the receipt records `generator_seed_forced` and that
`seed_matches_freeze` then evaluates false); `DRY_SWEEP=N` is a **reported, non-gating** stage
(G8) because the freeze seed is unknown until the freeze. The fixture-identity commits now carry
fixed dates, so a given tree always yields the same freeze-like hash and therefore the same dev arm.

## 7. Residual risk

* Run 0 **is** the post-install invocation: `tools/round-43/{heldout-gen-v4r43.py,c1-counter.py}`
  were byte-identical to the seat artifacts (`cmp` clean) and the harness read them from the lane.
  That is the receipt the freeze record should cite.
* A generator whose `--run` refuses on the dev arm exits the harness with code 12 and prints the
  per-carrier diff list: that is a legitimate pre-freeze finding (the data run would stop there),
  not a harness fault. D8 is exactly that case.
* Disk at the replay run: `df /fast/scratch` = 84 % used, 134 G free, no ENOSPC; the run needs
  ~1.5 GB (clone + REA work dirs). The soft guard was noted, not hit.
* One draw cannot prove a predictor correct. Run the harness at the freeze-candidate tree **and**
  with `DRY_SWEEP` when the round's defect is a predictor: 4 accepted draws and 1 refused (D8) is
  what a single-seed gate would have reported as PASS.
