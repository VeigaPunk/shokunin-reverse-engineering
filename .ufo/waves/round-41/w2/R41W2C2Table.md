# R41W2C2Table — SKILL rule block 20 (`<!-- sqfs-triage-table v3 -->`) row-by-row at e9a24d07

VERDICT: **DEFECTS FOUND** — 1 MEDIUM (the `dep-missing-le` cause cell asserts a resolution the frozen grammar cannot perform, and precedence clause 3's membership semantics are not implemented), 3 LOW (avm row vs clause 5's *failing-chunk* handler on multi-chunk tuples, executed divergent; the pre-check's **drop-`-be`** wrapper delivery is neither measured nor `[INFERENCE]`-marked; the block-19 supersession sentence overgeneralizes v2's partial+link fate), 2 INFO (the disclosed v1-v3 divergence, re-confirmed by execution; the pre-check's AVM walk is non-discriminating on LE bodies). Every source line I checked is byte-accurate. All 12 rows' decision cells implement their clauses on single-chunk, singleton-dependency tuples — the held-out shape — so the scored surface is unchallenged. **No R40-CL5 item is unrepaired**: M1–M3, L1, L3, L4, L6, L7 verified repaired in the frozen bytes; L2 is repaired for the *append* wrapper (measured, cited in-cell) but its marker-or-measurement standard was not extended to the pre-check's new *drop* branch (F3).

**Attacked:** every row's nine decision cells against the frozen precedence text (plans/round-41-claims.md `**Label precedence**`); every cause/source cell against the cited S112/S118/S119/S120/S121/S122/S124 lines (verified against installed copies whose sha256 equal the SOURCES pins, and one fresh fetch for S124); the layout pre-check paragraph against `w1/artifacts/R41C2TableDraft/l2-wrapper-measurement.md`; both supersession sentences against measured v1/v2 behaviour; and the R40-CL5 ledger row (M1–M3, L1–L7) item by item. The frozen interpreter and evaluator were executed against each other on hand-built seam tuples.

## 0. Method, pinned bytes, executed sanity

All review targets were read from `git show e9a24d07256d1606f01aa4d2d65f74e649c5f3d4:<path>` into scratch (SKILL.md 1479 lines; `tools/round-41/sqfs-triage-v3.py` 1772; `indep-eval-v3.py` 693; `corpus/SOURCES.md`; both round-41 knowledge entries; PROVINCE.md; round-39/40 lessons). Working-tree HEAD is `e1c83313` with 9 dirty paths — nothing was read from the worktree except installed tool sources, each sha256-checked against its SOURCES pin before line checks: S112 `squashfs.py` `2d7b901b54e2ad28…` (= pin), S118 `extractor.py` `1bb498119429ed80…` (= pin), S120 `report.py` `2329783fc645de8a…` and `command.py` `8ae7d2a3980b80b2…` (= pins), S122 `file_utils.py` `87d4dc9a51bc4e92…` (= pin), REA 6.5.0 `dist/**` (= S119's tarball-equal install). S124 was freshly fetched (`curl` of the pinned Freetz-NG URL): sha256 `7f0a1b252d4bbde7…` = row pin.

Executed at the pinned bytes (all exit 0):
- `python3 -I -B sqfs-triage-v3.py --skill SKILL.md --table-only` → `marker line: 434  actions line: 435  table line: 436  rules: 12` — the entry's recheck command is valid, 12 rows parse.
- `python3 -I -B sqfs-triage-v3.py --selftest` → 69 `ok` lines; `python3 -I -B indep-eval-v3.py --selftest` → `cases: 46, failures: []`.

Divergence probes (`artifacts/R41W2C2Table/probe-divergences.py`, results in `divergence-results.json`): envelopes are built with the frozen evaluator's own `_env` builder, so both engines read identical bytes; no REA/unblob run, no carrier, no lane write outside this report and the artifacts dir.

## 1. Row-by-row: decision cells vs precedence step (SKILL.md:438–449)

| # | row | cells vs its clause | verdict |
|---|---|---|---|
| 1 | no-squashfs-chunk | handler `none` = no `squashfs*`-prefixed handler; clause 2 = no `squashfs_v4_*`. Diverges only for a v1-v3-only chunk — **disclosed** (entry `What v3 adds` + interpreter docstring), executed: interp `(unclassified, none)` vs eval `(no-squashfs-chunk, inspect-input)` | OK (disclosed, F5) |
| 2 | dep-missing-be | `missing-extractor-dependency+` = membership for the one named kind ✓; deps exact singleton; BE/SR/P `*` (clause leaves them open) ✓ | OK for singleton D; F1 on supersets |
| 3 | dep-missing-le | same grammar; **cause cell claims "a dependency list naming both resolves to the BE row above" — false under exact-set cells** (executed, F1) | F1 (MEDIUM) |
| 4 | partial-body-failure | `extractor-failure+`, P `>0`, deps/BE/SR `*` = clause 4's "whatever other gaps or removed links accompany it"; ordered above avm/body/depth ✓ | OK |
| 5 | avm-marker-be-dropped | handler `squashfs_v4_be`, `extractor-failure+`, BE `no`, P `0` = clause 5 on single-chunk tuples; BE `n/a` correctly rejected (executed: timeout tuple lands body row, agreeing with eval) | OK single-chunk; F2 multi-chunk |
| 6 | body-extractor-failure | `extractor-failure+`, P `0`, everything else open = clause 6 ✓; cause rewritten per R40-CL5 M2 ✓ | OK |
| 7 | depth-limited | `depth-limited+`, all else `*` = clause 7 "whatever symlink gaps or removals accompany it"; after failure rows, before symlink rows ✓ | OK |
| 8 | mixed-symlinks | `unpublished-entry+` + SR `yes` = clause 8 ✓ | OK |
| 9 | escaping-symlink-removed | gap cell `none` (∅) + SR `yes` = clause 9 — the R40 L5 repair landed (v2 kept `*`) ✓ | OK |
| 10 | in-tree-symlink-metadata | exact singleton `unpublished-entry`; SR `no` is redundant-but-safe: every SR=yes + unpublished tuple is absorbed by row 8 above ✓; "a second gap kind … rows above decide it" is loose only in the SR=no unknown-kind case, which falls to step 12 as the clause says | OK |
| 11 | clean | `none` + SR `no` + P `>0` = clause 11 arm 1 (SR `no` redundant-safe under row 9) ✓ | OK |
| 12 | clean-empty | same with P `0` ✓ | OK |
| — | step 1 / step 12 | OP/PR pinned on every row (clause 1 gate, redundant-safe); no-match `(unclassified, none)` = step 12 ✓ | OK |

Actions: all 12 tokens appear in the `<!-- sqfs-triage-actions: … -->` line (:435) and each row's action is in vocabulary; the 12 labels + `unclassified` = the 13 distinct decisions the C2 receipt records.

## 2. Findings by severity

**F1 — MEDIUM — `dep-missing-le` cause cell asserts a machine behaviour the frozen grammar refutes; clause 3's "D holds" is not implemented.** SKILL.md:440 says *"a dependency list naming both resolves to the BE row above, not here"*. Dependency cells are exact-set: `_parse_set_cell(dep, contains=False)` → `('exact', frozenset)`, `match_set` compares `frozenset(values) == payload`, and the grammar refuses contains-form (`c_deps_cell_has_no_contains_form` selftest: `sasquatch+` → exit 2). Executed: `D={sasquatch-v4be, sasquatch}` → interpreter `(unclassified, none)`, evaluator clause 3 (`D holds sasquatch-v4be`) `(dep-missing-be, install-extractor-be)`; same for `D={sasquatch-v4be, other-tool}` (`dep-superset-other` in divergence-results.json). So the entry's design sentence — "each cell carries exactly the constraints its clause names and `*` for every feature the clause leaves open" — is falsified at clause 3, and the adjacent cause cell states the opposite of the executed behaviour. No score impact: unblob's extraction-time dependency report names exactly one executable (S120 `command.py` raises with the resolved Command's executable; the both-names `get_dependencies` list is unblob's install-time API, S112 :68-69), the held-out generator emits singleton D, and the C2 counter matched 52/52 pairs. The entry's Limits disclose neither this nor a reason. Smallest repair: reword the cause cell to the exact-set fact (a grammar change to membership would touch frozen C2 paths and cannot ride this round). Note the C2 NOT-MET verdict in the dispatch comes from the counter reading `class_expected.features` where combo carriers declare under `manifest['declared']` — a generator/counter key mismatch, unrelated to this block.

**F2 — LOW — avm row's handler cell cannot implement clause 5's "the failing chunk's handler (else H)".** The cell fnmatches any member of H (`rule_matches` pattern branch), the evaluator reads HF = the `extractor-failure` gap's own handler first (its selftest `b-step5-uses-failing-chunk-handler` pins exactly this). Executed two-chunk tuple (H={squashfs_v4_be, squashfs_v4_le}, failure on the LE chunk, BE=no, P=0): evaluator `(body-extractor-failure, preserve-failure)`, interpreter `(avm-marker-be-dropped, wrap-extractor-be)` — the wrong wrap instruction for a marker-less LE failure. Undisclosed: the entry's Limits name only the dep-masks-failure multi-chunk case. Synthetic-only on the scored set (every held-out envelope is single-chunk), REA-reachable in principle on multi-chunk inputs.

**F3 — LOW — the pre-check's drop-`-be` wrapper delivery is neither measured nor marked.** The paragraph (:416–432) prescribes: *"AVM layout with `-be` present → … rerun through a PATH executable named `sasquatch-v4be` that **drops** the `-be` token before exec'ing the real binary."* `l2-wrapper-measurement.md` measures PATH interception (decoy run 3) and the **append** wrapper end-to-end through REA (run 2); no wave artifact I read runs a **drop** wrapper through REA. Grounding exists only as a composition (PATH interception, measured; a genuine body failing with `-be` and extracting without it, round-40 `R40MistakeHunt.md` MH-6 — outside REA). Round-40 L2 set the standard — marker or measurement — and the avm row's *append* cell now meets it (source cell cites the measurement, SKILL.md:442); the pre-check's new *drop* branch repeats the exact shape L2 filed, unmarked. Recommend `[INFERENCE]` (composed, not run) or one composed run in the next table revision.

**F4 — LOW — block-19 supersession sentence overgeneralizes v2's partial+link fate.** SKILL.md:363-366: *"this table's exact-set cells send a partial failure that also carries a link gap into `escaping-symlink-removed`."* True for the escaping-link case (SR=yes; v2 escaping row G `*` absorbs it); for partial+**in-tree** (SR=no) v2 has no matching row and yields `unclassified` — exactly what the claims' own honest partition states ("v2 gives `unclassified` to a partial failure with in-tree links … and `expect-link-absent` to a partial failure with mixed links") and what wave 1 measured (`w1/R41C2ReconCombined.md`). The sentence needs the two-way split — the same verb-precision class this round repaired as R40-CL5 L1 for block 18.

**F5 — INFO (disclosed; re-confirmed by execution).** Row 1 `none` vs clause 2's v4-only test: a v1-v3-only chunk is `unclassified` in the table, `no-squashfs-chunk` in the precedence (executed, `v1v3-only-chunk`). Disclosed in the entry and the interpreter docstring; the generator never produces it.

**F6 — INFO — the pre-check's AVM-layout walk is not stated as BE-scoped.** "Walk the metadata headers … as 2-byte little-endian lengths; if they land exactly on `directory_table_start` the body is AVM layout" is trivially true for any healthy LE image (LE is its correct reading); it discriminates only for BE-structural bodies, which is how S114/S124 scope it. No action-level consequence: an LE failure tuple has `-be` absent and lands `preserve-failure` on both routes, and `-be` never accompanies an LE run — but the paragraph should say "BE-structural body" before "AVM layout".

## 3. Cause/source cells vs the cited sources (all line checks byte-level)

| row | citation | check |
|---|---|---|
| 1 | S112 :463,:522 v4 magic `[24] 04 00` / `[24] 00 04` (s_major 4); :102,:159,:245 v1/v2/v3 handlers | ✓ installed copy = pin |
| 2 | S112 :24-25 executables, :68-69 `get_dependencies`; S120 `command.py:70-72` FileNotFoundError → `ExtractorDependencyNotFoundReport`; S119 `FirmwarePublication.js:161-186`, `firmwareAnalysis.js:85` | ✓ all verified; "no argv exists" and "file count open" match `emptyGap` + `files` untouched |
| 3 | as row 2 + S119 :186-201 | ✓; the "names only the executable the handler resolved" half is code-true (one executable per Command) — which is also why F1's tuple is synthetic-only |
| 4 | S119 :288-293 extractor-failure per failed chunk; `w2/R40W2C2IndepEval.md` §6 (4 of 5 published match, 5th a 16384-byte truncation) | ✓ file exists; the L4 measurement citation is real |
| 5 | S112 :48 (`is_avm = header.bytes_used == header.mkfs_time`), :49-50 (omit `-be`); S121 `-DFIX_BE` build; wrapper measurement; knowledge 2026-10-26-r40-avm-be-squashfs-core.md :37-45 | ✓ all verified; :37-45 is the measured genuine-AVM carrier table — supports "genuine AVM-layout body extracts without `-be`", though the sharper layout anchor in that entry is :19-24 (anchor looseness, not error) |
| 6 | S124 :35; S120 `report.py:91-98` (`command`, stdout, stderr, exit_code); S112 :44-50; MH-6 | ✓ fetched S124 sha256 = pin, line 35 is literally "block length in AVM-BE format is stored in LE order"; MH-6 exists and measures the both-ways flip |
| 7 | S119 :23 (`MAX_EXTRACTION_DEPTH = 10`), :24-29 depth/child continuation, :294-299 depth-limited gaps (empty deps), :243-247 ceiling re-root; `FirmwareRelease.js:27-32` | ✓ incl. the "unexamined, never empty" third branch and 128 MiB / 120 s limits |
| 8 | S118 :58-65 loop, :79-90 containment; S122 `is_safe_path`; S119 :301-307 unpublished-entry, `firmwareAnalysis.js:139` kinds `symlink|special` | ✓ |
| 9 | S118 :42-47 `is_recursive_link`, :58-65, :79-90; S122 | ✓ removal reported, no gap minted, G stays ∅ |
| 10 | S119 :301-307, :139 | ✓ |
| 11 | S118 :67-69 empty-target silent removal; `[INFERENCE] no committed envelope carries an empty-target link` | ✓ branch adds no report; the L6 honesty marker is present |
| 12 | S119 :301-307; R39-CL3 D2; c2/H05,H06 | historical, carried from the round-40 review's verification; not re-derived here |

## 4. Layout pre-check paragraph (:416–432)

The 2×2 (AVM/standard-BE × `-be` absent/present) is coherent with rows 5/6: AVM+absent → damage (`preserve-failure`, overriding the avm cell — the R40-CL5 M3 fix, stated both in-paragraph and in the avm cause cell); AVM+present → drop wrapper (F3); standard+absent → `wrap-extractor-be` (the avm cell's own population); standard+present → damage (body cell). "The pre-check overrides the action cell where it fires; an inconclusive walk leaves the cell standing" matches the entry's Limits ("needs carrier bytes; inconclusive on a truncated body"), and "the action column is scored / cause and source are prose" matches the claim's scored-pair design. The timed-out-extractor sentence is implemented, measured: a report shaped `ExtractorTimedOut(cmd=…)` leaves the frozen interpreter at `BE: n/a`, `commands: []`, landing `(body-extractor-failure, preserve-failure)` — same pair as the evaluator (which also reads `n/a`), so the pre-check's `cmd`-vs-`command` sentence (S120 `report.py:125-138`, verified: `cmd: str`) is byte-true and score-safe.

## 5. Block-18/19 supersession sentences

- **Block 18 (:331-337)** — accurate. "Mislabels mixed-link images and non-firmware envelopes, cannot label partial failures or empty trees" matches the round-40 v1 measurements (mixed → `escaping-symlink-removed`, out-of-domain → `no-squashfs-chunk`, partial/empty → `unclassified`); the verb split is the R40-CL5 L1 repair, landed. "Wraps `-be` unconditionally on its AVM-marker row without the layout check every later table carries" matches the v1 row's action text; v2 (in-cause walk) and v3 (hoisted pre-check) both carry it.
- **Block 19 (:363-369)** — three of four claims accurate; **F4** on the fourth. "All four round-40 C1 carriers were `unclassified` here" is true (`{depth-limited, unpublished-entry}` matches no v2 row: mixed and in-tree need the exact singleton, escaping needs SR=yes, no depth row exists); "adds the `depth-limited` row this table lacks" ✓; "its layout pre-check replaces this bullet's claim that the AVM-marker row covers a doctored marker on a standard-BE body only" ✓ (that bullet text sits at :360-361, and the v3 pre-check does replace it).

## 6. R40-CL5 ledger (`corpus/lessons/round-40.md:112`) — item status at e9a24d07

| item | status | evidence |
|---|---|---|
| M1 stale embedded table copy | **repaired** | no `TABLE_BLOCK` assignment and no header-row literal in `sqfs-triage-v3.py` (only the docstring note :45 and the selftest's deliberately-split needle :1355 `'TABLE_BLOCK' + ' ='`); `--print-table` refused exit 2 (`c_print_table_removed`); `--table-only` prints the parsed block |
| M2 body-row cause denies the handshake population | **repaired** | row 6 cause rewritten (S124 :35, pre-check first); MH-6 population now named in-cell |
| M3 avm action vs cause's damage branch | **repaired** | pre-check override stated in-paragraph and in the avm cause cell (:442) |
| L1 block-18 verb | **repaired** | :331-337 splits mislabels / cannot label |
| L2 wrapper delivery | **repaired for append** (measured, cited in-cell); **new drop branch unmarked** → F3 | `l2-wrapper-measurement.md` exists and supports what its cell claims; F3 is the residue, not an unrepaired item |
| L3 dep rows omit REA as minter | **repaired** | both dep rows cite S119 (`FirmwarePublication.js:161-186`/`:186-201`, `firmwareAnalysis.js:85`); verified the minting code |
| L4 partial oracle-match unmeasured | **repaired** | cited measurement `w2/R40W2C2IndepEval.md` §6 exists (4/5 + truncation), no marker needed |
| L6 clean-row silent empty-target removal | **repaired** | row 11 states it (S118 :67-69) with the `[INFERENCE]` marker on the population |
| L7 none/no-match collapse | **repaired** | entry Limits: "`none` is both the `clean` row's action and the no-match action, so those two envelopes are distinguishable only by label" |
| (ledger tail) "`dependencies` never decides" | **repaired + disclosed** | clause 3 keys on D; entry discloses the column's redundancy on every measured class |

## 7. Residual risk and verification gaps

- No REA/unblob/sasquatch run and no carrier was touched (bounds); extractor-behaviour claims rest on installed sources, the cited wave measurements, and round-40 receipts.
- The probes are feature-level: they prove interpreter-vs-evaluator divergence on the named tuples, not that REA can produce every tuple. F1's both-names D and F2's two-squashfs-chunk H are [INFERENCE]-grade REA-reachable; F1's cause-cell falsehood stands regardless of reachability because it describes the table's own machine.
- Row 12's historical citations (R39-CL3 D2, H05/H06) and row 5's knowledge-entry anchor were not re-derived from round-39 bytes; both were verified by the round-40 review and I re-confirmed file existence only.
- The C2 counter's `declared`-key failure (dispatch; `l1/scores/c2-at-e9a24d07.json` field `declared_features.missing`) was taken as given, not re-adjudicated — it is a generator/counter interface defect outside this block; nothing in block 20 causes or repairs it.
- Table-bytes-equal-freeze and manifest bindings are counter bindings (other seats' scope); I ran the interpreter's own parse only.

## 8. Tooling record and artifacts

No tool installed, upgraded or removed; no pacman transaction. Used only: system `python3` (3.x), read-only `git show`/`rev-parse`/`status`, `curl` (one fetch: the pinned S124 patch, sha256-matched), `awk`/`grep`/`sha256sum` as short fact pipelines over scratch copies. Scratch `/fast/scratch/hyaku/kaidoku-r41/R41W2C2Table` removed at the end. Artifacts (final at yield): `artifacts/R41W2C2Table/{probe-divergences.py, divergence-results.json, env-*.json (9 envelopes)}`. Key executed outputs, verbatim:

```
sanity-clean            eval=(clean, none, step 11)                interp=[clean, none]
sanity-avm              eval=(avm-marker-be-dropped, wrap, step 5) interp=[avm-marker-be-dropped, wrap-extractor-be]
dep-both-names          eval=(dep-missing-be, install-be, step 3)  interp=[unclassified, none]        <- F1
dep-superset-other      eval=(dep-missing-be, install-be, step 3)  interp=[unclassified, none]        <- F1
step5-failing-chunk-le  eval=(body-extractor-failure, step 6)      interp=[avm-marker-be-dropped, wrap-extractor-be]  <- F2
v1v3-only-chunk         eval=(no-squashfs-chunk, step 2)           interp=[unclassified, none]        <- F5 (disclosed)
timeout-no-argv         eval=(body-extractor-failure, step 6)      interp=[body-extractor-failure, preserve-failure]  (agreement)
--table-only: exit 0, rules: 12   --selftest(interp): exit 0, 69 ok   --selftest(eval): exit 0, cases 46, failures []
```
