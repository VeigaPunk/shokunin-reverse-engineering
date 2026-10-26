# CTL-C2-6 — best table with no `-be` and no `MaliciousSymlinkRemoved` knowledge

The strongest shortcut available before the round-39 pre-freeze discoveries. Condition
cells for `-be in child argv` and `symlink removed` are forced to `*`; handler, gap kinds,
dependencies and published files are used fully.

Every row is grounded in round-38 recon: `dep-missing-be` and `dep-missing-le` differ in
handler and dependency name only (round-38 K1/K3/K4 `before.json`; dev `rea-dep-*-*.json`);
`unpublished-entry` marks the kept in-tree symlink (K2 `after.json`); `extractor-failure`
is the only gap kind left over.

## Queue-drain craft

<!-- sqfs-triage-table v1 -->

| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|
| dep-missing-le | squashfs_v4_le | missing-extractor-dependency | sasquatch | * | * | * | install the LE extractor and rerun in a fresh outdir | round-38 before arms |
| dep-missing-be | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | * | * | * | install sasquatch-v4be and rerun in a fresh outdir | round-38 before arms |
| in-tree-symlink-metadata | * | unpublished-entry | * | * | * | * | symlink kept as metadata, not a failure | round-38 K2 after |
| avm-marker-be-dropped | * | extractor-failure | * | * | * | * | extractor failed, treat as marker drop | R38W2AvmProbe |
| clean | * | none | * | * | * | >0 | nothing to triage | round-38 K3 after |

Prediction (N = 14): dep-missing-le 2, dep-missing-be 2, in-tree-symlink-metadata 2,
extractor-failure 2 (one of avm-marker-be-dropped / body-extractor-failure), `none` 2
(one of clean / escaping-symlink-removed). Total 10/14.

Why 10 is the ceiling for this shape: `clean` and `escaping-symlink-removed` share
H/G/D/BE/P and differ only in SR; `avm-marker-be-dropped` and `body-extractor-failure`
share H/G/D/SR/P and differ only in `-be` (verified: `evidence/rea-avm.json` vs
`evidence/rea-bodyfail.json`; the only feature difference is the standalone `-be` token).
A table without both features therefore loses two envelopes in each pair: 14 - 2 - 2 = 10.
