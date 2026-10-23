# ScribeGateCuration — frozen source/Gate audit

**Axis:** depth. **Scope:** prose audit of the frozen source rows and Round 34 `## Gate`; no source registry edits or script execution.

## Behavior and gates

Read the round-34 frozen `claims.json`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-34.md`, `corpus/knowledge/2026-10-23-r34-elf-version-needs.md`, and the retained `R34SourceNovelty.md` plus its capture manifest. The frozen claim names S103 as `claim_row` and S104 as `other_opened_row`; the lesson also discusses rejected S105. The supplied freeze is `54a87a51a865ab931fd355e767303337b05cccf4`; this scribe did not independently resolve Git objects or re-hash the freeze.

No scripts, counter, proposed/production reader, REA, binaries, external fetches, or Git/jj commands were run. No tool was installed. This report is not an outside source admit/reject verification and makes no runtime, loader, authenticity, or vulnerability claim. The lesson itself says the outside non-author admit/reject spot-check is pending and lane-dispatched reviewers are not outside verifiers.

## Source-row contract and status

`corpus/SOURCES.md` declares these columns, in order: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

The two rows frozen in `claims.json` (`source_rows`) are reproduced exactly from that map:

```text
| S103 | LSB 5.0.0 Symbol Versioning, version requirements — https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/symversion.html | spec | A | GNU version-needs record layout and field meanings; not section integers or observed loader behavior | §10.7.4; captured .ufo/waves/round-34/prep/R34SourceNovelty-files/lsb-symversion.html:615-677,717,839-845,937; sha256 982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91 | Decode Verneed/Vernaux offsets and current revision; distinguish raw version identifiers from unobserved symbol resolution | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r34-elf-version-needs.md |
| S104 | glibc 2.42 ELF definitions — https://raw.githubusercontent.com/bminor/glibc/d2097651cc57834dbfcaa102ddfacae0d86cfb66/elf/elf.h | code | A | ELF64 Half/Word widths, GNU section constants and Verneed/Vernaux layout only; not the stale vna_other Unused comment | commit d2097651cc57834dbfcaa102ddfacae0d86cfb66; captured .ufo/waves/round-34/prep/R34SourceNovelty-files/glibc-elf.h:28-33,459,1124-1161; sha256 fd6e7f3e3c74ee9d64b9f92ce3cc31b34413ca2622a167320ea053ce9a68110f | Obtain numeric constants and fixed scalar widths; use S103 rather than the Unused comment for version-index meaning | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r34-elf-version-needs.md |
```

The third candidate is a registry row, but not in the frozen claims `source_rows` map:

```text
| S105 | System V ABI draft — https://www.sco.com/developers/gabi/latest/contents.html | spec | A | Candidate authority for GNU Verneed/Vernaux records only | DRAFT 10 June 2013; contents line 3; bounded captures gabi-{contents,sheader,symtab,dynamic}.html under .ufo/waves/round-34/prep/R34SourceNovelty-files/; contents sha256 860a69166779d1c2264867df76c750e21af9f9f185fd451659be64e794da18b0 | REJECTED: four opened files lack GNU version-needs definitions; flip: an opened chapter/revision explicitly defines Verneed/Vernaux or .gnu.version_r | rejected | 2026-10-23 | on-release | corpus/lessons/round-34.md |
```

Thus S103/S104 are A-tier `spec`/`code` rows, `mined`, opened 2026-10-23, rechecked `on-release`, each used by only the new knowledge entry. S105 is A-tier `spec`, `rejected`, opened 2026-10-23, rechecked `on-release`, used by the round-34 lesson. The lesson says no existing row's status/recheck/used-by cell changed; this is a reported statement, not a Git-diff verification. `SOURCES.md` also sequences the topic S103 → S104 and says S105 is rejected for GNU-specific authority, not generic ELF usefulness.

## Gate quote limits

QUALITY #42 requires a `## Gate` quotation to be copied from contiguous served bytes, at most 25 words, with line/section; rendered-HTML wording crossing tags must be labelled `composite` when written. The three lesson Gate quotations and recorded counts are:

