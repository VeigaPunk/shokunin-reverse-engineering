# Round 34 source novelty — GNU ELF version requirements

Seat `KaidokuR34.R34SourceNovelty`. Base `ec3125ad3d130d92f888a4128dfaa2982f36fff7` (HEAD; subject `round-33 verifier spot-check`). `corpus/SOURCES.md` was not edited. No REA run, no production reader, no binary authoring. Held item `U064N008Hf47eb933` was not opened. No tool was installed. Pacman was not used (host pause). Answering model visible to this seat: `xai-oauth/grok-4.7-build-fast`. No safety refusal and no model switch in this seat.

**Verdict.** GNU symbol-version requirements (`.gnu.version_r` / `SHT_GNU_verneed` / `Elf64_Verneed` / `Elf64_Vernaux`) are not a governed surface. Recommend **S103** as the LSB 5.0.0 Symbol Versioning chapter, section 10.7.4, for the format. Do not register the System V gABI draft of 10 June 2013 as that authority. glibc 2.42 `elf/elf.h` was opened as the code that spells `Elf64_Verneed` and the missing integers; it is not the S103 row, and its `vna_other` comment is not the field rule.

## Lane sweep at the base

Governed paths `SKILL.md`, `PROVINCE.md`, `README.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge`, `corpus/lessons`, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `MINT.md`, then every tracked `*.md` outside `corpus/evidence` and `.ufo`:

`git grep -n -I` for `verneed`, `vernaux`, `gnu.version`, `symbol version`, `Elf64_Verneed`, `DT_VERNEED`, `SHT_GNU_ver` returns **one** line:

`corpus/knowledge/2026-10-13-elf-observation-jq.md:116` — `strings -a` on `/usr/bin/jq` printed the section names `.gnu.version` and `.gnu.version_r` while searching for a `jq-<digits>` literal. The entry's claim is that runtime `jq-1.8.2` is not that literal. It does not decode a version-need record.

`git ls-tree -r --name-only` filtered for `verneed|vernaux|version_r|symbol.version|gnu.version`: **zero filenames**.

Tracked files containing `gnu.version_r` at this commit: **45**. Classed by path: 1 knowledge file (the line above), 43 retained observation dumps (REA/readelf/rizin section inventories under `.ufo/waves` and `corpus/evidence/round-26` and `round-27`), and `.ufo/waves/round-20/w1/patches/RizinLeg-2.patch` (the same kind of section inventory inside a patch). Those dumps name the section and, in some layout JSON, the type label `SHT_GNU_verneed`. None is a `vn_*` / `vna_*` decision table. Highest registry id on the base is **S102**. S103 is unused.

## Frontier and newest lesson

`PROVINCE.md` `## Frontier` (`:73-96`) and `### Round-4 frontier (post-unlock)` (`:135-164`) do not mention symbol versions, verneed, or `.gnu.version_r`. The old "offline ELF layout" bullet was pruned into Core (`:77-80`); Core binary layout (`:131`) is `inspect-binary-layout` on `/usr/bin/jq`. The coverage map's Native ELF row (`corpus/README.md:19`) is held for jq/libjq e2e, not for version-need records. Adding a requirements reader would be depth on already-held ELF ground, the same shape as round 33's "no coverage widening," not a new Frontier bullet and not a coverage-map row.

Newest lesson is `corpus/lessons/round-33-verifier-spotcheck.md` (the tip commit). It agrees the round-33 admits and the S100-style reject, and its trend line is **expansion: unchanged**: the CHPE entry sits on round-32 hybrid ground, `PROVINCE.md` gained no frontier row. The lane lesson `corpus/lessons/round-33.md` is the prior record: R33-C1 stopped, S100's CHPE-authority rejection kept, S101/S102 added for different scopes. That rejection is not reversed here. Round 33 also says the next depth claim needs an admissible input manifest frozen before data, and the quarantined builder must not be revived. This seat did not pick carriers.

## S103 — recommend, do not register

LSB Core Specification, Generic Part, **5.0.0**, chapter title Symbol Versioning, section **10.7.4 Version Requirements**.

- URL: `https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/symversion.html`
- Fetch: HTTP 200, `content-type: text/html; charset=UTF-8`, `last-modified: Wed, 20 May 2015 12:43:14 GMT`, etag `"4aa5-51682c5423837"` (size field 0x4aa5 = 19109).
- Capture: `.ufo/waves/round-34/prep/R34SourceNovelty-files/lsb-symversion.html`, 19109 bytes, sha256 `982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91`.

Located quote, capture line 717, text after the split `<P` markup, 21 words by `str.split()`:

"Version of structure. This value is currently set to 1, and will be reset if the versioning implementation is incompatibly altered."

That sentence is `vn_version`. The same section's `<PRE>` (lines 671–677) is `Elfxx_Verneed`: `vn_version`, `vn_cnt`, `vn_file`, `vn_aux`, `vn_next`. Lines 839–845 are `Elfxx_Vernaux`: `vna_hash`, `vna_flags`, `vna_other`, `vna_name`, `vna_next`. Lines 615–623 name the section: `.gnu.version_r`, type `SHT_GNU_verneed`, count in `DT_VERNEEDNUM`, strings via `sh_link`.

`Elfxx` is defined on this page, not assumed. Lines 102–112, 20 words:

"The prefix Elfxx in the following descriptions and code fragments stands for either "Elf32" or "Elf64", depending on the architecture."

