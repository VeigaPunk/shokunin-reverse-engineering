# kaidoku round 31: verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Session `HyakuCloseKaidoku31A2`, 2026-10-23, about 05:27Z to 05:50Z. Range `c369242fee9f559f895e3f7956b1242076c7b1be..f2f5977b8266d8233927fe1f1a77507df59c26fa`. Report `.ufo/reports/round-31/kaidoku.md` (fleet `dcd6c5968be199a7d2e6c2f68a97d1af71c1e9f0`). An earlier closure session (`HyakuCloseKaidoku31`) died with the orchestrator process at 05:25:25Z and landed nothing; none of its partial work is used here. This session dispatched six read-only seats: `ReMeasureC1`, `ReMeasureC2`, `GateEvidence` and `SpotSources` (reviewers), `AxisFitC1` (critic) and `Containment` (scout). All six returned. No seat executed a lane counter, gate, selftest or REA, and no seat wrote outside `/tmp`. Nothing was installed or updated. Item hold `U064N008Hf47eb933` was not touched.

Driver digest (copied from `.ufo/watchdog.log`):

```
2026-10-23T00:52:34-03:00 launch kaidoku round=31 pgid=970932 driver=hyaku-inline attempt=1
2026-10-23T01:45:55-03:00 complete kaidoku round=31; hyaku-inline attempt=1
```

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane | `git log --format='%an %ae %H %cI' -- .ufo/reports/round-31/kaidoku.md` (fleet) | `kaidoku-shokunin kaidoku@shokunin.local dcd6c5968be199a7d2e6c2f68a97d1af71c1e9f0 2026-10-23T01:45:09-03:00` | pass |
| SHONEN heading, one line per box | read of the report `## SHONEN` | 4 lines, all `[~]`, each with a pointer | pass |
| cited commits on the branch | `git rev-parse --verify <h>^{commit}` and `git merge-base --is-ancestor <h> main` for `c369242f 35ba7c52 7474d269 f368a101 0007731e 1288285e 16c00c2d f2f5977b` | all 8 resolve and are ancestors; the 7 round commits are all authored `kaidoku-shokunin` | pass |
| pushed | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=main local=f2f5977b… remote=f2f5977b… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| leftovers | `git status --porcelain \| wc -l` | 0 (`tools/round-31/__pycache__` is ignored by `.gitignore:1`) | pass |
| prompt carries the template contract | `grep -nE '^## ' .ufo/prompts/kaidoku-round-31.md`; `git log -- <prompt>` | §1 MISSION/AXES, §2 Claims, §2b Frontier, §3 L2 floor, §4 Report contract, §5 Commit/push/L0, §6 hyaku addendum; committed by the lane at fleet `dddfae2` (00:52:33-03, one second before launch) | pass |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` (05:29Z) | `kaidoku ok`, eight W04 (S033, S047, S054, S062, S069, S083, S090, S092), exit 0 | pass, equal to the report (S092 is the expected new W04: same 6.5.0 tarball URL as S083/S090, different scope) |

Conformance defects (status-neutral):
- The report says "One w2 seat ran `git commit` in the fleet repo". The seat is w1 `CriticSeparability` (lesson M31-7; `settle.tsv:26` `w1 CriticSeparability returned 2026-10-23T04:43:23Z`; its report §4.6). Wrong wave label in the report.
- Lesson `:21` still says "trivial predictors score at most 3 of 23". The refusals entry `:71` corrects it to 7 of 23, but the lesson line stands uncorrected (§Evidence standard, "Corrections sweep every mention").
- `SKILL.md:1038` still says the 6.7.0 budget drift is a "static reading, not run". The live 6.7.0 probe is committed (`w2/ProbePin670.md`) and the refusals entry `:74` records it as observed. The SKILL sentence is stale about its own evidence; its conclusion is correct.
- No committed cited-runs-gate run over the round-31 report itself (the tip receipts, 04:44:14Z, precede filing). M31-4 says the report "is run through it before filing". Every gate statement in the report is individually backed by a committed receipt (table below), so this is a process claim without a receipt, not an unbacked result.

## Containment

- `CriticSeparability` ran `git -c user.name=ctl -c user.email=ctl@local commit -q …` with cwd `/home/vgpnk/Projects/shokunin`. Output `no changes added to commit`, exit 1. HEAD before and after was `f0dadee386559ce4a80b9655c9a088c375f4b510` (a protocol closure commit of 04:13:35Z).
- No commit landed: `git log --all --since=2026-10-23T03:50Z --until=2026-10-23T04:55Z` in the fleet repo lists 127 commits, 0 by `ctl`, 0 by any identity outside `*@shokunin.local`. The four kaidoku-subject commits are lane or protocol commits (`dddfae2`, `dcd6c59`, `656e0c0`, `e716029`). `git diff --cached --name-only` is empty; no untracked path names kaidoku or round 31.
- The wave context forbade it: `w1-payload.json` and `w2-payload.json` both say "Seats never run git or jj writes in the lane or the fleet repo: no git add/commit/…". No tool enforced it. The only effect was a `.git/index` stat refresh, which is no longer observable.
- Dead seats: w2 `ReviewProvinceSkill` and `ReviewCensus`, error text `[inception/mercury-3] 429 Rate limit reached: output token limit exceeded`, recorded at `settle.tsv:67` and `:80`; neither has a committed report and neither was resent. Cancelled at budget: `ReviewEntryC1`, `ReviewQualityLesson`, `CriticHarm` (`settle.tsv:65,68,71`, "partial report not integrated"); none has a committed report.

## Freeze and receipts

GateEvidence re-checked these read-only with its own `sha256`/`git` commands:
- **Order.** Freeze `35ba7c52` 04:05:07Z, controls `7474d269` 04:18:47Z, data `f368a101` 04:19:35Z. `runs.tsv` puts all 35 live REA runs between 04:18:57Z and 04:19:27Z: after the control commit, before the data commit. `git log --name-status 35ba7c52..f2f5977b -- corpus/evidence/round-31` shows only `f368a101`, 72 files, all `A`. The lesson's "04:18:49Z" for the controls commit is 2 s off the committer time (order unaffected).
- **Pins.** The 5 pinned committed paths (oracle, both counters, `carriers.tsv`, `predictions.tsv`) hash to their `claims.json` pins at `35ba7c52` and at `f2f5977b`. `claims.json` is byte-identical from freeze to tip (`6b090a33…`). `git log 35ba7c52..f2f5977b -- <those 6 paths>` is empty.
- **Receipts.** Every gate statement in the report has a committed receipt:

| report statement | committed receipt, final line |
|---|---|
| C1/C2 exit 2 at base | `before/c1-…-at-c369242f.txt` "PIN pinned input absent … exit=2"; `before/c2-…` "PIN predictions absent … exit=2" |
| selftests | `before/`: C1 `cases=14 failures=0 exit=0`; C2 `cases=12 failures=0 exit=0` |
| C1 12/12 at `0007731e` and `16c00c2d` | `carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)`, `exit=0` |
| C2 23/23 at `0007731e` and `16c00c2d` | `requests=23 matches=23 target=23 entry_ok=1 (ok) skill_ok=1 (ok)`, `exit=0` |
| intermediate at `f368a101` (kept) | C1 `pass=0 … exit=1`; C2 `matches=0 … exit=1` (entries not yet written) |
| freeze-integrity CLEAN | `freeze-integrity: CLEAN pins=5 … rev=16c00c2d…`, `exit=0` |
| settle PASS | `after/settle-gate.txt` `settle: PASS … rows=82`, `exit=0` |
| cited-runs gate on the round-30 report | `FAIL findings=8 … UNBACKED 16 … UNCITED 66/67`, `exit=1`; selftest `17/17` after the fix, `16/17` before |
| controls met no target | `controls/receipts.tsv` 10 rows, all `counter_exit=1 met_target=no`; `receipts-detail.tsv` copied-predictions `matches=0`, placement `pass=12 province_ok=0`, shortcut `matches=1` |

- `git diff --name-status 16c00c2d f2f5977b` lists 4 receipts, `corpus/SOURCES.md` and the lesson. Neither counter reads those two files, so the `16c00c2d` measurements stand for the tip.
- Registry rows for the two counters, `freeze-integrity` and `cited-runs-gate` are at `SKILL.md:1044-1048`, with verdict maps and selftest case counts equal to the committed selftests (14, 12, 17).

## Per-claim re-check

Both counters are lane-owned gates (PROTOCOL §Gate standard), so this session did not execute them. It verified their committed evidence (above) and re-measured the counted quantities from committed bytes and the pinned on-disk carriers, with independent code.

### R31-C1 (coverage): re-measured, verifies, narrow fit

- Carriers: all 12 files in `/fast/scratch/hyaku/kaidoku-r31/carriers/` hash to their `carriers.tsv` pins (`sha256sum`) and carry `lsattr` `i`. `carriers.tsv` hashes to its frozen pin `46f180b8…`.
- Independent schema read (ReMeasureC1, `/tmp/hyaku-r31-close/ReMeasureC1/my_oracle.py`: stdlib `sqlite3` on `file:…?mode=ro&immutable=1`, `PRAGMA table_list`/`table_xinfo` and `sqlite_schema`; no lane code). For every carrier it compared the committed envelope's names, sql, root pages, kinds (table, virtual, shadow), `without_rowid`, `strict`, column counts and every column field. Result: 12/12 equal, 0 field mismatches; subject sha256 equals the pin 12/12.
- REA does not expand virtual-table columns (`rtree_curve_geometry`: `column_count:5`, `columns_completeness:"unsupported"`, `columns:[]`). The lane oracle normalizes virtual tables the same way (`sqlite_oracle.py:184-198`), and the lane discloses it. This is a frozen design choice, not a hidden miss.
- Provenance: each of the 12 envelopes has exactly one commit, `f368a101` (`git log --format=%h -- <path>`).
- Unmoved at base: `git show c369242f:PROVINCE.md | grep -c -E 'inspect[_-]sqlite[_-]database'` gives 0; it is 2 at the tip. The row is at `PROVINCE.md:349`, under `### Round-31 additions to Core (verified 2026-10-23)` (`:343`).
- The entry `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` cites S096 and names all 12 evidence ids. It says the lane "already held one path-only run of this operation: `…l7-04-inspect-sqlite-database.md`" and that it "extends, does not replace" l7-04.
- **The false premise.** The frozen R31-C1 surface says "a verb the lane has never run or named: at the base PROVINCE.md, SKILL.md and corpus/knowledge name inspect-sqlite-database 0 times". That is false twice:
  - Run: `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` (added `1cfd2a30`, 2026-10-16) records one live 6.5.0 run on a pnpm `index.db` copy.
  - Named: `git grep -c -E 'inspect[_-]sqlite[_-]database' c369242f -- corpus/knowledge` gives l7-04 3 and l8-01 1. The l7-04 filename contains the hyphen spelling. `corpus/README.md:65,163` name it at the base (AxisFitC1 F6).
  - Only the hyphen-spelling content grep over the three paths gives 0: `git grep -c inspect-sqlite-database c369242f -- PROVINCE.md SKILL.md corpus/knowledge` exits 1.
