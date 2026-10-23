# ConnectorSiblingBoundary — round 34 depth boundary audit

Axes named: kaidoku owned `coverage`, `depth`, `calibration` (all tied at 10.0, none retired); fleet axes touched only as evidence: `freshness`, `operability`, `adjacency`. Sibling revenger province owns runtime REA evidence and is not absorbed into kaidoku's depth claim.

## Evidence inspected (read-only)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/claims.json` (freeze 54a87a51a865ab931fd355e767303337b05cccf4; instruments 8897a67f6074580d6eac1a3fc0e37fdcd7aa0df0)
- `tools/round-34/version-needs-counter.py`, `tools/round-34/elf-version-needs.py`, `tools/round-34/freeze-integrity.py`
- `.ufo/waves/round-34/prep/R34Overlap.md`, `R34SourceNovelty.md`, `R34Corrections.md`, `R34LegacyGaps.md`
- `corpus/knowledge/2026-10-23-r34-elf-version-needs.md`, `.ufo/waves/round-34/approved-skill-section.txt`
- `PROVINCE.md` (Core: native ELF via Ghidra; host fallback readers `readelf`, `objdump`, `llvm-readobj`)
- `/home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md` (sibling province scope)
- `corpus/lessons/round-29.md`, `round-32.md`, `round-32-verifier-spotcheck.md`, `round-33.md`, `round-33-verifier-spotcheck.md`
- `corpus/SOURCES.md` rows S103–S105

## Frozen depth surface versus sibling province and Core ELF methods
- R34-C1 is a **depth** claim only: a sourced GNU Verneed/Vernaux decision table plus a bounded static reader on already-owned ELF ground. It is not coverage, a new REA verb, a new host artifact class, or a PROVINCE Core row.
- Native ELF is already owned in kaidoku's province (`PROVINCE.md` Core: native ELF via Ghidra plus host fallback readers). The reader is a local, single-process, stdlib-only static decoder; it does not replace or widen `readelf`/`objdump`/`llvm-readobj`/Ghidra. No REA runtime capability is acquired or claimed.
- The sibling revenger province owns reverse-engineering runtime evidence and REA tooling. Per kaidoku's cross-lane registry note, province map entries are live state only and never stand for a sibling lane's current runtime capability. R34-C1 must not import, imply, or reuse revenger runtime evidence.
- The counter's two schedules (original bytes, then a private same-length ASCII permutation of the linked string table under opaque paths) test parser fidelity only. The transformed copy is explicitly not a loader-valid image.

## Connections to r29/r32/r33 mistakes
- **r29 (carrier provenance / freeze hygiene):** R29-C1 rest on author-selected interface lists rather than opened sources; freeze ledger disagreed with its gate; an unpinned script was named in claim text. R34 avoids these by binding 12 existing public host binaries in `expected.json` with size/SHA-256, pinning all instruments in `claims.json`, and requiring no new binary fixtures or held-builder outputs.
- **r32 (metadata-only forged tags; lexical shortcuts):** R32-C2 accepted explicit denial and word bags; CHPE metadata-only classification accepted forged tags. R34 counters require byte-derived fields, offsets, section ranges, and two schedules, so filename/id/hash/constant/word-bag shortcuts must fail the randomized schedule.
- **r33 (unprovable depth; held builder):** R33-C1 stopped because no admissible independent manifest existed and quarantined builder outputs could not be used. R34's manifest is independently authored and frozen before data; U064N008Hf47eb933 and R33FixtureBuilder derivatives remain held/untouched/excluded.
- **r33 report hygiene:** the non-author spot-check found SKILL changed while the report said unchanged, while PROVINCE was unchanged. R34's approved skill section is an explicit, bounded addition; PROVINCE Core should remain unchanged for this claim.

