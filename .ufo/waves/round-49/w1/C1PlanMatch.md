# R49-C1 plan ↔ counter ↔ controls match (wave 1, pre-freeze) — seat C1PlanMatch

Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Drafts read-only; all mutation in scratch clones built by `draft/mkclone.sh` (dev freeze `05dae3c2…`, scratch only). No tool installed or updated; no pacman; no data run; `c1-run.sh --data-run` never invoked; no lane, fleet or committed file written.

## Verdict

**NOT READY — do not freeze R49-C1 as drafted.** Two findings fail the plan's own rules:

1. **Kill rule fires on a constructible counterfactual (BLOCKING).** Copying the committed round-44 REA receipts, rewriting `parameters.output_directory` to a `/kaidoku-r49/` string, re-minting the evidence id with the frozen xpin rule, and planting the C1 landing blocks gives `exit 0`, `carriers_matched 4`, `met_target true`, `bindings_false []`, `failing []`. The plan's kill rule ("any counterfactual control reaching `carriers_matched == 4` with every binding true stops C1") is therefore reached, and no control in `c1-controls.py` exercises this shortcut (CTL-C1-4 as coded uses round-42 H41/H43/H44/H45 and does not rewrite the path).
2. **CTL-C1-5 is vacuous (BLOCKING for the control set).** It never runs the superblock probe on the mutated bytes. Its counter receipt scores the pristine carriers (`layout_ok true` ×4) and goes red only because no receipts exist (`receipt_present false`). The judge ignores its declared `probe_reds_every_mutation`. The probe itself does red all three mutations (probe output below), so the defect is in the control, not the probe.

Plus plan/counter/control disagreements that the freeze must fix or state: CTL-C1-4 names a different shortcut than the plan; the provenance sentence the plan says the counter "implements" is not implemented; two counter docstring predicates contradict the code; `sasquatch 4.5.1 on the child PATH` is unbound; the landing draft `R49EntryDraft` asserts pre-measured results and names the **round-44** freeze (`c48f8a4`) as the round-49 freeze.

## Findings table

Status: AGREES / DISAGREES / UNCHECKED. Line numbers are `draft/tools/round-49/c1-counter.py` unless stated. "run" = executed in scratch (exit and receipt listed).

