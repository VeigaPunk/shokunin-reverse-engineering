# Round 84 — a claim names its counter; a mutant dies only by its declared case; publication is not analysis

Base `043b89a25241710a68b45526c3287fb3c8d907c3`; declaration
`e0de2088a7bddc16305357f90ac7e889fa0a0d11` (three counters, the frozen mutant table and
`plans/round-84-claims.md`); first container `a5663ddedd157bb9113928f5fe80509d6f3fc7a1`
(`.ufo/waves/round-84/claims.json`). One v1 wave `r84-w1` (14 seats). The round-83 outside
review is carried in, not rewritten: its routed "full counter path before the next freeze" is
C1's surface, its "pin fixture identity and add boundary cases before the next predicate" is
C2's declared cases, and its 12-word quote correction is appended to `round-83.md` at round 84.

## Declared claims

| claim | axis | before | after |
|---|---|---|---|
| R84-C1 `tools/round-84/freeze-precheck.py` | calibration | maintained audit exits 0 on the round-83 container (FLAGGED/INSTRUMENT_NONE, disclosed) — refusals 0/1 | round-83 container refused with `CLAIM_NO_COUNTER_PATH:R83-C1`, round-84 container CLEAN, refused 1/1 accepted 1/1, `instruments-only` control accepts the defective container |
| R84-C2 `tools/round-84/mutation-closure.py` | depth | same frozen table at BASE: killed 4 of 13, 9 survivors (`pre/c2-base.json`, exit 1) | killed 13 of 13 by declared cases, survivors/inconclusive/red-pristine none, exit 0 |
| R84-C3 `tools/round-84/nested-sqfs.py` | coverage | nested sub-images below depth 1 is an unmeasured Frontier bullet; the counter does not exist at BASE | 9/9 arms on a reproducible three-level LE v4 gzip chain, file-count control firing, exit 0 |

## What moved, and only what moved

[observation] C1: the maintained post-hoc audit (`tools/round-29/freeze-gate.py`) audits 58
containers at BASE, flags `round-83` with `INSTRUMENT_NONE`, and exits 0 because the ledger row
is disclosed (`pre/c1-maintained-gate-base.json`). The new prefreeze gate refuses that same
container by its claim id and accepts the round-84 container whose three predicates each name
their counter path (`l1/scores/c1-at-container.json`, exit 0). The cheap rule that skips the
per-claim work — accept when `instruments` is non-empty — accepts the defective container
(`control.accepted true`), so the target is failable, not satisfied by container shape.

[observation] C2: at BASE the frozen 13-row table kills 4 (floor, failure, binder, membership)
and leaves 9 survivors — the recorded round-82 seven (`pin-call`, `static-refusal`,
`source-mined`, `source-date`, `source-base`, `source-plan`, `source-entry`) and the round-83 two
(`sb-header-position`, `sb-duplicate-last`). A survivor whose declared case does not exist is
scored a survivor, never a pass (QUALITY 138), so the nine absent declared cases are the work.
The nine required cases are: `runtime-pin-mismatch-refused`, `static-defect-no-execution`,
`sourced-row-rejected-status`, `sourced-row-wrong-date`, `sourced-row-at-base`,
`sourced-plan-missing`, `sourced-entry-uncited`, `late-single-header`,
`duplicate-target-second`. The sourced-arm cases must invoke the production `sourced_arm`
(parameterized by keyword defaults for row id and base revision) rather than re-typing its
expression — the round-82 MutationGates finding.

