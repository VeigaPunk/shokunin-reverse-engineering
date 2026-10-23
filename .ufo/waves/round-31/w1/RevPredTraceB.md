# RevPredTraceB — R31-C2 m-* rows traced to REA 6.5.0 code (pre-data)

Item: trace the 13 `m-*` rows of `corpus/evidence/round-31/c2/predictions.tsv` to the code the CLI
actually runs, and predict exit / ok / error.code / details.issues independently from the mutants'
filesystem state. No REA run on any carrier or mutant; no lane files touched besides this report.

- Date: 2026-10-23 (evidence commands run 04:00–04:20 UTC; stamp `2026-10-23T04:19:39Z`).
- Code read: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/...` (6.5.0 tree),
  cited below as `dist/...`; bundled copies in `dist/cli-runtime/cli.js` cited as `cli.js:NNNN`.
- Mutant evidence: `ls -la`, `stat`, `xxd -l 32`, `readlink` — read-only, at
  `/fast/scratch/hyaku/kaidoku-r31/mutants/<id>/`.
- node:sqlite probes: only on my own files under
  `/fast/scratch/hyaku/kaidoku-r31/seats/w1/RevPredTraceB/probe/` (node v24.21.0, `node:sqlite`).
- Installs: none (no tool installed or updated; existing node v24.21.0 used).

## 1. Reconstructed contract (the code the CLI runs)

Input validation first — `dist/sqlite/SqliteDatabaseProvider.js:283-295` (`validateSqliteInput`):
zod parse + `isAbsolute(path)`; all mutant paths are absolute and option-free (or
`--schema-scope database`), so this passes for all 13 rows. `schema_scope:"database"` requires no
table (`dist/domain/sqlite/sqliteDatabase.js:56-61` superRefine only demands `table` for
`"selected_table"`), so rows 7–8 pass input validation.

Then `#inspect` sets `phase = "artifact-read"` and calls
`captureSqliteDatabaseSnapshot` (`dist/sqlite/SqliteDatabaseProvider.js:147-152`;
`cli.js:6213-6216`). Order inside `dist/sqlite/SqliteDatabaseSnapshot.js`
(`captureSqliteDatabaseSnapshot`, lines 104-160):

1. `optionalStat` of `[db, db-wal, db-journal]` (lines 13-21): `ENOENT` → `null`; any other code
   (**ENOTDIR**) is **rethrown raw** (line 19-20).
2. `database === null` → `missingDatabase` (113-114; 97-102): `AnalysisInputError`, issue
   `path:["path"], reason:"invalid_value"`, message `Selected SQLite database does not exist: ${path}`.
3. journal exists → `verifyInactiveJournal(..., "initial")` (115-116):
   - lstat regular-file/symlink check first (52-54) → `ArtifactReaderFailure("path",
     \`Expected a regular journal without a symlink: ${path}\`)` — `path` here is `${db}-journal`;
   - open `O_NOFOLLOW|O_NONBLOCK`, read up to 28 bytes only if size > 0 (67-75);
   - refuse iff `size !== 0 && (bytesRead !== 28 || any nonzero byte)` (76-80) →
     `ArtifactReaderFailure("format", \`Rollback journal may require recovery: ${db}-journal.
     Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported.\`)`.
4. Combined budget **before** any file read (117-119): `selectedSize = db.size + wal?.size ?? 0n`;
   `> 268435456` (`dist/sqlite/SqliteDatabaseLimits.js:4`, `inputBytes = 256*1024*1024`) →
   `ArtifactReaderFailure("limit", \`Selected SQLite database and WAL exceed the combined
   268435456-byte snapshot budget: ${path}\`)`. The journal is not counted.
5. `readObservedArtifact(db)` (121) → `readStableArtifact` (`dist/artifacts/readStableArtifact.js`):
   regular-file/symlink check (31-33) → `ArtifactReaderFailure("path", \`Expected a regular file
   without a symlink: ${path}\`)`; then size-vs-limit check (34-35, unreachable for these rows
   because step 4 already used the same budget).
6. WAL copy (if any), then journal re-verified "after-copy" (149), then full file-set stat
   comparison (150-153).

Failure projection — `dist/sqlite/SqliteDatabaseFailures.js` (`sqliteDatabaseFailure`):
- `AnalysisInputError` passes through unchanged (line 31) — this covers `missingDatabase`.
- `ArtifactReaderFailure`: `reason:"limit"` → issue reason `out_of_range`; any other reason
  (`path`, `format`) → `invalid_format`; issue `path:["path"]`, message = failure message
  (lines 50-56).
- Raw fs `Error` with `code` while `phase === "artifact-read"`: `ENOTDIR`/`ENOENT` →
  `AnalysisInputError` `invalid_value`, message
  `Selected database file set could not be read (${code}): ${path}` — note the message names the
  **selected** path, not the failing member (lines 80-86).

