# BOUND — no `-be` / no `MaliciousSymlinkRemoved` table if `no-squashfs-chunk` is added

Not a control for the seven draft classes. It records the ceiling the no-BE/no-SR shape
reaches if the L1 adopts the conditional eighth class `no-squashfs-chunk` (H empty, G
empty, P 0; probes `evidence/rea-trunc.json`, `evidence/rea-badmagic.json`). The
`no-squashfs-chunk` block is separable without either hidden feature because `handler:
none` is a condition column, so the ceiling rises from 10/16-shape to 12/16; it still
does not reach the target.

## Queue-drain craft

<!-- sqfs-triage-table v1 -->

| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|
| dep-missing-le | squashfs_v4_le | missing-extractor-dependency | sasquatch | * | * | * | install the LE extractor and rerun | round-38 before arms |
| dep-missing-be | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | * | * | * | install sasquatch-v4be and rerun | round-38 before arms |
| in-tree-symlink-metadata | * | unpublished-entry | * | * | * | * | symlink kept as metadata | round-38 K2 after |
| avm-marker-be-dropped | * | extractor-failure | * | * | * | * | extractor failed, treat as marker drop | R38W2AvmProbe |
| clean | * | none | * | * | * | >0 | nothing to triage | round-38 K3 after |
| no-squashfs-chunk | none | * | * | * | * | * | no squashfs chunk detected | dev trunc/badmagic probes |