[observation] C3: at `--max-depth 3` all eight oracle members are published at exact paths with
matching sha256, but the envelope reports `coverage partial`, one `depth-limited` gap at
`firmware.bin_extract/inner-b.sqfs_extract/inner-c.sqfs_extract`, and `analysis_depth null` for
the level-3 files; at `--max-depth 4` the same eight members publish with `coverage complete`,
no gap, and `analysis_depth 3` for level-3. The file-count control fires because the file list is
identical at both depths — publication is not analysis. S302 (the provider's own
`depth-limited` remedy text) names the fix; S301 (`mksquashfs -repro-time`) grounds the
reproducible fixture identity.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M84-1 | a fixture that cannot pass its own gate | `l1/mistakes/m84-1-fixture-instruments.json`: a mutant fixture builder that omits `instruments` fails `clean-accepted`, `pin-mismatch-refused`, `cheap-rule-accepts-defective` (exit 1) | the tool's own `--selftest` at development time (the live failure was observed before the declaration commit) | fixture builder carries `instruments`; the mutant shows the check able to fail |
| M84-2 | a registry row names a used-by file that does not exist yet | `l1/mistakes/m84-2-census-before.txt`: `E11 S301 missing used-by corpus/lessons/round-84.md`, `E11 S302 missing used-by …` (census exit 1); after this lesson exists the round-end root census exits 0 | `scripts/sources-census.sh validate` E11 (the census, not a reviewer) | append registry rows only after their citing files exist, or expect E11 and create the files before the round-end census |
| M84-3 | a mutation row that cannot fail | `l1/mistakes/m84-3-single-edit-floor.json`: the single-edit `floor` mutant is verdict-neutral because `len(cases) < PRISTINE_FLOOR` is guarded again by `summary[0] < PRISTINE_FLOOR`; the single-edit row survives at BASE | the base arm's unexpected 3-killed result, then the mutant's own survivor status | the row is one behavior with two edits (`edits` list); the table records why, and the two-edit row is killed by `floor-refused` |
| M84-7 | an after-receipt produced by the working-tree instrument while the claim pins Git blobs | `l1/archive/c1-at-container.json` (16:46:07) was emitted by a worktree copy edited at 16:46:03 (`4aae3f26…`) while the pinned blob is `602239f5…`; SentinelScope F1 and ReviewerC1 H3 both prove it | a dispatched sentinel's digest census (the lane had no such check) | every landing receipt is now executed only after the instrument bytes are committed, and the stale receipt is archived rather than cited; the report names both digests |
| M84-6 | an absent field scored as a null value | `w1/ReviewerC3/verify.json` probe `d3_level3_key_drop`: the counter accepted a level-3 entry whose `analysis_depth` key was removed, because `.get("analysis_depth")` returns `None` for both | ReviewerC3's probe battery (a dispatched reviewer), then the new `dropped-analysis-depth-fails` selftest case | the arms require the key present (`"analysis_depth" in entry`) before accepting null; the selftest case fails on a dropped key |
| M84-5 | a table-supplied id used as a path component without containment | `l1/waves/round-84/w1/SentinelScope/esc-receipt.json` and `esc-receipt-abs.json`: a mutant id `../../escaped-dotdot` and an absolute id are joined under `--work/mutants/`; the absolute one wrote outside the work root | SentinelScope's escape probes (a dispatched attack seat) plus the new `unsafe-id-refused` selftest case | `unsafe_component()` refuses separators, parent and absolute spellings before any write and scores the row `inconclusive:unsafe-mutant-id`; the selftest asserts no escape path exists after the attempt (QUALITY 119/127) |
| M84-4 | a scorer field that reads two mutually exclusive arms conjunctively | the first `score_envelope()` returned `met = all(arms)`, and the coverage pair `coverage-partial`/`coverage-complete` can never both hold, so per-run `met` was dead | the tool's own selftest failed on both clean envelopes at development time | the per-run `met` field was removed and the aggregate is decided in `score()`. This is recorded as **not re-demonstrable on current bytes**: the field is gone, a revert of the code alone no longer fails the selftest. It is a design correction, not a demonstrated fix. |

## Gate

| item | decision | source opened 2026-11-04 | judgment |
|---|---|---|---|
| S301 mksquashfs(1) `-repro-time` | admit (mined, tier A) | https://man.archlinux.org/man/mksquashfs.1.en, snapshot 57 790 B sha256 `3ea8c1a1…`, derived-text lines 168-174: “build a reproducible filesystem image. This is equivalent to specifying -mkfs-time TIME and -inode-time TIME, which achieves reproducibility by setting all timestamps to TIME.” (24 words) | grounds deterministic fixture identity for carrier-class measurements; it says nothing about extraction behaviour, and two different source trees still differ |
| S302 rea-agents 6.5.0 `FirmwarePublication.js:17` | admit (mined, tier A) | installed package file sha256 `bb4f3246…`, line 17: “Rerun extract_firmware with a higher max_depth (up to 10) and a fresh output_directory to descend into this path.” (18 words) | the provider's own remedy text for a `depth-limited` gap; it does not establish how deep any vendor image nests |
| S303 npm tarball as gap-taxonomy authority | reject | https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz, opened 2026-11-04; the registry already holds this URL in five scopes (S083/S090/S092/S119/S123) | a tarball is not an anchored document; S302 is the anchored authority. Flip: a published REA documentation URL anchoring the gap taxonomy |