Worker — the CLI spawns the **on-disk** worker file, not a bundled copy:
`cli.js:6061` builds `dist/sqlite/SqliteDatabaseWorker.js` via `new URL("./SqliteDatabaseWorker.js",
new URL("../sqlite/SqliteDatabaseWorkerExecution.js", import.meta.url).href)`. Worker catch maps
`cause.errcode`: `7` → `"memory"`, `18` → `"output-limit"`, else `"format"`, message =
SQLite's message (`dist/sqlite/SqliteDatabaseWorker.js:24-34`). `dist/sqlite/SqliteDatabaseInspection.js:359-371`
opens the snapshot copy with `new DatabaseSync(snapshotPath, { readOnly: true, allowExtension: false,
readBigInts: true, ... })`. `reason:"format"` → `rejectedReply`
(`dist/sqlite/SqliteDatabaseWorkerExecution.js:33-57,110`): `rejectedArgument = { format: "path", ... }`,
issue `path:["path"], reason:"invalid_format", message = reply.message`.

CLI envelope — `dist/cli-runtime/cliResultOutput-DsRMI8CJ.js`: projected `AnalysisInputError` is
detected as failure (`projectCliOperationFailure`/`inferCliOperationFailure` 348-373) →
`process.exitCode = 1` (415) → JSON `{ ok:false, error:{code,...,details}, meta }`
(`fullFailureEnvelope` 762-764). `error.code` for `AnalysisInputError` = `"invalid_request"`
(`dist/domain/analysisErrorProjection.js:142`); `details.issues` = `[{path, reason, message}]`
(`errorDetails` → `requestErrorDetails`, `dist/domain/analysisErrorProjection.js:194-208`).
Accepts → `{ ok:true, data, meta }`, exit 0 (724-727). All `{P}`-style messages are template
literals interpolated at failure-construction time with the exact selected path.

Bundled-copy identity (read in full, compared against dist segments): `cli.js:299-383`
(`readStableArtifact`, regular-file check), `cli.js:5796-5841` (`sqliteDatabaseFailure`, incl.
`ENOTDIR` branch at 5810-5816), `cli.js:5861-5960` (`optionalStat`/`verifyInactiveJournal`/
`missingDatabase`/`captureSqliteDatabaseSnapshot`; journal symlink 5903, rollback refuse 5920,
missing-db 5936, budget 5952), `cli.js:6023-6041` (`rejectedArgument`/`rejectedReply`),
`cli.js:6213-6216` (phase + capture call). Logic identical to dist; only the worker file is loaded
from disk. **Observation** (corrects the task premise): the worker is *not* bundled in cli.js.

## 2. Per-row trace (frozen prediction vs my independent prediction)

Common refusal envelope for rows 1–6 and 9–13: exit `1`, stdout `ok:false`,
`error.code:"invalid_request"`, `details.issues` length 1. Common accept envelope for rows 7–8:
exit `0`, `ok:true`, no error/issues. All messages below with `{P}` replaced by the exact
`/fast/scratch/hyaku/kaidoku-r31/mutants/<id>/...` path.

