# R34ElfReader — static GNU ELF version-needs reader and decision table

- **Seat:** `KaidokuR34.R34ElfReader` (UFO-FSD executor)
- **Base:** `ec3125ad3d130d92f888a4128dfaa2982f36fff7` (observed with `git rev-parse HEAD` at session start; this seat made no VCS writes)
- **Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **Output dir:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ElfReader-files/` (did not exist; created by this seat)
- **Execution UTC:** 2026-10-23T10:24Z–10:32Z (final artifact mtimes 10:31:42Z / 10:32:05Z)
- **Answering model:** `opencode-go/deepseek-v4.1-flash`
- **Scope:** static metadata interpretation only. No exploitation, vulnerability work, execution of inputs, malware, synthetic binary construction, production-12 parsing or REA run. Held item `U064N008Hf47eb933` untouched; round-33 held builder outputs not recreated.

## 1. Artifacts

| File (absolute) | Bytes | sha256 |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ElfReader-files/reader.py` | 38,603 | `fb7e6a65a66469631206ad4a37eef091ad44598c9e1fe40aa487754202c45123` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ElfReader-files/decision-table.json` | 17,148 | `cc44ac7a1cbb267a3b1204e55f565be8df7fd80195998f2aec588b4bb58c7e92` |

`decision-table.json` is byte-identical to `reader.py --findings` output; a fresh pipe during evidence capture hashed to the same `cc44ac7a…b58c7e92`. No other lane file was created or edited; a probe-created `__pycache__/` was removed before final capture. All probes ran under `/fast/scratch/hyaku/kaidoku-r34/R34ElfReader/` and did not write to the lane.

## 2. Behavior and interface

- API: `parse(data: bytes) -> dict`, accepting bytes/bytearray/memoryview. Success shape is exactly
  `{"schema":1,"needed":[{"file":str,"versions":[{"name":str,"flags":int,"other":int,"hash":int}]}]}`.
- Canonical serialization: `json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=True)` plus one trailing newline by the CLI. `needed` is sorted by `file`; `versions` by `(name, other, flags, hash)` — `file`/`name`/`other` are primary as directed, the extra fields only break exact ties. Sorting compares Python strings whose code points are the raw bytes (Latin-1 decode), i.e. byte order.
- Rejection: `ElfError` with `.finding_id`, `.classification`, `.reason`, `.detail`. CLI prints
  `{"schema":1,"finding_id":…,"classification":…,"reason":…,"detail":…}` and exits `12` malformed / `11` unsupported / `13` io. Usage errors exit `2`; selftest failure exits `1`; success exits `0`.
- CLI: `reader.py PATH`; `reader.py --findings`; `reader.py --selftest [--binaries PATH…] [--no-oracle]`.
- Absent `.gnu.version_r` yields `{"needed":[],"schema":1}` with exit 0 (verified on `ld-linux`).
- Raw-field policy (per parent directive): `vna_hash` is read straight from the field and never recomputed compared; `vna_flags`/`vna_other` are emitted verbatim (no whitelist, no versym cross-check, bit 15 not masked); names are decoded as Latin-1 with no charset or GLIBC-pattern check. No hash function exists anywhere in the instrument.

## 3. Decision table — 37 declared findings

Composition: 23 `malformed`, 12 `unsupported`, 2 `io`; 26 anchored in the format sources (`format`), 11 declared profile bounds (`profile`). Stage counts: header 14, sections 1, verneed 7, entry 4, aux 3, strtab 1, strings 3, coverage 2, io 2. List order is the documented first-failure precedence. Every row carries `check`, `bound`, `bound_kind` and `anchor` in the JSON.

Sources used for anchors (all content-pinned):
`H` = `/usr/include/elf.h`, glibc `2.44+r50+g1848099f063e-1`, sha256 `c81533b751ce45e737d91c49a3a2ed5123b0dbc7006259a40ccb3904221847ca`;
`R` = binutils-2_47 `binutils/readelf.c`, sourceware `hb=binutils-2_47`, local copy sha256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`;
`L` = LSB 5.0.0 `LSB-Core-generic/symversion.html`, sha256 `982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91`.

