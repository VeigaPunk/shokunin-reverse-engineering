# R28-C2 source row — Sourcify canonical-signatures.json at 189cd726

Scout seat: KaidokuR28a2.SourceCanonicalList. All times UTC, 2026-10-22. Leaf seat, no subagents, no lane writes outside this report.

## Source opened (S085)

- URL: `https://raw.githubusercontent.com/argotorg/sourcify/189cd726f7ed8fb3d2f503402d5c133e0f50e1fd/services/4byte/src/utils/canonical-signatures.json`
- Opened: plain curl, 2026-10-22T18:23:19Z (HTTP 200, 3857 bytes) and again 2026-10-22T18:26:16Z (HTTP 200, 3857 bytes, headers captured).
- sha256 of bytes read: `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2` (both fetches identical; equals the expected value in the item).
- Response headers: `content-type: text/plain; charset=utf-8`, `content-length: 3857`, `etag: "74fd7b24a59b3312ec10ede9b1f4eda238c655fe5bc1989958b021682152f16d"`.
- Located quote, bytes at file lines 2-3 (JSON object member, no rendering involved):
  `"0xd55ec697": {` / `"signature": "upgrade()",` — selector `0xd55ec697` maps to signature `upgrade()`, source `generic:proxy` (line 4).

## Equality with the lane copy

- Lane copy `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-28/c2/canonical-signatures.json`: sha256 `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2`, 3857 bytes.
- `cmp -s` remote vs lane copy: `cmp_exit=0` — byte-identical (observation).
- Independent anchor: `git hash-object` on the served bytes returns `22ffd814d63d6ebb5b62129d2637b64d7d7de08c`, and `git cat-file blob 22ffd814...` from the clone hashes to the same sha256 (`cmp_exit=0`), so the served bytes are exactly that Git blob (observation).

## Key count and shape

- 36 keys (observation, three independent counts): parsed JSON object length 36; textual match of `^  "0x[0-9a-f]{8}": {$` = 36 in both the remote file and the lane copy; 36 `"source"` fields. No duplicate-key collapse (textual and parsed counts agree).
- Every key is `0x` plus 8 lowercase hex characters (length 10). File is 141 lines, mode 100644, trailing newline, LF only.
- Values are objects with keys `source` plus, for 31 of 36, `signature`. Five entries carry `source` only and no `signature`: `0x60806040`, `0x60a06040`, `0x60c06040`, `0x60e06040`, `0x61010060`, all `system:magic` (observation).
- `source` value counts: standard:erc20 11, protocol:uniswap 6, system:magic 5, generic:proxy 2, protocol:seaport 2, and one each of protocol:0x, protocol:1inch, protocol:gemswap, protocol:metamask, protocol:polynetwork, standard:eip712, standard:erc165, standard:erc721, standard:ownable, manual (observation).

## Commit history of the file

Clone: `git clone -q --filter=blob:none --no-checkout --single-branch https://github.com/argotorg/sourcify` in this seat dir (exit 0, 5.8 MB, default branch `staging`); then `git fetch --filter=blob:none origin '+refs/heads/*:refs/remotes/origin/*'` (exit 0).

Rename-aware history on the master/staging line, `git log --follow -M --format='%h %cI %s' --name-status -- services/4byte/src/utils/canonical-signatures.json`:

```
56c6b336 2025-10-29T10:07:53+01:00 Add canonical signature (#2471)
M   services/4byte/src/utils/canonical-signatures.json
5fc5ebc3 2025-10-08T15:30:17+02:00 Create 4byte service (#2402)
R100 services/server/src/server/services/utils/canonical-signatures.json -> services/4byte/src/utils/canonical-signatures.json
260c5e53 2025-09-16T16:58:25+02:00 4byte read endpoints (#2373)
A   services/server/src/server/services/utils/canonical-signatures.json
```

- Current bytes came in at `56c6b336` (blob `22ffd814`); earlier blob was `a32c56ec` at `5fc5ebc3`. All three commits are ancestors of `origin/master` (`merge-base --is-ancestor` exit 0 each).
- Widening to all refs (`git log --all` over both historical paths) adds three commits that exist only on the unmerged branch `origin/create-4bytes-service` and are ancestors of neither `origin/master` nor `origin/staging` (`git branch -r --contains` lists only that branch; `merge-base --is-ancestor` exits 1 against `origin/master` for each): `6cb98954 2025-10-07 Remove canonical signatures from the server` (deletes the server copy, 137 lines), `19a93cdd 2025-10-01 Rename everything to "4byte" instead of "4bytes"` (R100 `services/4bytes/...` -> `services/4byte/...`), `1c69f935 2025-09-25 Init 4byte service` (adds `services/4bytes/src/utils/canonical-signatures.json`).
- No commit after 2025-10-29 touches the path on any branch, and the master/staging content has been unchanged since `56c6b336`.

