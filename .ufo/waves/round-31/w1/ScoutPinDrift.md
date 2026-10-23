# ScoutPinDrift — REA pin drift, SQLite reader (6.5.0 round pin vs 6.7.0 client pin)

Seat: KaidokuR31.ScoutPinDrift. Date 2026-10-23 (UTC). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
Method: read-only `diff`/`diff -r` of the two npx caches plus source reading; no REA invocation; no lane
mutation beyond this report. Everything under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ScoutPinDrift/`.

## Pins compared

| pin | path | package.json version |
|---|---|---|
| round | `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | `6.5.0` |
| client | `~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` | `6.7.0` |

Observation: the `cli-runtime` bundles and `incur` are `0.6.1` in **both** caches, so CLI flag parsing and
exit-status plumbing are the same library in both pins.

## 1. Changed files (the assigned comparison set)

`diff -rq`, 2026-10-23T04:14:29Z, exit 1 for each differing file (full receipts in `out/receipts.txt`,
`out/changed-files.txt`):

| file | 6.5.0 sha256 | 6.7.0 sha256 |
|---|---|---|
| `dist/sqlite/SqliteDatabaseFailures.js` | `5a908695…90d419` | `eb4467eb…cde188` |
| `dist/sqlite/SqliteDatabaseInspection.js` | `edfcd90f…354970` | `31d2e208…35c9e` |
| `dist/sqlite/SqliteDatabaseSnapshot.js` | `c8af51f8…40ce19` | `87858b4a…36d277` |
| `dist/sqlite/SqliteDatabaseWorkerExecution.js` | `6e49c2ab…e4c203` | `875bad2e…4a6fc` |
| `dist/domain/sqlite/sqliteDatabase.js` | `c7a0eff5…000ae1` | `5f479efd…b289c1` |
| `dist/cli/sqliteCommands.js` | `c2ed3898…550d73` | `adf35d10…224ed` |
| `dist/artifacts/readStableArtifact.js` | `06a23746…9d2707` | `e5e889f3…f1213` |

Unchanged (sha256 equal in both pins): all of `dist/application/sqlite/` (`SqliteDatabaseCapability.js`,
`SqliteDatabasePort.js`, `SqliteDatabaseService.js`), `dist/sqlite/SqliteDatabaseWorker.js`
(`ebb39f58…60cf63`), `dist/sqlite/SqliteDatabaseLimits.js` (`92df76ff…074121`), and
`dist/domain/inputIssueProjection.js`.

## 2. Hunks per file

### `dist/sqlite/SqliteDatabaseSnapshot.js` — the one hunk that changes frozen predictions

6.5.0 (lines 117-119):
```js
const selectedSize = database.size + (wal?.size ?? 0n);
if (selectedSize > BigInt(SQLITE_DATABASE_LIMITS.inputBytes))
    throw new ArtifactReaderFailure("limit", `Selected SQLite database and WAL exceed the combined ${String(SQLITE_DATABASE_LIMITS.inputBytes)}-byte snapshot budget: ${path}`);
```
6.7.0 (lines 136-145):
```js
const selectedSize = database.size + (wal?.size ?? 0n);
if (selectedSize > BigInt(SQLITE_DATABASE_LIMITS.inputBytes))
    throw new AnalysisResourceConstraintError("inspect_sqlite_database", "file-size", `Selected SQLite database and WAL total ${selectedSize.toString()} bytes, exceeding the combined ${String(SQLITE_DATABASE_LIMITS.inputBytes)}-byte offline snapshot budget: ${path}`, {
        sqlite_snapshot_input_bytes: SQLITE_DATABASE_LIMITS.inputBytes,
        observed_sqlite_snapshot_input_bytes: selectedSize.toString(),
    }, { remediationAction: "Use the application's supported export workflow … REA will not truncate or modify the selected source." });
if (journal !== null)
    await verifyInactiveJournal(…);
```
Other hunks in this file:
- Sidecar observation split into `optionalSidecarStat`: database is stat'd first, then `${path}-wal`, then
  `${path}-journal` (6.5.0 used one `Promise.all`). 6.7.0 adds an `ENAMETOOLONG` branch producing
  `AnalysisCapabilityUnavailableError` with a path-length remedy.
- `verifyInactiveJournal` moved from **before** the size check to **after** it (order change, see 3e).
- `duringAcquisition` adds `ENAMETOOLONG` to the ENOENT/ENOTDIR/ELOOP "file set changed" set, and converts
  a mid-acquisition `ArtifactReaderFailure("limit")` into `ArtifactReaderFailure("integrity")`
  ("… exceeded its observed size during acquisition").
