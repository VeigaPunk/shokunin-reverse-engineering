# Round 31 source S094 — Chinook v1.4.5

## Drafted SOURCES.md row

Exact 11-column row for `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`:

```markdown
| S094 | Chinook Database v1.4.5 release assets — https://api.github.com/repos/lerocha/chinook-database/releases/tags/v1.4.5 | dataset | A | Byte provenance of R31-C1's two Chinook SQLite carrier containers only; not database semantics or REA behavior | Release tag v1.4.5; API `assets[]`: `Chinook_Sqlite.sqlite` (1,067,008 bytes, `digest: null`) and `Chinook_Sqlite_AutoIncrementPKs.sqlite` (1,067,008 bytes, `digest: null`); downloaded SHA-256 values equal the `container_sha256` values in `corpus/evidence/round-31/c1/carriers.tsv` | Bind the two R31-C1 Chinook carrier containers to the v1.4.5 release assets; GitHub's API lists their sizes but serves no asset digest, so byte identity rests on the retained download hashes matching the frozen carrier manifest. | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r31-sqlite-positive.md |
```

The row is a draft only; the lane SOURCES.md was not edited. The requested `used-by` path was absent when checked (see Known limit).

## Gate

- API metadata: `https://api.github.com/repos/lerocha/chinook-database/releases/tags/v1.4.5`; accessed 2026-10-23; downloaded 30,371 bytes; SHA-256 `d88ffdc57f04ecfad74288dc71c48a319389909fcb7625281a3de19aa14ed6ad`. Quote from the saved served JSON: line 367, `"name": "Chinook_Sqlite.sqlite",`; line 439, `"name": "Chinook_Sqlite_AutoIncrementPKs.sqlite",`.
- Asset `Chinook_Sqlite.sqlite`: `https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_Sqlite.sqlite`; accessed 2026-10-23; 1,067,008 downloaded bytes; SHA-256 `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a`. Asset-name quote locating it in the API response: line 367, `"name": "Chinook_Sqlite.sqlite",`.
- Asset `Chinook_Sqlite_AutoIncrementPKs.sqlite`: `https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_Sqlite_AutoIncrementPKs.sqlite`; accessed 2026-10-23; 1,067,008 downloaded bytes; SHA-256 `ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4`. Asset-name quote locating it in the API response: line 439, `"name": "Chinook_Sqlite_AutoIncrementPKs.sqlite",`.
- The API's `assets[]` metadata gives size `1067008` for both SQLite assets and `digest: null` for both (API JSON lines 392-393 and 464-465). No publisher digest was served.

## Commands and observations

UTC evidence-recording time: `2026-10-23T04:12:11Z` (sampled after the fetches and hash outputs).

1. API metadata fetch — exact command:

```sh
if timeout 900 curl -fsSL -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' 'https://api.github.com/repos/lerocha/chinook-database/releases/tags/v1.4.5' -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/release-v1.4.5.json; then printf 'curl exit code=0\n'; else rc=$?; printf 'curl exit code=%s\n' "$rc"; fi
```

Exact output: `curl exit code=0`. Curl exit 0; the command completed successfully. The saved metadata's `sha256sum`, `stat`, and `wc -l` output was:

```text
d88ffdc57f04ecfad74288dc71c48a319389909fcb7625281a3de19aa14ed6ad  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/release-v1.4.5.json
bytes=30371 file=/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/release-v1.4.5.json
632 /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/release-v1.4.5.json
```

Producing command: `timeout 900 sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/release-v1.4.5.json && timeout 900 stat -c 'bytes=%s file=%n' /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/release-v1.4.5.json && timeout 900 wc -l /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/release-v1.4.5.json`; exit 0; recorded at the UTC time above.

2. Asset downloads — exact curl commands and outputs:

```sh
if timeout 900 curl -fsSL 'https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_Sqlite.sqlite' -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite.sqlite; then printf 'curl exit code=0\n'; else rc=$?; printf 'curl exit code=%s\n' "$rc"; fi
```

Output: `curl exit code=0`.

```sh
if timeout 900 curl -fsSL 'https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_Sqlite_AutoIncrementPKs.sqlite' -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite_AutoIncrementPKs.sqlite; then printf 'curl exit code=0\n'; else rc=$?; printf 'curl exit code=%s\n' "$rc"; fi
```

Output: `curl exit code=0`. Both curl calls and their wrappers exited 0; recorded at the UTC time above.

3. Download hashes and byte sizes — producing command:

```sh
timeout 900 sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite.sqlite /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite_AutoIncrementPKs.sqlite && timeout 900 stat -c 'bytes=%s file=%n' /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite.sqlite /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite_AutoIncrementPKs.sqlite
```

Exact output excerpt; command exit 0, recorded at the UTC time above:

```text
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite.sqlite
ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite_AutoIncrementPKs.sqlite
bytes=1067008 file=/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite.sqlite
bytes=1067008 file=/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite_AutoIncrementPKs.sqlite
```

Observation: those hashes exactly match `container_sha256` in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/carriers.tsv` lines 7-8: `chinook` = `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a`; `chinook-autoinc` = `ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4`.

4. Draft artifact hash — `timeout 900 sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/S094.row.md && timeout 900 stat -c 'bytes=%s file=%n' /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/S094.row.md`; exit 0; recorded at the UTC time above. Output: SHA-256 `42a2c74bcbc68e33ea4e4ed008e8494cbdec176abdf4b2527780cbe3a156260e`, `858` bytes.

5. Used-by existence check — exact command: `if timeout 900 test -e /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-positive.md; then printf 'target exists\n'; else rc=$?; printf 'test -e exit code=%s\n' "$rc"; fi; timeout 900 date -u +%FT%TZ`. Exact output: `test -e exit code=1` then `2026-10-23T04:12:11Z`. The missing target is an observation, not a claim that a future integration will fail.

## Surfaces, scope, and limits

- Affected lane surface: this report only. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`, the carrier list and frozen carrier files were read only. No REA invocation, counter, test, or tool installation was made.
- Scope of S094: publication identity and downloaded-byte match for these two v1.4.5 assets. The asset API's digest fields are null; the hashes here are local hashes compared against the frozen carrier manifest, not publisher-supplied digests. Database semantics and REA behavior were not evaluated.
- Known limit: at `2026-10-23T04:12:11Z`, the requested used-by knowledge file did not exist (`test -e` exit 1), so the draft's `mined` status / used-by contract condition is not yet independently satisfied in the lane tree. Draft row is provided exactly as requested for integration when that entry exists.

## Scratch artifacts

- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/release-v1.4.5.json` — raw API response; SHA-256 `d88ffdc57f04ecfad74288dc71c48a319389909fcb7625281a3de19aa14ed6ad`.
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite.sqlite` — downloaded release asset; SHA-256 `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a`.
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/Chinook_Sqlite_AutoIncrementPKs.sqlite` — downloaded release asset; SHA-256 `ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4`.
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcChinook/S094.row.md` — drafted SOURCES row; SHA-256 `42a2c74bcbc68e33ea4e4ed008e8494cbdec176abdf4b2527780cbe3a156260e`.

No tools were installed or updated.