Durable copies of `H`, `R` and `L` are retained for L1 commit under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ElfReader-files/` (see §6). `H` is the **host glibc 2.44 header, not S104's pinned glibc 2.42** (`d2097651cc57834dbfcaa102ddfacae0d86cfb66`, capture `R34SourceNovelty-files/glibc-elf.h`, sha256 `fd6e7f3e…68110f`). `elf-h-2.42-vs-2.44-comparison.txt` compares the two: all 15 referenced macros have identical values and all four Elf64 struct field sequences are identical; only `Elf64_Verneed`/`Elf64_Vernaux` line numbers shift by 2 in the host header (host 1126–1135 / 1155–1163; pinned 1124–1133 / 1153–1161), as do `VER_NEED_CURRENT` and the two `VER_FLG_*` lines.

| # | finding id | class | stage | exact bound | kind |
|---|---|---|---|---|---|
| 1 | `error.malformed.elf_header_bounds` | malformed | header | len(data) >= 64 | format |
| 2 | `error.malformed.elf_magic` | malformed | header | data[0:4] == b"\x7fELF" | format |
| 3 | `error.unsupported.elf_class` | unsupported | header | e_ident[EI_CLASS] == ELFCLASS64 (2) | format |
| 4 | `error.unsupported.elf_data` | unsupported | header | e_ident[EI_DATA] == ELFDATA2LSB (1) | format |
| 5 | `error.malformed.ident_version` | malformed | header | e_ident[EI_VERSION] == EV_CURRENT (1) | format |
| 6 | `error.unsupported.osabi` | unsupported | header | e_ident[EI_OSABI] in {0, 3} | format |
| 7 | `error.malformed.elf_version` | malformed | header | e_version == EV_CURRENT (1) | format |
| 8 | `error.unsupported.elf_type` | unsupported | header | e_type in {ET_EXEC (2), ET_DYN (3)} | format |
| 9 | `error.unsupported.machine` | unsupported | header | e_machine in {EM_X86_64 (62), EM_AARCH64 (183)} | format |
| 10 | `error.malformed.ehsize` | malformed | header | e_ehsize == 64 | format |
| 11 | `error.malformed.shentsize` | malformed | header | e_shentsize == 64 | format |
| 12 | `error.unsupported.no_section_table` | unsupported | header | e_shoff != 0 | profile |
| 13 | `error.unsupported.shnum_extended` | unsupported | header | e_shnum != 0 | profile |
| 14 | `error.malformed.shoff_bounds` | malformed | header | 64 <= e_shoff and e_shoff + e_shnum*64 <= len(data) | format |
| 15 | `error.malformed.sh0_type` | malformed | sections | section[0].sh_type == SHT_NULL (0) | format |
| 16 | `error.malformed.verneed_bounds` | malformed | verneed | sh_offset + sh_size <= len(data) | format |
| 17 | `error.unsupported.multiple_verneed` | unsupported | verneed | count(sh_type == SHT_GNU_verneed (0x6ffffffe)) <= 1 | profile |
| 18 | `error.malformed.verneed_link` | malformed | verneed | 1 <= sh_link < e_shnum | format |
| 19 | `error.malformed.verneed_link_type` | malformed | verneed | section[sh_link].sh_type == SHT_STRTAB (3) | format |
| 20 | `error.malformed.strtab_bounds` | malformed | strtab | link.sh_offset + link.sh_size <= len(data) | format |
| 21 | `error.malformed.verneed_count` | malformed | verneed | sh_info==0 => sh_size==0; sh_info>0 => sh_size>=16 and every entry fits | format |
| 22 | `error.unsupported.verneed_entries` | unsupported | verneed | sh_info <= 1024 | profile |
| 23 | `error.unsupported.verneed_bytes` | unsupported | verneed | sh_size <= 65536 | profile |
| 24 | `error.unsupported.verneed_revision` | unsupported | entry | vn_version == 1 | format |
| 25 | `error.malformed.verneed_align` | malformed | entry | offset % 4 == 0 for each verneed, vn_aux target and vna_next target | format |
| 26 | `error.malformed.verneed_next` | malformed | entry | last: vn_next==0; other: vn_next>=16, target>offset, target+16<=sh_size | format |
| 27 | `error.malformed.verneed_aux` | malformed | entry | vn_cnt==0 => vn_aux==0; vn_cnt>0 => 16<=vn_aux and vn_aux+16<=sh_size | format |
| 28 | `error.unsupported.aux_entries` | unsupported | aux | sum(vn_cnt) <= 4096 | profile |
| 29 | `error.malformed.aux_count` | malformed | aux | for each of vn_cnt entries: cursor+16 <= sh_size | format |
| 30 | `error.malformed.aux_next` | malformed | aux | last: vna_next==0; other: vna_next>=16, target>cursor, target+16<=sh_size | format |
| 31 | `error.malformed.strtab_offset` | malformed | strings | 0 <= offset < link.sh_size | format |
| 32 | `error.malformed.string_unterminated` | malformed | strings | b'\x00' exists in [offset, link.sh_size) | format |
| 33 | `error.malformed.string_too_long` | malformed | strings | end - start <= 1024 | profile |
| 34 | `error.malformed.verneed_overlap` | malformed | coverage | 16-byte spans are pairwise disjoint | profile |
| 35 | `error.malformed.verneed_unreferenced` | malformed | coverage | every byte not covered by a parsed span == 0x00 | profile |
| 36 | `error.io.read` | io | io | os.stat/os.open/read succeed | profile |
| 37 | `error.io.size` | io | io | file size <= 536870912 bytes | profile |

Exact constants: ELF64 header 64 bytes; section header 64 bytes; Verneed 16 bytes; Vernaux 16 bytes; `SHT_GNU_verneed` `0x6ffffffe`; `SHT_STRTAB` 3; `SHT_NULL` 0; ELFCLASS64 2; ELFDATA2LSB 1; EV_CURRENT 1; ET_EXEC 2; ET_DYN 3; EM_X86_64 62; EM_AARCH64 183; `vn_version` 1. Profile limits are in the JSON `limits` object: input 536,870,912 B; entries 1,024; section bytes 65,536; aux total 4,096; name bytes 1,024.

Deliberately ignored (documented in `decision-table.json .ignored`): `sh_entsize` of the verneed section (GNU ld writes 0; readelf walks `vn_cnt`/`vn_next` instead, `R:14042-14155`); flag/hash/index values; name charset/pattern; section names; program headers, `.gnu.version`, `.gnu.version_d`, dynamic entries. Structure semantics are anchored at `L` (vn_version, vn_cnt, vn_file, vn_aux, vn_next, vna_hash, vna_flags, vna_other, vna_name, vna_next) and the ELF64 layouts at `H:1128-1135,1157-1163`; readelf's permissive truncation behavior (which this reader intentionally turns into rejects) at `R:14020-14155`.

## 4. Retained evidence (all probes bounded and completed)

Scratch base: `/fast/scratch/hyaku/kaidoku-r34/R34ElfReader/`. Durable copies of every log in this section are retained for L1 commit in the seat output dir; see §6. No probe was rerun to create those copies.

Inputs were byte-exact private copies of already-built public libraries, not production targets:

| copy | bytes | sha256 |
|---|---|---|
| `pub/libz.so.1` | 108,560 | `6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9` |
| `pub/libgcc_s.so.1` | 182,512 | `e618cb9c90c2eb3a1dad1cfea5b6c1eebcf2e799ad805976f4ae47bdd61c716a` |
| `pub/liblzma.so.5` | 219,344 | `6e4dae5b099ec0e40a56beead2e51f858535aa794b5a8574a6723dfc1da8a3c1` |
| `pub/ld-linux-x86-64.so.2` | — | `f5e11cc62f8f2c24dff532982559f4303dba3b17e7450551372a88c8e7ea8757` |

### 4.1 Internal selftest

`timeout 120 python3 -I -B reader.py --selftest`, exit `0`, `checks=128 binaries=0`. Log: `selftest-internal.log`, sha256 `f82a116662703734b628f0c089dd38246229d5c88fb0b850e6895c51995a047b`. It asserts: table uniqueness/prefix/field/exit consistency; AST equality between literal `_fail` ids in the source and all 37 declared ids (no undefined and no unraised id); Latin-1 decode; empty/offset/unterminated/1,024-boundary/1,025-too-long string behavior; sort and exact canonical text; empty/short/non-ELF negative prefixes. No ELF image is constructed.

### 4.2 Outer selftest with readelf oracle

`timeout 180 python3 -I -B reader.py --selftest --binaries <four copies>`, exit `0`, `checks=140 binaries=4`. Log: `selftest-outer.log`, sha256 `b1626303f4de5fed248e177ec509dc7af6645ce8fb14ebe9677226969f458156`.

```
outer …/libz.so.1 files=1 versions=5 oracle=readelf triples=5 flags_checked=5
outer …/libgcc_s.so.1 files=2 versions=8 oracle=readelf triples=8 flags_checked=8
outer …/liblzma.so.5 files=1 versions=10 oracle=readelf triples=10 flags_checked=10
outer …/ld-linux-x86-64.so.2 files=0 versions=0 oracle=readelf triples=0 flags_checked=0
reader-selftest: PASS checks=140 binaries=4
```

The oracle comparison is a multiset of `(file, name, other)` built independently from `readelf -V --wide` (binutils 2.47) text; all 23 triples matched. Flags text (`none`/`BASE`/`WEAK`/`INFO`) was parsed separately and matched on all 23 rows; observed flags were all `none`. readelf does not print `vna_hash`, so the hash field is not oracle-checked. `ld-linux` (ET_DYN, no `.gnu.version_r`) exercises the absent-section path and produces exactly `{"needed":[],"schema":1}`.

### 4.3 Renamed-string compatibility probe (parent counter schedule)

`timeout 90 python3 -B mutprobe.py`, exit `0`; log sha256 `b729c42c5ff43aeace066dfe818da3dd66b97bb3cf001beb59fc61d3f7c8e47a`. The probe copied `libz.so.1`, located its `.gnu.version_r` link, renamed all six referenced file/version strings with same-length ASCII rotation inside `.dynstr`, parsed the derived copy, then deleted it. Result: `files 1 -> 1`, `versions 5 -> 5`, `rows_preserved_with_hash 5 / 5`, `mutprobe: PASS`; the derived copy (`mutated_sha256 932ac53ccf6a0f66a285ce7ec04f3ba42b33a69bc2717f81e35fa557cfa0574a`) was never executed and is removed. Sample: `{"file":"mjcd.tp.6","versions":[{"flags":0,"hash":110530964,"name":"HMJCD_2.14","other":21},…]}`.

### 4.4 CLI boundaries

- `reader.py /nonexistent/path` → exit `13`, stdout `{"classification":"io","detail":{"errno":2,…},"finding_id":"error.io.read","reason":"cannot stat input","schema":1}` (`cli-missing.json`, sha256 `2d4ba2929c322330f4253fc3bb336287f1cbb1b8d77fdd737c2502a94b838e94`).
- `reader.py --findings /tmp/x` → exit `2`, `reader.py: error: PATH is not accepted with --findings` (`cli-usage.err`, sha256 `0df4abd65601522a6ea746a6f9cae83106e199e60ea2681d61dd2761f8d751ae`).
- `reader.py PATH` success on a copy emits the canonical JSON on one line, exit `0` (exercised for all four inputs above).

### 4.5 Instrument-local defects found and fixed before final capture

1. The first too-long string selftest expected `string_too_long` where the remaining table ended inside the scan window; the correct identity there is `string_unterminated`. A separate 1,100-byte case now exercises `string_too_long`, and the 1,025-byte-at-table-end case pins `string_unterminated`.
2. The readelf oracle regex initially omitted `0x`-prefixed offsets (readelf prints `000000` for zero and `0x0010` otherwise), yielding zero parsed rows; fixed before the final evidence run. No external harness errors and no safety refusals occurred.

## 5. Limits and risks

- **Profile, not universal ELF support.** Rejected by design and declared: non-ELF64, big-endian, non-x86_64/AArch64, ET_REL/ET_CORE/ET_NONE, OSABI outside {0,3}, absent section table, extended section numbering, more than one `SHT_GNU_verneed`, non-`SHT_STRTAB` link, nonzero unreferenced bytes, and overlapping entry spans. A host image with any of these would produce a declared reject where readelf might print partial output; the counter should compare only successful parses and treat declared rejects as out-of-profile.
- **Unexercised accept paths:** AArch64 and ET_EXEC have no public specimen in this probe set, so those accept branches are source-reviewed but not behaviorally evidenced. The structures are machine-independent, but this is `[INFERENCE]`, not measurement.
- **Unexercised negatives:** class/data/ident-version/OSABI/type/machine, overlap, unreferenced bytes, duplicate file names, multi-verneed, extended numbering and the entry/byte caps were not behaviorally tested, because ELF-image construction is prohibited; they are covered by the AST id-coverage check and by code review. Behavioral negatives were limited to empty/short/non-ELF prefixes and strtab helper blobs.
- **Hash:** emitted raw; no ELF-hash recomputation or comparison exists. readelf does not expose `vna_hash`, so the counter must source the expected hash from the raw field or another reader, not from readelf text.
- **Duplicates:** two verneed entries naming the same file are emitted as separate `needed[]` objects (stable sort preserves section order); they are not merged. No such specimen was exercised.
- **JSON presentation:** canonical output uses sorted keys, so `schema` appears after `needed`. Any comparator must parse JSON rather than require literal key order.
- **Bounds:** CLI refuses files over 512 MiB and one verneed section over 64 KiB; `parse()` itself has no size cap (caller-supplied bytes) and performs no I/O.
- No tools were installed or upgraded. Host tools used: Python 3.14.8, GNU readelf (binutils 2.47), x86_64 Linux. `eu-readelf` is present but was not needed.

## 6. Durable evidence retained for L1 commit

All files are in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ElfReader-files/`. Copies were made with `cp -p` after the observations; no selftest or probe was rerun for this section, and every copied artifact was sha256-verified equal to its source. This seat made no VCS writes; L1 owns the commit and will cite the landed line.

