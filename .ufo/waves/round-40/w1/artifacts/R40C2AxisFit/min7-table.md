  <!-- sqfs-triage-table v1 -->
  | label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | no-squashfs-chunk | `none` | `*` | `*` | `*` | `*` | `*` | no chunk -> rerun | x |
  | dep-missing-be | `*` | `*` | `sasquatch-v4be` | `*` | `*` | `*` | dep -> PATH | x |
  | dep-missing-le | `*` | `*` | `sasquatch` | `*` | `*` | `*` | dep -> PATH | x |
  | avm-marker-be-dropped | `*` | `*` | `*` | `no` | `*` | `*` | marker -> wrapper | x |
  | body-extractor-failure | `*` | `*` | `*` | `yes` | `*` | `*` | damage -> keep stderr | x |
  | escaping-symlink-removed | `*` | `*` | `*` | `*` | `yes` | `*` | escape -> absent | x |
  | in-tree-symlink-metadata | `*` | `unpublished-entry` | `*` | `*` | `*` | `*` | kept -> one gap | x |
  | clean | `*` | `*` | `*` | `*` | `*` | `*` | nothing to fix -> none | x |

