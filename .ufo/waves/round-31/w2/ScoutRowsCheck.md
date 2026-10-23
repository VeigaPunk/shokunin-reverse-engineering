# ScoutRowsCheck — q-ok-rows, deeper: are the 3 Album rows real, and what does REA return for row order and encodings?

Seat: `KaidokuR31.ScoutRowsCheck` (scout, leaf, no subagents). Item: `C2 q-ok-rows` depth check.
Lane base `c369242fee9f559f895e3f7956b1242076c7b1be`; freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`.
Read-only on the lane and on the `chattr +i` carriers; no REA run (the committed envelope and the wave-1
receipt in `runs.tsv` are the live record); no install. All times UTC, 2026-10-23.

## 0. Answer

**Verdict: holds.** The three returned Album rows are real rows of the carrier's `Album` table, and all nine
cells match an independent read-only SQLite read exactly. The returned AlbumIds are **1, 2, 3** and they
**are** the first three rows by rowid — but that is an observed consequence of scanning the table b-tree, not
a guarantee REA makes; REA reports `"order": "unspecified"` and the SQL has no `ORDER BY`. Every text cell is
`{"bytes_hex": <stored bytes>, "encoding": "UTF-8"}`, and for these three rows `bytes_hex` equals the UTF-8
of `value`; the `encoding` field is the **database-level** `PRAGMA encoding` value copied onto every text
cell, not per-cell detection.

Two caveats, both about the check rather than the data:

1. The counter's live q-ok-rows branch is **set membership**: it accepts any three tuples that exist in the
   oracle's 347-row `Album` set (`tools/round-31/c2-sqlite-refusals.py:176-193`). Three copies of one row, or
   rows 100/200/300, would pass that branch. The full-envelope committed rule is what pins the live run to the
   recorded rows 1,2,3, and that record is what I verified here. The frozen predicate sentence is worded
   exactly this way ("each in the oracle's table"), so the claim text is not overstated; a future doc sentence
   like "REA returns the first three rows" would be unbacked by the counter.
2. For q-ok-rows the live branch does **not** compare `artifact.bytes`, `wal`, `engine`, `database_encoding`,
   `indexes`, `views` or `triggers` against the oracle (the parenthetical exemption in the claim sentence).
   Those fields are pinned only live-vs-committed. I checked the material ones independently here: `bytes`
   1067008 and `database_encoding` UTF-8 both match the file.

## 1. Carrier and envelope identity (observation)

Command: `python3 -I -B verify_cells.py` (scratch, sha256 in §7), 04:33:43Z, exit 0:

```
carrier sha256: bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a frozen_match: True bytes: 1067008
envelope sha256: 4e8c69e42d08207875e9fee0e52cc952f1bf99d6678bb9780206c393de8d4a22
rows.order: 'unspecified' row_limit: 3 returned_rows: 3 truncated: True
database_encoding: UTF-8 columns: ['AlbumId', 'Title', 'ArtistId'] table: Album
```

`lsattr /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite` → `----i-----------------` (immutable, read
only). No `-wal`, `-shm` or `-journal` sidecar exists at read time (`art/db_read.txt`, 04:34:10Z). The
envelope's `subject.digest.sha256` equals the file's sha256.

## 2. Per-row and per-cell verdicts

Independent read: `python3 -I -B verify_cells.py` via `sqlite3.connect("file:…?mode=ro&immutable=1")`
+ `sqlite3` CLI 3.54.0 `-readonly …immutable=1` (`art/verify_cells.txt` 04:33:43Z exit 0;
`art/sqlite_cli.txt` 04:33:30Z exit 0). Columns labelled from `rows.columns`.

| row | cell | env type | env value | DB value | verdict |
|---|---|---|---|---|---|
| 1 | AlbumId | integer | `"1"` | `AlbumId=1` (rowid 1) | match |
| 1 | Title | text | `For Those About To Rock We Salute You` | same; `hex(CAST(Title AS BLOB))` = `466f722054686f73652041626f757420546f20526f636b2057652053616c75746520596f75` | match |
| 1 | ArtistId | integer | `"1"` | `ArtistId=1` (Artist `AC/DC`) | match |
| 2 | AlbumId | integer | `"2"` | `AlbumId=2` (rowid 2) | match |
| 2 | Title | text | `Balls to the Wall` | same; hex `42616c6c7320746f207468652057616c6c` (17 bytes) | match |
| 2 | ArtistId | integer | `"2"` | `ArtistId=2` (Artist `Accept`) | match |
| 3 | AlbumId | integer | `"3"` | `AlbumId=3` (rowid 3) | match |
| 3 | Title | text | `Restless and Wild` | same; hex `526573746c65737320616e642057696c64` (17 bytes) | match |
| 3 | ArtistId | integer | `"2"` | `ArtistId=2` (Artist `Accept`) | match |

Per-cell checks that all came back `true` for every text cell (`art/verify_cells.txt`):

- `bytes_hex == hex(CAST(Title AS BLOB))` from the database — **stored bytes, exact**.
- `bytes_hex == value.encode("utf-8").hex()` — **the UTF-8 of the display string equals the stored bytes**.
- `bytes.fromhex(bytes_hex).decode("utf-8") == value` — round-trip.
- `encoding == "UTF-8"` and equals `normalized_result.database_encoding`.
- Titles are 37/17/17 characters = 37/17/17 bytes, pure ASCII, no NUL/control characters, so no replacement
  character or BOM corner exists in this sample.

Integer cells carry only `{type, value}` (no `bytes_hex`/`encoding`); values are decimal strings, which is what
REA's `cell()` emits (`dist/sqlite/SqliteDatabaseInspection.js:96-97`, BigInt → `String(value)`).

Independent confirmation with a **pure-Python b-tree walk** (no SQLite code, `rawscan.py`, 04:33:25Z, exit 0):
it parses page 1 (`sqlite_schema`) itself, finds `Album` root page 19, decodes 12 leaf pages and 347 records:

```
decoded 347 Album rows from b-tree
page of first 3 rows: [(1, 445), (2, 445), (3, 445)]
first 3 in b-tree order: [(1, [None, 'For Those About To Rock We Salute You', 1]), (2, [None, 'Balls to the Wall', 2]), (3, [None, 'Restless and Wild', 2])]
rowids strictly ascending: True
EXACT_MATCH_ORDERED: True
ALL_ROWID_EQ_ALBUMID (record field NULL): True
COUNT: 347
```

Note the `None`: for this rowid table `AlbumId INTEGER PRIMARY KEY` is a **rowid alias**, so the record's first
field is stored as serial type NULL and SQLite materialises the rowid on read. The envelope's integer
`AlbumId` values are therefore the rowids, and they match. `sqlite3` agrees: `count 347`, `minmax rowid
(1, 347)`, join to `Artist` → `AC/DC`, `Accept`, `Accept`.

## 3. Row order: what REA returns

- Envelope: `"order": "unspecified"`, `row_limit: 3`, `returned_rows: 3`, `truncated: true` (true because 347 >
  3; computed by a second `SELECT 1 … LIMIT 1 OFFSET ?`, `SqliteDatabaseInspection.js:353-355`).
- Code (rea-agents **6.5.0**, `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, version and module
  sha256 in `art/rea_version.txt` 04:34:35Z): the row source is
  ``const source = `main.${quoteIdentifier(input.table)} NOT INDEXED`;`` (`:323`) and the read is
  ``db.prepare(`SELECT ${projection} FROM ${source} LIMIT ?`)`` (`:333`) — **no ORDER BY**, and
  `order: "unspecified"` is a hard-coded literal (`:342`). `NOT INDEXED` prevents the `IFK_AlbumArtistId`
  index from changing the scan; `EXPLAIN QUERY PLAN` on the same file yields `SCAN main.Album`
  (`art/db_read.txt` 04:34:10Z).
