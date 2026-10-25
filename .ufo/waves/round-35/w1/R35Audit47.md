# R35Audit47 — source tier authority

## Scope and method

Read-only assessment of source-tier authority relevant to frozen Round-35 C1 (`.jsc` → source mapping; S125/S129) and C2. No source, corpus, claim, counter, plan, VCS, or sibling path was modified. I read `plans/round-35-claims.md`, `.ufo/waves/round-35/claims-canonical.json`, `PROVINCE.md`, `corpus/SOURCES.md`, and `corpus/QUALITY.md`; no source fetch or runtime/tool probe was performed.

## Evidence

- `corpus/SOURCES.md` defines a registry column `tier`; its visible existing examples use A for official/specification/toolchain primary materials and B for community/open PR material. In particular, S032/S033 mark an open Ghidra PR B and narrowly limit what it supports. S099–S106 similarly scope A rows to specific official specifications or version-pinned source-code facts, not downstream behavior beyond their stated scope.
- `corpus/QUALITY.md:97` explicitly routes tier definitions, scope, and recheck policy to `corpus/SOURCES.md`, while claim admission separately follows QUALITY. This distinguishes source authority tier from whether a lane capability/claim is demonstrated.
- `PROVINCE.md:147-148` says `.jsc` disassembly is held, but a View8/jsc2js-style bytecode-to-source mapper remains Frontier. Thus upstream/project documentation may describe a mapper, but does not by itself establish that this lane's route works on typora's artifact.
- The plan names two shokuknow-package knowledge entries and requires new mined S125/S129 rows with `used-by` naming the matching entries. Those prospective rows and entries were absent from the SOURCES/knowledge inventory inspected; cannot assess their actual tier or source content yet.
- The canonical claims file identifies C1/C2 and frozen counters; it does not declare a tier override. Tier assignment therefore remains governed by SOURCES registry conventions and bounded source scope, not by the claim predicate.

## First falsification / limits

A plausible invalid inference would be “S125/S129 are tier A, therefore the lane's mapper works.” Tier A would only characterize the cited source's authority for its stated subject; it cannot alone falsify the explicit Frontier boundary or prove a successful lane probe. Conversely, assigning a source B solely because it is hosted by a community project would also need justification from the actual source and claim scope. Since S125/S129 have not landed in the inspected tree, no source-level tier verdict is possible.

No commands were run. Observations above are from the named files only; no network/live source authority, candidate capture integrity, tier policy outside SOURCES.md, mapper implementation, or measured C1/C2 result was tested. This is advisory evidence, not a predicate change or score.
