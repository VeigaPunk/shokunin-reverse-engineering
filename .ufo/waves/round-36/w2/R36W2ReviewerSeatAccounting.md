# R36W2ReviewerSeatAccounting — wave-1 seat accounting

**Seat:** R36W2ReviewerSeatAccounting (wave 2, leaf; advisory only). **Audit instant:** 2026-10-26T02:04–02:10-03:00.
**Target:** `w1-spec.json` items (43) × `.ufo/waves/round-36/w1/*.md` × `w1/swarm-registry.json` × `w1-results.json`.

## Verdict

| state | count | basis |
|---|---|---|
| spec items | 43 | `jq -r '.items[].name' w1-spec.json \| wc -l` → 43 |
| **settled** | **43** | non-zero report at the canonical path, unique content, exactly one commit, parseable result entry, no error envelope, agent == spec role |
| **reported** | **0** | no seat has a report without a usable result entry |
| **dead** | **0** | no result entry without a report, no error/empty output |
| **missing** | **0** | every spec name has both artifacts |
| outstanding | 0 | same |

The L1's count **43/43 holds name-for-name**. It is **not calibratable as a *settlement record***: no committed artifact carries a per-seat status or a settlement timestamp, and `swarm-registry.json` was frozen at dispatch time (F1, F2). Classification rule used (stated so it can be attacked): a seat is *settled* when its spec name has (a) a non-zero report at `w1/<name>.md`, (b) a result entry under the same name whose `output` parses as a JSON object with no `error` key, and (c) `agent` equal to the spec `role`. *reported* = (a) without (b); *dead* = (b) without (a) or an error output; *missing* = neither. Reportless "died and respawned under the same name" is invisible to these artifacts (see Limits).

## Name-set identity (all four surfaces)

```
$ cd .ufo/waves/round-36
$ jq -r '.items[].name' w1-spec.json | sort > spec;  jq -r '.results[].name' w1-results.json | sort > results
$ jq -r '.members|keys[]' w1/swarm-registry.json | sort > registry;  ls w1/*.md | sed 's#w1/##;s#\.md$##' | sort > files
spec=43 results=43 registry=43 files=43
== dup spec == (none)   spec==files   spec==results   spec==registry     # all three diffs empty
```

`ls w1/` = 44 entries: 43 `.md` + `swarm-registry.json`; 0 directories. No extra report, no seat without a report.
Report set: 43 files, total 737,629 B, min 4,545 B, max 34,735 B, **0 zero-byte**; 43 distinct sha256 (no duplicated report); set-manifest sha256 over sorted `basename sha256` = `6ddfec14b3d4a9f39e181ac710f795eaad765c26f7e60852088cc6061dfea065`. Every report contains its own seat name (`grep -q "$name"` → 0 misses).

## Per-seat accounting

`result pointer` is what the seat's own `output` object declares: `lane-rel` resolves from the lane root, `abs` is absolute, `fleet-rel` = `kaidoku-shokunin/...` (resolves only from `/home/vgpnk/Projects/shokunin`, **not** the lane root), `none` = no report/artifact/report_path key.