| # | Plan clause (P49-C1 / controls / target) | Counter / control binding (function, line) | Status | Evidence |
|---|---|---|---|---|
| 1 | Carrier table: 4 ids, handler, endian, oracle (v1le/v1be/v2le/v2be) | `carriers_spec` 865–990; `EXPECTED_IDS` 257; `carriers.json` | AGREES | carriers.json handlers v1,v1,v2,v2; endian le,be,le,be; sha256 of `corpus/evidence/round-42/c2/fixtures/*` at base equal the pins (checked). v2.1/v2ns not in the table. |
| 2 | Receipt at `corpus/evidence/round-49/c1/<id>/after.json`, first added in a commit descending from FREEZE | `receipt_present` 2084; `receipt_fresh` 2080–2083 (`first_add`, `is_ancestor`) | AGREES | — |
| 3 | `unblob 26.6.4, sasquatch 4.5.1 on the child PATH` | Only `engine [name, version]` in plus-extractor projection (1813–1815) compared to a rerun; no version pin; `sasquatch` absence only via `missing-extractor-dependency` gap. `extract-env.json` written by `c1-run.py` (≈670) is not read; the runner docstring cites an `extract_env_ok` clause that does not exist in the round-49 counter. | DISAGREES (unbound) | `grep -n extract_env_ok c1-counter.py` → none |
| 4 | Names the frozen handler, no failed chunk | `handler_ok` 1928–1929 (exact list equality); `chunks_ok` 1930 | AGREES | — |
| 5 | Publishes every oracle regular file at exact path, same sha256/size, no extra regular file | `oracle_hits_ok` 1944–1947; `extra_published` 1942 | AGREES | — |
| 6 | `gaps == []` | `gaps_ok` via `disposition_check` 1490–1569; `GAP_RULE` structural `{depth-limited:0, unknown-chunk-handler:0}` 350–365 → any gap fails (path-less kinds not structural → fail; path gaps match no nonregular row → fail) | AGREES (in effect) | — |
| 7 | `unpublished_entries == []` | No direct clause. Enforced only through rerun projection (`unpublished_entries` in `PROJECTION_KEYS` 1823–1824; built 1775–1801) | UNCHECKED directly; agrees via `projection_ok` | — |
| 8 | Subject digest == carrier pin | `subject_pin_ok` 1967–1970 | AGREES | — |
| 9 | Stored evidence id recomputed under REA 6.5.0 rule | `evidence_id_ok` 2128–2129; `evidence_ids` 596–632 (xpin: stored = f[1], recomputed id65 = f[2]) | AGREES | REA `dist/domain/evidence.js` 156–182: `semanticProjection` includes `parameters` and `normalized_result`, so the id is minted over `output_directory` as the plan says |
| 10 | Carrier bytes hash to pin; superblock reads magic, s_major, s_minor, endianness | `carrier_pin_ok` 2035–2036; `layout_probe` 1070–1171 | AGREES | Plan omits the compression class, `carve_ok` (2051) and `tree_ok` (2063) that the counter also enforces → plan under-states |
| 11 | Counter-time REA rerun has the same semantic projection | 2099–2112; `projection` 1707–1818; rerun replays receipt parameters `make_real_runner` 1859–1915 | AGREES | Not run here (needs REA npx); the rerun path ran inside CTL-C1-1/2/4 and the forge attack |
| 12 | `parameters.output_directory` is an absolute path inside the `/kaidoku-r49/` segment | `provenance_ok` 1176–1182: `isabs` and substring `'/kaidoku-r49/' in od` and no `..` | DISAGREES (weak; forgeable) | probes: `/tmp/kaidoku-r49/x` → True; `/fast/scratch/hyaku/kaidoku-r42/x/kaidoku-r49/y` → True; committed path inside scratch `/fast/scratch/hyaku/kaidoku-r49/x/corpus/evidence/round-49/c1/v1le` → True. The string is self-declared and the id is re-mintable with the public xpin tool (attack below) |
| 13 | "The committed evidence path is not the output directory — that sentence is the one the counter implements" | No comparison of `output_directory` with `corpus/evidence/...` anywhere in the counter. Runner `c1-run.py` `build_plan` default `outdir_mode='evidence'` (line 330) and its comment (330–343) quotes the superseded claim text ("names a corpus/evidence/round-49/c1/ path"). CLI default is `scratch` (≈799) | DISAGREES (sentence not implemented; runner function default is the superseded binding) | `grep -n "outdir_mode" c1-run.py` |
| 14 | PROVINCE `## Round-49 additions to Core` row names squashfs_v1 and squashfs_v2, names SquashFS v1/v2, cites entry path | `province_core_section` 2153–2154; `province_core_row` 2155–2159 | AGREES | Block-a row (landing draft) contains ENTRY path, `squashfs_v1`, `squashfs_v2`, `SquashFS v1 and v2` (checked in python) |
| 15 | One line carries `Round-49 frontier note`, the entry stem and a SquashFS v1/v2 token | `frontier_note` 2161–2163 | AGREES literally; token VACUOUS | `SQFS12_TEXT_RE` matches `squashfs-v1` inside the stem itself: a line with only `Round-49 frontier note` + stem → True (probe) |
| 16 | Entry exists at REV | `entry_present` 2164–2165 | AGREES | — |
| 17 | Entry `source:` lines cite S138 and S139 | 2166–2170 (lines starting `source:`; `sid_tokens`) | AGREES | Draft entry carries `source: S138`, `source: S139` (checked) |
| 18 | S138/S139 opened `2026-10-28` and list entry in used-by | `sourced` 2172–2185 (`c[8] == OPENED`, `ENTRY or STEM in c[10]`) | AGREES literally; re-open unbound | Base SOURCES already has S138 and S139 `opened 2026-10-28` (used-by the round-44 entry). Round 44 and round 49 share the date, so the `opened` check cannot show a round-49 re-open; the Frontier-step sentence "re-opened this round" is unbound |
| 19 | `corpus/README.md` `## Coverage map` maps the entry stem | `coverage_map_row` 2186–2189 | AGREES | base README has `## Coverage map` at line 11 |
| 20 | No frozen C1 path changed after FREEZE (freeze-integrity) | `frozen_drift` 1629–1683; `FROZEN_PATHS` 272–283; `FROZEN_PREFIXES` 286 | AGREES | Plan frozen list vs counter list: same files; counter also freezes carrier blobs and S138 tree roots (harmless) |
| 21 | Target: `carriers_matched == 4`, every binding true, `frozen_path_changed []`, exit 0 | `met_target` 2216–2218 (`carriers_unchanged`, `carriers_matched == target`, `BINDINGS` 334–337); output keys 2391–2395 | AGREES | — |
| 22 | Counting command argv | argparse 2316–2336 (`--root --rev --freeze --pkg65 --work --json-out` all present) | AGREES | — |
| 23 | Every file of the instruments, controls and fixtures exists in FREEZE | `tools/round-49/control-fixtures/**` does not exist in the draft; to be generated before FREEZE | UNCHECKED (pre-freeze action) | `ls draft/tools/round-49` |
| 24 | Receipts record exit code, stdout sha256, counter sha256 | `stamp_receipt` 479–481; `write_receipt` 2285–2296; controls receipts record all three | AGREES | — |
| 25 | Data run `c1-run.sh --data-run`; provenance.json binding scratch tree to verbatim copy | `c1-run.py` CLI default scratch (≈799), copy 430–434, `provenance.json` 679–684 | AGREES (CLI); `build_plan` default DISAGREES (row 13); counter does not read provenance.json | — |
| 26 | Controls list CTL-C1-0 | `control_c0` 624–633 | AGREES | run: exit 1, `carriers_matched 0`, six doc bindings false, verdict `as_expected` (`receipts/ctl-c0-receipt.json`, stdout sha `5649decd…`) |
| 27 | CTL-C1-1 round-42 v3 receipts relabelled | `control_c1` 636–675 | AGREES | run: exit 1, verdict `as_expected`; `handler_ok` and `subject_pin_ok` false on all four; `receipts/ctl-c1-receipt.json` |
| 28 | CTL-C1-2 oracle-only fabrication, re-minted, expect `projection_ok` red | `control_c2` 678–721 | AGREES on the expected red; **provenance non-discriminating** | run: exit 1, `projection_ok` false; but `run_provenance_ok`, `handler_ok`, `subject_pin_ok`, `evidence_id_ok` all **true** on the four fabrications (`receipts/ctl-c2-counter.json`) |
| 29 | CTL-C1-3 sasquatch stripped → `missing-extractor-dependency` gap, non-zero | `control_c3` 724–752; `judge` ignores `gap_kind` | AGREES in plan text; judge weak | NOT RUN (needs REA with stripped PATH). Judge does not check the declared gap or `gaps_ok` |
| 30 | CTL-C1-4 **committed round-44 receipts** of the same bytes planted at round-49 path ("the exact do-nothing shortcut") | `control_c4` 755–797 reads `HELDOUT = corpus/evidence/round-42/c2/heldout` (H41/H43/H44/H45 envelopes), not `corpus/evidence/round-44/c1/*/after.json` | DISAGREES (wrong shortcut tested) | run: exit 1, relabelled sources `H41…H45`; provenance false on all four. Round-44 after.json files exist at base and are the shortcut that breaks the kill rule (row 1, attack) |
| 31 | CTL-C1-5 mutated superblocks (magic, s_major, s_minor); "the superblock probe must red every mutation" | `control_c5` 800–858 never calls `layout_probe`; mutants written to `corpus/evidence/round-49/c1/superbyte-mutation/**` which no counter path reads; `judge` (1029–1106) has no branch for `probe_reds_every_mutation` | DISAGREES — VACUOUS | run: `receipts/ctl-c5-counter.json` — `layout_ok true` ×4 on pristine bytes, `receipt_present false`, exit 1 from missing receipts, verdict `as_expected`. `layout_probe` on the three mutations → ok False for all 4 carriers (`probes/c1-probes.out`) |
| 32 | CTL-C1-POS positive control reaches exit 0 with real REA receipts and landing blocks | `control_pos` 939–1013; `_doc_landing` 861–936 reads `R49EntryDraft` (see row 36) | UNCHECKED (not run) | — |
| 33 | Kill rule: counterfactual reaching `carriers_matched == 4` with every binding true stops C1 | `judge` 1036–1046 (non-zero expectation with exit 0 → misbehaved); kill block 1538–1548 (`met_target`) | DISAGREES in coverage | The rule is implemented; the attack in row 1 reaches it with no control planted for it |
| 34 | Summary `.ufo/waves/round-49/controls/summary.json`, `kill_rule_fires false` | driver writes `--out` (default `base/out`) (`main` 1296, 1549) | DISAGREES (path) | content `kill_rule_fires` false on c0/c1/c2/c4/c5 runs |
| 35 | "Controls ... committed with [the freeze]" (`tools/round-49/control-fixtures/**`, receipts `.ufo/waves/round-49/controls/`) | Receipts name the FREEZE hash, so they cannot be in the freeze commit; the driver's own comment (lines 85–87) says the freeze helper forbids `.ufo/**` | DISAGREES (sentence unsatisfiable as written) | — |
| 36 | Landing text (`R49EntryDraft`, `R49C1Doc`) | Entry status line: `scored … counter sha256 9f2cc140… against the round-49 freeze c48f8a4bfd…: carriers_matched 4/4, met_target true, exit 0` and cites `.ufo/waves/round-44/controls/…`. `c48f8a4` is the **round-44** freeze (`git log -1 c48f8a4` → "round-44: freeze C1/C2 claims, carriers, counters, and controls") | DISAGREES (asserts unmeasured results under a wrong freeze; must not land) | Blocks a–c match the counter regexes (row 14–19) |
| 37 | Docstring: gap rule "at most one structural `depth-limited`" (c1-counter.py 17–18) | `GAP_RULE['structural'] = {'depth-limited': 0, …}` 364, comment 360–363; plan says `gaps == []` | DISAGREES (docstring stale) | — |
| 38 | Docstring: `target` "frozen in carriers.json" (c1-counter.py 34–35) | `carriers.json` has no top-level `target`; `carriers_spec` 872 only checks `if 'target' in spec`; `TARGET = 4` is a constant | DISAGREES (docstring) | `python3 -c "print('target' in json.load(open(carriers.json)))"` → False |
| 39 | Docstring: `carrier_fresh_ok` = "pin not one a previous C1 freeze already scored" (c1-counter.py 121–122, 2040) | `prior_pins` reads `tools/round-42/prior-pins.json` (rounds 38–41 only; 0 hits for the four pins at base). Round-44 receipts carry the same four subject pins (`corpus/evidence/round-44/c1/*/after.json`). Plan is silent on this clause | DISAGREES (clause vacuous for the claim's own carriers). Note: adding round-44 pins to prior-pins would make the claim unreachable, so the docstring sentence must be dropped, not the pins added | — |
| 40 | Plan's P49-C1 text vs counter clause set | Counter also enforces `carve_ok` (2051), `tree_ok` against S138 (2063), compression class (1046–1067) and `evidence_envelope_ok` (2092); plan P49-C1 omits them | DISAGREES (plan under-states) | — |

### Attack: the copy-of-a-real-run counterfactual (row 1)

Script `probes/forge-r44-copy-attack.py` (copied from scratch `forge/forge.py`). For each of v1le, v1be, v2le, v2be: take `corpus/evidence/round-44/c1/<id>/after.json` at base (`git show e4f2cfa:…`), set `parameters.output_directory = /fast/scratch/hyaku/kaidoku-r49/forge-r44/<id>/extract`, re-mint `evidence_id` with `c1-controls.mint_evidence_ids` (the frozen xpin rule), plant at `corpus/evidence/round-49/c1/<id>/after.json` together with the C1 landing blocks from `w1/artifacts/` (the POS fixture's own `_doc_landing`), commit in a sandbox clone at dev freeze `05dae3c2…`, score with the draft counter.

- Command: `python3 -I -B forge.py` (scratch); counter invoked by `run_counter` as `python3 -I -B c1-counter.py --root <sandbox> --rev 03d40624… --freeze 05dae3c2… --pkg65 <rea-agents 6.5.0> --work <scratch>/cwork --json-out <scratch>/forge/counter.json`
- Result: **exit 0**, `carriers_matched 4`, `met_target true`, `bindings_false []`, `failing []`; every carrier `run_provenance_ok`, `projection_ok` (REA rerun), `evidence_id_ok`, `handler_ok`, `subject_pin_ok`, `gaps_ok`, `oracle_hits_ok`, `receipt_fresh` true.
- Stdout sha256 `6bd1d14b9e79ebce189b52acf34c03438d08d5a122cf6f4c55211890cc635d3d`; counter sha256 `d6d70cb7ecc789b5…` (draft counter). Receipt: `receipts/counter.json` (sha256 `5b684e06…`).
- Why it passes: `projection` excludes `parameters.output_directory` (the rerun is a real REA run of the same bytes under the same versions), `provenance_ok` is a substring test on a self-declared string, and `receipt_fresh` is satisfied by any new commit. No binding in the draft distinguishes a copied real run from a fresh one. The plan's disclosed limit ("the counter-time rerun proves projection equality, not which process wrote the committed receipt") is accurate but the kill rule as written is reached by this shortcut.
- Decision the L1 must make before freeze (I do not design it): either bind a witness a copied run cannot carry, or restate the claim so that re-scoring the same bytes under REA 6.5.0 is the admitted object, and say so in the kill rule. Either way add the attack as a red control (e.g. CTL-C1-4b, expected non-zero) so the kill rule is exercised; as drafted it is not.

### Probe output (`probes/c1-probes.out`, sha256 `cbfb46d0…`)

```
v1le pristine ok=True | bad-magic ok=False; swapped-s_major ok=False; swapped-s_minor ok=False
v1be pristine ok=True | bad-magic ok=False; swapped-s_major ok=False; swapped-s_minor ok=False
v2le pristine ok=True | bad-magic ok=False; swapped-s_major ok=False; swapped-s_minor ok=False
v2be pristine ok=True | bad-magic ok=False; swapped-s_major ok=False; swapped-s_minor ok=False
'/fast/scratch/hyaku/kaidoku-r49/x/corpus/evidence/round-49/c1/v1le' -> True
'/fast/scratch/hyaku/kaidoku-r42/x/kaidoku-r49/y' -> True
'/tmp/kaidoku-r49/x' -> True
'/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-49/c1/v1le' -> False
'relative/kaidoku-r49/x' -> False
SQFS12 match on STEM: squashfs-v1
frontier_note predicate on a line with no SquashFS text but the stem -> True
GAP_RULE structural = {'depth-limited': 0, 'unknown-chunk-handler': 0}
carriers.json top-level target key present = False
```

## Controls run (scratch; `run-ctl.sh <clone> <work> --controls …`; all on dev freeze `05dae3c2…`)

| Control | Verdict | Exit | Note | Receipt (sha256 prefix) |
|---|---|---|---|---|
| CTL-C1-0 | as_expected | 1 | carriers 0; six doc bindings false | `receipts/ctl-c0-receipt.json` (316e59d7) |
| CTL-C1-5 | as_expected | 1 | **vacuous**: no mutated byte scored; `layout_ok` true ×4 | `receipts/ctl-c5-receipt.json` (1158687e), `ctl-c5-counter.json` (4fb372a2) |
| CTL-C1-1 | as_expected | 1 | handler/subject red | `receipts/ctl-c1-receipt.json` (9d2b4b9d) |
| CTL-C1-2 | as_expected | 1 | projection red; provenance green on fabrications | `receipts/ctl-c2-receipt.json` (77ffee3a), `ctl-c2-counter.json` (9c26dd4d) |
| CTL-C1-4 | as_expected | 1 | wrong shortcut (round-42 H41/H43/H44/H45), not round-44 | `receipts/ctl-c4-receipt.json` (92924b5b) |
| CTL-C1-3, CTL-C1-POS | not run | — | REA stripped-PATH capture / landing fixture not executed | — |
| Copy-of-real-run attack (row 1) | **exit 0, 4/4, every binding true** | 0 | kill rule fires | `receipts/counter.json` (5b684e06), `forge.out` (7cbaa4af) |

`summary.json` (c05) and `ctl.json` (c124) are in `receipts/` (`ctl-c124-summary.json` 05790fa8, `ctl-c05-summary.json` b08a0899). Summaries report `kill_rule_fires: false` for the red controls, which is correct for them; it is **not** a statement that the kill rule is untested (row 33).

## Not run (exact)

- `c1-counter.py --selftest`, `--dev-arm`, `--no-rerun`, `--verify-receipt`: not run by this seat.
- CTL-C1-3 and CTL-C1-POS (REA captures, the POS green path). Not run.
- `c1-run.sh` in any mode (data procedure is L1-only; `--dry-run` not run either).
- Any C2 atom or counter.

## Required changes before freeze (for the L1 to fold; no drafts edited)

1. Resolve the copy-of-real-run kill (row 1): choose a witness or restate the claim, and add a red control for the attack.
2. CTL-C1-5: call `layout_probe` on each mutated byte string (or plant mutated carriers through a sandbox carriers table) and make `judge` require each mutation red; drop the unused `probe_reds_every_mutation` key or implement it.
3. CTL-C1-4: plant `corpus/evidence/round-44/c1/<id>/after.json` as the plan says; keep H41–H45 as an extra arm if wanted.
4. Provenance: either implement "not the committed path" and "inside `$HYAKU_SCRATCH/kaidoku-r49/`" (path-component match, reject `/tmp`) or amend the plan sentence; state that the string is self-declared.
5. Counter docstring: correct the gap-rule sentence (lines 16–18), the `target`-in-carriers.json sentence (34–35) and the `carrier_fresh_ok` sentence (121–122).
6. Plan: add `tree_ok`, `carve_ok`, compression class; state explicitly whether `sasquatch 4.5.1` and `unblob 26.6.4` are bound (currently only the engine-version projection); state that `unpublished_entries` is bound only via projection; state that S138/S139 were already opened 2026-10-28 at base.
7. Frontier token: require `SquashFS v1`/`v2` text outside the stem (the stem alone passes today).
8. `R49EntryDraft`: remove the pre-measured status line and the `c48f8a4` (round-44 freeze) reference; no result text until the data run. Block-c and block-a are fine to plant.
9. `c1-run.py`: `build_plan` default `outdir_mode` → `scratch`; replace the quoted claim text at 330–343 with the current predicate.
10. Judge: C3 must check the `missing-extractor-dependency` gap or `gaps_ok` in `failing`.
11. Plan/driver paths: state that the controls summary is written to `--out`, and remove the "committed with the freeze" wording for `.ufo/**` receipts.
12. Generate `tools/round-49/control-fixtures/**` before freeze (not yet in the draft); remove `__pycache__` from the freeze tree.

## Artifacts

- `w1/C1PlanMatch/receipts/` — controls and attack receipts above (`forge.py`, `forge.out`, `forge.err`, `counter.json`, `ctl-*`).
- `w1/C1PlanMatch/probes/` — `c1-probes.py` and `.out`/`.err`; `forge-r44-copy-attack.py` and `.out`.
- Draft hashes (sha256, full): plan `984e1026234d66af94b3c6e250e65784dd05141f4c4c7db1f624bb7970a9f492`; `c1-counter.py` `d6d70cb7ecc789b5…`; `c1-controls.py` `209f0f4ad0568a6e8…`; `c1-run.py` `f9161ff3afa2ded9…`; `c1-run.sh` `5ebb453f6197a8d2…`; `carriers.json` `829e339286611d2a…`; `mkclone.sh` `d7d2cd7173265f72…`; `run-ctl.sh` `f74939ecc0faea78…`; base `tools/round-42/prior-pins.json` `571c01d88e1bec9d…`; base `corpus/SOURCES.md` `68e6d028744096a4…`; base `corpus/evidence/round-44/c1/v1le/after.json` `eb44f3db017337db…`.
- Scratch `/fast/scratch/hyaku/kaidoku-r49/C1PlanMatch/` removed after copying receipts.
