# CTL-C2-5 — the round-36 LE table transcribed into the triage grammar

Faithful transcription of `SKILL.md` lines 1231-1242 (the round-36 `### Decision table —
REA envelope signal to action`) into the six condition columns. The lane's prior holding is
LE-only: it knows the LE dependency gap (`dependencies = ["sasquatch"]`, `handler =
squashfs_v4_le`), unpublished-entry symlinks, and clean publication with regular files.
It knows nothing about the BE dependency name, the AVM marker, body failure, or escaping
symlink removal, so those cases fall through to `unclassified` or are absorbed by the
clean row.

Row mapping (round-36 table row -> grammar row):

1. `kind = missing-extractor-dependency`, `dependencies = ["sasquatch"]`, `handler =
   squashfs_v4_le` -> handler `squashfs_v4_le`, gap kinds `missing-extractor-dependency`,
   dependencies `sasquatch`, everything else `*`.
2. "No sasquatch gap, and every oracle regular file is present..." (recalled: 0 gaps) ->
   gap kinds `none`, published files `>0`. The oracle path/sha check has no condition
   column and is dropped; `published files >0` is its nearest expressible part.
3. `kind = unpublished-entry` (and/or `unpublished_entries[].kind = symlink`) -> gap kinds
   `unpublished-entry`.

Rows 4-8 of the round-36 table have no condition column here and are not transcribable:
before-arm opaque-container publication (no published-files-only reading), the AppImage
`elf64`-then-squashfs chunk layout (no chunk-range feature), file-count-exceeds-oracle (no
oracle feature), `operation`/`provider.id` binding (no such feature), and evidence-id
recomputation (no such feature). They are dropped, not approximated.

## Queue-drain craft

<!-- sqfs-triage-table v1 -->

| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|
| dep-missing-le | squashfs_v4_le | missing-extractor-dependency | sasquatch | * | * | * | install sasquatch on PATH and rerun in a fresh outdir | SKILL.md 1235 |
| clean | * | none | * | * | * | >0 | nothing to install, record both arms unchanged | SKILL.md 1236 |
| in-tree-symlink-metadata | * | unpublished-entry | * | * | * | * | symlink retained as metadata, do not claim it published | SKILL.md 1238 |

Prediction (N = 14): dep-missing-le 2 right; in-tree-symlink-metadata 2 right; clean 2
right plus 2 escaping-symlink-removed mislabelled `clean`; dep-missing-be,
avm-marker-be-dropped and body-extractor-failure are `unclassified` (6 wrong). Total 6/14.