| # | seat | bytes | sha256[:12] | mtime (-03) | result pointer | state |
|---|------|-------|-------------|-------------|----------------|-------|
| 1 | R36ScoutSasquatchRelease | 5600 | 1018fb8db740 | 01:27:49 | lane-rel | settled |
| 2 | R36ScoutUnblobHandler | 8267 | fec230b70a93 | 01:28:36 | lane-rel | settled |
| 3 | R36ScoutNeovimRelease | 6434 | 24053768b49d | 01:28:27 | lane-rel | settled |
| 4 | R36ScoutAppImageSpec | 13335 | 64e16297ce6e | 01:29:27 | lane-rel | settled |
| 5 | R36ScoutUnblobReadme | 14142 | ab9c4916cab6 | 01:29:53 | lane-rel | settled |
| 6 | R36ScoutPrebuiltInventory | 4545 | 2f152c5fb70c | 01:29:04 | lane-rel | settled |
| 7 | R36ScoutQuarantine | 11955 | 9beb208960bd | 01:32:41 | fleet-rel | settled |
| 8 | R36ConnSiblingOverlap | 14265 | f6bef67a34cc | 01:35:40 | abs | settled |
| 9 | R36ConnAssimilationTheme | 18966 | fdb3f7a750da | 01:38:13 | lane-rel | settled |
| 10 | R36ConnSeparability | 19014 | 9bebb260d202 | 01:42:15 | abs | settled |
| 11 | R36ExecReproK1 | 14206 | bf849b18944e | 01:34:44 | none | settled |
| 12 | R36ExecReproK2 | 15371 | 7e55064bfc79 | 01:33:34 | lane-rel | settled |
| 13 | R36ExecReproK3 | 14729 | 38e6194e5754 | 01:33:33 | lane-rel | settled |
| 14 | R36ExecReproK4 | 20528 | cc74aeec31e8 | 01:37:28 | none | settled |
| 15 | R36ExecRecountC1 | 16054 | d20c89879099 | 01:35:16 | lane-rel | settled |
| 16 | R36ExecRecountC2 | 14108 | c49263a4f76a | 01:34:02 | none | settled |
| 17 | R36ExecIndependentC1 | 27964 | 850ce9c42230 | 01:37:50 | none | settled |
| 18 | R36ExecEvidenceIds | 16843 | 8d8d8e46d743 | 01:35:00 | lane-rel | settled |
| 19 | R36ExecSasquatchDirect | 11070 | e767355cf986 | 01:35:17 | none | settled |
| 20 | R36ExecSourceTreeOracle | 13027 | 6e1036d239fa | 01:34:11 | lane-rel | settled |
| 21 | R36ExecAppImageExtract | 10864 | 2f3982e81414 | 01:33:55 | lane-rel | settled |
| 22 | R36ExecHarnessRun | 17831 | a3538db4faa5 | 01:36:59 | none | settled |
| 23 | R36ScribeEntry | 31663 | 69069fbb8e34 | 01:38:13 | none | settled |
| 24 | R36ScribeProvince | 17252 | 71baeda0655d | 01:37:03 | lane-rel | settled |
| 25 | R36ScribeReadme | 12287 | 1062664c9fa6 | 01:36:23 | lane-rel | settled |
| 26 | R36ScribeSkill | 24388 | 94f5a822f563 | 01:37:25 | none | settled |
| 27 | R36ScribeSources | 16659 | 95c7e94ace26 | 01:39:01 | fleet-rel | settled |
| 28 | R36ScribeLessonMistakes | 17178 | 770ba55a4463 | 01:37:46 | none | settled |
| 29 | R36ScribeRoutedDefects | 29658 | 30dee5cfddaf | 01:40:23 | abs | settled |
| 30 | R36ScribeAssimilationGate | 28930 | aa32ddb977e0 | 01:41:15 | abs | settled |
| 31 | R36CriticC1Shortcut | 21070 | 93ac2644bb50 | 01:43:24 | lane-rel | settled |
| 32 | R36CriticC2Shortcut | 14479 | 50127130e9e9 | 01:40:44 | lane-rel | settled |
| 33 | R36CriticPredicateIdentity | 34735 | 841d130dd7c6 | 01:46:14 | lane-rel | settled |
| 34 | R36MutantC1 | 9301 | 88f0c4841d41 | 01:45:50 | none | settled |
| 35 | R36MutantC2 | 11293 | 45b91abc3a7c | 01:43:27 | lane-rel | settled |
| 36 | R36ReviewerReceipts | 13142 | ba7cc5a7357e | 01:42:14 | lane-rel | settled |
| 37 | R36ReviewerControls | 13100 | 196f885b824e | 01:48:17 | lane-rel | settled |
| 38 | R36ReviewerHarnessCode | 12838 | 62e236b6f723 | 01:50:33 | lane-rel | settled |
| 39 | R36ReviewerAdjacency | 9272 | bfde24eb9b58 | 01:41:25 | lane-rel | settled |
| 40 | R36SentinelInstall | 31900 | ea5f3e0503d9 | 01:48:26 | lane-rel | settled |
| 41 | R36RevengerOracle | 29303 | a58968d5c326 | 01:47:45 | lane-rel | settled |
| 42 | R36ReviewerQualityBar | 28066 | 16f47b48e058 | 02:00:23 | lane-rel | settled |
| 43 | R36CriticRoutedCoverage | 21997 | 9774af5acce1 | 01:43:00 | lane-rel | settled |

Pointer tally: 27 lane-rel (25 `report`, 2 `report_path`), 4 abs (1 `report`, 1 `report_path`, 2 `artifact`), 2 fleet-rel, 10 none. All 43 canonical files exist regardless of pointer class.

## Artifact binding

```
$ sha256sum .ufo/waves/round-36/w1-spec.json .ufo/waves/round-36/w1-dispatch.json
6067a4ab6983f19a8c5f7f126411899e8ad5594edc331639fe5b2af758496e31  w1-spec.json
7a68f12abfe13ad3df0a4e3343eb89bf438d37c91b8fa9dac0623a21254bbe91  w1-dispatch.json
$ git show HEAD:.ufo/waves/round-36/w1-results.json | sha256sum   # d175e4e4…fd4ae0, identical to worktree
$ git show HEAD:.ufo/waves/round-36/w1/swarm-registry.json | sha256sum # 2d3e932e…bd682, identical to worktree
$ git ls-tree -r HEAD -- .ufo/waves/round-36/w1 | wc -l            # 44 (43 md + registry)
$ git status --porcelain -- .ufo/waves/round-36                     # only ?? w2/ and ?? w2.ready.dispatched
```

