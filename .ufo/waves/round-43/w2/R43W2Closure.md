# R43W2Closure — closure audit of the round-43 report against committed evidence

Measured lane state for every check below: lane `HEAD = 5856614ac4bf7f2363bbcd1956644474a82108e5`
(parent `77d196c6`), branch `HEAD` (detached), working tree carrying the uncommitted round report
(`M SCORECARD.md`, `M SHONEN.md`, `M .ufo/waves/round-43/w2.ready`, untracked `w2/`). Freeze
`f3f8db389416d094b1ddeb1215ddcf914bfc0d1c` is an ancestor of `77d196c6` and of HEAD; base
`6b9e64fe7e0de202d9383baad5792fbfe039a743` is an ancestor of the freeze. Commit chain
`f3f8db38 → 681360e6 → 09ab56b8 → 77d196c6 → 5856614a` verified by `git rev-parse <c>^`.

## Reviewed surface (what "the final round report" is at this measurement)

No standalone L1 round-report file exists in the lane at this revision (`.ufo/waves/round-43/l1/`
holds logs, dry-run receipts and `scores/` only; `.ufo/waves/round-43/w2/` held no report when read).
The report surface reviewed is the round record that exists:

- `SCORECARD.md` `## Round 43 — …` section (uncommitted, header at line 3487 in the working tree);
- `SHONEN.md` four `Round 43:` assertion lines (uncommitted);
- `PROVINCE.md` `Round-43 frontier note` (committed at HEAD, `+6`);
- the two landed knowledge entries the record cites
  (`corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md`,
  `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md`) and `corpus/README.md` rows;
- the committed evidence the record points at: L1 score receipts
  (`.ufo/waves/round-43/l1/scores/`), controls (`.ufo/waves/round-43/controls/`),
  held-out set (`corpus/evidence/round-43/c1/heldout/`), C2 landing
  (`corpus/evidence/round-42/local-sources/`, `corpus/evidence/local-sources.json`),
  and the w1/w2 wave documents.

If the L1 files a separate wave-2 closure report after this seat, that file was not present and is
not covered here.

## Factual corrections

**C1 — `coverage 10 → 10` does not reproduce; the lane's own command A gives 9.93 at every
post-base revision of this round.** Ran the exact command-A recipe from `SCORECARD.md`
`## Measurement recipes` (git objects only, no worktree reads):

| rev | knowledge files | mapped | missing | coverage_score | rule blocks | citation-resolved | depth_score |
|---|---|---|---|---|---|---|---|
| base `6b9e64fe` | 135 | 135 | `[]` | **10.0** | 21 | 21 | 10.0 |
| freeze `f3f8db38` | 136 | 135 | `["2026-10-27-sasquatch-release-matrix"]` | **9.93** | 21 | 21 | 10.0 |
| measured `77d196c6` | 136 | 135 | `["2026-10-27-sasquatch-release-matrix"]` | **9.93** | 21 | 21 | 10.0 |
| HEAD `5856614a` | 137 | 136 | `["2026-10-27-r43-sqfs-triage-v4-scored"]` | **9.93** | 21 | 21 | 10.0 |

Cause, from committed bytes: the assimilation entry `2026-10-27-sasquatch-release-matrix` was first
added at `eadcbfa5` (before the freeze) and got its `## Coverage map` row only at HEAD; the scored
C1 entry `2026-10-27-r43-sqfs-triage-v4-scored` was first added at HEAD with a `## Knowledge` index
row (`corpus/README.md:220`) but **no `## Coverage map` row** — `grep -n r43-sqfs-triage-v4-scored
corpus/README.md` returns line 220 only. The SCORECARD sentence "Owned scores remain saturated:
coverage `10 → 10` …" is therefore false at the report's own measured revisions; the same sentence's
`depth 10 → 10` and `calibration 10 → 10` do reproduce (depth 21/21, calibration 10 at base).
Artifact: `command-A.txt`.

**C2 — `LOG round-43 entry` is cited twice and does not exist.** `SHONEN.md` line 10 ends
"… matched 78/78, exit 0, LOG round-43 entry." `grep -n "round-43\|Round 43" LOG.md` returns nothing
at HEAD or in the working tree; `LOG.md` is not modified. The end-to-end promotion checkbox requires
a logged task, so at this state the assertion's pointer is dangling.

**C3 — the report is not committed evidence.** `SCORECARD.md` and `SHONEN.md` are `M` in
`git status --porcelain` at this measurement. Every number below was checked against committed lane
bytes, but the report text itself is working-tree-only until the L1 landing commit.