- **S103:** line 717, “Version of structure. This value is currently set to 1, and will be reset if the versioning implementation is incompatibly altered.” — **21 words** (novelty manifest count); below 25. The retained line contains the sentence as one contiguous paragraph run.
- **S104:** line 459, “Version needs section.” — **3 words**; below 25, contiguous code comment.
- **S105:** contents line 3, “System V Application Binary Interface - DRAFT - 10 June 2013” — **11 words**; below 25, one heading.

No Gate quote exceeds the cap. The knowledge/source notes separately report S103's `Elfxx` paragraph as 20 words and its first `vna_other` sentence as 11; the note explicitly says the rest of line 937 would exceed 25 words if pasted whole. Those are not additional Gate quotations.

## Search-log counts and reject decision

The `corpus/SOURCES.md` 2026-10-23 search-log entry records three candidates screened: S103/S104 included and S105 excluded. The retained novelty report gives these base/repository counts:

- Governed-path `git grep -n -I` for the listed version-need terms: **1 hit**, `corpus/knowledge/2026-10-13-elf-observation-jq.md:116`; it is a `strings -a` observation of section-name text, not record decoding.
- Tracked filenames matching `verneed|vernaux|version_r|symbol.version|gnu.version`: **0**.
- Tracked files containing `gnu.version_r`: **45** — 1 knowledge file, 43 retained observation dumps, and 1 patch (`.ufo/waves/round-20/w1/patches/RizinLeg-2.patch`). The novelty report says the base registry's highest ID was S102 and S103 was unused.
- Candidate source set: **3 identified/screened, 2 included, 1 excluded**.
- S105 bounded sweep: **4 opened files** (contents plus section-header, symbol-table and dynamic chapters) and **zero hits** for the GNU version-need search. The source report's dynamic chapter example is `DT_SYMTAB` / `Elf32_Sym`/`Elf64_Sym`, which is generic symbol-table material, not a version-needs definition. Intro, relocation and program-header chapters were not opened.

**Search-term list discrepancy:** the novelty prose says the case-insensitive search used `verneed`, `vernaux`, `gnu.version`, `symbol version`, `SHT_GNU`, `Verneed` (6 listed forms); the capture manifest lists those plus `VERNEED` (7 forms); the lesson Gate lists only the first five forms. After case-folding, these represent the same five distinct needles. All three records report zero gABI hits; the discrepancy is in the enumerated forms, not the recorded result.

**Real rejection:** S105 is a real, opened 2013 gABI draft, not a fabricated malformed source. It is rejected only as authority for GNU `Verneed`/`Vernaux` records: the four actually opened files define generic ELF material but contain no GNU version-needs definition. This is not a web-wide absence claim, nor a rejection of gABI's generic ELF usefulness. The lesson's flip is: **“an opened chapter/revision explicitly defines Verneed/Vernaux or `.gnu.version_r`.”** The novelty report narrows the example to an explicit `Elf64_Verneed`/`Elf64_Vernaux` or `.gnu.version_r` definition and says a matching hit in an unopened chapter of this draft would also trigger the flip. No flip is recorded as having fired.

## Touched surfaces, out of scope, artifacts

- **Touched:** only this scoped report file. No shared registry, lesson, knowledge entry, or production file was edited.
- **Out of scope:** production behavior or scoring; independently fetching/reopening upstream sources; Git state/diff or frozen-object revalidation; consumer execution; outside admission; any inference about loader behavior, runtime resolution, authenticity, exploitability, or security significance.
- **Read-only inputs:** `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-34.md`, `corpus/knowledge/2026-10-23-r34-elf-version-needs.md`, `.ufo/waves/round-34/claims.json`, `.ufo/waves/round-34/prep/R34SourceNovelty.md`, and `.ufo/waves/round-34/prep/R34SourceNovelty-files/capture-manifest.json` in the assigned sandbox; frozen lesson/source excerpts and capture lines were read locally.
- **Report artifact:** `.ufo/waves/round-34/w1/ScribeGateCuration.md` (this file). No archival receipt files were needed.
