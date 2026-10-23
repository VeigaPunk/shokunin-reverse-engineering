# ReopenS094 — SOURCES row S094 and its Gate quote

Seat: KaidokuR31.ReopenS094 (scout, leaf). Round 31, wave 2. UTC work window
2026-10-23T04:29:57Z–2026-10-23T04:31:45Z. Read-only on the lane. No REA, no counter run, no
subagents, no tool installs.

## Verdict

- **Row verdict: agree** with `admit, mined` (S094), with one caveat that does not touch the row:
  the Gate's `d88ffdc5…d6ad` sha256 no longer matches the served API bytes and cannot be
  reproduced by another reader. The row itself carries no sha256 (the 11-column contract has no
  such column), and its own positive claims — two `.sqlite` release assets, `1,067,008` bytes each,
  `digest: null`, downloaded SHA-256 equal to `carriers.tsv` — all reproduce today.
- **Gate sha256 check: fails (reproducibility).** Counterexample below: the same URL on
  2026-10-23T04:29:57Z served 30,371 bytes hashing `f12bed17…af6cb`, not `d88ffdc5…d6ad`.
- **Gate quote check: holds.** Line 367, verbatim, 2 words.
- **Row columns vs the CORPUS.md SOURCES contract: hold.** All 11 columns present, enums valid,
  `used-by` path exists and cites S094.

## 1. Primary source opened (fresh)

Command (exit `curl_exit=0`; run 2026-10-23T04:29:57Z):

```sh
timeout 120 curl -sS -D headers.txt -o s094-api.json -L --max-time 100 \
  https://api.github.com/repos/lerocha/chinook-database/releases/tags/v1.4.5
```

Observed response line: `HTTP/2 200`; `x-github-api-version-selected: 2022-11-28`;
`last-modified: Mon, 12 Feb 2024 04:52:09 GMT`; `content-length: 30371`.

| field | value |
|---|---|
| URL | `https://api.github.com/repos/lerocha/chinook-database/releases/tags/v1.4.5` |
| access date | 2026-10-23 (04:29:57Z) |
| sha256 of bytes read | `f12bed17493dbc87950911161fa2e6994210059e60db0f0b4f9c6940629af6cb` |
| bytes / lines | 30,371 / 632 |
| located quote | line 367 (current bytes): `      "name": "Chinook_Sqlite.sqlite",` — the recorded quote `"name": "Chinook_Sqlite.sqlite",` is a contiguous substring, 2 whitespace-separated words (≤25), plain ASCII quotes, trailing comma included |

Parsed facts (`python3` json of the served bytes; observation): `tag_name` `v1.4.5`,
`published_at` `2024-02-12T04:50:23Z`, `draft` false, `prerelease` false, 16 assets total,
exactly 2 ending `.sqlite`, both `size 1067008`, both `digest: null`, and no asset in the release
has a non-null `digest`. Line 439 is `      "name": "Chinook_Sqlite_AutoIncrementPKs.sqlite",`,
so the wave-1 report's second locator is also correct in current bytes.

## 2. sha256 comparison — Gate vs row vs served bytes

- Gate table (`corpus/lessons/round-31.md:33`) records `API JSON d88ffdc5…d6ad`.
- Row `corpus/SOURCES.md:100` records **no sha256 at all**; its `anchor` cell gives
  `Release tag v1.4.5; API assets[]: Chinook_Sqlite.sqlite (1,067,008 bytes, digest: null) and
  Chinook_Sqlite_AutoIncrementPKs.sqlite (1,067,008 bytes, digest: null); downloaded SHA-256
  values equal the container_sha256 values in corpus/evidence/round-31/c1/carriers.tsv`.
  The contract's 11 columns have no sha column, so "the sha256 in the S094 row" is **N/A**; the
  row's reproducible substitutes are the sizes and `digest: null`, and those agree with the
  served bytes (1067008 / 1067008, digest null).
- Wave-1's retained copy still exists and hashes to the Gate's value:

```
$ timeout 60 sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/release-v1.4.5.json
d88ffdc57f04ecfad74288dc71c48a319389909fcb7625281a3de19aa14ed6ad  .../release-v1.4.5.json
```

  The Gate abbreviation `d88ffdc5…d6ad` is the prefix/suffix of that full hash, so the Gate value
  was not fabricated; it is a snapshot of bytes that change.
- Fresh bytes differ. `diff -u <w1 file> s094-api.json` exits 1 and touches **only**
  `download_count` (9 hunks, 9 lines each side), e.g.:

```
@@ -391,7 +391,7 @@
       "size": 1067008,
       "digest": null,
-      "download_count": 37501,
+      "download_count": 37503,
```

  Same length (30,371 bytes), same 632 lines, different content — GitHub's release JSON embeds
  live download counters, so the Gate's sha256 is not a stable identity for this URL.
  **Conclusion (observation + inference):** the recorded hash is honest for its moment but
  irreproducible; a non-author re-open must compare sizes/`digest`/asset names, not the JSON hash.
  The Gate also stores only an 8…4 abbreviation, the full 64 hex being confined to
  `.ufo/waves/round-31/w1/SrcChinook.md`.