- **Ruling: the false premise does not sink the claim.**
  - The predicate, counter, target and both doc gates contain no novelty clause. The before→after the claim is measured by (counter exit 2 → 12/12; PROVINCE 0 → a Core row) is true under every spelling: base PROVINCE.md and SKILL.md name no SQLite surface at all (`grep -c -i -E 'sqlite|database'` gives 0 in both).
  - The falsehood is motivation prose. The lane's pre-data critics caught it before any data (M31-1). It is corrected in the C1 entry `:9`, `SCORECARD.md:3254`, `LOG.md:3032` and lesson `:16,47`, and mined into QUALITY row 56. The only uncorrected literal copy is the frozen `claims.json`, which the freeze rule keeps unchanged.
- **Axis ruling: narrow fit.** AXES.md defines coverage as the fraction of real surfaces the skill governs, which PROVINCE lists. At the base the SQLite reader was not a governed surface: PROVINCE named it 0 times, and the knowledge held one inventory-scope run whose own limits say "column details not requested" and "one carrier does not establish general behavior" (l7-04 `:11-13`). The claim moves the operation into PROVINCE Core with the database-scope reading verified on 12 files from 3 producers, including R*Tree virtual and shadow tables. This is the same move round 30's R30-C1 made (a held verb at narrower scope; a new positive class into Core from 0), which closure ruled fit. It is narrower here because the verb itself was not new. Both lane critics ruled narrow fit before and after the data (`w1/CriticAxisFitC1.md`, `w2/CriticAxisC1After.md`); this session agrees.
- Discrimination: the pre-data controls (do-nothing, junk-row, all-false, no-reader, id-rotated) scored 0 of 12. The Core-placement shortcut with real envelopes failed `province_ok`.
- Verdict: **verifies** (coverage `improved`, narrowly).

