## CLAIM
Leg-5 receipts support a corpus knowledge entry for `inspect_electron_fuses` on one pinned Signal ELF, limited to static fuse-state observations and explicit provider limitations; they do not establish runtime behavior or justify Core promotion.

## METHOD
Read and compared the lane-A and lane-B saved leg-5 receipts against scout SC3, then checked the applicable admission criteria in `corpus/QUALITY.md`. No target probe, MCP call, network access, or independent re-hash was performed.

## FINDINGS
- Lane A records `rea-agents@6.5.0`, the CLI call, carrier path and SHA-256, full JSON result, and exit 0 (`.ufo/waves/luna-round-6/receipts/leg-5.md:3-12`). SC3 independently records the same path/hash and ELF/package markers (`.ufo/waves/luna-round-6/SC3.md:10-12`).
- Lane B records server 6.5.0 and the `inspect_electron_fuses` call (`receipts-B/leg-5.md:16,22,27-28`); its result has the same evidence ID, carrier digest, and nine fuse states. It explicitly classifies the frozen case `RESULT. MATCH` (`receipts-B/leg-5.md:48-52`).
- The sources support labeling reported fuse bytes as observations; runtime implications are derivations, not observed execution. Explicit unknowns include other Inspector-enabling paths and embedded ASAR enforcement (`receipts/leg-5.md:8`; `receipts-B/leg-5.md:28`). The evidence aligns with `corpus/QUALITY.md:11-20` when those limits and labels are preserved.

## THREATS
This is saved-receipt verification, not independent confirmation of provider semantics or current carrier bytes. Do not generalize the single Linux ELF result into application runtime behavior or cross-platform ASAR enforcement.

## VERDICT
CLEAN — sufficient pinned RESULT-class evidence for a narrowly scoped knowledge entry; not a Core promotion.