## Unsupported coverage/capability/runtime inferences identified
1. An empty `needed` list for a supported sectioned image with no `SHT_GNU_verneed` is **section-scope absence only**, not proof of no dynamic-only requirement (`DT_VERNEED`/`DT_VERNEEDNUM`) and not loader acceptance.
2. The reader's ELF64 LE x86_64/AArch64, ET_EXEC/ET_DYN, OSABI 0/3, one-verneed-section profile is a **conservative local scope**, not universal ELF validity. AArch64 and ET_EXEC branches were not exercised by the development public-library selftest.
3. Malformed/unsupported findings are **local reader findings**, not host-loader verdicts; AST/selftest coverage does not demonstrate every malformed ELF branch.
4. `vna_other` is retained as a raw 16-bit value including bit 15; S104's stale `Unused` comment is not adopted. This is a recorded field, not an interpretation of runtime version selection.
5. `vna_hash` is recorded metadata; the reader never recomputes or authenticates it. Equality of hashes is not consistency or authenticity evidence.
6. Section type/link, not section name, drives decoding; section names are not required.
7. The randomized second schedule is a **benign static decoding challenge**, not a claimed loader-valid image. It defeats replay shortcuts but does not prove absence of all adversarial inference.
8. The counter passing target=12 means finite pinned carriers matched independent records and pinned source text was retained; it does not prove universal parser correctness, authenticity, or runtime behavior.
9. Helper/AST selftests and positive public-carrier comparisons are different evidence classes and do not substitute for each other.
10. No new Core row, coverage-map row, or REA capability should be added merely because the table was measured.

## Proposed move (bounded)
Retain R34-C1 strictly as a depth claim: add the approved GNU ELF version-requirements decision table to SKILL and knowledge as section-derived metadata on already-owned ELF ground, keep the local static reader as a non-REA, non-runtime decoder, and leave PROVINCE Core and coverage unchanged. Synthesize the round's proposals by requiring byte-derived offsets/hashes in every matched record, opaque paths, two schedules, no held-builder reuse, no binary fixture authoring, and append-only correction of any report overstatement. This improves depth while harming no owned axis and adding no coverage/capability/runtime claim.

## Risks
- Low dependency diversity among host binaries may test parser fidelity more than version diversity; acceptable only if framed as metadata fidelity, not coverage.
- 64-bit-only scope; no claim for ELF32, big-endian, other architectures, or non-GNU toolchains.
- Source drift: S103/S104 pins and carrier hashes must be rechecked before admission.
- Expected-output circularity remains possible if byte offsets/hashes are not required; the counter's controls are the mitigation.
- Overreach risk if any prose implies runtime loader acceptance, selected dependency, symbol resolution, or authenticity.

## Verification (main agent; not executed here)
- Re-run read-only freeze integrity over the frozen claims and pins.
- Confirm `PROVINCE.md` unchanged versus base and SKILL section equals approved text.
- Confirm all 32 control seats' receipts show expected failures before any production reader run.
- Confirm held exclusions U064N008Hf47eb933 and R33FixtureBuilder remain untouched.

## Factual correction (appended; no predicate change)

- **Current frozen condition:** the counter's canonical equality is only over `{"schema":1,"needed":[{"file":...,"versions":[{"name","flags","other","hash"}]}]}`. It does **not** compare byte offsets, section ranges, or parser-derived ranges inside each record.
- Input binding is by original carrier `size` + `sha256` plus the independently frozen `string_table` `{"offset","size"}`; the parser's bounds are implementation-side protections, not fields in the matched output.
- The randomized second schedule tests actual string-table decoding by changing dependency/version names while leaving raw `flags`, `other`, and `hash` unchanged; it does not make the claim forgery-proof or grant immunity to adversarial inference.
- Earlier wording in this report suggesting that counters "require byte-derived offsets/ranges in every matched record" is a suggested strengthening, not a current frozen condition. General expected-output circularity is mitigated by the controls, not solved by offsets.
- This correction does not propose amending the frozen predicate, target, counter, or manifest.


Report trailer: `.ufo/waves/round-34/w1/ConnectorSiblingBoundary.md` (relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`).