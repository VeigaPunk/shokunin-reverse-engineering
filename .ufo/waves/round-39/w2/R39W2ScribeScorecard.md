# R39W2ScribeScorecard — SCORECARD `## Round 39`, LOG round-39 entry, `## Owned axes`/`## Capabilities` rows, SHONEN lines

**Verdict: DEFECTS FOUND** — both author verdicts reproduce and every number I re-derived matches the committed receipts, but the round's *self-assessment surface* is missing or stale at the landing: no round-39 commit touches `SCORECARD.md` or `LOG.md`, there is no `## Round 39` section, and the coverage row still reads `126/126` while command A measures `128/128` at `52b0eb29`. The four artifacts this seat was asked to draft are therefore the repair, not a copy edit; I wrote them against committed bytes at `52b0eb29` (and re-measured every count I put in them).

Seat: R39W2ScribeScorecard (leaf). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`; controls `72359309a052284029f8e0331ef211a67fe4b13b`; base `a2f64e1da78afcf8cc39287106604dbcc270844c`; measured surfaces `6fdaf4f1`, `52b0eb29`. I wrote only this report and `.ufo/waves/round-39/w2/artifacts/R39W2ScribeScorecard/`; no VCS mutation, no product edit, no judge run, no subagent.

## 1. What I attacked, and the axes

The thing attacked is the **landing's readability as a scored record**: whether `SCORECARD.md` (round section + owned-axis and capability rows), `LOG.md` and `SHONEN.md` would, if written from the committed state, state the round's coverage and depth movement with reproducible numbers, correct revisions, and no claim the bytes do not support.

- **coverage** (primary): every count in the coverage row and round section — 126/126 → 128/128, the two new entries, `missing []`, `dangling []`, and the mapped/unmapped identity of both new stems.
- **depth** (primary): 17/17 → 18/18 rule blocks, craft-section range 81–314 → 81–343, block 18 at `SKILL.md:316-343` with its table after the marker, and whether the new block's citations resolve (`citation_resolved_rules 18`).
- Secondary: calibration (each revision, receipt path, hash and quoted line verified before it entered a draft), and I crossed every wave-2 finding against its own receipt so no draft upgrades an unobserved claim.

## 2. What I ran (exact, read-only)

Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39W2ScribeScorecard` (removed at exit; the two cited outputs are copied into the artifacts dir). No tool was installed or upgraded; no REA, unblob or sasquatch run; no claim counter run by me — I read the committed receipts and the wave-2 re-scores. Nothing was re-run merely to decorate: the only executions were the measurements the drafts themselves assert.

| # | command | exit | result |
|---|---|---|---|
| 1 | command A verbatim from `SCORECARD.md:88-113` (here as `cmdA.py`) at `a2f64e1d`, `8fcda41c`, `6fdaf4f1`, `52b0eb29`, `e40a25df` | 0 ×5 | `126/126` + `17/17` at the base; `127/127` + `18/18` at the freeze; `128/128` + `18/18` at `6fdaf4f1`, `52b0eb29`, `e40a25df`; `missing []`, `dangling []` everywhere; `coverage_score 10.0`, `depth_score 10.0` |
| 2 | `git rev-parse <REV>:<path>` for the five frozen instruments at the freeze / `6fdaf4f1` / `52b0eb29` | 0 | `c1-counter.py 182308e4…`, `c2-counter.py bc20933b…`, `sqfs-triage.py b5c5379a…`, `heldout-gen.py 08869713…`, `plans/round-39-claims.md f6707233…` — identical at all three |
| 3 | triage block = `SKILL.md` bytes from `<!-- sqfs-triage-table v1 -->` to the next `\n## `, rstripped, sha256 | 0 | 3084 B, `2902dcbd…` identical at `8fcda41c`, `6fdaf4f1`, `52b0eb29` |
| 4 | `git log --oneline a2f64e1d..HEAD` | 0 | six commits (`8fcda41c`, `72359309`, `3c07eed7`, `6fdaf4f1`, `52b0eb29`, `e40a25df`); **none** touches `SCORECARD.md` or `LOG.md` |
| 5 | `jq` over `.ufo/waves/round-39/l1/scores/{c1-at-base,c1-at-6fdaf4f1,c2-at-freeze,c2-at-6fdaf4f1}.json` | 0 | see §4 |
| 6 | `jq` over the nine `controls/ctl-c1-*.json` and over `controls/ctl-c2-dev-scores.json .controls` | 0 | see §4 and F6 |
| 7 | line measurement of `SKILL.md` craft section and `PROVINCE.md` `## Adjacent` at the base and at `52b0eb29` | 0 | craft `81-314` → `81-343`; `## Adjacent` `97-125` unchanged; round-39 PROVINCE additions at `:378-384` |
| 8 | `git diff --stat 72359309 -- .ufo/waves/round-39/controls/` | 0, empty | the control receipts in the worktree are the committed ones |