| # | id | mutant FS (observed) | decisive code (dist; cli.js) | frozen | mine | verdict |
|---|----|----------------------|------------------------------|--------|------|---------|
| 1 | m-missing | dir empty (`ls`: only `.`/`..`) | optionalStat ENOENT→null (Snapshot:19); `database===null`→`missingDatabase` (Snapshot:113-114,97-102); passthrough (Failures:31); projection (AEP:142,194-208) | refuse/1/invalid_request/["path"]/invalid_value/`Selected SQLite database does not exist: {P}` | identical | **agree** |
| 2 | m-enotdir | only `file` (16 B regular); target `.../file/db.sqlite` | optionalStat rethrows ENOTDIR (Snapshot:19-20); phase "artifact-read" (Provider:147-152, cli.js:6213-6216); ENOTDIR branch (Failures:80-86) | refuse/1/invalid_request/["path"]/invalid_value/`Selected database file set could not be read (ENOTDIR): {P}` | identical | **agree** |
| 3 | m-not-sqlite | db 1 067 008 B; bytes 0-15 all zero (xxd), rest valid header | snapshot OK (regular, in budget); worker open → NOTADB errcode 26 (probe A) → `"format"` (Worker:29-33) → `rejectedReply` (WorkerExec:33-57) | refuse/1/invalid_request/["path"]/invalid_format/`file is not a database` | identical | **agree** |
| 4 | m-bad-pagesize | db 1 067 008 B; magic valid; bytes 16-17 = `03 00` = 768 (xxd) | same worker path; page size 768 not power of two → errcode 26 (probe B) → `"format"` | refuse/1/invalid_request/["path"]/invalid_format/`file is not a database` | identical | **agree** |
| 5 | m-journal-hot | db 1 067 008 B + journal 28 B, header `d9d5 05f9 20a1 63d7…` nonzero (xxd) | verifyInactiveJournal "initial" (Snapshot:115-116): size≠0, 28 B read, `header.some(b=>b!==0)` (76-80) → `"format"`; fires before budget (117) and db read (121) | refuse/1/invalid_request/["path"]/invalid_format/`Rollback journal may require recovery: {P}-journal. Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported.` | identical | **agree** |
| 6 | m-journal-short | journal 10 B, all zero (xxd); db valid | size≠0 → read loop stops at 10; `bytesRead(10) !== 28` alone triggers (Snapshot:76-80) → same `"format"` message as row 5 | identical to row 5 | identical | **agree** |
| 7 | m-journal-empty | journal 0 B; db valid | `size!==0n` false → never read, never refused (Snapshot:67-80); `--schema-scope database` needs no table (sqliteDatabase.js:56-61); worker opens db-only snapshot copy → schema listing | accept/0/—/—/—/— | identical (exit 0, ok true) | **agree** |
| 8 | m-journal-zero28 | journal 28 B all zero (xxd); db valid | 28 B read, all zero → `bytesRead===28 && !some(nonzero)` → inactive (Snapshot:76-80) → accept; journal never copied (`writeFile` only `database.snapshot`+`-wal`, Snapshot:123-140) | accept/0/—/—/—/— | identical | **agree** |
| 9 | m-journal-symlink | journal → symlink to `.../carriers/chinook.sqlite` (readlink) | lstat check before any open (Snapshot:52-54) → `"path"` → `invalid_format` (Failures:50-56); `Expected a regular journal without a symlink: {P}-journal` | refuse/1/invalid_request/["path"]/invalid_format/`Expected a regular journal without a symlink: {P}-journal` | identical | **agree** |
| 10 | m-db-symlink | db.sqlite → symlink to chinook.sqlite; no wal/journal | lstat sees link itself (size 55, not null, not dir); budget passes; `readStableArtifact` regular-file check (readStableArtifact:31-33, cli.js:~316) → `Expected a regular file without a symlink: {P}` → invalid_format | refuse/1/invalid_request/["path"]/invalid_format/`Expected a regular file without a symlink: {P}` | identical | **agree** |
| 11 | m-directory | db.sqlite is a directory (stat `%F`=directory) | lstat size 4096 → budget passes; same regular-file check (`isFile()` false) → same message → invalid_format | refuse/1/invalid_request/["path"]/invalid_format/`Expected a regular file without a symlink: {P}` | identical | **agree** |
| 12 | m-over-256mib | db 268 435 457 B regular, no wal/journal | budget check (Snapshot:117-119, Limits:4): 268435457 > 268435456 → `"limit"` → `out_of_range` (Failures:52); fires **before** readStableArtifact's own size/regular checks (121) | refuse/1/invalid_request/["path"]/out_of_range/`Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: {P}` | identical | **agree** |
| 13 | m-wal-over | db 1 067 008 B + wal 267 368 449 B (stat) | 1067008 + 267368449 = 268 435 457 > 268 435 456 → same `"limit"`/`out_of_range` before any byte is read | refuse/1/invalid_request/["path"]/out_of_range/`Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: {P}` | identical | **agree** |

Result: **13/13 agree** at the level of exit, ok, error.code, issue path, issue reason, message.

## 3. Order questions the task flagged

- **Budget vs regular-file check**: budget (Snapshot:117-119) is checked *before*
  `readObservedArtifact`→`readStableArtifact` (121). Both sizes come from the same earlier
  `lstat`s. For a symlink db, lstat returns the link's own byte length (55 for the chinook target
  path) — never over budget — so m-db-symlink/m-directory necessarily reach the regular-file
  message; an oversized regular file necessarily gets the budget message, never
  `Selected artifact exceeds ... bytes` (readStableArtifact:34-35), because the budget check uses
  the same limit value first.
- **Journal before everything local**: the journal lstat/open/header check (115-116) runs before
  the budget check (117) and before any db read (121). A hot journal plus an oversized db would
  report the journal, not the budget. The missing-db check (113-114) precedes the journal check.
- **ENOTDIR beats everything**: thrown from the very first `optionalStat` batch (13-21) and
  projected as `invalid_value` "could not be read (ENOTDIR)" (Failures:80-86) — it never reaches
  the missing-db branch because only `ENOENT` maps to `null` (Snapshot:19).
