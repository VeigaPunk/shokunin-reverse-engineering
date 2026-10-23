# RevLSBLayout — S103 reopen: exact URL, captured bytes, field ordering, table references

Seat: `KaidokuR34.RevLSBLayout`. 2026-10-23. Sandbox `/fast/scratch/hyaku/kaidoku-r34/w1/RevLSBLayout` at freeze `54a87a51a865ab931fd355e767303337b05cccf4` (verified). Read-only prose review: grep/read/curl/sha256/diff only — the proposed parser `tools/round-34/elf-version-needs.py` and the counter were **not** run. No tool install. Answering model not visible in-seat; no refusal, no transport switch. Receipts: `.ufo/waves/round-34/w1/RevLSBLayout-files/receipts.md` plus byte-identical live refetches `lsb-live.html`, `glibc-live-elf.h`.

## Verdict

**AGREE — reopen closes with no material defect.** The exact external URL serves bytes identical to the frozen capture today; every Verneed/Vernaux/sh_link/vn_version statement in the frozen table traces to a precisely correct line in the capture; every frozen line citation (S103 and S104) pins exactly. Three informational nuances below; none is a misattribution.

## Findings

### High / Medium
None.

### Low / Info

1. **[INFO] Skill-section citation one line wider than needed.** `.ufo/waves/round-34/approved-skill-section.txt`, row "Follow links", cites `S104:1158–1160` for `vna_next` semantics. In the capture `vna_name` is line 1158 and `vna_next` spans 1159–1160. Over-inclusion only; no field is misattributed.
2. **[INFO] LSB's literal `vn_file` sentence is anomalous prose; the table's reading is an interpretation — a correct one.** Capture ~line 730: "Offset to the file name string in the section header, in bytes." (LSB never says "string table" for `vn_file`.) The frozen knowledge row reads "`vn_file` is an offset into the linked string table", attributed to S103 §10.7.4 **plus** S104:1128–1129 ("Offset of filename for this dependency") and anchored by the sh_link sentence at 615–640. That composite reading is the standard semantics and is what the independent readelf records encode. AGREE with the table; the ambiguity belongs to the LSB page, and the table sources around it honestly.
3. **[INFO] Record-relative base of `vn_aux`/`vna_next` is not verbatim in either source.** S103 says only "Offset to a corresponding entry in the vernaux array, in bytes."; glibc 1130/1131/1159 say "Offset in bytes to …". The table states "byte offset from the current Verneed/Vernaux" and self-labels the distinction ("Keep file/section-relative and record-relative offsets distinct"; the NUL/bounds check is called "a local conservative reader rule"). Correct call, correctly labeled.

## Verification detail (all exercised this session)

**1. Exact external URL and captured bytes — CONFIRMED.**
`https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/symversion.html` (verbatim in claims.json S103 row). Live refetch 2026-10-23T10:57:55Z: HTTP/2 200, etag `"4aa5-51682c5423837"`, last-modified `Wed, 20 May 2015 12:43:14 GMT`, 19109 bytes, sha256 `982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91` — **byte-identical** to `prep/R34SourceNovelty-files/lsb-symversion.html` and equal to the frozen hash in claims.json (`frozen_inputs`, `sources`, S103 row) and to the prep report's recorded etag/last-modified/size. Companion S104 refetch at pinned commit `d2097651cc57834dbfcaa102ddfacae0d86cfb66`: HTTP 200, 195524 bytes, sha256 `fd6e7f3e…68110f`, byte-identical.

**2. Verneed field ordering — CONFIRMED.** Capture 671–677 verbatim: `vn_version`(Half), `vn_cnt`(Half), `vn_file`(Word), `vn_aux`(Word), `vn_next`(Word) → table's 16 bytes, `<HHIII`, +0/+2/+4/+8/+12. glibc `Elf64_Verneed` 1124–1133 member order matches. AGREE.

**3. Vernaux field ordering — CONFIRMED.** Capture 839–845 verbatim: `vna_hash`(Word), `vna_flags`(Half), `vna_other`(Half), `vna_name`(Word), `vna_next`(Word) → table's 16 bytes, `<IHHII`, +0/+4/+6/+8/+12. glibc `Elf64_Vernaux` 1153–1161 matches. AGREE.

