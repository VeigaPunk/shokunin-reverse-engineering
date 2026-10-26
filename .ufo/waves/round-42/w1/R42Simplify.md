# R42Simplify — YAGNI review of the round-41 tools that round 42 would port

**Verdict: DONE** — 24 ranked removal candidates (~1,300 of 8,042 lines, ≈16 %), 3 latent
under-bindings the port must *add* rather than keep, 5 draft clauses that collide with the code and
must be re-worded at the freeze. No lane file touched: only this report and
`.ufo/waves/round-42/w1/artifacts/R42Simplify/`.

Seat: simplifier (wave 1, pre-freeze). Item: list clauses/options/code no round-42 claim needs
(AVM-only probes a v3 carrier never reaches, dead profiles, unused CLI options, duplicated checks)
and the selftest cases that only test removed code — each ranked by safety, with the P42 clause a
removal would weaken. Edit nothing in the lane.

---

## 1. Method and evidence

Read at the base commit `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (lane HEAD during review was
`ae5dc3f39c3374cb683fa05eb5fd069dda10d376`; the three blobs are unchanged from the base — the round-41
wave-2 commits after `c4a38ea2` do not touch `tools/round-41/`):

    git -C …/kaidoku-shokunin show c4a38ea2:tools/round-41/c1-counter.py    → bbabbfec…f8845cfc  3413 lines
    git -C …/kaidoku-shokunin show c4a38ea2:tools/round-41/c2-counter.py    → c6c1ea64…98720af8  2499 lines
    git -C …/kaidoku-shokunin show c4a38ea2:tools/round-41/heldout-gen-v3.py → 652d71af…77d97e00 2130 lines

and `git -C …/kaidoku-shokunin log --oneline c4a38ea2..HEAD -- tools/round-41` prints nothing, so the
base blobs are still the working-tree blobs.

Every line number below is `file:line` **at that commit**. Inputs read: the draft
`plans/round-42-claims.md` (whole), `corpus/lessons/round-41.md` `## Routed defects into round 42`,
`corpus/lessons/round-41-verifier-spotcheck.md` §5, the frozen round-41 `carriers.json` /
`gap-rule.json`, the claims' P41-C1 predicate, and the installed unblob 26.6.4 handler source
(`…/unblob/handlers/filesystem/squashfs.py`) for the v3 superblock and handler names.

Two findings are machine-proven, offline, in `probe-c1.py` → `probe-c1.out` (exit 0; run as
`python3 -I -B probe-c1.py ./c1-base.py`):

    parse_oracle rows = [('usr/info.txt', 'aaaa…')]   err = None
    row width kept = 2 (rel, sha256) - size discarded
    oracle_hits(wrong size, right sha) = 1
    layout_probe(v3 LE) = magic hsqs, major 768, version_v4 False, ok False
    layout_probe(v3 BE) = magic sqsh, major 3,  ok False
    v3 bytes[20:22] read as v4 `compression` = 0

Oracle readiness spot-check (MIT fixture, fetched to scratch and discarded — URL + sha256 in
`base-blobs.txt`): `unsquashfs 4.7.5` prints `Found a valid little endian SQUASHFS 3:0 superblock`
and both readers agree on the file list (6 B / 7 B), so the counter's `oracle.tsv` contract needs no
new dialect work.

## 2. What the port must keep (contract preserved)

Only these parts of the three files are load-bearing for a P42 clause; everything in §3 is ranked
against them.