- **Journal header matrix** (Snapshot:67-80): size 0 → inactive (no read); size 10 (any content,
  here all zero) → `bytesRead 10 ≠ 28` → refuse format; size 28 all zero → inactive (PERSIST
  commit); size 28 nonzero (TRUNCATE-era hot journal `d9d505f9…`) → refuse format.

## 4. node:sqlite probes (my own files only, node v24.21.0)

Command (executed 04:1x UTC, exit 0; full transcript in the shell log):
`node -e` — build `valid.db` with `DatabaseSync` (`CREATE TABLE t …`, one insert), copy to
`zero16.db` and `ps768.db`, zero bytes 0-15 of the copy, set bytes 16-17 of the other to
`0x03 0x00` (= 768 big-endian), then open each with `new DatabaseSync(f, { open: true })`:

```
node v24.21.0
valid.db   -> OPENED OK, sqlite_master rows: 1
zero16.db  -> errcode: 26 code: "ERR_SQLITE_ERROR" message: "file is not a database"
ps768.db   -> errcode: 26 code: "ERR_SQLITE_ERROR" message: "file is not a database"
```

So SQLite (bundled in node v24.21.0) reports `SQLITE_NOTADB` (errcode 26) with message
`file is not a database` for **both** the zeroed magic and the invalid page size 768 — exactly the
frozen `m-not-sqlite`/`m-bad-pagesize` messages, which the worker passes through verbatim
(`Worker.js:24-34` → `WorkerExecution.js:53-55`).

## 5. Divergences and notes

- **Annotation typo, envelope-safe** (observation): predictions.tsv row m-wal-over code_pointer
  comment says "WAL 267367449 bytes"; the actual file is **267 368 449** bytes (`stat -c '%s'`).
  The sum with the db is 268 435 457 in reality (over budget by exactly 1 byte); with the typed
  figure it would be 268 434 457 (under budget). The refusal message contains no sizes, so the
  compared envelope fields are unaffected — but the frozen justification comment does not match
  the bytes on disk. Flagging for the counter owners; no claim-data impact predicted.
- The worker is spawned from the on-disk `dist/sqlite/SqliteDatabaseWorker.js`
  (cli.js:6061), so the worker-side line citations are to the dist files the CLI will really load.
- `verifyInactiveJournal`'s "initial" failure is staged as `ArtifactReaderFailure("format", …)`
  → `invalid_format`; the after-copy re-check stages `"integrity"` (different error class,
  irrelevant for the frozen static mutants).
- Confidence: rows 1,2,5,6,7,8,9,10,11,12,13 — observation-grade (direct code read + on-disk FS
  facts). Rows 3,4 — observation for the probe outputs, inference only in mapping errcode 26 →
  identical worker message (mapping code read directly; the mutants' exact bytes produce the same
  header conditions as my probe files: zeroed magic verified byte-for-byte for rows 3, and `03 00`
  at offset 16 for row 4 via `xxd -l 32`).

## 6. Commands and artifacts

Evidence commands (all `timeout`-bounded, read-only on mutants):
- `for m in …; do ls -la /fast/scratch/hyaku/kaidoku-r31/mutants/$m/; done`
- `stat -c '%n %s %F'` per member; `xxd -l 32` on db/journal heads; `readlink` on the two symlinks.
- `grep -n` line-number pins over the REA dist tree and `dist/cli-runtime/cli.js`.
- `read` (tool) of full file bodies: SqliteDatabaseSnapshot.js, SqliteDatabaseFailures.js,
  readStableArtifact.js, SqliteDatabaseWorker.js, SqliteDatabaseWorkerExecution.js,
  SqliteDatabaseLimits.js, SqliteDatabaseProvider.js:35-135, analysisErrorProjection.js,
  cli.js:299-383 / 5790-5965 / 6180-6268, cliResultOutput-DsRMI8CJ.js:340-430 / 640-779.
- Probe command shown verbatim in §4 (exit 0). No REA invocation anywhere. No lane writes except
  this report.

Seat artifacts under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/RevPredTraceB/` (sha256):
```
843640b6a878c4d95af42bed4300a70c07d5cbbbb20164f2067ea785b3a6ccea  probe/ps768.db
ecbff0cebc67c0bfde1b95f0a25f1c3f53cd902f9c6d7232773b03a15af753a0  probe/valid.db
f06fbfa92a6197db3c6a34d7eba4933e1c77c4e0a879da48709bcd79c21e8ee7  probe/zero16.db
```
(no scripts or clones; `tmp/` left empty)

## 7. Verdict

All 13 `m-*` frozen predictions are consistent with the REA 6.5.0 code paths traced end-to-end and
with the mutants' filesystem state: **13 agree, 0 disagree, 0 could-not-evaluate**. The single
divergence found is the m-wal-over size figure inside the frozen `code_pointer` comment
(267367449 vs actual 267368449), which does not touch any compared envelope field.
