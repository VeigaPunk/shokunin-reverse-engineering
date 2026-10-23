# Round 32 attempt-2 — A2SiblingOverlap sibling overlap audit

**UTC:** 2026-10-23T06:55:56Z
**Axes:** R32-C1 coverage (ARM64X hybrid PE, Frontier → Core); R32-C2 calibration (Capabilities summary vs pinned non-author closure).
**Scope:** read-only lane production files. No product, doc, index, Git, or jj state changed. Scratch: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2SiblingOverlap`.

## Sibling surfaces inspected

| File | SHA-256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md` | `c167827aa47405e51fa14891a52d0d2c2346c069e4a6151e40add67d2b3e8c4c` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md` | `3290ad6fd61e1a3dbc7a6e84bdfa862d80cbaf504216f90097426383f630f0bc` |
| `/home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md` | `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f` |
| `/home/vgpnk/Projects/shokunin/revenger-shokunin/.ufo/waves/kaika-r1/connector.md` | `59e63d40d93cbf82029a58150131c44f171ca3e65ebd234d38d10f9080dbd09d` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json` | `8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims-v3.json` | `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d` |

## Overlap 1 — ARM64X hybrid PE / CHPE code map

- Kaidoku owns the PE subtype reader-coverage surface. At the frozen base, `PROVINCE.md:83` (under `## Frontier`) reads: “Reserve: ARM64X hybrids (the 91MB Godot ARM64 template is held, arc2-r7).” `SKILL.md:48` lists “PE x86-64 / ARM64 | `rea analyze` (Ghidra PeLoader, wine-free) | held (cli-64, cli-arm64).” C1 proposes moving ARM64X hybrid PE into Core through REA 6.5.0 `inspect` `binary_overview` coverage on author-built carriers.
- Revenger owns reverse engineering of shipped artifacts, including PE format-level evidence. `revenger-shokunin/PROVINCE.md` states its domain is “reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence.” `revenger-shokunin/.ufo/waves/kaika-r1/connector.md:111` cites S028 (LIEF, ARM64EC/ARM64X PE support) as authoritative for “PE dynamic relocations, CHPE metadata, and exception-directory structure” and marks it “relevant to Revenger's C01 PE format frontier.”
- Contested scope: both lanes touch ARM64X PE. Kaidoku's C1 claim is reader-coverage (`binary_overview`, ordered segments, segment/procedure counts) on pinned author-built DLLs; revenger's touch is format-level reverse engineering of shipped PE artifacts, including CHPE metadata. Neither claim, as frozen, subsumes the other.
- Boundary: kaidoku must not absorb build-tool or PE-format maintenance. `tools/round-32/build-arm64x-carriers.sh` and the LLVM `loadconfig-arm64*.s` inputs are frozen fixture-generation inputs for C1, not a general PE build tool or format authority. Kaidoku may read revenger's PE artifacts, but does not own PE format reverse engineering.

## Overlap 2 — Capabilities summary calibration

- Kaidoku owns `SCORECARD.md` `## Capabilities` calibration against the outside closure record (fleet `MANIFEST.json` `capabilities_added` for kaidoku). C2 target: `statements=4 match=4 target=4 reverse_mismatch=0, exit 0`, with anchors frozen in `claims-v3.json`.
- No inspected sibling PROVINCE/SKILL claims a `## Capabilities` summary or capabilities-summary calibration surface. Kagi owns a different calibration surface: `kagi-shokunin/PROVINCE.md:52` documents `corpus/claim-ledger.sh` as a “calibration gate” over claim rows and revision stamps. That gate is not kaidoku's repertoire table and does not check kaidoku's `## Capabilities` rows.
- Contested scope: none observed beyond the general sibling-overlap census. Kaidoku's C2 is calibration of its own self-declared repertoire against a non-author closure record; kagi's claim ledger is calibration of claim metadata. They are distinct surfaces and neither absorbs the other.
- Boundary: kaidoku reads sibling calibration methods as evidence only; it does not absorb kagi's gate ownership or build-tool maintenance.

## Independent claim separability

- C1 and C2 are independent axes, counters, predicates, targets, and tools. C1 is frozen in `claims.json` (`tools/round-32/c1-arm64x-positive.py`); C2 v3 is frozen in `claims-v3.json` (`tools/round-32/c2-capability-calibration-v3.py`). `claims-v3.json` supersedes C2 only; C1 is unchanged. Shared inputs are only the base revision and fleet pin.
- C1 separability: oracle ARM64X/CHPE classification, REA 6.5.0 envelope field equality, frozen prediction equality, committed-vs-live envelope comparison, and the two doc gates (`entry_ok`, `province_ok`) are distinct checks. Build-tool fixture generation is outside the capability claim.
- C2 separability: the four capability statements (rounds 13, 14, 17, 27) are independently matchable by frozen key pattern, single-round last cell, anchor-path presence, and 5-word description overlap; the reverse-mismatch check is independent.
- Sibling overlap does not alter either claim's separability: revenger's PE format frontier and kagi's claim ledger are separate surfaces and do not provide shortcuts to C1 or C2 targets.

## No actions taken

No lane production files, docs, indices, Git, or jj state were edited. No counters, predicates, carriers, or build tools were run. Only this report and the assigned scratch directory were written.

Report: `.ufo/waves/round-32/a2audit/A2SiblingOverlap.md`