- Observed: the scan yields b-tree (rowid-ascending) order on this immutable file, so rows 1,2,3 came back
  first and in that order. This answer to "are they the first 3 by rowid" is **yes, by observation**, and
  **not by contract**: SQLite does not promise an order without `ORDER BY`, REA says `unspecified`, and
  `SKILL.md:1023` correctly records `3 Album rows, columns AlbumId, Title, ArtistId; order unspecified`.
  The committed-envelope rule does compare the `values` array order, so any future reordering by a live run
  would still be caught by the counter.
- A byte-level trap worth recording: the carrier contains free pages that retain stale page images. dbstat
  attributes the live `Album` b-tree to pages 19 (internal) plus 12 leaves 319/372/374/376/377/381/383/384/
  445/446/447/448; `freelist_count` is 199 and pages 2 and 55 are owned by no b-tree, yet page 55 is
  **byte-for-byte identical** to live leaf page 445 (1024/1024 bytes, `sha256 28a99b2b…77db83aa`, both
  35-cell table leaves with the three titles at in-page 939/963/987; `art/page55_eq.txt` 04:35:25Z exit 0),
  and page 2 is a stale internal-page image. A `grep` of the file for the titles therefore hits copies outside live
  pages; rows must be established by the b-tree walk (done) or a SQL read, not by byte search. Page 445, a
  live `Album` leaf, does contain the three records.

