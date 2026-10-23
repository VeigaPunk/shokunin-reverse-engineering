# ScoutPriorRust — prior kaidoku statements on `inspect_rust_binary`, `.dep-v0`, Rust dependency metadata

Seat: KaidokuR30.ScoutPriorRust (leaf, read-only on the lane). Written 2026-10-23 (UTC), against lane
`main` = `a6e7d9cee57eb0f74080b8557f17b7239deb96c9` (`git rev-parse main`, exit 0, 2026-10-23T02:47:35Z;
lane base `d210fb8f…` and instrument commit `0dbabf78…` both ancestors of `main`, exit 0 each).
No file in the lane was modified except this report. Labels: **[O]** observation (committed bytes read),
**[I]** inference, **[U]** unknown.

## Commands and evidence

1. Prescribed sweep (exact argv), output kept at scratch `grep-all.txt`:
   `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -i -e 'dep-v0' -e 'inspect.rust.binary' -e 'auditable_metadata' -e 'rustc_commit' main -- . ':!corpus/evidence/round-30' ':!tools/round-30' ':!.ufo/waves/round-30'`
   → **exit 0**, **356 hit lines across 205 files**, output sha256 `c329ea37c6e51255839784aa24743cb7dca5f3878fd2f7ac890901139267b8f0`
   (run 2026-10-23T02:47:02Z; byte-identical on re-run). **[O]**
2. Supplementary sweep for names the four tokens miss: `git -C … grep -n -i -e 'cargo-auditable' -e 'rust-auditable' -e 'dep_v0' main -- . ':!corpus/evidence/round-30' ':!tools/round-30' ':!.ufo/waves/round-30'` → exit 0, 39 hits / 39 files, sha256 `56c5002d7bc3e54b01f27be6876834d79e70f2a1d9c622ff1257793050e578ae`. **[O]**
3. Base-state zero check (supports the frozen `unmoved_command`s):
   `git -C … grep -c -e 'inspect.rust.binary' -e 'rust-auditable' -e 'dep-v0' -e 'cargo-auditable' main -- PROVINCE.md SKILL.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md`
   → **no output, exit 1** (0 matches in all five files) at 2026-10-23T02:47:02Z. **[O]** — PROVINCE.md and SKILL.md name the verb 0 times at base; no cargo-auditable/`.dep-v0` source row exists.
4. `git -C … grep -n '| S089 |' '| S090 |' main -- corpus/SOURCES.md` → no match, exit 1 at 2026-10-23T02:47:02Z. **[O]** — source ids S089/S090 are unoccupied; the round-30 additions collide with nothing.
5. `jq -r '.["positive"].stdout|fromjson|.catalog_zero|index("inspect-rust-binary")' .ufo/waves/round-22/w2/C1Refusal.json` → `53` for all three cases, exit 0, 2026-10-23T02:47:42Z. **[O]** — see R22 note below.

The 356-line hit set was classified by reading each hit (prose read in full where substantive). Scratch
artifacts (sha256): `grep-all.txt` `c329ea37…`; `matched-files.txt` `a2501166…`; `supplementary.txt`
`56c5002d…`; `condensed.txt` `0ccec97f…`.

## A. Canonical live statements — what the R30-C1/C2 entries must cite, supersede or leave unchanged

