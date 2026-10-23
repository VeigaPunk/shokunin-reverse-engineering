# Round 31 — `inspect-sqlite-database`: database-scope schema on published files, and its refusal signatures predicted from code

Author: kaidoku L1, round 31, attempt 1 (in-session hyaku lane subagent). Lane-round base
`c369242fee9f559f895e3f7956b1242076c7b1be`. Instruments, carriers, predictions and both claims frozen at `35ba7c52`
(`.ufo/waves/round-31/claims.json`, 04:05Z) before any REA run on a carrier or request. Pre-data control wave `w1`
(44 seats) dispatched 04:09Z; control receipts committed at `7474d269` (04:18:49Z) before the data commit `f368a101`.

Anti-loop: round 30 worked REA's Rust reader; this round leaves it for a different frontier area, REA's SQLite reader,
and keeps round 30's admitted shape (an independent oracle for the positive class, code-predicted refusals).

## Claims

- R31-C1, coverage (surface: PROVINCE Core gains `inspect_sqlite_database`; at the base PROVINCE names it 0 times under
  either spelling). Counter `tools/round-31/c1-sqlite-positive.py`; target `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0.
  Entry `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` (S096, S097, S093, S094, S095).
  Pre-data axis ruling (wave-1 `CriticAxisFitC1.md`): **narrow fit** — the frozen sentence "a verb the lane has never run
  or named" is false (l7-04 holds one inventory-scope run); the Core row and the database-scope reading are new (M31-1).
- R31-C2, depth (surface: a SKILL.md decision table of 23 refusal/edge outcomes predicted from the 6.5.0 code). Counter
  `tools/round-31/c2-sqlite-refusals.py`; target `requests=23 matches=23 target=23 entry_ok=1 skill_ok=1`, exit 0.
  Entry `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` (S092). Pre-data axis ruling (`CriticAxisFitC2.md`): fit;
  trivial predictors score at most 3 of 23.
- Lowest axis: coverage, depth and calibration are tied at 10 at the base (`SCORECARD.md:21-25`), none retired
  (`SCORECARD.md:144-156`); on a tie every owned axis is a lowest axis, so both claims satisfy the rule (round-30 routed defect 5).

## Gate

New SOURCES rows (all opened 2026-10-23 by wave-1 scribes; the L1 re-read each report and copied the drafted row):

| row | URL | access | sha256 | located quote (≤25 words) | decision |
|---|---|---|---|---|---|
| S092 | https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz (scope `package/dist/sqlite/`, `dist/domain/sqlite/`, `dist/artifacts/readStableArtifact.js`) | 2026-10-23 | tarball `531717a0…e699`; nine modules byte-identical to the installed copy | `package/dist/sqlite/SqliteDatabaseLimits.js:4`: "inputBytes: 256 * 1024 * 1024," | admit, mined (`SrcReaSqlite.md`); W04 duplicate URL with S083/S090 expected (same tarball, different scope) |
| S093 | https://pypi.org/pypi/pyproj/3.7.1/json (and the 3.4.1, 3.5.0, 3.6.1, 3.7.0 records) | 2026-10-23 | 3.7.1 `2ad9561a…b1b7` (others in `SrcPypiPyproj.md`) | line 1: `pyproj-3.7.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | admit, mined |
| S094 | https://api.github.com/repos/lerocha/chinook-database/releases/tags/v1.4.5 (+ two `.sqlite` assets) | 2026-10-23 | API JSON `d88ffdc5…d6ad`; assets equal `carriers.tsv` | line 367: `"name": "Chinook_Sqlite.sqlite",` | admit, mined (`SrcChinook.md`; the API serves `digest: null`) |
| S095 | https://pypi.org/pypi/pyogrio/0.11.1/json (+ sdist) | 2026-10-23 | JSON `5b286ab2…7162`; sdist `e1441dc9…082c` | line 1: `"filename":"pyogrio-0.11.1.tar.gz"` | admit, mined (`SrcPyogrio.md`; five fixtures equal the carriers) |
| S096 | https://www.sqlite.org/fileformat2.html | 2026-10-23 | `905067af…97a2` | `:328-330`: "This byte sequence corresponds to the UTF-8 string \"SQLite format 3\" including the nul terminator character at the end." | admit, mined (`SrcSqliteFormat.md`) |
| S097 | https://www.sqlite.org/pragma.html | 2026-10-23 | `af75d7d7…6034` | `:2009-2010`: "This pragma returns information about the tables and views in the schema, one table per row of output." | admit, mined (`SrcSqlitePragma.md`) |

