# Reviewer report — RevOtherMeaning (R34 w1, seat-r34-RevOtherMeaning)

Scope: wording review of raw `vna_other`, hidden-bit and hash phrasing in the new SKILL/knowledge versus S103 (LSB 5.0.0 §10.7.4) and S104 (glibc 2.42 `elf.h`) — whose `vna_other /* Unused */` comment conflicts with S103. Also: are version index, recorded hash and unknown loader truth kept separate? Source passages were reopened from the frozen captures at 54a87a51a865ab931fd355e767303337b05cccf4. Review only; no parser execution, no scoring, no production edits.

## 1. Source reopens (captured, digest-verified)

**S103 — `prep/R34SourceNovelty-files/lsb-symversion.html` (sha256 `982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91`, pin match).**

- Line 937 (the `vna_other` field description, full passage):
  > "Object file version identifier used in the .gnu.version symbol version array. Bit number 15 controls whether or not the object is hidden; if this bit is set, the object cannot be used and the static linker will ignore the symbol's presence in the object."
  First sentence = 11 words; second sentence (the hidden-bit part) is 26+ words, over the 25-word cap — matches the prep note in `R34SourceNovelty.md:45`.
- Line 717 (vn_version), verbatim: "Version of structure. This value is currently set to 1, and will be reset if the versioning implementation is incompatibly altered." (21 words — as quoted in the lesson.)
- Lines 615–627: `.gnu.version_r`, type `SHT_GNU_verneed`; number of entries "shall be contained in the `DT_VERNEEDNUM` entry".

**S104 — `prep/R34SourceNovelty-files/glibc-elf.h` (sha256 `fd6e7f3e3c74ee9d64b9f92ce3cc31b34413ca2622a167320ea053ce9a68110f`, pin match).**

- Lines 1147 / 1157: `Elf32_Half vna_other; /* Unused */` / `Elf64_Half vna_other; /* Unused */` — the conflicting comment exists exactly as described.
- Line 1085: `#define VER_FLG_WEAK 0x2 /* Weak version identifier. Also used by vna_flags below. */`.
- Lines 28/33: `typedef uint16_t Elf64_Half;` / `typedef uint32_t Elf64_Word;`.
- Line 459: `#define SHT_GNU_verneed 0x6ffffffe /* Version needs section. */`.
- Lines 1153–1161: `Elf64_Vernaux` = `Elf64_Word vna_hash; Elf64_Half vna_flags; Elf64_Half vna_other; Elf64_Word vna_name; Elf64_Word vna_next;`.

## 2. Wording verdicts (claim → source support)

| Claim (file, row) | Source passage | Verdict |
|---|---|---|
| "`vna_other` is the version identifier associated with `.gnu.version`" (SKILL 1168 / approved row 11) | S103:937 first sentence | Supported (mild paraphrase of "used in the .gnu.version symbol version array"; readelf.c 14310–14313 also matches `vna_other` against `.gnu.version` entries) |
| "raw bit 15 carries a hidden-bit meaning in S103" (knowledge row 21) | S103:937 second sentence | Supported; attribution to S103 is correct. Note: "hidden-bit" is the docs' coined paraphrase — LSB says "controls whether or not the object is hidden"; the consequence clause ("static linker will ignore…") is **not** imported, so no overclaim |
| "retain raw bit 15, flags and hash" (SKILL 1168) / "Store raw hash/flags/other values rather than silently discarding bits" (knowledge row 20) | reader emits `_u16` unmasked (reader.py 489/515; decision-table `ignored` list: emitted verbatim, no masking) | Supported |
| "Weak flag bit is `0x2`" (SKILL 1168; knowledge row 22) | S104:1085 `VER_FLG_WEAK 0x2` | Supported |
| "this reader does not authenticate the stored name hash or resolve symbols" (SKILL 1168); "the reader is not a name-hash authentication test" (knowledge row 22); "raw hash values remain recorded metadata, not consistency/authenticity evidence" (approved checklist 4) | instrument docstring: "vna_hash is emitted verbatim… never recomputes or compares a hash" and "does not resolve symbols" | Supported |
| "S104's `/* Unused */` comment is not adopted as the field's meaning" (knowledge row 21; lesson; claims/SOURCES S104 row) | S104:1147/1157 comment literally `Unused`; S103:937 defines the identifier | Supported — the conflict is real and the resolution is consistent |

No wording asserts anything beyond the two sources or the reader's actual behavior.

## 3. Are version index, recorded hash and unknown loader truth kept separate? Yes.

- **Version index** — meaning sourced only from S103:937; the reader never maps symbols to version indices (docstring lines 9–12; decision-table `ignored`: "no index/versym cross-check").
- **Recorded hash** — `vna_hash` is a verbatim field read (S104 layout); the separately authored expected record keeps its own SysV `elf_hash` cross-check as *author provenance*, not reader behavior (`prep/R34Expected-files/checks.json`: `sysv_hash_checked` 339, `sysv_hash_mismatches` [], `all_match` true — matches `R34Expected.md`'s "339 records, 0 mismatches").
- **Unknown loader truth** — knowledge rows 23 + "Unknown" section, and the SKILL "Stop rather than overclaim" row, hold DT_VERNEED/DT_VERNEEDNUM consistency, per-symbol associations, runtime selection and satisfiability as unknown. No claim conflates these with either the index meaning or the recorded hash.

## 4. Unsupported claims

None found that exceed the reopened sources or the reader's documented behavior. Precision notes (not defects):

1. "associated with `.gnu.version`" (SKILL) is looser than S103's "used in the `.gnu.version` symbol version array"; the readelf cross-reference supports it, so it is not unsupported.
2. "hidden-bit" is a coined term; its attribution is pinned to S103 in every occurrence (knowledge row 21; `R34SourceNovelty.md:45`). Keep that pin when copying the wording.
3. The frozen corpus does **not** exercise either source-grounded semantic: all 339 auxiliary records have `flags = 0` (no weak/base) and `other ∈ [2, 82]` with bit 15 never set. The docs already handle this honestly ("retaining other bits is not proof of their runtime interpretation"; "No weak flags observed" in the claim width).

## 5. Independent verification performed

- Both source-capture sha256 values match the claims/SOURCES pins (computed on the frozen tree).
- Both documents pinned in `claims.json` (`corpus/knowledge/2026-10-23-r34-elf-version-needs.md`, `.ufo/waves/round-34/approved-skill-section.txt`) match the on-disk bytes exactly.
- `claims.json` `source_rows` S103/S104 are byte-identical (mod-whitespace) to `corpus/SOURCES.md` rows 109/110.
- Frozen manifest width: 12 carriers, 107 needed records, 339 auxiliary records — matches the claim's `width`; `checks.json` `carrier_count` 12, `manifest_sha256` `f22e7e3b…` matches `claims.json` `manifest_sha256`.

## 6. Residual risk / verification gaps

- This is a read-only wording/source review: no production counter run, no parser scoring (pre-data boundary respected).
- The LSB "static linker" consequence sentence is untested by the corpus and untested by the reader; it is correctly not claimed anywhere — close the gap only with a dedicated probe if ever needed.