| locus (rev `main`) | statement | relation to R30-C1 / C2 |
|---|---|---|
| `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:1,5` | "REA 6.5.0 `inspect_rust_binary` — typed RESULT on two distinct carriers"; recheck: call the verb on the two pinned paths, record Evidence IDs, `auditable_metadata`, `rustc_commit`, limitations | **CITE** — this is the base-state entry R30-C1's surface names; the record-field list is the ancestor of C1's envelope fields |
| `…l7-02…md:7` | lane B `/usr/bin/rg` (sha `d006acfe…`): RESULT `ev_9ea97685…`, provider `rust-auditable` v1; `auditable_metadata` null; `rustc_commit` null | **CITE** — the only 6.5.0 ok-run record of the verb; null-metadata base state |
| `…l7-02…md:8` | lane A libsignal `.node` (sha `1b44ed53…`): RESULT `ev_0618e7a5…`; `auditable_metadata` null; `rustc_commit` `{evidence_kind:"inferred", hash da80ed…, file_offset 2287779}` | **CITE** — precision note: "null-metadata runs" in R30-C1 means `auditable_metadata` null; lane A's `rustc_commit` is non-null (inferred) |
| `…l7-02…md:9` | inference: the operation "inspects only `.dep-v0` and read-only compiler-path strings"; "Nulls are not evidence of missing dependencies or compilers"; scope "these two calls only" | **CITE / SUPERSEDE (scope)** — C1 supplies the positive-class counterpart (non-empty package lists decoded from `.dep-v0`); the "only .dep-v0" inference is corroborated, not contradicted |
| `…l7-02…md:10` | tool-reported limitation "No `.dep-v0` section was found…"; "Untested: non-ELF inputs, missing-metadata/rejected-input behavior, other REA versions"; guards 256 MiB file, 1 MiB section, min(8 MiB, 64× section) inflated JSON, 8 MiB report | **SUPERSEDE (tested clauses) / CITE (guards)** — C1 tests non-ELF inputs (PE, thin Mach-O) on the positive class; C2 tests rejected-input behavior; both at 6.5.0. The guard sentence must stay consistent with C2's limits table (see §D.2) |
| `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:3,11,15,19,22,28` | 6.7.0 evidence-ID formula for `inspect_rust_binary`; path-sensitive via `parameters.path`, `normalized_result.artifact.path`, `artifact-path` location; the `/usr/bin/rustc` probe has `auditable_metadata:null`, `rustc_commit:null`, "no `.dep-v0`" limitation; scope excludes 6.5.0/6.4.0 | **CITE / UNAFFECTED** — second base-state entry named by R30-C1; 6.7.0 pin, R30 runs 6.5.0; never carry its ids into 6.5.0 comparisons (see §C) |
| `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:12` | REA 6.4.0: `inspect_rust_binary` (L4) typed-refused `{"code":-32602,"message":"Tool inspect_rust_binary not found"}`; name absent from the 170-tool list | **CITE / UNAFFECTED** — version boundary (6.4.0 vs 6.5.0); no R30 interaction |
| `corpus/README.md:41` | Evidence-model row: `ev_` formula derived for four verb families (arc3-r7 EVM, r10 Rust, r11, r12) | **CITE / UNAFFECTED** — r10-derived; R30 does not re-derive an id rule |
| `corpus/README.md:63` | Rust coverage-map row (`…l7-02-inspect-rust-binary`, `…arc3-r10-rust-evidence-id-domain`): "`.dep-v0`/rustc commit unknown, not evidence of no dependencies" | **CITE / UNCHANGED for its carriers** — the r10 integration note says new tokens append to this Rust row; R30-C1 will add a row/token here |
| `corpus/README.md:68` | l8-01 row (6.4.0 six-name refusal) | **UNAFFECTED** |
| `corpus/README.md:159` | Knowledge-table row for l7-02 ("no `.dep-v0` found in libsignal `.node` or `rg`; absence does not prove no dependencies"; basis `rea-agents@6.5.0` receipts) | **CITE / UNCHANGED** — R30-C1 adds a sibling row |
| `corpus/README.md:216` | Known-gaps bullet: evidence-id identity is verb-family-specific; "for path-sensitive families, cross-path identity cites `subject.digest.sha256`" (with round-26/27 sub-bullets) | **CITE** — governs any id the R30 entries report: compare only within one pin and one path shape |
| `SCORECARD.md:1936` | round-10 section: `inspect_rust_binary` is path-sensitive because its semantic projection carries the three path fields (6.7.0) | **CITE / UNAFFECTED** |
| `SCORECARD.md:2023` | "the `ev_` domain is now closed for three verb families (inspect-evm-interface, inspect_rust_binary, inspect_artifact), each path-sensitive by its own projection, not by a universal rule" | **CITE / UNAFFECTED** |
| `LOG.md:1651` | round-10 log entry (same path-sensitivity statement; 88→89 map token) | **CITE / UNAFFECTED** |
| `SKILL.md:301-302` (+ citations `:306-308`) | craft rule: "EVM and Rust carry path in `parameters.path`, `normalized_result.artifact.path`, `locations[0].path`" (cites arc3-r10 entry) | **CITE / UNAFFECTED** — 6.7.0-derived; R30-C2's base fact "no SKILL.md line names inspect-rust-binary" (0 matches, command 3) is flipped by the new table |
| `PROVINCE.md` (whole file) | no statement: 0 occurrences of `inspect-rust-binary`/`rust-auditable`/`dep-v0` (command 3) | **FLIP (base state)** — R30-C1's `province_ok=1` adds the first PROVINCE naming |
| `corpus/SOURCES.md` | no `cargo-auditable`/`.dep-v0` source row; S089/S090 unoccupied (commands 3, 4) | **FLIP (base state)** — R30 adds them; no id collision |

