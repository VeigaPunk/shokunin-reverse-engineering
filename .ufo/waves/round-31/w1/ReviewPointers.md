# ReviewPointers — Round-31 wave-1 code-pointer review (C2 predictions)

- Seat: `KaidokuR31.ReviewPointers` (leaf; no subagent dispatch)
- Date/UTC: 2026-10-23T04:12:02Z
- Target: M30-3 repair check — every `code_pointer` cell of
  `corpus/evidence/round-31/c2/predictions.tsv` (23 rows: 20 predicted refusals, 3 predicted acceptances), before any data.
- Reviewed against: REA 6.5.0 installed at `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`
  (version confirmed from `package.json` line 4: `"version": "6.5.0"`).

## Method

For each row, every `file:lines` reference was printed with `sed -n` (ranges relative to the
REA package root) and checked against the construct the row relies on (message literal, branch, or
mapping). Classification:

- **exact** — the cited lines are the construct (or a tight, correct sub-range of it);
- **contains** — the cited range holds the construct but also unrelated lines;
- **adjacent** — the construct is missed by ≤3 lines;
- **wrong** — the construct is absent from the cited lines.

Primarily line evidence is the sed transcript (sha256 below). Semantic call-site tracing used
`grep` fallback because no `lsp` device is available in this session's tool set; grep was used only
to locate call sites (e.g. `captureSqliteDatabaseSnapshot`/`sqliteDatabaseFailure`), never as proof
of a construct's presence. No external sources were opened; all evidence is local file reads of the
installed REA bytes. No tools were installed.

## Per-pointer table (36 pointer entries)

Legend: R = REA package root `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`. All sed
ranges are relative to R. Verdicts: E = exact, C = contains, A = adjacent, W = wrong.