| code | P42 clause it serves |
|---|---|
| `git`/`show`/`first_add`/`is_ancestor`/`frozen_drift` (c1:345-357,1144-1188,1193-1207) | receipt first added after the freeze; "no frozen C1 path changed after the freeze" |
| `carriers_spec`, `parse_oracle`, `parse_nonregular`, `gap_rule_model`, `disposition_check` (c1:426-583,584-674,1022-1142) | the gap-rule accounting clause (one `unpublished-entry` gap or one `MaliciousSymlinkRemoved` per symlink; devices/dirs invisible; ≤1 structural `depth-limited`; no `unknown-chunk-handler`) |
| `squashfs_roots`/`subject_root`/`extract_rel`/`same_rel`/`diagnostic_rel` (c1:843-974) | "publishes every regular file … at its exact relative path under the chunk extract root" (R40-CL1 / D5 segment-bounded roots). The *prefix* becomes `squashfs_v3`; the algorithm stays |
| `evidence_ids` + xpin (c1:389-424) | "recomputes its evidence id" |
| `make_real_runner` + `REPLAY_PARAMS` (c1:1403-1466) | "a counter-time REA rerun has the same projection" (depth replay is what makes it about the image, not the flags) |
| `projection` core six fields (c1:1235-1360) | same clause |
| freeze integrity, writer scope, regeneration-bytes, manifest ordering, pair scoring, feature binding, `v4` block identity (c2:264-296,397-430,1163-1300,1356-1394,1486-1532) | P42-C2 bindings: byte-identical regeneration, manifest after freeze, interpreter==evaluator, `declared_features` |

## 3. Removal list, ranked by safety

Full machine-readable form with every span: `removal-spans.tsv`. Three bands: **A** = pure deletion
(no P42 clause contact), **B** = delete and re-word the draft (the code clause has no round-42
counterpart), **C** = delete and replace (the claim needs different code; porting as-is would
under-bind).

### Band A — pure deletions (no clause weakened)

| # | what | where | why round 42 does not need it |
|---|---|---|---|
| 1 | `--no-rerun` | c1:1755,1763-1770 | a mode the predicate explicitly refuses; only exits 2 |
| 2 | `frontier_note` binding, `FRONTIER_MARK`, AVM token in the PROVINCE row check | c1:315,318,1691,1695-1697 + 2 cases | P42-C1's docs clause is PROVINCE row + entry + README row + SOURCES row; no frontier note. Risk: the row predicate must lose *only* the AVM token, keeping "first cell names the family" |
| 3 | `compression_coverage` + `GZIP_ID`/`XZ_IDS` | c1:298-299,1712-1717,1732-1733 + 1 case | v3 superblocks have no compression field (`squashfs3_super_block_t`, unblob squashfs.py:281-315) and v3 is gzip-only, so "≥1 gzip **and** ≥1 xz id" can never pass. Also kills the draft's word "compression" (§5.1) |
| 4 | three of four projection profiles; `PROJECTION_KEYS_BY_PROFILE` | c1:1370-1400, branches 1247-1260/1285-1330 + 3 cases | P42-C1 binds one projection. Risk: keep exactly one profile **after** a stability re-measure on v3 bytes; shipping `plus-extractor` unmeasured risks `projection_ok` false negatives |
| 5 | `run_provenance_ok`, `PROV_SEGMENT`, `provenance_ok` | c1:294,768-776,1628-1631 + 2 cases | not named in P42-C1; receipt reuse is already blocked by `receipt_fresh` + the hashed evidence id |
| 6 | `receipt_paths`, `extract_root_confirmed`, `chunk_roots` | c1:794-828,1610-1619,893-897 | reporting only — none is in `CLAUSES` (c1:321-327) |
| 7 | `carriers_unchanged` / `gap_rule_unchanged`, and their conjuncts in `met_target` | c1:1496-1497,1737-1739 | duplicated by `frozen_drift` (both paths already in `FROZEN_PATHS`, c1:302-313), which is stricter — it catches change-then-restore |
| 8 | `MARKER_V2` + `v2_marker_at_rev/freeze` + its case | c2:122,1145-1146 + 1 case | round 42's predecessor block is v3; the v2 marker is two generations back |
| 9 | `advisory_rea_params`, `DEPTH_CLASS_PREFIX` | c2:178-179,1465-1483 | declared `binding: False`; P42-C2 binds no REA parameter |
| 10 | 2 of 3 `ACTION_SETS` (`tabledraft`, `actionreview`), `--actions-set`, `action_set`/`action_vocabulary` manifest fields | gen:157-200,204-209,2039-2046,2065-2072 | one frozen action vocabulary; carriers never depend on tokens. Keep `--actions-file` (binds the manifest to the SKILL action line — worth keeping) |
| 11 | generator-side `--verify` + `verify()`/`feature_diff`/`observed_features()` | gen:1858-1917,2033-2035 | recomputes exactly what the counter's `observed_features_match_declared` scores on the frozen set; the counter's dev dry run is the QUALITY-84 instrument |