## B. Raw receipts and round-history statements (provenance the canonical entries rest on)

All **[O]**, relation **CITE (provenance) / UNAFFECTED** unless noted.

- `luna-round-6/receipts-B/leg-4.md:5,14,47,50,67,69,71` — lane B raw exchange: call, envelope
  (`ev_9ea97685…`, subject sha `d006acfe…`), and line 69 verbatim:
  `auditable_metadata: null; rustc_commit: null; limitation: "No .dep-v0 section was found. Absence of .dep-v0 does not mean the binary has no dependencies."` — the source of l7-02:7,10.
- `luna-round-6/receipts/leg-4.md:1,9,28,34,43` — lane A raw receipt; `:43` "The SC2-carrier identity itself remains unverified" (fallback reason at `:15`).
- `luna-round-6/BB4.md:9-10` (independent lane-B re-run: `auditable_metadata: null`, "Arch ripgrep 15.2.0 is not cargo-auditable"), `CC4.md:4` (cross-lane agreement at outcome class), `RV2.md:9` (6.5.0 replay on `/usr/bin/rg`), `CB9.md:11` (canonical L4 target = Signal `.node`; RV2 off-target), `AC1.md:13` (L4 RESULT), `EX4.md:3,7,11,15` (fallback + "Rust compiler commit is inferred … not compiler authentication"), `P0.md:9`/`PR1.md:23`/`PR2.md:15`/`QA4.md:8` (frozen prediction L4 = RESULT class), `receipts/census-final.txt:13` and `receipts-B/census-laneB-final.txt:27` (census row `A=inspect_rust_binary -> B=inspect_rust_binary … RESULT`).
- `luna-round-7/E2D.md:10-17` (draft entry), `E2V.md:8-10` (carrier separation; do not merge), `G2.md:11-24` (narrower alt), `Q2.md:15-17` (admission-label lapse; slug mismatch), `FB1.md:8` (underscore vs hyphen name divergence), `K3.md:9`/`M1.md:12` (map rows; merged-carrier caveat), `CB3.md:7` (six files added), `CB5.md:10` (one Knowledge row, merged basis), `GB4.md:10,13` (facts check; "M1 row 2 compresses rg's observed 'no .dep-v0' into 'unknown'"), `GB5.md:10` (K3 clause merges carriers, omits lane A's inferred hash), `Z2.md:8` (convergence only at outcome class), `ZB.md:13` (primary E2D / narrower G2 ruling), `N1.md:10`, `C1.md:9`, `C7.md:10` (carrier separation), `DB2.md:2,8` (derivability audit; four gaps), `CB10.md:11` (provider pin `rust-auditable "1"`), `CB12.md:10` (provider values agree), `FINAL-MANIFEST.md:70-98` (final entry text + the two README rows), `RB1.md:2`, `RB4.md:12`, `VB1.md:11`, `VB5.md:10`, `T2.md:12`, `P1.md:14`, `P2.md:8`, `C3.md:19`, `XB1.md:58`, `CB7.md:34`.
- `luna-round-8/EX4.md:3,7,11`, `receipts/leg-4.md:13` (`-32602` refusal), `receipts/leg-9.md:10,19` (name absent, empty stdout sha `e3b0c442…`), `RV2.md:9` (same carrier: 6.4.0 refuses / 6.5.0 RESULT), `RB5.md:29,40`, `RE5.md:8`, `RE6.md:13`, `CB3.md:8`, `CB5.md:36,38`, `CB6.md:12`, `HB2.md:15`, `K1.md:5`, `P0.md:11`, `PR1.md:13,18`, `PR2.md:13`, `PS1.md:11`, `PS3.md:13`, `QB1.md:8`, `RB1.md:12`, `VB7.md:10`, `VB8.md:10`, `XG1.md:9`, `receipts/census-laneB-pre.txt:38,273` — the 6.4.0 symmetry battery's L4/L9 legs.
- `luna-round-9/C1.md:9` (l7-02's recheck uses pinned paths) and `G1.md:9` (citation-path fixes).
- `luna-round-10/W7.md:9` — CB7 census: C9 fail on l7-06 (gate literal `rea-agents@6.5.0`); entry 2's text "explicitly distinguishes the carriers".
- `luna-round-2/A6.md:8` (6.5.0 = 207 MCP / 153 CLI), `receipts/A6-6.5-help.txt:93`, `A6-6.5-llms.txt:94`, `G1-replay-2.txt:107`, `L6-help.txt:96` — the 6.5.0 CLI/llms description: "Inspect an embedded cargo-auditable Rust dependency list without target execution" (**the strongest prior statement of the positive input class; CITE for P1's surface**); `L7-mcp-tools-6.5.0.txt:11,14`, `L3-omp-pin.txt:12,16`, `A6-6.5.0-mcp-tools.txt:6` — tools/list containing the name.
- `arc2-loop1-round1/receipts/leg-2-tools-list.json:109` (count 207 → 6.5.0 pin), `leg-2-binary-session.json:1828`; same pair in `arc2-loop1-round2`.
- `.ufo/reports/luna-round-6/kaidoku.md:11`, `luna-round-8/kaidoku.md:10`, `arc3-loop1-round10/kaidoku.md:13,34,44`, `arc3-loop1-round11/kaidoku.md:71` — round reports.
- `luna-round-7/*` map/census receipts (`X1.md`-class tuples, `C3.md` slug finding, `CB7.md:34`) — historical process records.
- `corpus/knowledge/2026-10-13-r4-14-libsignal.md` (via `l7-02:8` citation; `README.md:25,130`) and `PROVINCE.md:155-156` — "stripped 24.9MB Rust/neon `.node`" anatomy. **UNAFFECTED** (different operation: `analyze`/`nm`/`strings`), but it is the provenance for the lane-A carrier's Rust identity.

## C. arc3-loop1 rounds 10–12 and later-round meta statements (evidence-id family; cite / unaffected)

- `arc3-loop1-round10/claims/c1/EX-4.md:3,11,15,19,22,28`; evidence `probe-{base1,base2,copyA,copyB}.json`,
  `rederive-commands.txt:5-8`, `identity.txt:13`; verdicts `CN-1.md:20,29-31,37`, `CN-4.md:18,20,22,24`,
  `CR-5.md:21`, `CR-7.md:30`, `CR-8.md:24`, `VZ-2.md:9,26,38`, `VZ-4.md:19,21,32,34` — 6.7.0 formula,
  four recomputed ids, path-sensitivity, `auditable_metadata:null`/`rustc_commit:null` probe.
  **CITE / UNAFFECTED** (pin 6.7.0).
- `arc3-loop1-round11/claims-frozen.md:20` — "r10 closed `inspect_rust_binary`". **CITE.**
- `arc3-loop1-round12/claims/c2/EX-9.md:48,57`, `EX-10.md:33`, `EX-11.md:7,47,48,72`, `EX-12.md:16`,
  `EX-13.md:19,29`, `EX-14.md:7,16` + `evidence/probe-commands.txt:11-13`, `EX-15.md:7,12,46`,
  `EX-16.md:8,19,27`, `SC-1.md:37,39`, `SC-2.md:9,18`, `SC-3.md:7,32,39,42,50`, `SC-4.md:24`,
  `verdicts/CN-4.md:28`, `verdicts/VZ-3.md:34`, `c3/RV-8.md:12`, `c3/RV-4/proposed-entries.json:16` —
  round-12 reproduction of the r10 path-sensitivity. **CITE / UNAFFECTED.**
- `round-25/a3/w1/PlannerWalk.md:18` (O5) — "At the lane's operative carrier pin `rea-agents@6.5.0`
  there is no control for any of them" (the six control-bearing verbs incl. `inspect_rust_binary`, r10).
  **CITE** — see §D.5 for the one way R30 could touch it.
- `round-26/w1/IdentityClaimsMap.md:45` (row 15: r10 among path-sensitive statements, "not a universal
  rule"); `round-26/w1/PinSourceDiff.md:82` — r10 row: "6.7.0 rule reproduces recorded id: yes, 2/2;
  6.5.0 rule: different id"; all eight arc3 envelopes carry `relationship_coverage: null`.
  **CITE + CONSTRAINT** — any 6.5.0 id R30 records is one rule-step from the arc3-r10 6.7.0 value;
  never copy the arc3 id string into a 6.5.0 claim.
- `round-26/w2/EntryTruth.md:22` (C3 T: r10 among the 6.7.0 two-path controls). **CITE.**
- `round-20/verify/round20/verb-coverage.json` (`per_command["inspect-rust-binary"] = 3`,
  rev `37e10c54…`, package 6.5.0) and `measure.json:153,300,471` (same tool output embedded);
  `round-20/w1/ScoutVerbZeroOracle.md:272` (row 58: `inspect-rust-binary | 4 files | 11 lines | invoke |
  corpus/README.md:148` — locus at the round-20 revision; current tip line 148 is not that row);
  `round-20/w1/VerbCoverageTool.md:21,24` (baseline 128/153 mentioned, 25 zero — the verb is not zero);
  `round-21/w1/ScoutCatalogBytes.md:75` (row 58 kebab↔snake mapping); `round-21/verify/*/verb-coverage.json:16`.
  **CITE** — historical census counts; R30-C1 adds mentions, so the counts go stale, not contradicted.
- `round-22/w2/C1Citation.json`, `C1Refusal.json`, `MutateC1.json`, `round-22/verify/*` — census receipts
  for R22-C1's six T1 verbs (`count-c1.py:15` T1 tuple does not contain the Rust verb). The verb string
  occurs only in the embedded `catalog_zero` complement (index 53 of all three cases, command 5).
  **UNAFFECTED** — artifact of that counter's complement list, not a statement about the Rust verb.
- `round-16/controls.json:796` + `round-17/{verify/controls.stdout:412,w2/controls.json:412}` +
  `round-18/{verify/controls.stdout:418,final-recheck/controls.receipt.json.stdout:418}` +
  `round-16/controls.py:8-11,163-166` and `verification.json:363` — frozen-baseline byte observations
  for `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md`: `byte_identical: true`,
  `appended_bytes: 0`, `prefix_preserved: true`; the control reports byte-prefix retention
  (append-only tolerated, rewrite flagged). **CONSTRAINT (leave unchanged)** — see §D.6.
- sha pins of l7-02's bytes in historical receipts: `arc3-loop1-round1/claims/c3/EX-30/corpus-full-sha-t0.txt:74`
  and `corpus-surfaces-sha-t0.txt:76`; `arc3-loop1-round2/claims/c2/EX-24/surf-census-*.txt:78` (15 files);
  `arc3-loop1-round3/claims/cross/CN-1/receipts/knowledge-digests-t0.txt:75` — all
  `748525e9391a7104f35d81f566cb87389111893a94ce56c9c1b26c98bbbf7430`; `arc3-loop1-round4/claims/c1/RV-2/evidence/prior-83.sha256:74`
  (same); `arc3-loop1-round3/claims/c1/EX-14/before-state.txt:93,177` (blob `23d8db35…`).
  **CITE / CONSTRAINT** — historical pins; an append to l7-02 preserves prefix but changes the file hash.
- README snapshots at earlier revisions (duplicates of §A rows): `arc3-loop1-round1/claims/c1/EX-13/README.{primary,alt-prose}.md:63,68,148`;
  `…/c1/RV-4/README.{before,after}.md:63,68,148`; `arc3-loop1-round3/claims/c1/RV-3/evidence/README-after-additive-rev4.md:63,68,148`;
  `…/c1/RV-4/{README.before,primary.README,honest-stop.README,caller-option-strict-additive.README}.md:63,68,148`.
  **CITE (historical copies).**
- `.ufo/interactive-sessions/20261015T050057Z/…jsonl:79,110` — session transcript quoting the REA skill /
  capabilities blob (contains the six verb names). **UNAFFECTED** (transcript, not a lane statement).

## D. Statements the round-30 results could contradict, or must reconcile

1. **l7-02:10 "Untested: non-ELF inputs, missing-metadata/rejected-input behavior, other REA versions."**
   R30-C1 tests non-ELF positive carriers (PE x86_64/arm64, thin Mach-O x86_64/arm64) and R30-C2 tests
   rejected-input behavior, both at 6.5.0. If either claim passes, this clause is **superseded for the
   measured classes** (the "other REA versions" clause stays). Not a contradiction; the R30 entries must
   name it, and any edit of l7-02 must follow the lane's supersession discipline (§D.6). **[O]** of the
   sentence; **[I]** of the supersession scope.
2. **Guard limits must agree.** l7-02:10 states guards "256 MiB file, 1 MiB section, min(8 MiB, 64× section)
   inflated JSON, 8 MiB report"; R30-C2's surface states "1 MiB compressed / 64x inflate ratio / 32-level
   nesting limits". These are consistent only if "section" = compressed section; the C2 table adds the
   32-level nesting limit and the file-backed/compressed-flag gates, which l7-02 never states. The C2 entry
   must phrase its limits as a refinement of l7-02's guard sentence, not a second, different set. **[I]** —
   flag for the C2 author.
3. **"Only null-metadata runs" wording.** The frozen R30-C1 surface says the lane holds "only null-metadata
   runs of this verb". l7-02:8 records lane A with a non-null (inferred) `rustc_commit`. "Null-metadata"
   must mean `auditable_metadata: null`; if the R30-C1 entry writes "all metadata null", it would contradict
   l7-02:8. **[O]** of both texts; **[I]** of the hazard.
4. **Absent section vs unusable section.** l7-02:7-10 and `receipts-B/leg-4.md:69` record that a binary with
   **no** `.dep-v0` returns an **ok RESULT** with `auditable_metadata: null` plus the limitation string
   (same in the 6.7.0 r10 probe, `…r10…md:22`). The frozen C2 predictions refuse **present-but-unusable**
   sections ("Dependency section is not file-backed", "Dependency section is not a complete zlib stream", …)
   and no mutant removes the section entirely. No contradiction exists, but the C2 entry must state the
   distinction explicitly or a reader will read the two together as a conflict. **[O]** of both texts; **[I]**
   of the reconciliation need.
5. **round-25 O5 / EntryTruth C4 "no two-path control at 6.5.0 for any of them".** R30-C1's predicate
   compares a committed envelope against a live run of the same carrier (same path) — a same-path
   agreement, not a two-path control; R30-C2 likewise runs each mutant once. If either counter adds a
   second path, a relocated copy, or a repeat control for this verb at 6.5.0, O5's sentence and C4's
   "no two-path control" become superseded for `inspect_rust_binary` (the first 6.5.0 control). From the
   frozen predicates only same-path agreement is required. **[U]** until the counters' run shapes are
   visible in their output; **[I]** on the relation.
6. **Frozen baselines / append-only.** `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md` is under
   the round-16/17/18 frozen-baseline controls (byte-identical, `appended_bytes: 0`, `prefix_preserved: true`)
   and its bytes are sha-pinned in arc3-loop1 rounds 1–4 receipts. The lane's supersession conventions:
   `corpus/QUALITY.md:4-5` "A criterion is replaced by a new row naming the row it supersedes, never
   rewritten"; QUALITY #19: "an overstatement is corrected by a named append-only line carrying the exact
   `file:line`, never by rewriting filed bytes". **Constraint**: R30 supersedes l7-02 by naming it in the new
   entries (and/or an append-only pointer), not by rewriting it; a rewrite trips the baseline controls and
   invalidates the sha pins. **[O]** of the controls and rules.
7. **Census counts go stale, not contradicted.** `per_command = 3` (round-20, rev `37e10c54…`), the oracle's
   row-58 "4 files / 11 lines" at the round-20 revision, and the 128/153 mentioned figure are historical
   receipts; R30-C1 adds a knowledge entry and a README row, so re-running those tools would print new
   numbers. No statement is contradicted if the round-30 entries do not re-assert the old counts. **[O]/[I].**
8. **`rustc_commit` is not part of R30.** l7-02 records both `null` (rg) and `{evidence_kind:"inferred", …}`
   (lane A); the r10 probe records null. No prior statement claims `rustc_commit` is always null, and no R30
   predicate reads it (P1/P2 cover `auditable_metadata` package lists, `file_offset`, `compressed_bytes`).
   The entries should not generalize about `rustc_commit`. **[O]** of the predicates.

## E. Net position

- The only prior statements in the lane's own voice on this surface are the two knowledge entries
  (l7-02, arc3-r10), their README rows (63, 159) and the l8-01 row (68), the SKILL.md craft-rule clause
  (301-302) and the README Known-gaps bullet (216); everything else is receipt, round-history, or census
  material. **[O]** from the classified 356-line hit set.
- No prior statement anywhere in the lane asserts a **positive** `.dep-v0` observation (a non-empty
  `auditable_metadata` package list). Every `.dep-v0` mention is an absence/null or a limitation string.
  R30-C1's positive class is new; it corroborates l7-02:9 and supersedes l7-02:10's untested clauses. **[O]**
  of the hit set, **[I]** of the corroboration.
- No prior statement predicts refusal signatures for this verb; R30-C2's decision table is new and refines
  l7-02:10's guard sentence (§D.2). **[O]/[I].**
- The 6.7.0 evidence-id family (r10 entry, rounds 10–12, rounds 25–26) is untouched by R30's 6.5.0 runs,
  except for the id-transfer constraint in §C. **[I].**

## F. Remaining unknowns

- Whether the R30-C1/C2 counters record any repeat or second path (decides the O5 relation, §D.5) — **[U]**;
  not visible from the frozen predicates and the excluded round-30 tree.
- Whether the L1 appends a supersession pointer to l7-02 or leaves it byte-identical and cites only from the
  new entries (both allowed; §D.6) — **[U]** (L1 decision).
- Round-22's `catalog_zero` semantics were confirmed only from `count-c1.py`'s docstring (T1 = six unrelated
  verbs); the exact counter revision behind the C1Refusal stdout was not re-derived — **[U]**, peripheral.
