# FEASIBILITY — a full table over the seven draft classes (NOT a shortcut control)

This file is evidence for the L1, not one of the six controls: it shows the stated grammar
plus the seven recon class signatures are jointly satisfiable, i.e. the draft P39-C2 is
achievable and the 10/14 ceiling of CTL-C2-6 is a control limit, not a grammar limit.
Every condition is taken from pre-freeze recon evidence (`class-signatures.json`).

The optional eighth class `no-squashfs-chunk` (probe `evidence/rea-trunc.json`,
`evidence/rea-badmagic.json`: H empty, G empty, P 0) needs exactly one extra row,
`handler = none`, and collides with no other class.

## Queue-drain craft

<!-- sqfs-triage-table v1 -->

| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|
| dep-missing-le | squashfs_v4_le | missing-extractor-dependency | sasquatch | * | * | * | install the LE extractor and rerun in a fresh outdir | SKILL.md 1235 |
| dep-missing-be | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | * | * | * | install sasquatch-v4be and rerun in a fresh outdir | round-38 before arms |
| avm-marker-be-dropped | squashfs_v4_be | extractor-failure | * | no | * | 0 | AVM marker dropped the -be token; do not record body damage | R38W2AvmProbe |
| body-extractor-failure | squashfs_v4_be | extractor-failure | * | yes | * | 0 | extractor ran with -be and failed on the body; carrier is damaged | dev rea-bodyfail.json |
| body-extractor-failure | squashfs_v4_le | extractor-failure | * | no | * | 0 | LE body damage runs with -le, which is not a -be token | dev rea-le-bodyfail.json |
| in-tree-symlink-metadata | * | unpublished-entry | * | * | * | * | symlink kept as metadata, not a failure | round-38 K2 after |
| escaping-symlink-removed | * | none | * | * | yes | >0 | escaping symlink removed, no gap, files still published | round-38 K1 after |
| clean | * | none | * | * | no | >0 | nothing to triage | round-38 K3 after |
| no-squashfs-chunk | none | * | * | * | * | * | no squashfs chunk detected; not a triage case | dev rea-trunc / rea-badmagic |

Scored on the seven class signatures: 14/14. The `no-squashfs-chunk` row matches no
seven-class fixture (all carry a chunk), so it does not change that score.