| Lane file | Bytes | sha256 | Origin |
|---|---|---|---|
| `selftest-internal.log` | 5,914 | `f82a116662703734b628f0c089dd38246229d5c88fb0b850e6895c51995a047b` | scratch log, identical bytes |
| `selftest-outer.log` | 7,413 | `b1626303f4de5fed248e177ec509dc7af6645ce8fb14ebe9677226969f458156` | scratch log, identical bytes |
| `rename-probe.log` | 407 | `b729c42c5ff43aeace066dfe818da3dd66b97bb3cf001beb59fc61d3f7c8e47a` | scratch `mutprobe.log`, identical bytes |
| `rename-probe.py` | 3,290 | `dfba3117a5560f56d30169dd2b4af4666fb746527325e92d96f9795edc704a9b` | scratch `mutprobe.py`, identical bytes |
| `readelf.c-binutils-2_47` | 689,644 | `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff` | sourceware `hb=binutils-2_47` |
| `elf.h-glibc-2.44` | 195,703 | `c81533b751ce45e737d91c49a3a2ed5123b0dbc7006259a40ccb3904221847ca` | `/usr/include/elf.h`, glibc 2.44 package |
| `lsb-symversion.html` | 19,109 | `982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91` | LSB 5.0.0 URL |
| `elf-h-2.42-vs-2.44-comparison.txt` | 2,850 | `d48a59d0b70861bd7be40fc3e609ed2d2a9b2f15803f9acae4e295d84407224d` | generated from S104 pinned capture + host copy |
| `capture-receipts.txt` | 6,093 | `72560dc99633f37157d699010937b3e23d45be9daba0db425c9e9f3779c2046e` | exact producing argv, exits and hashes |
| `development-binaries.tsv` | 1,226 | `f7b7c711dc78e3abb2d608f0e67720617f6466b53c2dfa77f87d5fb83c6e875b` | four development input digests |

