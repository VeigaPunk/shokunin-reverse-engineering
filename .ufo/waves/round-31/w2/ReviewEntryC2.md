# ReviewEntryC2 — R31 C2 knowledge entry

## Findings by severity

### Low — prior-history statement is too broad

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md:9` says the lane's “only prior knowledge” was the 2026-10-16 L7 entry. The base-tree L8 entry also records the operation name and a prior call attempt: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:12` says `inspect_sqlite_database` returned `{"code":-32602,"message":"Tool <name> not found"}` at REA 6.4.0.

**Evidence (observation):** command `git show c369242fee9f559f895e3f7956b1242076c7b1be:corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md`; exit 0; 2026-10-23T04:37:23Z. Exact excerpt: `inspect_sqlite_database (L6) ... each returned {"code":-32602,"message":"Tool <name> not found"}`. The entry's line 9 was also read successfully during 2026-10-23T04:37:03Z–04:37:11Z.

This prior 6.4.0 refusal does not establish 6.5.0 SQLite behavior or undermine the new refusal signatures, but it makes “only prior knowledge” unqualified and inaccurate. Consider narrowing it to “only prior successful SQLite inventory result” and cite the 6.4.0 tool-name refusal as prior history.

### Low — stage-summary pointers do not cover all named mechanics

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md:43` cites `sqliteDatabase.js:44-61` for the input schema but not the separate projection that turns custom issues into `invalid_value`. Its snapshot citations (`SqliteDatabaseSnapshot.js:106-121` and `readStableArtifact.js:31-35`) likewise do not cover the `ENOTDIR` branch named in that sentence.

**Evidence (observation):** direct `read` of the installed 6.5.0 source files, successful (the read device has no numeric process exit status), during 2026-10-23T04:37:03Z–04:37:11Z:
- `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseSnapshot.js:18-20`: only `ENOENT` becomes `null`; other errors are rethrown.
- `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseFailures.js:78-85`: `ENOENT`/`ENOTDIR` is mapped to `path:["path"]`, `reason:"invalid_value"`.
- `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/inputIssueProjection.js:66-72`: custom issue projection sets `path`, `reason:"invalid_value"`, and the message.

The stage ordering and conclusions are consistent with the source; add those precise pointers so the summary itself backs its `ENOTDIR` and projection clauses. The row-level pointers elsewhere in the entry already include `inputIssueProjection.js` for the three option-dependency predictions.

### Low — 6.7.0 “code paths unchanged” overstates the static comparison

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md:50` says “The other 21 rows' code paths are unchanged.” The 6.7.0 implementation changes a code path used by non-budget rows: `SqliteDatabaseInspection.js:123-153` replaces the 6.5.0 `PRAGMA main.table_xinfo(...)` reader with `temp.pragma_table_xinfo`, BLOB casts, explicit decoding, and sorting; `readSchema` calls `readColumns` for the selected ordinary table at lines 263-271. Thus `q-ok-rows` and `q-missing-column` enter changed implementation, even if the frozen inputs' compared fields remain the same. The entry correctly labels this as static and says no live 6.7.0 run occurred; describe the other 21 as predictions whose compared fields showed no identified drift, not as unchanged code paths.

**Evidence (observation):** direct `read` of both installed pins, successful (no numeric process exit status exposed), during 2026-10-23T04:37:03Z–04:37:11Z. 6.5.0 excerpt at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseInspection.js:126-142`: `PRAGMA main.table_xinfo(...)`, string column fields, direct return. 6.7.0 excerpt at `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/sqlite/SqliteDatabaseInspection.js:131-153`: `temp.pragma_table_xinfo`, BLOB casts, `decodeSchemaText`, and `columns.sort(...)`; call site lines 263-271 invokes this for a selected table. No live 6.7.0 REA run was performed.

## Checks with no finding

- The three-stage order is supported by 6.5.0: option refinement at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/sqlite/sqliteDatabase.js:44-61`; missing database, journal, budget, and snapshot acquisition at `.../sqlite/SqliteDatabaseSnapshot.js:106-121`; regular-file validation at `.../artifacts/readStableArtifact.js:31-35`; worker handling follows the snapshot. The pointer-coverage issue above is not an outcome contradiction.
- The correction at entry line 60 is accurate: read-only `stat` output was `db.sqlite 1067008`, `db.sqlite-wal 267368449`; sum `268435457`. The pointer-review counts and adjacent ENOTDIR citation at line 61 agree with `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/w1/ReviewPointers.md:71-97`.
- Shared-message claims at entry line 55 are consistent with the 23 prediction rows. Direct envelope comparison returned `equal outside meta: True` for `m-not-sqlite` and `m-bad-pagesize`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/w1/CtlC2ShortcutIds.md:111-122` records the rotated control's `matches=1` result.
- All 23 frozen IDs appear in the entry's decision table and predictions file. The accepted evidence IDs shown in the entry match the committed envelopes; `runs.tsv` records 23 live 6.5.0 calls in the stated interval.

## Residual risk and verification gaps

- The static 6.7.0 review is not a live compatibility test; no 6.7.0 invocation was made. The finding above concerns the too-strong “code paths unchanged” wording, not a demonstrated wrong result for the frozen 6.5.0 claim.
- No `lsp` device/server was available in this session; conclusions above use direct reads of the installed code and committed artifacts, not grep as semantic proof.
- No tools were installed or updated.

## Scratch artifacts

- `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReviewEntryC2/pin-diff-6.5-6.7.txt` — SHA-256 `8753039c6bec5af4188eea0596928739c1989453bc07067cd54d12578964ee06`.