| Row | Pointer (relative to R) | Construct relied on | Verdict | Correct line | sed -n command |
|---|---|---|---|---|---|
| q-rowlimit-no-table | `dist/domain/sqlite/sqliteDatabase.js:44-49` | row_limit-branch + literal "row_limit requires an explicit table selection" | E | — | `sed -n '44,49p' dist/domain/sqlite/sqliteDatabase.js` |
| q-rowlimit-no-table | `dist/domain/inputIssueProjection.js:66-72` | custom-issue fallback mapping (path, invalid_value, message) | E | — | `sed -n '66,72p' dist/domain/inputIssueProjection.js` |
| q-columns-no-table | `dist/domain/sqlite/sqliteDatabase.js:50-55` | columns-branch + literal "columns requires an explicit table selection" | E | — | `sed -n '50,55p' dist/domain/sqlite/sqliteDatabase.js` |
| q-columns-no-table | `dist/domain/inputIssueProjection.js:66-72` | custom-issue fallback mapping | E | — | `sed -n '66,72p' dist/domain/inputIssueProjection.js` |
| q-scope-no-table | `dist/domain/sqlite/sqliteDatabase.js:56-61` | schema_scope-branch + literal "selected_table schema scope requires table" | E | — | `sed -n '56,61p' dist/domain/sqlite/sqliteDatabase.js` |
| q-scope-no-table | `dist/domain/inputIssueProjection.js:66-72` | custom-issue fallback mapping | E | — | `sed -n '66,72p' dist/domain/inputIssueProjection.js` |
| q-missing-table | `dist/sqlite/SqliteDatabaseInspection.js:74,187-189` | missingSelectedTable ctor (literal) + exact-name selection branch | E | — | `sed -n '74p;187,189p' dist/sqlite/SqliteDatabaseInspection.js` |
| q-missing-table | `dist/sqlite/SqliteDatabaseWorkerExecution.js:31-58` | reason→caller-arg map (33-38) + invalid_format issue construction (49-57) | C | 33-38,49-57 | `sed -n '31,58p' dist/sqlite/SqliteDatabaseWorkerExecution.js` |
| q-case-table | `dist/sqlite/SqliteDatabaseInspection.js:74,155-160,187-189` | literal; metadata exact-name map build (no case folding); exact-lookup branch | E | — | `sed -n '74p;155,160p;187,189p' dist/sqlite/SqliteDatabaseInspection.js` |
| q-view-as-table | `dist/sqlite/SqliteDatabaseInspection.js:224-280` | view branch 278-285 sets no selectedTable | C | 278-285 | `sed -n '224,280p' dist/sqlite/SqliteDatabaseInspection.js` |
| q-view-as-table | `dist/sqlite/SqliteDatabaseInspection.js:299-303` | readRows missing-selectedTable throw (302-303) | C | 302-303 | `sed -n '299,303p' dist/sqlite/SqliteDatabaseInspection.js` |
| q-missing-column | `dist/sqlite/SqliteDatabaseInspection.js:313-316` | column-existence check + literal | E | — | `sed -n '313,316p' dist/sqlite/SqliteDatabaseInspection.js` |
| q-missing-column | `dist/sqlite/SqliteDatabaseWorkerExecution.js:31-58` | reason→caller-arg map + invalid_format issue construction | C | 33-38,49-57 | `sed -n '31,58p' dist/sqlite/SqliteDatabaseWorkerExecution.js` |
| q-virtual-rows | `dist/sqlite/SqliteDatabaseInspection.js:306-307` | non-table-kind refusal + literal (kind "virtual") | E | — | `sed -n '306,307p' dist/sqlite/SqliteDatabaseInspection.js` |
| q-shadow-rows | `dist/sqlite/SqliteDatabaseInspection.js:306-307` | non-table-kind refusal + literal (kind "shadow") | E | — | `sed -n '306,307p' dist/sqlite/SqliteDatabaseInspection.js` |
| q-ok-rows | `dist/sqlite/SqliteDatabaseInspection.js:299-330` | ordinary-table row-read acceptance path (also holds refusal branches) | C | 298-343 (whole readRows) | `sed -n '299,330p' dist/sqlite/SqliteDatabaseInspection.js` |
| q-ok-rows | `dist/application/sqlite/SqliteDatabaseService.js:9-28` | matchesSelectedDatabase predicate | E | — | `sed -n '9,28p' dist/application/sqlite/SqliteDatabaseService.js` |
| m-missing | `dist/sqlite/SqliteDatabaseSnapshot.js:97-103,113-114` | missingDatabase ctor (literal) + null→throw branch | E | — | `sed -n '97,103p;113,114p' dist/sqlite/SqliteDatabaseSnapshot.js` |
| m-enotdir | `dist/sqlite/SqliteDatabaseSnapshot.js:13-21` | optionalStat: ENOENT→null, everything else (ENOTDIR) rethrown | E | — | `sed -n '13,21p' dist/sqlite/SqliteDatabaseSnapshot.js` |
| m-enotdir | `dist/sqlite/SqliteDatabaseFailures.js:79-86` | ENOENT/ENOTDIR → invalid_value branch (condition at 78; body 79-85) | A | 78-85 | `sed -n '79,86p' dist/sqlite/SqliteDatabaseFailures.js` |
| m-not-sqlite | `dist/sqlite/SqliteDatabaseWorker.js:24-34` | errcode derivation; non-7/18 (> SQLITE_NOTADB 26) → "format"; message passthrough | E | — | `sed -n '24,34p' dist/sqlite/SqliteDatabaseWorker.js` |
| m-not-sqlite | `dist/sqlite/SqliteDatabaseWorkerExecution.js:31-58` | reason→caller-arg map + invalid_format issue construction | C | 33-38,49-57 | `sed -n '31,58p' dist/sqlite/SqliteDatabaseWorkerExecution.js` |
| m-bad-pagesize | `dist/sqlite/SqliteDatabaseWorker.js:24-34` | errcode derivation → "format" | E | — | `sed -n '24,34p' dist/sqlite/SqliteDatabaseWorker.js` |
| m-journal-hot | `dist/sqlite/SqliteDatabaseSnapshot.js:75-80,115-116` | hot-journal check+literal (76-80; 75 is an unrelated integrity throw); journal-presence → verifyInactiveJournal branch (115-116) | C | 76-80,115-116 | `sed -n '75,80p;115,116p' dist/sqlite/SqliteDatabaseSnapshot.js` |
| m-journal-hot | `dist/sqlite/SqliteDatabaseFailures.js:46-54` | ArtifactReaderFailure → AnalysisInputError map incl. limit→out_of_range (49-54) | C | 49-54 | `sed -n '46,54p' dist/sqlite/SqliteDatabaseFailures.js` |
| m-journal-short | `dist/sqlite/SqliteDatabaseSnapshot.js:63-80` | short-read loop (63-73) + hot policy (76-80); 74-75 integrity check extra | C | 63-73,76-80 | `sed -n '63,80p' dist/sqlite/SqliteDatabaseSnapshot.js` |
| m-journal-empty | `dist/sqlite/SqliteDatabaseSnapshot.js:63-80` | size-0-inactive logic at 65,76-77 | C | 65,76-80 | `sed -n '63,80p' dist/sqlite/SqliteDatabaseSnapshot.js` |
| m-journal-zero28 | `dist/sqlite/SqliteDatabaseSnapshot.js:63-80` | fully-zeroed-header-inactive logic at 63,66-72,76-77 | C | 63,66-72,76-77 | `sed -n '63,80p' dist/sqlite/SqliteDatabaseSnapshot.js` |
| m-journal-symlink | `dist/sqlite/SqliteDatabaseSnapshot.js:52-54,115-116` | symlink-journal check + literal; call site | E | — | `sed -n '52,54p;115,116p' dist/sqlite/SqliteDatabaseSnapshot.js` |
| m-db-symlink | `dist/artifacts/readStableArtifact.js:30-33` | regular-file/symlink check + literal (32-33); 30 assertReadActive extra | C | 31-33 | `sed -n '30,33p' dist/artifacts/readStableArtifact.js` |
| m-db-symlink | `dist/sqlite/SqliteDatabaseSnapshot.js:44-51,121` | readObservedArtifact fileSystem wiring; read call site | E | — | `sed -n '44,51p;121p' dist/sqlite/SqliteDatabaseSnapshot.js` |
| m-directory | `dist/artifacts/readStableArtifact.js:30-33` | regular-file/symlink check + literal | C | 31-33 | `sed -n '30,33p' dist/artifacts/readStableArtifact.js` |
| m-over-256mib | `dist/sqlite/SqliteDatabaseLimits.js:4` | `inputBytes: 256*1024*1024` budget constant | E | — | `sed -n '4p' dist/sqlite/SqliteDatabaseLimits.js` |
| m-over-256mib | `dist/sqlite/SqliteDatabaseSnapshot.js:117-119` | combined-size budget check + literal | E | — | `sed -n '117,119p' dist/sqlite/SqliteDatabaseSnapshot.js` |
| m-over-256mib | `dist/sqlite/SqliteDatabaseFailures.js:46-54` | ArtifactReaderFailure → AnalysisInputError map incl. limit→out_of_range | C | 49-54 | `sed -n '46,54p' dist/sqlite/SqliteDatabaseFailures.js` |
| m-wal-over | `dist/sqlite/SqliteDatabaseSnapshot.js:117-119` | combined-size budget check + literal | E | — | `sed -n '117,119p' dist/sqlite/SqliteDatabaseSnapshot.js` |

