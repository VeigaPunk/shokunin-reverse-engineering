# ScoutRejectGABI — S105 rejected gABI reopen

Seat `KaidokuR34.ScoutRejectGABI`. Sandbox `/fast/scratch/hyaku/kaidoku-r34/w1/ScoutRejectGABI`, branch `seat-r34-ScoutRejectGABI`, HEAD `54a87a51a865ab931fd355e767303337b05cccf4`. Freeze blobs were read from that revision. Lane HEAD at probe time was `d52e2404ea0160de990d28df673011bb671829f8`; the four gABI captures in the lane worktree still matched the freeze blobs byte for byte. No Git or jj write. No tool install. Pacman was not used. No parser, counter, or target binary was run. Visible answering model: `xai-oauth/grok-4.7-build-fast`. No safety refusal and no model switch.

**Verdict.** S105 stays rejected as authority for GNU version-needs. An independent case-insensitive search of the four already-opened files finds zero `verneed`, `vernaux`, `gnu.version`, `symbol version`, and `SHT_GNU` hits, and zero `gnu` at all. The frozen flip is unchanged. This is not a claim that the rest of the 10 June 2013 draft lacks those names.

## Identity quote

Capture `.ufo/waves/round-34/prep/R34SourceNovelty-files/gabi-contents.html`, line 3, SHA-256 `860a69166779d1c2264867df76c750e21af9f9f185fd451659be64e794da18b0`, 2717 bytes:

"System V Application Binary Interface - DRAFT - 10 June 2013"

`str.split()` yields 11 tokens: System, V, Application, Binary, Interface, `-`, DRAFT, `-`, 10, June, 2013. The spaced hyphens are tokens. That is the same 11-word count as `corpus/lessons/round-34.md:25`.

## Reject reason and flip, not amended

Frozen `corpus/SOURCES.md:111` teaches cell, status `rejected`, used by `corpus/lessons/round-34.md`:

"REJECTED: four opened files lack GNU version-needs definitions; flip: an opened chapter/revision explicitly defines Verneed/Vernaux or .gnu.version_r"

`corpus/SOURCES.md:115` keeps the limit: S105 is rejected for GNU-specific authority, not for generic ELF usefulness. The search log at `:140` already says unfetched gABI chapters remain unsearched.

`prep/R34SourceNovelty.md:72-76` gives the same reject in longer form. Reason: a generic ELF symbol-table and dynamic-section draft that never names the GNU requirement record cannot teach `Elf64_Verneed` or `.gnu.version_r`. Flip stated there: this draft, or a later gABI revision, gains an explicit `Elf64_Verneed` / `Elf64_Vernaux` or `.gnu.version_r` definition; a hit in an unfetched chapter of this same draft would be that flip. Absence from the table of contents is not, by itself, the proof.

`corpus/lessons/round-34.md:21` calls S105 a real reject, not an intentionally malformed invented source. `:25` repeats the flip as: an opened chapter/revision explicitly defines Verneed/Vernaux or `.gnu.version_r`. Unfetched chapters are not an absence claim.

`claims.json` `source_rows` at the freeze names S103 and S104 only. S105 is not a positive claim source.

## What this seat searched

Only these four freeze-equal files. Primary needle totals are 0. Extra needles also 0: `dt_verneed`, `version_r`, `.gnu.version_r`, `elf64_verneed`, `elf64_vernaux`, `vn_file`, `vna_name`, `vna_hash`, `vna_flags`, `vna_other`, `ver_need`, `gnu version`, `version-need`, `version_need`, `symbol-version`, `versym`, `verdef`, `dt_ver`. Case-folded `gnu` total is 0.

| file | bytes | sha256 | lines |
|---|---:|---|---:|
| `gabi-contents.html` | 2717 | `860a69166779d1c2264867df76c750e21af9f9f185fd451659be64e794da18b0` | 102 |
| `gabi-sheader.html` (`ch4.sheader.html`) | 48794 | `0f7178d014050c3f022fbe9e269cac2bcb2e77217dc9d1fb00f6d886a2e69891` | 1422 |
| `gabi-symtab.html` (`ch4.symtab.html`) | 20450 | `9f0c4eee93088a6d5d19b8e1d162c5f834a99209324e5b3c2ff19965ede71ed3` | 595 |
| `gabi-dynamic.html` (`ch5.dynamic.html`) | 46415 | `7e9e7587b90069398ae5830bbef0e40646a229531705cec86b69bee74e0e0602` | 1264 |