Rejected: a row for the REA `main`-branch SQLite guide (`CriticAxisFitC2.md` read it; it describes a later release, not
the 6.5.0 pin, so it cannot teach the pinned behaviour); a row for node:sqlite / libsqlite3 builds (host readers used as
oracle and probe, not learning sources); a separate row for pyproj 3.7.2 (its `proj.db` is byte-identical to 3.7.1's).
Row changes old→new: none to existing rows; S092–S097 new (status `mined`, used-by the two round-31 entries).

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail?) |
|---|---|---|---|---|
| M31-1 | A claim's novelty sentence rested on an unmoved grep keyed on one spelling: "a verb the lane has never run or named" counted only the CLI form `inspect-sqlite-database`, while the corpus held the tool form `inspect_sqlite_database` (l7-04, a live 6.5.0 run). | `.ufo/waves/round-31/w1/CriticAxisFitC1.md`, `CriticAxisFitC2.md`; `.ufo/waves/round-31/claims.json` (R31-C1 surface) | the pre-data axis-fit critics; QUALITY row 48 asks for an unmoved command but not for every spelling | QUALITY row 56. Shown able to fail: `git grep -c -E 'inspect[_-]sqlite[_-]database' c369242f -- corpus/knowledge PROVINCE.md SKILL.md` finds l7-04 (3) and l8-01 (1), exit 0, where the hyphen-only command found nothing (exit 1). The frozen claim text stays; this lesson, the entry and the SCORECARD section carry the correction. |
| M31-2 | Frozen inputs could be edited after the freeze without any tool noticing: the counters compare the tree with `--rev`, and `tools/round-30/prefreeze-gate.py` checks pins at the freeze commit only. | `.ufo/waves/round-31/w1/CtlC2RewritePred.md` (counter and prefreeze gate both passed an amended `predictions.tsv`); `CriticSeparability.md` (same for the oracle); `ReviewCounters.md` finding 1 | the pre-data control wave | `tools/round-31/freeze-integrity.py`, QUALITY row 55. Shown able to fail: `.ufo/waves/round-31/controls/freeze-integrity-ctl-rewritepred.txt` exit 1; CLEAN on the lane (`freeze-integrity-lane-at-35ba7c52.txt`, and at the measured tips in `after/`). |
| M31-3 | Both round-31 counters (and round 30's) print the full target line with exit 0 in `--write-evidence` mode, which skips the committed-record clause, so a write run reads like a passing receipt. | `.ufo/waves/round-31/w1/CtlC1JunkRow.md`, `CtlC1DoNothing.md`, `CtlC1AllFalse.md` (write mode on zero committed envelopes printed `pass=12 target=12`, exit 0) | the pre-data control wave; no lane rule | Registry rows (SKILL.md round-31 measurement registry) and both entries' recheck lines say a write run is never a receipt; the round's write runs are committed under `.ufo/waves/round-31/data/`, labelled as such, and every cited receipt is a no-flag run in `after/`. Not shown able to fail (the counters stay frozen); a next counter should run the committed clause in every mode. |
| M31-4 | The round-30 report cited gate PASS results with no committed receipt (settle PASS; prefile PASS while the only committed prefile run was red). | `corpus/lessons/round-30-verifier-spotcheck.md:27-28,144` | outside verifier (routed defect 1) | `tools/round-31/cited-runs-gate.py`, QUALITY row 52. Shown able to fail: `.ufo/waves/round-31/after/cited-runs-gate-round30-report.txt` exit 1 (`UNBACKED 16` settle, `UNCITED 66`, `UNCITED 67` prefile); the round-31 report is run through it before filing. |
| M31-5 | A hand-written annotation in a frozen file disagrees with the bytes: `m-wal-over` notes "WAL 267367449 bytes"; the file is 267,368,449. | `.ufo/waves/round-31/w1/ScoutPinDrift.md`, `RevPredTraceB.md` | wave-1 trace seats | Correction in `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` (frozen file unchanged). Not shown able to fail; annotations of sizes should be computed by the builder, not typed. |
| M31-6 | The wave-1 cited-runs gate's selftest passed in the seat's scratch dir and failed 16 of 17 from the lane path: it took the round from the first `round-NN` in the absolute report path, which under `tools/round-31/` is the wrong one. | `.ufo/waves/round-31/after/cited-runs-gate-selftest-before-fix.txt` (exit 1, `shorthand-relative: FAIL`) | the L1 re-running the selftest at its committed location | Use the last `round-NN` in the path (`cited-runs-gate.py:156-157`); `after/cited-runs-gate-selftest.txt` 17 of 17, exit 0. |
| M31-7 | Containment slip: seat `CriticSeparability` ran `git commit` with its cwd in the fleet repo (exit 1, nothing staged, no commit; it refreshed `.git/index` stat data). | `.ufo/waves/round-31/w1/CriticSeparability.md` (incident section) | none (the wave context forbids it; no tool enforces it) | Recorded; no file changed. Not shown able to fail. |

Round-30 routed defects (`corpus/lessons/round-30-verifier-spotcheck.md:142-151`), disposition:
1. Uncommitted gate PASS: M31-4 above; every gate result in the round-31 report cites a committed receipt.
2. M30-3: both round-31 counters compare the full committed envelope; the copied-predictions control scored 0 of 23 (`w1/CtlC2CopiedPredictions.md`; round 30: 16 of 19). QUALITY row 53.
3. Four wrong pointers: correction appended to `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` (302, 306, 139, 143). Round 31's own 36 pointers were checked before data: 0 wrong (`w1/ReviewPointers.md`).
4. 1 MiB / 64× limits: same appended correction; it cites `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:10`.
5. Lowest axis: stated in `claims.json` before data, here and in the SCORECARD round-31 section; owned-axes coverage and depth rows refreshed to `c369242f` (116/116, 17/17).
6. Token-only Core check: C1's `province_ok` checks placement of a table row under a Core heading; the placement control failed it with real envelopes (`w1/CtlC1Placement.md`). QUALITY row 54.
7. Restore time: correction appended to `corpus/lessons/round-30.md` (≤02:44:44Z).
8. Round-29 docstring: `tools/round-29/c1-fresh-naming.py` docstring-only fix (AST equal without the docstring, `w1/ExecR29Docstring.md`), with an `instrument_supersessions` entry in `.ufo/waves/round-29/claims.json`.

Census note: the round-start census was run at 04:21Z, after the freeze, with `corpus/SOURCES.md` unchanged from the base (`git diff --stat c369242f -- corpus/SOURCES.md` empty): `.ufo/waves/round-31/before/sources-census-start.txt`.
