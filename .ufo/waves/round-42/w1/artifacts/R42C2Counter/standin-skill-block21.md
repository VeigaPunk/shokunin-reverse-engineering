## Queue-drain craft (stand-in fragment, dry-run only)

- **SquashFS outcome triage v4 (round 42, stand-in, amendment A1, 13 columns).** Reads only the
  `<!-- sqfs-triage-table v4 -->` block below; the round-41 v3 table is superseded. This block is a STAND-IN for
  the `R42C2TableDraft` seat's block 21 and exists so the round-42 C2 counter can be dry-run end to end.
  `handler` globs over F (any handler in F matches; `none` = F empty); `failing handler` globs over HF
  (handlers of the extractor-failure gaps; F when none carries one; `*` matches anything, including an empty HF).

  <!-- sqfs-triage-table v4 -->
  <!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty cross-read-legacy isolate-residue -->
  | label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | container-depth-limited | `extract_firmware` | `unblob` | `none` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | no SquashFS handler at this depth is not evidence of no SquashFS image: a SquashFS chunk may sit inside a container below the depth budget | A1 step 2 |
  | no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | F is empty and nothing was depth-limited: no SquashFS chunk of any major was carved (a v1-v3 chunk is a SquashFS chunk, so it never lands here) | A1 step 3 |
  | dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_be` | `*` | `missing-extractor-dependency+` | `sasquatch-v4be` | `*` | `*` | `*` | `install-extractor-be` | a v4 BE chunk resolved sasquatch-v4be and it was not on the child PATH | A1 step 4 |
  | dep-missing-le | `extract_firmware` | `unblob` | `*` | `*` | `missing-extractor-dependency+` | `sasquatch` | `*` | `*` | `*` | `install-extractor-le` | every v1-v3 chunk of either byte order and every v4 LE chunk resolves plain sasquatch | A1 step 4 |
  | partial-body-failure | `extract_firmware` | `unblob` | `*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `>0` | `salvage-partial` | the extractor failed after publishing at least one regular file | A1 step 5 |
  | avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_*` | `squashfs_v4_be` | `extractor-failure+` | `*` | `no` | `*` | `0` | `wrap-extractor-be` | a failing v4 BE chunk whose child argv carries no `-be` | A1 step 6 |
  | legacy-body-failure | `extract_firmware` | `unblob` | `squashfs_*` | `squashfs_v[123]*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `cross-read-legacy` | a v1-v3 body failed with zero files: no byte-order handshake or AVM pre-check applies, so cross-read it with unsquashfs | A1 step 7 |
  | body-extractor-failure | `extract_firmware` | `unblob` | `*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `preserve-failure` | a v4 body failed with zero files and no AVM marker reading | A1 step 8 |
  | unknown-residue | `extract_firmware` | `unblob` | `*` | `*` | `unknown-chunk-handler+` | `*` | `*` | `*` | `*` | `isolate-residue` | bytes beside the SquashFS chunk that no handler claimed; REA publishes them as a `.unknown` file | A1 step 9 |
  | depth-limited | `extract_firmware` | `unblob` | `*` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | REA stopped at max_depth over a SquashFS chunk | A1 step 10 |
  | mixed-symlinks | `extract_firmware` | `unblob` | `*` | `*` | `unpublished-entry+` | `*` | `*` | `yes` | `*` | `audit-symlinks` | both link kinds in one image | A1 step 11 |
  | escaping-symlink-removed | `extract_firmware` | `unblob` | `*` | `*` | `none` | `*` | `*` | `yes` | `*` | `expect-link-absent` | a link escaped the root and was removed with no gap | A1 step 12 |
  | in-tree-symlink-metadata | `extract_firmware` | `unblob` | `*` | `*` | `unpublished-entry` | `*` | `*` | `no` | `*` | `count-gap` | the gap set is exactly one kind: in-tree links kept as metadata | A1 step 13 |
  | clean | `extract_firmware` | `unblob` | `*` | `*` | `none` | `*` | `*` | `no` | `>0` | `none` | every regular file published, no gap, no removed link | A1 step 14 |
  | clean-empty | `extract_firmware` | `unblob` | `*` | `*` | `none` | `*` | `*` | `no` | `0` | `confirm-empty` | the tree holds no regular file | A1 step 14 |

## Next section (stand-in fragment)