The comparison result is `IDENTICAL-DEFINITIONS`: 15/15 referenced macros equal and 4/4 Elf64 struct field sequences equal between the host 2.44 header and S104's pinned 2.42 capture, with only the line-number shifts noted in §3. Source URLs, the failed GitHub-raw attempts, and the successful sourceware fetch argv are recorded in `capture-receipts.txt`.

Development binaries — private copies verified equal to their resolved `/usr/lib` targets and excluded from the production/expected-author list:

| Role | Resolved original | Bytes | sha256 |
|---|---|---|---|
| libz | `/usr/lib/libz.so.1.3.2` | 108,560 | `6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9` |
| libgcc_s | `/usr/lib/libgcc_s.so.1` | 182,512 | `e618cb9c90c2eb3a1dad1cfea5b6c1eebcf2e799ad805976f4ae47bdd61c716a` |
| liblzma | `/usr/lib/liblzma.so.5.8.4` | 219,344 | `6e4dae5b099ec0e40a56beead2e51f858535aa794b5a8574a6723dfc1da8a3c1` |
| ld-linux | `/usr/lib/ld-linux-x86-64.so.2` | 263,152 | `f5e11cc62f8f2c24dff532982559f4303dba3b17e7450551372a88c8e7ea8757` |

`development-binaries.tsv` carries full 64-hex digests for both the resolved originals and the private copies, with `production_expected=exclude-development-only`.

## 7. Verification for main agent

- `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ElfReader-files && timeout 120 python3 -I -B reader.py --selftest` → exit 0, ends `reader-selftest: PASS checks=128 binaries=0`.
- `timeout 180 python3 -I -B reader.py --selftest --binaries <private copies>` → exit 0, 140 checks, four `outer` lines as quoted in §4.2.
- `python3 -I -B reader.py --findings | sha256sum` → `cc44ac7a1cbb267a3b1204e55f565be8df7fd80195998f2aec588b4bb58c7e92`.
- Main owns the independent readelf-author manifest and must not treat this seat's oracle run as that counter. The production 12 and REA remain unrun by this seat, per directive.

Trailer: .ufo/waves/round-34/prep/R34ElfReader.md
