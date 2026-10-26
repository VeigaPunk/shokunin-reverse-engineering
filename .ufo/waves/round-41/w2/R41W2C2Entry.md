# R41W2C2Entry — review of `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md` against the frozen interpreter, SKILL block 20 citations, committed evidence, and the R41-C2 honest stop

**Verdict: DEFECTS FOUND.** I attacked the knowledge entry for `2026-10-26-r41-sqfs-triage-v3.md` (round 41, C2 landing reference): its grammar statements vs the frozen interpreter `tools/round-41/sqfs-triage-v3.py`, the line-range citation(s) SKILL block 20 makes into it, its measured numbers vs committed evidence, and any claim the honest stop of R41-C2 (NOT MET) now contradicts.

Result: all grammar claims, the single citation `:11-25`, and every committed number in the entry verify exactly. Two defects found: (1) the entry's held-out composition enumeration is stale and does not sum to 52 — it lists 18 named classes while the frozen generator and manifest have 20; (2) the entry defines the H feature as "the `squashfs*` chunk handlers", which matches the interpreter but not the frozen claim text and evaluator (chunks ∪ gap handlers) — inert on the scored set (52/52) but a documentation/authority discrepancy. The honest stop's failure (`observed_features_match_declared` false) is a manifest↔counter key contract gap the entry never addresses; it contradicts nothing the entry tests, and a spot check shows the binding would hold if the counter read the `declared` key.

---

## 1. What I checked and how

Read-only investigation. Lane root used throughout: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. No git/jj mutation, no writes outside the report + artifacts paths, no subagents, no background jobs. Interpreter recheck run read-only (`--table-only`).