`w1-results.json` (sha256 `d175e4e414d918460b66ffb5c9038d44a4272af8217a5ea5dfcdaf0378fd4ae0`, mtime 02:01:06, committed `6f2ba761`): top-level keys `lane,round,wave,seats,results`; `seats` = 43 (number); 43 entries; entry keys `name,agent,output,note`; `note` null ×43; all 43 `output`s parse; 43 distinct output hashes; result order == spec order; `agent` == spec `role` for 43/43 and registry `role` == spec `role` for 43/43; no `error` key in any output.

## Findings

**F1 — the results manifest records no seat status and no timestamp (calibration, high).**
`w1-results.json` contains 0 occurrences each of `"status"`, `"settled"`, `"dead"`, `"missing"`, `"timestamp"`, `"utc"` (`grep -c` over the 218,650-byte file). Every `note` is `null`. The only count is `seats: 43`, which is the dispatch count, not a settled count. Therefore "43/43 settled" is derivable from file presence but **is not recorded**, and no per-seat settlement instant is committed (git stores no mtimes). Committable granularity is two commits: 42 report files in `01a44dbf` (2026-10-26T01:50:56-03:00), 1 in `6f2ba761` (02:01:31). QUALITY.md:128 requires "seat totals, settled seats and outstanding seats **with timestamps**".

**F2 — `swarm-registry.json` is a dispatch-time skeleton and cannot support settlement (calibration, high).**
```
createdAt 2026-10-26T04:26:30.277Z   updatedAt 2026-10-26T04:26:38.959Z   schema ufo-swarm-registry-v1
members 43: kind=spawn ×43, axes=coverage+calibration ×43, agentId=null ×43, item=null ×43; no status field
$ stat -c %y w1-dispatch.json   # 01:26:38.960532626 -0300   == updatedAt 04:26:38.959Z
$ git log -1 --format='%h %ci' -- w1/swarm-registry.json   # 01a44dbf 2026-10-26 01:50:56 -0300
```
The registry's last write is the instant the dispatch manifest was generated (8.4 s after `createdAt`); it was committed 24 minutes later with `updatedAt` unchanged, while **all 43 reports have mtimes after `updatedAt`** (earliest 01:27:49). It contains no agent id, no status, no timestamp per member — so it cannot distinguish dispatched from returned, and a reader must not cite it as settlement evidence.

**F3 — result outputs do not bind one report-path convention (medium; QUALITY 73/78 surface).**
10/43 outputs carry no report pointer at all (R36ExecReproK1, R36ExecReproK4, R36ExecRecountC2, R36ExecIndependentC1, R36ExecSasquatchDirect, R36ExecHarnessRun, R36ScribeEntry, R36ScribeSkill, R36ScribeLessonMistakes, R36MutantC1). 2/43 emit a path relative to the **fleet repo root**, which does not resolve from the lane root the seat bounds name:
`R36ScoutQuarantine` → `kaidoku-shokunin/.ufo/waves/round-36/w1/R36ScoutQuarantine.md`;
`R36ScribeSources` → `kaidoku-shokunin/.ufo/waves/round-36/w1/R36ScribeSources.md` (under `artifact`).
4 use absolute paths and 2 use an `artifact` key instead of `report`. The files themselves are present at the canonical paths, so this is a manifest-binding defect, not a missing seat.

**F4 — the "dispatched" marker postdates 12 reports (medium).**
`w1.ready.dispatched` content `2026-10-26T01:34:34`, file mtime 01:34:34.044. Twelve reports have earlier mtimes: R36ScoutSasquatchRelease 01:27:49, R36ScoutNeovimRelease 01:28:27, R36ScoutUnblobHandler 01:28:36, R36ScoutPrebuiltInventory 01:29:04, R36ScoutAppImageSpec 01:29:27, R36ScoutUnblobReadme 01:29:53, R36ScoutQuarantine 01:32:41, R36ExecReproK3 01:33:33, R36ExecReproK2 01:33:34, R36ExecAppImageExtract 01:33:55, R36ExecRecountC2 01:34:02, R36ExecSourceTreeOracle 01:34:11. The marker is therefore not the dispatch instant (dispatch manifest mtime is 01:26:38.960); citing it as start time would make 12 seats report before dispatch. [INFERENCE] it was written on acknowledgement, not at spawn.