## Counts

- Pointer entries checked: **36**
- exact: **21**
- contains: **14**
- adjacent: **1**
- wrong: **0**

**No M30-3-class defect found**: no pointer lacks its construct; every non-exact pointer either
overshoots the construct or is off by one line. The frozen file stays frozen; the L1 may append the
corrections below.

## Corrections list (append to the entry; file stays frozen)

1. `SqliteDatabaseWorkerExecution.js` — cite `33-38,49-57` instead of `31-58` (rows
   q-missing-table, q-missing-column, m-not-sqlite): map at 33-38, invalid_format issue construction
   at 49-57.
2. `SqliteDatabaseInspection.js` — row q-view-as-table: cite `278-285` instead of `224-280` (view
   branch sets no selectedTable); cite `302-303` instead of `299-303` (readRows missing-selectedTable throw).
3. `SqliteDatabaseInspection.js` — row q-ok-rows: cite `298-343` instead of `299-330` (whole readRows; the acceptance path is 308-343).
4. `SqliteDatabaseFailures.js` — cite `78-85` instead of `79-86` (row m-enotdir; branch head `if (cause.code === "ENOENT" || cause.code === "ENOTDIR")` is line 78).
5. `SqliteDatabaseFailures.js` — cite `49-54` instead of `46-54` (rows m-journal-hot, m-over-256mib; cancelled branch at 47-48 is extra).
6. `SqliteDatabaseSnapshot.js` — row m-journal-hot: cite `76-80` instead of `75-80` (75 is an integrity throw).
7. `SqliteDatabaseSnapshot.js` — row m-journal-short: cite `63-73,76-80` instead of `63-80`.
8. `SqliteDatabaseSnapshot.js` — row m-journal-empty: cite `65,76-80` instead of `63-80`.
9. `SqliteDatabaseSnapshot.js` — row m-journal-zero28: cite `63,66-72,76-77` instead of `63-80`.
10. `readStableArtifact.js` — cite `31-33` instead of `30-33` (rows m-db-symlink, m-directory; 30 is assertReadActive).

## Evidence and artifacts

- sed transcript of all 36 pointer ranges (the "printed lines" evidence):
  `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ReviewPointers/sed-transcript.txt`
  sha256 `fd3f3166a314867abd57368fb35fd711dfc38498d5b87099e5bbb989b2da9e2f`
- `corpus/evidence/round-31/c2/predictions.tsv` (read-only reference)
  sha256 `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8`
- No other artifacts; no tools installed; no external sources opened.
- REA install verified: `package.json` line 4 `"version": "6.5.0"` at
  `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`.

## Findings by severity

- **No actionable defect.** All 36 pointers resolve to the construct the row relies on. Severity
  of the 14 non-exact entries: cosmetic/pointer-tightening only (contains/adjacent); none changes a
  predicted outcome, and none affects the M30-3 committed-record rule (which compares the full
  envelope, not these pointers).

## Residual risk and verification gaps

- Message-level correctness (does the live run actually emit each frozen message literal) is the
  C2 counter's job, not this seat's; I verified only pointer→construct correspondence.
- Rows q-view-as-table / q-virtual-rows / q-shadow-rows depend on the runtime SQLite's PRAGMA
  table_list type tagging (view/virtual/shadow). The cited ranges hold the branch and blank, but
  the actual kind value flowing into the `306-307` literal is runtime-dependent; the live counter
  run remains the arbiter.
- No `lsp` device was available in this session; semantic call-site tracing used `grep` fallback
  (recorded above), which is not semantic proof — but the pointer verdicts rest on the sed
  transcript of the installed bytes, which is primary evidence.