## 3. Drafts produced (all under `.ufo/waves/round-39/w2/artifacts/R39W2ScribeScorecard/`)

| file | what it is | where it applies |
|---|---|---|
| `SCORECARD-round-39-section.md` | the `## Round 39` section in the round-38 form: base/freeze/controls/data revisions, freeze-integrity paragraph, the two-row claim table (`claim \| axis / surface \| before \| after \| counting command \| measured at \| verdict (author)`), owned scores, capability announcement, wave-2 falsification record, planned/retired | appended after the `## Round 38` section in `SCORECARD.md` |
| `LOG-round-39-entry.md` | the `## 2026-10-26 — round 39 …` entry: dispatch, freeze, controls, C2 data, C1 landing, scores, freeze integrity, surfaces, sources, assimilation, lesson/QUALITY/routed, wave-2 outcome, tooling line | appended to `LOG.md` |
| `owned-axes-rows.md` | the exact `SCORECARD.md:23` (coverage) and `:24` (depth) rows with only the round-39 changes applied, generated by string surgery on the current bytes so no history is retyped; calibration row explicitly unchanged | replaces those two rows |
| `capabilities-rows.md` | two `## Capabilities` rows — standard BE SquashFS v4 recursion; executable SquashFS `extract-firmware` outcome triage — each with pointers and its scope exclusions | appended to the `## Capabilities` table |
| `SHONEN-round-39-lines.md` | the four checklist `asserted:`/`boundary only:` lines at round 39 (craft `81-343` + 18/18; the six-carrier end-to-end run; the interpreter-executed triage table; `## Adjacent` 97-125 with the open PROVINCE pointer named, not hidden) | replaces the four assertions in `SHONEN.md` |
| `commandA-and-pins.txt` | command A output at five revisions, frozen-instrument blob hashes, triage-block hashes | receipt shown at §2 rows 1–3 |

## 4. Verified true (evidence), and what each draft therefore asserts

