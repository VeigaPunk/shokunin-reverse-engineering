# DRAFT registry row (for L1 to insert; NOT applied to corpus/SOURCES.md by this seat)

Insert after the S149 row (`corpus/SOURCES.md:155`), before the blank line at `:156`.
Verify: 11 cells, no `|` inside any cell, tier letter B.

| S150 | Freetz `squashfs4-host-be` patch 101, `AVM_BE`/`AVM_LE` symbols — https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch | code | B | the Freetz host-tool patch that defines the AVM target-format symbols and maps `AVM_LE` to little-endian byte order; a build patch from a third-party repack, not a description of AVM images | `+#define AVM_LE 2` (`:7`); the byte-order condition naming `SQUASHFS4_LE` or `AVM_LE` selects `__LITTLE_ENDIAN` (`:17`-`:18`); HTTP 200 on 2026-10-28 23:31:54Z, 1,153 B, sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707`; snapshot `.ufo/waves/round-50/w1/C1SrcFreetz/sources/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch` | Under its symbols-only name the patch adds the `AVM_LE` symbol and maps it to little-endian byte order and nothing else: no LE marker and no LE layout text. The marker write for `AVM_LE` is in patch 550 (a separate row, see the 550 draft); the shipped build compiles only `AVM_BE` (`squashfs4-host-be.mk:33`). | mined | 2026-10-28 | 180d | — |

## ID COLLISION (L1 decision required before insert)

`S150` is NOT free. Rounds 35, 36, 38, 39, 40, 43, 44, 45 cite `S150` for a rejected zenn.dev article
(quarantine, fabrication-class refuse). That candidate was never a row in `corpus/SOURCES.md`
(`git grep` at base `7c678ae` finds `S150` only in `corpus/lessons/*.md`). Reusing `S150` makes 239
historical citations point at a Freetz patch. Evidence: `git grep -c S150 7c678ae6d97aedb969fd253b52b3d2882ef1e186 -- corpus`;
`.ufo/waves/round-40/w1/artifacts/R40AssimE3/collision/staged-ids` and `.ufo/waves/round-41/w1/artifacts/R41Assim/assimilation/staged-ids`
list `S106..S237`-range staged ids that already collided with lane sources (`collision-documents.tsv`).
First id cited nowhere in the repo (scan of all files, `grep -rhoE '\bS[0-9]{3}\b' --exclude-dir=.git`): `S243`.
Recommendation: L1 chooses one of (a) `S243` (first unused id; breaks contiguity with S149 — state it in the lesson), or
(b) `S150` with the zenn quarantine id re-numbered in the lessons (a historical rewrite, not recommended).
This seat recommends (a). The row text above is unchanged apart from the id.
