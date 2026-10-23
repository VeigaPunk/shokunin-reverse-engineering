# ReDeriveProjB — independent re-derivation of committed C1 envelopes proj-361 / proj-370

Seat: `KaidokuR31.ReDeriveProjB` (round 31, wave 2, fresh falsify wave).
Verdict per carrier: **HOLDS** — each committed envelope equals an independent re-derivation
of the carrier file's schema, field by field, with **0 mismatches**.

Attack target: the claim that envelope `data.normalized_result` is a faithful record of the
actual SQLite schema of the frozen carrier file (R31-C1, P1-pass predicate). Re-derived the
schema from the file itself with readers that are NOT the lane oracle
`tools/round-31/sqlite_oracle.py`; no REA invocation anywhere.

## Readers used
- **A — Python stdlib `sqlite3` 3.54.0** (Python 3.14.8), connection
  `sqlite3.connect("file:<path>?mode=ro&immutable=1", uri=True)`, queries:
  `SELECT type,name,tbl_name,rootpage,sql FROM sqlite_schema` (natural order),
  `PRAGMA table_list`, `PRAGMA table_xinfo("<table>")` per table.
- **B — `sqlite3` CLI 3.54.0**: `sqlite3 -readonly -json "file:<path>?immutable=1" <sql>`.
Both readers exist on PATH; no tool installs were made this seat (no pacman/npm/uv actions).

## Commands (all under `timeout`, none > 120s; UTC 2026-10-23)
1. `timeout 300 python3 -I -B .../rederive.py <carrier> <envelope> <frozen_sha256> <frozen_bytes>` — exit 0 both carriers.
2. `timeout 300 python3 -I -B .../cli_crosscheck.py <carrier> <envelope>` — exit 0 both carriers.
3. `timeout 120 sqlite3 -readonly -json "file:...?immutable=1" "SELECT type,name,tbl_name,rootpage,sql FROM sqlite_schema ORDER BY rowid"` — exit 0 (raw CLI dump, artifact `cli_schema_361.json`).

## Per-carrier results

### proj-361 (`/fast/scratch/hyaku/kaidoku-r31/carriers/proj-361.db`)
- Fingerprint recomputed: sha256 `79b660eb3c09f50c0f251e958db7cbf9a2d5d18d2836e99082095b31c7e029c5`, bytes 8,581,120 — equals `subject.digest.sha256`, `artifact.sha256`, `artifact.bytes` and frozen `carriers.tsv` row.
- evidence_id in envelope: `ev_64b5feb7dadec43ad7eeb4f1972a845e697a36615ee6b505fa8f60e980349350`.
- Derived counts: tables 36, indexes 21, views 7, triggers 35; columns 385 (incl. `sqlite_stat1`; 5 autoindexes with `sql: null`).
- Fields compared (reader A): all 36 table entries (name, sql, root_page, kind, without_rowid, strict, column_count, columns_completeness, full column list of cid/name/declared_type/not_null/default_sql/primary_key_position/hidden — 385 columns), all 21 index entries (name, table, sql, root_page), all 7 views (name, sql), all 35 triggers (name, table, sql), plus artifact/wal/engine name/database_encoding/schema scope+completeness. Excluded per predicate P1-pass: `engine.version` and `limitations` (and `meta`).
- **Mismatches: 0** (exact JSON paths — none; `mismatches: []`).
- Cross-reader B: CLI `sqlite_schema` has exactly 99 rows; grouped by type, all 99 row-tuples equal the envelope's, including byte-identical `sql` text (longest trigger 128,117 chars). `PRAGMA table_list` kinds agree on every shared table name (all `table`); the only CLI-only entries are the 7 views and `sqlite_schema`/`sqlite_temp_schema`, which the envelope carries separately — not a discrepancy.
- Knowledge doc `corpus/knowledge/2026-10-23-r31-sqlite-positive.md`, Carriers row proj-361: evidence_id, sha prefix `79b660eb3c09`, bytes, 36/21/7/35, 385 columns, verdict P1-pass — all match.

### proj-370 (`/fast/scratch/hyaku/kaidoku-r31/carriers/proj-370.db`)
- Fingerprint recomputed: sha256 `976d427f037791c88b8d051a452e1fb13157c1c14b6e56d5a868097a4813cb7e`, bytes 9,154,560 — equals `subject.digest.sha256`, `artifact.sha256`, `artifact.bytes` and frozen `carriers.tsv` row.
- evidence_id in envelope: `ev_4bd51490c5d690a628d39e9217a635985d57fea0a7d5d65d2f8c2a5253d526da`.
- Derived counts: tables 37, indexes 21, views 7, triggers 36; columns 395.
- Same field set compared; **Mismatches: 0** (`mismatches: []`).
- Cross-reader B: CLI `sqlite_schema` has exactly 101 rows; all grouped row-tuples equal the envelope's; kinds agree on shared names.
- Knowledge doc row proj-370: evidence_id, sha prefix `976d427f0377`, bytes, 37/21/7/36, 395 columns, verdict P1-pass — all match.

## Tools / environment
- `python3` 3.14.8, `sqlite3` 3.54.0 (CLI and Python module), host Linux 7.2.11 arch1-1 (x64). No installs performed (recorded per operator tooling directive).
- Carrier files opened strictly read-only (`mode=ro&immutable=1`); no writes to carriers, lane, fleet repo, or git/jj state. No subagents spawned (leaf).

## Residual risk / verification gaps
- [INFERENCE] Both independent readers share the same system libsqlite3 3.54.0 catalog; a library-level bug shared by 3.54.0 and REA's 3.53.4 would pass unseen (same limit acknowledged in the knowledge doc). This seat did not byte-parse the file with a pure parser; that is the oracle's role and was deliberately avoided here.
- This seat ran no live REA counter; envelope-vs-independent-reader equality is what was re-derived. Live-run freshness remains C1 counter/L1 scope.
- Ordering equality is established under the envelope's type-grouped ordering; the CLI's rowid-interleaved order preserves the same relative order within each type.

## Artifacts (scratch `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveProjB/`)
| file | sha256 | purpose |
|---|---|---|
| `rederive.py` | `8b51eb523227b504da9644c27c277cbbd6dea345d5493aef9d074b65c430b6ba` | reader A + envelope diff |
| `cli_crosscheck.py` | `217cc4d199c1cf00be688e7aeba51dea021ebdfec92cae4fdf5c0dbceeca3547` | reader B cross-check |
| `cli_schema_361.json` | `afe580982d10de83382e7f709ecc67bcc3c98a209d36bc231ce97f20909e906b` | raw CLI dump (proj-361) |
