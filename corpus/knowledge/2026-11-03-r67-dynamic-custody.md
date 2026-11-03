source: S271 https://gabi.xinuos.com/elf/08-dynamic.html sections8.3–8.4; S272 https://gabi.xinuos.com/elf/04-strtab.html; ELF4.3 DRAFT
verified-at: 2026-11-03; primary reading and development only until terminal closure
recheck: python3 -I -B tools/round-67/elf-needed.py --elf PATH

# Sectionless dependency declaration custody

[OBSERVATION] Prospective craft, not yet admitted. Sources: GABI chapter8 §8.3 https://gabi.xinuos.com/elf/08-dynamic.html and chapter4 https://gabi.xinuos.com/elf/04-strtab.html; owned reading notes in .ufo/waves/round-67/prep/source-notes.md. Prior work: round34's stopped section-link inference, and round66 LOAD span provenance.

## Analyst checklist

1. Treat DT_STRTAB as an address, DT_NEEDED as an index, DT_STRSZ as a size.
2. End tag interpretation at DT_NULL; retain needed-entry order.
3. Accept substring indices. Do not deduplicate occurrences or impose UTF-8.
4. Establish both dynamic-field and referenced-string byte custody. Equal bytes do not settle competing origins.
5. Find termination within the declared string-table bound, not merely within the file.
6. Report declared names only. Do not infer loaded files, authenticity or transitive closure.

## Conservative profile decisions

A bounded offline reader can reject zero-fill, gaps, or competing LOAD origins instead of simulating a loader. That is its evidence policy, not a proof that every actual loader rejects the artifact. Adjacent unique mappings may contribute different physical offsets to one string; report the pieces rather than pretending a single flat offset explains it. Validation of all declared table bytes is stronger than validating only the selected string. Whichever profile is selected must state this explicitly and freeze its refusal precedence.

[UNKNOWN] Runtime bindings, full ABI acceptance, authenticity, transitives and other ELF classes/endian forms are not established. Exact bounded contract: .ufo/waves/round-67/prep/independent-contract.md. It checks the entire declared dynamic extent including post-NULL padding and the whole STRSZ extent, then interprets only pre-NULL tags. Singleton table address/size tags are required, even with no needed entries, and duplicates refuse. These are local conservative profile choices.
