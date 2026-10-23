# RevDecisionTable — round-34 approved decision table / knowledge entry vs reader code

Seat: KaidokuR34.RevDecisionTable (reviewer, godspeed). Method: static source audit only —
no execution, no binary fixtures, no REA run, no production edits. Everything cited was read
at the sandbox clone `/fast/scratch/hyaku/kaidoku-r34/w1/RevDecisionTable` (HEAD
`54a87a51a865ab931fd355e767303337b05cccf4`, identical blobs to the lane at the freeze; lane
HEAD `d52e2404` adds only wave records). Reviewed objects:

- Approved decision table: `.ufo/waves/round-34/prep/R34ElfReader-files/decision-table.json` (schema `r34-elf-verneed-decisions/1`, 37 findings)
- Approved knowledge entry: `corpus/knowledge/2026-10-23-r34-elf-version-needs.md`
- Approved skill section: `.ufo/waves/round-34/approved-skill-section.txt` and its landing in `SKILL.md`
- Reader code: `tools/round-34/elf-version-needs.py` (851 lines, digest `ac7d24a5…`), counter `tools/round-34/version-needs-counter.py` (`d7f0a8cf…`), claims `.ufo/waves/round-34/claims.json`, manifest `.ufo/waves/round-34/expected.json`
- Pinned captures: `elf.h-glibc-2.44` (`c81533b7…`), `readelf.c-binutils-2_47` (`7e81eedf…`), `lsb-symversion.html` (`982fe120…`), `glibc-elf.h` 2.42 (`fd6e7f3e…`)

## Verdict

The approved decision table, the knowledge entry, the SKILL section and the reader code are
mutually consistent on every behavior-bearing claim: all 37 finding ids, order, classifications,
stages, bounds, bound_kinds, thresholds, exit codes, accept sets, ignore list and the two-schedule
counter contract check out against the code, and every digest pin resolves. Anchor truthfulness is
high but not perfect: five Ehdr per-field line citations are wrong (F3 below). No correctness or
soundness defect was found in the reader's parse logic or the counter's pass predicate. Findings
below are accuracy/taxonomy issues in frozen artifacts, not repair requests against the predicate
(no target/predicate/counter amendment is proposed).

## Findings by severity

### MEDIUM-LOW

**F1 — Three profile-bounded local rules are classified `malformed`/exit 12 while structurally identical
caps are `unsupported`/exit 11, with no stated principle** (`decision-table.json` ↔ `tools/round-34/elf-version-needs.py:129-246`).