**C4 — no tool-install statement exists in the round record, and the two statements that do exist
conflict with observable host state.** The SCORECARD/SHONEN/PROVINCE round-43 text contains no
install statement. The w1 statements are "no tool installed, upgraded or removed"
(`w1/R43ScribeEntry.md:15`) and "no tool installed" (`w1/R43ScribeAssim.md:6`); `R43ScribeEntry.md`
F1 also states the 6.5.0 npx cache "**no longer exists**". At measurement:
`~/.npm/_npx/ad9a3fdbcad992c6/package.json` contains `rea-agents: ^6.5.0` and
`node_modules/rea-agents/package.json` reports version `6.5.0`; host global `rea-agents --version`
is `6.7.0`; the frozen generator invokes `npx -y rea-agents@6.5.0` (`tools/round-43/heldout-gen-v4r43.py`
lines 2719 and 2777, `REA_PACKAGE` line 189); `run.json` records `rea-agents@6.5.0`. So either the
cache existed (F1 false) or the data run's `npx -y` fetched it into `~/.npm/_npx` (a package
installation outside PATH that no round statement records). [INFERENCE] the cache fill happened
during the post-freeze data run, not wave 1; the committed record does not date it. The round record
should state which, because the C1 score's tool identity rests on that package.

**C5 — no explicit residual-risk statement.** The round-43 SCORECARD section states only the C2
verdict and "No C2 capability row is credited…". The plan's `## R43-C1 … Disclosed limits` /
`## C2 … Disclosed limits` blocks are the only enumeration of what is not proven (evaluator
agreement cannot distinguish tables; OOD vacuity H25/H26; generator-self-reported tuple check;
single seed draw; copies bind this checkout's pins; duplicate-key last-wins footnote), and the round
record does not restate them. Unlanded items the record does not name: `tools/round-42/prefile-gate.py
--round 43` run (plan amendment 7 — `.ufo/waves/round-43/l1/prefile-gate.json` absent), the required
`considerthese/` report line (`considerthese/` does not exist), and wave-2 settlement. Routed
`R40-CL2` remains open as the record says (`corpus/lessons/round-42.md:69`).

**C6 — S135/S136/S137 row-vs-entry fetch records disagree, and the frozen S137 row's digests have no
retained bytes.** Committed `corpus/SOURCES.md` rows (frozen at `f3f8db38`) vs the committed
`2026-10-27-sasquatch-release-matrix.md` source lines:

| row | SOURCES.md (frozen) | entry `source:` line |
|---|---|---|
| S135 | HTTP 200 at `2026-10-27T08:17:52Z`, 1068 B, `67303bbd…` | "opened … at `2026-10-27T08:08Z`", same bytes/hash |
| S136 | fetched `08:18:09Z`, 107313 B, `cb42cd61…` | fetched `08:18:38Z`, same bytes/hash |
| S137 | fetched `08:19:46Z`, 349255 B, `150c7584…`; later 349251 B, `e5f85ce0…` | fetched `08:20:30Z`, 349255 B, `89e7377d…`; second `09:05:48Z`, 349255 B, `56632d0f…`; r42 349266 B, `71ebf160…` |

The entry's page digests are corroborated by retained bytes
(`w1/artifacts/R43ScribeAssim/receipts/sasq-releases-r43.html` = `89e7377d…`,
`sasq-releases-r43-f2.html` = `56632d0f…`, API `rel-r43.json` = `cb42cd61…`, round-42
`sasq-releases.html` = `71ebf160…`). The frozen row's `150c7584…` and `e5f85ce0…` appear in no
retained artifact (`grep -rn 150c7584` / `e5f85ce0` over `.ufo/waves/round-43` → no hits). The S135
row and the plan/entry differ by 9m52s. Not a falsification of the matrix claim — the matrix rests
on the retained API capture, whose digest both sides share — but the registry row and the entry do
not describe the same fetches and a rechecker cannot reproduce the row's page digests from lane
bytes (page bytes are mutable by construction).

**C7 — the C2 score chain's child receipts and upstream inputs are gone; only embedded stdout
survives.** Both committed C2 score receipts bind `gate_receipt_sha256` /
`copy_audit_receipt_sha256` to paths under `/fast/scratch/hyaku/kaidoku-r43/l1-c2-score-final/`,
and the copy-audit invocation names `/fast/scratch/hyaku/kaidoku-r43/l1-c2-inputs/` (Go trees,
`rea6.7.0.tgz`, `rea6.5.0.tgz`). Neither directory exists now (`ls /fast/scratch/hyaku/kaidoku-r43/`
lists `l1-assim l1-c1-controls-final l1-c1-score l1-diag l1-license l1-verify w2` only). What remains
is the wrapper receipts' embedded `stdout_text`, which I read and counted. The record does not state
this limitation.

**C8 — round-43 control artifacts are post-freeze; the plan's "control tables … committed in the
freeze" is not literally satisfied by the round-43 copies.** `git ls-tree -r f3f8db38 --
.ufo/waves/round-43/controls` → 0 files; the tree first appears at `681360e6` (41 files, parent
`f3f8db38`). The control *documents* the receipts cite (`.ufo/waves/round-42/controls/c2/*`, e.g.
`CTL-C2-1-catch-all.md` `265216e8…`, `CTL-C2-7-lookup.md` `7f193c8f…`, `CTL-C2-REF-v4-precedence.md`
`70f908e0…`, `CTL-C2-0-base-SKILL.md` `94d13b44…`) are frozen ancestors and their digests match the
C1 control summary. Whether "committed in the freeze" is met by those sources or requires the
round-43 copies is a plan-reading question for the L1; the byte facts are as stated.

**C9 — "Wave 1: 32 seats, all settled" is true only as delivery, not as a clean sweep.** 32 results
in `r43-w1-results.json`, 32 `w1/*.md` reports, names match one-to-one; the 32 verdicts are 13
`DONE`, 10 `CONFIRMED`, 8 `DEFECTS`, 1 `UPDATE`. "All settled" is accurate; a reader taking it as
"no findings" would be wrong.

**C10 — one SCORECARD phrase describes the C2 stop as the tool being "overstrict" on the raw
numstat while the same 3-insertion count is also frozen in the plan.** `plans/round-43-claims.md`
states "BASE→REV numstat is exactly 3 insertions and 0 deletions"; `tools/round-43/c2-score-r43.py:194`
implements `sources_numstat == "3\t0\tcorpus/SOURCES.md"`; the committed diff is `4 0
corpus/SOURCES.md` (S135, S136, S137 rows + one blank line). The tool matches the frozen plan text;
the frozen plan's count is the one the committed diff falsifies. The report's parenthetical
("three S135–S137 rows plus a blank separator") is exact.

## Verified as written (no correction)

Hashes, all recomputed from committed bytes or the exact files read:

- v4 table region `SKILL.md`: **13 856 B, sha256 `92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2`**
  at `d1681696`, base `6b9e64fe`, freeze `f3f8db38`, `77d196c6` and HEAD (extraction: marker line →
  end of first markdown table; marker at line 525, `actions` 526, table 527, 15 rules when run through
  `tools/round-42/sqfs-triage-v4.py --skill SKILL.md --table-only`, exit 0).
- Whole `SKILL.md` blob `3268fe77d27272b89d75b8f88f75c24c24158407` at freeze, `77d196c6` and HEAD;
  base blob `68f7fe4e…`; `Status — unscored claim` paragraphs: 0 at base, 2 at freeze (R42-V3 repair
  before the freeze, as SHONEN states).
- Plan `plans/round-43-claims.md` = `0326dff9…`, equal to the C1 receipt's `frozen_units` entry at
  freeze and rev.
- `tools/round-43/c1-counter.py` `3a23e93e…` (= receipt `counter_sha256` = `counter_sha256_at_freeze`);
  `c2-score-r43.py` `459cbccb…` (freeze = rev = worktree); `verify-copies-r43.py` `00b3f7a4…`;
  `tools/round-41/local-source-gate.py` `cafe232a…`; `tools/round-42/sqfs-triage-v4.py` `497bab67…`;
  `indep-eval-v4.py` `7a135dd3…`; `fixtures.json` `9f957663…`; frozen EXPECT source
  `.ufo/waves/round-42/w1/artifacts/R42LocalSrc/build/verify-copies.py` `1f790e10…` at freeze and rev;
  round-42 generator port source `tools/round-42/heldout-gen-v4.py` = `c2b1641a…` at base.
- `git log --oneline f3f8db38..HEAD -- <every byte-frozen path>` is empty; receipt
  `frozen_paths_changed []`, `no_commit_touches_pinned true`.
- Map `corpus/evidence/local-sources.json` at `77d196c6` = `3158cdc9…` (tool constant `MAP_SHA256`);
  18 entries; all 18 `sha256` fields equal the committed copy blobs (17 under
  `corpus/evidence/round-42/local-sources/`, all mode `100644`; S126 entry preserved value-equal from
  base). `corpus/SOURCES.md` at rev = `251ec4a7…`; `git diff --numstat 6b9e64fe..77d196c6 --
  corpus/SOURCES.md` = `4 0`.
- C1 score receipt `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json`: `exit_code 0`, `matched 78`,
  `n 78` (54 named + 24 combo), 45/45 bindings true, `bindings_false []`, `met_target true`,
  `observed_features_match_declared true`, `generator.tuple_check` 78 carriers / `not_equal []` /
  `effective_n 76` / vacuous `["H25","H26"]`, `combo_unseen_majority` 21/24 (`need 12`),
  `lookup` 19/24 with `binding false` ("reported, not bound"), `evaluator_attempts`/`interpreter_attempts`
  exit 0, `manifest_first_add 77d196c6`, manifest `seed f3f8db38…`, generator sha `6ab0114d…`.
- **Independent recomputation:** re-ran the frozen counter
  `python3 -I -B tools/round-43/c1-counter.py --root <lane> --rev 77d196c6… --freeze f3f8db38… --scratch <own scratch> --json-out <artifact>`
  → **exit 0, `matched 78`, `bindings_false []`, `met_target true`**; the produced receipt is
  identical as data to the committed one except `argv`/`regen_argv` (scratch paths) — every other
  top-level key compares equal. Artifact:
  `artifacts/R43W2Closure/c1-rescore-at-77d196c6.json`, `c1-rescore.log`.
- All 14 committed fixtures under `corpus/evidence/round-42/c2/fixtures/` match the receipt's
  `fixture_scope.declared_sha256` (14/14).
- Round-42 stop receipt `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` = `0b4e6026…`
  (blob `9989e1c4…`, added by `d4b4b4fb`, message naming the C02 stop); `exit 1`,
  `bindings_false ["observed_features_match_declared"]`, `matched 78`, C02 `differ ["gap_kinds"]`.
- C2 receipts `c2-at-09ab56b8.json` and `c2-at-77d196c6.json`: identical check map, the only false
  entry `sources_numstat_three_additions`; `exit_code 1`; `gate_exit 0`; `rows_checked 19`;
  `rows_total 137`; `rows_failed []`; `copy_audit_exit 0`, `copy_audit_checks 136`,
  `copy_audit_failures 0`; `s126_preserved true`; `clone_clean true`; `freeze_is_ancestor true`;
  `sources_numstat "4\t0\tcorpus/SOURCES.md"`; `map_sha256_at_rev 3158cdc9…`; `sources_sha256_at_rev 251ec4a7…`;
  `score_tool.sha256 = sha256_at_freeze = sha256_at_rev = 459cbccb…`.
- **Independent C2 checks:** clean `git clone --shared` at `77d196c6` (toplevel asserted, `status
  --porcelain` empty), gate run with no overrides →
  **exit 0, `rows_checked 19`, `rows_total 137`, `rows_failed []`, `table_sha256 251ec4a7…`**;
  `find … -type l` over both copy trees → 0. Copy verifier re-run without the absent upstream inputs →
  **`checks: 136, failures: 3`**, the three failures being exactly `host-state S035
  internal-abi-go1.25.0.tar`, `host-state S035 internal-abi-go1.24.6.tar`, `host-state S081` ("no
  --upstream-dir"/"no --tarball"); all other 133 checks OK, including `host-identity S048 vs
  installed rea-agents 6.5.0 package OK 28 members`. Artifacts: `gate.json`, `gate.err`,
  `copyaudit-noupstream.tsv`.
- Generator refusal: `heldout-gen-v4r43.py --selftest-tuple` → **17/17 passed, exit 0**
  (`artifacts/R43W2Closure/selftest-tuple.txt`).
- Control verdicts read from committed receipts: CTL-C1-0 exit 2 (`no_manifest_at_rev`, counter hash
  both sides), CTL-C1-1 exit 1 (both placements; `seed_matches_freeze` false),
  CTL-C1-2 red exit 3 with `C02 … gap_kinds: declared ['extractor-failure','unpublished-entry'] !=
  observed ['depth-limited','extractor-failure','unpublished-entry']`, green exit 0,
  CTL-C1-3 `controls_at_target []`, all eight shortcut tables reproduced below target,
  CTL-C1-4 baseline `observed_features_match_declared true` (exit 1 on planted-manifest bindings) →
  hand-edited `false`, `envelopes_untouched true`, edit `H01/published`. CTL-C2-0 exit 1 with
  `rows_failed` = the 18 ids, CTL-C2-1 exit 1 `copy-missing`, CTL-C2-2 gate 0 / linter 1 for the
  symlink arm vs gate 0 / linter 0 baseline, CTL-C2-3 gate 0 on a 2-dirty-path tree.
- Round shape: wave 1 = 32 results / 32 reports / 32 spawns in `w1-dispatch.json`; wave 2 =
  32 items in `w2-spec.json`, `spawn 32`, 32 members in `w2/swarm-registry.json`, 32 names in
  `w2.ready.dispatched`.
- Held-out evidence tree at `77d196c6`: 391 files = 78 × {carrier.sqsh, envelope.json,
  rea-full.json, run.json, tree.json} + `manifest.json`.
- Host tool bytes cited by the entry: unblob LICENSE `67303bbd…`, `handlers/filesystem/squashfs.py`
  `2d7b901b…`, `extractor.py` `1bb49811…`; S119 tarball pin `531717a0…`; S130 tag commit
  `1fcc7a0a…`; provenance digests verified against retained files as in C6.
- PROVINCE round-43 note's matrix facts reproduce from the retained API capture
  (`rel-r43.json`): 8 releases, six assets each except `sasquatch-v1.0` with 2 (both amd64),
  architecture matrix starting at `sasquatch-v1.0.1`; no `*.deb` under `corpus/evidence/round-43` or
  `.ufo/waves/round-43` (0 files), so "no sasquatch release asset was downloaded" is consistent with
  lane bytes (negative evidence only).

## Out of scope / not claimed

- No REA, unblob, sasquatch, extractor or archive tool was run; no published firmware byte was opened;
  no network fetch. All checks read committed bytes or the frozen tools.
- No lane write, commit, VCS mutation, fleet write, PATH write, pacman call, subagent or background
  job. Disk guard green before and after (`/fast` 565 GiB free, `/home` 590 GiB free at measurement).
- No install or upgrade was performed by this seat (per `/home/vgpnk/.omp/agent/RULES.md`, no install
  was needed; nothing to record).
- Peer wave-2 reports were not reviewed (this seat audits the round report, not the 32 seats).
- The C2 score tool itself was not re-run: its upstream inputs and child-receipt directory are absent
  (C7). Its numstat check, gate, map bindings and count were verified from source + committed bytes,
  and its gate was re-run independently in a clean clone.
- `S135`/`S136`/`S137` were not re-fetched; their mutable-page digests are untestable from lane bytes.

## Limitations

- All measurements are at the working-tree state above; if the L1 edits `SCORECARD.md`/`SHONEN.md`
  (e.g. adds the missing coverage-map row or the LOG entry), C1/C2/C3 must be re-measured.
- The C1 "observed == declared" arm is re-derived by the frozen counter's own extraction, not by an
  independent extractor this seat ran; the tuple check is generator-self-reported plus
  counter-cross-checked, as the plan discloses.
- The copy-audit's three upstream-dependent checks could not be reproduced; the 136/0 claim rests on
  the committed wrapper receipt's embedded stdout for those three.
- [INFERENCE] tags appear only where noted (C4 cache-fill timing; C6 "not the same fetches" is a
  comparison of recorded instants/digests, not a claim about which process fetched what; C8
  interpretation of the plan sentence).
- `considerthese/` absence, `prefile-gate.json` absence and wave-2 pending settlement are stated as
  observed states, not as defects of the report text.

## Evidence inventory

- `artifacts/R43W2Closure/c1-rescore-at-77d196c6.json` `4e4c542f…` — independent counter re-run
  (identical to committed receipt except argv/regen_argv).
- `artifacts/R43W2Closure/c1-rescore.log` `1565eef4…` — counters stdout, exit 0.
- `artifacts/R43W2Closure/gate.json` `2b69a626…` / `gate.err` (empty, `e3b0c442…`) — clean-clone gate,
  exit 0.
- `artifacts/R43W2Closure/copyaudit-noupstream.tsv` `211f60b9…` — 136 checks, 3 upstream-dependent
  failures, exit 1.
- `artifacts/R43W2Closure/selftest-tuple.txt` `6ffd5520…` — 17/17, exit 0.
- `artifacts/R43W2Closure/command-A.txt` `fac178a0…` — command A at HEAD, freeze, base.

Scratch `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2Closure` removed after the artifacts above were
copied into the lane.

Report: .ufo/waves/round-43/w2/R43W2Closure.md