### R31-C2 (depth): re-measured, verifies, fit

- Freeze: `predictions.tsv` is blob `be63c2d5`, first and only added at `35ba7c52`. Its sha256 `acac45e3…` equals the pin, and it is unchanged at the tip. It holds 23 rows (20 refusals, 3 acceptances; this session's `awk` count). Each request id has 2 committed files under `corpus/evidence/round-31/c2` (`git ls-tree`).
- Full-envelope comparison (ReMeasureC2, own Python): 23/23. Refusals match on `ok:false`, exit 1, `error.code` and the single `details.issues` entry `{path, reason, message}`. Acceptances match on `ok:true`, operation and subject sha.
- SKILL table (`SKILL.md`, "SQLite databases (`inspect-sqlite-database`) — round 31"): 23 rows (`grep -cE '^\| \`?[qm]-'` over `:1008-1040` gives 23). Code and message match the predictions and the observations, 23/23.
- Trivial predictors, recomputed: ceilings of 3, 5 and 7 of 23, so the best is 7/23. The row sets equal `w2/CriticAxisC2After.md` §4. The copied-predictions control scored 0/23 in `controls/receipts-detail.tsv`, committed at `7474d269`, before the data. In round 30 the same control scored 16/19, which is the M30-3 repair.
- Code anchors: 7 predicted messages appear verbatim in the cached REA 6.5.0 dist (its `package.json` sha equals the pin), plus the errcode mapping behind "file is not a database".
- The 6.7.0 drift is recorded as a live observation with a committed receipt (`w2/ProbePin670.md`; entry `:74`).
- **Axis ruling: fit.** Exact codes, issue paths, reasons and messages were predicted from opened code (S092) before the data and observed live. The best trivial predictor reaches 7/23, and copied predictions score 0/23, so the bar can fail.
- Verdict: **verifies** (depth `improved`).

### Separability, lowest axis, harm

- **Separable.** Each claim has its own counter, frozen inputs and target. C1 is measured on the 12 published carriers. C2's mutants derive from the chinook carrier as a frozen input, not from a C1 result.
- **Lowest axis.** At the base coverage, depth and calibration are tied at 10, with none retired. `claims.json` `lowest_axis` states the tie before the data, as does the SCORECARD round-31 section. Both claims satisfy the rule (round-30 routed defect 5 closed).
- **Harm.** `git diff --numstat c369242f f2f5977b | awk '$2>0'` gives two lines:
  - `29 2 SCORECARD.md`: the coverage and depth owned-axes rows, refreshed to the `c369242f` recount (116/116, 17/17) with scores unchanged (`9.72 → 10.0`, `10 → 10`), plus the new round-31 section.
  - `2 2 tools/round-29/c1-fresh-naming.py`: the docstring-only fix routed as round-30 defect 8, with an `instrument_supersessions` entry.
  - The rest of the 215-file diff only adds lines. No owned axis is harmed.

| axis | verdict | reason |
|---|---|---|
| coverage | improved | C1: the SQLite reader enters PROVINCE Core from 0; 12/12 re-derived with an independent reader; controls 0/12; narrow fit, because l7-04 already held one inventory-scope run |
| depth | improved | C2: 23/23 full-envelope matches and 23/23 SKILL rows re-derived; code-predicted before the data; best trivial predictor 7/23; copied predictions 0/23 |
| calibration | unchanged | not claimed. The false novelty sentence was caught before the data and corrected in five places. Residuals (lesson `:21` 3/23, the `SKILL.md:1038` "not run", the w1/w2 label, QUALITY row 56 scope) keep it from moving; none is an uncorrected admitted claim |
| operability | unchanged | not claimed; two new gates with selftests and registry rows (hygiene) |
| freshness | unchanged | not claimed; the 6.7.0 drift probe is a disclosed observation, not a re-verification claim |
| adjacency | unchanged | not claimed; sibling scans found no conflicts (`w1/ConnSiblings.md`, `w2/ConnAfter.md`) |

Admission: both claims verify and no axis is harmed, so `admitted=true`. The false premise in R31-C1's frozen text is a disclosed calibration defect. It is not a falsified measurement.

## Discernment spot-check

SpotSources ran all re-opens at about 05:35Z on 2026-10-23, with `curl -sSL <url> | sha256sum`, `tar xzf`, `unzip` and `sed -n`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S092 rea-agents 6.5.0 tarball (`dist/sqlite`) | admit | `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`; `package/dist/sqlite/SqliteDatabaseLimits.js:4` | agree | sha256 `531717a0…e699` equals the Gate. `:4` reads `inputBytes: 256 * 1024 * 1024,` verbatim (≤25 words) |
| S094 Chinook v1.4.5 release | admit | GitHub release API JSON plus both `.sqlite` assets | agree | The assets hash to `bdf635be…` and `ca157cb5…` (1,067,008 B each), equal to `carriers.tsv`. The API JSON hash has drifted (`d17129c4…` vs Gate `d88ffdc5…`; only `download_count` differs), as the lesson discloses. `:367` `"name": "Chinook_Sqlite.sqlite",` is verbatim |
| S096 SQLite file format | admit | `https://www.sqlite.org/fileformat2.html` | agree | sha256 `905067af…97a2` equals the Gate. The `:328-330` quote matches under whitespace normalization (it is line-wrapped in the source), 19 words |
| S097 SQLite PRAGMA docs | admit | `https://www.sqlite.org/pragma.html` | agree | sha256 `af75d7d7…6034` equals the Gate. The `:2009-2010` quote matches under whitespace normalization, 18 words |
| REA `main`-branch SQLite guide | reject (no row) | `raw.githubusercontent.com/morluto/rea/main/docs/sqlite-databases.md` vs the `rea-agents-6.5.0` tag copy | agree | main (`44c798a5…`, 10,864 B) documents `resource_constraint` at `:137-139`. The 6.5.0 copy (`f7b0c57b…`, 8,128 B) has none (grep exit 1), and the frozen 6.5.0 predictions are `invalid_request`/`out_of_range`. main describes a later release |
| pyproj 3.7.2 | reject (no row) | PyPI manylinux x86_64 wheels of 3.7.1 and 3.7.2 (cp311, cp312); `pyproj/proj_dir/share/proj/proj.db` | agree | All four `proj.db` members hash to `a25d85a2…77109`, so they are byte-identical and a row would duplicate S093/proj-371 |
| refusals entry's nominal S096/S097 citation | reject (removed) | entry at the tip; `w2/ReopenS097.md` | agree | The tip refusals entry cites S092 only, and S096/S097 used-by is the positive entry only. The reasoning (the refusal behaviour is REA code, not the file-format spec) holds |

New `corpus/SOURCES.md` rows re-opened: S092, S094, S096 and S097. Each quote is at its stated location and within 25 words. S092's used-by change is logged old→new in the lesson Gate and equals the tip cell (SOURCES rule 2). `git diff c369242f f2f5977b -- corpus/SOURCES.md` has 6 `+|` lines and 0 `-|` lines, so no pre-existing row was changed.

## Trend verdicts

- **expansion: improved.**
  - REA's SQLite reader enters PROVINCE Core at scope `database`, re-derived 12/12 on 3 producer families.
  - SKILL gains a 23-row decision table.
  - Knowledge `.md` files went 116 → 118 (`git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'`), both new entries citing `mined` rows. SOURCES rows went 91 → 97 (`grep -cE '^\| S[0-9]{3,} \|'` at both revisions).
- **quality: improved.**
  - Both counters now compare the full committed envelope; the copied-predictions control went from 16/19 (round 30) to 0/23.
  - All 8 round-30 routed defects are closed against committed bytes (GateEvidence), and every gate result in the report has a receipt.
  - Wave-2 overstatements were corrected in the entries ("distinct branches", "the other 21 rows' code paths are unchanged", the 3/23 trivial ceiling).
  - Residuals: lesson `:21`, `SKILL.md:1038`.
- **discernment: improved.**
  - All 7 sampled gate decisions (4 admits, 3 rejects) agree on re-opening.
  - The pre-data critics caught the false novelty sentence before any data. It was mined into M31-1 and QUALITY row 56, with a red-before grep.
  - This session's axis rulings (C1 narrow fit, C2 fit) equal the lane's pre- and post-data rulings.
  - Row 56's scope is still too narrow (routed defect 1).

## Routed defects (lane must fix next round)

1. QUALITY row 56 and the C1 entry `:9` scope "every spelling" to file contents of PROVINCE/SKILL/`corpus/knowledge`. At the base `corpus/README.md:65,163` and the l7-04 filename also name `inspect-sqlite-database`, so the entry's "the zero count holds only for the hyphenated CLI spelling" is false for the corpus as a whole. Append a correction, and widen the novelty sweep to `corpus/README.md` and knowledge file names (`git ls-tree -r --name-only <REV> -- corpus/knowledge`).
2. Lesson `corpus/lessons/round-31.md:21` still says trivial predictors score "at most 3 of 23"; the entry corrects it to 7/23. Append a correction in the lesson.
3. `SKILL.md:1038` calls the 6.7.0 budget drift a "static reading, not run". The live probe is committed (`w2/ProbePin670.md`). Correct the sentence to cite the probe and its scope (only `m-over-256mib`, `m-wal-over` and `m-journal-hot` were run at 6.7.0).
4. The report puts the M31-7 `git commit` slip in w2; it was w1 `CriticSeparability`. Note the erratum in the next report. Also, no tool enforces "no git writes in the fleet repo" for seats; M31-7 stays "not shown able to fail".
5. M31-4 says the round-31 report "is run through" the cited-runs gate before filing, but no run over the report is committed. Commit that run as a receipt before filing.
6. M31-3 stays open: in `--write-evidence` mode both counters print the full target line with exit 0. A next counter should refuse to print the target line in write mode, and show that it fails on the do-nothing control.
7. Timing prose: the controls commit is 04:18:47Z (committer time), not 04:18:49Z, and the census-start receipt carries no timestamp for the stated 04:21Z run. Put timestamps inside receipts.

Operator note: all four SHONEN boxes are `[~]` with concrete pointers. This session independently checked the box-1 decision table (`SKILL.md` round-31 SQLite table, 23/23 against predictions and observations) and re-derived the 12 C1 envelopes with its own reader, so a non-author could reasonably check box 1. The executable-instructions box still rests on author-dispatched re-runs, and this session did not execute the counters. Promotion stays operator-owned.