So `Elf64_Verneed` / `Elf64_Vernaux` are the 64-bit spelling of those two figures. They are not given a second typedef on this page.

`vna_other`, line 937, first sentence, 11 words: "Object file version identifier used in the .gnu.version symbol version array." The rest of that line (hidden bit 15) is a second sentence and is over the 25-word quote cap if pasted whole; it is in the capture, not copied here as the row quote.

What this page does not teach: there is **no** `0x` token in the file. `SHT_GNU_verneed`, `DT_VERNEED`, `DT_VERNEEDNUM`, and `VER_FLG_WEAK` are names only. `Elfxx_Half` / `Elfxx_Word` widths are not stated here. Loader "shall" sentences are the specification, not a host observation. Nothing on the page is a parse of a public binary.

Proposed row text, not written:

`| S103 | LSB 5.0.0 Symbol Versioning, version requirements — https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/symversion.html | spec | A | .gnu.version_r / SHT_GNU_verneed record layout and field meanings, with Elfxx standing for Elf32 or Elf64; not section-type integers, not Half/Word widths, not a host binary, not loader behavior as observed | served HTML sha256 982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91, 19109 bytes, Last-Modified 2015-05-20, section 10.7.4, capture line 717 | vn_version is currently 1; Elfxx_Verneed/Vernaux field order and vna_other as the .gnu.version index are on this page; integers are not | mined | 2026-10-23 | on-release | (empty until a decision table cites it) |`

## Opened companion, not S103

glibc **2.42** `elf/elf.h`. Annotated tag object `d7be9df5ad9febb95e608e28dad3d89aa2049e33` peels to commit `d2097651cc57834dbfcaa102ddfacae0d86cfb66`. Git blob `2f29a47c0bb8c43d2ed0f8faab60dc8840b3f495` recomputed from the saved bytes (`blob <size>\0` + body) matches the GitHub contents API. Size 195524. sha256 `fd6e7f3e3c74ee9d64b9f92ce3cc31b34413ca2622a167320ea053ce9a68110f`.

URL: `https://raw.githubusercontent.com/bminor/glibc/d2097651cc57834dbfcaa102ddfacae0d86cfb66/elf/elf.h`

Capture: `R34SourceNovelty-files/glibc-elf.h`.

- `Elf64_Half` is `uint16_t` (line 28); `Elf64_Word` is `uint32_t` (line 33).
- `SHT_GNU_verneed` is `0x6ffffffe` (line 459). Comment, 3 words: "Version needs section."
- `DT_VERNEED` is `0x6ffffffe` (line 988); `DT_VERNEEDNUM` is `0x6fffffff` (line 990).
- `VER_FLG_WEAK` is `0x2` (line 1085), and the comment says it is also used by `vna_flags`.
- `VER_NEED_CURRENT` is `1` (line 1138), which matches the LSB `vn_version` sentence.
- `Elf64_Verneed` is lines 1124–1133; `Elf64_Vernaux` is lines 1153–1161. Member order matches the LSB figures.

Do not use the glibc comment on line 1157, `vna_other; /* Unused */`, as the meaning of that field. LSB line 937 says it is the version identifier in `.gnu.version`. A later glibc comment that states the index, or an LSB errata that retracts line 937, would be the flip for this comment. The typedef and the integer macros stay usable. Binutils was not opened.

## Rejection candidate

**Rejected as authority for GNU version requirements:** System V ABI, draft dated 10 June 2013, `https://www.sco.com/developers/gabi/latest/contents.html`. Identity line 3, the whole heading: "System V Application Binary Interface - DRAFT - 10 June 2013". Capture sha256 `860a69166779d1c2264867df76c750e21af9f9f185fd451659be64e794da18b0` (2717 bytes).

Searched, case-insensitive, for `verneed`, `vernaux`, `gnu.version`, `symbol version`, `SHT_GNU`, `Verneed`: the contents page, chapter 4 Sections (`ch4.sheader.html`, sha256 `0f7178d0…9891`, 48794 bytes), chapter 4 Symbol Table (`ch4.symtab.html`, sha256 `9f0c4eee…1ed3`, 20450 bytes), and chapter 5 Dynamic Linking (`ch5.dynamic.html`, sha256 `7e9e7587…0602`, 46415 bytes). **Zero matches.** The contents list has no symbol-versioning section. What that dynamic chapter does define, line 553, is `DT_SYMTAB`: "This element holds the address of the symbol table," then `Elf32_Sym` / `Elf64_Sym` on the next lines. That is a symbol table, not a version-need record.

Reason: a generic ELF symbol-table and dynamic-section draft that never names the GNU requirement record cannot teach `Elf64_Verneed` or `.gnu.version_r`. **Flip:** this draft, or a later gABI revision, gains an explicit `Elf64_Verneed` / `Elf64_Vernaux` or `.gnu.version_r` definition. Unfetched chapters (intro, relocation, program header) were not searched; a hit there would be that flip inside this same draft. Absence from the table of contents is not, by itself, the proof — the four fetched files are.

## What a later table may cite

From S103 plus the glibc companion, a decision table can state field order, `vn_version == 1`, `vna_other` as the `.gnu.version` index, and the integers `0x6ffffffe` / `0x6fffffff` / `0x2` with the file and line. It cannot yet state that a public binary's bytes match, that `sh_link` was checked, or that a weak flag was observed. Those need a frozen manifest and a reader, which this seat did not run.

Report: .ufo/waves/round-34/prep/R34SourceNovelty.md
