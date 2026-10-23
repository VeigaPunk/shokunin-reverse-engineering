# W2 seat ReDeriveProjChinook — independent re-derivation of C1 envelopes (proj-371, chinook)

Seat: `KaidokuR31.ReDeriveProjChinook` (leaf; no subagents).
Attacks: the committed C1 envelopes `corpus/evidence/round-31/c1/envelopes/proj-371.json` and `chinook.json` (P1-pass records).
Verdict: **holds** for both carriers — an independent reader (system libsqlite3 3.54.0 via Python `sqlite3`, no lane oracle `tools/round-31/sqlite_oracle.py`) reproduces every compared field of `data.normalized_result` with **0 mismatches** per carrier, and each `evidence_id` is named in `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` with matching T/I/V/Tr and column counts.

## Method

Independent reader (seat artifact `indep_reader.py`): opens each carrier `file:<path>?mode=ro&immutable=1` with the system libsqlite3 and reads
- `sqlite_schema` (`type,name,tbl_name,rootpage,sql`) ordered by `rowid` → tables, indexes, views, triggers;
- `PRAGMA main.table_list` → kind (`table`), `ncol`, `wr`, `strict`;
- `PRAGMA main.table_xinfo(<name>)` per non-virtual table → `cid,name,type,notnull,dflt_value,pk,hidden`;
- SQLite file header bytes 56–59 (4-byte big-endian text-encoding field) → `database_encoding`;
- `sha256`/byte count of the file → `artifact`.

This shares no code with the lane oracle, whose `sqlite_schema` rows come from a pure-Python b-tree byte parser; kinds/flags/columns here come from the system SQLite build (different from REA's bundled node SQLite 3.53.4 and from the oracle's byte parser). No tools were installed (system `python3` 3.14.8 with `sqlite3` 3.54.0; `sqlite3` CLI 3.54.0 present) — no installs to record.

Comparison (`compare.py`): recursive field-by-field diff of the envelope `data.normalized_result` vs the independent report at exact JSON paths, per the P1 normalization (skip `engine.version` and `limitations`, REA-owned fields; compare `engine.name`).

## Results

| carrier | tables | indexes | views | triggers | columns | mismatches | exit |
|---|---:|---:|---:|---:|---:|---:|---|
| proj-371 | 38 | 21 | 7 | 36 | 396 | 0 | 0 |
| chinook | 11 | 11 | 0 | 0 | 64 | 0 | 0 |

Compared fields (each table object): `name`, `sql`, `root_page`, `kind`, `without_rowid`, `strict`, `column_count`, `columns_completeness`, `columns[]` with `cid,name,declared_type,not_null,default_sql,primary_key_position,hidden`; each index: `name,table,sql,root_page`; each view: `name,sql`; each trigger: `name,table,sql`; plus `artifact{path,sha256,bytes}`, `wal`, `database_encoding`, `rows`. The long PROJ trigger SQL (up to ~128 KB) round-trips byte-exact (covered by the full-string diff).

Commands (all `timeout`-capped, exits recorded):
```
python3 -I -B indep_reader.py /fast/scratch/hyaku/kaidoku-r31/carriers/proj-371.db ind_proj371.json   # exit 0
python3 -I -B indep_reader.py /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite ind_chinook.json # exit 0
python3 -I -B compare.py …/envelopes/proj-371.json ind_proj371.json  # "mismatches: 0", exit 0
python3 -I -B compare.py …/envelopes/chinook.json ind_chinook.json    # "mismatches: 0", exit 0
```
Run time: 2026-10-23T04:31:54Z (final comparison pass; earlier runs at 04:31Z with identical results after a header-offset fix in the reader).

Cross-checks:
- `subject.digest.sha256` == `artifact.sha256` == freshly computed file sha256 (`a25d85a2ebfc…` / `bdf635be6985…`), bytes match (9261056 / 1067008); no `-wal`/`-journal` sidecars in the carrier dir → `wal: null` consistent.
- Knowledge entry names both ids with matching counts: line 21 proj-371 `ev_4a9d1724322141214d9678dcb36a5075036b6eee9b75c46996e045aca21a495f` 38/21/7/36, 396 cols; line 22 chinook `ev_fe9589c14b3445f946d1b213dd9915b44e67101a000ec14a92c5fb2fff303d52` 11/11/0/0, 64 cols.

## Limits of this re-derivation

- Same SQLite catalog (3.54.0) for kinds/columns as the oracle's PRAGMA reader; independent of the oracle's byte parser but not of libsqlite3. A catalog bug common to 3.53.4/3.54.0 would pass unseen (known limit, same as the round's).
- `columns_completeness: "complete"` is asserted for non-virtual tables (matches); virtual/shadow kinds are not exercised by these two carriers.

## Seat artifacts (`/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveProjChinook/`)

| file | sha256 |
|---|---|
| indep_reader.py | `314ae16a7654855a576be68f5b1e448103270bdc9758c1d518448ee83a04c078` |
| compare.py | `de958d85da4786f8ce3b5ace101715520b9bb20b1b835977bca7836a0b6a19f6` |
| ind_proj371.json | `8a5004aff4fa2c7fbfeaadb16ecce87d7dee2c33cd303dd814499c6c2bc20b7e` |
| ind_chinook.json | `37a5597e8703a7c560cdccbb55a23caacd1ef63431a8fda8f274f39908665e88` |
| tmp/ | (empty scratch dir) |
