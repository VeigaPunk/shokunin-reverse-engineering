source: S103 — https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/symversion.html §10.7.4; S104 — https://raw.githubusercontent.com/bminor/glibc/d2097651cc57834dbfcaa102ddfacae0d86cfb66/elf/elf.h:28-33,459,1124-1161
verified-at: 2026-10-23; source captures and independent expected-author records in .ufo/waves/round-34/prep/; counter results are separately revision-bound in SCORECARD and the round lesson
recheck: python3 -I -B tools/round-34/version-needs-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze <immutable-freeze-revision> --rev <measured-commit>; reopen S103/S104 on source changes

# GNU ELF version-needs records: decode declared metadata, not runtime resolution

## Question and novelty

Which dependency files and version labels does an ELF image declare in its GNU version-needs section, and where do those fields come from? Native ELF reading was already held. The base's `.gnu.version_r` mentions are section inventory or `strings` output, not a Verneed/Vernaux decision table (`.ufo/waves/round-34/prep/R34SourceNovelty.md:7-23`). This is new technical detail on existing ground, not broader coverage or an acquired REA verb.

## Source-grounded decoding table

| Surface | Exact rule | Authority and scope |
|---|---|---|
| Section identity and strings | `.gnu.version_r` has type `SHT_GNU_verneed`; use section `sh_link` to select its string table, not a guessed section name or a host path. The numeric type is `0x6ffffffe`. | S103 capture lines 615–640; S104 line 459. The name is context, the type/link drive decoding. |
| Scalar widths | In the cited 64-bit structures, Half is uint16 and Word is uint32; both Verneed and Vernaux occupy 16 bytes. Little-endian local decoding uses `<HHIII` and `<IHHII`. | S104 lines 28/33,1124–1133,1153–1161; 16 is the sum `2+2+4+4+4` or `4+2+2+4+4`, not a 64-bit-pointer assumption. |
| Verneed field offsets | `vn_version` +0, `vn_cnt` +2, `vn_file` +4, `vn_aux` +8, `vn_next` +12. Current `vn_version` is 1. | S103 lines 671–677,717; S104 lines 1124–1138. |
| Dependency file | `vn_file` is an offset into the linked string table. Decode through the first NUL inside that table's recorded bounds. It is a dependency label, not a filesystem authenticity claim. | S103 §10.7.4; S104 lines 1128–1129. The bound check is a local conservative reader rule. |
| Auxiliary list | `vn_cnt` gives associated auxiliaries. `vn_aux` is a byte offset from the current Verneed to the auxiliary array; `vna_next` is a byte offset from the current Vernaux to the next. `vn_next` similarly advances from the current Verneed, not from file offset zero. | S103 §10.7.4; S104 lines 1127–1132,1158–1160. Keep file/section-relative and record-relative offsets distinct. |
| Vernaux field offsets | `vna_hash` +0, `vna_flags` +4, `vna_other` +6, `vna_name` +8, `vna_next` +12. Store raw hash/flags/other values rather than silently discarding bits. | S103 lines 839–845; S104 lines 1153–1161. |
| Version identifier | `vna_other` is the version identifier used by `.gnu.version`; raw bit 15 carries a hidden-bit meaning in S103. This reader retains the raw 16-bit value and does not map dynamic symbols to their version indices. | S103 line 937. S104's `/* Unused */` comment is not adopted as the field's meaning. |
| Hash and flags | The hash field is recorded metadata; the reader is not a name-hash authentication test. The dependency flag bitmask includes weak bit `0x2`; retaining other bits is not proof of their runtime interpretation. | S103 §10.7.4; S104 `VER_FLG_WEAK` and Vernaux definition. |
| Sectionless/unsupported layout | A section-table reader does not establish the absence of GNU requirements in a sectionless ELF. Dynamic `DT_VERNEED`/`DT_VERNEEDNUM` interpretation and per-symbol `.gnu.version` associations are outside this counter's canonical record. | S103 mentions DT_VERNEEDNUM; local scope is section-derived records only. An exclusion is not universal malformed-ELF proof. |

## Local reader profile and error discipline

The lane-owned parser is deliberately scoped to ELF64 little-endian x86_64/AArch64 section tables. Before dereferencing, it checks file and section bounds, section-link type, record spans/counts and NUL termination in the linked string table. A malformed/unsupported input produces a declared finding rather than a partial success record. A supported image with no version-needs section produces an empty `needed` list; that is section-scope absence only. Extended section numbering, ELF32, big-endian encoding, dynamic-only lookup, symbol-to-version mapping, loader policy and dependency satisfiability are not demonstrated by this study.

Canonical output is `{schema:1, needed:[{file, versions:[{name,flags,other,hash}]}]}`. Files are sorted by file label, auxiliaries by `(name,other)`. Sorting is a comparison convention, not original order or runtime precedence. The parser's own bounds tests and the round's positive public-carrier comparison are different evidence classes; neither silently substitutes for the other.

## Independent comparison and controls

The independent author uses GNU `readelf --version-info --wide` and section information on public, already-built host binaries; it does not import the parser. When readelf does not display a raw field, the expected-author record states the independent derivation. The immutable manifest binds original bytes by SHA-256 and size. No target is executed.

The counter runs its pinned reader over original bytes and a second, private same-length ASCII-permuted linked string table, both under opaque random filenames. The expected dependency/version names are transformed consistently and re-sorted; raw hash/flag/index fields remain recorded values. The transformed copy is a benign static decoding challenge, **not** a claimed loader-valid image. It defeats filename/id and original-SHA replay without rebuilding binary fixtures. Each score receipt retains the input digest and translation for its schedule; random permutations need not reproduce byte-for-byte across runs, while the equality predicate remains fixed.

A pass of the counter means the frozen finite set matched the independent records and the pinned source-backed text was retained. It does not prove that no malicious implementation could infer expected values, that the metadata is authentic, or that the reader handles inputs outside the named profile. Source/table semantic support is separately reviewed by reopened sources; a text hash alone is not a knowledge-quality judgment.

## Observation / inference / unknown

- **Observation:** captured source bytes, existing ELF bytes and GNU readelf output. Live counter receipts name their measured revision and every equality result; no unrun result is asserted here.
- **Inference:** the decoded fields represent the GNU requirement metadata defined by S103/S104; byte/record equality supports this bounded decoding interpretation.
- **Unknown:** runtime acceptance, actual library selected, symbol resolution, authenticity, code behavior, security significance, other ELF encodings and all metadata not included in the canonical record.

## Reject and follow-up boundary

S105, the opened System V gABI draft, is rejected as authority for these GNU-specific structures: the four fetched chapters do not name Verneed/Vernaux or `.gnu.version_r` (`corpus/lessons/round-34.md`, Gate). It remains useful generic ELF material, not an inferred GNU extension specification. The held round-33 builder and its outputs are not inputs to this entry, its parser or its counter.