- **R39-C1 score.** `.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json`: `carriers_matched 6`, `target 6`, `met_target true`, no false binding, `frozen_path_changed []`, `revision 6fdaf4f1`. Before: `controls/ctl-c1-0-do-nothing.json` at the freeze gives `carriers_matched 0`, `met_target false`, `carriers_unchanged true`, every documentation binding false (`coverage_map_row`, `entry_present`, `frontier_note`, `province_core_row/section`, `sourced`) with `symlink_coverage`/`xz_leg` true; at the base the counter is `unevaluable: carriers.json absent at freeze` (`c1-at-base.json`, exit 2). Exit 1 for the freeze arm is in `.ufo/waves/round-39/w2/R39W2C1Rescore.md`.
- **R39-C2 score.** `c2-at-6fdaf4f1.json`: `matched 20`, `n 20`, `met_target true`, `met_target_consistent true`, `bindings_false []`; the freeze arm is exit 2 `no_manifest_at_rev` with `frozen_paths_changed []` (`c2-at-freeze.json`). The receipt's 20 carrier entries are 16 `after`-arm and 4 `before`-arm envelopes over 8 distinct labels, each with `class_match`, `digest_ok`, `commit_ok` and `regen_ok` true.
- **Controls.** Nine C1 receipts (`ctl-c1-0`…`ctl-c1-9`, id 5 skipped): seven carry `expected_exit 1` / `verdict as-expected` (`ctl-c1-1,2,4,6,7,8,9`), `ctl-c1-0-do-nothing.json` is a bare counter receipt (`carriers_matched 0`, `met_target false`, no expected/verdict fields), and `ctl-c1-3` is `expected_exit 0` / `verdict unexpected-exit` with `carriers_matched 6` and `frontier_note false` — the disclosed re-minted-fabrication limit. C2 control file: `CTL-C2-0` 0 exit 2, `CTL-C2-1` 4, `CTL-C2-2` 6, `CTL-C2-3` 10, `CTL-C2-4` 6, `CTL-C2-5` 0 exit 2 and `.formatfix` 8, `CTL-C2-6` 0 exit 2 and `.formatfix` 12, plus `FREEZE-table-informational` 20 (`met_target true`) — the design-data row, which is not a control and which both drafts label as carrying no evidence.
- **Surfaces moved.** `PROVINCE.md` `## Round-39 additions to Core` heading `:378`, `squashfs_v4_be` row `:382`, frontier note `:384`; `corpus/README.md` coverage-map rows `:93`/`:94`, knowledge rows `:203`/`:204`, Frontier line `:245`; entries `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md` (source line 3 = S122) and `…-r39-sqfs-outcome-triage.md`; SOURCES rows `S118`–`S122` (`corpus/SOURCES.md:124-128`), appended, tier A.
- **Proxies.** command A: coverage `126/126 → 128/128`, depth `17/17 → 18/18`, both `10.0`; the freeze reads `127/127` because the triage entry lands there. The drafts state the movement and keep the score at `10 → 10` (finite proxies retire no axis).
- **Capability evidence.** All six carriers were re-run by a wave-2 seat (`.ufo/waves/round-39/w2/R39W2C1AxisFit.md` §0), five more seats reproduced K1/K2/K3/K4/K6 (`R39W2ReproK{1,2,3,4,6}.md`), K5/K6 rebuild byte-for-byte (`R39W2K5K6Rebuild.md`), and H01–H20 re-derive from their own carriers in three seats (`R39W2HeldRepro{A,C,D}.md`). C1 33-case and C2/interpreter 27/35-case selftests are green in independent receipts (`R39W2C1Rescore.md`, `artifacts/R39W2C2Rescore/*-selftest.txt`).
- **Freeze integrity.** Row 2 of §2 plus `frozen_path_changed []` from both counters; the only post-freeze `SKILL.md` edit (`52b0eb29`, +28 lines at `:1328+`) is outside the triage block, which is byte-identical (row 3).
- **SHONEN ranges.** `SKILL.md:81-343` and `PROVINCE.md:97-125` measured at `52b0eb29`; safety refusal `:116-118`; round-36 tooling bullet `:119-125`.

## 5. Findings

**F1 (major — the axis move is unrecorded on the scored surface).** `git log a2f64e1d..HEAD -- SCORECARD.md LOG.md` is empty (exit 0, no output); `SCORECARD.md` has no round-39 section and `SCORECARD.md:23` still reads "126/126 knowledge files mapped after the round-38 landing" while command A gives `128/128`. Reproduces `R39W2C1AxisFit.md` D1. *Discharged by this seat's drafts* (`SCORECARD-round-39-section.md`, `owned-axes-rows.md`, `LOG-round-39-entry.md`); until they land, a closure reading `SCORECARD.md` alone cannot see a coverage change this round.

