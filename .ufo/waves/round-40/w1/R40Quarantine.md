# R40Quarantine — quarantine slice + AVM-theme join (round 40 wave 1)

**Verdict: CONFIRMED (slice, byte-identity) / DEFECTS FOUND in the carried dispositions (S150 stays "re-anchor"; S117 FLIPS unverifiable → adopt-with-anchor on new evidence).** The slice is byte-identical to rounds 38/39 (5 rows, sha256 `7383a90e…8e6a`). The strict join slice ∩ AVM-theme-entry ids is again **empty**, so I also hand-checked the AVM-theme entry the prompt singles out (`avm-image-extraction`, ids S200/S201), plus a drift recheck of the other AVM entries' external sources. Everything in `avm-image-extraction` holds; it is the cleanest AVM entry.

Seat `R40Quarantine` (leaf). Read-only on `/home/vgpnk/Projects/shokuknow`. No REA, no carrier, no V1, no tool install, no VCS mutation. Scratch `/fast/scratch/hyaku/kaidoku-r40/R40Quarantine` (removed at end). Evidence: `.ufo/waves/round-40/w1/artifacts/R40Quarantine/` (index at the bottom). All live fetches 2026-10-26.

## 1. Slice derivation — CONFIRMED identical

```
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > artifacts/R40Quarantine/quarantine-slice   # rc 0
```
- Register sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines, mtime Oct 24 08:37 — unchanged since round 38.
- `cmp` against `.ufo/waves/round-38/assimilation/quarantine-slice` → 0; against `.ufo/waves/round-39/w1/artifacts/R39Quarantine/quarantine-slice` → 0. sha256 of the slice `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a`.
- 5 lines, each with an S-id: `S150 S113 S117 S136 S147` (`cat -A` in the artifact; S113/S117/S136/S147 carry a stray backtick after the id and the prose class cell — the register's "unchecked family"; S150 is `payload-absent`).
- Round-39 lesson (`corpus/lessons/round-39.md` `### Assimilation`) already states "S150 … re-anchor, not refuse"; the prompt's destination `round-40/assimilation/quarantine-slice` is the L1's to create (I wrote the slice only in my artifacts dir).

## 2. AVM-theme join — still empty for the slice

AVM-theme entries: `merge/kaidoku/knowledge/corpus/knowledge/avm-{firmware-image-unblob,image-build-blocker,image-extraction,le-image-genuine-marker,le-variant-reachability}.md` (mtime 2026-10-24 23:33, unchanged since round 39). Their cited ids (S197–S201, S206/S207, S212–S214, S216–S220, S223) do not include any of the five slice ids. The register has rows with the same *numbers* only for other lanes (`kama` S200/S202/S206…, `mado` S201/S205, `kake` S206, `tsukuroi` S211/S213) — campaign ids are lane-local and these are different sources. Kaidoku has no register row for any AVM id.
→ strict hand-check set (slice ∩ AVM) = ∅; therefore every slice row was re-opened live (§3) and `avm-image-extraction` was verified end to end (§4).

## 3. Verdict table — the five slice rows (`artifacts/…/verdict-table.tsv`)

| id | r39 | r40 verdict | what I opened / located |
|---|---|---|---|
| S150 | refuse (w1) → re-anchor (w2) | **RE-ANCHOR** — refuse the row *as staged*; source is genuine | `https://zenn.dev/yasu01/articles/7370bd5d414ec4` HTTP 200, 174,088 B (sha256 `fd4c2f96…27ae` — bytes differ from R38's `42d59c48…` at the same size, so the page has per-fetch variation; every count below was taken on today's bytes). Register's string `シンボルがない場合のヒント` ×0 (`ヒント` ×0, `シンボルがない` ×0). **Gate quote** `GNU Binutils に含まれる逆アセンブラ。ほぼすべての Linux 環境に入っています。` ×2 (rendered under H3 `objdump`, which sits under H2 `道具の準備`; once more in the embedded JSON blob). **Also-quote** `strip されていても PLT のシンボルは残る場合があるので、ここが最初の手がかりになりました` ×2 (rendered under H3 `ライブラリ関数の特定`, H2 `パターン認識のコツ`). Anchor errors: the page is 第6回 (`第6回` ×2; the series table lists 第1…6回, 第4回 is the syscall article), not "part 4"; there is no `逆アセンブル`/`シンボルがない場合のヒント` heading. Corrected anchors for the row: §`objdump` and §`ライブラリ関数の特定`, part 6 of 6. |
| S113 | adopt-with-anchor | **ADOPT-WITH-ANCHOR** (21 locales + `x-default`, not "17") | `…/tools/adb?hl=en` 200, 368,063 B (sha256 `3c035d8b…16c416`). `hreflang` values: 22 distinct = ar bn de en es-419 fa fr he hi id it ja ko pl pt-BR ru th tr vi zh-Hans zh-Hant + `x-default`. Gate quote (`og:description` "Find out about the Android Debug Bridge, a versatile command-line tool that lets you communicate with a device.") ×2. Gate also-quote: the `<link rel="alternate" hreflang="ja" …?hl=ja" />` exists but is split over two source lines (`hreflang="ja"\n          href=…`), so the gate's one-line rendering is not a literal byte match — semantic match only. `grep -c 'tools/adb?hl=ja'` → 1. |
| S117 | unverifiable | **ADOPT-WITH-ANCHOR — FLIP** (anchor = Semantic Scholar record; DOI landing page still unreadable) | `doi.org/10.1109/SP46214.2022.9833799` → 302 → `ieeexplore.ieee.org/document/9833799/` HTTP 202, 0 B (publisher serves nothing, as before). **New today:** `api.semanticscholar.org/graph/v1/paper/DOI:10.1109/SP46214.2022.9833799?fields=title,venue,year,abstract` → HTTP 200 (R38 got 429 twice): the abstract contains, verbatim, the gate quote `four popular static and dynamic LLVM IR lifters that were developed by the industry or academia from a total of 252,063 executables` (Python `in` → True), and title/venue/year (`SoK: Demystifying Binary Lifters Through the Lens of Downstream Applications` / `IEEE Symposium on Security and Privacy` / 2022) are the gate's also-quote fields. Crossref 200 agrees: pages 1100-1119, 2022-05, 2022 IEEE SP. The row's scope also names "§ I Introduction" — not opened (no full text reachable). The prompt's default for the prose class cell is *unverifiable*; I flip because the quote is located, but the S2 API was 429 in earlier rounds, so the L1 may prefer "unverifiable" if it does not want a row anchored on a rate-limited API. Never a fabrication. |
| S136 | adopt-with-anchor | **ADOPT-WITH-ANCHOR** | `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md`: `grep -c '2 of 24 verbs are'` → 1; the quote starts on line 8 and `device-free` is on line 9 (a two-line span; R39 w1 mis-cited it as line 8 only). |
| S147 | adopt-with-anchor + conflict | **ADOPT-WITH-ANCHOR** (conflict stays) | `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` sha256 `ab36b310…58fe` (unchanged). `207 tools` on line 41 (`- REA release: \`rea-agents@6.7.0\`, skill v42, 207 tools.`) under `## State as of this writing`; no `REA release` heading exists. The gate's also-quote `or re-enable the plugin` ×0 (lines 23-25 forbid `rea-agents setup --client <client>` and `mcode plugin enable rea@official`). The lane pins `rea-agents` **6.5.0** (`…/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`) — the 6.7.0 vs 6.5.0 conflict stands; if adopted, cite as host-contract text, not as the lane's REA version. |

Changes versus round 39: **S117 flips** (new evidence); S136's line span and S147's missing phrase are now recorded precisely. Nothing is fabrication-class except S150's staged anchor cells.

## 4. AVM-theme entry hand-check — `avm-image-extraction` (S200, S201)

Verdict: **ADOPT-WITH-ANCHOR** (both ids); no falsified claim found. Details:

| claim in entry | check | result |
|---|---|---|
| recheck `grep -c -F 'sasquatch-v4be -no-exit-code -f -d' lanes/kaidoku/round11/work/lead1-avm-image.tsv` → 2 | run from shokuknow root | **2** ✓ |
| SourceForge path `project/squashfs/squashfs/squashfs4.3/` serves the tarball, md5 `d92ab59a…1e30dbf` | curl 200, 182,550 B; `md5sum` = `d92ab59aabf5173f2a59089531e30dbf`; sha256 `0d605512437b1eb800b4736791559295ee5f60177e102e4d4ccd0ee241a5f3f6` | ✓ |
| old path `project/squashfs/squashfs-tools/squashfs-4.3/` is not the path | HTTP 404 (both `downloads.sourceforge.net` and `sourceforge.net/…/download`); `round10/work/build-avm-tools.sh:6` contains that exact wrong path | ✓ |
| "twelve 404s" | `round10/work/lead1-avm-build.tsv` `tarball_4_3_mirrors_tried` lists 12 entries (SF direct and `/download` counted separately), `tarball_4_3_result` "every mirror returned 404" | ✓ (12 only if SF direct and /download count as two) |
| Freetz `squashfs4-host-be` pins 4.3 + 23 patches | live `Freetz/freetz` `tools/make/squashfs4-host-be/squashfs4-host-be.mk` lines 1-4: VERSION 4.3, SOURCE_MD5 `d92ab59a…`, SITE `@SF/squashfs`; live patches dir has 23 blobs whose names equal the lane's `round11/work/patches/` listing (`True 23 23`); `AVM-BE-format.txt` live = byte-identical to the lane's round-9 copy | ✓ |
| patches apply at `-p0`, gnu89 needed | `round10/work/lead1-avm-build.tsv` `patch_strip_level_required`; `round11/work/avm-build43.sh:22,27` `patch -p0` and `EXTRA_CFLAGS="-fcommon -DTARGET_FORMAT=AVM_BE -std=gnu89"` | ✓ — the entry omits `-fcommon` (minor; the recipe line has it) |
| image magic `sqsh`, XZ, `mkfs_time == bytes_used` (365 == 365) | independent `struct` parse of `round11/work/avm-be.squashfs` (4096 B, sha256 `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32`): magic `sqsh`, comp 4 (xz), mkfs_time 365, bytes_used 365, 5 inodes, root 128, version 4.0 | ✓ |
| unblob 26.6.4 → `handler=squashfs_v4_be`, `sasquatch-v4be -no-exit-code -f -d`, **no `-be`**, 4 files exact | installed unblob 26.6.4 `handlers/filesystem/squashfs.py`: `is_avm = header.bytes_used == header.mkfs_time`; `-be` appended only when not AVM, then `-no-exit-code -f -d {outdir} {inpath}`. I re-ran `unblob -v -e out` on a *copy* of the 4 KB image in scratch (development input, not a carrier): exit 0, `handler=squashfs_v4_be`, command `sasquatch-v4be -no-exit-code -f -d …` with no `-be`, outputs `apple1..4.txt` = apple/banana/cherry/date; direct `sasquatch-v4be` 4.5.1 also extracts 4 files, 1 dir | ✓ |
| entry's gate quote `sasquatch-v4be -no-exit-code -f -d` | not literal in the gate URL (`github.com/onekey-sec/unblob` is a repo root, 200); the literal string is in the lane TSV and the lane/this-round unblob logs; in unblob it is the command assembled across lines 53-60 of `squashfs.py` | anchor lives in the TSV, not at the URL (S201's gate URL `github.com/Freetz/freetz` likewise a repo root; its md5 quote is at `tools/make/squashfs4-host-be/squashfs4-host-be.mk:3`) |