- `OwnedFileHandle` + manual `finally` replaced by `withArtifactFileHandle` /
  `assertArtifactReadActive` from the new `dist/artifacts/ArtifactFileOperation.js` (absent in 6.5.0).
- Dead branch `throw new Error("Incomplete database file-set observation")` removed (`optionalStat`
  returns `null`, never `undefined`).

### `dist/sqlite/SqliteDatabaseInspection.js`

- `columnRow` now parses `name`, `type`, `dflt_value` as `Uint8Array` instead of `string`.
- `readColumns` query changed from `PRAGMA main.table_xinfo(<quoted name>)` to
  `SELECT cid, CAST(name AS BLOB) AS name, CAST(type AS BLOB) AS type, "notnull", CAST(dflt_value AS BLOB) AS dflt_value, pk, hidden FROM temp.pragma_table_xinfo(?, 'main') [WHERE CAST(name AS BLOB) IN (CAST(? AS BLOB), …)]`,
  decoding each text with the existing `decodeSchemaText(value, encoding, …)` and returning
  `columns.sort((l, r) => l.cid - r.cid)`.
- Call site passes `{ budget, encoding, selectedColumns: scope === "inventory" ? input.columns : undefined }`,
  so the `WHERE … IN (...)` subset only applies to `--schema-scope inventory` with `--column`.
- No other change: `engine: { name: "SQLite", version }` (`sqlite_version()` at line 407), `database_encoding`,
  `limitations`, `scope/completeness`, `artifact`, `wal`, `rows` are byte-identical code.

### `dist/sqlite/SqliteDatabaseFailures.js`

- `ArtifactReaderFailure` fallback issue reason: `cause.reason === "limit" ? "out_of_range" : "invalid_format"`
  becomes unconditional `"invalid_format"`.
- Cleanup branch rewritten around `ArtifactFileCleanupFailure` / `bindArtifactFileCleanup`; cancellation now
  uses `artifactFileCancellationCause`.
- `cause.code` set for the "file set could not be read" branch extended from `ENOENT|ENOTDIR` to
  `ENOENT|ENOTDIR|ELOOP|ENAMETOOLONG` (message format string unchanged).
- `if (cause instanceof AnalysisError) return cause;` unchanged, so the new 6.7.0
  `AnalysisResourceConstraintError` passes through this mapper untouched.

### `dist/sqlite/SqliteDatabaseWorkerExecution.js`

Only the malformed/missing reply branch: 6.7.0 distinguishes `ArtifactFileCleanupFailure` + aborted signal
(→ `AnalysisCancelledError`) from the `AnalysisOutputError` "Owned SQLite worker reply is missing or
malformed"; both bind cleanup. `if (!reply.ok) throw rejectedReply(reply, capturedOutput);` is unchanged.

### `dist/domain/sqlite/sqliteDatabase.js`

Descriptor-only: `.describe("… selected_table requires table. …")` and a new object-level
`.describe("When schema_scope is selected_table, also provide table.")`. The `.superRefine` issue
(`row_limit`/`columns`/`schema_scope` require a table) is identical, so the three `q-*-no-table` refusals
are unchanged; only `--help` text drifts.

### `dist/cli/sqliteCommands.js`

`run` body replaced by `finishAnalysisCommand(...)` and `path: resolve(args.path)` by
`path: absoluteCallerPath(args.path)`. For the frozen absolute, lexically clean paths both yield the same
string; `absoluteCallerPath` only strips `.` segments/repeated separators and keeps `..` for the filesystem.

### `dist/artifacts/readStableArtifact.js`

`assertReadActive` → `assertArtifactReadActive`; `OwnedFileHandle`/`finally` → `withArtifactFileHandle`;
`"limit"` failures now carry `{ boundary: "file-size" }`. No message or reason change that reaches a
frozen request (see 3d).

## 3. Prediction-relevant hunks: exactly **2 of 23** predictions change

### a. `m-over-256mib` — changes

Frozen: `refuse / exit 1 / invalid_request / ["path"] / out_of_range /
"Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: {P}"`.

Actual file (observation, `stat`, 2026-10-23T04:14:29Z): `m-over-256mib/db.sqlite` is a sparse
268435457-byte regular file (no WAL), i.e. budget + 1.

