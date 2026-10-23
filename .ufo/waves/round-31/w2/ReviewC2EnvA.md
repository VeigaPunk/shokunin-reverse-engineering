# ReviewC2EnvA — C2 rows q-rowlimit-no-table / q-columns-no-table / q-scope-no-table / q-missing-table / q-case-table / q-view-as-table

Reviewer: KaidokuR31.ReviewC2EnvA. UTC: 2026-10-23T04:31:33Z.

Scope: committed envelope vs frozen prediction (`corpus/evidence/round-31/c2/predictions.tsv`) vs SKILL.md `## SQLite databases (`inspect-sqlite-database`) — round 31` (lines 1014–1019) vs entry `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` (table rows 17–22), plus stage/code-line claims against the installed `rea-agents@6.5.0` dist (`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist`, read-only).

## Verdict

All six rows **HOLD**. No field mismatch, no unsupported wording found in SKILL or the entry for these rows. No failures.

## Per-id verification

Accepted comparison fields: escape (runs.tsv), envelope `ok`, `error.code`, `error.category`, `details.issues` (exact path/reason/message), presence of `details.captured_output`, prediction outcome/exit/code/issue_path/issue_reason/message, SKILL row, entry row.

| id | verdict | exact fields checked |
|---|---|---|
| q-rowlimit-no-table | holds | envelope: `ok:false`, `code:invalid_request`, `category:invalid_input`, issues `[{"path":["row_limit"],"reason":"invalid_value","message":"row_limit requires an explicit table selection"}]`, one entry, NO captured_output. Prediction row 2: refuse / exit 1 / invalid_request / ["row_limit"] / invalid_value / same message. runs.tsv exit 1, verdict P2-match. SKILL 1014 and entry row 17 identical. Stage snapshot/input (entry) — consistent with no captured_output and source 2ms. |
| q-columns-no-table | holds | Same shape; issues `[{"path":["columns"],"reason":"invalid_value","message":"columns requires an explicit table selection"}]`, no captured_output. Prediction row 3 matches. SKILL 1015, entry row 18 match. Stage snapshot/input. |
| q-scope-no-table | holds | Same shape; issues `[{"path":["schema_scope"],"reason":"invalid_value","message":"selected_table schema scope requires table"}]`, no captured_output. Prediction row 4 matches. SKILL 1016, entry row 19 match. Stage snapshot/input. |
| q-missing-table | holds | issues `[{"path":["table"],"reason":"invalid_format","message":"Selected ordinary table does not exist with that exact name: NoSuchTable"}]`; `captured_output` present `{"stdout":"","stderr":"","truncated":false}`. Prediction row 5 matches. SKILL 1017, entry row 20 match. Stage worker (entry) — captured_output present, consistent. |
| q-case-table | holds | issues `[{"path":["table"],"reason":"invalid_format","message":"Selected ordinary table does not exist with that exact name: album"}]`; captured_output present. Prediction row 6 matches (code_pointer note "exact-name map, no case folding"). SKILL 1018, entry row 21 match (table is `Album`, exact-name lookup, no case folding). Stage worker. |
| q-view-as-table | holds | issues `[{"path":["table"],"reason":"invalid_format","message":"Selected ordinary table does not exist with that exact name: coordinate_operation_view"}]`; captured_output present. Prediction row 7 matches (code_pointer note "a view row sets no selectedTable"). SKILL 1019, entry row 22 match (a view, proj-371). Stage worker. |

Acceptances: none of the six rows is an acceptance, so the evidence_id / subject-sha check is N/A for this set (applies to q-ok-rows, m-journal-empty, m-journal-zero28, out of scope here).

## Carrier facts (grounding the messages)

- `sqlite3 -readonly /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite "SELECT type,name FROM sqlite_master WHERE name IN ('Album','album','NoSuchTable')"` → exactly `table  Album` (exit 0). Supports: `album` refusal (exact-name, no case folding) and `NoSuchTable` absence.
- `sqlite3 -readonly /fast/scratch/hyaku/kaidoku-r31/carriers/proj-371.db "SELECT type,name FROM sqlite_master WHERE name='coordinate_operation_view'"` → `view  coordinate_operation_view` (exit 0). Supports the view-as-table wording.

## Stage/code-line claims verified against dist (read-only)

- `dist/domain/sqlite/sqliteDatabase.js:44-61` — exact three superRefine checks: row_limit (44–49), columns (50–55), schema_scope (56–61); each `code:"custom"`, path on the option's own path, message identical to envelope.
- `dist/domain/inputIssueProjection.js:66-72` — fallback branch projects a `custom` issue to `{path, reason:"invalid_value", message}`; exactly matches the projected `details.issues` entries.
- `dist/sqlite/SqliteDatabaseInspection.js:74` — `missingSelectedTable` definition, message template identical (`Selected ordinary table does not exist with that exact name: ${name}`).
- `SqliteDatabaseInspection.js:155-160` — `PRAGMA main.table_list` metadata map keyed by stored exact name (no folding); `:187-189` — `metadata.get(selectedName)` exact lookup, `undefined` → throw. Explains q-case-table.
- `SqliteDatabaseInspection.js:224-280` — table/index/view branches; the view branch (278–285) pushes to `schema.views` and never sets `selectedTable` (the cited range contains the construct; the parenthetical states the fact precisely). `:299-303` — `readRows` throws `missingSelectedTable(input.table)` when `selectedTable` is undefined, giving the view the identical missing-table message. Confirms q-view-as-table path (no earlier view rejection: `inspectSqliteDatabaseSnapshot` at 405–414 calls `readSchema` then `readRows` directly).
- `dist/sqlite/SqliteDatabaseWorkerExecution.js:31-58` — `rejectedReply` maps worker reason `selection` → path `["table"]`, `reason:"invalid_format"`, message from the worker reply, and attaches `capturedOutput` to the `AnalysisInputError`. Confirms the worker rows' `captured_output` presence and field shape.

## Non-failing observations

- Pointer precision: q-view-as-table's code_pointer cites `224-280` where the view branch itself is 278–285; the parenthetical disambiguates. Same class the wave-1 pointer review (36 pointers) already accepted as "contains the construct among other lines"; not a defect.
- Durations in envelope `meta` (excluded from the committed comparison): schema-stage rows 2ms vs worker rows 123–211ms, corroborating the entry's "refused before any SQLite open" vs worker split.
- Entry line 13's rule "worker rows carry `details.captured_output`; the others are refused before any SQLite open" holds for all six (captured_output present exactly on the three worker rows).
- Entry line 44's "the view is listed, but no table entry is built for it" matches the code (view branch builds no table record).

## Evidence commands

- Reads: envelope JSON for all six ids (`read`); predictions.tsv rows 2–7 / runs.tsv rows 2–7 (grep); SKILL.md 1008–1045; entry file full; dist files/ranges listed above. All local file reads, exit 0, 2026-10-23T04:19–04:31Z.
- Carrier probes: the two `sqlite3 -readonly` queries above, exit 0, 2026-10-23T04:31Z.
- No REA run performed (none needed; L1 measured C2 `requests=23 matches=23 exit 0` at 0007731e, unchanged).

## Artifacts / installs

- No scripts, drafts or raw outputs produced; no files written outside this report. No tool installs (sqlite3 preinstalled at /usr/bin/sqlite3; reads only).
