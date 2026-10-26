# R42Assim — re-opened sources (every cited source of the four candidates, plus the new ones)

All times UTC, 2026-10-26. Quotes are contiguous and ≤25 words. `receipts/` paths are relative to
`.ufo/waves/round-42/w1/artifacts/R42Assim/`.

## A. `sasquatch-prebuilt-package-inventory` (staged S130)

| cited source | re-open | bytes / digest | located quote | verdict on the row's claim |
|---|---|---|---|---|
| `https://github.com/onekey-sec/sasquatch/releases` (page) | 2026-10-26T21:52:15Z, HTTP 200 | 349266 B, sha256 `71ebf1600a0a9764f62298976d0d2bd0e0700694e3e2ed5612386c7c370b734a` (`receipts/sasq-releases.html`) | "Release list sasquatch-v4.5.1-6 sasquatch-v4.5.1-5 sasquatch-v4.5.1-4 sasquatch-v4.5.1-3 sasquatch-v4.5.1-2 sasquatch-v4.5.1-1 sasquatch-v1.0.1 sasquatch-v1.0" | tag list **holds** (8 tags); the row's **asset** facts do **not** come from this page — `grep -c 'sasquatch_1.0_amd64.deb'` → 0 on the page bytes |
| asset facts behind the same row | same time, REST endpoint `https://api.github.com/repos/onekey-sec/sasquatch/releases` | 87700 B, sha256 `57a19513ca266c10a310504fc33fa16f15e04f92f0be6840c2eb4e6c56a499db` (`receipts/rel.json`) | `sasquatch-v4.5.1-6` body: "unsquashfs: fix prototypes for C23 by @whispersofthedawn in https://github.com/onekey-sec/sasquatch/pull/32" | 8 releases; asset counts `[6,6,6,6,6,6,6,2]`; **v1.0 carries 2 assets, both amd64** |
| row `recheck:` (`grep -c 'sasquatch-v4.5.1-6'` → 12) | 2026-10-26T21:53:35Z, `curl -fsSL … \| grep -c` | — | — | **reproduces**: `12` |
| row claim "release body shows … 4.5.1 against 1.0" | same | body length 645 B | body lists three change lines, "New Contributors" and a changelog URL | **falsified** — the body names no version pair |

## B. `sasquatch-unblob-compatibility` (staged S183–S186)

