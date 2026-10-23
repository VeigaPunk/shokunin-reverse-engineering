# W2 ReDeriveProjA — independent re-derivation of committed C1 envelopes: proj-341, proj-350

Seat: `KaidokuR31.ReDeriveProjA` (leaf — no subagents spawned). Date: 2026-10-23.
Attack target: the committed C1 envelopes for carriers **proj-341** and **proj-350** — re-derived from the shipped carrier files with a reader that is **not** `tools/round-31/sqlite_oracle.py`, compared field by field against `data.normalized_result`, plus byte identity and the knowledge-ledger row.

## Verdict

| Carrier | Verdict |
|---|---|
| proj-341 | **holds** — 0 mismatches across all assigned fields |
| proj-350 | **holds** — 0 mismatches across all assigned fields |

No actionable finding against the envelopes, the carriers, or the knowledge-ledger rows for these two carriers.

## Reader and method

- Primary reader: `sqlite3` CLI 3.54.0 (pre-existing at `/usr/bin/sqlite3`; not installed by me), opened `-readonly "file:<path>?immutable=1"`. No tool installs were performed.
- Second reader for counts/encoding: Python 3.14.8 `sqlite3` module (libsqlite3 3.54.0), URI `mode=ro`+`immutable=1`, my own `SELECT count(*) … FROM sqlite_schema` queries.
- Derivation is my own code (`rederive.py`, sha256 below): `SELECT type,name,tbl_name,rootpage,sql FROM sqlite_schema ORDER BY rowid` + `PRAGMA table_list` (ncol, wr, strict) + `PRAGMA table_xinfo(<table>)` per table. Not a byte-parser, not the lane oracle; carriers untouched (chattr +i respected; `-readonly` + `immutable=1`).
- Comparison is keyed by name, field by field, all objects; the committed envelope's real column keys are `cid, name, declared_type, not_null, default_sql, primary_key_position, hidden` (the item brief's `type/notnull/default/pk` names do not appear in the committed envelopes — I compared the actual committed keys). `columns_completeness` is an envelope-only claim, not derivable; excluded from the leaf count and assessed qualitatively (backed: full column set matches, `column_count == ncol == len(columns)` for all 36 tables).
- Note: committed `schema.tables` includes `sqlite_stat1` (36 = 35 non-internal + 1). Verified real: my CLI reader sees it in the shipped file at root page 57. Indexes (21) include the 8 `sqlite_autoindex_*` rows with `sql: null`, as the knowledge doc describes.

## Per-carrier results

Commands (both carriers, run 2026-10-23T04:36:20Z, batch completed at that timestamp):

```
python3 rederive.py proj-341 /fast/scratch/hyaku/kaidoku-r31/carriers/proj-341.db \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/envelopes/proj-341.json
python3 rederive.py proj-350 /fast/scratch/hyaku/kaidoku-r31/carriers/proj-350.db \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/envelopes/proj-350.json
```

Both: **exit 0**, stdout ends `MISMATCHES: 0` (full stdout in artifacts below).

### proj-341 — observation
- Bytes/sha256: file = 8,278,016 bytes, sha256 `97a04533b1e7e3bfea9be2e11cc4e43a60539020d8cdd02622203d82db4c2414` — equals `subject.digest.sha256`, `normalized_result.artifact.sha256`, and `carriers.tsv`. `artifact.bytes` = 8,278,016 ✓. No `-wal`/`-shm`/`-journal` sidecars (matches `wal: null`).
- Encoding: derived `UTF-8` = envelope `UTF-8` ✓.
- Fields compared: **3,152** leaf envelope fields = 36 tables × 7 (name, sql, root_page, kind, without_rowid, strict, column_count) + 385 columns × 7 (cid, name, declared_type, not_null, default_sql, primary_key_position, hidden) + 21 indexes × 4 (name, table, sql, root_page) + 7 views × 2 (name, sql) + 35 triggers × 3 (name, table, sql) + 2 (artifact.bytes, database_encoding). **Mismatches: 0** (exact JSON-path list empty).
- T/I/V/Tr: envelope 36/21/7/35 = derived 36/21/7/35. 0 strict tables, 26 without_rowid tables, all `kind: "table"`.
- Entry order equals `sqlite_schema` rowid order for all four collections (observation; order is not a claimed field).
- Second reader (Python sqlite3) agrees: 35 external tables / 21 / 7 / 35, encoding UTF-8.