Entry-level observations (none breaks adoption):
- It is the only AVM entry whose claim about unblob ("exactly as its source says for the AVM case") is *correct*; the round-39 D2 defect ("marker invisible to unblob") sits in `avm-firmware-image-unblob.md:16,75` and `avm-le-image-genuine-marker.md:30`, not here.
- Its closing caveat ("does not generalise to every AVM image — one directory and four small files") is right and is exactly what R40-C1 contests with genuine vendor members.
- The entry says "the AVM-BE data layout" without stating the LE-header fact. **Verified here (relevant to R40-C1's oracle):** in the round-11 image the inode table header at offset 121 is `74 00` → LE length 116, compressed; the XZ body decompresses (160 B); read big-endian it would be 0x7400 = 29,696 (> 8192, impossible). The directory table header at 239 is `54 80` → LE 0x8054 = stored-uncompressed, 84 B. So a **lane-built genuine AVM-layout image already exists** (4 KB, own-work, built from SourceForge squashfs 4.3 + Freetz 23 patches, sha256 above) with BE superblock, LE metadata headers, XZ and the marker — a ready-made development fixture and sanity oracle input for the R40-C1 pure-Python reader (copy: `artifacts/…/avm-be-r11.squashfs`, header table: `avm-be-r11-header-check.txt`). It is not a frozen carrier; the L1 decides whether to promote it to a scored carrier (provenance is lane-built, the same class as the K1-K6 images).

Drift recheck of the other AVM entries' external sources (live 2026-10-26, no change vs round 39): S198 tags API 200, 18 tags, no `4.3` ✓; S206 patch 101 `AVM_LE 2`, `AVM_BE 3` (2 hits) ✓; S214 patch 613 `use_standard_mkfs_time` ✓; S216 index lists `FRITZ.Box_6490_Cable-07.57.image` ✓; S217 `Product: FRITZ!Box 6490 Cable` / `Version: FRITZ!OS 7.57` / `Release date: 04.09.2023` ✓; S220 README line 674 "AVM-LE … 6490, 6590 (x86 core only) … mkfs_time … equal to the bytes_used" ✓. Round-39 defects D1 (wrong recheck string in `avm-le-variant-reachability.md:7`), D2, D3 are in the shokuknow merge entries, still unfixed there (files untouched since 2026-10-24); they are not mine to edit.

## 5. Recommendations to the L1
1. Land the slice file at `.ufo/waves/round-40/assimilation/quarantine-slice` (copy from my artifacts; cmp against round 38's = identical).
2. Lesson text: S150 "re-anchor (gate quote and also-quote present ×2; corrected anchors §objdump and §ライブラリ関数の特定, part 6/6; refuse the staged row)"; S117 "adopt-with-anchor via the Semantic Scholar record (flip; flaky API)" or keep "unverifiable" if S2 is not trusted; S113/S136/S147 unchanged.
3. If an AVM entry is ever admitted, only `avm-image-extraction` passes today (with `-fcommon` and the anchor-lives-in-the-TSV note); the other four stay as round 39 decided.
4. This round nothing is appendable from the quarantine slice without an explicit L1 decision; I make no claim about registry appends.

## 6. Limits
- Single fetch per web source; Zenn bytes vary between fetches (same length, different hash), so only counts, not hashes, are comparable across rounds. The S2 API answered 200 here but 429 in R38; a rate-limited run could revert.
- Own-work TSVs were checked and the 4 KB image re-parsed and re-extracted, but the SourceForge-built binaries are not retained (as the entry says), so I did not rebuild `mksquashfs`.
- I did not open the S117 full text (§ I Introduction) nor any non-AVM entry's sources beyond the slice.
- No frozen carrier, V1, REA, or C2 held-out item was touched. `unblob` ran only on a copy of the round-11 development image, in the scratch dir (`cd "$S"`).

## Artifacts (`.ufo/waves/round-40/w1/artifacts/R40Quarantine/`)
`quarantine-slice`, `verdict-table.tsv`, `avm-be-r11.squashfs` (4096 B, sha256 `c7f74691…32d32`), `avm-be-r11-header-check.txt`, `unblob-dev-r11-image.log`, `lead1-avm-image.tsv`, `freetz-squashfs4-host-be.mk.live`, `freetz-AVM-BE-format.txt`, `s201-sq43-tarball.sha256`, `s150-zenn.html`, `s113-adb.html`, `s117-semanticscholar.json`, `s117-crossref.json`, `s198-tags.json`, `s206-patch101.txt`, `s214-patch613.txt`, `s216-index.html`, `s217-info_en.txt`.

Report: .ufo/waves/round-40/w1/R40Quarantine.md
