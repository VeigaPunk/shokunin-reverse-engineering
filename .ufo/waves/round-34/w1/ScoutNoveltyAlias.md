# ScoutNoveltyAlias — base novelty of the GNU version-needs decision table

Seat `KaidokuR34.ScoutNoveltyAlias`. Sweep revision is the claim base `ec3125ad3d130d92f888a4128dfaa2982f36fff7` (`round-33 verifier spot-check`, 2026-10-23 07:18:52 -0300), read from sandbox `/fast/scratch/hyaku/kaidoku-r34/w1/ScoutNoveltyAlias` whose HEAD is freeze `54a87a51a865ab931fd355e767303337b05cccf4`. `git merge-base --is-ancestor` of the base into that HEAD exited 0. This repeats the base text/filename sweep independently of `.ufo/waves/round-34/prep/R34SourceNovelty.md`. No production reader, counter, REA run, or target execution. No tool installed. Visible model: `xai-oauth/grok-4.7-build-fast`. No safety refusal.

**Verdict.** At the base there is no governed GNU version-needs decision table. Old hits are section-inventory mentions (a section name, a span, or a section-header type label). They do not state `Verneed`/`Vernaux` field order, widths, or `vna_other` meaning. The governed table first appears in the freeze commit, not at the base. Confidence: high for these tokens on text blobs. Binary blobs were not scanned (`git grep -I`).

A governed table, as pinned at freeze `SKILL.md:1158`, is the heading `## GNU ELF version requirements — section-derived metadata (round 34)` plus the Decision / Exact field/threshold / Meaning rows (`SHT_GNU_verneed = 0x6ffffffe`, `<HHIII` / `<IHHII`, `vn_*` / `vna_*` offsets, `vna_other` kept raw). That heading is absent at the base (`git grep -F` exit 1).

## Governed documents at the base

Command, 2026-10-23T10:53:06Z, exit 0, one line:

`git grep -n -I -e verneed -e vernaux -e 'gnu\.version' -e 'symbol version' -e Elf64_Verneed -e Elf64_Vernaux -e DT_VERNEED -e SHT_GNU_ver -e version_r -e 'version needs' -e 'version-need' ec3125ad -- SKILL.md PROVINCE.md README.md corpus/README.md corpus/SOURCES.md corpus/knowledge`

```text
corpus/knowledge/2026-10-13-elf-observation-jq.md:116:  `.gnu.version`, `.gnu.version_r`. No `jq-<digits>` literal appears.
```

Context `:113-117` is a `strings -a` observation used to separate the runtime string `jq-1.8.2` from file literals. It does not decode a version-need record.

The same token set on `corpus/lessons`, `corpus/QUALITY.md`, `LOG.md`, `SCORECARD.md`, `MINT.md`, `README.md`, `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`, and `PROVINCE.md` exited 1 (2026-10-23T10:53:18Z).

`SKILL.md:42` at the base is `## Decision table (this host, r3-verified)`. Its ELF row (`SKILL.md:46`) routes `ELF exe/lib` to `rea analyze`. That is a host routing table, not a GNU version-needs field table. The base skill ends in the round-33 CHPE / builder-free sections. No heading mentions version requirements.

`PROVINCE.md` `## Frontier` (`:73`) says offline ELF layout was pruned into Core. Core binary layout (`:131`) is `inspect-binary-layout` on `/usr/bin/jq`. `corpus/README.md:19` at the base holds Native ELF for jq/libjq e2e, not version-need records. `git diff --numstat ec3125ad 54a87a51 -- PROVINCE.md` is empty. Frontier text does not mention `verneed` or `.gnu.version_r`.

`corpus/SOURCES.md` highest id at the base is S102 (`:108`). `| S103 |` is absent (exit 1). `corpus/knowledge/2026-10-23-r34-elf-version-needs.md` is absent from the base tree (`git cat-file -e` fails) and present at the freeze.

Knowledge filenames containing `version` or `elf` at the base are `2026-10-13-elf-observation-jq.md`, `2026-10-13-r2-version-diff-compare.md`, `2026-10-13-r4-10-real-version-pair.md`, `2026-10-13-rea-self-documentation.md`, and `2026-10-20-r14-go-version-diagnosis.md`. The content grep above hits only the jq strings line. The other names are package/Go version topics.

Tracked filenames: `git ls-tree -r --name-only ec3125ad | grep -E -i 'verneed|vernaux|version_r|symbol[-_. ]version|gnu\\.version|version-needs|version_needs'` exited 1. Zero matching names. `git grep -l -I -F gnu.version ec3125ad -- tools` exited 1.