| cited source | re-open | bytes / digest | located quote | verdict |
|---|---|---|---|---|
| `…/unblob/main/python/unblob/handlers/filesystem/squashfs.py` (S183) | 2026-10-26T21:52:23Z, HTTP 200; and the 26.6.4 tag the same minute | both 19842 B, **both sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`**, equal to the installed copy | `48: is_avm = header.bytes_used == header.mkfs_time`; `50: commands_args.append("-be")` | content **holds today**, but the row cites a movable branch — the same defect round 38 refused `sasquatch-unblob-avm-branch` for |
| `lanes/kaidoku/round8/work/lead3-sasquatch-compat.tsv` (S184–S186) | file exists, 2175 B, sha256 `839535486b77c7893bbcf9d3eac2305647b1fa22761116a054dd202fc1bede64` | host-local campaign work file | row `be_image_built`: "no - mksquashfs on this host does not support big-endian output, so the sasquatch-v4be branch was NOT exercised" | **contradicts** the entry's `:33-34` "exercised, not assumed"; the TSV's own reconciliation row (`be_fixture_source`) is not cited by the entry |

## C. `avm-le-image-genuine-marker` (staged S212–S214)

| cited source | re-open | bytes / digest | located quote | verdict |
|---|---|---|---|---|
| `lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv` (S212) | exists; **imported** to `imported/lead2-avm-le-genuine.tsv` | 940 B, sha256 `523637c885bb50c6d445bb096f247b9a66ab33633cae46af18be4a3d4c1b9ffa` | `avm_marker  SET - mkfs_time equals bytes_used, which is upstream's own AVM marker`; `mkfs_time 361` / `bytes_used 361` | **holds**; rows' own names are wrong in one place (see below) |
| `lanes/kaidoku/round13/work/lead2-stale-build.tsv` (S213) | exists; **imported** to `imported/lead2-stale-build.tsv` | 964 B, sha256 `4c962bacd24af8132f31ce78c8e8ddf03d501f221f3590ef6bd69beafb339951` | `binary_sha256_before_no_clean_rebuild  1a7cfcf719459961ba1608185557e9c5` (identical after) | **holds** |
| `https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/tools/make/squashfs4-host-be/patches/613-avm_format_as_option.patch` (S214) | 2026-10-26T21:52:15Z, HTTP 200 | 1601 B, sha256 `9af3b3debee9f6a144c03411a439e51f4ba4f9a1bd3aaac6b8760fa9394193f8` (**identical to the campaign's own `613.patch`**) | "-no-mkfs-time\t\tuse AVM format (length instead of timestamp)" (patch lines 49-50) | **holds**; the entry's account of the `#ifdef`/`use_standard_mkfs_time` mechanism matches the bytes |
| the same path on `master` | 2026-10-26T21:52:42Z | HTTP **404** | — | the commit pin is load-bearing: the file is gone from the branch |
| the entry's "`unblob recognises`" denial (`:55-56`) | handler re-read (S108) | sha256 `2d7b901b…` | `48-50` quoted above | **falsified** on the big-endian arm |
| the entry's "`marker is invisible`" (`:30`) | handler re-read | same | `53: case Endian.LITTLE, _:` then `54: commands_args.append("-le")` | true **only** for the little-endian arm; the sentence is a universal today |
| the entry's "`what the lane keeps is the 4096-byte image`" | lane tree at base | `git ls-tree` has no such blob; the image lives in the campaign tree | — | **false**: the lane keeps nothing; bytes now imported beside this draft |

## D. `avm-le-variant-reachability` (staged S206–S207)

| cited source | re-open | bytes / digest | located quote | verdict |
|---|---|---|---|---|
| `https://raw.githubusercontent.com/Freetz/freetz/master/…/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch` | 2026-10-26T21:52:23Z, HTTP 200 | 1153 B, sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707` (`receipts/p101.patch`), **identical to the campaign's local copy** | `#define AVM_LE 2` / `#define AVM_BE 3` (patch lines 7-8) | the **define-value** correction **holds**; `AVM_BE_AVM_LE` occurs 0 times in the body |
| `lanes/kaidoku/round12/work/lead2-avm-le.tsv` (S207) | exists | 1310 B, sha256 `db153248a0a0d71aeb3b93ee4d8bfb4031dac2c4be303b60d568fa59b5a9d378` | `correct_define_measurement … mkfs_time 1792847340 != bytes_used 365 -> the AVM marker is NOT set on this path` | **holds for that run**, but that run used the stale binary — see the two 4096-byte images below |
| the entry's "what would close the variant" (`:30-33`) | retained bytes, hashed and read today | `avm-le-plain550.squashfs` = `avm-le-genuine.squashfs` = sha256 `18d3ad0563cce852a438fe414d881909a6097fc30a38ca523372931cfcafaee4` | `unsquashfs -s` → "Creation or last append time Wed Dec 31 21:06:01 1969" / "Filesystem size 361 bytes" (`receipts/unsquashfs-superblocks.txt`) | **falsified**: the plain recipe, no `-no-mkfs-time`, already sets 361 == 361 |

## E. New rows proposed by this seat

| source | re-open | bytes / digest | located quote |
|---|---|---|---|
| unblob `cli.py` @ 26.6.4 | 2026-10-26T21:53:00Z, HTTP 200 | 20221 B, sha256 `fc775f1ad66f05c0f6ba77fb74c80112ea99b4baf07900d7d701b7932259f86c` (= installed) | `(Severity.WARNING, 0),` in `get_exit_code_from_reports` (`receipts/severity-exit.txt`) |
| Freetz `550-mkfs_time__AVM_BE_AVM_LE.patch` @ master | 2026-10-26T21:54:49Z, HTTP 200 | 1080 B, sha256 `603c36c9e610a4f1a41548d167b7b984c8c7ac587c73fa5b19d1484d2aab15a7`, identical to the campaign copy | `sBlk->mkfs_time = (int) sBlk->bytes_used;` under `#if (TARGET_FORMAT == AVM_BE \|\| TARGET_FORMAT == AVM_LE)` |
| `~/.local/bin/sasquatch` (host probe) | 2026-10-26T21:54Z | sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` | = S107's `usr/bin/sasquatch` member digest, so the installed binary is that release's member |

## F. Host-local executables used (read-only, unmodified)

`/usr/bin/unsquashfs` 4.7.5 (stock, `-s`, `-lls`, `-d` into scratch), `~/.local/bin/sasquatch-v4be`
(one refusal run), `sha256sum`, `curl`. Nothing was installed, upgraded, moved or removed; no pacman
transaction; no REA call; no unblob run.