Under 6.7.0 the same input throws `AnalysisResourceConstraintError`, which
`projectAnalysisError` renders as (`dist/domain/analysisErrorProjection.js:55-71`,
`analysisErrorPresentation.js:153-177`, `errorSchemas.js`):
```
ok: false
error.code:        "resource_constraint"
error.category:    "resource_constraint"
error.message:     "Selected SQLite database and WAL total 268435457 bytes, exceeding the combined 268435456-byte offline snapshot budget: /fast/scratch/hyaku/kaidoku-r31/mutants/m-over-256mib/db.sqlite"
error.retryable:   false
error.remediation.action: "Use the application's supported export workflow to create a consistent, smaller offline SQLite snapshot containing only the relevant data, then inspect that snapshot. REA will not truncate or modify the selected source."
error.details:     { operation: "inspect_sqlite_database", resource: "file-size", reason: <same as message>,
                     reported_limits: { sqlite_snapshot_input_bytes: 268435456,
                                        observed_sqlite_snapshot_input_bytes: "268435457" } }
                   (no `issues` key: `issues` is projected only for AnalysisInputError)
```
Exit stays 1 (see 3f). Verdict: **this frozen prediction fails under 6.7.0** on `code`, `issue_path`,
`issue_reason`, `message`, plus envelope `details`/`remediation`. High confidence: constructor arguments
read at `SqliteDatabaseSnapshot.js:138-143`.

### b. `m-wal-over` — changes, identically

Frozen: same refusal text, same `out_of_range`.
Observation (`stat`): `db.sqlite` 1067008 bytes + `db.sqlite-wal` 267368449 bytes = 268435457 = budget + 1.
Under 6.7.0: `code "resource_constraint"`, message
`Selected SQLite database and WAL total 268435457 bytes, exceeding the combined 268435456-byte offline snapshot budget: /fast/scratch/hyaku/kaidoku-r31/mutants/m-wal-over/db.sqlite`,
`details.reported_limits.{sqlite_snapshot_input_bytes, observed_sqlite_snapshot_input_bytes}`, no `issues`.
Verdict: **fails under 6.7.0**.

Note (observation, not a drift issue): the frozen row's `code_pointer` annotation says
"WAL 267367449 bytes"; the actual file is 267368449 (the `--build` code truncates to
`BUDGET + 1 - len(base)`). The refusal itself is real (sum = budget + 1).

### c. The other 21 predictions — no changing hunk

- `q-rowlimit-no-table`, `q-columns-no-table`, `q-scope-no-table`: only `.describe()` text changed in
  `domain/sqlite/sqliteDatabase.js`; `.superRefine` and `inputIssueProjection.js` are identical.
- `q-missing-table`, `q-case-table`, `q-view-as-table`, `q-missing-column`, `q-virtual-rows`,
  `q-shadow-rows`: the refusal sites in `SqliteDatabaseInspection.js` (exact-name `metadata.get`,
  kind `virtual`/shadow selection, `column-selection`) are untouched; `readColumns` is only reached after a
  valid ordinary table is resolved, and with `--table` the call passes `selectedColumns: undefined` (default
  `selected_table` scope), i.e. the full column list as before. `rejectedReply` in
  `SqliteDatabaseWorkerExecution.js` is unchanged.
  Cosmetic only: the 6.7.0 `readColumns` rewrite shifts later line numbers by about +15 relative to the
  line numbers cited in `predictions.tsv`; the C2 counter compares code/issue/message, not pointers.