## Other tracked records: inventories, not the table

`git grep -l -I -F 'gnu.version_r' ec3125ad` → 45 files. `git grep -l -I -i -F verneed` → 13 files, all inside that 45. Tree-wide `git grep -n -I` for `vn_version`, `vn_cnt`, `vn_file`, `vn_aux`, `vna_hash`, `vna_flags`, `vna_other`, `vna_name`, `vna_next`, `VER_NEED_CURRENT`, `VER_FLG_WEAK`, `Elf64_Verneed`, `Elf64_Vernaux`, `Elfxx_Verneed`, `Elfxx_Vernaux` exited 1. Case-insensitive `symbol versioning` / `version requirements` / `Elf64_Verneed` also exited 1.

Per-blob classification (`git show` at the base; marker set `vn_version`, `vn_cnt`, `vna_hash`, `vna_flags`, `vna_other`, `vna_name`, `Elf64_Verneed`, `Elf64_Vernaux`): **0 of 45** contain a field marker. Full list: `.ufo/waves/round-34/w1/ScoutNoveltyAlias-files/base-gnu-version-r-classification.tsv`.

| kind | files | what the hit actually is |
|---|---:|---|
| section-name-and-span | 31 | `.gnu.version_r` as a named segment with start/end/length in REA analyze/inspect JSON, or the same JSON pasted into luna-round receipts. Example: `.ufo/waves/arc3-loop1-round12/claims/c1/EX-3/evidence/base1.json` has `"segment":".gnu.version_r","start":"0x1010a8","end":"0x101127","bytes":128` beside `.rela.dyn`. |
| section-header-type-label | 9 | `inspect_binary_layout` envelopes. One `SHT_GNU_verneed` line each (count 9). The object is a section header: `type`, `address`, `offset`, `size`, `alignment`. Not `vn_*` / `vna_*`. Paths: `corpus/evidence/round-26/c1/envelopes/inspect-binary-layout-{base,copy,repeat}.json` and round-27 `jq-` / `tinyxxd-inspect-binary-layout-{base,renamed,repeat}.json`. |
| readelf-or-rizin-type-column | 4 | Type column `VERNEED` next to the section name. `.ufo/waves/round-20/evidence/c2/rizin/readelf-jq-sections.stdout` line shape: `[ 7] .gnu.version_r    VERNEED ...`. Same column in `jq-iS-1.stdout`, `libjq-iS-1.stdout`, and `.ufo/waves/round-20/w1/patches/RizinLeg-2.patch` (the rizin inventory embedded in a patch). |
| knowledge-strings-mention | 1 | The `:116` line above. |

`SHT_GNU_verneed` occurs only in those 9 layout envelopes. The literal `VERNEED` occurs only in those 4 type-column files. Neither is a decision row.

## Freeze contrast (not a base hit)

`git diff --stat ec3125ad 54a87a51` on the governed docs: `SKILL.md` +43, new `corpus/knowledge/2026-10-23-r34-elf-version-needs.md` +47, `corpus/SOURCES.md` +7, `corpus/README.md` +3/−1, plus `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, and `corpus/lessons/round-34.md`. `PROVINCE.md` and root `README.md` are unchanged.

At the freeze, `SKILL.md:1158` is the governed table (the diff inserts it after the round-33 builder-free limits). `corpus/SOURCES.md:109` adds S103. `corpus/README.md:19` keeps the existing Native ELF row and appends the round-34 knowledge name, with the cell text "not coverage widening". That README edit is freeze-only. At the base the coverage map does not name version-needs.

So the base already holds native ELF (jq/libjq e2e and `inspect-binary-layout` section inventories). It does not hold a source-backed Verneed/Vernaux decision table. The old mentions are not that table.

## Commands and bounds

Receipt: `.ufo/waves/round-34/w1/ScoutNoveltyAlias-files/commands.txt`. Classification: `.ufo/waves/round-34/w1/ScoutNoveltyAlias-files/base-gnu-version-r-classification.tsv`. Searches were `git grep -I` / `git ls-tree` / `git show` / `git diff` at the named revisions. `tools/round-34/elf-version-needs.py` and `tools/round-34/version-needs-counter.py` were not run.

Unknown: tracked binary blobs (grep `-I` skips them). A binary that embedded `Elf64_Verneed` text would not show up. No text path did.

Report: .ufo/waves/round-34/w1/ScoutNoveltyAlias.md