### proj-350 — observation
- Bytes/sha256: file = 8,495,104 bytes, sha256 `deaa7e9db95ef993358557441d33d26c24e01edb82c82021e8f639cadbb284c2` — equals `subject.digest.sha256`, `normalized_result.artifact.sha256`, `carriers.tsv`. `artifact.bytes` = 8,495,104 ✓. No sidecars.
- Encoding `UTF-8` ✓. Fields compared: **3,152** (same breakdown, 385 columns). **Mismatches: 0**. T/I/V/Tr 36/21/7/35 envelope = derived; 0 strict, 26 without_rowid; order matches rowid order.
- Second reader agrees (35 external tables / 21 / 7 / 35, UTF-8).

### Knowledge-ledger check — observation
`corpus/knowledge/2026-10-23-r31-sqlite-positive.md`, Carriers table, read 2026-10-23T04:36:20Z–04:37:33Z:
- proj-341 row names `ev_52a9b4951d991aeead1fab8ed0374b3d22b5632e7927442f289df8f2ad4d1835` — equals `data.evidence_id`; T/I/V/Tr `36/21/7/35` and columns `385` — equal to both the envelope and my derivation; sha256 prefix `97a04533b1e7` and bytes 8,278,016 — equal to the file I read.
- proj-350 row names `ev_55b3f96bbc31f16782c8bde3ba06acd4646178224bd3e225b9b10e1457ec76aa` — equals `data.evidence_id`; `36/21/7/35`, columns `385`, prefix `deaa7e9db95e`, bytes 8,495,104 — all equal.
- Envelope `evidence_id` values were read from the envelopes themselves (04:35:40Z batch); no fabrication path exists between the three sources.

## Controls (comparator non-vacuity)

- Mutated-copy control, 2026-10-23T04:38:11Z: changed `sqlite_stat1.root_page` 57→58 in a scratch copy of proj-341.json, reran the comparator: **exit 1**, exactly one mismatch: `{"path": "schema.tables[name=sqlite_stat1].root_page", "envelope": 58, "derived": 57}`. The comparison detects real divergence at exact JSON paths.
- Honest harness log (my bugs, not lane evidence): first run 04:35:11Z exited 1 with `sqlite3.OperationalError: no such function: chr` (my second-reader query bug — fixed with a literal `LIKE 'sqlite\_%' ESCAPE '\'`); second run 04:35:40Z reported 1,564 mismatches caused by my wrong assumed column key names — after adapting to the committed keys, final runs 04:36:20Z give the 0 above. No lane file was written at any point.

## Residual risk / verification gaps

- **Shared-libsqlite3 common mode** [INFERENCE, matches the knowledge doc's own Limits]: kind/without_rowid/strict/column fields come from libsqlite3 3.54.0 via two clients (CLI + Python module share the library); the committed envelopes were produced by REA's bundled SQLite 3.53.4. Cross-version agreement is observed (3.54.0 reader = committed 3.53.4-based envelope, field-for-field), but a `table_list`/`table_xinfo` bug common to both would pass. The name/sql/root_page fields are covered by `sqlite_schema` reads only; I did not byte-parse the b-trees (that axis is the lane oracle's).
- `engine.version: "3.53.4"` (envelope) is a claim about REA's runtime, not the file — not testable from the carrier; the doc attributes it to node v24.21.0's bundled SQLite. Untested by me; not in my assigned fields.
- `columns_completeness: "complete"` and `schema.completeness: "complete"` are envelope claims; consistent with my full-set equality (nothing missing), not independently derivable as a claim.
- I covered exactly the two assigned carriers; no statement about the other 10.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveProjA/`)

| File | sha256 |
|---|---|
| `rederive.py` | `e47f6ed52d103d8d97b494cca23c544faad5df322f1e71a7891a53a5c6534b91` |
| `proj-341.out` (final run stdout, exit 0) | `bbf831720749d39966d953f17bf6d6138eccc84b81822de02bd4af008d37d93e` |
| `proj-350.out` (final run stdout, exit 0) | `86f6b549f814fcea3508480a0b421d57542f4698a236265310abacb61fcd6c2c` |
| `proj-341.err` / `proj-350.err` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `proj-341-mutated.json` (control input) | `fc32493ece8767c162766f00860e57f6dc637d636fdf7360dcb03c8d68da43bd` |
| `ctrl-mutated.out` (control stdout, exit 1) | `4a305313a5cb5790bd68d8028c79829627bd09ea37b2580b8c13ce3c6839a4de` |

Lane writes: this report only. No installs. No counter run, no REA invocation, no PIN observed.
