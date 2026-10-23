# RevGlibcTypes — S104 pinned glibc elf.h reopen (Kaidoku round 34, attempt 1)

Seat: reviewer `KaidokuR34.RevGlibcTypes`. Reviewed-at 2026-10-23 (final receipt 2026-10-23T10:58:02Z). Sandbox `/fast/scratch/hyaku/kaidoku-r34/w1/RevGlibcTypes` at freeze/base `54a87a51a865ab931fd355e767303337b05cccf4`, clean tree, separate clone/worktree. Assignment: reopen S104 (pinned glibc 2.42 `elf.h`, commit `d2097651cc57834dbfcaa102ddfacae0d86cfb66`), compare Half/Word widths, Elf64 structures, SHT_GNU_verneed constant and weak bit against the approved table; verify exact quote and pin. Scope honored: static metadata only — no parser run, no target binary execution, no runtime or malformed-input inference, no REA run.

## Verdict

**No defect found.** The pin is byte-exact, the quote is exact, every S104 line/range citation lands, and all four assigned comparison groups match the approved table exactly.

## Findings by severity

- Blocker: none.
- Major: none.
- Minor: none.
- Observations (non-defect): two, listed in §5.

## 1. Pin verification (byte-level, two hosts)

- `claims.json` `frozen_inputs` pin for `.ufo/waves/round-34/prep/R34SourceNovelty-files/glibc-elf.h` is `sha256 fd6e7f3e3c74ee9d64b9f92ce3cc31b34413ca2622a167320ea053ce9a68110f`. Recomputed over the lane production copy and the frozen sandbox copy: both equal the pin; lane↔sandbox `cmp` clean. The frozen SOURCES row, round-34 lesson, and knowledge header all repeat the same digest — consistent.
- Fresh re-fetch of the exact pinned URL `https://raw.githubusercontent.com/bminor/glibc/d2097651cc57834dbfcaa102ddfacae0d86cfb66/elf/elf.h` (exit 0): `sha256 fd6e7f3e…68110f`, 195,524 bytes, `cmp` byte-identical to the capture. The capture is an unmodified copy of the pinned commit's bytes, so all capture-relative line numbers are commit-exact.
- `git ls-remote` tag peel on **both** `github.com/bminor/glibc` and `sourceware.org/git/glibc`: `refs/tags/glibc-2.42^{}` = `d2097651cc57834dbfcaa102ddfacae0d86cfb66`. The pin is the glibc-2.42 release commit; the "glibc 2.42" label is exact, and two hosts agree.
- Frozen-tree integrity spot-check: sandbox `approved-skill-section.txt` = `c156effc825c46930bc08309888102a47e7011c5b589a453dceb2e961c8d2ba6` and sandbox `corpus/knowledge/2026-10-23-r34-elf-version-needs.md` = `d721189c9df0a267c22dd566d488deb3c19e3b1365f1e1f8cfaf0ba2092aa639`, both equal to `claims.json` `documents`.
- Live `SKILL.md` (frozen tree, lines 1158–1184) carries the approved table verbatim — heading, intro, 8 table rows, error-patterns paragraph, checklist 1–5. No drift between approved text and shipped SKILL section.

## 2. Exact quote

Capture line 459 (single occurrence of `SHT_GNU_verneed` in the header, confirmed by grep):

```
#define SHT_GNU_verneed	  0x6ffffffe	/* Version needs section.  */
```

The lesson's quote “Version needs section.” (3 words) is exact and contiguous; the comment carries two trailing spaces inside the `/* */` delimiters, which the quote does not misrepresent. Citation `S104:459` is exact.

## 3. Assigned comparison groups — approved table vs pinned capture

| Group | Approved-table claim | Pinned capture evidence | Result |
|---|---|---|---|
| Half/Word widths | "Half/Word widths are 16/32 bits, not pointer-sized" (Decode Verneed row; knowledge "Scalar widths" cites S104 28/33) | line 28 `typedef uint16_t Elf64_Half;`; line 33 `typedef uint32_t Elf64_Word;` — fixed-width typedefs, no pointer-sized definition | MATCH (lines and types exact) |
| Elf64 Verneed structure | 16 bytes, `<HHIII`, `vn_version` +0, `vn_cnt` +2, `vn_file` +4, `vn_aux` +8, `vn_next` +12; current version 1 (cited S104:1124–1138) | `Elf64_Verneed` 1124–1133: Half vn_version, Half vn_cnt, Word vn_file, Word vn_aux, Word vn_next = 2+2+4+4+4 = 16; `VER_NEED_CURRENT 1` at line 1138 | MATCH (offsets and size arithmetic exact) |
| Elf64 Vernaux structure | 16 bytes, `<IHHII`, hash +0, flags +4, other +6, name +8, next +12 (cited S104:1153–1161) | `Elf64_Vernaux` 1153–1161: Word vna_hash, Half vna_flags, Half vna_other, Word vna_name, Word vna_next = 4+2+2+4+4 = 16 | MATCH (offsets and size arithmetic exact) |
| SHT_GNU_verneed constant | `0x6ffffffe` (cited S104:459) | line 459 value `0x6ffffffe` | MATCH |
| weak bit | "Weak flag bit is `0x2`" (Preserve meaning row; knowledge cites S104 `VER_FLG_WEAK`) | line 1085–1086 `#define VER_FLG_WEAK	0x2	/* Weak version identifier.  Also used by vna_flags below.  */` | MATCH — and the header itself binds 0x2 to `vna_flags`, exactly the table's use |
| Elf64 structures ("Apply the local profile" row: 64-byte ELF/section headers) | 64-byte ELF header and section header | `Elf64_Ehdr` 81–97: 16 (`EI_NIDENT`, line 61) + 2+2+4+8+8+8+4+2+2+2+2+2+2 = 64 (Addr/Off = `uint64_t`, lines 43/46); `Elf64_Shdr` 397–409: 4+4+8+8+8+8+4+4+8+8 = 64 | MATCH |