- `q-ok-rows`: acceptance path unchanged; `columns` order is `cid` order in both (`table_xinfo` returns
  ascending `cid`, and 6.7.0's explicit sort is a no-op — see 4).
- `m-missing`: `missingDatabase(path)` message and `["path"]/invalid_value` unchanged; the database is
  still stat'd before any sidecar in 6.7.0.
- `m-enotdir`: the branch condition gained `ELOOP|ENAMETOOLONG` but `ENOTDIR` was already there and the
  message format is unchanged → identical envelope.
- `m-not-sqlite`, `m-bad-pagesize`: worker error → `SQLITE_NOTADB` mapping lives in
  `SqliteDatabaseWorker.js`, byte-identical.
- `m-journal-hot`, `m-journal-short`, `m-journal-empty`, `m-journal-zero28`, `m-journal-symlink`:
  `verifyInactiveJournal` body and both message strings ("Rollback journal may require recovery: …",
  "Expected a regular journal without a symlink: …") are unchanged; `optionalSidecarStat` returns the same
  `lstat` for a symlink or a normal file. `assertArtifactReadActive` only changes the cancellation path.
- `m-db-symlink`, `m-directory`: "Expected a regular file without a symlink: {P}" from
  `readStableArtifact` is unchanged (message, `path` reason, projection to `invalid_format`).

### d. Why the `limit` → `invalid_format` change does not move any frozen row by itself

The only `ArtifactReaderFailure("limit")` that a frozen request could reach in 6.7.0 is a mid-acquisition
size overrun, which `duringAcquisition` now rewrites to `"integrity"`. The direct budget refusal no longer
uses `ArtifactReaderFailure` at all (it throws the resource-constraint error before reading). So rule (a)/(b)
is the drift that matters, not the ternary.

### e. Order change (real semantic drift, not exercised by the freeze)

In 6.5.0 the journal is verified **before** the size check; in 6.7.0 **after**. A request that is both over
budget and carries a hot journal would report the journal refusal under 6.5.0 and
`resource_constraint` under 6.7.0. No frozen request combines these properties (each mutant carries
exactly one feature).

### f. Exit status is not affected

`logCliCommand` (`dist/cliLogging.js`) sets `process.exitCode = 1` when the returned value parses as
`analysisErrorProjectionSchema`. That schema is byte-identical in both pins
(`dist/contracts/errorSchemas.js`), and `resource_constraint` is a member of its discriminated union, so the
6.7.0 projection still parses and the process still exits 1. The 6.7.0 rewrite of `inferCliOperationFailure`
only wraps the payload identity; detection is preserved. [INFERENCE from code, not a live run.]

## 4. C1 report fields: no changing hunk

Fields C1 compares (`tools/round-31/sqlite_oracle.py:222-229`): `artifact{path,sha256,bytes}`, `wal`,
`engine{name}` (version dropped), `database_encoding`, `schema{scope,completeness,tables,indexes,views,triggers}`
and every table/column field (`cid,name,declared_type,not_null,default_sql,primary_key_position,hidden`),
`rows`. Nothing in the diffs touches `engine`, `encoding`, `artifact`, `wal`, table/index/view/trigger
shaping, or `scope/completeness`. The only report-field-adjacent rewrite is `readColumns`
(`name`/`declared_type`/`default_sql` now read as BLOB and decoded with `decodeSchemaText`).

Empirical check of that rewrite on the 12 frozen carriers (`out/check_columns_equiv.py`, exit 0,
2026-10-23T04:1xZ, system libsqlite3 3.54.0, read-only `mode=ro&immutable=1`):
```
carriers 12 encodings {'\x00\x00\x00\x01'} tables 313 columns 3060 mismatched_tables 0
```
- all 12 headers carry text-encoding 1 = UTF-8 (byte 56..59), so `decodeSchemaText(…, "UTF-8")` is the same
  transform the `PRAGMA` text path already applied;
- for all 313 ordinary tables the 6.5.0 form (`PRAGMA main.table_xinfo("<name>")`, TEXT) and the 6.7.0 form
  (`CAST(… AS BLOB)` + strict UTF-8 decode) are byte-equal on every `(cid, name, type, default, hidden)`
  tuple, with 0 mismatches and 0 ordering deviations.

Conclusion: no C1 report field changes for the 12 carriers. [INFERENCE grounded in the rewrite reading plus
the equivalence check; the 6.7.0 pin was not executed — lane rule restricts REA to counters.]
Residual risk: a UTF-16 or malformed-text carrier would now take the strict `decodeSchemaText` path
(`SqliteInspectionFailure("format", "SQLite schema … contains malformed … text")`) where 6.5.0 tolerated the
pragma's replacement text. None of the frozen carriers is such a file.

The `--schema-scope inventory` column subset does not change output: `column_count` comes from
`PRAGMA main.table_list`'s `ncol`, not from the read columns, and the inventory column array is discarded
(only `selectedTable` keeps it, and `readRows` prefers `input.columns` anyway).

## 5. SQLite versions

| reader | version | command / exit |
|---|---|---|
| Node bundled (`node:sqlite`) | **3.53.4** | `node -e "…new s.DatabaseSync(':memory:')…select sqlite_version() v…"` → `{ v: '3.53.4' }`, rc 0 |
| Node runtime | v24.21.0 | `node -v`, rc 0 |
| system libsqlite3 used by python3 | **3.54.0** | `python3 -I -B -c "import sqlite3;print(sqlite3.sqlite_version)"` → `3.54.0`, rc 0; `readlink -f /usr/lib/libsqlite3.so` → `/usr/lib/libsqlite3.so.3.54.0`; python 3.14.8 maps `libsqlite3.so.3.54.0` |

Consequence: REA 6.5.0 and 6.7.0 both open SQLite through `node:sqlite` (`DatabaseSync`) on the same host
Node, so `engine.version` is a property of the **runtime**, not of the REA pin. C1 drops `engine.version`,
and the committed-envelope rule compares 6.5.0 against 6.5.0, so the version difference does not enter any
frozen comparison. The oracle's independent check uses libsqlite3 3.54.0 against its pure-Python b-tree
parser; that is unchanged by this item.

## 6. Adjacent drift outside the assigned set (same contract, reported for completeness)

Also differing between the pins and reachable from the SQLite path: `dist/artifacts/ArtifactReader.js`
(`ArtifactReaderFailure` gains `cancellation`, `cleanupLeases`, `boundary`; `withCleanup` gains a lease
argument; `cleanupObservation` accepts resource arrays), a new `dist/artifacts/ArtifactFileOperation.js`
(absent in 6.5.0), `dist/domain/analysisErrorCore.js` (`AnalysisResourceConstraintError.retryable`,
`AnalysisCapabilityUnavailableError.remediationAction`, `AnalysisTimeoutError.{userMessage,remediationAction}`),
`dist/domain/analysisErrorProjection.js` (cleanup/partial-observation composition, `retryable ?? resource ===
"capacity"`), `dist/domain/analysisErrorPresentation.js`, `dist/cliLogging.js`, `dist/cli.js`,
`dist/cliOutput.js`, `scripts/rea.mjs` (`normalizeCliArguments`, SIGPIPE 141, `exit` hook).
Verdict for the 23 frozen predictions: none of these changes the compared fields of the 21 unaffected rows;
for the two affected rows they only alter the projected shape already described in 3a/3b. Output-flag
handling is a no-op for the counters' spaced `--format json --full-output` form.

## 7. Verdict

- Changed-file list: 7 files in the assigned set differ; `dist/application/sqlite/*` is identical.
- Prediction-relevant hunks: **2 of 23** frozen C2 predictions change under 6.7.0 — `m-over-256mib` and
  `m-wal-over` (refusal moves from `invalid_request`/`out_of_range`/`issues` to
  `resource_constraint`/`file-size`/`reported_limits`, with a new message and remediation; exit remains 1).
  The other 21 hold.
- C1 report fields: none change for the 12 frozen carriers.
- SQLite versions: node bundled 3.53.4 (node v24.21.0); system libsqlite3 3.54.0 (python 3.14.8).
- Confidence: high for the two changed predictions (constructor arguments read verbatim); medium-high for
  "no C1 field changes" (static reading plus the 12-carrier/3060-column equivalence check); no live 6.7.0
  run was performed, per the lane's REA rule.

## 8. Artifacts (under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ScoutPinDrift/`)

| file | sha256 |
|---|---|
| `out/receipts.txt` | `59dc5025f919f6546de488a32778fee81fc0c8ce04c6b6006299111375f6e42d` |
| `out/changed-files.txt` | `d5b1e7dd34f68f72e1314f2e746c7e7cb3ed2da1b4d1f6e3d4f95f137ad51c8f` |
| `out/diff-dirs.txt` | `d7f99ffe0fe32dee1fecf0a6041498faf5736dbbac75b285a18ddfc568ac601e` |
| `out/diff-files.txt` | `b697d698fcccd6c55e97594562bbc4fb5a2da816999ab3bb0633e5ddcfd90871` |
| `out/diff-sqlite-failures.txt` | `bfe456c4832531863148dd71dc5bcbb923e087e9e84426c54e3e52ea86020fc1` |
| `out/diff-sqlite-inspection.txt` | `f5cb18e7dbb8cac0919b5ddaead24026152ebe639f14d0976c50d9ad78cf082e` |
| `out/diff-sqlite-snapshot.txt` | `b13805fa2ae5f1f83fc6aae2866b26b3a407be0aabac5e7790aa3e910317280e` |
| `out/diff-sqlite-worker-exec.txt` | `31f6a64750404450b253418fdb148a19dcca0d0e519eac34ee40ca63528ac556` |
| `out/diff-domain-sqliteDatabase.txt` | `a286011af987897785a33534f3e9c4a6d10c0b2695a7cb93225bd439e68a0a66` |
| `out/check_columns_equiv.py` | `bf3b6b87019969919a4c4b1bd9e1f36a70c403bfc20a63b7af33950788ae8e78` |
| `out/columns-equiv.txt` | `3f9df576f1c83e4ae6c810fb941bd3905de4664326add331f3b723b2a8274e1c` |
| `out/SHA256SUMS` | `c5ee3f8131fac9d041f04be6e2639da0200df0c702942fca7a8da19745f122b9` (manifest of the rows above) |

No tools were installed or updated for this item.
