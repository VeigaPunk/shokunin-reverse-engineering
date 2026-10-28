# ScoutAssimilation — round 49 wave 1

**Verdict: Assimilation: none stands.** No staged entry is cheap, in-province, and not already held. `considerthese/` is absent. The package contains no SquashFS v1/v2 text, so it does not supply R49-C1. Axes checked: coverage (does any staged entry cover an open province surface the lane lacks), depth (can the staged bytes be copied), calibration (does the plan sentence match the package).

Lane HEAD `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` matches the round base. No tool was installed. No campaign command was run. Package root: `/home/vgpnk/Projects/shokuknow/merge/kaidoku`.

## Receipts

| UTC | command | exit | stdout sha256 |
|---|---|---|---|
| 2026-10-28T21:15:29Z | `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` (wrapper adds a UTC line and `EXIT:`) | 0 | `eabdb5adbf6e8f4f6b3f2aa96525a33ac7728d9879202c214116e007cd8f3606` (`r-disk-wrap.txt`; `/fast/scratch/hyaku` 46% used, 434.4G free) |
| 2026-10-28T21:13:26Z | `python3 -I -B inventory.py` (stdout saved as `inventory.json`) | 0 | `115d18d37f8b4eea5d1f4a491383f2bbdf7c3750460af8bfba5624242a6ba2ef` |
| 2026-10-28T21:13:34Z | `python3 -I -B summarize.py` | 0 | `9da31d6da33ce7fd679661e40b38fb6bb86d283977b297b54c6caad80dfada2b` |
| 2026-10-28T21:15:13Z | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD` | 0 | `45d3d31f191c7d9d0296cd258831fcfe4f9df96e9224e98468c0161157267cb4` (`r-rev.txt` → `e4f2cfa5…`) |
| 2026-10-28T21:15:13Z | `test -e …/kaidoku-shokunin/considerthese` | 1 | `cc5e55ebf3f7b45b96414b21a9908cfe76cc1374eb9ae90dffb5c82073c92817` (`r-consider.txt` prints `exists:1`) |
| 2026-10-28T21:15:13Z | count `squashfs_v1` / `squashfs_v2` / `SquashFS v1` / `SquashFS v2` in package `.md`/`.json`/`SOURCES.append.md`, then `sha256sum` the package roots and four entries | 0 | `0c4fffd7aeefb9e99302059d0cca92fd4399fd97bfb2ceb4590c8a926c5b3d5d` (`r-pins.txt`: `v1v2_hits 0`) |
| 2026-10-28T21:15:13Z | `find corpus/evidence \( -iname '*avm-le*' -o -iname '*genuine*' \)` and search `corpus/` for `18d3ad05…faee4` | 0 | `33d678bc5f3a24d912a2fc7939175e29a8923fcb3663b8f0b1fb9e01965b7425` (`r-image.txt`: no path printed; `corpus_sha_hits 0`) |
| 2026-10-28T21:16:56Z | keyword tokens in five edge entries | 0 | `c8734ce2006b96480dc6715fce9eca645bf207e34b471007997041a8a267aa33` |
| 2026-10-28T21:17:39Z | source-id collision scan of public unheld non-AVM entries | 0 | `369ae6d0f69a8a2777345297effa47b0e5ca949e261ec11ba12bec26d2236c35` |

Package file hashes (`r-pins.txt`): `MERGE-REPORT.md` `8ad9c44b…d5f4b7`, `MERGE-REPORT.json` `ba34532e…bde729`, `SOURCES.append.md` `b82d1276…510449`. Index of all 77 entries: `entries.tsv` sha256 `cc831abccdfdd0cb0f857036005506f00ce34f2e0b3164781d3d148a7827c364`.

## Package shape

| fact | value |
|---|---|
| files on disk | 80 (77 `knowledge/corpus/knowledge/*.md` + the three report files) |
| JSON entries | 77, every target file present |
| `amendments/` | absent |
| proposed rows accepted / refused | 132 / 0 (the package's own report; the lane has since refused several) |
| staged source ids | S106–S237 (132) |
| lane registry at HEAD | S001–S146 (146 rows) |
| id intersection | 41 rows, S106–S146, and they are different documents |

Example collisions, read this round:

- Staged `recorded-crash-size-ceiling.md` cites `source: S108` as `core(5)`. Lane S108 is the unblob 26.6.4 SquashFS handler (`corpus/SOURCES.md` row S108).
- Staged `jsc-mapper-cli-contract.md` cites `source: S125` as `jsc2js/main`. Lane S125 is the AVM FRITZ!Box 6490 download.
- Staged `jsc-mapper-release-inventory.md` cites `source: S129` as the jsc2js releases page. Lane S129 is the Binwalk v3 README.
- Staged `japanese-adb-mechanism-reading.md` cites `source: S148`. The lane has no S148 yet. Draft `c2-mismatch.py` A7 assigns S148 to the sysexits supersession of S146.

`MERGE-REPORT.md` still says the lane holds 105 rows and the first staged id is S106. That preamble is stale against S146.

## SquashFS / firmware overlap

`v1v2_hits 0`. Nothing in the package names `squashfs_v1`, `squashfs_v2`, or “SquashFS v1/v2”. Fourteen entries match those words in the filename or title. Five are already held. Six were refused and the staged bytes are still the refused text. One is unheld and not cheap. Two are the word “firmware” or “binwalk” in a literature title, not a handler entry.

| target | disposition |
|---|---|
| `corpus/knowledge/unblob-sasquatch-dependency.md` | **held**, round 36, as `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` |
| `corpus/knowledge/unblob-format-matrix.md` | **held**, round 38, as `corpus/knowledge/2026-10-26-unblob-format-matrix.md` |
| `corpus/knowledge/firmware-region-vocabulary.md` | **held**, round 41, renamed `corpus/knowledge/2026-10-26-binwalk-v3-unit-of-work.md` |
| `corpus/knowledge/sasquatch-prebuilt-package-inventory.md` | **held**, round 43, re-grounded as `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md` (sha256 `e1aae6ef…46795c`). The staged file still says the rendered releases page lists the `.deb` assets and that a release body states `4.5.1` against `1.0`. The held entry records the opposite: the page has zero asset filenames, and no release body states that pair |
| `corpus/knowledge/avm-image-extraction.md` | **held**, absorbed in round 40 into `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` |
| `corpus/knowledge/sasquatch-unblob-compatibility-precondition.md` | **refused** (round 36; grounds corrected in round 39). Staged claim is that the operator's tools are not installed |
| `corpus/knowledge/sasquatch-unblob-compatibility.md` | **refused** (rounds 42 and 43). Repeats held compatibility ground; three of four source lines are campaign-local |
| `corpus/knowledge/sasquatch-unblob-avm-branch.md` | **refused** (rounds 38–40). Staged closing premise is that a real AVM image still needs a tool this host does not have. AVM-BE is Core since round 41 |
| `corpus/knowledge/avm-image-build-blocker.md` | **refused** (rounds 39–40). Stale “one release away” |
| `corpus/knowledge/avm-le-variant-reachability.md` | **refused** (rounds 39, 40, 42). Headline says the LE route is closed; the package's own marker entry says the opposite |
| `corpus/knowledge/avm-firmware-image-unblob.md` | **refused** (round 40). Headline: unblob “never notices the AVM marker at all”. Rounds 40–41 showed the pinned handler branches on `mkfs_time == bytes_used` for big-endian |
| `corpus/knowledge/avm-le-image-genuine-marker.md` | **not held, not cheap.** See below |
| `corpus/knowledge/chinese-firmware-method-byte-level.md` | word overlap only (`firmware`). Intel ME patch writeup, not SquashFS. Source id S126 collides with the lane's AVM image row |
| `corpus/knowledge/japanese-surface-analysis-command-set.md` | tokens `binwalk`, `firmware`, `unblob` inside a surface-analysis memo. Not a handler entry. Source id S132 collides |

Three more bodies contain the word `firmware` and nothing else from the set (`chinese-static-tool-report.md`, `chinese-mcp-debug-platform.md`, `japanese-no-symbols-reading-workflow.md`). They are not SquashFS entries.

### Why `avm-le-image-genuine-marker` is not cheap

It is in province: `PROVINCE.md` still lists LE AVM members (`hsqs`) as Frontier, and round 40 deferred this entry for an LE-AVM round. Round 42 recommended admit-after-rewrite and did not land it. The staged file (sha256 `32077a8c…bd51b`, 4683 bytes) is still the pre-rewrite text:

- Lines 58–60 say “what the lane keeps is the 4096-byte image”. `find` under `corpus/evidence` printed nothing for `*avm-le*` / `*genuine*`. The image sha256 `18d3ad05…faee4` occurs 0 times under `corpus/`.
- Lines 52–53 say the upstream commit “introduced” `613-avm_format_as_option.patch`. Round 42 recorded that commit `761e1923f9d4` reverted it the next day and that `master` returns 404. The staged paragraph does not say so. Not re-fetched this round.
- `source: S212` and `source: S213` are `lanes/kaidoku/round13/work/*.tsv`. The TSV path exists on the shokuknow tree (`avm_le_tsv_exists=True` in `inventory.json`). It is not a lane source.
- Line 30 says the AVM marker “is invisible” to unblob because the handler stays `squashfs_v4_le`. That sentence is the same headline round 40 refused on `avm-firmware-image-unblob` for the big-endian handler.

A later LE-AVM round could re-ground a rewrite. Copying this file in round 49 would land a false retention claim beside a v1/v2 coverage claim.

## Other in-province candidates, read because a frontier bullet still names them

None is a clean copy.

- **`recorded-crash-size-ceiling.md`** (2080 bytes, sha256 `862aafc3…65e9eca`). Province already holds the 32 MiB `inspect_recorded_crash` cap. The staged load-bearing sentence says a piped `core_pattern` “bypasses the size ceiling that the lane hit”. The lane ceiling is REA's inspect cap (`PROVINCE.md` Core table), not `RLIMIT_CORE`. `source: S108` collides with the SquashFS handler row.
- **`jsc-mapper-cli-contract.md`** and **`jsc-mapper-release-inventory.md`** (sha256 `19dd4ea4…3f5e91` for the inventory). The frontier bullet “`.jsc` → source mapping” is still open, and View8 is already S017. The inventory claim says **677** releases. Its own recheck expects `grep -c 'Patched d8 for V8'` on the API's first page to print **100**. The contract cites `jsc2js/main` (movable). Both source ids collide (S125, S129).
- **`adb-locale-pinned-reference.md`** (sha256 `6142ec94…b79e5d`). The headline says “seventeen locales”. The same sentence lists eighteen names and then adds `zh-Hans` and `zh-Hant`. Round 36 already recorded that the live page's `hreflang` count is not 17 (`corpus/lessons/round-36.md` Gate). Not re-fetched this round. `source: S113` collides with the unblob BE-fixture row.

## Entries whose source ids are all above S146

Fourteen public entries do not cite S106–S146 (`r-id-scan.txt`: 25 of 39 public unheld non-AVM entries collide at or below S146; 14 do not). They are adb/CJK literature and dumpsys grammar, not SquashFS. They are not cheap this round:

- `japanese-adb-mechanism-reading.md` cites S148, the id draft A7 gives the sysexits repair.
- `japanese-no-symbols-reading-workflow.md` cites S150, the Zenn row rounds 36–47 kept as fabrication-class (quoted heading absent). Not re-opened this round.
- `adb-output-grammar-upstream.md` cites AOSP URLs, and its recheck greps `lanes/kaidoku/round10/work/aosp-AMS-android11.java`, which is not in the lane.
- The rest are the same class: a community or AOSP note, a new registry row, and a search-log change on `corpus/SOURCES.md`, which C2 re-derives (`c2-mismatch.py` A8, `rows B -> A`). That is a third landing, not a copy into the v1/v2 claim.

The other 60 entries are indexed in `entries.tsv` with `title_or_filename_overlap=no`. “Not already held” there means the stem is absent from `corpus/knowledge/` filenames and from the five renames above. It is not a prose-equivalence proof. Their `source:` lines still use the package id space.

## What the L1 should keep

`Assimilation: none` in the draft plan matches the package. There is no `considerthese/` directory. Do not append `SOURCES.append.md`. Do not copy any of the 77 files as staged.
