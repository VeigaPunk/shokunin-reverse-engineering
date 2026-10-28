# R44W2Sources — S138 / S139 re-open

Seat `R44W2Sources`. Axes checked: coverage (the two new rows still point at a live tree and a live release), depth (listing projection and tag peel, not just HTTP 200), calibration (gate quotes and the cited manifest digest against the bytes). No production file, claim, counter, rubric, or frozen byte was written. No tool was installed. Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2Sources` was removed after the fetches; a following existence check printed `SCRATCH_ABSENT`.

HEAD at the row comparison was `8bb1090af3fef64477c4337855e4347472db2701` (later than the dispatch tip `c86ea508`). `git diff --stat c48f8a4b..HEAD -- corpus/SOURCES.md` was empty, exit 0. Freeze `c48f8a4b` is an ancestor of that HEAD (`merge-base --is-ancestor` exit 0).

## Registry rows (worktree `corpus/SOURCES.md:144-145`)

Schema is the 11-column `## Registry` header (`corpus/SOURCES.md:5`), the contract `sources-census.sh` enforces (`SOURCES-CONTRACT-v1`: kind enum, tier `A|B|C`, status `queued|mined|rejected`, recheck an ISO date or `NNd` or a symbolic token). Both rows have 11 cells. They are byte-identical at freeze `c48f8a4b`, measured revision `55bcce69`, HEAD `8bb1090a`, and the worktree.

| field | S138 (`:144`) | S139 (`:145`) |
|---|---|---|
| kind | `dataset` (enum) | `docs` (enum) |
| tier | `A` | `A` |
| status | `mined` | `mined` |
| opened | `2026-10-28` (not future on this date) | `2026-10-28` |
| recheck | `180d` — matches `^[0-9]+d$` (`sources-census.sh:665`) | `on-release` — symbolic `^[A-Za-z][A-Za-z0-9 _-]*$` (`sources-census.sh:582`) |
| used-by | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | same path |

Both used-by paths exist. The entry cites them by id: `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12` (`source: S138`) and `:13` (`source: S139`). Cadence is valid and not overdue: `180d` is due at opened+180 (2027-04-26); `on-release` is reported and never judged overdue (`sources-census.sh:34-37`). Row-line sha256: S138 `0bd3e0990cea35c087833665aa65c5b7b16abf47e1473968e46a63d884474916`, S139 `2f625005cb1087c586eeacdcd86b19b9250e249c90d5915f810b52752f67f924`.

## Upstream re-open (2026-10-28T14:20:58Z)

All 10 frozen contents-API listings returned HTTP 200 with body sha256 equal to `corpus/evidence/round-44/oracle/manifest.json` and the same `(type, name, size, sha)` projection. `listing_failures = 0`. The 22 member files are still the six `__output__` children (3+3+4+4+4+4). Receipt: `.ufo/waves/round-44/w2/artifacts/R44W2Sources/reopen.json`.

Required trees:

| tree | HTTP | bytes | sha256 | names |
|---|---|---|---|---|
| `squashfs_v1/little_endian/__output__` | 200 | 1159 | `ac451319a1e22c0ad9ad24d02c0b26c8c19d0ffac7d5b14e5fc8a3c8072b1b63` (equals manifest `:23`) | `squashfs_v1.0_le.bin_extract` (1 dir) |
| `squashfs_v2/big_endian/__output__` | 200 | 2287 | `ba7e3dc2fda423fa6e9856c4ca066ca1d97ca0091617be1b162f3865c9e75be1` (equals manifest `:222`) | `squashfs_v2.0_be.bin_extract`, `squashfs_v2.1_be.bin_extract` (2 dirs; git sha `192d46c79d89e6e669a9325401ec3aa08c7d8a30` each) |

Saved bodies: `artifacts/R44W2Sources/live-squashfs_v1-little_endian-__output__.json`, `live-squashfs_v2-big_endian-__output__.json`.

squashfs-tools tag `4.7.5` is still published.

- Releases page HTTP 200, 398948 B, sha256 `ddf9b57f8092f69d66847fc54846153a56e677d58ef0ae9c21127bbdac9c00ae`, wall 0.756 s. The page contains `tag/4.7.5`.
- Tag API HTTP 200: `tag_name` `4.7.5`, `name` `Squashfs tools 4.7.5`, `published_at` `2026-03-01T23:05:47Z`.
- Annotated tag `1fdc2fe01d681438a04e2a137a9f51d829ba3358`, peeled commit `708c59ae80853b0845017c33b42e56061cc546cd`.
- Releases list: 9 tags (`4.7.5` `4.7.4` `4.7.3` `4.7.2` `4.7.1` `4.7` `4.6.1` `4.6` `4.5.1`).
- `git ls-remote` of `refs/tags/4.7.5` and `refs/tags/4.7.5^{}` exit 0, stdout sha256 `5223014dfa104beb5c87fd473bddb68734407023e77829e173e730de7782804d`, wall 0.448 s: tag object then peeled commit, the two shas above.
- `/usr/bin/unsquashfs --version` exit 1, wall 0.001 s, first line `unsquashfs version 4.7.5 (2026/03/01)`. `sha256sum /usr/bin/unsquashfs` (earlier capture) `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c`.

## Gate quotes (`corpus/lessons/round-44.md:21-25`)