## 4. Line-citation audit (every S104 range cited in reviewed artifacts)

| Citation | Content at that location in capture | Result |
|---|---|---|
| SOURCES row / knowledge header: `28-33` | Elf64_Half 28, Elf64_Word 33 | exact |
| `459` | SHT_GNU_verneed 0x6ffffffe + "Version needs section." | exact |
| `1124-1138` (Verneed) | Elf64_Verneed 1124–1133 plus VER_NEED_NONE/CURRENT 1137–1138 | exact |
| knowledge `1128-1129` (vn_file) | `Elf64_Word vn_file;` 1128 + comment 1129 | exact |
| Follow links `1130-1132` | vn_aux 1130, vn_next 1131, comment 1132 | exact |
| `1153-1161` (Vernaux) | Elf64_Vernaux exactly, typedef → `} Elf64_Vernaux;` | exact |
| Follow links `1158-1160` | vna_name 1158, vna_next 1159, comment 1160 (vna_next inside range) | exact |
| knowledge `1127-1132`, `1158-1160` (relative offsets) | contains vn_aux/vn_next 1130–1131 and vna_next 1159 | exact |
| lesson "lines 1124–1133 and 1153–1161 define the two structures" | both struct spans land exactly | exact |
| lesson "`Elf64_Half`/`Word` are uint16/uint32 at lines 28/33" | lines 28/33 | exact |

## 5. Scope discipline and observations

- The stale `/* Unused */` comment on `vna_other` genuinely exists in the pin (line 1147 Elf32 twin, line 1157 Elf64). The approved table and knowledge entry explicitly refuse to adopt it (S103 line 937 supplies the version-identifier meaning instead). The rejection is of real text, not a strawman — correct handling.
- No reviewed S104-bound sentence makes a runtime, loader-behavior, authenticity, or malformed-input claim; widths, offsets, constants and the weak bit are stated as static field interpretation only.
- Observation 1 (non-defect): the weak-bit citation points at `VER_FLG_WEAK` (1085), whose own comment scopes it to `vna_flags`; the approved wording "dependency flag bitmask includes weak bit `0x2`" is precisely what the header supports. Recorded for the audit trail.
- Observation 2 (non-defect): the remaining approved rows (local profile, LIMITS caps, stop-boundary) cite reader code and S103, not S104; they are outside this item's reopened source and were not re-audited here.

## Residual risk and verification gaps

- This seat's blob re-fetch used the bminor mirror (single transport here); two-host tag-peel agreement plus the prep capture's independent (per receipts, sourceware-fetched) byte-identity gives two converging transports. Residual mirror risk is negligible but nonzero.
- The 2.42-vs-2.44 host-header equivalence claim in `prep/R34ElfReader.md` (15 macros, 4 struct field sequences) was **not** re-verified by this seat — outside assignment. The S104 pin is self-consistent regardless of the host header.
- Citations are capture-relative; any future re-pin to a different glibc commit shifts them. The knowledge doc's "reopen S103/S104 on source changes" rule covers this.
- No ELF fixture opened, no `readelf` probe, no counter/reader/selftest executed — by assignment; runtime and behavioral validity remain unclaimed and untested here.

## Evidence

- Receipts: `.ufo/waves/round-34/w1/RevGlibcTypes-files/pin-verification-receipts.txt` (exact argv, exits, stdout, hashes, both-host tag peels, line-number table).
- Byte receipt: `.ufo/waves/round-34/w1/RevGlibcTypes-files/upstream-refetch-elf.h` (sha256 `fd6e7f3e…68110f`, 195,524 bytes, byte-identical to the frozen capture).
- Tooling: no tool installed or upgraded (curl, git, coreutils sufficient).

Report trailer: KaidokuR34.RevGlibcTypes, 2026-10-23; all paths relative to lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
