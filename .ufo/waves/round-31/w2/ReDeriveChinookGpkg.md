# Round 31 C1: independent re-derivation — Chinook AutoIncrement and GeoPackage Curve

**Verdict — observation:** both committed envelopes agree field-for-field with an independent `sqlite3` reader for the requested schema, and their digest/size and knowledge-table entries agree. No in-scope discrepancy found.

## Reader and comparison

I used system Python 3.14.8's `sqlite3` module (SQLite 3.54.0), opening each carrier with `mode=ro&immutable=1`; no imports or calls to `tools/round-31/sqlite_oracle.py`. `derive_catalog.py` independently queried `sqlite_master` (including stored SQL and root pages), `PRAGMA table_list`, `PRAGMA table_xinfo` (all non-virtual tables), and `PRAGMA encoding`. A read-only SQLite CLI check also queried `sqlite_master`, `table_list`, and encoding. The recursive comparison checks field types, keys, values, and list order.

Compared `normalized_result.schema` fields: scope/completeness; every table's name, SQL, root page, kind, `without_rowid`, `strict`, column count/completeness, and every column's cid/name/type/not-null/default/pk-position/hidden; every index's name/table/SQL/root page; and every view/trigger's name/table/SQL. Also checked normalized database encoding, subject local path and digest, and artifact path, SHA-256, and byte count against the carrier file.

## Results

| Carrier | Reader-derived schema | Mismatch paths | File identity vs envelope | Knowledge Carriers row |
|---|---|---|---|---|
| `chinook-autoinc` (`/fast/scratch/hyaku/kaidoku-r31/carriers/chinook-autoinc.sqlite`) | 12 tables, 11 indexes, 0 views, 0 triggers; 66 non-virtual-table columns | **0** | SHA-256 `ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4`; 1,067,008 bytes — both match | ID `ev_979cf0eb91af644ab3e6033917ccead5a4684dd71127d070346c085d94b92cce`; T/I/V/Tr `12/11/0/0` — match |
| `gpkg-curve` (`/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curve.gpkg`) | 13 tables (9 `table`, 3 `shadow`, 1 `virtual`), 8 indexes, 0 views, 18 triggers; 53 non-virtual-table columns | **0** | SHA-256 `03a9c5904fd3075c61ba96e5bf0aac381721d43799db23c06634a0c56e04f302`; 98,304 bytes — both match | ID `ev_4e5aa3c972f950b6e84a5ec33b123e7fdc896064db38809b035b7009eabac35f`; T/I/V/Tr `13/8/0/18` — match |

For the virtual R*Tree table, `table_list` reports kind `virtual`, column count 5; the envelope and independent derivation both report `columns_completeness: unsupported` and an empty column list. The three R*Tree shadow tables have complete `table_xinfo` columns.

## Evidence and commands

All commands below were run read-only and individually capped with `timeout` (30 or 120 seconds). UTC time for the final check batch: **2026-10-23T04:37:27Z** (start and end). Exit codes are from the command output.

1. **Independent extraction:** `timeout 120 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveChinookGpkg/derive_catalog.py` — exit **0**. Exact output:
   ```text
   chinook-autoinc tables=12 indexes=11 views=0 triggers=0 realcols=66
   gpkg-curve tables=13 indexes=8 views=0 triggers=18 realcols=53
   ```
2. **Field comparison and file checks:** `timeout 120 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveChinookGpkg/cmp_envelopes.py` — exit **0**. Exact output:
   ```text
   === chinook-autoinc ===
   0 mismatches on normalized_result.schema + database_encoding + subject/artifact path + artifact bytes + sha256
   counts T=12 I=11 V=0 Tr=0 realcols=66
   === gpkg-curve ===
   0 mismatches on normalized_result.schema + database_encoding + subject/artifact path + artifact bytes + sha256
   counts T=13 I=8 V=0 Tr=18 realcols=53
   carriers_with_mismatches=0
   ```
   Thus there are no differing JSON paths in the compared fields for either carrier.
3. **CLI cross-check:** for each `$f` in the two carrier paths, `timeout 30 sqlite3 -readonly "file:$f?immutable=1" "select count(*) from sqlite_master where type='table'; pragma encoding; pragma table_list;"` — exit **0** for both. It returned counts 12 / 13 and `UTF-8` / `UTF-8`; `table_list` independently showed the GeoPackage's virtual and shadow kinds.
4. **File size and digest:** `timeout 30 sha256sum <both carrier paths>` and `timeout 30 stat -c '%n %s' <both carrier paths>` — each exit **0**. Output:
   ```text
   ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4  .../chinook-autoinc.sqlite
   03a9c5904fd3075c61ba96e5bf0aac381721d43799db23c06634a0c56e04f302  .../gpkg-curve.gpkg
   .../chinook-autoinc.sqlite 1067008
   .../gpkg-curve.gpkg 98304
   ```
5. **Knowledge table:** `timeout 120 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveChinookGpkg/check_knowledge.py` — exit **0**. It printed both exact Carriers rows, with the evidence IDs and counts shown above, then `knowledge_rows=2 counts_and_ids_match`.
6. **Envelope provenance:** at the same UTC time, read-only `git show f368a101:<envelope path> | sha256sum` and `sha256sum <working-tree envelope>` matched for each envelope; all four commands exited **0**. The matching envelope hashes are `bf8229cc55413c4eb044d3ca511c2e814add4c705d294c654abd176255954d34` (Chinook) and `c74b7a3a5a0dd64b66b609a163e354d8b1bf5efa9e72bb7633405f757b1cffb4` (GeoPackage).

An earlier optional CLI probe had an SQL quoting typo (`type="table"`) and exited 1; it only read the file and made no changes. The corrected, timeout-capped command above exited 0. Final results rely on the corrected run and successful Python derivation/comparison.

## Residual risk / verification gap

**Inference:** this independently checks the envelopes against system SQLite 3.54.0 and is not an independent implementation of SQLite itself; the API-derived kind/column metadata could still share an upstream SQLite defect. The assignment is limited to these two carriers. No external source was opened, no tool was installed, no REA run was made, and no lane file other than this report was written.

## Scratch artifacts and SHA-256

All artifacts are under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveChinookGpkg/`:

- `check_knowledge.py` — `797d99b04015478b12db9a5f679ce2c35557f49bdd4def37366c32f2b5e61bdb`
- `cmp_envelopes.py` — `d2f41bb73f5891125fb8d516168ddd6588a4023fb9bd2bc42e6c5918e011d27e`
- `derive_catalog.py` — `7aa84856e0b0919bacd9f1d0af0846157725284e7100f7966a536d30172b48fc`
- `derived_gpkg-curve.json` — `efe9070cf4b8b5e09333308d05b327f0a9af823d6c98ac73dca211bfac3b3720`
- `derived_chinook-autoinc.json` — `00b7139767016d4d166979dd782771f8de961cf7587b7be7b468ea2f74a740bf`
- `shape_dump.py` — `7ae47a46e1b60da34eddbdfc12042907efe48b891ebdb412dee9a67306d8d1e1`
- `gpkg-curve.pretty.json` — `ffad42bda944ccfb3c75fcb10c3e8397b224259046850c78f438783619703c14`
- `chinook-autoinc.pretty.json` — `c377d9eb2b3805995ba80778937e3df7984a2fa15c7e63f60d7943c33d6d96a1`
- `dump_env.py` — `1272d3df5cbec1e8a210a149bc7dd74caea253b0daee4208ec49f4ddc0d16358`

Report: .ufo/waves/round-31/w2/ReDeriveChinookGpkg.md