| question | S138 | S139 |
|---|---|---|
| quote still located? | The named directory `squashfs_v2.0_be.bin_extract` is still a listing member. The grounds sentence is still `manifest.json` `source.grounds`. The cell's "1 token" count is not what the listing is. | Yes. Tag `4.7.5` is on the page and the API. The binary prints `unsquashfs version 4.7.5 (2026/03/01)` and exits 1. sha256 prefix `461e1fd9` / suffix `b1677c` matches the binary. |
| used-by names the entry? | Yes (`:144`) | Yes (`:145`) |
| ≤25 words? | No. The quote cell is 29 whitespace words (`round-44.md:24`). The grounds sentence itself is 18 words and would fit. The cell's "12 words" label is wrong: the quoted fragment is 10 words; full grounds is 18. | Yes. The quote cell is 11 words (`:25`). |
| recheck cadence valid? | Yes, `180d` | Yes, `on-release` |

## Drift since the rows were opened

- S138/S139 row bytes: none (freeze = measured rev = HEAD = worktree).
- unblob 26.6.4 `__output__` listings: none. All 10 saved body digests still match.
- S139 identity pins (tag name, release name, `published_at`, annotated tag, peeled commit, 9 tags, binary version line and sha256): none.
- S139 rendered page bytes: drifted, and the row already says that digest is not the pin (`SOURCES.md:145` anchor: "mutable page digest is not the recheck pin"). Recorded anchor is HTTP 200, 398943 B, sha256 `d08749f4b9cdcf2a01cd1d4e472b77e0372a9107aa720bf683f8383b644dbd93`. This reopen is HTTP 200, 398948 B, sha256 `ddf9b57f8092f69d66847fc54846153a56e677d58ef0ae9c21127bbdac9c00ae` (+5 B). Not a registry defect.
- S138's tree URL is the same URL S130 already carries. That is the pre-existing census W04 the lesson already records, not a change to the S138 row.

## Defects the record states and the bytes do not

1. **Listing count in the S138 gate quote is false.** `corpus/lessons/round-44.md:24` says listing member `squashfs_v2.0_be.bin_extract` under `squashfs_v2/big_endian/__output__` is "1 token". Command: `python3 -c 'import json; d=json.load(open("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w2/artifacts/R44W2Sources/live-squashfs_v2-big_endian-__output__.json")); print([e["name"] for e in d])'`. Exit 0. Observed `['squashfs_v2.0_be.bin_extract', 'squashfs_v2.1_be.bin_extract']`. The frozen manifest already had both dirs (`manifest.json:224-236`). The named member is present; the count 1 is not. v1 little-endian `__output__` really is one dir; the sentence is about the v2 big-endian tree.

2. **The manifest digest the lesson and the entry cite is not the file.** `corpus/lessons/round-44.md:24` and `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12` cite sha256 `4bc53dbba8beee0fbf912771efc0a55fd47a197cca1f56d2aaed790f817c1a13`. Command: `sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/oracle/manifest.json`. Exit 0. Stdout sha256 `c8928afe8cd6510515021fe5dcc5c3dee978ef8720c07de4feb1cc49fb7d8fae`. Observed `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe`. The same content sha is the blob at freeze and at `55bcce69` (git blob `a3ee20bb9ad21560e994f062a1ae9bd3ef4a3138`). `git log -- corpus/evidence/round-44/oracle/manifest.json` has one touching commit, `c1ff9e899a5c`, and that blob's content sha is `06a72dd5…`, not `4bc53dbb…`. No `manifest.json` under `round-44` hashes to the cited digest.

3. **The S138 gate cell breaks the column's own ≤25-word rule, and its word-count label is wrong.** Header `corpus/lessons/round-44.md:21` says "located quote (≤25 words)". The `:24` quote cell splits to 29 words. The parenthetical says the grounds phrase is 12 words. Whitespace split of `NOT handler code, NOT extractor behaviour, NOT a C1 carrier` is 10 words. Full `source.grounds` (`manifest.json`, the string `second oracle: unblob's expected member trees for squashfs_v1/v2; NOT handler code, NOT extractor behaviour, NOT a C1 carrier`) is 18 words. The sentence is still in the manifest; the labels 12 and the cell length are not.

S139's gate cell does not have these faults.

## Receipts

Seat `R44W2Sources`. File `.ufo/waves/round-44/w2/artifacts/R44W2Sources/receipts.json`.

| command | exit | stdout sha256 | wall s |
|---|---|---|---|
| `git ls-remote https://github.com/plougher/squashfs-tools.git refs/tags/4.7.5 refs/tags/4.7.5^{}` | 0 | `5223014dfa104beb5c87fd473bddb68734407023e77829e173e730de7782804d` | 0.448 |
| `sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/oracle/manifest.json` | 0 | `c8928afe8cd6510515021fe5dcc5c3dee978ef8720c07de4feb1cc49fb7d8fae` | 0.001 |
| `/usr/bin/unsquashfs --version` | 1 | `6154c39eee941fa66ea0ee7942802a2607d6ee2e749051c956569d7e9f6d333a` | 0.001 |

Contents-API and releases fetches are one record per URL in `reopen.json` (status, body sha256, wall). An earlier `/usr/bin/time` wrapper failed (exit 127, `command not found`) and did not run ls-remote; `identity-commands.txt` shows that miss. The successful ls-remote is the receipt row above. `git-and-binary.txt` is the earlier unsquashfs sha256 and the unpeeled `ls-remote` (tag object only, exit 0).