**F2 (moderate — the claim named a surface the landing did not edit).** The frozen claims say the moved surface is `PROVINCE.md:156-157`, but those lines are byte-identical at the base and at `52b0eb29` (base `:156-157` = the `sasquatch` Frontier bullet carrying its round-36 bracket; the round-39 supersession lives at `:384`, ~226 lines below). Two live sentences still assert big-endian SquashFS stays Frontier (`:157` and the round-38 note `:376`). Reproduces `R39W2C1AxisFit.md` D2. *Open.* The drafted section and SHONEN lines state the append-only move accurately and name the duplicate sentences rather than implying they were edited.

**F3 (minor — a false docstring inside frozen bytes).** `tools/round-39/heldout-gen.py` `corruption_bad_minor`'s docstring says an `s_minor` 5 image matches no v4 handler, while the landed class measures handler `squashfs_v4_be`, `extraction_failed` true, gap `extractor-failure` (`R39W2C2Shortcut.md` D1). The frozen claims and the recipe agree with the measurement, so only the docstring is wrong; editing it now would trip `frozen_path_changed` for every C2 score. *Open, erratum only* — recorded in the drafted section, not repaired.

**F4 (minor — the entry's voice outruns its receipts).** `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:37-38` attributes a stripped-`PATH` before-arm to "the same carriers", but only K1–K4 have such receipts; no K5/K6 before-arm exists (`R39W2C1EntryReview.md` D2). *Open.* The drafted capability row therefore claims the after-behaviour only, not an absent-dependency arm on K5/K6.

**F5 (minor — two SOURCES quote anchors are imprecise).** S118's quote is byte-exact only after whitespace normalisation and spans docstring lines 53–55 (the lesson says "51-56"; the docstring closes at 57); S121's quoted string is in `debian/rules:17`, not in the row's `unsquashfs.c` URL (`R39W2SrcReopen.md`). No recorded size or sha256 is affected. *Open, wording.*

**F6 (minor — the "C2: 8 controls" count is not reproducible from the committed file).** `72359309`'s `ctl-c2-dev-scores.json` carries seven named controls (`CTL-C2-0`…`CTL-C2-6`), two `.formatfix` re-scores of 5 and 6, and one informational row — nine scored rows, seven named controls, while the commit message and the lesson say "C2: 8 controls". No control reaches 20/20 under any count. The drafted LOG entry states the reproducible count and flags the discrepancy instead of repeating "8".

**F7 (observation — the C2 target does not yet mean "triage").** The production table scores 20/20 on the 20 development envelopes (labelled informational, correctly not treated as a control), and a table whose last row is all `*` also reaches 20/20 while mis-labelling an out-of-set envelope (`R39W2C2Shortcut.md` D2, landed table on the safe side). Carried into the drafted section as a disclosure and into `planned (round 40)` as an out-of-set-envelope clause, not as a defect of the landing.

**F8 (observation, not a landing defect).** `c2-counter.py --selftest` leaks one `gen.*` fixture per case into the shared scratch root (`R39W2C2Rescore.md` §7); harmless to the landing, relevant to concurrent seats. Not carried into any draft.

## 6. Out of scope / limits of this seat

- I did not run the C1/C2 counters, REA, unblob or sasquatch; every claim score in the drafts is read from `.ufo/waves/round-39/l1/scores/` and the wave-2 receipts, and the provenance sentence in the C1 row is attributed to the seats that ran it, not to me.
- I did not re-fetch any SOURCES URL; F5 is reported from `R39W2SrcReopen.md`'s fetch table (which records HTTP 200 and matching sha256s), not from my own fetch.
- The drafted `planned (round 40)` items are proposals grounded in the two disclosures the freeze itself makes (re-minted fabrication reaching 6/6 carriers; a default-row table reaching 20/20) plus the AVM-BE second choice carried from round 38 and the still-open R36-CL5. **[INFERENCE]** where I rank them; the selections are not measurements.
- I did not edit `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `PROVINCE.md`, `SKILL.md`, `corpus/` or `tools/`; the drafts are proposals for the integrator to apply and re-verify.
- Tooling record: no install or update (nothing needed; `git`, `python3`, `jq` only).