## 4. Encodings: what REA returns

- `projection` (`:317-322`) encodes text as ``CASE typeof(col) WHEN 'text' THEN 't' || hex(CAST(col AS BLOB))``,
  so `bytes_hex` is lowercased hex of **SQLite's stored text bytes** (`cell()` lowercases at `:109`).
- `cell()` (`:93-122`) decodes with `new TextDecoder(textEncoding(encoding), { ignoreBOM: true }).decode(…)`
  — **non-fatal**, so invalid byte sequences become U+FFFD in `value` while `bytes_hex` keeps the raw bytes;
  and it stamps `encoding` onto the cell (`:120`) from the database-level
  `db.prepare("PRAGMA encoding").get()` (`:395`, emitted as `database_encoding` at `:412`). It is not
  per-cell detection.
- Consequence for this request: `bytes_hex == UTF-8(value)` holds for all three titles *because the bytes are
  valid UTF-8*, not because REA validates them; the envelope's own limitation says so (`normalized_result.
  limitations[4]`: "Text display may replace invalid sequences; bytes_hex and encoding preserve SQLite's text
  byte representation"). BOMs are not dropped (`ignoreBOM: true`), untested here (ASCII).
- Coverage gap (observation, outside the frozen sentence): every round-31 carrier is UTF-8 — all 12 C1
  envelopes carry `database_encoding: "UTF-8"` (checked over `corpus/evidence/round-31/c1/envelopes/*.json`)
  and this carrier's header bytes 56..60 decode to 1 (`art/db_read.txt`). No carrier exercises the
  `UTF-16le`/`UTF-16be` branches or the replacement-character divergence between `bytes_hex` and `value`.
- Engine skew (observation, no effect observed): the envelope reports `engine.version 3.53.4` (REA's node
  SQLite) while this host's `sqlite3` CLI and Python are 3.54.0. The nine cells and the schema fields agree
  between the two reads, so the skew is inert on this data.

## 5. What the counter actually proves for q-ok-rows (code read, observation)

`tools/round-31/c2-sqlite-refusals.py:176-193`: table `Album`, `row_limit 3`, `returned_rows 3`, `columns ==
["AlbumId","Title","ArtistId"]`, every row tuple `(int(v0), v1, int(v2))` is in `oracle["album_rows"]` (the
full 347-row set), and `nr.schema.tables` equals the oracle's `Album` table. Then
`committed_check()` compares the whole live envelope to `HEAD:corpus/evidence/round-31/c2/envelopes/
q-ok-rows.json` minus top-level `meta`.

- Holds: the record I checked is the record the rule pins, and it matches the file.
- Not proven by the live branch alone: row identity, row order, distinctness, per-cell types/hex/encoding,
  and the un-exempted scalar fields.
- Observed schema cross-check (not my item, but cheap and it passed): envelope `Album` table has
  `root_page 19`, `kind table`, `without_rowid false`, `strict false`, `column_count 3`, and columns
  `(0,AlbumId,INTEGER,not_null,PK1,hidden0) (1,Title,NVARCHAR(160),not_null,PK0,hidden0)
  (2,ArtistId,INTEGER,not_null,PK0,hidden0)`, identical to `PRAGMA table_xinfo(Album)`.

## 6. Remaining unknowns

- No live REA re-run was made by this seat (contract: no REA outside a counter). The live receipt is the
  wave-1 `runs.tsv` row `q-ok-rows 2026-10-23T04:19:17+00:00 … P2-match accepted, 3 Album rows`; whether
  today's live run still returns this exact envelope is `ReRunC2`'s item, not mine. (Inference, unverified
  by me: on an immutable file and a fixed engine the scan order and cells are deterministic.)
- UTF-16 database encodings and malformed text bytes: not exercised by any round-31 carrier, behaviour known
  only from the code branch (`TextDecoder(…, {ignoreBOM:true})`, non-fatal).
- Who produced the carrier's 199 free pages and their stale leaf images (the Chinook release build): unknown
  and irrelevant to the read path.
- Hostile: none of the nine cells is derived or lossy; no non-ASCII, NUL, BOM, or float column is present in
  this sample.

## 7. Artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ScoutRowsCheck/`)

| path | sha256 |
|---|---|
| `rawscan.py` (pure-Python `sqlite_schema` + Album b-tree walk; exit 0 at the end) | `ee2cb393b8ec20f5ea27441d345264eb7c57b422a27ded1886602d4d7d81285b` |
| `verify_cells.py` (per-cell envelope-vs-DB verifier) | `acbdebe90a8069985f7a96942c353129f3b99bf1194417ef8b130a548a165279` |
| `art/rawscan.txt` (04:33:25Z, exit 0) | `90b48ec83fed00f1e2b8aa5c3a63d90378e660b7624ba48782affbcd95992e36` |
| `art/sqlite_cli.txt` (04:33:30Z, exit 0) | `e9b723efef044d682e7746c562ace223e985ac4d396379929a3005ef787f30d4` |
| `art/verify_cells.txt` (04:33:43Z, exit 0) | `3d18702091526e0223319410f3ffb544f4fbd06a98b78471968b0ccfb3f03592` |
| `art/db_read.txt` (04:34:10Z, exit 0: pragmas, plan, dbstat, page images) | `e4ec678180df4f1bebb4ec135f9a47abdc60a9ebb3cabe85c6999b81fb12991f` |
| `art/hexcheck.txt` (04:34:23Z, exit 0: envelope field inventory) | `2ddccc015f7485d2772a48e3c2f1f0c4d574fc6309108e0f518e69dd3d2c3285` |
| `art/rea_version.txt` (04:34:35Z, exit 0: rea-agents 6.5.0; module sha256 `edfcd90f9e2e1dbde531b6aafc4efb1bd105a372df617dee619a414425354970`) | `d00c20bf4166693568ea9ea72294b255fe7ec887b43e5dbc538374da1c740b05` |
| `art/page55_eq.txt` (04:35:25Z, exit 0: page 55 vs live leaf 445) | `ed1c9b647bf46ccca4b669f5c195792182f8455aa77ddc604b5ff4534b25f80f` |

Installs: none. Processes: all under `timeout`, none left running.

Report: `.ufo/waves/round-31/w2/ScoutRowsCheck.md`