Census: 205 rows / A187 B10 C8 / mined 184 rejected 21 before; 208 / A190 B10 C8 / mined 186
rejected 22 after. `validate --root /home/vgpnk/Projects/shokunin kaidoku` exits 0 at round end
(W04 duplicate-URL warnings retained, one of them S303's own).

## Wave and filing

`r84-w1`: 14 seats in one v1 wave — 5 executor, 2 scribe, 1 scout, 2 reviewer, 1 critic,
1 mutation-tester, 1 sentinel, 1 connector; attack roles 4/14 = 28.6 %; one connector; the L1
holds the planner seat (the validator rejects a planner role). Wave accounting, dead seats and
the integrated measurement are appended below at settlement.

## Limits and carry-in

- C1 refuses *metadata* defects, not wrong predicates: a container that names a path and pins it
  still passes even if the named script is not the one that measures the claim. The gate is a
  naming/pinning check, not a semantic binding.
- C1's gate is a *naming and pinning* check, not a semantic one. ReviewerC1 demonstrated
  two false-accept paths for the general property: a counter path that appears only in
  `kill_rule`/`id`/`axis` (or a negated sentence) also satisfies it, and the pin is compared at
  the measured revision, so an undisclosed re-pin passes this gate. The second is covered by the
  maintained gate's `INSTRUMENT_REVISED` finding between freeze and measured; the first is a
  disclosed limit of this finite two-container claim, not a repaired mechanism (the instrument
  bytes the reviewer attacked are the bytes that ship, so its verdict stays true of the landed
  tool).
- The C1 receipt produced before landing (`l1/scores/c1-at-container.json`, 16:46) was executed
  from a working-tree copy that had just been edited; ReviewerC1 (H3) showed it is not a receipt
  over pinned bytes. It is archived under `l1/archive/` and superseded by the landing receipt
  executed from the committed blob at the measured revision.
- C2's kills are selftest-case kills. A case that asserts a defect token without exercising the
  production path is still a kill by the letter of the rule; the reviewers and the mutation
  tester attack that reading, and any surviving independent mutant is reported below.
- C3's counter enforces less than its prose in three named places (ReviewerC3 F2/F5): the
  three fixture pins are recorded but not compared to a frozen value, so a recipe change would
  still pass while the oracle moves with it; A3's root check is a suffix match; and A9 pins the
  unblob identity but not the `sasquatch` child that decodes v4. Cross-run fixture identity was
  verified outside `met`: the pilot, ExecNested's independent build and ReviewerC3's rebuild all
  produced pins `a e82c5995…`, `b 7d2dd0e7…`, `c f68b42fa…` byte-for-byte. The `analysis_depth`
  key-presence repair (F3) makes A4 stricter than the previous bytes; it cannot make the claim
  easier and is disclosed as an instrument revision with old and new digests.
- C3's class is lane-built: no vendor carrier, gzip only, block 4096, three levels, unblob 26.6.4.
  `analysis_depth` is the provider's own field, not an independent observation of the bytes.
- Carried debt, unclosed: the seven round-82 mutation survivors are closed *as declared cases*
  only if the integrated selftest cases are real detectors (see the wave block); the round-81
  old-counter outer-selftest, the receipt-auth/gate-exits and r63 record-section sweeps, and the
  concurrent-replacement race remain named debt; the round-80/81 freeze rows stay FLAGGED as
  filed.

## Wave (appended at settlement)

`r84-w1`: 14 seats in one v1 wave — 5 executor (ExecPcDetectors, ExecSbDetectors, ExecMutantBase,
ExecNested, ExecGateForge), 2 scribe (ScribeKnowledge, ScribeSources), 1 scout (ScoutLoci), 2
reviewer (ReviewerC1, ReviewerC3), 1 critic (CriticClaims), 1 mutation-tester (MutationTester), 1
sentinel (SentinelScope), 1 connector (ConnectorScope); attack roles 4/14 = 28.6 %; one connector;
the L1 held the planner seat. All 14 settled and all 14 left a report (`l1/wave-accounting.json`);
no seat was replaced and no seat died. The dispatcher's results artifact records every `output` as
null with its own note that the orchestrator kernel restarted mid-wave, so the seat *report files*
are the evidence and the accounting records that limit instead of inventing outputs. Attack yields
integrated before landing: the sentinel's id-escape probe (M84-5), the reviewer's absent-key probe
(M84-6), the critic's control-order refutation (per-container control), its table-drop refutation
(frozen-table identity) and its depth-4 vacuity refutation (deepest-level arm). The scout's F12
(registry case counts) and F7 (docstring wording) are corrected in the final commit; its F8/F9
(round-82 and round-83 target revisions) are disclosed in those containers' supersessions.