## Staging comparison

- Pinned commit `189cd726f7ed8fb3d2f503402d5c133e0f50e1fd` ("Deploy latest to production (#3036)", 2026-10-21T14:56:36+02:00) is the tip of `origin/master`, a merge with parents `6048af7d` and `dc20a8ee`.
- Staging tip `0966a3bcf13a46b335dae390a0c95b3b0d980c69` ("Fix flaky cwd sandbox test in compilers package (#3038)", 2026-10-21T15:58:59+02:00) has parent `dc20a8ee`.
- Same file bytes at both: `git ls-tree` gives blob `22ffd814d63d6ebb5b62129d2637b64d7d7de08c` mode 100644 at `189cd726`, at `0966a3bc`, and at `origin/master` and `origin/staging` heads — so yes, the staging tip has the same bytes (observation; sha256 of both blobs `5572beb5...`).
- Nuance worth keeping straight: the two commits are siblings, not parent and child. `merge-base --is-ancestor 189cd726 0966a3bc` exits 1 (not an ancestor); their merge base is `dc20a8ee`. The file is unchanged across both, so the pinned copy is the current staging and master content.

## Verdict on the S085 row now in the working tree

The row is already present at `corpus/SOURCES.md:91`. Checked against this evidence: URL, sha256, "equal to the lane copy", and "36 keys" all hold (observation). Two corrections:

1. Wording "with the signature it keeps for each" overstates the file: 5 of 36 entries (`0x60806040`, `0x60a06040`, `0x60c06040`, `0x60e06040`, `0x61010060`, all `system:magic`) have no `signature` field at all. Suggested replacement for that clause: "with the signature it keeps for 31 of them; 5 `system:magic` entries carry only a source tag".
2. "Only these 36 selectors can ever carry `filtered: true`" is a consequence of the handlers code (S084), not of this dataset; true only if the code keys the map on the `0x`-prefixed form. That check belongs to the filter-code seat — flagged, not decided here. For those 5 signature-less entries the "name differs from the canonical signature" comparison has no canonical string to compare against, which the C2 counter and lesson should say explicitly (unknown until S084 is read).

Opened-source record for the row: URL as above, access date 2026-10-22, sha256 `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2`, quote at file lines 2-3 (`"0xd55ec697"` / `"signature": "upgrade()"`).

## Commands run (selection)

- `curl -sS -o canonical-signatures.remote.json -w 'HTTP %{http_code} bytes %{size_download}\n' <URL>` → `HTTP 200 bytes 3857`, exit 0, 18:23:19Z.
- `sha256sum` on lane copy and on fetched bytes → both `5572beb5...b3e2`; `cmp -s` → `cmp_exit=0`.
- `git clone --filter=blob:none --no-checkout --single-branch` → exit 0; `git rev-parse --is-shallow-repository` → `false`; branch commit count 3843.
- `git ls-tree <commit> -- services/4byte/src/utils/canonical-signatures.json` at both commits → `100644 blob 22ffd814...`.
- `git merge-base --is-ancestor 189cd726 0966a3bc` → exit 1; `git merge-base` → `dc20a8ee61787277e2a3a15f8d83c1ddc2350d47`.
- `git branch -r --contains 189cd726` → only `origin/master`.
- JSON checks via Python `json.load` → `len=36`, key length set `[10]`, all keys start `0x`.

## Seat artifacts (sha256)

- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/SourceCanonicalList/canonical-signatures.remote.json` — `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2`
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/SourceCanonicalList/canonical-signatures.remote2.json` — `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2`
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/SourceCanonicalList/blob-target.json` — `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2`
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/SourceCanonicalList/headers.txt` — `7b3bb07a8d93ccaed2d48ea6f9d2e057e3e6e56cdb27151492dd0ad59e67e8dc`
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/SourceCanonicalList/sourcify/` — blob-less clone, 5.8 MB, no file-level hash (repository).

Tooling: no installs or upgrades. Network use: three requests to raw.githubusercontent.com (not a 4byte.directory or openchain host, so outside that quota) plus one clone and one fetch from github.com. No REA run. No Git write in the lane; all Git work in this seat dir.