### Band B — delete and re-word the draft (the code clause has no round-42 counterpart)

| # | what | where | the draft wording that must change |
|---|---|---|---|
| 12 | the AVM marker / little-endian-metadata branch of `layout_probe`, `UNCOMPRESSED_FLAG`, `METADATA_MAX`, `sb_carrier`'s `marker`/`meta_le` args, and the 6 layout-case *fixtures* | c1:682-766 (marker+meta half), 296-297, 1814-1852, 2341-2365 | proven unreachable: a v3 superblock fails at `version_v4` and its offsets ≥32 differ, so no v3 carrier can ever reach `marker`/`layout_le`. P42-C1 keeps "magic/major" and adds "the one frozen per carrier" (§5.1). Replace with a v3 probe reading `s_magic` (per variant: `hsqs/sqsh`, `shsq/qshs`, `hsqt/tqsh`, `zlqs/sqlz`) and `s_major == 3`. `sb_carrier` itself must stay (every other case builds its fixtures with it) — only its AVM arguments and field offsets change, so the six cases are rewritten, not dropped |
| 13 | `REAL_LABEL = 'depth-limited'` | c2:150-151,1570 + 1 case | P42-C2 says the round-41 C1 receipts "get the **evaluator's pair**"; a hard-coded label re-introduces a bound the v4 precedence may not give. Keep evaluator==interpreter; re-point `REAL_RECEIPTS` (c2:146-149) from round-40 to the round-41 C1 receipts |
| 14 | `class_map_agreement`, `class_expected` read (`_pair` of `class_expected`), 3 `CE_*` cases | c2:1356-1382,1236,2255-2275 | not bound in P42-C2, and `class_expected.features` is the exact key R41-CL1 forbids as a declared-tuple source. Delete the read entirely; if a cross-check is wanted, the evaluator must emit it |
| 15 | `decisions_reported`, `row_decisions_consistent`, `distinct_decisions/rows`, `label_action_vocabulary`, `row` plumbing, 2 cases | c2:1396-1431,1443-1454 | the claim binds `(label, action)` pairs only; the row-reporting contract disappears with the interface ladder (#20) |
| 16 | `external.member`/`member_sha256`/`nested.*` spec keys and their checks | c1:628-669 + vendor-chain block 2916-2959 | this chain describes a FRITZ!OS *tar member*. DD-WRT `tqsh` (handler `squashfs_v3_ddwrt`, unblob squashfs.py:318-361) and OpenWrt images are themselves images with an interior squashfs; the reproducible chain becomes url → image sha256 → carve(offset,length) → carrier sha256. P42-C1 binds only "the carrier bytes hash to the pin", so this is a replace, not a loss |
| 17 | `combo_declared`'s v4 handler sets; `expected_features`'s endian→`squashfs_v4_*` map | gen:411-441,542-570 | P42-C2 adds "a widened `combo` family whose factors include the handler family" and legacy classes. The map must take the handler family as data; today `endian='le'` can only mean `squashfs_v4_le` |

### Band C — delete and replace (porting as-is would under-bind a P42 clause)

| # | what | where | the clause it would weaken |
|---|---|---|---|
| 18 | `parse_oracle`'s "≥2 columns" tolerance and the discarded size column; `oracle_hits`' sha256-only comparison | c1:426-452,1001-1009 | **P42-C1: "the same sha256 and size."** Proven: a row `rel, sha, 999999` parses, and a published file of the same sha with size 1 scores a hit (`probe-c1.out`). Require 3 columns and compare size |
| 19 | `handler_ok = HANDLER in chunk_handlers(env)` | c1:287-288,1569 | **P42-C1: "names a `squashfs_v3*` handler (the one frozen per carrier)."** Membership accepts a second, different handler; compare the exact frozen per-carrier handler name |
| 20 | the frozen-tool interface ladder: `run_interpreter`'s 4 argv probes + `--table-only`/`infer_index_base` row recovery, `run_evaluator`'s 5 argv probes, `parse_json_results`/`parse_tab_results`/`parse_table_only`/`parse_eval_pairs`/`_pair`/`norm_id` (mostly), and 8 green interface cases | c2:464-475,656-981,2283-2298 | not a weakening but 326 lines + 8 cases of compatibility with tools nobody has frozen yet. Round 42 freezes `sqfs-triage-v4.py` and `indep-eval-v4.py` **in the same commit as the counter**, so the CLI is a contract: one call each, a mismatch exits 2 loudly. Also record both tools' sha256 in the receipt (D4) — the ladder currently records only which interface answered |
| 21 | `selftest_rea` + `DEV_AVM_IMAGE` (sasquatch-v4be on the round-11 AVM image) | c1:300-301,3238-3413 | the dev arm for a v3 round is a legacy fixture, not an AVM image. Replace with a real-REA check on the pinned v3 fixture; the QUALITY-84 dry run still needs *a* real dev arm |
| 22 | generator `carriers[].declared` + `declared_schema.location`; counter's declared-key preference chain (`class_features`, `classes_features`, `feature_tuples`, `features_by_class`, `class_tuples`) and per-carrier mirrors (`class_expected.features`, `features`) + `FEATURE_ALIASES` | gen:1372,1464,1807-1822; c2:160-173,1486-1506,1516-1523 | **R41-CL1, and P42-C2's "ONE key (`declared_features`), read by the counter under exactly that key."** Confirmed at code level: the generator writes `declared`, the counter never reads `declared` (0 hits), and today's pass comes from `class_expected.features` — the very duplicate the fix forbids |
| 23 | `PLANNED_CLASSES` (20 names), `classes_cover_planned`, `COMBO_COUNT = 12`, `combo_family_wellformed`'s `C%02d` shape, 2 cases | c2:128-145,152,1098-1103,2350-2352 | P42-C2's held-out set adds legacy classes and *widens* combos; a hard-coded 20/12 makes `classes_cover_planned` false and `matched == n` unmeasurable. Keep the *idea* (a non-vacuity guard) with the v4 class list and `len(combos)` from the manifest's `families.combo.count` |
| 24 | `PRIOR_CARRIERS = '.ufo/waves/round-40/c1/carriers.json'` | c1:290,1157-1188 | CTL-C1-1 relabels **round-41** receipts; the freshness clause still needs the mechanism, pointed one round later |

**Approximate line totals** (def-boundary spans, [INFERENCE] as a count): A ≈ 330, B ≈ 360, C ≈ 610 —
≈ 1,300 lines, 16 % of 8,042. The single biggest item is #20 (326 lines + 8 cases); the biggest
*risk-reducing* items are #18, #19, #22.

## 4. Selftest cases that only test removed code

- c1 `--selftest`: 97 `add()` cases (c1:2285-3113) + `--selftest-rea`. **8 cases die outright and 6
  are rewritten with Band A/B.** Die outright: 1 `no xz carrier (compression coverage)`, 3 profile
  (`explicit core profile …`, `default profile (plus-extractor) …`, `unknown projection profile in
  carriers.json`), 2 `frontier note …`, 2 provenance (`foreign scratch provenance`, `provenance path
  climbs out`). Rewritten on a v3 superblock fixture (intents survive): `marker-stripped …`,
  `standard-BE carrier`, `metadata length plausible both ways`, `ambiguous length settled by
  identity`, `little-endian superblock magic`, `bytes_used beyond the file` — the last one still
  tests a real v3 field. Plus `selftest_rea` (#21). Everything else maps to a surviving clause:
  exact-path (7), two-root ambiguity (4), removal disposition (7), freeze integrity (8), structural
  gaps (4), vendor spec chain (1, re-pointed by #16).
- c2 `--selftest`: ~70 cases (c2:2274-2416). **13 die**: 8 interface greens (`answers through
  --envelopes`, `emits tab rows`, `names rows only`, `numbers rows from 1`, `evaluator emits a
  wrapped labels map`, `evaluator emits a result list`, `evaluator prints a table and writes
  --json-out`, `json results without a row index`), 3 `class_expected` report cases, 2 row/decision
  cases (`correct rows plus a final * unclassified row`, `interpreter reports neither a pair nor a
  row`). The `feat_mismatch` / `feat_absent` / `combo_feat_mismatch` reds **must be re-pointed** at
  `declared_features`, not deleted — they are the R41-CL1 regression tests.
- gen `--selftest` (determinism, gen:1923-2020): nothing to delete; "carriers regenerate
  byte-identically" is a P42-C2 binding.

## 5. Draft clauses that collide with the code (freeze must re-word)

1. **P42-C1 "superblock reads the frozen magic/major/compression".** v3 has no compression field and
   is gzip-only; the counter's only data path to a "compression" value is the v4 field at `20:22`,
   which on a v3 image is `inode_table_start_2`'s high half (probe reads 0). Drop "compression" or
   replace it with `s_minor`/`block_size`.
2. **P42-C1 "the one frozen per carrier"** is stricter than `handler_ok`; the counter must be
   changed, not the claim (#19).
3. **P42-C1 gap accounting vs `removed.silent`.** The code admits a symlink row with *no* record if
   the frozen rule lists its kind+detail under `removed.silent` (empty-target links, unblob
   extractor.py:68-71). The draft says every non-regular row is accounted by one gap *or* one
   diagnostic. A real vendor rootfs with an empty-target link would fail the draft but pass the code
   — decide at the freeze: keep `silent` and re-word, or forbid it and lose such carriers.
4. **`--max-depth 1` is not bound anywhere.** `REPLAY_PARAMS` (c1:1403-1406) replays the receipt's
   *own* parameters, so a depth-3 receipt is self-consistent and passes. The round-41 frozen
   `carriers.json` even carries a `rea_parameters: {max_depth: 1}` block that **nothing reads** (0
   hits in the counter). If round 42 freezes the same block, either bind it against
   `parameters.max_depth` per receipt or drop the block as decorative data.
5. **"the round-41 v4 classes"** (P42-C2) is ambiguous: all 20 round-41 class names remain reachable
   under the v4 precedence (rules 1-13), so none can be deleted — the choice is whether the v4
   held-out set keeps all 20 plus the new legacy classes or re-scopes them. The generator's
   `EXPECTATIONS` (gen:456-528) can be kept wholesale only if that is decided; its `handler`/`be`
   fields are v4-only and need the family as data for the legacy entries (#17).

## 6. Tradeoffs and open decisions for the L1

- Removing #20 trades fallback tolerance for a loud exit-2 on interface mismatch. That is the right
  trade only if the counters and both frozen tools land in one commit (they do), and if the receipt
  records each tool's sha256 (D4) — otherwise a future reader cannot tell which interface was scored.
- Removing #4 (3 profiles) should be paired with one measured run of the chosen profile on a v3 dev
  carrier; the round-41 stability evidence (`projection-profiles.json`) was measured on AVM v4 bytes.
- Removing #11 keeps the dev proof only in the counter. QUALITY 84 already requires the frozen
  counter's dry run on the dev arm, so this concentrates the instrument in one place; the cost is
  that a generator-side broken tuple is discovered later (still before the freeze).
- Removing #16 forces the carrier spec to name a carve (offset + length) even when it is 0. Keep at
  least `image_sha256` + `length`; a published image is not redistributable, so the fetch chain is
  the only reproducibility the artifact has.
- Keep `receipt_fresh`/`first_add`: it is the one clause that stops a relabelled round-41 receipt
  from scoring, and it is cheap.

## 7. Compliance

- No write outside `.ufo/waves/round-42/w1/R42Simplify.md` and
  `.ufo/waves/round-42/w1/artifacts/R42Simplify/`; no `git`/`jj` mutation (read-only `show`/`log`/
  `rev-parse` only); no VCS commands against a modified tree, so no clone was needed.
- No REA, unblob, sasquatch or unsquashfs run on any published image, and no third-party firmware
  copied anywhere: the only image touched was the MIT unblob 26.6.4 fixture (a designated development
  input, never a C1 carrier), read with `unsquashfs -s`/`-lls` and `7z l` in scratch and deleted
  afterwards. No tool installed or upgraded (nothing was missing: `unsquashfs 4.7.5`, `7z 26.04`,
  `python3` were already present, and this seat needs no extractor).
- Scratch `S=/fast/scratch/hyaku/kaidoku-r42/R42Simplify` removed before yielding; everything cited
  here is either a line number at `c4a38ea2` or a file in the artifacts dir
  (`removal-spans.tsv`, `base-blobs.txt`, `probe-c1.py`, `probe-c1.out`).