**4. Section `sh_link` meaning — CONFIRMED.** Capture 615–640 (sentence ends exactly at 640): sh_link "shall point to the section that contains the strings referenced by this section." Table: "use section `sh_link` to select its string table, not a guessed section name or a host path." AGREE. The numeric type `0x6ffffffe` is correctly attributed to S104:459, and `grep -c '0x'` over the whole LSB capture = **0** — S103 cannot teach the integer, so the split attribution is exact.

**5. `vn_version` quote and ≤25-word locator — CONFIRMED.** Quote at capture line 717, 21 words by `str.split()`: "Version of structure. This value is currently set to 1, and will be reset if the versioning implementation is incompatibly altered." Locator (7 words ≤ 25): "LSB 5.0.0 §10.7.4, capture lsb-symversion.html:717". Frozen paraphrase "current version 1" agrees; glibc `VER_NEED_CURRENT 1` at 1138 is consistent. Supporting Elfxx-prefix quote (capture 102–112, 20 words) validates reading the figures as `Elf64_*`.

**6. Frozen technical table references — every citation pins.**

| Frozen citation | Capture truth | Verdict |
|---|---|---|
| S103 `:615-640` (identity/sh_link, both docs) | paragraph 615→640 exact; heading §10.7.4 at 611-612 | exact |
| S103 `:671-677,717` (Verneed, vn_version) | typedef 671-677; quote 717 | exact |
| S103 `:839-845` (Vernaux) | typedef 839-845 | exact |
| S103 `:937` (`vna_other` identifier) | line 937, first sentence = identifier; bit-15 sentence separate | exact |
| S104 `:28/33` (Half/Word widths) | 28 `Elf64_Half uint16_t`; 33 `Elf64_Word uint32_t` | exact |
| S104 `:459` (`SHT_GNU_verneed 0x6ffffffe`) | line 459 | exact |
| S104 `:1124-1138` (Verneed + current 1) | struct 1124-1133; `VER_NEED_CURRENT 1` 1138 | exact |
| S104 `:1128-1129` (`vn_file`) | two-line comment on 1128-1129 | exact |
| S104 `:1130-1132` / `:1158-1160` (links) | 1130-1132 vn_aux/vn_next; 1158-1160 includes vna_name (info nit 1) | exact±1 |
| S104 `:1153-1161` (Vernaux) | struct 1153-1161; stale `vna_other /* Unused */` at 1157 | exact |
| S104 `VER_FLG_WEAK 0x2` | line 1085 | exact |
| Skill "local profile": caps 512MiB/1024/65536/4096/1024; errors + exits 11/12/13 | instrument `:75-80`, `:136-221`, `:229 EXIT_BY_CLASS = {"malformed": 12, "unsupported": 11, "io": 13}` | exact |
| Novelty claim `prep/R34SourceNovelty.md:7-23` (base mentions are inventories, not a table) | sweep/classification content sits in that range | exact |
| S105 reject `corpus/lessons/round-34.md` Gate | `## Gate` :19, S105 reject bullet :25, citing prep `:70-76` four-file zero-hit sweep | exact (internally; S105 reopen not this item) |

The frozen claims.json S103 row is a condensed form of the prep-proposed row with identical hash and anchors; the anchor set `:615-677,717,839-845,937` covers exactly the sh_link paragraph, the Verneed figure, the vn_version sentence, the Vernaux figure and the vna_other sentence. The predicate's "pinned source-backed decision table" is present in both frozen artifacts (knowledge `## Source-grounded decoding table`; skill section decision table).

## Residual risk and verification gaps

- Both captures are live-web artifacts: identical etag/last-modified today (2015-05-20 unchanged for LSB), but no long-term stability guarantee; the pinned glibc commit `d2097651…` protects S104. Named flip for the `Unused` rejection remains a later glibc comment or LSB errata on `vna_other`.
- Nuances 2–3 mean two field semantics (`vn_file` destination, link-offset base) rest on the standard interpretation cross-supported by S104 and the independent readelf records, not on verbatim LSB sentences. The independent manifest is the intended cross-check; I did not re-derive it (out of item).
- Parser/counter runtime behavior was verified only as declared constants (LIMITS, error names, EXIT_BY_CLASS); no execution, per assignment. Exit-code and finding emission at runtime is unverified by this seat.
- No verification of the counter's freeze arithmetic, carrier digests, or control behavior (other seats/items).
- No tool installs; pacman pause respected. Evidence argv/UTC retained in `RevLSBLayout-files/receipts.md`.

Report: .ufo/waves/round-34/w1/RevLSBLayout.md