Sources examined:
- `tools/round-41/sqfs-triage-v3.py` (docstring, `_parse_set_cell`, `_parse_handler_cell`, `parse_table`, `features`, `match_set`, `rule_matches`, selftest cases).
- `SKILL.md` block 20 (lines 380–460) and full-file grep for citations to the entry.
- Entry `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md` (all 111 lines).
- Committed scoring: `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`; controls `.ufo/waves/round-41/controls/c2/dev-scores-prefreeze.json`; held-out manifest `corpus/evidence/round-41/c2/heldout/manifest.json` (52 carriers); four round-40 C1 receipts `corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json`.
- Wave-1 measured artifacts `.ufo/waves/round-41/w1/artifacts/R41C2TableDraft/`: `a-heldout-26.tsv`, `c-combined.tsv`, `ctl-exact-c-combined.tsv`, `ctl-exact-b-c1-4.tsv`, `b-c1-4.tsv`, `checks.py`, `v3-refparse.py`, `l2-wrapper-measurement.md`.
- Round-40 sources cited by the entry: `.ufo/waves/round-40/w2/R40W2C2AxisFit.md` F6, `.ufo/waves/round-40/w1/R40MistakeHunt.md` MH-6 + `artifacts/R40MistakeHunt/avm-measurements.txt`, `.ufo/waves/round-40/w2/R40W2C2IndepEval.md` §6.
- Installed trees for S112/S118/S119/S120 line citations: unblob 26.6.4 (`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/`), rea-agents 6.5.0 (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`).
- `tools/round-41/heldout-gen-v3.py`, `tools/round-41/indep-eval-v3.py`, `tools/round-41/c2-counter.py`.

Tool availability note: no `lsp` device is mounted in this session, so semantic checks were done by direct code reads (not text-grep substitution for semantics — the code itself was read).

## 2. Grammar statements — CONFIRMED (entry vs frozen interpreter)

Entry claim (1): contains form only on gap kinds; `none` = empty set; deps exact-set by name, never substring.

- `parse_table` wires `_parse_set_cell(gap, 'gap kinds', contains=True)` and `_parse_set_cell(dep, 'dependencies', contains=False)` — the contains form exists ONLY in the gap-kind column (sqfs-triage-v3.py lines 406–407).
- `_parse_set_cell` (260–297): `*`/`none` reserved; contains form only when `contains=True` and cell ends `+` (`a,` join, no empty member, no duplicates, no reserved members); exact form is `a+b` join; both reject malformed cells with TableError (exit 2).
- `match_set` (650–658): `none` → `not values`; `contains` → `payload <= frozenset(values)`; exact → equality. So `none` = empty set, contains tolerates extras, exact rejects extras. Matches the entry's wording exactly.
- Dependencies: parsed with `contains=False`; matched by `match_set` equality on names; `fnmatch` is used only for handler patterns (rule_matches 670–672), never for deps. "Compared by name, never substring" holds.
- Selftest enforces these semantics: `c_contains_*`, `c_exact_*`, `c_none_gap_*`, `c_star_gap_*`, `c_deps_cell_has_no_contains_form` (rejects `sasquatch+` in deps), malformed-contains cases.

Entry claim (2): reader parses SKILL.md, no embedded table copy (R40-CL5 M1).

- Interpretation has no `TABLE_BLOCK`; selftest `c_no_embedded_table` asserts the module text contains no table, and `c_print_table_removed` asserts `--print-table` is gone. Docstring §3 states the same.

Entry claim: handler cell `none` means "no chunk handler starting `squashfs`"; a v1–v3-only chunk matches no row and lands `unclassified`, diverging from precedence step 2 (`no-squashfs-chunk`).

- `_parse_handler_cell` returns `('none', None)` for `none`; `rule_matches` fails the row when `feat['H']` is non-empty. `features()` builds H only from `normalized_result.chunks[].handler` values starting with `squashfs` (so v1–v3 handlers ARE in H). Row 1 (`no-squashfs-chunk`) uses handler `none`; all other rows require `squashfs_v4_*`. Hence a v1–v3-only envelope matches no row → `(unclassified, none)` — exactly as the entry states. The interpreter's docstring Limits ("A handler cell is a positive match: no cell can say 'no handler matching a pattern'") states the same limit. CONFIRMED.

Also verified: "Twelve rows carry twelve labels and twelve action tokens" — SKILL block 20 has 12 rows; actions line declares 12 tokens; `--table-only` prints `rules: 12`, marker line 434, actions line 435, table line 436, exit 0 (matches the entry's recheck line; `v3-refparse.py` fallback artifact exists).

## 3. Citation resolution — SKILL block 20 into the entry

- The ONLY line-range citation from SKILL.md into this entry is `SKILL.md:401`: `(corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:11-25)`. A full-file grep for the entry stem (`r41-sqfs-triage-v3`) returns exactly this one hit; the table rows' `source` columns cite S11x/S12x, round-39/40 entries, and c1/c2 data, never this entry.
- Resolution: entry lines 11–25 contain, verbatim in substance, the statements the SKILL sentence relies on: contains-form semantics for gap-kind cells ("a cell ending in `+` in `gap kinds` … is a **contains** test — the envelope's gap-kind set holds those kinds — while every other non-`*` gap-kind cell stays exact-set equality", lines 17–19), `none` = empty set (19), deps exact (20), no embedded copy (20–22), handler `none` semantics and the v1–v3 divergence (22–25). The SKILL sentence's second half ("instead of letting the first symlink row that happens to match absorb it") is a summary of the entry's later combined-gap-sets section (lines ~52–58), not of 11–25 — the citation anchors the grammar half and the mechanism half is consistent with the entry as a whole. No mis-citation found; the range is accurate for what it points at.

## 4. Measured numbers vs committed evidence — all CONFIRMED

| Entry claim | Committed evidence | Result |
|---|---|---|
| committed 26 round-40 envelopes score 26/26 unchanged | `a-heldout-26.tsv`: 26 rows, all `agree=yes` | ✓ |
| eighteen precedence-derived combined envelopes score 18/18 | `c-combined.tsv`: 18 rows, all `agree=yes` | ✓ |
| same block with every `+` stripped scores 7/18 on combinations | `ctl-exact-c-combined.tsv`: 7 `yes` (rows 4,7,15,16,17,18,19), 11 `NO` | ✓ |
| stripped block scores 0/4 on round-40 C1 carriers | `ctl-exact-b-c1-4.tsv`: 4 `NO` | ✓ |
| all four round-40 C1 carriers carry exactly `{depth-limited, unpublished-entry}` | direct read of `corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json`: kinds exactly `['depth-limited','unpublished-entry']`, handlers `['squashfs_v4_be']`, deps `[]`, files 697/8/7/6 (matches `b-c1-4.tsv`) | ✓ |
| MH-6: marker-stripped genuine AVM body — four files without the flag, zero with it | `artifacts/R40MistakeHunt/avm-measurements.txt` lines 14–15: `markerstripped noflag exit=0 files=4`, `markerstripped -be exit=1 files=0` | ✓ |
| L4/IndepEval §6: H21 publishes 5 files, 4 match oracle, fifth is 16384-byte truncation of a 19873-byte file | `R40W2C2IndepEval.md` lines 188–189 verbatim | ✓ |
| F6: v2 exact sets made H11+injected extractor-failure fall into `escaping-symlink-removed`/`expect-link-absent`, losing `salvage-partial` | `R40W2C2AxisFit.md` F6 (lines 124–136) verbatim | ✓ |
| L2: PATH wrapper `sasquatch-v4be` appending `-be` flips marker-only carrier from `extractor-failure`/`P=0` to three files sha256-identical to the tree | `l2-wrapper-measurement.md` runs 1–3: run 2 `G=∅`, `P=4` (WRAPPER-MARKER + alpha.txt/blob.bin/sub/beta.txt sha256-identical) | ✓ |
| controls pre-freeze 0,4,34,2,38,31,42,44 of 52; SKILL v3 52/52 | `dev-scores-prefreeze.json`: CTL-C2-0 0, -1 4, -2 34, -3 2, -4 38, -5 31, -6 42, -7 44, SKILL.md 52/52; n=52 everywhere; dev_seed = sha256("dev41") = c9e30c10… (verified by recomputation) | ✓ |
| held-out set generated from the round-41 freeze hash | manifest `seed` = d764389e9cbe61b9d1b07538ff3bff02d50bb34f = freeze commit; freeze-tree generator sha256 652d71af… = manifest `generator.sha256` (verified via `git show <freeze>:tools/round-41/heldout-gen-v3.py | sha256sum`) | ✓ |

Source-line citations S112/S118/S119/S120 (entry header + table rows): verified against installed trees with numbered line dumps:
- S112 `squashfs.py`: class at 24–70; AVM branch 44–50 exact (`is_avm = header.bytes_used == header.mkfs_time` at 48; `if not is_avm: commands_args.append("-be")` at 49–50); magic-pattern lines 102 (v1), 159 (v2), 245 (v3), 463 (v4 LE), 522 (v4 BE) — all exact.
- S118 `extractor.py`: `is_recursive_link` 42–47 exact; `fix_symlink` 50–92 exact; loop branch 58–65 exact; containment `is_safe_path` 79–91 exact. Minor: empty-target branch cited 67–69, actual removal lines are 70–71 (`path.unlink()`, `return path`); 67–69 covers readlink/condition/log — trivially over-reached, no mis-statement.
- S119 `FirmwarePublication.js`: `MAX_EXTRACTION_DEPTH = 10` at 23 exact; depth continuation 24–29 exact; `emptyGap` 39–46 exact; dependency gap rows 161–201 within the 160–206 block; extractor-failure emission 288–293 exact; depth-limited 294–300 exact; unpublished-entry 301–308 exact. `firmwareAnalysis.js` kind enum 85–90 exact; `unpublished_entries[].kind` enum `["symlink","special"]` at 139 exact. `FirmwareRelease.js` limits 27–32 exact (inputBytes 128 MiB at 28, timeoutMs 120_000 at 32).
- S120 `report.py`: `ExtractCommandFailedReport` 91–98 exact (field `command` at 95); `ExtractorDependencyNotFoundReport` 118–122 exact; `ExtractorTimedOut` 125–131 (field `cmd` at 129, `timeout` at 130) — entry's `:125-138` over-runs into the next class by 7 lines, but the cited fact (`cmd` not `command`) is exact at 129. `extractors/command.py` raise sites 60–77; the "before the spawn" phrasing in the table's cause is loose (the FileNotFoundError is thrown by the spawn attempt and caught at 69–77; the dependency report is constructed in the handler), but the substance ("no command ran, no argv exists") is correct.

## 5. Findings

### 5.1 [DEFECT — moderate] Entry's held-out composition enumeration is stale and does not sum to 52
Entry §Scoring: "The held-out set is generated from the round-41 freeze hash: v2's thirteen classes plus the combined classes `partial+in-tree`, `partial+mixed`, `depth-limited+in-tree`, `depth-limited+mixed` and `depth-limited` alone, two replicates each." That is 13+5 = 18 named classes → 36 envelopes + 12 combos = 48, not the frozen 52.
Frozen reality: `heldout-gen-v3.py` `DEFAULT_CLASSES` = 20 named recipes — the 18 above plus `body-extractor-failure-le` and `failure-depth-limited` (lines 359–378; both added by the round-41 amendment, claims `## Changes from the draft`: "two classes were added (`body-extractor-failure-le`, `failure-depth-limited`, `w1/R41C2Shortcuts.md` §6)"). The committed receipt confirms `planned_classes` length 20 and `n=52`.
Impact: SKILL block 20's citation into the entry is `:11-25` (grammar only), so the landing block is unaffected; but the entry is the reference document the block is "backed by" (claims C2 surface-moved), and its held-out description is factually incomplete/miscounting vs the freeze-time generator and manifest.

### 5.2 [DISCREPANCY — low] H feature definition differs between entry/interpreter (chunks-only) and frozen claim/evaluator (chunks ∪ gap handlers)
- Entry: "`H` the `squashfs*` chunk handlers" (and "v2's").
- Interpreter `features()`: H = `normalized_result.chunks[].handler` values starting `squashfs` (only).
- Frozen claim text (authority): "H = the handler names in `normalized_result.chunks[].handler` ∪ `normalized_result.extraction_gaps[].handler` (nulls dropped)".
- Evaluator `indep-eval-v3.py` (lines 35–37, 230–251): implements the union (+ raw ChunkReport fallback), and step 5 reads the failing-chunk handler HF with H fallback.
On the scored set this never diverges — the counter matched 52/52 against the evaluator, and all 40 class carriers' declared tuples matched observed features (receipt `declared_features.by_class` all `match`). So it is a documentation/authority-consistency note, not a scored defect; the entry describes the interpreter, the claim text describes the intended feature. Worth aligning in wave 2.

### 5.3 [NOTE] The honest stop: entry does not contradict it; the stop documents a separate key-contract failure
The R41-C2 honest stop in `c2-at-e9a24d07.json`: `matched=52`, `distinct_decisions=13`, `distinct_rows=12`, `real_receipts` all ok (interpreter AND evaluator give `depth-limited`/`raise-depth` on V1/V2/L1/L2), `class_map_agreement.agree=40` (reported, not bound), exit_code 1, `met_target=false`, with the single false binding `observed_features_match_declared`; `declared_features.missing = [C01…C12]`.

Mechanism (verified by reading both sides):
- The frozen generator writes every carrier's declared tuple under key `declared` (plus `declared_extras`), and `class_expected.features` ONLY for class carriers (combos have `class_expected: null`; manifest C01 shows `class_expected: null` + `declared: {...}`).
- The frozen counter's tuple reader (c2-counter.py ~1493–1506) looks only for `class_expected.features` → `features` → `declared_features` → manifest family maps (`class_features`/`classes_features`/`feature_tuples`/`features_by_class`/`class_tuples`). It never reads `declared`. Combos therefore hit `declared-tuple-incomplete` (C01–C12), `observed_features_match_declared=false`.
- Spot check (this seat): interpreter run on C01's envelope gives H=[squashfs_v4_be], G=[extractor-failure, unpublished-entry], D=[], BE=yes, SR=yes, P=7 → equals C01's manifest `declared` tuple (handler_set [squashfs_v4_be], gap_kinds [extractor-failure,unpublished-entry], gap_dependencies [], be_argv yes, symlink_removed true, published nonzero). C07 (G=[unpublished-entry], SR=no, P=5) and C12 (G=[depth-limited], P=8) likewise match their declared tuples. So the binding would hold on all spot-checked combos if the counter read the `declared` key — consistent with the stop's characterization as an honest, mechanical failure rather than a table/evaluator disagreement.
- Entry's Scoring sentence "A disagreement between the frozen independent evaluator and the generator's own class expectation is reported and fails the claim" predates the freeze's "reported, not scored" rule (claims: "The generator's class map is reported (`class_map_agreement`), not scored"; receipt note identical). No disagreement occurred (40/40 agree), so the entry is not contradicted on fact, but the sentence overstates the current claim's binding.

## 6. Verification gaps / residual risk
- I did not re-run `checks.py` or regenerate carriers; the committed TSVs, manifest seed/generator hashes and the v3-block identity bindings (receipt `v3_block_identical`, `manifest_after_freeze`, `generator_sha_matches_freeze`, `regenerated_seed_matches_freeze`) were verified by direct reads and a freeze-tree sha256 comparison.
- The evaluator/interpreter H-equivalence on the scored set is taken from the receipt's 52/52 match (external measurement), not re-derived here.
- Nothing in this seat mutates the lane; only this report and the artifacts file are written.
