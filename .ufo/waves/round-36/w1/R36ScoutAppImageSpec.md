# R36ScoutAppImageSpec — primary sources for the AppImage type-2 offset rule and `unsquashfs -o`

Seat: leaf scout, advisory only. Access date for everything below: **2026-10-26** (UTC 04:2x). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Only this file was written. No lane/VCS mutation, no install, no REA/unblob/sasquatch run. Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ScoutAppImageSpec` removed at the end.

## 1. Short answer

1. The **AppImage specification does not state the offset rule.** It says only that a type-2 image is an ELF "with a filesystem appended". It names no offset formula, no SquashFS requirement, and no `e_shoff` arithmetic. It is a primary source for "ELF runtime + appended filesystem" and nothing more.
2. The **offset rule is defined in the AppImage type-2 runtime's source** (`appimage_get_elf_size`, used as `fs_offset`, "= end of this ELF"). That code is the primary source for the formula.
3. The **c1-run.sh rule (`e_shoff + e_shnum*e_shentsize`) matches the runtime for K3 and K4 but is not the whole runtime rule.** The runtime takes `max(sht_end, last_section_end)`. `sht_end` is the c1-run.sh formula. `last_section_end` is `sh_offset + sh_size` of the section header at index `e_shnum-1`. The two coincide on K3/K4 (§4). c1-run.sh would be wrong on an image whose last section header describes data that extends past the section header table.
4. **`unsquashfs -o BYTES` is documented upstream and in the installed man page** as "skip BYTES at start of FILESYSTEM", default 0 (§3).
5. S110 row drafted for the runtime source (§5). Two optional rows (spec, man page) are drafted as S111/S112. Allocation of ids is L1's.

## 2. AppImage sources

### 2a. AppImage Specification (draft.md) — genuine primary, weak on the offset
- URL: https://github.com/AppImage/AppImageSpec/blob/master/draft.md (read as https://raw.githubusercontent.com/AppImage/AppImageSpec/master/draft.md).
- Pinned: last commit touching the file `5220f3e9da0b6368da23105f80b0aff02c66af87` (2026-09-25T06:06:32Z); blob bytes at that commit sha256 `dd0dd27b7ca09579956c3d80b21c0082c82f62454e0a3bfe3af0829b5b1c9be5`.
- Location: `## Specification` > `### Image format` > `#### Type 2 image format`, `draft.md:130` and `:137`.
- Quote (draft.md:130, 9 words): "**MUST** have appended to it a filesystem that the ELF part can mount".
- Quote (draft.md:137): "**MUST** contain the magic hex `0x414902` at offset 8".
- Also `### Runtime` (`draft.md:268`): the runtime uses "the filesystem image appended to the runtime binary" unless `TARGET_APPIMAGE` is set.
- What it does not say: no offset formula, no "SquashFS" in the Type 2 section (the filesystem kind is left to the runtime; the spec's `The filesystem image` section only says "Is an AppDir"). [OBSERVED by reading the whole file; the string `squashfs` does not occur in the Type 2 section.]
- A docs.appimage.org fetch (`reference/appimage-format.html`) returned no `offset`/`squashfs` text and was not used.

### 2b. type2-runtime `runtime.c` — genuine primary for the formula
- URL: https://github.com/AppImage/type2-runtime/blob/8f39b89e2ac31e1640b3d3f7e9a5108e6ce805fa/src/runtime/runtime.c
- Pinned: commit `8f39b89e2ac31e1640b3d3f7e9a5108e6ce805fa` (last commit touching the file, 2026-09-28T18:13:58Z); file sha256 `e90a7685e1e11cd422bbc9cc0032c975ef9ca998e3c3708050c1c5134286f618`. Repository is the AppImage organisation's official runtime (the object that is the `0x414902` ELF prefix of every type-2 image).
- Locations: `runtime.c:527` (`fs_offset` declaration), `:241-242` (ELF32), `:273-274` (ELF64), `:279` (`appimage_get_elf_size`), `:1500` (`fs_offset = appimage_get_elf_size(appimage_path)`), `:678-679` (`--appimage-offset`, "Print byte offset to start of embedded filesystem image").
- Quote (runtime.c:527, 17 words): "The offset at which a filesystem image is expected = end of this ELF".
- Quote (runtime.c:241-242, 15 words incl. code): "ELF ends either with the table of section headers (SHT) or with a section. sht_end = ehdr.e_shoff + (ehdr.e_shentsize * ehdr.e_shnum);"
- Code returned (`:243-244` and `:275-276`): `last_section_end = sh_offset + sh_size` of the header at index `e_shnum - 1`; `return sht_end > last_section_end ? sht_end : last_section_end;`.
- Earlier AppImageKit `src/runtime.c` (probonopd) returned HTTP 200 and carries the same function; it was not pinned. The type2-runtime repo is the current maintainer location. [INFERENCE: not diffed against AppImageKit.]

## 3. squashfs-tools documentation of `-o` / `-offset`

- Primary URL (upstream, pinned to the release matching the oracle binary): https://github.com/plougher/squashfs-tools/blob/4.7.5/Documentation/manpages/unsquashfs.1 (tag `4.7.5`; ref object `1fdc2fe01d681438a04e2a137a9f51d829ba3358`). File sha256 at tag `9721ca5b87d50570bd4f818f9d7c9c462c2f01325686cc8ad10c3af41570e628`; location `unsquashfs.1:177-178` (option line `\fB\-o\fR BYTES, \fB\-offset\fR BYTES`, then text at `:178`).
- Quote (≤25 words): "skip BYTES at start of FILESYSTEM. Optionally a suffix of K, M or G can be given to specify Kbytes, Mbytes or Gbytes respectively (default 0 bytes)." (24 words)
- Same text at master (commit `cc9daf6e6dcf0fa203000bcd49a43be3b0834f94`, 2026-07-19; file sha256 `c8add772a46b222371b7896684b65b08932d2b3ce2e67c7d9be5fce3668ad758`, `:194`).
- Installed copy: `/usr/share/man/man1/unsquashfs.1.gz:178`, owned by squashfs-tools 4.7.5-1 (`pacman -Qo`), identical sentence. This is the version the oracle ran (`oracle-run.json`: `unsquashfs version 4.7.5 (2026/03/01)`).
- Limits: the page says nothing about AppImages or ELF. It defines `-o` as a byte skip, which is all the oracle needs. `unsquashfs_help.c` (upstream) lists `-offset` in its option tables but its help text was not located by quote; not used.
- Secondary result (not used): Debian man page `manpages.debian.org/bullseye/squashfs-tools/unsquashfs.1` surfaced by search; it is a repackaging of the same page.

## 4. Does the c1-run.sh rule match the spec? — observed check

c1-run.sh (oracle mode) computes, for `\x7fELF`, class 2, data 1 (ELF64 LE): `shoff + shentsize * shnum`, then checks `hsqs` at that offset and passes it to `/usr/bin/unsquashfs -o`. Bare images (`hsqs` at byte 0) use offset 0.

| Question | Answer |
|---|---|
| Does the AppImage spec state this formula? | **No.** It says "appended". |
| Does the official runtime compute this value? | **Yes as one operand.** The runtime returns the larger of this value and `sh_offset + sh_size` of section header `e_shnum-1`. |
| Do the two agree on K3/K4? | **Yes** (below). |
| Does c1-run.sh equal the runtime for every ELF? | **No.** It differs when the last-indexed section's end exceeds the section header table's end. It also ignores ELF32 and big-endian (the runtime handles both); c1-run.sh exits on those with `unsupported carrier header`. |

Observed on K3/K4 (headers from public release URLs, `curl -r 0-2097151`; sha of the full files is the frozen carriers.json digests, not re-hashed here because only the first 2 MiB was fetched). Command: Python `struct` reads of `e_shoff`(0x28), `e_shentsize`/`e_shnum`(0x3a/0x3c), last section header `sh_offset`/`sh_size`(+0x18/+0x20).

| Carrier | magic@8 | e_shoff | shentsize | shnum | sht_end (c1-run.sh rule) | last_section_end | runtime rule = max | oracle-run.json `squashfs_offset` | `hsqs` at offset |
|---|---|---|---|---|---|---|---|---|---|
| K3 x86_64 | `414902` | 942712 | 64 | 30 | 944632 | 942712 | 944632 | 944632 | yes |
| K4 arm64 | `414902` | 934536 | 64 | 30 | 936456 | 934536 | 936456 | 936456 | yes |

Maximum `sh_offset+sh_size` over all non-NOBITS sections is 942712 / 934536 on both, i.e. below `sht_end`, so no choice of "last section" changes the result. [OBSERVED]. Both oracle offsets equal the runtime value, and the `hsqs` magic sits there. So the frozen oracle offsets for K3/K4 are what the AppImage runtime itself would use. K1/K2 are bare images (offset 0) and not covered by the AppImage spec at all.

Wording suggestion for any knowledge entry: "the offset is the end of the ELF as the type-2 runtime computes it (`appimage_get_elf_size`); for K3/K4 that equals `e_shoff + e_shnum*e_shentsize`". Do not say "the spec defines offset = end of ELF"; the spec defines no offset, and the runtime comment "end of this ELF" is the closest statement.

## 5. Draft SOURCES rows (11 columns: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by)

Census rules checked from `CORPUS.md:86-108`: kind in enum, tier A only for non-`community`, no `|` in cells, `opened` = the round that opened it. `used-by` path does not exist yet (E11 caution: L1 must land the entry in the same commit or before). Next free id at HEAD d2e46ef is S107 per `corpus/SOURCES.md` rows, with S107-S109 staged in `.ufo/waves/round-36/assimilation/staged-ids`; S110 is the id assigned to this seat.

S110 (genuine primary; the formula's source):

```
| S110 | AppImage type2-runtime runtime.c, appimage_get_elf_size — https://github.com/AppImage/type2-runtime/blob/8f39b89e2ac31e1640b3d3f7e9a5108e6ce805fa/src/runtime/runtime.c | code | A | Where the AppImage type-2 runtime locates the appended filesystem: the end of its own ELF, the larger of the section-header-table end and the last section header's end; not the SquashFS format and not unsquashfs behaviour | commit 8f39b89e2ac31e1640b3d3f7e9a5108e6ce805fa, 2026-09-28; file sha256 e90a7685e1e11cd422bbc9cc0032c975ef9ca998e3c3708050c1c5134286f618; runtime.c:241-244,273-276,279,527,1500 | Compute a type-2 AppImage's payload offset the way its runtime does, and know that `e_shoff + e_shnum*e_shentsize` alone is only one of the two operands. | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
```

Optional (L1 decides; each is a separate claim and needs its own id):

```
| S111 | AppImage Specification draft — https://github.com/AppImage/AppImageSpec/blob/5220f3e9da0b6368da23105f80b0aff02c66af87/draft.md | spec | A | The type-2 image is an ELF executable with a filesystem appended and the 0x414902 magic at offset 8; it defines no offset formula and does not name SquashFS in that section | commit 5220f3e9da0b6368da23105f80b0aff02c66af87, 2026-09-25; file sha256 dd0dd27b7ca09579956c3d80b21c0082c82f62454e0a3bfe3af0829b5b1c9be5; `Type 2 image format`, draft.md:128-137 | Separate what the spec guarantees (ELF plus appended filesystem) from what only the runtime source defines (the offset). | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
| S112 | squashfs-tools 4.7.5 unsquashfs(1) -offset — https://github.com/plougher/squashfs-tools/blob/4.7.5/Documentation/manpages/unsquashfs.1 | docs | A | The meaning of unsquashfs `-o`/`-offset` (a byte skip at the start of the filesystem, default 0); not any AppImage layout | tag 4.7.5; file sha256 9721ca5b87d50570bd4f818f9d7c9c462c2f01325686cc8ad10c3af41570e628; unsquashfs.1:177-178; installed copy /usr/share/man/man1/unsquashfs.1.gz:178 (squashfs-tools 4.7.5-1) | Run the independent oracle at a byte offset into a larger file with the documented option instead of carving the payload first. | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
```

Gate lines for the round lesson (URL, access date, ≤25-word quote):
- S110 — https://github.com/AppImage/type2-runtime/blob/8f39b89e2ac31e1640b3d3f7e9a5108e6ce805fa/src/runtime/runtime.c — 2026-10-26 — "The offset at which a filesystem image is expected = end of this ELF" (runtime.c:527).
- S111 — https://github.com/AppImage/AppImageSpec/blob/5220f3e9da0b6368da23105f80b0aff02c66af87/draft.md — 2026-10-26 — "MUST have appended to it a filesystem that the ELF part can mount" (draft.md:130).
- S112 — https://github.com/plougher/squashfs-tools/blob/4.7.5/Documentation/manpages/unsquashfs.1 — 2026-10-26 — "skip BYTES at start of FILESYSTEM. Optionally a suffix of K, M or G can be given to specify Kbytes, Mbytes or Gbytes respectively (default 0 bytes)." (unsquashfs.1:178).

## 6. Remaining unknowns / limits

- K3/K4 were checked from the first 2 MiB of each public release asset via a ranged GET. The frozen carrier files (L1's scratch) were not touched; the `squashfs_offset` values were read from `K3/oracle-run.json` and `K4/oracle-run.json`.
- The runtime was read from its main-branch commit above, not from the neovim-bundled runtime binary. [INFERENCE] the runtime inside neovim v0.12.6 uses the same function; the matching offset and `hsqs` magic on both carriers is consistent with that but does not prove it.
- AppImageKit's `src/runtime.c` and the type2-runtime copy were not diffed.
- `unsquashfs` interaction with an offset when the file has trailing data was not tested.
- If the entry quotes the runtime's `max(...)` rule, c1-run.sh's frozen formula stays frozen (reported only, not changed); the equivalence holds on K3/K4 as observed.

## 7. Tooling

No installs or upgrades (RULES.md read; pacman paused). Used `curl`, `sha256sum`, `jq`, `python3` (`struct`), `zcat`, `pacman -Qo` (read-only), `web_search`. Commands: GitHub contents/commits/ref API reads, `curl -sL <raw url>` and `curl -r 0-2097151` for the two neovim release assets.