**F5 — "43/43" exists only at HEAD, not at the named integration tip (calibration, medium).**
At `01a44dbf` (the assignment's integration tip, 01:50:56): 42/43 reports and **no** `w1-results.json` (`git cat-file -e 01a44dbf:.ufo/waves/round-36/w1-results.json` → `fatal: … exists on disk, but not in '01a44dbf'`). The 43rd report (R36ReviewerQualityBar, 02:00:23) and the results file arrive in `6f2ba761` (02:01:31), whose message is `round-36: wave-1 results (43/43 settled) and last report; wave-2 spec/dispatch`. The claim is true at HEAD and false at the cited tip.

**F6 — QUALITY "76" is not a numbered row (low; citation surface).**
`grep -n '^| 76 |' corpus/QUALITY.md` → no match. Row ids present: 1–74, 77, 78. Rule 76's text exists only as the changelog bullet at `corpus/QUALITY.md:128` ("Row 76 added after the round (seat accounting)…"). The rule is evaluable from that bullet, but "per QUALITY 76" points at a number with no row.

**F7 — no settle artifact exists for round 36 (medium; regression against prior rounds).**
`ls .ufo/waves/round-36 | grep -i settle` → none. Round 30/31 carry `settle.tsv` with statuses `returned/dead/cancelled` (round-30: 68 returned, 3 dead, 2 cancelled); round 35's routed defect R35-D2 required `w1-settle.json`/`w2-settle.json`. Round 36 has neither, so settled/dead cannot be stated from a status record at all.

## Observations (advisory, no defect claimed)

- **O1** — Wave-2 was authored before wave 1 finished: `w2-spec.json`/`w2-dispatch.json` 01:53:15, `w2.ready` 01:56:32, while the last wave-1 report landed 02:00:23 and `w1-results.json` at 02:01:06. Only 1 of 43 reports (R36ReviewerQualityBar) postdates the w2 spec. *Dispatch* order is clean: `w2.ready.dispatched` = 02:03:47, after the results commit 02:01:31. [INFERENCE] a w2 seat reading only its frozen context would miss that report; seats read the tree, so impact is unmeasured.
- **O2** — Dispatch-prompt clause of QUALITY.md:128 holds. 43 tasks; common prefix across all 43 prompts = `/skill:godspeed\n\n`; every prompt's last non-empty line is `Report: write your scoped findings to .ufo/waves/round-36/w1/<name>.md` (0 trailer violations); `w1-dispatch.json` counts `{spawn:43,resume:0,total:43}`; task names == spec names.
- **O3** — Result envelopes are heterogeneous (`report`/`report_path`/`artifact`/none; only 3/43 carry `summary`), so no mechanical settled/dead audit exists; this seat had to classify by file presence.

## Limits

- All mtimes are filesystem observations taken at the audit instant; git does not commit them. The only committable settlement times are the two commit timestamps (F1/F5).
- "0 dead" is inferred from complete artifacts. Nothing records a seat that died and was respawned under the same name (registry `agentId` null ×43), nor a seat whose final yield was an incremental section rather than a terminal result.
- No round-level record exists to test QUALITY.md:128's "round's record" clause: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/` has no `kaidoku.md` (only other lanes), and lane `corpus/lessons/round-36.md` / `SCORECARD.md` contain no seat-total line (`grep -rn '43/43|43 seats|spawned='` → no match). Filing is outside this wave.
- Report bodies were not read for semantic content; coverage here is name/artifact coverage. Whether each seat's evidence is sound is other wave-2 seats' assignment.
- Read-only git only; no VCS mutation. No tools installed in this seat (no pacman/uv/npx). Scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerSeatAccounting` created, used only for name lists, removed before filing.

## Commands exercised (selected, exact)

```
jq -r '.items[].name' w1-spec.json | wc -l                          # 43
jq -r '.items[] | .role' w1-spec.json | sort | uniq -c              # 3 connector, 4 critic, 12 executor, 2 mutation-tester,
                                                                    # 1 revenger, 5 reviewer, 7 scout, 8 scribe, 1 sentinel
ls w1/ | wc -l                                                      # 44 (43 .md + swarm-registry.json)
python3: for each results entry json.loads(output) → 43/43 parse; 43 distinct sha256
git log --oneline -- .ufo/waves/round-36/w1/<each>.md | wc -l       # 1 for all 43 (no post-filing edit)
git show --name-only --format='' 01a44dbf -- '.ufo/waves/round-36/w1/*.md' | grep -c '\.md$'   # 42
git show --name-only --format='' 6f2ba761 -- '.ufo/waves/round-36/w1/*.md'                     # R36ReviewerQualityBar.md
git rev-parse HEAD                                                  # 6f2ba761bb5bcd6482d45523379376dcb6a386f6
```

**Report: .ufo/waves/round-36/w2/R36W2ReviewerSeatAccounting.md**