Sandbox copies of the same four paths were byte-equal to the lane files and to `git cat-file -p 54a87a51:<path>`.

## What the opened pages do define

Contents lists no symbol-versioning section. Its HTML targets are `revision.html`, `ch4.intro.html`, `ch4.eheader.html`, `ch4.sheader.html`, `ch4.strtab.html`, `ch4.symtab.html`, `ch4.reloc.html`, `ch5.intro.html`, `ch5.pheader.html`, `ch5.prog_loading.html`, and `ch5.dynamic.html`. Searching the contents file searches those link labels. It does not search the chapter bodies.

Sections (`gabi-sheader.html:2-3`, title "Sections") names `SHT_NULL` through `SHT_SYMTAB_SHNDX` plus the `LO*`/`HI*` range markers. There is no `SHT_GNU_*`. Special section names run from `.bss` through `.text`, including `.dynstr` and `.dynsym`, and do not include `.gnu.version` or `.gnu.version_r`. The only line matching `version` is `:1225`, under `.comment`: "This section holds version control information." That is not a version-need record.

Symbol Table (`gabi-symtab.html:2-3`) Figure 4-18, lines 27–43, defines `Elf32_Sym` and `Elf64_Sym` (`st_name`, `st_info`, `st_other`, `st_shndx`, `st_value`, `st_size`). It does not define `Elf64_Verneed` or `Elf64_Vernaux`. The file has no `version` line.

Dynamic Linking (`gabi-dynamic.html:2-3`) defines dynamic tags including `DT_NEEDED`, `DT_STRTAB`, and `DT_SYMTAB`. It does not define `DT_VERNEED`, `DT_VERNEEDNUM`, or `DT_VERSYM`. Line 553, under `DT_SYMTAB`: "This element holds the address of the symbol table," (9 words). Lines 554–556 continue with `Elf32_Sym` / `Elf64_Sym`, not a version-need structure. The other `version` lines are `:937` `e_ident[EI_ABIVERSION]` and `:940` `e_version`. Those are generic ELF header fields.

So the opened draft can teach a symbol table and a needed-library tag. It cannot teach the GNU requirement record. That is why the reject stands.

## Not searched, and not an absence

These contents targets were not fetched and were not searched: `revision.html`, `ch4.intro.html`, `ch4.eheader.html`, `ch4.strtab.html`, `ch4.reloc.html`, `ch5.intro.html`, `ch5.pheader.html`, `ch5.prog_loading.html`. The novelty note names intro, relocation, and program header as examples; the list above is the full remainder of this contents page, still unopened. A GNU version-need definition in one of those bodies would meet the existing flip inside this draft. This seat did not look, so it does not report that they lack the names.

`gabi-symtab.headers` is not in the capture directory. Contents, section, and dynamic header receipts are present (HTTP 200, dates `Fri, 23 Oct 2026 10:23:05 GMT`, `10:23:49 GMT`, and `10:23:51 GMT`). The symbol-table bytes and digest still match the frozen capture and `capture-manifest.json`. Missing response headers are not a flip.

## Probe

Retained receipt: `.ufo/waves/round-34/w1/ScoutRejectGABI-files/search-receipt.json`.

- UTC `2026-10-23T10:54:33.621357+00:00`
- argv: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I -B -` (stdin probe; writes only the receipt above)
- exit 0; primary total 0; extra total 0; `gnu` total 0
- An earlier stdout-only run at `2026-10-23T10:53:42.291667+00:00` measured the same four digests and the same zero primary counts. A still earlier local script exited 1 on a `decode` bug before any hash; that failure is not a source result.

No production reader scoring. No rule repair.

Report: .ufo/waves/round-34/w1/ScoutRejectGABI.md