The table's own `bound_kind` axis separates "format" (ELF-format invalidity) from "profile"
(conservative local exclusion), and the classification axis separates `unsupported` (exit 11,
"could-not-evaluate" in the registry tally) from `malformed` (exit 12, "local
malformed-profile rejection/failed"). Three rows sit in the incoherent cell profile+malformed:

- `error.malformed.string_too_long` — bound `end - start <= 1024`, anchor `LIMITS.max_string_bytes`. A >1024-byte NUL-terminated name is valid ELF that the reader decodes faithfully if the cap is lifted; it is a capability limit, yet it reports exit 12 "failed".
- `error.malformed.verneed_unreferenced` — bound "every byte not covered by a parsed span == 0x00", bound_kind `profile`. Its own anchor says "readelf ignores unreferenced bytes" (verified: `readelf.c:14142-14155` walks `vn_next`/`vn_cnt` and never inspects padding), i.e. the pinned oracle happily decodes an input this reader rejects as malformed.
- `error.malformed.verneed_overlap` — defensible (overlapping spans make the decode ambiguous), but still a local GNU-ld-layout convention, not ELF-format invalidity.

Meanwhile the same-shaped `LIMITS` caps `error.unsupported.verneed_entries` (`sh_info <= 1024`),
`error.unsupported.verneed_bytes` (`sh_size <= 65536`) and `error.unsupported.aux_entries`
(`sum(vn_cnt) <= 4096`) are `unsupported`/exit 11. Same bound nature, opposite classification,
no documented criterion. Observable consequence: an input outside a name cap counts as reader
"failed" in a counter receipt, an input outside an entry cap counts as "could-not-evaluate".
This is exactly the conservative-local-exclusion vs format-invalidity boundary the review was
asked to check; the table should either reclassify the three rows (keeping `bound_kind=profile`)
or state the classification principle (e.g. "malformed = a faithful local decode is impossible;
unsupported = decodable but out of scope"). Frozen artifact — correction note only.

### LOW

**F2 — Declared `precedence` order is not implemented in multi-fault corners** (`precedence` array ↔ parse()` raise order, `elf-version-needs.py:294-530`).

The table declares an ordered check list ("a single input is checked top-to-bottom"), and the
header stage conforms exactly (rows 0-14 in code order). Three corners diverge when two findings
apply to one input:

- (a) `error.unsupported.multiple_verneed` (row 16) is raised before `error.malformed.verneed_bounds` (row 15) is ever evaluated for `hits[0]`: two verneed sections where the first lies outside file bounds report multiple_verneed, but the declared order puts verneed_bounds first.
- (b) `error.malformed.verneed_align` (row 24) for aux cursors is enforced inside the aux loop, i.e. after `error.malformed.verneed_aux` (26), `error.unsupported.aux_entries` (27), `error.malformed.aux_count` bounds (28) and after the `vn_file` string decode (30-32) for the same entry; a `vn_aux` that is both misaligned and accompanied by an out-of-strtab `vn_file` reports `strtab_offset`, not `verneed_align`.
- (c) a `vn_next` target that is both misaligned and out of body bounds reports `verneed_next` (25); declared order puts align (24) first. Same for `vna_next` targets vs `aux_next` (29).

Single-fault behavior conforms everywhere (each bound was checked against exactly one code site).
Also the code comment at `elf-version-needs.py:126` is garbled: "the last applicable row wins
first" — the implemented and documented semantics are "first applicable row wins". Only visible
to a consumer asserting exact ids on double-fault fixtures.

**F3 — Five Ehdr per-field anchor line numbers do not resolve to the named fields in the pinned capture**
(`FINDINGS` rows ↔ `elf.h-glibc-2.44` sha `c81533b7…`; same text in `decision-table.json`).

Verified field lines in the capture (Elf64_Ehdr spans 81-97; members 83-96): `e_shoff` = 89,
`e_ehsize` = 91, `e_shentsize` = 94, `e_shnum` = 95, `e_shstrndx` = 96, `e_entry` = 87,
`e_phentsize` = 92. The rows cite:

- `error.unsupported.no_section_table`: "H:87 (e_shoff)" — 87 is `e_entry`; e_shoff is 89.
- `error.unsupported.shnum_extended`: "H:91 (e_shnum)" — 91 is `e_ehsize`; e_shnum is 95.
- `error.malformed.ehsize`: "H:92,81-97" — 92 is `e_phentsize`; e_ehsize is 91.
- `error.malformed.shentsize`: "H:95,397-409" — 95 is `e_shnum`; e_shentsize is 94.
- `error.malformed.shoff_bounds`: "H:87,91,397-409" — should be 89,95.

Field names, the struct range 81-97 and every macro-level anchor in the same block are correct
(EI_MAG0 103, EI_CLASS/ELFCLASS64 119-122, EI_DATA/ELFDATA2LSB 125-127, EI_VERSION 131-132,
EI_OSABI/{NONE 0,GNU 3} 135-140, ET_EXEC/ET_DYN 160-161, EM_X86_64 219, EM_AARCH64 317,
EV_CURRENT 378, Elf64_Shdr 397-409, SHT_NULL 430, SHT_STRTAB 433, Verneed members 1128-1135,
VER_NEED_CURRENT 1140, Vernaux members 1157-1163), and the bounds/checks themselves are
correct — this is purely a citation-accuracy defect in a frozen artifact; reader behavior and
counter outcomes are unaffected.

**F4 — Knowledge entry under-specifies the versions sort** (`corpus/knowledge/2026-10-23-r34-elf-version-needs.md` ↔ `_assemble`, `elf-version-needs.py:311-324`).

The entry says "auxiliaries by `(name,other)`"; the code sorts by `(name, other, flags, hash)`
(its docstring says the same, "parent contract: file, name, other"). The two coincide for all
counter-admissible records because the counter's `canonical()` forbids duplicate `(name,other)`
pairs, but as a description of the parser's general canonical output the entry is imprecise.

## Verified clean (evidence matrix)

- **Table == code**: all 37 findings compared field-for-field (`id`, order, `classification`, `stage`, `check`, `bound`, `bound_kind`, `anchor`) between `decision-table.json` and `FINDINGS`/`findings_document()`; `limits` == `LIMITS` (536870912 / 1024 / 65536 / 4096 / 1024), `ignored` 7/7 verbatim, `precedence` == findings order, `accepts` constants == code constants (SHT_GNU_verneed 0x6FFFFFFE = 1879048190, EM 62/183, ET 2/3, OSABI {0,3}, EV_CURRENT 1), `scope`/`profile`/`schema` equal. Exit map `EXIT_BY_CLASS` = malformed 12 / unsupported 11 / io 13, argparse usage exit 2, selftest exit 1 — matches both SKILL registry rows.
- **SKILL section**: `SKILL.md` "## GNU ELF version requirements — section-derived metadata (round 34)" matches `approved-skill-section.txt` line-for-line (blank-line-normalized diff shows only the next heading as section boundary); thresholds (`≤536870912/1024/65536/4096/1024`), exit codes 11/12/13/2, and the "conservative local exclusions" framing all match code.
- **Digest pins**: reader `ac7d24a5…`, counter `d7f0a8cf…`, freeze-integrity `fe955c57…`, author_expected `916e0669…`, expected.json `f22e7e3b…`, knowledge `d721189c…`, approved section `c156effc…`, S103 `982fe120…`, S104 `fd6e7f3e…`, all 12 carriers `e01…e12` — every `claims.json` `instruments`/`documents`/`frozen_inputs`/`sources` entry re-hashed and matched at the freeze copy.
- **Manifest vs claim width**: expected.json has 12 carriers e01-e12, 107 needed records, 339 auxiliary records, 11 `string_table` bindings, only e12 empty, sizes 14416-2939928 (inside the 16 MiB manifest cap and 512 MiB reader cap) — exactly the frozen claim's `width` and `empty_control`.
- **Conservative-exclusion vs format-invalidity split**: header `unsupported` rows (class/data/osabi/type/machine) are format+unsupported (valid elsewhere) — coherent; `no_section_table`/`shnum_extended`/`multiple_verneed` + the three caps are profile+unsupported (local exclusions) — coherent; `verneed_revision` format+unsupported (unknown future revision, LSB "currently set to 1" verified) — coherent. The only incoherent cell is F1's three rows. Absent- verneed on a supported image returns an empty list (code: `if not hits: return _assemble([])`), matching the "section-scope absence only" wording.
- **readelf.c anchors** (all verified in capture): case dispatch at 9089 and 14020; declared-count loop with silent truncation 14042-14058 (readelf breaks/warns where the reader hard-rejects — the table's stricter "every entry fits" is correctly framed as a local rule); get_data 14050-14056; vn_aux overflow 14079-14087; aux fit 14096-14109; vna_next invalid/overflow 14118-14134; vn_next invalid/overflow 14138-14151; no unreferenced-byte check anywhere in 14142-14155.
- **LSB/S104 anchors** (verified): §10.7.4 with `.gnu.version_r`/`SHT_GNU_verneed`/`sh_link` at capture 615-640; Elfxx_Verneed struct + "currently set to 1" 668-720 (717); Vernaux struct 839-845; bit-15 hidden identifier 937; S104 2.42: `Elf64_Half/Elf64_Word` typedefs 28-33, `SHT_GNU_verneed 0x6ffffffe` exactly at 459, Verneed/Vernaux 1124-1161 with the stale `/* Unused */` comment the entry explicitly declines to adopt.
- **Counter contract**: two schedules — schedule 0 original bytes; schedule 1 Sattolo single-cycle shuffle (provably no fixed points) over the 65-byte ASCII alphabet applied only to the manifest `string_table` region, prediction translated with the same table and re-sorted; since `canonical()` forbids duplicate `(name,other)` and duplicate files, the prediction's stable `(name,other)` sort equals the reader's 4-key sort, so no spurious mismatch is possible. Bytes outside the alphabet (e.g. `+`) pass through untranslated in both data and prediction — equality preserved. Schedule-1 binding errors are self-punishing (name-absent → `Unevaluable` exit 2; wrong-but-name-containing region → mismatch exit 1); no false-pass path was found **within the reviewed binding-error paths only** — this is a statement about those paths, not about the claim's discrimination power. The claim's discrimination is separately falsified: the kill-rule control (below) is an actual false accept. e12 (empty, no `string_table`) repeats its empty record on schedule 1, per `empty_control`. Opaque random filenames, no argv/expected leakage to the reader. `documents_ok` gates the pass; SOURCES.md S103/S104 rows present exactly once (lines 109-110).

## Residual risk and verification gaps

- `--findings` byte equality with `decision-table.json` was not verified (execution is out of scope for this seat); content equality was verified field-by-field instead.
- The 11 `string_table {offset,size}` bindings are validated by the counter only structurally (bounds + expected names present in the region); confirming each points at the carrier's actual `sh_link` strtab requires parsing carrier ELFs, which this prose audit does not do. Misbinding cannot produce a false pass (see counter analysis), and bounded control runs are the assigned falsifier.
- `freeze-integrity.py` and `author_expected.py` were checked at digest and registry-contract level, not line-by-line.
- F1-F4 live in frozen artifacts (table JSON, reader FINDINGS literals, knowledge entry); under the freeze discipline they are reportable observations, not in-wave repairs — no predicate, target, or counter change is recommended.
- No tools were installed or upgraded for this item; no fixes applied; sandbox left clean, no processes started.

Addendum (post-review, parent IRC): R34-C1 is stopped under the original kill rule on an actual
false accept, not a generic stop: a structure-blind size/fixed-slice replay reader (no verneed
decoding — carrier size plus fixed-offset slices) scored 12/12 matched on both schedules at the
same frozen counter (`--control-reader` at freeze `54a87a51…`, instruments `8897a67f…`), i.e. the
counter's opaque-path/random-name and two-schedule design does not discriminate a reader that
ignores version-needs structure; Main approved no production run. The findings above are
unaffected: they describe the frozen table/entry/code content only and are retained as
observation; no frozen-document repair or predicate amendment is made or proposed.

Report: .ufo/waves/round-34/w1/RevDecisionTable.md
