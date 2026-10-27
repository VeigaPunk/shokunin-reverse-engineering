DONE (rev 2, after the L1's C05 counterexample) — `heldout-gen-v4r43.py` authored as a faithful port of `tools/round-42/heldout-gen-v4.py`, with the ONE functional change QUALITY 85 names (manifest finalization becomes measured: post-run refusal, exit 3 `declared_tuple_unobserved`, no manifest on any difference), a predictor fix whose rule is now **“the extractor ran AND a recursive extraction output directory exists”** (the C05 correction: a residue carve is a file, not an extraction directory), the `--carriers-only` / `--tuple-check` / `--selftest-tuple` surfaces, and everything green/red as specified: 17/17 offline cases (incl. C02 and C05 red/green), two 78-carrier `--run --verify` dev arms at exit 0, and a verified seam with the L1's `c1-counter.py`.

# R43C1Gen — round 43 w1: `tools/round-43/heldout-gen-v4r43.py`

Seat: R43C1Gen (leaf executor). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `6b9e64fe7e0de202d9383baad5792fbfe039a743`. **Nothing was installed into the lane**: the tool and
every receipt live under `.ufo/waves/round-43/w1/artifacts/R43C1Gen/`; the L1 installs the tool.
No VCS mutation, no REA/unblob on any published third-party image: every live run was on my own
freshly generated carriers plus the pinned MIT unblob 26.6.4 fixtures (read-only inputs).

## 1. Deliverable

| path (artifacts) | what |
|---|---|
| `heldout-gen-v4r43.py` | the port; sha256 `6ab0114d555a09a93ab61459c7adb76a45957a35dc69671b64e7733225aca97a`, 4185 lines |
| `port.diff` | full `diff -u` against the round-42 blob `6b9e64f:tools/round-42/heldout-gen-v4.py` |
| `shape-c05-measurement.json` | the 6-shape C05-family measurement (raw REA-derived tuples) |
| `receipt-*.txt` | 17 receipts, cited below |

### Diff summary (line-count-wise)

| | |
|---|---|
| base blob | `6b9e64f…:tools/round-42/heldout-gen-v4.py`, sha256 `c2b1641a…3a5e1`, **3419** lines |
| port | `heldout-gen-v4r43.py`, **4185** lines |
| patch | **+787 / −90 lines, 20 hunks** |

Hunk groups (every line accounted for):

1. **module docstring** (+36): the ROUND 43 contract paragraph (what changed, and what did not).
2. **`VERSION`** `r42-c2-v4` → `r43-c1-v4`.
3. **`default_fixture_pins()` / `pins_logical_path()`** (+28/−2): resolves the *frozen* round-42 pin list
   (`tools/round-42/fixtures.json`) and records a lane-relative name, so a manifest carries no host path.
4. **`combo_declared()`** (−21/+~40, moved block): the `depth-limited` `reached` clause becomes the measured
   rule (§3) and the `published` computation moves above it (pure reordering; no other value changes).
5. **`shape_of_data()` split out of `_envelope_parts()`** (+19/−10): the finalize step re-derives a produced
   envelope's shape with *the same* code the run used.
6. **measured finalization machinery** (+257): `write_manifest_file`, `manifest_projection`,
   `_read_json_any`, `envelope_shape_on_disk`, `canonical_tuple`, `declared_tuple_of`, `observed_tuple`,
   `diff_tuple`, `tuple_check`, `measure_out_dir`, `print_tuple_diffs`, `tuple_check_block`,
   `finalize_manifest`, `run_tuple_check_dir`.
7. **`build_set()`** (+6/−3): `write_manifest` flag; manifest metadata `round 43` / `claim R43-C1` /
   `generator.name heldout-gen-v4r43.py` / `generator.path` / `generator.port_of`, plus a
   `declared_schema.finalization` note.
8. **`verify()`** (+18/−1): re-runs the tuple check over the envelopes on disk; a mismatch fails the exit.
9. **`regen_check()`** (+20/−10): the manifest byte comparison is over the **seed-determined projection** (§5.2);
   carriers and `tree.json` comparisons are byte-for-byte unchanged from round 42.
10. **`run_tuple_selftest()`** (+~370): the offline suite — gate green/reds, the C02/C05 predictor
    regression against measured tuples, and the C05 gate red/green; also called at the end of `--selftest`.
11. **CLI/`main()`** (+75/−53): `--carriers-only`, `--tuple-check DIR`, `--selftest-tuple`; `--seed` optional
    only for the read-only check; the `--run` flow builds with the manifest deferred, runs REA, then finalizes.

Everything the L1 listed as “keep exactly” is untouched in behaviour: the 27 named classes + `combo` family
(27×2 + 24 = 78 carriers), all seed semantics, the `--run` REA envelope production, the `declared_features`
single-key contract (R41-CL1), and carrier/tree byte regeneration.

## 2. The refusal (exit semantics, exact)

```
python3 -I -B tools/round-43/heldout-gen-v4r43.py --seed <FREEZE> --out <DIR> --run --scratch <S>
```

* **Agreement** (every carrier's measured six-field tuple equals its declared tuple): manifest written with
  `generator.tuple_check` = `{rule, fields[6], measured: true, all_equal: true, carriers: {<id>: {observed:{…6…}, declared:{…6…}, equal:true}}}`; exit **0**.
* **Any difference**: stdout gets
  `declared_tuple_unobserved: N of M carrier(s) observed a tuple the manifest would not have declared -- writing NO manifest`
  then the per-carrier diff list (`C20  combo  gap_kinds: declared [...] != observed [...]`); **no `manifest.json`
  is written** (it was never written earlier in this mode); exit **3**.
* REA run failure (no envelope) → exit **1** (round-42 semantics), no manifest.
* `--tuple-check DIR` (read-only, no `--seed`): exit **3** on any difference, **0** on agreement, **2** when
  `DIR/manifest.json` is absent; writes nothing.
* `--verify` (needs `--run`): exit **1** on any feature-table, `combo_unseen_majority`, re-run tuple-check or
  regen failure.
* `--carriers-only`: carriers + per-carrier files only, **no manifest**, exit 0.

The declared tuple is still a pure function of class/factors; it is never read back from a run — the refusal
is the guard, so the check cannot be satisfied by copying the observation.

## 3. The predictor rule (and the C05 correction)

`combo_declared`, at `max_depth == 1`:

```python
extraction_output = (capped                       # the tar member's extract dir
                     or bool(factors['body_v4'])  # any v4 chunk extracts
                     or not damage_effective)     # a clean legacy chunk extracts
reached = (not dep_effective) and extraction_output
```

**Mechanism** (REA 6.5.0 / unblob 26.6.4, `--max-depth 1`): unblob adds a descent task only for an extraction
directory that exists (`processing.py:372-378`: `if extract_dir.exists(): add_subtask(...)`), and REA mints
`depth-limited` where the ceiling stops that descent (`processing.py:274`). So the invariant is **“a recursive
extraction output directory exists”** — not “anything was published”.

**Measured** on fresh trees (own carriers, forced factor vectors, six C05-family shapes + five earlier probes):

| shape at depth 1 | `dl_paths` | `depth-limited` |
|---|---|---|
| legacy clean + residue | `…/0-4096.squashfs_v3_extract` | **PRESENT** |
| **legacy damage + residue (C05)** | **`[]`** | **ABSENT** |
| legacy damage + residue + wrap | `…/0-10240.tar_extract` | PRESENT |
| legacy + v4 sibling, damage + residue | two squashfs extract dirs | PRESENT |
| v4 damage + residue | the v4 extract dir | PRESENT |
| legacy clean + wrap | `$output/firmware.bin_extract` | PRESENT |
| v4 damage, links none/in-tree/escaping/both (no residue) | the v4 extract dir | PRESENT |
| v4 clean / legacy clean | extract dir | PRESENT |
| legacy fixture damage alone | `[]` | ABSENT |
| any dependency failure | `[]` | ABSENT |
| v4 damage at depth 3 | `[]` | ABSENT |

`receipt-shape-c05.txt` + `shape-c05-measurement.json`.

### The two directions of the round-42 error (both reproduced on real REA)

Round 42's clause (`a failing root chunk mints nothing`) is wrong in one direction and right in another. With the
round-42 predictor swapped back in, at seed `6aba53e3…` (draws both shapes), the guard refuses **2 of 24** combos —
one of each direction (`receipt-postrun-refusal.txt`):

| combo | round-42 declared | observed |
|---|---|---|
| C14 (C02 shape: v4 damage, no residue) | `['extractor-failure']` | `['depth-limited','extractor-failure']` (under-prediction) |
| C20 (C05 shape: legacy damage + residue) | `['depth-limited','extractor-failure','unknown-chunk-handler']` | `['extractor-failure','unknown-chunk-handler']` (over-prediction) |

My first port fixed only the first direction (`published == 'nonzero'`), which the L1's pre-freeze dry-run
caught as C05; the rule above fixes both, and both are now pinned by offline regression cases.

**Regression**: over **all 48 committed combos** (round-42 held-out seed `d1681696` + dev seed `e48947bb`) the port
has **0 mismatches**; the round-42 generator as control has **1 (C02)** — `receipt-predictor-regression.txt`.

## 4. Controls (all executed; receipts in the artifacts dir)

| control | command | result |
|---|---|---|
| **CTL-C1-2 RED** | `--tuple-check corpus/evidence/round-42/c2/heldout` | **exit 3**, exactly 1 of 78: `C02 gap_kinds: declared ['extractor-failure','unpublished-entry'] != observed ['depth-limited','extractor-failure','unpublished-entry']` |
| GREEN (committed, second seed) | `--tuple-check corpus/evidence/round-42/c2/dev` | **exit 0**, 78/78 |
| **Post-run refusal, real REA, both directions** | round-42 predictor swapped in (scratch driver), seed `6aba53e3…`, `--classes combo --run` | **exit 3**, 2 of 24 (C14 under, C20 over), **manifest absent** |
| Offline selftest | `--selftest-tuple` | **17/17 PASS** (gate green; C02/C05/extra-kind/wrong-handler/`declared`/`class_expected.features` reds; verify red on a mutated envelope; **6 predictor cases vs measured tuples**; **C05 gate green + red**) |
| Inherited `--selftest` | `--selftest` in the install layout | **17/17** round-42 checks + **17/17** tuple cases, exit 0 |
| End-to-end, both-shapes seed `6aba53e3…` | 78 carriers `--run --verify` | exit 0; tuple_check 78/78; 78/78 reached declared; `combo_unseen 19/24 PASS`; regen: projection identical, carriers 78/78, tree.json 78/78 |
| End-to-end, round-42 seed `d1681696` | 78 carriers `--run --verify` | exit 0; same five PASS lines; **78/78 carriers byte-identical to the committed round-42 set**, `declared_features` changed for **C02 only** |
| **End-to-end at the L1's failing dry-run seed `b8201bf…`** | 78 carriers `--run --verify` | exit 0; tuple_check 78/78; regen all PASS; **C05 declared == observed** = `{gap_kinds:['extractor-failure','unknown-chunk-handler'], handler_set:['squashfs_v2'], be_argv:'no', published:'nonzero'}` — the exact tuple the dry run saw |
| **The L1's `dry-run-r43.sh` with `DRY_SEED=b8201bf… DRY_SWEEP=6`** | their harness, my scratch work dir | **verdict=PASS, exit 0**: G0 preflight (sees this tool's sha and its `--carriers-only`/`--tuple-check`/`--selftest-tuple`), G1 clone + freeze-like commit `9753b25d`, G4 region hash equals `d1681696`, G2 dev arm exit 0, G3 single-key + `generator.tuple_check` 36/36 all-equal, G5 counter coverage 45 bindings, G6 refusal red (my `--tuple-check` on their tampered fixture: exit 3, manifest not rewritten) + green control, G7 counter-level red, and G8's **6-draw sweep: 6/6 accepted** |
| Install-layout run (`<lane>/tools/round-43/…`) | 4 carriers `--run` | all defaults resolve; pins recorded `tools/round-42/fixtures.json` |
| **Seam with the L1's `c1-counter.py`** | its own helpers, read-only, over a real manifest of mine | `tuple_check_entries` spelling `'equal'`, 78 entries, none missing; `generator_tuple_check_all_equal=True`; `generator_tuple_check_consistent` cross-checked **78**, mismatches **0**; `manifest_generator_path` accepts `heldout-gen-v4r43.py`; its regen detects my `--carriers-only` |

The selftest cases the seat named are all present: green = declared == observed → manifest written with
`generator.tuple_check` all-equal; reds = a declared gap-kind set missing `depth-limited` beside a failing chunk
at the depth ceiling (**the C02 shape**), an extra declared kind, a wrong handler family, the tuple under
`declared` only (R41-CL1), the tuple under `class_expected.features` only (R41-CL1), and `--verify` red on a
mutated envelope — plus, for the C05 correction, a **predictor regression** (six shapes vs their measured tuples)
and the **C05 gate pair**: green when the declaration omits `depth-limited`, red when it adds it.

## 5. Seam and contract notes for the L1

### 5.1 Manifest write timing

* `--run` → written **only** by the finalize step (with `generator.tuple_check`); a refusal leaves no manifest.
* no `--run` (a regeneration) → written by `build_set` exactly as round 42, **without** the measured block
  (nothing was measured; asserting `equal: true` there would be a false claim).
* `--carriers-only` → no manifest at all.

The L1's counter already regenerates with `--carriers-only` and reads carrier bytes off the output tree, so no
counter change is needed (§4, last row).

### 5.2 `--verify`'s manifest byte check is over the seed-determined projection

`generator.tuple_check` records a *measurement of a run*, which a no-REA rebuild cannot reproduce; the check is
therefore “manifest bytes identical (seed-determined projection; the measured tuple_check block is checked
separately)”. Carriers and `tree.json` are compared byte-for-byte exactly as round 42 (78/78 on both arms).
Two operational notes: `generator.sha256` is the tool's own hash, so *editing the tool between a build and its
regen invalidates the projection* (I hit this once mid-run — it is a feature, not a flake); and if a literal
whole-file comparison is preferred, the counter must regenerate with `--run` (78 REA runs).

## 6. Risks / disclosed limits

1. **The round-43 seed is the freeze hash — unknowable while authoring.** The rule is validated on 48 committed
   combos, 11 fresh-tree probes (two shape families) and two complete 78-carrier dev arms; a shape I did not draw
   could still mispredict, in which case the generator refuses (exit 3, no manifest). **Treat an exit-3 data run
   as an honest stop, not a retry signal.**
2. `generator.tuple_check.observed == declared` by construction (that is the gate); the counter independently
   re-derives `observed` from the committed envelopes, and `--tuple-check DIR` is the receipt worth committing.
3. The refusal's stdout diff list is the diagnostic; the exit code is the contract. Both are emitted before any
   manifest write, so a partial manifest cannot exist.
4. Pins stay the round-42 MIT files (`tools/round-42/fixtures.json`, pins_sha256 `9f957663c1f2…`); no `--fetch`.
5. `--verify` still does not re-run REA during regen (round-42 behaviour); the tuple re-check re-reads artifacts.

## 7. Tooling

No install or upgrade was needed or performed: `sasquatch`, `sasquatch-v4be`, `unblob` 26.6.4, `unsquashfs`,
`7z`, `jq`, node v24.21.0 / `npx` with `rea-agents@6.5.0` (already in the npx cache) were used as-is. No `pacman`
transaction (host-wide guard honoured). Scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43C1Gen` was removed after the
receipts were copied here.

The tool hardcodes **no** scratch path and carries **no** host path (`grep -c "/home/vgpnk\|/fast/scratch"` → 0):
every write is governed by `--scratch` / `TMPDIR`. The single `/tmp/...` occurrence is inert text inside a
*synthesised* diagnostic argv in the offline selftest fixture (it mimics what REA records and is never a path).

## 8. Files this seat wrote

* `.ufo/waves/round-43/w1/R43C1Gen.md` (this report)
* `.ufo/waves/round-43/w1/artifacts/R43C1Gen/heldout-gen-v4r43.py`, `port.diff`, `shape-c05-measurement.json`
* `.ufo/waves/round-43/w1/artifacts/R43C1Gen/receipt-{diff-summary,selftest-tuple,selftest-full,control-red-round42-heldout,control-green-round42-dev,predictor-regression,shape-c05,dryrun-seed-c05-declaration,postrun-refusal,e2e-both-shapes-seed,e2e-dryrun-seed,e2e-round42-seed,carrier-identity,install-layout-run,counter-seam,dryrun-harness,tooling}.txt`

Nothing else in the lane was touched.