## 3. Substantive claim re-verified independently

Fresh downloads of both assets (each `curl_exit=0`, `-fsSL --max-time 280`, 2026-10-23T04:31:32Z):

```
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  Chinook_Sqlite.sqlite
ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4  Chinook_Sqlite_AutoIncrementPKs.sqlite
bytes=1067008 ...
bytes=1067008 ...
```

These equal `corpus/evidence/round-31/c1/carriers.tsv` lines 7–8 (`chinook` `bdf635be…`,
`chinook-autoinc` `ca157cb5…`) and the on-disk carriers `/fast/scratch/hyaku/kaidoku-r31/carriers/
chinook.sqlite`, `chinook-autoinc.sqlite` (`sha256sum` and `stat` above, exit 0). So the row's
`teaches` ("bind the two carrier containers to the v1.4.5 release assets") reproduces.

One wording note (observation, minor): the Gate cell reads `assets equal carriers.tsv`, but the
API JSON cannot show that — it serves `digest: null`; equality rests on downloaded bytes. The
row's own anchor states exactly this and is accurate.

## 4. Row against the CORPUS.md SOURCES contract

Header (observation, `corpus/SOURCES.md:6`): `| id | source | kind | tier | scope | anchor |
teaches | status | opened | recheck | used-by |`. S094 row (line 100) field-by-field:

| column | value | contract check |
|---|---|---|
| id | S094 | `S`+3 digits, unique (census duplicate check prints nothing) |
| source | `Chinook Database v1.4.5 release assets — https://api.github.com/...` | title — canonical URL ✓ |
| kind | dataset | in enum ✓ |
| tier | A | A/B/C ✓; scoped to the `scope` cell; kind ≠ community ✓ |
| scope | "Byte provenance of R31-C1's two Chinook SQLite carrier containers only; not database semantics or REA behavior" | present, scoped ✓ |
| anchor | `Release tag v1.4.5; API assets[]: <names>, sizes, digest: null; ... carriers.tsv` | revision (tag) + named JSON member; **no in-document line locator** (the Gate supplies line 367/439). Weaker than S096/S097 `:328-330`-style anchors, but not a bare homepage — recorded as a weakness, not a violation |
| teaches | one grounded benefit (bind carriers to assets; digest absent) | grounded by §2/§3 ✓ |
| status | mined | mined ⇒ needs a citing path ✓ |
| opened | 2026-10-23 | ISO date ✓ |
| recheck | on-release | allowed cadence ✓ |
| used-by | `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | path exists (`test -e` → EXISTS); cites S094 at line 3 (`S094 (Chinook v1.4.5 release assets, 2 carriers)`) and in table rows 22–23 ✓ |

Contract census commands (run from the lane root, output as shown):

```
awk -F'|' '...NF!=13...' corpus/SOURCES.md        -> 0
awk -F'|' '...enum violations...' corpus/SOURCES.md -> (empty)
awk -F'|' '...S094... NF'                          -> NF=13
```

Append-only (rule 2), read-only git from the lane:

```
git -C <lane> show 0007731e:corpus/SOURCES.md | grep -c '^| S094'  -> 1
git -C <lane> show 1288285e:corpus/SOURCES.md | grep -c '^| S094'  -> 1
diff <(..0007731e..) <(..1288285e..)                                -> empty, exit 0
```

So the row entered at the integration commit and was not mutated afterwards. Rule 1 (opened in
the row-writing round) holds: `opened 2026-10-23`, wave-1 opened it the same round and the Gate
carries URL, access date and the ≤25-word quote.

## 5. Remaining unknowns

- Whether the `download_count` delta (e.g. 37501→37503 for `Chinook_Sqlite.sqlite`) is explained
  exactly by wave-1 and this wave's downloads: plausible (inference), not proven; the point
  relevant to S094 is only that the field is mutable.
- No observed defect in the row's byte-provenance claim itself; the only failed check is the
  Gate's JSON sha256, which is a Gate-record issue, not a row-content issue.

## Scratch artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS094/`)

| artifact | sha256 | bytes |
|---|---|---|
| `s094-api.json` (fresh served bytes) | `f12bed17493dbc87950911161fa2e6994210059e60db0f0b4f9c6940629af6cb` | 30371 |
| `headers.txt` (response headers) | `b84e39d0099f59a3ce2e425645e8aaf33c5af4264776dc1097fe7ad15c17d32f` | 1327 |
| `w1-vs-fresh.diff` (`diff -u` w1 saved vs fresh, exit 1) | `0a05f7adbbc8e898416c858528aa2c6b63e35edea4af321714deff4cee70d1f5` | 3519 |
| `Chinook_Sqlite.sqlite` (fresh download) | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` | 1067008 |
| `Chinook_Sqlite_AutoIncrementPKs.sqlite` (fresh download) | `ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4` | 1067008 |

No tools installed or updated.
